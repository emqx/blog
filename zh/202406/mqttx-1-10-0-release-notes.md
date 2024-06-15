MQTTX 1.10.0 版本现已发布！

在本次更新中，CLI 版本在文件管理和配置功能方面进行了显著增强。主要更新包括：支持从文件中读取和写入消息、高级配置选项、文本输出模式、以及改进的日志记录。此外，桌面版本现在支持数据库重建，以防止文件损坏引起的问题，并且能更好地处理大数据的展示。这些更新希望为所有 MQTTX 用户提供更加强大和用户友好的体验。

> *点击此处下载最新版本：*https://mqttx.app/zh/downloads 

## CLI 中的文件管理

MQTTX 1.10.0 在 CLI 中引入了强大的文件读写功能。此功能可以无缝处理文件输入和输出的消息负载，从而在数据工作流中提供集成和自动化。

### 文件读取

> 注意：由于 MQTT 协议的限制，消息的载荷大小不得超过 256MB。在传输前，请验证你的 MQTT broker 的载荷大小限制。

**使用** `pub` **命令**

使用以下命令从文件读取消息：

```shell
mqttx pub -t topic --file-read path/to/file
```

`--file-read` 选项允许你直接从文件读取内容作为发布的载荷。这对于使用预定义的测试数据进行各种发布场景非常方便。

**使用** `bench pub` **命令**

`--file-read` 命令从文件中读取消息体，类似于简单的 `pub` 命令：

```shell
mqttx bench pub -c 10 -t topic --file-read path/to/file
```

利用 `bench` 命令的内置强大功能，您可以通过使用 `--split` 选项将文件内容分割到单独的消息中，以便发送不同的数据段。默认字符是 `\n`。

例如，有一个包含以下内容的文件：



```
hello
world
```

您可以使用：

```shell
mqttx bench pub -c 10 -t topic --file-read path/to/file --split
```

如果文件是用逗号分隔的，将 `--split` 改为 `,`：

```shell
mqttx bench pub -c 10 -t topic --file-read path/to/file --split ','
```

最后还可以设置 `-im` 来定义发布消息的时间间隔。

### 文件写入

如果要将收到的消息写入到文件中，可以使用以下命令：

```shell
mqttx sub -t topic --file-write path/to/file
```

`--file-write` 选项会将每条消息追加到文件中，每条消息默认使用换行符 `\n` 分隔，这非常适合用于日志记录或累积文本数据。对于需要维持连续接收消息日志的应用程序来说，这个功能非常方便。

如果要更改分隔符，可以使用 `--delimiter` 选项。例如：

```shell
mqttx sub -t topic --file-write path/to/file --delimiter ','
```

### 文件保存

若要将每条单独的消息保存为一份单独的文件，请使用：

```shell
mqttx sub -t topic --file-save path/to/file
```

`--file-save` 选项将每条传入的消息保存为一个单独的文件。已有的文件将自动重新编号并保存，以防止覆盖。此功能对于需要存储单个消息以进行进一步处理或分析的应用程序非常方便。

例如，要将传入的消息保存到指定的目录：

```shell
mqttx sub -t topic --file-save /path/to/directory/message.txt
```

如果 `/path/to/directory/message.txt` 已经存在，新的消息将被保存为 `message(1).txt`、`message(2).txt` 等。这样可以防止由于覆盖现有文件而导致的任何数据丢失。

> 请勿同时使用 --file-write 和 --file-save。

### 类型格式

文件传输也支持指定对应的文件格式来格式化消息。如果未指定，默认为纯文本（UTF-8）格式。可以使用 `--format` 选项对消息内容进行格式化以处理不同的数据格式：

```shell
mqttx pub -t topic --file-read path/to/file --format type
mqttx sub -t topic --file-save path/to/file --format type
```

支持输出到文件的数据格式包括 `json`，`base64`，`hex`，`binary` 和 `cbor`。

为此，该版本还引入了一个新的 `binary` 格式来处理更常见的文件传输场景。通过指定二进制格式，MQTTX 收发时将处理和生成相应的二进制文件。

如果文件有以下扩展名，它将自动识别文件格式为二进制：

- **图片：** `.png`，`.jpg`，`.jpeg`，`.gif`，`.bmp`，`.ico`，`.tif`，`.tiff`
- **视频：** `.mp4`，`.avi`，`.mov`，`.mkv`，`.flv`，`.wmv`，`.mpeg`，`.3gp`
- **音频：** `.mp3`，`.wav`，`.flac`，`.aac`，`.ogg`，`.wma`，`.m4a`，`.m4p`
- **压缩：** `.zip`，`.gz`，`.rar`，`.tar`，`.7z`，`.bz2`，`.xz`，`.jar`
- **二进制：** `.bin`，`.exe`，`.dll`，`.so`，`.dmg`，`.iso`，`.img`
- **文档：** `.pdf`，`.epub`

