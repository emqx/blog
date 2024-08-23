## MQTT 有效载荷简介

MQTT 有效载荷是指 MQTT 消息中包含的实际数据。尽管 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)对有效载荷的格式没有硬性要求，并且允许传输任何形式的二进制数据，但在实际应用中，我们通常会使用一些常见的数据格式，如 JSON、二进制、十六进制和 Protobuf。

理解有效载荷的格式及其处理方法至关重要，因为它们构成了物联网生态系统中设备之间信息交换的核心内容。在本文中，我们将探讨如何使用 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 和 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)来传输和处理这些数据格式。

如果您想进一步了解 MQTT 有效载荷的相关内容，可以参考这篇文章：[Payload Format Indicator 和 Content Type 介绍与示例 ｜ MQTT 5.0 特性详解](https://www.emqx.com/zh/blog/mqtt5-new-features-payload-format-indicator-and-content-type) 

## MQTT 中常见的消息传输数据格式

### 纯文本

纯文本是最简单的数据格式，常用于传输简单的文本信息，如即时消息、通知等。例如：

```
你好，这是一段纯文本。
```

### JSON

JSON（JavaScript Object Notation）是一种轻量级的数据交换格式。它既易于机器解析和生成，又便于人类阅读和编写，通常用于描述对象或事件。例如：

```json
{"temperature": "22.1"}
```

### 原始二进制数据

原始二进制数据是指不适合人类直接阅读的数据格式。它由二进制数字序列（0 和 1）组成，用于表示文本、图像、音频、视频或其他类型的数据。这些数据通常以二进制形式存储在计算机的内存或存储设备中。通常，我们使用十六进制来表示原始二进制数据。例如，字符串 `aaa` 的原始二进制形式为：

```
0x616161
```

### 十六进制字符串

十六进制字符串是一种将二进制数据以十六进制字符表示的方法。例如，字符串 `aaa` 的十六进制表示为 `616161`。十六进制字符串常用于编码原始二进制数据，使其转换为更易读、易打印的形式。

### Protobuf

协议缓冲区（Protobuf）是一种免费开源的跨平台数据格式，用于将结构化数据序列化。它在开发需要通过网络通信的程序或存储数据时特别有用。例如，以下是一个消息模式的定义：

```protobuf
message Sensor {
  required int32 temperature = 1;
}
```

那么表示温度为 22 的二进制 Protobuf 消息为：

```
0816
```

## 使用不同格式发送和接收数据

### 环境配置

#### MQTT Broker

EMQX 是一款功能强大且高度可扩展的 MQTT Broker，专为物联网和实时消息传输设计。

在本文中，我们将使用 Docker 在本地安装 EMQX 5.6.1 来进行演示：

```shell
docker run  --rm -p 18083:18083 -p 1883:1883  emqx/emqx:5.6.1
```

安装完成后，打开浏览器访问 `http://127.0.0.1:18083`，进入 EMQX Dashboard，默认的用户名为 `admin`，密码为 `public`：

![EMQX Dashboard](https://assets.emqx.com/images/91a20129ce36884aad71803f3770f104.png)

#### MQTT 客户端

为了进行测试，我们推荐使用 MQTTX CLI 作为 MQTT 客户端。[**MQTTX**](https://mqttx.app/zh) 是由 EMQ 开发的开源跨平台 MQTT 5.0 桌面客户端，适用于 macOS、Linux 和 Windows。

您可以从[此处](https://mqttx.app/)获取 MQTTX CLI。

以 MacOS 为例，安装 MQTTX CLI 的命令如下：

```shell
brew install emqx/mqttx/mqttx-cli
```

安装完成后，可以通过以下命令测试是否能够成功连接到本地的 EMQX：

```shell
mqttx conn -h 127.0.0.1 -p 1883
```

如果连接成功，您将看到类似以下的输出：

![Connect to the local EMQX](https://assets.emqx.com/images/7d35c1562c1f4aa48dd3aaeebff6cfce.png)

### 发送和接收消息

MQTT 消息的有效载荷可以采用任何字符串或二进制格式。我们可以使用 MQTTX CLI 创建一个名为 `sub` 的订阅者，并订阅 `test/sub` 主题：

```shell
mqttx sub -h 127.0.0.1 -p 1883 -i sub -t test/sub
```

然后，向 `test/sub` 主题发布一条简单消息：

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/sub -m 'Hi, plaintext payload'
```

在订阅者端，我们可以看到成功收到该消息：

![received message](https://assets.emqx.com/images/966758dfbbc63319065da3c4dde64edd.png)

#### 有效载荷的 Content-Type 字段

在 MQTT 5.0 协议中，引入了 `Content-Type` 字段，用于标识有效载荷的格式（参见：[Content Type in PUBLISH message](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901118)）。

因此，在发布消息时，可以使用该字段来明确描述有效载荷的格式：

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/sub -m 'Hi, plaintext payload' --content-type 'plain/text'
```

这样，订阅者在接收到消息时，会看到对应的内容类型设置：

![plain/text message](https://assets.emqx.com/images/c8ee52162ed750baf01eeeac083f6972.png)

#### JSON 格式的有效载荷

[**JSON**](https://www.json.org/json-en.html) 是一种轻量级的数据交换格式，既易于人类读写，也易于机器解析和生成。

我们通过 MQTTX CLI 发送 JSON 格式的消息，操作方式与发送纯文本消息类似。

请注意：`--format` 参数用于告知 MQTTX CLI 输入的有效载荷是 JSON 字符串，并进行合法性验证：

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/sub \\
  --content-type 'application/json' \\
  --format json \\
  -m '{"key": "value"}'
```

消息发布成功后，输出如下：

![JSON message](https://assets.emqx.com/images/f4fb2894acb3a1618025ddb8aa85cf9f.png)

#### 十六进制字符串格式的有效载荷

[十六进制](https://en.wikipedia.org/wiki/Hexadecimal)字符串是一种将二进制数据表示为十六进制数字的格式，每个字节使用两位十六进制数字表示。这种格式更易于人类阅读，常用于编程和数据通信。

在 MQTT 中，十六进制字符串可以像普通字符串一样直接发送：

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/sub \\
  -m '31310000ffff'
```

发布后，输出如下所示：

![Hex String message](https://assets.emqx.com/images/ab83426ae3328095d34b650d85948d01.png)

#### 二进制格式的有效载荷

根据 MQTT 协议的定义，有效载荷的格式没有限制，这意味着它可以是任何类型的二进制数据。

使用 MQTTX CLI，可以通过 `--format hex` 选项发送二进制数据。例如：

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/sub \\
--format hex \\
-m '31 31 00 00 ff ff'
```

以下截图显示接收方将二进制数据解码为 `11��`，因为 `0x31` 对应的是字符 `1` 的编码：

![Binary format message](https://assets.emqx.com/images/ea6a05c3ce2225e21d4ab90a700055c6.png)

## 使用 EMQX 规则引擎处理 JSON 格式的有效载荷

EMQX 提供了强大的规则引擎，能够方便地处理和解析各种格式的有效载荷。了解更多信息，请访问 [EMQX 规则引擎](https://docs.emqx.com/zh/enterprise/latest/data-integration/rules.html)。

对于 JSON 格式的有效载荷，EMQX 规则引擎能够提取和操作其中的字段。以下是使用 EMQX 规则引擎处理 JSON 有效载荷的具体步骤。

### 创建规则和操作

您可以在 EMQX Dashboard 中添加以下规则来提取 JSON 字段：

```sql
SELECT
  payload.temperature as t
FROM
  "test/msg_in"
```

此规则的作用是从 `test/msg_in` 主题的消息有效载荷中解析并提取 `temperature` 字段，并将其重命名为 `t`。

接下来，为该规则添加一个 `Republish` 操作，将重组后的 JSON 数据重新发布到 `test/msg_out` 主题。

以下是添加规则和操作的过程：

![Add the Rule and Action](https://assets.emqx.com/images/3ab8c91a8e3cf62c5eec87b654917621.png)

`Republish` 操作的参数设置如下：

![The Republish Action parameters](https://assets.emqx.com/images/ece20aa554ae0a6b54c454f78f9d73d7.png)

### 使用 MQTTX CLI 测试

创建规则后，我们可以使用 MQTTX CLI 对其进行验证。首先，使用以下命令订阅 `test/msg_out` 主题：

```shell
mqttx sub -h 127.0.0.1 -p 1883 -i sub -t test/msg_out -v
```

然后，发布一条 JSON 格式的消息 `{"temperature": 23.5, "altitude": 100}` 到 `test/msg_in` 主题：

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/msg_in \\
  --format json \\
  -m '{"temperature": 23.5, "altitude": 100}'
```

在订阅者的输出中，我们可以看到 `test/msg_out` 收到的消息，其中 JSON 消息的 `temperature` 字段被成功提取并重新格式化为 `{"t": 23.5}`：

![Test with MQTTX CLI](https://assets.emqx.com/images/e49e555c12ca620145ecdfd31f98dad9.png)

## Q&A

### **哪种数据格式最适合我的应用？**

选择数据格式应基于您的具体应用需求。例如，如果您需要一种易于人类阅读的格式，并且带宽不是问题，那么 JSON 可能是最好的选择。但如果带宽有限，则可能更适合使用更紧凑的格式，如二进制或十六进制。如果您希望在结构化数据和效率之间取得平衡，同时可以接受一定的复杂性，那么 Protobuf 可能是最合适的选择。

### **能否用 MQTT 有效载荷发送图片或其他大文件？**

虽然技术上可以通过 MQTT 有效载荷发送图片或其他大文件，但通常不建议这样做。MQTT 设计用于传输小型、高频的消息，发送大文件可能导致网络拥塞或其他问题。

### **MQTT 有效载荷最大是多少？**

MQTT 有效载荷的最大大小为 256 MB。然而，出于网络性能和效率的考虑，通常建议将有效载荷大小控制在 1 MB 以下。

### **可以加密 MQTT 有效载荷吗？**

可以，您可以在发送前对 MQTT 有效载荷进行加密，并在接收时解密。这为传输敏感数据提供了额外的安全保护。不过，您需要在发送和接收消息过程中分别进行加密和解密操作。

## 结语

总而言之，MQTT 为物联网设备之间以多种格式传输数据提供了极大的灵活性。有效载荷数据格式的选择应根据应用的具体需求，如网络带宽、人类可读性以及数据结构的复杂性。通过深入了解这些不同的格式及其在 MQTT 中的处理方式，开发人员可以优化物联网解决方案的效率和性能。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
