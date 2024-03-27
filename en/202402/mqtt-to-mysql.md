## What is MySQL?

MySQL is an open-source relational database management system (RDBMS) that provides reliable, high-performance data storage and retrieval solutions. It is widely used in various scale applications and websites. MySQL supports standard SQL, allowing developers to use familiar syntax for data querying, insertion, updating, and deletion operations. It also offers rich features such as transaction processing, replication, and high availability options to ensure data consistency and reliability. Whether it's a small project or a large enterprise-level application, MySQL provides stable, high-performance data storage and processing capabilities.

## The Role of MySQL in IoT

MySQL boasts distinctive advantages in the realm of IoT:

- **Structured Data Storage:** MySQL stores data in the table, necessitating a predefined table structure and field data types. This structured approach ensures data consistency and integrity.
- **Powerful Query Language:** With support for standard SQL queries, MySQL provides robust operations such as filtering, sorting, joining, and aggregating.
- **Scalability and Availability:** Leveraging features like master-slave replication and sharding, MySQL enables high availability and horizontal scaling of data.
- **Transaction Processing:** Supporting ACID transactions, MySQL ensures data consistency and reliability amid concurrent operations and system failures.

While MySQL excels in handling large-scale structured data and intricate queries, its structured data storage and powerful query language may not be optimal for telemetry data. Telemetry data, often classified as unstructured, demands high-speed write throughput and long-term storage capabilities. 

In IoT applications, MySQL finds its niche in storing device metadata, event data, and a limited amount of telemetry data, such as device configuration, online/offline status, and current sensor readings. Managing these data is crucial for operational administration across the entire application, supporting both overall functionality and specific application scenarios.

## Integrating MySQL with MQTT

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is an OASIS standard messaging protocol for the IoT. It is designed with an extremely lightweight publish/subscribe messaging model, making it ideal for connecting IoT devices with a small code footprint and minimal network bandwidth and exchanging data in real-time between connected devices and cloud services.

Integrating MySQL with MQTT enables efficient data exchange and management in IoT and real-time applications. Developers can build robust IoT solutions where sensor data, user information, or application logs can be stored, retrieved, and processed efficiently. This integration allows for real-time data synchronization, analytics, and decision-making, enhancing the overall functionality and performance of IoT systems.

Here are some common use cases for integrating MySQL with MQTT:

- **IoT Data Management**: One of the primary uses of MySQL and MQTT integration is in managing IoT data. MQTT can be used to collect real-time data from sensors, devices, or applications, while MySQL stores this data in a structured format. This integration allows for efficient data storage, retrieval, and analysis, enabling businesses to gain valuable insights from IoT devices.
- **Real-time Monitoring and Alerts**: By integrating MySQL with MQTT, organizations can set up real-time monitoring systems that track various metrics and trigger alerts based on predefined thresholds. For example, in a manufacturing environment, MQTT can gather machine data, which is then stored in MySQL. Thresholds for machine performance can be set in MySQL, and when these thresholds are exceeded, MQTT can send alerts to relevant stakeholders.
- **User Activity Logging**: MySQL and MQTT integration can be used to log user activity in real time. For instance, in a web application, MQTT can capture user actions such as logins, clicks, or transactions, which are then stored in MySQL for auditing, analysis, and security purposes.
- **Remote Device Management**: Integrating MySQL with MQTT is beneficial for remote device management scenarios. MQTT can be used to send commands or configurations to remote devices, and MySQL can store information about device status, settings, and historical data. This setup enables centralized control and monitoring of distributed devices.

## Demo: Building a Real-Time Data Monitoring Application with MySQL and MQTT

Next, we will guide you through the process of using EMQX to collect sensor data from oil pipelines and integrate it with MySQL for real-time data storage and analysis.

### Prerequisites

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

### How it Works

This is a simple and effective architecture that utilizes the following key components:

