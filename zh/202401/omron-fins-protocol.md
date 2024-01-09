## 什么是 FINS 协议

Omron FINS（ Factory Interface Network Service ）是 OMRON 为工业自动化控制开发的网络通信协议。它可以通过 FINS 命令实现以太网、控制网络和 RS232C / 485 串行通信之间的无缝通信。FINS 协议在 TCP / IP 模型的应用层上工作，这确保了其良好的可扩展性、实用性和实时性，从而通过 Omron FINS 以太网驱动器将客户端应用程序（包括 HMI、SCADA、Historian、MES、ERP 和无数自定义应用程序）与控制器连接起来。

FINS 协议有两个变种：FINS / UDP 协议使用 UDP 数据包进行通信，FINS / TCP 协议使用 TCP 连接。

### FINS 会话过程

FINS 会话过程基于 TCP / IP 协议。下图描述了 FINS 会话开始时几个数据帧的作用。FINS 协议的会话有一个请求帧，发起方的节点参数附加在请求帧上。服务器端（如 PLCS ）将确认并向请求者返回其节点参数。只有基于 TCP 的 FINS 需要会话进程。

![FINS 会话过程](https://assets.emqx.com/images/0d8af5289a27e88ab5a6f415cb8c3b34.png)

### FINS 数据帧结构

FINS 数据帧结构包含三个部分，分别是 FINS 头部、FINS 命令代码段以及 FINS 命令参数段。

![FINS 数据帧结构](https://assets.emqx.com/images/c7c31b73393dedb48c4cc1be9e0e1464.png)

命令帧和响应帧都由用于存储传输控制信息的 FINS 头部、用于存储命令的 FINS 命令字段和用于存储命令参数或传输/响应数据的 FINS 参数/数据字段组成。

![FINS 头部](https://assets.emqx.com/images/58272c4a564c4b6a36879a61c1270837.png)

命令的响应代码（ MRES 和 SRES 各一个字节）被添加到响应帧 FINS 参数/数据字段的开头。

![命令的响应代码](https://assets.emqx.com/images/4ad7fb747e362f0bc2cebf6fcdda12e2.png)

FINS/UDP 只包含两部分: FINS 命令代码段和 FINS 命令参数段。

## FINS 可读写 IO 存储区

下表给出了读取或写入可编程控制器数据时要使用的地址。

- 在对可编程控制器编程时，数据区地址列（ Data area address ）给出了正常的地址范围。
- 通讯使用地址列（ Address used in communications ）就是在 CV 模式命令和回复中使用的地址（ CV 模式命令就是 FINS 命令的别名）。这些地址与存储器区域代码结合起来，指定可编程控制器存储器的位置。它们与数据的实际内存地址不同。
- 字节数列（ No. of bytes ）指定该区域读或写数据的字节数。相同区域的字节数因内存区域代码而异。

不同的 PLC CPU 型号有不同的存储器区域。下面以 CV500 或 CVM1-CPU01-E 为例进行说明。

![FINS Read/Write IO Memory Area](https://assets.emqx.com/images/fb21a9091c3f037fb1b3d5d18e65c80e.png)

## FINS 命令列表

在下表中命令代码字段列（Command Code），每一个小格代表一个字节( 两个 16 进制数据)。表格列出了 CV 系列可编程控制器支持的 FINS 命令和在不同的可编程控制器模式下，哪些命令是可用的。

![FINS Command List](https://assets.emqx.com/images/28160d8d452c41d9c73bc7b1a4c411de.png)

> **注：**当可编程控制器处于 RUN 模式时，不能将数据从文件传输到程序区域，但可以从程序区域传输到文件。

## 为什么需要桥接 FINS 到 MQTT？

随着工业 4.0 浪潮的到来，工业领域对数据智能、互联互通和云边缘协作的需求不断增长。在这种背景下，FINS 协议可能会面临一些问题。

首先，作为一种内网应用协议，FINS 的设计并没有考虑到安全性，其通信方法很简单，容易受到黑客攻击和数据篡改，从而对生产环境构成威胁。此外，FINS 仅能在复杂的应用架构中进行一对一的通信，不能有效支持分布式和云原生应用的开发。

与 FINS 相比，MQTT 具有显著的优势。MQTT 是一种轻量级的发布-订阅消息传输协议，通常用于物联网应用程序中的远程监控和通信。它提供了一种简单灵活的方式在设备之间传输消息，同时有效处理大量并发连接。它目前用于物联网、移动互联网、智能硬件、网联汽车、智慧城市、远程医疗、电力、石油和能源等各个领域。

在物联网领域，MQTT 显然更适合分布式系统中的消息传输。因此，我们可以将 FINS 与 MQTT 结合，互为补充。

## 结语

本文介绍了 FINS 协议的相关基础知识。将 FINS 数据桥接到 MQTT 可以为工业场景带来更多好处，使其更加高效。有关 FINS 协议桥接到 MQTT 的详细教程，请参考：[工业物联网数据桥接教程：FINS 桥接到 MQTT](https://www.emqx.com/zh/blog/bridging-fins-data-to-mqtt) 



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
