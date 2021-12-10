[HStreamDB](https://hstream.io), the cloud-native distributed streaming database has officially released v0.6 in November. Straight after that, the HStreamDB team continues to work on the release of v0.7.

## v0.6 was officially released

In HStreamDB v0.6, we have presented many practical new features and functions, including HServer cluster mode, shared subscription, HStream Metrics, and REST API. For details, please refer to [HStreamDB v0.6 is officially released: horizontal scalability and real-time data distribution are improved, and new functions bring new possibilities](https://www.emqx.com/zh/blog/hstreamdb-v-0-6-release-notes).

## v0.7 is in steady development as planned

In v0.7, we will focus on improving the stability of the HStreamDB cluster and expanding the capabilities of the core data storage and consumption. The main progress we have made so far are listed as follows:

### Transparent partition: design and prototype

To further improve a single stream's scalability and reading/writing performance, v0.7 will introduce the transparent partition. Every stream will contain multiple partitions, which are invisible to users. The load balance of reading/writing traffic in the cluster will be realized through partitioning to support a higher throughput of a single stream. At the same time, partitions will be entirely implicit for users. Users do not need to specify the number of partitions or any partition logic in advance, nor do they need to worry about the series of problems such as data redistribution and order caused by the increase and decrease of partitions. We believe that stream as itself is a concise and powerful enough abstraction. Thus partitions should only be the implementation details and should not be exposed to users.

At present, we have completed the basic design of the transparent partition. Since this function significantly impacts the internal implementation, we will first carry out function verification and implementation exploration through a prototype. Right now, we are still implementing the prototype.

### Support docker-compose

HStreamDB is a distributed system with multiple components, and its deployment and use are relatively complex. We have improved the previous Docker-based startup method to facilitate users to get started and experience in the local environment. It now supports a one-step startup of a multi-node local HStreamDB cluster. For more details, please refer to the [document](https://hstream.io/docs/en/latest/start/quickstart-with-docker.html#start-hstreamdb-server-and-store).

### Jepsen test

We are currently using the Jepsen framework to test the functionality and stability of the HStreamDB cluster. Jepsen is a test framework written by Kyle Kingsbury in Clojure to verify the consistency of distributed systems, which has helped many well-known database products find problems, including Elasticsearch, Cassandra, etc. It is currently used in more distributed systems to test and verify their functions and fault tolerance.

As for us, we have successfully applied the framework to HStreamDB, conducted some basic tests, and found several minor problems. Later, we will implement a special checker in Jepsen to test relevant functions in combination with the data consistency model of HStreamDB and perform more abundant tests based on the error injection capabilities provided by Jepsen.

### REST API based on gRPC-Gateway

The communication protocol and interface between HStreamDB Server and the client are gRPC. Although gRPC has excellent advantages in development and performance, it still needs to be supported by REST API in browsers and three-party ecological integration scenarios. For this reason, in v0.6, we implemented part of the REST API based on the servant framework of Haskell. The main problem is that we need to simultaneously maintain these two sets of interfaces, which is expensive. The behaviour of these two sets of interfaces can not always be guaranteed to be consistent. We decided to use gRPC-Gateway to replace the current independent REST API implementation through investigation and research to solve these problems.

gRPC-Gateway can automatically generate a layer of REST API based on the underlying gRPC implementation, so we only need to maintain a set of gRPC implementations and always ensure the consistency of behaviour at the cost of losing some performance. However, it is not a problem for most scenarios of REST API applications. At present, we have completed the migration from servant to gRPC-Gateway.
