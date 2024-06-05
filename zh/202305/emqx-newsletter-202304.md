4 月，[EMQX 开源版](https://www.emqx.io/zh)发布了 v5.0.22、v5.0.23、v5.0.24 三个版本，简化了多个配置项，新增 CRL、OCSP Stapling 支持。[EMQX 企业版](https://www.emqx.com/zh/products/emqx)发布了 v4.4.17 和 v4.4.18，提升了规则数量较多时规则引擎的性能。除此之外，还修复了多个已知错误。

[EMQX Cloud](https://www.emqx.com/zh/cloud) 本月发布了 [BYOC 版本](https://www.emqx.com/zh/cloud/byoc)，为用户提供更加强大的数据合规与安全保障。云原生团队则发布了一个可将 EMQX 集群数据导出为 Prometheus 采集格式的工具：EMQX Exporter。

## EMQX

### 简化配置项

EMQX 供了精细的配置项以满足不同场景下功能的灵活使用和性能优化配置，但于不熟悉 EMQX 的用户来说，过多的配置也给用户上手使用带来了一定难度。

从开源版 v5.0.22 开始，EMQX 将通过隐藏大量高级选项、移除非必要选项以及提供不同粒度配置手册的形式简化配置项，以降低使用门槛，提高用户的使用效率。

### CRL 与 OCSP Stapling 支持

开源版 v5.0.22 中，EMQX 引入了 CRL 与 OCSP Stapling 的支持。您可以控制每一张证书的有效性，及时吊销非法客户端证书，实现灵活且高级别的物联网应用安全保障。

### 提升规则数量较多时规则引擎的性能

在复杂的应用中，用户可能会创建数十乃至数百个规则。企业版 v4.4.17 中针对此场景进行了优化。

测试结果表明，在 32 核 32GB 服务器上，700 条简单规则、每个规则以 1000 条每秒的速度执行时，规则引擎 CPU 使用率下降到了优化前的 55% ~ 60%。

### 新增 OCPP 协议接入网关

[OCPP](https://www.openchargealliance.org/) (Open Charge Point Protocol) 是一个连接充电桩与中央管理系统的开放通信协议，旨在为电动汽车充电基础设施提供统一的通信规范。

企业版 v4.4.18 新增了 OCPP 1.6-J 版本的协议网关，能够接入符合 OCPP 规范的各品牌充电桩设备，并通过规则引擎与数据集成、REST API 等方式与管理系统（Central System）集成，帮助用户快速构建电动汽车充电基础设施。

### 重要进展

- 已完成 EMQX 上 GCP IoT Core 设备的连接认证开发，该功能可以实现 GCP IoT Core 到 EMQX 的迁移。
- MQTT 文件上传功能已经完成开发以及内部 Demo，计划在 5.1.0 版本中发布。

### 其他更新

- MQTT over QUIC 支持受密码保护的证书。
- 改进 [REST API 文档](https://docs.emqx.com/zh/emqx/v5.0/admin/api-docs.html)，提供了更清晰的 API 名称，并将常用的 API 置于前面方便查找。
- 改进文件描述符耗尽时的错误日志，方便快速定位问题。
- 规则引擎新增 `date_to_unix_ts` 时间戳转换函数。
- 废弃 `*-override.conf` 配置文件。
- 数据桥接消息缓冲支持 `memory_only` 模式，该模式可以提供更好的性能。
- 简化速率限制功能的配置并优化部分代码，重命名部分配置项、隐藏不重要的字段。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>

## EMQX Cloud

### BYOC (Bring Your Own Cloud) 版本发布

EMQX Cloud 已于 4 月 12 日上线 BYOC 1.0 Beta 版。[EMQX Cloud BYOC](https://www.emqx.com/zh/cloud/byoc) 允许用户在其现有的云基础架构环境中部署 MQTT 消息服务。用户不仅可以通过 EMQ 团队提供的专业运维管理服务**享受云计算带来的便利，同时还能获得强大的数据合规与安全保障**。

EMQX Cloud BYOC 为对数据隐私控制及定制化云服务有更高需求的企业提供了一种理想的解决方案，用户可以充分借助 EMQX 物联网 MQTT 消息服务器的强大能力，在自己的云环境中构建更加安全、高度可扩展的 MQTT 云部署，满足自身的物联网业务需求。

了解详情：[EMQX Cloud BYOC 版本发布：在您的云上体验全托管的 MQTT 消息服务](https://www.emqx.com/zh/blog/deploy-the-most-powerful-mqtt-server-in-your-own-cloud)  

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>

## EMQX Kubernetes Operator

本月即将发布的 EMQX Operator 2.1.2 中，修复了下列问题：

- 解决了当 EMQX Operator 长时间运行时内存占用过大的问题
- 修复了在某些情况下 EMQX Replicant 节点会在 EMQX Core 节点之前更新的问题

## EMQX Exporter

EMQX Exporter 是一个用于将 EMQX 集群（EMQX Prometheus API 中未包含的监控部分）的数据导出为 Prometheus 可采集格式的工具。EMQX Exporter 充当了连接 Kubernetes 和 Prometheus 之间的桥梁，它可以将 EMQX 中的指标数据转换为 Prometheus 可以读取的格式，并将这些数据暴露给 Prometheus 以便于其进行监控和报告。EMQX Exporter 可以帮助用户更好地理解 EMQX 集群的健康状况和性能表现，并能够快速发现和解决潜在的问题。

项目地址: [https://github.com/emqx/emqx-exporter](https://github.com/emqx/emqx-exporter) 

**目前支持的 EMQX 版本**

- EMQX 4.4 开源版和企业版
- EMQX 5 开源版和企业版

**支持的指标**

- license
- rule engines
- authentication
- acl
- messages
- input/output per second
- cluster status



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
