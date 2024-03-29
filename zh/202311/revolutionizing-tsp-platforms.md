## 摘要

随着整个汽车出行领域智能化和网联化的发展，车机，这一 “人-车-云” 之间交互的窗口，已成为目前汽车智能化、网联化的核心部件，也是用户驾乘体验中的关键场景之一。通过车机和车企网联平台的连接，车企能够实时获取车辆数据和车主使用情况，对车辆和车主进行精细化管理和维护、提供个性化运营关怀，同时联动手机 APP 更能为车主提供寻车定位、个人兴趣点推送等优质的服务应用。因此，各个汽车制造厂商正逐步建立基于数据和服务的车联网 TSP 平台系统，以提供更智能化和人性化的体验。

要构建能够满足如今消费者丰富需求的车联网 TSP 平台，汽车主机厂面临诸多技术挑战，包括可靠的车云连接、有效的数据传输以及灵活的数据处理等。EMQ 为汽车主机厂提供了车云互联基础设施解决方案，以帮助客户应对海量车机、Tbox 与云端 TSP 的连接与上下行数据交互需求，解决海量连接、高数据吞吐、安全认证、复杂网络环境等挑战，从而协助主机厂构建高性能、高可靠、易于维护的车联网TSP平台。

## 基于 EMQX 的高性能、高可用车联网 TSP 数据底座解决方案

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) (Message Queuing Telemetry Transport) 是一种专门针对低带宽、高延迟、不可靠网络等场景而设计的轻量级消息传输协议。其发布/订阅模式、会话保持机制、QoS 消息质量机制使其对比私有 TCP 及 HTTP 协议，在弱网支持、并发能力等方面更适用于车联网场景。在车联网场景中，像 EMQX 这样的 MQTT Broker 就成为了车联网平台架构中接入层核心，因为 Broker 可以解耦平台与海量车机、代理车机与云平台间的连接交互。EMQX 是基于 MQTT 协议的企业级数据接入平台，能连接车辆和云端，提供连接和数据解决方案。它的高性能、高可靠、可伸缩性设计，能够实时移动和处理车联网数据，帮助车企解决上述车联网平台在连接和数据基础设施层面的挑战，开发团队可专注上层应用的开发。

![车联网 TSP 数据底座解决方案](https://assets.emqx.com/images/cf3920d60e1a31edc14205ed10524715.png)

1. 整体架构：分布式、高可用

   由于数据保护的需要，车企的车联网平台多采用私有化部署。EMQX 集群和用户业务系统通常一同部署在 IDC 或公有云环境中。通过负载均衡与 EMQX 分布式集群部署，可以实现百万级别的车机连接和数据吞吐能力，为上层业务应用提供坚实接入基础。

2. 车机连接：高并发、高安全

   车机通过蜂窝网络物理链路、MQTT 协议接入 EMQX，EMQX 分布式高可用架构支持百万级并发连接。连接安全方面，EMQX 支持 TLS 安全协议，车机可以通过单向、双向 TLS 认证接入以及与 PKI/CA 系统对接适配一机一密的认证方案。另外，EMQX 能够提供连接状态实时感知。

3. 数据传输：多保障、高吞吐
   - 依靠 MQTT 及 EMQX 提供的心跳监测、会话保持、QoS 等级等多重保障机制，即使车辆因为网络原因断开连接，相应的消息传递仍能在重连后恢复，实现在复杂的网络环境下实时、安全、可靠的车机消息通信。
   - 基于订阅、发布模式以及 EMQX 海量 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)、百万级 TPS 消息吞吐能力，EMQX 能够支持在每个车机与平台连接内建立多个不同的逻辑隔离的 MQTT 主题，支撑上下行不同业务数据传输。为了实现车辆状态感知监控、在线寻车等业务场景，车机实时上报车辆的位置、续航状态等信息；为了实现用户兴趣点下发、关怀消息下发、运营消息下发等场景，云端车联网平台向车机推送相应的指令或业务消息。
   - 针对像用户兴趣点推送、养护关怀消息、运营消息等从云端下发到车机端的场景，平台往往是针对车型等批量下发。但是下发时部分车辆可能处于掉线或熄火离线状态，EMQX 的离线下发功能可以结合数据库落盘缓存数据，在基础接入层确保车机上线后能够及时获取到云端下发的消息。

4. 消息及事件的处理与集成：

   通过内置的规则引擎，可以将车机上报数据消息以及车机连接或断连、消息送达确认等事件，进行预处理后桥接集成到相应的数据系统。例如将海量车机上行数据，经过编解码等预处理后，桥接到 Kafka 等消息队列缓冲，后台应用服务从容获取数据进行业务分析应用；将车机连接、断开连接等事件信息存储到数据库中，用于后续车辆上下线情况分析等。灵活的数据预处理及集成能力，可以让上层业务应用更专注于应用的开发。

