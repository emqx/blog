金秋十月，NanoMQ 继续保持稳步更新，最新的 0.13 版本将于近日正式发布。此版本的更新继续聚焦于桥接功能部分：为原来的 MQTT over QUIC 桥接功能增加了多路桥接和更丰富的 QUIC 传输层配置参数，新增了内置的 Azure 桥接功能。另外新增了规则引擎消息重发布功能。

## 更完善的 MQTT over QUIC 桥接

在 0.12 版本中推出的 MQTT over QUIC 桥接功能与 EMQX 5.0 配合使用得到了用户的热烈反响。在 0.13 版本中，我们为此功能进行了多项加强：

### 多路桥接

原先的 MQTT over QUIC 桥接功能只能支持连接一个服务端，这无法满足多路数据同步和传输的要求。与传统的基于 TCP 的 MQTT 连接相同，NanoMQ 也为基于 QUIC 的桥接功能的传输层做了优化，使其能够支持同时建立多个 MQTT over QUIC 连接。用户只需要和使用标准 MQTT 桥接功能一样，在配置文件中设置多个桥接目标配置(只摘录部分相关)：

```
## Bridge via both TCP & QUIC ##
## 以同时桥接到EMQX公共服务器和EMQX Cloud为例，配置桥接URL ##
bridge.mqtt.emqx1.address=mqtt-quic://broker.emqx.io:14567
bridge.mqtt.emqx2.address=mqtt-quic://54.75.171.11:14567
bridge.mqtt.emqx3.address=mqtt-tcp://broker.emqx.io:1883

......
```

多路桥接时，桥接数据是会同时发布给每个桥接对象的。NanoMQ 也支持同时进行基于 TCP 和 QUIC 的 MQTT 桥接。

### QUIC & TCP 自动切换

MQTT over QUIC 能够帮助 IoT 应用极大改善弱网状态下的数据传输和地址迁移问题。但由于 QUIC 是基于 UDP 的，目前许多运营商仍然对 UDP 包有特殊的路由策略，这往往导致 QUIC 连接无法成功建立或一直被丢包。NanoMQ 也考虑到需要应对复杂的中间网络问题，特地推出了 QUIC 连接失败时自动切换至标准 MQTT over TCP 桥接的功能。

