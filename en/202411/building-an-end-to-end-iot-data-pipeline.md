> This guest blog is contributed by EMQX community.

## **Introduction**

The rise of the Internet of Things (IoT) has drastically transformed the way we interact with and leverage data from physical devices. As industries embrace IoT for various applications, from smart factories to real-time health monitoring, a significant challenge arises: how to efficiently gather, store, analyze, and visualize this massive influx of data in real-time. This blog delves into a real-world implementation of an IoT project utilizing several cutting-edge technologies to build a full data pipeline that ingests data from industrial devices, processes it at the edge, stores it efficiently, and visualizes analytics.

## **Overview of the System Architecture** 

![System Architecture](https://assets.emqx.com/images/451b2e1e01e5dbbc4370f62f3ea77124.png)

In this project, we have an interconnected architecture where data flows from industrial devices via OPC-UA into a real-time system. Below is a step-by-step breakdown of the components used and their roles:

1. **Node-RED for OPC-UA Integration**: Node-RED serves as the data extraction layer, pulling sensor data from OPC-UA servers (a machine-to-machine communication protocol for industrial automation). It offers a low-code environment for building IoT workflows, which simplifies the integration of devices without needing extensive coding.
2. **EMQX MQTT Broker for Data Transport**: The sensor data extracted from OPC-UA is sent to an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) using MQTT (Message Queuing Telemetry Transport), a lightweight protocol optimized for low-bandwidth, high-latency, or unreliable networks. EMQX, a highly scalable and distributed MQTT broker, is used to ensure that data from multiple sensors can be transmitted efficiently and reliably.
3. **Python for MQTT Client and Data Processing**: A Python program acts as an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools), subscribing to topics on the MQTT broker to read real-time sensor data. This program serves as the key processing layer that reads the raw data, performs some initial transformations, and stores it into QuestDB for historical storage and further analysis.
4. **QuestDB for Time-Series Storage**: QuestDB is the database used to store the sensor data. It is a high-performance time-series database specifically designed to handle real-time, time-stamped data. QuestDB's real-time nature ensures that IoT data is not only stored efficiently but can also be queried with low latency, making it ideal for real-time dashboards.
5. **Grafana for Real-Time Visualization**: Grafana, an open-source analytics and monitoring platform, connects to QuestDB to visualize the sensor data in real-time. This ensures that stakeholders can continuously monitor the condition of devices, observe trends, and track performance metrics with intuitive dashboards.
6. **Edge Analytics for On-Site Intelligence**: A significant portion of the project involves edge analytics, where the Python program performs real-time analysis of the data close to the source. By analyzing data at the edge, we reduce the need for sending all raw data to the cloud, decrease latency, and ensure immediate insights (e.g., anomaly detection or fault prediction).
7. **DuckDB for Aggregated Storage**: As part of the analytics pipeline, aggregated and processed data is stored in DuckDB, a fast, embeddable SQL database designed for analytics. DuckDB is excellent for handling large-scale, structured analytics workloads and offers a lightweight solution for storing edge-processed results.
8. **PowerBI for Business Intelligence**: Finally, the aggregated data from DuckDB is visualized using PowerBI, a powerful business intelligence tool that provides detailed reports and interactive dashboards. This aggregated data provides higher-level insights (such as monthly performance trends, device usage patterns, etc.) compared to the real-time views in Grafana.

## **Detailed Explanation of Components**

### **Node-RED and OPC-UA Integration**

Node-RED is an open-source flow-based development tool that simplifies the process of integrating IoT devices. It provides a graphical interface where users can design flows that connect various nodes representing devices, APIs, and services.

In this case, **OPC-UA** is a widely used communication protocol for data exchange in industrial automation. Node-RED’s OPC-UA node allows it to interface with industrial machines and sensors, extracting valuable operational data.

This data is then sent to an MQTT broker (EMQX) as the next step.

### **MQTT with EMQX Broker**

