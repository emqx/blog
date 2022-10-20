In September, we released [Neuron](https://neugates.io/) 2.2. A series of new drivers and features have been added for this version: Beckhoff ADS, OPC DA, and NONA11 drivers have been added to unify the ports exposed by HTTP services. In addition, we focused on data statistics and the establishment of event alert system in the month. We plan to make the key data and events in the system visualized through Prometheus in Neuron 2.3, so as to improve the monitoring and management of Neuron and its connected devices during its use.

## Data upgrade

The latest version adds a script to upgrade data from Neuron 1.x to 2.x. At the same time, after Neuron 2.2, data upgrade is integrated into the installation package. When installing the new version, the data of the old version can be automatically upgraded to the new version for support. It is unnecessary to configure the device and device point data again after the installation of the new version.

After the introduction of SQLite to store the Neuron configuration information in Neuron 2.2, Neuron uses SQL schema to perform version management on the data storage organization format, which facilitates data upgrade during version upgrade.

## Key data statistics and event notification

Neuron will provide HTTP and MQTT based data statistics plug-ins in v2.3 to present some key data and events of Neuron.

The statistics mainly include the north-south node data statistics, including the number of nodes, the number of nodes in operation, the number of nodes disconnected from the device, the number of points configured in the southbound node, the number of bytes and instructions sent and received by the node, and more detailed status information of the node, such as the delay between the node and the device.

Event notification is mainly internal to Neuron. Some key changes are notified externally as events. For example, add, delete or modify the relevant configuration of the equipment and the point information, establish and disconnect the connection between Neuron and the equipment, etc.

The HTTP Server based interface will collect statistical information and events in the data format conforming to the Prometheus specification, facilitating access to the Prometheus monitoring system to monitor and manage Neuron and its equipment.

## Upcoming Drivers

### QnA 1E driver

This driver is similar to the existing driver QnA 3E. It is mainly connected to some older models of Mitsubishi PLC and supports serial communication. The supported data types are the same as QnA 3E, including common data types.

### CNC FANUC driver

This driver is mainly used in CNC (Computer Numerical Control) and interacts with FANUC's CNC to obtain some basic information, such as spindle speed, distance, absolute and relative position information, etc.

## Problem fixing

- Fix the precision problems of float data and double data
- Fix the problem of “importing a large number of points takes a long time”.

## Other Updates

- UI modifications are imported or exported to the group list page. Now you can import or export point data of multiple groups at once.
- Prompt of UI improvement error.




<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
