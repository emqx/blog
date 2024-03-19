## What is Timescale?

Timescale is a robust and versatile database solution tailored specifically for managing time-series data, offering scalability, performance, and advanced analytical capabilities to meet the demands of modern data-intensive applications.

Developed as an extension of PostgreSQL, Timescale combines the reliability and familiarity of PostgreSQL with enhanced capabilities for managing time-stamped data. It excels in managing data that is timestamped or sequenced in chronological order, making it ideal for applications such as IoT (Internet of Things) devices, financial data analysis, monitoring systems, and more. Its architecture is optimized for time-series workloads, offering features like automatic data partitioning based on time intervals, native time-based indexing, and advanced compression techniques to reduce storage requirements.

## The Power of MQTT with Timescale in IoT

Combining the power of [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) with Timescale in IoT environments unleashes a formidable synergy that revolutionizes data handling and analytics. 

As a lightweight messaging protocol ideal for IoT devices due to its low bandwidth and resource requirements, MQTT facilitates seamless communication between sensors, actuators, and backend systems. By integrating MQTT with Timescale, IoT applications gain the ability to efficiently store, manage, and analyze massive volumes of time-stamped data. Timescale's partitioning capabilities based on time intervals ensure optimal data organization, while its advanced compression techniques minimize storage overhead. This combination not only enhances data scalability and reliability but also empowers IoT systems with real-time analytics, trend analysis, predictive maintenance, and actionable insights, driving innovation and efficiency in IoT deployments across industries.

Here are some use cases where integrating MQTT with Timescale can be highly beneficial:

- **Smart Agriculture Monitoring**: MQTT facilitates real-time communication between soil sensors, weather stations, and irrigation systems in agriculture. Timescale can store and analyze this data, enabling farmers to make data-driven decisions regarding watering schedules, fertilizer usage, and crop health monitoring.
- **IIoT Predictive Maintenance**: Combining MQTT messages from industrial equipment (such as pumps, motors, and turbines) with Timescale allows for the creation of predictive maintenance models. By analyzing historical data trends, anomalies, and sensor readings, maintenance teams can preemptively identify and address potential equipment failures, reducing downtime and operational costs.
- **Energy Management and Monitoring**: MQTT can collect data from smart meters, solar panels, and energy storage systems in real time. Integrating this data with Timescale enables energy providers and consumers to monitor energy consumption patterns, optimize energy usage, and forecast demand more accurately, leading to improved efficiency and cost savings.

## A Quick Demo: An IoT Time-Series Data Application with MQTT and Timescale

### Prerequisites

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

### How it Works

