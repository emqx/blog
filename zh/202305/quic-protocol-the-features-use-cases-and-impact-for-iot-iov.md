## 什么是 QUIC 协议

QUIC（Quick UDP Internet Connections）是由谷歌公司开发的一种基于用户数据报协议（UDP）的传输层协议，旨在提高网络连接的速度和可靠性，以取代当前互联网基础设施中广泛使用的传输控制协议（TCP）。

QUIC 通过加密和多路复用技术来提供更高的安全性和更快的数据传输。它支持在单个连接上并行发送多个数据流，从而降低延迟并提高吞吐量。QUIC 还具有拥塞控制和流量控制等机制，以应对网络拥塞并保证数据传输的稳定性。

国际互联网工程任务组（IETF）已完成对 QUIC 的标准化，并且主流的 Web 浏览器和服务器正在逐步采用它。与 TCP 相比，QUIC 在高延迟和不稳定的网络环境中，如移动网络，可以显著提升网页加载速度并减少连接中断，使得网络体验更加流畅。

## QUIC 协议的基本特性

**相互独立的逻辑流**

相互独立的逻辑流是 QUIC 的核心特性之一。它允许在单个连接上并行传输多个数据流，并且每个流可以独立地处理。相比之下，TCP 只支持单数据流，需要按照发送顺序接收和确认每个报文。通过多路复用，应用程序可以更高效地发送和接收数据，并更好地利用网络带宽等资源。

**一致安全性**

QUIC 的另一个重要特性是它提供了端到端的安全保护。所有通过 QUIC 发送的数据都是默认加密的，并且不支持明文通信。这有助于防止数据被窃听和其他形式的攻击。QUIC 使用传输层安全协议（TLS）来建立和维护安全连接和端到端加密。

**低延迟**

QUIC 协议的设计目的是减少建立连接所需的延迟，以便在端点之间快速地发送和接收数据。对于移动网络这种高延迟的网络环境来说，这一点尤为重要。为了实现这个目标，QUIC 最小化了建立连接所需的往返次数，并且采用更小的报文来发送数据。传统的互联网协议通常存在延迟问题，例如美欧之间的往返时间有时可达 300 或 400 毫秒。

**可靠性**

QUIC 基于 UDP 但可提供可靠传输能力。类似于 TCP，它是一种面向连接的传输协议。QUIC 协议在数据传输过程中具有报文丢失恢复和重传功能，这可以确保数据的完整性和准确性。此外，QUIC 可以保证数据包按照发送顺序到达，避免因数据包乱序导致的数据错误。

**消除 HOL 阻塞**

QUIC 通过支持多个数据流来解决 HOL 阻塞问题。这使得来自不同应用的消息可以独立地传递，避免了因为等待其他应用而可能产生的延迟。

## QUIC 协议常见的应用场景

随着 HTTP/3 和 QUIC 越来越流行并被广泛采用，涌现出多种多样的应用场景。这些应用场景覆盖了直播、视频、点播、下载、Web 加速等领域，其中最具潜力的应用场景有：

1. **实时 Web 和移动应用：**这些应用（如集成了语音和视频通信功能的 Web 和移动应用）需要低延迟和可靠的数据传输。QUIC 利用相互独立的数据流和拥塞控制机制，使其成为这些应用的理想选择，因为它可以快速高效地发送和接收数据。在 QUIC 的多路复用模式下，同一连接内不同数据流之间的数据传输互不干扰。
2. **与物联网设备通信：**物联网设备通常使用 TCP 和 MQTT 等协议进行通信。然而，这些协议在受限的网络环境中可能存在高延迟和丢包等问题。相比之下，专为高延迟和丢包的网络环境而设计的 QUIC 可以提供更可靠和高效的替代方案。QUIC 可以实现接近零的往返时间（RTT），这对于提高网络性能和用户体验至关重要。
3. **车联网和网联汽车：**QUIC 可以极大地促进车联网生态系统的发展。这些系统需要实时的数据交换来提供诸如交通管理、车辆跟踪和安全功能等服务。QUIC 具有低延迟、多路复用的特性，以及对数据包丢失和重排序的处理能力，可以确保车辆和基础设施组件之间可靠而高效的通信。此外，QUIC 使用 TLS 加密保护敏感车辆数据，提供了更强的安全保障。
4. **云计算：**云计算是指通过互联网提供计算资源的服务。使用 QUIC 协议可以带来多方面的好处，例如低延迟和端到端加密，这可以提升用户体验、增强系统安全。
5. **支付和电子商务应用：**这些应用需要安全可靠的数据传输。QUIC 通过 TLS 加密和可靠的 HTTP3 数据流，使其成为这些应用的理想选择，有助于保证数据安全完整地传输。从终端用户的角度来看，QUIC 协议通过保证更快、更顺畅的交易，优化了用户体验。

