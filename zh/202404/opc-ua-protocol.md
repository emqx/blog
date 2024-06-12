OPC UA（OPC Unified Architecture）是一个独立于平台、面向服务、开放和安全的通信架构。它被设计用来实现不同供应商的工业自动化设备、系统和软件应用的互操作性。OPC UA 信息模型定义了使用各种传输协议交换数据的编码规格。

OPC UA 和其前身——开放平台通信（OPC）是由同一个基金会所开发，但两者有显著不同，基金会继续开发 OPC UA 的目的是为了发展比原来 OPC 通讯更理想的架构，也更符合正在发展中的工业自动化需求。

## OPC UA 协议的发展历程

![OPC UA](https://assets.emqx.com/images/f4582b4676a6867f6beefa40c055fae2.png)

在 OPC UA 规范发布之前，行业供应商、最终用户和软件开发商曾合作开发了一套用于定义工业过程数据、警报和历史数据的规范。这套规范被称为 OPC Classic，于 1995 年首次发布，基于 Microsoft Windows 的 COM/DCOM 技术栈。它包括以下三个部分：

1. **OPC Data Access(OPC DA)**：定义了数据交换，包括数值、时间和质量信息。
2. **OPC Alarms & Events(OPC A&E)**：定义了报警和事件类型消息的交换以及状态管理。
3. **OPC Historical Data Access(OPC HDA)**：定义了可用于查询和分析历史数据的方法。

OPC Classic 以其在过程控制中的卓越性能而著称。然而，由于技术的进步和外部因素的变化，它已不能完全满足人们的需求。为解决这一问题，OPC 基金会于 2006 年推出了 OPC UA。这项新技术提供了跨平台数据传输、更可靠的安全性和更强的数据处理能力。OPC UA 集成了现有 OPC Classic 规范的所有功能，同时解决了 OPC Classic 存在的诸多问题。

目前，OPC UA 的最新版本是 1.05。除了提供客户端-服务器（订阅）模式，OPC UA 还包括一个 Pub-Sub 机制，允许通过 UDP 协议、[MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)或 [AMQP 协议](https://www.emqx.com/zh/blog/mqtt-vs-amqp-for-iot-communications)推送 JSON 规格的数据（也可以使用标准定义的二进制规格 - UADP）。

## OPC UA 的特点

**功能对等性**：所有 OPC Classic 规范都映射到 UA，OPC UA 包含 OPC Classic 中的 DA、A&E 和 HDA 功能：

| 功能     | 说明                                                         |
| :------- | :----------------------------------------------------------- |
| 发现     | 在本地 PC 或网络上查找可用的 OPC UA 服务器                   |
| 地址空间 | 所有数据都是分层表示的（例如文件和文件夹），允许 OPC UA 客户端发现、利用简单和复杂的数据结构 |
| 按需     | 基于访问权限读取和写入数据/信息                              |
| 订阅     | 监视数据/信息，并且当值变化超出客户端的设定时报告异常        |
| 事件     | 基于客户端的设定通知重要信息                                 |
| 方法     | 客户端可以基于在服务器上定义的方法来执行程序等               |

**平台独立性：**从嵌入式微控制器到基于云的基础设施，OPC UA 都不依赖于 Windows 平台，可在任何平台上部署使用。

**安全性：**信息加密、身份验证和审核，企业在选择技术标准时最重要的考虑之一是安全性。OPC UA 在通过防火墙时通过提供一套控制方案来解决安全问题：

| 功能       | 说明                                                         |
| :--------- | :----------------------------------------------------------- |
| 传输       | 定义了许多协议，提供了诸如 OPC 二进制传输或更通用的 SOAP-HTTPS 等选项 |
| 会话加密   | 信息以128位或256位加密级别安全地传输                         |
| 信息签名   | 信息接收时的签名与发送时必须完全相同                         |
| 测序数据包 | 通过排序消除了已发现的信息重放攻击                           |
| 认证       | 每个 UA 的客户端和服务器都要通过 OpenSSL 证书标识，提供控制应用程序和系统彼此连接的功能 |
| 用户控制   | 应用程序可以要求用户进行身份验证（登录凭据，证书等），并且可以进一步限制或增强用户访问权限和地址空间“视图”的能力 |
| 审计       | 记录用户和/或系统的活动，提供访问审计跟踪                    |

**可扩展性：** OPC UA 的多层架构允许在不影响现有应用程序的情况下，采用新的技术和方法，如新的传输协议、安全算法、编码标准和应用服务。这种添加新功能的能力使 OPC UA 成为一个 "面向未来"的框架。同时，OPC UA 与现有产品保持兼容。这意味着今天的 UA 产品可以与未来的 UA 产品互操作。

**综合信息建模：**用于定义复杂信息，OPC UA 信息建模框架将数据转换为信息，通过完全面向对象的功能，即使是最复杂的多级结构也可以建模和扩展，数据类型和结构可在配置文件中定义。

![OPC UA Information Modelling Framework](https://assets.emqx.com/images/1161f4a8f02d771efa813f234c8515a9.png)

## OPC UA 协议的应用

OPC UA 在工业自动化和物联网领域有着广泛的应用，例如数据收集、设备集成、远程监控、历史数据访问等。

### 制造业

- 数据收集和监控：制造业中的设备和生产线可以通过 OPC UA 轻松地收集数据，实时监控生产过程并优化生产效率。
- 设备集成和互操作性：来自不同制造商的设备可以无缝集成，实现从传感器到机器人等设备之间的数据交换。

### 建筑自动化

- 智能建筑管理：利用 OPC UA 连接照明、空调和安防系统等建筑自动化系统，可以实现智能能源管理和设备控制。
- 设备监控和维护：通过 OPC UA 可以实现建筑设备的状态监控和维护，提高设备的可靠性和效率。

### 石油和天然气

- 远程监控和控制：利用 OPC UA 可以远程监控和控制油田、管道和炼油厂的设备，减少人工干预。
- 数据历史记录：利用 OPC UA 的历史数据访问功能记录设备运行数据，便于分析和优化。

### 可再生能源

- 风电和太阳能场：利用 OPC UA 监控风电和太阳能场的运行状态，实现远程控制和故障排除。
- 电网管理：可再生能源接入和电网管理需要实时数据交换，OPC UA 提供了可靠的通信机制。

### 公用事业

- 水处理和供水系统：利用 OPC UA 监控水处理设备、泵站和供水系统，确保水质和供水稳定。
- 电力系统：利用 OPC UA 可以实现电力设备的监控、故障检测和远程操作。

## OPC UA 的信息模型

OPC UA 信息模型是节点的网络（Network of Node），或者称为结构化图（Graph），由节点（Node）和引用（Reference）组成，这种结构图称之为 OPC UA 的地址空间。地址空间以标准形式表示对象——地址空间中的模型元素被称为节点，对象及其组件在地址空间中表示为节点的集合，节点由属性描述并由引用相连接。OPC UA 建模其实就是建立节点以及节点间的引用。

### 对象模型

OPC UA 使用了对象作为过程系统表示数据和活动的基础。对象包含了变量，事件和方法，它们通过引用来互相连接。

![OPC UA 对象模型](https://assets.emqx.com/images/313bb04eebc2beaacc6c359eba0e17d8.png)

### 节点模型

![OPC UA 节点模型](https://assets.emqx.com/images/185c6a8d55d470c5e558bd3afd76a0ca.png)

- 属性（Attribute）用于描述节点，不同的节点类有不同的属性（属性集合）。节点类的定义中包括属性的定义，因此地址空间中不包括属性。
- 引用（Reference）表示节点之间的关系。引用被定义为引用类型节点的实例，存在于地址空间中。
- 节点模型的通用属性如下：

| Name                | Use  | Data Type              | Description                                |
| :------------------ | :--- | :--------------------- | :----------------------------------------- |
| **Attributes**      |      |                        |                                            |
| NodeId              | M    | NodeId                 | See 5.2.2                                  |
| NodeClass           | M    | NodeClass              | See 5.2.3                                  |
| BrowseName          | M    | QualifiedName          | See 5.2.4                                  |
| DisplayName         | M    | LocalizedText          | See 5.2.5                                  |
| Description         | O    | LocalizedText          | See 5.2.6                                  |
| WhiteMask           | O    | AttributeWhiteMask     | See 5.2.7                                  |
| UserWriteMask       | O    | AttributeWriteMask     | See 5.2.8                                  |
| RolePermissions     | O    | RolePermissionsType[]  | See 5.2.9                                  |
| UserRolePermissions | O    | RolePermissionsType[]  | See 5.2.10                                 |
| AccessRestrictions  | O    | AccessRestrictionsType | See 5.2.11                                 |
| **References**      |      |                        | No References specified for this NodeClass |

### 引用模型

包含引用的节点为源节点，被引用的节点称目标节点。引用的目标节点可以与源节点在同一个地址空间，也可以在另一个 OPC 服务器的地址空间，甚至是目标节点可以不存在。

![OPC UA 引用模型](https://assets.emqx.com/images/3b484967bea36515325de244dda332bd.png)

### 节点类型

在 OPC UA 中，最重要的节点类别是对象，变量和方法。

- 对象节点，对象节点用于构成地址空间，不包含数据，使用变量为对象公开数值，对象节点可用于分组管理对象，变量或方法（变量和方法总属于一个对象）。
- 变量节点，变量节点代表一个值，值的数据类型取决于变量，客户端可以对值进行读写和订阅。
- 方法节点，方法节点代表服务器中一个有客户端调用并返回结果的方法，输入参数和输出结果以变量的形式作为方法节点的组成部分，客户端指定输入参数，调用后获得输出结果。

## OPC UA 协议的工作原理

硬件供应商支持 OPC UA 的方式有两种：在设备中嵌入 OPC UA 服务器，或在 PC 上提供软件，通过专用协议获取数据，并通过 OPC UA 将其公开给其他平台。一些中端和高端 PLC（如西门子 S71200/1500） 集成了 OPC UA 服务器，同时西门子还提供 WINCC 等软件，通过 OPC/OPC UA 间接向第三方提供来自其他设备的数据。

 ![opc ua client and server](https://assets.emqx.com/images/e9398279706d0e493388a5c60fede41f.png)

数据通过 OPC UA 服务器公开后，可使用 OPC UA 协议规定的两种访问模式——请求/响应模式和发布/订阅模式进行访问。首先，客户端必须与服务器建立连接，连接建立后会在客户端和服务器之间创建一个会话通道。

在请求/响应模式下，客户端应用程序可以通过会话通道向服务器请求一些标准服务，如：从节点读取原始数据、向节点写入数据、调用远程方法等。

![request/response mode](https://assets.emqx.com/images/f7c47ebeb1f5da8bc6290b6b014b106e.png) 

在发布/订阅模式下，每个客户端可以创建任意数量的服务器订阅，当服务器的节点数据发生变化时，通知消息会立即推送到客户端。

![publish/subscribe mode](https://assets.emqx.com/images/16eedf2be88eb090746d9a7de6ad40e5.png)

一般来说，终端用户不必关注上述过程。他们只需要关心 OPC UA 服务器地址、用户登录策略、通信安全策略以及数据的访问地址。

### OPC UA 服务器端点

| **Protocol**      | **Url**                                |
| :---------------- | :------------------------------------- |
| OPC UA TCP        | `opc.tcp://localhost:4840/UADiscovery` |
| OPC UA Websockets | `opc.wss://localhost:443/UADiscovery`  |
| OPC UA HTTPS      | `https://localhost:443/UADiscovery`    |

### 用户验证方法

1. Anonymous
2. Username & Password
3. Certificate

### 安全模式

1. None
2. Sign
3. Sign & Encrypt

### 安全策略

1. Basic128Rsa15
2. Basic256
3. Basic256Sha256
4. Aes128Sha256RsaOaep
5. Aes256Sha256RsaPass

### 节点地址

| **Address type** | **Address**          |
| :--------------- | :------------------- |
| Byte string      | ns=x;b=<byte string> |
| GUID             | ns=x;g=<GUID>        |
| Int              | ns=x;i=x             |
| String           | ns=x;s=<string>      |

## OPC UA 与 MQTT 的结合

MQTT（Message Queuing Telemetry Transport）是一种为物联网设备和应用程序设计的消息协议，采用发布与订阅模型，具有轻量、高效、可靠，支持实时通讯等优点。 MQTT 非常适合资源受限的环境，特别是需要高效使用电力和带宽的场景。

业界在 MQTT 3.1.1 的基础上建立了名为 SparkplugB 的工业物联网数据规范，在保证灵活和效率的前提下，提供了基础的数据统一建模能力。得益于 MQTT 协议的优秀设计，SparkPlugB 提供了良好的网络状态感知能力，并且能够为设备和系统提供强大的互操作性。

OPC UA 和 MQTT 在功能上有一定程度的重叠，但它们的使用场景却截然不同：

- OPC UA 是一种用于工业场景的通信协议，可使来自不同制造商的不同设备和系统使用标准化语言进行无缝通信。
- MQTT 是一种物联网协议，专为基于互联网的传感器数据传输而设计，既能满足低带宽和不可靠的网络条件，又能有效处理连续的实时数据。它的订阅/发布机制为使用提供了极大的灵活性。

在工业场景中，MQTT 擅长在分布式系统中发送信息，而 OPC UA 则侧重于提供互操作性。通过将两者结合，可以使用 OPC UA 对业务数据进行抽象和聚合，而 MQTT 则可以利用其强大的连接能力，以分布式方式实现无缝数据交换。

## OPC UA over MQTT

OPC 基金会在最新的 OPC UA 规范中提出的 Pub-Sub 模型允许使用 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 将数据变更推送给订阅者。

![OPC UA over MQTT](https://assets.emqx.com/images/e3772239f0f42b2f622996c721d7e57f.png)

Pub-Sub 的安全性比客户端/服务器中的安全性要复杂一些，而且规范没有那么细致。在 MQTT 网络中，安全性基于 SSL/TLS，MQTT Broker 除了可以为传输启用 SSL/TLS，还可以定义应用程序级身份验证，原则上，对于每个可以加入网络的订阅端和发布端，这些安全模式要么全有，要么全无。新的 OPC UA 标准化仍在进行中，丰富的 OPC UA 信息模型如何以最佳方式映射到 MQTT 目前尚不明确。

## 使用 EMQX 和 Neuron 桥接 OPC UA 到 MQTT

[Neuron](https://neugates.io/zh) 是一款现代的工业物联网连接服务器，可以连接多种使用标准协议或者设备专有协议的工业设备，实现了工业物联网平台与海量设备的互联。作为一款轻量级的工业协议网关软件，Neuron 可以运行在各种有限资源的物联网边缘硬件设备上，其主要目标是应对以统一方式访问以数据为中心的自动化设备的挑战，从而为智能制造提供必要的支持。

[EMQX](https://www.emqx.com/zh/products/emqx) 是一款大规模可扩展的云原生分布式物联网 MQTT 消息服务器。作为全球最具扩展性的 MQTT 消息服务器，EMQX 可为海量物联网设备提供高效可靠的连接，实现消息和事件流的高性能实时移动和处理，帮助用户快速构建关键业务的物联网平台与应用。

Neuron 的南向 OPC UA 驱动程序可采集和汇总 OPC UA 数据源，将其转换为 MQTT 协议，并传输到 EMQX MQTT Broker。然后，后者将其分发到各种分布式应用程序。

完整桥接教程请查看: [Bridging OPC UA Data to MQTT for IIoT: A Step-by-Step Tutorial](https://www.emqx.com/zh/blog/bridging-opc-ua-data-to-mqtt-for-iiot)



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
