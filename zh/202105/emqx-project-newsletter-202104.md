> 本文内容来自 EMQ 欧洲研发团队

随着四月的结束，距离 EMQX 4.3.0 正式版的发布又更近了一些。我们也已逐步将研发重心迁移到 5.0 上，正式开启了 5.0 版本的开发阶段。社区 Open Day 与 Demo Day 也如期举行，感谢研发团队的付出和社区成员的支持。



## 4.3.0 版本即将发布，性能提升

4.3.0 依旧保持着快速推进，目前已经已经来到了 4.3-rc.5。我们仍在为了给大家带来更好的使用体验而不断努力，在当前版本中又对通配符订阅进行了问题修复与性能提升，力求让 4.3.0 正式版不辜负大家的等待。我们将在下期 Demo Day 中为大家演示 4.3.0 版本中使通配符订阅速度提高 10 倍的有关详情，请关注后续的活动预告。

## 升级保障

我们近期发布了 4.0.13 和 4.2.11 两个修复版本，修复了数据导入和导出的一些问题，以确保升级到 4.3 版本时数据的顺利迁移。

## 更高质量

我们的测试团队已经为 PostgreSQL、MySQL、Redis 等数据库添加了自动化集成测试，将陆续支持更多数据库。

## 灵活性

我们 fork 了 Erlang/OTP 以实现 Mnesia 数据同步的性能优化。同时还添加了一个补丁，允许 atuto-probing 网络对等体的 IPv6 堆栈支持。所有的改变都与上游兼容，这意味着 EMQX 可以在上游的 Erlang/OTP 上顺畅地运行。

## 连接性（MQTT over QUIC）

我们实现了 MQTT-over-QUIC 项目的一个新的里程碑：对在 EMQX 中运行的 QUIC 进行完全集成演示（视频回放：[https://www.bilibili.com/video/BV1y64y1m72P](https://www.bilibili.com/video/BV1y64y1m72P)）。下一步我们将使其为生产做好准备。详情请在 GitHub 查看项目时间表（[https://github.com/emqx/emqx/discussions/4379](https://github.com/emqx/emqx/discussions/4379)）。

## 伸缩性（Rlog）

Rlog 的最新进展已在 Demo Day 中进行了演示（视频回放：[https://www.bilibili.com/video/BV1Ub4y1D7kD/?spm_id_from=333.788.recommend_more_video.-1](https://www.bilibili.com/video/BV1Ub4y1D7kD/?spm_id_from=333.788.recommend_more_video.-1)），EMQX 节点现在可以异步同步路由信息了！这将使 EMQX 集群更加稳定，更好弹性伸缩和云原生支持。

## 下一代：5.0 版本功能

- 我们已经基于 JSON 处理的事实标准 [jq ](https://stedolan.github.io/jq/)的开源内核构建了 NIF 绑定。它将被应用与 EMQX 规则引擎中，为 JSON 数据流处理提供灵活强大的扩展。
- HOCON 将是 EMQX 的下一代配置，我们正在为 HOCON 增加 schema 校验支持。在 EMQX 5.0 中，该 schema 将被用于配置文件的校验和动态修改配置的校验。 



## 社区

- [askemq.com](https://askemq.com) 社区的周 PV 已经达到了 5000，越来越多的用户选择在 askemq.com 交流讨论，我们也看到有很多热心的社区伙伴与我们的工程师一起参与社区支持，对此我们感到欣慰与振奋。
- 在过去两个月，EMQ 各项目团队陆续开展了包括 Demo Day（项目最新进展分享）、Open Day（项目改进建议与长期发展规划的讨论）、Sharing Day（技术知识分享） 在内的社区活动，EMQX 团队也积极参与其中。目前为止已成功举办多期，与众多社区成员进行了分享交流。未来的活动预告信息将在 EMQ 官网活动页面中发布。回放视频将发布在 EMQ 官方 B 站账号（EMQ-映云科技）。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
