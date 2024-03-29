在[上一篇文章](https://www.emqx.com/zh/blog/exploring-isa95-standards-in-manufacturing)中，我们探讨了 ISA95 的概念以及它定义的各种数据和操作模型。本文将继续深入探索 ISA95 标准如何帮助制造商在信息技术（IT）和运营技术（OT）之间实现有效的衔接。此外，我们还将了解为什么[统一命名空间](https://www.emqx.com/zh/blog/unified-namespace-next-generation-data-fabric-for-iiot)(Unified Namespace)是一种更适合现代工业制造的解决方案。

## 自动化金字塔模型的数据流

在本系列的上一篇文章中，我们介绍了自动化金字塔(Automation Pyramid)，它用一种可视化的方式，显示了不同层级的自动化技术如何协同工作和通信，以实现工业流程的管理和控制。

![Automation Pyramid](https://assets.emqx.com/images/201ebdca20d9c3429d72dca978f93e6a.png)

如上图所示，自动化金字塔描述了信息如何从现场层向上流动到企业层，从而实现数据驱动的决策和流程优化。相反地，从企业层向现场层下发的指令和控制信号，会对工业流程的运行产生影响。

1. **现场层到控制层：**现场层的传感器和执行器采集有关物理流程的各种数据，例如温度、压力和流量等。这些数据被传送到控制层，由可编程逻辑控制器（PLC）和分布式控制系统（DCS）接收和处理。PLC 和 DCS 根据收到的数据运行控制算法，从而改变工厂中的机器和流程的运行状态。
2. **控制层到监控层：**控制层从负责工业流程不同环节的多个 PLC 和 DCS 单元收集数据。数据被发送到监控层，由监控和数据采集（SCADA）系统实时显示信息并将流程可视化。监控层的操作员可以向控制层下达命令，以调节流程的参数或执行某些操作。
3. **监控层到 MES 和企业层：**监控层的 SCADA 系统将有关流程的数据传输到制造执行系统（MES）以及更高级别的企业级系统。MES 层使用来自监控层的数据管理资源的分配、调度和生产活动。这些从多个自动化系统节点收集的数据将用于在企业层进行分析和决策。
4. **企业层到下层：**企业层包括了像企业资源规划（ERP）这样的业务系统，它们根据来自下层的数据做出高层次的决策，例如安排生产计划和规划资源。在企业层做出的决策会通过发送改变生产计划或资源分配的命令，对下层的操作产生影响。
5. **反馈回路：**在不同层之间建立有反馈回路，以保证在某个层次采取的行动能够对流程产生预期的影响。例如，如果在企业层设定了一个特定的生产目标，那么控制层就会调整相应的参数以实现该目标，并将结果反馈回来进行评估。

## 自动化金字塔中的数据管理挑战

工业物联网设备、边缘计算和云集成等现代技术，为自动化金字塔各层之间的互动带来了新的可能性。边缘设备可以在本地对数据进行预处理，并只把有用的信息发送到上层，从而减少延迟。云集成可以实现远程监测和深度分析。总体而言，随着技术的不断进步，不同层之间的互动变得更加复杂和灵活。这也导致自动化金字塔模型难以适应现代技术的需求，面临着以下一些挑战：

1. **数据孤岛：**在工业环境中通常包含多个系统，每个系统都会生成和存储自己的数据。这种情况导致了数据孤岛问题，也就是信息被困在自动化金字塔的特定层中，无法进行共享。数据孤岛现象影响了部门间的透明度和协作，使得获取全面的运营视图变得困难。
2. **缺乏标准化：**自动化金字塔的各个层级可能采用不同的数据格式、协议和通信方法。由于缺乏标准化，增加了数据在层与层之间集成和传输的难度，进而引发了兼容性问题和繁琐的手动干预需求。
3. **数据复杂性：**工业流程涵盖多种数据来源，包括传感器、可编程逻辑控制器（PLC）、监控和数据采集（SCADA）系统以及制造执行系统（MES），这些数据源生成了大量复杂的数据。随着系统的不断发展和数据量的增加，有效地管理和组织这种多样化的数据日益变得具有挑战性。
4. **可扩展性问题：**传统的数据组织和传输方法可能难以有效地应对现代工业流程中数据量的激增。随着数据量不断增加，现有的架构可能无法承受压力，从而导致性能瓶颈和数据处理延迟。
5. **实时性要求：**许多工业流程需要实时或准实时的数据分析和决策。在自动化金字塔的各个层级之间快速准确地收集、传输和处理数据变成了一个重大的挑战。
6. **集成复杂性：**把新的系统、技术或设备集成到现有的自动化架构中可能非常复杂和耗时。集成过程可能需要使用定制的连接器、中间件或接口，以保证数据在层与层之间顺畅地流动。
7. **数据安全和隐私：**工业环境是网络安全攻击的首要目标。在保证数据的完整性和保护敏感信息的同时，确保数据在自动化金字塔的各个层级之间安全地流动是一个巨大的挑战。
8. **遗留系统兼容性：**许多工业设施中还存在着一些使用过时的通信协议或技术的遗留系统。将这些遗留系统与现代的数据组织和传输方法整合起来可能非常困难。
9. **维护和支持：**随着时间的推移，传统的数据组织方法可能导致技术债务，使得系统的维护和支持变得更加复杂和消耗资源。这可能影响到系统的灵活性和采纳新技术的能力。

以上这些挑战会影响工业流程的效率、可扩展性和整体效果。

## 统一命名空间的优势

在工业领域，统一命名空间是一种标准化和一致化表示和组织各种系统、流程和组件数据的方法。其目的是确保以一种与底层系统或技术无关的方式命名、访问和管理数据。统一命名空间提供了一个桥梁，以弥合不同数据源、遗留系统和现代技术之间的差距，从而建立可以在组织内部轻松访问、共享和利用的统一数据视图。

![Unified Namespace](https://assets.emqx.com/images/fabbcf68bef153964108dfde023542d1.png)

## 使用统一命名空间替代自动化金字塔

在工业自动化中采用统一命名空间架构是一种革命性的解决方案，它有效地解决了传统自动化金字塔模型中固有的几个挑战。

首先，统一命名空间在促进无缝集成方面表现出色，与自动化金字塔相比，它有效地避免了数据孤岛和复杂的集成流程。通过提供标准化的数据表示和访问框架，它简化了自动化生态系统中不同层级之间的通信，从而提高了互操作性和数据交换的效率。

其次，这种方法通过为来自不同来源、协议和技术的数据提供统一的接口，显著提升了数据的可访问性。而自动化金字塔则将关键数据隐藏在分层系统中，使其难以用于决策和分析。

最后，统一命名空间展现了出色的可扩展性、灵活性和适应性，能够满足现代工业流程中快速增长的数据需求。它通过推广标准化实践和减少对定制连接器的需求，有效降低了技术债务。通过提供全局的数据视图，它赋予组织全面洞察力，促进了跨部门的协作，提升了工业领域的灵活性和创新性。

## 结语

虽然传统的自动化金字塔在理解工业控制系统方面仍然具有价值，但统一命名空间通过满足工业 4.0 和数字化转型的需求成为了更优于它的解决方案。随着行业的不断发展，采用统一命名空间使企业能够充分发挥数据的潜能，简化运营，推动创新，最终引领他们迈向更高效、更具竞争力的未来。

将 [EMQX](https://www.emqx.com/zh/products/emqx) 和 [Neuron](https://www.emqx.com/zh/products/neuronex) 集成到现有基础设施中，实现统一命名空间架构将变得非常简便。在接下来的文章中，我们将更深入地探讨这种集成，详细解释为何 EMQX 和 Neuron 是构建您组织内统一命名空间的理想组合。两者共同为统一命名空间提供了坚实的基础，能够轻松连接工业生态系统的各个层面，从而简化您的数据管理。



<section class="promotion">
    <div>
        联系 EMQ 工业领域解决方案专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
