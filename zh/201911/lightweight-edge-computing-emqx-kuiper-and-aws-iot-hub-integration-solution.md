## 背景

本文以一个常见的物联网使用场景为案例，介绍了如何利用边缘计算来实现对业务的快速、低成本和有效地处理。

在各类物联网项目中，比如智能楼宇项目，需要将楼宇的数据（比如电梯、燃气、水电等）进行采集和分析。一种解决方案是将所有的设备直接接入在云端的物联网平台，类似于像 AWS IoT 或者 Azure IoT Hub。这种解决方案的问题在于，

- 数据处理时延较长：通过 Internet 传输和云端的处理后返回给设备，所需时间较长
- 数据传输和存储成本：通过 Internet 传输需要带宽，对于大规模连接的物联网项目来说，耗费的带宽会相当可观
- 数据的安全性：有些物联网的数据会相当敏感，全部通过物联网传输的话会有风险

为了解决以上的问题，业界提出了边缘计算的方案，边缘计算的核心就在于把数据进行就近处理，避免不必要的时延、成本和安全问题。

## 业务场景

假设现有一组设备，组中的每个设备有一个 id，通过 MQTT 协议往 MQTT 消息服务器上相应的主题发送数据。主题的设计如下，其中 {device_id} 为设备的 id。

```
devices/{device_id}/messages
```

每个设备发送的数据格式为 JSON，发送的通过该传感器采集的温度与湿度数据。

```json
{
    "temperature": 30, 
    "humidity" : 20
}
```

现在需要实时分析数据，并提出以下的需求：对每个设备的温度数据按照每 10 秒钟计算平均值(``t_av``)，并且记下 10 秒钟内的最大值 (``t_max``)、最小值(``t_min``) 和数据条数(``t_count``)，计算完毕后将这 4 个结果进行保存，以下为样例结果数据：

```json
[
    {
        "device_id" : "1", "t_av" : 25,  "t_max" : 45, "t_min" : 5, "t_count" : 2
    },
    {
        "device_id" : "2", "t_av" : 25,  "t_max" : 45, "t_min" : 5, "t_count" : 2
    },
    ...
]
```

## 方案介绍

如下图所示，采用边缘分析/流式数据处理的方式，在边缘端我们采用了 EMQX 的方案，最后将计算结果输出到 AWS IoT 中。

