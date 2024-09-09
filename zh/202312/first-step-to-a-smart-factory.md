如[之前的文章](https://www.emqx.com/zh/blog/a-digital-transformation-journey-to-smart-manufacturing)所述，获取和利用运营技术（OT）和信息技术（IT）来源的数据已经成为当务之急。IT 和 OT 的融合是工业 4.0 革命的核心驱动力，它能让企业基于数据做出决策，优化流程，提高效率。要实现 IT 和 OT 的融合，有两个关键点。

1. 打通 IT 和 OT 之间的隔阂，实现数据互通。
2. 识别来自不同系统的数据源。

在本文中，我们将探讨稳定可靠的 MQTT Broker [EMQX](https://www.emqx.com/zh/products/emqx) 和强大的工业协议网关 [Neuron](https://github.com/emqx/neuron) 在无缝获取和集成 OT 和 IT 数据源方面的重要作用。

## 应对 OT-IT 融合的挑战

在传统工业环境中，OT 和 IT 通常是各自为政的。OT 系统（包括传感器、PLC、SCADA 系统等）负责控制和监测工厂车间的物理过程。而 IT 系统则负责处理企业级数据，包括库存、客户信息和业务分析。

[智能制造](https://www.emqx.com/zh/blog/the-smart-manufacturing-revolution)的真正潜力在于将这两个领域融合起来。从 OT 设备获取实时数据并将其与 IT 系统集成，可以让制造企业更深入地了解生产过程，实时监测设备运行状况，并实施预测性维护策略。这种融合还能够改善供应链管理，提高产品质量控制和决策水平。

### EMQX: 强大的 MQTT Broker

EMQX 是 OT-IT 融合的核心，它是一个高度灵活的 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)。[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种轻量级的消息传输协议，专为低带宽、高延迟或不可靠的网络中的设备间通信而设计，非常适合在经常面临挑战的 OT 环境中使用。

![EMQX: The MQTT Broker Powerhouse](https://assets.emqx.com/images/054425d2d4deee6846b338accf21ae4a.png)

作为数据交换的中心枢纽，EMQX 能够轻松连接各种 IT 系统，包括 Kafka、Pulsar 等流式分析平台，以及 Oracle、PostgreSQL、Cassandra 等数据存储系统，甚至 SAP 等工业系统。它高效地管理 MQTT 通信，确保从这些数据源传送的数据可靠地到达其他 IT 系统，以进行分析、决策或数据存储。此外，EMQX 还具有高度的可扩展性，能够处理来自众多 IT 系统的海量数据，使其成为大规模工业运营的理想选择。

### Neuron：工业连接网关

EMQX 能够通过 Neuron 进一步增强其功能，Neuron 是一个强大的工业互联网连接网关，作为 OT 和 IT 世界之间的桥梁，实现了数据协议和格式的无缝转换，确保了兼容性。Neuron 支持包括 [Modbus](https://www.emqx.com/zh/blog/modbus-protocol-the-grandfather-of-iot-communication)、[OPC UA](https://www.emqx.com/zh/blog/opc-ua-over-mqtt-the-future-of-it-and-ot-convergence) 和 Ethernet/IP 等在内的多种工业通信协议，能够将它们转换为基于 MQTT 的协议，例如 [MQTT Sparkplug](https://www.emqx.com/zh/blog/mqtt-sparkplug-bridging-it-and-ot-in-industry-4-0) 和 [OPC UA over MQTT](https://www.emqx.com/zh/blog/opc-ua-over-mqtt-the-future-of-it-and-ot-convergence)。这使得 Neuron 能够适配各种 OT 设备，如 PLC、传感器和执行器等，并与 IT 系统进行连接。

![Neuron: The Industrial Connectivity Gateway](https://assets.emqx.com/images/b57fde2a3772cf0354962f7ee66403be.png)

通过与边缘流处理引擎 [eKuiper](https://ekuiper.org/zh) 集成，Neuron 可以在边缘对数据进行预处理。这意味着它可以在数据发送到 IT 系统之前对其进行过滤、聚合或转换。这种能力显著降低了 IT 资源的压力，并确保只有有用和处理过的数据才能到达企业系统。此外，Neuron 和 eKuiper 的集成版本 NeuronEX 支持边缘计算，使 AI 和机器学习算法能够在边缘运行，实现实时决策和预测分析。

### EMQX 与 Neuron 的结合

EMQX 和 Neuron 的协同效应体现在它们能够从 OT 源获取、转换数据并高效地将其传递到 IT 系统，实现 IT 和 OT 的融合。这一强大的组合为制造商提供了实时的洞察力、有价值的数据和适应多变的生产环境的灵活性。

![EMQX & Neuron](https://assets.emqx.com/images/2d49c5e8df480a4bebc7c88134acf2bb.png)

借助 EMQX 和 Neuron，从 OT 和 IT 源获取和利用数据将变得更加容易。对于那些想要在不断变化的工业环境中保持竞争力的公司来说，EMQX 和 Neuron 是发挥智能制造潜能的必备工具。通过无缝地获取和整合 OT 和 IT 数据源，企业可以采用预测性维护策略，优化生产流程和提升运营效率。这不仅减少了停机时间和维护成本，而且提高了产品质量、供应链管理和最终的盈利。

## 智能工厂中的数据源识别

正确识别数据源可以帮助您获得运营洞察、提升效率和实现数据驱动的决策。在下图中，我们展示了制造企业的工业系统中常见的网络拓扑结构，以及各个组件如何互联。EMQX 将作为这些系统进行消息交换的核心。Neuron 支持这些 OT 设备和传感器以 MQTT 格式实时上报数据。

![Identifying the Data Sources in a Smart Factory](https://assets.emqx.com/images/e87900711e70ea2a3d47ccf0fe36dd3e.png)

下面，我们来看看在智能工厂中如何识别数据源，以及在哪里获取这些有价值的信息。

### 1. 传感器和物联网设备：数字神经系统

智能工厂的核心是由传感器和设备组成的复杂网络。这些数字感知器被有策略地部署在工厂各处，监测温度、湿度、压力、振动等多种变量。它们构成了工厂的数字神经系统，持续地收集设备状态、环境条件和产品质量的实时数据。我们使用 Neuron 来采集这些数据，并在收到指令时控制设备。

传感器和设备是重要的数据源，提供了用于过程优化、预测性维护和质量控制的原始数据。它们提供了运营的微观视角，使工厂经理能够定位低效问题并识别改进的方向。

### 2. PLC 和 SCADA 系统：制造业的“乐队指挥”

可编程逻辑控制器（PLC）和数据采集与监视控制系统（SCADA）是负责着制造业的系统编排。PLC 控制工厂中的机器和设备，而 SCADA 系统监控和管理整个生产过程。Neuron 有大量的 PLC 驱动程序，可以访问 PLC 数据。Neuron 也可以使用 OPC UA、MQTT 和 API 等标准协议，来连接 SCADA 系统。

PLC 和 SCADA 系统作为数据源，收集和传输设备性能、生产速率和过程参数的数据。它们能够提供制造业运营效率的宝贵洞察，反映制造业运营的效率，支持实时决策和过程优化。

### 3. 历史数据库：归档过去以洞察未来

历史数据库是专门用于存储历史数据的数据仓库。它们是智能工厂的重要数据源，因为它们能够记录和保存来自传感器、PLC 和其他来源的数据变化。这些历史数据成为分析趋势、发现异常和做出明智决策的宝贵资源。EMQX 提供了多种连接器，用于将数据导入到不同的数据存储或历史数据库中。

历史数据库在回溯分析中发挥着作用，让制造商能够从过去的表现中汲取经验并持续改进流程。它们在合规和报告方面也扮演着关键角色，保证工厂符合行业规范和标准。

### 4. 企业系统：连接商业洞察的桥梁

智能工厂不只局限于车间，它们也在向企业系统拓展。企业资源规划（ERP）、客户关系管理（CRM）和供应链管理（SCM）系统是提供商业运营洞察的重要数据来源。利用标准的通信协议，如 MQTT Sparkplug 或 OPCUA over MQTT，这些企业系统可以互相沟通，甚至通过 EMQX Broker 直接与机器和设备对话。

企业系统的数据涵盖了订单信息、库存水平、客户偏好和销售数据。这些数据有助于让制造流程与商业目标保持一致，实现灵活的生产计划、需求预测和库存管理。

### 5. 云计算：在云平台上处理数据

AWS、Azure 和 Google Cloud 等云计算平台提供了丰富的服务和工具，用于管理和分析来自各种来源的数据，是智能制造不可或缺的一部分。云为现代制造设施中的数据驱动决策提供了可扩展性、可靠性和可访问性。EMQX 作为一个中间件层，实现了工厂地面系统和设备与云平台的连接，保证了通信的安全、高效和可扩展。

来自维护记录和预测分析模型的数据可用于预测设备故障和安排维护。云是部署这些分析模型的理想平台。

## 结语

准确识别数据源是迈向数据驱动的智能工厂的第一步。传感器、PLC、SCADA 系统、历史数据库、企业系统和边缘计算设备共同构成了支撑智能制造的数据生态系统。通过利用 EMQX 和 Neuron 接入这些数据源，工厂可以优化流程、减少停机时间、提升质量，在不断发展的工业 4.0 时代中保持洞察力和敏捷性。





<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
