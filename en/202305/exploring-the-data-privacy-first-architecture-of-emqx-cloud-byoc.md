With the exponential growth of the Internet of Things (IoT), ensuring data privacy and security has become more crucial than ever. The need for a secure, scalable, and reliable IoT infrastructure has become paramount.

EMQ recently launched [EMQX Cloud BYOC](https://www.emqx.com/en/cloud/byoc) edition with a privacy-first architecture, providing an ideal solution that addresses these concerns. Users can deploy MQTT clusters in their own cloud environment while completely controlling data privacy and security.

> Learn more about BYOC: [Exploring BYOC: Taking Your MQTT Cloud Service to the Next Level](https://www.emqx.com/en/blog/exploring-byoc-taking-your-mqtt-cloud-service-to-the-next-level) 

In this blog, we will dive into the architecture of EMQX Cloud BYOC and explore how it can secure your IoT infrastructure.

## EMQX Cloud BYOC Overall Architecture

EMQX Cloud BYOC provides a flexible and scalable architecture that gives customers complete control over access. The architecture consists of two environments: 

- The EMQX Cloud's environment: Offering a range of features, including access control management, data integration, monitoring, and alerts, which enable customers to manage their MQTT cluster. 
- The customer cloud environment: Hosting an EMQX MQTT cluster managed by EMQX Cloud. All of the customer's MQTT data traffic goes in and out through this MQTT cluster.

![The architecture diagram of EMQX Cloud BYOC](https://assets.emqx.com/images/caaab8b3bbaefaad3b82d8e1ec7f4909.png)

<center>The architecture diagram of EMQX Cloud BYOC</center>

In the customer's cloud environment, an EMQX cluster and BYOC Agent node are placed in an independent VPC. The load balancing service of the cloud platform is used to control the MQTT device traffic inflow. VPC peering is utilized for communicating with other IoT applications or message persistence components. The BYOC Agent node is responsible for managing the EMQX cluster, monitoring logs, and conducting data backup tasks.

In the EMQX cloud environment, a web-based management console is provided for easy management and control of your EMQX clusters, as well as viewing cluster logs and monitoring data. The Operation and Maintenance (O&M) Service is designed to collect monitoring data and logs, manage alert rules, and automate self-recovery processes.

## The Heart of BYOC: Privacy-First Architecture

The privacy-first architecture of EMQX Cloud BYOC can also be divided into two parts: the control plane and the data plane. 

The control plane, located in the EMQX cloud environment, features a management console and monitoring data. Its primary function is to collect monitoring data during system operation and send control instructions to the customer's cluster. It only deals with control and monitoring data and does not involve any business data inflow or outflow.

On the other hand, the data plane includes EMQX clusters and BYOC Agent nodes, both of which are located in the customer's cloud environment. They are responsible for managing the inflow and outflow of customers' business data. 

In this way, privacy-first is at the heart of EMQX Cloud BYOC, as it provides complete control over access and improved privacy and security for enterprises looking to deploy secure and reliable IoT systems. With this BYOC architecture, customers' business data can be securely isolated in the customer's cloud environment, which meets customers' security and compliance needs. 

## Pre-Requests for Using EMQX Cloud BYOC

To use EMQX Cloud BYOC, customers need to meet certain technical requirements as follows:

- Familiarize yourself with the basic concepts of public cloud services and network structures, such as VPC, subnet, ECS, etc.
- Have a public cloud account and an EMQX Cloud account.
- Prepare relevant cloud resources and account permissions.
- Set up an Ubuntu 20.04 LTS environment to run the installation script.
- Prepare EMQX Cloud BYOC license.
- Prepare a domain name and its SSL certificate

## Go For BYOC and Control Your Data Today

Besides a privacy-first architecture that enables secure data traffic and storage in your own cloud, EMQX Cloud BYOC also provides enterprise-grade security features and customization options that allows scalable, flexible deployment and integration. With the support of technical experts from EMQ, your MQTT infrastructure management will be easier than ever.

[Visit our website](https://www.emqx.com/en/cloud/byoc) or [contact us](https://www.emqx.com/en/contact?product=cloud) for more info.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
