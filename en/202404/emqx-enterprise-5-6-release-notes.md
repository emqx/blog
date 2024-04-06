[EMQX Enterprise](https://www.emqx.com/en/products/emqx) 5.6.0 is now available!

This latest version introduces a host of new features and enhancements, including integration with Amazon S3 and RabbitMQ consumer, support for JSON Schema-based message validation in the rule engine, and more. Additionally, it includes several performance improvements and bug fixes to enhance overall stability.

## Amazon S3 Data Integration

[Amazon Simple Storage Service (Amazon S3)](https://aws.amazon.com/s3/) is a highly reliable, stable, and secure Internet-oriented storage service that can be deployed and utilized rapidly. EMQX now offers seamless data integration with Amazon S3, enabling efficient storage of MQTT messages into Amazon S3 storage buckets for flexible IoT data storage.

This integration opens up opportunities for various business scenarios, such as data analytics, by combining IoT data with Amazon S3's extensive ecosystem of applications. Furthermore, Amazon S3 offers a cost-effective alternative to traditional databases for long-term data storage.

Moreover, EMQX is compatible with other storage services supporting the S3 protocol, such as [MinIO](https://min.io/) and [Google Cloud Storage](https://cloud.google.com/storage). By leveraging S3, developers can build scalable and reliable IoT applications, driving business agility and optimizing costs.

Learn more: https://docs.emqx.com/en/enterprise/v5.6/data-integration/s3.html

## RabbitMQ Consumer Data Integration

EMQX introduces RabbitMQ consumer data integration, enabling message bridging from RabbitMQ to MQTT.

Users can set up EMQX to retrieve messages from a designated queue in RabbitMQ. Subsequently, they can utilize the rule engine to conduct versatile data processing on these messages before publishing them to an MQTT topic as specified by EMQX.

This functionality combines the powerful features of RabbitMQ and EMQX, allowing tasks such as asynchronous device command issuance, task scheduling, and message forwarding. It provides users with greater flexibility and scalability, helping them meet their business requirements effectively.

Learn more: https://docs.emqx.com/en/enterprise/v5.6/data-integration/data-bridge-rabbitmq.html

## JSON Schema-Based Message Validation in Rule Engine

In an IoT environment, it's essential for devices and applications to communicate seamlessly, necessitating adherence to specific message formats. Receipt of an unexpected message format can result in processing anomalies for subscribers or pose security risks. To uphold system stability and reliability, early-stage data format validation is imperative to identify and prevent the propagation of improperly formatted messages.

JSON stands as the predominant data exchange format in IoT applications. Leveraging JSON Schema enables the straightforward definition of structured specifications for JSON data, encompassing validation rules for essential data attributes like mandatory fields, data types, ranges, and structures.

In this release, we introduce JSON Schema-based validation within the rule engine. This functionality facilitates the validation of incoming JSON objects against predefined schemas, ensuring that the data system exclusively processes anticipated messages. Furthermore, alongside JSON Schema, EMQX extends support for the validation of Arvo and Protobuf message formats.

Learn more: https://docs.emqx.com/en/enterprise/v5.6/data-integration/schema-registry.html

Here’s an example SQL query statement for validating messages under the t/# topic against a schema named my_schema and returning messages with a validation result (is_valid field) of true:

```sql
SELECT
  schema_check('my_schema', payload) as is_valid
FROM
  't/#'
WHERE is_valid = true
```

By modifying the JSON Schema definition, you can achieve different use cases, such as:

1. Validating whether the data is valid JSON:

   ```json
   {
     "type": "object"
   }
   ```

1. Validating that field values fall within the range of 0 to 100:

   ```json
   {
     "type": "object",
     "properties": {
       "value": {
         "type": "number",
         "minimum": 0,
         "maximum": 100
       }
     }
   }
   ```

1. Validating latitude and longitude address formats, which can also be used for implementing geofencing restrictions using multiple schemas:

   ```json
   {
     "type": "object",
     "properties": {
       "latitude": {
         "type": "number",
         "minimum": -90,
         "maximum": 90
       },
       "longitude": {
         "type": "number",
         "minimum": -180,
         "maximum": 180
       }
     }
   }
   ```

## Enhanced Blacklisting Options for Flexibility

In this release, the Blacklist feature now offers additional matching rules:

1. **Client ID/Username Pattern:** You can now use expressions to block a range of clients that match specific profiles. For instance, using the expression ^emqx-* will block all clients whose client ID or username begins with emqx-.
2. **IP Address Ranges:** You can specify the segments of IP addresses from which clients are to be blocked.

With these straightforward rules, you can cover a wide range of blocking scenarios, enhancing management flexibility and security.

Learn more: [https://docs.emqx.com/en/enterprise/v5.6/access-control/blacklist.html#create-banned-clients](https://docs.emqx.com/en/enterprise/v5.6/access-control/blacklist.html)

## Improved Client Management Features

EMQX has previously provided comprehensive MQTT client management capabilities through the Dashboard and REST API. These capabilities include querying online status and connection information, monitoring traffic and message exchange statistics, and viewing statuses of the Inflight Window and the Message Queue. These features offer robust support for users and application developers.

In this release, we have further bolstered these capabilities to enable users to achieve even more flexible and detailed client management.

### Enhanced Query Flexibility

We upgrade the existing GET /clients REST API to offer more versatile querying options and field customization:

- Conduct bulk queries by specifying multiple client IDs: `GET /clients?clientid=client1&clientid=client2`
- Perform bulk queries with multiple usernames: `GET /clients?username=user11&username=user2`
- Utilize the fields parameter to choose specific fields for return: use `GET /clients?fields=clientid,username,connected`

These query methods can be combined to suit your requirements. For instance, you can simultaneously query multiple clients while requesting only certain fields. This proves beneficial in scenarios requiring frequent queries, reducing the number of requests and data exchanged. Consequently, you can efficiently obtain the desired information.

Learn more: [https://docs.emqx.com/en/enterprise/v5.6/admin/api-docs.html#tag/Clients/paths/~1clients/get](https://docs.emqx.com/en/enterprise/v5.6/admin/api-docs.html#tag/Clients/paths/~1clients/get)

### Viewing Messages in Inflight Window and Message Queue

We introduce functionality to view message lists within the [Inflight Window and Message Queue](https://docs.emqx.com/zh/enterprise/v5.5/design/inflight-window-and-message-queue.html).

In EMQX, the Inflight Window and Message Queue within client sessions are pivotal features enhancing message transfer efficiency and offline message processing capabilities. They help to improve system stability, reliability, and performance.

In situations where subscribers lag in message processing or disconnect, messages accumulate in the Inflight Window and Message Queue. Viewing the message list allows for evaluating the extent of message buildup's impact and conducting functional debugging and troubleshooting tasks.

Learn more: [https://docs.emqx.com/en/enterprise/v5.6/admin/api-docs.html#tag/Clients/paths/~1clients~1%7Bclientid%7D~1mqueue_messages/get](https://docs.emqx.com/en/enterprise/v5.6/admin/api-docs.html#tag/Clients/paths/~1clients~1{clientid}~1mqueue_messages/get)

## High-Frequency Log Event Throttling

In EMQX, certain operations like message discarding or client publishing authorization failures can result in various issues such as excessive log generation and resource consumption.

The log throttling feature mitigates the risk of log overflow by restricting the logging of repetitive events within a defined time frame. By logging only the initial occurrence and suppressing subsequent repetitions of the same event within this frame, log management becomes more efficient without compromising observability.

The following log events are currently supported:

- authentication_failure: Authentication failure
- authorization_permission_denied: Authorization permission denied
- cannot_publish_to_topic_due_to_not_authorized: Unable to publish to the topic due to lack of authorization
- cannot_publish_to_topic_due_to_quota_exceeded: Unable to publish to the topic due to quota exceeded
- connection_rejected_due_to_license_limit_reached: Connection rejected due to license limit
- dropped_msg_due_to_mqueue_is_full: Message dropped because the message queue was full

Learn more: [https://docs.emqx.com/en/enterprise/v5.6/observability/log.html#log-throttling](https://docs.emqx.com/en/enterprise/v5.6/observability/log.html#log-throttling)

## Other Updates

- The Kafka producer client "wolff" has been upgraded from version 1.10.1 to 1.10.2. This latest version maintains a persistent metadata connection for each connector, optimizing EMQX performance by reducing the need to establish new connections for various actions and connector health checks.
- Several events prone to causing log flooding have been downgraded from warning to info level.
- Support has been added for cluster discovery using DNS AAAA record types during DNS auto-clustering.
- Enhanced error reporting has been implemented for the "frame_too_large" event and parsing failures of CONNECT packets due to formatting errors, providing additional troubleshooting information.
- The rule engine now includes new SQL functions for more flexible data handling, including:
  - map_keys(): Returns all keys in a Map.
  - map_values(): Returns all values in a Map.
  - map_to_entries(): Converts a Map into an array of key-value pairs.
  - join_to_string(): Joins an array into a string.
  - join_to_sql_values_string(): joins array elements as strings, if the elements are formatted as strings, they are wrapped in single quotes and used as the VALUES clause of the join SQL statement.
  - is_null_var(): Checks if a variable is NULL.
  - is_not_null_var(): Checks if a variable is not NULL.
- Added a new swagger_support option to the Dashboard configuration that allows you to enable or disable Swagger API documentation to improve security.
- Improved log readability with 2 tweaks: removed mfa metadata from log messages to improve clarity, and adjusted the order of fields in text-format logs to: tag > clientid > msg > peername > username > topic > [other fields].

## Bug Fixes

Below are the significant bug fixes addressed:

- [#11868](https://github.com/emqx/emqx/pull/11868) Resolved an issue where Will messages failed to publish after session takeover.
- [#12347](https://github.com/emqx/emqx/pull/12347) Updated MQTT Sink data integration to ensure all messages are treated as valid, even with incomplete data or non-existent placeholders. This prevents incorrect rejection and discarding of messages as invalid.
  - Payload and Topic templates now render undefined variables as empty strings instead of literal "undefined" strings.
- [#12492](https://github.com/emqx/emqx/pull/12492) Now includes the final Receive-Maximum property in CONNACK messages for MQTT 5.0 clients. This value takes the minimum between the client's Receive-Maximum and max_inflight configured by EMQX, which was previously omitted.
- [#12541](https://github.com/emqx/emqx/pull/12541) Introduced a parameter check for DNS auto-cluster configuration to ensure proper linkage between [node.name](http://node.name/) and cluster.discover_strategy. For instance, when using A or AAAA record types, all nodes must utilize a static IP address as the hostname.
- [#12566](https://github.com/emqx/emqx/pull/12566) Enhanced the bootstrap mechanism for REST API keys:
  - Skips empty lines in bootstrap files to avoid errors.
  - Prioritizes the bootstrap file, automatically deleting conflicting old keys when a new key is added.

For additional feature changes and bug fixes, please refer to the [EMQX Enterprise 5.6.0 changelog](https://www.emqx.com/zh/changelogs/enterprise/5.6.0).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
