## Introduction

Industry 4.0 has ushered in a new era of technological advancements, and the [Industrial Internet of Things (IIoT)](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) is at the forefront of this revolution. IIoT has transformed the way data is collected, analyzed, and utilized. With billions of interconnected devices, real-time data flow is crucial to achieving automation, efficiency, and predictive maintenance. 

In this article, we will introduce a complete solution for Industrial IoT using [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), edge intelligence, and Timescale. We'll provide a step-by-step guide on how to integrate EMQX Cloud, a fully managed MQTT cloud service platform, with edge computing intelligence and Timescale's analytical capabilities. This will enable a revolutionary transformation in the Industrial IoT, and we'll explain everything in detail.

## EMQX Cloud: Addressing Challenges in IIoT

[EMQX Cloud](https://www.emqx.com/en/cloud) is a cloud-based MQTT broker service designed specifically for handling large-scale IIoT data streams. It provides seamless connectivity from the edge to the cloud, ensuring real-time data transmission, processing, and analysis.

EMQX Cloud can empower IIoT advancement in the following aspects:

- **Handling Large Data Volumes**: In IIoT environments, devices generate massive amounts of data that require high-performance message delivery and data routing. EMQX Cloud efficiently handles large-scale data streams with its high-performance MQTT message broker and data routing capabilities, ensuring real-time data transmission and processing.
- **Device Management**: Managing connections, states, and firmware updates for a large number of devices is challenging. EMQX Cloud provides robust device connection management, allowing real-time monitoring of device online status and supporting over-the-air updates and remote management.
- **Scalability and Reliability**: As the number of devices increases, system scalability and reliability become critical. EMQX Cloud, with its cloud-based deployment and load-balancing technology, achieves highly scalable architecture, ensuring system availability and stability.
- **Security Challenges**: Data security in IIoT is paramount, as it may contain sensitive industrial information. EMQX Cloud offers robust data security protection by supporting TLS/SSL encryption and authentication, guaranteeing data confidentiality during transmission and storage.

## IIoT Solution with EMQX Cloud, Timescale, and Edge Intelligence

To build a seamless and efficient IoT data management solution for IIoT, we involve [NanoMQ](https://nanomq.io/) on a Raspberry Pi for communication with devices on edge, EMQX Cloud as a data hub to ensure the data transmission from edge to cloud, and Timescale for the data analysis. Organizations can gain in-depth insights from the collected and processed data, thus making informed decisions.

In this article, we will perform the following three major tasks to demonstrate this solution:

**Task 1: Installing NanoMQ on Raspberry Pi**

First, we will walk you through how to install and configure NanoMQ on a Raspberry Pi. This is the first step in connecting devices to EMQX Cloud, ensuring everything is ready.

**Task 2: Bridging NanoMQ Data to EMQX Cloud**

Task Two involves bridging data effectively from NanoMQ on the Raspberry Pi to EMQX Cloud. We will provide detailed guidelines to ensure the connection is set up correctly.

**Task 3: Bridging EMQX Cloud Data to Timescale**

Finally, we will discuss how to set up EMQX Cloud to bridge data to Timescale. This will help you achieve complete data flow.

## Deploying Edge Computing Solutions: Setting Up an Edge MQTT Broker

When deploying edge computing solutions, choosing the right tools and components is crucial. NanoMQ, as an edge MQTT broker from EMQ, has its unique advantages.

### NanoMQ: A Perfect Choice as an Edge MQTT Broker

NanoMQ is a lightweight, high-performance MQTT 5.0 broker designed for edge computing scenarios. Its advantages include:

- **Lightweight and Resource-Friendly**: NanoMQ is designed to run on resource-constrained edge devices with minimal impact on device performance.
- **Support for MQTT 5.0**: It supports the MQTT 5.0 protocol, providing more features and better performance to handle complex communication requirements.
- **Quick Deployment**: NanoMQ offers a simplified deployment process, allowing you to quickly configure and launch the MQTT broker, reducing deployment and configuration complexity.
- **Reliability and Stability**: NanoMQ is extensively tested and validated, demonstrating excellent stability and reliability for continuous operation in edge environments.

### Install and Configure NanoMQ on Edge Devices

1. **Download NanoMQ**

   Visit the EMQ official website and download the NanoMQ version suitable for your edge device.

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

   ![Start NanoMQ](https://assets.emqx.com/images/ec38d78a50dd4b984442814775694ed5.png)

### Verify the Installation and Functionality of NanoMQ

To verify the installation and functionality of NanoMQ, you can perform the following actions:

1. **Connect to NanoMQ**

   Use MQTT client tools such as MQTTX or mosquitto_sub/mosquitto_pub to connect to NanoMQ.

   ![Connect to NanoMQ](https://assets.emqx.com/images/65e801bffae9143af49a745c87fbc824.png)

1. **Publish and Subscribe to Messages**

   Publish a message and ensure it can be successfully delivered to subscribers. This can verify the broker's message delivery functionality.

   ![Publish and Subscribe to Messages](https://assets.emqx.com/images/1393ca4be29f1862c6c0bb06cb81f5f4.png)

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

   ![Configure Device Parameters and Establish Connection](https://assets.emqx.com/images/cfe8d45d6f03468fa705d868b86f9c07.png)

1. **Publish and Subscribe Testing**

   Use MQTTX to connect to EMQX Cloud, subscribe to the "emqx/test" topic, and check if you receive messages from NanoMQ.

   ![Publish and Subscribe Testing](https://assets.emqx.com/images/5af5fbea88a0ab7d64ee9331a21b7dbd.png)

In summary, configuring the connection of edge devices to EMQX Cloud requires detailed setup, and testing the connection through publishing and subscribing to MQTT topics can help verify the feasibility of the connection. This process lays the foundation for achieving a seamless connection between EMQX Cloud and edge devices.

## Integration with Timescale: Configuration, Data Transformation, and Persistence

### Timescale as a Time Series Database

In this task, we will delve into data analysis, using Timescale to gain insights into IIoT (Industrial Internet of Things) data. We will discuss the features of Timescale query language, how to extract data, create simple dashboards for real-time data monitoring, and how to perform testing to verify data accuracy and real-time data.

**1. Focusing on Time Series Data**: Timescale is specifically designed for handling time series data. In the context of the Industrial Internet of Things, a large volume of data is recorded with timestamps, such as sensor data and event logs. Therefore, choosing a database system specialized in time series data can provide more efficient data storage and querying.

**2. Horizontal Scalability**: In an IIoT environment, data volumes can grow rapidly. Timescale supports horizontal scalability, allowing easy expansion of storage capacity to accommodate growing data requirements. This ensures performance and reliability when handling large-scale time series data.

**3. Support for Complex Queries**: Timescale offers powerful query capabilities, enabling complex analytics operations such as data aggregation, sliding time window analysis, time series interpolation, and more. This is crucial for data analysis and forecasting in IIoT applications.

**4. Data Retention Policies**: Data in the Industrial Internet of Things often needs to be managed according to specific retention policies to save storage space and maintenance costs. Timescale provides automated data partitioning and data expiration policies to automatically remove old data while retaining necessary historical data.

**5. Integration with EMQX Cloud**: Due to the close integration of EMQX Cloud with Timescale, the process of data transmission from edge devices to the database becomes smoother, ensuring data real-time and integrity.

**6. Community Support and Ecosystem**: Timescale is an open-source project with a large community support, allowing benefit from rich features and extensions contributed by the community. Moreover, integration with other tools and frameworks is relatively straightforward, building more robust data analysis and visualization tools.

In conclusion, the reasons for choosing Timescale as a time series database include its specialization in time series data, scalability, strong query support, data management policies, and collaboration with EMQX Cloud, making it an ideal choice for processing large-scale time series data in IIoT.

### Create a Timescale Cloud Instance

1. Login to Timescale Cloud and go to the Create Service page.

   ![Login to Timescale Cloud](https://assets.emqx.com/images/cf060c589fa325867db0fa73c98596c8.png)

1. On the Create Service page, choose a region from the region field's dropdown list. Click Create Service at the bottom of the page.

   ![Create Service page](https://assets.emqx.com/images/c8e0cd1e3e6a75049325bbfebf2a3601.png)

1. Once the service is created, you can connect to it as instructed on this page, or you can connect to your service by following these steps. Be sure to save your username and password.

   ![service is created](https://assets.emqx.com/images/b713f484dea04da82afd304b5bbdcbff.png)

1. Create a new table named temp_hum using the SQL statement below. This table will be used to store temperature and humidity data reported by devices.

   ```
   CREATE TABLE temp_hum (
   up_timestamp TIMESTAMPTZ NOT NULL,
   client_id TEXT NOT NULL,
   temp DOUBLE PRECISION NULL,
   hum DOUBLE PRECISION NULL
   );
   ```

   ```
   SELECT create_hypertable('temp_hum', 'up_timestamp');
   ```

   ![CREATE TABLE](https://assets.emqx.com/images/eca566fd919823e387623ed570a287fd.png)

1. Insert test data and view it.

   ```
   INSERT INTO temp_hum(up_timestamp, client_id, temp, hum) values (to_timestamp(1603963414), 'temp_hum-001', 19.1, 55);
   ```

   ```
   SELECT * FROM temp_hum;
   ```

   ![Insert test data](https://assets.emqx.com/images/27373a1516af6804642aaa6d402c4565.png)

Once connected to the service, you can go to the service overview page where you can find your connection information.

### Set Up Timescale Integration in EMQX Cloud

1. **Enable NAT Gateway**

   NAT Gateway provides the ability for EMQX Cloud Professional Edition deployments to access public network resources without the need for VPC peering connections. Before connecting to Timescale, please enable NAT Gateway.

   ![Enable NAT Gateway](https://assets.emqx.com/images/064abf5509b91e875c669cb61aa8b11d.png)

1. **Create resources**

   In the left menu, navigate to Data Integration and find the Timescale resource type.

   ![Create resources](https://assets.emqx.com/images/5f2c1ffa92bf84906447f54bcdb0b2af.png)

   Fill in the Timescale database information you created earlier. Set the connection pool size to 1 and click Test to test the connection.

   ![Create resources](https://assets.emqx.com/images/b14b2ae65629ebda608102eeadf75337.png)

   - If the connection fails, check whether the database configuration is correct.
   - If the connection succeeds, click "Create" to create the Timescale resource.

1. **Create rules**

   Under "Configured Resources," select the Timescale resource. Click "New Rule" and enter the following rule to match SQL statements. The SELECT part of the rule includes the following fields:

   - up_timestamp: Real-time timestamp of the message reported.
   - client_id: ID of the device sending the message.
   - Payload: The payload of the "temp_hum/emqx" topic message, including temperature and humidity data.

   ```
   SELECT
   timestamp div 1000 AS up_timestamp, clientid AS client_id, payload.temp AS temp, payload.hum AS hum
   FROM
   "temp_hum/emqx"
   ```

   ![New rule](https://assets.emqx.com/images/5db0635e76b38a156a7b4266ef007373.png)

   Enable SQL Testing, fill in the required fields, and click SQL Test to test if the rule is effective. You should get the expected results shown in the screenshot.

   ![Enable SQL Testing](https://assets.emqx.com/images/9e80ddbd6d6e4f48265cc9aec8200c79.png)

1. **Create Actions**

   Click the "Next" button at the bottom to create actions. Choose the resource created earlier from the drop-down list. In the SQL Template, enter the following data to insert them into the SQL template.

   ```
   INSERT INTO temp_hum(up_timestamp, client_id, temp, hum) VALUES (to_timestamp(${up_timestamp}), ${client_id}, ${temp}, ${hum});
   ```

   ![Create Actions](https://assets.emqx.com/images/9f6c255a9d640a4d9ed143c2cf2eddb1.png)

   Please verify that the information is accurate. Once confirmed, click on the 'Confirm' button located at the lower right corner to complete the configuration process for data integration. By following these steps, you can seamlessly configure Timescale integration, transform MQTT data into a structure that is suitable for the time series database, and ensure the transmission and storage of data is precise. This will allow you to easily analyze and query time series data with utmost convenience.

## In-Depth Data Analysis: Gaining Insights with Timescale

Once data has been successfully integrated into Timescale, the next step is to perform in-depth analysis of the data using query and visualization tools to gain insights into the performance and operational status of the IIoT (Industrial Internet of Things) system. Here are some key aspects of using Timescale for data analysis:

### Features of Timescale Query Language

Timescale's query language extends standard SQL to support the characteristics of time series data. This includes time window queries, data interpolation, data downsampling, and complex time series operations. Here are some key features:

- **Time Window Queries**: You can use time window functions to perform time-based operations such as sliding time window aggregation. This is useful for analyzing data trends over different time periods, such as hourly, daily, or monthly data trend analysis.
- **Data Interpolation**: Timescale supports interpolation functions that allow you to fill in missing time series data points. This is helpful for handling incomplete data sets and generating smooth curve charts.
- **Data Downsampling**: If your original data is very granular, you can use downsampling to reduce data volume for easier visualization and analysis. Downsampling can aggregate data into larger time intervals.
- **Complex Time Series Operations**: Timescale supports various complex time series operations such as cross-linking time series, performing mathematical calculations on time series, and applying window functions. These operations enable you to perform advanced analysis tasks.

### Create Simple Dashboards for Real-Time Monitoring

Dashboards are a powerful way to visualize analytical results. Using dashboards, you can:

1. **Monitor Key Metrics in Real-Time**: Display important metrics and data trends on the dashboard so engineers and operators can stay updated on system performance.

   ![Monitor Key Metrics in Real-Time](https://assets.emqx.com/images/a7662c5f91142a9e8e8328f7a299503a.png)

1. **Visualize Data**: Use visual tools such as charts, graphs, and maps to transform data into easily understandable visuals for identifying trends and anomalies.

   ![Visualize Data](https://assets.emqx.com/images/09c7a52957e5adfcc0248b722cbe6a69.png)

1. **Customize Dashboards**: Create custom dashboards based on specific needs to ensure that relevant data and metrics are highlighted.

   ![Customize Dashboards](https://assets.emqx.com/images/0b736170764f2b898ceaf84e74688151.png)

### Test and Verify Data Accuracy and Real-Time Updates

Data analysis includes not only queries and visualization but also verifying data accuracy and real-time updates. This is a critical part of ensuring the IIoT system is operating correctly. To test and verify data, you can:

1. **Compare with Original Data**: Compare query results with original data to ensure that the transformation and storage processes have not introduced any errors.

   ```
   SELECT * FROM temp_hum ORDER BY up_timestamp DESC LIMIT 10;
   ```

   ![Compare with Original Data](https://assets.emqx.com/images/8ac19c931740f8b57baaa11bc6b43641.png)

1. **Monitor Data Update Frequency**: Check whether data is updating at the expected frequency. If there are delays in data updates, it may require performance optimization or troubleshooting.
2. **Regular Data Verification**: Establish automated data verification processes to ensure data accuracy continuously. This includes writing test scripts to validate data integrity.

Through in-depth data analysis, dashboard monitoring, and data verification, you can gain valuable insights into the performance and operational status of the IIoT system, helping you make timely decisions and improve the system. The flexibility and powerful features of Timescale make it an ideal choice for processing large-scale time series data.

## Conclusion

As the IIoT continues to evolve, there is a need for a platform that can handle complex data flows, provide real-time data analysis, and integrate seamlessly with edge devices. EMQX Cloud, as a fully managed MQTT cloud service platform, offers these capabilities, ensuring a smooth and reliable flow of data from the edge to the cloud. By deploying NanoMQ on edge devices, connecting them to EMQX Cloud, and integrating with Timescale, you can achieve an end-to-end solution for handling large-scale time series data in the IIoT. 

[EMQX Cloud](https://www.emqx.com/en/cloud) is an essential component for industrial IoT solutions that require reliable data transmission and device management. Its integration with Timescale provides the ability to efficiently store and analyze time series data, enabling you to gain insights into your IIoT system's performance and operational status. With these tools and techniques, you can harness the power of the Industrial Internet of Things, improving automation, efficiency, and predictive maintenance in industrial settings.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
