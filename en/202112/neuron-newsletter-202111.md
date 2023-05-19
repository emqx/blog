In November, the Neuron team still focused on the development of v2.0, improved some features and unit tests, added overall functional tests, and fixed the bugs found in the tests. At the same time, the v2.0-alpha version is under active preparations for the release.

## Functionality improvements in Neuron v2.0

- Improve some HTTP request interface of the Webserver, including user login and logout, node setting, start and stop, datatag addition, deletion, subscription and read/write, configuration update of group config, etc.
- Improve some interface of [MQTT](https://www.emqx.com/en/mqtt-guide), including support for some functional interface of the Webserver, support for node control, datatag addition, deletion, modification, and search, support for the attribute of datatag, support for configuration update of group config, and plug-in acquisition and update.
- Improve the function and stability of Modbus driver. The function of data periodically reading/writing is optimized, and the subscription relationship changes after the group config is updated.

## Test of Neuron v2.0

- Improve the unit test of common data types, fix the problem of memory leak, and increase the stability.
- Use the robot automatic test framework to conduct a complete functional test of Neuron. At present, functional tests related to nodes, grouping data and plug-ins have been completed.

## Neuron v2.0 Bugfix

Neuron v2.0 fixes the following issues:

- The system crashes in node control, and the obtained node information is not complete.
- Group config subscription sometimes fails.
- The core layer sometimes forwards messages to mismatched nodes.
- Some data types will be wrong during the serialization of data transmission.
- Memory leak when transferring data.

## Current status of Neuron 1.x

Before Neuron v2.0 is officially commercialized, the functionality upgrade and maintenance of Neuron v1.x are particularly important. We recently released v1.3.4, including the following features:

- The timestamp in the MQTT json package is extended from 10 digits to 13 digits.

- OPC driver fixes the problem of 「0x00AA0000-non-critical timeout」that appeared when the certificate is connected to Siemens PLC S71200.

- Modify SEMI in the status bar of the UI interface and change it to EXPIRED.

- Fins on TCP driver data type problem is fixed.

- Limit the excessive growth of the data Log file to avoid affecting the system operation.


Neuron v1.x has been widely used or is being tested in different industries, including shipping, oil field, semiconductor and so on. The Neuron team is also improving Neuron v1.x based on user feedback and needs. v1.4.0 will be released soon, please stay tuned.

 
<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a >
</section>
