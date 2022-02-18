近日，由 EMQ 开源的跨平台 MQTT 5.0 桌面测试客户端[ MQTT X 发布了最新版本 v1.7.0](https://www.emqx.com/zh/blog/mqttx-v-1-7-0-release-notes)。MQTT X 支持快速创建多个同时在线的 MQTT 客户端，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的连接、发布、订阅功能及其他 [MQTT 协议](https://www.emqx.com/zh/mqtt)特性。

新发布的 1.7.0 版本对 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 实现了更为全面的支持，是全球目前为止对 MQTT 5.0 支持最为完整的桌面测试客户端工具。同时新增了很多优化用户体验的功能。

在本文中，我们将详细介绍 MQTT X v1.7.0 新增功能的具体使用操作，特别是如何使用 MQTT X 来测试 MQTT 5.0 的诸多特性，以便读者可以在实际项目中更好地应用 MQTT 5.0。

## 准备 MQTT 消息服务器

在使用 MQTT X v1.7.0 对 MQTT 5.0 的特性进行测试之前，我们首先需要准备支持 MQTT 5.0 的 [MQTT Broker](https://www.emqx.io/zh)。

本文将使用由 [EMQX Cloud](https://www.emqx.com/zh/cloud) 提供的免费在线 MQTT 5.0 服务器配合 MQTT X 客户端进行测试。作为一款全托管的云原生 MQTT 5.0 消息服务，EMQX Cloud 可以在数分钟内快速创建一个 MQTT 服务，并且完整支持 MQTT 5.0 协议，也是全球首个全托管的 MQTT 5.0 公有云服务。

开始 30 天免费试用：[https://www.emqx.com/zh/cloud](https://www.emqx.com/zh/cloud) 

在测试开始前，免费在线的 MQTT 5.0 服务器服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

## MQTT 5.0 测试

### 用户属性

在 1.7.0 版本中，我们首先支持了用户属性的配置。[用户属性](https://www.emqx.com/zh/blog/mqtt5-user-properties)是 MQTT 5.0 中非常实用的一个特性，它是一种自定义属性，允许用户向 MQTT 消息添加自己的元数据，传输额外的自定义信息以扩充更多应用场景，比如实现消息的分发，文件传输，语言区分等。该功能与 HTTP 的 Header 的概念非常类似。我们可以在创建客户端连接和发布消息时进行用户属性的配置。

**客户端连接**

点击新建按钮，来到新建客户端的页面，首先我们需要选择 MQTT 的版本为 5.0，这样就可以看到下方出现了配置用户属性的卡片，卡片内是一个可以配置键值对的输入框，可以点击右上角的添加按钮，来增加用户属性配置，点击每一行末尾的删除按钮可以删除配置，最后输入需要配置的属性名称和内容即可。连接成功后，MQTT 服务器就可以获取到该客户端的用户属性内容。

![MQTT 连接时的用户属性](https://static.emqx.net/images/7e973abe8364e62413e56b7447dc3599.png)


**消息发布**

除了客户端连接时的用户属性配置外，该版本还支持配置发布消息时的用户属性。当新建连接为 MQTT 5.0 的客户端时，我们可以看到右下角的发布消息的区域出现了一个 `Meta` 按钮，点击该按钮即可出现配置发布时的属性的卡片，我们可以在卡片顶部看到用户属性配置。

![MQTT 发布时的用户属性](https://static.emqx.net/images/c58496f4c49176b8d791f8652405e73b.png)
 
当配置用户属性完成后，点击保存按钮，此时我们再输入 Topic 和 Payload 点击发送，可以看到发送的消息框内，包含了当前消息所包含的用户属性的内容，如果当我们接收到的消息也包含了用户属性时，我们在接收到的消息框内也可以看到客户端发送过来的用户属性配置。

![消息框内的用户属性](https://static.emqx.net/images/93f27cdf5831517109a58ed3de9c56f5.png) 

MQTT X 对于用户属性的支持，可以帮助开发者在测试和验证具有 MQTT 5.0 用户属性功能的应用场景时，对该功能进行快速验证和测试，从而提升开发和使用效率。

### 请求响应

在 1.7.0 版本中，支持了 MQTT 5.0 中的[请求响应](https://www.emqx.com/zh/blog/mqtt5-request-response)，提供对响应主题和对比数据属性的配置，控制响应消息被路由回请求的发布者。

因为 MQTT 协议是基于 Pub/Sub 模式的，区别于类似 HTTP 协议这样的请求响应模式，我们很难接收到一些响应消息。比如当我们要测试发布一条控制指令，我们很难获取到指令发送后的响应是什么，虽然可以实现，但过于复杂。而 MQTT 5.0 中的请求主题可以更快更有效的实现这一能力。

我们以发布一条开关灯的指令，并响应指令状态为例，展示响应主题的使用方法。我们点击 Meta 按钮，输入框内输入一个响应主题：/ack/1，输入一个对比数据：light，并在当前连接客户端订阅一个 /ack/1。

> 注意：MQTT 的请求响应是异步的，对比数据可以将响应消息与请求消息关联。

![MQTT 响应主题与对比数据](https://static.emqx.net/images/513b3b0225fcf4e506bbfee2df9b6df0.png)
 
我们使用 [MQTT.js](https://www.emqx.com/zh/blog/mqtt-js-tutorial) 再实现一个客户端，模拟接收控制指令的灯设备。当接收到开灯指令后，给响应主题发送一个开启成功的响应消息。实现关键代码：

```
client.on('message', (topic, payload, packet) => {
  console.log('Received Message:', topic, payload.toString())
  if (packet.properties && packet.properties.responseTopic) {
    client.publish(packet.properties.responseTopic, 'Success!', {
      qos: 0,
      retain: false,
    })
  }
})
```

点击发送消息，我们就能接收到来自灯设备接收开关指令成功后的响应消息了。

![MQTT 发布消息](https://static.emqx.net/images/1e34a978935a109429f75ca7814494b6.png)
 

不过目前 MQTT X 对于请求响应特性仅支持在发送时配置响应主题和对比数据。后续将继续优化响应部分的配置，为用户带来更完整的测试请求响应的能力。

### 内容类型和载荷格式

在 1.7.0 版本中，支持指定配置[有效载荷的格式和内容类型](https://www.emqx.com/zh/blog/mqtt5-new-features-payload-format-indicator-and-content-type)。允许在消息发布时指定载荷格式（二进制、文本）和 MIME 样式内容类型。我们只需要在发布消息前，点击 Meta 按钮，在输入框内输入 Content Type，点击设置 Payload Format Indicator 的值后，发布消息即可。

![MQTT 内容类型和载荷格式](https://static.emqx.net/images/2537699f80d7f48dd7e6c7d089be746f.png)
 
内容类型的一个比较典型的应用就是存放 MIME 类型，比如 text/plain 表示文本文件，audio/aac 表示音频文件，而 application/json 表示是一条 JSON 格式的应用消息。

而有效载荷指示器属性的值设置为 false 时，消息是未确定的字节，当该属性值设置为 true 时，意味着消息体中的有效载荷是 UTF-8 编码的字符数据。

这将有助于 MQTT 客户端或 MQTT 服务器可以更加有效的解析消息内容，而不用特意去对于消息体进行格式或类型的判断。

### 订阅选项

在 1.7.0 版本中还对 MQTT 5.0 中的[订阅选项](https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options)进行了支持。在新建一个 MQTT 5.0 的连接后，我们打开订阅主题的弹出框，可以看到下方出现了包含了 No Local、Retain as Published 和 Retain Handling 的配置选项，用户可以使用这些订阅选项来改变服务端的行为。

![MQTT 订阅选项](https://static.emqx.net/images/af0bca2827e425a17960efe7a2a9fa19.png)

设置 No Local flag 为 true，那么服务端将不会向你转发你自己发布的消息。否则如果你订阅了自己发布消息的主题，那么你将收到自己发布的所有消息。

设置 Retain as Published flag 为 true 时，可以指定服务端向客户端转发消息时是否要保留其中的 Retain 标识，而不是客户端直接依靠消息中的 Retain 标识来区分这是一个正常的转发消息还是一个保留消息。

Retain Handling 这一选项用来指定订阅建立时服务端是否向客户端发送保留消息。设置为 0，只要客户端订阅成功，服务端就发送保留消息；设置为 1，客户端订阅成功且该订阅此前不存在，服务端才发送保留消息；设置为 2，即便客户订阅成功，服务端也不会发送保留消息。

在后续版本中我们还将继续支持订阅标识符等 MQTT 5.0 中的新特性。

## 其他新功能使用

### 一键多主题订阅

在之前的版本中，我们每次打开订阅主题的弹框只能订阅一个主题，对于想要订阅多个主题的用户来说，每次都需要点击打开和关闭才能订阅多个主题，不是很方便。因此该版本中，我们做了优化，支持一次订阅多个主题。

我们打开订阅主题的弹出框后，在 Topic 输入框内，输入多个 Topic 并使用逗号（,）进行分割，点击确认订阅成功后，我们可以看到订阅列表中包含了多个 Topic。对于使用客户端层的别名功能也可以支持同时对多个 Topic 进行设置，同理使用逗号分隔（,）。

> 注意：别名输入框内的内容需要与 Topic 输入框内的 Topic 一一对应。

![MQTT 一键多主题订阅](https://static.emqx.net/images/80e2cf14cc1efe0198686c68e618569b.png)

### 禁止消息自动滚动

设置中新增了对接收和发布消息时，消息列表自动滚动的控制。可以到设置页面中开启自动滚动功能，适用于当消息接收速率较慢时，帮助用户查看到最新消息。当接收消息的速率过快时，可以点击关闭该功能，帮助用户查看一些已发送或已接收到的旧消息。

> 注意：当关闭自动滚动功能后，可以提升部分发送和接收消息时的性能。

![MQTT X 禁止消息自动滚动](https://static.emqx.net/images/ad7e215dde3b8f4410c39748023dd16d.png)

## 结语

通过本文，相信大家对 MQTT X v1.7.0 的功能使用有了更多了解。MQTT X 与 EMQX 配合使用，可以帮助您充分掌握 MQTT 5.0 协议，并在实际项目中将其特性更好地加以应用。

后续我们还会完善 MQTT X 对类似主题别名、请求响应和订阅标识符等配置的支持能力，敬请期待。
