## **OPC 协议概述**

OPC（Open Platform Communications）协议在工业自动化领域扮演着至关重要的角色，它是设备、控制系统以及应用间通信的核心技术标准。该协议通过为不同厂商的设备和系统提供统一的数据交换方式，显著提升了工业控制系统的互操作性与工作效率。

The OPC standard is divided into Classic and Unified Architecture:

OPC 标准主要分为两大类，分别是经典架构和统一架构：

- **OPC 经典**规范诞生于 1996 年，基于微软 Windows 技术，使用分布式组件对象模型（COM/DCOM）在软件组件之间交换数据。它包括 OPC DA、OPC AE、OPC HAD 和 OPC DX 等子规范，这些子规范分别提供了过程数据访问、报警事件订阅和历史数据查询的单独定义。
- **OPC 统一**架构（UA），作为 OPC 经典的继任者，于 2006 年发布。它将各种 OPC 经典子规范的功能集成到一个可扩展的框架中，独立于平台且面向服务。它不再依赖 COM 实现，并在安全性和可扩展性方面更加强大。

OPC UA 和 OPC DA 在互操作性、安全性、功能、性能和兼容性等多个方面有显著差异，这些差异可能会影响生产和管理成本。本文将提供关于 OPC DA 和 OPC UA 的全面指南，帮助读者根据特定的工业需求做出明智的选择，从而有效减少不必要的成本。

## **深入探索 OPC DA**

### OPC DA 简介

在 OPC 技术诞生之前，自动化领域缺乏一个用于设备互联的统一标准。各硬件制造商和软件制造商都采用自己的通信协议，这不仅导致了协议的混乱，也使得通信成本上升。

为了促进不同软件和硬件之间的互操作性，OPC 经典应时而生。

OPC DA（Data Access）是 OPC 基金会最初推出的协议标准之一，主要用于实时数据的访问与交换。它基于微软的 COM/DCOM 技术，为工业自动化系统提供了一个统一的通信接口。

OPC DA 支持实时数据的读取、写入、订阅和取消订阅等操作。它采用客户端/服务器架构，使得多个客户端能够同时从服务器获取数据。

它广泛应用于制造、过程控制、能源管理以及石油和天然气、化工、制药和电力等领域。

### OPC DA 的优缺点

优点：

- 技术成熟
- 应用广泛
- 易于实施和部署

缺点：

- 依赖 Windows 平台
- 缺乏安全机制
- 数据模型简单
- 对接难度较大

## **OPC UA 协议解析**

### OPC UA 简介

