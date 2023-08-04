OPC-UA, HTTP, [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication), [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), and Sparkplug are common and popular technologies used in industrial communication, each designed for specific levels and purposes of communication. 

OPC-UA is often used in floor plant environments, HTTP is commonly used for internet communication, MQTT is suitable for on-premises or cloud platform communication, and Modbus is prevalent in device-level communication.

While these technologies have different design purposes, it is possible to compare them in terms of communication efficiency. In this blog, we will make a comparison between these protocols regarding four communication criteria that affect transmission bandwidth:

- Connection Overhead
- Connection Persistence
- Data on Change
- Data Compression

> The figures and findings in this blog are based on [Johnathan Hottell experiment](https://cirrus-link.com/efficient-iiot-communications-a-comparison-of-mqtt-opc-ua-http-and-modbus/) in 2019.

## Connection Overhead

When two devices communicate over a network, they typically establish a connection to exchange data. This process involves several steps that contribute to connection overhead, including:

- Handshaking: Before data transfer can begin, the devices need to establish a connection by exchanging a series of messages, known as a handshake. The handshake verifies the identity of the devices, negotiates communication parameters, and ensures that both parties are ready to transmit and receive data. This initial negotiation and verification process incur time and network resources overhead.
- Protocol Overhead: Network protocols, such as TCP/IP, introduce additional overhead to ensure reliable and orderly data transmission. These protocols add control information, error-checking mechanisms, sequencing, and acknowledgment mechanisms to ensure data integrity and delivery. While these features enhance the reliability of network communication, they also introduce overhead in terms of processing and network resources.

**OPC-UA:** OPC-UA introduces additional overhead due to its complex architecture and extensive set of functionalities. Establishing an OPC-UA connection involves multiple steps, including handshakes, security negotiations, and session establishment, which result in higher connection overhead.

**Modbus:** Modbus has low connection overhead since the protocol does not require extensive handshaking or complex session management. Modbus primarily focuses on direct access to data points, and the connection establishment involves minimal overhead, typically limited to establishing a network connection and addressing the slave device.

**HTTP:** HTTP introduces higher connection overhead compared to the other mentioned protocols. Each HTTP request-response cycle typically involves establishing a new connection, which incurs additional overhead in terms of handshakes, header exchanges, and session management.

**MQTT:** MQTT is designed to be lightweight and efficient, resulting in low connection overhead. It uses a simple binary protocol with minimal header size, reducing the amount of data needed for establishing and maintaining a connection.

**Sparkplug:** The additional overhead introduced by Sparkplug is minimal compared to MQTT, as it primarily focuses on defining a payload format and data representation rather than altering the connection behavior.

![Connection Overhead](https://assets.emqx.com/images/61836cfb2e768c29126b7b569a7010b4.png)

In short, OPC-UA, being a more robust and feature-rich protocol, may have higher connection overhead than other technologies. MQTT, as a simpler and lightweight protocol, generally has lower connection overhead. HTTP and Modbus have request and response model, and they also have fair connection overhead. Sparkplug has a bit more data on connection because of the “Birth” message. The experiment results shown in the figure are quite consistent with our knowledge.

## Connection Persistence

Once a connection is established, some level of overhead is incurred to maintain it. This includes periodically exchanging keep-alive messages to ensure the connection remains active and managing connection state information at both ends. Additionally, connection-oriented protocols may need to reestablish the connection if interrupted or lost, further contributing to overhead. Therefore, keeping connections open for multiple requests can impact efficiency by reducing the overhead associated with establishing new connections.

**OPC-UA:** OPC-UA is a client-server model. The connection between the client and the server can be either persistent or non-persistent, depending on the requirements and characteristics of the application or protocol being used. But we assume the persistent connection is used in this case.

**Modbus:** Modbus is also a client-server model. Modbus does not inherently require a persistent connection between the client and server. Instead, a connection is established for each request, and once the response is received, the connection is closed.

**HTTP:** HTTP is a stateless protocol primarily used for web communication. Each HTTP request-response cycle is independent, and connections are not kept alive between requests by default.

**MQTT:** MQTT employs a persistent connection model. Once a client establishes a connection with an MQTT broker, the connection remains open until explicitly closed by either the client or the broker. It also provides features like keep-alive mechanism and automatic reconnection to ensure connection reliability in case of network disruptions.

**Sparkplug:** Sparkplug, built on MQTT, inherits the connection maintenance characteristics of MQTT. It utilizes the persistent connection model, enabling long-lived connections between clients and the MQTT broker. We assume that Sparkplug has similar results as MQTT.

![Connection Persistence](https://assets.emqx.com/images/b88e36335eacb30f81e7e6f167be2389.png)

OPC-UA and MQTT are designed to support connection persistence, allowing multiple requests to be handled over a single connection, thus reducing the overhead of connection establishment. HTTP and Modbus, in their standard configurations, typically use short-lived connections, which may result in higher connection overhead for each request.

## Data on Change

"Report on change" is a mechanism commonly used in industrial automation and communication protocols to transmit data only when there is a change or update in the values of monitored variables or parameters. Instead of continuously transmitting data at fixed intervals, the report-on-change approach optimizes network bandwidth by sending data updates only when necessary.

In systems where large amounts of data are monitored or controlled, transmitting all the data at regular intervals can lead to inefficient use of network resources. Report on change minimizes unnecessary network traffic and reduces data transmission overhead by selectively sending data updates when there is a significant change in the values of monitored variables.

**OPC-UA:** OPC-UA supports the "report on change" mechanism through its subscription model. OPC-UA clients can establish subscriptions to monitor specific variables or nodes in the server. The server then sends data updates to the client only when there is a change in the subscribed data.

**Modbus:** As a simple and traditional protocol, Modbus does not have inherent support for the "report on change" mechanism. It primarily focuses on providing direct access to data points without built-in mechanisms for reporting changes.

**HTTP:** HTTP has not the "report on change" functionality, but it can be implemented at the application layer using long-polling or server-sent events (SSE) techniques. These techniques enable the server to push data updates to clients when changes occur.

**MQTT:** MQTT does not inherently support the "report on change" mechanism as part of its standard specification. However, MQTT can be combined with other protocols or application logic to implement a report-on-change functionality.

**Sparkplug:** Sparkplug provides native support for the "report on change" mechanism. It defines a standard payload format that includes metadata and data values. The subscribing clients receive updates only when there is a change in the data value.

![Data on Change](https://assets.emqx.com/images/0f8dc966b9714bcb2616caf3218f912b.png)

OPC-UA pub/sub model and MQTT support a data-on-change mechanism, where data is sent only when it has changed, reducing unnecessary network traffic and improving efficiency. OPC read/write model, HTTP and Modbus, on the other hand, often rely on periodic or polling-based data retrieval, which may result in higher network traffic and less efficient bandwidth utilization. The Johnathan experiment reflect the fact that the “report on change” mechanism can significantly reduce the network traffic.

## Data Compression

Data compression in communication refers to the process of reducing the size of data for efficient transmission over communication networks or channels. It involves applying compression techniques to the data before sending it and then decompressing it at the receiving end to restore the original data. It's important to note that both the sender and the receiver in a communication system must support the same compression algorithm to ensure successful compression and decompression.

**OPC-UA:** OPC-UA uses UA-XML, UA-JSON, or UA-binary to transport the data. These data formats do not support data compression. OPC-UA uses base64 to encode data, in which does not have compression capability. OPC-UA binary was shown transport compression could not yield bandwidth improvements unless data is compressed as a service.

**Modbus:** Modbus does not include native data compression capabilities. It primarily focuses on transmitting data in a straightforward and efficient manner without additional overhead.

**HTTP:** HTTP itself does not provide native data compression; it supports features like content encoding, where data compression can be applied to the payload being transmitted.

**MQTT:** MQTT itself does not have built-in data compression as part of its core specification. However, MQTT can be used in conjunction with other compression techniques or libraries to compress the payload data before transmission.

**Sparkplug:** Sparkplug is a messaging protocol specifically designed for industrial IoT applications, built on top of MQTT. Sparkplug has defined the Google Protobuf payload data format for the standard. Protobuf is somehow a compressed data format. Sparkplug can be considered the protocol with data compression.

![Data Compression](https://assets.emqx.com/images/c56858826e93a396cd76204f2c5fea42.png)

OPC-UA provides built-in support for data compression, but the data compression rate is not high and not helpful for the efficient transfer of compressed data. HTTP and MQTT may support data compression, but it is not a standard feature and would require additional configuration or implementation at application level. Modbus doesn’t support any data compression. Sparkplug has defined its payload as Google Protobuf, which is somehow compressed data in transmission.

## Head-to-Head Comparison Chart

| **Protocol**  | Connection Overhead | Connection Persistence | Data on Change | Data Compression |
| :------------ | :------------------ | :--------------------- | :------------- | :--------------- |
| **OPC-UA**    | Poor                | Poor                   | Not Support    | Moderate         |
| **Modbus**    | Excellent           | Moderate               | Not Support    | Poor             |
| **HTTP**      | Excellent           | Poor                   | User Defined   | User Defined     |
| **MQTT**      | Excellent           | Good                   | User Defined   | User Defined     |
| **Sparkplug** | Good                | Good                   | Support        | Excellent        |

## Conclusion

From the comparison above, we can conclude that the Sparkplug protocol is the most efficient protocol for industrial usage. It provides native support for the "report on change" mechanism, making them well-suited for efficient transmission of data updates. It also has low connection overhead due to its lightweight protocols and persistent connection models, ensuring continuous communication and efficient message delivery. 

Both [EMQX](https://www.emqx.com/en/products/emqx) and [Neuron](https://neugates.io/) support the Sparkplug protocol. EMQX provides advanced features such as load balancing, clustering, and message persistence, ensuring the efficient and reliable transmission of data using the Sparkplug protocol, whereas  Neuron provides features like data aggregation and device management, allowing for handling large-scale deployments of IIoT devices.



<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
