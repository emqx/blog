In the Industrial Internet of Things (IIoT), bidirectional data flow is key to enabling smart manufacturing. Beyond collecting data from devices, many scenarios now require the ability to send commands back for control and automation.

NeuronEX is a real-time data acquisition and analytics software deployed at the industrial edge. It supports a wide range of industrial protocols for efficient data collection, filtering, and edge processing. More importantly, it offers flexible device control capabilities, allowing commands to be sent back to devices for closed-loop control in diverse industrial applications.

This article explores NeuronEX’s device control features and how they can help optimize production and enhance automation.

## What is Device Control

Device control refers to the process of sending commands to downstream automation devices to control device behavior or modify device parameters. NeuronEX provides multiple control methods to meet the needs of different application scenarios:

- **Dashboard Control**: Human control through an intuitive user interface.
- **MQTT Control**: Sending control commands to devices via [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt).
- **Data Processing Module Control**: Implementing intelligent control using NeuronEX's data processing engine.
- **API Control**: Programmatic control through RESTful API interfaces.

During the device control process, device tags must have writable attributes; otherwise, the write operation will fail. A writable attribute means that the tags configured in NeuronEX must have the write property, and the corresponding tags on the device side must also support write operations.

## Dashboard Control

Dashboard control is the most intuitive human-machine interaction method, suitable for operations personnel performing daily operations and temporary debugging. Access the NeuronEX Web interface, go to **Data Collection** -> **Data Monitoring** page, select the appropriate southbound device and group name, find tags with write attributes, click the Write button at the end, enter a new value in the popup dialog, and click "Submit" to complete device control.

![image.png](https://assets.emqx.com/images/75000a59e380aa80291e13c77aca44ee.png)

## MQTT Control

### Feature Introduction

MQTT control allows any client program that supports the MQTT protocol to send command data to the corresponding topic on an [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison). The NeuronEX northbound MQTT plugin subscribes to this topic to receive data and sends control commands to the southbound driver node to implement device control. 

This method is especially effective when using EMQX to build a UNS(Unifed Name Space) in industrial scenarios.

![image.png](https://assets.emqx.com/images/f3129f258abc1f116c511c8f910f040c.png)

To use this method, you need to configure the northbound MQTT plugin in NeuronEX and set the **Write Request Topic** and **Write Response Topic**. At the same time, you need to configure the southbound driver node and set the tags to readable and writable status. The following example provides detailed instructions using EMQX and MQTTX (as an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools)).

### Complete MQTT Example

**1) Configure Southbound D11river**

Configure the ModbusTCP southbound driver **modbus1** in NeuronEX, with group name **group1**, and add three data points **tag1**, **tag2**, **tag3** (supporting read and write). The modbus1 driver reads data from a Modbus simulator. For detailed information about this step, please refer to Connecting Southbound Drivers.

![image.png](https://assets.emqx.com/images/041de51184ac382996cea18ee5ebc363.png)

**2) Configure Northbound MQTT Plugin**

Create a new northbound MQTT plugin in NeuronEX. In the plugin configuration, you can use the default **Write Request Topic** `/neuron/HgihrB/write/req` and **Write Response Topic** `/neuron/HgihrB/write/resp` to receive MQTT control commands, as shown below. In this example, we use EMQ's public MQTT server `broker.emqx.io` as the MQTT Broker.

![image.png](https://assets.emqx.com/images/686f3bdf45807b66da065f27f8899ef0.png)

**3) EMQX Configuration**

There is no need to deploy or configure EMQX separately since we are using EMQ's public MQTT server.

**4) MQTTX Configuration**

Add a new connection in MQTTX to connect to the public MQTT server `broker.emqx.io`.

