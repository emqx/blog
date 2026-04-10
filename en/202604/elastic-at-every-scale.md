> EMQX Tables Technical Series Part 3: How GreptimeDB scales from a single node to a distributed cluster without changing your architecture, your pipeline, or your database.

 

[EMQX Tables](https://www.emqx.com/en/cloud/emqx-tables) is a fully managed time-series database service built into EMQX Cloud. Among all the time-series databases available, EMQX Cloud chose GreptimeDB as the underlying engine.

[Part 2](https://greptime.com/blogs/2025-01-23-greptimedb-cloud-native-storage-engine) of this series covered how GreptimeDB cuts storage costs by 10x through decoupled compute and storage. But cost is only half the problem.

When your device fleet grows from thousands to millions, the bottleneck shifts. Storage is cheap, but can your database keep up with the writes? Can you add capacity without a weekend migration? And when a node goes down at 3 am, how quickly does data come back?

These are architecture questions, not tuning questions. GreptimeDB's answer starts with a three-component design.

## Three Components, One Separation of Concerns

A distributed GreptimeDB deployment has three core components.

- **Frontend** is the stateless access layer. It accepts client connections - SQL, PromQL, InfluxDB Line Protocol, OpenTelemetry - and handles query planning and routing. Because it holds no data, you can add or remove Frontend instances freely. Scaling write ingestion is as simple as adding more Frontend pods.
- **Datanode** is the storage and execution layer. It manages Regions (more on those in a moment), executes sub-queries, persists WAL, and flushes immutable data files to object storage. Each Datanode is independent; it doesn't know about other Datanodes.
- **Metasrv** is the control plane. It stores all metadata (catalogs, schemas, tables, Region locations) and makes scheduling decisions. Every Datanode sends heartbeats to Metasrv carrying load metrics: Region count, read/write capacity units, CPU, I/O. Metasrv uses this global view to coordinate Region placement and migration.

![967e658d9df885692335a2aa56534ba5.png](https://assets.emqx.com/images/94e9f2b71b4f72c93910b50e13729ae6.png)

Frontend caches routing tables locally and only contacts Metasrv on a cache miss, so the control plane stays out of the hot write path.

## Region: The Unit of Elasticity

The concept that makes everything else work is the **Region**.

Every table is horizontally partitioned into one or more Regions, each covering a contiguous range of data. Regions are distributed across Datanodes, and Metasrv can migrate, split, or merge them at any time based on load.

![95c5c49bae5aa59aaca1b9deb6d2d684.png](https://assets.emqx.com/images/60389d164e306f54670d1b96892c25b9.png)

*Regions of a single table, partitioned by* `device_id` *range and distributed across three Datanodes. A Datanode can also hold Regions from other tables.*

This matters for IoT because **migrating a Region is nearly free**.

In a traditional database, moving data between nodes means physically copying rows or pages: slow, expensive, and risky under load. In GreptimeDB, Region data already lives in object storage. S3 doesn't belong to any single Datanode. Migration is a metadata operation: Metasrv updates the routing table, the target Datanode opens the Region files it can already see, and the old Datanode closes them.

This is the difference between *elastic* and *"can scale with enough pain."* When a single IoT table receives millions of writes per day, and one Region becomes a hotspot, Metasrv splits it automatically. When a Datanode is overloaded, Regions migrate to idle nodes while writes keep flowing.

## Scale the Way Your Business Grows

Most databases force you to pick an architecture upfront and live with it. GreptimeDB doesn't. The same storage engine, the same wire protocols, the same SQL runs across three deployment tiers, and you move between them without rebuilding your pipeline.

### Standalone: Start Simple, Stay Reliable

A single GreptimeDB process handles everything. This is where most projects begin: development environments, small-scale production, proof-of-concept deployments.

Standalone isn't a toy. When configured with object storage, disaster recovery is genuinely solid. Back up to S3 with one command:

```shell
greptime cli data export \
    --addr localhost:4000 \
    --s3 \
    --s3-bucket my-backup-bucket \
    --s3-access-key <YOUR_ACCESS_KEY> \
    --s3-secret-key <YOUR_SECRET_KEY> \
    --s3-region us-east-1 \
    --s3-root greptimedb/backups
```

Because your data is already in object storage, backups are incremental and cheap: you're snapshotting metadata and flushed SST files, not copying a monolithic data directory. Restore is fast for the same reason. For scenarios where brief, planned downtime is acceptable, this is often all you need.

On cloud platforms, Standalone can go further. A primary instance and a standby share the same object storage backend; when the primary fails, the standby takes over without replicating any data. It simply opens the same files. This gives you automatic failover with near-zero recovery overhead.

### Active-Active Failover: HA Without Object Storage

Not every environment has object storage. Edge deployments, on-premise installations, and air-gapped networks often store data on local disks, which changes the HA calculus significantly.

GreptimeDB Enterprise's Active-Active Failover is designed for exactly this scenario: **two peer nodes, bidirectional write replication, no shared storage required**.

Both nodes serve reads and writes simultaneously. Neither is a fixed primary. Writes accepted by either node are asynchronously replicated to the peer, and GreptimeDB's architecture prevents circular replication, so you don't need to think about it.

![7f11b5b78f493b2ff888cb21af070302.png](https://assets.emqx.com/images/784de60e3459b80e4f9a3533eee135ed.png)

Queries run locally on whichever node the client connects to, no cross-node merge, no coordination overhead. If Node A goes down, Node B already has the data. Failover is handled by a load balancer or your client SDK's built-in failover configuration; GreptimeDB itself doesn't need a third node to orchestrate the switch.

**RPO is configurable.** By controlling how many pending writes can remain unreplicated, you tune the tradeoff between write throughput and read consistency across nodes. Set the threshold to zero, and asynchronous replication becomes effectively synchronous: RPO = 0.

Two nodes, straightforward operations, protection against single-node failures—and you can place nodes in different regions for geographic redundancy without adding architecture complexity. For most private-deployment IoT scenarios, this hits the right balance.

### Distributed Cluster: Horizontal Scale, No Ceiling

When data volume or write throughput genuinely requires horizontal scale (millions of devices, tens of thousands of writes per second), you run the full distributed mode.

Frontend instances scale independently for ingestion. Datanode instances scale for storage and query capacity. Regions distribute automatically across Datanodes as you add capacity.

Adding a Datanode triggers automatic Region rebalancing: Metasrv migrates Regions from loaded nodes to the new one. Because Region data lives in object storage, this happens with no downtime and no bulk data transfer across the network.

For deployments requiring cross-region disaster recovery, GreptimeDB supports a single cluster spanning multiple regions and data centers: Metasrv consensus across three regions, data replicated via remote WAL (Kafka) and object storage. RPO = 0, RTO in minutes. Topology options range from a 2-2-1 configuration (two active DCs, one replica) to full three-region active deployments.

## Fault Recovery: What Happens When a Node Goes Down

Fault recovery in GreptimeDB flows from one architectural fact: **durable state lives outside the compute nodes**.

Every write lands in two places before the client sees success: the WAL (local disk or a remote Kafka cluster) and the Datanode's in-memory MemTable. The MemTable eventually flushes to immutable SST files in object storage. The WAL truncates after each flush.

When a Datanode fails:

1. Heartbeats to Metasrv stop. Metasrv detects the failure.
2. Metasrv identifies which Regions were on the failed node.
3. Metasrv opens those Regions on other Datanodes; they can access the SST files in object storage immediately.
4. Each Region replays its WAL to recover writes that hadn't been flushed yet. With remote WAL (Kafka), this works even if the original node's local disk is unrecoverable.

For IoT workloads, the practical implication is that **individual device data streams are not lost**. Regions covering active devices recover and resume accepting writes. Recovery time depends on WAL replay volume, typically minutes.

Frontend failures are trivial. Stateless nodes carry no data, so clients simply reconnect to another instance. Metasrv itself runs as a leader-follower cluster backed by RDS or etcd, with a failure domain independent of the data path.

## One Architecture, Three Scales

The most underrated property of this design: **there is no hard migration path between tiers**.

Moving from Standalone to Active-Active Failover doesn't require exporting and reimporting data. Moving from Active-Active to a full Distributed Cluster doesn't require a schema migration or a rewritten pipeline. The same InfluxDB Line Protocol, the same SQL queries, and the same Grafana dashboards work across all three tiers.

This matters for IoT teams. Projects start small. If your database choice now locks you into a painful migration later, you pay that cost twice: once in engineering time, once in the delayed decision to scale. With GreptimeDB, the architecture decision you make on day one stays valid at day one thousand.

## What's Next

The final part of this series answers a different question: once data is in GreptimeDB, **how does it query so fast?**

Part 4 will cover the query optimizer, the role of Parquet column pruning and predicate pushdown, and a complete benchmark comparison against InfluxDB and TimescaleDB with full methodology: dataset, schema, hardware, and software versions.

Ready to explore? Try [EMQX Tables](https://www.emqx.com/en/cloud/emqx-tables) for a fully managed experience, or deploy open-source [GreptimeDB](https://github.com/GreptimeTeam/greptimedb) directly.

## References

**1** [GreptimeDB Architecture](https://docs.greptime.com/user-guide/concepts/architecture)

**2** [GreptimeDB Table Sharding](https://docs.greptime.com/contributor-guide/frontend/table-sharding)

**3** [Disaster Recovery Overview](https://docs.greptime.com/user-guide/deployments-administration/disaster-recovery/overview)

**4** [DR Solution Based on Active-Active Failover](https://docs.greptime.com/enterprise/deployments-administration/disaster-recovery/dr-solution-based-on-active-active-failover)

**5** [DR Solution Based on Cross-Region Deployment](https://docs.greptime.com/user-guide/deployments-administration/disaster-recovery/dr-solution-based-on-cross-region-deployment-in-single-cluster)[DR Solution Based on Cross-Region Deployment in a Single Cluster | GreptimeDB Documentation](https://docs.greptime.com/user-guide/deployments-administration/disaster-recovery/dr-solution-based-on-cross-region-deployment-in-single-cluster)
