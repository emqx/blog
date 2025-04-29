We're thrilled to announce the latest EMQX Cloud release (if you haven't seen the full update yet, check it out [here](https://www.emqx.com/en/blog/discover-whats-new-in-emqx-cloud)!). One of the most exciting new features on our Dedicated plan is **Cluster Linking**. 

If you've ever needed to synchronize MQTT data across different regions, bridge hybrid environments, or build highly resilient architectures, this feature is built for you. In this blog, we will deep dive into this powerful capability and explore how it can supercharge your EMQX Cloud deployments.

![image.png](https://assets.emqx.com/images/bd32ae0d8fefc9bd4e03b75c6e219d1f.png)

## **What Is Cluster Linking?**

Think of Cluster Linking as a dedicated, high-speed highway connecting two or more independent EMQX clusters. It's a **native feature** built into EMQX, designed specifically to efficiently and reliably synchronize real-time MQTT messages across geographically distributed or logically separated deployments.

Compared to traditional MQTT bridging, Cluster Linking is more efficient, scalable, and tolerant of network interruptions. It reduces bandwidth usage and forwards specific topics from one cluster to another, either one-way or bidirectionally. In short, it’s like giving your MQTT clusters a direct, private line to communicate — no matter where they’re deployed.

## **Why Cluster Linking Matters**

Cluster Linking isn't just another feature, it's a solution to some of the biggest challenges in scaling MQTT deployments:

- **Breaking Down Geographic Barriers:** Need to serve users or devices across the globe? Cluster Linking lets you replicate data between EMQX Cloud deployments in different regions (e.g., US East to EU West), ensuring low latency for local clients while maintaining a consistent global data network.
- **Boosting Reliability and Availability:** Set up active-active configurations across availability zones or regions. If one cluster runs into issues, the linked cluster(s) maintain data flow, boosting your application's resilience and enabling disaster recovery scenarios.
- **Simplifying Data Distribution and Segregation:** Whether you need to sync specific topics between dev, test, and production environments, or aggregate data from multiple edge clusters into a central cloud cluster, Cluster Linking makes complex routing easier and more reliable.
- **Scaling Without Silos**: As your IoT ecosystem grows, you might need to split workloads across clusters for performance or compliance. Cluster Linking keeps everything connected so you can scale without breaking your architecture.
- **Streamlining Your Architecture**: Forget about managing multiple brokers or building custom integrations, Cluster Linking is baked right into EMQX, making setup and maintenance a breeze.

In short: Cluster Linking helps you build more **scalable, resilient, geographically distributed** MQTT applications with less complexity.

## **Where Cluster Linking Shines**

**Global Automotive and Connected Vehicles**

In the automotive world, real-time data exchange across regions is critical. Cluster Linking ensures low-latency communication and high availability as vehicles move between regions — powering use cases like:

- Real-time traffic updates
- Vehicle-to-everything (V2X) communication
- Autonomous driving systems
- Fleet management across multiple countries

![image.png](https://assets.emqx.com/images/344f9b20f764557d147442aede5f8db8.png)

**Manufacturing and Industrial IoT**

Global manufacturers can synchronize production lines, monitor equipment health, and perform predictive maintenance across multiple facilities worldwide — all through a unified MQTT network powered by Cluster Linking.

**Multi-Region Deployment and Disaster Recovery**

Businesses can implement robust multi-region strategies with automatic failover. If one region goes down, client connections can seamlessly switch to another — ensuring business continuity for mission-critical IoT applications.

## **Cluster Linking vs. MQTT Bridge: Key Difference**

This is a great question! While both Cluster Linking and MQTT bridging move messages between brokers, they serve different purposes:

|                    | MQTT Bridge                                         | Cluster Linking                                        |
| ------------------ | --------------------------------------------------- | ------------------------------------------------------ |
| Type               | MQTT client-based                                   | Native EMQX Feature                                    |
| Use Case           | Connecting EMQX to any MQTT broker                  | High-performance synchronization between EMQX clusters |
| Performance        | Standard MQTT client behavior                       | Optimized for EMQX-EMQX communication                  |
| Routing            | Forwards all messages, even if no subscribers exist | Intelligently forwards only needed messages            |
| Namespace          | Separate topic namespaces; manual mapping required  | Unified namespace across clusters                      |
| Bidirectional Flow | Requires extra setup                                | Built-in with automatic loopback prevention            |

**Think of it this way:** MQTT Bridge is like using public roads — flexible, but subject to traffic. Cluster Linking is like a private high-speed rail line — faster, more reliable, and purpose-built for EMQX Clusters.

![image.png](https://assets.emqx.com/images/6cabaa751f53d5016bae94fba465be1f.png)

**When to Use Which?**

- Use **Cluster Linking** when you want optimized, resilient data synchronization between EMQX clusters (especially across regions). 
- Use **MQTT Bridge** when connecting EMQX to other MQTT brokers or when you need flexible, cross-platform interoperability.

## **Ready to Link Your Clusters? Let’s Get Started!**

Cluster Linking is now available on the EMQX Cloud Dedicated Plan — and setting it up is straightforward through the EMQX Cloud Console.

- **New to EMQX Cloud?** [Sign up for a free trial](https://accounts.emqx.com/signup?continue=https%3A%2F%2Fcloud-intl.emqx.com%2Fconsole%2Fdeployments%2Fnew)
- **Already using EMQX Cloud?** [Log in](https://accounts.emqx.com/signin?continue=https%3A%2F%2Fcloud-intl.emqx.com%2Fconsole%2Fdeployments%2Fnew) to your console and explore Cluster Linking
- **Prefer cloud marketplaces?** EMQX Cloud is available on [AWS](https://aws.amazon.com/marketplace/pp/prodview-g6zejrbcad6mu), [Azure](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/emqtechnologiesincorporated1678779968155.emqx_cloud?tab=Overview), and [Google Cloud](https://console.cloud.google.com/marketplace/product/emq-public-380104/emqx-cloudpay-as-you-go?pli=1) marketplaces

We believe Cluster Linking will open powerful new possibilities for your MQTT architectures. 

We can't wait to see what you build with it!