[OPC UA](https://www.emqx.com/zh/blog/opc-ua-protocol) 是 OPC 基金会在吸取 OPC DA 经验的基础上推出的新一代协议标准。它采用面向服务的架构（SOA），提供了一个与平台无关、安全性高、可扩展性强的通信机制。

OPC UA 相较于 OPC DA，引入了更加丰富的数据模型，支持复杂数据类型和语义描述。它还内置了如认证、授权和加密传输等安全机制。除此之外，OPC UA 还支持 TCP、HTTPS、WebSocket 等多种传输协议。

OPC UA 凭借其卓越的性能和灵活性，已在工业物联网（IIoT）、智能制造、远程设备监控等多个领域得到广泛应用。例如，在智能工厂中，OPC UA 能够实现从生产线设备到更高层级管理系统（如 MES、ERP 等）的无缝数据集成。

### OPC UA 的优缺点

优点：

- 平台无关
- 强化的安全特性
- 丰富的信息模型
- 方便对接

缺点：

- 协议相对较为复杂

## **详细对比**

|              | **OPC UA**                                                   | **OPC DA**                                                   |
| :----------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 服务发现     | 支持在本地网络或 Internet 上查找可用的 OPC UA 服务器         | 仅支持在本地网络查找 OPC DA 服务器                           |
| 命名空间     | 所有数据以层次化方式表示（类似文件和文件夹），不管简单还是复杂的数据结构， OPC UA 客户端都能够发现并使用 | 提供基础的层次化数据表示支持                                 |
| 访问控制     | 根据访问权限进行数据/信息的读写                              | 支持                                                         |
| 订阅         | 支持                                                         | 支持                                                         |
| 事件         | 支持                                                         | 支持                                                         |
| 方法         | 支持远程方法调用                                             | 不支持                                                       |
| 跨平台       | 提供良好的跨平台支持，支持主流芯片架构，兼容多种操作系统     | 仅支持 Windows 操作系统                                      |
| 数据传输     | 定义了多种协议，提供如 OPC 二进制传输或更通用的 SOAP-HTTPS 等多种选择 | 依赖 Windows COM 和 DCOM 传输，编程接口中隐藏了所有传输细节  |
| 会话安全     | 信息以 128 位或 256 位加密级别安全传输；接收和发送信息时的签名必须一致；每个 UA 客户端和服务器都必须通过 OpenSSL 证书进行认证，确保应用程序和系统的连接控制；通过排序机制消除重放攻击；应用程序可以要求用户认证（登录凭证、证书等），并可进一步限制或增强用户的访问权限和查看地址空间的能力；记录用户和/或系统活动，提供访问审计跟踪功能 | 采用 Windows DCOM 会话机制，安全细节被隐藏                   |
| 未来前景     | OPC UA 的多层架构设计允许引入创新技术和方法，如新的传输协议、安全算法、编码标准和应用服务，而不会影响现有应用程序 | 微软已宣布停止支持 DCOM 技术，OPC DA 在新版 Windows 操作系统中无法得到可靠支持 |
| 综合信息建模 | 不断引入新功能                                               | 不支持                                                       |

## **OPC UA 与 OPC DA 选型**

在决定采用 OPC UA 还是 OPC DA 时，您需要考虑以下几个关键因素：

- **系统平台及兼容性需求**

  OPC UA 能够适应多种环境和设备，而 OPC DA 的服务器和客户端仅能在 Windows 操作系统上运行。如果您的部署环境较为复杂，那么 OPC UA 将是更优的选择。

- **数据模型的复杂性及功能需求**

  OPC UA 提供了强大的业务抽象能力，可以直接将业务逻辑转化为实际的 OPC UA 信息模型，并且易于调整；相比之下，OPC DA 仅提供基于 “服务器/组/标签”的层次结构。对于需要处理复杂业务逻辑的情况，OPC UA 更为合适。

- **安全性和可靠性要求**

  OPC DA 需要一个稳定的操作环境，通常是内网环境。如果您的网络环境较为复杂，例如需要通过公共网络传输数据，那么 OPC UA 将是更安全的选择。

- **可扩展性和未来发展需求**

  OPC UA 的可扩展性远超 OPC DA，而且随着微软对 COM 技术的支持减少，OPC DA 的未来将受到影响。OPC DA 的设计基于过时的中间件技术思想。因此，对于面向未来的应用，您应该优先考虑 OPC UA。

- **项目预算和实施时间表**

  考虑到 OPC UA 的诸多优势，它似乎可以有效降低部署和维护成本。对于预算有限的项目，您可以根据具体情况在 OPC UA 和 OPC DA 之间做出选择。

- **技术团队的经验和能力**

  OPC UA 相较于 OPC DA，需要更深入地理解配置和开发的概念，尤其是在会话安全和综合信息建模方面。而 OPC DA 的配置主要集中在 Windows 系统内的设置上。

## **关于 OPC UA 和 OPC DA 的常见问题解答**

### OPC UA 能否完全取代 OPC DA？

虽然 OPC UA 是基于 OPC DA 的升级版，但在特定场景下，尤其是对于老旧系统，OPC DA 仍然具有其独特的应用价值。两者可以并存，相互补充。

### 实施 OPC UA 是否困难？

尽管 OPC UA 协议可能较为复杂，但目前已有许多成熟的开发工具包和框架，这些工具大大降低了实施难度。此外，许多供应商提供了基于 OPC UA 的成熟解决方案。

## **NeuronEX：支持 OPC 协议的工业网关**

[NeuronEX](https://www.emqx.com/zh/products/neuronex) 是专为工业领域设计的软件，专注于设备数据采集和边缘智能分析。它主要部署于工业环境，促进工业设备通信、工业总线协议采集、工业系统数据集成、边缘级数据过滤与分析、AI 算法集成，以及与 [工业物联网平台](https://www.emqx.com/zh/blog/iiot-platform-key-components-and-5-notable-solutions)集成。NeuronEX 提供多协议接入能力，支持同时接入如 [Modbus](https://www.emqx.com/zh/blog/modbus-protocol-the-grandfather-of-iot-communication)、[OPC UA](https://www.emqx.com/zh/blog/opc-ua-protocol), Ethernet/IP、Ethernet/IP、[BACnet](https://www.emqx.com/en/blog/bacnet-protocol-basic-concepts-structure-obejct-model-explained)、西门子、三菱等数十种工业协议。

NeuronEX 的 OPC UA 插件可作为客户端访问 KEPServerEX、工业网关 OPC 服务器、Prosys 模拟服务器和 Ignition 等 OPC UA 服务器。它也可以直接访问硬件设备的内置 OPC UA 服务器，例如西门子 S7-1200 PLC、欧姆龙 NJ 系列 PLC 等的内置服务器。更多信息，您可以查看 [OPC UA | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/opc-ua/overview.html)以及[在工业物联网中将 OPC UA 数据桥接到 MQTT：详细教程](https://www.emqx.com/zh/blog/bridging-opc-ua-data-to-mqtt-for-iiot)。

NeuronEX 不直接支持 OPC DA 数据的直接采集。但是，可以使用 NeuOPC 将 OPC DA 转换为 OPC UA，然后利用 NeuronEX 的 OPC UA 插件进行数据采集。更多信息，您可以查看 [OPC DA | Neuron 文档](https://docs.emqx.com/zh/neuron/latest/configuration/south-devices/opc-da/overview.html)。

## **结语**

虽然在某些特定场景下 OPC DA 可能具有优势，但总体而言，OPC UA 提供了一个更加健壮且面向未来的解决方案，具备增强的安全特性和更好的现代工业应用支持。选择 OPC UA 还是 OPC DA 将取决于每个工业项目的具体需求和目标，做出明智的决策将对效率、成本效益和长期整体性能产生重大影响。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
