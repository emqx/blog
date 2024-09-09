[在之前的文章中](https://www.emqx.com/zh/blog/unified-namespace-next-generation-data-fabric-for-iiot)，我们介绍了什么是统一命名空间（UNS），以及它为什么是工业物联网 4.0 的核心技术。在构建统一命名空间过程中，MQTT 技术往往是首选。不熟悉 MQTT 的读者可能会好奇，为什么 MQTT 总是和统一命名空间一起出现在工业物联网 4.0 的解决方案中呢？本文将为您揭示 MQTT 成为构建统一命名空间的最佳伙伴的原因。

## 什么是 MQTT

在探索统一命名空间之前，我们有必要先了解一下 MQTT 的基本知识。

MQTT（Message Queuing Telemetry Transport）是一种轻量级、基于发布/订阅模式的消息传输协议。它由 Andy Stanford-Clark（IBM）和 Arlen Nipper（Eurotech）于 1991 年创建，目的是为了在不稳定的卫星网络上连接石油管道。因此，MQTT 从诞生之日起就致力于为资源受限的设备和低带宽、高延迟或不可靠的网络提供高效的连接。如今，它已经成为物联网行业的事实标准。

深入了解 MQTT，请阅读文章：[MQTT 协议入门：基础知识和快速教程](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)。

## 为何使用 MQTT 构建统一命名空间

在上篇文章中，我们介绍了一个常见的统一命名空间定义：统一命名空间是将业务映射到数字基础设施上。要建立高效的统一命名空间，关键在于拥有一个能够有效地连接大量制造设备，并将整个业务从物理世界融合到数字世界的技术栈。

这正是 MQTT 在统一命名空间中起着关键作用的原因。在其他行业（比如[车联网](https://www.emqx.com/zh/blog/mqtt-for-internet-of-vehicles)），MQTT 通常被用作标准通信协议，依靠 MQTT Broker 来管理分散的连接和连接分布式设备，在[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)中也是如此。

以下是 MQTT 适合用于构建统一命名空间的原因。

### MQTT 具有轻量级、扩展性强的特点

统一命名空间需要一个数据中心作为连接所有制造环节（包括 PLC、SCADA、MES 和 ERP）的唯一数据源。实时数据的量非常庞大，数据中心在大型的解决方案中通常要处理数千甚至数百万的并发连接。

MQTT 由于采用了二进制格式，所以具有极低的开销和带宽消耗。这种轻量级的设计最小化了消息的大小，减少了网络流量。这一特性与统一命名空间和工业物联网非常契合。

![MQTT Characteristics](https://assets.emqx.com/images/9526d72e6e7443079eae5989030e2403.png)

![MQTT Packet](https://assets.emqx.com/images/5b297fda9fd32c49b606fbf65f11f540.png)

企业应该将更多精力集中于业务运营，而不是浪费时间考虑如何扩展基础设施资源以支持未来业务的迅速增长。这就是为什么统一命名空间的可扩展性至关重要。在 MQTT 架构中，有些 Broker 具有出色的可扩展性，能够支持每秒处理数百万条消息，例如 [EMQX](https://www.emqx.com/zh/products/emqx)。

> 要了解更多信息，请阅读：[EMQX 5.0 支持 1 亿 MQTT 连接](https://www.emqx.com/zh/blog/reaching-100m-mqtt-connections-with-emqx-5-0)

### MQTT 连接万物

MQTT 或许是工业物联网领域的新秀，但它已经赢得了广泛的关注。这是因为 MQTT 涵盖了旧的工业物联网技术的最大公共子集，使它成为一种能够连接现有系统的各个组件而不带来任何副作用的理想工具。

没有任何一种技术和产品能够适应所有的场景，不能单靠 [OPC UA](https://www.emqx.com/zh/blog/opc-ua-over-mqtt-the-future-of-it-and-ot-convergence) 或仅依赖一种协议来构建统一命名空间，尤其是还需要引入云计算技术时。统一命名空间必须将不同的技术融合在一起，而 MQTT 就是那个能够将它们统一在一个命名空间中的连接器和协调器。

![Adopt MQTT in UNS](https://assets.emqx.com/images/ae8ba11ca3abe2ddbc134ab220585b55.png)

在开源世界中，有许多数据转换工具和协议代理软件，例如 [Neuron](https://github.com/emqx/neuron)、ignition 和 PLC4X。您既可以把 [OPC UA 和 MQTT](https://www.emqx.com/zh/blog/bridging-opc-ua-data-to-mqtt-for-iiot) 连接在一起，也可以把 Modbus 和 Ethercat 连接在一起。

<section class="promotion">
    <div>
        免费试用 Neuron
      <div class="is-size-14 is-text-normal has-text-weight-normal">连接海量异构工业设备从边缘到云端。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>

在工业物联网 3.0 中，进行数字化转型的公司需要在传统系统的各个层级之间传输数据，例如 MES、ERP、CRM 和 WMS。这就造成了一个复杂的互联难题，被称为“data spaghetti”， 即数据意大利面问题，意指复杂的链路像缠绕的意大利面一样无法理顺。

![Unified Namespace](https://assets.emqx.com/images/bf5d1a5ec1731d08ca519aa798be5b6a.png)

而通过将 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 作为中间枢纽，协助信息交流，统一命名空间就能够以更高效的方式传输数据。这是我们需要用 MQTT 来搭建统一命名空间的主要原因之一。

### MQTT 保证数据安全

在统一命名空间的背景下，PLC 不需要应对来自未知来源的轮询请求。它只需要建立一个到可信 Broker 的持久连接，并且这个 Broker 是所有设备与之通信的唯一数据中心。如此只需要保证这一个 Broker 的数据安全问题即可保证整个系统的安全。

MQTT Broker 不仅实现了工业物联网 4.0 输入和输出的解耦，还负责保障分散的设备和系统连接的安全性。借助 MQTT 强大的安全功能，它完全有能力充当生产线的隔离数据中心，以防止异常数据进入敏感的 PLC。这样，统一命名空间可以将安全问题交由 Broker，并在一个集中的位置进行管理。

### MQTT 支持事件驱动架构

对于工业物联网 4.0，数据主要是由设备生成的，而不是人类。而且大部分时候，PLC 的读数并没有变化，没必要把重复的数据传送到统一命名空间，造成网络资源浪费。

但是，一旦寄存器的值变化了，就必须马上上报给 ERP/MES 或云端，以尽可能地利用信息的价值，因为信息的流动性和边际价值会随着时间的推移而降低。这就是所谓的“有异则报”。

![Event-Driven Architecture](https://assets.emqx.com/images/f32b6b5a3705f2250b52882f1d533909.png)

因此，事件驱动技术，比如 MQTT，对于建立统一命名空间是非常重要的。MQTT Broker 可以感知客户端状态的变化。这种感知是通过 SparkPlugB 和 MQTT 遗嘱消息功能实现的。有了遗嘱消息和 SparkPlugB，MQTT 只传送变化的数据，并保证不会把过期的数据发送给订阅的客户端。

## 将 MQTT 主题作为统一命名空间的元数据

统一命名空间是物理世界中业务的数字反映。物理世界处于主导地位，驱动数字世界，而不是相反。我们需要生成数据的详细上下文，才能将其转换为信息，例如站点的位置、PLC 属于哪条线路和哪个单元。幸运的是，MQTT 的发布/订阅消息传输模型为将 PLC 的上下文映射到数字世界提供了一种简便的方法。

使用 MQTT 的统一命名空间让用户能够浏览所有的命名空间和功能。并且了解每个数据标签的实时状态。

MQTT 主题的定义如下：

**namespace/group_id/message_type/edge_node_id/[device_id]**

![MQTT topic](https://assets.emqx.com/images/402d188d0059c04cfcd6faf4b79ab849.png)

<center>图源 OSISoft AF</center>

<br>

[MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)的组织方式类似于文件夹结构，按照层次结构排列。我们可以把每一层次的命名空间看作是一个主题，这样就可以在 MQTT 中创建一个树形结构的视图。

当订阅者从主题**“Enterprise A/Site A/Area A/Process Cell A/Bio Reactor**”获取数据时，它能够自动识别数据的来源，并根据实际情况做出相应的处理。同时，它们还可以使用通配符同时订阅多个数据点。

![MQTT topics and metadata](https://assets.emqx.com/images/385a249a15ea3470675cf71d71872271.png)

MQTT 可以帮助您定义元数据，保证不同系统在统一命名空间中的数据一致性和语义准确性。

## OPC UA：构建统一命名空间的 MQTT 替代方案

确切地说，MQTT 是构建统一命名空间的最佳选择，但并非唯一选择。您也可以使用其他协议来构建统一命名空间，例如 OPC UA 和 HTTP，或者纯粹的 Modbus + TCP/UDP。在众多协议中，OPC UA 由于其强大的商业支持和标准的悠久历史，其仍然是工业物联网的热门选项。

> 有关它们之间的详细比较可参考以下文章：
>
> [工业物联网协议比较：MQTT Sparkplug vs OPC-UA](https://www.emqx.com/zh/blog/a-comparison-of-iiot-protocols-mqtt-sparkplug-vs-opc-ua)
>
> [OPC-UA、Modbus、MQTT、Sparkplug、HTTP 工业通信效率对比](https://www.emqx.com/zh/blog/efficiency-comparison-opc-ua-modbus-mqtt-sparkplug-http)

不过，这并不是非此即彼的情况，更好的方法是通过[将它们桥接在一起](https://www.emqx.com/zh/blog/bridging-opc-ua-data-to-mqtt-for-iiot)，或者[使用 OPC UA over MQTT 的方式实现 ](https://www.emqx.com/zh/blog/opc-ua-over-mqtt-the-future-of-it-and-ot-convergence)，来结合双方的优势。

## 使用 MQTT 构建统一命名空间的总体架构

从理论上说，统一命名空间是能够统一业务中所有命名空间的全局命名空间。每个工厂、每个站点、每个 PLC 都是一个独立的命名空间。

![Architecture of Building UNS with MQTT](https://assets.emqx.com/images/b9dade93ea0b5ed12476809c1705465a.png)

统一命名空间的目标是将技术应用到整个业务，并对这些技术加以组织，以便于管理。这样就可以在其基础上构建出更多的解决方案。MQTT 的关键作用是连接 OT、CT 和 IT 世界中的各种零散技术，并将它们无缝地集成在一起。

## 结语

在本文中，我们探讨了 MQTT 在统一命名空间中的作用，以及 MQTT 为什么是所有 IT 系统的数据驱动力。在统一命名空间中使用 MQTT，可以带来诸多益处，可以彻底改变我们在数字世界中的连接和沟通方式。企业可以优化它们的数据流程，打造更快速更互联的系统，并为创新和发展带来新的机遇。

在下篇文章中，我们将详细介绍 EMQ 在 MQTT 领域对统一命名空间所做的创新贡献。



<section class="promotion">
    <div>
        联系 EMQ 工业领域解决方案专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
