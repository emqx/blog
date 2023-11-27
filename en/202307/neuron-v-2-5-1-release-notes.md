The [industrial IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) connectivity server, Neuron 2.5.1, has been officially released!

The latest version brings several new features, including device-based templates for southbound integration, UDP transport support for [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication), read retry support for Modbus, and high availability Master-Slave mode for IEC104. Furthermore, five new southbound drivers have been introduced: Profinet IO, Mitsubishi FX, Omron FINS UDP, Panasonic Mewtocol, and DLT645-1997.

In addition, we’ve made some adjustments to the product from this version:

- Provide an [international edition](https://www.emqx.com/en/try?product=neuron) for English-speaking users.
- NeuronEX, the edition integrated with eKuiper, has been discontinued.
- The Modbus TCP community plugin has been discontinued in the open-source version. Modbus TCP and Modbus RTU plugins are now open-sourced. Users can experience all protocol drivers within 30 tags or nodes without any time limit for free. Learn more here: [Experience Neuron Industrial IoT Gateway Software for Free with Time-Unlimited Trial License](https://www.emqx.com/en/blog/experience-neuron-industrial-iot-gateway-software-for-free-with-time-unlimited-trial-license) 

Download the latest version here: [https://www.emqx.com/en/try?product=neuron](https://www.emqx.com/en/try?product=neuron).

## New Features Overview

### Device-Based Templates

This feature is introduced for scenarios where a large number of devices with similar configurations need to be set up. It allows for the quick creation of multiple devices with the same set of points but different configurations. 

![Templates](https://assets.emqx.com/images/313c741b7e535e721cd1219e14f9d444.png)

<center>Templates</center>

<br>

![Create Device Nodes Based on Templates](https://assets.emqx.com/images/839758563bab6cb3de66b83ae3cdb299.png)

<center>Create Device Nodes Based on Templates</center>

<br>

> Templates also support import/export functionality. Please refer to the [template usage documentation](https://neugates.io/docs/en/latest/configuration/templates/templates.html) for more details.

### Modbus UDP Transport Support 

Modbus TCP plugin now supports UDP transport based on the Modbus TCP protocol. This enables communication using UDP protocol at the transport layer.

![Modbus TCP Configuration Interface](https://assets.emqx.com/images/aa097aa11868bbcf275ae331573d4f0b.png)

<center>Modbus TCP Configuration Interface</center>

### Modbus Read Retry

The Modbus plugin now supports read retries in case of device connection issues. Users can configure the number of retries and the interval between retry attempts on the plugin's configuration page.

### IEC104 High Availability Master-Slave Mode

IEC104 protocol now supports a high availability Master-Slave mode for improved reliability. This mechanism ensures uninterrupted operation by allowing a backup device to take over in case of failure or unavailability of the primary device. The high availability mode is crucial for applications requiring high availability and reliability in critical domains such as power systems.

![IEC60870-5-104 Configuration Interface](https://assets.emqx.com/images/0a15e1d0b53e54e4a4b88dec92c2bfc6.png)

<center>IEC60870-5-104 Configuration Interface</center>

## New Drivers at a Glance

### Profinet IO 

Profinet IO (Industrial Ethernet Input/Output) is a real-time Ethernet communication protocol used in the field of industrial automation. It is based on Ethernet technology and aims to provide high-performance, reliable data exchange and real-time control. Profinet IO is specifically designed for communication between input/output (I/O) devices and control systems. It allows for real-time transmission of digital and analog signals, as well as control and monitoring of device status.

![Profinet IO ](https://assets.emqx.com/images/f561fb20b9ce986c5a298884fe3bdbb1.png)



> [Profinet IO Driver User Manual](https://neugates.io/docs/en/latest/configuration/south-devices/profinet/profinet.html)

### Mitsubishi FX

Mitsubishi FX series PLC is an economical and practical product line offered by Mitsubishi Electric. It is widely recognized for its user-friendly interface, reliability, stability, and flexibility. The FX series PLC is suitable for applications of various scales and complexities, ranging from small-scale machinery to large production lines.

The Mitsubishi FX plugin in Neuron allows access to Mitsubishi's FX0, FX2, FX3, and other series PLCs through the FX programming port.

![Mitsubishi FX](https://assets.emqx.com/images/af0daafca5c6d872b1f6e873331bdc0b.png)

> [Mitsubishi FX Driver User Manual](https://neugates.io/docs/en/latest/configuration/south-devices/mitsubishi-fx/overview.html#parameter-configuration)

### Omron FINS UDP 

Omron FINS is a communication protocol used in the field of industrial automation. The FINS protocol enables data exchange and communication between Omron devices, including programmable logic controllers (PLCs), sensors, and servo drives.

In the FINS protocol, UDP (User Datagram Protocol) is a transport layer protocol used for transmitting FINS protocol packets over a network. UDP is a connectionless protocol that provides a simple, unreliable data transmission mechanism suitable for applications requiring efficiency and real-time performance.

The FINS UDP driver in Neuron 2.5.1 enables fast and real-time data exchange between Omron devices over Ethernet. UDP communication offers lower communication latency compared to other protocols like TCP, but it does not provide reliability and data integrity checks. Therefore, when using FINS UDP for communication, it is essential to ensure network stability and employ appropriate mechanisms to handle data loss and errors.

![Omron FINS UDP](https://assets.emqx.com/images/d9ffce2539d9929ad67128b4d474b7b8.png)

> [Omron FINS UDP Driver User Manual](https://neugates.io/docs/en/latest/configuration/south-devices/omron-fins/omron-fins-udp.html)

### Panasonic Mewtocol 

Panasonic Mewtocol is a communication protocol used in the field of industrial automation. It is a protocol for data exchange and communication between Panasonic devices, including programmable logic controllers (PLCs), human-machine interfaces (HMIs), servo systems, and other industrial equipment.

The Panasonic Mewtocol plugin in Neuron enables access to Panasonic's FP-XH and FP0H series PLCs over Ethernet.

![Panasonic Mewtocol ](https://assets.emqx.com/images/ae5b3e0fde0b98ec26bf59a4760beaa1.png)

> [Panasonic Mewtocol Driver User Manual](https://neugates.io/docs/en/latest/configuration/south-devices/panasonic-mewtocol/overview.html)

### DLT645-1997

DL/T645-1997 is a technical standard used in China for electronic energy meters. This standard defines the communication protocol and data format for information exchange between electronic energy meters and data acquisition systems.

DL/T645-1997 specifies the structure of data frames, the content of data fields, and the communication methods for transmitting energy consumption and other related information. It covers various aspects such as meter reading, load control, event recording, and parameter settings.

This standard provides a common framework for communication between energy meters and power supply companies or other entities involved in energy monitoring and management. It enables accurate and efficient data collection, billing, and analysis of energy usage.

The DL/T645-1997 plugin supports both serial port connection and transparent TCP connection.

![image.png](https://assets.emqx.com/images/d8b746a9604695910dbbba729bf4dbb8.png)

> [DLT645-1997 Driver User Manual](https://neugates.io/docs/en/latest/configuration/south-devices/dlt645-1997/dlt645-1997.html#module-description)

## Future Plans

### MQTT Functionality Upgrades 

This includes adding frequency control for reporting offline cached data and supporting custom Topic definition for MQTT offline cached data reporting.

### Driver Upgrades 

Ongoing improvements and upgrades are planned for drivers such as IEC60870-5-104 and BACnet/IP. Additionally, we are actively working on adding support for protocols like SECS/GEM.

### Enhanced Features 

We will continuously optimize log downloading and DEBUG log functionality to improve user experience and facilitate troubleshooting. We will also enhance the configuration documentation support feature.



<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
