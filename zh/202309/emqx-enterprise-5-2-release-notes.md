[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 5.2.0 版本现已正式发布！

新版本带来了一系列重磅更新，最令人瞩目的是可拖拽的可视化 Flow 设计器，它可以帮助企业快速创建、测试和部署数据集成。同时，我们新增了对 Amazon Kinesis 和 Azure Event Hubs 的支持，实现了海量物联网设备数据与云服务的无缝连接。此外，新版本还进行了多项改进以及 BUG 修复，进一步提升了整体性能和稳定性。

## Flow 设计器 —— 拖拽和可视化数据集成

Flow 设计器是一个可视化界面，它在早些发布的数据集成可视化查看工具 Flows 基础上，增加了创建和编辑的能力。

它允许用户使用更简单的方式，通过拖拽的方式自由编排规则和数据桥接，在几分钟内即可实现消息与事件的实时处理，并与外部 40 余种数据系统的集成。创建完成后，用户可以通过统一的视图清晰地管理数据集成流程，并监控每个处理节点的状态。

Flow 设计器底层仍使用规则 SQL 与数据桥接，继承了 EMQX 强大的数据处理能力和优异性能。同时，它还允许用户在 UI 和 SQL 编辑器之间自由切换，既保留了习惯的 SQL 编辑方式，也提供了更简单快速的上手能力。相比之前的版本，现在用户无需熟悉 EMQX 规则 SQL 语法，就可以通过简单的 UI 进行业务开发，这有助于用户更轻松地应用 EMQX 的数据处理能力实现业务创新。

![EMQX MQTT Flow](https://assets.emqx.com/images/a5e5ee9c9ba1d9b586fbaf6686285ec5.png)

## 独立的 Webhook 页面，简化配置流程

Webhook 是 EMQX 最常用的数据集成方式之一。为进一步降低使用门槛，EMQX 最新版本新增了独立的 Webhook 配置页面，可大幅简化将数据发送到外部 HTTP 服务器的配置流程。

过去，实现这一功能需要编写规则 SQL 并配置数据桥接，这要求用户对 SQL 语法比较熟悉，特别是在处理客户端事件时，需要了解事件在 SQL 语句中的映射关系（如下列 SQL 所示），增加了学习难度。

```
SELECT 
  *
FROM
  "$events/client_connected"
```

全新的 Webhook 配置页支持纯表单操作，用户可通过简单的点选方式选择需要发送的消息或事件。这样极大地降低了使用门槛，用户无需理解 EMQX 的内部规则语言就可以快速建立事件或消息到外部 Web 服务的连接。

![EMQX MQTT Webhook](https://assets.emqx.com/images/5346f10083e440e6cb1acf96e2f25ffc.png)

## 简化数据桥接配置参数，专注业务流程

EMQX 的数据桥接提供了丰富和全面的参数配置，以便满足企业级消息消息中间件对性能、稳定性以及不同业务场景下灵活配置的需求。通过调整对应功能的参数，可以实现时延与写入速度之间的平衡，或者增加更多的连接实现更高吞吐（相应的对外部数据服务的压力会更大）。

但是我们也注意到，对于大多数场景来说，一些参数并不需要进行调整，使用 EMQX 提供的默认值即可。因此在此次版本中，我们将高级设置的方式折叠了这些参数配置。用户只需专注在业务流程和逻辑设置上，当遇到特定的性能瓶颈或场景需求时，可以打开高级设置进行参数微调。

下图是简化后的 Timescale 数据桥接创建页面，用户仅需关注连接与数据写入流程配置：

![EMQX Timescale 数据桥接](https://assets.emqx.com/images/5ad670a3da4fa19a13ee91a1bd94bb2f.png)

此举在降低学习曲线的同时，仍然保留了 EMQX 对复杂场景的适应能力，让 EMQX 的数据桥接功能对用户更加友好。

## Amazon Kinesis 集成

[Kinesis](https://aws.amazon.com/cn/kinesis/) 是 AWS 上完全托管的实时流数据处理服务，可以轻松地进行流数据的收集、处理和分析。它可以经济高效地处理任意规模的实时流数据，并具有高度的灵活性，能够低时延的处理来自数十万个来源的任意数量的流数据。

EMQX 与 Amazon Kinesis 结合使用，能够实现海量 IoT 设备连接，进行实时消息进行采集、传输，并通过 EMQX 数据集成连接到 Amazon Kinesis Data Streams，进行实时分析与复杂的流处理。

利用 Kinesis 构建的流数据管道，可以大幅降低 EMQX 与 AWS 平台之间的接入难度，为用户提供更丰富、灵活的数据处理方案。够助力 EMQX 用户在 AWS 上构建功能完备、性能卓越的数据驱动型应用。

![EMQX Amazon Kinesis 集成](https://assets.emqx.com/images/183950805b3b5b875b099f3cb6092c04.png)

## Azure Event Hubs 集成

[Event Hubs](https://azure.microsoft.com/zh-cn/products/event-hubs) 是由 Azure 提供的是一种简单、可信且可扩缩的完全托管型实时数据引入服务。每秒能够处理数百万个流式事件，从而构建动态数据管道并迅速应对业务挑战。Event Hubs 支持根据使用需求动态调整吞吐量按需付费，并提供了强大的安全和隐私保护。

Event Hubs 可作为 EMQX 与 Azure 丰富的云服务应用之间的数据通道，将物联网数据集成到 Azure Blob Storage、Azure Stream Analytics 以及部署在 Azure 虚拟机上的各类应用和服务当中。

借助 Event Hubs 构建的低延迟传输通道，可以简化 EMQX 与 Azure 平台之间的接入，帮助用户快速实现海量物联网设备数据与 Azure 的连接。让用户更便捷的获得云计算带来的数据分析和智能化能力，构建功能强大的数据驱动型应用。

![EMQX Azure Event Hubs 集成](https://assets.emqx.com/images/fd9ef9911155ae39c1af91c9abcd4ef3.png)

## HStream 集成

[HStream](https://hstream.io/) 是 EMQ 专为物联网数据存储和实时处理而推出的开源、云原生分布式流数据平台。

它通过专门设计的分布式容错日志存储集群，能够可靠地存储数百万个设备数据流，并提供一级订阅支持，可以实时推送最新数据流到您的应用。并在需要时随时回放和消费数据流。

HStream 独特的融合架构设计，结合 EMQX 海量设备和多协议接入能力，允许用户能够在一个平台上高效完成对所有实时消息、事件以及其他数据流的摄取、存储、处理和分发，为物联网数据流的运维管理和实时应用开发提供了便捷性。

## GreptimeDB 集成

[GreptimeDB](https://greptime.com/) 是一个开源、分布式、云原生时序数据库，融合时序数据处理和分析能力。GreptimeDB 专为云而生，充分利用云的优势，如弹性、可扩展性和高可用性。

GreptimeDB 与 EMQX 集成使用，能够实现海量物联网数据的长期存储与实现查询，以及随业务发展的灵活扩展。无限的历史数据存储，针对时序数据优化的 SQL，两者能够满足对长时间范围内海量数据集的探索与挖掘。用户可以随时查询任意时间段的历史数据，并通过 SQL 即时洞察时序趋势，从繁杂数据中提取核心业务价值，并实现数据驱动的智能决策。

## 规则引擎支持 Sparkplug B 消息编解码

[Sparkplug](https://www.eclipse.org/tahu/spec/sparkplug_spec.pdf) 是工业物联网领域热门的一个开源规范，它基于 MQTT 提供的一套明确定义的 Payload 和状态管理体系，实现了互操作性和一致性。

Sparkplug B 简化了 MQTT 命名空间，用于监控、控制、和数据采集系统（SCADA）、实时控制系统以及设备。它采用 Protobuf 编码数据，以实现轻便、高效和灵活的数据交换。 EMQX 的最新版本在规则引擎 SQL 中添加了 Sparkplug B 消息编解码函数，使得在 EMQX 中，用户可以直接使用 `sparkplug_encode` 和 `sparkplug_decode` 函数，从而更加便捷地进行 Sparkplug B 消息到 JSON 格式的编码和解码。

解码后的 JSON 数据可以通过规则引擎其他函数进行复杂处理，并集成到外部数据桥接中，以实现丰富的业务集成。这有助于简化工业物联网中不同设备的互操作性，提高开发效率，构建灵活可扩展的物联网应用。

## OpenTelemetry 指标集成

[OpenTelemetry](https://opentelemetry.io/) 是 CNCF 下的一个开源可观测性框架，旨在于使用标准化的数据格式，将程序中的 [traces](https://opentelemetry-io.translate.goog/docs/concepts/observability-primer/?_x_tr_sl=en&_x_tr_tl=zh-CN&_x_tr_hl=zh-CN&_x_tr_pto=wapp#distributed-traces)、[metrics](https://opentelemetry-io.translate.goog/docs/concepts/observability-primer/?_x_tr_sl=en&_x_tr_tl=zh-CN&_x_tr_hl=zh-CN&_x_tr_pto=wapp#reliability--metrics) 和 [logs](https://opentelemetry-io.translate.goog/docs/concepts/observability-primer/?_x_tr_sl=en&_x_tr_tl=zh-CN&_x_tr_hl=zh-CN&_x_tr_pto=wapp#logs) 等可观察性数据发送到后端组件。

本次发布中 EMQX 添加了对 metrics 集成的支持，为 EMQX 提供开箱即用的监控能力。有助于更好地观察、分析和诊断 EMQX 集群运行状况。

未来版本中，EMQX 计划进一步支持 OpenTelemetry 的 traces 与 logs 集成，通过分布式链路追踪与日志关联，直观分析请求在 EMQX 中的处理情况，实现端到端的分布式诊断能力。这将进一步丰富 EMQX 的监控数据，帮助用户更全面和细致地监测系统运行状态，快速定位并解决异常。

## 性能提升

性能始终是 EMQX 关注的一部分，本次发布中我们进行了以下提升：

- 更新 Mria 版本，通过合并索引更新提升了保留消息发布速度。
- 规则引擎使用主题索引加速规则匹配，大幅提升了 EMQX 处理大量规则的性能。
- 新增节点池和通道池配置，调优这些配置在高延迟的集群互联网路可显著提升 EMQX 性能。

## 更多新功能

除了前面介绍的主要功能外，各组件均有针对性功能升级，满足用户日常运维和使用需求：

- 认证、授权以及数据桥接中的 Redis 连接支持设置用户名，以便连接到如 AWS MemoryDB 等需要用户名的 Redis 服务中。
- Kafka 数据桥接新增消费者模式动态设置MQTT主题功能，可以实现更灵活的 Kafka-MQTT 主题映射，动态控制数据下发的 MQTT 目标主题。
- GCP PubSub 数据桥接现在支持设置 PubSub 消息的属性和排序键，可以利用这些特征实现更丰富的消息路由和有序传输。
- 为 RabbitMQ 数据桥接添加 TLS 连接支持。
- 更新了 `jq` 依赖版本，修复了一些小的安全问题。
- 客户端认证与授权支持使用 LDAP 作为数据源。
- 发布了适用于 Amazon Linux 2023 与 Debian 12 的安装包。
- 优化了 Prometheus 指标集成时消息、过载保护、授权、认证等功能的指标，使其更加清晰丰富。

## BUG 修复

以下是主要 BUG 修复列表：

- 修复了 EMQX 关闭过程中记录无关错误日志的问题。[#11065](https://github.com/emqx/emqx/pull/11065)
- 修复了启用 debug/trace 时客户端无法发送包含大尺寸 payload 消息的问题。 [#11279](https://github.com/emqx/emqx/pull/11279)
- 修复了在发送带有非零 `ack_flag` 的 CONNACK 数据包时 `packets_connack_sent` 指标未增加的问题。[#11520](https://github.com/emqx/emqx/pull/11520)
- 添加了对 API 中时间戳的最大值的检查，以确保它是有效的 Unix 时间戳。[#11424](https://github.com/emqx/emqx/pull/11424) 

更多功能变更和 BUG 修复请查看 [EMQX Enterprise 5.2.0 更新日志](https://www.emqx.com/zh/changelogs/enterprise/5.2.0)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
