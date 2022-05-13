上个月，[NanoMQ 团队为 NNG 项目增加了 MQTT 协议支持](https://www.emqx.com/zh/blog/nanomq-newsletter-202111)。本月这一新生高效的 MQTT SDK（NanoSDK）正式合并入了 [https://github.com/nanomq/nanomq](https://github.com/nanomq/nanomq)  的主分支，在此基础上，我们还开发了 NanoMQ 的一项重要功能：MQTT 桥接。

为了优先完成 [NanoMQ](https://nanomq.io/zh) 的 Broker 功能，我们在之前已深度修改了 NNG 底层代码，这导致 NanoMQ 无法与 NNG 原有功能和 SP 协议兼容。因此在这次合并中我们一并解决了 NanoMQ 与 NNG 的兼容问题。通过增加了若干独立的 NNG API，使得 Broker 和 SDK 能够共存。用户能够在使用 NanoMQ 的同时，不影响其中自带的 NNG 原有功能，同时可以更好地利用 NanoSDK 客户端来开发便捷的客户端功能。


## MQTT 桥接介绍

桥接是一种连接多个 [EMQX](https://www.emqx.com/zh/products/emqx) 或者其他 MQTT 消息中间件的方式。不同于集群，工作在桥接模式下的节点之间不会复制主题树和路由表。多数用于将重要主题和设备的数据在复数 Broker 间打通，此特性在云边协同和多活架构场景里都有广泛使用。

![MQTT 桥接](https://assets.emqx.com/images/56831bea36c514268a2360bd47f43d1f.png)

```
              ---------                     ---------                     ---------
Publisher --> | NanoMQ | --Bridge Forward--> | EMQX | --Bridge Forward--> | Cloud | --> Subscriber
              ---------                     ---------                     ---------
```

NanoMQ 在 0.5.5 版本中正式支持了这一功能。使用方法如下：

用户可以通过修改新增的 /etc/nanomq_bridge.conf 配置文件来启用和自定义 MQTT 桥接功能。

```
## Bridge address: host:port .#### Value: String## 
Example: mqtt-tcp://127.0.0.1:1883
bridge.mqtt.address=mqtt-tcp://broker.emqx.io:1883
```

远端桥接地址，即要桥接的 Broker 的 IP 和端口。

```
## Protocol version of the bridge.##
bridge.mqtt.proto_ver=4
```

桥接的 [MQTT 协议](https://www.emqx.com/zh/mqtt)版本，目前只支持 MQTT 3.1.1 与 MQTT 4

```
## The ClientId of a remote bridge.
## Placeholders:
##  ${node}: Node name
## Value: String
bridge.mqtt.clientid=bridge_client
```

桥接所使用的 MQTT 连接的客户端的 ClientID

```
## Ping interval of a down bridge.
## Value: Duration
## Default: 10 seconds
bridge.mqtt.keepalive=60
```

桥接所使用的 MQTT 连接的心跳间隔。

```
## The Clean start flag of a remote bridge.
#### Value: boolean
## Default: true
bridge.mqtt.clean_start=true
```

桥接所使用的 MQTT 连接的会话保持状态。

```
## The username for a remote bridge.
## Value: String
bridge.mqtt.username=username
## The password for a remote bridge.
## Value: String
bridge.mqtt.password=passwd
```

桥接所使用的 MQTT 连接的用户名和密码。

```
## Topics that need to be forward to IoTHUB
## Value: String
bridge.mqtt.forwards=topic1/#,topic2/#
```

所想要和对端 Broker 桥接的主题，可使用通配符。即所有发给 NanoMQ 的满足 topic1/# 和 topic2/# 主题（通配符）标准的消息，在桥接的远端 Broker 相同的主题都也能收到。

```
## Need to subscribe to remote broker topics
## Value: String
bridge.mqtt.subscription.1.topic=cmd/topic1
```

桥接的远端 MQTT Broker 的主题。即 NanoMQ 会订阅目标 Broker 的 cmd/topic1 主题。所桥接的 Broker 的 cmd/topic1 主题收到的所有消息，在 NanoMQ 本地的 cmd/topic1 都能同样受到。可按照编号增加主体数量。

```
## Need to subscribe to remote topics QoS.
## Value: Number
bridge.mqtt.subscription.1.qos=1
```

桥接的远端 MQTT Broker 的主题时所使用的的订阅 QoS 等级，按照序号与上一个配置对应。因为消息下行桥接其实就是本地 Broker 去订阅远端 Broker 的主题，所以也有订阅的 QoS 等级。

```
## parallel
#### Value: 1-CPU Cores
bridge.mqtt.parallel=2
```

桥接使用的 Context 数量，建议与运行平台 CPU 核数相同。此选项影响启动内存和桥接连接的吞吐量。

## **实现方式**

我们通过在 NanoMQ 的应用层添加了一个专门用途的特殊 Context 来完成桥接工作，并为 Broker 的每个 Context 增加了转为桥接使用的 AIO，通过这个 AIO 完成内部的消息在 Broker 和桥接客户端之间的共享。如此做虽然增加了少许启动内存，但既不影响 NanoMQ 原来的高并发低延时吞吐能力，又能够保证桥接客户端和连接能够和普通 MQTT 消息一样共享 CPU 资源调度。

我们推荐在边缘端使用 NanoMQ 作为边缘 MQTT Broker 负责消息汇聚后桥接至云端的 EMQX。

![NanoMQ.png](https://assets.emqx.com/images/4c2eb846529d49339b79dc0911d59798.png)

NanoMQ 桥接至 EMQX 的配置如上一章节所述。EMQX 桥接至 NanoMQ 的配置可参考 [https://docs.emqx.io/en/broker/v4.3/bridge/bridge-mqtt.html#mqtt-bridge](https://docs.emqx.io/en/broker/v4.3/bridge/bridge-mqtt.html#mqtt-bridge)


<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a >
</section>
