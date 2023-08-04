In February, the Neuron team devoted its efforts to developing new drivers. We added southbound drivers, including IEC61850 driver, Allen-Bradley DF1, and Profinet driver. We also provided support for static nodes. These new drivers and features will be released in Neuron 2.4.

## IEC61850 Driver

The IEC61850 standard is widely used in the field of power system automation. Neuron has developed an IEC61850 driver that enables users to easily connect to and interact with devices that utilize the MMS protocol. In addition, the Neuron driver has mapped multiple data types in MMS to the corresponding Neuron types, making it easier to perform data acquisition and modification. With the IEC61850 driver, users can now specify the address and type of the object attribute (DA) in the intelligent electronic device (IED), enabling them to gather and modify the data efficiently.

## Allen-Bradley DF1 Driver

The DF1 protocol is a widely used data link layer communication protocol, particularly within AB's programmable controller. It is supported by all series of programmable controllers, as well as computers equipped with RSLinx communication software. DF1's physical layer is built on established electrical standards like RS232 and RS485, while its application layer includes different commands for different types of devices. The combination of these layers enables efficient and reliable communication based on the DF1 protocol.

Neuron has made significant progress in implementing the application layer commands for the half-duplex communication, using CRC checksum. When establishing a connection between Neuron and a device, the serial port is used, and communication is established with the designated PLC module via the site number.

## Profinet Driver

Profinet is an Ethernet-based fieldbus that allows for efficient communication between devices. Neuron will serve as a Controller in Profinet, enabling the exchange of data with Profinet IO devices at a high frequency and with millisecond accuracy, depending on the hardware configuration of the device. Profinet cyclic data runs mainly on Ethernet layer 2, it's important to note that if there is no IP network layer, data forwarding between routes will not be possible. Therefore, it's essential to ensure that both Neuron and Profinet IO devices are located within the same LAN.

## Support Static Node

Static nodes feature allows for the configuration and upload of static data. Static nodes are not sent down to the plugin level and are managed entirely by the Neuron core. They can be added to any Group in the Neuron platform and read and written to by the user. The value of a static node can be modified at any time, and the updated value is automatically sent to clients who northbound subscribe to the Group.

## Upgrade Data Processing User Interface

The currently released NeuronEX features a data stream processing UI that is compatible with eKuiper 1.6. In order to keep up with newer versions of eKuiper, we upgraded the data stream processing UI and added UI for the Source configuration and upload plugin.

## Bug Fixes

This month, we have addressed several issues, including:

- The [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication) RTU configuration page not switching correctly according to the schema.
- A connection exception being caused by an SSL certificate when multiple OPC UA nodes are configured.
- The multi-threaded data competition problem in the ADS plugin.
- Abnormal exits of the S7Comm plugin in some cases.
- An exception occurred when configuring VOLUME in Docker images.



<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
