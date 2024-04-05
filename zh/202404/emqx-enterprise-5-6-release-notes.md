[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 5.6.0 版本现已正式发布！

在这个版本中，我们引入了一系列新的功能和改进，包括 Amazon S3 和 RabbitMQ 消费者数据集成，规则引擎 JSON Schema 消息验证等功能。此外，新版本还进行了多项改进以及 BUG 修复，进一步提升了整体性能和稳定性。

## 新增 Amazon S3 数据集成

[Amazon Simple Storage Service (Amazon S3) ](https://aws.amazon.com/s3/) 是一种面向互联网的存储服务，具有高度的可靠性、稳定性和安全性，能够快速部署和使用。EMQX 提供了与 Amazon S3 的数据集成，能够将 MQTT 消息高效地存储至 Amazon S3 存储桶中，实现灵活的物联网数据存储功能。

![新增 Amazon S3 数据集成](https://assets.emqx.com/images/3f0ee01be11e4d7a4f1e035ab4e327b6.png)

这允许将物联网数据与 Amazon S3 丰富的生态应用结合，以实现更多的业务场景，例如数据分析。同时，相较于数据库 Amazon S3 提供了更低成本的数据存储服务，可以满足数据长期存储的需求。

EMQX 也兼容其他支持 S3 协议的存储服务，例如 [MinIO](https://min.io/) 与 [Google Cloud Storage](https://cloud.google.com/storage)。您可以基于 S3 构建高效、可靠和可扩展的物联网应用，并在业务灵活性和成本优化方面受益。

[查看文档](https://docs.emqx.com/zh/enterprise/v5.6/data-integration/s3.html)

## 新增 RabbitMQ 消费者数据集成

EMQX 新增了 RabbitMQ 消费者数据集成功能，实现了 RabbitMQ 到 MQTT 的消息桥接功能。

用户可以配置 EMQX，实现从 RabbitMQ 中指定队列消费消息，在使用规则引擎对消息进行灵活的数据处理，将消息发布到 EMQX 指定的 MQTT 主题中。

![新增 RabbitMQ 消费者数据集成](https://assets.emqx.com/images/5f8d74647b12fcb67a824ea9c1b9a119.png)

这个功能可以整合 RabbitMQ 与 EMQX 强大特性，能够实现诸如异步设备指令下发、定时任务调度、消息转发等功能，为用户提供更多的灵活性和扩展性，帮助用户更好地满足业务需求。

[查看文档](https://docs.emqx.com/zh/enterprise/v5.6/data-integration/data-bridge-rabbitmq.html)

## 规则引擎支持 JSON Schema 消息验证

为了确保物联网应用中的设备与应用之间能够正确交互，消息的格式必须符合特定的规范。如果收到意外的消息格式，可能会导致订阅者处理异常或引发安全问题。为了保证系统的稳定性和可靠性，我们需要进行数据格式校验，及早发现并屏蔽错误格式的消息。

JSON 是目前物联网中最常用的数据交换格式，通过 JSON Schema 能够方便定义 JSON 数据的结构化规范，包括对数据字段的必填性、类型、范围和结构等进行校验。

在本次 EMQX 发布中，我们在规则引擎中引入了基于 JSON Schema 的消息验证功能。这个功能可以用来验证输入的 JSON 对象是否符合预定义的 Schema，以确保数据系统只接收到预期内的消息。除了支持 JSON Schema 外，EMQX 还可以验证 Arvo 和 Protobuf 格式的消息。

[查看文档](https://docs.emqx.com/zh/enterprise/v5.6/data-integration/schema-registry.html)

以下是一个示例的 SQL 查询语句，用于在 `t/#` 主题下验证消息是否符合名为 `my_schema` 的 Schema，并返回验证结果（`is_valid` 字段）为 `true` 的消息：

```sql
SELECT
  schema_check('my_schema', payload) as is_valid
FROM
  't/#'
WHERE is_valid = true
```

修改 JSON Schema 定义即可实现不同的用例，比如：

1. 验证是否为有效的 JSON 数据：

   ```json
   {
     "type": "object"
   }
   ```

1. 验证字段值是否在 `0~100` 合法范围内：

   ```json
   {
     "type": "object",
     "properties": {
       "value": {
         "type": "number",
         "minimum": 0,
         "maximum": 100
       }
     }
   }
   ```

1. 验证经纬度地址格式，也可以通过多个 Schema 实现类似地理围栏的限制：

   ```json
   {
     "type": "object",
     "properties": {
       "latitude": {
         "type": "number",
         "minimum": -90,
         "maximum": 90
       },
       "longitude": {
         "type": "number",
         "minimum": -180,
         "maximum": 180
       }
     }
   }
   ```

## 黑名单支持更灵活的封禁方式

本次发布中，EMQX 黑名单功能增加了新的匹配规则：

1. **客户端 ID/用户名模式**：您可以使用表达式来封禁符合特定特征的一系列客户端。例如，使用表达式 `^emqx-*` 能够封禁所有客户端 ID 或用户名以 `emqx-` 开头的客户端；
2. **IP 地址范围：**您可以指定要封禁的客户端来自的 IP 地址段。

![黑名单支持更灵活的封禁方式](https://assets.emqx.com/images/0567938a746b40c69791fbb94bc892cc.png)

通过使用这些简单的规则，您可以实现广泛的封禁范围，从而提高管理灵活性和使用安全性。

[查看文档](https://docs.emqx.com/zh/enterprise/v5.6/access-control/blacklist.html#创建黑名单)

## 增强客户端管理能力：批量查询、返回指定字段，查看队列与飞行窗口中的消息

此前 EMQX 通过 Dashboard 与 REST API 提供了丰富的 MQTT 客户端管理能力，可以实现在线状态与连接信息查询、流量与报文收发统计、消息队列与飞行窗口状态查看等功能，为用户和应用开发者提供了强大的支持。

在本次发布中，我们进一步增强了客户端管理能力，帮助用户实现更灵活和深度的客户端管理。

### 更灵活的查询方式

我们升级了现有的 `GET /clients` REST API，增加了批量查询和指定返回字段的功能：

- 指定多个客户端 ID 实现批量查询：`GET /clients?clientid=client1&clientid=client2`
- 指定多个查询用户名实现批量查询：`GET /clients?username=user11&username=user2`
- 使用 `fields` 参数指定返回某些字段：使用 `GET /clients?fields=clientid,username,connected`

以上查询方式可以组合使用以满足需求。例如，您可以同时查询多个客户端并且只返回特定的字段。这在需要频繁进行查询的场景下非常有用，可以有效减少请求次数和数据量。这样一来，您可以更高效地获取所需的信息。

[查看 API 文档](https://docs.emqx.com/zh/enterprise/v5.6/admin/api-docs.html#tag/Clients/paths/~1clients/get)

### 查看飞行窗口与队列中的消息

我们实现了[飞行窗口（Inflight Window）和消息队列（Message Queue）](https://docs.emqx.com/zh/enterprise/v5.5/design/inflight-window-and-message-queue.html)消息列表查看功能。

客户端会话中的飞行窗口和消息队列是 EMQX 中的两个重要特性，能够提高消息传输效率和处理离线客户端消息的能力，对于提高系统的稳定性、可靠性和性能至关重要。

当订阅者消息处理缓慢或离线时，消息将在飞行窗口与消息队列中堆积。通过查看消息列表可以评估消息堆积造成的影响范围，并进行功能调试和错误排除操作。

[查看 API 文档](https://docs.emqx.com/zh/enterprise/v5.6/admin/api-docs.html#tag/Clients/paths/~1clients~1{clientid}~1mqueue_messages/get)

## 高频日志事件限流

在 EMQX 中，消息丢弃、客户端发布授权检查失败等操作都可能导致大量的日志产生和资源消耗问题。

日志限流功能可以通过限制指定时间窗口内重复事件的记录来减少日志溢出的风险。通过仅记录第一个事件并在此窗口内抑制后续相同事件的记录，日志管理能够变得更加高效，同时不牺牲可观测性。

目前支持的日志事件如下：

- authentication_failure: 认证失败
- authorization_permission_denied: 授权权限拒绝
- cannot_publish_to_topic_due_to_not_authorized: 由于未授权无法发布到主题
- cannot_publish_to_topic_due_to_quota_exceeded: 由于配额超限无法发布到主题
- connection_rejected_due_to_license_limit_reached: 由于 License 限制达到而拒绝连接
- dropped_msg_due_to_mqueue_is_full: 由于消息队列已满而丢弃消息

[查看文档](https://docs.emqx.com/zh/enterprise/v5.6/observability/log.html#日志限流)

## 其他功能更新

- 将 Kafka 生产者客户端 `wolff` 从版本 1.10.1 升级到 1.10.2。这个最新版本为每个连接器维持一个长期的元数据连接，通过减少为动作和连接器健康检查建立新连接的频率，优化了 EMQX 的性能。
- 将几个可能导致日志泛滥的事件级别从 `warning` 改为 `info`。
- DNS 自动集群时，支持使用 DNS AAAA 记录类型进行集群发现。
- 改进了 `frame_too_large` 事件和格式错误的 `CONNECT` 包解析失败的错误报告，提供了额外的信息帮助实现故障排除。
- 规则引擎新增以下 SQL 函数用于更灵活的数据处理：
  - `map_keys()`: 返回一个 Map 中的所有键。
  - `map_values()`: 返回一个 Map 中的所有值。
  - `map_to_entries()`: 将一个 Map 转换为包含键值对的数组。
  - `join_to_string()`: 将一个数组连接成一个字符串。
  - `join_to_sql_values_string()`: 拼接数组元素为字符串，如果元素格式为字符串，将使用单引号包裹，用作拼接 SQL 语句的 VALUES 子句。
  - `is_null_var()`: 检查一个变量是否为 NULL。
  - `is_not_null_var()`: 检查一个变量是否不为 NULL。
- 在 Dashboard 配置中新增了 `swagger_support` 选项，允许启用或禁用 Swagger API 文档以提升安全性。
- 通过 2 项调整改进了日志可读性：移除日志消息中的 `mfa` 元数据以提高清晰度；调整了文本格式日志的字段顺序，新的字段顺序为：`tag` > `clientid` > `msg` > `peername` > `username` > `topic` > [其他字段]

## BUG 修复

以下是主要 BUG 修复列表：

- [#11868](https://github.com/emqx/emqx/pull/11868) 修复了会话接管后未发布遗嘱消息的问题。
- [#12347](https://github.com/emqx/emqx/pull/12347) 对 MQTT Sink 数据集成进行了更新，确保即使在数据不完整或使用了不存在占位符时，消息也始终被视为有效。此调整防止了之前发生的消息被错误地视为无效并随后被丢弃的情况。
  - 当 Payload 和 Topic 模板中的变量未定义时，现在它们被渲染为空字符串，而不是字面量 undefined 字符串。
- [#12492](https://github.com/emqx/emqx/pull/12492) 新增在 MQTT 5.0 客户端的 CONNACK 消息中返回最终的 Receive-Maximum 属性。这个值取客户端的 Receive-Maximum 和 EMQX 配置的 `max_inflight` 最小值。此前这个值未在 CONNACK 消息中发送回客户端。
- [#12541](https://github.com/emqx/emqx/pull/12541) 为 DNS 自动集群配置引入了新的参数校验，以确保 `node.name` 和`cluster.discover_strategy` 之间的联动性。例如，当使用 A 或 AAAA 记录类型时，所有节点必须使用静态IP 地址作为主机名。
- [#12566](https://github.com/emqx/emqx/pull/12566) 增强了 REST API 密钥的 bootstrap 机制：
  - bootstrap 文件中的空行将被跳过，修复了之前生成错误的行为。
  - bootstrap 文件将具有最高优先级。如果文件中的新密钥与现有密钥冲突，旧密钥将被自动删除。

更多功能变更和 BUG 修复请查看 [EMQX Enterprise 5.6.0 更新日志](https://www.emqx.com/zh/changelogs/enterprise/5.6.0)。

 

<section class="promotion">
    <div>
        免费试用 EMQX Enterprise
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
