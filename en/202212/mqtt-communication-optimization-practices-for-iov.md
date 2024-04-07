Intelligence is trending in all industries. Nowadays, vehicle is no longer just a means of transportation, but a mobile intelligent node with autonomous reasoning capability and ability to interact with the cloud for vehicle-road coordination.

Many new application scenarios not only need strong computing power to process large amount of data, but also demand for low latency, low energy consumption, and high reliability on the communication links. Traditional communication protocols such as HTTP cannot simultaneously meet the above requirements. As the de facto standard protocol in IoT, MQTT provides a Pub/Sub message model with a streamlined and excellent protocol design to meet the needs of low latency and consumes much less power than HTTP/WebSocket, which is suitable for intelligent mobility with limited resources. Also, [Internet of Vehicles](https://www.emqx.com/en/blog/mqtt-for-internet-of-vehicles) scenarios are different from the scenarios of smart homes and robots, which have fixed geo-locations and stable connectivity. Under the circumstance of IoV, there are higher requirements for the application of MQTT protocol due to the rapid movement of vehicles, constant switching scenarios, and complex networking conditions.

In this article, we will deeply analyze the cause of problems when applying MQTT on message transmission in mobility scenarios, and use MQTT protocol features to solve the problems and optimize the solutions, so as to help users build a more robust communication architecture for mobile automotive.

<section
  class="promotion-pdf"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/a4b8936bb3d27fbccd734eccbe3f821b.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="promotion-pdf__title" style="
    line-height: 1.2;
">
      Rev Up Your Connected Vehicles Future with MQTT
    </div>
    <div class="promotion-pdf__desc">
      The key to building a scalable, secure system for your connected-vehicles business.
    </div>
    <a href="https://www.emqx.com/en/resources/driving-the-future-of-connected-cars-with-mqtt?utm_campaign=embedded-driving-the-future-of-connected-cars-with-mqtt&from=blog-mqtt-communication-optimization-practices-for-iov" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## What actually happens when you drive at high speed or go through a tunnel?

I believe we all have the similar experiences as below when using 4G phones:

The carrier signal strength suddenly weakens when entering a basement, and ongoing application will experience service interruption although the connectivity sustains; Similar case happens when traveling across the boundary between different networking coverages or switching WiFi AP (wireless access point). This is a typical network migration problem caused by mobile devices. In IoV scenarios, as the vehicles are moving at high speed, especially on highways with sparse base station coverage or through tunnels, this problem will occur more frequently, causing the MQTT connection to be interrupted and reconnected on the automotive side.

The main link that connects vehicle to the mobile network is the 4G base station. It's one of many important factors in delivering high-quality service and distinguishing incumbency from obsolescence. The numbers of 4G base stations is rapidly growing in the past decades, but most of these base stations are concentrated in urban areas, while the signal coverage in the countryside, highways, and tunnels is far less complete than that in cities. At present, network coverage solutions for areas such as highways and national and provincial roads are basically divided into public network extension coverage and private network coverage solutions.

- Public network extension: The route area is planned in unison with the surrounding area and covered by using conventional base station cellular networking. It is also called large network extension coverage because it often extends the network resources of the large network directly to the expressway.

  ![Public network base station coverage diagram](https://assets.emqx.com/images/6ee88c0ad064127989d25d6b9ae2d9ba.png)

  <center>Public network base station coverage diagram</center>

- Private network: optimized for special requirements of special point coverage and line coverage scenarios, and configured with special frequencies, signaling and functions for heterodyne networking. Due to high construction costs, it is often used more for coverage along high-speed railroads. The dedicated network is completely isolated from the public network, and only at specific entrances and exits such as expressway toll booths can one enter or leave the dedicated network.

  ![Dedicated network extension coverage diagram](https://assets.emqx.com/images/075367a119dc245fd8a72ddc900b61fe.png)

  <center>Dedicated network extension coverage diagram</center>

It can be found that the network we use is provided by many cellular base stations built by communication providers. During the rapid movement of a vehicle, the location is updated frequently and often switches between multiple base station coverage areas. This results in a high signaling load on its network and frequent base station switching, which will eventually lead to network link interruptions in the in-vehicle 4G module. Dedicated network coverage can reduce inter-network switching and co-channel interference by using BBU+RRU cell merging technology to solve this problem. However, due to the high construction cost of the dedicated network solution, Internet of Vehicles is more likely to face the first public network coverage solution in actual scenarios.

![Check 4G connection from the management system provided by carrier](https://assets.emqx.com/images/f94103a2283e464a0e32a4f79963035d.png)

<center>Check 4G connection from the management system provided by carrier</center>

As a result, we will find that the 4G connection on the automotive side is constantly on and off as shown in the figure above.



**Doppler effect and tunnel coverage**

In addition to the network problems caused by the base station coverage, the Doppler effect can also cause an increase on latency and packet loss rate when the vehicle is traveling at a very high speed. The higher the vehicle speed, the greater the frequency deviation, the worse the latency, and the greater the probability of packet loss.

![Doppler effect diagram](https://assets.emqx.com/images/58c316b4f6c321e79ebdec84e4146961.png)

<center>Doppler effect diagram</center>

## **What happened to the MQTT connection?**

We have known the network conditions of the vehicle, so how do these factors affect MQTT connection on the automotive side?

As we all know, MQTT connections are also based on the TCP/IP stack. You may have questions: TCP/IP protocol stack has a connection keeping alive mechanism, and MQTT protocol also has the Keep Alive parameter for connection reconstruction and recovery. Even if the base station switch led to a temporary communication interruption, the communication link will be quickly restored when entering the range of the next base station. Then, why it also leads to frequent MQTT connection offline on automotive? To answer this question, we need to analyze TCP/IP and the mobile network access process together.

![TCP/IP handshake process](https://assets.emqx.com/images/02f7f7d058871e3a9e2c9532d05efa08.png)

<center>TCP/IP handshake process</center>

When TCP/IP was first created, it was mainly aimed at stable wired networks. As a reliable transport protocol, it has internal data ACKs that enable data retransmission and connection reuse. However, this is all based on the premise that the IP address remains unchanged, while in Internet of Vehicles scenario, the base station switching will cause changes of the IP address on the automotive side. Each time the 4G module of the automotive enters a new base station coverage area, it will re-initiate a network attachment request.

![Network access process - UE initialization and attachment to UE-UTRAN network](https://assets.emqx.com/images/807d7bb626df44bf3ab44e81f2a8dabf.png)

<center>Network access process - UE initialization and attachment to UE-UTRAN network</center>

The protocol details are not explained here. Since we are still using the IPV4 standard, the 4G module will send a key signaling PDN (Packet Domain Network) to the newly searched eNB base station in the process of reconnecting to the network to request assigning a new IP address for itself. This address is often a NAT address, which is also a part of the technology that 4G terminals are online when they are switched on. This is also accompanied by network quality detection, APN matching and other processes to determine the type of network used by the terminal and push network routing to ensure connectivity. If the edge eNB base station is not optimized for the 4G card and PDN signaling of the automotive, it cannot know the original IP address used by the terminal, and then the IP address changed and needs to be re-bound with NAT address. For long link protocols like MQTT and TCP/IP, after the IP address changes, the TCP server cannot identify whether the current client is still the original client, so the TCP connection has to be re-established, and thus the MQTT connection has to be rebuilt as well.

![Relationship between TCP connections and MQTT connections](https://assets.emqx.com/images/700ce6cbc7404b011b29397707e3517f.png)

<center>Relationship between TCP connections and MQTT connections</center>

The above is the process of a normal fast-moving vehicle switching between cellular base stations. In reality, the network is more complex: the public network coverage solution shares the base station and access network resources, so if the edge base station load is too high, eNB base station will not respond to PDN requests and other situations may occur. The network side does not respond to the bearer requests, not to mention the pseudo base station. In addition, the multipath effect and signal fading caused by geographic environment and Doppler effect can lead to increased latency and connection interruption.

## How to improve MQTT connection stability on mobile networks?

Once the root cause of the problem is clear, we will use the features of the MQTT protocol to solve the above problems and build a more stable communication architecture of Internet of Vehicle to avoid data loss due to reconnections and interruptions.

Although the TCP/IP part cannot be changed, the MQTT protocol provides many configurable parameters and message QoS levels for us to configure. For some critical data, such as important status changes on the automotive side and requests from users, we need to ensure that messages arrive, which requires us to use QoS 1/2.

### Clean Session

First, we need to solve the problem of IP updates causing the client to be unrecognized after a TCP reconnection. We can solve this with the MQTT session hold feature.

> To know more about the MQTT session state, please refer to the article: [MQTT Session](https://www.emqx.com/en/blog/mqtt-session)  

MQTT requires the client and server to store a series of states (i.e., session states) associated with the client identity (ClientID) for the duration of the session. We call the sequence of messages sent and received from the time a client initiates an MQTT connection request to the server, through the connection is broken, until the session expires, as “a session”. A session may last for only one TCP connection, or it may exist across multiple TCP connections. So, using the unique client identifier corresponding to each automotive during such network switching allows the MQTT Broker to recognize the new connection as the previous client even if the TCP connection is rebuilt, and thus retransmit the cached QoS messages and apply the previous connection state.

The client uses clean session, take Java code as an example:

```
public MQTTPublisher(String address, String clientId, boolean cleanSession, int qos) throws MqttException {
this.clientId = clientId;
this.qos = qos;
this.client = new MqttClient(address, clientId, persistence);
MqttConnectOptions connOpts = new MqttConnectOptions();
connOpts.setCleanSession(cleanSession);
this.client.connect();
}
```

### MQTT 5.0

Based on this frequent disconnection and reconnection of network connections, MQTT 5.0 also optimized the protocol response in order to avoid the application layer receiving frequent online and offline events that affect business.

Will Delay Interval: We often use [will messages](https://www.emqx.com/en/blog/use-of-mqtt-will-message) to track and inform clients about their offline. Will messages will be received frequently in this case. So, an important use of the Will Delay Interval is to avoid posting will messages when frequent network connections are temporarily disconnected, since the clients will often quickly reconnect to the network and continue the previous session.

Session Expiry Interval: MQTT 3.1.1 does not explicitly specify session hold time. If a large number of clients using the session hold feature frequently go online and offline, it can cause an increase in Broker memory usage and eventually affect the high availability of the service. So, MQTT 5.0 also designed session expiration time for this case. Clients can use this feature to set their own session hold time when connecting.

### QoS 1/2

After setting the session hold state, we can use QoS messages to ensure that the message arrives.

> A detailed explanation of QoS can be found in the article: [Introduction to MQTT QoS (Quality of Service)](https://www.emqx.com/en/blog/introduction-to-mqtt-qos)  

We recommend using QoS 1 for sending important data on the automotive side and using MQTT SDK with QoS retransmission capability and built-in QoS message window (queue), such as [NanoSDK](https://github.com/emqx/NanoSDK), which features asynchronous acknowledgment, built-in QoS message queue, automatic retransmission, and high throughput and consumption capabilities.

### Broker QoS MsgQueue

QoS messages are persisted in memory on the Broker side. In addition to a built-in message queue on the client side, the Broker also has a QoS message queue. As mentioned above, base station switching that often occurs in Internet of Vehicles scenarios leads to connection reset, which is reflected in MQTT connections as QoS message backlogs. Both the client and server will have unacknowledged messages in the queue. So, we need to set the message queue length according to the actual situation.

Take EMQX as an example, message queue setting:

Open emqx.conf

```
mqtt {
 ## @doc Maximum QoS 2 packets (Client -> Broker) awaiting PUBREL.
 max_awaiting_rel  =  100

 ## @doc The QoS 2 messages (Client -> Broker) will be dropped if awaiting PUBREL timeout.
 await_rel_timeout  =  300s

 ## @doc Maximum queue length. Enqueued messages when persistent client disconnected, or inflight window is full.
 max_mqueue_len  =  1000
}
```

`max_awaiting_rel` is the message queue length for accepting QoS 2. QoS 1 has no limit for this item.

`await_rel_timeout` is the QoS 2 message timeout time.

`max_mqueue_len` is the cache length of the queue for downlinking QoS 1/2

The default QoS 2 message queue length is only 100. Here, it is recommended to increase it according to the frequency of publishing messages to the client and the consumption capacity. Generally, it is considered to be the average number of messages per second generated by the publisher *2. This queue provides a certain buffer time for the consumer side to finish consuming the backlog of messages after reconnection.

![Broker QoS MsgQueue](https://assets.emqx.com/images/6fc5308177d8974ab2aa4a3674e43907.png)

## A more excellent solution: MQTT over QUIC

TCP uses quaternions to identify the uniqueness of a connection, while UDP does not have the same requirement. On June 11, 2022, the IETF officially published the HTTP/3 RFC technical standards document, making the UDP-based QUIC one of the transport layer standards. The QUIC-based MQTT solution is also expected to become the next industry standard.

With the QUIC protocol's address migration, streaming multiplexing, split flow control, and lower connection establishment latency, we expect to completely solve the connectivity problem in Internet of Vehicles scenarios.

![0-RTT Diagram](https://assets.emqx.com/images/e759647760382f083fd64d0b82800f42.png)

![0-RTT Diagram](https://assets.emqx.com/images/e08d6490681f8931d06f54bed496424e.png)

<center>0-RTT Diagram</center>

QUIC can detect address changes and automatically re-establish the connection using 0-RTT approach, making the client and server unaware of IP address changes, thus completely avoiding a series of problems described above.

<section
  class="promotion-pdf"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/129d83b2aebdc64d6c1385236677b310.png" alt="MQTT over QUIC" width="160" height="226">
  </div>
  <div>
    <div class="promotion-pdf__title" style="
    line-height: 1.2;
">
      Next-Gen Standard Protocol for IoV
    </div>
    <div class="promotion-pdf__desc">
      Revolutionizing IoV messaging with MQTT over QUIC.
    </div>
    <a href="https://www.emqx.com/en/resources/mqtt-over-quic-revolutionizing-iov-messaging-with-the-next-gen-standard-protocol?utm_campaign=embedded-mqtt-over-quic&from=blog-mqtt-communication-optimization-practices-for-iov" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## Epilogue

In this article, we analyze the causes of MQTT communication instability in Internet of vehicles mobile scenarios; and we solved the data loss problem caused by unstable connections due to high-speed mobility to a certain extent by using MQTT protocol features, such as clean session, QoS, client ID configuration, and built-in message queue caching on the client and server sides.

In addition, as mentioned earlier, MQTT over QUIC may be a better solution in comparison. The latest release of [EMQX 5.0 supports MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic) and is designed with a unique messaging mechanism and management method, which can effectively reduce the data packet loss rate and handshake latency. Internet of Vehicles users can use EMQX 5.0 to get a more efficient and low-latency IoT data transmission experience. With EMQ's active promotion in the MQTT over QUIC standardization process, it is believed that the message transmission problems in the scenarios of weak network and unfixed network path in Internet of vehicles and other IoT industries will be further solved in the future.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
