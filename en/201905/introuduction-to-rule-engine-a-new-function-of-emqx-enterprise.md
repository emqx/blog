### EMQ X Enterprise Rule Engine

EMQ X rule engine is used to configure the processing and response rule of
EMQ X messages or events. As a new important function of EMQ X in 2019, rule engine not only provides a clear and flexible "configurable" business integration solution, which is used to simplify the business development process, improve usability, and reduce the coupling degree between the business system and EMQ X, but also provides a better infrastructure for the private function customization of EMQ X to speed up development delivery.

The open source version of rule engine provides basic processing capabilities and has been integrated into EMQ X v3.1.0. A more flexible, more usable and customizable rule engine is being developed for testing, which is planned for release in the next EMQ X Enterprise Edition.

#### Examples of typical application scenarios for rule engine are as follows:

- Action listening: In the development of intelligent door lock for smart home, the function of the door lock will be abnormal because of offline resulting by the network or power failure, man-made damage and other reasons. Through using rule engine configuration to monitor offline events, it can push the fault information to the application service and realize the ability of first time fault detection in the access layer.

- Data filtering: Truck fleet management of vehicle network. Vehicle sensors collect and report a large amount of operational data. The application platform only focuses on data with a vehicle speed greater than 40 km/h. In this scenario, the rule engine can be used to conditionally filter messages to the service, and data that satisfies the condition can be written to the business message queue .

- Message routing: In the intelligent billing application, the terminal device distinguishes the service type by different topics. The message of billing service can be connected to the billing message queue by configuring the rule engine, and the non-billing information can be connected to other message queues to realize the routing configuration of business messages.

- Message encoding and decoding: In the application scenarios such as public protocol/proprietary TCP protocol access and industrial control, the encoding and decoding of binary/special format message body can be done through the local processing function of the rule engine (which can be customized and developed on EMQ X). Relevant messages can also be routed through the rule engine to external computing resources such as function computing for processing (processing logic can be developed by users), and the messages can be converted into JSON format that is easy for business processing, which simplifies the difficulty of project integration and improves the ability of rapid development and delivery of applications.



#### Rule Engine Working diagram
![image20190506171815028.png](https://static.emqx.net/images/36d63fd4f77f70b7ed9652ade79a0010.png)

The rule engine filters, transforms and enriches the data through embedding in the message forwarding process of EMQ to achieve efficient data processing. The new rule engine covers the functions of multiple **plugins**in EMQ X, and centrally manages the independent external resources in the original **plugins**, thus realizing resource reuse and reducing management and listening complexity. At the same time, the rule engine builds into EMQ X most of the calculations that can only be performed on the application side . By calculating, screening, and filtering high-value data to improve message processing efficiency, the business architecture is simplified, the data transfer path is decreased and message processing delay is reduced.

#### Rule engine related features include:

- Message Rules: Process messages from device to EMQ X, realize conditional calculation and filtering, message structure adjustment, message redistribution, persistence and bridging;

- Event Rules: Process the event information in the communication life cycle of device, realize the functions of device status record, including online or offline notification , authentication connection record, message status record such as message billing statistics.

- Resource management: Centrally manage external resources, achieve resource reuse, and reduce management listening complexity.

Like the other functions of EMQ X, the rule engine also provides a similar HTTP REST API to facilitate the integration of application development for user . The visual creation, editing and management functions of the rule engine are also realized in the EMQ X Dashboard

![1_jUIScQ1L9b4BIi__yiXg.png](https://static.emqx.net/images/8e8c5c679822a0f510f653313102c0da.png)

![1_J6wo0pQ5z0jk0DEtFNv42g.png](https://static.emqx.net/images/136f4a9b7b4a05ab1db0880a8c68a6b3.png)
### Message Rule

With the help of message rule in the rule engine, users can route messages from the device to EMQ X or write them to objects or resources such as various databases, message queues, HTTP REST gateways, or resend them to the device for server-side computing.

The rule engine provides functions of data query and processing based on SQL expressions, allowing the user to filter data and convert messages into a preset format before configuring subsequent processing actions.

#### An example of a SQL expression is as follows:

```sql
-- Select the name field in the body of the message sent to the "t/a" topic, with a filter condition of name = 'EMQ'
select payload.name as name from "message.publish" where topic = 't/a' and name = 'EMQ'

-- Select the message body sent to the "command/#" topic
select payload from "command/#"

```



#### The typical functions and application scenarios of message rules are as follows:

- Filter by the topic of the message, specify the message to be processed, and republish to the new topic after processing;

- Develop screening criteria for conditional screening of specific fields of the message body to process data that satisfies the conditions;

- Convert the message body to a preset structure for processing, reduce the resource of internal communication and external storage and calculating;

- Process the message body or specified fields in the message body by using preprocessing methods such as message digest, encoding transformation and mathematical operations, and perform simple calculations in the Broker to reduce operation latency.



#### Each message rule contains the following attributes:

Attribute |Description|
----------|--------------------|
Source |The source of the data stream to be processed, based on the MQTT topic, using the FROM command in SQL to screen |
Condition |Conditional filtering expression for the message body (JSON information only) and message context information (such as QoS, Client ID, Username) that is used to determine the matching condition and message structure of the rule, using the `WHERE` command in SQL for query. |
Processor |Selection expression for message body (JSON information only) and message context information (such as QoS, Client ID, Username) that is used to select and preprocess specified data. Multiple built-in preprocessing methods such as message digest, encoding and decoding and coding conversion, simple mathematical operations in the rule engine, using SQL clauses and SQL function for processing.
Action |The action that needs to be triggered after the message hits the rule and processes it successfully, specifying the specific action operations such as writing the database SQL statement, the object and the topic sent to the message queue. A rule can define one or more actions to implement multi-end processing of rules.



### Event rule

With the event rule in the rule engine, users can process various event information in the device communication life cycle. The typical functions and application scenarios of the event rule are as follows:

- Device event actions log: such as device connection/disconnection, message publishing, sending/arrival/discard, device subscription/unsubscription, and so on, with the purpose of device operation record and behavior analysis;

- Device online and offline notifications and records: Listening for two events of client.connected and client.disconnected, that can be used to record the device's online and offline status;

- Message status record: Listening for the message related event can implement key message command status monitoring, such as "issue success/failure callback".