![MQTT to Timescale](https://assets.emqx.com/images/b9dccfd771d8dc7b5ba8aecb3ac12808.png)

This is a simple and effective architecture that avoids complex components. It utilizes the following three key components:

| Component Name                                           | Version      | Description                                                  |
| :------------------------------------------------------- | :----------- | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+       | A command line tool is leveraged to generate factory energy consumption data. |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.0.4+       | MQTT broker used for message exchange between factory and the Timescale. |
| [Timescale](https://www.timescale.com/)                  | latest-pg12+ | Used for IIoT data storage and management, as well as providing time aggregation and analysis capabilities for Grafana. |
| [Grafana](https://grafana.com/)                          | 9.5.1+       | Visualization platform utilized to display and analyze the collected data. |

In addition to the basic components, EMQX provides comprehensive observability capabilities. You can use the following components to monitor EMQX metrics and load when the system is running:

| Component Name                                         | Version | Description                                          |
| ------------------------------------------------------ | ------- | ---------------------------------------------------- |
| [EMQX Exporter](https://github.com/emqx/emqx-exporter) | 0.1     | Prometheus exporter for EMQX                         |
| [Prometheus](https://prometheus.io/)                   | v2.44.0 | Open-source systems monitoring and alerting toolkit. |

### Clone the Project Locally

Clone the [emqx/mqtt-to-timescaledb](https://github.com/emqx/mqtt-to-timescaledb) repository locally, and initialize the submodule to enable the EMQX Exporter (optional):

```shell
git clone https://github.com/emqx/mqtt-to-timescaledb
cd mqtt-to-timescaledb

# Optional
git submodule init
git submodule update
```

The codebase consists of four parts:

- The `emqx` folder contains EMQX-TimescaleDB integration configurations to automatically create rules and data bridges when launching EMQX.
- The `emqx-exporter`, `prometheus` and `grafana-provisioning` folders include observability and energy consumption data visualization configurations for EMQX.
- The `create-table.sql` file defines the database table schema, which will create the tables in Timescale during initialization.
- The `docker-compose.yml` orchestrates all components to launch the project with one click.

### Start MQTTX CLI, EMQX, and Timescale

Please make sure you have installed the [Docker](https://www.docker.com/), and then run Docker Compose in the background to start the demo:

```shell
docker-compose up -d
```

Now, MQTTX CLI will simulate 10 factories connecting to EMQX, and report the energy consumption data of major equipment on their production lines at a frequency of 1 message per second. The energy data in JSON format will be sent to the topic `mqttx/simulate/IEM/{clientid}`.

All equipment will collect the current instantaneous power usage (randomly simulated, not exceeding max power), calculate the electricity consumption for 1 second, and publish the data to EMQX.

| Equipment Name       | Max Power (KWh) |
| :------------------- | :-------------- |
| Air Compressor 1     | 15              |
| Air Compressor 2     | 20              |
| Lighting             | 5               |
| Cooling Equipment    | 100             |
| Heating Equipment    | 200             |
| Conveyor             | 50              |
| Coating Equipment    | 20              |
| Inspection Equipment | 10              |
| Welding Equipment    | 20              |
| Packaging Equipment  | 30              |
| Cutting Equipment    | 70              |

```json
{
    "factory_id": "08",
    "factory": "Miller and Sons",
    "values": {
        "air_compressor_1": 3.72,
        "air_compressor_2": 5.01,
        "lighting": 0.95,
        "cooling_equipment": 23.19,
        "heating_equipment": 52.66,
        "conveyor": 10.66,
        "coating_equipment": 5.21,
        "inspection_equipment": 2.6,
        "welding_equipment": 5.27,
        "packaging_equipment": 7.38,
        "cutting_equipment": 12.56
    },
    "timestamp": 1691144157583
}
```

EMQX will create a rule to ingest messages from the factory. You can also modify this rule later to add custom processing using EMQX's[ built-in SQL functions](https://docs.emqx.com/en/enterprise/v5.1/data-integration/rule-sql-builtin-functions.html):

```sql
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

After the rules process the data, EMQX will insert the energy consumption data from the message payload into the specified table in Timescale through data bridges. Configuring INSERT SQL on the data bridges allows flexibly accomplishing this operation.

![Configuring INSERT SQL](https://assets.emqx.com/images/4fa61dcfe7fbc0f8774268d70b53b21a.png)

### Subscribe to Data from EMQX

Docker Compose has included a subscriber to print all energy consumption data. You can view the data with this command:

```bash
$ docker logs -f mqttx
[8/4/2023] [10:15:57 AM] › topic: mqttx/simulate/IEM/mqttx_85df7038
payload: {"factory_id":"08","factory":"Miller and Sons","values":{"air_compressor_1":3.72,"air_compressor_2":5.01,"lighting":0.95,"cooling_equipment":23.19,"heating_equipment":52.66,"conveyor":10.66,"coating_equipment":5.21,"inspection_equipment":2.6,"welding_equipment":5.27,"packaging_equi...
```

To subscribe and receive the data with any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools):

```shell
mqttx sub -t mqttx/simulate/IEM/+
```

### View Enengy Data in Grafana

To view enengy data in the Grafana dashboard, open `http://localhost:3000` in your browser, log in with username `admin` and password `public`.

After successful login, go to “Home → Dashboards” page and select “Energy Monitoring data”. The dashboard comprehensively displays the key energy consumption metrics of various industrial equipment, including the cumulative energy consumption value of each equipment and the energy consumption share of each plant, which fully presents the real-time energy usage of the industrial system and facilitates data-driven energy-saving management.

![View MQTT Enengy Data in Grafana](https://assets.emqx.com/images/d00a78b068cc7cdfc435a7f99d36306c.png)

## Conclusion

MQTT with Timescale integration is a powerful combination that can help you build efficient and scalable IoT applications. With MQTT, you can easily connect and manage your IoT devices, while Timescale provides a robust and scalable platform for processing and analyzing the data generated by these devices. By leveraging EMQX as a real-time [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and utilizing its SQL data integration to ingest data into Timescale, you can create a seamless data pipeline that allows you to collect, process, and analyze data from your IoT devices in real-time. This can help you gain valuable insights into your device performance, optimize your operations, and make data-driven decisions.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
