## Introduction of MQTT publish/subscribe mode

MQTT is based on the **Publish/Subscribe** mode for communication and data exchange, which is essentially different from the  **Request/Response** mode of HTTP.

**Subscriber** will subscribe to a **Topic** to the **Broker**. After a successful subscription, the broker forwards the message under the topic to all subscribers.

Topic uses ‘/’ as a separator to distinguish between different levels. Topics containing the wildcard ‘+’ or ‘#’ are also called as **Topic Filters**, and topics without wildcards are called **Topic Names**. E.g:

```
sensor/1/temperature

sensor/1/#

sensor/+/temperature
```



## Introduction of MQTT broker 

#### MQTT broker definition and function

[MQTT broker](https://www.emqx.io/products/broker), also known as the MQTT message server, can be a server or a cluster of servers running MQTT message server software. MQTT broker is responsible for receiving network connections from the client and handling the client's requests of Subscribe/Unsubscribe and Publish, as well as forwarding the messages published by the client to other subscribers.

MQTT broker is widely used in the industries of  power, new energy, smart city, smart home, smart meter reading, vehicle networking, finance and payment, operators and so on.

![mqttbroker.png](https://static.emqx.net/images/8d8c91c5ca707baa23974eccac269a04.png)

#### Common open source MQTT broker

- [EMQ X](<https://github.com/emqx/emqx>) - EMQ X is developed based on the Erlang/OTP platform and is the most popular MQTT broker in the open source community. In addition to the MQTT protocol, EMQ X also supports protocols such as MQTT-SN, CoAP, LwM2M, and STOMP. Currently, EMQ X has more than 5,000 corporate users and more than 20 partners  of  world top 500 in the global market.
- [Eclipse Mosquitto](<https://github.com/eclipse/mosquitto>)- Mosquitto is an early open source MQTT broker that includes a C/C++ client library and command line clients of `mosquitto_pub` and `mosquitto_sub` for publishing and Subscribing. Mosquitto is lightweight and suitable for use on all devices from low-power single-board computers to  servers.
- [VerneMQ](<https://github.com/vernemq/vernemq>) - VerneMQ is a high-performance, distributed MQTT message broker. It scales horizontally and vertically on commodity hardware to support a high number of concurrent publishers and consumers while maintaining low latency and fault tolerance. VerneMQ is the reliable message hub for your IoT platform or smart products.
- [HiveMQ CE](<https://github.com/hivemq/hivemq-community-edition>) - HiveMQ CE is a Java-based open source MQTT broker that fully supports MQTT 3.x and MQTT 5. It is the foundation of the HiveMQ Enterprise Connectivity and Messaging Platform.



## Main functions implemented by MQTT broker

#### Protocol access

- Full MQTT V3.1/V3.1.1 and V5.0 protocol specification support;
- IoT protocol access support such as MQTT-SN, CoAP, lwM2M.

#### Cluster deployment

Support multi-server node clustering and support automatic discovery of nodes. Compared to a single server, a cluster can bring the following advantages through collaboration between multiple servers:

- High availability. Failures of a single or a small number of server  will not cause the stop of entire message service, and the remaining nodes that are working normally can continue to provide services;
- Load balancing. Through the load balancing mechanism, the cluster can distribute the load evenly across the nodes;
- Higher overall performance. Compared with single deployment, multi-node clusters can double the connection and message processing capabilities of the entire system;
- Scalability. Capacity expansion can be done by adding new nodes to the cluster without downtime.

#### Access security

- SSL, WSS encrypted connection, and single/two-way security authentication support ;
- Client ID, IP address, username and password, LDAP and browser cookie authentication support;
- Access Control (ACL) based on client ID, IP address, username;
- Limit of message rate and connection rate.

#### Data persistence

The main usage scenarios of data persistence include recording the client's online and offline status, subscribed topic information, message content, and sending message receipts after the message arrives to various databases such as Redis, MySQL, PostgreSQL, MongoDB, and Cassandra.

#### Other functions

- HTTP message publishing interface support, which makes it easier for upper-layer applications to send messages to devices through the REST API;

- MQTT broker bridging, that supports message bridging between different MQTT brokers or different clusters. Bridging makes it easy to bridge messages to cloud services, streaming services, or other MQTT message servers. Bridging can accomplish some functions that cannot be achieved by simply using a cluster, such as deploying across VPCs, supporting heterogeneous nodes, and increasing the service limit for a single application;

- Support for shared subscriptions. Shared subscription is a mechanism that allows the distribution of messages for a subscription group to be evenly distributed to members of a subscription group. In a shared subscription, clients that subscribe to the same topic receive messages under this topic in turn. The same message will not be sent to multiple subscribing clients, thus achieving load balancing between multiple subscribing clients;

- Rule engine support for configuring the processing and response rules of message streaming and device events. The rules describe three configurations of w**here the data comes from, how to filter and process the data ,  where the results go to.** One of the available rules contains three elements: trigger event ( Trigger when satisfying certain conditions, process rules (filtering and processing data from context information), response actions (such as persistence to database, republishing processed messages, forwarding messages to message queues, etc.).

  

## Use of MQTT broker

To facilitate testing, we use the online broker provided by  [EMQ](<https://github.com/emqx/emqx>) , which contains all the functions of EMQ X Enterprise.

> **Broker address**： broker.emqx.io
>
> **Broker port**： 1883、8883（SSL）、8083（Websocket）、8084（WSS）

We use the online version of the WebSocket tool provided by EMQ to connect to the client :[http://tools.emqx.io](http://tools.emqx.io/)。

#### MQTT broker connection

Open the address [http://tools.emqx.io](http://tools.emqx.io/) using the browser, click the **New Connection** button in the lower left corner, and fill in the link information in the box on the right. Fill out the required fields and click the **Connect** button to create a link and connect to the Broker.

![image20191021162759103.png](https://static.emqx.net/images/30b5213111f97b77b0d240bf362c5884.png)

#### Publish message

After the connection is successful, click **Write a message** in the lower right corner to pop up the message publishing box, fill out **Topic** and **Payload** and click the send icon to publish the message.

![image20191021163628054.png](https://static.emqx.net/images/f79cc8b5a60eae7893b32789a998e54a.png)

#### Topic subscription

- **Subscribe to regular topics**

  In the  **Subscriptions** module, subscribe to the **hello** topic. At this point, if you send a message to the **hello** topic, the message will be received in the message list (the message received on the left).

![image20191021164254287.png](https://static.emqx.net/images/97f3b1c0c5b962188060fab5ea27ae7a.png)

- **Subscribe to wildcard topics**

  Subscribe to the wildcard topic **testtopic/#** and send a message to the **testtopic/1** topic, which will be received in the message list.

![image20191021164555568.png](https://static.emqx.net/images/69709893f3708fbb33428eb3f53b1484.png)

