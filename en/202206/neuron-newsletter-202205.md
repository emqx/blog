In May, we released Neuron 2.0.1, of which some problems discovered in v2.0.0 are fixed. We mainly focused on the development of new drivers, adding the southbound BACnet/IP and KNXnet/IP drivers and northbound Sparkplug application, and customizing the extended [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication) TCP protocol, which significantly improved the point acquisition efficiency.

## KNXnet/IP Divers

[KNX](https://www.emqx.com/en/blog/knx-protocol) is a unified and manufacturer-independent communication protocol, which is used to intelligently connect the most advanced home and building system technologies, including the management of heating, lighting and access control systems in family residences and office complexes that require high comfort and versatility. KNX may be used to plan and implement efficient and energy-saving solutions, and provide more functions and convenience while reducing energy costs.

Our KNX drivers support the BIT/BOOL/INT8/UINT8/INT16/UINT16/FLOAT data types, and serve as KNXnet/IP Client for data acquisition and device control. KNXnet/IP driver supports two point addresses, one is KNX group address, which the users can write only, and the other is KNX group address with a KNX individual address, which the users can read only.

## BACnet/IP Driver

[BACnet](https://www.emqx.com/en/blog/bacnet-protocol-basic-concepts-structure-obejct-model-explained) is a communication protocol for smart buildings, which is defined by the International Standardization Organization (ISO), American National Standards Institute (ANSI) and American Society of Heating, Refrigeration and Air Conditioning Engineers (ASHRAE). Communication designed by BACnet for the application of smart buildings and control systems may be used in HVAC system (including heating, ventilation and air conditioning), as well as lighting control, access control system, fire detection system and other related devices.

Our drivers support the BIT//FLOAT data types, and serve as BACnet/IP Client for data acquisition and equipment counter-control. Currently, OBJECT TYPE  supported by BACnet/IP  mainly include ANALOG INPUT, ANALOG OUTPUT, ANALOG VALUE, BINARY_INPUT, BINARY_OUTPUT, BINARY_VALUE, MULTI_STATE_INPUT, MULTI_STATE_OUTPUT and MULTI_STATE_VALUE. The protocol layer adopts the asynchronous sending and receiving instructions, which can support 255 concurrent instructions at the maximum, thus improving the acquisition and counter-control efficiency.

## Sparkplug

[MQTT Sparkplug](https://www.emqx.com/en/blog/mqtt-sparkplug-bridging-it-and-ot-in-industry-4-0) is an interoperability protocol for smart manufacturing and industrial automation. It provides a consistent way for equipment manufacturers and software providers to share data structures as to accelerate the digital transformation of the existing industries.

The northing configuration is similar to the MQTT plug-in, and the MQTT Topic composition matches the Group of Neuron. It supports reporting subscription data according to the Group of Neuron, and writing the acquisition device of Neuron at the Application end of Sparkplug. The data supports all defined types of Neuron southing devices.

## Customized Modbus TCP Driver

Custom Modbus driver needs equipment-side support. It uses the length of 2 bytes in Modbus TCP MBAP to replace the length of a single byte in ADU to represent the frame length, and Modbus TCP frames can support up to 65535 bytes at the maximum. The extended protocol can collect more than 30,000 data points in one acquisition instruction, which reduces the quantity of interactions between Neuron and equipment, and greatly improves the acquisition efficiency.

## Other Updates

- Neuron is integrated with the Dashboard of eKuiper.
- Plenty of official website files have been optimized and will continue to improve.
- As for some issues from GitHub, we optimized the compilation and cross-compilation of Neuron, which lowered the threshold for constructing an entry-level development environment.
- The realization of open source Modbus TCP has been reconstructed.
- The problems discovered during testing in v2.0.0 have been solved.


<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
