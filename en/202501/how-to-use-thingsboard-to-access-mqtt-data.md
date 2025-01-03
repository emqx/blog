## Introduction

ThingsBoard is a powerful open-source IoT platform for data collection, processing, visualization, and device management. Supporting key IoT protocols like [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), [CoAP](https://www.emqx.com/en/blog/coap-protocol), and HTTP, it offers both cloud and private deployment options to meet diverse needs.

Integrating ThingsBoard with MQTT offers a robust solution for real-time IoT data visualization, essential for understanding and managing diverse sensor data within an IoT ecosystem. ThingsBoard is renowned for its rich features and scalability, capable of handling large-scale device data and supporting complex analytics and automation workflows. When paired with the lightweight MQTT protocol, this integration ensures efficient, low-latency communication across devices, allowing data to be captured, processed, and visualized in real-time.

In this guide, we'll show you how to integrate a third-party [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), specifically EMQX, with ThingsBoard Cloud. You'll also learn how to create a custom dashboard to visualize MQTT data.

## Preparation

### Set Up ThingsBoard Cloud

Register at [ThingsBoard Cloud](https://thingsboard.cloud/signup). No installation is required for cloud users. In addition, you can also choose to [download and install](https://thingsboard.io/docs/user-guide/install/installation-options/) a private deployment.

### Creating an MQTT Broker on the EMQX Platform

We will use EMQX Platform to create a third-party MQTT broker. [Sign up for the EMQX Platform Console](https://accounts.emqx.com/signup?continue=https%3A%2F%2Fcloud-intl.emqx.com%2Fconsole%2F) and create a new deployment. As a new user, you will have a free 14-day trial for Dedicated plan.

In this context, a deployment refers to an MQTT broker cluster. EMQX Dedicated plan offers VPC peer-to-peer connectivity and a REST API, along with robust and flexible data integration capabilities. This makes it easy for users to connect with their existing cloud service resources. By providing a comprehensive operations and monitoring service, it saves significant time and labor costs, allowing businesses to concentrate on delivering greater value.

## Integrating EMQX Platform with ThingsBoard

### Configure EMQX Platform

1. **Obtain Connection Address and Port**

   First, create a Dedicated deployment. Once the instance status shows as **Running** on the EMQX deployment **Overview** page, locate the connection address and port for MQTT. This information will be used later when setting up integrations in ThingsBoard.

   ![EMQX deployment Overview page](https://assets.emqx.com/images/19a5925c1e3793226e2552a1290f31ef.png)

1. **Add Authentication Information**

   ![Authentication](https://assets.emqx.com/images/594e698d1e5753d84161cf38beb4efda.png)

### Configure ThingsBoard

Go to **Integrations** in ThingsBoard and click the **+** button to create a new integration. In the add integration pop-up dialog, you need to complete the following four steps:

1. **Choose MQTT integration type**

   Choose **MQTT** as the integration type and enter a name, such as "Integration with EMQX Platform". Keep other options at their default values and click “Next” to proceed to the second step.

1. **Configure an uplink data converter**

   Add a new **Uplink converter** to process incoming MQTT message payloads into the ThingsBoard format.

   Example: Name it **MQTT-Uplink**, enable **Debug Mode**, and paste the following script to decode the payload:

   ```
   // Decode an uplink message from a buffer
   // payload - array of bytes
   // metadata - key/value object
   
   // decode payload to json
   var payloadJson = decodeToJson(payload);
   var result = {
      deviceName: payloadJson.deviceName,
      attributes: {
          model: 'Model A',
          serialNumber: 'SN111',
          integrationName: metadata['integrationName']
      },
      telemetry: {
          temperature: payloadJson.temperature,
          humidity: payloadJson.humidity,
      }
   };
   
   // Helper functions
   function decodeToString(payload) {
      return String.fromCharCode.apply(String, payload);
   }
   function decodeToJson(payload) {
      // covert payload to string.
      var str = decodeToString(payload);
   
      // parse string to JSON
      var data = JSON.parse(str);
      return data;
   }
   
   return result;
   ```

   Optionally, click the **Test Decoder Function** button to test and verify whether the decoder function meets the expectations.

   Then click “Next” to proceed to the third step.

1. **Skip downlink data converter**

   The downlink data converter is optional, so we will skip this step.

1. **Integrate EMQX with ThingsBoard**

   Paste the **MQTT connection address** and **port** from your EMQX Platform instance.

   Since authentication is enabled by default in all EMQX Platform deployments, enable **Basic authentication** and input the **username** and **password** created in the EMQX **Authentication** section.

   Click **Check Connection**. A pop-up message will appear in the bottom right corner, notifying you that the connection has been successfully established. This indicates that the integration with the EMQX Platform deployment was successful. 

   Finally, define the filter topic (e.g., `/test/integration/emqxplatform`) to use during the testing phase, then click **Add** to complete the integration setup.

   ![Integrate EMQX with ThingsBoard](https://assets.emqx.com/images/4b314f24e73dd1d7332a078617aec8e3.png)

## Integration Test

After completing the above integration configuration, use the [MQTT 5.0 client tool](https://mqttx.app/), MQTTX, to simulate a device, in order to test and verify the effectiveness of the functionality.

1. Use MQTTX to connect to the EMQX Platform deployment.

2. After the connection is successfully established, simulate a device by sending temperature and humidity data to the filter topic `/test/integration/emqxplatform`, which was configured during the integration above.

   ```json
   {
     "deviceName": "Device Test",
     "temperature": 28,
     "humidity": 70
   }
   ```

   ![MQTTX](https://assets.emqx.com/images/e71f79a5258171c34bde2bd30d04184b.png)

3. In Thingsboard, go to the **Integrations** menu under **Integrations Center** and click 

   `Integration with EMQX Platform` name, you can see that there is an MQTT message publishing record for the event. This means that the EMQX Platform deployment has been successfully integrated.

   ![Integrations](https://assets.emqx.com/images/d9b2667b29b374c30831eef6f666e663.png)

## Customizing Your Dashboard to Access MQTT Data

1. Go to the **Dashboards** menu and click the **+** button to create a new dashboard. Name it "EMQX Platform Integration Dashboard."

2. Add a time-series table widget. Open the dashboard and click **+ Add new widget**. Search for **Timeseries table** and select it.

   ![Add new widget](https://assets.emqx.com/images/3c2824ae3fb57e182227c20b1bcfdd87.png)

   a. To configure a “Timeseries table” widget, follow these steps:

      i. **Select Device**: In the “Datasource” section, choose the device “Device Test.”

      ii. **Configure Temperature Column**: In the “Columns” section, select or input “temperature” as the key and set the label to “temperature.”

      iii. **Configure Humidity Column**: Still in the “Columns” section, select or input “humidity” as the key and set the label to “humidity.”

      iv. **Confirm Configuration**: Once configured, click the “Add” button at the bottom right to complete the process.

      ![Timeseries table](https://assets.emqx.com/images/2331efba55cdf34a7ce6c99f13d10ba1.png)

   b. Return to MQTTX, change the temperature value to 25 and humidity value to 80, publish a message again, and the corresponding data will be displayed in the table configured.

3. Similar to step 2 above, click Add a widget, search for charts, select Timeseries Line Chart, configure it, and change the real-time range to the last 5 hours. Using MQTTX, send another set of data, and the corresponding data will be displayed in both components.

   ![Timeseries Line Chart 1](https://assets.emqx.com/images/32e37805d996eec975e6c83c20e89b97.png)

   ![Timeseries Line Chart 2](https://assets.emqx.com/images/2ced6f37e65feefca2939374e0228d9c.png)

## Summary

By following these steps, you have successfully integrated the EMQX Platform with ThingsBoard and created a custom dashboard to visualize MQTT data. This integration enables efficient real-time monitoring of IoT devices, making it easier to manage data and improve operational insights.

For further exploration, you can customize your dashboard even more, add additional widgets, and fine-tune your system to suit your specific use case. This will allow you to monitor device-related data in real-time detail visually and set alert thresholds to help you resolve issues on time.

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