![image.png](https://assets.emqx.com/images/332a997a57a0fd72507abd2369c913cd.png)

Refer to the NeuronEX MQTT data control format. The JSON message structure for controlling a single data tag is as follows:

- **uuid** is a unique identifier generated by NeuronEX, used to match response data when receiving control responses.
- **node** is the southbound driver node name; in this example, it's `modbus1`.
- **group** is the southbound driver group name; in this example, it's `group1`.
- **tag** is the southbound driver tag name; in this example, it's `tag1`.
- **value** is the value to be written; in this example, it's `1234`.

```json
{
    "uuid": "cd32be1b-c8b1-3257-94af-77f847b1ed3e",
    "node": "modbus1",
    "group": "group1",
    "tag": "tag1",
    "value": 1234
}
```

For more information about the NeuronEX MQTT data control format, such as multi-tag writing, please refer to [MQTT Upstream and Downstream Data Format](https://docs.emqx.com/en/neuronex/latest/configuration/north-apps/mqtt/api.html#write-tag).

In MQTTX, enter the JSON message above and configure the send topic as `/neuron/HgihrB/write/req`. Click the “send” button to send the control command to the MQTT Broker.

To check if the control was executed successfully, you can use MQTTX's “**+ New Subscription**” button to subscribe to the `/neuron/HgihrB/write/resp` topic and view the response data.

![image.png](https://assets.emqx.com/images/a38bc23a0db2a4c24288463ff386ba5a.png)

**5) View Control Results**

On the **Data Collection** -> **Data Monitoring** page in NeuronEX, you can see that the value of tag1 has been updated to 1234, indicating that the control of tag1 in the southbound driver modbus1 through the MQTT client MQTTX was successful.

![image.png](https://assets.emqx.com/images/5f308dc588aa27fc3eeee825bfb9100e.png)

There’s no need to configure the southbound driver to the MQTT driver's subscription list if you only want to control devices using the MQTT driver. However, if you also want to report data from the southbound driver to the MQTT Broker via the MQTT driver, you must add the southbound driver to the MQTT driver’s subscription list.

## Data Processing Module Control

### Feature Introduction

NeuronEX's data processing module provides powerful data analysis and processing capabilities that can automatically trigger device control based on business logic, implementing automated control and closed-loop feedback.

In this example, we will use the value of tag1 collected by the NeuronEX southbound driver node modbus1 to automatically control and write to tag2 of the southbound driver node modbus1.

### Usage Example

**1) Send modbus1 Driver Data to the Data Processing Module**

Continue using the modbus1 driver from the [Complete MQTT Example](https://emqx.atlassian.net/wiki/spaces/EMQXBC/pages/1617821733/NeuronEX+Device+Control+Best+Practices#complete-mqtt-example). As shown in the figure below, configure the driver collection group to the data processing module's subscription group. After configuration, the neuronStream in the data processing module will receive all collection data from the modbus1 driver every second.

![image.png](https://assets.emqx.com/images/d8561b59d3f292588b4d217ff7f963b9.png)

**2) Create a Rule and Test Data Inflow**

To create a rule, navigate to the **Data Processing -> Rules page** and click on "Create Rule." Then, click the "Run Test" button to confirm that the data processing module is receiving collection data from the Modbus1 driver every second. This indicates that the previous configuration steps were successful. Once you have verified this, you can stop the rule test.

![image.png](https://assets.emqx.com/images/62b1aa25905bb72556f44c2b53796a41.png)

**3) Configure Control**

Edit the SQL editor on the current page and enter the following SQL statement. This SQL statement renames the value of tag1 to tag2, and the SQL data result is `{tag2: 1234}`. You can also enable rule debugging here to test and view the rule SQL output.

```sql
SELECT
  values.tag1 as tag2
FROM
  neuronStream
```

Select the rule action as `Neuron` type and configure as follows, indicating that the SQL output data result will be written to **tag2** of the southbound driver **modbus1** collection group **group1**.

![image.png](https://assets.emqx.com/images/5163d0920b13e0a76fdc400d407b25c0.png)

![image.png](https://assets.emqx.com/images/c23e3457d8c117ad2e3b647b235ba064.png)

After saving the rule, it automatically enters the running state.

**4) View Control Results**

Navigate to the **Data Collection** -> **Data Monitoring** page to verify that the value of **tag2** has been updated to `1234`. This indicates that the control of **tag2** in the southbound driver **modbus1** through the data processing module was successful.

At this point, we can click the Write button for **tag1** to write a new value of `5678`, and we can see that the value of **tag2** is also updated to `5678`, indicating that the control of **tag2** in the southbound driver **modbus1** through the data processing module was successful.

![image.png](https://assets.emqx.com/images/56690ef54a1db3f055a748ed5ead5821.png)

Using data processing module control enables the implementation of more complex control logic. This includes triggering various control operations based on different conditions, or initiating control actions based on combinations of multiple conditions, thereby facilitating the rapid development of intelligent applications in industrial settings.

## API Control

### Feature Introduction

NeuronEX provides comprehensive RESTful API interfaces that allow third-party applications to implement device control through the HTTP protocol. This method offers high flexibility and is suitable for integration with other systems.

By calling NeuronEX's RESTful API, you can read and write device tags data. For more details, please refer to the [NeuronEX API Documentation](https://docs.emqx.com/en/neuronex/latest/api/api-docs.html).

### POSTMAN Control Example

POSTMAN is a commonly used API testing tool that can implement device control by calling NeuronEX's RESTful API.

**1) Obtain NeuronEX Token**

In POSTMAN, select the POST method and call the `localhost:8085/api/login` interface. Set the request body to JSON format, enter the username and password, and click the send button to obtain the NeuronEX Token.

![image.png](https://assets.emqx.com/images/dbf2f66cbb508bf5f65bce195a345ab0.png)

**2) Call the Control Interface to Write Data**

In POSTMAN, select the POST method and call the interface at `localhost:8085/api/neuron/write`. Set the request header for `Authorization` with the value `Bearer ${Token}`. Then, set the request body to JSON format and input the control JSON message. Finally, click the send button to execute device control. For detailed information about the `/api/neuron/write` interface, please refer to the [NeuronEX API Documentation](https://docs.emqx.com/en/neuronex/latest/api/api-docs.html#tag/rw/paths/~1api~1neuron~1write/post).

```json
{
  "node": "modbus1",
  "group": "group1",
  "tag": "tag1",
  "value": 12
}
```

![image.png](https://assets.emqx.com/images/7abec667d00ffb08f3984a45d6ba3cf9.png)

**3) View Control Results**

On the **Data Collection** -> **Data Monitoring** page in NeuronEX, you can see that the value of **tag2** has been updated to `12`, indicating that the control of **tag2** in the southbound driver **modbus1** through the API was successful.

![image.png](https://assets.emqx.com/images/059398c041facfaa8a36982d77c0fa0c.png)

## Summary

The multiple device control functions provided by NeuronEX offer powerful support for intelligent control of industrial devices. Whether it's manual operation, remote control, or automated control, all can be implemented through NeuronEX. The flexible combination of these functions can greatly enhance the intelligence level and operational efficiency of industrial production.

Users can choose the most suitable control solution based on their actual needs and implement comprehensive device management and control from edge to cloud through NeuronEX.

Download NeuronEX now and start your industrial digital transformation journey: [https://www.emqx.com/en/try?tab=self-managed](https://www.emqx.com/en/try?tab=self-managed)

For the full features of NeuronEX, please refer to the documentation: [Product Overview | NeuronEX Documentation](https://docs.emqx.com/en/neuronex/latest/)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
