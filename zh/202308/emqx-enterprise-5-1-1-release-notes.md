我们很高兴地宣布：[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 5.1.1 版本现已正式发布！

新版本在发布订阅授权检查中增加了 QoS 级别和保留消息检查条件以提供更灵活客户端权限控制，在规则 SQL 中新增了 3 个随机函数满足特定场景的需求。除此之外还修复了多项 BUG。

## 发布订阅权限支持检查 QoS 级别和保留消息标志

EMQX 提供了发布订阅权限控制功能，能够精确控制客户端的行为。

下表是发布订阅权限的结构组成，在条件部分，此前版本仅支持主题，用于指定允许或拒绝的客户端主题范围，EMQX Enterprise 5.1.1 中新增了 QoS 级别和保留消息标志的判断。

相比只检查主题的旧版规则，新规则的组成更全面，可以灵活地从多个维度控制客户端的访问行为，提升系统安全性。

| **权限**  | **客户端(匹配方式)**     | **操作**  | **条件**              |
| --------- | ------------------------ | --------- | --------------------- |
| 允许/拒绝 | 客户端 ID/用户名/IP 地址 | 发布/订阅 | 主题/**QoS/保留消息** |

这是一个向后兼容的功能扩展，用户可以继续使用既有配置无需任何变更。如果要启用新功能只需更新相关数据和配置即可，以 MySQL 数据源为例：

```
-- 之前
-- 权限数据
INSERT INTO mqtt_acl(username, topic, permission, action)
  VALUES('emqx_u', 't/1', 'deny');

-- EMQX 权限查询 SQL
SELECT action, permission, topic FROM mqtt_acl where username = ${username};


-- 现在
-- 权限数据，新增 qos_i, retain_i
INSERT INTO acl(username, topic, permission, action, qos_i, retain_i)
  VALUES('username', 't/1', 'deny', 'publish', 1, 1);

-- EMQX 权限查询 SQL
SELECT permission, action, topic, qos_i as qos, retain_i as retain
          FROM mqtt_acl WHERE username = ${username};
```

## 规则 SQL 支持 random 与 UUIDv4 随机函数

规则引擎的 SQL 语句新增了3个随机数生成函数，用于满足特定场景的需求。

### random **函数**

random 函数用于生成 0(包含) 到 1(不包含) 之间的随机浮点数，执行示例如下：

```
random() = 0.521534842864676
random() * 100 = 32.04042160431394
```

random 函数可用于对海量数据进行抽样和模拟。例如，该 SQL 语句利用 random 在 where 条件中进行概率过滤，表示只有 50% 的消息会匹配规则并写入数据库:

```
SELECT
  *
FROM
  "t/#"
WHERE 
  random() > 0.5
```

### **uuid_v4 函数**

UUID(通用唯一标识符)是一种通用的 ID 生成方案，由 32 个十六进制字符组成,以 8-4-4-4-12 的格式使用连字符分隔。其中 UUID 版本 4 (UUIDv4) 通过随机数生成，可以保证强随机性，使用范围更为广泛。

除了标准 UUID 外，EMQX 还提供了没有连字符的 UUID 函数，执行示例如下：

```
uuid_v4() = 04b31953-2f70-4ca0-a409-5c5f6b0a839f
uuid_v4_no_hyphen() = df272a785ac24d7fb82aa29af9e82dd8
```

UUID 函数可以作为数据库主键或设备与消息的唯一标识，也可用于数据跟踪和审计。例如，该 SQL 语句在事件上下文中添加了 `myid` 字段，后续的数据桥接中可以使用 `${myid}` 语法提取生成的 UUID，可用作数据主键或消息的唯一标识：

```
SELECT
  uuid_v4() as myid,
  *
FROM
  "t/#"
```

## Kafka 桥接支持设置消息头

Kafka 消息头（headers）允许生产者将消息元数据放入消息，用于传递额外上下文，实现消息追踪、去重以及数据透传等功能。

在 EMQX Enterprise 5.1.1 中，你可以在 Kafka 数据桥接中定义需要传输的 Kafka 消息头，实现设备信息(例如客户端ID、用户名)、消息类型、QoS级别，乃至 MQTT 5.0 用户属性（User Property ）的透传。这些元数据可以帮助后端应用更轻松地解析处理海量的物联网数据。

![桥接 MQTT 数据到 Kafka](https://assets.emqx.com/images/5bc4bda7f080da75b5ff54cab92b297c.png)

## BUG 修复

以下是主要 BUG 修复列表：

- 修复主题重写验证问题，目标主题不再允许使用通配符 [#11004](https://github.com/emqx/emqx/pull/11004)。
- 添加了对桥接资源 `worker_pool_size` 的最大数量的验证。现在最大数量为 1024，以避免因不合理数量的工作进程导致大内存消耗 [#11106](https://github.com/emqx/emqx/pull/11106)。
- 修复 Webhook 桥接异步模式下，4XX 和 5XX HTTP 状态码被统计为成功指标的问题 [#11162](https://github.com/emqx/emqx/pull/11162)。
- REST API 使用 `DELETE` 请求操作不存在的资源时，一致性地返回 `404` 状态码 [#11211](https://github.com/emqx/emqx/pull/11211)。
- 修复了 InfluxDB 桥接写入配置中，某个字段混用小数和整数时可能会导致 Influx Line Protocol 序列化失败的问题 [#11223](https://github.com/emqx/emqx/pull/11223)。

更多功能变更和 BUG 修复请查看 [EMQX Enterprise 5.1.1 更新日志](https://www.emqx.com/zh/changelogs/enterprise/5.1.1)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
