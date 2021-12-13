[HStreamDB](https://hstream.io), a distributed cloud-native streaming database open-sourced by EMQ, has now officially released v0.6 !

HStreamDB is the first cloud-native streaming database explicitly designed for streaming data, dedicated to efficient storage and management of large-scale data streams. It supports complex real-time analysis on dynamically changing streams and one-stop management of accessing, storing, processing, and distributing them. In the foreseen future, it will be the ideal solution for real-time stream data analysis and processing scenarios in the fields of IoT, Internet, finance, and other relevant areas.

In the new-released 0.6 version, we provided the cluster mode for HServer, which enables flexible expansion of the computing layer nodes according to client requests and the scale of computing tasks. At the same time, we have implemented "shared-subscription" to allow multiple clients to consume on the same subscription in parallel, which significantly improves the distribution ability of real-time data.

Download the latest version: [Docker Hub](https://hub.docker.com/r/hstreamdb/hstream/tags)

## Quick overview of the new version

### Cluster mode support, and imporvements in horizontal scalability of HServer

HStreamDB v0.6 supports cluster mode of HServer. The cluster mode allows quick horizontal expansion, supports node health detection and failure recovery, and improves the fault tolerance and scalability of HStreamDB. Another feature worth mentioning is that HServer supports load balancing. By monitoring the real-time load status of nodes in the cluster, the load balancer will fairly assign the computing tasks to different nodes to realize the efficient use of cluster resources.

For the startup and deployment of the cluster, you can refer to the following documents:

- [https://hstream.io/docs/en/latest/start/start-hserver-cluster.html](https://hstream.io/docs/en/latest/start/start-hserver-cluster.html#start-local-hserver-cluster-with-docker) 
- [https://hstream.io/docs/en/latest/deployment/deploy-k8s.html](https://hstream.io/docs/en/latest/deployment/deploy-k8s.html)

![HStreamDB 架构图](https://static.emqx.net/images/553197ac2ae839659a3ba7cdd4b016e7.png)

### Shared subscription support, and enhancements in real-time data distribution

In HStreamDB v0.6, we have reconstructed the subscription pattern and introduced a new [shared subscription](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription) implementation.

In the previous design, only one client could consume from the same subscription, which restricts the HStreamDB's capability of real-time data distribution. The new implementation introduces the concept of a Consumer Group, which manages the consumption of streams in a unified manner. All consumers of the same subscription will join the same consumer group, and the client can join or leave the current consumer group at any time.

HStreamDB currently supports "at least once" consumption. HServer will distribute data to consumers in the consumer group in the round-robin. HServer will automatically resent messages without corresponding client's Ack reply to available consumers after the timeout. All members in the same consumer group share the consumption progress, and HServer is responsible for maintaining the progress. The high fault tolerance of HStreamDB ensures that the collapse of any node will not affect the consumption of streams.

Moreover, we have also updated the HSteamDB [Java client](https://github.com/hstreamdb/hstreamdb-java) to version v0.6, which fully supports HStreamDB's cluster and shared subscription functions. The new reconstructed subscription part of the Java client APIs will enhance ease of use. 

For the usage of HStreamDB Java Client, please refer to [hstreamdb-java/examples at main · hstreamdb/hstreamdb-java](https://github.com/hstreamdb/hstreamdb-java/tree/main/examples)

### HStream Metrics and enhancements in system observability

In HStreamDB v0.6, we have also collected some statistics, such as stream written rate, consumption rate and other basic stats.

Users can view these indicators in the HStream CLI as follows:

```
-- Find the top 5 streams that have had the highest throughput in the last 1 minutes.
sql> 
SELECT streams.name, sum(append_throughput.throughput_1min) AS total_throughput 
FROM append_throughput
LEFT JOIN streams ON streams.name = append_throughput.stream_name  
GROUP BY stream_name 
ORDER BY total_throughput DESC 
LIMIT 0, 5;
```

The query result is shown in the figure below:

![query result](https://static.emqx.net/images/11bc8c9fb3b67f8eb6466327e547439f.png)

### Rest API for writing data, and more possibilities for HStreamDB

Now you can use any language to write data to HStreamDB through Rest API. In the future, we plan to implement more Rest APIs to facilitate the secondary development of open source users around HStreamDB. For example, with HStream Rest API combined with the Webhook of the open-source EMQ X, you can realize the rapid integration of EMQ X and HStreamDB.

![HStreamDB Rest API](https://static.emqx.net/images/efe9a264a84a0c302bb9e5ba62c13c47.png)

## Development plan

In subsequent versions of HStreamDB, we will continue to iterate around the following goals:

- Improve the stability of the cluster: add more integration tests and error injection tests, improve code design and fix bugs

- Improve usability and operation and maintenance capabilities: Improve CLI tools, configuration, Rest API, and Java Client

- Increase the scalability of streams: Currently, HStreamDB can efficiently support concurrent reading and writing of many streams. However, when a single stream becomes a hot spot, it will face a performance bottleneck. In the future, we plan to solve this problem through **transparent partition**. The core principle is to try to maintain the simplicity of the user-level concept and encapsulate the complexity of partition in the internal implementation. Compared with other existing solutions, it will greatly enhance the user's experience.

  In subsequent versions of HStreamDB, we will continue to emphasize the following goals:

  - Improve the stability of the cluster: add more integration and error injection tests; improve code design and fix bugs.
  - Improve usability and maintainability: Improve CLI tools, configuration, Rest API, and Java Client.
  - Increase the scalability of streams: HStreamDB support efficient concurrent reading and writing of many streams. However, when a single stream becomes a hot spot, it will meet a performance bottleneck. We are planning to solve this problem through **an implicit partition**. The core principle is to maintain the simplicity of the user-level concept and encapsulate the complexity of partition within the internal implementation. Compared with other existing solutions, it will significantly enhance the user's experience.

HStreamDB is a pioneering attempt in data infrastructure to move forward to the real-time data era. With the continuous advancement of R&D, these large-scale multi-source continuously generated streaming data will get more efficient storage management and real-time analysis through HStreamDB. We believe that this will magnificently catalyze the process of obtaining insight and generating value from data. Welcome to follow and witness the follow-up progress of HStreamDB.
