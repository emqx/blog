11 月，EMQX 开源版和企业版分别发布了多个迭代版本，在安全性保障和生态集成方面又有了新的提升。

MQTT 消息云服务 EMQX Cloud 推出了新功能——自定义函数，用户可以更方便地将 IoT 数据处理为符合数据流的数据格式。

## EMQX

11 月 EMQX 开源版发布了 [v4.4.11](https://github.com/emqx/emqx/releases/tag/v4.4.11)、[v4.3.22](https://github.com/emqx/emqx/releases/tag/v4.3.22) 以及 [v5.0.10](https://github.com/emqx/emqx/releases/tag/v5.0.10)、[v5.0.11](https://github.com/emqx/emqx/releases/tag/v5.0.11) 版本，企业版发布了 [v4.3.17](https://www.emqx.com/zh/changelogs/enterprise/4.3.17) 以及 [v4.4.11](https://www.emqx.com/zh/blog/emqx-enterprise-v-4-4-11-released) 版本。

由于开源版 4.3 版本已达到 18 个月生命周期（v4.3.0 于 2021 年 5 月 8 日发布），因此 v4.3.22 是 EMQX 4.3 开源版的最后一个社区版本。

同时，我们还将 v4.4 和 v5.0 的二进制包中 Erlang/OTP 版本从 v24.1.5 升级到了 [v24.3.4.2](https://github.com/erlang/otp/releases/tag/OTP-24.3.4.2)。

### Google Cloud Pub/Sub 集成

企业版 v4.4.11 中新增了 Google Cloud Pub/Sub 集成，您可以使用 Pub/Sub 将 MQTT 消息发送到位于 Google Cloud 上的服务和托管的后端应用中，更快地基于 GCP 构建物联网应用。

![Pub/Sub 集成](https://assets.emqx.com/images/03fab0f56293d933fcbabcd762752ab4.png)

对于 Google IoT Core 用户，您无需做更多改变就能将 MQTT 传输层迁移至 EMQX，继续使用 Google Cloud 上的应用和服务。

### CRL 与 OCSP Stapling  

持有数字证书的物联网设备，如果出现私钥泄漏、证书信息有误的情况，或者设备需要永久销毁时，需要吊销对应证书以确保不被非法利用，4.4 版本中加入了 CRL 与 OCSP Stapling 功能用以解决这个问题，为您的物联网应用提供灵活且高级别的安全保障。

CRL（Certificate Revocation List，证书吊销列表） 是由 CA 机构维护的一个列表，列表中包含已经被吊销的证书序列号和吊销时间。EMQX 允许配置 CA 的请求端点并定时刷新获取 CRL，而客户端无需维护 CRL，在连接握手时通过 EMQX 即可完成证书有效性验证。

OCSP（Online Certificate Status Protocol，在线证书状态协议）是另外一个证书吊销方案，相比于 CRL， OCSP 提供了实时的证书验证能力。OCSP Stapling 是该项技术的最新改进，进一步解决了 OCSP 隐私问题和性能问题。

启用 OCSP Stapling 后，EMQX 将自行从 OCSP 服务器查询证书并缓存响应结果，当客户端向 EMQX 发起 SSL 握手请求时，EMQX 将证书的 OCSP 信息随证书链一同发送给客户端，由客户端对证书有效性进行验证。

### 固定认证与 ACL 顺序

在 EMQX 4.x 版本中添加了两个新配置，用于设置认证和 ACL 检查顺序。当启用多个认证或 ACL 插件/模块时，您可以使用逗号分隔的插件名称或别名来设置其执行顺序。

### 通过文件初始化 API 密钥

4.x 版本的另一个新特性是能够通过文件初始化 API 密钥，预设的密钥可以帮助用户在 EMQX 启动时做一些工作：如运维人员编写运维脚本管理集群状态，开发者导入认证数据到内置数据库中、初始化自定义的配置参数，在之前这些工作必须在启动完成后新建密钥对才能进行。

```
# 指定 bootstrap 文件
# etc/plugins/emqx_management.conf
management.bootstrap_user_file ="etc/bootstrap_apps_file.txt"

# 使用 {appid}:{secret} 的格式初始化密钥对
# etc/bootstrap_apps_file.txt
appid1:secret
appid2:secret2
```

### 产品优化改进

我们修复了多个已知 BUG，包括连接 MongoDB 认证失败时打印大量日志的错误，消息重发布或桥接消息到其他 MQTT Broker 时添加主题校验流程避免消息发布错误，以及 EMQX 5.0 中大规模性能测试时连接数非常大的情况下[复制节点](https://github.com/emqx/eip/blob/main/implemented/0004-async-mnesia-change-log-replication.md#rlog-replica)可能无法启动的问题。

除此之外，我们还在 MQTT 协议实现和安全设计上中添加了许多改进，包括 gen_rpc 库质询-响应式的身份验证支持。

### 更好的运维体验

4.x 版本中移除对 `GET /emqx_prometheus` 接口的认证要求，用户可以更方便地使用 Prometheus 抓取 EMQX 指标。

此外，上月发起的 v5.0 中 REST API 体验改善计划也正在进行。[EMQX 5.0.11](https://github.com/emqx/emqx/releases/tag/v5.0.11) 版本中已经包含了一些不错的改进，包括 `/gateways` API 的重新设计。



各版本详细更新日志请查看：

- [EMQX 开源版 v4.3.22](https://www.emqx.com/zh/changelogs/broker/4.3.22)
- [EMQX 开源版 v4.4.11](https://www.emqx.com/zh/changelogs/broker/4.4.11)
- [EMQX 企业版 v4.3.17](https://www.emqx.com/zh/changelogs/enterprise/4.3.17)
- [EMQX 企业版 v4.4.11](https://www.emqx.com/zh/blog/emqx-enterprise-v-4-4-11-released)
- [EMQX 开源版 v5.0.10](https://www.emqx.com/zh/changelogs/broker/5.0.10)
- [EMQX 开源版 v5.0.11](https://www.emqx.com/zh/changelogs/broker/5.0.11)

## EMQX Cloud

### 自定义函数

EMQX Cloud 全新推出了自定义函数功能，借助云平台的函数计算能力，用户可定义编写脚本，并在数据集成功能中调用该函数。设备通过 topic 上报数据，平台接收数据后，数据解析脚本对设备上报的数据进行处理，进而再转入其他的工作流当中。

自定义函数功能可应用于多种场景：如将设备端上报的非十进制数据转化为十进制数据，符合应用标准后存入到数据库中；或者是将设备中的原始数据转化、整合为符合特殊行业协议的数据格式。

![自定义函数](https://assets.emqx.com/images/362760d4bb181dea0b63739497b49d76.png)

目前自定义函数支持部署在阿里云平台上的专业版用户，每个开通服务的部署都可以获得**每个月 50000 次的免费调用次数，**现在开通服务即可以立刻使用。有关自定义函数功能详情请关注后续推送。

### 优化丢弃消息监控指标

对丢弃消息监控指标进行了优化。现在，在部署控制台中选择`指标`，在丢弃消息指示中，可以看到丢弃消息的种类：过期而被丢弃的消息以及因为队列占满而被丢弃的消息。这将使运维监控和错误排查更方便。

![优化丢弃消息监控指标](https://assets.emqx.com/images/4fe5b66355c1ebf59151d27fcea82470.png)

## EMQX Kubernetes Operator

11 月，自动化部署管理工具 EMQX Kubernetes Operator 进行了如下完善优化：

- 解决了在 v2alpha1 中，当没有发现 sts 时候出现的 crash bug
- 解决了在用户没有修改 CR 的情况下，sts 可能会一直更新的问题
- 解决了当 replicas 设置为 1 时，service 无法更新的问题
- 修复了在 status.Condition 中，lastTransitionTime 字段的错误
- 新增支持 EMQX 和 reloader 镜像 Registry



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
