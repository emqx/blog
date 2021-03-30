



OpenTSDB 是可扩展的分布式时序数据库，底层依赖 HBase 并充分发挥了HBase的分布式列存储特性，支持数百万每秒的读写。

面对大规模快速增长的物联网传感器采集、交易记录等数据，时间序列数据累计速度非常快，时序数据库通过提高效率来处理这种大规模数据，并带来性能的提升，包括：更高的容纳率（Ingest Rates）、更快的大规模查询（尽管有一些比其他数据库支持更多的查询）以及更好的数据压缩。

本文以 `CentOS 7.2` 系统中的实际例子来说明如何通过 OpenTSDB 来存储相关的信息。



## 安装与验证 OpenTSDB 服务器

读者可以参考 OpenTSDB [官方文档](http://opentsdb.net) 或 [Docker](https://hub.docker.com/r/petergrace/opentsdb-docker/) 来下载安装 OpenTSDB 服务器，本文使用 OpenTSDB 2.4.0 版本。



## 配置 EMQ X 服务器

通过 RPM 方式安装的 EMQ X，OpenTSDB 相关的配置文件位于 `/etc/emqx/plugins/emqx_backend_opentsdb.conf`，考虑到功能定位，OpenTSDB 插件仅支持消息存储功能。更多 backend 插件详见 [EMQ X 数据持久化](https://developer.emqx.io/docs/tutorial/zh/backend/whats_backend.html)。

**配置连接地址与连接池大小、batch 策略：**

```bash
## OpenTSDB Server 接入地址
backend.opentsdb.pool1.server = 127.0.0.1:4242

## 连接池大小
backend.opentsdb.pool1.pool_size = 8


## Max batch size of put 最大批量写条数
backend.opentsdb.pool1.max_batch_size = 20

## 通过 topic 过滤器存储全部消息
backend.opentsdb.hook.message.publish.1 = {"topic": "#", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```

**OpenTSDB Backend 消息存储规则参数: **

通过 topic 过滤器，设置需要存储消息的主题，pool 参数区别多个数据源：

```bash
## Store Publish Message
backend.opentsdb.hook.message.publish.1 = {"topic": "#", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```

启动该插件：

```bash
./bin/emqx_ctl plugins load emqx_backend_opentsdb
```



### 消息模板

由于 MQTT Message 无法直接写入 OpenTSDB, OpenTSDB Backend 提供了 emqx_backend_opentsdb.tmpl 模板文件将 MQTT Message 转换为可写入 OpenTSDB 的 DataPoint。 

> 消息模板功能需要重启 EMQ X 才能应用更改。

tmpl 文件位于 `data/templates/emqx_backend_opentsdb_example.tmpl`，使用 json 格式, 用户可以为不同 Topic 定义不同的 Template, 类似: 

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

其中, measurement 与 fields 为必选项, tags 与 timestamp 为可选项。<Where is value of> 支持通过占位符如 `$key` 提取变量名为 `key` 的变量，支持的变量如下：

- qos: 消息 QoS
- form: 发布者信息
- topic: 发布主题
- timestamp: 时间戳
- payload.*: JSON 消息体内任意变量，如 `{ "data": [{ "temp": 1 }] }` 使用 `["$payload", "data", "temp"]`  可以提取出 `1` 来

本示例设定模板如下：

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

当 Topic 为”sample” 的 MQTT Message 拥有以下 Payload 时:

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



Backend 会将 MQTT Message 转换为:

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



## 使用示例

EMQ X  管理控制台 **WebSocket** 页面中，向 `sample` 主题发布如上格式消息消息，消息将解析存储到 OpenTSDB `udp` 数据库对应的 `measurement` 中。

## 总结

读者在理解了 OpenTSDB 中所存储的数据结构，学习使用消息模板配置写入消息字段格式后可以结合 OpenTSDB 拓展相关应用。


