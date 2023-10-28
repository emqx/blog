## Introduction

As renewable energy like solar and wind power evolve, energy storage emerges as an essential method to smooth the fluctuating output and achieve the supply-demand balance. Additionally, in the realm of electric vehicles(EV), the increasing demand for the secondary use of EV batteries has also led to a thriving market for energy storage.

[EMQX](https://www.emqx.com/en/products/emqx) and InfluxDB together offer a scalable IoT platform that enables efficient and real-time collection of data from distributed energy storage devices. The collected data is then centrally managed and analyzed to facilitate power dispatching and electricity trading. This article provides a detailed guide on how to connect energy storage devices with EMQX and integrate it with InfluxDB to ensure reliable data storage and enable real-time analytics.

You can read this blog to learn more about how EMQX enables easy integration of time-series databases like InfluxDB and Timesacle with MQTT: [Time-Series Database (TSDB) for IoT: The Missing Piece](https://www.emqx.com/en/blog/time-series-database-for-iot-the-missing-piece).

## What is InfluxDB

InfluxDB is a time series database designed specifically for time series data. It can efficiently store and query massive amounts of time series data. InfluxDB supports high write throughput and provides rich data retention policies, allowing high-speed writes of massive IoT data with low-cost storage optimization. At the same time, InfluxDB provides SQL-like query language that makes it easy to query and aggregate time series data, enabling fast analysis and monitoring of IoT data. It is highly suitable for IoT scenarios. EMQX now supports connection to mainstream versions of InfluxDB Cloud, InfluxDB OSS, or InfluxDB Enterprise.

## Prerequisites

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

## How it Works

![MQTT to InfluxDB](https://assets.emqx.com/images/2aabbc7e8a0a861e03881f9e4ec85002.png)

This is a simple and effective architecture that avoids complex components. It utilizes the following four key components:

| Component Name                                           | Version | Description                                                  |
| :------------------------------------------------------- | :------ | :----------------------------------------------------------- |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+  | A command line tool for energy data generation.              |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.0.4+  | MQTT broker used for message exchange between energy storage device and the InfluxDB. |
| [InfluxDB](https://influxdata.com/)                      | 2.0.0+  | Used for energy data storage and management, as well as providing time aggregation and analysis capabilities for Grafana. |
| [Grafana](https://grafana.com/)                          | 9.5.1+  | Visualization platform for the collected data display and analysis. |

In addition to the basic components, EMQX provides comprehensive observability capabilities. You can use the following components to monitor EMQX metrics and load when the system is running:

| Component Name                                         | Version | Description                                          |
| ------------------------------------------------------ | ------- | ---------------------------------------------------- |
| [EMQX Exporter](https://github.com/emqx/emqx-exporter) | 0.1     | Prometheus exporter for EMQX.                        |
| [Prometheus](https://prometheus.io/)                   | v2.44.0 | Open-source systems monitoring and alerting toolkit. |

## Clone the Project Locally

Clone the [emqx/mqtt-to-influxdb](https://github.com/emqx/mqtt-to-influxdb) repository locally, and initialize the submodule to enable the EMQX Exporter (optional):

```
git clone https://github.com/emqx/mqtt-to-influxdb
cd mqtt-to-influxdb

# Optional
git submodule init
git submodule update
```

The codebase consists of four parts:

- The `emqx` folder contains EMQX-InfluxDB integration configurations to automatically create rules and data bridges when launching EMQX.
- The `mqttx` folder contains a simulation script for simulating energy storage devices connecting to EMQX and generating data.
- The `emqx-exporter`, `prometheus` and `grafana-provisioning` folders include observability and energy consumption data visualization configurations for EMQX.
- The `docker-compose.yml` orchestrates all components to launch the project with one click.

## Start MQTTX CLI, EMQX, and InfluxDB

Please make sure you have installed the [Docker](https://www.docker.com/), and then run Docker Compose in the background to start the demo:

```
docker-compose up -d
```

Now, MQTTX CLI will simulate 10 energy storage devices connecting to EMQX, and periodically publish the energy generation and consumption status on the device to specific topics. The energy data in JSON format will be sent to the topic `mqttx/simulate/Energy-Storage/{clientid}`.

The simulator accurately replicates real-world situations. It begins functioning 24 hours prior to the present moment. Each energy storage device has a distinct initial level of electricity. Energy generation and consumption fluctuate throughout the day, resulting in continuous charging and discharging of the storage units. The battery's temperature and voltage are critical indicators that reflect the energy storage system's operational status.

This is an example of data published to EMQX for a specific energy storage device:

```
{
    "id": "87780204-890a-4b9a-b271-b0cf719ca62f",
    "name": "Energy_Storage_0",
    "type": "FX48-B2800",
    "inputPower": 0.01,
    "outputPower": 136.98,
    "percentage": 100.01,
    "remainingCapacity": 2799.62,
    "timestamp": 1696721283913,
    "temperature": 19.48,
    "voltage": 1230.59,
    "battery": [
        {
            "id": "ec6fd356-2862-44a1-899b-80410890ecf6",
            "name": "Battery_1",
            "voltage": 1230.6,
            "temperature": 19.15,
            "percentage": 100.01,
            "inputPower": 0.01,
            "outputPower": 45.66
        },
        {
            "id": "f07a09de-43a0-4306-8997-a96fd583d76d",
            "name": "Battery_2",
            "voltage": 1230.6,
            "temperature": 19.95,
            "percentage": 100.01,
            "inputPower": 0.01,
            "outputPower": 45.66
        },
        {
            "id": "70e5a888-186b-4ef2-b122-a63ba6c1499b",
            "name": "Battery_3",
            "voltage": 1230.57,
            "temperature": 19.34,
            "percentage": 99.99,
            "inputPower": 0.01,
            "outputPower": 45.66
        }
    ],
    "deltaCapacity": -0.38
}
```

EMQX will create a rule to ingest messages from the energy storage device. You can also modify this rule later to add custom processing using EMQX's[ built-in SQL functions](https://docs.emqx.com/en/enterprise/v5.1/data-integration/rule-sql-builtin-functions.html):

```
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

After the rules process the data, EMQX will insert the energy data from the message payload into the `iot_data` bucket in InfluxDB through data bridges. 

## Subscribe to Data from EMQX

Docker Compose has included a subscriber to print all energy data. You can view the data with this command:

```
$ docker logs -f mqttx
[9/24/2023] [10:15:57 AM] › topic: mqttx/simulate/Energy-Storage/mqttx_6d014c26
payload: {"id":"87780204-890a-4b9a-b271-b0cf719ca62f","name":"Energy_Storage_0","type":"FX48-B2800","inputPower":2.41,"outputPower":539.24,"percentage":94.68,"remainingCapacity":2649.52,"timestamp"...
```

To subscribe and receive the data with any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools):

```
mqttx sub -t mqttx/simulate/IEM/+
```

## View Enengy Data in Grafana

To view energy data in the Grafana dashboard, open `http://localhost:3000` in your browser and log in with username `admin` and password `public`.

After successful login, go to “Home → Dashboards” page and select “EMQX Energy Storage”. The dashboard provides a comprehensive overview of the energy storage devices' status, including current stored electricity, input and output power, and trends of these metrics at different times. With these key metrics, you can intuitively monitor the operation of storage devices, promptly identify issues for maintenance, and make informed energy dispatch decisions based on real-time data. The rich visualizations in the dashboard also enable more efficient and intuitive data analytics and decision making.

![View Enengy Data in Grafana](https://assets.emqx.com/images/486833a1a4142053e77e6d577a401e07.png)

## Conclusion

In this post, we have explored how to integrate EMQX and InfluxDB to build an energy storage management application. By leveraging EMQX as a real-time [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and ingesting data into InfluxDB, we have created an end-to-end solution for collecting and analyzing time-series energy storage data.

This demo project provides a starting point for building scalable time-series data platforms, opening opportunities for real-time monitoring, optimization, and intelligence in energy storage and other time-sensitive use cases. The reliability of EMQX and the analytical power of InfluxDB unlock valuable insights from time-series data.

**Next steps:** Please Visit the [GitHub link](https://github.com/emqx/emqx/mqtt-to-influxdb) for the Demo of ingesting time series data into InfluxDB.





<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
