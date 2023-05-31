本文是 MQTT 协议的入门指南，提供了实用的代码示例。物联网和 MQTT 的初学者可以通过本文掌握 MQTT 的基本概念，快速开启 MQTT 服务和应用的开发。

## 什么是 MQTT？

MQTT（Message Queuing Telemetry Transport）是一种轻量级、基于发布-订阅模式的消息传输协议，适用于资源受限的设备和低带宽、高延迟或不稳定的网络环境。它在物联网应用中广受欢迎，能够实现传感器、执行器和其它设备之间的高效通信。

## 为什么 MQTT 是适用于物联网的最佳协议？

MQTT 所具有的适用于物联网特定需求的特点和功能，使其成为物联网领域最佳的协议之一。它的主要特点包括：

- **轻量级：**物联网设备通常在处理能力、内存和能耗方面受到限制。MQTT 开销低、报文小的特点使其非常适合这些设备，因为它消耗更少的资源，即使在有限的能力下也能实现高效的通信。
- **可靠：**物联网网络常常面临高延迟或连接不稳定的情况。MQTT 支持多种 QoS 等级、会话感知和持久连接，即使在困难的条件下也能保证消息的可靠传递，使其非常适合物联网应用。
- **安全通信：**安全对于物联网网络至关重要，因为其经常涉及敏感数据的传输。为确保数据在传输过程中的机密性，MQTT 提供传输层安全（TLS）和安全套接层（SSL）加密功能。此外，MQTT 还通过用户名/密码凭证或客户端证书提供身份验证和授权机制，以保护网络及其资源的访问。
- **双向通信：**MQTT 的发布-订阅模式为设备之间提供了无缝的双向通信方式。客户端既可以向主题发布消息，也可以订阅接收特定主题上的消息，从而实现了物联网生态系统中的高效数据交换，而无需直接将设备耦合在一起。这种模式也简化了新设备的集成，同时保证了系统易于扩展。
- **连续、有状态的会话：**MQTT 提供了客户端与 Broker 之间保持有状态会话的能力，这使得系统即使在断开连接后也能记住订阅和未传递的消息。此外，客户端还可以在建立连接时指定一个保活间隔，这会促使 Broker 定期检查连接状态。如果连接中断，Broker 会储存未传递的消息（根据 QoS 级别确定），并在客户端重新连接时尝试传递它们。这个特性保证了通信的可靠性，降低了因间断性连接而导致数据丢失的风险。
- **大规模物联网设备支持：**物联网系统往往涉及大量设备，需要一种能够处理大规模部署的协议。MQTT 的轻量级特性、低带宽消耗和对资源的高效利用使其成为大规模物联网应用的理想选择。通过采用发布-订阅模式，MQTT 实现了发送者和接收者的解耦，从而有效地减少了网络流量和资源使用。此外，协议对不同 QoS 等级的支持使得消息传递可以根据需求进行定制，确保在各种场景下获得最佳的性能表现。
- **语言支持：**物联网系统包含使用各种编程语言开发的设备和应用。MQTT 具有广泛的语言支持，使其能够轻松与多个平台和技术进行集成，从而实现了物联网生态系统中的无缝通信和互操作性。您可以阅读我们的 [MQTT 客户端编程](https://www.emqx.com/zh/blog/category/mqtt-programming)系列文章，学习如何在 PHP、Node.js、Python、Golang、Node.js 等编程语言中使用 MQTT。

## MQTT 的工作原理

要了解 MQTT 的工作原理，首先需要掌握以下几个概念：MQTT 客户端、MQTT Broker、发布-订阅模式、主题、QoS。

**MQTT 客户端**

任何运行 [MQTT 客户端库](https://www.emqx.com/zh/mqtt-client-sdk)的应用或设备都是 MQTT 客户端。例如，使用 MQTT 的即时通讯应用是客户端，使用 MQTT 上报数据的各种传感器是客户端，各种 [MQTT 测试工具](https://www.emqx.com/zh/blog/mqtt-client-tools)也是客户端。

**MQTT Broker**

MQTT Broker 是负责处理客户端请求的关键组件，包括建立连接、断开连接、订阅和取消订阅等操作，同时还负责消息的转发。一个高效强大的 MQTT Broker 能够轻松应对海量连接和百万级消息吞吐量，从而帮助物联网服务提供商专注于业务发展，快速构建可靠的 MQTT 应用。

关于 MQTT Broker 的更多详情，请参阅文章 [2023 年最全面的 MQTT Broker 比较指南](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)。

**发布-订阅模式**

发布-订阅模式与客户端-服务器模式的不同之处在于，它将发送消息的客户端（发布者）和接收消息的客户端（订阅者）进行了解耦。发布者和订阅者之间无需建立直接连接，而是通过 MQTT Broker 来负责消息的路由和分发。

下图展示了 MQTT 发布/订阅过程。温度传感器作为客户端连接到 MQTT Broker，并通过发布操作将温度数据发布到一个特定主题（例如 `Temperature`）。MQTT Broker 接收到该消息后会负责将其转发给订阅了相应主题（`Temperature`）的订阅者客户端。

![MQTT 发布-订阅模式](https://assets.emqx.com/images/a6baf485733448bc9730f47bf1f41135.png)

**主题**

MQTT 协议根据主题来转发消息。主题通过 `/` 来区分层级，类似于 URL 路径，例如：

```
chat/room/1

sensor/10/temperature

sensor/+/temperature
```

MQTT 主题支持以下两种通配符：`+` 和 `#`。

- `+`：表示单层通配符，例如 `a/+` 匹配 `a/x` 或 `a/y`。
- `#`：表示多层通配符，例如 `a/#` 匹配 `a/x`、`a/b/c/d`。

> **注意**：通配符主题只能用于订阅，不能用于发布。


关于 MQTT 主题的更多详情，请参阅文章[通过案例理解 MQTT 主题与通配符](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)。

**QoS**

MQTT 提供了三种服务质量（QoS），在不同网络环境下保证消息的可靠性。

- QoS 0：消息最多传送一次。如果当前客户端不可用，它将丢失这条消息。
- QoS 1：消息至少传送一次。
- QoS 2：消息只传送一次。

关于 MQTT QoS 的更多详情，请参阅文章 [MQTT QoS 0, 1, 2 介绍](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)。

## MQTT 的工作流程

在了解了 MQTT 的基本组件之后，让我们来看看它的一般工作流程：

1. **客户端使用 TCP/IP 协议与 Broker 建立连接**，可以选择使用 TLS/SSL 加密来实现安全通信。客户端提供认证信息，并指定会话类型（Clean Session 或 Persistent Session）。
2. **客户端既可以向特定主题发布消息，也可以订阅主题以接收消息**。当客户端发布消息时，它会将消息发送给 MQTT Broker；而当客户端订阅消息时，它会接收与订阅主题相关的消息。
3. **MQTT Broker 接收发布的消息**，并将这些消息转发给订阅了对应主题的客户端。它根据 QoS 等级确保消息可靠传递，并根据会话类型为断开连接的客户端存储消息。

## 开始使用 MQTT：快速教程

下面我们将通过一些简单的示例来展示如何使用 MQTT。在开始之前，需要准备 MQTT Broker 和 MQTT 客户端。

### 准备 MQTT Broker

您可以选择私有部署或完全托管的云服务来建立自己的 MQTT Broker。或者您也可以使用免费的公共 Broker。

- **私有部署**

  [EMQX](https://www.emqx.io/zh) 是最具扩展性的开源 MQTT Broker，适用于物联网、工业物联网和车联网。您可以运行以下 Docker 命令来安装 EMQX。

  ```
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  
  ```

- **全托管的云服务**

  通过全托管的云服务启动 MQTT 服务是最便捷的方式。如下图所示，[EMQX Cloud](https://www.emqx.com/zh/cloud) 可以在几分钟内启动，并在 AWS、Google Cloud 和 Microsoft Azure 的 17 个区域提供运行支持。

  ![EMQX MQTT Cloud](https://assets.emqx.com/images/d019e0dbc27f706eca6256e11720eb9b.png)

- **免费的公共 MQTT Broker**

  在本文中，我们将使用 EMQ 提供的[免费公共 MQTT Broker](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，它基于完全托管的 [MQTT 云服务 - EMQX Cloud](https://www.emqx.com/zh/cloud) 创建。服务器信息如下：

  >Server: `broker.emqx.io`
  >
  >TCP Port: `1883`
  >
  >WebSocket Port: `8083`
  >
  >SSL/TLS Port: `8883`
  >
  >Secure WebSocket Port: `8084`

### 准备 MQTT 客户端

在本文中，我们将使用 [MQTTX](https://mqttx.app/zh) 提供的支持浏览器访问的 MQTT 客户端工具，访问地址为 [http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client) 。 MQTTX 还提供了[桌面客户端](https://mqttx.app/zh)和[命令行工具](https://mqttx.app/zh/cli)。

[MQTTX](https://mqttx.app/zh) 是一款跨平台的 MQTT 5.0 桌面客户端，可在 macOS、Linux、Windows 操作系统上运行。其用户友好的聊天式界面使用户能够轻松创建多个 MQTT/MQTTS 连接，并进行 MQTT 消息的订阅和发布。

![MQTTX](https://assets.emqx.com/images/ada10fb84b685af3cadcae6c95197c4f.gif)

<center>MQTTX 界面</center>

目前，各种编程语言都拥有成熟的开源 MQTT 客户端库。我们在[流行的 MQTT 客户端库和 SDK](https://www.emqx.com/zh/mqtt-client-sdk) 中精选了多个编程语言的 MQTT 客户端库，并提供了详细的代码示例，旨在帮助您快速了解 MQTT 客户端的使用。

### 创建 MQTT 连接

在使用 MQTT 协议进行通信之前，客户端需要创建一个 MQTT 连接来连接到 Broker。

在浏览器中打开 [http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client) , 点击页面中间的 `New Connection` 按钮，将看到如下页面。

![创建 MQTT 连接](https://assets.emqx.com/images/5e110d181ce8489c275d5674910fa16d.png)

 

我们在 `Name` 中输入 `Simple Demo`，然后点击右上角的 `Connect` 按钮，建立一个 MQTT 连接。如下图所示，表示连接成功。

![MQTT 连接成功](https://assets.emqx.com/images/9583db03a552b24980cf49005e3dc668.png)

 

要了解更多关于 MQTT 连接参数的内容，请查看我们的文章：[建立 MQTT 连接时如何设置参数](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)。

### 通过通配符订阅主题

接下来，我们在上面创建的 `Simple Demo` 连接中通过通配符订阅主题 `sensor/+/temperature`，这样就可以接收所有传感器发送的温度数据了。

如下图所示，点击 `New Subscription` 按钮，在弹出框中的 `Topic` 字段中输入主题 `sensor/+/temperature`，QoS 保持默认值 0。

![订阅 MQTT 通配符主题](https://assets.emqx.com/images/79321fd9e22058e27a256152b60908d6.png)

 

订阅成功后，会在订阅列表的中间看到新增了一条记录。

![MQTT 主题订阅成功](https://assets.emqx.com/images/3687ba334049a0ca19e3300a2cbc4a98.png)

 

### 发布 MQTT 消息

接下来，我们点击左侧菜单上的 `+` 按钮创建两个连接，分别命名为 `Sensor 1` 和 `Sensor 2`，用来模拟两个温度传感器。

![创建 MQTT 连接](https://assets.emqx.com/images/0c96ec70a51ecc605bad4972edd77fb1.png)

连接创建成功后，会看到三个连接，每个连接左侧的在线状态指示灯都是绿色的。

![三个连接创建成功](https://assets.emqx.com/images/70010ba4da8d452ab0f738d36013dd9a.png)

选择 `Sensor 1` 连接，在页面下方的发布主题中输入 `sensor/1/temperature`，在消息框中输入以下 JSON 格式的消息，然后点击右下方的发布按钮发送消息。

```
{
  "msg": "17.2"
}
```

![发布 MQTT 消息](https://assets.emqx.com/images/859966556e5649f1d6ec9bf378162def.png)

如下图所示，消息发送成功。

![MQTT 消息发布成功](https://assets.emqx.com/images/b1a46d8a415603d87e0c4244ee34bc02.png)

使用相同的步骤，在 `Sensor 2` 连接中发布以下 JSON 消息到 `sensor/2/temperature` 主题。

```
{
  "msg": "18.2"
}
```

您会看到 `Simple Demo` 连接收到两条新消息。

![2条消息提示](https://assets.emqx.com/images/f815767a47f234424ae55ea0fe39eb04.png)

点击 `Simple Demo` 连接，会看到两个传感器发送的两条消息。

![查看消息详情](https://assets.emqx.com/images/f88de809773829f6a86dcedc2f612dd5.png)

### MQTT 功能演示

#### 保留消息

当 MQTT 客户端向服务器发布消息时，可以设置保留消息标志。保留消息存储在消息服务器上，后续订阅该主题的客户端仍然可以收到该消息。

如下图所示，我们在 `Sensor 1` 连接中勾选 `Retain` 选项，然后向 `retained_message` 主题发送两条消息。

![MQTT Retain](https://assets.emqx.com/images/5c7dcb078d223e0b6d33cb66241caa5d.png)

接着，我们在 `Simple Demo` 连接中订阅 `retained_message` 主题。订阅成功后，会收到 `Sensor 1` 发送的第二条保留消息，这说明服务器只会为主题保留最近的一条保留消息。

![MQTT 保留消息](https://assets.emqx.com/images/afe8cca62d576404d5f622f362ef3592.png)

关于保留消息的更多细节，请阅读文章 [MQTT 保留消息初学者指南](https://www.emqx.com/zh/blog/mqtt5-features-retain-message)。

#### Clean Session

MQTT 客户端通常只能在在线状态下接收其它客户端发布的消息。如果客户端离线后重新上线，它将无法收到离线期间的消息。

但是，如果客户端连接时设置 Clean Session 为 false，并且使用相同的客户端 ID 再次上线，那么消息服务器将为客户端缓存一定数量的离线消息，并在它重新上线时发送给它。

> 本次演示使用的公共 MQTT 服务器设置为缓存 5 分钟的离线消息，最大消息数为 1000 条，且不保存 QoS 0 消息。

下面，我们创建一个 MQTT 3.1.1 连接，并用 QoS 1 来演示 Clean Session 的使用。

> MQTT 5.0 中将 Clean Session 拆分成了 Clean Start 与 Session Expiry Interval。详情请参考文章 [Clean Start 与 Session Expiry Interval](https://www.emqx.com/zh/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)。

创建一个名为 `MQTT V3` 的连接，设置 Clean Session 为 false，选择 MQTT 版本为 3.1.1。

![设置 Clean Session 为 false](https://assets.emqx.com/images/1472ce0ea8e728647d973cae56e6b1d5.png)

连接成功后，订阅 `clean_session_false` 主题，并将 QoS 设置为 1。

![订阅 clean_session_false 主题](https://assets.emqx.com/images/7a5792040185d956803cb7406b2df3af.png)

订阅成功后，点击右上角的断开按钮，断开连接。

![断开 MQTT 连接](https://assets.emqx.com/images/fd5726bd0e2a5b9d9d73a7095f322ecf.png)

然后，创建一个名为 `MQTT_V3_Publish` 的连接，MQTT 版本也设置为 3.1.1。连接成功后，向 `clean_session_false` 主题发布三条消息。

![创建一个名为 MQTT_V3_Publish 的连接](https://assets.emqx.com/images/0659785e98cb03f9d6e78497e0adb26f.png)

接着，选择 `MQTT_V3` 连接，点击连接按钮重新连接到服务器，会收到三条离线消息。

![接收到三条离线消息](https://assets.emqx.com/images/106cc289cbb3a07be2ed294dd97fe420.png)

关于 Clean Session 的更多细节，请阅读文章 [MQTT Persistent Session 与 Clean Session 详解](https://www.emqx.com/zh/blog/mqtt-session)。

#### 遗嘱消息

MQTT 客户端在向服务器发起 CONNECT 请求时，可以选择是否发送遗嘱消息标志，并指定遗嘱消息的主题和有效载荷。

如果 MQTT 客户端异常离线（在断开连接前没有向服务器发送 DISCONNECT 消息），MQTT 服务器会发布遗嘱消息。

我们创建一个名为 `Last Will` 的连接来演示这个功能。

- 为了快速看到效果，我们把 Keep Alive 设置为 5 秒。
- Last-Will Topic 设置为 `last_will`。
- Last-Will QoS 设置为 `1`。
- Last-Will Retain 设置为 `true`。
- Last-Will Payload 设置为 `offline`。

![创建名为 Last Will 的连接](https://assets.emqx.com/images/3fc9e2c463bd38c21dc7f523520c7076.png)

连接成功后，我们断开电脑网络超过 5 秒（模拟客户端异常断开连接），然后再恢复网络。

接着启动 Simple Demo 连接，并订阅 `last_will` 主题。您会收到 `Last Will` 连接设置的遗嘱消息。

![收到 Last Will 连接设置的遗嘱消息](https://assets.emqx.com/images/a216808a1ba964bbddc75708bc55c072.png)

关于 MQTT 遗嘱消息的更多内容，请阅读文章 [MQTT 遗嘱消息的使用](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)。

## 深入学习 MQTT

本文详细介绍了 MQTT 的基本概念和使用流程，您可以按照本文所学的内容尝试使用 MQTT 协议。

如果您想了解更多 MQTT 的知识，建议您阅读 EMQ 提供的 [MQTT 教程：从入门到精通](https://www.emqx.com/zh/mqtt-guide)系列文章，了解 MQTT 主题、通配符、保留消息、遗嘱消息等功能。通过这些文章，您将能够探索 MQTT 的更高级应用场景，并开始进行 MQTT 应用和服务的开发。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
