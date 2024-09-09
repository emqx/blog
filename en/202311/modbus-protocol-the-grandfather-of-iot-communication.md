## What Is the Modbus Protocol?

The Modbus protocol is a communication protocol that allows devices to communicate over various types of media, such as serial lines and Ethernet. It was developed in 1979 by Modicon, a company that produced Programmable Logic Controllers (PLCs), to enable these devices to communicate with each other.

Modbus provides a messaging structure designed to establish master-slave communication between intelligent devices. A Modbus message sent from a Device A (master) will initiate a response from Device B (slave). The function of the Modbus protocol is to define the content of the communication, how the information is packaged, and the order in which messages are sent and received.

The Modbus protocol is simple and robust, making it a popular choice for industrial control systems. It's an open standard, meaning it's free for anyone to use and modify, leading to its widespread adoption throughout the industry.

This is part of a series of articles about the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) and related protocols.

## History and Origin of Modbus Protocol

The Modbus protocol was developed in 1979 by Modicon, a company now owned by Schneider Electric. Modicon created the protocol to be used with its PLCs (Programmable Logic Controllers), which are used in the manufacturing industry for automation of industrial electromechanical processes.

The Modbus Organization, a group of independent users and suppliers who advocate for the use of the Modbus protocol, was established in 2002 to provide public access to the protocol, its specifications, and its related information. The organization also ensures the Modbus protocol's continued availability, enhancement, and application in industrial automation markets.

Since its inception, the Modbus protocol has been implemented in a wide range of devices across many different industries. It has remained popular due to its simplicity, openness, and ease of implementation.

## Components of Modbus Protocol

### Modbus Devices/Machines

Modbus devices or machines are the actual physical devices that communicate using the Modbus protocol. These devices can be anything from temperature sensors to motor controllers, and they can be located anywhere from a factory floor to a remote oil field.

### Modbus Master

The Modbus master is the device that initiates a Modbus transaction. It sends a request to a Modbus slave device and waits for a response. The master can communicate with multiple slaves, and it can request different types of data from each one.

### Modbus Slave

A Modbus slave is a device that waits for a request from a Modbus master. When it receives a request, it will process it and send a response back to the master. The slave does not initiate communication; it only responds to requests from the master.

### Data Model and Registers

The Modbus data model is based on a series of registers. These registers are simply memory locations in the device that can hold data—they represent storage area within a device. There are two types of registers:

- **Holding registers:** Can be read and written to by a Modbus master.
- **Input registers:** Can only be read by a master.

### Types of Inputs

There are two main types of inputs in a Modbus system:

- **Coils** are a type of data in the Modbus protocol that represents binary states, such as ON/OFF or TRUE/FALSE. They can be read and written to by a Modbus master.
- **Discrete inputs** are similar to coils in that they represent binary states. However, unlike coils, they can only be read, not written to.

### Modbus Message Frame

A Modbus frame is the structure of a Modbus message. It consists of a start frame, function code, data, and an end frame. The following table shows the structure of the frame in more detail, in the ASCII variant of the protocol (learn more below):

| Start | Address | Function | Data    | LRC     | End   |
| :---- | :------ | :------- | :------ | :------ | :---- |
| :     | 2 Chars | 2 Chars  | N Chars | 2 Chars | CR LF |

### Modbus Communication Modes

There are three main communication modes in the Modbus protocol:

- RTU (Remote Terminal Unit)
- ASCII (American Standard Code for Information Interchange)
- TCP/IP (Transmission Control Protocol/Internet Protocol)

## Varieties of Modbus Protocol

There are several variations of the Modbus protocol. The main ones include:

### Modbus RTU

Modbus RTU (Remote Terminal Unit) is a binary implementation of the Modbus protocol. It is typically used over serial communication and is known for its compact data representation, which makes it efficient and fast. This efficiency makes its implementation in hardware devices quite straightforward. Communication under this protocol utilizes physical interfaces like RS-485 or RS-232.

