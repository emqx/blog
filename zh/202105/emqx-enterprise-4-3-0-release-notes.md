EMQ X Enterprise 是一个弹性伸缩的企业级物联网 MQTT 消息平台，支持百万级物联网设备一站式接入、MQTT&CoAP 多协议处理、低时延实时消息通信。提供基于 SQL 的内置规则引擎，灵活处理/转发消息到后端服务，存储消息数据到各种数据库，或桥接 Kafka、RabbitMQ 等消息中间件，能够在各类物联网设备与企业系统之间高效、可靠、灵活的双向移动数据。

EMQ X Enterprise 适用于各种物联网应用场景，支持公有云、私有云、物理机、容器/K8s 任意部署，能够帮助企业快速构建 IoT 平台和应用。

企业版介绍：[https://www.emqx.com/zh/products/emqx](https://www.emqx.com/zh/products/emqx)

下载地址：[https://www.emqx.com/zh/downloads](https://www.emqx.com/zh/downloads)



![](https://static.emqx.net/images/4b87d5ae6dc17bb84f6414e4d8fc504c.png)



## 概览

EMQ X Enterprise v4.3.0 版本继承了开源版 4.3.0 版本中的诸多性能提升和功能改进，详见 [EMQ X v4.3 正式发布：性能大幅提升，更好用的多语言扩展](https://www.emqx.com/zh/blog/emqx-4-3-0-release-notes)。在此基础上，企业版 4.3.0 中新增了 Kafka 分区动态扩容的支持，以及更灵活的通过 Kafka 下发 MQTT 消息的方式。

详细更新日志：[https://www.emqx.com/zh/changelogs/enterprise/v4.3.0](https://www.emqx.com/zh/changelogs/enterprise/v4.3.0)



## 规则引擎升级：数据灵活无限集成

[EMQ X 的规则引擎](https://docs.emqx.cn/enterprise/latest/rule/rule-engine.html)是标准 MQTT 之上基于 SQL 的核心数据处理与分发组件，可以方便的筛选并处理 MQTT 消息与设备生命周期事件，分发移动数据到包括 MySQL、InfluxDB、Kafka 在内的十余种数据库和消息系统中，能够零代码集成企业系统，帮助企业快速构建 IoT 平台和应用。

作为 EMQ X 重磅功能，规则引擎基于 SQL 提供了清晰、灵活的「配置式」业务集成方案，简化了业务开发流程，提升用户易用性并降低业务系统与 EMQ X 的耦合度。
![配图3.png](https://static.emqx.net/images/40b090be34291c0d202613e2598ff767.png)

### 新增消息桥接到 Kafka 分区支持动态扩容

EMQ X 结合 Apache Kafka 使用能够以高可靠、松耦合的方式将物联网设备与企业系统集成在一起，也是我们的企业客户实践中乃至物联网业内最常用的技术方案。

自功能发布以来，EMQ X + Kafka 方案足够健壮和成熟，满足了大量企业客户对物联网应用整体性能以及关键业务中数据的安全性、稳定性要求。在过去的版本迭代中我们持续针对 Kafka 方案进行着优化，最初使用了自研驱动，大幅度提高了生产性能，后续在规则引擎引入 Kafka 生产能力提高了数据集成的灵活性。最近的 4.2 版本中，我们为 Kafka 驱动增加了缓存机制进一步保证了数据可靠性。

![配图Artboard.png](https://static.emqx.net/images/12d0fb25e06f518e620cf718b094b85c.png)

在企业版 4.3.0 版本中，我们加入了 Kafka 分区动态扩容能力。

生产环境的 Kafka 集群扩容是一个比较常见的需求和操作，然而 Kafka 新增节点后，并不会将数据 `rebalance` 到新的节点。Kafka 扩容之后需要对相应的 Topic 分区扩容，扩容后的数据均衡，实际上就是对 Topic 进行分区重分配。

在当前版本中，无需额外操作，规则引擎使用的 Kafka Topic 在扩容之后， EMQ X 能够自动刷新分区数，该配置选项见下图所示：

![配图4.png](https://static.emqx.net/images/97d72c45072d70cf0e15ca35df1b47ae.png)


### 规则引擎所有支持批量的操作默认启用批量异步

从 4.2.2 版本开始，EMQ X 规则引擎为写入数据库、Kafka 等 I/O 操作提供了异步和批量写入模式，异步模式可以将设备消息通信与数据处理分离，提供更高的 I/O 性能并避免 I/O 阻塞客户端正常 Pub/Sub 流程，详见 EMQ X Enterprise 4.2.2 发布说明。

之前此功能是默认关闭、建议用户开启的，该版本中我们为了给用户带来更好的体验将选项置为默认开启状态。

### 规则引擎支持 ClickHouse 离线消息与代理订阅

支持使用 ClickHouse 作为 Storage 使用离线消息与代理订阅功能。鉴于 ClickHouse 不适用于频繁的小数据操作特性，若没有强烈的项目刚需和必要的场景，离线消息与代理订阅场景不建议使用 ClickHouse。



### 规则引擎重构 InfluxDB 以增强性能

我们为 InfluxDB 新增了 HTTPS 支持，并支持 InfluxDB 批量写入。



## Kafka 下发改进：更易用的 Kafka 消息下发

EMQ X 的 模块 -> Kafka 消费组 功能可以使用外部 Kafka 作为消息队列，从指定 Kafka Topic 中消费消息并转换成为 MQTT 消息，发送到具体的 MQTT Topic 中，数据流如下图所示：

![配图Artboard2.png](https://static.emqx.net/images/9fe7501172ea1e95ec7052c733c1c8ec.png)

### Kafka-MQTT 1:M Topic 映射消息下发

当前版本中，我们提供了 Kafka 下发数据选择功能，这个新的功能来源于某位企业客户的建议，正常情况下 Kafka 消息中包含 `value`、`topic`、`key` 以及 `offset` 等数据：

```json
{
    "value": "{\"foo\": \"bar\"}",
    "ts_type": "create",
    "ts": 1621419857749,
    "topic": "test",
    "offset": 2,
    "key": "",
    "headers": []
}
```

此前的设计中我们仅支持转发 Kafka 消息中的 `value` 值到指定的 MQTT Topic 中，用户无法再获取其他数据，然而这些数据在某些场景下也有相应的用处，比如用户期望使用消息中的唯一 `key` 作为下发 MQTT Topic 的一部分。

在配置 `Kakfa Topic` - `MQTT Topic` 的映射关系时，我们提供了MQTT Payload 的内容配置项，针对某个映射，用户可以选择转 发完整的 Kafka 消息还是消息的 `value` 内容。


![配图5.png](https://static.emqx.net/images/75d08b256fd1db259bf8369aeb184081.png)


### Kafka 下发与规则引擎组合使用

由于 Kafka 跟 MQTT 有很大的区别，实际使用中 Kafka Topic 无法与 MQTT Topic 一一建立映射关系：Kafka Topic 总是少量的，MQTT Topic 数量可能很多，对此可以组合使用规则引擎功能来进行数据分发：

- 物联网应用将下发指令放入 Kafka 消息中，包括目的地MQTT Topic、Payload 等，比如 `{ "topic": "foo", "payload": "bar" }`；

- 将指令写入 Kafka 某个 Topic 比如 `foo`；

- EMQ X Kafka 消费者建立映射关系，将上一步中的消息映射到某个 MQTT Topic 比如 `foo_mqtt` 中，实际上客户端不会订阅该 Topic，这个 Topic 只是中转使用 的 Topic，目的是让规则引擎借助该 Topic 获取来自 Kafka的消息;

- 编写规则引擎，从中转 Topic `foo_mqtt` 中获取数据，解析 下发指令中的 topic 、 payload 信息，选择**消息重新发布**动作，在动作中通过 `${topic} ${payload}` 等变量提取语 法，动态填充**目的地主题**、**消息内容模板字段**，实现 Kafka- MQTT 的动态解析下发。



## 问题修复

- 规则引擎动作编辑数据不一致问题
- Dashboard 模块翻译问题
- 规则引擎 SQL语句支持 null 函数，undefined 转成 null

## 未来展望

EMQ X 自 2013 年发布以来，至今已服务全球超过 300 家企业客户，帮助车联网、工业制造、能源电力、金融支付等各个行业客户搭建具有竞争力的物联网平台，实现数字化、智能化转型。在未来，EMQ 将继续专注客户需求及使用体验，提供更加优质的产品与服务。

4.3.0 版本是企业版 4.x 最后一个次要版本，我们将为该版本持续提供 18 个月的维护服务，推荐所有 4.x 的企业用户升级到此版本。目前 EMQ X 团队已进入到 5.0 版本开发工作中，企业版 5.0 计划在 7 月份发布，届时将为大家带来全新的「一次连接、无限集成」规则引擎，以及更清晰易用的功能划分、更全面的云原生集成能力。
