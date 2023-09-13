信息技术（IT）与运营技术（OT）的融合是指将原本独立的企业网络和计算系统与工业控制系统和设备相互连接，从而形成一个统一互联的生态系统。在选择 IT 与 OT 融合的协议时，需要综合考虑多种因素，包括具体的行业需求、现有的基础设施、安全性以及可扩展性等。

OPC UA 和 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是 IT 与 OT 融合场景中常用的协议。随着这两种技术的不断发展， OPC UA over MQTT 作为将两者有机结合的新协议，为行业带来了更多的优势。本文将详细介绍 OPC UA over MQTT，并探讨它在推动 IT 和 OT 融合方面的潜力。

## OPC UA over MQTT 的起源

**OPC UA** 是一种广受欢迎的协议，它能够有效地连接 IT 和 OT 环境。它提供了安全可靠的通信，以及标准化的数据模型，适用于实时数据交换和复杂信息共享。OPC UA 具有内置的安全机制，支持多种平台和设备。

[**MQTT**](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种轻量级的发布-订阅消息传输协议，专为资源受限环境中的高效数据传输而设计。它非常适合物联网和 OT 集成场景，在这种场景下带宽和功耗是重要的考虑因素。[MQTT 的发布-订阅模型](https://www.emqx.com/zh/blog/mqtt-5-introduction-to-publish-subscribe-model)支持向多个订阅者高效分发数据。

**OPC UA over MQTT** 是一种将 MQTT 和 OPC UA 整合在一起的协议，它充分发挥了这两种协议的优势。OPC UA 和 MQTT 各自拥有独特的优点，非常适合 IT 和 OT 的融合场景，其中 MQTT 用作传输方式，负责传送具备丰富数据语义的 OPC UA 数据。MQTT 的轻量级发布-订阅消息传输模型与 OPC UA 的标准化数据建模、安全特性以及广泛的复杂信息交换功能相结合，可以带来极大的益处。

## MQTT 发布-订阅模型的优势

### 灵活可扩展的 IT 和 OT 基础设施

MQTT 是一种以消息为核心的协议。它采用发布-订阅的消息传输模式，发布者将消息发送到中央消息 Broker，订阅者从 Broker 那里接收消息。[MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 在发布者和订阅者之间起着桥梁的作用，它接收发布者发布的消息，并将它们转发给订阅了特定主题的订阅者。

![Flexible and Scalable IT and OT Infrastructure](https://assets.emqx.com/images/04fad3e33add07f5623fb11655bde6de.png)

发布-订阅模式的消息传输系统天然具有比客户端-服务器系统更高的可扩展性。在客户端-服务器模型中，每个客户端都必须与服务器建立并保持连接，随着客户端数量的增加会导致性能瓶颈。在发布-订阅模型中，发布者只需将消息发送到中央 Broker，由 Broker 负责将消息分发给关注的订阅者。这种架构能够更有效地应对发布者和订阅者数量的增长。

### 网络带宽利用率

在客户端-服务器系统中，每个客户端的请求都会通过轮询机制在网络和服务器上产生流量。这就导致即使目标值没有变化，也会造成大量的网络流量浪费。而在发布-订阅系统中，订阅者只有在数据发生变化时才会收到更新，避免了不必要的网络开销。这对于物联网等需要及时发送传感器数据或状态更新的应用非常重要。

### 事件驱动架构

发布-订阅模型非常适合事件驱动型架构，在这种架构中，组件会对事件或数据变化做出反应。这在需要基于特定条件或事件触发动作的场景中非常有用。这得益于发送者（发布者）和接收者（订阅者）的解耦。发布者无需知道订阅者的身份，订阅者也无需知道发布者的身份。这种分离使得组件可以灵活地运行，互不干扰，从而提升资源利用率和响应能力。

![Publish-subscribe model](https://assets.emqx.com/images/c1ab4dba0def1c22c94be5f471ea5cff.png)

所以，发布者和订阅者不必了解彼此的存在或具体实现细节，从而便于在不影响整个系统的情况下更换或更新单个组件。

## OPC UA 丰富的数据语义

除了 MQTT 发布-订阅机制所带来的优势之外，OPC UA 在保障不同设备和应用之间的无缝通信方面也扮演了重要的角色。它擅长处理复杂的数据结构、层次化的数据模型、元数据，并且拥有强大的安全功能，非常适合具有复杂数据关系的应用场景。这使得该协议能够适应复杂多样的工业环境，不受不同工业领域使用的底层技术或供应商的限制。

OPC UA 已经在制造、过程自动化、能源、汽车等多个领域得到广泛应用。很多依托稳健和标准化通信来支撑运营的领域都采用了 OPC UA，特别是在一些可靠性和安全性至关重要的关键应用场景（如发电厂、化学处理和航空航天）。

## Operational Model of Building OPC UA over MQTT Messages

## OPC UA over MQTT 消息的操作模型

下图展示了发布者生成和发布消息的内部步骤，以及该过程所需的参数。该图还介绍了订阅者接收、解码和理解消息的过程，以及实现这些操作所需的参数。

![Diagram](https://assets.emqx.com/images/a43616ab5a8ac59a146fbfbac290a262.png)

### 发布者处理流程

**第 1 步 - 收集数据**

在开始阶段，需要收集数据（DataSet），以便进行发布。这个过程需要用一个名为 PublishedDataSet 的结构来设置收集的方式。在 PublishedDataSet 中，由 DataSetMetaData 定义了数据的基本细节。通过此数据收集过程，就能生成 DataSet 中每个字段的具体值。

**第 2 步 - 创建 DataSetWriter 和 DataSetMessage**

然后，用一个名为 DataSetWriter 的组件来生成 DataSetMessage。一个 WriterGroup 里面的不同 DataSetWriter 可以生成各自的 DataSetMessage，它们可以合并成一个统一的 NetworkMessage。

**第 3 步 - 创建 NetworkMessage**

接着，要基于之前获得的信息以及在 PubSubConnection 中设置的 PublisherId，来创建一个 NetworkMessage。这个 NetworkMessage 的结构必须符合所采用的特定通信协议。

**第 4 步 - 发布 NetworkMessage**

最后一步是把构建好的 NetworkMessage 发送到指定的面向消息的中间件。为了完成这一步，需要预先设定好中间件的地址。

### 订阅者处理流程

**第 1 步 - 连接和订阅**

订阅者根据需要选择面向消息的中间件，并通过给定的地址建立连接，可以使用 OPC UA UDP 的多播方式，也可以连接到 MQTT Broker。然后，订阅者开始监听传入的消息。为了只接收感兴趣的消息，订阅者可以设置一些过滤器，比如 PublisherId、DataSetWriterId 或 DataSetClassId，来排除不符合指定标准的消息。

**第 2 步 - 处理传入的 NetworkMessage**

NetworkMessage 到达后，要根据发布者使用的安全参数进行解密和解码。

**第 3 步 - 解码和应用相关处理**

NetworkMessage 解码后得到的 DataSetMessage 会被定向到对应的 DataSetReader。然后用 DataSetMetaData 来解码 DataSetMessage 的内容，DataSetMetaData 包含了字段的语法、版本信息和属性等详细信息。最后是与应用相关的处理，这里可以进行一些操作，比如把接收到的值映射到订阅者的 OPC UA AddressSpace 中的相应节点。

**第 4 步 - SubscribedDataSet 的订阅和管理**

订阅者需要配置 SubscribedDataSet 来分发数据。

有两种不同的配置方案：

- TargetVariables 配置用于将 DataSetMessage 字段分派到订阅者 OPC UA AddressSpace 中预先定义的变量。
- SubscribedDataSetMirror 配置用于将接收到的 DataSet 字段转换为订阅者 OPC UA AddressSpace 中的变量，如果这些变量不存在，它们将作为订阅者配置的一部分被创建。

### 配置工具

发布者和订阅者的设置和自定义通常通过专用的配置工具来实现。此配置过程包含两种方式：

1. 使用符合 PubSub 配置信息模型的通用 OPC UA PubSub 配置工具。

   ![OPC UA PubSub configuration tool](https://assets.emqx.com/images/3a778dee963d7d49584be505613cc445.png)

   > 注意：为了与 PubSub 配置信息模型保持一致，发布者和订阅者都需要充当 OPC UA 服务器。

2. 根据应用的具体特点使用供应商的专业配置工具。

   ![vendor-specific configuration tools](https://assets.emqx.com/images/a469e1b8753a2e096dc71e99b6d6eabc.png)

配置过程包括数据集的排列，以及确定最终发布数据的来源。这个配置可以使用 PubSub 配置模型来完成，该模型提供了一个标准化的框架，或者可以使用供应商设计的配置工具来定制，以适应他们的特定产品。

虽然 OPC UA 应用可以被预先配置为发布者，但通常还需要进一步配置来指定要包含在消息中的内容和发送这些消息的频率。这样就可以根据应用的需求，精确地调整消息内容和传输间隔，保证 OPC UA 网络中发布者和订阅者之间的高效通信。

## 适用于 IT 和 OT 组织的成熟协议

OPC UA over MQTT 是一个成熟的协议，已经在各个领域得到了广泛的应用和认可。它常被应用于监控和数据采集系统（SCADA）、制造执行系统（MES）、工业物联网解决方案等。许多工业自动化供应商，如西门子、倍福和库卡，都在其产品（从可编程逻辑控制器、传感器到软件平台）中提供了对 OPC UA over MQTT 的支持。这种广泛的支持体现了该协议的成熟度。

OPC UA over MQTT 协议不仅适用于物联网部署，还适用于云端应用。许多云服务提供商（如 AWS、Azure 和 GCP）都支持该协议，使得物联网数据可以轻松地集成到云端服务中，进行存储、分析和可视化。通过 OPC UA over MQTT 协议，OPC UA 的能力可以从云端延伸到边缘设备，并实现与工业物联网生态系统的无缝对接。

![Proven Protocol for IT and OT Organization](https://assets.emqx.com/images/f76c2d7f2c580da82d9c0c5b89d7be3e.png)

## 安全和认证

OPC UA over MQTT 提供了全面的安全机制，涵盖认证、授权、加密和数据完整性等方面。它能够应对工业环境中固有的安全挑战，有助于保护敏感数据和防止未经授权的访问。

## 结语

总之，OPC UA over MQTT 协议将 OPC UA 和 MQTT 协议的优势融合在一起，实现了高效的通信、标准化的数据建模和互操作性，是工业和物联网应用的理想选择。通过利用 MQTT 的轻量级特性和发布-订阅架构，同时保留 OPC UA 强大的数据表示和标准化服务，OPC UA over MQTT 协议为现代通信需求提供了一个灵活和多功能的解决方案。

[EMQX](https://www.emqx.com/zh/products/emqx) MQTT Broker 和 [Neuron](https://www.emqx.com/zh/products/neuron) 网关可以完美地支持 OPC UA over MQTT 协议。EMQX 作为一个 MQTT Broker，在消息传输方面表现出色，并具备高效的数据分发能力。而 Neuron 专注于将 OPC UA 与 MQTT 桥接，让您能够充分利用这两种协议的优势。



<section class="promotion">
    <div>
        联系 EMQ 工业领域解决方案专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