5. 高效的监控运维：

   EMQX 提供了直观的可视化监控和管理界面，用户可以实时监控车机连接状态和消息流量指标，并通过接口将监控数据推送到客户三方监控系统。热配置修改、热升级的机制，让客户在做一些配置调整的时候，不需要停止服务，最大程度的保证了车机连接及数据传输的持续性。而慢订阅、日志追踪等功能，则很好地帮助客户在出现连接异常、消息接收时延过大等问题时能够快速排查锁定原因。

## 构建车联网 TSP 平台面临的挑战

- 汽车保有量不断增长，如何支持海量车机并发连接

  随着汽车销售量的不断增加，平台接入车机规模不断扩大，大型车企汽车保有量超过百万，在节假日等高峰期间，平台需要能够维持接入几十万量级的并发连接。

- 上下行多种业务数据，如何支持高并发消息吞吐

  为了实现丰富的业务场景，每个连接到云端的车机都会同时有多种上行及下行数据传输。所以当车辆数量达到几十万量级时，平台就需要支持百万级的消息吞吐。

- 如何确保安全连接保障数据安全

  随着车辆互联度的增加，车辆也越来越容易受到网络威胁。车机通常会基于公网连接，为了保护用户的隐私并维护整个系统的安全性，保证车机与云端通信链路和数据的安全是一个关键的挑战。另外，不同车型可能采用的不同认证方案，需要实现统一的认证接入。

- 车辆所处网络环境复杂，如何保证消息实时性与可靠性

  车辆在行驶过程中经常会遇到遮蔽、隧道、基站切换等复杂网络环境，造成车机与云端的链接断开，如何在复杂的网络环境下保证重要消息能够可靠到，避免因为连接重连和中断造成的数据丢失成为挑战。另外，车辆停车后车机将处于较长时间断电离线状态时，如何保证云端下发消息能够触达也是运营关怀等下行业务需要解决的问题。

- 业务侧对数据需求不同，如何实现灵活数据分流、存储

  在车机上报数据被采集后，根据数据内容及需要，往往需要被不同的后台应用服务获取。对于多个应用服务需要实时获取的数据，往往需要存入消息队列。对于需要进行历史分析的数据，往往需要存入数据库中。如何将接入的在海量车端数据去实现灵活的预处理、分流、数据桥接集成，对于平台基础层设计也是一个挑战。

## 相关产品

### EMQX Enterprise

[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) (以下简称 EMQX) 是一个强大的企业级物联网消息平台，专为大规模部署和物联网应用中的高可靠性而设计。在车联网车云互联场景中，EMQX 通过以下能力为用户带来收益：

- 高可靠性和可扩展性：EMQX 采用分布式架构，具有高可用性和可扩展性，可以处理大规模并发消息传输。它支持水平扩展，以适应不断增长的物联网设备和数据流量，确保系统稳定性。
- 丰富的协议支持：除了 MQTT 协议外，EMQX 还支持多种消息传输协议。它允许开发人员扩展支持各种私有协议，以满足其应用需求。
- 数据集成：EMQX 与各种数据存储服务、消息队列、云平台和应用无缝集成。它可以连接到云服务，实现远程数据传输和基于云的分析。
- 安全和认证：EMQX 提供强大的安全功能，包括 TLS/SSL 加密传输、客户端认证和访问控制。它支持多种认证方法，如用户名/密码、X.509 证书和 OAuth，确保物联网通信的安全性。
- 规则引擎和数据处理：EMQX 具有灵活的规则引擎，可以基于设备数据进行实时数据处理和转发。它支持数据过滤、转换、聚合和持久化等操作，帮助用户根据业务需求进行分析和决策。
- 可视化监控和管理：EMQX 提供直观的可视化监控和管理界面，允许用户实时监控物联网设备和消息传输。用户可以查看连接状态、消息流量和其他指标，还可以进行设备管理、故障排除和系统配置操作。

<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>

### NanoSDK

[NanoSDK](https://github.com/emqx/NanoSDK) 是基于 NNG 项目拓展的 MQTT 3.1.1/5.0 SDK，同时也是第一个原生支持 MQTT over QUIC 的 C 语言 SDK。

- 其内部只依赖原生的 POSIX 校准API 实现。可轻松移植和适配到各种操作系统和硬件芯片架构。
- NanoSDK 不同于传统 MQTT SDK 只有 1-2 个线程，内部提供全异步 I/O 实现，默认多线程收发消息。因此 NanoSDK 可以充分的利用系统资源，提供更高消费吞吐能力。提供了高性能的客户端消费能力和更高的资源利用性价比。
- MQTT 3.1.1/5.0 支持原生断网消息缓存到 SQLite，并在网络恢复后自动续传。
- 内置多协议，支持诸如 MQTT 3.1.1/5.0 + SSL/TLS, MQTT over QUIC，WebSocket，nanomsg/SP, ZeroMQ 等协议的客户端支持。
- 提供丰富的 API 接口，合并 Broker 和 Brokerless 的消息模式，用户可以通过 API 自主协调。
- 代码完全开源，且由 EMQ 提供商业化原厂技术支持。



<section class="promotion">
    <div>
        联系 EMQ 车联网解决方案专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
