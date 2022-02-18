## Neuron 2.0 progress and planning

### Function operation is basically completed

At present, we have basically completed the function operation of version 2.0 and developed a supporting Web UI to configure Neuron, view the connection status of Neuron, read and write and monitor device data. Now it is possible to connect OPC UA and [Modbus](https://www.emqx.com/en/blog/building-modbus-based-iiot-app-with-neuron) devices simultaneously and read and write their data.

### Focus on data collection, aggregation, and forwarding

According to users' feedback on Neuron 1.x, we have made significant adjustments to the product planning of the new version of Neuron, streamlined some functions, and focused on data collection, aggregation, and forwarding of industrial protocols.

In addition, Neuron 2.0 will support the simultaneous connection of multiple devices of the same protocol and different protocols. It is no longer necessary to start multiple Neuron processes to connect multiple devices as Neuron 1.x.

Other major new features are as follows:

- Pluggable southbound device driver and northbound application
- Highly integrated with other EMQ products, including eKuiper, EMQX, Fabric, etc.
- Minimal memory usage
- Support runtime update of device drivers

## Neuron 1.x current state

Currently, the latest version of Neuron is v1.3.3, and we will release v1.3.4 next month. We mainly repair the maintenance function of data log size to prevent the log from becoming too large due to the increase of time and affecting the system operation.
