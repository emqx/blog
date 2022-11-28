我们很高兴地告诉大家，[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 4.4.11 版本正式发布！

在此版本中，我们发布了 CRL 与 OCSP Stapling 为客户端提供更灵活的安全防护，新增了 Google Cloud Pub/Sub 集成帮助您通过 Google Cloud 各类服务发掘更多物联网数据价值，还加入了满足自动化运维需要的预定义 API 密钥功能。除此之外，我们还修复了多项 BUG。

## CRL 与 OCSP Stapling

此前版本中，通过 EMQX 内置的 SSL/TLS 支持，您可以使用 X.509 证书实现客户端接入认证与通信安全加密，本次发布的版本在此基础上新增了 CRL 与 OCSP Stapling 功能。

持有数字证书的物联网设备，如果出现私钥泄漏、证书信息有误的情况，或者设备需要永久销毁时，需要吊销对应证书以确保不被非法利用，CRL 与 OCSP Stapling 就是解决这一问题的关键。

CRL（Certificate Revocation List，证书吊销列表） 是由 CA 机构维护的一个列表，列表中包含已经被吊销的证书序列号和吊销时间。EMQX 允许配置 CA 的请求端点并定时刷新获取 CRL，而客户端无需维护 CRL，在连接握手时通过 EMQX 即可完成证书有效性验证。

OCSP（Online Certificate Status Protocol，在线证书状态协议）是另外一个证书吊销方案，相比于 CRL， OCSP 提供了实时的证书验证能力。OCSP Stapling 是该项技术的最新改进，进一步解决了 OCSP 隐私问题和性能问题。

启用 OCSP Stapling 后，EMQX 将自行从 OCSP 服务器查询证书并缓存响应结果，当客户端向 EMQX 发起 SSL 握手请求时，EMQX 将证书的 OCSP 信息随证书链一同发送给客户端，由客户端对证书有效性进行验证。

![CRL 与 OCSP Stapling 工作流程](https://assets.emqx.com/images/a5ace2d3c1ebbb2299997896e706c37a.png)

<center>CRL 与 OCSP Stapling 工作流程</center>

通过 CRL 与 OCSP Stapling 功能，您可以控制每一张证书的有效性，及时吊销非法客户端证书，为您的物联网应用提供灵活且高级别的安全保障。

## Google Cloud Pub/Sub 集成

[Google Cloud Pub/Sub](https://cloud.google.com/pubsub) 是一种异步消息传递服务，旨在实现极高的可靠性和可扩缩性。

现在，您可以通过 EMQX 规则引擎的 GCP Pub/Sub 集成能力，快速建立与该服务的连接，这能够帮助您更快的基于 GCP 构建物联网应用：

- **使用 Google 的流式分析处理物联网数据**：以 Pub/Sub 以及 Dataflow 和 BigQuery 为基础而构建整体解决方案，实时提取、处理和分析源源不断的 MQTT 数据，基于物联网数据发掘更多业务价值。
- **异步微服务集成：**将 Pub/Sub 作为消息传递中间件，通过 pull 的方式与后台业务集成；也可以推送订阅到 Google Cloud 各类服务如 Cloud Functions、App Engine、Cloud Run 或者 Kubernetes Engine 或 Compute Engine 上的自定义环境中。

![通过规则引擎与 Pub/Sub 集成](https://assets.emqx.com/images/231c11c8fbf7713bb46e461c7b28c410.png)

<center>通过规则引擎与 Pub/Sub 集成</center>

对于 Google IoT Core 用户，您无需做更多改变就能将 MQTT 传输层迁移至 EMQX，继续使用 Google Cloud 上的应用和服务。

## 通过文件初始化 API 密钥

本次发布提供了 API 密钥初始化能力，允许您在启动 EMQX 前通过特定文件设置密钥对。

预设的密钥可以帮助用户在 EMQX 启动时做一些工作：如运维人员编写运维脚本管理集群状态，开发者导入认证数据到内置数据库中、初始化自定义的配置参数。

[EMQX Kubernetes Operator ](https://www.emqx.com/zh/emqx-kubernetes-operator)也基于此特性来实现集群启动时的配置和管理操作。

```
# 指定 bootstrap 文件
# etc/plugins/emqx_management.conf
management.bootstrap_user_file ="etc/bootstrap_apps_file.txt"

# 使用 {appid}:{secret} 的格式初始化密钥对
# etc/bootstrap_apps_file.txt
appid1:secret
appid2:secret2
```

## BUG 修复

以下是主要 BUG 修复，完整 BUG 修复列表请参考 [EMQX 企业版 4.4.11 更新日志](https://www.emqx.com/zh/changelogs/enterprise/4.4.11)。

- 改进规则的 "最大执行速度" 的计数，只保留小数点之后 2 位 [#9185](https://github.com/emqx/emqx/pull/9185)。 避免在 dashboard 上展示类似这样的浮点数：`0.30000000000000004`。
- 修复在尝试连接 MongoDB 数据库过程中，如果认证失败会不停打印错误日志的问题 [#9184](https://github.com/emqx/emqx/pull/9184)。
- 限速 “Pause due to rate limit” 的日志级别从原先的 `warning` 降级到 `notice` [#9134](https://github.com/emqx/emqx/pull/9134)。
- 修正了 `/status` API 的响应状态代码 [#9210](https://github.com/emqx/emqx/pull/9210)。 在修复之前，它总是返回 `200`，即使 EMQX 应用程序没有运行。 现在它在这种情况下返回 `503`。
- 修复规则引擎的消息事件编码失败 [#9226](https://github.com/emqx/emqx/pull/9226)。 带消息的规则引擎事件，例如 `$events/message_delivered` 和 `$events/message_dropped`, 如果消息事件是共享订阅产生的，在编码（到 JSON 格式）过程中会失败。 影响到的版本：`v4.3.21`, `v4.4.10`, `e4.3.16` 和 `e4.4.10`。
- 修复调用 'DELETE /alarms/deactivated' 只在单个节点上生效的问题，现在将会删除所有节点上的非活跃警告 [#9280](https://github.com/emqx/emqx/pull/9280)。
- 在进行消息重发布或桥接消息到其他 MQTT Broker 时，检查 topic 合法性，确定其不带有主题通配符 [#9291](https://github.com/emqx/emqx/pull/9291)。
- 关闭管理端口（默认为8081）上对 HTTP API `api/v4/emqx_prometheus` 的认证，Prometheus 对时序数据抓取不在需要配置认证 [#9294](https://github.com/emqx/emqx/pull/9294)。
- 修正了在 Kafka Consumer 中选择 `reset_by_subscriber` 偏移重置策略的选项。
- 修复了 SQL Server 资源中，无法在 `server` 字段里使用除 `1433` 之外的端口的问题。
- 解决从 e4.4.5 以及更早的版本升级 EMQX 的时候，Kafka 资源的认证类型从 `PLAIN` 变成了 `NONE` 的错误。

## 结语

除了企业版 4.4.11 外，同期 EMQX 还发布了包括开源版在内的另外 3 个版本，请参考：

- [EMQX 企业版 4.3.17 更新日志](https://www.emqx.com/zh/changelogs/enterprise/4.3.17)
- [EMQX 开源版 4.3.22 更新日志](https://www.emqx.com/zh/changelogs/broker/4.3.22)
- [EMQX 开源版 4.4.11 更新日志](https://www.emqx.com/zh/changelogs/broker/4.4.11)

 



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
