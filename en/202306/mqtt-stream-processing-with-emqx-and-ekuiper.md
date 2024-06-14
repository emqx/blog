## Introduction

[MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol that is ideal for IoT applications. It is designed to be simple, open, and easy to implement, making it a popular choice for IoT applications. MQTT data are ingested continuously and in real-time and thus are suitable to be processed by stream processing engines.

As a large-scale distributed [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) for IoT, [EMQX](https://github.com/emqx/emqx) can efficiently and reliably connect to massive IoT devices, and process and distribute messages and event flow data in real-time. [eKuiper](https://ekuiper.org/) is an open-source stream processing engine that can filter, transform, and aggregate streaming data.

This article will demonstrate using eKuiper to stream process MQTT data from EMQX in real-time.


![MQTT Stream Processing with EMQX and eKuiper](https://assets.emqx.com/images/fae0396b7c04f6b24fd42fa693023746.png)


## Scenario Description

Suppose we have an [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) `demo/sensor` that collects temperature and humidity data in EMQX. We want to use eKuiper to subscribe to the topic, process and analyze the data with streaming technology and trigger actions to users' HTTP service or save the result to external storage.

### EMQX

Thanks to EMQX’s standard MQTT protocol support, eKuiper can connect to any version of EMQX. Here, we use the free public MQTT Broker provided by [EMQX Cloud](https://www.emqx.com/en/cloud) for testing:

| Cluster | Address of Cluster | Listening Port |
| :------ | :----------------- | :------------- |
| emqx1   | `broker.emqx.io`   | 1883           |

### eKuiper

We can install eKuiper on the edge or cloud side. We can use `Docker` to quickly install it.

```
docker run -p 9081:9081 -d --name kuiper -e MQTT_SOURCE__DEFAULT__SERVER=tcp://broker.emqx.io:1883 lfedge/ekuiper:1.10.0
```

By this command, we can pull eKuiper 1.10.0 version docker image and start running it. We set the REST API port to 9081, and we will use this API to manage eKuiper in this tutorial. We also set the default MQTT broker address to EMQX Cloud cluster by the environment variable.

For other installation methods, please check the [installation guide](https://ekuiper.org/docs/en/latest/installation.html) to install eKuiper.

## Configure eKuiper to Subscribe to MQTT Data Stream

The MQTT data are usually unbounded and continuous streaming data. In eKuiper, there is a concept called stream, which is a model for such kind of data. Before processing the MQTT data, we need to create a stream to describe the data.

Let's use eKuiper REST API to create a stream:

```
POST http://127.0.0.1:9081/streams
Content-Type: application/json

{
  "sql": "CREATE STREAM demoMqttStream (temperature FLOAT, humidity FLOAT) WITH (TYPE=\"mqtt\", DATASOURCE=\"demo/sensor\", FORMAT=\"json\", SHARED=\"true\")"
}
```

Send out the above request with any HTTP clients such as Postman. We can create a stream named `demoMqttStream` with MQTT type data source. The `datasource` property is `demo/sensor`, which means subscribing to this topic in MQTT. The data format is JSON. The `SHARED` option means the stream is shared by all the rules.

> **Note:**
>
> - The default MQTT broker address is set to `tcp://broker.emqx.io:1883` when we run the eKuiper docker container. If you use another MQTT broker, change that address to your broker address when installing.
> - If you want to change the MQTT broker address and any other MQTT connection parameter like authentication, try to change the setting on `data/mqtt_souce.yaml` file.
> - You can subscribe to multiple topics by using the `+` and `#` wildcard in the `datasource` property. For example, `demo/+` means to subscribe to all the topics starting with `demo/`. `demo/#` means to subscribe to all the topics starting with `demo/` and all the subtopics under `demo/`.

## Stream Processing MQTT data

In eKuiper, we define rules for stream processing workflows. A rule is a SQL statement that defines how to process the data and the actions to perform after processing. Besides continuous data processing, stream processing engines like eKuiper also support stateful processing. We will demonstrate two examples of stream processing and stateful processing.

### Stateful Alert Rule

The first stream processing example is to detect the temperature and humidity data and trigger an alert when the temperature has increased more than 0.5 or the humidity has increased more than 1. This requires the processing engine to maintain the state of the previous data and compare it with the current data.

Suppose we have an HTTP webhook that can receive the alert data with the URL `http://yourhost/alert`. We can create a rule with the following HTTP request.

```
###
POST http://{{host}}/rules
Content-Type: application/json

{
  "id": "rule1",
  "sql": "SELECT temperature, humidity FROM demoMqttStream WHERE temperature - LAG(temperature) > 0.5 OR humidity - LAG(humidity) > 1",
  "actions": [{
    "rest": {
      "url": "http://yourhost/alert",
      "method": "post",
      "sendSingle": true
    }
  }]
}
```

We create a rule named `rule1` with the SQL statement below:

```
SELECT temperature, humidity 
FROM demoMqttStream 
WHERE 
  temperature - LAG(temperature) > 0.5 
  OR humidity - LAG(humidity) > 1
```

This SQL query will select the temperature and humidity data from the `demoMqttStream` when their change meets our criteria. Whereas the `LAG` function is used to get the previous data.

The `actions` property defines the actions to perform after the rule is triggered. Here, we use the `rest` action to send the data to the `http://yourhost/alert` endpoint. The sent data is the JSON format of the data selected by the SQL query. Thus, the data sent to the endpoint will be like this:

```
{
  "temperature": 25.5,
  "humidity": 60.5
}
```

#### Test the Rule

We can use [MQTTX](https://mqttx.app/) or any other MQTT client to publish MQTT data to the `demo/sensor` topic. Those data will be processed by the rule. For example, we publish the following data on the topic:

```
{"temperature": 25.5, "humidity": 60.5}
{"temperature": 26.1, "humidity": 62}
{"temperature": 25.9, "humidity": 62.1}
{"temperature": 26.5, "humidity": 62.3}
```

We will receive in our HTTP alert services the following data:

```
{"temperature": 26.1, "humidity": 62}
{"temperature": 26.5, "humidity": 62.3}
```

This is because only for the 2nd and 4th messages, the temperature has increased more than 0.5 or the humidity has increased more than 1.

If you encounter any problems running the rule, please refer to [How to Debug Rules | eKuiper Documentation](https://ekuiper.org/docs/en/latest/getting_started/debug_rules.html) for help.

### Time Window Aggregation Rule

The second example is to calculate the average temperature and humidity for each minute and send it back to EMQX. This involves a classical stream processing concept called time window. We can create a rule with the following HTTP request.

```
###
POST http://{{host}}/rules
Content-Type: application/json

{
  "id": "rule2",
  "sql": "SELECT 
  trunc(avg(temperature), 2) as avg_temperature, trunc(avg(humidity), 2) as avg_humidity, window_end() as ts FROM demoMqttStream GROUP BY TumblingWindow(mi, 1)",
  "actions": [{
    "mqtt": {
      "server": "tcp://broker.emqx.io:1883",
      "topic": "result/aggregation",
      "sendSingle": true
    }
  }]
}
```

We create a rule named `rule2` with the SQL statement below:

```
SELECT 
  trunc(avg(temperature), 2) as avg_temperature, 
  trunc(avg(humidity), 2) as avg_humidity,
  window_end() as ts
FROM demoMqttStream
GROUP BY TumblingWindow(mi, 1)
```

This SQL query will select the average temperature and humidity data for each minute. The time window is defined in the `GROUP BY` clause with `TumblingWindow`. This window type splits MQTT data into fixed-length windows. In the `SELECT` clause, we use the aggregate function `avg` to calculate the average values for both temperature and humidity in the time window. The `window_end()` function is used to get the end time of the time window so that we'll know when these average values are calculated. The `trunc` function is used to round the average value to 2 decimal places.

The `actions` property defines the actions to perform after the rule is triggered. Here, we use the `mqtt` action to send the data to the `result/aggregation` topic in EMQX. The sent data is the JSON format of the data selected by the SQL query. Thus, the data sent to the topic will be like this:

```
{
  "avg_temperature": 25.5,
  "avg_humidity": 60.5,
  "ts": 1621419600000
}
```

#### Test the Rule

Again, we can use [MQTTX](https://mqttx.app/) or any other MQTT client to publish MQTT data to the `demo/sensor` topic. Those data will be processed by the rule. For example, we publish the following data to the topic with a 30 seconds interval, and the two minutes data is like this:

```
{"temperature": 25.5, "humidity": 60.5}
{"temperature": 26.1, "humidity": 62}
{"temperature": 25.9, "humidity": 62.1}
{"temperature": 26.5, "humidity": 62.3}
```

We will receive in our HTTP alert services the following data:

```
{"avg_temperature": 25.8, "avg_humidity": 61.25, "ts": 1621419600000}
{"avg_temperature": 26.2, "avg_humidity": 62.2, "ts": 1621419660000}
```

We have sent out 2 minutes' data so that we got two average values for each minute.

## Summary

In this tutorial, we have learned how to use eKuiper to process MQTT data. Now you can:

- Subscribe to EMQX MQTT broker to get MQTT data
- Create rules to process MQTT data
- Send the processed data back to the EMQX broker

We show two examples to demonstrate the streaming capability of eKuiper against MQTT data. eKuiper has a powerful streaming capability that can be leveraged against a wide range of streaming data sources. Welcome to explore eKuiper's capabilities to build efficient data processing pipelines against the MQTT data in real time.


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
