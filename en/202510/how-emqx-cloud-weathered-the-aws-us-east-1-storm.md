> On October 20, 2025, a significant AWS us-east-1 outage disrupted countless global services from banking apps to smart home devices, starkly highlighting our dependence on core cloud infrastructure.
>
> As the Product Lead for EMQX Cloud, I want to share our experience. This event was a real-world test of our architectural principles, which helped us maintain service continuity when many others struggled. This is not about assigning blame; it's about sharing the lessons learned in building resilient IoT infrastructure.

## **EMQX Cloud: A Brief Introduction**

[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed MQTT data platform built for IoT applications at scale. As the cloud-native offering of EMQX, the world's most scalable [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), we provide enterprise-grade messaging infrastructure without the operational overhead. Our platform handles millions of concurrent connections and billions of messages daily, serving thousands of customers across industries from automotive to smart energy.

Our core mission is simple: ensure reliable, real-time message delivery for mission-critical IoT applications. This commitment to reliability shaped every architectural decision we've made since day one.

## **Our Experience During the Outage**

When the AWS US-East-1 region began experiencing issues on October 19th, we braced for impact. To our relief, and honestly, validation of our architectural choices, EMQX Cloud's core MQTT services remained largely unaffected.

Among our thousands of customers, only a handful reported occasional connection hiccups. The vast majority of our MQTT clusters running in AWS US-East-1 continued operating normally throughout the entire incident. Messages kept flowing, devices stayed connected, and critical IoT operations continued uninterrupted.

That said, we weren't completely immune. Some customers using our data integration features experienced elevated error rates when writing to affected AWS services like DynamoDB, Kinesis, S3 or RDS. However, the core MQTT communication layer remained stable, and once AWS services recovered, our data integrations automatically resumed normal operation without manual intervention, demonstrating the resilience built into our platform.

## **The Architecture of Resilience: Why EMQX Cloud Survived**

Our ability to weather this storm wasn't luck; it was the result of deliberate architectural decisions we've maintained since launching EMQX Cloud. Here are the key principles that protected our customers:

### 1. Staying Disciplined: The Power of Restraint

While it's tempting to leverage every managed service a cloud provider offers, we've deliberately maintained what we call "infrastructure minimalism." On AWS, EMQX Cloud uses only the most fundamental IaaS services: EC2 for compute and NLB for load balancing. That's it.

This "less is more" approach offers two significant advantages:

- **Reduced failure surface**: With fewer dependencies, there were simply fewer things that could break. While services depending on DynamoDB, Lambda, or other PaaS services struggled, our clusters kept running on basic compute infrastructure.
- **Enhanced portability**: Our minimal dependency footprint makes it straightforward to migrate between cloud providers or regions. This isn't just theoretical; we've helped customers execute such migrations with minimal friction.

### 2. Multi-AZ by Default: No Compromise on Availability

Even for our smallest Dedicated Flex deployments, we insist on distributing EMQX broker nodes across multiple availability zones. Yes, this increases costs due to cross-AZ traffic. Yes, it adds complexity to our deployment automation. But we believe it's non-negotiable for production IoT workloads. It provides inherent protection against failures affecting a single data center, which is a common cause of service disruptions. For us, the trade-off is clear: ensuring business continuity for our customers is always our top priority.

### 3. A True Multi-Cloud Strategy. No Vendor Lock-in

EMQX Cloud isn't just "cloud-compatible", we're genuinely cloud-agnostic. Whether you deploy on AWS, Azure, or Google Cloud, you get the same user experience, the same features, and the same architecture. This consistency isn't accidental; it's enforced by our infrastructure minimalism principle.

This approach gives our customers real options. They're not locked into a single cloud provider's ecosystem. If one cloud experiences issues, they can run disaster recovery workloads elsewhere with confidence that EMQX Cloud will behave identically.

## Lessons Learned: Building Your Own Resilient IoT Infrastructure

While we're proud of how EMQX Cloud performed during the outage, it also highlighted important lessons for anyone building IoT infrastructure:

### 1. Consider the Entire Data Pipeline

Our data integration features experienced elevated errors because downstream services were affected. This reminds us that resilience isn't just about your MQTT broker, it's about every link in your IoT data pipeline. A perfectly functioning MQTT cluster doesn't help if your data can't reach its destination. 

**Recommendation**: Map your entire data flow and identify potential single points of failure. Have fallback strategies for each component, whether that's alternative data stores, message buffering, or degraded operation modes.

### 2. High Availability Isn't Enough. Think Disaster Recovery

Even with our multi-AZ deployment and high SLA guarantees, regional outages remain a possibility. For truly critical applications, you need to think beyond high availability to full disaster recovery.

**Multi-AZ Deployment (What We Provide by Default)**

Our standard EMQX Cloud Dedicated deployments automatically include:

- Cluster nodes distributed across multiple availability zones
- Automatic failover at the node level
- Cross-AZ data replication
- Load balancer health checks with automatic bad node isolation

This protects against single AZ failures and individual node failures, covering the vast majority of failure scenarios.

**Cross-Region Disaster Recovery (For Critical Applications)**

For applications that cannot tolerate any regional failure, consider this architecture:

```
Production Architecture:
├── Primary Region (e.g., AWS us-west-2)
│   ├── EMQX Cluster (Multi-AZ)
│   ├── External Resources (Databases, Auth Services)
│   └── Network Configuration (VPC Peering, NAT)
└── DR Region (e.g., AWS us-east-1)
    ├── EMQX Cluster (Multi-AZ)
    ├── External Resources (Replicated)
    └── Network Configuration (Mirrored)

DNS Layer:
└── Weighted Routing
    ├── Primary Cluster: Weight 100 (Normal)
    └── DR Cluster: Weight 0 (Standby)
```

Key considerations:

- Maintain identical cluster specifications across regions
- Configure complete networking and external resources in each region
- Use DNS for unified traffic management and failover
- Test failover procedures regularly

### 3. Consider Multi-Cloud Strategies

Since EMQX Cloud provides identical experiences across cloud providers, you can implement cross-cloud disaster recovery. Your primary cluster might run on AWS while your DR cluster runs on Azure or Google Cloud, providing protection against provider-wide issues.

### 4. Active-Active with Cluster Linking

For organizations with global operations, we recommend considering our Cluster Linking feature instead of traditional primary-standby DR setups.

With Cluster Linking, you can:

- Deploy regional clusters serving local traffic
- Connect clusters into a logical global mesh
- Enable cross-region message routing when needed
- Achieve automatic failover without wasted standby resources

This approach is more economical than traditional DR, each cluster actively serves traffic while providing mutual backup capabilities. When one region fails, devices automatically reconnect to the nearest available cluster with full message routing preserved.

Learn more about Cluster Linking: [Cluster Linking | EMQX Platform Docs](https://docs.emqx.com/en/cloud/latest/cluster_linking/cluster_linking.html) 

## Moving Forward Together

The recent AWS outage was a powerful reminder that in the cloud era, resilience must be architected, not assumed. By adhering to principles of restraint, multi-AZ deployment, and a true multi-cloud strategy, we are committed to providing an IoT messaging platform that our customers can trust, even when the unexpected happens.

If you're looking for an MQTT platform that's proven its resilience in real-world outages, we'd love to help. Our team can assist with:

- Architecting high-availability deployments
- Implementing cross-region disaster recovery
- Planning multi-cloud strategies
- Optimizing cluster linking topologies

[Contact our team](https://www.emqx.com/en/contact?product=cloud) to discuss how EMQX Cloud can provide the resilient foundation your IoT applications deserve.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