![QUIC & TCP 自动切换](https://assets.emqx.com/images/f966e05d747d74f08cc4403dc6a88af4.png)

<center>切换逻辑示意图</center>
 

使用时只需要在配置文件中设置新增的 `bridge.mqtt.emqx.hybrid_bridging` 选项为 `true` 来开启这一模式。注意目前并不能自动切换回 QUIC，后续再备用桥接目标功能中会支持这一需求。另外，因为此过程不计为连接通断，所以也不会发出桥接断开/连接的上下线事件消息。

### 更丰富细致的配置选项

QUIC 作为新晋的网络标准，而且具有一定的设计自由度，所以往往需要针对不同的网络环境和场景修改其内部参数，为此 NanoMQ 暴露了一些常用的配置选项，以下是对它们的详细解释：

```
## Newly added config params for QUIC ##
##--------------------------------------------------------------------

## Ping: QUIC 传输层发送Ping包的时间间隔
##
## Value: Duration
## Default: 120 seconds
bridge.mqtt.emqx.quic_keepalive=120

## Idle Timeout: 保持QUIC连接的最大空闲时间，超过此设置时间长度的无活动连接将会被主动关闭。
设置为0的话就不侦测无活动连接，若MQTT层keepalive设置的过大，这会造成僵尸连接的风险
## Value: Duration
## Default: 120 seconds
bridge.mqtt.emqx.quic_idle_timeout=120

## Disconnect Timeout: QUIC Stream 最大等待对端ACK的时间，超过此时间未收到回应的Stream
会被认为无效并断开。
## Value: Duration
## Default: 20 seconds
bridge.mqtt.emqx.quic_discon_timeout=20

## Handshake Timeout: NanoMQ建立QUIC连接时的最大等待时间 
## Value: Duration
## Default: 60 seconds
bridge.mqtt.emqx.quic_handshake_timeout=60

## Hybrid bridging: 混合桥接模式的开关，若开启会根据QUIC链接的建立情况自动退回 MQTT over
 TCP 桥接模式
## Value: true/false
## Default: false
bridge.mqtt.emqx.hybrid_bridging=false
##
##--------------------------------------------------------------------
```

### QUIC 桥接支持 SQLite 数据缓存

NanoMQ 的桥接功能一大特色是桥接能够支持断网数据本地缓存，网络恢复自动重传。之前此项功能只对标准的 MQTT over TCP 有效。从 0.13 版本开始，当开启 SQLite 自动缓存功能时，此功能对 QUIC 桥接也同样有效。

### 自动化发布包含 QUIC 功能的安装包

在 0.12 版本，用户如果想要使用 NanoMQ 的 QUIC 相关功能，需要自行下载源码编译安装，过程较为复杂。为了方便用户使用，从 0.13 版本开始，NanoMQ 新增了自动化编译打包流程，每次都会自动编译出包含 QUIC 库在内的二进制包供用户直接安装使用。希望以此来降低项目中引入 QUIC 功能的上手门槛，用户只需简单安装 EMQX 5.0 + NanoMQ 并做相应配置即可。

## Azure IoT Hub 桥接

微软的 Azure 云服务有提供一个兼容部分 MQTT 协议的物联网服务：IoT Hub，详情可参阅微软官方文档（[了解 Azure IoT 中心 MQTT 支持](https://learn.microsoft.com/zh-cn/azure/iot-hub/iot-hub-mqtt-support) ）。NanoMQ 也内置支持了与其的桥接功能，具体使用方式如下：

Azure 强制要求必须使用 TLS 加密连接，且使用的 Topic 和认证用的用户名密码必须在其控制台预先创建设备来配置使用。

![Azure IoT Hub 桥接](https://assets.emqx.com/images/86d28634e46ce0a3859c895cd13786bb.png)

目前 NanoMQ 只支持使用对称秘钥加密和用户名+密码的方式认证链接 Azure IoT Hub。

配置后的页面如图：

![Azure IoT Hub 桥接](https://assets.emqx.com/images/83cf4f9dc216a5cf314ad245206f8ac9.png)

之后修改桥接配置文件，其中需要特殊对待的配置有：

```
bridge.mqtt.azure.address=tls+mqtt-tcp://azure-iot-hub.net:8883 (使用Azure提供的主机名)
bridge.mqtt.azure.clientid=device01 (使用在Azure控制台创建的设备名)
bridge.mqtt.azuer.username= {iothubhostname}/{device_id}/?api-version=datetime
(主机名+设备名+API版本日期拼接而成)
bridge.mqtt.azuer.password=***** （ 使用SAS令牌，需要用Azure提供的工具本地生成 ）
bridge.mqtt.azuer.tls.enable=true (必须使用TLS加密)
bridge.mqtt.azuer.forwards=devices/{device_id}/messages/events/
bridge.mqtt.azuer.subscriptions.1.topic=devices/{device_id}/messages/devicebound/#
（订阅和发布的主题必须按照Azure规则配置）
```

![例：使用VS Code生成SAS令牌的方法](https://assets.emqx.com/images/004b1f9680c3d933f1c40a44215b1140.png)

<center>例：使用VS Code生成SAS令牌的方法</center>

如此启动 NanoMQ 就能够完成将本地标准 MQTT 客户端的消息转换桥接至 Azure IoT Hub。

## 规则引擎消息重发布

规则引擎消息重发布功能在 v0.13 中测试完成正式发布。支持根据用户编写的 SQL 语句将本机 NanoMQ 里命中的消息修改后重新发布到目标 MQTT 服务的主题。简单示例如下：

```
## 重新发布消息到此目标主机：
rule.repub.1.address=mqtt-tcp://broker.emqx.io:1883
## 重新发布到此目标主题：
rule.repub.1.topic=topic/repub1
## 根据如下规则过滤本机NanoMQ的消息：
rule.event.publish.1.sql="SELECT topic, payload FROM "abc""
```

如此就能将本地 NanoMQ 的”abc”主题中的消息和主题名一起组合成新的消息转发给云端公有的 EMQX MQTT 服务。

同时，这一版本开始规则引擎也能够支持使用 HTTP API 来对部分规则进行热更新。

## 即将到来

目前 NanoMQ 正计划将配置文件格式更新为更易读的 HOCON（*Human-Optimized* *Configuration Object* *Notation*）。关于配置文件使用体验，欢迎用户在 Github 提出宝贵建议。同时 NanoMQ 还将增加 Reload 命令和 HTTP API 来支持部分配置选项的热更新，并增加 ACL 支持等功能。





<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
