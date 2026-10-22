HiveMQ is retiring its Cloud Serverless Free and Pay As You Go plans on **December 31, 2026**. If you're currently running MQTT workloads on either plan, you'll need to move your devices and applications to another broker before the deadline.

For developers and organizations relying on HiveMQ Cloud Serverless, this may mean an unexpected migration, additional development work, and limited time to evaluate alternatives. Whether you're managing a small project or a production deployment, changing MQTT brokers requires careful planning, especially when your applications depend on uninterrupted connectivity.

Fortunately, moving to another broker doesn't have to mean rebuilding your applications or managing your own infrastructure. [EMQX Cloud](https://www.emqx.com/en/cloud) offers a fully managed MQTT service with flexible deployment options to support your transition.

We've seen significant interest in EMQX Cloud as an alternative, and we're helping developers and organizations explore their options and prepare for the transition.

## What's Happening to HiveMQ Cloud Serverless?



According to [HiveMQ's official end-of-life documentation](https://docs.hivemq.com/hivemq-cloud/serverless-end-of-life.html), both Serverless Free and Serverless Pay As You Go clusters will be retired on December 31, 2026.

Here's what existing users need to know:

- **New Serverless clusters are no longer available.** Users can no longer create new clusters or upgrade existing ones to Pay As You Go.
- **MQTT connectivity will end.** Devices and applications still connected to affected clusters will lose access after the deadline.
- **Cluster data will be permanently deleted.** This includes retained messages, client sessions, access credentials, and permissions.
- **Migration is not automatic.** Customers are responsible for moving their clients, configurations, and any data they need to preserve.

HiveMQ is offering eligible customers a free, 12-month license for its self-managed Enterprise Broker, limited to 100 concurrent connections and 100 messages per second. Customers can also explore HiveMQ's other paid and managed offerings.

However, for teams that originally chose Serverless to avoid maintaining their own infrastructure, moving to a self-managed broker may not be the right fit.

## Why Choose EMQX Cloud?



EMQX Cloud is a multicloud MQTT platform managed by EMQ, which serves more than 1,500 customers worldwide and supports over 500 million connected devices.

For HiveMQ Cloud Serverless users, the goal is simple: find a reliable replacement that supports their existing applications without adding unnecessary complexity. EMQX Cloud offers several advantages that can help make that transition easier.

### Continue with Fully Managed MQTT



If you're accustomed to a managed MQTT service, there's no need to start provisioning servers, maintaining broker software, or handling infrastructure upgrades yourself.

EMQX Cloud manages the underlying broker infrastructure, allowing your team to focus on connecting devices, developing applications, and working with your IoT data.

### Keep Using Your Existing MQTT Clients



EMQX Cloud supports MQTT 3.1, 3.1.1, and 5.0, along with standard MQTT features such as publish/subscribe messaging, QoS levels, retained messages, and shared subscriptions.

Because both platforms use MQTT, you can generally continue using your existing MQTT clients and SDKs rather than rewriting applications around a different protocol.

You'll still need to update broker endpoints, credentials, and potentially TLS or authorization settings. Any broker-specific behavior should also be tested before moving production traffic.

### Connect MQTT Data to More Systems



For applications that need more than MQTT messaging, EMQX Cloud also offers built-in data processing and integration capabilities.

Depending on your deployment plan, you can filter, transform, and route MQTT messages to databases, analytics platforms, cloud services, and other applications without building every integration from scratch.

These capabilities can support your applications as they grow, but you can also start with the MQTT connectivity you need today.

## Choosing the Right EMQX Cloud Deployment



If you're moving from HiveMQ Cloud Serverless, two EMQX Cloud deployment options are worth considering: Serverless and Dedicated Flex.

### EMQX Cloud Serverless



For smaller projects, development environments, and applications with variable traffic, EMQX Cloud Serverless offers:

- Usage-based pricing with a free monthly quota
- Support for up to 1,000 concurrent connections
- MQTT connectivity over TLS and secure WebSockets
- A straightforward way to create a deployment and test your existing MQTT clients

Serverless has [limits](https://docs.emqx.com/en/cloud/latest/create/restriction.html) on connections, message throughput, subscriptions, and supported connection methods. Be sure to confirm that your workload fits within these limits before migrating.

### EMQX Cloud Dedicated Flex



For applications that need additional capacity, dedicated infrastructure, or more advanced networking and integration capabilities, Dedicated Flex offers:

- Isolated MQTT cluster resources
- Flexible connection and messaging capacity
- Advanced authentication and authorization options
- Private networking capabilities
- Additional data processing and integration features

Choosing between Serverless and Dedicated Flex depends on your workload, connection requirements, and the capabilities your applications need.

You can compare features and pricing in the [EMQX Cloud documentation](https://docs.emqx.com/en/cloud/latest/price/plans.html) or on our [pricing page](https://www.emqx.com/en/pricing).

## Preparing for Your Migration



Moving between MQTT brokers requires some preparation, particularly if you're managing production devices or applications that depend on continuous connectivity.

Before making the switch, it's important to understand your current workload, evaluate your deployment requirements, and identify any configurations or broker-side data that need to be preserved. Testing your new environment while your existing HiveMQ cluster is still running can also help reduce the risk of disruption.

## Up Next: A Step-by-Step Migration Guide



This article is the first in our two-part series to help HiveMQ Cloud Serverless users transition to EMQX Cloud.

While we've covered what you need to know and how to prepare, our upcoming **step-by-step migration guide** will walk through the technical process, including deployment setup, configuration examples, screenshots, and testing your MQTT connections.

## Make the Move Before December 31



With the December 31 deadline fast approaching, now is the time to begin planning your transition. Starting early will give you room to evaluate your options, complete the migration, and avoid unnecessary disruption.

Our team is here to help you evaluate EMQX Cloud and find a deployment that fits your needs.

Ready to explore your options?

Visit our [HiveMQ Cloud migration page](https://go.emqx.com/hivemq-cloud-migration) to compare EMQX Cloud deployment options, review our migration checklist, and get help planning your move.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
