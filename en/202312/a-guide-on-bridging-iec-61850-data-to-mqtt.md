Our [previous blog](https://www.emqx.com/en/blog/iec-61850-protocol) introduced the IEC 61850 protocol, which is widely used in the power industry. This blog will explore the combination of IEC 61850 with [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), achieving data abstraction and integration with IEC 61850 and seamless data exchange using MQTT.

We will demonstrate using Neuron to collect data from the LibIEC61850 simulator, uploading the collected data to a locally-built EMQX MQTT Broker (`mqtt://192.168.10.174:1883`), and finally using the MQTT client tool, MQTTX’s subscription topic feature to see how the data has changed.

| **Application**            | **IP address** | **Port** |
| :------------------------- | :------------- | :------- |
| server_example_control.exe | 192.168.10.174 | 49333    |
| IEDExplorer                |                |          |
| Neuron                     | 192.168.10.174 | 7000     |
| EMQX                       | 192.168.10.174 | 1883     |
| MQTT X                     |                |          |

## Install the IEC 61850 Simulator

Go to [GitHub - mz-automation/libiec61850](https://github.com/mz-automation/libiec61850) to download the source code, follow the instructions on the project page to compile the source code. This article will demonstrate the compilation and installation on Windows 11, and then start **server_example_control.exe** on port 49333.

Open Developer PowerShell for VS 2019 to generate a Visual Studio project.

```
$ cd libiec61850
$ mkdir build
$ cd build
$ cmake -G "Visual Studio 16 2019" .. -A x64
```

Open libiec61850.sln in the build directory using Visual Studio to generate the solution.

```
$ ./examples/server_example_control/Release/server_example_control.exe 49333
```

## Install IEDExplorer

1. Download IEDExplorer here: [IEDExplorer](https://sourceforge.net/projects/iedexplorer/)
2. Open IEDExplorer_0.79n.exe and set the IP address and port on which the **server_example_control.exe** server listens, and start the connection.

![image.png](https://assets.emqx.com/images/3cedba15094356a42f99beaf63f393ea.png)

## EMQX Quick Start

Execute the following commands to install and run the EMQX container. For more information on how to install the EMQX container, please visit the [Installation Guide](https://www.emqx.io/docs/en/v5.0/deploy/install.html).

```
docker pull emqx/emqx:5.1.0
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083
```

## Neuron Quick Start

Neuron offers several installation methods, which you can review in detail in the [Installation Guide](https://neugates.io/docs/zh/latest/installation/installation.html). This example uses a containerized deployment so that you can start experiencing Neuron as soon as possible. Execute the following commands to install and run the Neuron container.

```
$ docker pull emqx/neuron:latest
$ docker run -d --name neuron -p 7000:7000 --privileged=true --restart=always emqx/neuron:latest
```

Open a web browser, and enter the address and port number of the gateway where you are running Neuron to get to the management console page. The default port number is 7000. Go to `http://localhost:7000/` (localhost can be replaced with your actual IP address) through your browser.

#### Step 1: Login

After the page opens, it goes to the login interface, where you can log in with the initial user name and password (initial user name: admin, initial password: 0000).

#### Step 2: Add Southbound Device

Select Southbound Devices in the **Configuration** menu to enter the **South Devices** screen and click **Add Device** to add a new device.

- Name: fill in the device name, for example, iec61850-174;
- Plug-in: drop-down box to select the IEC61850 plug-in.

#### Step 3: Set the Southbound Device Parameters

Automatically enter the device configuration interface after adding a southbound device, fill in the parameters and submit.

- Device IP address: Fill in the IP address of server_example_control.exe, such as 192.168.10.174.
- Device Port: Enter 49333.
- Local AP Title: Default setting "1.1.1.999".
- Local AE Qualifier: default setting 12.
- Local P Selector: default setting 1.
- Local S Selector: Default setting 1.
- Local T Selector: Default setting 1.
- Remote AP Title: Default setting "1.1.1.999.1".
- Remote P selector: default setting 1.
- Remote S Selector: default setting 1.
- Remote T Selector: Default setting 1.
- Enable connection authentication: default setting False.

#### Step 4: Create a Group in the Device Card

Click any blank space of the device node card to enter the group list management interface, and click Create to bring up the dialogue box for creating a group. Fill in the parameters and submit:

- Group name: Fill in the group name, for example, group-0;
- Interval: default 1000.

#### Step 5: Add Data Point Locations to the Group

Enter the point list management interface, click **Create**, fill in the point parameters and submit:

- Name: Fill in the name of the point, for example, RptID;
- Attribute: Drop down to select point properties, e.g. Read, Write;
- Type: Drop down to select the data type, for example, String;
- Address: Fill in the drive address, for example, simpleIOGenericIO/LLN0$RP$ControlEventsRCB01$RptID.
- Description, Decimal, and Precision are not filled in.

#### Step 6: View Collected Data in Data Monitoring

Select **Monitoring→Data Monitoring** to enter the Data Monitor interface and view the values read from the created points.

![View Collected Data in Data Monitoring](https://assets.emqx.com/images/e5f659115ea24301b8eabd6d98890621.png)

#### Step 7: Add a Northbound Plug-in Module to the Application

Select **North Apps** in the Configuration menu and click **Add Application**.

- Name: Fill in the application name, for example, MQTT;
- Plugin: drop-down box to select the MQTT plugin.

#### Step 8: Set the North Application Parameters

- Client ID: Note that this ID should be independent of each other. Duplicate IDs will cause the client to be kicked. For example, set to MQTT2000;
- QoS Level: Default is 0;
- Reporting data format: Default is Values-format;
- Write request subject: Defaults to /neuron/MQTT/write/req;
- Write response subject: Defaults to /neuron/MQTT/write/resp;
- Offline Cache: Off by default;
- Server Address: Fill in the address of the locally installed EMQX MQTT Broker at 192.168.10.174, which is your actual IP address;
- Server Port: Default 1883;
- User name, password: Not filled;
- SSL: Disabled by default.

#### Step 9: Subscribe to the South Tag Group

Go to the list of subscription groups and click **Add Subscription**.

- South Device: Drop-down box to select a created southbound device. For example, iec61850-174;
- Group: Drop-down box to select the group to subscribe to, e.g., group-0;
- Topic: The MQTT topic, which in this case defaults to /neuron/MQTT/group-0. Next, subscribe to this topic in MQTTX and receive messages.

## Receive the Data Using MQTTX

You can go to the [MQTTX official website](https://mqttx.app/) to download and install it. After installation, start MQTTX and add connection, set Host to `mqtt:://192.168.10.174`, Port to `1883`, subscribe to the topic `/neuron/MQTT/group-1`, and then you can receive the data transferred from IEC 61850.

![MQTTX](https://assets.emqx.com/images/c38ef0cc51ceb04e0fb5b97d9990ad79.png)

## Summary

The IEC 61850 specification enables communication and data exchange between power devices, while MQTT provides an efficient, flexible, and secure messaging mechanism. By taking advantage of both protocols, the integration seamlessly transfers device data to the cloud, facilitating efficient and secure remote monitoring. The ability to access real-time information from devices and processes enables organizations to optimize operations, increase productivity, and ensure the highest levels of quality. 



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
