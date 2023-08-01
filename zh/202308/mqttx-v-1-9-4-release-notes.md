近日，MQTT 5.0 客户端工具 MQTTX 1.9.4 正式发布。本次更新为用户提供了更高效的 Protobuf 消息传输支持，并优化了自动更新功能，同时进行了一些功能特性的优化和增强。

> 最新版本下载：[https://mqttx.app/downloads](https://mqttx.app/downloads) 

## Protobuf 格式 MQTT 消息传输测试

为了满足大规模和高频数据交换的测试需求，我们在 MQTTX 中引入了对 Protobuf 的支持。这个新功能将极大地提升消息传输效率，使得消息传输更加高效、可靠，同时也进一步拓展了 MQTTX 的测试能力。

### 使用命令行客户端

在命令行客户端中，我们可以直接使用以下命令进行 Protobuf 格式的消息传输：

```
# Subscription
mqttx sub -t 'testtopic/#' -h broker.emqx.io -Pp ./TestPerson.proto -Pmn Person

# Publish
mqttx pub -t 'testtopic/protobuf' -Pp ./TestPerson.proto -Pmn Person -h broker.emqx.io -m '{"id":0, "name": "test"}'
```

这里的 `-Pp` 参数用于定义 Protobuf 消息格式的 `.proto` 文件路径，而 `-Pmn` 参数则用于指定 Protobuf 消息类型的名称（必须存在于 `.proto` 文件中）。

> 注意：发布或订阅时，您需要在任意路径下新建一个 proto 文件，然后在连接时指定 `.proto` 文件的路径和消息类型的名称。

### 使用桌面客户端

在桌面客户端中，我们优化了脚本部分，并新增了**自定义函数**和**编解码**脚本功能。在自定义函数中延续了之前的脚本功能，而在编解码中，现在可以使用自定义的 proto 文件格式进行数据的 protobuf 格式编解码。操作步骤如下：

1. 进入脚本页面，选择编解码。
2. 新建或导入一个 proto 文件。
3. 连接页面，选择运行脚本，选择一个刚才新建的编解码，输入一个 Proto Name 即消息的类型名称。
4. 收发消息时即可显示。

需要注意的是，在脚本中函数和编解码可以同时使用。默认的使用顺序为：在发送数据时，首先使用自定义函数处理 payload，然后使用编解码脚本对数据进行编码；在接收数据时，首先对数据进行解码，然后再使用自定义函数处理数据。

![MQTT Script](https://assets.emqx.com/images/01fbf004ccd70d255d99c62eabe4c871.png)

<center>Scripts</center>

## 桌面端自动更新优化

在 1.9.4 版本中，我们对桌面端的自动更新功能进行了重要优化。新的自动更新功能可以预览新功能，并在更新过程中显示进度条，使得用户可以更清晰地了解更新内容和下载进度。

![Update Available](https://assets.emqx.com/images/dd3f581b80fdfafa43dafc63f02e1464.png)

<center>Update Available</center>

<br>

![Download Progress](https://assets.emqx.com/images/1f5f29fe8d12623915c7a52679655a7d.png)

<center>Download Progress</center>

## 命令行客户端功能增强

在 1.9.4 版本中，我们增强了命令行客户端的功能：

### **支持 MQTT over WebSocket 连接**

命令行客户端现在支持 MQTT over WebSocket 连接，这将有助于设计更灵活的测试场景。您可以使用以下命令来建立一个基于 WebSocket 的连接：

```
mqttx conn -h broker.emqx.io -p 8083 -l ws
```

此处的 `-l` 参数表示连接协议，其可选值包括 `mqtt`、`mqtts`、`ws`、`wss`，默认值为 `mqtt`。

### **支持发送多种格式的消息**

我们增加了在发布消息时指定数据格式的支持。目前，CLI 支持 Hex、JSON、Base64 等编码方式。例如，您可以使用以下命令发送 Hex 格式的消息：

```
mqttx pub -t testtopic/protobuf -h broker.emqx.io -m '7b0a 2020 2274 656d 7022 3a20 3331 2e35 2c0a 2020 2268 756d 223a 2032 300a 7d' --format hex
```

此处的 `--format` 参数用于指定消息的格式，其可选值包括 `base64`、`json`、`hex`。

## **网站全新升级**

本次升级还包括对官方网站 [mqttx.app](https://mqttx.app/zh) 的全面优化，更加直观地展示了 MQTTX 的功能和应用场景。

> 你的全功能 MQTT 客户端工具

![MQTT Client](https://assets.emqx.com/images/ee05da05ecf66c263fae0df84d918a6b.png)

<center>Overview</center>

## 其他功能优化及问题修复

我们对 MQTTX 的其他功能进行了一些优化和修复。具体包括：

- 对脚本功能进行了修改和优化：
  - 将原始脚本功能改为自定义函数。
  - 自定义函数中支持导入本地 JavaScript 文件。
  - 支持提示消息经过了何种脚本进行过处理。
- 修复了 web 版的右键菜单与浏览器默认事件冲突，提供更流畅的操作体验。
- 修复 bench 命令连接计数统计错误，以便更准确地了解当前连接状态。
- 已更新 MQTTX Web 的 Logo。
- 修复了重启客户端后保持选中上次连接的问题。
- CLI 优化了参数检查和错误处理。
- 修复了更新期间版本比较的问题。
- 提升用户界面（UI），优化消息框的显示宽度。

## 未来规划

- 将物联网场景数据模拟功能同步到桌面客户端中。
- 提升对于特殊数据格式（如 JSON）在显示消息框内的高亮显示。
- 编解码支持 Avro 的消息格式。
- 支持 Sparkplug B。
- 可配置忽略 QoS 0 的消息存储，以减少存储空间的占用。
- MQTT Debug 功能。
- 接收到的消息可以进行自动图表绘制。
- 插件功能（协议扩展 CoAP，MQTT-SN 等）。
- 脚本测试自动化（Flow）。



<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>
