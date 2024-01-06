## 什么是 TwinCAT

TwinCAT（The Windows Control and Automation Technology）是由德国倍福自动化有限公司（Beckhoff Automation）开发的用于自动化技术的软件平台。它被用于编程和控制各种类型的工业自动化设备，例如可编程逻辑控制器（PLC）、运动控制系统、人机界面（HMI）等。

TwinCAT 具有模块化和可扩展的特点，使其可用于广泛的应用和行业。它支持多种编程语言，包括结构化文本（ST）、梯形图（LD）、功能块图（FBD）、顺序功能图（SFC）和 C/C ++。

## TwinCAT 发展历程

TwinCAT 作为一套工业自动化的纯软件解决方案由 Beckhoff Automation 于 1995 年首次推出。TwinCAT 的原始版本被设计为在标准 Windows PC 上运行，它使用 Windows NT 专有的实时扩展来实现确定性控制。

多年来，TwinCAT 不断发展并扩展出了广泛的自动化功能，包括对更多的编程语言的支持以及集成运动控制、CNC 功能和对实时以太网协议的支持等附加功能。

2011 年，Beckhoff 推出了重大改进版本 TwinCAT 3。TwinCAT 3 基于新的软件架构，该架构的设计更加模块化和可扩展，使其具有更广泛的应用。TwinCAT 3 还增加了对分布式控制系统、多核处理器和高级运动控制等高级功能的支持。一个重要的功能是与 Microsoft Visual Studio 的集成，它允许用户利用丰富的开发工具集。TwinCAT 3 运行时可用于 64 位操作系统，并且优化了对处理器的多核特性的利用。

## TwinCAT 架构

TwinCAT 平台采用模块化架构，它由多个不同的软件产品组成，可以一起使用以创建完整的自动化解决方案。基本系统由开发组件（engineering）和运行时组件（runtime）组成，可以通过应用特定的功能组件（Functions）进行灵活扩展。总体而言，模块化架构为工业自动化提供了灵活和可扩展的平台，允许用户根据其特定的需求和要求定制系统。

![TwinCAT Architecture](https://assets.emqx.com/images/dab48e1ca10e88daa809e2cca20450fd.png)

#### 开发组件

TwinCAT XAE（eXtended Automation Engineering）是基于 Microsoft Visual Studio 的 TwinCAT 3 开发环境。它提供了一套全面的工具，用于创建、调试和部署自动化程序，包括对多种编程语言的支持。

#### 运行时组件

TwinCAT XAR（eXtended Automation Runtime）是 TwinCAT 3 系统的核心，负责执行 PLC 程序、协调运动控制以及处理与自动化系统中其他设备的通信。运行时组件可以在从小型嵌入式系统到大型工业 PC 等各种硬件平台上运行。

#### 功能组件

TwinCAT 功能组件为基本系统提供了广泛的扩展选项。例如，TwinCAT 3 HMI 可以基于 Web 技术（HTML5、JavaScript/TypeScript）开发与平台无关的用户界面，TwinCAT 3 Vision 提供可扩展的图像处理功能，而TwinCAT 3 Measurement 则提供附加的测量技术功能。

## ADS 协议

ADS (Automation Device Specification) 协议是 TwinCAT 系统中的传输层。它是为了在自动化系统中不同组件之间进行数据交换而开发的，例如 PLC、HMI 和其他设备。ADS 协议提供了高效的数据传输方式，支持实时、异步和通知式数据传输模式，使得 TwinCAT 系统中的各个组件可以彼此通信并协同工作。

![Structure of the ADS communication](https://assets.emqx.com/images/827c80b382efe2953d22ad7d7347ba4d.png)

<center>ADS 通信结构</center>

<p>

ADS 协议在运行于 TCP/IP 或 UDP/IP 协议之上，其 TCP 端口号为 48898 。

ADS 使用客户端-服务器模型进行通信，其中一个设备（客户端）向另一个设备（服务器）发送请求并接收响应。请求和响应可以包括数据、命令或状态信息。这种通信模型可用于在 TwinCAT 系统中的不同组件之间进行通信，包括 PLC、HMI 和其他设备。

![image.png](https://assets.emqx.com/images/8f9f320789aa3a7ccc4d77c34ab35bf7.png)

<center>ADS 报文结构</center>

<p>

ADS 协议提供了一组[命令](https://infosys.beckhoff.com/english.php?content=../content/1033/tcadscommon/12440300683.html&id=)，用于服务器和客户端之间的通信，其中最重要的是 [ADS Read](https://infosys.beckhoff.com/english.php?content=../content/1033/tcadscommon/12440300683.html&id=) 和[ADS Write](https://infosys.beckhoff.com/content/1033/tcadscommon/12440291467.html) 命令。

## TwinCAT 桥接到 MQTT

随着工业 4.0 的到来，制造业中的智能化、自动化和数据化需求越来越高。在这种背景下，MQTT 协议相较 ADS 协议有许多优势。

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种为物联网设备和应用程序设计的消息协议，采用发布与订阅模型，具有轻量、高效、可靠的，支持实时通讯等优点。 MQTT 非常适合资源受限的环境，特别是需要高效使用电力和带宽的场景。目前已经广泛应用于物联网、移动互联网、智能硬件、车联网、智慧城市、远程医疗、电力、石油与能源等领域。

此外，MQTT 是一种开放标准协议，有许多开源实现，相比于 ADS 协议可以运行在更多不同的平台上。

## 结语

在本文中，我们讨论了 TwinCAT 协议及其在工业场景中的重要作用，还解释了为什么需要将 TwinCAT 数据桥接到 MQTT 以提高这些场景的效率。有关如何桥接这两个协议的详细指南，请参考：[工业物联网数据桥接教程：TwinCAT 桥接到 MQTT](https://www.emqx.com/zh/blog/bridging-twincat-data-to-mqtt) 



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
