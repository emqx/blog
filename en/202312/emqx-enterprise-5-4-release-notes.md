[EMQX Enterprise](https://www.emqx.com/en/products/emqx) 5.4.0 is now officially available!

This release introduces OpenTelemetry distributed traces and logs integration, adds support for the OCPP (Open Charge Point Protocol) protocol, and integrates with Confluent for data processing. Additionally, this version includes several enhancements and bug fixes to improve the overall performance and stability of the product.

## OpenTelemetry Distributed Traces and Logs Integration

EMQX 5.2.0 introduced [OpenTelemetry](https://opentelemetry.io/) metrics integration. Building on this, version 5.4.0 further integrates distributed traces and logs, fully implementing the functionality required by the OpenTelemetry observability framework.

### Distributed Traces

OpenTelemetry distributed traces track the flow of requests in distributed systems, allowing visualization and analysis of performance and behavior. In MQTT scenarios, this concept enables cross-participant (publisher-MQTT server-subscriber) request tracing during message transmission.

EMQX adheres to the [W3C Trace Context MQTT](https://w3c.github.io/trace-context-mqtt/) specification for end-to-end distributed tracing functionality. When publishing, the client includes the `traceparent` user property in the message, and traces document the message flow between EMQX cluster nodes and subscribers. For MQTT v3.1/3.1.1 clients lacking support for setting user properties, EMQX can be configured to internally add trace IDs to messages automatically, ensuring distributed tracing.

With OpenTelemetry distributed tracing, EMQX system administrators and developers can monitor and analyze IoT application performance in real time, facilitating quick troubleshooting when failures occur.

### Logs

OpenTelemetry logs, similar to file-stored logs, are used to record critical events, status updates, and error messages. They play a crucial role in aiding developers and operation teams in comprehending application behavior and troubleshooting issues.

Unlike traditional logs, OpenTelemetry logs use a standardized format, enhancing parsing, analysis, and processing. These logs include extensive contextual details such as Trace IDs, tags, attributes, and more.

EMQX allows concurrent activation of OpenTelemetry indicators, tracing, and logging functionalities. Indicators provide real-time status monitoring, tracing data reveals request flows and paths, and log data furnishes additional details and contextual information. The integration of these three functions establishes a unified view and analysis platform, forming a comprehensive observation solution. This unified platform empowers users to efficiently manage and utilize data, gaining comprehensive application observation capabilities. This facilitates accurate issue localization and resolution, significantly enhancing operational efficiency.

## OCPP Protocol Gateway

[OCPP](https://www.openchargealliance.org/) (Open Charge Point Protocol) is an open communication protocol connecting charging piles and centralized management systems, aiming to standardize communication for electric vehicle charging infrastructure.

EMQX 5.4.0 introduces a gateway based on the OCPP 1.6-J protocol. This gateway offers integrated upstream and downstream messaging capabilities for charging pile devices adhering to OCPP standards. The gateway also includes a range of security, management, and integration features, such as:

1. Ensuring transport layer security through TLS/SSL encrypted connections.
2. Providing access authentication options such as username/password and JWT.
3. Granting control over upstream and downstream message permissions.
4. Offering client management capabilities through Dashboard and REST API.
5. Supporting flexible and diversified application scenarios by seamlessly combining with the MQTT protocol.
6. Enabling integration with third-party management systems (Central System) through rule engine, data integration, and REST API.

These features enable users to establish a secure and reliable electric vehicle charging infrastructure, facilitating effective management and operation of charging businesses.

## Integration with Confluent

Confluent is a robust data streaming platform, offering both fully managed Confluent Cloud and self-hosted Confluent Platform products. It specializes in processing and managing continuous, real-time data streams.

Confluent offers a variety of services, including the Kafka service, Schema Registry, and Event Stream Processing tools. Additionally, it enables cross-region data replication and provides other powerful features. EMQX seamlessly integrates with the Confluent ecosystem, delivering a versatile end-to-end solution for real-time data collection, transmission, processing, and analysis in the IoT realm. This integration enhances an organization's ability to gain deeper insights and make informed decisions.

## Security Enhancement

1. Enhanced security by adding support for enabling authentication on the REST API `GET /api/v5/prometheus/stats` used for fetching metrics in Prometheus Pull mode integration.
2. Improved configuration file security by allowing the storage of sensitive configurations in separate files, which can be loaded by specifying the file path using the `file://` prefix in the configuration file.
3. The REST API now integrates Role-Based Access Control (RBAC) for more fine-grained security management. When creating an API key via the Dashboard or a key initialization file, you can assign one of the following roles:
   - Administrator: Grants access to all system resources.
   - Viewer: Permits viewing of resources and data, corresponding to all GET requests in the REST API.
   - Publisher: Specialized for MQTT message publishing, allowing access only to APIs related to publishing.

## Enhanced Performance with the New Route Storage Architecture

In this release, a revamped route storage architecture has been implemented to boost subscription and routing performance, albeit with a slight uptick in memory usage. This enhancement is particularly beneficial in scenarios involving shared subscriptions with the use of wildcards. In an internal benchmark comparison, EMQX 5.4.0 demonstrates a 30% increase in average subscription speed compared to version 5.3.0.

The new storage architecture eliminates the necessity for constructing individual indexes, thereby completely preventing cluster routing inconsistencies in extreme cases.

New storage system is on by default and will update older clusters automatically. To use the old system, you can adjust `broker.routing.storage_schema`.

## Additional Features

1. Introduced JT/808 and GB/T 32960 IoV protocol gateways, facilitating standardized vehicle data access. These gateways seamlessly integrate with the vehicle management platform through EMQX's integration capabilities, ensuring interoperability.
2. Enhanced the REST API and Dashboard with a backup and recovery function. Users now have the capability to create multiple data backups for the cluster and restore them as needed.
3. Incorporated an Audit Log Management page into the Dashboard, enabling users to track all changes made to EMQX devices and data. This includes actions such as device kick out, rule creation/deletion, and more.
4. Extended support for the SAML protocol in Dashboard Single Sign-On (SSO) to integrate with Azure Entra ID.
5. Strengthened client authentication by supporting authentication via the bind operation when the data source is the LDAP. This is particularly useful when account data already exists on the LDAP server or when there is a lack of permission to add or modify data.
6. Restructured the data bridging design by introducing connectors and actions (sinks). Connectors manage data integration to external systems and can be reused across multiple actions, while actions configure how data is manipulated. This design enhances flexibility and scalability for clearer data integration configuration and management.
7. Streamlined the node rebalance operation status API `GET /api/v5/load_rebalance/availability_check` by eliminating the need for authentication, simplifying configuration for the load balancer.
8. Introduced a new Reset License feature, allowing to set existing license to the default trial license.
9. Modified the default trial license specification from 100 to 25 connections.

## Bug Fixes

The major bug fixes include:

- [#10976](https://github.com/emqx/emqx/pull/10976) Fixed the issue related to the duplicate processing of topic filters in shared subscriptions. In previous implementations, the subscription storage method was not adequately adapted for shared subscriptions, resulting in message routing failures and routing table leaks between nodes during 'subscribe-unsubscribe' events for specific topics and processes.
- [#12048](https://github.com/emqx/emqx/pull/12048) Addressed a bug where the COAP gateway was overlooking subscription options.
- [#12158](https://github.com/emqx/emqx/pull/12158) Resolved an issue where the rule engine failed to connect to [Upstash](https://upstash.com/) Redis. Before the fix, the Redis driver for EMQX, after establishing a TCP connection to the Redis service, used [inline commands](https://redis.io/docs/reference/protocol-spec/#inline-commands) to send AUTH and SELECT commands. However, the Upstash Redis service does not support inline commands, causing connection failures. The fix ensures EMQX's Redis driver now uses RESP (Redis Serialization Protocol) to send AUTH and SELECT commands.

For a comprehensive list of feature changes and bug fixes, please refer to the [EMQX Enterprise 5.4.0 changelog](https://www.emqx.com/en/changelogs/enterprise/5.4.0).



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
