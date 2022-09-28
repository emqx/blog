## Highlights

- Shards in Streams - direct access to records in shards of streams
- HStream IO- built-in data integration framework for HStreamDB
- New Stream Processing Engine
- Gossip-based HServer Clusters
- Update Java and Go clients; Add Python Client

## Shards in Streams

We have extended the sharding model in v0.8, which provides direct access and management of the underlying shards of a stream, allowing a finer-grained control of data distribution and stream scaling. Each shard will be assigned a range of hashes in the stream, and every record whose hash of `partitionKey` falls in the range will be stored in that shard.

Currently, HStreamDB supports:

- set the initial number of shards when creating a stream
- distribute written records among shards of the stream with `partitionKey`s
- direct access to records from any shard of the specified position
- check the shards and their key range in a stream

In future releases, HStreamDB will support the dynamic scaling of streams through shard splitting and merging.

## HStream IO

HStream IO is the built-in data integration framework for HStreamDB, composed of source connectors, sink connectors and the IO runtime. It allows interconnection with various external systems and empowers more instantaneous unleashing of the value of data with the facilitation of efficient data flow throughout the data stack.

In particular, this release provides connectors listed below:

- Source connectors:
  - [source-mysql](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/sink_mysql_spec.md)
  - [source-postgresql](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/source_postgresql_spec.md)
  - [source-sqlserver](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/source_sqlserver_spec.md)
- Sink connectors:
  - [sink-mysql](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/sink_mysql_spec.md)
  - [sink-postgresql](https://github.com/hstreamdb/hstream-connectors/blob/main/docs/specs/sink_postgresql_spec.md)

You can refer to [the documentation](https://hstream.io/docs/en/latest/io/overview.html) to learn more about HStream IO.

## New Stream Processing Engine

We have re-implemented the stream processing engine in an interactive and differential style, drastically reducing latency and improving the throughput. The new engine supports **multi-way join**, **sub-queries**, and **more** general materialized views.

The feature is still experimental. For tryouts, please refer to [the SQL guides](https://hstream.io/docs/en/latest/guides/sql.html).

## Gossip-based HServer Clusters

We refactor the hserver cluster with gossip-based membership and failure detection based on [SWIM](https://ieeexplore.ieee.org/document/1028914), replacing the ZooKeeper-based implementation in the previous version. The new mechanism will improve the scalability of the cluster and as well as reduce dependencies on external systems.

## Java Client

The [Java Client v0.9.0](https://github.com/hstreamdb/hstreamdb-java/releases/tag/v0.9.0) has been released, with support for HStreamDB v0.9.

## Golang Client

The [Go Client v0.2.0](https://github.com/hstreamdb/hstreamdb-go/releases/tag/v0.2.0) has been released, with support for HStreamDB v0.9.

## Python Client

The [Python Client v0.2.0](https://github.com/hstreamdb/hstreamdb-py/releases/tag/v0.2.0) has been released, with support for HStreamDB v0.9.
