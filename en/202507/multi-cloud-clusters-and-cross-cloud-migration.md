## Introduction

Imagine losing millions in revenue because a single cloud provider’s outage halts your operations. The GCP global outage in June 2025 exposed this harsh reality, disrupting services for countless businesses worldwide. This is why multi-cloud strategies are gaining traction, enabling organizations to distribute workloads across providers like AWS, GCP, and Azure to avoid vendor lock-in, boost cost efficiency, and eliminate single points of failure. However, multi-cloud deployments come with challenges like management complexity and data portability. EMQX Cluster Linking, a powerful feature of the EMQX MQTT platform, offers a seamless solution for connecting clusters across clouds, ensuring flexibility, scalability, and resilience for your IoT infrastructure.

> Learn more about Cluster Linking: [Cluster Linking Deep Dive: Unlock Global Scale & Resilience on EMQX Cloud](https://www.emqx.com/en/blog/cluster-linking-deep-dive) 

## Why Cluster Linking is Essential for Multi-Cloud Deployment

Cluster Linking addresses the inherent challenges of distributed systems across diverse cloud environments, transforming independent clusters into a cohesive and resilient messaging platform. 

- **Builds a Unified, Resilient Platform:** Cluster Linking connects EMQX clusters deployed across different cloud platforms and regions, creating a system where all clusters act as one cohesive MQTT messaging platform, regardless of their cloud provider. This allows clients to connect to any cluster and communicate seamlessly with devices connected to other clusters, while also significantly enhancing **high availability and disaster recovery**. Should one cloud platform or region experience an outage, the interconnected clusters in another cloud can seamlessly take over, ensuring continuous service and business continuity.
- **Enables Seamless Cross-Cloud Communication and Routing:** Traditional inter-cloud communication for MQTT messages is complex and inefficient due to network isolation between different cloud platforms. Cluster Linking provides an optimized, built-in solution for **efficiently and reliably routing MQTT messages** between these disparate cloud clusters. This ensures messages are accurately delivered from publishers to subscribers, regardless of which cloud they're connected to.
- **Facilitates True Multi-Cloud Architecture and Reduces Vendor Lock-in:** Without Cluster Linking, EMQX deployments across multiple clouds would remain isolated, independent clusters. Cluster Linking is the **key component to achieving a true, unified, and collaborative multi-cloud MQTT infrastructure**. By enabling this interconnectedness, it empowers businesses to avoid over-reliance on a single cloud provider, offering greater flexibility in choosing the most suitable and cost-effective cloud services for their needs.
- **Simplifies Operations:** Manually managing message synchronization and routing across different cloud environments is incredibly complex and prone to errors. Cluster Linking abstracts away this complexity, making the **operation and maintenance of multi-cloud deployments significantly simpler and more controllable**.

## Multi-Cloud Cluster Linking: A Hands-On Example

This section demonstrates how to deploy EMQX clusters across multiple cloud providers. Please note that this demonstration focuses on the cluster linking under the same EMQX Platform account. For detailed instructions on linking across different accounts or to a self-hosted broker, refer to the [official documentation](https://docs.emqx.com/en/cloud/latest/cluster_linking/cluster_linking.html).

### Prerequisites

1. Create two Dedicated deployments in different cloud platforms: `deployment-aws` and `deployment-gcp`. Refer to the [EMQX Cloud documentation](https://docs.emqx.com/en/cloud/latest/create/dedicated.html#create-a-dedicated-deployment) on creating deployments for detailed steps on setting up Dedicated deployments.
2. Ensure public network access via [NAT Gateway](https://docs.emqx.com/en/cloud/latest/vas/nat-gateway.html):
   - Each deployment must set up the NAT Gateway.
   - The NAT Gateway must be in the `Running` state to allow external connections.

### Create Cluster Linking

1. Open the **Cluster Linking** page in the Console for `deployment-aws`.

2. Click **New** to create a new cluster link.

3. On the **New Cluster Linking** page, configure the following options:

   - **Deployment Name**: Select `deployment-gcp`, the Dedicated deployment to link to.

   - **Address**: The MQTT host and port of the deployment to be linked. It is auto-filled based on the selected deployment.

   - **Username / Password**: Use valid credentials configured in `deployment-gcp` to authenticate the connection.

   - **Client ID Prefix**: Set a unique prefix for Client IDs, e.g., `from-aws`.

     Depending on the cluster size and configuration, multiple MQTT client connections might be established to `deployment-gcp`, and each client must have a unique ClientID. You can control how these ClientIDs are allocated by setting the *Client ID Prefix* for these connections (e.g., `from-aws-1`, `from-aws-2`).

   - **Topics**: List of MQTT topic filters that specify which messages the current deployment will receive from the remote deployment, for example, `from-cluster`. 

   - **Advanced Settings**: Configure additional settings such as MQTT protocol parameters.

4. Click **Confirm**. The new link will appear on the **Cluster Linking** page and be enabled by default.

   ![image.png](https://assets.emqx.com/images/2be479fba1494ac04aec18d1f4866e33.png)

5. Repeat the process on `deployment-gcp` to create a reverse link back to `deployment-aws`.

   ![image.png](https://assets.emqx.com/images/7f3fff1ea33eb1b619f6e66372f7b82b.png)

### Example Behind-the-Scenes

When Cluster Linking is established, EMQX uses the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) to bridge messages between clusters. For example, when a client connected to `deployment-aws` publishes a message to the `from-cluster` topic, EMQX routes it to `deployment-gcp` via the configured link, ensuring subscribers on both clusters receive the message. This process leverages MQTT’s lightweight publish-subscribe model for efficient, real-time communication.

### Verify Multi-Cloud Cluster Connectivity

To confirm successful Cluster Linking, use MQTTX, a free MQTT client tool for testing connections (download at [MQTTX: Your All-in-one MQTT Client Toolbox](https://mqttx.app/) ):

1. Create a connection named `aws-client` in MQTTX, connecting to `deployment-aws` using its MQTT host and credentials.
2. Create a second connection named `gcp-connection`, connecting to `deployment-gcp`.
3. Subscribe both clients to the `from-cluster` topic configured during Cluster Linking.
4. Using `aws-client`, publish a test message to the `from-cluster` (e.g., “Hello from AWS”).
5. Verify that both `aws-client` and `gcp-connection` receive the message, confirming bidirectional message routing across clouds.

## Network Interconnection Solutions

To enable seamless communication between EMQX clusters across different cloud platforms, robust network interconnection solutions are essential. This section explores three common approaches—NAT Gateway, VPN Connectivity, and Direct Connect/Cloud Interconnect, highlighting their trade-offs and ideal use cases to help you choose the best option for your multi-cloud MQTT deployment.

### Default NAT Gateway

The **Network Address Translation (NAT)** Gateway is the default method for connecting EMQX clusters across different cloud platforms. It routes traffic through a public IP, hiding private IP addresses while enabling internet access. This approach is straightforward to set up, making it suitable for smaller organizations or proof-of-concept deployments needing quick connectivity.

- **Security**: Since traffic is routed through a public network, it is essential to implement robust security measures, such as **firewalls**, **VPNs**, or **encryption**, to safeguard data.
- **Performance**: NAT connections typically introduce latency due to the overhead of translating and routing traffic. It may not provide optimal performance compared to dedicated network connections.
- **Use Case**: Ideal for startups or small-scale IoT deployments where cost is a priority and low-to-moderate performance is acceptable.

### **VPN Connectivity**

For organizations looking to secure the communication between cloud environments, **Virtual Private Network (VPN) Tunnels** offer a reliable solution. By creating an encrypted tunnel between cloud providers’ Virtual Private Clouds (VPCs), VPNs provide a secure and stable connection. This method is well-suited for mid-sized businesses needing secure, cost-effective communication for IoT workloads, such as industrial sensor networks.

- **Security**: The encrypted tunnel ensures that all traffic between cloud platforms remains private and protected from external threats.
- **Stability**: VPNs are generally more stable than public internet-based connections and can support a variety of traffic types. However, they still rely on the public internet, meaning performance can be impacted by congestion or routing inefficiencies.
- **Use Case**: Best for mid-sized enterprises requiring secure, reliable connectivity without the high costs of dedicated networks.

### **Direct Connect / Cloud Interconnect**

For organizations requiring high-performance connectivity, **Direct Connect** (AWS) or **Cloud Interconnect** (Google Cloud) provides a dedicated, private network link between data centers and cloud environments. Although these solutions come at a higher cost, they bypass the public internet and offer significant advantages. This premium solution is ideal for mission-critical IoT applications.

- **Performance**: Direct, private connections offer higher bandwidth, lower latency, and more reliable performance compared to NAT or VPN solutions, making them ideal for mission-critical applications.
- **Service Level Agreement (SLA)**: These solutions come with guaranteed SLAs for uptime, which is essential for enterprises with stringent availability requirements.
- **Cost**: Higher costs make this suitable for large organizations prioritizing performance over budget.
- **Use Case**: Essential for enterprises running latency-sensitive, high-throughput IoT applications requiring robust SLAs.

## Conclusion

**EMQX Cluster Linking** is crucial for ensuring seamless multi-cloud deployment, high availability, and business resilience. By enabling flexible cross-cloud migration, routing messages across platforms, and providing an efficient, unified MQTT infrastructure, it allows organizations to break free from vendor lock-in, enhance disaster recovery, and streamline operations. Ultimately, Cluster Linking simplifies the complexity of multi-cloud management and ensures business continuity, making it an essential component for a robust and flexible IoT architecture.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
