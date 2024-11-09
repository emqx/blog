>This guest blog is contributed by RisingWave.

## Overview

Real-time data processing is crucial in the Industrial Internet of Things (IIoT) space, where timely insights can drive significant operational improvements. By leveraging platforms like EMQX for various industrial data streaming and RisingWave for real-time analytics, manufacturers can process and analyze data from machines as it's generated, enabling predictive maintenance, reducing downtime, and improving efficiency. The integration of these technologies can empower industries to respond instantly to equipment failures, optimize production, and make data-driven decisions that enhance overall equipment effectiveness (OEE) and streamline operations across the board.

This blog will outline the integration of EMQX with RisingWave, creating a robust system designed for real-time monitoring and predictive maintenance within the IIoT framework.

## The Technical Stack

### EMQ and EMQX

[EMQ](https://www.emqx.com/en) is a global leader in providing edge-cloud connectivity and data platform solutions. EMQ facilitates data collection, transmission, transformation, storage, analysis, and control between the physical devices and digital systems with its high-performance MQTT messaging platform EMQX and other software solutions. 

EMQ helps businesses tackle data challenges across various scenarios, such as connected vehicles, smart factories, smart buildings, retail, robotics, drones, maritime shipping, and large-scale distributed energy device networks (including renewable energy grids, distributed energy storage, transmission and distribution power grid, gas and water networks).

EMQX is a scalable, distributed MQTT platform that supports unlimited connections, offers seamless integration, and can be deployed anywhere. It can seamlessly integrate IoT data with various backend databases and analytics tools, enabling enterprises to build IoT platforms and applications with leading competitiveness rapidly.

### RisingWave

[RisingWave](https://risingwave.com/) is an SQL-based platform for event-driven workloads, designed to handle large volumes of real-time data efficiently. It offers robust connectors for various data systems, Postgres compatibility, and delivers low-latency results using real-time materialized views. With simple scaling and seamless integration, it is ideal for use cases such as predictive maintenance, quality control, supply chain optimization, energy management, and production line optimization.

### Integration of EMQX, RisingWave, and Grafana

In this blog post, we develop a real-time monitoring, predictive maintenance, and anomaly detection system for PBL86-80 motors used in robotic solutions in manufacturing. This system collects data from the motors on a factory-floor, sends it to an EMQX broker running in EMQX Platform and ingests it into RisingWave for advanced real-time analytics for monitoring, predictive maintenance and anomaly detection. Then, Grafana is used to create charts and real-time dashboard that monitors the factory shop floor.

![Overview of the technical stack](https://assets.emqx.com/images/d6e7c95e10a450d6b36713fdad6bc909.png)

<center>Overview of the technical stack</center>

## Set up EMQX to Ingest Real-Time Machine Data from Shop-Floor

This section goes through the steps to create an EMQX broker on the EMQX Platform and connect it to RisingWave for data ingestion. For more information regarding the data ingestion from EMQX, please refer to [EMQX documentation](https://docs.emqx.com/en/).

### **Sign up for an EMQX Platform Account**

Begin by signing up for [EMQX Platform Cloud Deployment](https://accounts.emqx.com/signup?continue=https%3A%2F%2Fwww.emqx.com%2Fcn%2Fcloud) account with 14-day free-trial, which provides access to EMQX services.

![Sign up for EMQX Cloud](https://assets.emqx.com/images/cd5e9fbc91eecdd2fdee850087d0412e.png)

 <center>Sign up for EMQX Cloud</center>

### Create a New Deployment

Log in to you account, and on the start page, click **New Deployment** to go to the New Deployment page.

![Create a new deployment](https://assets.emqx.com/images/f81679f6c02ee10908c730b45e8da53b.png)

<center>Create a new deployment</center>

<br>

Select the **Serverless** plan, which provides a free EMQX broker, leave all the deployment settings at their default values, and click **Deploy** to get started with the broker.

![Deploy a serverless EMQX broker](https://assets.emqx.com/images/5125beab117cc09be3b7aabe056482d1.png)

<center>Deploy a serverless EMQX broker</center>

<br>

After you deploy the serverless EMQX broker, it is ready to use.

![Serverless EMQX Cloud deployment](https://assets.emqx.com/images/8615f3822def2b190f9425db3c72c6b3.png)

<center>Serverless EMQX Cloud deployment</center>

<br>

This is an overview of the EMQX Serverless deployment, showing its status, connection information, and deployment API key.

![Overview of the EMQX Serverless deployment](https://assets.emqx.com/images/ac49f3e4035cd818c7c62e717fd9b6bd.png)

<center>Overview of the EMQX Serverless deployment</center>

### **Configure Authentication and Authorization**

Add authentication information before connecting any clients or applications to ensure your data is secure. You can do so by navigating to the deployment's **Access Control** -> **Authentication** page.

![Add username and password for authentication](https://assets.emqx.com/images/0e1629254bdc0e4f9844f73a67945486.png)

<center>Add username and password for authentication</center>

<br>

Then go to the Authorization page to grant permission to publish and subscribe to a topic.

![Add authorization details](https://assets.emqx.com/images/17f58386a1019ed68079f016cc7d04a9.png)

<center>Add authorization details</center>

<br>

We are now ready to ingest shop-floor data from the factory floor into the EMQX broker using the Paho Python client.

Here is a sample of the shop-floor data for electric motors in JSON format:

```json
{
  "machine_id": "machine_1",
  "winding_temperature": 80,
  "ambient_temperature": 40,
  "vibration_level": 1.97,
  "current_draw": 14.43,
  "voltage_level": 50.37,
  "nominal_speed": 4207.69,
  "power_consumption": 646.32,
  "efficiency": 82.88,
  "ts": "2024-09-09 09:57:51"
}
```

## **Ingest Data from EMQX into RisingWave**

We’ll use RisingWave to ingest and analyze the events from EMQX. In this blog, we use RisingWave Cloud, which provides a user-friendly experience and simplifies the operational aspects of managing and utilizing RisingWave for our real-time monitoring and predictive maintenance system.

### Create a RisingWave Cluster

To create a RisingWave cluster in [RisingWave Cloud](https://cloud.risingwave.com/) and explore the various features it offers, you can sign up for the free plan available. The free plan allows you to test the functionalities of RisingWave without any cost. For detailed instructions on how to create a RisingWave cluster and get started, you can refer to the [official RisingWave documentation](https://docs.risingwave.com/docs/current/intro/). It will provide you with step-by-step guidance on setting up and exploring the features of RisingWave. If you need additional help with setting up this integration, join our active [Slack community](https://www.risingwave.com/slack).

### Create a Source

Once you have deployed the RisingWave cluster, create a source in the [Workspace](https://docs.risingwave.com/cloud/console-overview/) using the following SQL query:

```sqlite
CREATE TABLE shop_floor_machine_data (
    machine_id VARCHAR,
    winding_temperature INT,
    ambient_temperature INT,
    vibration_level FLOAT,
    current_draw FLOAT,
    voltage_level FLOAT,
    nominal_speed FLOAT, 
    power_consumption FLOAT,
    efficiency FLOAT,
    ts TIMESTAMP
)
WITH (
    connector='mqtt',
    url='ssl://xxxxxxxxx.us-east-1.emqxsl.com:8883',
    topic= 'factory/machine_data',
    username='xxxxxx',
    password='xxxxxx',
    qos = 'at_least_once',
) FORMAT PLAIN ENCODE JSON;
```

### Create Materialized Views for Data Analysis in RisingWave

We create a set of materialized views in RisingWave based on the `shop_floor_machine_data` source table to facilitate monitoring, predictive maintenance, and anomaly detection. In RisingWave, materialized views are automatically and incrementally updated with each new event, ensuring minimal computing overhead. The RisingWave engine continuously monitors for relevant events from the source after the materialized view is created.

#### **Materialized View for Machine Metrics Aggregation**

This query creates a materialized view `monitoring_mv` that provides one-minute aggregated metrics for each machine on the shop floor. It calculates the average values for winding temperature, ambient temperature, vibration level, current draw, voltage level, nominal speed, power consumption, and efficiency, grouped by machine ID and time windows (window start and window end).

```sql
CREATE MATERIALIZED VIEW monitoring_mv AS 
SELECT
    machine_id,
    AVG(winding_temperature) AS avg_winding_temperature,
    AVG(ambient_temperature) AS avg_ambient_temperature,
    AVG(vibration_level) AS avg_vibration_level,
    AVG(current_draw) AS avg_current_draw,
    AVG(voltage_level) AS avg_voltage_level,
    AVG(nominal_speed) AS avg_nominal_speed,
    AVG(power_consumption) AS avg_power_consumption,
    AVG(efficiency) AS avg_efficiency,
    window_start, 
    window_end
FROM TUMBLE (shop_floor_machine_data,ts, INTERVAL '1 MINUTE')
GROUP BY machine_id, window_start,window_end;  
```

#### **Materialized View for Maintenance Alerts Based on Recent Machine Metrics**

This query creates a materialized view named `maintenance_mv` that combines recent and historical averages for machine metrics, such as winding temperature, vibration level, current draw, power consumption, and efficiency. It generates alerts for potential maintenance issues by comparing recent statistics against historical averages, flagging conditions like overheating, increased vibration, overcurrent, or efficiency drops. The results are ordered by the end of the time window for easy monitoring.

```sql
CREATE MATERIALIZED VIEW maintenance_mv AS 
WITH Historical_Averages AS (
    SELECT
        machine_id,
        AVG(winding_temperature) AS avg_winding_temp,
        AVG(vibration_level) AS avg_vibration,
        AVG(current_draw) AS avg_current_draw,
        AVG(power_consumption) AS avg_power_consumption,
        AVG(efficiency) AS avg_efficiency
    FROM shop_floor_machine_data
    WHERE ts < NOW() - INTERVAL '1' HOUR  -- Historical data for the last 1 hour 
    GROUP BY machine_id
),
Recent_Stats AS (
    SELECT
        machine_id,
        COUNT(*) AS event_count,
        window_start,
        window_end,
        AVG(winding_temperature) AS avg_winding_temp,
        AVG(vibration_level) AS avg_vibration,
        AVG(current_draw) AS avg_current_draw,
        AVG(power_consumption) AS avg_power_consumption,
        AVG(efficiency) AS avg_efficiency
    FROM TUMBLE (shop_floor_machine_data,ts, INTERVAL '1 MINUTES')
    GROUP BY machine_id, window_start,window_end
)
SELECT
    r.machine_id,
    r.window_start,
    r.window_end,
    r.avg_winding_temp,
    r.avg_vibration,
    r.avg_current_draw,
    r.avg_power_consumption,
    r.avg_efficiency,
    CASE
        WHEN r.avg_winding_temp > h.avg_winding_temp + 5 THEN 'Potential Overheating'
        WHEN r.avg_vibration > h.avg_vibration + 0.1 THEN 'Increased Vibration'
        WHEN r.avg_current_draw > h.avg_current_draw + 2 THEN 'Possible overcurrent condition'
        WHEN r.avg_efficiency < h.avg_efficiency - 5 THEN 'Efficiency Drop'
        ELSE 'Normal'
    END AS maintenance_alert
FROM
    Recent_Stats r
JOIN
    Historical_Averages h
ON
    r.machine_id = h.machine_id
WHERE
    r.avg_winding_temp > h.avg_winding_temp + 5 OR
    r.avg_vibration > h.avg_vibration + 0.1 OR
    r.avg_current_draw > h.avg_current_draw + 2 OR
    r.avg_efficiency < h.avg_efficiency - 5
ORDER BY
    r.window_end DESC;
```

#### **Materialized View for Anomaly Detection in Machine Metrics**

This query creates a materialized view named `anomalies_mv` that identifies anomalies in machine metrics by analyzing recent data. It computes average values, standard deviations, and maximums for metrics such as winding temperature, vibration level, current draw, voltage level, and power consumption over one-minute intervals. By comparing current metrics with historical data, it generates alerts for significant deviations and rising trends, filtering the results to highlight only notable anomalies and ordering them by the time window's end.

```sql
CREATE MATERIALIZED VIEW anomalies_mv AS
WITH Anomaly_Metrics AS (
    SELECT
        machine_id,
        window_start,
        window_end,
        AVG(winding_temperature) AS avg_winding_temp,
        AVG(vibration_level) AS avg_vibration,
        AVG(current_draw) AS avg_current_draw,
        AVG(voltage_level) AS avg_voltage_level,
        AVG(power_consumption) AS avg_power_consumption,
        STDDEV_POP(winding_temperature) AS stddev_winding_temp,
        STDDEV_POP(vibration_level) AS stddev_vibration,
        STDDEV_POP(current_draw) AS stddev_current_draw,
        STDDEV_POP(voltage_level) AS stddev_voltage_level,
        STDDEV_POP(power_consumption) AS stddev_power_consumption,
        MAX(winding_temperature) AS max_winding_temp,
        MAX(vibration_level) AS max_vibration,
        MAX(current_draw) AS max_current_draw,
        MAX(voltage_level) AS max_voltage_level,
        MAX(power_consumption) AS max_power_consumption
    FROM TUMBLE (shop_floor_machine_data,ts, INTERVAL '1 MINUTES')
    GROUP BY machine_id, window_start,window_end
),
Trend_Analysis AS (
    SELECT
        machine_id,
        window_start,
        window_end,
        avg_winding_temp,
        avg_vibration,
        avg_current_draw,
        avg_voltage_level,
        avg_power_consumption,
        stddev_winding_temp,
        stddev_vibration,
        stddev_current_draw,
        stddev_voltage_level,
        stddev_power_consumption,
        max_winding_temp,
        max_vibration,
        max_current_draw,
        max_voltage_level,
        max_power_consumption,
        LAG(avg_winding_temp, 1) OVER (PARTITION BY machine_id ORDER BY window_end) AS prev_avg_winding_temp,
        LAG(avg_vibration, 1) OVER (PARTITION BY machine_id ORDER BY window_end) AS prev_avg_vibration,
        LAG(avg_current_draw, 1) OVER (PARTITION BY machine_id ORDER BY window_end) AS prev_avg_current_draw,
        LAG(avg_voltage_level, 1) OVER (PARTITION BY machine_id ORDER BY window_end) AS prev_avg_voltage_level,
        LAG(avg_power_consumption, 1) OVER (PARTITION BY machine_id ORDER BY window_end) AS prev_avg_power_consumption
    FROM Anomaly_Metrics
)
SELECT
    machine_id,
    window_start,
    window_end,
    avg_winding_temp,
    avg_vibration,
    avg_current_draw,
    avg_voltage_level,
    avg_power_consumption,
    stddev_winding_temp,
    stddev_vibration,
    stddev_current_draw,
    stddev_voltage_level,
    stddev_power_consumption,
    max_winding_temp,
    max_vibration,
    max_current_draw,
    max_voltage_level,
    max_power_consumption,
    CASE
        WHEN max_winding_temp > avg_winding_temp + 3 * stddev_winding_temp THEN 'Anomalous Winding Temperature'
        WHEN max_vibration > avg_vibration + 3 * stddev_vibration THEN 'Anomalous Vibration Level'
        WHEN max_current_draw > avg_current_draw + 3 * stddev_current_draw THEN 'Anomalous Current Draw'
        WHEN max_voltage_level > avg_voltage_level + 3 * stddev_voltage_level THEN 'Anomalous Voltage Level'
        WHEN max_power_consumption > avg_power_consumption + 3 * stddev_power_consumption THEN 'Anomalous Power Consumption'
        WHEN (avg_winding_temp - prev_avg_winding_temp) > 2 * stddev_winding_temp THEN 'Rising Winding Temperature'
        WHEN (avg_vibration - prev_avg_vibration) > 2 * stddev_vibration THEN 'Increasing Vibration'
        WHEN (avg_current_draw - prev_avg_current_draw) > 2 * stddev_current_draw THEN 'Rising Current Draw'
        WHEN (avg_voltage_level - prev_avg_voltage_level) > 2 * stddev_voltage_level THEN 'Rising Voltage Level'
        WHEN (avg_power_consumption - prev_avg_power_consumption) > 2 * stddev_power_consumption THEN 'Rising Power Consumption'
        ELSE 'Normal'
    END AS anomaly_alert
FROM Trend_Analysis
WHERE
    max_winding_temp > avg_winding_temp + 3 * stddev_winding_temp OR
    max_vibration > avg_vibration + 3 * stddev_vibration OR
    max_current_draw > avg_current_draw + 3 * stddev_current_draw OR
    max_voltage_level > avg_voltage_level + 3 * stddev_voltage_level OR
    max_power_consumption > avg_power_consumption + 3 * stddev_power_consumption OR
    (avg_winding_temp - prev_avg_winding_temp) > 2 * stddev_winding_temp OR
    (avg_vibration - prev_avg_vibration) > 2 * stddev_vibration OR
    (avg_current_draw - prev_avg_current_draw) > 2 * stddev_current_draw OR
    (avg_voltage_level - prev_avg_voltage_level) > 2 * stddev_voltage_level OR
    (avg_power_consumption - prev_avg_power_consumption) > 2 * stddev_power_consumption
ORDER BY
    window_end DESC;
```

## Send the Data from RisingWave to Apache Grafana for Visualization

We’ll configure Grafana to read data from RisingWave and build visualizations.

### Connect RisingWave to Grafana

To utilize RisingWave as a data source in Grafana and create visualizations and dashboards, follow the instructions provided in [Configure Grafana to read data from RisingWave](https://docs.risingwave.com/docs/current/grafana-integration/).

Once the connection between RisingWave and Grafana is established, you can incorporate materialized views from RisingWave as tables to design charts and build a comprehensive dashboard.

### Visualize Data with Grafana: Table, Charts, and Dashboards

This table is generated from the previously created `shop_floor_machine_data` table, which stores sensor readings and operational metrics from machines on the shop floor. Each record represents a machine's performance at a specific point in time.

![table](https://assets.emqx.com/images/409939ff79c9680e9ef706f34c63c8c6.png)

This chart is generated from the `anomalies_mv` materialized view, which displays alerts like "Anomalous Vibration Level" or "Rising Power Consumption" triggered when deviations exceed predefined thresholds. These alerts highlight unusual machine behavior, enabling real-time monitoring and predictive maintenance.

![image.png](https://assets.emqx.com/images/374f53dedd55e9eaf9473c4db30af926.png)

This chart is based on the `maintenance_mv` materialized view, which tracks real-time machine performance metrics and compares them against historical averages to detect potential maintenance issues. When specific thresholds are exceeded — such as a winding temperature increase of more than 5 degrees or an efficiency drop of over 5% — the system triggers alerts like "Potential Overheating" or "Efficiency Drop." This enables proactive maintenance, helping prevent equipment failures.

![image.png](https://assets.emqx.com/images/f2eb99a27073910559957b6759e275ec.png)

This chart is based on the `shop_floor_machine_data` table and displays the winding temperatures of the machines on the shop floor. If the winding temperature exceeds the threshold of 81°C, the corresponding data points are highlighted in red to indicate a potential issue.

![image.png](https://assets.emqx.com/images/0cdc4377cc4272c28c3c8056b8dd4004.png)

This chart is based on the `shop_floor_machine_data` table and illustrates the vibration levels of the machines on the shop floor. If the vibration level exceeds the threshold of 2.05, it indicates potential mechanical issues that may require attention.

![image.png](https://assets.emqx.com/images/9bb61f6802d65336ee5fcc32cafe04c3.png)

This pie chart, generated using data from the shop_floor_machine_data table, represents the distribution of ambient temperatures across the factory floor.

![image.png](https://assets.emqx.com/images/51e57fa2d0068f239745de37578dc11f.png)

This bar chart is generated using data from the `shop_floor_machine_data` table and displays the nominal speed and power consumption of the machines. A red line is included to indicate the threshold of 4210, serving as a reference point for comparison.

![image.png](https://assets.emqx.com/images/45c04c2bf56aa275382e685b156e0065.png)

This chart is based on the `shop_floor_machine_data` table and displays the efficiency of all the machines. If the efficiency drops below the threshold of 80, the affected data points are highlighted in red to indicate suboptimal performance.

![image.png](https://assets.emqx.com/images/fcfb806ab19389a573eb37e52315b3e1.png)

This is a real-time unified dashboard that monitors the factory shop floor, providing a comprehensive view of operational performance. It displays alerts related to predictive maintenance and anomaly detection, enabling quick identification of potential issues and facilitating proactive management of equipment health.

![image.png](https://assets.emqx.com/images/3be77a2a0612df3c445f7bd16832a5d5.png)

## Conclusion

In this blog, we explored a real-time monitoring and predictive maintenance system for PBL86-80 motors in manufacturing. The system collects motor data, sends it to EMQX, and processes it in RisingWave for real-time analytics, enabling monitoring, predictive maintenance, and anomaly detection. Grafana visualizes the data through real-time dashboards.

We demonstrated how EMQX and RisingWave form a perfect combination for anomaly detection, predictive maintenance, and real-time monitoring in IIoT and manufacturing scenarios. We encourage users to explore both platforms to build scalable, cost-effective solutions for their diverse IIoT use cases.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
