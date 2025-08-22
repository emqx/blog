## **Introduction: Bridging the Gap Between OT and IT**

In the wave of Industry 4.0, seamlessly integrating real-time device data from the OT (Operational Technology) layer with cloud applications in the IT (Information Technology) layer is key to unlocking data potential and achieving smart manufacturing. The Siemens S7-1200 PLC, a cornerstone of industrial automation, contains a vast amount of production status and equipment parameter data. Efficiently and reliably transmitting this valuable OT data to an [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) for use by MES, SCADA, or cloud-based AI analytics platforms is a common challenge for many enterprises.

Traditional solutions often involve complex programming and protocol conversion, which are both time-consuming and labor-intensive. Now, with the powerful industrial edge gateway software, NeuronEX, you can easily build a stable data bridge from a Siemens S7-1200 PLC to MQTT in under 10 minutes, all in a no-code fashion.

This article will provide a step-by-step guide to walk you through the entire configuration process, from PLC setup to successfully viewing data in an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools).

## **Architecture**

This tutorial aims to read specified variable data from a Siemens S7-1200 PLC, send the data in JSON format to a designated MQTT Broker, and verify the data using the [MQTTX](https://mqttx.app/) client software. The technical architecture consists of three core components:

- **Data Source:** Siemens S7-1200 PLC
- **Data Collection Software:** NeuronEX 
- **Data Destination:** EMQX (this article uses the public broker `broker.emqx.io` as an example)
- **MQTT Client Tool:** MQTTX

![b23dc7105aa27796551bd58bf50b442c.png](https://assets.emqx.com/images/969b5982923163e75cd2254fbf9ec005.png)

## **Prerequisites**

Before you begin, please ensure you have the following:

- A Siemens S7-1200 PLC and TIA Portal programming software.

- NeuronEX: Quickly deploy it via Docker with a single command.

  ```shell
  # Start NeuronEX
  docker run -d --name neuronex -p 8085:8085 --log-opt max-size=100m --privileged=true emqx/neuronex:latest
  ```

- An MQTT Client: We will use [MQTTX](https://mqttx.app/) to verify the data later.

## Connecting Siemens S7-1200 PLC to MQTT

### **Step 1: Configure Siemens S7-1200 PLC**

To allow NeuronEX to access PLC data, ensure that the network between NeuronEX and the S7-1200 is clear. We will use NeuronEX to collect data from the Data Block (DB2) and M area of the Siemens S7-1200. The tags to be collected from the data block (DB2) are shown in the red box in the figure below:

![image.png](https://assets.emqx.com/images/3217258af31e56280a9df26634ecdb99.png)

### **Step 2: Add a Southbound Device in NeuronEX**

Now, let's tell NeuronEX where to read the data from.

1. Access the NeuronEX management interface at `http://localhost:8085`
2. Navigate to **Data Collection** -> **South Devices** and click **Add Device**. Select the **Siemens S7 ISOTCP** plugin.
3. Fill in the device information:
   - **Name:** `S7-1200-Workshop`
   - **Target PLC IP Address:** Enter the IP address of your PLC.
   - Leave the other parameters at their default values.

![image.png](https://assets.emqx.com/images/ad293a232b01af344da2968e0e4d0bd6.png)

### **Step 3: Create Data Tags**

This is the core step where you define "what data to collect".

1. Click on the newly created `S7-1200-Workshop` driver to enter the **Group List** page and create a collection group named `group1`.
2. Enter the group and start to **Add Tag**. Add the following tags precisely according to the addresses in your PLC:

| Data Type | PLC Address Example | NeuronEX Configuration                     | Address Format Description                  |
| :-------- | :------------------ | :----------------------------------------- | :------------------------------------------ |
| **Bool**  | `M10.0`             | **Type**: `BIT`, **Address**: `M10.0`      | M area, bit 0 of byte 10.                   |
| **Int**   | `MW20`              | **Type**: `INT16`, **Address**: `MW20`     | M area, word starting at address 20.        |
| **Real**  | `MW30`              | **Type**: `FLOAT`, **Address**: `MW30`     | M area, double word starting at address 30. |
| **DINT**  | `DB2.DBW4`          | **Type**: `INT32`, **Address**: `DB2.DBW4` | In DB2, double word starting at address 4.  |

![image.png](https://assets.emqx.com/images/df9f39d8bf7518deaa0d197ca8a92b07.png)

### **Step 4: Monitor Data Collection**

After completing step 3, you can view the real-time status of the `S7-1200-Workshop` driver on the **South Devices** page. A **Connected** status indicates that the connection between NeuronEX and the S7-1200 is `connected`.

![image.png](https://assets.emqx.com/images/61a0f2f8a5fa5e0190554194ab63e9cc.png)

You can view the real-time values of these tags on the **Data Collection** -> **Data Monitoring** page. You will see that the value of `tag4` is `-123`, which matches the value in the TIA Portal software.

![image.png](https://assets.emqx.com/images/49d95a3c45319edfc7c109ffe78f51f8.png)

### **Step 5: Configure the Northbound MQTT Application**

Finally, let's configure the data's destination.

1. On the left menu, click **North Apps** -> **Add Application** to add a northbound MQTT application.

2. Select the **MQTT** plugin and configure the connection parameters:

   - **Name**: `emqx`
   - **Server Address**: `broker.emqx.io` ([Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker))
   - **Port**: `1883`
   - Leave other settings at their default values.

3. Click **Create**.

   ![image.png](https://assets.emqx.com/images/d71cb5eb5c680b8c57801f30198776ef.png)

4. After creating the MQTT application, click the **Add Subscription** button.

   ![image.png](https://assets.emqx.com/images/56d51f622361534bb48535fbe1703522.png)

5. Add the collection group from the southbound driver `S7-1200-Workshop` to the subscription, and set the publishing [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) to `neuronex/s7-1200/data`.

   ![image.png](https://assets.emqx.com/images/531ce4b79dcc2eb3e5346223daa99e03.png)

### **Step 6: Subscribe and Verify Data**

This is the final step to complete the data flow.

1. Open your MQTTX client, create a new connection to `broker.emqx.io:1883`, and subscribe to the topic `neuronex/s7-1200/data`.
2. You will immediately see the PLC data collected by NeuronEX being continuously pushed to MQTTX in a standard JSON format!

![image.png](https://assets.emqx.com/images/97297eadfa53aa26d250c5e30f28bd73.png)

## **Conclusion**

Congratulations! You have successfully connected a Siemens S7-1200 PLC to MQTT within 10 minutes using NeuronEX. The entire process requires no code and is completed through a simple web interface, establishing a stable and efficient channel for industrial data collection and cloud integration.

This demonstrates the powerful capabilities of NeuronEX as a modern industrial edge gateway: it can dive into the OT layer to finely handle device protocols and data tags, and seamlessly integrate with the IT world to easily deliver data to the cloud.

Download NeuronEX now to kickstart your industrial IoT journey: [Download NeuronEX](https://www.emqx.com/en/try?tab=self-managed).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
