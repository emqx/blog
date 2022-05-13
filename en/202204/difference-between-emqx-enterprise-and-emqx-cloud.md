As a software supplier for open-sourced IoT data infrastructure, EMQ provides 2000+ enterprise users from more than 50 countries around the world with high-reliability and high-performance real-time connection, movement, and processing of massive IoT data from edge to cloud by EMQX, the world’s leading open-source cloud-native MQTT message broker.

Starting from an open-source project, EMQX has developed into the on-premises version, EMQX Enterprise, and the SaaS version, EMQX Cloud, to meet the demands of different types and scales of enterprises and accelerate the digitalization, real-time and intelligent transformation for them.

This article will make a detailed comparison and interpretation of EMQX Enterprise and EMQX Cloud from product architecture, features, and applicable scenarios. You can know how to select more suitable IoT data access software following this article.

## Products Overview

EMQX Enterprise is an open-source cloud-native IoT MQTT message broker based on the Erlang/OTP platform, with integrated distributed MQTT message service and powerful IoT rule engine. It supports multiple standard IoT protocols and Industry-specific protocols. It provides high-reliability connection and low latency message routing of massive IoT devices.

EMQX Cloud is the world's first fully managed MQTT 5.0 public cloud service launched by EMQ, providing MQTT message service with a one-stop operation and maintenance host and a unique isolated environment for MQTT services. EMQX Cloud can help you quickly build industry applications and easily realize the collection, transmission, computation, and persistence of IoT data.

Based on EMQX Broker, EMQX Enterprise and EMQX Cloud extend the features such as the protocol support, rule engine, data persistence and others to help connect IoT devices. The workflow involves collecting data generated from devices, transmitting it securely through encrypted connection, device authentication and access rights control, and then transferring it to various third-party data systems through the rule engine for secondary processing and display.

**In brief, the biggest difference between the two is the way of delivery.** EMQX Enterprise is an on-premises product at the enterprise level, which is suitable for enterprises with relatively complete operation and maintenance teams and self-management. EMQX Cloud is a fully managed cloud-native MQTT message service, which can be deployed and hosted on public cloud platforms such as AWS, Azure, and GCP. It is more applicable to small and medium-sized enterprises whose most business architectures are in the cloud and need an automatic fully managed operation, maintenance, and monitoring.



## Comparison of Features

| **Features and Services**                       | **EMQX Cloud**                                               | **EMQX Enterprise**                                          |
| ----------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Basic features of EMQX Broker                   | Full support                                                 | Full support                                                 |
| High Availability Cluster                       | Support                                                      | Support                                                      |
| Monitoring                                      | EMQX Cloud Monitoring Console                                | EMQX Cluster Monitoring Dashboard                            |
| Rule engine and data persistence                | Full support                                                 | Full support                                                 |
| Deployed environment                            | Public cloud platform, including AWS, Azure, Google Cloud.   | Enterprise private environment, supporting various infrastructures such as public cloud, private cloud and enterprise private computer room. |
| Integration of alert                            | Built-in alert forwarding to Slack, Webhook and PagerDuty.   | Requires development integration based on EMQX API or rule engine. |
| Log tracking                                    | View logs online                                             | View log file                                                |
| Management of multi-account and multi-project   | Support                                                      | Not support                                                  |
| Services for operation, maintenance and support | 7*24 fully managed services, operation and maintenance services | Multi-level online or on-site technical support services     |
| Database authentication                         | Support EMQX built-in database only. External database needs to be supported by submit a ticket. | Support built-in and external database.                      |
| Extension of modules and plug-ins               | Support after submitting the ticket.                         | Support                                                      |

## Comparison of Target Users

EMQX Enterprise is suitable for deployment with strict requirements and needs to be deployed in a specified deployment environment, especially in a private environment. Meanwhile, the enterprise has a relatively complete team for operation, maintenance, and support with daily basic software operation and maintenance.

EMQX Cloud is more suitable for enterprises whose business system has been or is planned to be deployed on the public cloud platform, has strong demand for infrastructure software SLA, hopes to reduce the operation and maintenance pressure of the team by purchasing consignment operation and maintenance service, and has relatively flexible process of product procurement and way of payment. EMQX Cloud also provides multi-project and multi-role management capabilities for project managers of enterprises.

## Comparison of Price and Service Support

Both EMQX Enterprise and EMQX Cloud are provided by the global support team with technical support of different specifications and forms such as 5x8/7x24 and online/offline, as well as commercializing services such as customized development, architecture consultation, and project integration.

In terms of price, EMQX Cloud has very flexible and transparent quotations for different plans, and there are two types, pay as you go and annual prepayment, with different degree of discount. You can choose the plan and specification here to make a price estimate: [https://www.emqx.com/en/cloud/pricing](https://www.emqx.com/en/cloud/pricing) 

The scheme of the price of EMQX Enterprise will provide different modes of the price in conformity with the maximum number of connections, usage time, and enterprise usage scenario. For a detailed quotation, you can click the link:[https://www.emqx.com/en/contact](https://www.emqx.com/en/contact) 

## Summary

With this article, you will have a clearer understanding of EMQX Enterprise and EMQX Cloud. You can make a choice by the development status, business form, and business demand of your enterprise. Meanwhile, EMQX Enterprise and EMQX Cloud both offered a free trial. You are welcome to try it and determine which one is better for your business.

EMQX Cloud: [Sign up for EMQX Cloud](https://www.emqx.com/en/signup?continue=https%3A%2F%2Fcloud-intl.emqx.com%2Fconsole%2Fdeployments%2F0%3Foper%3Dnew) 

EMQX Enterprise: [https://www.emqx.com/en/try?product=enterprise](https://www.emqx.com/en/try?product=enterprise)