![emqx_aws.png](https://static.emqx.net/images/ef141d43e1c05f0f35d45f334730febd.png)

- EMQX Edge 可以接入各种协议类型的设备，比如 MQTT、CoAP、LwM2M 等，这样用户可以不需要关心协议适配方面的问题；另外它本身也比较轻量级，适合部署在边缘设备上
- EMQX Kuiper 是 EMQ 发布的基于 SQL 的轻量级边缘流式数据分析引擎，安装包只有约 7MB，非常适合于运行在边缘设备端
- AWS IoT 提供了比较全的设备接入和数据分析的方案，此处用于云端的结果数据接入，以及应用所需的结果数据分析

## 实现步骤

### 安装 EMQX Edge & Kuiper

- 写本文的时候，EMQX Edge 的最新版本是4.0，用户可以通过 Docker 来安装和启动 EMQX Edge

  ```shell
  # docker pull emqx/emqx-edge
  # docker run -d --name emqx -p 1883:1883  emqx/emqx-edge:latest
  # docker ps
  CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS                                                                                                           NAMES
  a348e3ac150c        emqx/emqx-edge:latest   "/usr/bin/docker-entr"   3 seconds ago       Up 2 seconds        4369/tcp, 5369/tcp, 6369/tcp, 8080/tcp, 8083-8084/tcp, 8883/tcp, 11883/tcp, 0.0.0.0:1883->1883/tcp, 18083/tcp   emqx
  ```

  用户可以通过 ``telnet`` 命令来判断是否启动成功，如下所示。

  ```shell
  # telnet localhost 1883
  Trying 127.0.0.1...
  Connected to localhost.
  Escape character is '^]'.
  ```

- 安装、启动 Kuiper

  点击[这里](https://github.com/emqx/kuiper/releases)下载最新版 Kuiper，并解压。在写本文的时候，Kuiper 最新版本为 0.0.3。

  ```shell
  # unzip kuiper-linux-amd64-0.0.3.zip
  # cd kuiper
  # bin/server
  Serving Kuiper server on port 20498
  ```

  如果无法启动，请查看日志文件 ``log/stream.log``。

### 创建流

Kuiper 提供了一个命令用于管理流和规则，用户可以通过在命令行窗口中敲入 ``bin/cli`` 查看有哪些子命令及其帮助。``cli`` 命令缺省连接的是本地的 Kuiper 服务器，``cli`` 命令也可以连接到别的 Kuiper 服务器，用户可以在 ``etc/client.yaml``配置文件中修改连接的 Kuiper 服务器。用户如果想了解更多关于命令行的信息，可以参考[这里](https://github.com/emqx/kuiper/tree/master/docs/cli)。

创建流定义：创建流的目的是为了定义发送到该流上的数据格式，类似于在关系数据库中定义表的结构。 Kuiper 中所有支持的数据类型，可以参考[这里](https://github.com/emqx/kuiper/blob/master/docs/streams.md)。

```shell
# cd kuiper
# bin/cli create stream demo '(temperature float, humidity bigint) WITH (FORMAT="JSON", DATASOURCE="devices/+/messages")'
```

上述语句在 Kuiper 中创建了一个名为 demo 的流定义，包含了两个字段，分别为 temperature 和 humidity，数据源为订阅 MQTT 的主题 ``devices/+/messages``，这里请注意采用了通配符 ``+``，用于订阅不同设备的消息。该数据源所对应的 MQTT 服务器地址在配置文件 ``etc/mqtt_source.yaml``中，可以根据所在的服务器地址进行配置。如下图所示，配置 ``servers`` 项目。

```yaml
#Global MQTT configurations
default:
  qos: 1
  sharedsubscription: true
  servers: [tcp://127.0.0.1:1883]
```

用户可以在命令行中敲入 ``describe`` 子命令来查看刚创建好的流定义。

```shell
# bin/cli describe stream demo
Connecting to 127.0.0.1:20498
Fields
--------------------------------------------------------------------------------
temperature	float
humidity	bigint

FORMAT: JSON
DATASOURCE: devices/+/messages
```

### 数据业务逻辑处理

Kuiper 采用 SQL 实现业务逻辑，每10秒钟统计温度的平均值、最大值、最小值和次数，并根据设备 ID 进行分组，实现的 SQL 如下所示。

```sql
SELECT avg(temperature) AS t_av, max(temperature) AS t_max, min(temperature) AS t_min, COUNT(*) As t_count, split_value(mqtt(topic), "/", 1) AS device_id FROM demo GROUP BY device_id, TUMBLINGWINDOW(ss, 10)
```

这里的 SQL 用了四个聚合函数，用于统计在10秒钟窗口期内的相关值。

- ``avg``：平均值
- ``max``：最大值
- ``min``：最小值
- ``count``：计数

另外还使用了两个基本的函数

- ``mqtt``：消息中取出 MQTT 协议的信息，``mqtt(topic)`` 就是取得当前取得消息的主题名称
- ``split_value``：该函数将第一个参数使用第二个参数进行分割，然后第三个参数指定下标，取得分割后的值。所以函数 ``split_value("devices/001/messages", "/", 1) ``调用就返回``001``

``GROUP BY`` 跟的是分组的字段，分别为计算字段 ``device_id``；时间窗口 ``TUMBLINGWINDOW(ss, 10)``，该时间窗口的含义为每10秒钟生成一批统计数据。

### 调试 SQL

在正式写规则之前，我们需要对规则进行调试，Kuiper 提供了 SQL 的调试工具，可以让用户非常方便地对 SQL 进行调试。

- 进入 kuiper 安装目录，并运行 ``bin/cli query``

- 在出现的命令行提示符中输入前面准备好的 SQL 语句。

  ```shell
  # bin/cli query
  Connecting to 127.0.0.1:20498
  kuiper > SELECT avg(temperature) AS t_av, max(temperature) AS t_max, min(temperature) AS t_min, COUNT(*) As t_count, split_value(mqtt(topic), "/", 1) AS device_id FROM demo GROUP BY device_id, TUMBLINGWINDOW(ss, 10)
  query is submit successfully.
  kuiper >
  ```

  在日志文件 ``log/stream.log`` 中，可以看到创建了一个名为 ``internal-kuiper_query_rule`` 的临时规则。

  ```
  ...
  time="2019-11-12T11:56:10+08:00" level=info msg="The connection to server tcp://10.211.55.6:1883 was established successfully" rule=internal-kuiper_query_rule
  time="2019-11-12T11:56:10+08:00" level=info msg="Successfully subscribe to topic devices/+/messages" rule=internal-kuiper_query_rule
  ```

  值得注意的是，这个名为 ``internal-kuiper_query_rule`` 的规则是通过 ``query`` 创建的，服务器端每5秒钟会检测一下 ``query`` 客户端是否在线，如果``query`` 客户端发现有超过10秒钟没有反应（比如被关闭），那么这个内部创建的 ``internal-kuiper_query_rule`` 规则会被自动删除，被删除的时候在日志文件中会打印如下的信息。

  ```
  ...
  time="2019-11-12T12:04:08+08:00" level=info msg="The client seems no longer fetch the query result, stop the query now."
  time="2019-11-12T12:04:08+08:00" level=info msg="stop the query."
  time="2019-11-12T12:04:08+08:00" level=info msg="unary operator project cancelling...." rule=internal-kuiper_query_rule
  ...
  ```

- 发送测试数据

  通过任何的测试工具，向 EMQX Edge 发送以下的测试数据。笔者在测试过程中用的是 [JMeter](https://www.emqx.com/zh/blog/introduction-to-the-open-source-testing-tool-jmeter) 的 [MQTT 插件](https://github.com/emqx/mqtt-jmeter)，因为基于 JMeter 可以做一些比较灵活的自动数据生成，业务逻辑控制，以及大量设备的模拟等。用户也可以直接使用 ``mosquitto`` 等其它客户端进行模拟。

  - 主题：``devices/$device_id/messages``，其中``$device_id`` 为下面数据中的第一列
  - 消息：``{"temperature": $temperature, "humidity" : $humidity}``, 其中``$temperature`` 和 ``$humidity`` 分别为下面数据中的第二列和第三列

  ```
  #device_id, temperature, humidity
  1,20,30
  2,31,40
  1,35,50
  2,20,30
  1,80,90
  2,45,20
  1,10,90
  2,12,30
  1,65,35
  2,55,32
  ```

  我们可以发现发送了模拟数据后，在 ``query`` 客户端命令行里在两个10秒的时间窗口里打印了两组数据。这里输出的结果条数跟用户发送数据的频率有关系，如果 Kuiper 在一个时间窗口内接受到所有的数据，那么只打印一条结果。

  ```json
  kuiper > [{"device_id":"1","t_av":45,"t_count":3,"t_max":80,"t_min":20},{"device_id":"2","t_av":25.5,"t_count":2,"t_max":31,"t_min":20}]
  
  [{"device_id":"2","t_av":37.333333333333336,"t_count":3,"t_max":55,"t_min":12},{"device_id":"1","t_av":37.5,"t_count":2,"t_max":65,"t_min":10}]
  ```

### 创建、提交规则

完成了 SQL 的调试之后，开始配置规则文件，将结果数据通过 Kuiper 的 MQTT Sink 发送到远程的 AWS IoT 中。 在 AWS IoT 中，用户需要先创建好以下内容，

- 设备：代表处理设备数据的网关，该网关安装了 Kuiper，网关在把相关相关数据处理完毕后，将结果发送到 AWS 云端。此处创建的名称为 demo，如下图所示。

![aws_device.png](https://static.emqx.net/images/f3fbfca657ce289ec90cc6d9f7c88b96.png)

- 设备连接证书与密钥：AWS 的物联网设备通过证书来连接，保证其安全性。在创建设备的过程中，AWS会生成的以下三个文件。这里会用到的是证书与私钥。

  - 证书：类似于 ``d3807d9fa5-certificate.pem``
  - 私钥：类似于 ``d3807d9fa5-private.pem.key``
  - 公钥：类似于 ``d3807d9fa5-public.pem.key``

  关于这方面更多的信息，请参考 AWS [创建设备的文档](https://docs.aws.amazon.com/iot/latest/developerguide/register-device.html)。

**编写 Kuiper 规则文件**

规则文件是一个文本文件，描述了业务处理的逻辑（前面已经调试好的 SQL 语句），以及 sink 的配置（消息处理结果的发送目的地）。连接 AWS IoT 的大部分信息都已经在前文中描述。 Kuiper 的测试结果将被发送到 AWS IoT设备的 ``devices/result`` 主题下。

```json
{
  "sql": "SELECT avg(temperature) AS t_av, max(temperature) AS t_max, min(temperature) AS t_min, COUNT(*) As t_count, split_value(mqtt(topic), \"/\", 1) AS device_id FROM demo GROUP BY device_id, TUMBLINGWINDOW(ss, 10)",
  "actions": [
    {
      "log": {}
    },
    {
      "mqtt": {
        "server": "ssl://xyz-ats.iot.us-east-1.amazonaws.com:8883",
        "topic": "devices/result",
        "qos": 1,
        "clientId": "demo_001",
        "certificationPath": "/var/aws/d3807d9fa5-certificate.pem",
        "privateKeyPath": "/var/aws/d3807d9fa5-private.pem.key"
      }
    }
  ]
}
```

**通过 Kuiper 命令行创建规则**

```shell
# bin/cli create rule rule1 -f rule1.txt
Connecting to 127.0.0.1:20498
Creating a new rule from file rule1.txt. 
Rule rule1 was created.

```

在日志文件中可以查看规则的运行连接情况，如果配置项都正确的话，应该可以看到到 AWS IoT 的连接建立成功。

```
......
time="2019-11-13T17:41:19+08:00" level=info msg="The connection to server tcp://10.211.55.6:1883 was established successfully" rule=rule1
time="2019-11-13T17:41:19+08:00" level=info msg="Successfully subscribe to topic devices/+/messages" rule=rule1
time="2019-11-13T17:41:20+08:00" level=info msg="The connection to server ssl://xyz-ats.iot.us-east-1.amazonaws.com:8883 was established successfully" rule=rule1
......

```

- 通过 AWS IoT 提供的 MQTT Client 工具，订阅设备的``devices/result``主题。并往本地的 EMQX Edge 上发送模拟数据。经过 Kuiper 处理后，相应的处理结果被发送到了 AWS IoT 中。如下图所示，收到了两次测试结果（第一次结果被折叠）。

![aws_iot_result.png](https://static.emqx.net/images/d26d4b4ef111c63b2cd56dc2d29a2847.png)

用户可以通过 AWS IoT Rule 将分析结果存储到 Amazon DynamoDB 数据库或者其它服务中，前端的应用程序可以通过读取 DynamoDB 中的数据来呈现给终端用户，具体请参考 [ Amazon DynamoDB 文档](https://docs.aws.amazon.com/iot/latest/developerguide/iot-ddb-rule.html)。

## 总结

通过本文，读者可以了解到利用 EMQX 在边缘端的解决方案可以非常快速、灵活地开发出基于边缘数据分析的系统，实现数据低时延、低成本和安全的处理。

AWS IoT 也提供了 Greengrass 的边缘解决方案，与 AWS Greengrass 相比，Kuiper 方案更加轻量级，业务逻辑的实现方式（基于 SQL）在编程上也相对更加简单。AWS Greengrass 提供了基于 Lambada 的编程模型，通过提供不同编程语言的 SDK 来实现边缘端的数据分析，以及往 AWS IoT 的分析结果上传，因此在业务逻辑实现的灵活性上会更好。最后，与 Greengrass 只能连接 AWS IoT 不同，Kuiper 在与不同的第三方 IoT 平台的集成的灵活性上也更好。

如果有兴趣了解更多关于边缘流式数据分析的内容，请参考 [Kuiper 开源项目](https://github.com/emqx/kuiper)。
