EMQX 6.0.0 marks a monumental leap forward as the first major release following the extensive version 5 series, redefining IoT data streaming with unified MQTT and message queuing. This landmark version introduces transformative features like Message Queue for durable, asynchronous messaging, namespaced roles for secure multi-tenancy, and seamless integrations with databases like AWS AlloyDB and BigQuery. 

Designed for dynamic environments, EMQX 6.0.0 empowers smart cities, industrial IoT, and connected vehicles, turning complex challenges into scalable, resilient solutions. Discover the innovations shaping the future of connected systems.

## Reliable MQTT Messaging with Message Queue

EMQX 6.0.0 redefines [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) with a native Message Queue feature, seamlessly integrating real-time pub/sub with durable, asynchronous message queuing. This server-side buffer captures messages matching a specified topic filter, persisting them even when subscribers are offline. Clients consume these messages by subscribing to the special `$q/{TopicFilter}` topic format, ensuring reliable data delivery in dynamic IoT environments.

### **Why It Matters:**

Unlike traditional MQTT, which relies on subscriber availability, Message Queues decouple publishers and subscribers to support both real-time and asynchronous messaging workloads, offering persistent storage, configurable retention (e.g., TTL), and QoS 1 delivery. This unified approach simplifies IoT architectures by consolidating real-time and asynchronous messaging into a single EMQX platform, eliminating the need for external queuing systems.

### **Key Benefits:**

- **Unified MQTT and Queuing**: Combines MQTT’s lightweight pub/sub with enterprise-grade message queuing, eliminating the need for external systems like RabbitMQ or Kafka.
- **Last-Value Semantics**: Optionally retains only the latest message per key (e.g., device ID), ideal for tracking fast-changing states like sensor readings or device configurations.
- **Flexible Dispatch**: Offers configurable strategies (Random, Round Robin, or Least Inflight Subscriber) to optimize message distribution across multiple clients.
- **Guaranteed Delivery**: Ensures no data loss during subscriber disconnections or network disruptions, perfect for unreliable networks in IoT deployments.

### **Example Use Case**:

In a smart agriculture system, soil sensor data published to `farm/+/sensors` is stored in a Message Queue. A monitoring application subscribes to `$q/farm/+/sensors` to retrieve all readings, including those from offline periods. With Last-Value Semantics enabled, only the latest sensor data per device is retained, simplifying data processing for irrigation decisions.

