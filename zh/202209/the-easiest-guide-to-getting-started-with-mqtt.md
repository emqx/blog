全球物联网正在高速发展，专门针对低带宽和不稳定网络环境的物联网应用设计的 MQTT 协议也因此得到广泛应用。

[MQTT](https://mqtt.org/) 是一种基于发布/订阅模式轻量级消息传输协议，具有简单易实现、支持 QoS、报文小等特点，非常适用于工业互联网、车联网、智能硬件、电力能源等领域。

本文将通过讲解与演示向读者展示 MQTT 协议的入门使用流程，物联网及 MQTT 初学者可以通过本文以更简单的方式理解 MQTT 相关概念，快速开始 MQTT 服务及应用的开发。

## MQTT 连接

在使用 MQTT 协议进行通信之前，需要先建立一个 MQTT 连接，连接由客户端向服务器端发起。

### MQTT 客户端

任何运行了 MQTT 客户端库的程序或设备都是一个 MQTT 客户端，例如：使用了 MQTT 的即时通讯 APP 是一个客户端，使用 MQTT 上报数据的各种传感器设备是一个客户端，以及各种 MQTT 测试工具也是一个客户端。

目前，基本所有的编程语言都有成熟的开源 MQTT 客户端库，读者可参考 EMQ 整理的 [MQTT 客户端库大全](https://www.emqx.com/zh/mqtt-client-sdk)选择一个合适的客户端库来构建满足自身业务需求的 MQTT 客户端。也可直接访问 EMQ 提供的 [MQTT 客户端编程](https://www.emqx.com/zh/blog/tag/mqtt-%E5%AE%A2%E6%88%B7%E7%AB%AF%E7%BC%96%E7%A8%8B)系列博客，学习如何在 Java、Python、PHP、Node.js 等编程语言中使用 MQTT。

本次演示我们将使用由 MQTT X 提供的支持浏览器访问的在线 MQTT 客户端：[http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client)。MQTT X 是目前开源客户端中 GitHub Star 数最多的，它同时也提供了桌面客户端（[https://mqttx.app/zh](https://mqttx.app/zh)）与命令行客户端（[https://mqttx.app/zh/cli](https://mqttx.app/zh/cli)），感兴趣的读者可自行下载使用。

### MQTT 服务器

MQTT 服务器负责接收客户端发起的连接，并将客户端发送的消息转发到另外一些符合条件的客户端。一个成熟的 MQTT 服务器可支持海量的客户端连接及百万级的消息吞吐，帮助物联网业务提供商专注于业务功能并快速创建一个可靠的 MQTT 应用。

MQTT 服务器一般有私有部署、全托管云服务、公共在线三种形式。

- 私有部署需要自行搭建与维护服务器，适合接入量较大、且有技术团队支持的公司。

  读者若是希望搭建私有 MQTT 服务器进行测试，可运行如下 Docker 命令直接安装 EMQX 开源版。

  ```
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  ```

  也可参考博客[如何在 Ubuntu 上安装 EMQX MQTT 服务器](https://www.emqx.com/zh/blog/how-to-install-emqx-mqtt-broker-on-ubuntu)进行安装。

- 全托管云服务免除了企业维护基础设施的负担，简单几步就能轻松开启 MQTT 服务。如下图，EMQX Cloud 支持按连接创建 MQTT 服务，且可选择部署在多个云平台。

   ![MQTT Cloud](https://assets.emqx.com/images/71a7d845d76b5d298a64d395fc8d1ad7.png)

- 公共的在线服务器一般由各个 MQTT 服务器的所属商业公司所提供，主要用来做 MQTT 流程测试。

本次演示我们将使用由 EMQ 提供的[公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务器基于[全托管的 MQTT 云服务 - EMQX Cloud](https://www.emqx.com/zh/cloud) 创建，服务器信息如下：

- Broker： `broker.emqx.io`
- TCP Port： `1883`
- Websocket Port： `8083`

### 创建连接

接下来我们开始正式创建一个 MQTT 连接，使用浏览器访问 [http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client)，然后点击页面中间的 ` New Connection` 按钮，将会看到如下页面。

![创建 MQTT 连接](https://assets.emqx.com/images/5e110d181ce8489c275d5674910fa16d.png)

各个连接的参数的意义如下：

- **Name**：为该在线客户端特有，只是一个区分不同连接的名称，与连接的建立无关系。使用代码连接时没有该参数。
- **Client ID**：服务端使用 Client ID 识别客户端，连接服务端的每个客户端都必须要有唯一的 Client ID。
- **Host**：为连接的服务器地址及协议，协议一般有 4 种：基于普通 TCP 的 MQTT、基于 SSL/TLS 的 MQTT、基于 WebSocket 的 MQTT，基于加密 WebSocket 的 MQTT。本文使用的在线工具基于浏览器运行，所以只能选择 ws 或 wss 协议。
- **Port**：连接的服务器端口。
- **Path**：选 ws 或 wss 协议时需要填写，EMQX 服务器默认为 `/mqtt`。
- **Username，Password**：MQTT 可以通过发送用户名和密码来进行相关的认证和授权，但是，如果此信息未加密，则用户名和密码是以明文的方式发送的。
- **Connect Timeout**：连接超时时间，连接在多少秒内未成功则不再继续连接。
- **Keep Alive**：保活周期，是一个以秒为单位的时间间隔。客户端在无报文发送时，将按 Keep Alive 设定的值定时向服务端发送心跳报文，确保连接不被服务端断开。更多细节可查看博客：[MQTT 协议中的 Keep Alive 机制](https://www.emqx.com/zh/blog/mqtt-keep-alive)。
- **Clean Session**：清除会话，为 `false` 时表示创建一个持久会话，在客户端断开连接时，会话仍然保持并保存离线消息，直到会话超时注销。否则表示创建一个新的临时会话，在客户端断开时，会话自动销毁。
- **Auto Reconnect**：自动重连，几乎所有客户端库都实现了自动重连。如果设置了自动重连，当网络不佳连接被断开后，客户端将自动重新发起连接。
- **MQTT Version**：MQTT 版本，建议使用 5.0。MQTT 5.0 是为适应迅速增长的设备数量与企业需求而全面更新的一个版本，其在 3.1.1 版本基础上增加了会话/消息延时、原因码、主题别名、用户属性、共享订阅等更加符合现代物联网应用需求的特性。更多 MQTT 5.0 详细信息可查看 EMQ 提供的 [MQTT 5.0 专题系列](https://www.emqx.com/zh/mqtt/mqtt5)文章。

我们在 `Name` 里输入 `Simple Demo`，并点击右上角的 `Connect` 按钮即可创建一个 MQTT 连接，如下表示连接建立成功。

![MQTT 连接成功](https://assets.emqx.com/images/9583db03a552b24980cf49005e3dc668.png)

## 发布与订阅

连接成功后，客户端就能进行消息的收发，在消息收发前我们需要先理解发布/订阅模式。

### 发布/订阅模式

发布订阅模式区别于传统的客户端-服务器模式，它使发送消息的客户端（发布者）与接收消息的客户端（订阅者）分离，发布者与订阅者不需要建立直接联系。我们既可以让多个发布者向一个订阅者发布消息，也可以让多个订阅者同时接收一个发布者的消息，它的精髓在于由一个被称为代理（MQTT 服务器）的中间角色负责所有消息路由和分发的工作。

下图为 MQTT 的发布/订阅流程：温度传感器作为一个客户端连接至 MQTT 服务器后，即可向某个主题（比如 `Temperature`）发布温度消息，服务器收到该消息后会将消息转发至订阅了 `Temperature` 主题的客户端（比如下图的手机、浏览器等应用）。

![发布/订阅模式](https://assets.emqx.com/images/a6baf485733448bc9730f47bf1f41135.png)

### 主题（Topic）

MQTT 协议基于主题进行消息路由，主题类似 URL 路径，例如：

```
chat/room/1

sensor/10/temperature

sensor/+/temperature    
```

主题通过 `/` 分割层级，支持 `+`， `#` 通配符:

- `+`：表示通配一个层级，例如 `a/+` 匹配 `a/x`， `a/y`

- `#`：表示通配多个层级，例如 `a/#` 匹配 `a/x`，`a/b/c/d`

更多关于 MQTT 主题的介绍可查看博客：[MQTT 主题的高级特性](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)。

### 消息服务质量（QoS）

MQTT 协议提供了 3 种消息服务质量等级（Quality of Service），它保证了在不同的网络环境下消息传递的可靠性。

- QoS 0：消息最多传递一次。

  如果当时客户端不可用，则会丢失该消息。发布者发送一条消息之后，就不再关心它有没有发送到对方，也不设置任何重发机制。

- QoS 1：消息传递至少 1 次。

  包含了简单的重发机制，发布者发送消息之后等待接收者的 ACK，如果没收到 ACK 则重新发送消息。这种模式能保证消息至少能到达一次，但无法保证消息重复。

- QoS 2：消息仅传送一次。

  设计了重发和重复消息发现机制，保证消息到达对方并且严格只到达一次。

更多关于 MQTT QoS 的介绍可查看博客：[MQTT QoS 服务质量介绍](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)。

### 订阅主题

接下来我们模拟温度传感器场景，在之前创建的 Simple Demo 连接里订阅所有的温度传感器上报的温度数据，即订阅通配符主题 `sensor/+/temperature`。

如下图，点击按钮 `New Subscription`，在弹出框的 Topic 下面输入主题 `sensor/+/temperature`，QoS 保持默认 0 不变。

> Color 字段可修改订阅标签的颜色，Alias 字段可修改订阅主题的显示名称。这两个字段为该在线客户端特有，使用代码连接时无此参数。

![订阅 MQTT 主题](https://assets.emqx.com/images/79321fd9e22058e27a256152b60908d6.png)

订阅成功后即可看到中间的订阅列表里多了一条记录。

![主题订阅成功](https://assets.emqx.com/images/3687ba334049a0ca19e3300a2cbc4a98.png)

### 发布消息

接下来我们点击最左侧的 `+` 按钮分别创建 `Sensor 1` 和 `Sensor 2` 两个连接，模拟两个温度传感器。

![创建 MQTT 连接](https://assets.emqx.com/images/0c96ec70a51ecc605bad4972edd77fb1.png)

连接创建好后如下图所示，将会看到 3 个连接，并且连接左侧的在线状态圆点都为绿色（绿色说明连接成功）。

![连接创建成功](https://assets.emqx.com/images/70010ba4da8d452ab0f738d36013dd9a.png)

选中 Sensor 1 连接，在页面右下部分输入发布主题 `sensor/1/temperature`，消息框内输入如下 JSON 格式消息，并点击右侧最底部的发布按钮发送消息。

```
{
  "msg": "17.2"
}
```

![发布 MQTT 消息](https://assets.emqx.com/images/859966556e5649f1d6ec9bf378162def.png)

如下表示消息发送成功。

![消息发布成功](https://assets.emqx.com/images/b1a46d8a415603d87e0c4244ee34bc02.png)

使用同样的步骤，在 Sensor 2 连接里向 `sensor/2/temperature` 主题发布如下 JSON 消息。

```
{
  "msg": "18.2"
}
```

将会看到 Simple Demo 连接收到 2 条新消息。

![消息通知](https://assets.emqx.com/images/f815767a47f234424ae55ea0fe39eb04.png)

点击 Simple Demo 连接，将会看到两个传感器发送的两条消息。

![收到两条 MQTT 消息](https://assets.emqx.com/images/f88de809773829f6a86dcedc2f612dd5.png)


## MQTT 重要特性演示

### 保留消息（Retained Message）

MQTT 客户端向服务器发布消息时，可以设置保留消息标志。一个主题下最新一条保留消息会驻留在消息服务器，后来的订阅者订阅主题时仍可以接收该消息。

如下图，我们在 Sensor 1 连接里向 `retained_message` 主题发送两条不一样的消息，且发送消息时勾选 `Retain` 选项。

![MQTT 保留消息](https://assets.emqx.com/images/5c7dcb078d223e0b6d33cb66241caa5d.png)

然后，我们再在 Simple Demo 连接里订阅 `retained_message` 主题，订阅成功后将会收到 Sensor 1 发送的第二条保留消息，由此可见服务器只会保存一个主题下最后一条保留消息。

![MQTT 保留消息](https://assets.emqx.com/images/afe8cca62d576404d5f622f362ef3592.png)

### 清除会话（Clean Session）

一般情况下 MQTT 客户端仅能接收到在线时其他客户端发布的消息，如果客户端离线再上线后将收不到离线期间的消息。但是当客户端使用固定的 Client ID，且连接参数 Clean Session 为 false 时，客户端离线后消息服务器可以为客户端保持一定量的离线消息，并在客户端再次上线后发送给客户端（且为客户端恢复下线前的订阅信息）。

本次演示使用的公共 MQTT 服务器设置的离线消息保存时间为 5 分钟，最大消息数为 1000 条，且不保存 QoS 0 消息。接下来我们创建一个  MQTT 3.1.1 版本的连接，并验证 QoS 1 情况下的离线会话。

> MQTT 5 中使用 Clean Start 与 Session Expiry Interval 改进了 Clean Session，详情可查看博客：[Clean Start 与 Session Expiry Interval](https://www.emqx.com/zh/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)。

如下图，创建一个名为 `MQTT V3` 的连接，Clean Session 设置为 false，MQTT 版本选择 3.1.1。

![MQTT 清除会话](https://assets.emqx.com/images/1472ce0ea8e728647d973cae56e6b1d5.png)

连接成功后订阅 `clean_session_false` 主题，且 QoS 设置为 1。

![订阅 MQTT 主题](https://assets.emqx.com/images/7a5792040185d956803cb7406b2df3af.png)

订阅成功后，点击右上角的断开连接按钮。

![断开 MQTT 连接](https://assets.emqx.com/images/fd5726bd0e2a5b9d9d73a7095f322ecf.png)

接下来创建一个名为 `MQTT_V3_Publish` 的连接，MQTT 版本同样设置为 3.1.1，连接成功后向 `clean_session_false` 主题发布三条消息。

![发布 MQTT 消息](https://assets.emqx.com/images/0659785e98cb03f9d6e78497e0adb26f.png)

然后选中 MQTT_V3 连接，点击连接按钮连接至服务器，将会成功接收到 3 条离线期间的消息。

![MQTT 离线消息](https://assets.emqx.com/images/106cc289cbb3a07be2ed294dd97fe420.png)

### 遗嘱消息（Last Will）

MQTT 客户端向服务器发起连接请求时，可以设置是否发送遗嘱消息（Will Message）标志，和遗嘱消息主题（Topic）与内容（Payload）。设置了遗嘱消息消息的 MQTT 客户端异常下线时（客户端断开前未向服务器发送 DISCONNECT 消息），MQTT 消息服务器会发布该客户端设置的遗嘱消息。

更多关于遗嘱消息的介绍可查看博客：[MQTT 遗嘱消息（Will Message）的使用](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)。

如下图，我们创建一个名为 `Last Will` 的连接。

- 为了能快速看到效果，我们设置 Keep Alive 为 5 秒
- Last-Will Topic 设置为 `last_will`
- Last-Will QoS 设置为 `1`
- Last-Will Retain 设置为 `true`
- Last-Will Payload 设置为 `offline`

![MQTT 遗嘱消息](https://assets.emqx.com/images/3fc9e2c463bd38c21dc7f523520c7076.png)

连接成功后，我们断开电脑网络 5 秒钟以上（模拟客户端异常下线），再打开网络。然后启动 Simple Demo 连接，并订阅 `last_will` 主题，将会收到 `Last Will` 连接设置的遗嘱消息。

![MQTT 遗嘱消息](https://assets.emqx.com/images/a216808a1ba964bbddc75708bc55c072.png)


至此，我们完成了对 MQTT 相关基础概念及其使用流程的讲解与演示，读者可以根据本文所学尝试上手使用 MQTT 协议。接下来读者可访问 EMQ 提供的 [MQTT 客户端编程](https://www.emqx.com/zh/blog/tag/mqtt-客户端编程)系列博客，学习如何在 Java、Python、PHP、Node.js 等编程语言中使用 MQTT，开始 MQTT 应用及服务开发，探索 MQTT 的更多高级应用。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
