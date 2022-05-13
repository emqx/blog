We are pleased to announce that the latest version v0.7 of [HStreamDB](https://hstream.io), the cloud-native distributed streaming database HStreamDB is now officially released!

HStreamDB is the first cloud-native streaming database explicitly designed for streaming data, dedicated to efficient storage and management of large-scale data streams. It supports complex real-time analysis on dynamically changing streams and one-stop management of accessing, storing, processing, and distributing them. In the foreseen future, it will be the ideal solution for real-time stream data analysis and processing scenarios in the fields of IoT, Internet, finance, and other relevant areas.

Major optimizations in v0.7 include higher stability, scalability and availability. In the new version, we not only fixed numbers of problems found through integration tests, Jepsen tests and other means to improve the stability of the system but also introduced several new features and improvements, including transparent sharding, a new operation and maintenance management tool, a new version of hstreamdb-java, brand-new cluster load balancing algorithm, and improvements in use and deployment.

Download address of the latest version: [https://hub.docker.com/r/hstreamdb/hstream/tags](https://hub.docker.com/r/hstreamdb/hstream/tags) 

GitHub project address: [https://github.com/hstreamdb/hstream](https://github.com/hstreamdb/hstream) 

## Overview of the new version

### Transparent sharding is implemented to improve the scalability of stream

In previous versions, HStreamDB has supported the storage and management of large-scale data streams. To further enhance the scalability and read/write performance of a single stream and ensure the sequence of data, transparent sharding is added in HStreamDB v0.7:

- For the concern of scalability, a stream may contain multiple shards (the number of shards is changing). The read/write traffic load will be balanced in the cluster across the internal shards to achieve a higher throughput of a single stream.

- As for the sequence order, each piece of written data will carry an ordering key specified by the user. Each ordering key conceptually corresponds to a logical shard. Data in the same logical shard will be delivered to the same consumer in written order, as shown in the figure below.

  ![HStreamDB](https://assets.emqx.com/images/dffa53e70e086e03fe2c537321eacd7f.png)

It is worth noting that partitions are entirely transparent to users in HStreamDB v0.7. Users do not need to specify the number of shards or any sharding logic in advance. Nor do they need to worry about data redistribution and data disorder caused by shards change. From a perspective of system implementation, sharding is an effective method to solve single-point bottlenecks and improve the horizontal scalability of the system. From users' standpoint, exposing partitions directly to users destroys the abstraction of the upper layer and dramatically increases the cost of users' learning, use, and maintenance. Transparent sharding achieves scalability and ensures sequencing without exposing additional complexity to users, significantly improving the user experience.

For a more detailed introduction to transparent partition, please refer to [HStreamDB Docs](https://hstream.io/docs/en/latest/concepts/transparent-sharding.html)

### Cluster load-balancing algorithm is improved for higher distribution efficiency

It is necessary to distribute the read/write traffic of the client to each node in the cluster as evenly as possible for achieving a balanced usage of the resources of each node across the cluster. The load balancing strategy of HStreamDB v0.6 was based on the hardware usage of nodes. The main problem is that nodes need to exchange various hardware resource information, including CPU, memory, and network. Besides, this method has a certain lag. Overall, the old implementation was relatively complex and inefficient.

Therefore, we reimplemented a new load balancing module based on the consistent hashing algorithm in HSteamDB v0.7. Consistent hashing is an elegant and powerful algorithm used by various distributed systems, such as DynamoDB. The allocation strategy based on consistent hashing makes the load balancing module no longer need to maintain hardware resource information all the time and makes the core algorithm more concise. It can also deal with the problem of redistribution when cluster members change. At the same time, it is also very flexible and can be easily scaled and optimized. For example, it can deal with heterogeneous nodes by configuring different weights. There are also some latest optimizations, such as Google's [Consistent Hashing with Bounded Loads](https://ai.googleblog.com/2017/ 04/consistent-hashing-with-bounded-loads.html).

### HStream Admin tool is added to facilitate operation and maintenance management

We provide a new management tool to facilitate the maintenance and management of HStreamDB. HAdmin can be used to monitor and manage various resources of HStreamDB, including Stream, Subscription and Server nodes. HStream Metrics, previously embedded in HStream SQL Shell, has also been migrated to the new HAdmin. In short, HAdmin is prepared for HStreamDB operation and maintenance personnel, and SQL Shell is for HStreamDB end users.

For detailed instructions, please refer to [HStreamDB Docs](https://hstream.io/docs/en/latest/admin/admin.html#server-command)

### **Hstreamdb-java v0.7 is released to support new features of HStreamDB v0.7**

Hstreamdb-java is currently the main HstreamDB client and will always support the latest features of HSteamDB. The new functions of HStreamDB v0.7 are also supported in hstreamdb-java v0.7. Specifically, compared with hstreamdb-java v0.6, in addition to the fixes of several problems, hstreamdb-java v0.7 mainly includes the following noteworthy features and improvements:

- Support for HStreamDB v0.7 transparent partition.
- Improved support for clusters. Add the ability for requests to be retried across multiple nodes in the cluster in the case of recoverable failures.
- New buffered producer interface and implementation. Since users have different writing latency and throughput requirements in different scenarios, we split the original producer into two independent `BofferedProducer` and `Producer` for clarity. `BufferedProducer` is mainly used for high-throughput scenarios, and the `Producer` is mainly used for low-latency scenarios.
- Two flush modes are added in BufferedProducer. The original producer only supports triggering flush according to the number of data bars in batch mode. Now, BufferedProducer has added two flush modes, size-triggered and time-triggered. These three types of trigger conditions can work simultaneously, which can more flexibly meet the needs of users.

hstreamdb-java GitHub repository: [https://github.com/hstreamdb/hstreamdb-java](https://github.com/hstreamdb/hstreamdb-java)

### The deployment and use process are simplified to improve the user experience

- To facilitate users to experience and use HStreamDB quickly, we have added a quick start document based on docker-compose: [HStreamDB Docs](https://hstream.io/docs/en/latest/start/quickstart-with-docker.html).
- To quickly deploy and use HStreamDB clusters on multiple machines, we have developed a cluster deployment script, which you can download from the link [https://github.com/hstreamdb/hstream/blob/main/script/dev-deploy](https://github.com/hstreamdb/hstream/blob/main/script/dev-deploy)
- With the continuous increase of HStreamDB configuration items, the original method of passing the configuration through the command line is insufficient. Therefore, we have introduced the way of unifying management of configuration items through configuration files. Please refer to [https://hstream.io/docs/en/latest/reference/config.html#configuration-table](https://hstream.io/docs/en/latest/reference/config.html#configuration-table).

## Future Plan

In the next development stage, we will focus on the following objectives:

- Continuously improve the stability of the system to achieve production availability.
- Continuously improve system availability and monitoring capability for operation and maintenance to enhance security support.
- Upgrade the existing stream processing engine to bring more powerful real-time processing and analysis capabilities

Please stay tuned!
