近日，由 EMQ 开源的 [MQTT 5.0 跨平台桌面客户端 MQTTX](https://mqttx.app/zh) 发布了 1.8.0 版本。MQTTX 为连接测试各类 [MQTT 消息服务器](https://www.emqx.io/zh)而生，支持快速创建多个同时在线的 [MQTT 客户端](https://www.emqx.io/zh/mqtt-client)连接，采用一键式的连接方式和简洁的图形界面，帮助使用者便捷地测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的连接、发布、订阅功能，探索更多 [MQTT 协议](https://www.emqx.com/zh/mqtt)特性。

最新发布的 v1.8.0 除了通过新增的快速复制连接功能优化使用体验之外，还扩展了两个新的使用场景，即增加了 CLI（命令行） 和 Web 端这两种新的交互方式 。这使得 MQTTX 1.8.0 成为支持使用场景最完整的 MQTT 测试客户端。用户可以根据使用需求，自行选择下载桌面客户端、使用终端命令行或是在桌面浏览器上快速完成对 MQTT 的连接测试。

## MQTTX CLI：在终端快速开发和调试 MQTT 服务与应用

随着 MQTT 协议在物联网领域的广泛使用，越来越多的用户选择使用 MQTTX 进行物联网连接测试。对于部分用户如服务端开发者、服务运维人员等来说，下载桌面客户端可能会占用系统的大量磁盘空间，每次测试前都需要在带有图形化界面的操作系统中打开客户端应用来调试。在这种情况下，桌面客户端这种使用方式就变得不太友好。

因此 MQTTX 增加了命令行这一交互形式——MQTTX CLI。这是一款全开源的 MQTT 5.0 命令行客户端工具，即命令行上的 MQTTX。**开发者无需使用图形化界面，就能通过 MQTTX CLI 使用命令行快速开发和调试 MQTT 服务与应用。**从而实现以下使用目标：

- 在服务器终端内就可以测试已经部署好的 MQTT 服务
- 通过编辑和使用命令行脚本完成 MQTT 服务的快速测试
- 使用命令行脚本来完成一些简单的压力测试或自动化测试

> MQTTX CLI 网站：[https://mqttx.app/zh/cli](https://mqttx.app/zh/cli) 
>
> MQTTX CLI v1.8.0 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.8.0](https://github.com/emqx/MQTTX/releases/tag/v1.8.0) 
>
> MQTTX CLI GitHub 仓库：[https://github.com/emqx/MQTTX/tree/main/cli](https://github.com/emqx/MQTTX/tree/main/cli) 

![MQTT CLI](https://assets.emqx.com/images/6e1009d394255edd48a9da76ae698a94.jpeg)



## 便捷高效：无需依赖环境即可安装使用

### 安装

MQTTX CLI 可以快速下载并安装到 macOS、Linux 和 Windows 系统上，**安装前不需要任何的依赖环境准备**，只需在终端内执行命令，即可安装和使用 MQTTX CLI。

对于 macOS 和 Linux 系统的用户，我们提供了快捷的安装方法，使用命令行可以快速下载二进制文件，并安装最新的 MQTTX CLI 稳定版到操作系统上。Windows 用户则可以到 MQTTX 的[发布页面](https://github.com/emqx/MQTTX/releases)内，找到对应的系统架构的 `exe` 包，手动下载后使用。

> 注意：下载安装时请注意区分当前使用系统环境的 CPU 架构

#### **macOS**

- **Homebrew**

  macOS 用户可以通过 Homebrew 来快速安装和使用 MQTTX CLI

  ```
  brew install emqx/mqttx/mqttx-cli
  ```

- **Intel Chip**

  ```
  curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-macos-x64
  sudo install ./mqttx-cli-macos-x64 /usr/local/bin/mqttx
  ```

- **Apple Silicon**

  ```
  curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-macos-arm64
  sudo install ./mqttx-cli-macos-arm64 /usr/local/bin/mqttx
  ```

#### **Linux**

- **x86-64**

  ```
  curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-linux-x64
  sudo install ./mqttx-cli-linux-x64 /usr/local/bin/mqttx
  ```

- **ARM64**

  ```
  curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-linux-arm64
  sudo install ./mqttx-cli-linux-arm64 /usr/local/bin/mqttx
  ```

#### **Windows**

Windows 用户请到 MQTTX 的下载页面内手动下载对应的 `exe` 文件来使用，下载地址：[https://github.com/emqx/MQTTX/releases/tag/v1.8.0](https://github.com/emqx/MQTTX/releases/tag/v1.8.0) 

![Windows MQTT](https://assets.emqx.com/images/e236e184d509efcad443b0551f00dacf.png)

#### **NPM**

除上述方法外，我们还提供了使用 `npm` 的安装方式，这样无论当前是什么操作系统环境，只要您的系统中有 `Node.js` 环境，就可以快速安装和使用。

```
npm install mqttx-cli -g
```

### 快速开始

在完成下载安装后，便可在终端内直接输入 `mqttx` 命令来运行和使用了。您可以加 `-V` 参数来验证 MQTTX CLI 是否安装成功，当输出一个版本号时，就证明 MQTTX CLI 已经成功安装。

```
$ mqttx -V
1.8.0
```

为测试 MQTTX CLI 的使用，我们需要准备一个 MQTT 服务，本文将使用 EMQ 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 [MQTT 物联网云平台 - EMQX Cloud](https://www.emqx.com/zh/cloud) 创建，服务器接入信息如下：

- Broker: `broker.emqx.io`
- TCP Port: **1883**
- WebSocket Port: **8083**

准备好 MQTT 服务后，我们就可以在终端内使用命令行来完成消息的发布与订阅了，我们先在一个终端窗口内，编辑一条订阅主题的命令。

**订阅**

```
mqttx sub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883
```

在完成订阅后，我们再新建一个终端窗口，编辑一条发布到刚才订阅的主题的消息的命令。

**发布**

```
mqttx pub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883 -m 'hello from MQTTX CLI!'
```

此时我们可以在订阅主题命令的窗口内，看到一条刚才发布过来的消息。

![MQTT CLI](https://assets.emqx.com/images/7922ba94a119c37a15722bd6c7f7ed7c.png)

**发布多条消息**

MQTTX CLI 还支持一个 `pub` 命令可以发布多条消息的功能，只需要在编辑是在命令中添加一个  `-M` 参数和 `-s` 参数，每次输入完成后换行即可。

```
mqttx pub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883 -s -M
```

![MQTT CLI](https://assets.emqx.com/images/549a31f8b062f099c0eac8c0c6047f35.png)

最后，我们再通过使用 MQTTX 的桌面客户端来和 MQTTX CLI 来连接到同一个 MQTT 服务，来测试和验证 MQTTX CLI 的功能，我们使用 MQTTX CLI 发布一条消息，通过 MQTTX 桌面客户端来接收，再反向使用 MQTTX 桌面客户端来发送一条消息到 MQTTX CLI。此时，我们可以看到两边都收到了各自收发的消息。

![MQTT 桌面客户端](https://assets.emqx.com/images/e8712613d23e472e642949c639d471ac.png)

<center>MQTTX 桌面客户端</center>

![MQTT CLI](https://assets.emqx.com/images/af38097e9c9832ad8cfa3959085ed280.png)

<center>MQTTX CLI</center>

## 结语

至此，我们就完成了使用 MQTTX CLI 对 MQTT 消息发布订阅功能的测试和验证。除上述常用功能使用外，MQTTX CLI 还支持设置遗嘱消息、使用 SSL/TLS 来测试 mqtts 的连接等。未来还将支持 MQTT 5.0 连接。

MQTTX CLI 的发布，为物联网开发者进行 MQTT 连接测试提供了一种新的选择。而对命令行调用、桌面客户端下载和在线浏览器这几种交互形式的完整支持，使得 MQTTX 1.8.0 可帮助不同使用场景需求的用户完成对 MQTT 服务或应用的开发与调试，从而提高用户自身相关业务能力与稳定性。简单易用的测试客户端工具 MQTTX 结合高效可靠的物联网消息服务器 EMQX，将帮助物联网开发者构建具有竞争力的物联网平台与应用。

## 附：使用帮助

您可以在命令行内输入 `--help` 参数来获取使用帮助，或查阅下方的使用参数表来使用 MQTTX CLI。

```
# 获取 mqttx 命令的帮助
mqttx --help

# 获取订阅命令的帮助
mqttx sub --help

# 获取发布命令的帮助
mqttx pub --help
```

### 使用**参数对照表**

| 参数          | 描述                         |
| :------------ | :--------------------------- |
| -V, --version | 输出当前 MQTTX CLI 的版本号 |
| -h, --help    | 展示 mqttx 命令的帮助信息    |

| 命令 | 描述               |
| :--- | :----------------- |
| pub  | 向主题发布一条消息 |
| sub  | 订阅一个主题       |

**订阅**

| 参数               | 描述                                     |
| :----------------- | :--------------------------------------- |
| -h, --hostname     | MQTT Broker 的 Host 地址，默为 localhost |
| -p, --port         | MQTT Broker 的端口号                     |
| -i, --client-id    | 客户端 ID                                |
| -q, --qos <0/1/2>  | 消息的 QoS，默认为 0                     |
| --clean            | clean session 的标志位，默认为 true      |
| -t, --topic        | 需要订阅的 Topic                         |
| -k, --keepalive    | MQTT 的 Keep Alive，默认为 30            |
| -u, --username     | 连接到 MQTT Broker 的用户名              |
| -P, --password     | 连接到 MQTT Broker 的密码                |
| -l, --protocol     | 连接时的协议，mqtt, mqtts, ws or wss     |
| --key              | key 文件的路径                           |
| --cert             | cert 文件的路径                          |
| --ca               | ca 证书的文件路径                        |
| --insecure         | 取消服务器的证书校验                     |
| --will-topic       | 遗嘱消息的 topic                         |
| --will-message     | 遗嘱消息的 payload                       |
| --will-qos <0/1/2> | 遗嘱消息的 QoS                           |
| --will-retain      | 遗嘱消息的 retain 标志位                 |
| -v, --verbose      | 在接收到的 Payload 前显示当前 Topic      |
| --help             | 展示 sub 命令的帮助信息                  |

**发布**

| 参数               | 描述                                     |
| :----------------- | :--------------------------------------- |
| -h, --hostname     | MQTT Broker 的 Host 地址，默为 localhost |
| -p, --port         | MQTT Broker 的端口号                     |
| -i, --client-id    | 客户端 ID                                |
| -q, --qos <0/1/2>  | 消息的 QoS，默认为 0                     |
| -t, --topic        | 需要发布的 Topic                         |
| -m, --message      | 需要发布的 Payload 消息                  |
| -r, --retain       | 设置发送消息为 Retain 消息，默认为 fasle |
| -s, --stdin        | 从 stdin 中读取信息体                    |
| -M, --multiline    | 可以通过多行发布多条消息                 |
| -u, --username     | 连接到 MQTT Broker 的用户名              |
| -P, --password     | 连接到 MQTT Broker 的密码                |
| -l, --protocol     | 连接时的协议，mqtt, mqtts, ws or wss     |
| --key              | key 文件的路径                           |
| --cert             | cert 文件的路径                          |
| --ca               | ca 证书的文件路径                        |
| --insecure         | 取消服务器的证书校验                     |
| --will-topic       | 遗嘱消息的 topic                         |
| --will-message     | 遗嘱消息的 payload                       |
| --will-qos <0/1/2> | 遗嘱消息的 QoS                           |
| --will-retain      | 遗嘱消息的 retain 标志位                 |
| --help             | 展示 pub 命令的帮助信息                  |
