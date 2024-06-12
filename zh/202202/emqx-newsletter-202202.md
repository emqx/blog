本月 EMQX 团队陆续发布了 v4.3、v4.4 的最新维护版本，其中也包括了面向社区用户的 4.4.0 正式版本，该版本包含了慢订阅、在线 Trace 等全新功能。

云服务方面，[EMQX Cloud](https://www.emqx.com/zh/cloud) 本月推出了全新增值服务，以满足不同用户的个性化需求。同时还为入门用户提供了一对一演示，现已开放预约。

## EMQX

### v5.0 新进展：beta.4 仍在推进，rc 版本即将到来

本月我们除了继续完善 v5.0 的热配置、规则引擎、网关等重要功能，同时也在持续提高测试覆盖率以确保产品的最终交付质量。beta.4 版本预计将在三月中下旬与广大用户见面，rc 版本则预计将在四月初正式发布。

### 开源版 v4.4.0 发布

开源版 v4.4.0 与 v4.3.12 保持同步，即 v4.4.0 具备了 v4.3.12 及其之前版本的所有 Bug 修复和功能改进，在此基础上，v4.4.0 带来了以下新特性：

- 支持实时跟踪客户端事件并在 Dashboard 上查看，支持跟踪 ClientID、 IP 地址和主题
- 新增慢订阅功能来统计消息传输过程中花费的时间，并记录和展示耗时较高的客户端和主题
- 支持集群节点从 v4.3 到 v4.4 滚动升级
- 支持动态修改 [MQTT Keep Alive](https://www.emqx.com/zh/blog/mqtt-keep-alive)，以适应不同的能耗策略
- MongoDB 认证支持 DNS SRV 和 TXT Records 解析，可与 MongoDB Altas 无缝对接

其他重要变更：

- **对于 Debian/Ubuntu 用户**，Debian/Ubuntu 软件包 (deb) 安装的 EMQX 现在是从 systemd 启动的。这是为了使用 systemd 的监督功能来确保 EMQX 服务在崩溃后重启。包安装服务从 init.d 升级到 systemd 已经过验证，还是建议大家在部署到生产环境之前再验证确认一下，至少要保证 systemd 在你的系统中是可用的
- 提供使用不同 Erlang/OTP 版本构建的发行包，v4.4.0 提供了使用 OTP23 和 OTP24 构建的两种发行包
- 包名中的 centos8 已经被替换为 rockylinux8

> 更多版本信息请参阅 [4.4.0 更新日志](https://www.emqx.com/zh/changelogs/broker/4.4.0)。
>
> 下载试用传送门：[EMQX 4.4.0](https://www.emqx.com/zh/downloads-and-install/broker)。

### 维护版本升级

本月我们还为当前维护版本分别发布了 v4.3.12 社区版、v4.3.7 企业版以及 v4.4.1 企业版共计 3 个版本，除了修复已知问题，我们还在这些版本中进行了一些功能改进，包括：

- 规则引擎支持会话消息丢弃事件
- 改进规则引擎执行过程的统计指标
- 支持客户端级别的消息丢弃的相关统计指标（仅 v4.4.1 企业版）

> 详细内容请参考各个版本的更新日志：[v4.3.12 社区版](https://www.emqx.com/en/changelogs/broker/4.3.12)、[v4.3.7 企业版](https://www.emqx.com/en/changelogs/enterprise/4.3.7)、[v4.4.1 企业版](https://www.emqx.com/en/changelogs/enterprise/4.4.1)。

### Webinar & Conference

本月我们举办了主题为《在 EMQX 中使用 TLS/SSL 确保 MQTT 安全》的 Webinar，EMQ 售前工程师 Kary Ware 分享了如何正确验证、安装和配置 SSL/TLS 证书等知识点。

> 视频回看链接：[Webinar: Ensure MQTT Security with TLS/SSL](https://www.youtube.com/watch?v=HRqJLi7-9KU) 

EMQX 团队提交的两次演讲被 5 月在瑞典斯德哥尔摩举行的 Code BEAM 会议接受，同时，EMQ 还成为了 Code BEAM 的 Gold Sponsor。

- [Saved Companies Hours of Downtime by Being Paranoid ](http://codesync.global/speaker/dmitrii-fedoseev/#934trace-specifications-and-chaos-engineering-advanced-testing-with-snabbkaffe)[![img](https://codesync.global/assets/img/favicon.93e85b1c.png)Dmitrii Fedoseev](http://codesync.global/speaker/dmitrii-fedoseev/#934trace-specifications-and-chaos-engineering-advanced-testing-with-snabbkaffe)
- [QUICER: Next-Generation Transport Protocol Library for BEAM](http://codesync.global/speaker/william-yang/#937quicer-next-generation-transport-protocol-library-for-beam) [![img](https://codesync.global/assets/img/favicon.93e85b1c.png)William Yang](http://codesync.global/speaker/william-yang/#937quicer-next-generation-transport-protocol-library-for-beam)

Code BEAM 会议致力于聚集 Erlang 和 Elixir 社区中的优秀人才，共同分享交流 BEAM 语言在生产中的使用，以及如何在电子商务、工程、物联网、游戏、区块链、金融科技、安全、机器学习等领域进行革新。

### OASIS Sponsorship

本月，[EMQ](https://www.emqx.com/zh) 正式成为世界知名非营利性开源和开放标准机构 OASIS （结构化信息标准促进组织, Organization for the Advancement of Structured Information Standards）最新的 Foundational Sponsor。EMQ 与 IBM 公司是全球仅有的两家最高级别成员单位。未来 EMQ 也将最大程度地参与到物联网开放标准的生命周期当中，与 OASIS 共同主导相关标准的制定、发展与应用。

详情请见：[EMQ Becomes OASIS Open’s Newest Foundational Sponsor - OASIS Open](https://www.oasis-open.org/2022/02/18/emq-becomes-oasis-open-newest-foundational-sponsor/)

## EMQX Cloud

### 新增增值服务

面对客户不尽相同的个性化需求，[EMQX Cloud](https://www.emqx.com/zh/cloud) 团队在原有产品形态基础上，新设置增值功能板块，为用户提供更多高价值功能。未来用户将可以根据自身实际需求选择开通增值服务，节省不必要的成本支出，同时又能满足定制化需求。

目前 EMQX Cloud 上架了 NAT 网关和内网负载均衡两个增值服务，主要为了有特殊需求的专业版用户进行资源的连接，为云连接架构的实现提供更加灵活的方案。

> 使用增值服务需开通 EMQX Cloud 专业版部署，首次使用用户可享受 14 天免费试用。服务详情请关注公众号后续推送。

![EMQX Cloud 增值服务](https://assets.emqx.com/images/f18513a3d828ae15c6e8c82652ed0be3.png)

### 开放一对一演示预约

初次了解我们产品的用户现在可以在官网来申请更加针对性的演示，除了系统地介绍服务和功能之外，EMQX Cloud 团队还会了解客户的具体需求，帮助用户更好地搭建自己的物联网应用架构。

> 申请入口：[EMQX Cloud 在线演示](https://www.emqx.com/zh/contact?product=cloud) 

![EMQX Cloud 在线演示](https://assets.emqx.com/images/447a23a1415ab4dfe5ed658d4cc74128.png)

### PrivateLink 双向打通验证

**私网连接**（PrivateLink）能够实现专有网络 VPC 与阿里云上的服务建立安全稳定的私有连接，简化网络架构，实现私网访问服务，避免通过公网访问服务带来的潜在安全风险。EMQX Cloud 已经验证了不同账号之间的双向打通，可以更灵活地跨账号和跨 VPC 服务访问方式，避免复杂的路由和安全配置。

对比云企业网的方式， PrivateLink 的主要优势有：

- 配置简单
- 费用更优
- 更安全，终端节点服务提供方只需要暴露部分监听端口

![PrivateLink](https://assets.emqx.com/images/db7d346d8197e074fb213f41483c165c.png)

图源：[什么是PrivateLink](https://www.alibabacloud.com/help/zh/doc-detail/161974.htm)
 

为了完成「通过世界级开源软件产品服务人类未来产业与社会」的使命，敬请期待一个更优秀的 EMQX。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
