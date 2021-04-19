
## 背景

在各类物联网项目中，设备产生的消息不仅仅作用于设备之间，还需要供业务系统使用以实现如安全审计、流量计费、数据统计、通知触发等功能，类似很容易通过以下原型系统完成：

![Artboard.png](https://static.emqx.net/images/e20e318b0a4c27eca8d1f66dac6254e7.png)



该原型中需要在 EMQ X 上维护多个数据通道，以供每个业务环节按照各自需求从 EMQ X 中获取消息数据。这种解决方案的问题在于：

- 每个业务需要与 EMQ X 建立数据通道，数据通道的建立与保持需要额外的资源开销，数据同步速度严重影响 EMQ X 高速消息交换；
- 随着业务增长，每次新增业务环节都需要牵动整个系统变更；
- 由于每个环节处理速度与时序不一样，消息量较大时部分业务会出现阻塞情况，进一步产生数据丢失、系统稳定性降低等严重后果。

以上问题与当下互联网应用中遇到的问题高度一致，即多个业务系统之间的数据集成与数据同步问题。互联网应用中普遍集成消息队列以进行削峰、限流、队列处理等操作，实现数据与业务的解耦，借助 EMQ X 提供的 RabbitMQ、Kafka、RocketMQ、Pulsar 等消息与流中间件桥接功能，物联网项目也可以使用该模型来解决以上问题。

本文以常见物联网使用场景为例，介绍了如何利用 EMQ X 消息中间件与开源流处理平台 Kafka 处理物联网海量消息数据，以高可靠、高容错的方式存储海量数据流并保证数据流的顺序进行消息数据存储，同时有效地将消息数据提供给多个业务环节使用。



## 业务场景

假设现在有一个智能门锁项目，所有门锁每间隔 1 分钟或任何时间开/关锁等门锁状态变更时上报一次门锁信息，上报 MQTT 主题如下（QoS = 1）：

```bash
devices/{client_id}/state
```

每个设备发送的数据格式为 JSON，包括门锁电量、开锁状态、操作结果等数据，内容如下：

```json
{
  "process_id": "7802441525528958",
  "action": "unlock",
  "battery": 83.4,
  "lock_state": 1,
  "version": 1.1,
  "client_id": "10083618796833171"
}
```

每个门锁均订阅一个唯一的主题，作为远程下发开锁指令，下发 MQTT 主题如下（QoS = 1）：

```bash
devices/{client_id}/command
```

下发的数据包括开锁指令、消息加密验证信息等：

```json
{
  "process_id": "7802441525528958",
  "action": "unlock",
  "nonce_str": "u7u4p0n8",
  "ts": 1574744434,
  "sign": "e9f5af7deaa28563"
}
```



上行、下行消息数据需要供以下三个业务环节使用：

- 消息通知：将开锁状态通知到门锁用户绑定的通知方式（手机短信、邮件）；
- 状态监控：分析处理门锁定时上报的状态信息，如果电量、状态异常等需触发告警通知用户；
- 安全审计：分析上下行消息数据，记录用户开锁行为，同时防范下行指令被篡改、重放等方式攻击。

该方案中，EMQ X 会将以上主题的消息统一桥接到 Kafka 供业务系统使用，实现业务系统与 EMQ X 解耦。

> client_id 为门锁 ID，同门锁连接至 EMQ X 使用的 MQTT Client ID。



## 方案介绍

**Kafka** 是由 Apache 软件基金会开发的一个开源流处理平台，由 Scala 和 Java 编写。该项目的目标是为处理实时数据提供一个统一、高吞吐、低延迟的平台。

kafka 有以下特性：

- 高吞吐量：吞吐量高达数十万高并发，支持数千个客户端同时读写；
- 低延迟：延迟最低只有几毫秒，轻松构建实时流应用程序；
- 数据可靠性：将消息数据安全地分布式存储，复制到容错集群中，严格按照队列顺序处理，提供消息事务支持，保证数据完整性和消费可靠性；
- 集群容错性：多节点副本中，允许 n-1 个节点失败
- 可扩展性：支持集群动态扩展。

该方案中集成 Kafka 为 EMQ X 消息服务器与应用程序之间的消息传递提供消息队列与消息总线。生产者（EMQ X）往队列末尾添加数据，每个消费者（业务环节）依次读取数据然后自行处理，这种架构兼顾了性能与数据可靠性，并有效降低系统复杂度、提升系统扩展性。该方案原型如下：

![Artboard Copy 12.png](https://static.emqx.net/images/3d0fa8599ebec0f272ef9bb6a3185d01.png)



## EMQ X Enterprise 安装

### 安装

> 如果您是 EMQ X 新手用户，推荐通过 [EMQ X 指南](https://docs.emqx.io/tutorial/v3/en/) 快速上手

访问 [EMQ 官网](https://www.emqx.cn/downloads) 下载适合您操作系统的安装包，**由于数据持久化是企业功能，您需要下载 EMQ X 企业版（可以申请 License 试用）** 写本文的时候 EMQ X 企业版最新版本为 v3.4.4，下载 zip 包的启动步骤如下 ：

```bash
## 解压下载好的安装包
unzip emqx-ee-macosx-v3.4.4.zip
cd emqx

## 将 License 文件复制到 EMQ X 指定目录 etc/, License 需自行申请试用或通过购买授权获取
cp ../emqx.lic ./etc

## 以 console 模式启动 EMQ X
./bin/emqx console
```



### 修改配置

本文中需要用到的配置文件如下：

1. License 文件，EMQ X 企业版 License 文件，使用可用的 License 覆盖：

```
etc/emqx.lic
```

2. EMQ X Kafka 消息存储插件配置文件，用于配置 Kafka 连接信息、数据桥接主题：

```bash
etc/plugins/emqx_bridge_kafka.conf
```

根据部署实际情况填写插件配置信息如下，其余配置项请熟读配置文件做出调整或直接使用默认配置即可：

```bash
## 连接地址
bridge.kafka.servers = 127.0.0.1:9092

## 需要处理的 Hooks 由于我们使用 QoS 1 的进行消息传送，可以使用 ack hooks 
## 注释其他无关事件、消息 Hooks

## bridge.kafka.hook.client.connected.1     = {"topic":"client_connected"}
## bridge.kafka.hook.client.disconnected.1  = {"topic":"client_disconnected"}
## bridge.kafka.hook.session.subscribed.1   = {"filter":"#", "topic":"session_subscribed"}
## bridge.kafka.hook.session.unsubscribed.1 = {"filter":"#", "topic":"session_unsubscribed"}
## bridge.kafka.hook.message.deliver.1      = {"filter":"#", "topic":"message_deliver"}

## filter 为需要处理的 MQTT 主题, topoc 为写入的 Kafka 主题
## 注册多个 Hooks 实现上行、下行消息处理

## 上报指令选择 publish hooks
bridge.kafka.hook.message.publish.1        = {"filter":"devices/+/state", "topic":"message_state"}

## 下发指令选择 acked hooks，确保消息抵达才入库
bridge.kafka.hook.message.acked.1       = {"filter":"devices/+/command", "topic":"message_command"}
```



## Kafka 安装与初始化

通过 Docker 进行安装 Kafka，映射数据 `9092` 端口供连接使用，Kafka 依赖 Zookeeper，下面提供完整安装命令：

```bash
## 安装 Zookeeper
docker run -d --name zookeeper -p 2181 -t wurstmeister/zookeeper

## 安装并配置 Kafka
docker run -d --name kafka --publish 9092:9092 \
		--link zookeeper --env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
		--env KAFKA_ADVERTISED_HOST_NAME=127.0.0.1 \
		--env KAFKA_ADVERTISED_PORT=9092 \
		wurstmeister/kafka:latest
```

**预先在 Kafka 创建需要使用的主题：**

```bash
## 进入 Kafka Docker 容器
docker exec -it kafka bash

## 上行数据主题 message_state
kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic message_state

## 下行数据主题 message_command
kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic message_command
```



**至此，可以重启 EMQ X 并启动插件以应用以上配置**:

```bash
./bin/emqx stop

./bin/emqx start

## 或使用 console 模式可以看到更多信息
./bin/emqx console

## 启动插件
./bin/emqx_ctl plugins load emqx_bridge_kafka

## 启动成功后会有以下提示
Plugin load emqx_bridge_kafka loaded successfully.
```



## 模拟测试

### 使用 kafka-console-consumer 启动消费

该方案中三个业务环节详细实现本文不再赘述，本文仅需保证消息写入 Kafka 即可，可以使用 Kafka 自带的消费命令查看主题内的数据：

```bash
## 进入 Kafka Docker 容器
docker exec -it kafka bash

## 上行数据主题
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic message_state --from-beginning

## 开启另外一个窗口查看下行数据主题
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic message_command --from-beginning
```

命令成功执行后将阻塞等待消费该主题的数据，我们继续后续操作。



### 模拟测试数据收发

通过 **EMQ X 管理控制台**中的 **WebSocket** 工具可以模拟智能门锁上/下行业务数据。浏览器打开 `http://127.0.0.1:1883` 进入 **EMQ X 管理控制台**，打开 **Tool** -> **WebSocket** 功能，输入连接信息建立 MQTT 连接模拟门锁设备。连接信息里 **Client ID** 根据业务指定，本文使用 `10083618796833171` 。

### 订阅下行控制主题

根据业务需求，需订阅门锁专属下行控制主题 `devices/{client_id}/command`，此处需订阅 `devices/10083618796833171/command` 主题并**设置 QoS = 1**：

![image20191126150024089.png](https://static.emqx.net/images/0f345321939c4a4033508a6457a1cccc.png)



### 模拟下发指令

向门锁控制主题 `devices/{client_id}/command` 发送开锁指令，此处下发数据为：

- 主题：`devices/10083618796833171/command`

- QoS：1

- payload:

  ```json
  {
    "process_id": "7802441525528958",
    "action": "unlock",
    "nonce_str": "u7u4p0n8",
    "ts": 1574744434,
    "sign": "e9f5af7deaa28563"
  }
  ```

下发成功后管理控制台 **Publish** 界面可以收到一条消息：

![image20191126150044511.png](https://static.emqx.net/images/ee02694f902b7584ecb89f97293eb485.png)

同时 Kafka `message_command` 主题消费者将收到一条或多条消息(**EMQ X ack hooks 触发次数以实际收到消息客户端数量为准**)，消息为 JSON 格式，内容经格式化后如下：

```json
{
  "client_id": "10083618796833171",
  "username": "",
  "from": "10083618796833171",
  "topic": "devices/10083618796833171/command",
  "payload": "eyAgICJwcm9jZXNzX2lkIjogIjc4MDI0NDE1MjU1Mjg5NTgiLCAgICJhY3Rpb24iOiAidW5sb2NrIiwgICAibm9uY2Vfc3RyIjogInU3dTRwMG44IiwgICAidHMiOiAxNTc0NzQ0NDM0LCAgICJzaWduIjogImU5ZjVhZjdkZWFhMjg1NjMiIH0=",
  "qos": 1,
  "node": "emqx@127.0.0.1",
  "ts": 1574751635845
}
```

该条消息包含了 MQTT 接收/发布客户端信息与 Base64 编码后的 Payload 数据：

- client_id: 接收客户端 client_id
- username: 接受客户端 username
- from: 发布客户端 client_id
- topic: 消息发布目标主题
- payload: 经 Base64 编码后的消息 Payload
- qos: 消息 QoS
- node: 消息处理节点
- ts: hooks 毫秒级触发时间戳



### 模拟上报状态

向门锁控制主题 `devices/{client_id}/state` 发送状态数据，此处发布数据为：

- 主题：`devices/10083618796833171/state`

- QoS：1

- payload:

  ```json
  {
    "process_id": "7802441525528958",
    "action": "unlock",
    "battery": 83.4,
    "lock_state": 1,
    "version": 1.1,
    "client_id": "10083618796833171"
  }
  ```



上报成功后 Kafka `message_state` 消费者将收到一条消息（**EMQ X publish hooks 触发次数与发布消息有关，与消息主题是否被订阅以及订阅数量无关**）,消息为 JSON 格式，内容经格式化后如下：

```json
{
  "client_id": "10083618796833171",
  "username": "",
  "topic": "devices/10083618796833171/state",
  "payload": "eyAgICJwcm9jZXNzX2lkIjogIjc4MDI0NDE1MjU1Mjg5NTgiLCAgICJhY3Rpb24iOiAidW5sb2NrIiwgICAiYmF0dGVyeSI6IDgzLjQsICAgImxvY2tfc3RhdGUiOiAxLCAgICJ2ZXJzaW9uIjogMS4xLCAgICJjbGllbnRfaWQiOiAiMTAwODM2MTg3OTY4MzMxNzEiIH0=",
  "qos": 1,
  "node": "emqx@127.0.0.1",
  "ts": 1574753026269
}
```

该条消息仅包含 MQTT 发布客户端信息与 Base64 编码后的 Payload 数据：

- client_id: 发布客户端 client_id
- username:发布客户端 username
- topic: 消息发布目标主题
- payload: 经 Base64 编码后的消息 Payload
- qos: 消息 QoS
- node: 消息处理节点
- ts: hooks 毫秒级触发时间戳

至此，我们成功完成 EMQ X 桥接消息至 Kafka 所有步骤，业务系统接入 Kafka 后可以根据消费到的消息数量、消息发布者/订阅者的 client_id 以及消息 payload 内容进行业务判断，实现所需业务功能。

## 性能测试

如果读者对该方案的性能感兴趣，可以采用 [MQTT-JMeter](https://github.com/emqx/mqtt-jmeter) 插件对其进行测试。需要注意的是，读者需要在性能测试过程中保证做好 EMQ 集群、Kafka 集群、Kafka 的消费者，以及 JMeter 测试集群相关的优化与配置，才可以得到相关配置下正确的最佳性能测试结果。

## 总结

通过本文读者可以了解到 EMQ X + Kafka 物联网消息处理方案为消息通信与业务处理带来的重要作用，利用该方案可以搭建松耦合、高性能、高容错的物联网消息处理平台，实现数据高效、安全地处理。

本文编码实现具体的业务逻辑，读者可以根据本文提供的业务原型与系统架构进行扩展。由于 RabbitMQ、RocketMQ、Pulsar 等 EMQ X 已经支持的消息/流处理中间的在物联网项目中集成的架构思想与 Kafka 相近，读者也可以以本文作为参考，根据自身技术栈自由选用相关组件进行方案集成。


