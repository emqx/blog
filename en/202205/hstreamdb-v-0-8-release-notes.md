HStreamDB v0.8 is now officially released!

In v0.8, we offer better read/write performance, improved long-running stability and reliability, new security support based on mTLS, new metrics, an admin server, benchmark tools, and Terraform deployment support. Besides, the latest version provides multiple new configurations and improvements on stream and subscription and enhanced clients in multi-language (Java, Go, Erlang). 

## New features of HStream Server

### Add mTLS support

Considering the security needs of users when deploying in production (e.g. public cloud and private cloud), such as connection encryption and identity authentication, we provide mTLS support in v0.8. Users can use mTLS by setting relevant configurations for servers and clients (currently only supported by Java clients). For details, please refer to the document: [https://hstream.io/docs/en/latest/security/overview.html](https://hstream.io/docs/en/latest/security/overview.html).

### Add multiple configurations for Stream and Subscription

#### Stream

Add configuration `max-record-size`: Users can control the maximum data size allowed by the stream through this configuration, and the data exceeding this threshold will fail to write.

Add attribute `backlogRetention`: This attribute determines how long the current records of the stream can reside, and HstreamDB will clean the data beyond this time limit.

#### Subscription

Add attribute `maxUnackedRecords`: This attribute caps the maximum number of records distributed but not yet acknowledged on each subscription. When unacked records of a subscription reach the value of this attribute, the data delivery on the subscription will stop to prevent the accumulation of unacked records in extreme cases, which could affect the performance of HServer and corresponding consumers. It is suggested that users configure this parameter reasonably according to their capacity for data consumption.

### **Add multiple stats in HStream Metrics**

To make it easier for users to monitor the HStream cluster, we have refined and enriched the monitored stats of the HStream, including real-time stats (e.g. second-to-minute write rate) and historical stats (e.g. the total number of append_requests). Besides, we provide these stats in multiple dimensions such as records, bytes, requests, and other measurements and more detailed indicators such as success/failed and percentile latency indicators of core paths (read/write). At present, you can use hadmin can to view these indicators. Please refer to the document for details:[https://hstream.io/docs/en/latest/admin/admin.html#hsteam-stats](https://hstream.io/docs/en/latest/admin/admin.html#hsteam-stats) 

### Add Admin Server

In the previous v0.7, we provided an automatically generated HTTP Server based on the gRPC-Gateway, which provides the REST API and forwards the received HTTP request to the HStream Server. Although the method, which was based on automatic generation, has the advantages of simple development and low maintenance cost, it also has some feature limitations.

Moreover, considering that we upgraded the original location of the HTTP Server to a unified Admin Server, it will be responsible for serving various CLI tools and dashboards or providing open REST API for developers to use. Therefore we re-implemented an Admin Server, GitHub address: [https://github.com/hstreamdb/http-services](https://github.com/hstreamdb/http-services).

### Add rapid deployment based on Terraform

Terraform is an open-source infrastructure-as-code tool developed by HashiCorp. It can help developers, operators, and maintainers manage their architecture and resources in an automated and reproducible manner and administer cloud services efficiently. Terraform allows us to deploy quickly, experience, and test HStreamDB in various public and private cloud environments. For details, please refer to the document: [https://hstream.io/docs/en/latest/deployment/deploy-terraform.html](https://hstream.io/docs/en/latest/deployment/deploy-terraform.html). 

## Optimization and improvement of HSstream Server 

### Optimization of data consumption

In v0.7, the relevant state of a subscription might be distributed on multiple HServer nodes in the cluster. Although this design brings excellent flexibility and fine-grained scalability, it has also brought implementation complexity, including the demand for multi-round RPC communication and state maintenance across nodes. In the new implementation, we restrict the state of a subscription from crossing nodes, which leads to the simplification of the protocol. We use STM to deal with the concurrency state in the new implementation. Benefiting from the usability and composability of STM, we improve the performance of high concurrency while ensuring correctness at the same time.

In addition, we have made the following improvements to the overall data consumption process:

- The realization of retransmission after data consumption timeout is optimized, and the efficiency of data retransmission is improved.
- The performance of reading data is optimized.
- The handling of duplicate ack messages is improved.

### Optimization of resource deletion

The deletion of stream and subscription is improved, and the option of forced deletion is supported. For details on how to create and manage related resources in HStreamDB, please refer to the document:  [https://hstream.io/docs/en/latest/guides/stream.html#create-and-manage-streams](https://hstream.io/docs/en/latest/guides/stream.html#create-and-manage-streams) and [https://hstream.io/docs/en/latest/guides/subscription.html](https://hstream.io/docs/en/latest/guides/subscription.html)  

## HStreamDB Java Client v0.8 

### New features of hstreamdb-java v0.8

- Add support for multiple new features of hstreamdb v0.8: including new configurations of TLS, stream and subscription and forced deletion support.
- BufferedProducer configurations have adopted new designs. Subscription includes BatchSetting and FlowControlSetting: BatchSetting explicitly controls the method of making a batch, the size and sending time of batch by BufferedProducer, and so on. It can be jointly controlled by three options: `recordCountLimit`, `bytesLimit`, and `ageLimit`. Depending on different scenarios, it can also be flexibly configured to meet different throughput and latency requirements. FlowControlSetting mainly controls the memory space occupied by the whole BufferedProducer and the behaviour after reaching the limit.

### Performance optimization of hstreamdb-java v0.8

- BufferedProducer uses the strategy of parallel sending for multiple different orderingKey data, significantly improving the write performance in multi-key scenarios.
- The batch mechanism is enabled for the acknowledgement transmission of the Consumer, which enhances the performance of the Consumer. The newly-added configuration of the Consumer's `ackAgeLimit` is used to control the transmission latency of the batched ack.

## Newly-added multi-language clients and performance testing tools

### hstreamdb-go v0.1.0 released

Hstreamdb-go is the Golang client of HSstreamDB. It has released v0.1.0. At present, it supports the basic interaction with HStreamDB. GitHub address:[https://github.com/hstreamdb/hstreamdb-go](https://github.com/hstreamdb/hstreamdb-go) 

### New hstreamdb-erlang

Hstreamdb-erlang is the Erlang client library of HSstreamDB. GitHub address: [https://github.com/hstreamdb/hstreamdb-erlang](https://github.com/hstreamdb/hstreamdb-erlang)

It can support the efficient integration with the high-performance IoT message broker EMQX to achieve the rapid and persistent storage of massive IoT data received by EMQX to HStreamDB and provide an end-to-end solution for IoT data for users. The Erlang client has the essential capability of creating streams and writing data. However, the client is still in the early stage of development, and new features and performance optimization are ongoing.

More language support is also planned, and suggestions and feedback are welcome. As HStreamDB uses gRPC to communicate with the client, the cost of developing new language clients is greatly reduced due to the extensive language support and engineering convenience of gRPC. New client development is appreciated.

### Added benchmark tools

To make it easy for users to evaluate the performance of HSstreamDB quickly, we open-source a set of benchmark tools. For details, please refer to  [https://github.com/hstreamdb/bench](https://github.com/hstreamdb/bench) 

## Problem fix

The v0.8 also contains several problem fixes that improve the stability of the long-term operation. For details, please refer to the release notes:  [https://hstream.io/docs/en/latest/release_notes/HStreamDB.html#v0-8-0-2022-04-29](https://hstream.io/docs/en/latest/release_notes/HStreamDB.html#v0-8-0-2022-04-29)