要手动指定二进制格式，使用：

```shell
mqttx pub -t topic --file-read path/to/file --format binary
mqttx sub -t topic --file-save path/to/file --format binary
```

## CLI 配置文件

此版本引入了配置文件功能，它可以存储各种设置的默认值，为 MQTTX CLI 提供了简化和可定制的体验。初始化后，配置文件将存储在用户的主目录 `$HOME/.mqttx-cli/config` 中。

### 功能

配置文件包括用于控制界面和功能参数的设置。这些设置允许 MQTTX CLI 使用预定义的值，提高效率，避免需要反复输入信息。

**默认：**

- **output**
  - **text:** 默认模式提供包含关键信息的简洁输出。
  - **log:** 显示带有日期和时间戳的详细日志输出。

**MQTT:**

- **host:** 默认是 localhost。
- **port:** 默认是 1883。
- **max_reconnect_times:** 默认是 10。
- **username:** 默认为空。
- **password:** 默认为空。

默认部分中的 output 设置控制 CLI 的输出显示。用户可以根据自己的需要选择不同的模式。

如果命令行没有提供这些参数，MQTTX CLI 将使用 mqtt 部分中的配置文件中的值。`host`, `port`, `username`, 和 `password`

`max_reconnect_times` 控制重连尝试的次数。一旦到达设定的次数，连接将自动关闭，以防止无限制的重连。

如果不需要 `username` 和 `password` 这样的配置项，它们可以从配置文件中省略。

**初始化配置**

默认情况下不提供配置文件。要创建或更新配置文件，运行 `init` 命令。此命令将提示你输入所需的值：

```shell
mqttx init
? Select MQTTX CLI output mode Text
? Enter the default MQTT broker host broker.emqx.io
? Enter the default MQTT port 1883
? Enter the maximum reconnect times for MQTT connection 5
? Enter the default username for MQTT connection authentication admin
? Enter the default password for MQTT connection authentication ******
Configuration file created/updated at /Users/.mqttx-cli/config
```

**配置文件示例**

```shell
[default]
output = text
[mqtt]
host = broker.emqx.io
port = 1883
max_reconnect_times = 5
username = admin
password = public
```

### 界面改进

配置文件中的 `output` 设置提供了两种模式：

- **文本模式：** 提供简洁清晰的输出，只包含关键信息，便于阅读和理解。

  ```shell
  mqttx conn
  ✔ Connected
  ```

- **日志模式：** 此模式显示带有日期和时间戳的详细日志输出，有助于记录和调试。

  ```shell
  mqttx conn
  [5/24/2024] [11:26:17 AM] › …  Connecting...
  [5/24/2024] [11:26:17 AM] › ✔  Connected
  ```

用户可以通过选择适当的输出模式，根据自己的工作流和偏好定制 MQTTX CLI。

## 桌面版本白屏问题

我们对桌面版本中白屏问题的报告进行了调查，找出了两个主要原因：数据库文件损坏和处理大消息负载时的性能问题。为解决这些问题，我们对 MQTTX 进行了优化。

### 数据库重建

SQLite 数据库文件损坏可能由多种因素引起，特别是在软件升级后：

1. **架构改变不兼容**：在升级过程中改变数据库结构，但没有正确迁移旧数据。
2. **升级中断**：软件更新期间出现意外中断导致数据库文件不完整。
3. **竞态条件**：并发访问没有正确管理，导致写入冲突。
4. **升级脚本出错**：更新期间数据库脚本执行错误影响数据完整性。
5. **磁盘空间不足**：更新期间由于空间不足阻止完整的数据写入。
6. **文件系统或硬件问题**：底层存储问题导致文件损坏。

当出现这些问题时，用户无法打开 MQTTX。新版本的 MQTTX 检测到数据库文件损坏时，会显示出一个数据库重建页面。用户可以点击重建按钮来修复损坏的数据库文件并重新初始化数据。

> 注意：数据库重建后，所有本地数据将会丢失。

