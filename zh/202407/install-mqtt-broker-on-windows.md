## 引言

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种轻量级、基于发布/订阅模式的消息传输协议，旨在用极小的代码空间和网络带宽为物联网设备提供简单、可靠的消息传递服务。MQTT 经过多年的发展，如今已被广泛应用于资源开采、工业制造、移动通信、智能汽车等各行各业，使得 MQTT 成为了物联网传输协议的事实标准。

出于稳定性、可靠性、成本等多方面的考虑，众多 MQTT 服务实现更倾向于选择拥有丰富开源生态系统的 Linux 环境，Windows 平台上可选的 MQTT 服务相对有限。NanoMQ 是用于物联网边缘的超轻量级 MQTT 消息服务器，具有极高的性能性价比，适用于各类边缘计算平台。NanoMQ 有着强大的跨平台和可兼容能力，不仅可以用于以 Linux 为基础的各类平台，也为 Windows 平台提供了 MQTT 服务的新选择。

本文将以 NanoMQ 为例，使用二进制包和源代码编译两种方式演示如何在 Windows 平台中快速搭建 MQTT 服务。

## NanoMQ 简介

[NanoMQ](https://github.com/nanomq/nanomq) 是 EMQ 于 2021 年发布的开源项目，旨在为物联网边缘场景提供轻量级、快速、支持多线程的 MQTT 消息服务器和消息总线。NanoMQ 基于 NNG 的异步 I/O 构建，内置 Actor 多线程模型。相较于 Mosquitto 的单线程设计，NanoMQ 能够充分发挥现代 SMP 系统的多核优势，在边缘多核环境中展现出了比 Mosquitto 高达 10 倍的性能表现。NanoMQ 基于标准 POSIX 接口开发，可以轻松通过 MinGW 的 POSIX 编译环境移植到各类 Windows 环境中。经过三年研发迭代，NanoMQ 于 2024 年 1 月正式加入 LF Edge 基金会，未来将与 LF Edge 旗下的 EdgeX Foundry 框架深度集成，共同促进物联网边缘设备和应用之间的互操作性。

![NanoMQ](https://assets.emqx.com/images/6e38ec07d1c4d717bbaaeeffdeaa7866.png)

NanoMQ 主要具有以下特性：

- **超轻量化**：安装包约 200KB 左右，运行占用资源极小。根据编译和启动的配置，启动所需内存资源从300Kb 到 3Mb 不等。
- **兼容性和可移植性**：NanoMQ 采用纯净的 C/C++ 开发，只依赖于标准 POSIX API，同时支持大小端兼容，可无缝对接各类网络应用，零成本迁移到各类嵌入式平台。
- **可伸缩性**：借助内置的异步 IO 架构和多线程模型，NanoMQ 在保持轻量化的同时仍具备一定可横向拓展的并发吞吐能力。仅需不到 10MB 的内存消耗，即可支持超过 10W 的消息吞吐。
- **SMP 支持**：NanoMQ 在边缘多核平台上对 SMP 有着良好的支持，能够充分发挥多处理器的能力，从而提升系统性能。
- **容器支持**：NanoMQ 能够轻松地通过容器进行部署和运行，并且与主流的边缘容器编排方案兼容，使得部署过程更加灵活和便捷。

## 二进制包安装

首先进入 NanoMQ 官网[下载页面](https://nanomq.io/zh/downloads)，选择 Windows 平台下载安装包：

 ![下载 NanoMQ](https://assets.emqx.com/images/f1e7353ce8855112f706c28e8d0b5cab.png)

可以在解压后文件夹中的`bin`目录下用 Windows 命令行使用 NanoMQ。将解压后的` C:\xxx\nanomq-0.21.10-windows-x86_64\bin` 目录添加到环境变量中，则可以在 Windows 命令行或者 PowerShell 中直接使用 NanoMQ。输入 `nanomq --help` 可以看到简要的使用说明。

![NanoMQ 命令](https://assets.emqx.com/images/c809e5d435db10295b7a940f77828298.png)

使用 `nanomq start --conf C:\nanomq\config\nanomq.conf` 启动 NanoMQ。其中` C:\nanomq\config\nanomq.conf` 为 NanoMQ 配置文件的地址，配置文件示例可以在解压后文件夹中的` config` 目录下找到。NanoMQ 的详细配置说明请参见[官方文档](https://nanomq.io/docs/zh/latest/config-description/introduction.html)。

接下来使用 NanoMQ 的 MQTT 客户端工具 `nanomq_cli` 来进行 NanoMQ 的使用说明。`nanomq_cli` 同样可以在 `bin` 目录下找到。

![nanomq_cli](https://assets.emqx.com/images/0aac3562ec1e83fe0e5f87d2b5dabfbe.png)

从上图中可以看到 `nanomq_cli` 的通过 `sub` 命令订阅了主题 `nmqtest`，接收到了 `nanomq_cli` 通过 `pub` 命令发布的 `HelloWorld` 消息。

## 源码编译与运行

在 Windows 平台编译需要提前准备 [MinGW-w64](https://www.mingw-w64.org/)、[Make](https://gnuwin32.sourceforge.net/packages/make.htm) 和 [CMake](https://cmake.org/)。

- **MinGW-w64** 是将 GCC 编译器和 GNU Binutils 移植到 Windows 平台下的产物，包括一系列头文件（Win32API）、库和可执行文件，是一个在 Windows 平台上开发和运行原生 Windows 应用程序的开源软件开发环境。Cygwin 同 MinGW 类似，也用于移植 Unix 软件到 Windows，但它们采用截然不同的实现。Cygwin 重视兼容性优先于性能，MinGW 则着重于简化与性能。本文将以 MinGW 为例进行 NanoMQ 的编译。
- **Make 和 CMake** 则是用于 NanoMQ 项目自动化构建的工具。参考下载地址：[MingGW-w64](https://www.mingw-w64.org/downloads/#mingw-builds)，[Make](https://sourceforge.net/projects/gnuwin32/files/make/3.81/make-3.81.exe/download?use_mirror=jaist&download=)，[CMake](https://cmake.org/download/)。其中 MinGW-w64 应尽量选择较新版本。

接下来在 Windows 命令行、PowerShell 或者 Git Bash 中输入以下命令：

```
# 1. clone 源码 （已通过ZIP下载源代码则不需要这一步）
PS: D:\Project> git clone https://github.com/nanomq/nanomq.git
PS: D:\Project> cd nanomq

# 2. 更新和初始化 git 子模块
PS: D:\Project\nanomq> git submodule update --init --recursive

# 3. 创建并进入 build 目录
PS: D:\Project\nanomq> mkdir build
PS: D:\Project\nanomq> cd build

# 4. 编译 NanoMQ
PS: D:\Project\nanomq\build> cmake -G "MinGW Makefiles" ..
PS: D:\Project\nanomq\build> make -j 8

# 5. 运行 NanoMQ
PS: D:\Project\nanomq\build> .\nanomq\nanomq.exe broker start
```

除了 NanoMQ 自带的客户端工具，还可以使用开源 MQTT 客户端工具 [MQTTX](https://mqttx.app/zh) 来进行消息收发测试。

![MQTTX](https://assets.emqx.com/images/592ff1bd8178f5c1ab9b89ce6fe3de9c.png)

从上图中同样可以看到，订阅了 `nmqtest` 主题的客户端通过 NanoMQ 收到了另一个客户端发布的 `hello` 消息。

## 结语

本文通过二进制包和源码编译的方式完成了 NanoMQ 在 Windows 平台的安装，并对其使用进行了演示测试。NanoMQ 为在 Windows 平台上构建物联网边缘计算应用提供了一个便捷而强大的选择。它的轻量级、高性能以及专注于边缘计算的设计使其成为一个理想的消息传输解决方案。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
