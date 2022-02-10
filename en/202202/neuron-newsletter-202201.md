In January, we are mainly focusing on Neuron2.0-alpha.2 which was released at the end of the month. In this version, the persistence function of Neuron is added, the import and export of web pages are supported, the process of stress test is added, the separate commercial modules are supported, and the problems found in alpha.1 are solved.

## Major update of Neuron 2.0-alpha.2

### Add persistence function

In the alpha.2 version, the persistence function is added to Neuron, which can save the information of node configuration, subscription relationship, data point configuration, registered plugin of the running state of Neuron to the file of the gateway device. When Neuron is restarted, the node configuration, subscription relationship and data point configuration in Neuron can be automatically restored based on the persistent information saved in the file.

### Support web import and export

Through the import and export functions of node configuration, subscription relationship, and data point configuration in the web, users can remotely add or update data point configuration and data point subscription relationships in batches.

### OPC UA Drives data subscription

This new function greatly reduces the data bandwidth consumption caused by the data change of OPC UA device.

### MQTT interface form modification

In the latest version, the original method of calling specific Neuron interface functions according to the function code is removed. The new interface forms will be classified according to the interface functions, each interface function is a Topic, and all the Topics form a hierarchical Topic tree, which is more convenient for users.

### Add stress test process

The stability of Neuron can be tested for a long time under certain stress to prepare for a stable beta version.

### Support separate commercial modules

In the alpha.2 version, we support plugin development of driver modules in independent commercial Neuron, and third-party users will be able to use Neruon to develop their own private industrial protocol drivers.

## Test and bug fixes for Neuron 2.0

Both unit test and function test have been added to the daily development process of Neuron 2.0, which is running well in the CI workflow of GitHub. Complete unit test and function test will be performed on each submitted PR to ensure the steady progress of Neuron's daily development work.

At the same time, we fixed the following problems in the previous version:

- Modbus TCP read/write function test failed
- Memory leak in Data Value shared mode
- Neuron sometimes crashes when using Control-C to exit
- Neuron sometimes fails to exit with Control-C
- The problem that requires the user to select the Node Type

## Neuron 1.4.0 progress

### New functions

We also completed the development of Neuron 1.4.0 this month. One of the important upgrades is the addition of String type processing, which was developed from customer requirements. Now, in addition to integers and floating numbers, strings are also supported for point data. Users can directly use the strings to represent numerical values, and process the strings when reading and writing PLC data.

We have added string class functions to the following drivers:

- Modbus TCP/RTU/RTU on TCP
- OPC UA
- Siemens ISOTCP
- Omron FINS on TCP
- Mitsubishi Q-Series and L-Series
- Mitsubishi FX5U

In addition, we have also enhanced the capability of OPC UA, which now supports the processing of OPC Chinese labels. For Siemens ISOTCP, the function of writing point information has been added.

### Bug fixes

- Fixed Mitsubishi Q series read/write Dword and String.
- Fixed OPCUA to support utf8.
- Fixed unreadable dot demo.
- Fixed API function 50.
