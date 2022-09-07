## Introduction: New data integration capabilities

EMQX is designed for high-performance, real-time data processing and integration for IoT platforms and applications. The latest release of [EMQX 5.0](https://www.emqx.com/en/blog/emqx-v-5-0-released) is deeply refactored and optimized to make data integration easier and more flexible.

EMQX 5.0 integrates Webhook and data storage/bridging plug-ins together to manage both northbound and southbound data flow in a unified interface. Based on the same rule processing functions, users can also process southbound messages from the cloud to edge devices.

Also, EMQX 5.0 provides data integration visualization capabilities (Flows). Through the Dashboard, users can clearly see how IoT data is processed by the rules engine and how data flows to external data services or devices.

Subsequent versions will also support drag-and-drop orchestration of rules and data bridges (Flow Editor) on the Dashboard to easily connect IoT hardware data flows together through a visual interface.

This article will demonstrate the value and application of this important capability in EMQX and explore the specific upgrades and optimizations that have been made in EMQX 5.0.

## What is data integration?

EMQX data integration is a combination of the [rules engine](https://www.emqx.com/en/solutions/iot-rule-engine) and data bridge features introduced in version 4.x. It is a data processing and distribution component based on the publish/subscribe model. Through simple, visual configuration, you can integrate **message flows** and **device events** with message brokers such as Kafka, RabbitMQ, and various SQL / NoSQL / chronological databases and other data systems.

EMQX's simple, efficient, real-time data integration solution is achieved through two main features: **Rules** and **Data Bridges**.

Rules are used for message and event data processing, enabling operations such as data format conversion, message coding and decoding, and business logic processing through SQL-like syntax combined with built-in or user-extended custom functions. For more information about rules, see [Rules](https://www.emqx.io/docs/en/v5.0/data-integration/rules.html) in the EMQX docs.

Data Bridges are used to interface with data systems to enable high-performance, bidirectional data movement between EMQX and external systems. Data bridges allows users to push messages from EMQX to an external data system in real-time or to pull data from an external data system and push it to a topic in EMQX. For more information on data bridges, see [Data Bridges](https://www.emqx.io/docs/en/v5.0/data-integration/data-bridges.html).

![EMQX data integration](https://assets.emqx.com/images/8ea87178108fd15755534ac746118d3f.png)

## Why data integration?

The MQTT protocol is designed for hardware device-to-server messaging. To achieve a complete IoT application, it is necessary to connect devices with business systems capable of storing reported data in the cloud and distributing business instructions.

To achieve this in traditional IoT applications, developers need to write code, and subsequent changes in the business require upgrades to the whole application. The device side and business platform side are often operated by independent teams, which complicates the process further. The key to fast project delivery and upgrade iterations is decoupling the device side from the cloud business platform and still interfacing between the two efficiently.

EMQX data integration is designed to solve this problem. By providing flexible, low-code configuration capabilities, it helps users easily get started and quickly achieve various application integration and business innovation needs.

After years of practical implementation in IoT application scenarios in various industries, EMQX data integration has become a key capability for overall application building and continues to create value for users.

![EMQ Overall solution for IoV](https://assets.emqx.com/images/b92fa001c3c610d29128e675baa509cd.png)

<center>EMQ Overall solution for IoV: Build upper TSP and other services around rules engine</center>

## **Bidirectional data flow: both data reporting and downward messaging support rules processing**

The data between devices and business systems in IoT applications are usually bidirectional. There are scenarios for both data collection/reporting and the need to send messages downward from the cloud. Combining the two is necessary to achieve a complete business process.

In previous versions, EMQX's rules were executed by device messages and event triggers. This meant that rules could only satisfy the data collection and reporting use cases, but cloud-to-device messaging scenarios could not use the data processing capabilities of rules directly. Users needed to use a transit solution: sending data to an existing EMQX topic first and then processing it through rules.

EMQX 5.0 is optimized to satisfy both use cases: it provides bidirectional data bridging capabilities—in addition to bridging device data to an external system, data can be bridged to EMQX from external data systems such as another MQTT service or Kafka. The data will be sent to the designated device after rules processing.

![Bidirectional data flow](https://assets.emqx.com/images/3640b94059479d7d15a36e6b1d766c45.png)

<center>EMQX data integration southbound/downward message processing flow diagram: purple path is version 4.x solution</center>

Data bridging with bidirectional data flow decouples the connection between message-generating business systems in the cloud and EMQX, enabling continuous, large-scale, downward messaging with real-time processing and providing more possibilities for IoT business development.

## Flow Editor: Process data flow with visual orchestration rules

In previous versions, EMQX data integration was achieved by configuring SQL-like statements with rule actions, which had the following benefits:

- SQL syntax is widely used in the database field and users with a technical background can quickly get started and master writing complex rules in a short time;
- SQL rules are more readable than many programming languages and can be created and changed at runtime, making them suitable for rapidly changing businesses.

Data integration and data processing around SQL allows users to quickly develop and implement the required business logic, but it also brings some problems:

- Technical staff need to be familiar with EMQX SQL syntax before they can start writing business rules. For non-technical staff, SQL is not intuitive enough and the threshold for getting started is high;
- Some complex scenarios, such as distributing data to different data bridges based on conditions within the same rule, cannot be implemented using SQL, resulting in users having to create multiple similar rules;
- Inability to add an event to an existing rule without modifying the SQL;
- When there are many rules, it is difficult to maintain and manage or create a clear data processing and integration process.

In EMQX 5.0, we have prioritized solving the problem of data integration maintenance and management with many rules through visualization (Flows). Through the Dashboard page, users can clearly see how IoT data is processed by rules and flows to external data systems. Users can also see the data integration topology of external system data that is processed and distributed to devices as well as monitor the status of any rule or data bridging node in this link.

![EMQX Data Flow Editor](https://assets.emqx.com/images/08ef9906452ab24cfbf3ced2d7e15091.png)

In a future version, we will build a data Flow Editor with visual orchestration capability into EMQX. It will be browser-based and paired with the underlying execution engine, allowing users to freely orchestrate rules and create data bridges in a drag-and-drop manner within the EMQX Dashboard. IoT hardware data flows will be easily connected together through a visual interface to achieve faster, more flexible IoT business development and delivery.

## Data integration upgrade guide: Migrating from v4 to v5

EMQX 5.0 SQL rules are fully compatible with the syntax of version 4.x, but the design splits rule actions into two categories: built-in actions (message republishing, console output) and data bridges (Webhook, MQTT Bridge), which enables the reuse of rules and data bridges.

In addition to the new architectural design, EMQX also consolidates data integration-related features from older versions. Prior to the introduction of the rules engine in version 4.x, users could use plug-ins to create simple integrations. For compatibility reasons, we did not remove these plug-ins after the rules engine was released, which resulted in some fragmentation of functionality.

EMQX 5.0 formally removes the associated plug-ins to provide users with clearer and more complete data integration capabilities, reducing the difficulty of learning and selection.

The following is a comparison of the functional changes from EMQX open-source version 4.x to 5.0.

| **4.x Plug-ins** | **4.x Rules Engine Actions** | **5.0 Rules/Data Bridge Actions** |
| :--------------- | :--------------------------- | :-------------------------------- |
| emqx_bridge_mqtt | Bridging Data to MQTT Broker | MQTT Bridge                       |
| emqx_web_hook    | Sending Data to Web Services | Webhook                           |
| -                | Message republishing         | Message republishing              |
| -                | Check (debug)                | Console output                    |
| -                | Empty action (debugging)     | -                                 |

## Epilogue

In building IoT platforms and applications, it is an essential challenge to process massive amounts of data accurately and in real time according to demand and to interface with upper-level business systems. As an [MQTT-based IoT messaging server](https://www.emqx.io/) that can "connect any device, at any scale, anywhere," EMQX provides powerful, easy-to-use, and constantly improving data integration capabilities to help users tackle these data processing challenges and achieve business innovations.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
