Officially launched in September, the official version of [EMQX Enterprise](https://www.emqx.com/en/products/emqx) 3.4.0 is released by EMQ. In this version, the management configuration and rule engine functions are enhanced, message encoding and decoding, cluster hot configuration and vehicle networking protocol support  are added, and a new management monitoring Dashboard page is designed, and this version is a stable version recommended for enterprise applications.

The relevant installation package is ready for download from [EMQ website](https://www.emqx.com/en/try), and  a free self-service application for trial is avaiable from the website.



> EMQX Enterprise is an Enterprise-level Iot MQTT messaging platform that supports one-stop access of millions of IoT devices, MQTT&CoAP multi-protocol processing, and low-latency real-time messaging. It  also supports SQL-based built-in rule engine, flexible processing/forwarding of messages to back-end services, storage of message data to various databases, or bridging of enterprise middleware such as Kafka, RabbitMQ, and Pulsar.
>
> EMQX Enterprise is applicable for a variety of IoT applications, helping enterprises quickly build IoT applications and support the deployment on public clouds, private clouds, physical machines, containers/K8S and so on.



### Brand-new Dashboard UI

In previous versions of EMQX, EMQ has expanded a series of basic functions around MQTT message access to facilitate the rapid construction of IoT applications, such as authentication/ACL, data persistence and message bridging (Enterprise Edition) and integration into Dashboard. .

In order to support the introduction of more new functions and the  improvement of system usability and monitoring management ability after the introduction of functions, EMQ development team took the lead in designing a new Dashboard UI for the enterprise version, adjusting the interface style, operability, application structure and data display focus, and striving to create an IoT Hub Management Platform with comprehensive function:

- Realize full control of EMQX cluster status, add the real-time display interface of key operational indicators;
- Provide aggregate statistics and persistent records of operational indicators and display them at the front end. Cluster history messages, links, topics and subscription indicators are clear at a glance.
- Strengthen business functions, display licensee authorization information including issuing company, number of authorization lines, expiration date, and more convenient and quicker for enterprise operation and maintenance;
- Implement basic equipment management function, simplify connection information, support online kick out equipment, view and manage equipment subscription information, add subscription relationship manually, etc.
- Optimize rule creation steps, provide creation wizards to facilitate quick learning of the enterprise, and clarify the rules engine application relationship;
- Added alarm management, globally displays the current number of alarms, and provides historical alarm record troubleshooting, which is convenient for discovering problems and solving problems and avoiding the risks caused by alarms.

![11111.png](https://static.emqx.net/images/d737da2ec945d7e8e4aa630264d172b9.png)



### Hot configuration of parameters is supported by Dashboard

Prior to 3.4.0, all modifications to the EMQX main configuration `etc/emqx.conf` required a restart to apply, such as anonymous authentication (allow_anonymous), ACL switches and policies (enable_acl), connection statistics (enable_stats),  that all have a need for non-stop changes.

After evaluation, EMQ lists dozens of configuration items that do not affect system stability but have hot configuration requirements, and provide hot configuration capabilities in Dashboard and REST APIs.

![2.png](https://static.emqx.net/images/b89c633085a8e75c186c091d1c50a283.png)



### Cluster management is supported by Dashboard

In this version,  management functions are added for clusters. The visual interface provides invitation and kick-out functions for clusters in manual cluster mode. Cluster parameters are displayed in other automatic cluster modes, which greatly facilitates monitoring  management and the reference configuration of new nodes..
![Dashboard.png](https://static.emqx.net/images/a2be9d0a7ebb7f4e8c22b959f65176a6.png)



### Powerful  Schema Registry 

In the IoT application, in order to balance network transmission performance and device processing capability, many of the underlying device communication relies on message data in a relatively low-level, streamlined format. Broker needs to process various compressed binary data formats and industry-specific data formats, or even a private data format. 

In the past, this kind of data was bridged to the application system and sent back to Broker for processing after the coding and decoding of the application system. The integration of the whole architecture is very complex, which has the problems of high processing delay and unclear processing logic.

To address this pain point, a set of Broker's built-in, real-time codec system Schema Registry is designed and developed by EMQ . The Schema Registry supports Avro, Protocol Buffers and third-party codec service packet parsing.

Schematic diagram for use with both Schema and rules engine:

![Schema Registry .png](https://static.emqx.net/images/e295802e25b24d1c66c85b664b155bb4.png)




At present, three kinds of protocol parsing methods are supported by EMQX :

- Avro is a remote procedure call and data serialization framework developed within Apache's Hadoop project. It uses JSON to define data type and communication protocol, and uses compressed binary format to serialize data, with EMQX Enterprise built-in support;
- Protocol Buffers is a lightweight and efficient structured data storage format that can be used for structured data serialization. It is ideal for data storage or RPC data exchange formats. It can be used for language-independent, platform-independent and extensible serialized structured data formats in communication protocols, data storage and other fields, with EMQX Enterprise has built-in support.
- The third-party codec service delivers the original message data through the TCP and HTTP communication to the external codec service, waiting for the coded data to be returned, and then conducting the subsequent logic. The third-party service can be a self-built codec gateway or even a hot Serverless application in cloud computing.


![4.png](https://static.emqx.net/images/ae6f8f44bfff90d96a714beccf888647.png)



As shown in the figure above, we have created a new codec service, which is used in the rules engine like this:

```sql
SELECT decode('schema:1.0', payload) as payload
FROM 
	"message.publish"
WHERE
	topic =~ 't/#'
```

Using the Schema Registry combined with the rules engine function, the codec rules are created directly in the rules engine through the decode and encode functions. This process greatly simplifies the integration of message applications.

### Support of the  China National Protocol Agreement JT/T808 for vehicle networking

The new vehicle networking protocol access JT/T808, with full name "JT/T 808-2013 Road Transportation Vehicle Satellite Positioning System Beidou Compatible Vehicle Terminal Communication Protocol Technical Specification", is a industry communication protocol. Through the adaptation of the protocol, EMQ has established a complete industry/private protocol access development mode, which provides a successful template for the subsequent customization development of other protocols.

Schematic diagram of JT/T808 protocol access architecture:

![ JT:T808.png](https://static.emqx.net/images/54516d671cbb83d5a21312903517adca.png)





### New version feature planning

In future versions, Dashboard's functions will continue to be enhanced, and the following improvements are planned to be achieved through continuous adjustments and optimizations:

- Optimizing Plug-in Configuration Function: For security reasons, plug-in configurations on Dashboard currently do not persist to Broker. Stable configurations need to be manually written to the configuration file after successful debugging. With the improvement of security of Dashboard and related APIs, subsequent EMQ plans will persist plug-in configurations on the interface. In most scenarios, no additional operations on configuration files are needed.
- Provide plug-in function management interface: At present, Dashboard's management of plug-ins is limited to configuration. Many plug-ins, such as `emqx_auth_clientid, emqx_auth_username, emqx_configs,` have corresponding business functions and usage modes besides basic configuration. EMQ will be adapted and developed one by one in Dashboard to provide plug-in configuration and user interface;
- Plug-in hot installation and hot upgrade: upload binary plug-in package in Dashboard, realize non-stop plug-in installation and upgrade, hot install hot upgrade is mainly used to deal with important repair and small-scale function upgrade of EMQX;
- Customize alarm implementation: user-defined alarm rules and trigger mode will be supported in the future, so that the alarm reminder can not be offline.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
