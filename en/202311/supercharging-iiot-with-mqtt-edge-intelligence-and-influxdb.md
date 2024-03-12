## Introduction

In the wave of Industry 4.0, [Industrial Internet of Things (IIoT)](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) is leading a revolution, redefining the way data is collected, analyzed, and utilized. In this vast network consisting of billions of devices, real-time data flow is crucial for achieving automation, efficiency, and predictive maintenance. 

This article presents a solution for IIoT with [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), edge intelligence, and InfluxDB. We will provide a detailed guide on how to integrate the fully managed MQTT cloud service platform, [EMQX Cloud](https://www.emqx.com/en/cloud), with edge computing intelligence and InfluxDB's analytical capabilities to bring about a transformative change in the Industrial IoT.

## EMQX Cloud: Addressing Challenges in IIoT

EMQX Cloud is a cloud-based [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) service designed specifically for handling large-scale IIoT data streams. It provides seamless connectivity from the edge to the cloud, ensuring real-time data transmission, processing, and analysis.

EMQX Cloud can empower IIoT advancement in the following aspects:

- **Handling Large Data Volumes**: In IIoT environments, devices generate massive amounts of data that require high-performance message delivery and data routing. EMQX Cloud efficiently handles large-scale data streams with its high-performance MQTT message broker and data routing capabilities, ensuring real-time data transmission and processing.
- **Device Management**: Managing connections, states, and firmware updates for a large number of devices is challenging. EMQX Cloud provides robust device connection management, allowing real-time monitoring of device online status and supporting over-the-air updates and remote management.
- **Scalability and Reliability**: As the number of devices increases, system scalability and reliability become critical. EMQX Cloud, with its cloud-based deployment and load-balancing technology, achieves highly scalable architecture, ensuring system availability and stability.
- **Security Challenges**: Data security in IIoT is paramount, as it may contain sensitive industrial information. EMQX Cloud offers robust data security protection by supporting TLS/SSL encryption and authentication, guaranteeing data confidentiality during transmission and storage.

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

## IIoT Solution with EMQX Cloud, InfluxDB, and Edge Intelligence

To build a seamless and efficient IoT data management solution for IIoT, we involve [NanoMQ](https://nanomq.io/) on a Raspberry Pi for communication with devices on edge, EMQX Cloud as a data hub to ensure the data transmission from edge to cloud, and InfluxDB for the data analysis and visualization. Organizations can gain in-depth insights from the collected and processed data, thus making informed decisions.

In this article, we will perform the following three major tasks to demonstrate this solution:

**Task 1: Installing NanoMQ on a Raspberry Pi**

First, we will guide you through the step-by-step process of installing and configuring NanoMQ on a Raspberry Pi. This is the first step in connecting devices to EMQX Cloud, ensuring everything is ready.

**Task 2: Bridging NanoMQ Data to EMQX Cloud**

It involves effectively bridging NanoMQ on the Raspberry Pi with EMQX Cloud. We will provide detailed instructions to ensure the connection is set up correctly.

**Task 3: Bridging EMQX Cloud Data to InfluxDB 3.0**

Finally, we will discuss how to set up EMQX Cloud to bridge data to InfluxDB 3.0. This will help you achieve seamless data flow.

## Deploying Edge Computing Solutions: Setting up an Edge MQTT Broker

When deploying edge computing solutions, choosing the right tools and components is crucial. NanoMQ, as an edge MQTT broker from EMQ, has its unique advantages. 

### NanoMQ: A Perfect Choice as an Edge MQTT Broker

NanoMQ is a lightweight, high-performance MQTT 5.0 broker designed for edge computing scenarios. Its advantages include:

- **Lightweight and Resource-Friendly**: NanoMQ is designed to run on resource-constrained edge devices with minimal impact on device performance.
- **Support for MQTT 5.0**: It supports the MQTT 5.0 protocol, providing more features and better performance to handle complex communication requirements.
- **Quick Deployment**: NanoMQ offers a simplified deployment process, allowing you to quickly configure and launch the MQTT broker, reducing deployment and configuration complexity.
- **Reliability and Stability**: NanoMQ is extensively tested and validated, demonstrating excellent stability and reliability for continuous operation in edge environments.

### Install and Configure NanoMQ on Edge Devices

1. **Download NanoMQ**

   Visit the EMQ official website and [download the NanoMQ](https://www.emqx.com/en/try?product=nanomq) version suitable for your edge device.

1. **Install NanoMQ**

   Depending on the device's operating system, execute the NanoMQ installation process. This typically involves extracting the downloaded files and running an installation script. In this example, we will use Apt sources to install NanoMQ on a Raspberry Pi.

   ```
   ## Download the repository
   curl -s https://assets.emqx.com/scripts/install-nanomq-deb.sh | sudo bash
   
   ## Install NanoMQ
   sudo apt-get install nanomq
   ```

1. **Configure NanoMQ**

   To configure NanoMQ bridging, modify the configuration file located at /etc/NanoMQ_bridge.conf by specifying MQTT broker parameters such as listening ports, authentication settings, and other options to forward data from specified topics to EMQX Cloud.

   Configuration parameters include:

   - Remote broker address
   - MQTT protocol version
   - Client identifier (automatically assigned by NanoMQ by default)
   - Clean start
   - Keep Alive
   - Username
   - Password
   - Forwarded topics (multiple topics separated by commas)
   - Quality of Service (QoS) level
   - Client parallel count

   In this example, the configuration file is nanomq_bridge.conf.

   ```
   bridges.mqtt.name {
     server = "mqtt-tcp://x.x.x.x:1883"
     proto_ver = 4
     username = xxx
     password = xxx
     clean_start = true
     keepalive = 60s
     forwards = [
       {
         remote_topic = "emqx/test"
         local_topic = "emqx/test"
         qos = 0
       }
     ]
     max_parallel_processes = 2
     max_send_queue_len = 1024
     max_recv_queue_len = 1024
   }
   ```

1. **Start NanoMQ**

   Use a startup script or command to launch NanoMQ. Once started, NanoMQ will begin listening on the specified port and be ready to accept MQTT connections.

   ```
   nanomq start --conf /etc/nanomq_bridge.conf
   ```

   ![nanomq start](https://assets.emqx.com/images/3753b2f29ab0d32d512442b49310b02f.png)

### Verify the Installation and Functionality of NanoMQ

To verify the installation and functionality of NanoMQ, you can perform the following actions:

1. **Connect to NanoMQ**

   Use [MQTT client tools](https://www.emqx.com/en/blog/mqtt-client-tools) such as [MQTTX](https://mqttx.app/) or mosquitto_sub/mosquitto_pub to connect to NanoMQ.

   ![**Connect to NanoMQ**](https://assets.emqx.com/images/0e3c186de5d1e75d767772994bf3d8ee.png)

1. **Publish and Subscribe to Messages**

   Publish a message and ensure it can be successfully delivered to subscribers. This can verify the broker's message delivery functionality.

   ![Publish and Subscribe to Messages](https://assets.emqx.com/images/084277ddcbe19c07a310e154e07aeba5.png)

1. **Monitor and Logs**

   Check NanoMQ's log files to ensure there are no errors or exceptions. This helps ensure the broker is working correctly.

1. **Performance Testing**

   You can use performance testing tools to simulate high-load conditions to ensure NanoMQ performs well on edge devices.

   Once you have successfully verified the installation and functionality of NanoMQ, you can trust it as an MQTT broker in your edge computing solution to support your IoT communication needs.

## Achieving Seamless Connection Between EMQX Cloud and Edge Devices

1. **Obtain SSL/TLS Certificates (Optional)**

   First, ensure that you have valid SSL/TLS certificates on EMQX Cloud. These certificates are used for encrypting communication to ensure data transmission security.

1. **Configure Device Parameters and Establish Connection**

   On the edge device, use the configured parameters to attempt a connection to the EMQX Cloud server.

   ![Configure Device Parameters and Establish Connection](https://assets.emqx.com/images/39d624c7a0310f61a732e7f0260f40d9.png)

1. **Publish and Subscribe Testing**

   Use MQTTX to connect to EMQX Cloud, subscribe to the "emqx/test" topic, and check if you receive messages from NanoMQ.

   ![Publish and Subscribe Testing](https://assets.emqx.com/images/f6aefc6a7aa15444e66fc4e617091224.png)

In summary, configuring the connection of edge devices to EMQX Cloud requires detailed setup, and testing the connection through publishing and subscribing to MQTT topics can help verify the feasibility of the connection. This process lays the foundation for achieving a seamless connection between EMQX Cloud and edge devices.

## Integrating InfluxDB: Configuration, Data Transformation, and Persistence

### The Power of InfluxDB

InfluxDB is a high-performance time series database, particularly suitable for storing and querying time-related data such as sensor data, monitoring metrics, logs, and more. The reasons for choosing InfluxDB as a time series database typically include:

1. **Performance and Scalability**: InfluxDB is optimized to efficiently handle large volumes of time series data. It supports horizontal scaling, allowing it to handle continuously growing data workloads.
2. **Data Model**: InfluxDB's data model is well-suited for time series data. It uses a structure of measurements, tags, and fields, making data storage and querying highly flexible.
3. **Query Language**: InfluxDB provides a powerful query language, including InfluxQL and Flux, for executing complex time series data analysis and aggregation operations.
4. **Community Support**: InfluxDB has an active community that provides extensive documentation, plugins, and tools, making it easier to use in various applications.
5. **Integration Support**: InfluxDB supports various integration methods, making it easy to integrate with other systems and applications, including EMQX Cloud.

### Create an InfluxDB Cloud Serverless Instance

To set up InfluxDB integration in EMQX Cloud, you can follow these steps:

1. Log in to the InfluxDB Cloud Serverless control panel using your InfluxDB Cloud account.

   ![Log in to the InfluxDB Cloud Serverless](https://assets.emqx.com/images/f44332d0238ca39f0aa39be18d39b73b.png)

1. **Create a Bucket**

   After logging into the control panel, navigate to the "Load Data" page and create a bucket named "emqx."

   ![Create a Bucket](https://assets.emqx.com/images/ca3d43e0ac57b021a39553259490c235.png)

1. **Generate an API Token**

   Return to the "Load Data" page and click "Generate API TOKENS" to create a new token. In this case, we will create a token with full permissions. Once the token is created, you can choose to enable or disable it.

   ![Generate an API Token](https://assets.emqx.com/images/6d48057aee8e40d00dfd171390221497.png)

### Set up InfluxDB Integration in EMQX Cloud

1. **Set up NAT Gateway**

   NAT Gateway provides EMQX Cloud Professional Edition deployments with the capability to access public resources without the need for VPC peering. Before connecting to InfluxDB, please set up NAT Gateway.

   ![Set up NAT Gateway](https://assets.emqx.com/images/b9a8b85008662953c821476cb64b07e9.png)

1. **Create a New Resource**

   Access the EMQX Cloud console, open the Data Integration page, and select the InfluxDB HTTP V2 service.

   ![Access the EMQX Cloud console](https://assets.emqx.com/images/06923956a7cbdaea916fbd8a78152841.png)

   Enter the configuration details in the new resource page. Note that the port is set to 443 and HTTPS is enabled.

   ![Enter the configuration details ](https://assets.emqx.com/images/b33969b3bb37b87203511764ee23e3aa.png)

   After configuring, click "Test Connection" to ensure the resource is available. Once the resource initialization is successful, confirm the settings.

1. **Create a Rule**

   After successfully creating the resource, return to the Data Integration page and find the newly created resource. Click "Create Rule."

   Our goal is to trigger the engine whenever the "emqx/test" topic receives monitoring data. Here, you need to apply some SQL processing:

   - Target only the "emqx/test" topic.
   - Retrieve the three data points we need: location, temperature, and humidity.

   Following these principles, the SQL should look like this:

   ```
   SELECT
       payload.location as location,
       payload.temp as temp,
       payload.hum as hum
   FROM "emqx/test"
   ```

   ![New rule](https://assets.emqx.com/images/9dbf31c9f9a4f8acb029765df275b740.png)

   This SQL can be interpreted as: When a message is received on the "emqx/test" topic, select the location, data.temperature, and data.humidity fields from the message.

   Next, you can click the "SQL Test" button, fill in the following data:

   - Topic: emqx/test
   - Payload:

   ```
   {
   "location": "Prague",
   "temp": 26,
   "hum": 46.4
   }
   ```

   Click "SQL Test" and check the data output. If the settings are correct, the test output should display the complete JSON data.

   ![Click "SQL Test](https://assets.emqx.com/images/3427b77af9cb833bc8857c6946d0b4d4.png)

1. **Create an Action**

   Click "Next" and on the new action page, the default action type is "Save Data to InfluxDB." Select the resource you created earlier.

   For this case, you can fill out this part as follows:

   - Measurement can be set arbitrarily; here, we use "temp_hum."
   - Field Keys are filled with the two data points we want to record: "temp" and "hum."
   - Tag Keys are set to "location."
   - Timestamp Key is left blank by default.

   ![Create an Action](https://assets.emqx.com/images/dca45f76f92356095909a00b3cd80bb2.png)

   After confirming that the information is correct, click "Confirm" in the lower right corner to complete the data integration configuration. Through these steps, you can successfully configure InfluxDB integration, transform MQTT data into a format suitable for a time series database, and verify the correct transmission and storage of data. This allows you to easily analyze and query time series data.

## In-Depth Data Analysis: Gaining Insights with InfluxDB

In this section, we will delve into data analysis using InfluxDB to gain insights into IIoT data. We'll cover the characteristics of the InfluxDB query language, how to extract data, and create simple dashboards for real-time monitoring. Additionally, we'll discuss testing methods to verify data accuracy and real-time performance.

### Characteristics of InfluxDB Query Language

InfluxDB is an **open-source time series** database designed specifically for storing and querying time-related data. Its query language has the following characteristics:

- **Focus on Time Series**: InfluxQL focuses on time series data, making it highly suitable for dealing with real-time and historical data. You can perform various operations such as data aggregation, filtering, slicing, and grouping to extract insights about time series data.
- **SQL-Style Syntax**: If you are familiar with SQL, learning InfluxQL will be relatively easy. It uses a syntax similar to SQL, making data querying more intuitive and straightforward.
- **Built-In Functions**: InfluxQL provides numerous built-in functions for performing data processing operations, such as calculating averages and sums, finding minimum and maximum values, and more. These functions can help you extract key data statistics.

### Create Simple Real-Time Monitoring Dashboards

Real-time monitoring is an essential application scenario for IIoT. You can use InfluxDB and related tools to create simple yet powerful dashboards for real-time monitoring of IIoT data.

1. **Data Source Setup**

   By using the InfluxDB query language, you can extract insights about IIoT data. For example, you can execute the following query to obtain data statistics about temperature and humidity sensors at a factory location for the last hour, grouped by time intervals.

   ```
   SELECT *
   FROM "temp_hum"
   WHERE
   time >= now() - interval '1 hour'
   AND
   ("hum" IS NOT NULL OR "temp" IS NOT NULL)
   AND
   "location" = 'Prague'
   ```

1. **Data Visualization**

   Set up a dashboard to display temperature, humidity, pressure, or other data over time in the form of charts or gauges. This helps monitor the device and process status in real-time.

   ![Data Visualization 1](https://assets.emqx.com/images/170c7d91ecb5fc6fbf71a6da8a14d8a0.png)
   ![Data Visualization 2](https://assets.emqx.com/images/8ca11d422cfd449f46c005c1de6bd6f7.png)
   ![Data Visualization 3](https://assets.emqx.com/images/e4d42dfe1b3cc5f3f030950437c3f692.png)

1. **Real-Time Monitoring Configuration**

   You can also consider setting up real-time monitoring modules to periodically query InfluxDB and display the latest data on the dashboard. This helps you keep track of the status and performance of IIoT devices in real-time.

### Test Data Accuracy and Real-Time Performance

1. **Compare with Data Source**: Compare data in InfluxDB with the original data source to ensure consistency.
2. **Create Test Cases**: Write test cases to simulate data input under different conditions and check if the system responds correctly.
3. **Real-Time Testing**: Monitor the data timestamps to ensure that data is transmitted and stored in a timely manner.
4. **Data Quality Monitoring**: Use dashboards to monitor outliers or missing data, as well as data integrity.

Through in-depth data analysis using InfluxDB and related tools, you can gain important insights about IIoT data, ensure data accuracy and real-time performance, and take appropriate actions when necessary. This is crucial for the success of IIoT applications.

## Conclusion

In conclusion, we have successfully completed the process of deploying NanoMQ on a Raspberry Pi, establishing data bridging, transmitting data to EMQX Cloud, and integrating data bridging with InfluxDB 3.0. 

As IIoT continues to evolve, a platform is needed that can handle complex data streams, ensure security, and provide deep insights. EMQX Cloud not only meets these requirements but also drives innovation in IIoT through its tight integration with MQTT and InfluxDB. This integration ensures a seamless data flow from devices to databases, regardless of the data volume or complexity. 




## Related resources

- [Integrating MQTT Data into InfluxDB for a Time-Series IoT Application](https://www.emqx.com/en/blog/building-an-iot-time-series-data-application-with-mqtt-and-influxdb)
- [MQTT Performance Benchmark Testing: EMQX-InfluxDB Integration](https://www.emqx.com/en/blog/mqtt-performance-benchmark-testing-emqx-influxdb-integration)
- [Getting Data from EMQX Cloud with InfluxDB Native Collector](https://www.emqx.com/en/blog/getting-data-from-emqx-cloud-with-influxdb-native-collector)
- [Save MQTT Data from EMQX Cloud on GCP to InfluxDB Cloud through the public network](https://www.emqx.com/en/blog/save-mqtt-data-from-emqx-cloud-on-gcp-to-influxdb-cloud-through-the-public-network)


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
