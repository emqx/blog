**目录**

- [明确您的项目需求](#明确您的项目需求)

- [MQTT Broker 如何工作](#mqtt-broker-如何工作)

- [安全性](#安全性)

- [集群与弹性伸缩](#集群与弹性伸缩)

- [数据集成与规则引擎](#数据集成与规则引擎)

- [性能](#性能)

- [云原生](#云原生)

- [支持扩展开发](#支持扩展开发)

- [成本](#成本)

- [其他需要关注的因素](#其他需要关注的因素)

- [结语](#结语)

  

MQTT Broker 是用于连接物联网设备，完成消息传递的重要组件。MQTT Broker 的选型，是物联网应用构建过程中最为基础也是最为关键的一步。本文将从物联网应用普遍场景和项目需求出发，提供一些通用的选型思路和关注点，帮助读者了解如何选择一款最适合自己的 MQTT Broker。

## 明确您的项目需求

目前市面上可供选择的 MQTT Broker 多达数十种，其中既有支持私有部署的 MQTT Broker，也有提供 MQTT 接入的云服务。

数量繁多的 MQTT Broker 在给您的选择带来更多灵活性的同时，也增加了选择的难度。

我们很难提供一个万能的公式来指导您如何选择 MQTT Broker，但是您可以从自己的项目需求出发，结合以下问题进行考虑：

1. 长远来看希望接入多少客户端？
2. 对基础性能指标的要求？对消息时延与可靠性敏感吗？
3. MQTT Broker 需要部署在哪里，数据最终被如何使用？
4. 用户群/物联网设备的地理分布是什么？
5. 数据特点是什么，消息大小与频率是否是必须考虑的选项？
6. 您的应用程序如何处理物联网数据，比如首选的编程语言、数据存储与分析组件是什么？
7. 所处行业是否有广泛使用的 MQTT Broker？
8. 是否有预算购买付费服务？
9. …

根据以上问题，下文中我们将结合 MQTT Broker 能够提供的特性进行进一步探讨，帮助您更加明确自己所需要的 MQTT Broker 是怎样的。

## MQTT Broker 如何工作

在开始之前我们首先来了解一下 MQTT Broker 是如何工作的。

MQTT Broker 遵循 **发布-订阅** 消息传递模型。在这个模型中，一个客户端（消息发布者）将消息发布到一个主题中，而另一个客户端（消息订阅者）则订阅特定的主题，当发布者发布一条消息时，所有订阅了该主题的订阅者都会收到该消息。

> 查看博客 [MQTT 发布/订阅模式介绍](https://www.emqx.com/zh/blog/mqtt-5-introduction-to-publish-subscribe-model)了解更多。

如下图所示，通过 **发布-订阅** 模型，消息可以在一个或多个订阅者之间派发，订阅者可以是设备，也可以是应用程序。

![MQTT 发布-订阅模型](https://assets.emqx.com/images/b9575ac3d6916dc629c12aa2de5ce5c3.png)

进行消息传递时客户端和 MQTT Broker 遵循以下步骤：

1. 建立连接：发布者与订阅者客户端发起连接请求与 MQTT Broker 建立连接；
2. 订阅主题：订阅者客户端订阅一个或多个主题；
3. 消息发布：发布者客户端指定主题和 Payload 发布消息；
4. 消息路由：当 Broker 收到消息时，它将检查订阅者列表，并向所有订阅了该主题的客户端路由发送消息；
5. 断开连接：客户端主动发送请求断开连接，MQTT Broker 也可以在网络异常或心跳超期后断开与客户端的连接。

在基础消息传递功能上，大多数 MQTT Broker 都实现了 MQTT 协议所定义的基本功能，如 QoS 级别控制、客户端身份认证、保留消息、共享订阅等，这些功能能够帮助您快速实现特定场景下的需求。

但这不是全部。如果将 MQTT Broker 看作一个港口，消息传递则仅仅是实现了货物的运转。实际上，为了保证货物的运转，需要一个完善的物流系统和仓储设施来提供基础保障；为了将来自各地的货物发往不同的目的地，需要对货物进行拆箱装箱并使用不同的物流方式发送；在物流的淡季与旺季，需要对港口设施与人员规模进行动态灵活调整以满足需求的同时实现效益最大化。

以上要求对应到 MQTT Broker 分别是基础运行时的安全防护、故障处理、指标监控，MQTT 消息传递时的数据处理与数据集成，以及整个服务的弹性伸缩能力，这些特性是构建一个企业级、满足不同需求物联网应用的必备条件。

## 安全性

安全性是所有物联网应用需要首要关注的问题，在选择 MQTT Broker 时您应该考虑以下几个方面。

### 客户端身份认证

![MQTT 客户端身份认证](https://assets.emqx.com/images/5401567bf5cb065fe376afee0b2b4f5c.png) 

MQTT 客户端身份认证是指客户端连接 MQTT Broker 时，需要提供特定的凭证用以证明客户端的身份。常见的身份认证手段和其对 MQTT Broker 的要求如下：

| **认证方式**    | **描述**                                                     | **功能要求**                                                 |
| :-------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 用户名/密码认证 | 客户端连接时，提供特定的用户名和密码，服务器收到后，会校验后决定是否允许连接。 | 支持与多种数据库集成使用<br>兼容现有数据库数据<br>支持自定义认证并与企业现有认证服务结合使用 |
| JWT 认证        | 不需要服务器来保留客户端的认证或会话信息，客户端携带签发的 Token 实现认证。 | 支持 JWKs支持完整的加密算法                                  |
| X.509 证书认证  | 客户端与服务器之间采用 TLS/SSL 协议进行加密通信，防止窃听和数据丢失，同时使用 X.509 客户端证书进行身份认证。 | SSL/TLS 低性能开销<br>支持 OCSP Stapling/CRL                     |

### 发布订阅授权

![MQTT 发布订阅授权](https://assets.emqx.com/images/54531dbe656b0d85d4657db65f3ab665.png)

授权是指对在客户端发布和订阅前，检查是否具有对应主题的操作权限。权限列表通常存储在内部或外部数据库中，随着业务变化需要在运行时动态更新。

授权功能常见的要求如下：

| **功能要求**             | **说明**                                             |
| :----------------------- | :--------------------------------------------------- |
| 细粒度的权限控制         | 能够满足各个级别的权限控制需求                       |
| 支持缓存                 | 发布订阅是高频操作，缓存机制能够有效缓解高峰时的压力 |
| 支持与多种数据库集成使用 | 用户可以灵活选择自己熟悉的技术栈                     |
| 兼容现有数据库数据       | 从旧系统迁移时需要考虑此项                           |

### 软件漏洞与企业 IT 安全

根据软件行业过往的历史教训，软件的安全漏洞将会为企业业务带来巨大影响。

如果您打算将某个 MQTT Broker 用于生产，请务必严格评估它是否经过了安全验证，常用的安全验证途径有：

- 开源验证：Broker 的代码是否开源，是否经过了开源社区充分验证；
- 安全集成：是否具备充分的应用安全测试与安全防护，是否采用专业的安全解决方案。

企业 IT 安全的意义在于保护企业的数据安全，防止数据泄露，避免数据被破坏、窃取、滥用等，为此需要 MQTT Broker 提供包括密码策略、安全审计、数据加密等功能。

## 集群与弹性伸缩

MQTT Broker 集群是指将多个单独的 MQTT Broker（可以称其为节点）连接在一起，共同处理连接和消息的分布式的系统。

集群对于客户端来说是一个整体，其内部机制、节点数量的变化对客户端是无感的，所有的连接、消息发布订阅跟在单节点上没有任何区别。

![MQTT 负载均衡](https://assets.emqx.com/images/adde22edec17a94cc8f8ec96d82e79d0.png)

### 为什么需要 MQTT Broker 集群

#### 提供更大的接入规模并保持可扩展性

试想您将一款汽车接入到了物联网中，当它以每月数千到数万台的销量涌向市场时，未来几年内您的 MQTT Broker 需要面对数万到数百万连接的增长；而随着车载系统 OTA 升级，越来越多的数据需要传递到云端，MQTT Broker 的消息吞吐也水涨船高。

在支持集群的 MQTT Broker 中，您可以在运行时向集群添加更多节点轻松地进行水平扩展，使其能够处理越来越多的 MQTT 消息和客户端连接。

#### **确保服务高可用**

并非所有应用都需要应对业务增长压力，当您的业务仅限于某个学校或制造工厂的环境监测时，未来数年内客户端与消息数量是可以预计的，甚至它不会发生任何变化。

您可能已经意识到了：单台 MQTT Broker 可以承载数万个客户端，这足以满足大多数物联网应用需求，集群是否是必要的？

答案是肯定的，在一个 MQTT Broker 集群中，即使某些节点发生故障集群也可以继续运行，从而确保应用无单点故障、服务始终可用。

因此，当您对应用的可靠性有要求时，请务必选择支持集群的 MQTT Broker。

### 只有少部分 MQTT Broker 支持集群

MQTT Broker 集群最重要的工作是确保集群节点能够高效可靠地同步和复制 MQTT 会话状态信息，包括订阅的消息和未完成的消息传输，并实现连接的负载均衡、设备的集中管理，同时确保整个集群具备可扩展性和高可用性。

要全部实现这些特性并不容易，因此绝大部分 MQTT Broker 只能以单节点的形式部署，考虑到扩容能力与高可用特性的重要性，其中一些 Broker 提供了特别的实现方案：

**通过 MQTT 桥接功能连接多个 Broker**

以 MQTT 消息发布订阅的方式在多个 Broker 之间传递消息，这种方式一定程度上可以实现接入能力扩展，让更多的客户端连接到一起通信，但其通信非常低效，且无法保证高可用性。

**在多个节点之间全量的同步会话状态**

同时启动多个 MQTT Broker，在节点之间全量的同步会话状态，借助负载均衡，在单节点故障时立即切换到另一个可用节点。这种方式以单机热备份的方式实现了高可用性，但对于扩展性没有帮助，且增加了使用成本。

以上方案确实有效，但无法同时兼顾扩容能力与高可用性，并为部署引入了额外的复杂操作。因此如果您想更加轻松地构建可按需扩展的可靠物联网业务，最理想的选择是那些支持集群的 MQTT Broker。

<section class="promotion">
    <div>
        EMQX 是如何支持单集群亿级 MQTT 并发连接的？
    </div>
    <a href="https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0" class="button is-gradient px-5">点击查看详细测试过程 →</a>
</section>

## 数据集成与规则引擎

在构建物联网应用时，除了设备与设备的通信，通常需要在多个系统之间进行数据交换。

例如，您可以通过 MQTT Broker 采集工厂产线传感器的数据，并发送到与之配套的 MES、ERP 系统当中，数据库或事件驱动的消息队列如 Apache Kafka 就是两个系统之间最好的桥梁；

您也可以将遍布某个城市的所有气象传感器数据存储到时序数据库 InfluxDB 中，以便进一步的处理和分析，充分挖掘数据价值。

实现这一目的最简单的方法是编写一个应用程序：从 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)订阅消息，写入到对应的的数据集成当中。由于这类需求普遍存在，一些 MQTT Broker 会以插件或扩展的方式直接提供类似的功能。

在最终写入数据之前，您可能还需要将数据进行过滤、编解码转换等处理，以满足实际的业务需求。

一些 MQTT Broker 提供了用于数据处理的规则引擎，允许在 Broker 上创建数据驱动型的规则并将处理结果写入到数据集成当中。此功能通常以低代码的方式如 SQL、表单编辑等方式进行配置。

整个流程如下图所示：

![规则引擎流程图](https://assets.emqx.com/images/b8b1b2be373f56476be6e1269bb76d47.png)

在需要与外部数据系统集成的物联网应用中，内置数据集成和规则引擎是 MQTT Broker 一个重要的加分项，它不需要额外的开发工作，能够加快业务的交付，同时它还可以随集群伸缩扩容，实现最终的高可用性。

## 性能

MQTT Broker 用于连接大量客户端，并实现海量的消息传递，在此过程中需要考虑以下性能指标：

1. 最大连接数：MQTT Broker 支持的最大客户端连接数的上限；
2. 消息传输延迟：消息从发送端到接收端的时间消耗，在网络环境相同的情况下，主要取决于 MQTT Broker 性能；
3. 消息发送/接收速率：每秒钟 MQTT Broker 能够处理的消息发送/接收的数量；
4. 消息存储性能：有些 MQTT Broker 支持消息的持久化与外部数据集成，这就需要考虑消息的存储性能。

性能指标看起来很好衡量，数据大小决定一切，通常具有较高性能 MQTT Broker 在其他方面也不会太差，但性能指标不应该是评判 MQTT Broker 好坏的唯一标准，除非它真的非常差劲。

但要注意的是 MQTT Broker 宣称的性能指标都是在特定的场景下测试的，消息速率、主题层级、消息 QoS、消息 Payload 大小以及是否启用规则引擎等任意条件都会对其结果造成影响。

另外，任何 Broker 都可以对外提供一个难以复现并且用户永远用不到的指标，如果您真的对性能有很高要求，请谨慎思考它的技术是否真的能带来这个结果，它的测试结果是否能够复现。实践出真知，最好结合自己的应用场景实际做一下压力测试。

## 云原生

云原生是一种软件架构和交付方式，旨在支持在云端高效、可靠地构建和运行应用程序。

借助云原生技术，您可以将 MQTT Broker 与基础设施视为一个整体，借助容器、微服务和自动化运维等技术实现 MQTT Broker 的高效、灵活、可靠部署。

同时，云原生技术还能够提供配置管理、集群扩容、无缝升级、故障处理和统一监控等管理操作，更好地支持大规模物联网应用的开发和运营。

要实现以上目标，需要要求 MQTT Broker 的伸缩能力以及管理功能与云底层能力深度适配，而事实上每个 Broker 对云原生的应用程度有所不同。

> 使用 [EMQX Kubernetes Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 在 Kubernetes 上自动化部署、配置、管理 EMQX 集群。

## 支持扩展开发

单一的软件无法满足所有用户需求，在一些应用中，您需要扩展开发 MQTT Broker 以添加不同的功能，例如支持更多消息传输协议、实现特有的认证授权流程、支持特殊的数据加密方式、监控告警功能等。

这需要 MQTT Broker 提供对应的扩展机制如插件机制，以方便必要时进行二次开发，除此之外还需要支持使用您熟悉的语言来进行扩展。

> 查看 EMQ 提供的 [MQTT 编程](https://www.emqx.com/zh/blog/category/mqtt-client)系列博客，学习 MQTT 协议在各类客户端中的应用实践。

## 成本

成本是一个综合的概念，需要结合您的预算进行考虑。

您可以根据情况购买企业服务或使用开源 MQTT Broker，目前可供选择的开源 MQTT Broker 很多，在开源协议允许的情况下，通常不需要任何购买费用即可部署。但安装、维护与扩展开发需要消耗更多的资源。

如果您的应用规模很大，您需要考虑 MQTT Broker 性能差异带来的成本差异，更好的性能指标意味着更少的硬件、网络和维护开销，这能够降低总体成本。

如果您选择的是托管 [MQTT 云服务](https://www.emqx.com/zh/cloud)，其计费模式通常与连接数和流量成正比，请务必阅读每个计费方案的细则，选择您的使用场景下成本最优的方案。

## 其他需要关注的因素

除了 MQTT Broker 本身外，您还可以从以下方面考虑：

- **更快、更本地化的商业服务**

  优先选择那些可以提供本地化或全球化的服务 MQTT Broker 提供商，这能够让企业更快地获取技术支持，可以加快交付并节省大量成本。 

- **避免从头开始构建系统的风险和成本**

  尽量选择那些经过验证的 MQTT Broker 或技术，选择行业验证过的解决方案，避免从头开始构建系统，从而降低投资风险和成本。 

- **支持边缘和云的无缝集成**

  如果您需要在边缘部署，请选择资源占用更低、具有边缘优化、或者有成熟云端-边缘解决方案的 MQTT Broker。

## 结语

本文列举了在进行 MQTT Broker 选型时开发者需要考虑的主要因素。读者可以根据自身项目的实际情况，逐一排查并综合考量，选择最适合自己的 MQTT Broker。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>