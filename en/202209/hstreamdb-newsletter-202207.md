This month, the HStreamDB team has been finishing up the development and release of v0.9. The work includes further refinement and testing of the new features that v0.9 will bring, such as improvements on the model of stream sharding, a new clustering mechanism, HStream IO, etc. Main HStreamDB clients have also been updated to accommodate the new HServer.

## Stream Sharding Model Improvements

In previous versions, HStreamDB used a transparent sharding model. The number of partitions of each stream will adapt according to the write loads; also, these shards were not visible to the user. The benefit of this model is that it keeps the user concept simple while retaining the flexibility to allow dynamic scaling of the number of shards with the load and maintain the order of the records required during the process. 

The main problem of the current model is that users will not be able to perform shard-level operations like reading data from any specified location of any specified shard. For this reason, we decided to provide users with more control so that they can:

- Control the routing of data between partitions via `partitionKey`.
- Read data from any shard directly from a specified location
- Manual control o the scaling of shards under a stream

In terms of implementation, HStreamDB adopts a key-range-based sharding mechanism, where all shards under a stream share a key space, each shard belongs to a continuous subspace (key range), and the expansion and contraction of shards correspond to the splitting and merging of subspaces. With this new design, the scaling of shards will be fast and more controllable without causing inefficiencies or affecting data order due to the redistribution of old data, which is also how transparent sharding manages the shards.

These improvements on the sharding model will be included in the upcoming v0.9 release (the control over partition splitting and merging have not been supported yet).

## HStream IO Updates

HStream IO is the built-in data integration framework for HStreamDB, composed of source connectors, sink connectors and the IO runtime. It allows interconnection with various external systems and empowers more instantaneous unleashing of the value of data with the facilitation of efficient data flow throughout the data stack. 

Following the support of the CDC source for multiple databases last month, we added sink connector support for MySQL and PostgreSQL this month with improvements and enhancements on the embedded IO runtime in connector parameter checking, configuration document generation, and task security exit. SQL shell now also provides commands to facilitate the creation and management of IO tasks via the CLI:

## HStream MetaStore

Currently, HStreamDB uses Zookeeper to store metadata of the system, for example, information about task assignment and scheduling, which brings some extra complexity to the deployment and operation of HStreamDB, such as JVM reliance for deployment, and separate management on Zookeeper clusters.

For this reason, we plan to remove the dependency of HStreamDB on Zookeeper and introduce a dedicated HStream MetaStore component (HMeta for short), which will provide a set of abstract metadata storage interfaces, and theoretically, we can implement it based on multiple storage systems. We are developing a default realization of the interface based on [RQLite](https://github.com/rqlite/rqlite). RQLite is developed based on SQLite and raft in Golang and is very lightweight and easy to deploy and manage.

Development of HMeta is still ongoing. And as mentioned in our previous newsletter, the new clustering mechanism for HServer no longer relies on Zookeeper, and this month we have migrated the EpochStore from HStore to HMeta. We will not include this feature in the upcoming v0.9 release. It needs more testing, and we plan to release it in v0.10.

## Client updates

As for the updates on the client end, for example, hstreamdb-java, the main changes include:

- `createStream` can now specify the initial number of partitions
- Added listShards method
- producer and `bufferedProducer` are adapted to the new partitioning model
- Reader class added, which can be used to read any partition

Support for v0.9 will be included for clients in other languages (Golang, Python).

## Others

Some other notable features completed this month include:

- Add advertised-listeners configuration for HServer, which is used to solve the problem of external client access to HStreamDB when HStreamDB is deployed in complex network environments.
- Improvements on the bootstrap process for HServer cluster