Modbus RTU over TCP is a hybrid of the Modbus RTU and Modbus TCP protocols. Despite Ethernet being the physical medium, data transmission follows the RTU format in this mode. The significant advantage of this pairing is its ability to accommodate pre-existing RTU-based systems onto the Ethernet, with minimal hardware updates. Consequently, designers usually resort to this during the expansion of control ranges, trying to utilize as many in-place devices and structures as possible.

### Modbus ASCII

Modbus ASCII (American Standard Code for Information Interchange) is an ASCII implementation of the Modbus protocol. It is less efficient than Modbus RTU, but it is easier to use and debug because it uses human-readable characters.

### Modbus TCP/IP

Modbus TCP/IP is a version of the Modbus protocol that is used over TCP/IP networks. It allows for communication over long distances and across different networks.

### Modbus UDP

Modbus UDP (User Datagram Protocol) is a version of the Modbus protocol that uses the UDP transport protocol. It is less reliable than Modbus TCP/IP because it does not guarantee delivery or correct sequence of packets, but it is faster and requires less bandwidth.

### Modbus Plus

Modbus Plus (MB+ or Modbus+) is a proprietary variant of the Modbus protocol, which was introduced by Schneider Electric. It is a peer-to-peer communication protocol that offers higher speed and more deterministic data transfer compared to the standard Modbus.

## Differences Between Modbus TCP, RTU, and ASCII

### Modbus TCP vs RTU

The main differentiation between Modbus TCP and Modbus RTU resides in their communication media and application scenarios. Modbus TCP is primarily suitable for network communication, particularly long-distance communication, whereas Modbus RTU is great for serial communication, especially for short-distance communication between devices.

Modbus TCP is the Modbus protocol based on TCP/IP, mostly employed in LAN or internet communication. In Modbus TCP, each message includes a header carrying meta-information about the message, like length and transaction identifiers. Unlike Modbus RTU, Modbus TCP lacks CRC integrity check. Its headers mainly serve as markers for complete Modbus messages and their positions in transactions. Although, due to the absence of CRC error detection, Modbus TCP relies on the underlying TCP/IP network protocol for data integrity and correct data transmission.

Modbus RTU does not include distinct message headers, but it incorporates CRC error detection to its messages. This variant provides an efficient method to detect deviations in the transmitted messages – both content and transfer order changes. However, without specific message headers, any changes done to the transferred information will be impossible to pinpoint in the transaction details from the message alone.

### Modbus RTU vs ASCII

In comparison to Modbus RTU, Modbus ASCII has lower data transmission efficiency. However, its ASCII formatting offers the convenience of data debugging, making it particularly useful in settings requiring human-machine interactions.

## Uses of Modbus Protocol

### Industrial Automation

The Modbus protocol finds wide application in the field of industrial automation. In industrial settings, it is essential to maintain a reliable and efficient communication network between numerous devices and machines. Modbus enables easy and standardized communication between a variety of devices, such as Programmable Logic Controllers (PLCs), sensors, and actuators. It is often employed in manufacturing plants, power plants, oil refineries, and other industrial settings to monitor and control equipment and processes.

### Vehicle Systems

The Modbus protocol is also utilized within vehicle systems, specifically in the realm of electric vehicles. It aids in monitoring and controlling various parameters, including battery management systems, charging systems, and inverter systems. Modbus offers an efficient and easy-to-implement protocol for ensuring the smooth operation of these systems.

### Communications in IoT

With the rise of the Internet of Things (IoT), the Modbus protocol has gained significant relevance. Modbus, especially Modbus TCP/IP, is used to enable communication between IoT devices, sensors, and controllers over ethernet networks. Its simplicity and wide support make it a common choice for IoT communications.

### Sensor and Actuator Communication

