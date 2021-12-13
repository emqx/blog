## MQTT 发布订阅模式简述

MQTT 是基于 **发布（Publish）/订阅（Subscribe）** 模式来进行通信及数据交换的，与 HTTP 的 **请求（Request）/应答（Response）** 的模式有本质的不同。

**订阅者（Subscriber）** 会向 **消息服务器（Broker）** 订阅一个 **主题（Topic）** 。成功订阅后，消息服务器会将该主题下的消息转发给所有的订阅者。

主题（Topic）以 ‘/’ 为分隔符区分不同的层级。包含通配符 ‘+’ 或 ‘#’ 的主题又称为 **主题过滤器（Topic Filters）**，不含通配符的称为 **主题名（Topic Names）** 。例如:

```
sensor/1/temperature

sensor/1/#

sensor/+/temperature
```



## MQTT Broker 简介

### MQTT Broker 定义及其作用

MQTT Broker 也称为 MQTT 消息服务器，它可以是运行了 MQTT 消息服务器软件的一台服务器或一个服务器集群。MQTT Broker 负责接收来自客户端的网络连接，并处理客户端的订阅/取消订阅（Subscribe/Unsubscribe）、消息发布（Publish）请求，同时也会将客户端发布的消息转发给其他订阅者。

MQTT Broker 广泛应用于：电力、新能源、智慧城市、智能家居、智能抄表、车联网、金融与支付、运营商等行业。

![mqttbroker.png](https://static.emqx.net/images/130555059bfc4e888f223a6fe9b63352.png)


### 常见开源 MQTT Broker

- [EMQ X](<https://github.com/emqx/emqx>) - EMQ X 基于 Erlang/OTP 平台开发，是开源社区中最流行的 MQTT 消息服务器。除了 [MQTT 协议](https://www.emqx.com/zh/mqtt)之外，EMQ X 还支持 MQTT-SN、CoAP、LwM2M、STOMP 等协议。目前，EMQ X 在全球市场已有 5000+ 企业用户，20+ 世界五百强合作伙伴。
- [Eclipse Mosquitto](<https://github.com/eclipse/mosquitto>) - Mosquitto 是开源时间较早的 MQTT Broker，它包含了一个C/C ++的客户端库，以及用于发布和订阅的 `mosquitto_pub`、`mosquitto_sub` 命令行客户端。Mosquitto 比较轻量，适合在从低功耗单板计算机到完整服务器的所有设备上使用。
- [VerneMQ](<https://github.com/vernemq/vernemq>) - VerneMQ 基于 Erlang/OTP 平台开发，是高性能的分布式 MQTT 消息代理。它可以在硬件上水平和垂直扩展，以支持大量并发客户端，同时保持较低的延迟和容错能力。
- [HiveMQ CE](<https://github.com/hivemq/hivemq-community-edition>) - HiveMQ CE 是基于 Java 的开源 MQTT 消息服务器，它完全支持 MQTT 3.x 和 [MQTT 5](https://www.emqx.com/zh/mqtt/mqtt5)，是 HiveMQ 企业版消息连接平台的基础。



## MQTT Broker 实现的主要功能

### 协议接入

- 完整的 MQTT V3.1/V3.1.1 及 V5.0 协议规范支持；
- MQTT-SN 、CoAP、lwM2M 等物联网协议接入支持。

### 集群部署

多服务器节点集群，且支持节点的自动发现。相对于单服务器，集群能通过多台服务器之间的协作带来以下优势：

- 高可用性。单台或少量的服务器故障并不会导致整个消息服务中断，其余的正常工作的节点可以继续提供服务；
- [负载均衡](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-2-sticky-session-load-balancing)。通过负载均衡机制，集群可以把负载平均的分布在各个节点；
- 更高的整体性能。相比单机部署，多节点的集群能够成倍的提升整个系统的连接和消息处理能力；
- 可扩展性。可以通过在集群中添加新节点的方式来完成扩容而无需停机。

### 接入安全

- SSL、WSS 加密连接，及单/双向安全认证支持；
- 客户端 ID、IP 地址、用户名密码、LDAP 及浏览器 Cookie 认证支持；
- 基于客户端 ID、IP 地址、用户名的访问控制（ACL）；
- 消息速率、连接速率限制。

### 数据持久化

数据持久化的主要使用场景包括将客户端上下线状态，订阅主题信息，消息内容，消息抵达后发送消息回执等操作记录到 Redis、MySQL、PostgreSQL、MongoDB、Cassandra 等各种数据库中。

### 其他功能

- HTTP 消息发布接口支持，使上层应用能更方便的通过 REST API 给设备发送消息；

- MQTT Broker 桥接，支持不同 MQTT Broker 或不同集群之间的消息桥接。桥接可以很方便的将消息桥接到云服务、流式服务、或其他 MQTT 消息服务器。桥接可以完成一些单纯使用集群无法实现的功能：跨 VPC 部署、支持异构节点、提高单个应用的服务上限；

- 支持[共享订阅](https://www.emqx.com/zh/blog/introduction-to-mqtt5-protocol-shared-subscription)。共享订阅是一种机制，允许将订阅组的消息分发均匀地分发给订阅组成员。在共享订阅中，订阅同一主题的客户机依次接收此主题下的消息。同一消息不会发送给多个订阅客户端，从而实现多个订阅客户端之间的负载均衡；

- 规则引擎支持，用于配置消息流与设备事件的处理、响应规则。规则描述了**数据从哪里来**、**如何筛选并处理数据**、**处理结果到哪里去**三个配置，即一条可用的规则包含三个要素：触发事件（满足某个条件时触发）、处理规则（从上下文信息中过滤和处理数据）、响应动作（如持久化到数据库、重新发布处理后的消息、转发消息到消息队列等）。

  

## MQTT Broker 的使用

为了方便测试，我们使用 [EMQ](<https://github.com/emqx/emqx>) 提供的线上版 Broker，该 Broker 版本包含了 EMQ X Enterprise 的所有功能。

> **Broker 地址**： broker.emqx.io
>
> **Broker 端口**： 1883、8883（SSL）、8083（Websocket）、8084（WSS）

连接客户端我们使用 EMQ 提供的线上版 Websocket 工具：[http://tools.emqx.io](http://tools.emqx.io/)。

### MQTT Broker 的连接

使用浏览器打开地址 [http://tools.emqx.io](http://tools.emqx.io/)，点击左下角的 **New Connection** 按钮，并在右侧框里填写链接信息，填写好必填字段后点击 **Connect** 按钮创建链接并连接至 Broker。

![image20191021162759103.png](https://static.emqx.net/images/e1b4f7bd9aa72ca5ff936524c6c8aec4.png)


### 消息发布

连接成功后，点击右下角的 **Write a message** 弹出消息发布框，填写好 **Topic** 及 **Payload** 后点击发送图标即可发布消息。

![image20191021163628054.png](https://static.emqx.net/images/318be47c4eb4c32ac495e029cc9af992.png)


### 主题订阅

- **订阅普通主题**

  在中间的 **Subscriptions** 模块里，订阅 **hello** 主题。此时给 **hello** 主题发送消息的话，消息列表里会收到该消息（左侧为接收到的消息）。

![image20191021164254287.png](https://static.emqx.net/images/4057ffe1de052abc384c2a7ff3e03823.png)


- **订阅通配符主题**

  订阅通配符主题 **testtopic/#**，并给 **testtopic/1** 主题发送消息，此时消息列表里会接收到该消息。

![image20191021164555568.png](https://static.emqx.net/images/2e77b972df9bfeda49da9d0de34953ce.png)
