我们很高兴地向大家宣布：EMQX v5.0.0-rc.2 现已发布，距离全新的 EMQX v5.0 更近一步！

目前，EMQX v5.0 正式版的主要功能已经成型，发布在即。本文将通过 EMQX v5.0.0-rc.2 带大家从全新 Dashboard 的视角快速预览 v5.0 的新增功能设计变动，也欢迎大家下载试用，抢先体验 v5.0。

GitHub 下载：[https://github.com/emqx/emqx/releases/tag/v5.0.0-rc.2](https://github.com/emqx/emqx/releases/tag/v5.0.0-rc.2)

EMQX 官网下载：[https://www.emqx.com/zh/downloads/broker/v5.0.0-rc.2](https://www.emqx.com/zh/downloads/broker/v5.0.0-rc.2)

## 指标与状态一目了然

通过准确的监控指标与告警机制，能够尽早发现 EMQX 集群中的问题，并做出响应解决问题，进而保证产品的稳定性，提升用户体验。

### 洞察实时状态

在 5.0 版本中我们提供了更多的监控数据并将其可视化展现到 Dashboard 上，您可以在显眼的位置看到客户端实时连接情况以及消息流入流出速度，通过节点拓扑一目了然洞察集群中所有节点状态。

![EMQX 5.0 Dashboard](https://assets.emqx.com/images/f06fe7d927ebd765989b277cd7f268fe.png)

### 回溯历史指标

提供至多 7 天的多个纬度历史数据并通过在线图标展示，您可以从中直观地回溯业务增长趋势，避免错过任何数据波动。

如果您想使用自己熟悉的指标监控与告警技术栈，轻点鼠标即可在界面上集成 Prometheus 和 StatsD 系统。

![EMQX 5.0 仪表盘](https://assets.emqx.com/images/a77e433870b91146623b82c7f9ee60e7.png)

![EMQX 集成 Prometheus 和 StatsD](https://assets.emqx.com/images/79d870627770a341aa73921b36d4cfad.png)

 
## 在 Web 上配置认证与授权

认证与授权是最核心的安全功能之一，5.0 版本中我们针对易用性和使用流程进行了重点改造。

### 舍弃枯燥的认证插件

将功能的配置从插件迁移到 Web 页面，在页面上选择您需要的认证方式，选择您擅长的数据源，填入参数即可为所有节点启用连接认证和权限控制功能，为客户端提供最重要的安全防护。如果需要在集群启动前完成配置，您仍然可以使用配置文件的方式进行设置。

如果您选择使用内置数据库，您可以在 Web 页面上完成认证数据的添加与管理，不需要阅读文档，不需要再开发新的代码，一切操作随心应手。

![EMQX 5.0 创建认证](https://assets.emqx.com/images/5b88f954971be6c1199c6114f61154e6.png)

![EMQX 5.0 创建认证 2](https://assets.emqx.com/images/84045601237c7f556fc30871058c0741.png)


### 查看运行统计

我们针对每个认证和权限控制提供了运行统计，确保您不错过任何一次失败请求；通过当前速度指标，您可以检测认证服务的负载情况。

![EMQX 查看运行统计](https://assets.emqx.com/images/90e8ee89ea64206d3569e1975b1f0119.png)

### 调整配置应用顺序

当您启用多个认证配置时（尽管我们不推荐这么做，但某些场景下确实很需要这个特性），EMQX 将按照配置顺序从上到下依次执行验证操作。您可以通过拖拽、上下移动的方式调整配置之间的执行顺序，确保符合业务需求。

![EMQX 调整配置应用顺序](https://assets.emqx.com/images/40921cfe0f6077137741bec0cc16215f.png)

## 规则引擎与数据桥接

我们将之前分散在各处的 Webhook、桥接插件、MQTT 消费组整合到一起，使用统一的操作流程进行配置使用。

### 可视化规则配置

在创建时，我们提供 SQL 输入与 Web 配置的模式，即使您不了解规则 SQL 也能完成规则配置；对于复杂数据，您可以一键代入 SQL 模板，快速探索数据处理方式。

![EMQX 可视化规则配置](https://assets.emqx.com/images/64d5f8144073cc3b41a3ea9b8826ea83.png)

![EMQX 可视化规则配置 2](https://assets.emqx.com/images/03c8939954841617a1ae4a2fa77e67a5.png)

### 双向数据流

此前的规则引擎中，我们仅支持将消息从 EMQX 发送到外部集成（Sink），如果您想要将消息从外部集成发送到设备（Source）可以使用桥接插件如 MQTT Bridge，但这将无法使用规则引擎的筛选和处理能力。

在 5.0 版本中，我们提供了双向数据流：您可以在远程 MQTT Broker 和 EMQX 之间自由的桥接消息，并使用规则 SQL 实时提取、过滤、丰富和转换数据。

![EMQX 双向数据流](https://assets.emqx.com/images/b04f853471664f18379ee107d872d026.png)

### 可视化的数据流

我们在 Flow Chart 页面提供了一个可视化的面板，您可以查看所有 IoT 规则和 Data Bridge 的数据流关系。「数据从设备进入 MQTT 主题，经过 IoT 规则处理，最后将处理发送到某个 Web 服务或数据库中」这一精心编排的处理过程将被完美的展示到页面上。

后续的版本我们计划继续完善 Flow Chart 面板，届时您可以在面板上使用拖拽、连接的方式自由的编排您的数据集成逻辑。

![EMQX 可视化的数据流](https://assets.emqx.com/images/03b9bce2f7b4a6456d6ed2d00984cf4d.png)
 

## 像 Chrome 一样管理拓展插件

5.0 版本中我们允许通过插件包的的形式编译、分发、安装插件。当您需要扩展功能时，找到您需要的插件， 在 Web 界面完成上传即可进行安装，整个过程甚至不需要重启 EMQX 集群。

同时，一个规范的插件将会随身附带使用说明、插件主页地址等信息，对于普通用户来说，您可以依照说明快速上手使用插件；同时，对于插件开发者来说，您的开发成果也将被更多用户了解。

如果您在 4.x 3.x 等旧版本中使用了其他插件也不必担心，5.0 版本完全兼容之前的插件。

![EMQX 安装插件](https://assets.emqx.com/images/65ea54ae2bde9ecd9ee0f77bca2d100c.png)

![EMQX 插件管理](https://assets.emqx.com/images/d087f1e205a16a6e2dd4ca81fa2a345c.png)

## 在页面上配置所有参数

5.0 版本中我们更换了配置文件格式并优化了配置项，以为您提供更好的配置：包括更容易理解的配置项名称、更合理的配置结构、统一的配置规范。

我们提供了热配置能力，无论是在 Web 页面还是文件进行的配置都可以热更新到集群。

![EMQX 热配置](https://assets.emqx.com/images/83f4c472cfe8ccbf623239afd0d4a10e.png)

## 写在最后

以上是您可以通过 Dashboard 看到的 EMQX v5.0 部分新功能，上述功能在本次发布的 EMQX 5.0.0-rc.2 版本中已经全部可以抢先体验。

除此之外，EMQX v5.0 还增加了 MQTT Over QUIC、Mria 数据库以及基于 RocksDB 的 session 持久化等重要特性，我们将在不久后的正式版中一并向大家介绍。敬请关注。

有关 5.0 版本的功能设计与 BUG 反馈，欢迎大家在公众号后台回复「**5.0**」参与讨论。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
