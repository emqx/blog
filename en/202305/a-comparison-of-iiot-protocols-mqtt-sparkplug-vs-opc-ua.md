## Introduction

Industrial systems rely heavily on efficient and secure communication protocols to exchange data seamlessly. Two prominent contenders in this space are [MQTT Sparkplug](https://www.emqx.com/en/blog/mqtt-sparkplug-bridging-it-and-ot-in-industry-4-0) and OPC UA. In this blog, we will comprehensively compare MQTT Sparkplug and OPC UA, and their successors, offering a clearer understanding of which protocol aligns best with your specific requirements.

## OPC Classic and OPC UA

The precursor of OPC UA is OPC Classic (also known as OPC DA or OPC Data Access), a set of industrial automation standards developed by the OPC Foundation. First published in 1996, the OPC Classic specification defines a standardized method for exchanging data between software applications and industrial hardware devices such as sensors, controllers, and programmable logic controllers (PLCs).

However, one of its major drawbacks is that OPC Classic is tightly integrated with the Microsoft Windows operating system and its proprietary DCOM technology. This type of dependency severely compromises the protocol's usability, scalability, interoperability, security, and platform independence, which is a significant limitation for an open standard.

In response to these limitations, the OPC Foundation started work in 2006 on OPC Unified Architecture (UA) as a successor to the OPC Classic specification. Both specifications have a functionally equivalent protocol, but use different underlying communication technologies. In addition, OPC Classic DA 3.0 was released the same year and is still in use today.

## IoT-Ready Protocol: Evolution of MQTT 

In the late 1990s, Andy Stanford-Clark and Arlen Nipper were working on a pipeline monitoring project that required a lightweight protocol for communicating with remote sensors and devices. The project required monitoring capabilities in a low-power, low-bandwidth environment. However, existing messaging protocols such as HTTP and SMTP were considered too heavy and inefficient for this specific use case.

To address these challenges, [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) was developed as a publish/subscribe (Pub/Sub) messaging protocol. MQTT was designed with a small code footprint and minimal bandwidth requirements, making it suitable for deployment in low-power, low-bandwidth environments. Its primary purpose is to facilitate large-scale, real-time data exchange between devices and systems, enabling standardized data communication even when different formats and structures are involved. This characteristic makes MQTT particularly suitable for IoT and M2M (machine-to-machine) applications.

In 2010, MQTT was released as an open standard by OASIS (Organization for the Advancement of Structured Information Standards), making it available to a wide range of organizations and industries. Then, in 2014, MQTT 3.1.1 was introduced, including several new features such as improved error handling and support for Quality of Service (QoS) levels. Then, in 2019, MQTT 5.0 was released with significant enhancements such as support for custom properties, persistent sessions, and improved error reporting.

## Combining the Advantages: OPC UA over MQTT

The [MQTT publish/subscribe (pub/sub) model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) offers several advantages over the classic OPC UA client-server model, including:

- Scalability: The pub/sub model can effectively handle a large number of devices and systems, making it well-suited for industrial automation and IoT applications.
- Real-time data exchange: The pub/sub model is specifically designed to facilitate real-time data exchange, enabling devices and systems to promptly respond to environmental changes.
- Reduced network traffic: The pub/sub model helps reduce network traffic by allowing devices and systems to receive only the data they are interested in, rather than receiving all data from all sources.

The OPC Foundation released the OPC UA Pub/Sub specification in 2018. This specification defines a publish-subscribe communication model for OPC UA, which can be implemented using the MQTT (Message Queuing Telemetry Transport) protocol as a transport mechanism. OPC UA's Pub/Sub model is a powerful new feature that provides significant benefits for industrial automation and IoT applications.

## Enhancing Industrial Connectivity: MQTT Sparkplug Specification

The MQTT protocol has achieved great success in IoT scenarios. However, its applicability to industrial automation systems is limited due to a lack of interoperability. To address this limitation, Cirrus Link Solutions introduced the Sparkplug specification in 2016, aiming to simplify the implementation of MQTT in industrial automation systems. This specification establishes a standardized format for MQTT messages, facilitating the exchange of data between different devices and applications.

One notable feature of Sparkplug is its support for bi-directional communication between devices. This capability enables devices to not only send commands but also receive responses from other devices within the network.

5 key concepts to explain why MQTT Broker is perfect for implementing Sparkplug design principles: [5 Key Concepts for MQTT Broker in Sparkplug Specification](https://www.emqx.com/en/blog/5-key-concepts-for-mqtt-broker-in-sparkplug-specification).

## OSI Model Overview

MQTT and OPC UA are the two main popular protocols used in industrial automation and IoT applications, and they have different architectures and designs that reflect their different intended uses. Here is a comparison of MQTT, OPC UA, and their variants in terms of the OSI (Open Systems Interconnection) model:

| **OSI Model**          | **MQTT**          | **OPC UA**                           | **MQTT Sparkplug**                      | **OPC UA over MQTT**           |
| ---------------------- | ----------------- | ------------------------------------ | --------------------------------------- | ------------------------------ |
| **Application Layer**  | Pub/Sub mechanism | OPC UA communication (60 data types) | Sparkplug communication (18 data types) | OPC UA pub/sub communication   |
| **Presentation Layer** | not defined       | UA-JSON<br>UA-XML<br>UA-Binary       | Protobuf                                | UA-JSON<br>UA-XML<br>UA-Binary |
| **Session Layer**      | no session        | Client-server session management     | Sparkplug session awareness             | no session                     |
| **Transport Layer**    | TCP/IP            | TCP/IP                               | MQTT                                    | MQTT                           |


**Transport Layer:** Both MQTT and OPC UA utilize TCP/IP as the underlying protocol for communication. For MQTT Sparkplug and OPC UA over MQTT, the transport protocol uses MQTT as transport protocol, because these two protocols take advantage of the MQTT pub/sub model.

**Session Layer:** OPC UA incorporates a session layer responsible for managing the connection between clients and servers. It handles tasks such as session establishment, authentication, and encryption. In contrast, MQTT does not possess a session layer management feature. However, MQTT Sparkplug addresses this limitation by introducing Sparkplug session awareness at the session layer.

**Presentation Layer:** OPC UA incorporates a well-defined information model that defines the structure and semantics of exchanged data between clients and servers, such as UA-JSON and UA-binary. On the other hand, MQTT lacks a formal information model but relies on topic-based messaging for data communication between clients and servers. However, MQTT Sparkplug addresses this gap by specifying Google Protobuf as the message format to enhance MQTT's capabilities.

**Application Layer:** MQTT and OPC UA diverge significantly in their application layer protocols. MQTT follows a publish/subscribe model that organizes messages using topics, while OPC UA adopts a client/server model and utilizes a hierarchical object model to organize data. The OPC UA pub/sub specification serves as a solution for the OPC UA client/server model.

## Comparing MQTT Sparkplug and OPC UA

Both MQTT Sparkplug and OPC UA are popular protocols for Industrial IoT, and they have different strengths and weaknesses that may make one more suitable than the other depending on the specific use case. Here are some key differences between the two protocols and their variants:

| **Criteria**            | **MQTT**                                                     | **MQTT Sparkplug**                                           | **OPC UA**                                                   | **OPC UA over MQTT**                                         |
| ----------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Messaging Model**     | pub/sub                                                      | pub/sub                                                      | client-server                                                | pub/sub                                                      |
| **Bandwidth Usage**     | minimal overhead<br>low bandwidth and low power              | minimal overhead<br>low bandwidth and low power              | large code<br>footprint<br>high bandwidth                    | large code<br>footprint<br>high bandwidth                    |
| **Message Payload**     | not defined                                                  | lightweight messaging that is typically smaller than OPC UA  | more complex data types, and its messages can be much larger than MQTT Sparkplug. | more complex data types, and its messages can be much larger than MQTT Sparkplug. |
| **Interoperability**    | no interoperable                                             | interoperable (18 data types)                                | highly interoperable (60 data types)                         | highly interoperable (60 data types)                         |
| **Scalability**         | High scalability                                             | high scalability with the ability to handle millions of messages per second. | scalable but requires more complex architecture to handle large amounts of data | better scalability than OPC UA client/server model           |
| **Ease of Integration** | simple to use and requires minimal configuration             | simple to use and requires minimal configuration             | requires more setup and configuration                        | requires more setup and configuration                        |
| **Quality of Services** | QoS 0 (at most once), QoS 1 (at least once), and QoS 2 (exactly once) | QoS 0 (at most once), QoS 1 (at least once), and QoS 2 (exactly once) | provides a reliable transport layer that ensures messages are delivered in order and without loss | provides a reliable transport layer that ensures messages are delivered in order and without loss |
| **State Awareness**     | No                                                           | Yes                                                          | Yes                                                          | Yes                                                          |
| **Auto Discovery**      | No                                                           | No                                                           | Yes                                                          | Yes                                                          |
| **Application**         | IoT, home automation and M2M applications                    | IIoT and M2M applications                                    | industrial automation                                        | industrial automation                                        |
| **Real Time**           | Yes                                                          | Yes                                                          | Yes                                                          | Yes                                                          |
| **Security**            | security features are considered less secure than OPC-UA     | security features are considered less secure than OPC-UA     | digital certificates, digital signatures, data encryption, and secure authentication | digital certificates, digital signatures, data encryption, and secure authentication |
| **Information Model**   | does not have built-in support for information modeling      | support sophisticated information modeling but not as many as OPC UA. | support sophisticated information modeling systems that allow for the creation of complex data structures and models | support sophisticated information modeling systems that allow for the creation of complex data structures and models |

In short, OPC UA is an open standard that incorporates a well-defined set of data type specifications. On the other hand, MQTT Sparkplug is also an open standard but has fewer efforts in standardizing data types compared to OPC UA. Consequently, MQTT Sparkplug has less protocol overhead during data transmission.

## Conclusion

MQTT Sparkplug utilizes a lightweight messaging protocol, making it well-suited for low-bandwidth or unreliable networks. On the other hand, OPC UA employs a more robust messaging protocol capable of handling larger data volumes, which is better suited for high-speed and secure networks. 

The competition between OPC UA and MQTT continues to this day. EMQ is introducing the [MQTT over QUIC](https://www.emqx.com/en/blog/mqtt-over-quic) protocol for the automobile industry, while the OPC Foundation has released OPC UA over TSN (Time-Sensitive Networking). OPC UA over TSN provides a standardized method for transmitting real-time data over Ethernet networks, aiming to streamline complex industrial automation and control systems.



<section class="promotion">
    <div>
        Try Neuron for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect disparate industrial devices to the cloud.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
