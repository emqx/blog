
OpenTSDB is an extensible distributed time series database, whose bottom layer relies on HBase and makes full use of the distributed column storage feature of HBase to support millions of reads and writes per second.

Facing large-scale rapid growth of loT sensor acquisition, transaction records and other data, time series data accumulates very quickly. The time series database processes this large-scale data by improving efficiency, and it brings performance improvements, including higher Ingest Rates, faster large-scale queries (Although it supports more queries than other relational databases), and better data compression.

This article will describe how to store related EMQ X MQTT messages through OpenTSDB by practical examples in the system `CentOS 7.2`. 



## Install and verify OpenTSDB server

Readers can refer to the [OpenTSDB documentation](https://opentsdb.net) or [Docker](https://hub.docker.com/r/petergrace/opentsdb-docker/) to download and install the OpenTSDB server. This article uses OpenTSDB 2.4.0. 



## Configure EMQ X MQTT server

If users use RPM method to install [EMQ X](https://emqx.io/), the OpenTSDB related configuration files is located in `/etc/emqx/plugins/emqx_backend_opentsdb.conf`. The OpenTSDB plugin only supports message storage considering the function location. 

Configure the connection address, connection pool size and batch strategies 

```bash
## OpenTSDB Server connected address
backend.opentsdb.pool1.server = 127.0.0.1:4242

## Connection pool size
backend.opentsdb.pool1.pool_size = 8


## Max batch size of put
backend.opentsdb.pool1.max_batch_size = 20

## Store all information through the topic filter
backend.opentsdb.hook.message.publish.1 = {"topic": "#", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```

**OpenTSDB Backend message storage rule parameters:**

Set the topic which needs to store information through the topic filter, and distinguish the pool parameter between multiple data sources:

```bash
## Store Publish Message
backend.opentsdb.hook.message.publish.1 = {"topic": "#", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```

Enable this plugin:

```bash
./bin/emqx_ctl plugins load emqx_backend_opentsdb
```



### Message template

Because the **MQTT Message** can not be written directly to OpenTSDB, OpenTSDB backend provides the emqx_backend_opentsdb.tmpl template file to convert the MQTT Message to DataPoint that can be written to OpenTSDB.

> The message template function requires EMQ X to be restarted to apply the changes.

The tmpl file is located in `data/templates/emqx_backend_opentsdb_example.tmpl`. Using the json format, users can define different Template for different Topic, which is similar to:

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
        "value": ["$payload", "data", "$0", "temp"],
        "timestamp": "$timestamp"
    }
}
```

Among them, measurement and fields are required to be filled, and tags and timestamp are optional. Supports to extract variables with the name ` key` by placeholders such as `$key`. The supported variables are as follows:

- qos: Message QoS
- form: Publisher information
- topic: Published topic
- timestamp
- Payload.*: Any variable in the JSON message body, such as `{ "data": [{ "temp": 1 }] }`. Use `["$payload", "data", "temp"]` to extract `1`.  

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
        "value": ["$payload", "data", "$0", "temp"],
        "timestamp": "$timestamp"
    }
}

```

When the MQTT message with the Topic "sample" has the following Payload: 

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



Backend will convert the MQTT Message to:

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
    "value": "1",
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
    "value": "2",
    "timestamp": "1560743513626681000"
  }
]
```



## Example

In the EMQ X management console **WebSocket** page, publish the message in the above format to the topic `sample`, the message will be parsed and stored in the `measurement` corresponding to the OpenTSDB `udp` database.

## Summary

Readers can extend related applications by using OpenTSDB, after understanding the data structure stored in OpenTSDB and learning how to use the message template to configure the written message field format. 