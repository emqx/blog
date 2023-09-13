With the development and popularity of IoT technology, more and more smart devices are equipped with network connectivity and data transmission capability.

Most of the devices in IoT scenarios are resource-constrained, such as CPU, RAM, Flash, and network broadband. In particular, battery-powered devices are sensitive to power consumption and transmission protocol bandwidth. Also, the direct use of TCP and HTTP protocols for data exchange between devices and platforms cannot meet the requirements of devices for low power consumption.

To enable these devices to access the network smoothly, the [CoAP protocol](https://www.emqx.com/en/blog/iot-protocols-mqtt-coap-lwm2m) was born. As a fully managed MQTT messaging service dedicated to providing data connectivity for various IoT scenarios, [EMQX Cloud](https://www.emqx.com/en/cloud) also supports CoAP protocol access to devices, allowing them to publish, subscribe, and receive messages to EMQX Cloud in a defined CoAP message format.

>**EMQX Cloud Introduction**
>
>EMQX Cloud is a fully managed cloud-native MQTT service from EMQ that connects to massive IoT devices and integrates with various databases and business systems.
>
>As the world's first fully managed MQTT 5.0 public cloud service, EMQX Cloud provides one-stop O&M colocation and MQTT messaging services in a unique isolated environment.
>
>In the era of the Internet of Everything, EMQX Cloud can help users quickly build industry applications for the IoT field and can help users quickly build industry applications for the IoT field, and easily realize the collection, transmission, calculation, and persistence of IoT data.
>
>EMQX Cloud is available in dozens of countries and regions around the world, providing low-cost, secure, and reliable cloud services for 5G and Internet of Everything applications, with infrastructure computing facilities provided by cloud providers.


This article will describe how to use EMQX Cloud to access CoAP protocol devices.

## Introduction to the CoAP Protocol 

Due to the complexity and diversity of IoT scenarios, hardware conditions at the device side, network stability, traffic limitations, device power consumption, and the number of device connections, the messaging of IoT devices is very different from the traditional Internet scenarios, and therefore a variety of IoT communication protocols have been created.

CoAP protocol gateway is a kind of HTTP-like protocol in the IoT world, used in resource-constrained IoT devices, its detailed specification is defined in RFC 7252.

### Protocol Features 

CoAP is based on many HTTP design ideas but also improves many design details according to the specific situation of resource-constrained devices, adding many practical features. For example：

- Based on the message model
- Transport layer based on UDP protocol, supporting restricted devices
- Use a request/response model similar to HTTP requests, HTTP is in text format, CoAP is in binary format, and more compact than HTTP
- Supports bi-directional communication
- Lightweight and low power consumption
- Supports reliable transmission, data retransmission, and block transfer to ensure reliable data arrival
- Supports IP multicast
- Supports watch mode
- Support asynchronous communication

### Market Status 

Compared to [MQTT](https://www.emqx.com/en/mqtt-guide), CoAP is lighter, has lower overhead, and is more appropriate in the certain device and network environments.

## CoAP Protocol Access to EMQX Cloud 

### Create Deployment 

Create a new deployment and get the public network connection address: 120.77.x.x on the EMQX Cloud deployment page.

![1.png](https://assets.emqx.com/images/2b6ae176fa00cb2aedda20233b52ab5a.png)

### Turn on the CoAP Access Gateway

CoAP access gateway is currently in internal testing, you can submit a work order to enable the access capability. Once enabled, the CoAP Access Gateway address is your deployment connection address, 120.77.x.x, on port udp 5683.

### Connecting to deployments, publishing messages

The [libcoap](https://github.com/obgm/libcoap) is a very easy-to-use CoAP client library, and we use it here as a CoAP client to test the functionality of the EMQX Cloud CoAP access gateway.

The installation and deployment can be seen in the following example.

```
git clone http://github.com/obgm/libcoap
cd libcoap
./autogen.sh
./configure --enable-documentation=no --enable-tests=no
make
```

#### 1. Publishing Example 

We use libcoap to publish a message to the EMQX Cloud deployment.

- Topic name: "topic1"
- Client ID: "client1"
- User name: "emqx"
- Password: "public"
- Payload: "hello,EMQX Cloud"

```
# CoAP terminal sends the message "hello EMQX Cloud"，topic 为 topic1
./examples/coap-client -m put -e "hello,EMQX Cloud" "coap://120.77.x.x:5683/mqtt/topic1?c=client1&u=emqx&p=public" 
```

![CoAP terminal sends the message](https://assets.emqx.com/images/7983bafd716c5f631cc16173dd4cdc91.png)

Next, we use [MQTTX](https://mqttx.app) to subscribe to the corresponding `topic1`, you can see that the message has been successfully published.

![MQTTX receive messages](https://assets.emqx.com/images/73eb0bb27c70213dded07d7569cebba1.png)

#### 2、Subscription Example 

We use libcoap to subscribe to a topic.

- The topic name is: "topic1"
- Client ID is: "client1"
- User name: "emqx"
- Password is: "public"
- Payload is: "hello,EMQX Cloud"

Next, we use MQTTX to send "hello, EMQX Cloud" to `topic1`.

![MQTTX send messages](https://assets.emqx.com/images/45f5cd23ad12da6b86d95b901d91bbbe.png)


```
# CoAP terminal subscribe to topic1，-s 20 means the subscription is maintained for 20 seconds
 ./examples/coap-client -m get -s 20 "coap://120.77.x.x:5683/mqtt/topic1?c=client1&u=emqx&p=public"
```

In the meantime, if a message is generated on `topic1`, libcoap will receive it.

![libcoap receive messages](https://assets.emqx.com/images/8efbf3a5b5df7a91ee6783b1ccfb5ea6.png)

## Summary 

At this point, we have completed the whole process of using the CoAP protocol gateway to access EMQX Cloud.

Currently, IoT protocols are diversified, different protocols apply to different industries and scenarios, and there are multiple protocols available in the same scenario. The CoAP protocol gateway provides a new possibility to solve the data connectivity problem of IoT devices. EMQX Cloud supports multi-protocol access and connects hundreds of millions of IoT devices reliably to EMQX Cloud through open standard IoT protocols MQTT, [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket), CoAP/LwM2M, so that IoT data can be more valuable.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
