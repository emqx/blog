In the latest version 5.0, EMQX made a breakthrough by relaying MQTT message over QUIC protocol.

QUIC (RFC 9000) is the underlying transport protocol of the next-generation Internet protocol HTTP/3, which provides connectivity for the modern mobile Internet with less connection overhead and message latency compared to TCP/TLS protocols.

Based on the advantages of QUIC, which make it highly suitable for IoT messaging scenarios, EMQX 5.0 introduces QUIC support (MQTT over QUIC) and designs a unique messaging mechanism and management approach.

This article will explain MQTT over QUIC in detail to show the advantages and value of this leading technology implementation for IoT scenarios. Readers will be able to leverage EMQX 5.0's support for QUIC through this article, and make the IoT data transfer more efficient, stable, and low-cost in various MQTT application scenarios.

## What is QUIC?

[QUIC](https://datatracker.ietf.org/doc/html/rfc9000) is a common transport layer network protocol built on top of UDP, originally proposed by Google as an alternative to TCP+TLS to improve end-to-end user experience.

QUIC has many advantages over existing TLS over TCP implementation:

- High-performance low latency of connection handshake with one round trip or zero round trip.

  QUIC reduces the overhead during connection setup. As most of the network connections will demand TLS, QUIC exchanges the TLS keys in the initial handshake process. When the client opens a connection, the response contains the data needed for further encryption. This eliminates the need to set up the TCP connection and then negotiate the security protocol over TLS. And most important it saves round trips during connection setup and thus reduces the overall connection setup latency.

- QUIC runs over UDP

  QUIC runs over UDP not TCP. QUIC stream is separately flow controlled and lost data retransmitted at the level of QUIC, not UDP. This means that if an error occurs in one stream would not affect the other streams in the same connection. For the application over the QUIC layer, data processing will not be blocked due to some error in a single multiplexed stream thus improving the parallelization and overall performance.

- End-to-end encryption, handshake authentication via TLS 1.3

- Multiplexed connections

  Allowing one connection carries multiple streams for parallelization.

- Improved congestion control, pluggable congestion control policies

  Application over QUIC, runs closely to QUIC stack can do flow control on its own and also get involved for congestion control.

  This makes the Application very flexible for priority traffic, rate-limiting, and managing overloaded situations.

- Multipath support for smooth connection migration

  QUIC supports connection migrations on both server and client side, that makes connection can get kept alive even lower layer network is switched such like the client is moving from Wifi access network to cellular network (4G, 5G). 

- Existing networks can be supported without retrofitting or upgrading

  QUIC has become the underlying transport protocol for the next-generation Internet protocol, HTTP/3.

> **Introduction to the HTTP/3 protocol**
>
> In October 2018, the IETF's HTTP and QUIC Working Group jointly decided to name HTTP mapping over QUIC as [HTTP/3](https://en.wikipedia.org/wiki/HTTP/3) in order to accelerate its adoption as a global standard. On June 6, 2022, the IETF standardized HTTP/3 to [RFC](https://en.wikipedia.org/wiki/Request_for_Comments) <sup>[9114](https://datatracker.ietf.org/doc/html/rfc9114)</sup>.
>
> The goal of HTTP/3 is to provide fast, reliable and secure Web connections on all types of devices by solving the transport-related problems of HTTP/2. HTTP/3 uses similar semantics to the HTTP/2 version, including the same request methods, status codes and message fields. The fundamental difference is that HTTP/2 uses TCP/TLS as the underlying protocol, whereas HTTP/3 uses QUIC.
>
> According to W3Techs, at least 40% of Internet traffic is over QUIC, and 25% of the top 10 million websites already support the HTTP/3 protocol, including top-streaming sites such as Google, Youtube, Facebook, etc.

## Prospects for QUIC in MQTT communication scenarios

MQTT is a connection-based IoT communication protocol with a compact message structure that enables stable transmission over severely constrained hardware devices and low-bandwidth, high-latency networks. The keep alive mechanism, will message, QoS, and many other features can cope with various IoT scenarios.

Nevertheless, the MQTT protocol has inherent drawbacks in certain complex network environments due to underlying TCP transport protocol limitations.

- Frequent connection interruptions due to network switching
- Difficult to re-establish connection after disconnection: the operating system is slow to release resources after disconnection, and the application layer cannot sense the disconnection status in time, and the Server/Client overhead is high when reconnecting
- In a weak spotty network environment, data transmission is blocked by congestion, packet loss, and retransmission

For example, connected vehicle users usually face similar problems: vehicles may run in mountainous areas, mines, tunnels, etc., which can cause connection interruptions when entering signal dead zones or passively switching base stations(also referred to as spotty network). Frequent connection interruptions and slow connection establishment can lead to poor user experience. In some services with high requirements for real-time data transmission and stability, such as the L4 driverless vehicle, it costs a lot for customers to mitigate this problem.

In these scenarios, the low connection overhead and multi-path support of QUIC shows its strengths. After deeper exploration, we believe that MQTT over QUIC is a great solution to this dilemma - based on QUIC's 0 RTT/1 RTT reconnect/new capability and migration support, it can effectively improve user experience in weak networks and irregular network paths.

## MQTT over QUIC implementation of EMQX 5.0

The current implementation of EMQX replaces the transport layer with a QUIC Stream, where the client initiates the connection and creates a bi-directional Stream. EMQX and the client interact on it.

Considering the complex network environment, if for some reason the client fails to complete QUIC connection handshake, it is recommended that the client automatically fall back to a traditional TCP connection to ensure connectivity. 

![MQTT over QUIC](https://assets.emqx.com/images/ab1fd9ac55e41a49deb66b5e19cf354d.png)

MQTT protocol can benefit from using QUIC as its transport as follows:

- Keep connection alive even after network switch, NAT rebinding.
- Fast connection establishment, reduces handshake latency.
- Mitigating frequent connect/reconnect
- Quick connection recovery
- **More advanced congestion control:** effectively reduces packet loss and enables continuous and stable data transmission despite network fluctuations in tests
- **Operationally and maintenance friendly:** reduce overhead (time overhead, client/server performance overhead) caused by massive reconnection, reduce system overload caused by unnecessary application layer state migration (0 RTT)
- **More flexible architectural innovations:** e.g., Direct server return (DSR, direct server return mode), where only ingress/request traffic passes through the LB and egress and response traffic bypasses the LB and goes directly back to the client, reducing bottlenecks in the L
- **Multi-path support for smooth connection migration:** handover from 4G to WIFI, or if the quintet changes due to NAT Rebinding, QUIC can maintain a connection on the new quintet, especially for mobile devices where the network changes frequently
- **More agile development and deployment:** It is suggested to implement the QUIC protocol stack in the userspace, enabling fast iterations, quic bugfix rollout and reduce the lead time from PoC to production.
- **End-to-end encryption:** QUIC packet leaves minimal information unencrypted in the headers to make communication secure and uninterceptable by middleboxes.

There are also more opportunities to be explored:

- **Streams with different topics:** We could use parallel streams in the same connection to carry different topics to make sending/receiving process parallelized with different priorities and mitigate the HOL (Head Of Line) blocking issue.
- **Streams with different QoS:** For example, in "Flow Control", QoS 0 messages should give way to high QoS message.
- **Separate control messages into different streams:** MQTT control messages can be sent in one or two directions. For example, the client can send UNSUBSCRIBE requests asynchronously through a short-lived unidirectional stream to request the server to stop sending data that is no longer of interest.
- **Finer-grained send and receive collaborative flow control:** Flow control is performed on a per-flow basis or across the entire connection, enabling finer-grained flow control.

## QUIC vs TCP/TLS

We simulated the performance of QUIC and TCP/TLS under different scenarios based on EMQX v5.0 in the lab environment.

**Test Environment**

- Test platform: EMQX 5.0 with single node
- Server specification: AWS EC2 M4.2xlarge (8 cores 32GB)
- Operating system: Ubuntu 20.04
- Number of clients: 5000
- loadgen parallel number: 8
- latency measurements: P95 (percentile) 

### Client connection latency

This is to compare the handshake performance, MQTT connection setup establishment, and subscription completion at different network latencies(ping roundtrip). 

With 1ms roundtrip time,  QUIC and TLS do not show that many differences in latency performance.

As the latency grows, 30ms roundtrip time, QUIC outperforms TLS a lot.

We could conclude that MQTT over QUIC fits well in a network that has high latency.

 
![1ms latency](https://assets.emqx.com/images/6ec16485127c7b3af944f415b0ec374f.png)

<center>1ms latency</center>

![10ms latency](https://assets.emqx.com/images/29183f0df07a6fa9d816c996f8607361.png)

<center>10ms latency</center>

![30ms latency](https://assets.emqx.com/images/675ae637c908e2281644e67d59d6591f.png)

<center>30ms latency</center>

### 0 RTT reconnection latency

This is to test the latency required to reinitiate a connection and resume reconnection after a disconnection.

After the 1-RTT scenario, EMQX would send NST (new session ticket) to client for reentering, client could use this session ticket to reestablish the connection to server by encrypting the first packet it is sending. this is what we called 0-RTT scenario. QUIC can also carry the application layer packet on the first packet in the 0 RTT scenario.

Application layer could exchange data much earlier while the TCP/TLS requires at least 2 roundtrips to finish the handshake and then start exchanging application data.

![0 RTT reconnection latency](https://assets.emqx.com/images/a54c9d8c85f5328b93ecbbef3ed84a87.png)

The benefit of 0 RTT is that it effectively reduces the handshake overhead and improves performance (handshake latency) for both the client and the server. EMQX sends NST packets to the client by default, with a validity of 2 hours.

However, since 0 RTT early data is not protected against replay attacks, QUIC recommends not carrying data on 0 RTT that would change the application state.

> EMQX does not support early data by default, and this test is only used for comparison and verification.

The test results show that QUIC outperforms pure TCP after the first handshake if the MQTT layer protocol is properly designed.

![0 RTT reconnection latency](https://assets.emqx.com/images/c480ba4b1e495eb9faff3c9743d8579c.png)

### Server resource usage when connecting/reconnecting

This test is for the resource usage comparisons in the scenario of massive client connect, disconnect and then reconnect.  The results show that QUIC outperforms TLS in terms of CPU and memory usage, but reconnection consumes more bandwidth than TLS. Due to different implementations, here we compare the performance of two implementations (TCP/TLS and QUIC) in EMQX

| **Test Items**                       | **QUIC**           | **TLS**         |
| :----------------------------------- | :----------------- | :-------------- |
| CPU (first connection)               | ~60%               | ~80%            |
| CPU (reconnect)                      | ~65% ¹             | ~75%            |
| Maximum memory usage                 | 9 GB               | 12 GB           |
| Network bandwidth usage (Trans+Recv) | Peak value 100Mb ² | Peak value 30Mb |

> Note 1: mainly refer to the additional overhead of MQTT clearing sessions and kicking off old connections
>
> Note 2: Mainly refer to the large number of QUIC initial handshake packets due to transport path MTU validation

![Grafana](https://assets.emqx.com/images/3108ce23fc605d03a2698faf98d1e241.png)

### Client address migration

This test simulates the changes in business layer messaging during large-scale client address migration.

When the client source address (address and port) is changed, traditional TCP/TLS clients must detect a disconnect, failure of routing or packet loss at the application layer before reconnecting. This process is very slow due to various timers and involves many unnecessary retransmissions, loss recovery, etc. The application over TLS runs into the blocking state, before it starts to clean the state and reestablish the connection, the application data exchange is blocked.  

QUIC's processing is smoother, keeping connections alive when the address is switched without requiring reconnections and leaving the application to no perception (however the application layer can subscribe to address changes if needed).

This result shows that QUIC is well suited for environments where networks are frequently switched.

![Grafana](https://assets.emqx.com/images/ea72707f0db3796196d8712292aadd74.png)

### Network packet loss test

This is to test the data transmission in the weak network condition. We did three separate tests: EMQX terminated TCP/TLS, QUIC, and Ngnix terminated TCP/TLS.

Test scenario: EMQX publishes QoS 1 messages at the rate of 20K/s and network errors are injected during the process: 20% out of order (inconsistent order of packets at the sender and receiver side), 10% packet loss. Additional network switching interferences are added every 30 seconds in the QUIC test.

In this case, the data received by the QUIC server is slightly jittery, but no messages are lost; while TLS shows congestion and packet loss due to a poor network environment. This result shows that QUIC can provide reliable transmission in a weak spotty network environment.

![Grafana](https://assets.emqx.com/images/8a64b8e0b7116433c18888821fe2fb6c.png)

![Grafana](https://assets.emqx.com/images/6eb8067fc845ca58c14b844f523ee0bf.png)

> When we removed the network error, we can see in the yellow circle that TLS sending and receiving is back to normal, the number of packets is consistent without stacking, while the QUIC has only gone from slightly jittery to smoother.

## Easier to use: MQTT over QUIC SDK

[NanoSDK](https://github.com/nanomq/NanoSDK/) 0.6.0 has released the first C language MQTT over QUIC SDK based on the MsQuic project.

NanoSDK provides a better IoT connectivity experience by adding QUIC support to the transport layer of NNG, enabling protocols such as MQTT and nanomsg to move from TCP to UDP. It internally binds QUIC Stream to MQTT connection mapping and has a built-in function of 0 RTT fast handshake reconnection.

> For message code example, please refer to [NanoSDK QUIC Demo](https://github.com/nanomq/NanoSDK/blob/main/demo/quic/client.c).

We will also release SDKs for Python, Go, and other languages based on the NanoSDK in the near future, so that more users can experience the advantages of MQTT over QUIC as soon as possible.

At the same time, the relevant SDK will support QUIC to TCP fallback. When QUIC is not available, the connection layer will automatically switch to TCP/TLS 1.2, ensuring that services can operate normally in all types of network environments.

![MQTT over QUIC SDK](https://assets.emqx.com/images/da19ba7b24d557ba10f6ff9a104e6f07.png)

NanoSDK and EMQX send and receive messages through QUIC

## Future EMQX QUIC

![Future EMQX QUIC](https://assets.emqx.com/images/e1636c3a5d5fb4dd7538ff76caa6a4a6.png)

Combining QUIC features with IoT scenarios, we have planned many features for MQTT over QUIC, such as topic prioritization by differentiating control channels, non-reliable real-time streaming for high-frequency data transfer scenarios, and flexible topic and data channel (Stream) mapping to reduce interference between topics. These will may be presented in future releases depending on the feedback from the community and our customers.

EMQ is also actively promoting the standardization of MQTT over QUIC. We are preparing a draft proposal about MQTT over QUIC after becoming the only Chinese company with voting rights in the OASIS MQTT Technical Committee in 2018 and participating in the 5.0 protocol standard development. We believed that in the near future, the underlying protocol of MQTT will support both TCP and QUIC, benefiting the entire IoT industry.

## Epilogue

It’s quite obvious that QUIC is very suitable for the weak, lossy, spotty IoT network environment where the UDP MTU size of the traditional TCP/IP network can be guaranteed or the environment where the network is frequently switched. QUIC has great potential for IoT scenarios where the devices are constantly on the move (such as the Internet of vehicles, mobile collection, etc.), or the device wants to keep long living MQTT session while has to sleep periodically.

MQTT over QUIC of EMQX 5.0 is the first implementation around the world, making EMQ once again lead the global trend of MQTT brokers. EMQ will continue the technological innovations to drive the continuous iterative upgrade of products and provide a reliable infrastructure for the IoT field to power business innovation.


<section class="promotion">
    <div>
        Get Scalable and Robust IoT Connectivity with EMQX 5.0
    </div>
    <a href="https://www.emqx.com/en/try?product=broker" class="button is-gradient px-5">Get Started →</a>
</section>