The Modbus protocol plays a key role in facilitating communication between sensors and actuators. It provides a standard interface for transmitting data, such as sensor readings or control signals for actuators. This enables a centralized control system or PLC to monitor and control a wide variety of equipment in a coordinated manner. The use of Modbus protocol in sensor and actuator communication is prevalent in a range of fields, from industrial machinery to environmental monitoring systems.

## Limitations of the Modbus Protocol

While the Modbus protocol offers many benefits, it also has some limitations. One of these is its lack of built-in security features. Since the protocol was developed before the widespread use of the internet, it does not include mechanisms to secure communication, making it vulnerable to cyber attacks.

Another limitation is the protocol's simplicity. While this makes it easy to use and implement, it also means that it lacks some of the advanced features found in more modern protocols.

Despite these limitations, the Modbus protocol remains a popular choice for many applications due to its simplicity, robustness, and wide compatibility.

## Integrating the Modbus Protocol with the Industrial Internet of Things (IIoT): Neuron and EMQX

With the growth of the Industrial Internet of Things ([IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges)), there are many opportunities for the integration of Modbus protocol with modern IoT devices for automation, control, and data analytics. With IIoT, Modbus devices can now be part of a much larger, interconnected system, where data from these devices can be collected, analyzed, and utilized to optimize operations, improve safety, and reduce costs.

[Neuron](https://github.com/emqx/neuron) is an open source edge industrial protocol gateway, which provides support for various Modbus drivers, including Modbus TCP, Modbus RTU, Modbus UDP, and Modbus RTU over TCP. These Modbus drivers enable seamless integration of Modbus-enabled devices with Industrial Internet of Things applications. They allow Neuron to communicate with a wide range of industrial devices using different Modbus variants and protocols, enabling data acquisition, control, and interoperability with other components of the solution.

Here's a description of each Modbus driver:

- **Modbus TCP:** Modbus TCP is a widely used communication protocol that allows for the transmission of Modbus messages over TCP/IP networks. It enables communication between Modbus master devices (Neuron) and Modbus slave devices (such as sensors, actuators, or other industrial devices). Neuron's Modbus TCP driver enables seamless integration and communication between these devices, facilitating data exchange and control.
- **Modbus RTU:** Modbus RTU is a popular serial communication protocol used for communication between Modbus master and slave devices over serial interfaces, such as RS-485 or RS-232. It utilizes a binary representation of data and supports half-duplex communication, where data is transmitted in either direction but not simultaneously. Neuron's Modbus RTU driver enables connectivity with Modbus devices that utilize this serial communication protocol, allowing for data exchange and control in industrial environments.
- **Modbus UDP:** Modbus UDP (User Datagram Protocol) is a variant of the Modbus protocol that uses UDP for communication. UDP is a connectionless protocol that offers low overhead and fast transmission. Modbus UDP is often used in scenarios where speed is critical, such as real-time control applications. Neuron's Modbus UDP driver enables communication with Modbus devices that utilize UDP as the underlying transport protocol.
- **Modbus RTU over TCP:** Modbus RTU over TCP is a mechanism that allows Modbus RTU frames to be encapsulated within TCP/IP packets for communication. It combines the simplicity and efficiency of Modbus RTU with the broader network capabilities of TCP/IP. Neuron's Modbus RTU over TCP driver enables communication with Modbus devices that use the Modbus RTU protocol but are connected to the network via TCP/IP.

[EMQX](https://www.emqx.com/en/products/emqx) is the industry’s leading [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), providing efficient messaging for IIoT communication. Neuron and EMQX together form a powerful combination for supporting IIoT infrastructure, where Neuron acts as an edge industrial protocol gateway, facilitating connectivity with OT devices and enabling secure data exchange, while EMQX provides fast and reliable messaging. Together, they ensure seamless integration, reliable data communication, and enable advanced analytics and control in IIoT environments.

Learn more about EMQX and Neuron for Modbus environments: [Bridging Modbus Data to MQTT for IIoT: A Step-by-Step Tutorial](https://www.emqx.com/en/blog/bridging-modbus-data-to-mqtt-for-iiot).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
