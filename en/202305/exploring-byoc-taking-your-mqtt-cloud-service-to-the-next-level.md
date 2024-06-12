## Introduction

Are you looking to take your IoT infrastructure to the next level? MQTT protocol has already become the most popular choice for IoT platform building due to its lightweight, [publish/subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) and reliability. However, as the business grows, IoT solution providers may face increasing costs associated with maintaining their infrastructure and stricter data privacy requirements. 

EMQ, the leading provider of open-source MQTT messaging platforms, offers [EMQX Cloud BYOC edition](https://www.emqx.com/en/cloud/byoc) to enable you to deploy MQTT clusters in your cloud environment of choice while keeping complete control over your data privacy and security.

In this blog, we'll explore the BYOC model and architecture of EMQX Cloud BYOC edition to help you understand how it can benefit your business.

## What is BYOC?

BYOC stands for "Bring Your Own Cloud", an offering model allowing you to deploy your MQTT clusters in your preferred cloud environment such as Amazon Web Services (AWS), Microsoft Azure, or Google Cloud Platform. It enables you to retain full control over your cloud infrastructure and ensure compliance with strict regulations.

## Offering Model: Pay Only for What You Use

EMQX Cloud BYOC edition offers a cloud-native architecture emphasizing scalability, availability, and security, with high service availability and a 99.99% service level agreement (SLA) for MQTT services.

The licensing model is based on a subscription, which provides you with the flexibility to scale your MQTT infrastructure as needed. You only pay for the services you use, with no upfront investment required. 

The subscription also includes access to technical support and maintenance using cloud-native tools like Prometheus, Grafana, and open Telemetry, which will ensure that your MQTT infrastructure remains reliable and up-to-date.

## Architecture: Ensure High-Level Data Privacy

The EMQX Cloud BYOC architecture has two parts: EMQX Cloud’s environment and customer’s cloud environment. Figure 1 above shows how they are set up.

![The architecture diagram of EMQX Cloud BYOC](https://assets.emqx.com/images/9ab816f6809f3ceb4fd14f4c4b0bbc08.png)

<center>The architecture diagram of EMQX Cloud BYOC</center>

In the customer's cloud environment, an EMQX cluster and BYOC Agent node are put in an independent VPC. The load balancing service of the cloud platform (like AWS Network Load Balancer) is used to control the MQTT device traffic inflow, while VPC peering is used to communicate with other IoT applications or message persistence components. The BYOC Agent node manages the EMQX cluster, gets monitoring logs, and does data backup tasks.

On the EMQX Cloud’s environment side, there's a management console with BYOC. This allows you to easily manage and control your EMQX clusters using a GUI interface and view cluster logs and monitoring data.

When it comes to data control, the architecture can be divided into the control plane and the data plane. 

- The control plane, located on the EMQX cloud environment side, collects monitoring data and sends control instructions to your cluster. It does not handle any business data inflow or outflow. 
- The data plane includes the EMQX clusters and BYOC Agent nodes that are in the your cloud environment. They mainly manage the inflow and outflow of customers' business data. 

With this BYOC architecture, customers' business data is well isolated in your cloud environment, which meets your company's security and compliance needs.

## Advantages: Flexible, Reliable, and Easy-to-Use MQTT Service

Here are what you can benefit from EMQX Cloud BYOC:

* Complete control over your access and data
* Minimal to zero operation requirements
* Low network latency
* Flexible deployment options
* Reliable service with SLAs
* Access to expert support
* Customize your cloud environment as per your requirements
* Ensure data security by keeping your data in your own cloud

## Use Cases: Boost Data Security for Every Business

EMQX Cloud BYOC edition has been adopted by businesses across a range of industries, including Internet of Vehicles (IoV), healthcare, and smart cities.

In IoV scenarios, sensitive data such as vehicle location and driving behavior needs to be transmitted from the vehicle side to the MQTT Broker via either public or private networks, and then saved into the company's centralized data platform.

EMQX Cloud BYOC can ensure that the entire data chain is within the customer's own cloud account to prevent unauthorized access and data breaches. This addresses the risks of data leakage from the source, reduces the involvement of intermediaries, and simplifies data management complexity.

## Summary

In conclusion, EMQX Cloud BYOC offers a powerful solution for businesses that require advanced data control and security measures. With the BYOC architecture, companies can leverage EMQX's proven MQTT technology while maintaining full control over their data within their own cloud environment. This provides enhanced security and compliance capabilities, as well as greater flexibility and scalability. 

If you're looking to take your MQTT service to the next level, do not hesitate to  [visit our website](https://www.emqx.com/en/cloud/byoc)  or  [contact us](https://www.emqx.com/en/contact?product=cloud)  today to schedule a demo!

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