[**MQTT**](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a widely adopted protocol in IoT projects because of its efficiency in environments with constrained bandwidth and high latency. The protocol works on a publish-subscribe model, where devices (publishers) send data to specific topics, and consumers (subscribers) can subscribe to these topics to receive the data.

In this architecture, **EMQX** is the MQTT broker that handles communication between Node-RED (acting as a publisher) and a Python program (acting as a subscriber). This broker ensures secure, scalable, and fast data transmission from IoT devices to processing systems.

> For a comprehensive guide on using MQTT with Node-RED, please refer to: [MQTT with Node-RED: A Beginner's Guide with Examples](https://www.emqx.com/en/blog/using-node-red-to-process-mqtt-data)

### **Python for Data Processing**

The Python client subscribes to the MQTT topics and reads the data being streamed from the industrial devices. The main tasks of this Python program are:

- Parsing the incoming messages.
- Performing initial data processing, which can include data cleaning, normalization, or transformation.
- Forwarding the data to **QuestDB** for storage or performing immediate edge analytics.

### **QuestDB for Time-Series Data**

Time-series databases like **QuestDB** are optimized for storing data where time is a critical component, as is the case with IoT sensor data. QuestDB can handle massive amounts of high-frequency data, allowing for efficient storage and fast querying. This is essential for our real-time dashboards, which need immediate access to the latest data points to ensure accuracy in monitoring the state of devices.

### **Grafana for Visualization**

**Grafana** connects to QuestDB to create intuitive and real-time visual dashboards. This allows for real-time monitoring of device health, performance metrics, and sensor readings. Grafana’s flexibility with queries, along with its wide array of visualization options, makes it ideal for real-time IoT analytics.

### **Edge Analytics**

**Edge analytics** refers to performing analytics at or near the data source (the edge) rather than sending all data to a central cloud or server for analysis. This approach has several advantages:

- **Reduced Latency**: Since data is analyzed locally, insights can be generated instantly, allowing for real-time decision-making.
- **Bandwidth Optimization**: Instead of sending all raw data to the cloud, only valuable, pre-processed, or filtered data is transmitted, significantly reducing network congestion.
- **Enhanced Security**: Sensitive data can be analyzed locally, ensuring that only necessary data is transmitted, reducing the risk of exposure.

In our project, the Python program performs real-time analysis of data as soon as it arrives from the MQTT broker. Examples of edge analytics include anomaly detection (detecting out-of-range values), simple event-based rules (if temperature exceeds a threshold, trigger an alert), or summarization of data (e.g., calculating average values over a window of time).

### **DuckDB for Aggregated Analytics Storage**

**DuckDB** is a high-performance analytical SQL database designed to be embedded in analytics environments. Once edge analytics is completed, the summarized data (such as daily averages, trends, or key insights) is stored in DuckDB for further analysis.

DuckDB is lightweight and designed for complex analytics queries, making it ideal for handling aggregated IoT data on the edge before it is sent to more comprehensive reporting tools like PowerBI.

### **PowerBI for Business Intelligence**

Finally, **PowerBI** is used for visualizing the aggregated data stored in DuckDB. While Grafana focuses on real-time, operational monitoring, PowerBI is used for business-level insights such as:

- Aggregated trends over time.
- Detailed usage reports.
- Performance comparisons across devices or periods.

By connecting PowerBI to DuckDB, we create rich, interactive dashboards and reports that provide deeper insights to decision-makers.

## **Conclusion**

In this project, we built an efficient, real-time IoT pipeline that integrates a range of technologies, from **Node-RED** for device data extraction, **EMQX** as the MQTT broker, **Python** for processing, **QuestDB** for real-time data storage, **Grafana** for visualization, **DuckDB** for analytics storage, and finally **PowerBI** for business intelligence reporting.

The use of **edge analytics** ensures that data processing happens close to the source, reducing latency and improving the system's responsiveness, while **IoT analytics** provides deeper insights and better decision-making capabilities by analyzing both real-time and historical data. By leveraging this architecture, industries can streamline their IoT workflows and gain powerful insights from their devices, driving efficiency and innovation.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
