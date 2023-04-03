3 月，EMQX 开源版发布了 v5.0.19、v5.0.20 以及 v5.0.21 三个版本，提供 Rocky Linux 9 以及 MacOS 12 Intel 平台安装包。企业版发布了 v4.4.15 以及 v4.4.16 版本，提供了 Apache IoTDB 支持、HStreamDB 最新版本的适配、MongoDB 6.0 支持等多个更新。除此之外，还修复了多个已知错误。

云服务方面，EMQX Cloud Serverless 正式版即将于四月初正式上线。该版本通过多租户技术和按量计费的模式，为用户提供了极速的部署创建和有效的成本控制。

## EMQX

### Rocky Linux 9 与 MacOS 12 Intel 平台安装包

从开源版 v5.0.21 开始，EMQX 提供了 Rocky Linux 9 （兼容 Red Hat Enterprise Linux 9）操作系统安装包。此前 MacOS 12 只有 Apple Silicon 平台的安装包，本次发布后加入了 Intel 平台的支持。

### EMQX Helm Chart 中添加 extraVolumeMounts

extraVolumeMounts 是 Kubernetes Pod 中添加额外的卷挂载配置，Pod 可以将多个卷挂载到容器中，以方便应用程序访问数据或共享存储资源。

EMQX 在 Helm Chart 中添加了 extraVolumeMounts 的支持，能够将自定义的 ACL 规则文件 `acl.conf`、TLS 证书、配置等文件挂载到 EMQX 实例。

### 安全增强

#### 调整黑名单作用范围

当 MQTT 会话被接管时（即 `clean_start = fasle` 的客户端断开连接后发起重连），将检查并过滤会话中的消息。

如果消息发布者客户端 ID 已被黑名单封禁，对应的消息将被清除以避免发送给订阅者。

#### 错误日志中隐藏 HTTP 请求 Body

在使用 HTTP 服务进行客户端认证检查时，请求 Body 可能会携带客户端的明文密码，如果输出到日志中可能会造成泄露，因此 EMQX 在错误日志中隐藏了请求 Body。

这是一个底层驱动改动，对应的授权以及数据桥接 WebHook 也会受到此影响。

### 企业版 v4.4.15 新功能

企业版 v4.4.15 提供了 Apache IoTDB 数据集成、HStreamDB 最新版适配、MongoDB 6.0 支持等诸多特性，详情请参考： [EMQX Enterprise 新版发布：支持 Apache IoTDB、更新 HStreamDB 与 MongoDB 适配版本](https://www.emqx.com/zh/blog/emqx-enterprise-v-4-4-16-released)。

### 问题修复

我们修复了多个已知 BUG，包括 Swagger API 文档渲染崩溃、规则引擎 API 返回的错误可读性较差问题。

>各版本详细更新日志请查看：
>
>- [EMQX 开源版 v5.0.19](https://www.emqx.com/zh/changelogs/broker/5.0.19)
>- [EMQX 开源版 v5.0.20](https://www.emqx.com/zh/changelogs/broker/5.0.20)
>- [EMQX 开源版 v5.0.21](https://www.emqx.com/zh/changelogs/broker/5.0.21)
>- [EMQX 企业版 v4.4.15](https://www.emqx.com/zh/changelogs/enterprise/4.4.15)
>- [EMQX 企业版 v4.4.16](https://www.emqx.com/zh/changelogs/enterprise/4.4.16)


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>


## EMQX Cloud

### Serverless 正式版发布

EMQX Cloud 将于 4月 1 日上线 Serverless 1.0 正式版。EMQX Cloud Serverless 是基于 EMQX 共享集群的全托管 MQTT 服务，用户只需几秒钟即可完成部署的创建。该版本采用按实际使用资源量即连接分钟数计费的模式，并且提供每个月 100 万的免费连接分钟数，可以帮助独立开发者或小微企业以更低的成本高效开发物联网应用，非常适合项目的研发、测试、业务早期等应用场景。

同时 Serverless 正式版上线了消费限额设定功能，用户可以为自己的部署设定每个月的最大使用额度，更好地掌控财务状况。当然也可以将每月的消费限额设置为 0，这样就可以获得一个永久免费使用的 Serverless MQTT 服务。

### 工单系统优化

现在创建工单时可以关联相关的部署，以便技术支持团队掌握相关信息，进行更好的支持服务。同时现在可以查看已经关闭的工单，更方便地回溯历史问题。

### 新的可用区

EMQX Cloud 国内站增加了阿里云成都区域。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
