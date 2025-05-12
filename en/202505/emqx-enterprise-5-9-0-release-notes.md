We're excited to unveil **EMQX Enterprise 5.9.0**, the latest milestone in our mission to deliver the world's most scalable and reliable MQTT messaging platform. This release introduces a new license model designed to support continued innovation and enhanced user support. 

> For detailed information about the new license model, refer to [this blog](https://www.emqx.com/en/blog/adopting-business-source-license-to-accelerate-mqtt-and-ai-innovation). 

Alongside this, groundbreaking features like Namespace and Smart Data Hub are introduced to empower businesses to build efficient, intelligent, and secure IoT ecosystems. Let’s explore what’s new!

## Namespace: Deploy Multi-Tenancy with Ease and Efficiency

The new [Namespace](https://docs.emqx.com/en/emqx/latest/multi-tenancy/namespace.html) feature simplifies multi-tenancy by allowing isolated tenant configurations within a single EMQX cluster. Each namespace can be customized with tenant-specific settings, such as rate limits. This ensures operational efficiency, resource optimization, and data privacy for each tenant without deploying multiple clusters.

**Key Benefits**:

- **Seamless Multi-Tenancy**: Support diverse tenants—such as departments, customers, or applications—within a single cluster, reducing infrastructure overhead.
- **Easy Configuration**: Create and manage namespaces via the EMQX HTTP API or Dashboard.
- **Per-Tenant Controls**: Apply rate limiters and other policies at the namespace level.
- **Enhanced Scalability**: Manage thousands of tenants efficiently, making it ideal for smart cities or connected vehicle platforms.

For example, a connected vehicle platform can create a namespace for a tenant (e.g., `tenant-a`) using the HTTP API and configure a tenant-specific rate limiter to restrict connections to 10 per second. This ensures `tenant-a` operates within defined resource boundaries, maintaining performance isolation within the same EMQX cluster.

## Smart Data Hub: All-in-One Solution for Intelligent Data Processing

The [Smart Data Hub](https://docs.emqx.com/en/emqx/latest/data-integration/smart-data-hub.html) in version 5.9.0 integrates essential data processing capabilities like Schema Registry, Schema Validation, and Message Transformation into a cohesive solution. A highlight of this release is support for the External HTTP Server schema in Schema Registry, which enhances flexibility for schema management.

**Key Components and Enhancements**:

- **Schema Registry**: Centrally manage Avro, Protobuf, and JSON schemas. The new External HTTP Schema Registry allows EMQX to fetch schemas dynamically from external HTTP servers, simplifying integration with third-party systems and enabling real-time schema updates without modifying the EMQX cluster.
- **Schema Validation**: Enforces data integrity by validating incoming messages against predefined schemas, reducing errors in downstream processing.
- **Message Transformation**: Transforms message payloads in real time (e.g., filtering, enriching, or reformatting), enabling seamless data integration with databases, AI/ML platforms, or analytics tools.

For instance, in a connected vehicle platform, the Smart Data Hub can validate sensor data against a Protobuf schema fetched from an external HTTP server, transform it for compatibility with a cloud analytics platform, and deliver real-time insights to optimize vehicle performance. This integration makes the Smart Data Hub a cornerstone for industries like manufacturing, logistics, and smart energy.

## Fallback Actions: Ensuring Reliable Data Integration

New [Fallback Actions](https://docs.emqx.com/en/emqx/latest/data-integration/data-bridges.html#fallback-actions) ensure reliable data integration, even in the face of failures. When a data integration fails to deliver messages to an external system (e.g., due to network issues or service unavailability), fallback actions allow you to define alternative handling strategies, such as storing messages in a buffer, redirecting them to another Sink, or logging them for later analysis. This ensures that critical IoT data is not lost, even during transient failures.

For example, in a smart energy grid, if a primary data integration to a cloud analytics platform fails, fallback actions can redirect meter data to a local buffer, ensuring no data is lost until connectivity is restored.

## Enhanced Security: Robust Protection for Your IoT Infrastructure

Security is paramount in IoT, and EMQX Enterprise 5.9.0 introduces a suite of advanced security features to safeguard your deployments. These enhancements provide granular control and robust administrative protections.

### Authenticator Preconditions

The [Authenticator Preconditions](https://docs.emqx.com/en/emqx/latest/access-control/authn/authn.html#authenticator-preconditions) feature implements conditional logic in the authentication chain to optimize authentication workflows and reduce backend load. It allows EMQX to apply different authenticators for clients connecting through different listeners or based on client attributes. EMQX can then invoke authenticators only when appropriate and avoid unnecessary requests to external systems.

### Multi-Factor Authentication

EMQX Enterprise 5.9.0 introduces [Multi-Factor Authentication (MFA)](https://docs.emqx.com/en/emqx/latest/multi-factor-authn/multi-factor-authentication.html) for the EMQX Dashboard. Administrators and users must authenticate using a primary credential (password) and a secondary factor, such as a time-based one-time password (TOTP) generated by an authenticator app. MFA can be enabled via the Dashboard, ensuring secure access to critical management functions.

### Account Lockout and Unlock

The [Account Lockout and Unlock](https://docs.emqx.com/en/emqx/latest/dashboard/introduction.html#account-lockout-and-unlock) feature protects against brute-force attacks by temporarily locking user accounts after a configurable number of failed login attempts. Administrators can unlock accounts manually via the Dashboard or configure automatic unlocking after a set period, ensuring a balance between security and user convenience.

### Password Expiration

The [Password Expiration](https://docs.emqx.com/en/emqx/latest/dashboard/introduction.html#password-expiration) feature allows administrators to enforce periodic password updates for Dashboard users, enhancing security by minimizing long-term credential exposure. Users are prompted to update their passwords before expiration, maintaining uninterrupted access.

Together, these security enhancements make EMQX Enterprise 5.9.0 one of the most secure MQTT platforms available, ready for regulated and mission-critical IoT deployments.

## Other Enhancements and Important Bug Fixes

EMQX Enterprise 5.9.0 includes several performance optimizations, observability improvements, and critical bug fixes to enhance the platform’s reliability and usability.

### Node-Level Cache for External Authentication and Authorization

This feature improves throughput by caching [authentication](https://docs.emqx.com/en/emqx/latest/access-control/authn/authn.html#external-resource-cache)/[authorization](https://docs.emqx.com/en/emqx/latest/access-control/authz/authz.html#external-resource-cache) results locally at the node level—reducing response times and backend load.

### Disk Log Data Integration

The [Disk Log Data Integration](https://docs.emqx.com/en/emqx/latest/data-integration/disk-log.html) feature enables EMQX to persist event data to disk. This allows for retention of event data, which is valuable for troubleshooting or historical analysis.

### OpenTelemetry End-to-End Trace Support for Rule Engine

OpenTelemetry end-to-end trace support for the Rule Engine enables comprehensive monitoring of data flows through rules and actions. This improves observability, making it easier to debug and optimize complex data pipelines.

### Enhanced MQTT Rate Limiting with Burst Support

Enhanced MQTT rate limiting now supports burst capacity, allowing temporary spikes in connections or message rates. Configurable via the Dashboard or configuration file, it ensures stable performance during peak loads in applications like smart metering.

### Additional Key Enhancements and Fixes

- **Improved Performance of Durable Sessions (**[#14498](https://github.com/emqx/emqx/pull/14498)**)**: Optimized session handling so that idle durable sessions no longer consume CPU resources. Also fixed an issue with the QoS upgrade feature to ensure subscribers only receive messages at their subscribed QoS level, improving both efficiency and delivery accuracy.
- **Cluster Linking Route Replication Fixes (**[#15067](https://github.com/emqx/emqx/pull/15067)**)**: Resolved several issues affecting route replication, including reconnect loops caused by misconfigurations, crashes when closing nonexistent MQTT client connections, and failures during replication bootstrapping with shared subscriptions.

These enhancements and fixes make EMQX Enterprise 5.9.0 more performant, reliable, and observable, ensuring a robust foundation for enterprise IoT deployments. For more information, refer to the [Release Notes](https://docs.emqx.com/en/emqx/latest/changes/changes-ee-v5.html#_5-9-0).

## Get Started with EMQX Enterprise 5.9.0

EMQX Enterprise 5.9.0 is now available on our [official website](https://www.emqx.com/en/try?tab=self-managed). Whether you’re scaling multi-tenant platforms, processing data in real time, or securing mission-critical deployments, this version has you covered. 

Download EMQX Enterprise 5.9.0 today, explore the new features, and see how EMQX can transform your IoT strategy. For questions or to discuss your use case, reach out to our [sales team](https://www.emqx.com/en/contact).



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?tab=self-managed" class="button is-gradient">Get Started →</a>
</section>
