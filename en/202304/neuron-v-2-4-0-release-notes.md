[Neuron](https://neugates.io/), the modern [industrial IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) connectivity server, has just released its latest version, Neuron 2.4.0. This release introduces several new features, including newly-added drivers, a new application, and improvements to existing functionality.

## 5 Additional Drivers for Different Scenarios

### [IEC61850 MMS](https://neugates.io/docs/en/latest/configuration/south-devices/iec61850/overview.html) and Allen-Bradley DF1

One of the most significant additions to Neuron 2.4.0 is the support for IEC61850 MMS. This widely used protocol for communication in electrical substations has been integrated into the Neuron, allowing for more streamlined communication with industrial devices that use this protocol. Additionally, the Allen-Bradley DF1 driver has been added, providing users with another option for connecting to Allen-Bradley PLCs.

### [HJ212-2007](https://neugates.io/docs/en/latest/configuration/south-devices/hj212-2017/hj212-2017.html) and [ABB COMLI](https://neugates.io/docs/en/latest/configuration/south-devices/comli/comli.html)

Other newly added drivers include HJ212-2007 and ABB COMLI. HJ212-2007 is a Chinese national standard for ambient air quality monitoring. ABB COMLI is a protocol used for communication between devices in industrial automation systems such as robotics, power, and automation. These drivers expand Neuron's capabilities even further, allowing it to communicate with even more diverse industrial devices through their own dedicated protocols.

### [WebSocket Application](https://neugates.io/docs/en/latest/configuration/north-apps/websocket/websocket.html)

Neuron 2.4.0 also introduces a new WebSocket application driver for real-time communication between devices and Neuron, providing faster response times in critical infrastructure monitoring and control. 

## Updates for Existing Plugins

Updates have also been made to several existing features in Neuron. 

- **Leveraging more power of existing protocol drivers.** IEC60850-5-104 now supports telemetry and clock synchronization, giving users greater device synchronization control. And MQTT offers configurable QoS and custom topic subscriptions for group subscriptions, further increasing protocol flexibility.
- **Introducing real-time configuration change event reporting in** **monitoring plug-in.** This new feature allows users to monitor changes to their configuration in real-time, providing greater visibility into their industrial devices and ensuring they can respond quickly and effectively.
- **Connecting to eKuiper on different machines.** Users can now deploy Neuron and the streaming engine, eKuiper, on separate devices, allowing for a more customizable and efficient industrial IoT environment setup.  
- **Enhancing data flexibility with new read-write storage points.** The new storage points are readable and writable, providing even greater flexibility in how users can manipulate their data, making it easier to manage and customize their industrial IoT environment to meet their specific needs. 

## API and UI Improvements

Neuron 2.4.0 also comes with new APIs that enhance the management of industrial IoT environments. These APIs include the capability to get and replace global configuration, a file download API, and an updated monitoring API that now provides system CPU, memory, and disk statistics. The new APIs provide users with more powerful tools to ensure optimal performance and timely detection of issues.

The user interface has also been updated, with the node and tag list now supporting list mode and fuzzy search. Additionally, the interface now provides improved support for both English and Chinese languages, making it more accessible to users around the world.

![Neuron Tag List](https://assets.emqx.com/images/ac42874fb381a9d8f456c841973f738e.png)

<center>Tag List</center>

## Conclusion

Neuron 2.4.0 release represents a major step forward for industrial IoT connectivity. With its new features and updates, Neuron continues to provide users with a powerful and flexible tool for managing their industrial IoT environment while ensuring they can stay on top of any issues. Whether managing a small industrial network or a large-scale operation, Neuron 2.4.0 is a must-have tool to take your [industrial IoT platform](https://www.emqx.com/en/blog/iiot-platform-key-components-and-5-notable-solutions) to the next level.


<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
