5 月，[EMQX 开源版](https://www.emqx.io/zh)发布了 v5.0.25、v5.0.26 两个版本，改进了速率限制机制，提升了多个组件的性能与安全性，并修复了已知的错误。

[EMQX Cloud](https://www.emqx.com/zh/cloud) 对控制台的操作日志模块设计和监控页部署指标进行了升级更新，方便用户更好地管理 EMQX Cloud。此外，EMQ 即将推出 EMQX 运维最佳实践系列课程。

## EMQX

### 改进速率限制

EMQX 的速率限制功能可以控制每秒钟客户端建立连接的速率，限制消息的流入数量和流量的大小速度。

合理的速率限制方案能够保障 EMQX 的稳定性与可靠性。在 5.0.25 版本中我们对速率限制进行了多项改进，以便用户能够更快实现这一目标。

1. 简化速率限制的配置项，现在仅需一行配置就能完成对应配置：

   ```
   listeners.ssl.default {
     bind = "0.0.0.0:8883"
     ...
     # 每秒建立连接速度
     max_conn_rate = "1000/s"
     # 单个客户端每秒流入消息条数
     messages_rate = "1000/s"
     # 单个客户端每秒流入消息字节数
     bytes_rate = "10MB/s"
   }
   ```

   除了配置文件方式外，用户也可以通过 Dashboard，在监听器配置中实现速率限制的热配置。

2. 优化不设置速率限制(`infinity`)时速率限制器的性能表现，减少了内存和 CPU 的使用量。

3. 移除监听器上默认的 `1000/s` 连接速率限制。

### 性能优化

1. 提高了 MQTT 数据包处理的性能。
2. 通过解除临时引用来提高内部程序读取指定配置项时的性能。
3. 优化代码的热路径(hot code path)以减少在消息处理、连接管理、认证授权等核心功能中频繁执行的代码所占用的内存，提高系统的性能和效率。
4. 优化内部指标计数机制，数值增量为 0 时不进行操作以减少性能开销。
5. 优化了同步模式下 Webhook 数据桥接的性能。
6. 为 Webhook 数据桥接添加了重试机制，通过在不阻塞缓冲层的情况下重试失败请求，在高消息速率的情况下提高吞吐量。

### 安全性增强

1. 加密 Webhook 以及 HTTP 认证/授权配置中的 `Authorization` 请求头，防止可能的敏感信息泄露。
2. 对数据桥接、认证等资源相关的日志进行脱敏，提升连接配置的安全性。

### 其他功能与改进

- 为 `emqx ctl listeners` 命令返回结果添加连接关闭计数指标 `shutdown_count`。
- 将日志追踪记录的时间精度从秒提高到微秒，以支持更精细故障排查、性能分析需求。
- 在 `force_shutdown` 配置中，将 `max_message_queue_len` 重命名为 `max_mailbox_size` ，旧名称作为别名被保留，保证向后兼容性。
- 为减少歧义与配置复杂度，隐藏 Webhook `resource_option.request_timeout` 配置项，并使用 `http` `request_timeout` 来设置该值。
- 引入一个更直观的配置项 `keepalive_multiplier`，并弃用旧的 `keepalive_backoff` 配置。在进行这个改进之后，EMQX 通过将 `keepalive` * `keepalive_multiplier` 来周期性地检查客户端的 keepalive 超时状态。

### 问题修复

我们修复了多个已知 BUG，包括通过 `systemd` 停止 EMQX 时可能导致的日志打印崩溃、规则 SQL 中 `FOREACH...DO` 语句使用的问题。

各版本详细更新日志请查看：

- [EMQX 开源版 v5.0.25](https://www.emqx.com/zh/changelogs/broker/5.0.25)
- [EMQX 开源版 v5.0.26](https://www.emqx.com/zh/changelogs/broker/5.0.26)

<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>

## EMQX Cloud

### 全新设计的操作日志

[EMQX Cloud](https://www.emqx.com/zh/cloud) 控制台对操作日志模块（原事件模块）进行了升级。现在，当您登录到 EMQX Cloud 控制台时，只需点击右上角的头像，然后点击「操作日志」，即可查看您的操作历史记录。您可以查询距离当前时间 90 天内的所有操作日志。这将帮助您更好地了解您的操作历史记录以及管理您的 EMQX Cloud 资源。

EMQX Cloud 控制台的操作日志模块记录了多种事件，包括但不限于账号登录、部署相关事件、TLS 配置、VPC 配置、数据集成配置、增值服务相关事件、子账号操作和财务相关事件等。控制台管理者可以使用操作日志模块清晰地了解关键操作和事件发生的时间、操作者、源 IP 地址和详细信息等。这些信息可以帮助您更好地追踪和识别异常操作，并增强平台的安全性和合规要求。

![EMQX Cloud 操作日志](https://assets.emqx.com/images/d30090528d36f73d6cc705ac27d04b4b.png)

### 监控页部署指标更新

监控页部署指标区域的新增指标不仅提供了更多有用信息，而且可以更加全面地了解部署的运行状况。现在包含：当前部署连接数、总 TPS、消息流入 TPS、消息流出 TPS、保留消息数、主题数、订阅数、共享订阅数。这些指标的新增可以帮助用户更好地监控和管理部署，及时发现并解决潜在问题，从而提高系统的可靠性和稳定性。

![EMQX Cloud 监控页部署指标更新](https://assets.emqx.com/images/ed2dded5af1ffbb5ce2c327c0674ebaf.png)

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>

## EMQX Kubernetes Operator

### 功能更新

在本月发布的 EMQX Operator 1.2.7-ecp.1 中，新增了以下功能：

- 添加一个新的字段 `.spec.emqxTemplate.reloaderImage` 来指定 reloader 镜像。
