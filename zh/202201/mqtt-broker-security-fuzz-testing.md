物联网市场正在以爆炸式的增长势头飞速发展。随着设备规模的不断增长和业务逻辑的日渐复杂，物联网平台基础设施的安全性也愈发重要。物联网平台对协议的具体实现是否完整、对特定消息的解析过程是否安全就成了重中之重。

这需要面面俱到地针对协议中的繁杂标准和指定的行为规范进行较为完整的测试。同时，考虑到实际使用中可能存在的各种干扰和攻击，测试过程也需要覆盖各种非标准异常报文，以分析目标平台对异常情况的容错和处理能力。

模糊测试是一个非常有效的测试手段。本文将以 EMQ X 为例，介绍如何使用模糊测试工具来发现 MQTT 服务器/[MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)对协议实现上可能存在的缺陷和漏洞。

## 什么是模糊测试

模糊测试 （fuzz testing, fuzzing）是一种软件测试技术。其核心思想是将自动或半自动生成的随机数据输入到一个程序中，并监视程序异常，如崩溃、断言（assertion）失败，以发现可能的程序错误，比如内存泄漏。模糊测试常常用于检测软件或电脑系统的安全漏洞。

模糊测试可以被用作白盒、灰盒或黑盒测试。通常用于黑盒测试，回报率较高。

