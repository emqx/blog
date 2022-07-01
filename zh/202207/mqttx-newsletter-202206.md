在过去的一月中，MQTT X 发布了最新的 1.8.0 版本（下载地址：[https://github.com/emqx/MQTTX/releases/tag/v1.8.0](https://github.com/emqx/MQTTX/releases/tag/v1.8.0) ），优化部分使用体验和改进各项问题的同时，新增了 CLI 和 Web 端的 MQTT 客户端工具，支持在终端命令行或桌面浏览器上快速完成对 MQTT 的连接测试。

## 1.8.0 版本概览

### 支持复制连接

在之前的版本中，通常如果想在现有的连接基础上建立一个新的连接，需要到创建连接页面内，配置相同的连接信息，或在连接页面内选择已经创建过的连接并修改连接名称后，才能创建新的连接。

为优化使用体验，该版本中支持了快速复制连接功能，在连接列表中鼠标右键点击连接，在右键菜单中，选择复制，即可快速复制并创建一个新的连接。

![MQTT X](https://assets.emqx.com/images/6a6b44461629b93eca37285480cd38a2.png)

### 其它优化

- 更新关于页面
- 修复了无法清除过长消息的问题
- 修复了过长消息在不同的页面中重复显示的问题
- 修复新建连接时，左侧菜单的选中问题
- 修复一些英文版大小写显示的问题

## MQTT X CLI

伴随着 MQTT X v1.8.0 的正式发布，我们推出了一款 MQTT 命令行客户端工具——MQTT X CLI。

MQTT X CLI 是一款全开源的 MQTT 5.0 命令行客户端工具，也是命令行上的 MQTT X，旨在帮助开发者无需使用图形化界面，也能快速开发和调试 MQTT 服务与应用。

随着 MQTT 协议在物联网领域的广泛使用，MQTT X 用户量也逐渐增多，为满足不同的用户之间各不相同的调试需求和使用环境，MQTT X 将使用场景扩展到了使用命令行的交互形式上来。服务端的开发者和用户得以在服务器终端内快速测试部署好的 MQTT 服务，或使用一些命令行脚本来快速测试 MQTT 服务，在不同的使用场景下快速完成对 MQTT 服务或应用的开发与调试，提高自身的相关业务能力与稳定性。

了解详情可查看 MQTT X CLI GitHub 仓库：[https://github.com/emqx/MQTTX/tree/main/cli](https://github.com/emqx/MQTTX/tree/main/cli) 

![MQTT CLI](https://assets.emqx.com/images/807209f2aa2d04ef17cca61bd56a475f.png)

### 快速开始

**安装**

MQTT X CLI 同样可以快速下载并安装到 macOS，Linux 和 Windows 系统上，**安装前不需要任何的依赖环境准备**，只需要在终端内输入命令行后，即可简单快速的安装和使用 MQTT X CLI。

点击查看如何快速[安装 MQTT X CLI](https://github.com/emqx/MQTTX/blob/main/cli/README-CN.md#安装)，安装完成后，可在终端内直接运行 `mqttx` 命令。

**订阅**

```
mqttx sub -t 'hello' -h 'broker.emqx.io' -p 1883
```

**发布**

```
mqttx pub -t 'hello' -h 'broker.emqx.io' -p 1883 -m 'from MQTTX CLI'
```

有关 MQTT X CLI 的具体使用场景和使用方法，敬请关注后续文章推送。

## MQTT X Web

除发布了 MQTT X CLI 版本外，本次更新还推出了一款 MQTT 在线客户端工具——MQTT X Web。

MQTT X Web 是一款开源的 MQTT 5.0 浏览器客户端，也是一个在线 MQTT WebSocket 客户端工具。开发者无需在本地下载和安装 MQTT X，使用 WebSocket 在浏览器中快速连接到 MQTT，即可更快地开发和调试你的 MQTT 服务和应用程序。

了解详情可查看 MQTT X Web GitHub 仓库：[https://github.com/emqx/MQTTX/tree/main/web](https://github.com/emqx/MQTTX/tree/main/web) 

快速使用和体验课访问 MQTT X Web 在线地址：[http://tools.emqx.io/](http://tools.emqx.io/) 

> 注意：在浏览器端只支持使用 WebSocket 连接到 MQTT 服务，请注意配置连接 MQTT 的协议和端口号，目前仅支持使用部分 MQTT X 的功能，我们将在后续继续同步与更新，将尽快统一 MQTT X 本地与在线工具的使用体验。

![MQTT WebSocket](https://assets.emqx.com/images/cd9cdd01ffe502a4a251c3eb6aa68e88.png)

## 未来规划

MQTT X 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网平台的测试和开发提供便利。

接下来我们将重点关注以下方面：

- 使用体验升级
- 插件系统（例如支持 SparkPlug B，集成 MQTT X CLI）
- 脚本功能优化
- 推出 MQTT X Mobile 移动端应用
- 完善 MQTT X Web 功能
- MQTT Debug 功能
