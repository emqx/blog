## Introduction

With the rapid growth of renewable energy, real-time monitoring and analysis of energy storage systems is crucial for performance and efficiency. The integration of [EMQX](https://www.emqx.com/en/products/emqx) and [Timescale](https://timescale.com/) provides the foundation for building a scalable IoT platform to holistically monitor distributed energy storage systems.

In this article, we will create a demo project on how EMQX can collect sensor data from energy storage systems and be integrated with Timescale for real-time storage and analytics. EMQX reliably aggregates data from storage systems via [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), while Timescale offers a performant time-series database.

## Prerequisites

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

## How it Works

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

## Clone the Project Locally

Clone the [emqx/mqtt-to-timescaledb](https://github.com/emqx/mqtt-to-timescaledb) repository locally, and initialize the submodule to enable the EMQX Exporter (optional):

```
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

## Start MQTTX CLI, EMQX, and Timescale

Please make sure you have installed the [Docker](https://www.docker.com/), and then run Docker Compose in the background to start the demo:

```
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

```
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

```
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

After the rules process the data, EMQX will insert the energy consumption data from the message payload into the specified table in Timescale through data bridges. Configuring INSERT SQL on the data bridges allows flexibly accomplishing this operation.

![Configuring INSERT SQL](https://assets.emqx.com/images/4fa61dcfe7fbc0f8774268d70b53b21a.png)

## Subscribe to Data from EMQX

Docker Compose has included a subscriber to print all energy consumption data. You can view the data with this command:

```
$ docker logs -f mqttx
[8/4/2023] [10:15:57 AM] › topic: mqttx/simulate/IEM/mqttx_85df7038
payload: {"factory_id":"08","factory":"Miller and Sons","values":{"air_compressor_1":3.72,"air_compressor_2":5.01,"lighting":0.95,"cooling_equipment":23.19,"heating_equipment":52.66,"conveyor":10.66,"coating_equipment":5.21,"inspection_equipment":2.6,"welding_equipment":5.27,"packaging_equi...
```

To subscribe and receive the data with any MQTT client:

```
mqttx sub -t mqttx/simulate/IEM/+
```

## View Enengy Data in Grafana

To view enengy data in the Grafana dashboard, open `http://localhost:3000` in your browser, log in with username `admin` and password `public`.

![View MQTT Enengy Data in Grafana](https://assets.emqx.com/images/d00a78b068cc7cdfc435a7f99d36306c.png)

## Conclusion

In this post, we have explored how to integrate EMQX and Timescale to build an industrial energy monitoring pipeline. By leveraging EMQX as a real-time MQTT broker and utilizing its SQL data integration to ingest data into Timescale, we have created an end-to-end solution for collecting and analyzing time-series sensor data.

This demo project provides a starting point for building scalable time-series data platforms, opening opportunities for real-time monitoring, optimization, and intelligence in industrial facilities and other time-sensitive use cases. The reliability of EMQX and the analytical power of Timescale unlock valuable insights from time-series data.

> Please Visit the [GitHub link](https://github.com/emqx/mqtt-to-timescaledb) for the Demo of ingesting time series data into Timescale.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
