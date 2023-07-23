[EMQX](https://www.emqx.com/zh/products/emqx) 为用户提供了一个功能强大的内置管理控制台，即 EMQX Dashboard。通过这个控制台的 Web 界面，用户可以轻松监控和管理 EMQX 集群，并配置各种必要的功能。在最近发布的 EMQX Enterprise 5.1 中，EMQX Dashboard 引入了全新而直观的设计，为用户提供了最友好的 MQTT Broker 管理界面。

EMQX Dashboard 新颖的 UI/UX 设计带来了视觉效果和内容布局的提升，让用户能够方便地查看关键数据和指标。它还提供了许多内置功能，例如对连接、订阅和发布进行高级认证和权限管理。另外，它还能通过数据桥接和规则引擎，实现数据的无缝集成和转换。

## 优化菜单栏：轻松精准地操作 EMQX

重构后的菜单根据不同的角色和职责将任务进行了分类，以确保工作流程的清晰性和专注度。

<div style="text-align:center;">
  <div style="display:inline-block;"><img src="https://assets.emqx.com/images/b0df2eb462165fc57b21ef700fc300c5.gif"></div>
  <div style="display:inline-block;"><img src="https://assets.emqx.com/images/6fc8d90a3a350db5f4fcbf774584a120.gif"></div>
</div>

<center>EMQX 4.4 的导航菜单 / EMQX 5.1 的导航菜单</center>

<br>

新的菜单结构包含以下几个部分：

1. 监控：为日常运维人员提供集群性能的概览和各种细分视图，包括客户端、订阅、保留消息和延迟发布等。它还提供了告警集成和监控功能。
2. 访问控制：专注于 MQTT 访问安全管理，让管理员能够管理和审核 MQTT 客户端的认证和授权。它还支持客户端黑名单管理。
3. 集成：通过引入可视化的 Flows 页面，简化数据集成。用户可以方便地查看每个主题的数据处理规则和与第三方数据系统的集成情况。该部分还包括规则引擎和数据桥接管理。
4. 管理：将之前分散的配置选项整合在一起，按主题类别进行归类。配置界面采用横向布局，提供了更宽敞的配置视图。
5. 诊断：提供了多种自我诊断功能，帮助用户排查和解决错误和问题。
6. 系统：允许添加或删除 EMQX Dashboard 用户账户，以及能够生成 API 密钥（用于认证和脚本调用 HTTP API）。

## 通过简化和分类的设置来优化您的 MQTT 体验

重新设计的配置界面对众多配置选项进行了归纳和分类，提升了易用性。此外，垂直布局也被改为了水平布局，为配置设置提供了更充足的空间。

![MQTT Settings](https://assets.emqx.com/images/236962a1a0e822dd494ae6d02f7d83f9.gif)

<center>MQTT 设置</center>

## 增强的监控集群概览：信息更丰富，可用性更高

通过增强的监控集群概览，用户可以获得全方位和详细的集群视图。这些改进提供了更丰富的信息和更好的可用性，使监控和分析集群性能变得更加轻松。借助我们强化的监控功能，您可以随时了解集群的状态，做出明智的决策，提升集群的效率。

- 活动连接指示器：能够区分在线和离线连接，是对原有总连接数指标的补充。

  ![Live connections indicator in cluster overview](https://assets.emqx.com/images/562b8d0f7b00cee1dc3ab325c3a6433f.png)

  <center>集群概览中的活动连接指示器</center>

- 节点拓扑：自从 EMQX 5.0 版本引入 Mria 集群架构以来，EMQX 支持多达 23 个节点，并且能够处理多达 [1 亿个并发 MQTT 连接](https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0)。为了更好地展示节点之间的关系，节点信息面板经过重新设计，新增了节点拓扑视图。这个视图使用不同的颜色表示节点的状态，例如在线或异常。

  ![image.png](https://assets.emqx.com/images/f1158ebc6657be23f823553801d94237.png)

<center>EMQX 节点信息面板</center>

## 可视化的双向数据集成

EMQX 利用其规则引擎和数据桥接功能，赋予企业用户强大的数据集成能力。

EMQX Enterprise 5.1 引入了一个易用的 Flows 页面，为用户提供了直观的可视化界面。通过该界面，您可以方便地查看每个主题的数据处理规则以及与第三方系统的集成情况。实时掌握数据流的每一个环节，简化开发和配置过程。

> 要了解更多信息，请关注我们即将推出的博客系列：“使用 EMQX Data Integration 双向集成 MQTT Broker/Kafka/Pulsar”。

![数据集成的 Flow 视图](https://assets.emqx.com/images/6eb9d437eb81a4363fff410e80b7ad1c.png)

<center>数据集成的 Flow 视图</center>

## 通过帮助台轻松掌握 EMQX

我们提供了一个全新的侧边栏，方便用户快速访问用户手册、核心概念、重要功能的使用指南和常见问题解答。此外，您还可以通过侧边栏浏览 EMQX 社区论坛和博客，以获取更多产品信息并随时反馈您的意见。

![帮助台](https://assets.emqx.com/images/c9fba5e4778c3cfe4212a70d38a9e92c.png)

<center>帮助台</center>

## 结语

EMQX 5.1 的最新版本在 EMQX Dashboard 的用户界面和用户体验方面进行了重大改进，为用户提供了更出色的 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 管理体验。通过重新设计的界面、丰富的功能和无缝的数据集成能力，EMQX 使企业能够充分利用 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 技术的优势，为其物联网应用提供全面支持。欢迎尽情探索全新的 EMQX Dashboard，为您基于 MQTT 的解决方案开启无限的可能性。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
