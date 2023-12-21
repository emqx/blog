8 月，NanoMQ 继续保持稳步更新。最新的 0.11.0 版本已于 8月底正式发布（[https://github.com/nanomq/nanomq/releases/tag/0.11.0](https://github.com/nanomq/nanomq/releases/tag/0.11.0)）。此版本继续增强了桥接功能，增加了 MQTT 5.0 + MQTT over QUIC 桥接模式，新增和修复了对已连接客户端状态进行监控和查询的 HTTP API。此外各项性能优化和缺陷修复也在持续进行中。

## 桥接功能更新

作为 NanoMQ 最为广泛使用的功能之一，桥接功能本月得到重大更新升级，新增了 2 种桥接模式：MQTT over QUIC 桥接和 MQTT 5.0 协议桥接。

### MQTT over QUIC 桥接

继 EMQX 5.0 全球率先发布 MQTT over QUIC 支持后，NanoMQ 项目也为了降低此功能的使用门槛在 0.11 版本推出了 MQTT over QUIC 桥接功能。目前 NanoSDK 已支持以 QUIC 协议作为 MQTT 的传输层，因此与其兼容的 NanoMQ 项目的桥接功能也一并得到了无缝升级。用户可以使用 QUIC 作为 MQTT 协议的传输层来与 EMQX 5.0 消息服务建立桥接进行数据同步，从而为无法集成或找到合适的 MQTT over QUIC SDK 的端侧设备和难以修改固件的嵌入式设备提供在 IoT 场景利用 QUIC 协议优势的捷径。

![MQTT over QUIC 桥接](https://assets.emqx.com/images/cb49af66a1494dfc036a99703835bc58.png)

<center>桥接结构示意图</center>

在需要与云端 MQTT 服务进行数据同步的各种物联网场景中，通过 NanoMQ 的多协议接入能力，可以将其作为边缘消息总线和统一的数据空间，统一汇聚诸如 HTTP、MQTT 3.1.1/5.0、WebSocket、nanomsg/nng  和 ZeroMQ 等常用的 broker/brokerless 消息协议，再由 NanoMQ 内部强大的 Actor 消息处理模型转化成标准的 MQTT 消息后，通过 QUIC 传输层的 0RTT 快速重连和被动地址切换等功能来克服网际漫游、弱网传输和 TCP 队头阻塞等各类常见的物联网连接问题。还可以通过 NanoMQ 的规则引擎对数据做重定向、本地缓存或持久化。依靠 EMQX+NanoMQ 的云边一体化的消息架构，用户能够快速且低成本的在泛物联网场景中完成跨时空地域的数据采集和同步需求。

**如何使用 MQTT over QUIC 桥接功能**

目前 NanoMQ 的 QUIC 模组处于默认关闭状态，用户如需使用需通过编译选项打开后安装使用，完整的下载和编译安装命令可以参考：

```
git clone https://github.com/nanomq/nanomq.git
cd nanomq ; git submodule update --init --recursive (同步submodule时可能耗时较久)

mkdir build && cd build
cmake -G Ninja -DNNG_ENABLE_QUIC=ON ..
sudo ninja install
```

开启 QUIC 桥接功能的 NanoMQ 编译安装完成后，可以在配置文件`/etc/nanomq_bridge.conf`中配置 MQTT over QUIC 桥接功能和对应的主题，使用 `mqtt-quic` 作为 URL 前缀即是采用 QUIC 作为 MQTT 的传输层：

```
## Bridge address: host:port .
##
## Value: String
## Example: ## Example: mqtt-tcp://broker.emqx.io:1883 （这是标准MQTT over TCP）
bridge.mqtt.emqx.address=mqtt-quic://54.75.171.11:14567

## Protocol version of the bridge. （注意：QUIC桥接目前只支持V4即MQTT 3.1.1版本）
bridge.mqtt.emqx.proto_ver=4

## Whether to enable bridge mode for mqtt bridge
## Value: boolean
bridge.mqtt.emqx.bridge_mode=true

## The ClientId of a remote bridge.
## Default random string.
## Value: String
#bridge.mqtt.emqx.clientid=bridge_client

## Ping interval of a down bridge.
## Value: Duration
## Default: 10 seconds
bridge.mqtt.emqx.keepalive=60

## The Clean start flag of a remote bridge.
##
## Value: boolean
## Default: true
bridge.mqtt.emqx.clean_start=true

## The username for a remote bridge.
bridge.mqtt.emqx.username=username

## The password for a remote bridge.
bridge.mqtt.emqx.password=passwd

## Topics that need to be forward to IoTHUB
##
## Value: String
## Example: topic1/#,topic2/#
bridge.mqtt.emqx.forwards=topic1/#,topic2/#

## Need to subscribe to remote broker topics
##
## Value: String
bridge.mqtt.emqx.subscription.1.topic=cmd/topic1
```

然后启动 NanoMQ 即可：

```
nanomq start --bridge <PATH of nanomq_bridge.conf>
```

验证 QUIC 桥接是否成功，只需往桥接的上下行主题发送数据即可，也可以使用 NanoMQ 自带的 nanomq_cli 工具中的 QUIC 客户端来与 EMQX 5.0 测试验证。

### MQTT 5.0 桥接

除了 QUIC 桥接，0.11 版本也支持使用 MQTT 5.0 进行桥接，用户只需在配置文件中修改桥接的协议版本即可：

```
## Protocol version of the bridge. （注意：MQTT 5.0 只适用于 Vanila MQTT）
bridge.mqtt.emqx.proto_ver=5
```

之后用户就可以通过桥接连接转发 MQTT 5.0 消息了，享受诸如自定义属性等新特性。

## HTTP API 更新

通过 HTTP REST API 来对边缘服务进行监控和运维一直是广大普通用户的需求之一，NanoMQ 0.11 也新增了对当前连接的 MQTT 客户端信息的查询 API，方便第三方应用快速准确的获取所有客户端的在线情况，或查询某个特定客户端的健康状态。

获取所有在线客户端的情况：

```
$ curl -i --basic -u admin:public -X GET "http://localhost:8081/api/v4/clients"

{"code":0,"data":[{"client_id":"nanomq-f6d6fbfb","username":"alvin","keepalive":60,"conn_state":"connected","clean_start":true,"proto_name":"MQTT","proto_ver":5,"recv_msg":3},{"client_id":"nanomq-bdf61d9b","username":"nanomq","keepalive":60,"conn_state":"connected","clean_start":true,"proto_name":"MQTT","proto_ver":5,"recv_msg":0}]}
```

通过客户端 ID 查询指定客户端的在线情况

```
$ curl -i --basic -u admin:public -X GET "http://localhost:8081/api/v4/clients/nanomq-29978ec1"

{"code":0,"data":[{"client_id":"nanomq-29978ec1","username":"","keepalive":60,"conn_state":"connected","clean_start":true,"proto_name":"MQTT","proto_ver":5}]}
```

关于 API 的请求和返回参数详情，请参阅 NanoMQ Docs（[https://nanomq.io/docs/zh/latest/http-api/v4.html#客户端](https://nanomq.io/docs/zh/latest/http-api/v4.html#客户端) ）。

## 其他功能更新

同时，NanoMQ 0.11 还响应用户和社区要求更新和优化了如下功能：

### 退避时间设置 （Backoff timer）

在 MQTT 协议中规定 Broker 要在 1.5 倍于客户端设置的 [Keep Alive](https://www.emqx.com/zh/blog/mqtt-keep-alive) 时间后踢出没有活动的连接。但是实际场景中许多用户希望能够自由灵活调节这一时间长度以适应不同的网络环境。所以新增了这一配置选项，用户通过配置该选项来调整 NanoMQ 处理非活动客户端的最大时间上限。

例如，如果按照以下设置，如果一个客户端的 Keep Alive 时间设置为 60s，且一直没有活动，NanoMQ 将会在 1.25 * 60 = 75s 后关闭此客户端的连接。

```
## The backoff for MQTT keepalive timeout.
## broker will discolse client when there is no activity for
## 'Keepalive * backoff * timeout.
##
## Value: Float > 0.5
keepalive_backoff=1.25
```

### MQTT over QUIC CLI 工具

如果通过`-DNNG_ENABLE_QUIC=ON` 开启了 QUIC 模块，那么会自动编译 nanomq_cli 中的 MQTT over QUIC  客户端工具：

```
nanomq_cli quic --help
Usage: quic conn <url>
       quic sub  <url> <qos> <topic>
       quic pub  <url> <qos> <topic> <data>
       
## subscribe example
nanomq_cli quic sub mqtt-quic://54.75.171.11:14567 2 msg
```

## Bug 修复及优化

1. 为 NanoMQ 增加了自动化 CI 测试框架，以保证测试覆盖率。
2. 修复了 WebSocket&TLS 的传输层。
3. 增加了 nanomq_cli 工具的帮助信息。
4. 修复了一个使用共享订阅时可能导致主题匹配不正确的问题。
5. 修复了客户端使用持久会话后断开连接，会话总是比设定时间更早过期的问题。
6. 修复了桥接连接使用非异步订阅方式可能造成的线程阻塞问题。

## 即将到来

下个版本中，NanoMQ 将为大家带来规则引擎的重发布和热更新功能，并且增加桥接连接的状态管理能力。未来 NanoMQ 还将继续设计和规划利用 QUIC 的 Multi-Stream 特性来应对物联网场景里的多种传输媒介共用带来的链接复用问题，也会在 QUIC 的 Flow Control 基础上完成多种类型数据流统一调度的本地数据网关代理功能。



<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
