[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 4.4.22 版本现已正式发布！

新版本带来全局的预设 MQTT 消息过期时间功能，可以灵活设置消息在系统中的最大保留时间，避免消息堆积问题。同时新增了多个企业特性，包括审计日志，Dashboard RBAC 权限控制，进一步提升了企业部署的安全性和治理能力。此外，新版本还进行了多项改进以及 BUG 修复，进一步提升了整体性能和稳定性。

## 全局预设 MQTT 消息过期时间

物联网应用中，数据和事件数据通常具有明确的时效性，过期的数据不再具有使用价值，需要及时清除，以避免订阅端收到过期消息，并因此产生性能损耗或错误操作。同时及时清除过期的消息也可以避免数据占用服务器的存储和网络资源，能够提高消息传输效率。

消息过期时间与业务超时逻辑的统一这对于某些场景很重要，例如智能家居或车联网行业，由于网络波动导致消息延迟或失效需要及时丢弃过期消息，以避免用户发出的开锁指令被超时执行，带来额外的安全隐患。在金融支付业务中，这一特性可以确保数据在规定的时间内被处理，防止数据被滞留或被滥用，以提高消息的可靠性和安全性。

[MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 提供了[消息过期间隔](https://www.emqx.com/zh/blog/message-retention-and-message-expiration-interval-of-emqx-mqtt5-broker)支持，允许客户端在发布消息时通过 Message-Expiry-Interval 属性指定该条消息的过期时间。在 MQTT 服务器后续的消息投递过程、以及保留消息列表中，过期的消息将被丢弃。然而，对于使用 MQTT v3.3.1 版本的用户来说，他们无法利用这一特性，这给应用的开发实践带来了一些限制。

为此，自 v4.4.22 版本起 EMQX 提供了全局预设的 MQTT 消息过期时间，在不改动客户端的情况下，允许用户通过配置文件为所有消息设置统一的消息过期时间实现这一需求，配置示例如下如下：

```
# emqx.conf

# 设置消息过期时间为 120s
mqtt.message_expiry_interval = 120s
```

这一特性同时适用于所有 MQTT 版本客户端。对于 MQTT v5.0 客户端来说，如果发布者设置了消息过期间隔的消息，消息过期配置将被忽略；相反，如果发布者没有消息设置过期时间，那么将按照此配置生效。

## 审计日志

审计日志（Audit Log）是记录软件或系统关键操作活动的功能，能够让您实时跟踪集群管理与配置过程中的重要操作，助力企业用户满足合规要求。

EMQX 新增的审计日志支持记录来自 [Dashboard](https://docs.emqx.com/zh/enterprise/v5.3/dashboard/introduction.html) 、[REST API](https://docs.emqx.com/zh/enterprise/v5.3/admin/api.html) 以及[命令行](https://docs.emqx.com/zh/enterprise/v5.3/admin/cli.html)的所有变更性操作，例如用户登录，对客户端、访问控制以及数据集成等资源的修改。

审计日志会记录每项操作的操作对象，发起用户、来源 IP、浏览器特性、关键参数以及操作结果，企业用户可以方便地在 Dashboard 上进行管理，或通过日志集成到第三方分析系统中管理，以实现运营过程中的合规性和安全性审计。

![EMQX 审计日志](https://assets.emqx.com/images/399947163116f23683aeb66a8098d8bf.png)

## Dashboard RBAC 访问权限控制

EMQX Dashboard 是管理和配置 EMQX 集群的关键组件。对于大型企业用户，团队成员之间通常有不同的工作划分。根据团队成员的角色，只为他们分配 Dashboard 的最低访问权限是一种安全性最佳实践。

本次发布 Dashboard 中引入了基于角色的访问控制（RBAC）权限管理功能。RBAC 可以根据用户在组织中的角色，为用户分配不同的访问权限。这一功能简化了权限管理，通过限制访问权限提高了安全性，并提升了组织的合规性，是 Dashboard 不可或缺的安全管理机制。

目前，Dashboard 预设了两个角色：

**管理员（Administrator）**

管理严拥有对 EMQX 所有功能和资源的完全管理访问权限，包括客户端管理、系统配置、API 密钥以及用户管理。

**查看者（Viewer）**

查看者只能以只读的方式访问 EMQX 的数据和配置信息，例如查看客户端列表、获取集群指标与状态、查看数据集成配置，无权进行创建、修改和删除操作。

这一功能满足了企业用户对访问控制的的权限划分安全需求，能够帮助 EMQX 更好地适应大规模企业用户的使用和管理流程。

## 规则 SQL 新增多个实用函数

以下是新增的规则引擎函数的介绍，包括函数名称、函数作用与使用场景以及函数示例：

### map_keys

返回给定映射（Map）中所有键的列表，可以使用这个函数来提取映射中的键。

示例：

```
map_keys(json_decode('{ "a" : 1, "b" : 2 }')) = ['a', 'b']
```

### map_values

返回给定映射（Map）中所有值的列表，可以使用这个函数来提取映射中的值。

示例：

```
map_values(json_decode('{ "a" : 1, "b" : 2 }')) = [1, 2]
```

### map_to_entries

将给定的映射（Map）转换为键-值对的列表，可以使用这个函数来将映射类型的数据转换为便于处理和分析的键-值对列表。

示例：

```
json_encode(map_to_entries('{"a": 1, "b": 2}')) = '[{"value":1,"key":"a"}, {"value":2,"key":"b"}]'
```

### join_to_string

将字符串列表或数组的元素连接成一个字符串，用于构建以特定符号分隔的字符串，例如动态拼接 SQL 语句。

示例：

```
join_to_string(['a', 'b', 'c']) = 'a, b, c'
join_to_string('-', ['a', 'b', 'c']) = 'a-b-c'
```

### join_to_sql_values_string

将字符串列表或数组的元素连接成一个适用于SQL语句的值字符串，用于构建 SQL 语句中的值列表部分，确保字符串值正确格式化和引用。

示例：

```
join_to_sql_values_string(['a', 'b', 1]) = '\'a\', \'b\', 1'
```

### is_null_var

检查变量是否为 null，可以进行变量的空值检查，以便在规则条件中进行相应的处理。

示例：

```
is_null_var(undefined_var) = true
```

### is_not_null_var

检查变量是否不为 null，可以进行变量的非空值检查，以便在规则条件中进行相应的处理。

```
is_not_null_var(mget('a', json_decode('{"a": null}'))) = false
```

上述函数用于将 JSON 格式的数据自由的转换为数据库 SQL 语句、HTTP 请求模板等格式，您可以根据具体的业务需求灵活地应用这些函数来处理和转换数据，完整规则 SQL 函数请参考[此处](https://docs.emqx.com/zh/enterprise/v4.4/rule/rule-engine_buildin_function.html)。

## 其他更新

- LwM2M 网关支持使用块传输协议（Block Wise Transfer）发送下行数据，有效地解决传输过程中的内存和网络带宽限制。
- 更新 Erlang/OTP 的版本到 OTP-24.3.4.2-4，修复了潜在问题并提升安全性。
- OCSP Stapling 和 CRL 创建与更新 REST API 提供了增加更严格的 Schema 校验。
- 为 MQTT 桥接动作增加 `QoS` 选项，用于指定桥接消息的 QoS 等级，实现更灵活的消息桥接。

## BUG

- 修复了 Kafka 客户端（wolff）生产者崩溃的问题。避免在初始化规则时删除 Kafka 资源，导致依赖这个资源的规则失败，这个错误随后传播，触发了错误升级机制，最终导致所有规则都崩溃的问题

- 修复规则引擎的 GCP PubSub 动作在异步发送模式下，统计计数不增长的问题。

- 修复手动重连资源时，只有当前节点的资源会执行重连的问题。

- 修复了多 CPU 场景下，支持批量模式的数据集成动作，批量发送性能比 4.4.5 之前的版本有所下降的问题。

  更多功能变更和 BUG 修复请查看 [EMQX Enterprise 4.4.22 更新日志](https://www.emqx.com/zh/changelogs/enterprise/4.4.22)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
