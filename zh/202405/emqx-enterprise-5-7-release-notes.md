[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 5.7.0 版本现已正式发布！

在这个版本中，我们引入了一系列新的功能和改进，包括会话持久化、消息 Schema 验证、规则引擎调试与追踪测试等功能。此外，新版本还进行了多项改进以及 BUG 修复，进一步提升了整体性能和稳定性。

## 会话持久化

EMQX 内置的会话持久化（Durable Session）功能提供了强大的持久性和高可用性。该功能允许将 MQTT 持久会话（Persistent Session）及其消息存储到磁盘上，并在 EMQX 集群的多个节点之间持续复制会话元数据和 MQTT 消息。

该功能具备灵活的配置参数，通过配置复制因子，用户可以自定义每条消息或会话的副本数量，从而在持久性和性能之间实现平衡。

![EMQX Cluster](https://assets.emqx.com/images/35b93a2ccd5debb9b279925c957ac011.png)

与内存存储相比，将 MQTT 消息存储在共享的、复制的持久存储中，可以降低在线和离线会话的内存使用量，支持更大规模的会话和消息处理。会话持久化功能还实现了有效的故障转移和恢复机制，确保服务的连续性和高可用性，从而提高系统的可靠性。

[查看文档](https://docs.emqx.com/zh/enterprise/v5.7/durability/durability_introduction.html)

## 消息 Schema 验证

EMQX 内置了 Schema 验证功能，用于验证 MQTT 消息的结构和格式，对于不符合格式的消息可以丢弃或断开其客户端连接，并打印日志和触发规则引擎事件以方便用户进行进一步的处理。

Schema 验证可使用 JSON Schema、Protobuf 和 Avro 等多种格式的模式，或使用内置的 SQL 语句验证来自指定主题的消息格式。通过据格式校验，可以及早发现并屏蔽这些不合规消息,保证系统稳定可靠。

 ![消息 Schema 验证](https://assets.emqx.com/images/934f3752314a746ac87882ab3a223f1d.png)

除了验证外，同一份 Schema 还能用于 EMQX 规则引擎的 Schema 编解码和 Schema 检查功能，以及外部数据系统和业务流程中，帮助用户实现：

- **数据完整性**：验证 MQTT 消息的结构和格式，以确保数据的一致性和正确性。
- **数据质量**：强制执行数据质量，检查缺失或无效的字段、数据类型和格式，可以确保数据的质量和一致性。
- **统一的数据模型**：确保整个团队和项目中使用统一的数据模型，减少数据不一致和错误。
- **重用和共享**：允许团队成员重用和共享 Schema，可以提高团队成员之间的协作效率，减少重复工作和错误。

[查看文档](https://docs.emqx.com/zh/enterprise/v5.7/data-integration/schema-validation.html)

## **规则支持调试与追踪**

规则引擎现在提供了 DEBUG 与追踪功能，允许使用模拟数据或真实客户端触发规则，执行规则 SQL 以及规则中添加的所有动作，并获取每个步骤的执行结果。

下图是功能的截图，当规则 SQL 或任意动作执行失败时，可以在 Dashboard 页面上看到出错的记录，并快速定位到对应动作，查看结构化的错误信息以进行错误排查。

![规则页面](https://assets.emqx.com/images/96b706704cb6881856755a8f917275d9.png)

从图中可以看到，规则被触发了 4 次，前 3 次规则执行完全成功，第 4 次由于 HTTP 服务动作执行失败。结合错误日志，能够看到错误原因是 HTTP 服务器响应了 302 状态码。

相较于此前的 SQL 测试，规则 DEBUG 与追踪功能能够验证整个规则是否按预期工作，快速排查并解决存在的问题。这不仅加快了开发速度，还确保了规则在实际运行时能够如期执行，避免在真实环境中出现故障。

[查看文档 ](https://docs.emqx.com/zh/enterprise/v5.7/data-integration/rule-get-started.html#测试规则)

## 规则动作支持快速输入变量

在此前版本中，规则动作支持使用 `${var}` 占位符语法来使用规则处理结果中的变量，以实现灵活的配置，例如，动态的构造 HTTP 请求、MySQL 的 INSERT 语句、AWS S3 对象键等。这一功能带来了极大的灵活性，但用户需要自主推导当前规则 SQL 中可用的变量，并完整手动输入。这增加了使用难度，且容易出错。

在本次发布中，Dashboard 的动作配置页面为支持使用占位符变量的输入框添加了动态输入提示。类似编辑器的代码提示功能，根据当前规则 SQL 自动推导出可用的变量，在用户输入过程中快速提示可用的值。这不仅方便用户精准进行功能配置，还显著减少了出错的可能性。

 ![规则动作支持快速输入变量](https://assets.emqx.com/images/590d0fa6fa377c3f05834696d04ba637.png)

## 日志追踪功能增强

在日志追踪中新增了以下两个特性：

1. **支持指定规则 ID 跟踪规则执行结果**：精准地跟踪和调试某一特定规则的执行过程，日志输出将包含规则 SQL 的执行结果，以及与规则中添加的所有动作的执行过程日志，以便快速定位和排查问题。
2. **支持设置日志追踪输出格式为 JSON**：更便于自动化日志处理和分析，提升数据处理效率。

[查看文档](https://docs.emqx.com/zh/enterprise/v5.7/observability/tracer.html#追踪指定规则)

## 客户端属性

客户端属性是 EMQX 提供的一种机制，允许使用键值对的方式为每个客户端设置额外的属性。

属性值可以从 MQTT 客户端连接信息（如用户名、客户端 ID、TLS 证书）处理生成，也可以从认证成功返回的附带的数据中设置。例如：

添加配置，在客户端连接时以 `:` 分割客户端 ID 并将第一段作为 VIN 属性：

```
mqtt.client_attrs_init = [
  {
    expression = "nth(1, tokens(clientid, ':'))"
    set_as_attr = "VIN"
  }
]
```

属性可以用于 EMQX 的认证授权、数据集成和 MQTT 扩展功能等功能中。以 MySQL 授权检查为例，可以配置查询 SQL，根据客户端属性中的 VIN 查找客户端具有的发布订阅权限：

```sql
SELECT 
  permission, action, topic, qos, retain 
FROM mqtt_acl 
  WHERE VIN = ${client_attrs.VIN}
```

相较于直接使用客户端 ID 等静态属性，客户端属性能够更灵活的用在各类业务场景中，并简化开发流程，增强开发工作的适应性和效率。

[查看文档](https://docs.emqx.com/zh/enterprise/v5.7/client-attributes/client-attributes.html)

## JWT 认证到期断开客户端连接

JWT 规范中带有过期时间属性，在签发 Token 时允许声明一个过期时间。在此之前，EMQX 的 JWT 认证中仅在客户端连接时检查这一属性，在连接成功后，即使在 JWT 过期客户端也能保持连接。

本次发布中，EMQX 在 JWT 认证中添加了令牌过期后断开 MQTT 连接的功能。默认情况下该功能是启用的，以避免潜在的安全隐患，从而提升系统的整体安全性。

如果要保留以前的行为，请关闭 JWT 认证器设置中**过期后断开连接**选项。

![客户端认证](https://assets.emqx.com/images/c116403c926ec36bf327d5762912a581.png)

[查看文档](https://docs.emqx.com/zh/enterprise/v5.7/access-control/authn/jwt.html)

## 插件开发支持热配置与自定义 UI

此前 EMQX 已经支持了插件，能够用来扩展实现自定义的功能。在一些插件中，可能需要用户填写相应的配置参数。

本次发布为插件添加了参数热配置功能，并允许用户通过 Avro Schema 来声明管理参数配置所需的 UI 页面，EMQX Dashboard 会在插件管理页面中自动加载。

开发者只需专注于后端业务逻辑的实现，UI 页面由系统自动生成，减少了开发工作量。对于用户，则可以直观地配置插件参数，提升用户体验。

这是插件中可选的功能，用户仍然可以使用纯后端进行开发。

[查看文档](https://docs.emqx.com/zh/enterprise/v5.7/extensions/plugins.html#为插件编写-config-schema-可选)

## 其他功能

1. Apache IoTDB 数据集成支持 IoTDB v1.3.0 版本以及批量插入功能，提高了数据写入性能。
2. 将错误格式导入内置身份验证数据库时，提供了更具体的错误信息，便于用户快速定位问题。
3. RocketMQ 添加了对命名空间和密钥调度策略的支持，实现与阿里云上托管的 RocketMQ 集成。

## BUG 修复

以下是主要 BUG 修复列表：

- [#12653 ](https://github.com/emqx/emqx/pull/12653)规则引擎的 `bin2hexstr` 函数现在支持位大小不能被 8 整除的参数，例如 `subbits` 函数的返回值。

- [#12657](https://github.com/emqx/emqx/pull/12657) 修复规则引擎 SQL 不允许将任何表达式作为数组元素的问题，现在可以使用任何表达式作为数组元素，例如：

  ```sql
  SELECT
    [21 + 21, abs(-abs(-2)), [1 + 1], 4] as my_array
  FROM 
    "t/#"
  ```

- [#12765 ](https://github.com/emqx/emqx/pull/12765)确保统计数据 `subscribers.count` `subscribers.max` 包含共享订阅者，此前只包含非共享订阅者。

- [#12812](https://github.com/emqx/emqx/pull/12812) 修复了连接器因健康检查阻塞，导致更新或删除连接器超时的问题。

- [#12996 ](https://github.com/emqx/emqx/pull/12996)修复保留消息 `emqx_retainer` 进程泄漏问题。此前客户端在接收保留消息时断开连接可能会导致进程泄漏。

- [#12871](https://github.com/emqx/emqx/pull/12871) 修复疏散节点导致的节点启动问题。此前，如果节点疏散过程中关闭了 EMQX，则 EMQX 将无法重新启动。

- [#12888](https://github.com/emqx/emqx/pull/12888) 修复导入备份数据后 License 相关的配置丢失问题。

- [#12895](https://github.com/emqx/emqx/pull/12895) 添加了 DynamoDB 连接器和动作中一些必要但缺失的配置。

更多功能变更和 BUG 修复请查看 [EMQX Enterprise 5.7.0 更新日志](https://www.emqx.com/zh/changelogs/enterprise/5.7.0)。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