> 来源：[https://zh.wikipedia.org/wiki/模糊测试](https://zh.wikipedia.org/wiki/模糊测试)

## 准备工作

### 测试工具及对象选择

本文我们选择 Defensics 作为模糊测试的工具。Defensics 是 Synopsys 新思公司开发的黑盒模糊测试工具，提供了对大量文件格式、网络协议、接口的模糊测试套件。它针对 [MQTT](https://www.emqx.com/zh/mqtt) v3.1 协议标准，使用大量自动生成的 MQTT 数据包对 Broker/Client 进行测试，帮助开发者和测试人员提高软件的安全性。

> 针对 MQTT v5 的测试套件目前尚未发布

我们将以[开源 MQTT 消息服务器 - EMQ X](https://www.emqx.io/zh) 为例，对其协议实现情况进行安全性测试。EMQ X 是由 [EMQ 映云科技](https://www.emqx.com/zh/about) 开源的大规模可弹性伸缩的云原生分布式物联网 MQTT 消息服务器，可高效可靠连接海量物联网设备，高性能实时处理消息与事件流数据，助力构建关键业务的物联网平台与应用。

### 测试环境准备

本次测试在 Arch Linux 环境下进行，滚动更新至最新版本，使用 [EMQX 5.0-beta.2-8be2aaf7](http://github.com/emqx/emqx) 进行测试 。

此外，在进入下一步之前，需要从 Synopsys 处下载 Defensics 的安装包、后缀名为 `.install` 的测试套件安装文件、以及 DEFENSIC 可执行文件以提供给 FlexNet 许可服务器验证 license 状态使用。

![下载 Defensics 的安装包](https://static.emqx.net/images/f3dc5f87dc2e8bf9a32a6416a38cac17.png)

下载文件列表

### 部署许可服务器（FlexNet）

Synopsys Defensics 使用 FlexNet 管理许可证书，需要在执行 Defensics 模糊测试器的的网络环境中部署 FlexNet Server ，以管理从 Synopsys 处取得的许可证书（即 `license.lic` 文件）。

可以选择使用 Systemd User Unit 在本地部署启动 FlexNet Daemon ，配置如下。其中 `license.lic` 证书文件及 `DEFENSIC` 可执行文件将位于同一目录，FlexNet 将会从 `$PATH` 中的在更宽泛的场景下也可以将其部署在专用的证书服务器上以对更多的用户提供证书认证服务。其他详细信息和具体参数可参考 Defensics 及 FlexNet Publisher 相关文档。

![lmgrd.service Systemd User Unit](https://static.emqx.net/images/4b1e7fce7b405396c8cf79ba78652c18.png)

`lmgrd.service` Systemd User Unit

之后使用命令 `systemctl --user enable --now lmgrd.service` 启动认证服务器 Synopsys 提供的 Vendor Daemon。Defensics 便可以通过许可认证开始测试了。

### 其他配置

在 Linux 系统中可能存在显示问题及字体模糊的情况，可以参考 [Java Runtime Environment fonts - ArchWiki](https://wiki.archlinux.org/title/Java_Runtime_Environment_fonts) 进行配置。

### 安装 Defensics 及测试套件

以 root 身份执行 `.sh` 安装程序进行安装。并且安装过程中建议勾选启动脚本的生成选项 `/usr/local/bin/Defensics` 。

![Defensics 安装选项](https://static.emqx.net/images/40526d60677f11ae7c202597fbbe5b49.png)

安装选项

如果一切顺利，启动 Defensics 后在 `File -> License Manager` 中就可以看到经过验证的 License 状态。之后就可以安装并加载测试套件了。

![Defensics 安装测试套件](https://static.emqx.net/images/e02693d733f6a8842b1cd5babb9fe39d.png)

安装测试套件

## Defensics 测试

### 基础配置

在基础配置中设置 MQTT Server 的 ip 地址和端口号，以及用于测试的 MQTT Client 配置。

> 其中 MQTT 默认为 1883 端口（在启用了 TLS/SSL 时为 8883 端口）。

如果 MQTT Server 启用了客户端认证或消息主题权限，需要对测试用的两个客户端进行更详细的配置。
另外 Defensics 也提供了更进阶的 Payload 模糊测试和基于 TLS/SSL 连接的测试。但本次测试仅涉及 MQTT v3.1.1 协议标准相关的模糊测试，所以无需进行配置。

![MQTT Basic Configuration](https://static.emqx.net/images/1553f5d3865aa2698c0e93f6c5ca08dc.png)

Basic Configuration

在配置了相应的字段值后，Defensics 将会以指定的 Client ID 、用户名密码连接 MQTT Server ，并会用指定的 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)进行消息发布和主题订阅，即 `PUBLISH` 与 `SUBSCRIBE` 。

对于更高阶和复杂的测试，可以使用 `Edit sequence` 功能编辑对应的配置文件，来改变连接或断开连接时的行为，例如连接后自动订阅，连接后立刻发布消息等操作。

### 可操作性测试

完成配置后在 `Interoperability` 中进行可操作性测试，来验证不同的报文能否正常进行发送接收。在与 MQTT Server 正常连通的情况下，可以执行的测试组将会以绿色标注。

![Defensics Interoperability Test](https://static.emqx.net/images/a89b566ffdc482858cbd8b613fff761c.png)

Interoperability Test

### 高级配置

在这一部分，允许用户对具体的测试用例执行过程进行配置，但一般来说默认配置已经足够。

其中包括了对测试用例执行过程的控制，例如超时阈值、重复次数、尝试次数等。

![Defensics Test Case Run Control](https://static.emqx.net/images/e94910e510168e37f0cd9fe619f1b12c.png)

Test Case Run Control

另外用户也可以根据实际情况进行网络相关的配置，以获取在不同网络情景下的测试结果。此时也可以选择根据 MQTT Server 的目标 IP 进行自动配置。

![Defensics ip 自动配置](https://static.emqx.net/images/2c53185bc298a950b9387f301b4fb975.png)

Capture Conf

![TCP Conf](https://static.emqx.net/images/191ab05ba62b366fbdf69814d846e674.png)

TCP Conf

另外也可以根据 CVSS （通用漏洞评分系统）提供的漏洞分级方法对可能检测到的异常情况进行评估。

### 仪表配置（Instrumentation）

仪表是指在测试过程中观察和控制被测系统，观察的目标是检测由测试引起的任何故障。仪表还可用于在运行测试时重新启动或以其他方式控制被测系统。

大多数测试套件都启用了默认检测，无需进行额外配置。并且此默认配置的性质因不同的测试套件而异。

### 选择测试用例

Defensics 对于 MQTT v3.1.1 协议标准，提供了总计超过 100 万的测试用例可以用来对目标系统进行全面的模糊测试。与此同时，也支持用户进行基于这些细分的测试用例自行选择、组合用例，来针对性地聚焦分析并解决问题。

此次我们选取部分用例进行测试，其中包括 `CONNECT-DISCONNECT` `PUBLISH-qos-0` `SUBSCRIBE-qos-0` 三组用例，并同时选择全部异常消息用例进行测试。

![Defensics 选择测试用例](https://static.emqx.net/images/fef47b90282c571e94c3cc4af639d4c9.png)

Test Case Choosen

在针对于异常消息的测试中，也可以选择各类不同数据的异常行为数量和程度进行测试。例如文本、二进制数据、数字、字符等；同时也可以配置溢出异常的字节限制来使用值溢出的畸形报文进行测试。

![Sequence anomalies Choosen](https://static.emqx.net/images/9f6730c95cec21e5e706a70ef80ec99f.png)

Sequence anomalies Choosen

![Defensics Customize anomalies size](https://static.emqx.net/images/b0d285fcd915a63216b78d5f54984f68.png)

Customize anomalies size

### 执行测试

选择好测试用例的种类和异常数据的数量，便可以开始测试。本次测试用时约 6 分钟，其中约 98% 通过测试，约 1%（2779条用例）结果未知。

![Defensics 执行测试](https://static.emqx.net/images/818cbe6bdbdc592fea058c00a747e66f.png)

Run time 06:03

### 分析保存结果

我们先来选取其中一条未知结果的异常报文进行分析。

可以看到 Defensics 为了评估被测对象的健壮性，在模糊测试时尝试使用了不符合协议规范的异常数据进行测试。例如图中被进行了红色高亮标注部分，这部份两字节数据在 MQTT v3.1.1 协议的 `SUBSCRIBE` 报文中，指示了订阅主题的 UTF-8 字符串的长度。即表示接下来长度 `0x009A` (154字节)的数据为订阅主题过滤器的 UTF-8 字符串。但该主题过滤器实际长度 18 字节，值应为 `0x0012` ，与实际长度不符。

按照协议的强制性规范声明，在此种情况下，服务端必须关闭传输这个协议违规控制报文的网络连接**[MQTT-4.8.0-1]。**

但并未具体规定是否必须有指示错误原因的报文回传。所以 EMQ X 仅进行了内部错误处理，对异常报文直接丢弃。也不对发送方进行任何信息回传操作，所以 Defensics 将此条结果标记为未知。

但按照协议，**此结果仍然符合要求。**

![Defensics 结果分析](https://static.emqx.net/images/66fbd43d3a9d1ef7404ee98f7c15d6e5.png)

Malformed Subscribe Packet

经过统计，2779 条结果未知的测试用例中，不同类型的错误如下表所示：

| **错误类型**                              | **数量** |
| :---------------------------------------- | :------- |
| 报文过大(overflow)                        | 190      |
| 固定报头错误(fixed-header)                | 44       |
| 固定报头标志位错误(flags)                 | 34       |
| 报文剩余长度值异常(remaining-length)      | 1167     |
| 报文标识符异常(packet-identifer)          | 626      |
| 主题过滤器结构错误(topic-filters)         | 304      |
| 主题过滤器长度值异常(topic-filter-length) | 414      |

EMQ X 在面对这些异常报文时，直接作了丢弃处理，并未发回关于错误信息的指示报文。

对于其中一部分错误类型，由于错误点位的信息比较关键，试图对关键信息边界进行猜测甚至可能造成更大、更无法接受的错误。
例如上面剖析过的字符串长度指示值错误。如果对主题过滤器及其长度进行猜测，可能会得到错误的主题过滤器，造成客户端得到非预期的主题订阅。甚至也有可能是主题过滤器长度正确，而主题过滤器的值在传输过程中丢失损坏。

这类逻辑错误在系统运行中更加难以发现和排查，并且后果更难以接受。所以此时对异常报文直接丢弃成为了更优选择。

至于其他类型的错误，由于错误点位过于明显，相较之下更可能的原因是传输过程中的数据丢失、或数据流边界错误导致的异常。所以更倾向于认为这些数据不是 MQTT 报文，也作了丢弃处理，不去耗费额外的资源对这些异常进行处理。

## 总结

本文大致梳理了使用 Synopsys 出品的 Defensics 模糊测试器及配套的 MQTT v3.1 协议测试套件，对 EMQ X 的模糊测试过程，并且选取了部分用例进行测试和结果原因分析。

可以看到 EMQ X 在对协议的实现上非常完整，即使使用大量错误报文进行测试也不会导致 EMQ X 失去提供服务的能力，可以保证协议的安全性，为实际项目的稳定运行提供安全保障。

EMQ 致力于为物联网领域提供高可用、高可靠的 MQTT 消息服务器及其他数据基础设施软件。在去年，我们也与 Synopsys 达成了合作，该公司将全面负责 EMQ 各产线产品整个生命周期的安全和质量风险管理。我们希望用户可以通过 EMQ 的产品，构建更加稳定可靠的物联网平台与应用。

EMQ X 开源项目也随时欢迎您的参与，欢迎通过 [GitHub：https://github.com/emqx/emqx](https://github.com/emqx/emqx) 向我们提交 PR 或 Issue。
