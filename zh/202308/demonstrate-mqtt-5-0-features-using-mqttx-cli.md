[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 作为目前物联网领域最为流行的通信协议，它的最新版本早已在 2019 年就已经来到了 5.0。与之前的版本相比，5.0 增加了会话过期、原因码、共享订阅、请求响应等更符合现代物联网应用需求的特性，这也让它成为了目前绝大多数物联网企业的首选版本。

为了让大家更全面地了解 MQTT 5.0，本文将依次介绍 5.0 引入的各个新特性，并使用 [MQTTX CLI](https://mqttx.app/zh) 工具演示我们应该如何在 [EMQX](https://www.emqx.io/zh) 中使用这些特性，你可以通过复制和粘贴命令轻松地运行本文中的示例。

在正式开始前，我们需要完成以下准备工作：

1. 使用 Docker 来部署一个最基础的 EMQX 实例，你可以运行以下命令来启动 EMQX：

   ```
   docker run -d --name emqx -p 18083:18083 -p 1883:1883 emqx:5.1.3
   ```

2. 下载并安装 [MQTTX CLI](https://mqttx.app/zh/downloads) 1.9.4。它是一款开源的 MQTT 5.0 命令行客户端工具，我们将通过它来完成本文的所有示例。

3. 安装 [Wireshark](https://www.wireshark.org/)。在部分示例中，我们将用它来抓取并分析一些 MQTT 报文，这可以帮助我们更好地了解究竟发生了什么。

## 特性 1：会话过期

在 MQTT 5.0 中，客户端可以在 CONNECT 报文中通过 Session Expiry Interval 来指示它期望的网络连接断开后会话的过期间隔（以秒为单位）。如果服务端不接受这个过期间隔，也可以在 CONNACK 报文中指示一个新的过期间隔，客户端则需要遵从服务端的要求。

在会话过期之前，[MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)与服务端都需要存储相应的会话状态。以服务端为例，它需要存储的会话状态包括已经发送但尚未完成确认的消息，尚未发送的消息以及客户端的订阅列表等等。

只要客户端与服务端的连接在会话过期前恢复，那么它们就可以继续之前的通信，就像连接从未断开过一样。

### 示例 1

客户端 sub1 订阅主题 t1，并设置会话过期间隔为 60 秒，订阅完成后在终端输入 Ctrl+C 断开客户端连接：

```
mqttx sub --client-id sub1 --session-expiry-interval 60 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
✔  Subscribed to t1
^C
```

在 60 秒内向主题 t1 发布一条消息：

```
mqttx pub --topic t1 --message "Hello World"
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

客户端 sub1 重新连接，注意这里指定了 --no-clean 选项表示希望复用之前的会话，我们将看到此客户端收到了我们在它连接之前发布的消息：

```
mqttx sub --client-id sub1 --no-clean --session-expiry-interval 0 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
payload: Hello World
✔  Subscribed to t1
```

### 示例 2

EMQX 默认允许的最大会话过期间隔为 2 小时，我们可以打开 EMQX Dashboard（浏览器中输入 `http://localhost:18083` 即可访问），通过 `Management -> MQTT Settings -> Session` 页面中的 Session Expiry Interval 配置项来修改它。

本示例中我们将它设置为 0 秒，即会话将在网络连接断开时立即过期：

![MQTT Session Expiry Interval](https://assets.emqx.com/images/84a3d445ad64b2bb5c0ac0d7575637cf.png)

接下来，重复示例 1 中的步骤，这一次客户端 sub1 将不会在重新连接后收到消息：

```
mqttx sub --client-id sub1 --session-expiry-interval 60 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
✔  Subscribed to t1
^C

mqttx pub --topic t1 --message "Hello World"
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published

mqttx sub --client-id sub1 --no-clean --session-expiry-interval 0 --topic t1
…  Connecting...
✔  Connected
…  Subscribing to t1...
✔  Subscribed to t1
```

## 特性 2：消息过期

在 MQTT 5.0 中，我们可以为每条消息设置一个过期间隔（以秒为单位），如果消息在服务端中停留超过了这个间隔，那么它将不会再被分发给客户端。

当我们想要长时间地保留会话，但是又想要发送一些具有时效性的消息时，这个特性将会非常有用。

另外，如果客户端在发布消息时设置了过期间隔，那么服务端在转发这个消息时也会包含过期间隔，但过期间隔的值会被更新为服务端接收到的值减去该消息在服务端停留的时间。

这样接收者就可以知道这个消息是有时效的，以及它将在多少时间后过期。

### 示例 1

客户端 sub2 订阅主题 t2，并设置会话过期间隔为 300 秒，订阅完成后在终端输入 Ctrl+C 断开客户端连接：

```
mqttx sub --client-id sub2 --session-expiry-interval 300 --topic t2
…  Connecting...
✔  Connected
…  Subscribing to t2...
✔  Subscribed to t2
^C
```

向同一主题发布一条消息，并设置消息过期间隔为 5 秒钟

```
mqttx pub --topic t2 --message "Hello World" --message-expiry-interval 5
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

等待 10 秒钟后客户端 sub2 恢复连接，但是它将不会收到我们刚刚发布的消息：

```
sleep 10; mqttx sub --client-id sub2 --no-clean --session-expiry-interval 300 --topic t2
…  Connecting...
✔  Connected
…  Subscribing to t2...
✔  Subscribed to t2
```

### 示例 2

继续向主题 t2 发布消息，并设置消息过期间隔为 60 秒钟：

```
mqttx pub --topic t2 --message "Hello World" --message-expiry-interval 60
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

等待 10 秒后客户端 sub2 恢复连接，它将收到我们刚刚发布的消息，并且其中的消息过期间隔为 50 秒。

```
sleep 10; mqttx sub --client-id sub2 --no-clean --session-expiry-interval 0 --topic t2 --output-mode clean
{
  "topic": "t2",
  "payload": "Hello World",
  "packet": {
      ...
    "properties": {
      "messageExpiryInterval": 50
    }
  }
}
```

## 特性 3：令所有响应报文支持原因码

MQTT 5.0 不仅为所有响应报文都增加了原因码字段，同时也扩展了可用的原因码。现在服务端和客户端都可以更清晰地向对方指示错误原因。

比如当消息到达但当前不存在任何匹配的订阅时，服务端将会丢弃这个消息。但为了让消息的发送者得知这一情况，服务端会将响应报文中的原因码设置为 0x10（仅限 QoS 1 与 QoS 2 消息），表示不存在匹配的订阅者。

> 你可以通过 [MQTT 5.0 Reason Code 速查表](https://www.emqx.com/zh/blog/mqtt5-new-features-reason-code-and-ack) 了解更多原因码相关的知识。

### 示例

本示例中我们将用到 Wireshark。启动 Wireshark 后首先选择正确的网卡，如果你的 EMQX 与 MQTTX CLI 同样运行在同一台机器上，那么你应该与本示例一样选择环回接口，然后输入以下过滤语句抓取报文：

```
tcp.port == 1883
```

向主题 t3 发布 QoS 1 消息：

```
mqttx pub --topic t3 --message "Hello World" --qos 1
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

在 Wireshark 中我们将看到 EMQX 返回的 PUBACK 报文中 Reason Code 被设置为 0x10：

![Wireshark](https://assets.emqx.com/images/dc6b0ade500c1df276114bd14d4792fe.png)

## 特性 4：服务器断开

MQTT 5.0 允许服务端在断开网络连接前发送 DISCONNECT 报文，以便向客户端指示连接断开的原因。

### 示例

在 Wireshark 中输入以下过滤语句抓取报文：

```
tcp.port == 1883
```

建立一个 MQTT 连接：

```
mqttx conn --client-id conn4
…  Connecting...
✔  Connected
```

在另一个终端窗口中使用 EMQX 提供的 CLI 命令手动踢除客户端：

```
docker exec emqx emqx ctl clients kick conn4
ok
```

我们将在第一个终端窗口中看到连接被断开：

```
✖  Connection closed
```

EMQX 发送的 DISCONNECT 报文中 Reason Code 被设置为 0x98，表示此连接因为管理操作而被关闭：

![Wireshark](https://assets.emqx.com/images/05744c8ecd86b07215cff789c10425cb.png)

## 特性 5：载荷格式与内容类型

在 MQTT 5.0 中，消息的发布者可以通过 Payload Format Indicator 来指示该消息的内容是 UTF-8 编码的字符数据还是未指定格式的二进制数据。

Content Type 则可以进一步指示消息内容的具体格式，这样接收者可以更容易地知道应该如何解析这个消息。常见的做法是将其设置为一个 MIME 内容类型，例如 `application/json`。当然这并不是强制的，我们也可以使用任意的 UTF-8 字符串来指示我们自定义的消息类型 。

### 示例

订阅主题 t6：

```
mqttx sub --topic t6 --output-mode clean
```

在另一个终端窗口中发布消息，设置 Payload Format Indicator 表示此消息的内容是 UTF-8 编码的字符数据，设置为 Content Type 为 `application/json` 表示这是一个 JSON 格式的消息：

```
mqttx pub --topic t6 --message "{\"content\": \"Hello World\"}" --payload-format-indicator --content-type application/json 
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

第一个终端窗口将打印接收到的消息内容，我们可以看到消息中包含了 Content Type 和 Payload Format Indicator：

```
{
  "topic": "t6",
  "payload": "{\"content\": \"Hello World\"}",
  "packet": {
        ...
    "properties": {
      "contentType": "application/json",
      "payloadFormatIndicator": true
    }
  }
}
```

## 特性 6：请求/响应

MQTT 5.0 极大地改善了对请求响应模式的支持。请求方可以在请求消息指定响应主题（Response Topic），响应方则需要向该响应主题发布响应消息。

这在同时存在多个请求方，响应方需要将响应正确地回复给其中一个请求方时非常有用，不同请求方只需要指定不同的响应主题即可。一个简单的做法是在响应主题中包含自己的 Client ID。

MQTT 不能保证请求方的请求一定被响应方收到，反之亦然。所以请求方还需要能够正确地将自己发出的请求与收到的响应进行关联。在 MQTT 5.0 中，我们可以在请求消息中设置对比数据（Correlation Data），响应方将原封不动地在响应消息中返回这个对比数据，这样请求方就能够知道这是哪个请求的响应。

### 示例

在第一个终端窗口中，响应方订阅请求主题：

```
mqttx sub --client-id responder --topic request --session-expiry-interval 300 --output-mode clean
```

在第二个终端窗口中，请求方发布请求消息，并设置响应主题为 `response/requester1`：

```
mqttx pub --client-id requester1 --session-expiry-interval 300 --topic request --message "This is a reuqest" --response-topic response/requester1 --correlation-data request-1
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

在第一个终端窗口中，响应方收到请求消息，消息中包含了响应主题与对比数据：

```
{
  "topic": "request",
  "payload": "This is a reuqest",
  "packet": {
    "properties": {
      "correlationData": {
        "type": "Buffer",
        "data": [
          114,
          101,
          113,
          117,
          101,
          115,
          116,
          45,
          49
        ]
      },
      "responseTopic": "response/requester1"
    }
  }
}
```

回到第二个终端窗口，请求方订阅响应主题（在实际应用中，请求方需要在发布请求前订阅响应主题以免错过响应消息）：

```
mqttx sub --client-id requester1 --no-clean --session-expiry-interval 300 --topic response/requester1 --output-mode clean
```

在第一个终端窗口中，响应方收到请求中的响应主题发布响应响应，并携带对比数据：

```
mqttx pub --client-id responder --topic response/requester1 --message "This is a response" --correlation-data request-1
```

在第二个终端窗口中，请求方收到响应消息：

```
{
  "topic": "response",
  "payload": "This is a response",
  "packet": {
      ...
    "properties": {
      "correlationData": {
        "type": "Buffer",
        "data": [
          114,
          101,
          113,
          117,
          101,
          115,
          116,
          45,
          49
        ]
      }
    }
  }
}
```

## 特性 7：共享订阅

MQTT 5.0 增加了对共享订阅的支持，使得订阅端能够以负载均衡的方式来消费消息。

它允许我们将订阅客户端划分为多个订阅组，消息仍然会被转发给所有订阅组，但一个订阅组内的客户端将以随机、轮询等策略交替接收消息。这些策略完全由服务端实现，客户端不需要进行任何修改，唯一需要做的就是通过 `$share/{ShareGroup}/{Topic}` 来发起共享订阅。

### 示例

在第一个终端窗口中，订阅主题 `$share/g1/t7`：

```
mqttx sub --topic '$share/g1/t7'
…  Connecting...
✔  Connected
…  Subscribing to $share/g1/t7...
✔  Subscribed to $share/g1/t7
```

在第二个终端窗口中，同样订阅主题 `$share/g1/t7`：

```
mqttx sub --topic '$share/g1/t7'
…  Connecting...
✔  Connected
…  Subscribing to $share/g1/t7...
✔  Subscribed to $share/g1/t7
```

在第三个终端窗口中，改为订阅主题 `$share/g2/t7`：

```
mqttx sub --topic '$share/g2/t7'
…  Connecting...
✔  Connected
…  Subscribing to $share/g2/t7...
✔  Subscribed to $share/g2/t7
```

在第四个终端窗口中，向主题 t7 发布消息，这里我们使用了 `--multiline` 选项，以每次键入回车的方式发送多条消息：

```
mqttx pub --topic t7 -s --stdin --multiline
…  Connecting...
✔  Connected, press Enter to publish, press Ctrl+C to exit
Message 1
Message 2
Message 3
Message 4
Message 5
Message 6
^C
```

EMQX 默认的共享订阅策略为 `round_robin`，这表示消息将轮流分发给同一个订阅组内的订阅者。所以我们将看到第一个和第二个终端窗口中的订阅者将交替接收我们发布的消息：

```
payload: Message 1

payload: Message 3

payload: Message 5
```

```
payload: Message 2

payload: Message 4

payload: Message 6
```

共享订阅组 `g2` 中只有一个订阅者，所以我们将在第三个终端窗口中看到订阅者收到了所有消息：

```
payload: Message 1

payload: Message 2

payload: Message 3

payload: Message 4

payload: Message 5

payload: Message 6
```

## 特性 8：订阅标识符

MQTT 5.0 允许客户端在订阅时设置一个订阅标识符（Subscription Identifier），服务端会将该标识符与订阅绑定，当服务端向该订阅转发消息时，它会在消息中附上对应的标识符。客户端可以使用消息中的订阅标识符，决定触发哪一个回调，或者进行其他操作。

### 示例

同一个客户端订阅主题 `t8/1` 与 `t8/#`，并设置不同的订阅标识符：

```
mqttx sub --client-id sub8 --session-expiry-interval 300 --topic t8/1 --subscription-identifier 1
…  Connecting...
✔  Connected
…  Subscribing to t8/1...
✔  Subscribed to t8/1
^C
mqttx sub --client-id sub8 --no-clean --session-expiry-interval 300 --topic t8/# --subscription-identifier 2 --output-mode clean 
```

在第二个终端窗口中，向主题 `t8/1` 发布消息：

```
mqttx pub --topic t8/1 --message "Hello World"
```

第一个终端窗口中的订阅端将收到两条消息，根据消息中的订阅标识符我们可以得知，第一条消息来自订阅的主题 `t8/#`，第二条消息来自订阅的主题 `t8/1`：

```
{
  "topic": "t8/1",
  "payload": "Hello World",
  "packet": {
        ...
    "properties": {
      "subscriptionIdentifier": 2
    }
  }
}
{
  "topic": "t8/1",
  "payload": "Hello World",
  "packet": {
        ...
    "properties": {
      "subscriptionIdentifier": 1
    }
  }
}
```

> 当消息匹配同一个客户端的多个订阅时，MQTT 服务端可以向这些重叠的订阅分别发送一条消息，也可以向这些重叠的订阅只发送一条消息。EMQX 属于前者。

## 特性 9：主题别名

MQTT 5.0 允许我们在发布消息时以一个两个字节长度的整数类型的主题别名来替代主题名，这在主题名较长时可以有效减少 PUBLISH 报文的大小。

使用主题别名时，我们需要先发送一个同时包含主题名与主题别名的消息，让对端建立映射关系，然后才能发送仅包含主题别名的消息。

主题别名的映射不属于会话状态的一部分，所以即便客户端重连时恢复了会话，它与服务端也需要重新建立主题别名的映射。

客户端和服务端使用的主题别名映射相互独立。因此一般来说，客户端发送给服务端的主题别名值为 1 的消息和服务端发送给客户端的主题别名值为 1 的消息，将被映射到不同的主题。

客户端和服务端还可以在连接时约定互相可以发送的主题别名的最大值。EMQX 默认允许的主题别名的最大值为 65535，我们可以打开 EMQX Dashboard（浏览器中输入 `http://localhost:18083` 即可访问），通过 `Management -> MQTT Settings -> General` 页面中的 Max Topic Alias 配置项来修改它。

![MQTT 主题别名](https://assets.emqx.com/images/c853659e22cf620edc4eadb562cf7633.png)

## 特性 10：流量控制

MQTT 5.0 中客户端与服务端可以在连接时使用接收最大值（Receive Maximum）来指示自己愿意同时处理的未确认的 QoS 1 和 QoS 2 消息的最大数量。

当已经发送但未完全确认的消息数量达到接收最大值限制时，发送方就不能继续向接收方发送消息（QoS 0 消息不受此限制）。这可以有效避免发送方发送过快导致超出接收方的处理能力。

## 特性 11：用户属性

MQTT 5.0 中的大部分报文都可以包含用户属性。用户属性是一个由 UTF-8 编码的字符串组成的名称-值对，名称和值的具体内容可以由客户端和服务端的实现自行定义，我们可以在没有超过报文最大长度的前提下指定任意多个用户属性。

CONNECT、SUBSCRIBE 这类报文中的用户属性，通常取决于具体 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)的实现。

PUBLISH 报文中的用户属性，会被服务端直接原封不动地转发给订阅端，所以只要消息的发布端和订阅端约定好用户属性的内容即可。比如在应用消息的用户属性中附上发布端的 Client ID，这样订阅端将可以知道消息来自哪里。

### 示例

订阅主题 t11：

```
mqttx sub --topic t11 --output-mode clean
```

在另一个终端窗口中，向主题 t11 发布消息，并设置了两个用户属性，一个指示消息的来源，一个指示消息的发布时间：

```
mqttx pub --client-id pub11 --topic t11 --message "Hello World" --user-properties "from: pub11" --user-properties "timestamp: 1691046633"
```

回到第一个终端窗口中，订阅端收到的消息中包含了我们设置的用户属性：

```
{
  "topic": "t11",
  "payload": "Hello World",
  "packet": {
        ...
    "properties": {
      "userProperties": {
        "from": "pub11",
        "timestamp": "1691046633"
      }
    }
  }
}
```

## 特性 12：最大报文长度

MQTT 5.0 允许客户端和服务端在连接时通过 Maximum Packet Size 属性相互约定自己能够处理的最大报文长度，之后任何一方都不得发送超过约定长度限制的报文，否则将造成协议错误而被关闭连接。

所以当 PUBLISH 报文过大导致无法转发时，服务端将直接丢弃该 PUBLISH 报文。

### 示例 1

在第一个终端窗口中，向服务端声明自己可接受的最大报文长度为 128 字节，并订阅主题 t12：

```
mqttx sub --maximum-packet-size 128 --topic t12
…  Connecting...
✔  Connected
…  Subscribing to t12...
✔  Subscribed to t12
```

在第二个终端窗口中，发布一个长度小于 128 字节的消息：

```
payload=$(head -c 10 < /dev/zero | tr '\0' 0)
mqttx pub --topic t12 -m "$payload"
```

在第一个终端窗口中，订阅端将收到以下消息：

```
payload: 0000000000
```

继续在第二个终端窗口中发布一个长度超过 128 字节的消息：

```
payload=$(head -c 128 < /dev/zero | tr '\0' 0)
mqttx pub --topic t12 -m "${payload}"
```

这一次第一个终端窗口中的订阅端将不会收到消息，我们输入 Ctrl+C 断开订阅端连接，然后运行以下命令查看 EMQX 日志：

```
docker logs emqx
```

我们将看到消息因 `frame_is_too_large` 而被丢弃的日志：

```
2023-08-03T06:17:52.538541+00:00 [warning] msg: packet_is_discarded, mfa: emqx_connection:serialize_and_inc_stats_fun/1, line: 872, peername: 172.17.0.1:39164, clientid: mqttx_f0a3847c, packet: PUBLISH(Q0, R0, D0, Topic=t12, PacketId=undefined, Payload=******), reason: frame_is_too_large
```

### 示例 2

EMQX 默认允许的最大报文长度为 1MB，我们可以打开 EMQX Dashboard（浏览器中输入 `http://localhost:18083` 即可访问），通过 `Management -> MQTT Settings -> General` 页面中的 Max Packet Size 配置项来修改它。

注意最大长度限制的是所有报文，所以如果设置了一个过小的最大报文长度，可能导致连接无法建立。这是我们要注意避免的。

本示例中，我们将它修改为 1024 字节：

![图片.png](https://assets.emqx.com/images/512963490e383148c2288bf5255f8751.png)

然后在 Wireshark 中输入以下过滤语句抓取报文：

```
tcp.port == 1883
```

在终端窗口中，发布一个长度超过 1024 字节的消息：

```
payload=$(head -c 1024 < /dev/zero | tr '\0' 0)
mqttx pub --client-id pub12 --topic t12 -m "${payload}"
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

在 Wireshark 中我们将看到 EMQX 返回了 DISCONNECT 报文，并将 Reason Code 被设置为 0x95，表示连接因为收到了过大的报文而被关闭：

![Wireshark](https://assets.emqx.com/images/3ac6a07014588cc82ea14365795e8843.png)

## 特性 13：可选的服务端功能

MQTT 允许服务端不完全支持协议声明的功能和特性，但服务端需要在 CONNACK 报文中告知客户端自己不支持的功能，避免客户端使用这些不可用的功能。可选的服务端功能包括：

- 支持的最大 QoS 等级

- 保留消息

- 通配符订阅

- 订阅标识符

- 共享订阅

如果客户端仍然使用了服务端已经告知不可用的功能，那么就会造成协议错误被服务端关闭连接。

### 示例

EMQX 默认支持所有 MQTT 特性，但我们可以手动关闭一些功能，比如通配符订阅、共享订阅以及保留消息等等。本示例中我们关闭了保留消息功能：

![MQTT 关闭保留消息](https://assets.emqx.com/images/16873e4be8c387d5766c68b69d2a51f1.png)

然后在 Wireshark 中输入以下过滤语句抓取报文：

```
tcp.port == 1883
```

在终端窗口中发布一条保留消息：

```
mqttx pub --topic t13 --message "This is a retained message" --retain
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

在 Wireshark 中我们将看到 EMQX 在 CONNACK 报文中返回了各个功能的可用情况，其中保留消息被声明为不可用：

![Wireshark](https://assets.emqx.com/images/542a90a629c938de745d7abb7016ca1e.png)

而在客户端发布保留消息后，EMQX 返回了 DISCONNECT 报文，并将 Reason Code 被设置为 0x9A，表示服务端不支持保留消息：

![Wireshark](https://assets.emqx.com/images/e79cda1541771f559068a4813d1d3ded.png)

完成此示例后，请将 EMQX 的保留消息功能再次打开，以免影响后续的示例。

## 特性 14：订阅选项

MQTT 5.0 在 QoS 的基础上又提供了三个新的订阅选项，分别为：

1. No Local，用于指示消息是否可以被转发给发布此消息的客户端。

2. Retain As Published，用于指示服务端向该订阅转发消息时是否需要保留其中的 Retain 标志。

3. Retain Handling，用于指示订阅建立时服务端是否需要向该订阅发送保留消息，这个选项有三个可取值：

   1. 设置为 0，只要订阅建立，就发送保留消息。

   2. 设置为 1，只有在订阅建立时该订阅当前不存在才发送保留消息。

   3. 设置为 2，订阅建立时不发送保留消息。

你可以阅读 [MQTT 订阅选项的使用](https://www.emqx.com/zh/blog/an-introduction-to-subscription-options-in-mqtt) 了解订阅选项的更多知识。

### 示例 1 - No Local

客户端 sub14 和 pub14 分别发布一条消息到主题 t14，这里我们借助了 EMQX 的 [延迟发布](https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-delayed-publish.html#%E5%BB%B6%E8%BF%9F%E5%8F%91%E5%B8%83) 功能，让消息延迟 10 秒发布：

```
mqttx pub --client-id sub14 --topic '$delayed/10/t14' --message "You will not receive this message"
mqttx pub --client-id pub14 --topic '$delayed/10/t14' --message "You will receive this message"
```

令客户端 sub14 订阅主题 t14，并设置 No Local 选项，它将收到客户端 pub14 发布的消息，但不会收到它自己发布的消息：

```
mqttx sub --client-id sub14 --topic t14 --no_local
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
payload: You will receive this message
```

### 示例 2 - Retain As Published

在第一个终端窗口中，订阅主题 t14，并设置 Retain As Published 选项：

```
mqttx sub --topic t14 --retain-as-published --output-mode clean
```

在第二个终端窗口中，向主题 t14 发布一条保留消息：

```
mqttx pub --topic t14 --message "Hello World" --retain
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

在第一个终端窗口中，订阅端将收到设置了 Retain 标志位的消息：

```
{
  "topic": "t14",
  "payload": "Hello World",
  "packet": {
      ...
    "retain": true,
        ...
  }
}
```

清除保留消息：

```
mqttx pub --topic t14 --message '' --retain
```

### 示例 3 - Retain Handling

向主题 t14 发布一条保留消息：

```
mqttx pub --topic t14 --message "This is a retained message" --retain
…  Connecting...
✔  Connected
…  Message publishing...
✔  Message published
```

订阅相同主题并设置 Retain Handling 为 0，我们将收到保留消息：

```
mqttx sub --client-id sub14 --session-expiry-interval 300 --topic t14 --retain-handling 0
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
payload: This is a retained message
retain: true
^C
```

在终端输入 Ctrl+C 断开客户端连接。

重连并恢复会话，订阅相同主题，但是将 Retain Handling 设置为 1，这一次我们将不会收到保留消息，因为在服务端此订阅已经存在：

```
mqttx sub --client-id sub14 --no-clean --session-expiry-interval 300 --topic t14 --retain-handling 1
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
^C
```

在终端输入 Ctrl+C 断开客户端连接。

重连但创建一个全新的会话，订阅相同主题，将 Retain Handling 设置为 2，这一次我们仍然不会收到保留消息：

```
mqttx sub --client-id sub14 --topic t14 --retain-handling 2
…  Connecting...
✔  Connected
…  Subscribing to t14...
✔  Subscribed to t14
```

清除保留消息：

```
mqttx pub --topic t14 --message '' --retain
```

## 特性 15：遗嘱延迟

在 MQTT 5.0 中，客户端可以为遗嘱消息设置一个延迟间隔，而不再是让它在网络连接断开时就立即发布，如果客户端连接能够遗嘱延迟间隔到达前及时恢复，那么遗嘱消息就不会被发布。这可以有效地避免遗嘱消息仅仅因为客户端连接的短暂中断而被发布。

如果遗嘱延迟间隔大于会话过期间隔，那么遗嘱消息将在会话过期时被立即发送，所以我们还可以将遗嘱消息用于会话到期通知。

### 示例 1

在第一个终端窗口中订阅主题 t15：

```
mqttx sub --topic t15
…  Connecting...
✔  Connected
…  Subscribing to t15...
✔  Subscribed to t15
```

在第二个终端窗口中建立一个设置了遗嘱消息的 MQTT 连接，并将遗嘱延迟间隔设置为 10 秒。连接成功后输入 Ctrl+C 断开客户端连接：

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 10 --session-expiry-interval 300
…  Connecting...
✔  Connected
^C
```

第一个终端窗口中的订阅端将在 10 秒后收到遗嘱消息：

```
payload: I'm offline
```

### 示例 2

在第二个终端窗口中再次建立一个设置了遗嘱消息的 MQTT 连接，并将遗嘱延迟间隔设置为 10 秒。连接成功后输入 Ctrl+C 断开客户端连接：

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 10 --session-expiry-interval 300
…  Connecting...
✔  Connected
^C
```

在 10 秒内重连：

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 10 --no-clean --session-expiry-interval 300
```

这一次第一个终端窗口中的订阅端将不会收到遗嘱消息。

### 示例 3

我们还可以为遗嘱消息设置 Will Retain 标识，让它成为一个保留消息，避免订阅端因不在线而错过遗嘱消息。

继续在第二个终端窗口中建立一个设置了遗嘱消息的 MQTT 连接，这一次我们将遗嘱延迟间隔设置为 0 秒，因此遗嘱消息将在连接断开时立即发布。连接成功后输入 Ctrl+C 断开客户端连接：

```
mqttx conn --client-id conn15 --will-topic t15 --will-message "I'm offline" --will-delay-interval 0 --will-retain --session-expiry-interval 300
…  Connecting...
✔  Connected
^C
```

在第一个终端窗口中订阅主题 t15，我们将收到在这之前发布的遗嘱消息：

```
mqttx sub --topic t15
…  Connecting...
✔  Connected
…  Subscribing to t15...
✔  Subscribed to t15
payload: I'm offline
retain: true
```

## 特性 16：由服务端指定保活时间

保活时间决定了客户端发送相邻两个控制报文的最大空闲时间，服务端可以根据是否在预期的时间内收到客户端的报文来判断它是否仍然活跃。

在 MQTT 5.0 中，服务端可以不接受客户端指定的保活时间，并在 CONNACK 报文中返回它希望客户端使用的 Keep Alive，客户端必须使用这个保活时间来维持通信。

### 示例

EMQX 默认由客户端指定保活时间，我们可以打开 EMQX Dashboard（浏览器中输入 `http://localhost:18083` 即可访问），通过 `Management -> MQTT Settings -> General` 页面中的 Server Keep Alive 配置项来修改它。

本示例中，我们将它修改为 10 秒：

![MQTT 保活时间](https://assets.emqx.com/images/db10dece7733daaa0bde63bdda8e314e.png)

然后在 Wireshark 中输入以下过滤语句抓取报文：

```
tcp.port == 1883
```

回到终端窗口，发起一个 MQTT 连接，并将 Keep Alive 设置为 30 秒：

```
mqttx conn --keepalive 30
…  Connecting...
✔  Connected
```

我们将在 Wireshark 中看到 EMQX 在返回的 CONNACK 报文中设置了 Server Keep Alive 属性，且值为 10。连接建立后，客户端也是以 10 秒为间隔发送心跳报文而不是 30 秒：

![Wireshark](https://assets.emqx.com/images/2285d82210f5ba969519114020937ef1.png)

## 特性 17: 返回服务端分配的 Client ID

当客户端使用一个长度为 0 的 Client ID 发起连接时，服务端将会为客户端分配一个唯一的 Client ID。在 MQTT 5.0 中，这个分配的 Client ID 可以包含在 CONNACK 报文中返回给客户端。这避免了客户端因为不知道 Client ID 而无法在下一次连接时恢复会话。

### 示例

在 Wireshark 中输入以下过滤语句抓取报文：

```
tcp.port == 1883
```

回到终端窗口，发起一个 MQTT 连接，并将 Client ID 设置为一个长度为 0 的字符串：

```
mqttx conn --client-id ''
```

我们将在 Wireshark 中看到 EMQX 返回的 CONNACK 报文中包含了一个 Assigned Client Identifier 属性，它的值就是 EMQX 为客户端分配的 Client ID：

![Wireshark](https://assets.emqx.com/images/ed6e0702da12fdf44e13504af7162759.png)

## 结语

以上就是 MQTT 5.0 所有特性的基本介绍与演示，你可以试着将演示中的步骤转换成代码然后在你的客户端中复现。如果你希望了解这些 MQTT 5.0 全新特性的更多内容，你可以访问我们的 [MQTT Guide](https://www.emqx.com/en/mqtt-guide)，它聚合了所有你需要知道的 MQTT 的知识。





<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
