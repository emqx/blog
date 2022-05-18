This April, the HStreamDB team completed multiple features, optimizations and fixes of problems for the HStream Server. Besides some new monitor metrics, a new Admin Server and a new Erlang client are also provided.

# HStream Server

### Optimization of Core Features and Fix of Problems

#### Subscription

- Add configuration `maxUnackedRecords`: This configuration is used to control the maximum number of records that have been distributed but not yet acked on each subscription. When the number of unacked records on a subscription reaches the value of this configuration, the subscription will stop sending data to prevent the accumulation of unacked records in extreme cases, affecting the performance of HServer and corresponding consumers. It is suggested that users configure this parameter reasonably according to their capacity for data consumption in practice.
- Improve the implementation and efficiency of retransmission after consumption timed out.
- Optimize the performance of reading data.
- Optimize implementation of subscription deletion.
- Improve the handling of duplicate ack messages.
- Fix the problem caused by workload balancing during the distribution of subscription data.
- Fix the data loss issue caused by the unavailability of the original consumer during the data resending.

#### Stream

- Add configuration `maxRecordSize`: Users can control the maximum data size supported by streams. The data exceeding this threshold will fail to return the write.
- Optimize the implementation of stream deletion
- Fix the problem of memory allocation during data writing.

### Add Multiple Metrics for Monitor

HStream Metrics are refined and enriched, divided into real-time indicators (e.g. write rate in the second level) and historical indicators (e.g., number of requests in minute level). We now provide statistical indicators of multiple dimensions, records, bytes and requests and detailed indexes such as success_requests and failed_requests, and percentile latency indicators of core links.

## HStream Admin Server

In the previous v0.7, we provided an automatically generated HTTP Server based on the gRPC-Gateway automatic generation, which provides the REST API and forwards the received HTTP request to the gRPC request of the HStream Server. Although the method, which was based on automatic generation, has the advantages of simple development and low maintenance cost, it also has some limitations on features.

Moreover, considering that we upgraded the original location of the HTTP Server to a unified Admin Server, it will be responsible for serving a variety of CLI Tools and Dashboards and providing open REST API for developers to use. For this reason, we have re-implemented an Admin Server, GitHub address: [https://github.com/hstreamdb/http-services](https://github.com/hstreamdb/http-services)

## HStreamDB Client

### HStreamDB Java Client

- Add configuration support for subscription `maxUnackedRecords`.
- Add configuration of the consumer's ackAgeLimit is used to control the transmission latency of the batched ack.
- Add force deletion support for the subscription.
- Add force deletion support for stream.
- Optimize the behaviour of the consumer when it is closed.
- Adjust the public interface exposed by BatchSetting and FlowControlSetting.
- Fix the problem of calculating the accumulated record size by BufferedProducer.
- Enrich the introduction and description of Javadoc related interface is enriched.

### HStreamDB Erlang Client

We added an Erlang client library hstreamdb-erlang for HStreamDB, GitHub address:[https://github.com/hstreamdb/hstreamdb-erlang](https://github.com/hstreamdb/hstreamdb-erlang) . It is mainly used to support efficient integration with the high-performance IoT message server [EMQX](https://www.emqx.com/en/products/emqx) to achieve the rapid and persistent storage of massive IoT data received by EMQX to HStreamDB and provide end-to-end solution of IoT data for users. The Erlang client has the essential capability of creating streams and writing data. However, the client is still in the early stage of development, and new features and performance optimization are ongoing.
