
EMQ X Enterprise IoT MQTT messaging platform supports one-stop access for millions of IoT devices, MQTT & CoAP multi-protocol processing and low latency real-time message communication. It supports a built-in SQL-based rules engine, flexible processing/forwarding of messages to back-end services, storage of message data to various databases, or bridging to enterprise middleware such as Kafka and RabbitMQ.

EMQ X Enterprise is suitable for various IoT application scenarios, and helps enterprises to build IoT applications quickly and supports arbitrary deployment of public cloud, private cloud, physical machine and container/K8S.

URL: https://www.emqx.io/products/enterprise

Download: [Download](https://www.emqx.io/downloads#enterprise) now without providing any information!

![enterprisemqttbroker.png](https://static.emqx.net/images/4b87d5ae6dc17bb84f6414e4d8fc504c.png)

## Overview

The rules engine of EMQ X Enterprise v4.2.2 can choose to store data synchronously/asynchronously, and some resources provide a batch enable switch that allows the user to select different data processing modes according to their needs, balancing data processing performance and the data timing issue.

At the same time, this version improves the ease of use of the LwM2M protocol and allows the LwM2M connection to be managed separately via the REST API and the Dashboard visual interface, including a list of clients accessing EMQ X via the LwM2M protocol as well as the corresponding Object and Resource.

Detailed update log: https://www.emqx.io/changelogs/enterprise/v4.2.2

## Features

### Rules engine

[EMQ X rules engine](https://docs.emqx.io/en/broker/latest/rule/rule-engine.html) is used to configure the message flows, and processing and forwarding rules of device events, and **supports forwarding data to various databases, flow processing and data analysis systems, including Apache Kafka and Clickhouse, to quickly build a one-stop platform for IoT data integration, cleaning, storage, analysis and visualization.**

As a key feature of EMQ X, the rules engine provides a clear and flexible "configurable" business integration solution based on SQL, simplifying the business development process, improving user usability and reducing the coupling between the business system and EMQ X. 

The rules engine of version 4.2.2 has added the following new features:

- **Added support for the Oracle, MS SQL Server, DolphinDB database**

  Oracle and MS SQL Server are prominent representatives of the commercial relational database camp with a high market share, and this update fills in the gaps in the integrity of the technology stack and covers a broader customer base.

  [DolphinDB](https://www.dolphindb.com/) is a high-performance distributed time-series database developed by Zhejiang Zhiyu Technology Co. It integrates the programming language with powerful features and a high-capacity and high-speed analysis system of streaming data. Also, it provides a one-stop solution for the rapid storage, retrieval, analysis and calculation of large amounts of structured data, suitable for quantitative finance and industrial IoT. EMQ X uses DolphinDB to offer more data processing options for the financial and industrial network of IoT. 

- **Both synchronous/asynchronous data processing methods can be configured for the action**

  Previously, the rules engine only supported synchronous mode for processing device data due to time-series considerations. In the case of Publish, for example, the rules engine will block the Publish process when the data is deposited, and waits until it has been deposited before publish the message to the specified topic.

  In the case of large message volumes, if the user does not wish to block normal Pub/Sub and other processes, asynchronous mode can be selected when creating the rules engine. Asynchronous mode separates device message communication from data processing and prevents the rules engine from blocking the normal behaviour of the client.

  > In practice, the difference in time-series between the two has little or no impact on the business, and the rules engine action is preferentially recommended in asynchronous mode.

- **More actions support batch processing and provide enable configuration**

  Previously, in the rules engine, there are only a few actions such as save data into MySQL support batch processing, and by default, it can not be closed the batch processing feature once enable.

  Current resources to support batch processing: MySQL、PostgreSQL、ClickHouse、TDengine、Cassandra、SQL Server、Oracle、DolphinDB。

  **Enabling batch processing can bring several times the performance improvements, but there are corresponding problems**. Take MySQL as an example, the rules engine does not write to the database immediately when it performs an action, but waits for a batch to be processed.

  - Principle: Multiple INSERT operations with a certain number of bars or over a period of time will be merged into one in order to increase the efficiency of insertions.

  - Execution with full number of bars (batch count): If there are 100 INSERT operations that need to be performed, merge them into one insert operation and reset timer

  - Time to execute (batch interval): If you wait 10ms before the 100 bars are reached, merge them into one insert and reset the timer

    > The number of batches and the batch interval can be set at the time of action creation itself.

  The problems with this process are:

  - Delays in storing data into the database: Due to batch interval and batch number, data is not stored in real-time.
  - Batch insertion with partial failure: Partial data errors can result in the loss of the entire batch, e.g. constraint errors, type errors. This is handled in MySQL but is easily overlooked by users.
  - Operational audit issues: Bulk inserts can complicate database SQL auditing.

With this update, it is up to the user to decide whether or not to enable the batch function on the action to circumvent the above problem.

![WechatIMG4339.png](https://static.emqx.net/images/8d7c7df1d9e383c9b564509403718f6e.png)


### Support for LwM2M visualization and REST API management

LwM2M is a set of lightweight protocols for the IoT, defined by the Open Mobile Alliance (OMA), which provides device management and communication features, especially for end devices with limited resources.

EMQ X-LwM2M implements most of the features of LwM2M. Applications and MQTT clients can access LwM2M-enabled devices via EMQ X-LwM2M and devices can report notifications to EMQ X-LwM2M for bi-directional data communication.

![WechatIMG4340.png](https://static.emqx.net/images/c5580c872ed07fc6983e3995867c0b51.png)

In EMQ X v4.2.2, users can manage LwM2M connections individually via the Dashboard visualization interface and REST APIs, obtain information such as IMEI, LifeTime, objectList, etc. for Lw connections, helping enterprises to quickly implement secure and reliable device interconnections, application development of IoT platforms and vertical industries.




### Optimising Auth HTTP performance

EMQ X can make a request to the user-defined Authentication HTTP Service to query authentication and ACL permissions. The authentication service controls the authentication results via the HTTP **statusCode** returned.

HTTP authentication enables more complex authentication logic than database authentication, JWT, etc. This update optimizes the HTTP performance of EMQ X authentication requests and can carry the higher connection, publish/subscribe rates.

### Functional adjustments

- The depth of the CA certificate SSL supports to configure has been added.

### Problem fixes

- Fix for incorrect counting of asynchronous patterns for rules engine actions
- Fixes for anomalies in hot upgrades

### Contacts

If you have any questions about EMQ X Enterprise, please feel free to contact us at [contact@emqx.io](mailto:contact@emqx.io).




