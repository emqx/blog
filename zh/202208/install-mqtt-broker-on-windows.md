MQTT 已经是物联网事实上的标准通信协议。在目前市面上提供的各类开源 MQTT 服务器中，最常见的是 Linux 平台为基础，对于 Windows 平台的支持较少，即使支持也存在性能较弱、功能单一、版本兼容性等问题。

然而在工业自动化和建筑智能领域，有许多场景仍然依赖于 Windows 的生态环境。特别是工控上位机仍然大量使用 C# 开发运行在安装 Windows 的工控机中，有的成本敏感场景甚至还在使用 WinCE 操作系统。为了能让这些用户也能在 Windows 上使用到方便易用、轻量小巧、功能齐全的 MQTT 消息服务，超轻量级物联网边缘 [MQTT 消息服务器 NanoMQ](https://nanomq.io/zh) 依赖其强大的跨平台和可兼容能力，通过 MinGW 的 POSIX 编译环境成功移植到了各类 Windows 环境。

本文将以 NanoMQ 为例，演示如何通过安装包和源代码编译两种安装方式，在 Windows 系统中快速搭建一个可以支持多协议连接的物联网 MQTT 消息服务器。

## NanoMQ 简介

[NanoMQ](https://nanomq.io/zh) 是 EMQ 推出的面向物联网边缘计算场景的超轻量级高性能 **MQTT** 消息服务器+消息总线（Github 地址: [https://github.com/emqx/nanomq](https://github.com/emqx/nanomq)），具有超轻量、高吞吐、低延迟、兼容性高和可移植等优点，能够在各类操作系统和 CPU 架构上部署。

![NanoMQ 架构图](https://assets.emqx.com/images/bae685d3d50deac2f584b84c77d23595.png)
                                                       
目前 **NanoMQ** 具有的功能有：

- 完整支持**MQTT 3.1.1/5.0**。
- 嵌入式规则引擎，支持消息的实时处理和持久化。
- 支持云端桥接，并可以进行消息离线缓存和自动重传。
- 提供丰富的 HTTP REST APIs，方便云边协同和远程运维监控。
- 多协议支持 ：MQTT over WebSocket， ZeroMQ 和 nanomsg 等。
- 支持第三方 HTTP 认证和 WebHook 集成方式。

## 安装包安装

第一种方法我们将直接使用二进制安装包进行安装。

### 下载安装包

首先进入 NanoMQ 官网下载页面：[https://nanomq.io/zh/downloads](https://nanomq.io/zh/downloads)，并选择 Windows 平台下载安装包：

![下载 NanoMQ](https://assets.emqx.com/images/1c543cbc23cddcc54254628b096c0dce.png)

<center>从 NanoMQ 官网下载 Windows 发布包</center>

目前最新的 NanoMQ Windows Release 版本是 0.10.5。

### 安装包安装

下载会得到一个 msi 格式的安装包，双击进行安装。

![NanoMQ 安装包](https://assets.emqx.com/images/12f966985547af7ba79a27ff1bc2ce3b.png)

<center>下载的安装包</center>

选择安装路径和所需安装的功能，安装包也包含了 NanoSDK 的库文件：

![选择安装路径和所需安装的功能](https://assets.emqx.com/images/6792ade9bba8f1d2dc870f7e240038bb.png)

安装完成后程序自动退出。

### 测试和启动 NanoMQ 服务

目前 NanoMQ 还不包含可视化界面，所以需要通过命令行或者服务启动，启动方式如下：

打开命令行窗口或者 PowerShell，输入 nanomq 可以看到：

![MQTT CLI](https://assets.emqx.com/images/7963252c538f688a95eb3d3d04a7ee3a.png)

<center>检查命令是否能够正常使用</center>

说明系统已经成功安装了 NanoMQ，可以通过输入 --help 了解具体有哪些命令选项。

启动的话可以使用 `nanomq start --conf C:\nanomq\config\nanomq.conf` 配置文件指定的路径请根据第二步的安装选择的路径找到对应的配置文件，简单的配置选项有：

```
## url
## Connect with the host and port
## 监听的端口和IP地址
## Value: nmq-tcp://host:port
url=nmq-tcp://localhost:1883

## num_taskq_thread
## Use a specified number of taskq threads 
## 线程数，建议设置成和CPU核数相同
## Value: 1-255
num_taskq_thread=4

## max_taskq_thread
## Use a specified maximunm number of taskq threads
## 线程数，建议设置成和CPU核数相同
## Value: 1-255
max_taskq_thread=4

## msq_len
## The queue length in-flight window
## This is essential for performance and memory consumption
## 飞行窗口长度大小，影响broker最大内存占用
## Value: 1-infinity
msq_len=256
```

在 Windows 平台，监听的 URL 需要设置成 `nmq-tcp://localhost:1883` 。除了 nanomq.conf 配置文件外，其他功能的具体配置方法可以参考 [NanoMQ的文档页面](https://nanomq.io/docs/zh/latest/)。

测试 NanoMQ 服务是否正常运行，可以使用 NanoMQ 自带的客户端工具直接测试：

![MQTT 客户端工具](https://assets.emqx.com/images/b5baf4e537603e5bd3c7d9bf1e5a7e6e.png)

通过 NanoMQ 的 Pub/Sub 命令，可以看到已经可以正常收发消息，Sub 客户端可以收到 Pub 客户端发的 Hello 消息。

## 源码编译及运行

第二种方法是通过源代码进行编译安装，这种方法允许我们在 Windows 上对 NanoMQ 进行二次开发并增加自己需要的功能。

目前 NanoMQ 在 Windows 下的编译需要 [MinGW-w64](https://www.mingw-w64.org/downloads/#mingw-builds)、[Make](http://gnuwin32.sourceforge.net/packages/make.htm) 和 [CMake](https://cmake.org/download/)。

- **MinGW-w64** 下载地址: [https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/installer/mingw-w64-install.exe/download](https://sourceforge.net/projects/mingw-w64/files/Toolchains targetting Win32/Personal Builds/mingw-builds/installer/mingw-w64-install.exe/download)
- **Make** 下载地址：[https://sourceforge.net/projects/gnuwin32/files/make/3.81/make-3.81.exe/download?use_mirror=jaist&download=](https://sourceforge.net/projects/gnuwin32/files/make/3.81/make-3.81.exe/download?use_mirror=jaist&download=)
- **CMake** 下载地址: [https://cmake.org/download/](https://cmake.org/download/) 

### 源码准备

首先需要从 NanoMQ 源代码仓库下载源代码，注意 NanoMQ 内部包含一个子模块 NNG。

**NanoMQ** 源码仓库: [https://github.com/emqx/nanomq](https://github.com/emqx/nanomq)  

下载链接：[https://github.com/emqx/nanomq/archive/refs/heads/master.zip](https://github.com/emqx/nanomq/archive/refs/heads/master.zip)

NanoNNG 源码仓库：[https://github.com/nanomq/NanoNNG/tree/main](https://github.com/nanomq/NanoNNG/tree/main)  

下载链接：[https://github.com/nanomq/NanoNNG/archive/refs/heads/main.zip](https://github.com/nanomq/NanoNNG/archive/refs/heads/main.zip)

NNG 的源代码需要放置在 nanomq 的 nng 目录下，准备好源代码后就可以开始编译。

### 编译安装 NanoMQ

#### 命令行编译

> 以下命令在 Windows PowerShell 或 Git bash 中运行.

```
# 1. clone 源码 （已通过ZIP下载源代码则不需要这一步）
PS: D:\Project> git clone https://github.com/emqx/nanomq.git
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

#### Visual Studio Code 中编译

> 需提前安装 VS Code 的 C/C++ 和 CMake 相关插件

![C/C++](https://assets.emqx.com/images/41960bdb54a8eae23fba1917a6eb36cc.png)

![CMake Tools](https://assets.emqx.com/images/39d8e44d66499dc8913286fe0f7d599d.png)

![CMake Integration](https://assets.emqx.com/images/00e257e5ab1163ff3dc30c5f2d2c4c3f.png)

1. 点击选择编译工具链；

2. 选择 GCC 8.1.0 i686-w64-mingw32 （可能根据你所安装的 MinGW 版本不同而有所不同）；

3. 点击 build 开始编译 NanoMQ。

   ![编译 NanoMQ](https://assets.emqx.com/images/2c6a8081e9b9ad6036ce8b79417e7352.png)

### 运行测试

除了 NanoMQ 自带的客户端工具，还可以使用 [开源 MQTT 测试客户端工具 MQTT X](https://mqttx.app/zh) 来进行基础的消息收发测试。

MQTT X 下载地址：[https://www.emqx.com/zh/try?product=MQTTX](https://www.emqx.com/zh/try?product=MQTTX) 

![MQTT 测试客户端工具 MQTT X](https://assets.emqx.com/images/0788a29dbccc7d6f253fa6bc0914ffe2.png)

从 MQTTX 可以看到消息能够通过 NanoMQ 进行正常收发。

## 结语

至此，我们已经成功在 Windows 平台搭建了完整的 MQTT Broker，为广大 Windows 生态用户和其他无法使用 Linux 环境的场景提供了一个轻量且性能强大功能齐全的 MQTT 消息服务器。后续我们还将进一步介绍如何在 Windows 上使用 NanoMQ 的规则引擎和 WebHook 等更多高级功能。
