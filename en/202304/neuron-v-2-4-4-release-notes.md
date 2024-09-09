In April 2023, [Neuron](https://github.com/emqx/neuron) open-sourced the [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication) RTU/TCP to replace the previous Modbus TCP driver. The new Modbus RTU/TCP driver has better compatibility and supports both Client/Server modes, enabling it to adapt to more industrial devices. In addition, to facilitate user trial and evaluation, the latest version allows trial usage of the plugin without the need to import a license. 

## Modbus RTU/TCP Open Sourced

Neuron has completely open-sourced the [Modbus RTU](https://docs.emqx.com/en/neuron/latest/configuration/south-devices/modbus-rtu/modbus-rtu.html) and [Modbus TCP](https://docs.emqx.com/en/neuron/latest/configuration/south-devices/modbus-tcp/modbus-tcp.html) plugins. These plugins support additional data types such as Double and INT64. They introduce the Server mode, which is particularly useful for accessing DTU devices through 4G network, eliminating the requirement for port forwarding. 

In addition, these plugins allow for configuration adjustments of command-sending policies, ensuring better compatibility for scenarios that involve multiple devices on a single serial port.

You can find the source code in our GitHub repository: [https://github.com/emqx/neuron/tree/main/plugins/modbus](https://github.com/emqx/neuron/tree/main/plugins/modbus)  

## Embedded Free Trial License

In the latest version, Neuron provided a 30-tag trial license that allows users to try all drivers for free. By downloading the installation package or Docker image from the official website once, users can experience all drivers within 30 tags for an unlimited time.

## BACnet/IP Driver Enhancement

[BACnet](https://www.emqx.com/en/blog/bacnet-protocol-basic-concepts-structure-obejct-model-explained) is a communication protocol widely used in the field of building automation and control:

- In HVAC (Heating, Ventilation, Air-conditioning and Cooling) system: Detect and control devices such as air handlers, fans, chillers, humidifiers, and exhaust fans. 
- In lighting systems: Control the lighting system in the building, such as light switches, dimmers, and timers. 
- In security systems: Detect and control surveillance cameras, access control systems, fire alarm systems, etc. 
- In building energy management systems: Detect and control in real-time, optimizing energy efficiency, including electricity, gas, water, etc., 

The latest version of Neuron comes with improved BACnet/IP support. It facilitates the integration of a broader range of device types and expands the amount of information that can be read from device data tags.

## Bug Fixes

- Fix known UI issues in version 2.4.x.
- Fix the issue where SparkPlugB crashes when not configured.
- Fix read errors in the file plugin.
- SparkPlugB plugin adapted for Ignition.
- Fix the issue of abnormal WebSocket connection.
- Add statistics for cache memory information in API: /api/v2/metrics.
- Modify operating system information in API:  /api/v2/metrics.
- Optimize configuration for MQTT plugin offline caching.

 

<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
