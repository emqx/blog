We are excited to announce the official release of [EMQX Enterprise](https://www.emqx.com/en/products/emqx) version 5.5.0!

This version introduces a variety of new features and improvements, including integration with Elasticsearch, enhanced collaboration with Apache IoTDB and OpenTSDB, support for excluding topics in the authorization cache, and more. Moreover, the new version includes various bug fixes and performance enhancements, making it more stable and reliable.

## New Integration with Elasticsearch

Elasticsearch is a distributed engine for searching and analyzing data, offering functionalities such as full-text search, structured search, and data analytics. EMQX 5.5 supports the integration with Elasticsearch, allowing data insertion, updating, and deletion operations. This enables device data to be written to Elasticsearch, giving users the flexibility to use Elasticsearch’s search and analysis features for data processing.

After writing device data to Elasticsearch, users can leverage its search and analysis features. Some common use cases are event and log monitoring for IoT devices, geolocation data processing (Maps), and terminal security monitoring. For instance, IoT devices produce a lot of log data, which can be sent to Elasticsearch for storage and analysis. By connecting to visualization tools like Kibana, users can create charts based on this log data, providing real-time insights into device status, operation records, error messages, and more.

## Improve Integration with Apache IoTDB and OpenTSDB

Integration with Apache IoTDB and OpenTSDB has been improved in this version, and it now supports configuring templates for writing data. This makes writing data more flexible by specifying timestamps, field names, and data types for each field, simplifying data integration development.

## Support Batch Setting of Fields for InfluxDB, IoTDB, and TDengine

In industrial or IoV applications dealing with time-series data, there are scenarios where the data in a single message may originate from hundreds or even more data points. It is a repetitive and complex task to configure to extract them from the message and store them correspondingly in the database.

To solve this, EMQX provides batch setting functionality, allowing users to edit the field names to be written and the extraction method from the payload through a CSV file, imported via the Dashboard. This makes configuration easier for various data integrations, including InfluxDB, Apache IoTDB, and TDengine.

## Support Message Penetration for SysKeeper

In accordance with network security requirements in production systems of the power industry, network communication between production control zones, non-production control zones, and production management zones needs to be secured through unidirectional GAP devices.

EMQX has added forward penetration functionality for SysKeeper 2000. This feature can be enabled through configuration, enabling exchanging of EMQX messages between different production zones. This ensures data communication between two production zones while complying with regulatory requirements, offering customized support for IoT applications in the power industry and helping to achieve secure and efficient operation of power systems.

## Support Excluding Topics in Authorization Cache

EMQX has built-in client authorization features, ensuring application security. This includes authorization caching, which lowers backend load and boosts system performance.

On top of the caching feature, for some security-critical operations, users may want to exclude some topics from caching to get real-time permission control for communication security. In this version, EMQX allows excluding topics from authorization caching, letting clients tailor security requirements at different levels and achieve efficient and stable system operation.

## Improve Observability

EMQX provides users with comprehensive metrics integrated with monitoring services. Before, Prometheus was used for metric integration, but it could only get basic metrics related to clusters, clients, and MQTT. Metrics for authentication and authorization, rule engine, and data integration were not monitored.

In this version, we improve observability by providing more metrics, such as:

1. Authentication and Authorization: Status of each authentication and authorization service, and allow/deny records.
2. Rules: Execution status for each rule, like triggers, passes and failures, and execution speed.
3. Data Integration: Connection status for each external integration, and execution status for Sink and Source.
4. SSL/TLS certificate expiration, for certificate rotation monitoring.
5. License expiration time.

With these detailed metrics, users can do business-level monitoring, getting detailed insights into the current status of major components and helping to monitor and solve system issues.

## Enhance Performance

1. Kafka producer data integration now works faster and uses fewer resources on the Kafka server. This is good for applications that depend a lot on Kafka for data streaming, as it makes the whole system more efficient and reliable.
2. Cluster nodes can now update multiple subscriptions in batches, which speeds up the subscription process in Core-Replicant architecture for clusters across different regions or with high network latency. In a test with a 220ms network latency, the subscription speed was 20% faster. This also lowers the pressure on the proxy pool of cluster connections, reducing the chance of system overload.
3. Network communication is now more efficient when cleaning up routes. In the new design, when a node goes offline, the other nodes only need to do a “match and delete” operation, which cuts down the number of network packets and the network load between clusters. This is especially helpful for EMQX clusters in high-latency cross-regional environments.
4. GreptimeDB data integration can now do asynchronous write operations for better performance.
5. Support for concurrent creation and update of data integrations, improving operation speed for tasks such as importing backup files.

## Additional Updates

1. The ACL permission list in the token for JWT authentication has a new data format that allows more flexible usage.
2. Retained messages now support search and one-click clearing. The management of retained messages was already supported, but this version makes it easier and better. Users can search and manage retained messages by topic on the Dashboard and clear them with one click.
3. Delayed messages can now be deleted in batches by specifying topics, which makes the operation more efficient and less complex.
4. The page size limit for REST API pagination has been increased from 3000 to 10000, which supports larger data volumes in API calls.
5. MQTT bridge for data integration has been redesigned, so that one set of MQTT connections can be used for multiple message subscription and publishing configurations. This makes the configuration and management of data integration more flexible and efficient.

## Bug Fixes

The following are major bug fixes:

- [#12243](https://github.com/emqx/emqx/pull/12243) Fixed some minor race conditions that could cause global route states to be inconsistent, making sure the global route states are always correct and consistent to improve system stability.
- [#12269](https://github.com/emqx/emqx/pull/12269) Improved the error handling for the `/clients` interface. Now, if the query string is not valid, EMQX will return a 400 status and more specific error information instead of a general 500. This makes error handling more clear, helping users to know the causes of errors.
- [#12303](https://github.com/emqx/emqx/pull/12303) Fixed a problem with retained message indexing. Before, if a client had wildcard subscriptions, it might get retained messages that did not match its subscribed topics.
- [#12404](https://github.com/emqx/emqx/pull/12404) Fixed a problem where data integration metrics might stop being collected when data integration was restarted in high message traffic situations. Now, data integration metrics can be collected reliably in any situation, improving system reliability.
- [#12301](https://github.com/emqx/emqx/pull/12301) Fixed a problem in InfluxDB where numbers in line protocol were stored as strings. Now, numbers will be stored as numbers, improving data accuracy.

For more feature changes and bug fixes, please see the [EMQX Enterprise 5.5.0 Changelog](https://www.emqx.com/en/changelogs/enterprise/5.5.0).



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
