[IoTDB](https://iotdb.apache.org/) 是最早由清华大学发起的开源时序数据库项目，现已经是 Apache 的顶级项目。IoTDB 可以为用户提供数据收集、存储和分析等服务。由于其轻量级架构、高性能和高可用的特性，以及与 Hadoop 和 Spark 生态的无缝集成，满足了工业 IoT 领域中海量数据存储、高吞吐量数据写入和复杂数据查询分析的需求。


[EMQX](https://www.emqx.io/zh) 是一个大规模扩展、可弹性伸缩的开源云原生分布式物联网消息中间件，由开源物联网数据基础设施软件供应商 [EMQ 映云科技](https://www.emqx.com/zh/about) 发布。EMQX 可以高效可靠地处理海量物联网设备的并发连接，并且内置了强大的规则引擎功能，用以对事件和消息流数据进行高性能地实时处理。规则引擎通过 SQL 语句提供了灵活的 "配置式" 的业务集成方案，简化了业务开发流程，提升了易用性，降低了用户的业务逻辑与 EMQX 的耦合度。

本文将介绍如何使用 EMQX 规则引擎的 MQTT 数据桥接功能，接收 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)发送的数据，并实时插入到时序数据库 IoTDB。

## 准备工作

本文示例中用到的软件和环境：

- **操作系统：** Mac OSX
- **IoTDB：** [Binary 包（Server），版本 0.12.4](https://www.apache.org/dyn/closer.cgi/iotdb/0.12.4/apache-iotdb-0.12.4-server-bin.zip)
- **MQTT 服务器：** [EMQX 开源版 v4.3.11](https://www.emqx.com/zh/downloads/broker/4.3.11/emqx-macos-4.3.11-amd64.zip)
- **MQTT 客户端软件：**[MQTTX v1.6.0](https://mqttx.app/zh)


## IoTDB 安装

首先我们需要从 [IoTDB 官方页面](https://iotdb.apache.org/Download/)下载 IoTDB Server（单机版）的二进制包。

下载完成之后解压，进入解压后的目录：

```shell
% ls
LICENSE         README.md       RELEASE_NOTES.md data             ext             licenses         sbin
NOTICE           README_ZH.md     conf             docs             lib             logs             tools
```

要启用 IoTDB 的 [MQTT 协议](https://www.emqx.com/zh/mqtt)支持，需要改动 IoTDB 的配置文件 `conf/iotdb-engine.properties`：

> *后续建模使用了一个存储组 [root.sg](http://root.sg/)，为了增加写入并行度，需要同时将 iotdb-engine.properties 中的  virtual_storage_group_num 设置为机器核数。

```
####################
### MQTT Broker Configuration
####################

# whether to enable the mqtt service.
enable_mqtt_service=true

# the mqtt service binding host.
mqtt_host=0.0.0.0

# the mqtt service binding port.
mqtt_port=2883

# the handler pool size for handing the mqtt messages.
mqtt_handler_pool_size=1

# the mqtt message payload formatter.
mqtt_payload_formatter=json

# max length of mqtt message in byte
mqtt_max_message_size=1048576
```

其中 `enable_mqtt_service` 默认为 false，需要改成 `true`。`mqtt_port` 默认值是 1883，为了避免与 emqx 的端口号冲突，需要改为 2883。

然后使用 `./sbin/start-server.sh` 启动 IoTDB 服务端：

```shell
% ./sbin/start-server.sh
---------------------
Starting IoTDB
---------------------
Maximum memory allocation pool = 2048MB, initial memory allocation pool = 512MB
If you want to change this configuration, please check conf/iotdb-env.sh(Unix or OS X, if you use Windows, check conf/iotdb-env.bat).
2022-01-10 14:15:31,914 [main] INFO o.a.i.d.c.IoTDBDescriptor:121 - Start to read config file file:./sbin/../conf/iotdb-engine.properties
...
2022-01-10 14:14:28,690 [main] INFO o.a.i.d.s.UpgradeSevice:73 - Upgrade service stopped
2022-01-10 14:14:28,690 [main] INFO o.a.i.db.service.IoTDB:153 - Congratulation, IoTDB is set up successfully. Now, enjoy yourself!
2022-01-10 14:14:28,690 [main] INFO o.a.i.db.service.IoTDB:101 - IoTDB has started
```

我们保持这个终端窗口不动，另外打开一个新的命令行终端窗口，启动 IoTDB 的 shell 工具：

```shell
% ./sbin/start-cli.sh
---------------------
Starting IoTDB Cli
---------------------
_____       _________ ______   ______
|_   _|     | _   _ ||_   _ `.|_   _ \
| |   .--.|_/ | | \_| | | `. \ | |_) |
| | / .'`\ \ | |     | | | | | __'.
_| |_| \__. | _| |_   _| |_.' /_| |__) |
|_____|'.__.' |_____| |______.'|_______/ version 0.12.4


IoTDB> login successfully
IoTDB>
```

至此 IoTDB 环境就准备好了。如要了解 IoTDB 的基本使用方法，可以参考官网的[快速上手页面](https://iotdb.apache.org/zh/UserGuide/Master/QuickStart/QuickStart.html)。

## 安装、配置 EMQX

### 下载和启动 EMQX

我们直接使用命令行下载 macOS 版本的 EMQX 开源版，更多安装包请访问 [EMQX 开源版下载页面](https://www.emqx.io/zh/downloads)。

```shell
% wget https://www.emqx.com/en/downloads/broker/4.3.11/emqx-macos-4.3.11-amd64.zip
```

然后解压并启动 EMQX：

```shell
% unzip -q emqx-macos-4.3.11-amd64.zip
% cd emqx
% ./bin/emqx console

log.to = "console"
Erlang/OTP 23 [erts-11.1.8] [emqx] [64-bit] [smp:8:8] [ds:8:8:8] [async-threads:4] [hipe]
Starting emqx on node emqx@127.0.0.1
Start mqtt:tcp:internal listener on 127.0.0.1:11883 successfully.
Start mqtt:tcp:external listener on 0.0.0.0:1883 successfully.
Start mqtt:ws:external listener on 0.0.0.0:8083 successfully.
Start mqtt:ssl:external listener on 0.0.0.0:8883 successfully.
Start mqtt:wss:external listener on 0.0.0.0:8084 successfully.
Start http:management listener on 8081 successfully.
Start http:dashboard listener on 18083 successfully.
EMQX Broker 4.3.11 is running now!
Eshell V11.1.8 (abort with ^G)
(emqx@127.0.0.1)1>
```

### 配置规则

使用浏览器打开 [EMQX Dashboard](http://127.0.0.1:18083/#/rules/create)，在规则引擎页面创建一条规则：

![EMQX 规则引擎](https://assets.emqx.com/images/2450022faf9e2a01426972e4cfe432b7.png)

SQL 语句为：

```sql
SELECT
    clientid,
    now_timestamp('millisecond') as now_ts_ms,
    payload.bar as bar
FROM
    "t/#"
```

然后我们在页面的底部，给规则加一个 "桥接数据到 MQTT Broker" 动作：

![桥接数据到 MQTT Broker](https://assets.emqx.com/images/faa1282d60b525ec58a92659bc164c70.png)

这个动作需要关联一个资源，我们点击右上角的 “新建资源” 来创建一个 `MQTT Bridge` 资源：

![创建 EMQX 资源](https://assets.emqx.com/images/c70c3f7c941ed1b74db9ee154b86f5df.png)

远程 Broker 地址要填写 IoTDB 的 MQTT 服务地址，即 "127.0.0.1:2883"。客户端 Id、用户名、密码都填写 root，因为 root 是 IoTDB 默认的用户名和密码。

其他选项保持默认值不变，点击 ”测试连接“ 按钮确保配置无误，然后再点击右下角的 ”新建“ 按钮创建资源。

现在返回到动作创建页面，关联资源的下拉框里自动填充了我们刚才创建的资源。

现在我们继续填写更多的动作参数：

![创建 EMQX 响应动作](https://assets.emqx.com/images/88ef0eeae52b08d1da0854d465719067.png)

IoTDB 不关心消息主题，我们填一个任意的主题：`foo`。

IoTDB 要求消息内容是一个 JSON 格式，消息内容模板可以按照上图中样式填写。详情请参见 IoTDB 的[通信服务协议文档](https://iotdb.apache.org/UserGuide/V0.13.x/API/Programming-MQTT.html)。

```json
{
 "device": "root.sg.${clientid}",
 "timestamp": ${now_ts_ms},
 "measurements": [
   "bar"
 ],
 "values": [
   ${bar}
 ]
}
```

注意其中的 "${clientid}", "${now_ts_ms}" 以及 "${bar}" 都是从规则的 SQL 语句的输出中提取的变量，所以必须保证这些变量跟 SQL 语句的 SELECT 字句对应上。

现在可以点击 ”确认“ 保存动作配置，然后再次点击 ”新建“ 完成规则的创建。

## 使用 MQTT Client 发送消息

接下来我们使用 [MQTT 客户端工具 - MQTT X](https://mqttx.app/zh)，来发送一条消息给 EMQX：

> MQTT X 是 EMQ 发布的一款完全开源的 MQTT 5.0 跨平台桌面客户端。支持快速创建多个同时在线的 MQTT 客户端连接，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的连接、发布、订阅功能及其他 MQTT 协议特性。

![MQTT 客户端工具 - MQTT X](https://assets.emqx.com/images/207d7a3cd3603ee89cdf82fcaabaecb0.png)

MQTT 客户端的连接参数里面，我们只需要填一个参数，Client ID："abc"，其他的保持默认值不变。

连接成功之后，我们发送 2 条主题为："t/1" 的消息，消息内容格式为：

```json
{
 "bar": 0.2
}
```

然后回到 EMQX Dashboard 的规则引擎页面，观察规则的命中次数，确认规则被触发了 2 次：

![EMQX Dashboard 规则引擎页面](https://assets.emqx.com/images/cf313af6faa9b4708b13bc19a99f6ebb.png)

最后我们回到命令行终端的 IoTDB 客户端窗口，使用下面的 SQL 语句查询数据：

```sql
IoTDB> SHOW TIMESERIES root.sg.abc
+---------------+-----+-------------+--------+--------+-----------+----+----------+
|     timeseries|alias|storage group|dataType|encoding|compression|tags|attributes|
+---------------+-----+-------------+--------+--------+-----------+----+----------+
|root.sg.abc.bar| null|     root.sg|   FLOAT| GORILLA|     SNAPPY|null|      null|
+---------------+-----+-------------+--------+--------+-----------+----+----------+
Total line number = 1
It costs 0.006s

IoTDB> SELECT * FROM root.sg.abc
+-----------------------------+---------------+
|                         Time|root.sg.abc.bar|
+-----------------------------+---------------+
|2022-01-10T17:39:41.724+08:00|            0.3|
|2022-01-10T17:40:32.805+08:00|            0.2|
+-----------------------------+---------------+
Total line number = 2
It costs 0.007s
IoTDB>
```

数据插入成功！

## 结语

至此，我们完成了通过 EMQX 规则引擎功能将消息持久化到 IoTDB 时序数据库。

在实际生产场景中，我们可以使用 EMQX 处理海量的物联网设备并发连接，并通过规则引擎灵活地处理业务功能，然后将设备发送的消息持久化到 IoTDB 数据库，最后使用 Hadoop/Spark、Flink 或 Grafana 等对接 IoTDB 实现大数据分析、可视化展示等。

EMQX + IoTDB 的组合是一个简洁、高效且易扩展、高可用的服务端集成方案，对于物联网设备管理和数据处理场景来说，是一个不错的选择。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
