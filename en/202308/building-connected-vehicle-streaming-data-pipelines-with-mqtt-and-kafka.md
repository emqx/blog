## Introduction

In today's IoT landscape, the integration of [MQTT and Kafka](https://www.emqx.com/en/blog/mqtt-and-kafka) offers immense value across various use cases. Whether it's [Connected Cars](https://www.emqx.com/en/blog/connected-cars-and-automotive-connectivity-all-you-need-to-know) and Telematics, Smart City Infrastructure, [Industrial IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges) Monitoring, or Logistics Management, the combination of MQTT and Kafka enables seamless, efficient and real-time data processing.

This article will provide a demo to illustrate how MQTT and Kafka can be integrated. We will simulate vehicle devices and their dynamic Telematics data, connect them to an [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), and then send the data to Apache Kafka. We have selected [EMQX](https://www.emqx.com/en/products/emqx) as the MQTT Broker because it comes with a built-in Kafka data integration that simplifies the process.

## Prerequisites

- Git

- Docker Engine: v20.10+

- Docker Compose: v2.20+

## How It Works

![MQTT to Kafka Architecture](https://assets.emqx.com/images/414774fb7f5b20256d52eaf70196798a.jpg)

<center>MQTT to Kafka Architecture</center>

<br>

This is a simple and effective architecture that avoids complex components. It utilizes the following 3 key components:

| Component Name                                           | Version | Description                                                  |
| -------------------------------------------------------- | ------- | ------------------------------------------------------------ |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+  | A command line tool to generate simulated vehicle and test data. |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.0.4+  | MQTT broker used for message exchange between vehicles and the Kafka system. |
| [Kafka](https://kafka.apache.org/)                       | 2.8.0+  | Apache Kafka serves as a distributed streaming platform for ingesting, storing, and processing vehicle data. |

In addition to the basic components, EMQX provides comprehensive observability capabilities. You can use the following components to monitor EMQX metrics and load when the system is running:

| Component Name                                         | Version | Description                                                  |
| ------------------------------------------------------ | ------- | ------------------------------------------------------------ |
| [EMQX Exporter](https://github.com/emqx/emqx-exporter) | 0.1     | Prometheus exporter for EMQX                                 |
| [Prometheus](https://prometheus.io/)                   | v2.44.0 | Open-source systems monitoring and alerting toolkit.         |
| [Grafana](https://grafana.com/)                        | 9.5.1+  | Visualization platform utilized to display and analyze the collected data. |

Now that you have understood the basic architecture of this project, let's get the vehicle started!

## 5 Steps to Setup MQTT to Kafka Demo

### 1. Clone the Project Locally

Clone the [emqx/mqtt-to-kafka](https://github.com/emqx/mqtt-to-kafka) repository locally, and initialize the submodule to enable the EMQX Exporter (optional):

```
git clone https://github.com/emqx/mqtt-to-kafka
cd mqtt-to-kafka

# Optional
git submodule init
git submodule update
```

The codebase consists of 3 parts:

- The `emqx` folder contains EMQX-Kafka integration configurations to create rules and data bridges when launching EMQX automatically.

- The `emqx-exporter`, `prometheus` and `grafana-provisioning` folders include observability configurations for EMQX.

- The `docker-compose.yml` orchestrates multiple components to launch the project with one click.

### 2. Start MQTTX CLI, EMQX, and Kafka

Please make sure you have installed the [Docker](https://www.docker.com/), and then run Docker Compose in the background to start the demo:

```
docker-compose up -d
```

Now, 10 Tesla vehicles simulated by MQTTX CLI will connect to EMQX and report their status to the topic `mqttx/simulate/tesla/{clientid}` at a frequency of once per second.

In fact, EMQX will create a rule to ingest messages from Tesla. You can also modify this rule later to add custom processing using EMQX's [built-in SQL functions](https://docs.emqx.com/en/enterprise/v5.1/data-integration/rule-sql-builtin-functions.html):

```
SELECT
  payload
FROM
  "mqttx/simulate/#"
```

EMQX also creates a data bridge to produce vehicle data to Kafka with the following key configurations:

- Publish messages to the `my-vehicles` topic in Kafka

- Use each vehicle's client ID as the message key

- Use the message publish time as the message timestamp

![Kafka Config](https://assets.emqx.com/images/ad15e9decf2e5be01d712ec0b3aa2090.png)

### 3. Subscribe to Vehicle Data From EMQX

> This step has no special meaning for the demo, just to check if the MQTTX CLI and EMQX are working.

Docker Compose has included a subscriber to print all vehicle data. You can view the data with this command:

```
$ docker logs -f mqttx
[8/4/2023] [8:56:41 AM] › topic: mqttx/simulate/tesla/mqttx_063105a2
payload: {"car_id":"WLHK53W2GSL511787","display_name":"Roslyn's Tesla","model":"S...
```

To subscribe and receive the data with any MQTT client:

```
mqttx sub -t mqttx/simulate/tesla/+
```

### 4. Subscribe to Vehicle Data From Kafka

Assuming everything is functioning properly, EMQX is streaming data from the vehicle into the `my-vehicles` topic of Kafka in real-time. You can consume data from Kafka with the following command:

```
docker exec -it kafka \
  kafka-console-consumer.sh \
  --topic my-vehicles \
  --from-beginning \
  --bootstrap-server localhost:9092
```

You will receive JSON data similar to this:

```
{"vin":"EDF226K7LZTZ51222","speed":39,"odometer":68234,"soc":87,"elevation":4737,"heading":33,"accuracy":24,"power":97,"shift_state":"D","range":64,"est_battery_range":307,"gps_as_of":1681704127537,"location":{"latitude":"83.3494","longitude":"141.9851"},"timestamp":1681704127537}
```

The data is inspired by [TeslaMate](https://github.com/adriankumpf/teslamate), a powerful self-hosted Tesla data logger, and you can check the MQTTX CLI [script](https://github.com/emqx/MQTTX/blob/main/scripts-example/IoT-data-scenarios/tesla.js) to see how the data is generated.

### 5. View EMQX Metrics (Optional)

If you have enabled EMQX Exporter in step 1, it will faithfully collect all EMQX metrics including client connections, message rate, rule executions, etc. It provides valuable insights into the system.

To view EMQX metrics in the Grafana dashboard, open `http://localhost:3000` in your browser, log in with username `admin` and password `public`.

## Conclusion

In this blog post, we have explored how to integrate MQTT and Kafka to build a connected vehicle streaming data pipeline. By leveraging EMQX as an MQTT broker and utilizing EMQX Data Integration to stream data to Kafka, we have created an end-to-end solution for accumulating and processing streaming data.

Next, you can directly integrate applications into Kafka to consume vehicle data and decouple them. You can also leverage Kafka Streams to perform real-time stream processing on automotive data, conduct statistical analysis and anomaly detection. The results can be output to other systems via Kafka Connect.

This demo project serves as a starting point for building scalable and reliable streaming data pipelines. The powerful integration of MQTT and Kafka opens up opportunities for real-time analytics, monitoring, and decision-making in various domains.

**Next steps:**

- Please Visit the [GitHub link](https://github.com/emqx/mqtt-to-kafka) for the Demo of Streamlining MQTT Data Integration with Kafka.
- Learn how to configure this data flow pipeline from scratch, you can refer to the [EMQX documentation](https://docs.emqx.com/en/enterprise/v5.1/data-integration/data-bridge-kafka.html).
