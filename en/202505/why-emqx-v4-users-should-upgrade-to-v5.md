## Introduction

As an industry-leading MQTT platform, EMQX can connect, move, process, and integrate real-time data from millions of devices, transforming it into valuable insights for business applications.

If you're using EMQX 4.x, you already know how powerful EMQX is for handling MQTT messaging at scale. But as IoT deployments grow, the demands for higher performance, enhanced security, and seamless integrations are increasing.

With EMQX 5.x, we've addressed the limitations of EMQX 4.x and introduced game-changing improvements that make your IoT infrastructure faster, more secure, and easier to manage.

Still wondering if upgrading is worth it? Let’s break it down.

## Why Upgrade: Key Features and Enhancements in EMQX 5.x

### Scale Beyond Limits: Higher Throughput, Lower Latency

If your EMQX 4.x deployment struggles with scaling, high latency, or resource consumption, EMQX 5.x solves these issues with a more efficient cluster architecture.

EMQX 4.x used the Mria cluster architecture, where each node stored full session and routing data, causing high memory usage and slower synchronization as clusters grew. In contrast, EMQX 5.x introduces a [Core+Replicant architecture](https://docs.emqx.com/en/emqx/latest/deploy/cluster/mria-introduction.html):

- Core nodes manage authentication, session state, and cluster control.
- Replicant nodes relay messages without storing session data, reducing memory overhead and improving scalability.

This decoupled design allows clusters to scale up to 100 million+ connections, with auto-discovery and dynamic scaling eliminating manual node management.

| **Performance Metric**          | **EMQX 4.x**           | **EMQX 5.x**                       | **Why Upgrade?**                    |
| :------------------------------ | :--------------------- | :--------------------------------- | :---------------------------------- |
| Maximum Connections per Cluster | ~10 million            | 100 million+                       | 10x scalability increase            |
| Latency                         | ~50ms under heavy load | Sub-10ms response time             | Lower response time                 |
| Cluster Scaling                 | Manual node management | Auto-discovery and dynamic scaling | No more manual intervention         |
| Load Balancing                  | Basic round-robin      | Intelligent workload distribution  | More efficient resource utilization |

If you're experiencing slowdowns under high traffic, upgrading to EMQX 5.x will drastically improve reliability, reduce resource usage, and ensure seamless scaling.

### More Powerful Rule Engine & Data Integration: Process IoT Data Smarter

EMQX 4.x’s Rule Engine has limited flexibility when handling complex data transformations and real-time processing. EMQX 5.x addresses these limitations with the [Smart Data Hub](https://www.emqx.com/en/blog/introducing-emqx-platform-smart-data-hub), a comprehensive solution that introduces advanced capabilities such as schema registry, schema validation, and message transformation.

#### Example: Real-Time IoT Sensor Data Processing with Smart Data Hub

Imagine a smart factory that uses MQTT to collect temperature, humidity, and machine status data from thousands of IoT sensors. The challenge is ensuring incoming messages are validated, structured, and efficiently routed to multiple destinations, including a cloud database, real-time dashboard, and an AI-driven analytics engine.

**In EMQX 4.x**

- The rule engine could only filter messages based on simple SQL-like conditions, requiring external tools for data transformation.
- If data needed to be sent to multiple systems, users had to manually configure separate rules for each destination.
- No built-in schema validation, meaning incorrectly formatted messages could cause errors in downstream applications.

**In EMQX 5.x with Smart Data Hub**

- **Schema validation ensures data accuracy:** Incoming MQTT messages are automatically checked against predefined schemas. This prevents incorrect formats from being processed, ensuring data quality.

- **Message transformation eliminates middleware:** Using jq-based transformations, raw MQTT messages like:

  ```json
  {
    "device_id": "sensor_001",
    "temperature": "25.5",
    "humidity": "60"
  }
  ```

  can be transformed within EMQX into a structured format:

  ```json
  {
    "sensor_id": "sensor_001",
    "metrics": {
      "temperature": 25.5,
      "humidity": 60
    },
    "timestamp": "2024-03-03T12:00:00Z"
  }
  ```

  This means data arrives in the correct structure without external processing.

- **Schema registry maintains consistency:** All sensors follow a centralized schema, making it easy to enforce data standards across the entire IoT system.

- **Automated multi-destination routing:** Instead of configuring multiple rules manually, the event-driven rule engine automatically routes transformed and validated messages to multiple destinations simultaneously, using EMQX’s built-in [data integration](https://docs.emqx.com/en/emqx/latest/data-integration/data-bridges.html) capabilities:

  - A cloud database for historical storage (e.g., PostgreSQL, MySQL, MongoDB, AWS RDS).
  - A real-time monitoring dashboard for instant visualization (e.g., InfluxDB, Prometheus, which feeds Grafana or Kibana dashboards).
  - An AI analytics engine for predictive maintenance insights (Apache Kafka or Google Pub/Sub, which connects to an AI-driven analytics engine).

- **Fewer manual configurations, faster insights:** With built-in event triggers and automation, messages are processed instantly based on predefined rules. In addition, a powerful visual tool “[Flow Desginer](https://docs.emqx.com/en/emqx/latest/flow-designer/introduction.html)” helps you make the configuration of data processing and integration simpler and more efficient.

If you need real-time, structured, and high-quality IoT data processing, upgrade to EMQX 5.x to fully automate and optimize your IoT data processing.

### Enterprise-Grade Security: Advanced Authentication & Compliance

Security is more critical than ever, especially with large-scale IoT deployments. EMQX 4.x provided basic security features, but EMQX 5.x takes security to the next level.

| **Security Feature**   | **EMQX 4.x**                                                 | **EMQX 5.x**                                                 | **Why Upgrade?**                            |
| :--------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :------------------------------------------ |
| Authentication Methods | X.509 Certificate, Username/password (via external databased and services), JWT | X.509 Certificate, Username/password (via external databased and services), JWT<br>MQTT 5.0 Enhanced Authentication (SCRAM, Kerberos)<br>Single Sign-On (SSO) | More flexible and secure authentication     |
| Access Control         | Basic ACLs                                                   | Granular Role-Based Access Control (RBAC)                    | More precise permission management          |
| Encryption Support     | One-way TLS                                                  | One-way and mutual TLS (Faster & More Secure)                | Stronger encryption with better performance |
| Regulatory Compliance  | Limited support                                              | GDPR, HIPAA, ISO 27001 compliant                             | Meet industry security standards easily     |

If you’re working with sensitive IoT data, EMQX 5.x ensures your system is compliant with the latest security standards.

### Better Observability & Monitoring: Gain Real-Time Insights

In EMQX 4.x, troubleshooting was often time-consuming due to limited visibility into MQTT message flow and system performance. Debugging required manual log analysis, and tracking message delivery paths was not intuitive, leading to delays in identifying issues.

EMQX 5.x dramatically improves observability and monitoring with a user-friendly Dashboard UI, built-in tracing tools, and enhanced visual monitoring features.

#### What’s New in EMQX 5.x for Monitoring & Troubleshooting?

- Redesigned Dashboard UI
  - Offers enhanced real-time observability with more in-depth metrics. For example, in v4, you could see total message rates per node, but in v5, you can break it down by topic, client, or authentication mechanism.
  - EMQX v5 expands the scope of metrics, tracking not just system-level performance but also application-level behaviors, such as authentication and authorization performance, and rule engine execution time & success/failure count.
- EMQX v5 can directly export metrics to [Datadog](https://docs.emqx.com/en/emqx/latest/observability/datadog.html), a cloud-based observability and security platform, allowing real-time monitoring of MQTT broker performance in the Datadog dashboard.
- Unified Tracing, Metrics, and Logging with [OpenTelemetry](https://docs.emqx.com/en/emqx/latest/observability/opentelemetry/opentelemetry.html)
  - EMQX v5 integrates native OpenTelemetry support, allowing users to collect metrics in tracing systems like Jaeger.
  - Users can correlate logs, traces, and metrics for in-depth debugging.
- Machine (indexer) friendly structured logs in JSON format. Error logs are consistently tagged with 'msg' tokens to facilitate locating the cause of the problem.

If you're spending too much time troubleshooting or struggling with limited visibility in EMQX 4.x, upgrading to EMQX 5.x will make monitoring, debugging, and optimizing your MQTT infrastructure easier than ever.

### MQTT Over QUIC: Faster, More Reliable, and Built for the Future

Traditional MQTT relies on TCP, which can struggle with latency, congestion, and unreliable mobile networks. EMQX 5.x introduces [MQTT over QUIC](https://docs.emqx.com/en/emqx/latest/mqtt-over-quic/introduction.html), a next-generation transport protocol designed to enhance speed, reliability, and security.

| **Feature**                      | **EMQX 4.x (TCP-based MQTT)**               | **EMQX 5.x (MQTT over QUIC)**                               | **Why Upgrade?**           |
| :------------------------------- | :------------------------------------------ | :---------------------------------------------------------- | :------------------------- |
| Connection Establishment         | Slow multi-step TCP handshake.              | Faster QUIC handshake with built-in TLS 1.3.                | Reduces connection time.   |
| Performance in Unstable Networks | Packet loss causes delays.                  | QUIC recovers lost packets without blocking other messages. | More reliable messaging.   |
| Reconnection Time                | Requires full TCP/TLS re-negotiation.       | Near-instant reconnections with 0-RTT resumption.           | Reduces downtime.          |
| Security                         | Separate TCP and TLS layers add complexity. | QUIC has built-in TLS 1.3 for encryption.                   | More secure and efficient. |

#### When Should You Use MQTT over QUIC?

- IoT applications with frequent network switching (e.g., mobile, vehicle tracking, smart wearables).
- Low-latency industrial IoT scenarios that require real-time updates.
- Edge computing use cases where reducing connection overhead is critical.

By upgrading to EMQX 5.x, users can take advantage of MQTT over QUIC to ensure faster, more reliable, and secure communication, especially in challenging network environments.

## How to Upgrade: Ease of Upgrade and Migration Path

Migrating from EMQX 4.x to 5.x is designed to be smooth and low-risk, ensuring minimal disruptions to existing deployments.

#### Key Improvements in the Upgrade Process

- **Backward Compatibility:** EMQX 5.x supports legacy MQTT clients and authentication mechanisms used in EMQX 4.x.
- **Automated Data Migration:** EMQX provides detailed migration guides and automated scripts to simplify configuration and rule conversion. Configuration, authentication data, and message routing rules can be migrated with minimal manual effort.
- **Zero-Downtime Upgrades:** Starting with EMQX 5.1, the system supports seamless rolling upgrades for the cluster. With rolling upgrade support, clusters can be upgraded one node at a time, keeping connections active and preventing service interruptions.

With EMQX 5.x’s automated tools, transitioning from 4.x is seamless, with minimal disruption to your IoT operations. For detailed steps to upgrade, refer to: [Upgrade EMQX Cluster from 4.4 to 5.x | EMQX Docs](https://docs.emqx.com/en/emqx/latest/deploy/upgrade-cluster.html).

## Long-Term Support and Future-Proofing

Upgrading to EMQX 5.x is not just about gaining better performance and new features—it is a strategic investment in long-term stability, security, and future readiness.

### Long-Term Support for EMQX 5.x

EMQX 5.x is the latest major version designed with a focus on long-term stability and ongoing improvements, including continuous security updates, bug fixes, and performance improvements. Users upgrading from EMQX 4.x benefit from:

- Regular security patches to address emerging threats and vulnerabilities.
- Optimized performance updates to ensure high throughput and low latency.
- Compatibility with upcoming MQTT protocol enhancements, keeping deployments aligned with industry best practices.
- Enterprise-grade reliability, reducing risks of technical debt and outdated infrastructure.

Staying on EMQX 4.x means missing out on these critical updates, increasing the likelihood of performance degradation, security risks, and compatibility issues as the IoT ecosystem evolves.

### Staying Ahead with Emerging Technologies

EMQX 5.x is designed to keep pace with modern IoT demands, integrating cutting-edge features that provide a competitive advantage for businesses.

- Multi-Tenancy Support
- AI-Driven Data Processing
- Cloud-Native Optimization
- Next-Generation Connectivity
- Improved Monitoring & Troubleshooting

## Customer Success Story with EMQX 5.x

### A Technology Company Improved Authentication Management with EMQX 5.x

**Challenge:** A technology company providing real-time data solutions faced challenges in EMQX Platform v4 with managing authentication priorities. Their system relied on multiple authentication sources, but there was no way to control their execution order, making troubleshooting difficult and authentication handling inefficient.

**Solution:** After upgrading to EMQX 5.x, the new authentication order feature allowed administrators to:

- Customize authentication priority through a drag-and-drop interface.
- Improve troubleshooting by providing real-time visibility into the authentication flow.

**Result:** The upgrade helped the company reduce authentication failures, enhance system monitoring, and optimize login processing, ensuring a more reliable and efficient authentication workflow.

For businesses managing multiple authentication sources, EMQX 5.x simplifies authentication control and enhances system security, making it a valuable upgrade from v4.

### An IoT Company Enhanced Data Processing with EMQX 5.x

**Challenge:** A company in the IoT industry needed a more efficient way to process MQTT messages in EMQX Platform. In EMQX v4, limited rule SQL functionality made it hard to extract nested JSON fields, restructure data, and apply advanced filtering. This forced them to use external tools, increasing system complexity and latency.

**Solution:** After upgrading to EMQX 5.x, the company was able to leverage JQ functions within the rule engine, allowing them to extract specific fields from nested JSON, restructure payloads, and apply custom filtering rules directly in their rule SQL queries.

Additionally, independent action metrics in EMQX 5.x’s data integration provided better visibility into each processing step, making it easier to troubleshoot issues and identify performance bottlenecks. 

**Result:** The company welcomed the upgrade, saying:
*"I am very welcome to upgrade the setup from v4 to v5. Since our setup is straightforward, I guess it will be no problem to be a pilot for beta test of the upgrade."*

With this transition, they eliminated unnecessary external processing, streamlined their data transformation workflows, and gained better visibility into system performance.

## Conclusion: Upgrade Now to Future-Proof Your IoT Infrastructure

If you’re still on EMQX 4.x, you’re missing out on massive improvements in performance, security, and scalability. Here’s why you should upgrade today:

- 10x scalability (100M+ connections supported)
- 5x lower latency for real-time responsiveness
- Seamless integrations with databases, cloud services & analytics tools
- Enterprise-grade security & compliance
- Zero-downtime upgrades & Kubernetes-native auto-scaling

Start your migration today and unlock the full potential of EMQX 5.x!

Want expert help? [Contact us](https://www.emqx.com/en/contact) now for a consultation!