![数据库重建](https://assets.emqx.com/images/5ffffea84aac38f13a52c96a25663e22.png)

另一个问题是由大型消息负载造成的性能损失。虽然通常情况下的 MQTT 消息负载通常在 1MB 以下，但最大也可达 256 MB。因此当用户发送大文件时，MQTTX 在渲染这些消息时可能会导致用户界面冻结或崩溃，结果显示白屏。

在新版本中，我们添加了一个数据阈值。当负载大小超过 512KB 时，MQTTX 只会显示消息内容的一部分。用户可以点击“显示更多”以查看完整消息。此外，用户还可以使用“保存到本地”按钮将大型消息保存到本地系统，以便使用其他应用程序查看。

![点击查看更多](https://assets.emqx.com/images/dace20d9bb40a5fe982b636764cfa767.png)

![保存到本地](https://assets.emqx.com/images/b0a3c32ec345e784ebd2e29814f8ef5b.png)

这些改进确保 MQTTX 可以更有效地处理大型负载，防止用户界面冻结，并提高整体用户体验。

## Web 版更新

### 通过 env 文件支持 BASE_URL 配置

如果您需要进行个性化设置，如修改默认连接路径、部署路径或输出路径，您可以在 `web/.env` 或 `web/.env.docker` 文件中进行相应修改。这两个文件对应不同的打包需求，您可以根据实际情况进行修改。

| 配置项                   | 描述                                   |
| :----------------------- | :------------------------------------- |
| VUE_APP_PAGE_TITLE       | 浏览器标题栏显示的标题                 |
| VUE_APP_PAGE_DESCRIPTION | 用于 SEO 的简洁页面描述                |
| VUE_APP_DEFAULT_HOST     | MQTT broker 服务器连接的默认地址       |
| BASE_URL                 | 应用部署的根 URL，有助于构建链接和路由 |
| VUE_APP_OUTPUT_DIR       | 编译后的构建文件将被放置的目录         |

这些更新旨在提供更灵活、用户友好的体验，使您可以根据需求定制 MQTTX 网页版设置。

## 重要更新

| 旧命令                                           | 新命令                                                  |
| :----------------------------------------------- | :------------------------------------------------------ |
| mqttx conn -h broker.emqx.io  -p 1883 --save     | mqttx conn -h broker.emqx.io -p 1883 --save-options     |
| mqttx conn --config /Users/mqttx-cli-config.json | mqttx conn --load-options /Users/mqttx-cli-options.json |

在此次更新中，我们将原来的 `--config` 参数更改为了 `--options` 参数。此变更更好地反映了这些参数的目的，即保存和加载常用的命令参数。

- **-so, --save-options**：将参数保存到本地配置文件，支持 JSON 和 YAML 格式。默认路径是 `./mqttx-cli-options.json`。
- **-lo, --load-options**：从本地配置文件加载参数，支持 JSON 和 YAML 格式。默认路径是 `./mqttx-cli-options.json`。

## 其他更新

**新功能和改进**

- **自动重新订阅提示**：订阅对话框现在增加了自动重新订阅提示。在进行订阅时，您可以看到是否启用了自动重新订阅功能。
- **GPT-4o 支持**：在 MQTTX Copilot 中增加了对 GPT-4o 的支持，为您的 MQTTX 体验带来先进的 AI 能力。

**错误修复**

- **版本更新对话框**：修复了版本更新对话框，确保其适当适应暗黑模式，并在不同主题中提供一致的用户体验。
- **主题过滤**：解决了主题过滤的问题，确保主题的准确和可靠过滤。
- **日志改进**：增强了日志格式，并通过灰色显示输出元信息并改进了 bench sub 日志，使日志更易读，对于调试更有用。
- **订阅错误**：修复了处理多主题时的订阅错误逻辑，确保更流畅和可靠的订阅。
- **CLI 发布失败处理**：改进了 CLI 发布失败的重新连接逻辑，确保 CLI 更优雅地处理发布失败并尝试重新连接。

这些更新着重于改善用户体验，增强功能，并修复关键错误，以确保 MQTTX 的更顺畅和可靠的操作。

## 未来规划

- **Payload 图表可视化增强 - MQTTX Viewer**：
  - **主题树视图**：增强主题的组织和可视化。
  - **差异视图**：轻松比较不同的消息或负载。
  - **仪表板视图**：提供可定制的 MQTT 活动概览，以获取个性化洞见。
  - **JSON 视图**：改进 JSON 格式数据的处理和显示。
  - **系统主题视图**：专门针对系统相关 MQTT 主题的视图。
- **支持可配置的断开连接属性（MQTT 5.0）**：通过自定义断开连接设置来增强连接管理。
- **物联网场景数据模拟**：将此功能带到桌面客户端，以简化物联网场景测试。
- **Sparkplug B 支持**：扩展 MQTTX 功能，包括对 Sparkplug B 的特殊支持。
- **QoS 0 消息存储优化**：提供可配置选项，减少存储空间使用。
- **MQTT GUI 调试功能**：帮助调试 MQTT 通信的新功能。
- **插件功能**：引入支持协议扩展（如 CoAP 和 MQTT-SN）的插件系统。
- **Avro 消息格式支持**：增加对 Avro 消息格式的编码和解码能力。
- **脚本测试自动化（流程）**：简化自动化测试工作流的创建和管理。



<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://mqttx.app/zh/downloads" class="button is-gradient">免费下载 →</a>
</section>
