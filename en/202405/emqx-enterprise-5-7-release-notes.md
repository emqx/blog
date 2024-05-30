[EMQX Enterprise](https://www.emqx.com/en/products/emqx) 5.7.0 is now available!

This release introduces several new features and improvements, including durable sessions, message schema validation, and enhanced debugging and tracing capabilities for the rule engine. Additionally, numerous enhancements and bug fixes have been implemented to further improve overall performance and stability.

## Durable Session

The new Durable Session feature of EMQX provides robust persistence and high availability. It allows MQTT persistent sessions and their messages to be stored on disk, with session metadata and MQTT messages continuously replicated across multiple nodes in an EMQX cluster.

![EMQX cluster](https://assets.emqx.com/images/2b18b36064c0b25e06d6d4dbfa835093.png)

This feature offers flexible configuration options, enabling customization of the number of replicas per message or session by adjusting the replication factors. This allows for balancing persistence and performance.

Storing MQTT messages in shared, replicated persistent storage reduces memory usage for both online and offline sessions, supporting larger sessions and greater message processing capacity than in-memory storage. Durable sessions also enhance system reliability by enabling effective failover and recovery mechanisms, ensuring service continuity and high availability.

[Learn more](https://docs.emqx.com/en/enterprise/v5.7/durability/durability_introduction.html)

## Message Schema Validation

EMQX's built-in Schema Validation feature ensures the structure and format of MQTT messages are correct. Messages that do not conform to the required format can be discarded or disconnected from the client, with logs generated and rule engine events triggered for further processing.

Schema validation supports various formats such as JSON Schema, Protobuf, and Avro, or can use built-in SQL statements to validate message formats from specific topics. By detecting and blocking non-compliant messages early, schema validation ensures system stability and reliability.

In addition to validation, the same Schema can also be used for Schema encoding/decoding and Schema checking functions in the EMQX rule engine, as well as in external data systems and business processes, helping users achieve:

- **Data Integrity**: Ensures data consistency and correctness by validating the structure and format of MQTT messages.
- **Data Quality**: Maintains data quality by checking for missing or invalid fields, data types, and formats.
- **Uniform Data Model**: Reduces data inconsistencies and errors by enforcing a uniform data model across teams and projects.
- **Reuse and Sharing**: Enhances collaboration by allowing team members to reuse and share schemas, reducing duplication of effort and errors.

[Learn more](https://docs.emqx.com/en/enterprise/v5.7/data-integration/schema-validation.html)

## Rule Supports Debugging and Tracing

The rule engine now offers enhanced debugging and tracking features, allowing you to trigger a rule using simulated data or a real client, execute the rule's SQL and all associated actions, and view the execution results of each step.

Below is a screenshot of this feature. When the rule's SQL or any action fails to execute, the error log is displayed on the Dashboard, enabling you to quickly identify the corresponding action and view the structured error message for troubleshooting.

 ![Rule Supports Debugging and Tracing](https://assets.emqx.com/images/46459849806919421c82741d6d71439a.png)

In the screenshot, we can see that the rule was triggered four times. The first three executions were completely successful, but the fourth failed due to an error in the HTTP service action. By reviewing the error logs, we can determine that the failure was caused by the HTTP server responding with a 302 status code.

Unlike the previous SQL test, the rule debugging and tracking feature verifies that the entire rule functions as expected and facilitates quick troubleshooting and issue resolution. This not only accelerates development but also ensures that the rule will perform correctly in real-world scenarios, preventing failures during actual execution.

[Learn more](https://docs.emqx.com/en/enterprise/v5.7/data-integration/rule-get-started.html#test-rule)

## Enhanced Rule Action with Streamlined Variable Input

In previous releases, rule actions allowed the use of the `${var}` placeholder syntax to incorporate variables into rule processing for flexible configurations, such as dynamically constructed HTTP requests, MySQL INSERT statements, and AWS S3 object keys.

While this feature offered significant flexibility, users had to manually identify and input the variables available in the current rule SQL, which was time-consuming and error-prone.

In this release, the Dashboard's Action Configuration page now includes dynamic input hints for fields that support placeholder variables. Similar to code hints in an editor, the available variables are automatically derived from the current rule SQL, and users are promptly shown the available values during input. This enhancement simplifies the configuration process and significantly reduces the potential for errors.

![Rule Action](https://assets.emqx.com/images/b4226886ac5b842bb900887e1e04165e.png)

## Log Tracking Feature Enhancements

Two new features have been added to log tracking:

1. **Specify Rule ID for Tracing Execution Results**: This feature allows you to precisely trace and debug the execution of a specific rule. The log output will include the rule's SQL execution result and the logs for all actions within the rule, enabling quick identification and resolution of issues.
2. **Set Log Output Format to JSON**: This feature facilitates automated log processing and analysis, enhancing data processing efficiency.

[Learn more](https://docs.emqx.com/en/enterprise/v5.7/observability/tracer.html#trace-by-rule-id)

## Client Attributes

Client attributes in EMQX allow you to set additional attributes for a client using key-value pairs.

Attribute values can be derived from MQTT client connection information (e.g., username, client ID, TLS certificate) or set based on data returned by successful authentication. For example, you can configure EMQX to split the client ID at the colon (:) on client connection and use the first segment as a VIN attribute:

```
mqtt.client_attrs_init = [
  {
    expression = "nth(1, tokens(clientid, ':'))"
    set_as_attr = "VIN"
  }
]
```

These attributes can be utilized in various EMQX features, such as authentication&authorization, data integration, and MQTT extensions. For instance, in MySQL authorization checking, you can configure the SQL query to determine a client's publish/subscribe permissions based on the VIN attribute:

```sql
SELECT
  permission, action, topic, qos, retain
FROM mqtt_acl
  WHERE VIN = ${client_attrs.VIN}
```

Compared to using static attributes like client IDs, client attributes offer greater flexibility for various business scenarios. They simplify the development process, enhancing adaptability and efficiency.

[Learn more](https://docs.emqx.com/en/enterprise/v5.7/client-attributes/client-attributes.html)

## Disconnect Client When JWT Authentication Expires

The JWT specification includes an expiration time attribute that sets an expiration time when issuing a token. Previously, EMQX's JWT authentication only checked this attribute during client connection, allowing clients to stay connected even after the JWT expired.

In this release, EMQX introduces the ability to disconnect clients once their JWT expires. This feature is enabled by default to enhance system security and prevent potential vulnerabilities.

To maintain the previous behavior, you can disable the **Disconnect After Expiration** option in the JWT authenticator settings.

 ![JWT Authentication](https://assets.emqx.com/images/8ac058d5c642d47567312b954713554d.png)

[Learn more](https://docs.emqx.com/en/enterprise/v5.7/access-control/authn/jwt.html)

## Plugin Support for Hot Configuration and Customizable UI

Previously, EMQX supported plugins for extending customized features, sometimes requiring users to manually fill in configuration parameters.

This release introduces hot configuration functionality for plugins, allowing users to define the necessary UI pages for managing parameter configurations via Avro Schema. These pages are automatically loaded by the EMQX Dashboard on the plugin management page.

Developers can now focus solely on implementing back-end business logic, while the system automatically generates the UI pages, reducing the development workload. For users, this enables intuitive configuration of plugin parameters, enhancing the user experience.

This feature is optional, allowing users to continue with pure back-end development if preferred.

[Learn more](https://docs.emqx.com/en/enterprise/v5.7/extensions/plugins.html#write-configuration-schema-for-the-plugin-optional)

## Additional Features

1. Apache IoTDB data integration now supports IoTDB v1.3.0 and introduces batch insertion functionality, enhancing data writing performance.
2. More specific error information is provided when importing error schemas into the built-in authentication database, facilitating quicker problem identification for users.
3. RocketMQ now supports namespaces and key scheduling policies, enabling seamless integration with RocketMQ hosted on AliCloud.

## Bug Fixes

Here are the major bug fixes included in this release:

- [#12653 ](https://github.com/emqx/emqx/pull/12653)The bin2hexstr function in the rule engine now properly supports arguments with bit sizes not divisible by 8, such as those returned by the subbits function.

- [#12657](https://github.com/emqx/emqx/pull/12657) An issue where the rule engine SQL didn't allow any expression as an array element has been resolved. Now, any expression can be used as an array element, for example:

  ```sql
  SELECT
    [21 + 21, abs(-abs(-2)), [1 + 1], 4] as my_array
  FROM
    "t/#"
  ```

- [#12765 ](https://github.com/emqx/emqx/pull/12765)The subscribers.count and subscribers.max now correctly includes shared subscribers; previously, only non-shared subscribers were included.

- [#12812](https://github.com/emqx/emqx/pull/12812) Fixed an issue where connectors were blocking due to health checks, causing timeouts for updating or deleting connectors.

- [#12996 ](https://github.com/emqx/emqx/pull/12996)Fixed a leak in the emqx_retainer process for retained message. Previously, a client disconnecting while receiving a retained message could cause a process leak.

- [#12871](https://github.com/emqx/emqx/pull/12871) Resolved a node startup issue caused by node rebalance. Previously, if EMQX was shut down during node rebalance, it would not restart.

- [#12888](https://github.com/emqx/emqx/pull/12888) Fixed an issue with License-related configuration loss after importing backup data.

- [#12895](https://github.com/emqx/emqx/pull/12895) Added necessary but missing configurations in DynamoDB connectors and actions.

For more details on feature changes and bug fixes, please refer to the [EMQX Enterprise 5.7.0 changelog](https://www.emqx.com/en/changelogs/enterprise/5.7.0).



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div>Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient">Get Started →</a>
</section>
