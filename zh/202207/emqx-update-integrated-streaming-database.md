近日，EMQX 开源版 v4.3.16、开源版 v4.4.5 与企业版 v4.3.11、企业版 v4.4.5 四个维护版本正式发布。

此次发布实现了与流数据库 [HStreamDB](https://hstream.io/zh) 的集成，提供一站式数据接入与实时处理分析。新增了排他订阅功能和规则引擎消息重发布时动态 QoS 与保留消息设置支持，同时支持在消息发布的 API 中设置 MQTT 5.0 的发布属性（PUBLISH Properties），帮助用户应对更多场景使用需求。此外还修复了多项已知 BUG。

欢迎下载使用：[https://www.emqx.com/zh/try?product=enterprise](https://www.emqx.com/zh/try?product=enterprise)

## 规则引擎新功能

### 集成 HStreamDB，一站式数据接入、存储与分析

包含版本 `企业版 v4.3.11` `企业版 v4.4.5`

[HStreamDB](https://hstream.io/zh) 是一款为物联网数据存储和实时处理而生的流数据库。它使用标准 SQL (及其流式拓展）作为主要接口语言，以实时性作为主要特征，集实时数据采集和捕获系统、实时数据存储系统、流计算引擎、下游的数据和应用系统于一体，旨在简化数据流的运维管理以及实时应用的开发。

规则引擎现已支持将 EMQX 的数据持久化到 HStreamDB，从而实现对这些数据的实时处理分析与洞察。性能测试中，EMQX 在 32 核 64GB 配置下可以稳定支持 8 万连接、每秒 8 万 QoS 0、Payload 4KB 的消息持久化至 HStreamDB，集成使用方式请参照[文档](https://docs.emqx.com/zh/enterprise/v4.4/rule/backend_hstreamdb.html)。

![EMQX-HStreamDB XMeter 性能测试报告](https://assets.emqx.com/images/26dabfde29c5f6e2542ec1072968fc7c.png)

<center>EMQX-HStreamDB XMeter 性能测试报告</center>

### **消息重发布动作支持保留消息与动态 QoS** 

包含版本 `开源版 v4.3.16` `开源版 v4.4.5` `企业版 v4.3.11` `企业版 v4.4.5`

我们在消息重发布功能中引入保留消息和动态 QoS 支持，以满足用户特定的场景下的需求。其中保留消息需求来源于 [EMQX 问答社区](https://askemq.com/t/topic/1899)，旨在将客户端最新状态通过保留消息存储到 EMQX 中以便后续处理。

![EMQX Dashboard](https://assets.emqx.com/images/96fc4029081f378263d40d700bca5ed6.png)

## 新增排他订阅功能

包含版本 `开源版 v4.3.16` `开源版 v4.4.5` `企业版 v4.3.11` `企业版 v4.4.5`

排他订阅只允许单个订阅者订阅某个主题，使用排他订阅时，可以轻松实现「某些数据同时只能被一个订阅者处理」这类业务。

排他订阅的使用与共享订阅十分相似，使用特定的主题前缀 `$exclusive` 表明这是一个排他订阅，某个客户端订阅成功后，新的客户端将无法再次订阅相同主题。

排他订阅默认关闭，需要在此配置项中开启：

```
mqtt.exclusive_subscription = true
```

排他订阅生效示例：

```
// 成功
clientA.subscribe('$exclusive/t/1')

// 失败，该主题已有订阅者
clientB.subscribe('$exclusive/t/1')

// 成功，不带前缀的普通主题仍然可以成功订阅
clientC.subscribe('t/1')

// 需要携带前缀以取消订阅
clientA.unsubscribe('$exclusive/t/1')
// 成功
clientB.subscribe('$exclusive/t/1')
```

## **消息发布 API 支持设置 MQTT 5.0 发布属性（PUBLISH Properties）**

包含版本  `开源版 v4.4.5`  `企业版 v4.4.5`

MQTT 5.0 支持在消息发布时设置额外的属性如[消息过期间隔](https://www.emqx.com/zh/blog/message-retention-and-message-expiration-interval-of-emqx-mqtt5-broker)、[主题别名](https://www.emqx.com/zh/blog/mqtt5-topic-alias)和[用户属性](https://www.emqx.com/zh/blog/mqtt5-user-properties)等，新版本中用户可以在消息发布 API 中使用此特性，以满足更多业务需求。

以下是包含发布属性的消息发布示例：

```
curl -i --basic -u admin:public -X POST "http://localhost:8081/api/v4/mqtt/publish" -d \
'{
  "topic":"t/1",
  "payload":"Hello World",
  "qos":1,
  "retain":false,
  "clientid":"emqx_c",
  "properties": {
    "user_properties": { "id": 10010, "name": "emqx", "foo": "bar"},
    "content_type": "text/plain",
    "message_expiry_interval": 3600
  }
}'
```

## 更多功能优化

- 支持通过 CLI 一键更新集群 License
- Dashboard 和管理 API 的 HTTPS 监听器可以使用受密码保护的私钥文件，提供了 `key_password` 配置项
- 支持在主题重写规则中使用占位符 `%u` 和 `%c`
- 优化规则引擎资源创建时的 UI，例如折叠部分不常用的选项等
- 为 ExHook 底层的 gRPC 连接开放了 KeepAlive、TCP_NODELAY、SO_RCVBUF 和 SO_SNDBUF 共 4 个与 TCP 相关的配置项

## BUG 修复

各版本 BUG 修复详情请查看：

- 开源版 v4.3.16： [https://www.emqx.com/zh/changelogs/broker/4.3.16](https://www.emqx.com/zh/changelogs/broker/4.3.16)
- 开源版 v4.4.5： [https://www.emqx.com/zh/changelogs/broker/4.4.5](https://www.emqx.com/zh/changelogs/broker/4.4.5) 
- 企业版 v4.3.11：[https://www.emqx.com/zh/changelogs/enterprise/4.3.11](https://www.emqx.com/zh/changelogs/enterprise/4.3.11)
- 企业版 v4.4.5： [https://www.emqx.com/zh/changelogs/enterprise/4.4.5](https://www.emqx.com/zh/changelogs/enterprise/4.4.5)


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
