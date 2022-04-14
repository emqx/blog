In March, the HStreamDB team optimized the HStream server, which comprised simplification and code refactoring of read path protocol and the newly supported mutual TLS. As for clients of HStreamDB, we have improved `BufferedProducer` in the Java client to enhance writing performance in multi-key scenarios. Furthermore, we have also released the first version of Golang Client. Besides updates about new features, we also open-sourced some essential bench tools and fixed the problems identified in various tests.

## HStream Server

### Simplification of read path protocol and code refactoring

Read path refers to the module implementing the subscription feature HStream Server. The code logic of this part is relatively complicated. In general, it consists of the following two aspects:

- State management for subscription: it mainly involves consumption progress tracking, maintenance of ack window, resending timed-out records and submission and persistence of the snapshot. This part is critical to ensure at-least-once record consumption and subsequent exactly-once semantics support.
- Maintenance and dynamic data distribution for Consumer Group: A subscription can be consumed by multiple consumers via consumer group. Consumers will be actively entering and exiting. Therefore the number of consumers is dynamic; meanwhile, the transparent partitions of the stream associated are also created dynamically. These dynamics have brought significant challenges to quickly and timely distributing the data in each partition to the appropriate consumer and the redistribution at the time of failure.

In the previous implementations of HStream v0.7, the state of one subscription may be distributed on multiple HServer nodes in the cluster. Although the design brought great flexibility and fine-grained scalability, it also led to the complexity of the implementation. Except that the client and server require multiple rounds of RPC communication on the read path, it is hard to maintain the state across nodes in the case of high concurrency. We also found some difficult bugs introduced into relevant implementations, declining consumer performance under general conditions.

Therefore, in a new implementation, we limit the state of a subscription to one node only, which simplifies the protocol. Moreover, in the new implementation, we use STM to handle concurrent states. Thanks to the usability and composability provided by STM, it has improved the performance under high concurrency while ensuring correctness.

### Mutual TLS support

We can implement connection encryption, identity authentication and other security features based on TLS. This month, the relevant codes supporting mTLS have been merged into the main branch. Although the official release of the feature will be in v0.8, users can now play around with the latest image of HStreamDB, and users can activate the TLS support by enabling the following configuration in the HServer configuration. Refer to the documentation for details: [https://hstream.io/docs/en/latest/security/overview.html](https://hstream.io/docs/en/latest/security/overview.html)

### Backlog duration that supports configuration of stream

Now, when creating a Stream, the attribute of Backlog duration can be specified. This attribute determines how long the data of the current stream can reside in HStreamDB, and hstream will clean up the data beyond this period.

## Java Client

### Performance optimization of BufferedProducer

For easier understanding and use, we have adjusted the relevant configurations of BufferedProducer, mainly classified into BatchSetting and FlowControlSetting. `BatchSetting` determines how BufferedProducer batches, batch size and sending time, etc. It provides three options: `recordCountLimit`, `bytesLimit`, and `ageLimit` to satisfy different throughput and delay requirements according to different scenarios. `FlowControlSetting` mainly controls the memory space size occupied by the entire BufferedProducer and the behaviour after reaching the limit. At present, the default behaviour after the limit is a blockage. At the same time, BufferedProducer alters the use method of parallel sending strategy to data of multiple different ordering key, which improves the writing performance in the multi-key scenario.

### Consumer Batch ACK

Previously, the consumer immediately sent ACK of each Record, which led to performance issues in scenarios with large amounts of data. Now, with the batch mechanism activated for ACKs, the performance of the consumer improves. 

### TLS support

The Java client also adds support for TLS, which user can use in the following ways:

## Golang Client

hstreamdb-go v0.1.0 release

hstreamdb-go is the Golang client of HStreamDB, and v0.1.0 was released last month. At present, it supports the basic interaction ability with HStreamDB. For the repository, see [https://github.com/hstreamdb/hstreamdb-go](https://github.com/hstreamdb/hstreamdb-go) .

## Testing

### Chaos Testing

Upholding the principle of Vary Real-world Events and Automate Experiments to Run Continuously of Chaos Engineering, we enriched failure-injection testing for Jepsen. In addition to the node fault, we have also introduced the fault types such as external service failure, data packet loss and network delay, etc. This part of the test will also automatically run at a high frequency so that we can discover and solve problems in time.

### Bench tools

We open-sourced some essential HStreamDB bench tools, which can quickly evaluate the performance of HstreamDB. These bench tools are developed based on hstreamdb-java. They are:

- Write bench: to test the writing performance of HStreamDB
- Read bench: to test the reading performance of HStreamDB
- Write&read bench: to test performance under mixed reading-writing load of HStreamDB 

## Bugfix

We also fixed some problems identified in various testing; among them, those with more severe impact include:

- Fixed the problem that HServer exiting unexpectedly after Zookeeper clustering failed
- Fixed the problem of distribution uniformity of load balancing algorithm under some circumstances
- Fixed the issue where the consumer caused the hserver to exit unexpectedly under some circumstances