*Learn more about* [*Message Queue*](https://docs.emqx.com/en/emqx/latest/message-queue/message-queue-concept.html)*.* 

## Multi-Tenancy with Namespaced Roles

EMQX 6.0.0 takes multi-tenancy to the next level with namespaced roles in the Dashboard. This feature enhances role-based access control (RBAC) by restricting users to specific namespaces, making it easier to manage large-scale multi-tenant IoT deployments.

Namespaced roles empower administrators to manage multiple tenants efficiently, with each tenant operating in a self-contained environment. Users see only their namespace’s resources, such as Rules or Connectors, and start on a filtered Dashboard Overview page. 

### **Key Benefits:**

- **Secure Isolation**: Namespaced roles limit users to their assigned namespace (e.g., `ns:team_a::administrator`), ensuring data and resource isolation across tenants like teams, business units, or customers.
- **Granular Control**: Administrators have full control over namespace-specific resources (e.g., Connectors, Rules), while cluster-level settings remain read-only for namespaced users and editable only by global administrators.
- **Streamlined Management**: Easily create and assign namespaced roles (Administrator or Viewer) when adding users via the Dashboard, API, or CLI, reducing administrative overhead.
- **Enterprise-Ready**: Ideal for service providers or enterprises managing multiple clients or departments, enabling cloud-native, scalable IoT solutions with robust security.

### **Example Use Case**:

An IoV platform offers MQTT-as-a-service. Internal teams like fleet operations and maintenance operate as separate tenants. A user with the `ns:fleet_ops::administrator` role can manage `sensors/data` in `ns:fleet_ops` for bus tracking, while a user in `ns:maintenance` can use an identical `sensors/data` in `ns:maintenance` for diagnostics, without conflicts. Administrators set per-tenant resource limits (e.g., message throughput), ensuring fair allocation and preventing any team from overloading the cluster.

*For how to create a namespaced role, refer to* [*Create a User with a Namespaced Role*](https://docs.emqx.com/en/emqx/latest/dashboard/system.html#create-a-user-with-a-namespaced-role)*.* 

## Optimized Durable Storage for Better Performance

EMQX 6.0.0 optimizes durable storage by decoupling session data from the broker’s other metadata, significantly reducing RAM usage and enhancing storage efficiency, critical for large-scale IoT deployments.

For example, in a smart grid, millions of meter readings are stored durably. The optimized storage reduces memory usage, allowing the cluster to handle more devices without scaling hardware.

### **Key Improvements**:

- **Reduced Memory Footprint**: Optimized RocksDB memory usage with new configuration parameters:
  - `durable_storage.messages.rocksdb.write_buffer_size`: Controls memtable size per shard.
  - `durable_storage.messages.rocksdb.cache_size`: Sets block cache size per shard.
  - `durable_storage.messages.rocksdb.max_open_files`: Limits file descriptors per shard.
  - `durable_storage.messages.layout.wildcard_thresholds`: Tunes wildcard optimization for the wildcard_optimized_v2 layout.
- **New Serialization Schema**: Default changed to asn1 for more efficient message storage.
- **Enhanced Performance**: Improved storage efficiency ensures faster message retrieval and lower resource consumption.

## New and Enhanced Data Integrations

In EMQX 6.0.0, the data integration expands with support for [AWS AlloyDB](https://docs.emqx.com/en/emqx/latest/data-integration/alloydb.html), [CockroachDB](https://docs.emqx.com/en/emqx/latest/data-integration/cockroachdb.html), [AWS Redshift](https://docs.emqx.com/en/emqx/latest/data-integration/redshift.html), and [BigQuery](https://docs.emqx.com/en/emqx/latest/data-integration/bigquery.html), alongside enhancements to existing integrations for Snowflake, RocketMQ, S3 Tables, and RabbitMQ.

### New Supported Integrations

- **AWS AlloyDB, CockroachDB, and Redshift**: Stream MQTT data to these high-performance databases for real-time analytics and scalable storage. Perfect for enterprise-grade IoT analytics.
- **Google BigQuery**: Integrate MQTT data with BigQuery for large-scale data warehousing and advanced querying, enabling insights from massive IoT datasets.

### Integration Enhancements

- **Snowflake Snowpipe Streaming**: Support for Snowpipe Streaming (preview, AWS-hosted Snowflake accounts) enables low-latency data ingestion into Snowflake tables.
- **RocketMQ Action**: New key and tag template fields, plus a `key_dispatch` option for the Produce Strategy, allow greater customization of message metadata.
- **S3 Tables Connector**: `access_key_id` and `secret_access_key` are now optional, with automatic retrieval from EC2 Instance Metadata Service v2 APIs for seamless AWS integration.
- **RabbitMQ Sink**: Define custom Headers and Properties Templates to enhance message routing and compatibility within RabbitMQ.

## Advanced LLM-Based MQTT Data Processing

Building on the AI capabilities introduced in 5.10.0, EMQX 6.0.0 enhances LLM-based data processing with support for **Google Gemini** models, alongside OpenAI and Anthropic Claude. New APIs and configuration options make AI integration more robust and customizable.

### **Key Enhancements:**

- **Google Gemini Support**: Leverage Gemini’s advanced reasoning to build intelligent flows that analyze structured MQTT payloads, detect complex conditions across multiple fields, and generate precise, context-aware alerts.
- **New API Endpoint**: List all available models for an AI provider via a dedicated API, simplifying integration and model selection.
- **Transport Options**: Configure connection timeouts and maximum connections to AI Completion Providers for better performance and reliability.

*Explore processing LLM-based data with the new* [*Gemini node*](https://docs.emqx.com/en/emqx/latest/flow-designer/gemini-node-quick-start.html) *in Flow Designer.*

## Additional Enhancements

EMQX 6.0.0 includes numerous other improvements and bugfixes to enhance performance, security, and usability. 

- **License TPS Limits**: Adds Transactions Per Second (TPS) limits for Enterprise Licenses, capping the total MQTT messages processed across the cluster. Exceeding the limit triggers an observability alarm, without blocking message flow. Alarms persist until a higher TPS license is applied or manually cleared via Dashboard/CLI.
- **Enhanced Security**: Introduces client ID throttling during reconnects to prevent instability, client ID overriding via authentication results for flexible control, and ACL rules in LDAP authentication to reduce server queries. The default authorization flow action changes from `allow` to `deny`, bolstering security.
- **Improved Deployment**: Adds EMQX Operator and Helm Charts documentation, supports Debian 13 packages (discontinuing Debian 10), and introduces automatic trace log rotation and a “force deactivate alarm” API for better operational control.
- **Performance Boost**: Optimizes fanout MQTT scenarios for faster processing and reduces memory usage in the authorization flow, enhancing efficiency for large-scale deployments.

Stay tuned for the full changelog, which will detail additional features like enhanced observability, clustering improvements, and important bug fixes.

*View the [EMQX 6.0.0 Release Notes](https://www.emqx.com/en/changelogs/enterprise/6.0.0) for the complete list.*

## Ready to Experience EMQX 6.0.0?

Download EMQX Enterprise 6.0.0 from the official website and unlock the power of durable messaging, AI-driven insights, and multi-tenant IoT solutions. Build smarter, more scalable, and secure data pipelines today.

Need assistance or want to explore how EMQX 6.0.0 fits your IoT use case? Contact our team for a personalized consultation.



<section class="promotion">
    <div>
        Try EMQX for Free
    </div>
    <a href="https://www.emqx.com/en/try?tab=self-managed" class="button is-gradient">Get Started →</a>
</section>
