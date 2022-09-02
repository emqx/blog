8 月，eKuiper 发布了 1.6.1 Fixpack 版本。该版本主要增强了产品运维的稳定性和易用性，包括提供可移植性更强的预编译二进制包、Docker Image 和插件包，管理控制台提供了规则告警等功能。此外，该版本也解决了一些 Bug。接下来，eKuiper 团队将进入 1.7.0 版本的开发周期，更加专注于新功能的开发。

## 多平台插件一键安装

eKuiper 自带的插件在产品发布的持续集成（CI）流水线中会自动预编译和打包，用户在 eKuiper manager 管理控制台中可以选择插件类型，自动拉取预编译包一键安装。

之前版本中，预编译插件的编译环境绑定在 Debian/Ubuntu 系统，编译出的插件仅能使用在带 slim 的 Docker 版本中，例如 `lfedge/ekuiper:1.6.0-slim`。用户如果通过二进制安装包或者 alpine 的 Docker Image 部署 eKuiper，需要使用自带插件时，仍然需要通过较为繁琐的步骤进行编译。

新版本中，我们重构了 CI 的编译流程，实现了预编译插件的多平台支持。预编译的插件包含两种系统的版本，每个系统下又有多个不同 CPU 架构的预编译包。预编译的插件 URL 格式为 `https://packages.emqx.net/kuiper-plugins/{version}/{os}/{type}/{name}_{arch}.zip`。例如，1.6.1 版本的 Debian 系统下的 Redis sink 插件 AMD64 版本的 URL 为 [https://packages.emqx.net/kuiper-plugins/1.6.1/debian/sinks/redis_amd64.zip](https://packages.emqx.net/kuiper-plugins/1.6.1/debian/sinks/redis_amd64.zip)。预编译插件的有两种 OS 版本：Debian 和 alpine。其中，alpine 专门提供给 Docker Image `lfedge/ekuiper:{version}-alpine` 使用。其余 Linux 平台均可使用 Debian 版本，包括二进制的 tar 包和其余版本的 Docker Image。

在新版的 eKuiper manager 中，使用官方的镜像和二进制包，选择插件版本后均可以一键安装插件。

### 二进制包低版本系统支持

修改了编译流程之后，新的官方二进制包可以支持在较旧的操作系统中使用，例如 Ubuntu 18.04 和 CentOS 7 等 glibC 版本的较低的系统。

## Neruon/MQTT 自动重连和连接错误告警

使用 Neuron 和 MQTT 连接的规则，若规则运行期间由于网络或应用自身等原因连接断开后，规则将可以得到连接断开的通知。若使用连接的为 source，则连接断开时，source 的异常指标数目会加 1。若使用连接的为 sink，则会在每个数据发送时返回一个发送异常。

当故障恢复后，Neuron 和 MQTT 连接会自动重连。新版本中解决了使用 Windows 或 MacOS 的 Docker 运行 eKuiper 时自动重连失效的问题。

自动重连的功能保证了规则启动后可以无需人工干预自动从错误中恢复，达到长期稳定运行的效果。但是，由于异常发生时，规则本身仍为运行状态，用户需要点击查看规则的状态才能够知道规则运行中产生过的异常。新版本中，规则的指标添加了 `last_exception` 和 `last_exception_time` 用于获取最近一次异常消息和发生的时间，方便快速地定位问题。

新版本的管理控制台中也适配了规则异常指标，提供了规则异常告警功能，并在规则列表中显示，提醒用户进行进一步的排查。告警查看排查完成后，用户可以点击清除告警，以清除已查看过的告警，这样新的告警出现后才会显示在列表页面中。

![eKuiper 控制台](https://assets.emqx.com/images/b681cef501e99fdbf2fe8facc16a682a.png)

## Bug 修复

- MQTT 连接默认采用 3.1.1 协议版本，防止 NanoMQ 连接失败
- 兼容 1.5.0 及之前版本的配置文件
- 修复共享源的规则重启可能失败的问题

## 即将到来

接下来我们将开始 1.7.0 版本的开发。计划中的新功能包括动态表/初步流批一体处理的支持、连接资源管理功能等，敬请期待。
