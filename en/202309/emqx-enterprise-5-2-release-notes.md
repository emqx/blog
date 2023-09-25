[EMQX Enterprise](https://www.emqx.com/en/products/emqx) 5.2.0 is now officially released!

This version introduces several significant enhancements. The most remarkable one is the Flow Designer, a visual tool that allows enterprise users to easily create, test, and deploy data integrations through simple drag-and-drop actions. Moreover, we have also added data integration supports for Amazon Kinesis and Azure Event Hubs, which facilitate the integration of massive IoT device data with cloud services. Furthermore, this version contains many other improvements and bug fixes, which boost the overall performance and stability.

## Flow Designer: Visualized Data Integration

The Flow Designer is a new feature that extends the capabilities of the previous Flows, which only display data integrations, by enabling the creation and modification of data integrations.

This tool offers a user-friendly approach to designing rules and data bridges through a simple drag-and-drop interface. It enables real-time processing of messages and events while seamlessly integrating with more than 40 external data systems in just minutes. After creating these integrations, users can easily manage the data integration process and monitor the status of each processing node through a unified view.

The Flow Designer still utilizes rule SQL and data bridging in the underlying layer, inheriting EMQX's robust data processing capabilities and exceptional performance. Simultaneously, it offers users the flexibility to seamlessly switch between the UI and SQL editors, offering the choice to use the familiar SQL editing style or the faster and more intuitive UI editing style. This enhancement allows users to develop their business through a straightforward UI without the need to delve into EMQX's rule SQL syntax, thereby facilitating the application of EMQX's data processing capabilities for business innovation.

![MQTT Flow](https://assets.emqx.com/images/e2c849a1c0298ca975b238afeff50cb9.png)

## Simplified Webhook Integration

Webhook is one of the most popular data integration methods in EMQX. To make it even easier to use, the latest version of EMQX has added a dedicated Webhook configuration page, which can greatly simplify the setup process of sending data to external HTTP servers.

In the past, this feature necessitated writing rule SQL and configuring data bridging, demanding familiarity with SQL syntax. This complexity was particularly evident when dealing with client-side events, where understanding how events were mapped in SQL statements (as shown in the following SQL) presented a steep learning curve.

```
SELECT 
  *
FROM
  "$events/client_connected"
```

The new Webhook configuration page allows users to select the messages or events they want to send by simply using forms, without writing any code. This makes it much easier to use, as users can quickly connect an event or message to an external web service without having to learn the SQL syntax of EMQX rule.

![EMQX Webhook](https://assets.emqx.com/images/116164945d05aaa323a475ff4938f7a9.png)

## Simplified Data Bridging Configuration

EMQX's data bridging feature provides rich and comprehensive configuration options to meet the needs of enterprise-class messaging middleware in terms of performance, stability, and flexible configuration in various business scenarios. By adjusting the parameters of the corresponding functions, it is possible to balance latency and write speed, or to increase more connections to achieve higher throughput (which also puts more pressure on external data services).

However, we have noticed that for most scenarios, many parameters remain unchanged, and EMQX's default values suffice. Therefore, in this release, we have concealed these parameter configurations within advanced settings. This allows users to concentrate solely on configuring business processes and logic. When specific performance bottlenecks or scenario requirements arise, users can configure advanced settings to fine-tune parameters.

Below is a simplified version of the Timescale data bridge creation page, where you only need to focus on the connection and data write process configuration:

![EMQX data bridging](https://assets.emqx.com/images/8c3d39342afeb393a1f4852513d7d683.png)

This makes it easier to learn while preserving EMQX's adaptability to complex scenarios, making the data bridging functionality of EMQX more user-friendly.

## Integration with Amazon Kinesis

[Kinesis](https://aws.amazon.com/cn/kinesis/) is a fully managed service on AWS that enables you to collect, process, and analyze streaming data in real time. It can handle streaming data of any size with low cost and high flexibility and can process any amount of streaming data from hundreds of thousands of sources with low latency.

EMQX, in conjunction with Amazon Kinesis, facilitates massive IoT device connectivity. It empowers real-time message capture, transmission, and seamless integration with Amazon Kinesis Data Streams, enabling real-time analytics and complex stream processing with EMQX data integration.

Utilizing Kinesis' streaming data pipeline significantly simplifies the connection between EMQX and the AWS platform, offering users more versatile data processing options. This empowers EMQX users to create high-performance, data-driven applications on AWS.

![Integration with Amazon Kinesis](https://assets.emqx.com/images/5cc996d1bec5f99222fb63132abf42e7.png)

## Integration with Azure Event Hubs

[Event Hubs](https://azure.microsoft.com/zh-cn/products/event-hubs) is a simple, reliable, and scalable fully managed service on Azure designed for real-time streaming data processing. With the capability to handle millions of streaming events per second, it empowers users to create dynamic data pipelines and swiftly address business challenges. Event Hubs supports scaling throughput based on usage demand and a pay-as-you-go pricing model and offers strong security and privacy protections.

Event Hubs act as a data channel between EMQX and Azure's rich set of cloud services and applications, integrating IoT data into Azure Blob Storage, Azure Stream Analytics, and various applications and services deployed on Azure virtual machines.

The low-latency transport channel offered by Event Hubs simplifies the connection between EMQX and the Azure platform, enabling users to swiftly link vast IoT device data with Azure. This facilitates access to cloud computing's data analysis and intelligence capabilities, empowering the creation of robust data-driven applications.

![Integration with Azure Event Hubs](https://assets.emqx.com/images/df865256e8f5090841125c10a84a605b.png)

## Integration with HStream

[HStream](https://hstream.io/) is EMQ's open-source, cloud-native distributed streaming data platform that is specially designed for IoT data storage and real-time processing.

It can reliably store millions of device data streams using a distributed, fault-tolerant storage cluster, providing real-time subscription support to deliver the latest streams to your applications. Additionally, it gives you the flexibility to replay and consume data streams whenever needed.

HStream's distinctive converged architecture, combined with EMQX's extensive device connectivity and multi-protocol support, enables users to efficiently manage the ingestion, storage, processing, and distribution of real-time messages, events, and data streams on a unified platform. This offers convenience for operating IoT data streams and developing real-time applications.

## Integration with GreptimeDB

[GreptimeDB](https://greptime.com/) is an open-source, cloud-native time-series database that encompasses time-series data processing and analysis capabilities. It's meticulously designed for cloud environments, harnessing the cloud's inherent strengths such as elasticity, scalability, and high availability.

GreptimeDB integration with EMQX empowers users to achieve long-term storage and efficient querying of massive IoT data, with the flexibility to scale in alignment with business growth. It offers boundless historical data storage and SQL optimizations tailored for time-series data, making it well-suited for exploring and extracting insights from large datasets over long periods of time. Users can effortlessly query historical data at any point in time, gaining immediate insights into time-series trends via SQL queries. This facilitates the extraction of essential business value from intricate data, fostering data-driven intelligent decision-making.

## Rule Engine Support for Sparkplug B Message Codecs

[Sparkplug](https://www.emqx.com/en/blog/sparkplug-3-0-advancements-and-formalization-in-mqtt-for-iiot) is an open-source specification widely used in [Industrial IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges). It relies on a well-defined set of payload and state management systems provided by MQTT, enabling interoperability and consistency.

Sparkplug B makes the MQTT namespace easier for SCADA systems, real-time control systems, and devices. It uses Protobuf to encode data for lightweight, efficient, and flexible data exchange. 

This version adds Sparkplug B message encode/decode functions to the rule engine SQL, allowing users to easily encode and decode Sparkplug B messages to JSON format by using the `sparkplug_encode` and `sparkplug_decode` functions directly in EMQX. The resulting decoded JSON data can then undergo complex processing through other Rule Engine functions and seamlessly integrate with external data bridges, facilitating robust business integration. This enhancement simplifies the interoperability of different devices in industrial IoT, improves development efficiency, and enables flexible and scalable IoT applications.

## Integration with OpenTelemetry Indicator

[OpenTelemetry](https://opentelemetry.io/), a member of the CNCF, is an open-source observability framework designed to transmit observable data, including [traces](https://opentelemetry-io.translate.goog/docs/concepts/observability-primer/?_x_tr_sl=en&_x_tr_tl=zh-CN&_x_tr_hl=zh-CN&_x_tr_pto=wapp#distributed-traces), [metrics](https://opentelemetry-io.translate.goog/docs/concepts/observability-primer/?_x_tr_sl=en&_x_tr_tl=zh-CN&_x_tr_hl=zh-CN&_x_tr_pto=wapp#reliability--metrics), and [logs](https://opentelemetry-io.translate.goog/docs/concepts/observability-primer/?_x_tr_sl=en&_x_tr_tl=zh-CN&_x_tr_hl=zh-CN&_x_tr_pto=wapp#logs), from applications to backend components using a standardized data format.

This release supports OpenTelemetry metrics, providing built-in monitoring capabilities to enhance the observation, analysis, and diagnosis of EMQX cluster performance.

EMQX plans to support OpenTelemetry traces and logs in future releases. By incorporating distributed tracing and correlating logs and directly analyzing how requests are processed within EMQX, we can enable end-to-end distributed diagnosis capabilities. This enhancement will enrich EMQX's monitoring data, enabling users to comprehensively and precisely monitor system operation status while quickly identifying and addressing anomalies.

## Performance Enhancements

Performance has always been a priority for EMQX, and we have made the following improvements in this release:

- Upgraded the Mria version to enhance publishing speed for retained messages by merging the index updates.
- Improved rule matching performance by using topic indexing in the Rule Engine, which is particularly beneficial for managing large numbers of rules.
- Introduced new node pooling and channel pooling configurations. Adjusting these configurations can significantly boost EMQX performance on high-latency clusters.

## Additional New Features

In addition to the main features mentioned earlier, several components have been upgraded to enhance daily operations and user experience:

- Authentication, authorization, and Redis connections in data bridges now support setting usernames for connecting to Redis services that require usernames, such as AWS MemoryDB.
- Kafka data bridging now offers dynamic [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) settings in consumer mode, allowing more flexible Kafka-MQTT topic mapping and MQTT target topic control.
- GCP PubSub data bridging now supports setting PubSub message attributes and sort keys, enabling richer message routing and ordering.
- RabbitMQ data bridging now includes TLS connection support.
- The `jq` dependency version has been updated to fix minor security issues.
- Client authentication and authorization are now supported using LDAP as a data source.
- Installation packages for Amazon Linux 2023 and Debian 12 are now available.
- Metrics for messages, overload protection, authorization, and authentication have been optimized for greater clarity and richness for Prometheus integration.

## Bug Fixes

The following is a list of major bug fixes:

- Fixed issue with logging of unrelated errors during EMQX shutdown. [#11065](https://github.com/emqx/emqx/pull/11065)
- Fixed an issue that prevented clients from sending messages with large payloads when debug/trace was enabled. [#11279](https://github.com/emqx/emqx/pull/11279)
- Fixed an issue where the `packets_connack_sent` metric was not incremented when sending CONNACK packets with a non-zero `ack_flag`. [#11520](https://github.com/emqx/emqx/pull/11520)
- Added a check for the maximum value of the timestamp in the API to ensure it is a valid Unix timestamp. [#11424](https://github.com/emqx/emqx/pull/11424)

See the [EMQX Enterprise 5.2.0 changelog](https://www.emqx.com/en/changelogs/enterprise/5.2.0) for more feature changes and bug fixes.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
