在快速发展的物联网 (IoT) 时代，[MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)已成为众多公司和开发者工作中不可或缺的组成部分。MQTT 客户端工具的使用已变得非常普遍，方便地实现了与 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 的无缝连接，执行诸如发布、订阅和消息交换等多种功能。

对于希望深入了解 MQTT 特性并简化物联网应用调试过程的开发人员而言，选择合适的工具至关重要，有助于缩短开发周期。然而市面上众多 MQTT 客户端工具各自有着不同的功能重点，这使得开发人员在决定最合适的选项时面临挑战。

本文整理了 2024 年七款最有价值的 MQTT 客户端工具。该选型分为桌面端、浏览器端、命令行和移动端四个类别，旨在帮助您快速识别适合您 MQTT 开发工作的理想工具。


## 如何选择一个 MQTT 客户端？

MQTT 客户端工具常用于建立与 [MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 的连接，进行主题订阅、消息收发等操作。一个优秀的 MQTT 客户端工具应该具备如下特性：

- 支持加密连接；
- 支持 [MQTT 5](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 特性；
- 在功能全面的基础上保持易用性；
- 支持多个客户端同时在线；
- 跨平台，不同操作系统下都可以使用；
- 支持 MQTT over WebSocket；
- 进阶功能：支持自定义脚本、日志记录、 MQTT Payload 格式转换等。

## **前提条件：准备一个 MQTT Broker**

在深入了解 MQTT 工具之前，我们需要一个 MQTT Broker 来进行通信和测试。我们选择在 `broker.emqx.io`  上提供的免费公共 MQTT Broker。

**MQTT Broker 信息**

>服务器：`broker.emqx.io`
>
>TCP 端口：1883
>
>WebSocket 端口：8083
>
>SSL/TLS 端口：8883
>
>安全 WebSocket 端口：8084

更多相关信息，请查看：[免费的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 

## MQTT 桌面客户端

### MQTTX

[MQTTX](https://mqttx.app/zh) 是 EMQ 开源的一款跨平台 MQTT 5.0 客户端工具，它支持 macOS, Linux, Windows，并且支持 MQTT 消息格式转换。

MQTTX 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建连接保存并同时建立多个连接客户端，方便用户快速测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的 **连接/发布/订阅** 功能及其他特性。

MQTTX 致力于打造优雅、易用的全平台 MQTT 客户端，并在最近发布了 MQTTX CLI 及  MQTTX Web 两个版本，目前在 GitHub Star 数已达到 2K，已成为使用场景最完整的 MQTT 测试客户端。

![MQTTX](https://assets.emqx.com/images/ada10fb84b685af3cadcae6c95197c4f.gif)

#### 特性

- 跨平台，支持 Windows，macOS 和 Linux
- 支持 MQTT 3.1.1、3.1 以及 5.0 协议
- 单/双向 SSL 认证：支持 CA、自签名证书，以及单、双向 SSL 认证
- 支持 Light、Dark、Night 三种主题模式切换
- 支持 WebSocket 连接至 MQTT 服务器
- 支持 Hex, Base64, JSON, Plaintext
- 支持简体中文、英文、日文、土耳其文及匈牙利文
- 订阅 Topic 支持自定义颜色标记
- 支持 $SYS 主题自动订阅，查看流量统计
- 自定义编辑脚本测试和模拟收发数据
- AI 驱动的 MQTTX Copilot：简化 MQTT 测试与开发
- 完整的日志记录

#### 下载

- 官网下载：[https://mqttx.app/zh](https://mqttx.app/zh)
- GitHub 下载：[https://github.com/emqx/MQTTX/releases](https://github.com/emqx/MQTTX/releases)

### MQTT Explorer

MQTT Explorer 是一个全面的 MQTT 客户端，它的一大亮点是提供了 MQTT 主题的结构化展示及动态预览。

MQTT Explorer 还支持对接收到的 payload 消息进行差异对比及可视化图表展示。与 MQTT.fx 相似，MQTT Explorer 只能创建一个单一的客户端连接，不能多个客户端同时在线。

![MQTT Explorer](https://assets.emqx.com/images/7be0606fdbb16f93359429dba0cc3e6e.png?imageMogr2/thumbnail/1520x)

#### 特性

- 可视化 Topics 和 Topic 变化的动态预览
- 删除保留的 Topics
- 搜索/过滤 Topics
- 递归删除 Topics
- 当前和以前收到的消息的差异视图
- 发布 Toipcs
- 绘制数字 Topics
- 保留每个 Topic 的历史记录
- Dark/Light 主题

#### 下载

下载地址：[https://github.com/thomasnordquist/MQTT-Explorer/releases](https://github.com/thomasnordquist/MQTT-Explorer/releases)

### MQTT.fx

MQTT.fx 是由 Jens Deters 个人开发的，MQTT.fx 适用 Apache License 2.0 协议但并未提供源码。遗憾的是 MQTT.fx ⽬前已经停⽌维护，并转为由 Softblade 公司资助开发另发⾏了其商业版本 MQTT.fx® 5.0，采⽤收费许可证⽅式经营该软件。

MQTT.fx 使用 JavaFX 技术开发，可以保存多个连接配置，支持多种类型的加密方式，指定多种类型的证书，创建连接时可以指定使用 HTTP 代理服务器。

总的来说 MQTT.fx 有丰富且成熟的功能，支持了 TCP 连接中所有可能遇到的配置项，但是用户同一时间只能建立一个连接，不能满足同时使用多个测试连接的需求。另外它没有实现对 WebSocket 的支持，在 MQTT over WebSocket 的测试场景中无法使用。

![MQTT.fx](https://assets.emqx.com/images/4f592bb17cbbfe3adf0d13e07277c0dd.png?imageMogr2/thumbnail/1520x)

#### 特性

- 预定义消息模板
- 通过系统主题 `$SYS` 获取 broker 状态
- 记忆最近使用主题的
- 通过 Nashorn Engine ，支持 JavaScript 脚本
- 支持日志显示，显示连接中的日志信息
- 跨平台桌面，支持 Windows、MacOS 和 Linux

#### 下载

下载地址：[https://www.jensd.de/wordpress/?p=2746](https://www.jensd.de/wordpress/?p=2746)



## MQTT 在线客户端

### MQTTX Web

[MQTTX Web](https://mqttx.app/zh/web) 是一款开源的 MQTT 5.0 浏览器客户端，也是一个在线 [MQTT WebSocket](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket) 客户端工具。开发者无需在本地下载和安装 MQTTX，即可使用 WebSocket 在浏览器中快速连接到 MQTT 服务器，更快地开发和调试 MQTT 服务和应用。

![MQTTX Web](https://assets.emqx.com/images/2c99b9ae65c524993e522621cad154d2.png)

立即体验：[https://mqttx.app/web-client/](https://mqttx.app/web-client/)

更多详情，请查看 GitHub 仓库：[https://github.com/emqx/MQTTX/tree/main/web](https://github.com/emqx/MQTTX/tree/main/web)



## MQTT 命令行客户端

### MQTTX CLI

[MQTTX CLI](https://mqttx.app/zh/cli) 是一款全开源的、强大而易用的 MQTT 5.0 命令行客户端工具，也是命令行上的 MQTTX，旨在帮助开发者无需使用图形化界面，也能快速开发和调试 MQTT 服务与应用。

![MQTT CLI](https://assets.emqx.com/images/6e1009d394255edd48a9da76ae698a94.jpeg)

#### 特性

- **MQTT 协议支持：**完整支持 MQTT 3.1.1、3.1 以及 5.0
- **跨平台兼容**：支持 Windows、MacOS 和 Linux
- **无依赖限制**：基于命令行的安装和使用，无任何环境依赖要求
- **易于集成：**可快速集成到自动化测试脚本中
- **MQTT 基准测试**: 开箱即用的 MQTT 性能测试工具
- **配置文件**: 支持为 `连接`、`发布` 和 `订阅` 保存为本地配置文件
- **优雅的输出**: 输出对用户友好、易于理解的命令行内容，便于查看测试步骤及内容
- **多种安全认证**：支持 CA、自签名证书及单向和双向 SSL 认证
- **MQTT 消息模拟**：基于场景，支持自定义和内置选项

#### 下载

MQTTX CLI 可以快速下载并安装到 macOS、Linux 和 Windows 系统上，**安装前不需要任何的依赖环境准备**，只需在终端内执行命令，即可安装和使用 MQTTX CLI。

立即下载试用：[https://mqttx.app/zh/cli](https://mqttx.app/zh/cli)

#### 快速开始

订阅

```
mqttx sub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883
```

发布

```
mqttx pub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883 -m 'hello from MQTTX CLI!'
```

发布多条消息

```
mqttx pub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883 -s -M
```

MQTTX CLI 支持一个 `pub` 命令可以发布多条消息的功能，只需要在编辑是在命令中添加一个 `-M` 参数和 `-s` 参数，每次输入完成后换行即可。

性能测试

```
# Connect Benchmark
mqttx bench conn -c 5000
# Subscribe Benchmark
mqttx bench sub -c 5000 -t bench/%i
# Publish Benchmark
mqttx bench pub -c 5000 -t bench/%i
```

![MQTT CLI](https://assets.emqx.com/images/549a31f8b062f099c0eac8c0c6047f35.png)

### NanoMQ CLI

[NanoMQ](https://nanomq.io/zh) 是用于物联网边缘的超轻量级 MQTT 消息服务器，它同时也内置了一个强大的 MQTT 协议性能测试工具 `bench` 及 MQTT 测试客户端。

#### 特性

- 支持性能测试
- 支持 MQTT 5.0
- 可运行在边缘端
- 支持从文件读取数据作为 payload

#### 下载

下载地址：[https://nanomq.io/zh/downloads](https://nanomq.io/zh/downloads)

#### 快速开始

性能测试工具 bench

```
# 启动 10 个连接，每秒向主题 t 发送 100 条 Qos0 消息，其中每个消息负载的大小为 16 字节
nanomq_cli bench pub -t t -h broker.emqx.io -s 16 -q 0 -c 10 -I 10

# 启动 500 个连接，每个连接使用 Qos0 订阅 t 主题
nanomq_cli bench sub -t t -h broker.emqx.io -c 500

# 启动 100 个连接
nanomq_cli bench conn -h broker.emqx.io -c 100
```

MQTT 测试客户端

```
# 向主题 t 发送 100 条 Qos2 消息测试。
nanomq_cli pub -t t -h broker.emqx.io -q 2 -L 100 -m test

# 订阅主题 t
nanomq_cli sub -t t -h broker.emqx.io -q 1
```

### Mosquitto CLI

Mosquitto 是一个开源(EPL/EDL 许可证)的消息代理，安装之后默认提供了 mosquitto_pub 和 mosquitto_sub 两个命令行 MQTT 客户端工具。

Mosquitto CLI 有多个配置选项，支持 TLS 证书连接、通过代理服务器连接，支持 debug 模式，在 debug 模式下可以获取更详细的消息信息。

#### 特性

- 轻量级命令行工具，支持 debug 模式
- 支持加密及非加密连接至 MQTT 服务器
- 便于在远程服务器测试

#### 下载

下载地址：[https://github.com/eclipse/mosquitto](https://github.com/eclipse/mosquitto)

#### 快速开始

订阅

```
mosquitto_sub -t 'test/topic' -v
```

发布

```
mosquitto_pub -t 'test/topic' -m 'hello world'
```

## MQTT 移动客户端工具

### EasyMQTT

EasyMQTT 是一款适用于 iPhone、iPad 和 macOS 的 MQTT 客户端，让您可以与任何 MQTT Broker 进行交互。您可以使用它管理家庭中的设备设置，控制如 Zigbee2MQTT 的应用程序，或监控远程 Broker。该工具拥有简洁、用户友好的界面，并支持浅色和深色模式。

![EasyMQTT](https://assets.emqx.com/images/f9118dd8e7c71a668b3667b1c629a1d0.png)

#### 下载

下载地址：[‎https://apps.apple.com/us/app/easymqtt/id1523099606?platform=iphone](https://apps.apple.com/us/app/easymqtt/id1523099606?platform=iphone) 

## 结语

本文全面介绍了不同类别的 MQTT 客户端工具。其中，MQTTX 作为一个快速发展的客户端工具脱颖而出，以其现代化的聊天式界面、全面的 MQTT 5.0 支持和丰富的功能带来了卓越的用户体验。MQTTX 提供桌面版、命令行版和浏览器版三个版本，能够满足各种场景下的 MQTT 测试需求。毋庸置疑，MQTTX 已成为 2024 年最优秀的 MQTT 客户端工具之一。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div>全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient">开始试用 →</a>
</section>
