# Neuron v1.3.0 is officially released with one-stop access to industrial data

As an important part of the [EMQ](https://www.emqx.com/en) industrial Internet cloud-edge collaboration solution, [IoT Edge Industrial Protocol Gateway Software - Neuron](https://www.emqx.com/en/products/neuron) has provided many users in the industrial field with the necessary functions for the industrial equipment data collection on the edge side since its releases, such as industrial protocol conversion and access, and equipment remote monitoring and management.

Neuron supports the access and conversion of dozens of industrial equipment protocols including Modbus, OPCUA, Mitsubishi, Siemens, Rock Automation, OMRON, etc., without the need for a container framework. It has ultra-low resource consumption and supports X86 and ARM architectures. It is an ideal choice for building an industrial IoT platform.

**Neuron v1.3.0 has been officially released recently**, and the download link is : [https://www.emqx.com/en/downloads?product=neuron](https://www.emqx.com/en/downloads?product=neuron)


## The protocol support list is expanded to cover the power industry

In the newly released Neuron v1.3.0, protocol support for the electric power industry such as DL/T645-07, IEC 60870-5 104, and IEC 61850 MMS has been added. At the same time, a PLC protocol of **FINS on TCP** is added. This means that Neuron will help more industry users realize the data management of edge devices.

> As the IEC 61850 protocol requires some functions related to model import and model analysis, the protocol only supports customization for the time being.

Taking the DL/T645-07 protocol as an example, the device wiring method is shown in the figure below. The meter is powered on and connected to the computer via a serial port connection through a USB to Modbus converter. Neuron can read the current, voltage, power and other parameters of the meter through configuration.

![Neuron read meter data](https://static.emqx.net/images/11c78b34a4a50b06668f8d2c12150dad.png)


## Existing protocol support is further enhanced

The supported protocols such as OPC UA and Modbus are enhanced and improved in the new version.

### OPC UA subscription function

In the property settings, there are buttons to select the subscription function to subscribe. This function receives data in a passive way, which can reduce the number of Neuron's read operations on the device, so as to reduce network traffic. When the subscribed point has the subscription permission on the OPC UA server, the data change of the point will be automatically updated to Neuron.

![OPC UA subscription function](https://static.emqx.net/images/e3ded90ea988a9b2644151f134217fbb.png)

### Modbus supports TCP Server mode

Modbus supports the connection of DTU devices. After configuring the remote server address in the cloud of the DTU device as the IP address of the environment where Neuron is running and configuring the corresponding port number, Neuron can access the DTU device to read data. In the driver settings of Neuron, when setting the Hostname, fill in the IP address of the environment where Neuron runs.

### Add the function that each point of Modbus can define byte order separately

Drive address format: STN!ADDR.BIT#ENDIAN

![Neuron Modbus](https://static.emqx.net/images/75a4b526fd72c473e2a3a293b257e87f.png)


## Improved security and more reliable data communication

The Web Server API HTTPS authentication function is added in the latest version. A secure SSL encrypted transmission protocol is added. On the Server API, you can encrypt the communication between the browser and the server through a remote HTTPS connection to ensure the security of data transmission.

![Neuron HTTPS](https://static.emqx.net/images/03093d2ffdc8d79d3305d79b79651cf5.png)


## Fix the bug and use it more smoothly

### Fix the problem that the user cannot log in with username when the server forces using UserTokenPolicy in the OPC UA protocol

Due to security considerations, some OPC UA servers prohibit the use of clear text to pass username and password when the device is logging in, but will provide a series of 「description of authentication methods」to the device. Then, the device will process the user information according to the description and submit it to the OPC UA server again. OPC UA will take corresponding actions only after verifying the user's information.

![Neuron OPC UA](https://static.emqx.net/images/47fba5367ff1814bbf5d3585ec1c7475.png)

### Fix startup problem of Docker 

Fix the problem of「has fatal error」in instance 1 when starting ten instances in Docker at the same time.


## With the original intention of open source, Neuron v2.0 is worth looking forward to

At present, the Neuron team is still improving the functions and performance of the product so that it can better integrate and collaborate with other EMQ products in the future. Neuron's future research and development will focus more on its core functions, and dig deeper into its product positioning of 「IoT Edge Industrial Protocol Gateway Software」to provide support for data「connection and mobility」in the industrial field.

At the same time, as an open source IoT data infrastructure software provider, EMQ will also start its open source process in Neuron v2.0. Neuron v2.0 will adopt a brand-new data communication architecture, make full use of the performance of multi-core CPUs, enhance the system responsiveness and carrying capacity, and obtain a faster response and higher data bandwidth with less memory. In addition, it will support the simultaneous connection of multiple devices, dynamic configuration changes (without restart) and hot updates of drivers.

The open source Neuron v2.0 will bring more users in the industry one-stop access support for edge industrial data, and a more open product form will also accelerate industry integration, and jointly promote the development of the industrial Internet with upstream and downstream partners.

The open source Neuron v2.0 will bring one-stop access support for edge industrial data to more users in the industry. A more open product form will also accelerate industrial integration and jointly promote the development of industrial Internet with upstream and downstream partners.

Please stay informed with us! 