| Component Name                                           | Version | Description                                                  |
| :------------------------------------------------------- | :------ | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+  | A command line tool for testing data generation.             |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.0.4+  | An MQTT broker used for message exchange between pipelines and MySQL. |
| [MySQL](https://www.mysql.com/)                          | 4.4.6+  | A database for storing and managing oil production data, as well as providing time aggregation and analysis capabilities for Grafana. |
| [Grafana](https://grafana.com/)                          | 9.5.1+  | A visualization platform for displaying and analyzing collected data. |

### Clone the Project Locally

Clone the [emqx/mqtt-to-mysql](https://github.com/emqx/mqtt-to-mysql) repository locally using Git:

```
git clone https://github.com/emqx/mqtt-to-mysql
cd mqtt-to-mysql
```

The codebase consists of four parts:

- The `emqx` folder contains EMQX-MySQL integration configurations to automatically create rules and data bridges when launching EMQX.
- The `mqttx` folder offers a script to simulate oil pipeline sensors connected to the EMQX and generating data.
- The `prometheus` and `grafana-provisioning` folders contain configurations for visualizing energy consumption data.
- The `docker-compose.yml` orchestrates all components to launch the project with one click.

### Start MQTTX CLI, EMQX, and MySQL

Please make sure you have installed the [Docker](https://www.docker.com/), and then run Docker Compose in the background to start the demo:

```
docker-compose up -d
```

The MQTTX CLI will simulate ten groups of sensor devices within EMQX. These devices will periodically publish real-time data, including oil pressure, casing pressure, back pressure, wellhead temperature, production, etc., from the pipeline to a designated topic. The transmitted data is formatted in JSON and sent to the topic `mqttx/simulate/oil-extraction/{clientid}`.

This is an example of data published to EMQX:

```
{
    "oilPressure": 1375829.01,
    "casingPressure": 429647.68,
    "backPressure": 142174.65,
    "wellheadTemperature": 75.03,
    "voltage": 360.84,
    "current": 29.4,
    "flowRate": 127.8,
    "id": "2eb9b000-c6a1-4af1-92c0-6e3026e2db92",
    "name": "oil_well_0"
}
```

### Store Oil Pipeline Data

EMQX will create a rule to receive messages from each sensor. You can also modify this rule later to add custom processing using EMQX's [built-in SQL functions](https://docs.emqx.com/en/enterprise/v5.4/data-integration/rule-sql-builtin-functions.html):

```
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

Once the rules have processed the data, EMQX will utilize rule actions to write the sensor data from the oil pipeline, present in the message payload, to the `oil_well_data` table within MySQL's `iot_data` database.

The EMQX MySQL data integration allows the insertion of data through SQL templates. This facilitates the effortless writing or updating of specific field data into corresponding tables and columns within the MySQL database. Such integration ensures flexible storage and management of data:

```
INSERT INTO oil_well_data
  (
    oil_well_id,
    NAME,
    oilpressure,
    casingpressure,
    backpressure,
    wellheadtemperature,
    voltage,
    CURRENT,
    flowrate
  )
  VALUES
  (
    ${payload.id},
    ${payload.name},
    ${payload.oilPressure},
    ${payload.casingPressure},
    ${payload.backPressure},
    ${payload.wellheadTemperature},
    ${payload.voltage},
    ${payload.current},
    ${payload.flowRate}
  )
```

### Log Events from Acquisition Devices

Additionally, EMQX will create a rule to log the online and offline statuses of the acquisition devices connected to EMQX. This logging serves the purposes of device management and fault warning. If a device unexpectedly goes offline, immediate notification allows for prompt issue identification and resolution.

EMQX's rule engine extends support to the full MQTT device lifecycle event handling. For a comprehensive understanding and monitoring of various events through the rule engine, you can also refer [here](https://docs.emqx.com/en/enterprise/v5.4/data-integration/rule-sql-events-and-fields.html#mqtt-events).

```
SELECT
  *
FROM
  "$events/client_connected",  "$events/client_disconnected"
```

Upon successful connection or disconnection of a device, EMQX activates the rule and records the event in the `oil_well_events` table within MySQL's `iot_data` database.

The recorded information encompasses the event name and client ID, with the event time being automatically generated by MySQL:

```
INSERT INTO oil_well_events(event, clientid) VALUES(${event}, ${clientid})
```

### Subscribe to Data from EMQX

Docker Compose has included a subscriber to print all vehicle data. You can view the data with this command:

```
$ docker logs -f mqttx
[1/12/2024] [10:15:57 AM] › topic: mqttx/simulate/oil-extraction/mqttx_4f113a38
payload: "oilPressure":1375829.01,"casingPressure":429647.68,"backPressure":142174.65,"wellheadTemperature":75.03,"voltage":360.84,"current":29.4,"flowRate":127.8,"id":"2eb9b000-c6a1-4af1-92c0-6e3026e2db92","name":"oil_well_0"}
```

To subscribe and receive the data with any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools):

```
mqttx sub -t mqttx/simulate/oil-extraction/+
```

### View Pipeline Data through Grafana

To access pipeline data on the Grafana dashboard, navigate to `http://localhost:3000` in your browser and log in using the credentials `admin` (username) and `public` (password).

After logging in, visit the Home → Dashboards page and choose the Oil Extraction dashboard. This dashboard provides a comprehensive overview of your oil pipeline, featuring real-time metrics such as current oil pressure, casing pressure, back pressure, wellhead temperature, and more. Additionally, it displays trends in these metrics over time. The visualization of these key metrics facilitates visual monitoring of the production status, enabling the prompt identification of any potential anomalies or issues.

## Conclusion

In this blog, we delve into the integration of MQTT and MySQL to construct a comprehensive real time data monitoring application. By utilizing EMQX as a real-time [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and seamlessly importing data into MySQL, we can enhance operational efficiency, minimize downtime, and bolster safety through data-driven analytics and proactive maintenance of production lines.

EMQ offers a complete solution that includes data acquisition, edge computing, cloud access, and AI technology for the oil and gas industry. It integrates data from wells, edge gateways, and cloud applications into a unified platform. This enables various scenarios such as production monitoring, maintenance, safety and environmental oversight, and asset tracking, further accelerating the digital transformation and advancement of the industry.

For detailed information, please refer to [MQTT Platform for Oil & Gas Industry](https://www.emqx.com/en/solutions/industries/oil-gas).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
