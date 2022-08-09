EMQX Cloud, a fully managed [MQTT cloud service](https://www.emqx.com/en/cloud), can provide users with reliable real-time IoT data movement, processing, and integration, helping to accelerate the development of IoT platforms and applications.

In EMQX Cloud, the "Data Integration" module, optimized and upgraded based on the original high-performance built-in rule engine, provides a clear and flexible architecture solution for users to configure and respond to message flow and device event rules. It supports dozens of data integration resources, including Kafka, MySQL, Redis, Webhook, etc., and is a powerful tool to help users realize flexible data processing and integration.

In the latest updated version, EMQX Cloud has added support for two external databases, HStreamDB and Alibaba Cloud Tablestore.

## Feature Introduction

With the help of the data integration feature, users can complete the configuration according to their own needs through four simple steps：1)creating resources; 2)creating rules; 3)adding actions; 4)running test, and then realize the flexible operation of device data. It not only greatly simplifies the development process and reduces the coupling degree between the business system and EMQX Cloud, but also provides a better infrastructure for EMQX Cloud’s private feature customization.

![EMQX Cloud](https://assets.emqx.com/images/68ef246302fa60f850b5670ee55b1841.png)

EMQX Cloud currently supports integration with multiple types of data queues, databases and web services. New additions are two databases developed by EMQ and Alibaba Cloud respectively.

![EMQX Cloud data integrations](https://assets.emqx.com/images/c1a2ede68a48f76ae8d4c65665c93d71.png)
 

#### HStreamDB

[HStreamDB](https://hstream.io/) is an open-source streaming database designed for streaming data by EMQ, which can manage the entire life cycle of access, storage, processing, and distribution of large-scale real-time data streams. It uses standard SQL (and its streaming extensions) as the main interface language and takes real-time as the main feature, aiming to simplify the operation and maintenance management of data flow and the development of real-time applications. After integrating with EMQX Cloud, users can easily realize the cloud upload, processing and distribution of device data.

![Configuration interface of HStreamDB](https://assets.emqx.com/images/07da21ea25a228665a1c513fe389528b.png)

<center>Configuration interface of HStreamDB</center>

#### Alibaba Cloud Tablestore

Alibaba Cloud Tablestore provides Serverless table storage services for massive structured data, and provides a one-stop IoTstore solution for in-depth optimization of IoT scenarios. It is suitable for structured data storage in scenarios such as massive bills, IM messages, IoT, Internet of Vehicles, risk control, and recommendation, providing low-cost storage of massive data, millisecond-level online data query and retrieval, and flexible data analysis capabilities.

![Configuration interface of Tablestore](https://assets.emqx.com/images/3ef0c2ade81269c7c9fa1cbca8e8acd4.png)

<center>Configuration interface of Tablestore</center>

 

## User guide of data integration

HStreamDB data integration reference document: [https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_save_hstreamdb.html](https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_save_hstreamdb.html) 

 

> Note:
>
> 1. This update resource is not available in the standard plan.
>
> 2. For professional plan deployment users: Please complete the creation of the peering connection first. The IP mentioned in this article refers to the intranet IP of resources (Professional version deployment users can also use public network IP to connect resources if NAT gateway is activated.)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
