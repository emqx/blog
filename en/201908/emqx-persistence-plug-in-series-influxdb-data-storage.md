InfluxDB is an open source sequential database developed by InfluxData. It was written by Go and focuses on querying and storing sequential data with high performance. InfluxDB is lighter than the OpenTSDB database introduced in the previous issue, and is better than OpenTSDB in benchmarking indicators given officially by InfluxData.

Faced with the large-scale and rapid growth of IoT sensor acquisition, transaction records and other data, accumulation speed of time series data is very fast. Sequential database can process such large-scale data by improving efficiency, and bring performance improvement, including: higher Ingest Rates, faster large-scale queries (although some other databases support more queries than it) and better data compression.

This article uses the actual example in the `CentOS 7.2` system to illustrate how to store related information through InfluxDB.



## Install and verify the InfluxDB server

Readers can refer to the InfluxDB official documentation (https://docs.influxdata.com/influxdb) or Docker (https://hub.docker.com/_/influxdb) to download and install the InfluxDB server. This article uses the InfluxDB version 1.7.



## Configure EMQX server

EMQX is installed via RPM, the InfluxDB related configuration file is located in  the directory of `/etc/emqx/plugins/emqx_backend_influxdb.conf`, and the InfluxDB plugin only supports message storage considering the function location.

**Configure the connection address and connection pool size：**

```bash
## InfluxDB UDP Server
## Use only UDP for access
backend.influxdb.pool1.server = 127.0.0.1:8089

## InfluxDB Pool Size
backend.influxdb.pool1.pool_size = 5

## Whether or not set timestamp when encoding InfluxDB line
backend.influxdb.pool1.set_timestamp = trues
```

**InfluxDB Backend message storage rule parameters:**

 Set the subject that needs to store the message with the topic filter, and distinguish  the pool parameter  between multiple data sources:

```bash
## Store Publish Message
backend.influxdb.hook.message.publish.1 = {"topic": "#", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```

Start the plugin by the method of either `command line` or `console`.



### Message template

Because MQTT Message cannot be written directly to InfluxDB, InfluxDB Backend provides the emqx_backend_influxdb.tmpl template file to convert MQTT Messages into DataPoints that can be written to InfluxDB.

> The message template feature requires EMQX to be restarted to apply the changes.

The tmpl file is located in `data/templates/emqx_backend_influxdb_example.tmpl`. Using the json format, users can define different Templates for different Topic, which is similar to:

```json
{
    "timestamp": <Where is value of timestamp>
		"measurement": <Where is value of measurement>,
    "tags": {
        <Tag Key>: <Where is value of tag>
    },
		"fields": {
    	<Field Key>: <Where is value of field>
    }
}
```

Among them, measurement and fields are required to be filled, and tags and timestamp are optional. <Where is value of> Supports to extract variables with the name `key`by placeholders such as `$key`. The supported variables are as follows:

- qos: Message QoS
- form: Publisher information
- topic: published topic
- timestamp
- Payload.*: Any variable in the JSON message body, such as `{ "data": [{ "temp": 1 }] }` Use `["$payload", "data", "temp"]` to extract `1 .

This example sets the template as follows:

```json
{
    "sample": {
        "measurement": "$topic",
        "tags": {
            "host": ["$payload", "data", "$0", "host"],
            "region": ["$payload", "data", "$0", "region"],
            "qos": "$qos",
            "from": "$from"
        },
        "fields": {
            "temperature": ["$payload", "data", "$0", "temp"]
        },
        "timestamp": "$timestamp"
    }
}
```

When the MQTT Message with Topic "sample" has the following Payload:

```json
{
  "data": [
    {
      "temp": 1,
      "host": "serverA",
      "region": "hangzhou"
    },
    {
      "temp": 2,
      "host": "serverB",
      "region": "ningbo"
    }
  ]
}
```



Backend converts the MQTT Message to:

```json
[
  {
    "measurement": "sample",
    "tags": {
      "from": "mqttjs_ebcc36079a",
      "host": "serverA",
      "qos": "0",
      "region": "hangzhou"
    },
    "fields": {
      "temperature": "1"
    },
    "timestamp": "1560743513626681000"
  },
  {
    "measurement": "sample",
    "tags": {
      "from": "mqttjs_ebcc36079a",
      "host": "serverB",
      "qos": "0",
      "region": "ningbo"
    },
    "fields": {
      "temperature": "2"
    },
    "timestamp": "1560743513626681000"
  }
]
```



## Example

On the **WebSocket** page of EMQX Management Console , the above format message message is published to the `sample` topic, and the message is parsed and stored in the `measurement` corresponding to the InfluxDB `udp` database.

## Summary

When the readers understands the data structure stored in InfluxDB and learns to use the message template to configure the written message field format, they can extend the application in conjunction with InfluxDB.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
