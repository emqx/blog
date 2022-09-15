Node-RED is a programming tool for wiring together hardware devices, APIs and online services in new and interesting ways.

It provides a browser-based editor that makes it easy to wire together flows using the wide range of nodes in the palette that can be deployed to its runtime in a single click. 

Besides some basic network service application nodes, such as HTTP and WebSocket, Node-RED provides access support to the [MQTT](https://www.emqx.com/en/mqtt) protocol. Currently, it provides an MQTT subscription node and a release node. The subscription node is used for data input, while the release node can be used for data output.

This article will introduce the complete operation process for accessing the MQTT server by using Node-RED, filtering and processing the MQTT data before sending it to the [MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker). Users may quickly understand how to use Node-RED for simple stream processing of MQTT data.

## Install Node-RED

Node-RED, installed either on your PC, or devices such as Raspberry Pi, or cloud servers, can be quickly installed and used. Here are two common methods for installation:

Use `npm` for global installation:

```
npm install -g --unsafe-perm node-red
```

Use `Docker` for installation:

```
docker run -it -p 1880:1880 --name mynodered nodered/node-red
```

## Run

If you use npm for global installation, and after you are prompted that the installation is successful, you can start the Node-RED immediately by simply running the node-red command globally. 

Whether Docker or npm is used, after successful startup, we only need to open the browser and enter the current address plus 1880 port number to open the browser editor page of Node-RED. For example, if running locally, open the browser and enter [http://127.0.0.1:1880](http://127.0.0.1:1880/). When you see the page shown in the following figure, it means that Node-RED has been successfully started:

![Node-RED](https://assets.emqx.com/images/cd66e004a35d9588c000d3f7e21ab5c2.png)

## Use MQTT in Node-RED

This article will introduce the free public [MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ, which is created on the basis of [MQTT Cloud - EMQX Cloud](https://www.emqx.com/en/cloud). the access information of the server is as follows:

In the following functional demonstration, we will provide a simple use case of using Node-RED to process the received JSON data containing temperature and humidity information, then make a rule judgment on the temperature value, and send the currently changed temperature value again through MQTT when the temperature changes.

### **Connect MQTT server**

First, drag and drop a node of MQTT into the page in the menu bar on the left. After double-clicking the node, a configuration page for editing MQTT node will appear on the right, then create a new connection information according to the content prompts, fill in other connection information of MQTT, and click on the Done button to save the node information.

![Node-RED MQTT in node](https://assets.emqx.com/images/597fb3a3e45ce8544d89d7e8cbdd0b86.png)

### **Process MQTT data**

Data access: Drag and drop a JSON node into the page, and we can configure an Action in the configuration page of JSON node. Then we set it as Always Convert to Javascript Object. As we can't be sure whether the received data is a JSON format data or a JSON string, the first step is to perform JSON conversion on the received messages. After configuration, we connect this node with the MQTT in node.

![Node-RED JSON node](https://assets.emqx.com/images/25874952e5de18fe8126ca5afa3d392b.png)

Data filtering: after we configure and format the received message data, drag and drop a filter node into the page. After double-clicking the node, configure the rules in the configuration page. Select a Mode first and set it as a block unless value changes. The filtering rule is that the value of the currently received data needs to be changed. At present, the data is in JSON format, and what we should judge is a certain value in the JSON data, so we need to set the value as msg.payload.temperature in Property. After the configuration is completed, click the Done button to save the configuration of data filtering node, and finally connect the node with the JSON node after the previous configuration.

![Node-RED filter node](https://assets.emqx.com/images/9b77d353d63a4f2b32045f9d7399cd78.png)

Using template: after filtering the data, drag and drop a template node into the page, and double-click the node to configure the template content, so that the filtered data can be output through the template. Of course, the filtered data can be directly output by skipping this step.

![Node-RED template node](https://assets.emqx.com/images/8818d78773b2e7e7b0450c507073ac8c.png)

### **Publish the processed MQTT data**

Finally, send the processed data by MQTT after the above data processing and filtering, drag and drop an MQTT out node into the page, fill in the same connection information as MQTT in node, configure a Topic for users to receive data, save it, then connect it with the template node, and click the Deploy button in the upper right corner to deploy the current rule application online.

![Node-RED MQTT out node](https://assets.emqx.com/images/a0aeb565961ad24ed5d0344d16adc01b.png)


## Test

After finishing the function arrangement of the whole stream data processing, we use [MQTT 5.0 client - MQTT X](https://mqttx.app) to test and validate the usability of this function. We create a new connection, connect it with the MQTT cloud service address previously configured in Node-RED, and then enter the Topic in the MQTT in node to send a message, so that Node-RED can receive the MQTT data we have sent.

Then we subscribe to a Topic configured in MQTT X node to receive the processed message data. When a message data containing temperature and humidity information is sent, we can receive a message sent according to the message template we set, but we can't receive it again if it is sent again.

![MQTT X publish messages](https://assets.emqx.com/images/d7f584d50d337c45918af3f3187e522b.png)

As the temperature value has not changed at this time, and when we modify the temperature value again, we will find that we have received another message reminding us that the temperature value has changed.

![MQTT X receive messages](https://assets.emqx.com/images/04d009b040ca894f026a4beb34014f92.png)

## Summary

Now we have completed the whole process for installing and connecting with MQTT cloud service by using Node-RED, and filtering and processing MQTT message data, and finally sending the processed data message.

The interaction and use of Node-RED, that is, using UI to describe general business logic, can lower the threshold for non-professional developers to get started. TO use a visual tool to quickly create the required complex execution tasks, users may build complex tasks through simple node connection, which is very helpful, especially for some IoT application scenarios.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
