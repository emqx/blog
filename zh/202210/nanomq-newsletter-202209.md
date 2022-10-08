9 月，NanoMQ 继续保持稳步更新，最新的 [0.12.1 版本](https://github.com/emqx/nanomq/releases/tag/0.12.1)已于近日正式发布。此版本依旧带来了丰富的更新：桥接功能中增加了上下线事件和连接状态监控能力；重构升级了原有的日志系统；配置文件得到了简化，将多个配置文件合并整理为统一的单一文件。

## 桥接连接状态事件消息

IoT 应用中，弱网状态下时常出现网络不稳定的情况，需要一个可靠的途径来侦测当前设备的联网状态以及与云端的连通性。为此，NanoMQ 提供了利用桥接连接来探测网络连接状态的能力。当用户在边缘侧使用 NanoMQ 桥接到云端时，NanoMQ 会创建一个 MQTT 连接到指定的云端 Broker，基于 MQTT 的长连接特性，本地网络里的设备可以利用此连接来判断网络状态。

![桥接 MQTT](https://assets.emqx.com/images/5799e4f6ddc357fafb8ca36f24b66a58.png)

<center>网络侦测：桥接连接状态消息</center>

如上图所示，当本地网络中断或其他故障导致桥接连接断开时，NanoMQ 会检测到桥接连接断开的情况，并将其转化为一个客户端上下线事件消息发布到系统主题中。网络恢复后桥接连接自动重连，也会发布一个上线事件消息到系统主题。本地的客户端和其他服务可以根据收到的此消息进行对应的应急处理，还可以配置多个桥接目标来作为备选服务避免因为云端服务中断导致的误判。

### 如何获取桥接上下线事件消息

目前 NanoMQ 的桥接状态事件支持所有的桥接方式，包括 MQTT 3.1.1/5.0 和 MQTT over QUIC。 上下线事件消息的系统主题分别为 `$SYS/brokers/disconnected` 和 `$SYS/brokers/connected`。事件消息同样也支持作为一个标准 Publish 消息被以 WebHook 的方式获取。这里以一个 MQTT over QUIC 桥接配置为例，示范如何获取桥接连接的上下线消息：

若桥接配置为(只摘录部分相关)：

```
bridge.mqtt.emqx.clientid=quic_client
bridge.mqtt.emqx.keepalive=5
bridge.mqtt.emqx.quic_keepalive=120
bridge.mqtt.emqx.clean_start=false
bridge.mqtt.emqx.username=quic_bridge
bridge.mqtt.emqx.password=passwd
```

使用 NanoMQ 命令行工具订阅对应主题，那么当本地网络中断时，桥接断开就会触发：

```
nanomq_cli sub --url mqtt-tcp://localhost:1883 -t '$SYS/brokers/connected'
connect_cb: mqtt-tcp://localhost:1883 connect result: 0 
$SYS/brokers/connected: {"username":"quic_bridge", "ts":1664277443551,"proto_name":"MQTT","keepalive":5,"return_code":"0","proto_ver":4,"client_id":"quic_client", "clean_start":0}
```

那么当本地网络恢复时，桥接重连成功就会触发：

```
nanomq_cli sub --url mqtt-tcp://localhost:1883 -t '$SYS/brokers/disconnected'
connect_cb: mqtt-tcp://localhost:1883 connect result: 0 
$SYS/brokers/disconnected: {"username":"quic_bridge","ts":1664277394014,"reason_code":"8b","client_id":"quic_client"}
```

可见上下线事件消息中的客户端 ID 和用户名/密码都与桥接配置中的一致，可以此来区分本地客户端和桥接客户端。目前桥接连接状态与普通 MQTT 客户端是共享同一个系统主题，NanoMQ 也考虑为桥接网络状态单独设立一个系统主题，以及作为云边消息总线加入标准的网络健康监控功能。欢迎广大用户提交相关  Issue 和功能申请。

### 新增 QUIC 传输层的 Keep Alive 参数配置

QUIC 内置了一个连接保持机制，为了让用户能够更细颗粒度的控制 MQTT 和 QUIC 的超时时间，NanoMQ  的桥接功能把两者的超时设置都暴露为可设置状态，后续还会开放更多的 QUIC 传输层参数供用户调优。

```
## Ping: interval of a downward bridging connection via QUIC.
bridge.mqtt.emqx.quic_keepalive=120
```

## 配置文件简化

在 0.12 版本之前，NanoMQ 每个模块都有一个独立的配置文件，需要单独打开每个文件进行修改配置，启动较为繁琐。从0.12 版本开始，我们将正式统一合并所有的配置项到 nanomq.conf， 并且为每个模块单独增加了分组。

需要注意的是，之前的命令行参数中指定桥接配置文件和用户名密码文件路径的功能被废弃。

```
  --bridge <path>            The path of a specified bridge configuration file 
  --auth <path>              The path of a specified authorize configuration file 
```

此修改不影响 ZeroMQ 网关的配置文件（nanomq_gatewaty.conf属于 nanomq_cli）和容器部署情况下通过环境变量指定配置文件的方式。

## 日志系统重构

NanoMQ 的旧有日志系统支持命令行、文件和 Syslog 三种模式，但是不能通过配置进行开关，不支持分级输出，而且需要在编译阶段通过修改 CMake 参数来启用，调试和运维分析有一定困难。在 0.12 版本我们重构了整个日志系统，保持对原有三种输出目标和 Syslog 标准兼容外，新增了 trace | debug | info | warn | error | fatal 5 种日志等级，以及指定日志文件路径和日志文件滚动更新等功能。

日志配置示例：

```
## ------------------ Logging Config ------------------ ##
## - file: 输出日志到文件
## - console: 输出日志到命令行
## - syslog: 输出日志到 syslog系统
## Value: file | console | syslog 支持并列配置
log.to=file,console,syslog

## Value: trace | debug | info | warn | error | fatal
## 设置日志等级
##
## Default: warn
log.level=warn

## 若配置了输出日志到文件，则在此指定文件路径
log.dir=/tmp

## 若配置了输出日志到文件，则在此指定文件名
log.file=nanomq.log

## 单个日志文件的最大大小，若超过则会滚动更新
## 支持单位参数: KB | MB | GB
log.rotation.size=10MB

## 最大保存的滚动更新的日志文件个数
log.rotation.count=5
```

## NanoSDK 增加更多 API 封装

此前 NanoSDK 的 API 多为 NNG 的风格，需要用户自己组装 MQTT 消息并发送来完成订阅和接触订阅的操作。从 NanoSDK 0.7.5 开始，NanoSDK 里新增了以下更方便、封装程度更高的 MQTT API：

| nng_mqtt_subscribe()         | perform a subscribe request synchnously     |
| ---------------------------- | ------------------------------------------- |
| nng_mqtt_subscribe_async()   | perform a subscribe request asynchnously    |
| nng_mqtt_unsubscribe()       | perform an unsubscribe request synchnously  |
| nng_mqtt_unsubscribe_async() | perform an unsubscribe request asynchnously |
| nng_mqtt_disconnect()        | Disconnect an MQTT client                   |

具体使用方式请参阅 [NanoSDK Doc](https://github.com/emqx/NanoSDK/blob/0.7.5/docs/man/libnng.3.adoc#mqtt-message-handling)。

## 即将到来

规则引擎的消息重发布功能和规则热更新将在下一个版本中正式发布。同时会为 NanoMQ 增加 Reload 命令来进行配置文件热更新，为 MQTT over QUIC 桥接功能增加多次重连失败可以自动切换为标准 TCP 的功能（Fallback to TCP），来保证在不支持 QUIC 的网络下保持桥接连接功能正常。





<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
