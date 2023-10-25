[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 4.4.21 版本现已正式发布！

新版本带来多个功能更新，其中包括新增了 Confluent 集成，改进消息重发布动作，支持设置 MQTT 发布属性和用户属性等，进一步提升了 EMQX 的易用性和灵活性。

## 新增 Confluent 集成

本次发布的 EMQX Enterprise 版本在规则引擎中新增了[ Confluent 集成](https://docs.emqx.com/zh/enterprise/v4.4/rule/bridge_confluent.html)。Confluent 是一个全面的数据流平台，提供全托管的 Confluent Cloud 与自托管的 Confluent Platform 产品，用于处理和管理连续、实时的数据流。

Confluent 包含多项服务，例如 Kafka 服务，Schema Registry 与事件流处理工具，以及跨区域的数据复制能力和其他丰富的扩展功能。EMQX Enterprise 与 Confluent 生态集成，能够为企业提供灵活的物联网实时数据采集、传输、处理和分析全套解决方案，为企业提供更多的洞察和决策支持。

此前 EMQX Enterprise 可以通过 Kafka 兼容的方式与 Confluent 进行集成，但配置和管理过程相对繁琐。新增的 Confluent 集成轻松简化了这一过程，使用户更便捷地访问和利用实时数据流，大大提升了整个集成流程的用户友好性。

## 通过 Kafka 进行 MQTT 消息下发支持映射 MQTT 主题

EMQX Enterprise 的 [Kafka 消息下发](https://docs.emqx.com/zh/enterprise/v4.4/modules/kafka_consumer.html)功能现已引入了动态 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)映射的新特性，这一功能允许用户通过 Kafka 消息和消息元数据动态地构造 MQTT 主题并下发消息。

用户现在能够将 Kafka 主题，甚至是 Kafka JSON 格式消息中的某个字段作为 MQTT 主题的一部分，如下所示：

```
downlink/${key}/${value.client_sn}
```

在实际进行消息下发时，主题的第二三层级将会被替换为实际的 Kafka 消息 Key 以及消息中的 `client_sn` 字段的值。

这一特性为消息下发带来了更大的灵活性，用户能够根据消息内容的不同动态地定制 MQTT 主题，使得针对不同设备、传感器或数据类型的消息能够自动分配到不同的 MQTT 主题下发到指定设备，从而更好地满足不同场景下的适用性和可定制性。

## 规则引擎消息重发布支持 MQTT 发布属性和用户属性

[MQTT 属性](https://www.emqx.com/zh/blog/mqtt5-new-features-properties-and-loads)是 MQTT 5.0 引入的一项重要特性，它为 MQTT 协议带来了更多的灵活性和扩展性。这些属性允许在 MQTT 连接、订阅和发布消息中包含额外的信息，实现事件和消息更灵活的控制和数据传递。

在本次发布中，EMQX Enterprise 进一步增强了规则引擎消息重发布功能，为用户提供了 MQTT 属性设置的支持。这意味着您可以添加预定义的键值配置来转发消息的 MQTT 属性，这些属性包括消息的 Payload 格式、消息的过期时间等。此外，还可以自定义消息的[用户属性](https://www.emqx.com/zh/blog/mqtt5-user-properties)，从而实现更加灵活的消息定制。

## BUG 修复

以下是本次发布 BUG 修复列表：

- 修复 Kafka 集成无法将数字类型的值作为 Kafka Headers 发送的问题。

  修复之前，当 “Kafka Headers 值的编码类型” 设置为 "NONE" 的情况下，如果 "Kafka Headers" 字段里包含了带有数字类型的 JSON 对象例如 `{"a": 1, "b": "str"}`，数字类型的值（`"a":1`）将会被忽略，不会被发送到 Kafka。修复之后 JSON 中的数字类型会先转换为字符串再发送到 Kafka。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
