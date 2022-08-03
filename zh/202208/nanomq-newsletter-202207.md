7 月，NanoMQ 继续保持稳步更新。v0.10.0 于 8 月初正式发布（[https://github.com/emqx/nanomq/releases/tag/0.10.1](https://github.com/emqx/nanomq/releases/tag/0.10.1)）。此版本主要增强了桥接功能，新增了发布消息的 HTTP API。同时还为 NanoSDK 增加了 MQTT 5.0 支持。各项性能优化和缺陷修复也在持续进行中。

## 桥接功能更新

桥接功能在 0.10 版本得到了重大更新，增加了多路桥接、AWS IoT Core 内置桥接等功能。这些更新同时也影响了配置文件的格式，v0.10 与 v0.9.0 之前的桥接配置文件（nanomq_bridge.conf）不再兼容，用户升级时需要注意更新配置文件格式。

### 多路 MQTT 桥接配置

在物联网领域，异构计算和计算卸载是常见的场景，端侧各类无线传感网络的数据往往需要与多个云端同步或被多个应用重复消费。[MQTT broker](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 是解决数据流可重用需求的捷径，而 NanoMQ 作为主要针对边缘计算场景的消息服务，多云桥接也是用户普遍需要的功能。在 v0.9.0 之前，NanoMQ 的 MQTT 桥接只支持单一目标。多路 MQTT 桥接经过测试验证后在 0.10 版本正式推出，能够支持用户通过自定义桥接命名来让 NanoMQ 同时与多个远端 MQTT 服务进行实时数据同步。

![多路 MQTT 桥接](https://assets.emqx.com/images/2fefca47412600ccc528301c57f5a922.png)

比如我们想要让 NanoMQ 将特定主题（msg1/#, msg2/#）的消息都同步到云端，同时从云端的主题（cmd/topic1）收取消息并转发给本地的设备。简单配置示例如下：

```
## Take EMQX & EMQX cloud as example ##
## 以同时桥接到 EMQX 公共服务器和 EMQX Cloud 为例，配置桥接URL ##
bridge.mqtt.emqx.address=mqtt-tcp://broker.emqx.io:1883
bridge.mqtt.cloud.address=mqtt-tcp://emqx.cloud:1883

## 设置桥接的MQTT协议版本，可选MQTT V4和MQTT V5 ##
bridge.mqtt.emqx.proto_ver=4
bridge.mqtt.cloud.proto_ver=4

## 开启桥接状态 ##
bridge.mqtt.emqx.bridge_mode=true
bridge.mqtt.cloud.bridge_mode=true

## 设置桥接客户端的Client ID ##
bridge.mqtt.emqx.clientid=bridge_client
bridge.mqtt.cloud.clientid=bridge_client

## 设置桥接客户端的心跳间隔 ##
bridge.mqtt.emqx.keepalive=60
bridge.mqtt.cloud.keepalive=60

## 设置需要上行同步数据的主题 ##
bridge.mqtt.emqx.forwards=msg1/#,msg2/#
bridge.mqtt.cloud.forwards=msg1/#,msg2/#

## 设置需要下行同步数据的主题 ##
bridge.mqtt.emqx.subscription.1.topic=cmd/topic1
bridge.mqtt.cloud.subscription.1.topic=cmd/topic1
```

之后启动 NanoMQ，就会根据配置的远端 MQTT 服务的 URL 来自动启动桥接通道，并管理和监控连接健康状态和同步数据。

特别提醒：增加了多路桥接功能后的版本使用不同格式的桥接配置文件，所以 v0.10 不再和 v0.9.0 之前的 nanomq_bridge.conf 兼容。

### AWS Bridge

AWS IoT Core 是在欧美广泛使用的公有云 IoT 服务之一。但由于其与标准 MQTT 连接多有不同，且不支持 QoS 2 通信质量，让许多使用标准 MQTT SDK 的客户端设备难以连接和享受出海服务。

NanoMQ 0.10 版本增加了内置 AWS 桥接功能来解决这一问题。**NanoMQ** 负责将接收到的指定 *topic* 的数据转发到远端 **AWS IoT MQTT Broker**，并从 **AWS IoT MQTT Broker** 订阅指定 *topic*。

使用此内置桥接功能需要默认环境里已经安装了 AWS 的 IoT SDK：

#### 安装AWS SDK

```
## 下载源码
wget https://github.com/aws/aws-iot-device-sdk-embedded-C/releases/download/202108.00/aws-iot-device-sdk-embedded-C-202108.00.zip

## 解压
unzip aws-iot-device-sdk-embedded-C-202108.00.zip

## 编译
cd aws-iot-device-sdk-embedded-C
mkdir build
cmake -G Ninja -DBUILD_DEMOS=OFF -DCMAKE_C_STANDARD=99 -DINSTALL_TO_SYSTEM=ON ..
ninja

## 安装到系统
sudo ninja install 
sudo cp ../demos/logging-stack/logging_*.h  /usr/local/include/aws/
sudo ldconfig
```

然后配置 NanoMQ 默认路径下的配置文件/etc/nanomq_aws_bridge.conf，或通过命令行启动 NanoMQ 时指定配置文件 nanomq start --bridge <nanomq_aws_bridge.conf>

#### 配置参数

- 桥接模式开关(默认false关闭)

  ```
  bridge.mqtt.aws.bridge_mode=true
  ```

- AWS IoT Core Endpoint 地址

  ```
  bridge.mqtt.aws.host=a2zegtl0x5owup-ats.iot.us-west-2.amazonaws.com
  bridge.mqtt.aws.port=8883
  ```

- MQTT 协议版本

  ```
  bridge.mqtt.aws.proto_ver=4
  ```

- 转发 Topic (多个 topic 用逗号,隔开)

  ```
  bridge.mqtt.aws.forwards=topic_1,topic_2
  ```

- 订阅 Topic

  ```
  bridge.mqtt.aws.subscription.1.topic=cmd/topic1
  bridge.mqtt.aws.subscription.1.qos=1
  ...
  bridge.mqtt.aws.subscription.{n}.topic=cmd/topicn
  bridge.mqtt.aws.subscription.{n}.qos=1
  ```

NanoMQ 就能够与 AWS IoT Core 建立桥接，进行数据同步。

由于 AWS 的 C 嵌入式 SDK 不支持跨平台，所以目前此功能并未打包进二进制安装包中。需要使用 AWS 桥接的用户需通过以下命令自行编译安装 NanoMQ 的 AWS IoT Core 桥接功能。

```
cmake -G Ninja .. -DENABLE_AWS_BRIDGE=ON

sudo ninja install
```

## 新增 HTTP  API

MQTT 是基于异步模式设计的消息协议，但在许多场景里仍然会和许多第三方应用通过 HTTP REST API 交互，这就需要 MQTT 服务能够同时兼容支持并转换异步和同步模式。所以 NanoMQ 在 0.10 版本响应用户的呼声也加入了支持通过 HTTP API 进行发布消息的功能。

简单的使用方式示例如下：

#### HTTP 发布消息

/api/v4/mqtt/publish

```
$ curl -i --basic -u admin:public -X POST "http://localhost:8081/api/v4/mqtt/publish" -d \
'{"topic":"a/b/c", "payload":"Hello World", "qos":1, "retain":false, "clientid":"example"}}'

## NanoMQ回复：
{"code":0}
```

#### HTTP 批量发布消息

/api/v4/mqtt/publish_batch

```
$ curl -i --basic -u admin:public -X POST "http://localhost:8081/api/v4/mqtt/publish_batch" -d '[{"topic":"a/b/c","payload":"Hello World","qos":1,"retain":false,"clientid":"example"},{"topic":"a/b/c","payload":"Hello World Again","qos":0,"retain":false,"clientid":"example"}]'

## NanoMQ回复：
{"data":[{"topic":"a/b/c","code":0},{"topic":"a/b/c","code":0}],"code":0}
```

## NanoSDK 支持 MQTT 5.0

NanoSDK 在此前支持了以 QUIC 作为 MQTT 传输层来解决弱网环境和网络切换等问题。

7 月中，此项目得到了重大更新：新发布的 NanoSDK 0.7.0 版本支持 MQTT 5.0，并增加更多针对 MQTT 用户的高度封装 API。目前 NanoSDK 已经能够支持 MQTT 5.0 协议的大部分功能特性。

## NanoMQ 命令行工具分离

NanoMQ 0.10 还有一个改动需要用户注意，此版本开始将原有的命令行工具箱与 MQTT Broker 服务分离，从不同的命令入口启动。

原 NanoMQ 启动命令：

```
## NanoMQ Broker：
nanomq broker start
## NanoMQ 客户端：
nanomq pub --url "mqtt-tcp://broker.emqx.io:1883" -t topic -m hello
```

0.10 版本后的启动命令：

```
## NanoMQ Broker：
nanomq start
## NanoMQ 客户端：
nanomq_cli pub --url "mqtt-tcp://broker.emqx.io:1883" -t topic -m hello
```

## 即将到来 ：MQTT 5.0 + MQTT over QUIC 桥接

得益于 NanoSDK 对 MQTT 5.0 和 QUIC 传输层的支持，NanoMQ 的桥接功能即将在 0.11 版本得到重大升级。用户将能够选择 MQTT 5.0 版本进行桥接，或者使用 QUIC 作为桥接连接的传输层，从而为无法集成  QUIC SDK 或者没有合适 MQTT over QUIC SDK 选择的本地端侧设备提供传输层转换，以配合 EMQX 5.0 发挥 QUIC 在弱网环境下的优势。

关于 QUIC 的详解请参考: [MQTT over QUIC：物联网消息传输还有更多可能 ](https://www.emqx.com/zh/blog/mqtt-over-quic)


<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