## MQTT 与 MQTT over QUIC

[MQTT](https://www.emqx.com/zh/mqtt-guide) 是一种适用于低带宽、高延迟或不稳定网络环境的轻量级消息协议。它运行在应用层，主要用于机器对机器（M2M）通信和物联网场景。MQTT 采用发布/订阅模型，设备将消息发送到 Broker（即发布），其他设备根据主题接收这些消息（即订阅）。

对于 Web 应用而言，QUIC 专注于提高其性能和安全性，而 MQTT 则专为资源受限的网络环境提供轻量级和高效的消息传递解决方案。基于 QUIC 的 MQTT 可以显著提高性能并降低延迟，同时无需额外的 TLS 开销。由于大多数 QUIC 栈实现是在用户空间完成的，因此可以根据应用层的要求，自定义 QUIC 的数据传输，以适应不同的网络环境。

## MQTT over QUIC 与 MQTT over TCP/TLS 对比

MQTT over TCP/TLS 指的是使用 TCP 作为传输层的 MQTT 协议。TCP 是一种可靠的、面向连接的协议，可确保数据包在设备之间的正确传递。 TLS 是一种加密协议，通过加密两个端点之间传输的数据，为网络提供安全通信。通常情况下，TLS 作为 TCP 的上层协议使用，它使用 TCP 在两个端点之间建立和维护连接，并加密在该连接上传输的数据。

![MQTT over QUIC](https://assets.emqx.com/images/c9b14126eeeb755091acaf59a27c6da6.png)

MQTT over QUIC 相比 MQTT over TCP/TLS 具有明显的优势：

**连接建立：**

- MQTT over TCP/TLS：MQTT over TCP/TLS 遵循 TLS1.2 规范，需要在 TCP 层和 TLS 层各进行一次握手。这意味着在应用层开始交换数据之前，需要进行两到三次往返通信。
- MQTT over QUIC：MQTT over QUIC 遵循 TLS1.3 规范，可以利用零或一次往返（0-RTT 或 1-RTT）握手快速建立连接，降低连接建立时的延迟。

**延迟和性能：**

- MQTT over TCP/TLS：提供可靠的数据传输，但 TCP 的 HOL 阻塞问题和拥塞控制机制可能导致延迟增加和性能降低，尤其是在不可靠的网络环境下。
- MQTT over QUIC：将 TCP 的可靠性与 UDP 的低延迟特性相结合。QUIC 的多路复用特性有助于最小化 HOL 阻塞问题，从而在有丢包或高延迟的网络环境下提高性能。

**安全性：**

- MQTT over TCP/TLS：为了保证 MQTT 通信的安全，通常将其与 TLS 结合使用，TLS 提供了加密和认证功能。但是，这需要在连接建立和数据传输过程中增加额外的开销。
- MQTT over QUIC：QUIC 使用 TLS1.3 实现了内置加密，提供了安全的通信，无需额外的设置或开销。

**客户端的连接迁移：**

- MQTT over TCP/TLS：如果 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)或服务器更换了 IP 地址或网络，那么现有的 TCP 连接就必须断开并重新建立，这会增加应用对异常处理的难度，容易出现各种因处理异常导致的 Bug。
- MQTT over QUIC：支持连接平滑迁移，允许客户端或服务器在不影响正在进行的通信的情况下更换 IP 地址、端口或网络。

**应用和支持：**

- MQTT over TCP/TLS：已经得到了广泛的应用和支持，很多平台和编程语言都有 [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)、客户端和库的实现。
- MQTT over QUIC：到目前为止，由于 QUIC 仍然是一种新兴的协议，因此 MQTT over QUIC 还没有得到广泛的应用和支持。

## MQTT over QUIC 在车联网中的应用场景

在车联网场景下，MQTT over QUIC 可以带来很多优势，因为低延迟、可靠和安全的通信对各种应用来说都非常重要。由于 QUIC 结合了 TCP 和 UDP 的优点，并且提供了内置的加密，因此它可以显著提高基于 MQTT 的车联网应用的性能和安全性。

在车联网中使用 MQTT over QUIC 的场景包括：

- **车对基础设施（V2I）通信：**QUIC 的低延迟和可靠的数据传输可以提高车辆与基础设施组件（如交通信号灯、收费系统或智能停车系统等）之间的通信效率。
- **车对车（V2V）通信：**快速和安全的数据交换对于诸如碰撞避免、协同自适应巡航控制和编队等应用非常关键。MQTT over QUIC 可以为这些应用提供必要的速度和安全保障。
- **车联网（V2X）通信：**V2X 通信将车辆、基础设施和其他道路用户组合起来，旨在提高道路安全和交通效率。MQTT over QUIC 可以提供可靠的通信，并减少延迟，确保关键信息的及时交换。
- **车载资讯娱乐和远程诊断系统：**MQTT over QUIC 可以提高资讯娱乐系统的性能，实现更快的媒体流、导航更新和实时交通信息，同时确保通信安全。
- **车队管理和跟踪：**实时跟踪和管理车队需要车辆和管理系统之间的高效通信。MQTT over QUIC 可以提供可靠和安全的通信，实现车辆位置、诊断和驾驶行为的实时更新。
- **OTA 更新：**安全可靠的 OTA 更新对更新车辆固件和软件至关重要。MQTT over QUIC 可以提供必要的安全性和可靠性，无需中断车辆操作就可以传送这些更新。
- **应急响应：**在紧急情况下，可靠和快速的通信非常重要。MQTT over QUIC 可以确保及时安全地在应急车辆、响应团队和控制中心之间交换信息。

## EMQX：首个实现 MQTT over QUIC 的 MQTT Broker

[EMQX](https://www.emqx.io/) 是全球领先的开源 MQTT Broker，拥有高性能的实时消息处理引擎，为海量的物联网设备事件流处理提供动力。EMQX 从 5.0 版本开始支持 MQTT over QUIC，成为首个支持 MQTT over QUIC 的 MQTT Broker。不仅为现代复杂网络的 MQTT 消息传输提供了一种更高效安全的新方式，同时可以在某些场景下显著提高 MQTT 性能。

EMQX 支持将传输层替换为 QUIC 流，客户端可发起连接并创建双向流，从而实现更加高效可靠的通信。EMQX 支持两种操作模式：

- **单流模式**是一种基本模式，它将 [MQTT 报文](https://www.emqx.com/zh/blog/introduction-to-mqtt-control-packets)封装在一个双向的 QUIC 流中。该模式提供了快速握手、有序数据传输、连接恢复、0-RTT、客户端地址迁移以及增强的丢包检测和恢复等功能。这种模式使得客户端和 Broker 之间的通信更加快速和高效，同时保持有序，还能够快速恢复连接，并支持在不影响客户端通信的情况下迁移其本地地址。
- **多流模式**利用了 QUIC 的多路复用特性，允许 MQTT 报文在多个流中传输。这使得单个 [MQTT 连接](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)可以并行传输多个主题的数据且互不干扰。该模式还提供了多项优化，例如解耦连接控制和 MQTT 数据交换、避免 HOL 阻塞、分离上行和下行数据、优先处理不同类型的数据、提高并发性、增强鲁棒性、允许对数据流进行流量控制以及降低订阅延迟等。

![单流模式与多流模式](https://assets.emqx.com/images/c616fc21fc02c7e3da8ac4839c8f1307.png)

**使用 NanoSDK 客户端连接 MQTT over QUIC**

[NanoSDK](https://github.com/nanomq/NanoSDK/) 是基于 C 语言开发的第一个支持 MQTT over QUIC 的 SDK，完全兼容 EMQX 5.0。NanoSDK 的主要特点包括异步 I/O、将 MQTT 连接映射到 QUIC 流、低延迟的 0-RTT 握手以及多核并行处理等。

![NanoSDK](https://assets.emqx.com/images/118e7b112f66553ae4f4d33a759cc409.png)

此外，EMQX 还为多种编程语言提供了客户端 SDK，以支持 MQTT over QUIC，包括：

- [NanoSDK-Python](https://github.com/wanghaEMQ/pynng-mqtt)：NanoSDK 的 Python binding。
- [NanoSDK-Java](https://github.com/nanomq/nanosdk-java)：NanoSDK 的 Java JNA binding。
- [emqtt - Erlang MQTT 客户端](https://github.com/emqx/emqtt)：使用 Erlang 开发的支持 QUIC 的 MQTT 客户端。

**更多内容推荐：**

- [了解更多](https://docs.emqx.com/en/enterprise/v5.0/mqtt-over-quic/introduction.html#mqtt-over-quic) EMQX 的 MQTT over QUIC 解决方案。

- [阅读我们的博客](https://www.emqx.com/en/blog/getting-started-with-mqtt-over-quic-from-scratch)开始使用 MQTT over QUIC。

  

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
