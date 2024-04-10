## Introduction

In the rapidly expanding world of IoT, where devices ranging from sensors to smart appliances communicate with each other and with central servers, the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) plays a crucial role. 

When it comes to implementing IoT projects, cost is often a significant consideration, especially for individual developers with limited budgets and startups in prototype development. Opting for a free MQTT broker can lead to substantial cost savings without compromising on essential features and performance.

This blog will introduce the common free MQTT brokers available and how to choose the right solution for seamless and reliable MQTT communication.

## Common Types of Free MQTT Brokers

### Open Source MQTT Broker

[Open source MQTT brokers](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023) are software solutions that are freely available for developers to download, use, and modify according to their needs. 

**Popular Open Source MQTT Broker:**

- EMQX: [EMQX](https://www.emqx.io/) is one of the most popular open source MQTT brokers and has 11.5k stars on GitHub. It is the world's most scalable MQTT broker that supports masterless clustering for high availability and horizontal scalability. EMQX is widely used for business-critical applications in various industries, such as IoT, [industrial IoT](https://www.emqx.com/en/use-cases/industrial-iot), [connected cars](https://www.emqx.com/en/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know), [manufacturing](https://www.emqx.io/use-cases#manufacturing), and telecommunications.
- Mosquitto: [Mosquitto](https://www.emqx.com/en/blog/mosquitto-mqtt-broker-pros-cons-tutorial-and-modern-alternatives) is known for its lightweight footprint, making it suitable for resource-constrained environments commonly found in IoT deployments. It supports the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) versions 3.1, 3.1.1, and 5.0, providing flexibility and compatibility with a wide range of MQTT clients and devices.
- NanoMQ: [NanoMQ](https://nanomq.io/) is a lightweight and fast MQTT messaging broker designed for edge computing scenarios in IoT. It is lightweight and high-performance, making it suitable for various edge computing platforms. 

**Limitations of Open Source MQTT Brokers:**

- **Self-Management:** Users of open source MQTT brokers are responsible for managing and maintaining the software, including updates, security patches, and scalability.
- **Learning Curve:** Customizing and managing open source brokers may require technical expertise, leading to a learning curve for less experienced developers.
- **Limited Support:** While communities provide support, it may not match the level of dedicated support offered by commercial solutions.

### Public MQTT Broker

[Public MQTT brokers](https://www.emqx.com/en/mqtt/public-mqtt5-broker) are hosted services that offer MQTT broker functionality accessible over the internet. These brokers are maintained by service providers and offer a convenient way for developers to quickly set up and test MQTT communication without the need for self-hosting or infrastructure management.

EMQX and Mosquitto also provide public MQTT broker services, allowing developers to connect their devices and applications to a reliable MQTT broker without the hassle of setting up their own infrastructure. The EMQX public broker offers scalability, high availability, and security features, making it a popular choice among IoT developers for prototyping and testing.

**Limitations of Public MQTT Brokers:**

- **Dependency on Service Provider:** Public MQTT brokers are dependent on the service provider's uptime and reliability, which may impact application availability.
- **Limited Customization:** While public brokers offer essential features, customization options may be limited compared to self-hosted or open source solutions.
- **Data Privacy Concerns:** Developers need to consider data privacy and security implications when using public brokers, especially for sensitive or production-grade applications.

## EMQX Serverless: A Free MQTT Broker without Hassle

EMQX Serverless is a serverless MQTT service based on EMQX MQTT Platform leveraging a clustered multi-tenancy architecture. It features seamless and automatic scaling to meet business demands and offers a convenient pay-as-you-go pricing model. Users can deploy their MQTT services in just 5 seconds without concerns about server infrastructure management or resource allocation when the service scales.

Learn more: [Secure, Scalable, and Serverless MQTT Messaging](https://www.emqx.com/en/cloud/serverless-mqtt) 

### Billing Model of EMQX Serverless

EMQX Serverless employs a pay-as-you-go billing model, based on three key components: session minutes, traffic (bandwidth), and rule actions.

- Session Minutes: Calculated per session initiated within a minute or part thereof.
- Traffic (Bandwidth): Encompasses both inbound and outbound messages processed by the deployment.
- Rule Actions: Pertains to the total number of actions performed within Data Integration.

For comprehensive details on EMQX Serverless Pricing, please visit our [pricing page](https://www.emqx.com/en/pricing).

## How to Get a Forever Free MQTT Broker: Free Quota and Spend Limit

### Free Quota

EMQX Serverless includes a monthly free quota of billing units, ensuring you can enjoy a complimentary MQTT service as long as your usage stays within this quota.

| **Billing Unit** | **Free Quota**                    | **Pricing**                       |
| :--------------- | :-------------------------------- | :-------------------------------- |
| Session minute   | 1 million session minutes / month | $2.00 per million session minutes |
| Traffic          | 1 GB / month                      | $0.15 / GB                        |
| Rule action      | 1 million rule actions            | $0.25 per million rule actions    |

By setting the Spend Limit to 0 and utilizing the free quota, you can streamline your operations without any initial costs and without the need for a credit card.

To give you a vivid idea of how much are 1 million session minutes and 1 GB of traffic:

If a single [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) remains connected for a whole month, it will consume approximately 43,200 session minutes. Based on this estimate, one million session minutes could support up to 23 clients remaining connected for a month. This number will increase if clients go online and offline periodically.

Assuming an average message size of 500 bytes, it is estimated that approximately 2,147,483 messages can be sent and received in a month. With 23 MQTT clients, each client could send and receive around 130 messages per hour continuously for a month. It is obvious that the free quota can support small-scale IoT scenarios with ease.

### Spend Limit

You may want to ensure that you can always use the service without incurring any additional fees. The Spend Limit feature ensures you can keep your monthly expenses within a pre-defined limit and receive alerts as you near this threshold.

The Spend Limit is adjustable from 0 to 10,000:

- Set to 0: The deployment will operate within the free quota only. Once this quota is depleted, the deployment will pause.
- Set between 1 and 10,000: Offers the flexibility to either pause the deployment or receive an alert when the monthly limit is reached.

You can obtain an MQTT broker forever free with the value set to zero. And if you are willing to pay for the extra session minutes or traffic, you don’t have to worry about overspending by setting a Spend Limit.

## 6 Steps to Get Started with a Free MQTT Broker

1. Register for an account on the EMQX website. Log in to the EMQX Platform Console and Select 'New Deployment' on the start page.

2. Select the Serverless card to access Serverless Configuration. Choosing a region, opt for one that is geographically close to your location.

   ![Choose plan](https://assets.emqx.com/images/5c34405e61e6c334954d5cb5d47ffce3.png)

1. In the Spend Limit Section, leave the default setting as 0. Spend Limit of 0 means that you use the free quota, containing 1 million session minutes, 1 GB of traffic, and 1 million rule actions for each month. 

   ![Spend Limit Section](https://assets.emqx.com/images/23423ec9aed85dd01f2f9378d1057349.png)

1. Review the summary on the right, and Click the “Deploy“ button on the bottom.

   ![Review the summary](https://assets.emqx.com/images/1e5f48101776d0962844ed3b3ab834ed.png)

1. Please review and accept the terms. 

2. Wait for the deployment status to display as "Running". Then, click on the deployment card to access the deployment overview page.

   ![deployment overview page](https://assets.emqx.com/images/f52c2ed8f5ac7ac9093d67eac6840522.png)

Now you have an MQTT Broker forever free. Please refer to the product documentation for a complete list of features and instructions: [EMQX Platform Documentation](https://docs.emqx.com/en/cloud/latest/).

For an in-depth comparison of the features offered by the Serverless Plan and the Dedicated Plan, please refer to: [https://www.emqx.com/en/pricing](https://www.emqx.com/en/pricing) .

## Summary

In conclusion, leveraging a free MQTT broker like EMQX Serverless can be a game-changer for IoT projects, especially for individual developers and small businesses looking to minimize costs without compromising on quality and scalability. Get your free MQTT broker today and elevate your IoT business with its scalability, flexible deployment, and cost savings.



<section class="promotion">
    <div>
        Try EMQX Serverless for Free
        <div>No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient">Get Started →</a>
</section>
