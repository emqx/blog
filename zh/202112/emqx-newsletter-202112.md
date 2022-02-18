本月，集成了在线 Trace、慢订阅等全新功能的 EMQX 企业版 v4.4.0 正式发布，开源版也来到了 4.4-beta.1 版本，正式版不久后将与大家见面。我们也针对近期发现的各项问题发布了开源版 v4.3.11 和企业版 v4.3.6，进一步提升了软件的稳定性。

此外，EMQX 5.0-beta.2 版本本月已正式发布，beta.3 版本也在本月完成了代码开发工作，目前已进入测试阶段。

云服务方面，EMQX Cloud 本月针对用户体验进行了进一步产品优化，新增了部署连接指引及相关帮助文档，在交互上更加友好，为用户提供更便捷的使用体验。

## EMQX：各版本进展顺利

### EMQX 开源项目 GitHub Star 数突破 9K

我们非常高兴地看到 EMQX 项目（[https://github.com/emqx/emqx](https://github.com/emqx/emqx) ）的 GitHub Star 数在本月突破了 9K！这离不开广大社区用户和开发者对我们的支持。EMQX 团队将继续致力于为大家提供高性能、高可用的 MQTT 消息服务器，也欢迎大家通过 GitHub 与我们交流，提交项目 issue 或 PR。

![EMQX GitHub](https://static.emqx.net/images/ceeea48431795ee2d40c81140d60474d.png)

### 最新发布：EMQX 企业版 v4.4.0

最新发布的企业版 v4.4.0 新增了 3 项集成支持，同时增加了 2 个新功能帮助用户提升异常诊断能力。更新详请可以参阅 [Enterprise 4.4.0 Release Note](https://www.emqx.com/zh/changelogs/enterprise/4.4.0)。

规则引擎新增对 InfluxDB 2.0 & InfluxDB Cloud、 SAP Event Mesh、 MatrixDB 的支持，同时增加MongoDB 集成支持 DNS SRV 和 TXT Records 解析，可以与 MongoDB Altas 无缝对接，增强了与云服务的集成能力。

新增的在线 Trace 和慢订阅统计功能则通过在 Dashboard 上对客户端和主题的追踪与管理，改善了用户自行排查、诊断客户端异常行为时的体验，帮助用户及时发现生产环境中消息堵塞等异常情况，提高了用户感知能力，方便用户及时调整相关服务。

此外，新版本还支持动态修改 MQTT Keep Alive，允许用户服务通过 HTTP API 随时更新客户端的 Keep Alive，这一功能将为车联网行业 T-BOX 等设备在不同工况下的能耗策略切换场景提供便利。

4.4.0 版本适配了 Erlang/OTP 24，目前 EMQX 官网也默认提供基于 OTP 24 的安装包下载。我们也保留了基于 OTP 23 的版本，用户可以点击[EMQX Enterprise下载页面](https://www.emqx.com/zh/downloads-and-install?product=enterprise&version=4.4.0&os=Docker&oslabel=Docker)右侧的 `历史版本` 来访问所有版本。我们也在安装包的包名中包含了 OTP 版本以帮助大家分辨。

对于正在使用 EMQX Enterprise 4.3.x 的用户，现在我们可以更方便地将 EMQX 从 4.3 版本滚动升级到 4.4 版本。EMQX 4.4 的节点现在能够和 EMQX 4.3 的节点运行在同一个集群下，当然前提是并未启用 4.4.x 中的全新功能（这可能导致集群调用出错）。基于这一点，我们可以依次将集群中的 4.3 节点替换为 4.4 节点，最终在不停止集群服务的情况下，完成版本升级。

### 4.3 版本情况：企业版 v4.3.6 支持 Ali Lindorm 数据库

本月我们依旧陆续从社区，从测试团队收到了一些问题反馈，在完成这些问题的修复验证后，我们分别发布了开源版 4.3.11 和企业版 4.3.6，欢迎广大用户升级至最新版本以获得更佳的稳定性体验，可以访问以下链接查看相应的修复日志：[EMQX 4.3.11](https://www.emqx.com/zh/changelogs/broker/4.3.11)，[EMQX Enterprise 4.3.6](https://www.emqx.com/zh/changelogs/enterprise/4.3.6)。

企业版 4.3.6 除问题修复以外，我们还完成了规则引擎对 Ali Lindorm 数据库的支持，Lindorm 是面向物联网、工业互联网、车联网等设计和优化的云原生多模超融合数据库。EMQX 目前支持 Lindorm 的时序数据引擎，并已通过了 10w/s 的写入性能测试，后续版本中我们还将持续优化。

### 5.0 新进展：beta.2 发布，beta.3 进入测试阶段

本月初我们完成了 5.0-beta.2 的测试工作并将其正式发布，该版本我们主要关注在 HTTP API 的持续改进上，想要抢先体验的用户可以访问 [EMQX 5.0-beta.2 Released](https://github.com/emqx/emqx/releases/tag/v5.0-beta.2) 下载试用。

接下来的 beta.3 我们期望给用户带来一个早期的 Dashboard 版本，以满足更多想要提前一睹 5.0 风采的用户。目前代码开发工作基本完成，测试工作已经紧锣密鼓地展开，预计下个月 beta.3 将与大家正式见面。

## EMQX Cloud：交互优化帮助用户轻松上手

### 部署连接指引

在 [EMQX Cloud](https://www.emqx.com/zh/cloud) 控制台中初次创建部署时，除了关键功能点的引导介绍，用户还将获得从连接到部署相关的知识点指导说明，帮助用户从建立连接、认证设置、终端连接、进阶功能这几个方面由浅入深掌握控制台的使用。

![MQTT 云服务器创建](https://static.emqx.net/images/9f01bdf3be20b562b3c7cacb1f661665.png)

同时添加了客户端连接指引页面，引导用户通过 [MQTT 客户端](https://www.emqx.com/zh/mqtt-client-sdk)或者 SDK 来连接到服务。部署连接指引可以让用户更清晰地了解创建部署完成的后续操作，降低用户使用门槛。

![连接到 MQTT 云服务](https://static.emqx.net/images/a8f0cb0ef85620d61010caaf19a4304c.png)


### 帮助文档指引及结构优化

帮助中心上线了全新的引导首页（[https://docs.emqx.cn/cloud/latest/](https://docs.emqx.cn/cloud/latest/)），可以帮助用户更清晰快速了解我们的产品。针对采购、商务、开发人员等不同角色进行了模块聚合，方便用户快速找到自己需要的内容，并根据引导掌握 EMQX Cloud 的所有功能使用操作。

### 更完善的多语言 SDK 接入Demo

我们优化和更新了主流编程语言的 SDK 连接到 MQTT 服务的代码示例以及讲解，其中包括 Java、Python、Go、C、C#、JS（Node.js）这些常用的开发语言，并且包含 React、Vue、Electron 的示例 Demo 帮助全栈开发者快速使用我们的产品。同时还更新了针对于开发版的 ESP8266 和 ESP32 的教程，让嵌入式开发者更快地连接到 MQTT 服务。您可以根据教程引导（[https://docs.emqx.cn/cloud/latest/connect_to_deployments/overview.html](https://docs.emqx.cn/cloud/latest/connect_to_deployments/overview.html)），直接复制相关的代码就可以快速实现连接。

### 欠费停机规则更新

对于国内用户欠费且透支额度使用完的情况，将会先停止部署，两天后再删除部署。这样的规则设置将尽可能避免由于商务上的原因导致未及时续费而引起的数据和配置损失，保障用户的利益。


为了完成「通过世界级开源软件产品服务人类未来产业与社会」的使命，敬请期待一个更优秀的 EMQX。
