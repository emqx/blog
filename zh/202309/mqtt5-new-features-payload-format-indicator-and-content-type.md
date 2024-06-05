在本文中，我们将聚焦于 MQTT 5.0 的 Payload Format Indicator 和 Content Type 这两个属性，探讨它们如何使我们对消息的解析变得更加透明和高效。

## 什么是 Payload Format Indicator?

Payload Format Indicator 是 MQTT 5.0 引入的一个全新属性，用来指示 [MQTT 报文](https://www.emqx.com/zh/blog/introduction-to-mqtt-control-packets)中有效载荷的格式。但 CONNECT、SUBSCRIBE 与 UNSUBSCRIBE 报文中有效载荷的格式都是固定不变的，所以实际上只有 PUBLISH 报文和 CONNECT 报文中的遗嘱消息需要声明其有效载荷的格式。

如果 Payload Format Indicator 的值为 0 或者没有指定这个属性，表示当前有效载荷是未指定的字节流；而如果这个属性的值为 1，则表示当前有效载荷是 UTF-8 编码的字符数据。

这允许接收者在无需解析具体内容的前提下检查有效载荷的格式，例如服务端可以检查有效载荷是否是一个有效的 UTF-8 字符串，避免将格式不正确的应用消息分发给订阅者。不过考虑到这个操作对服务端带来的负担和实际能够取得的收益，这通常是一个可选的行为。

![MQTT Payload Format Indicator](https://assets.emqx.com/images/1918b4c4b45be63be94faefda5552178.jpg)

## 什么是 Content Type?

Content Type 也是 MQTT 5.0 引入的一个全新属性，与 Payload Format Indicator 类似，它同样仅存在于 PUBLISH 报文和 CONNECT 报文的遗嘱消息中。

Content Type 的值是一个 UTF-8 编码的字符串，用来描述应用消息的内容，这可以帮助接收端了解如何解析应用消息的有效载荷。例如，消息的内容是一个 JSON 对象，那么 Content Type 可以被设置为 "json"。

这个字符串的具体内容完全由发送端和接收端决定，在消息的整个传输过程中，服务端不会使用这个属性来验证消息内容的格式是否正确，它只负责将这个属性原封不动地转发给订阅者。

所以只要接收端能够理解，你甚至可以用 “cocktail” 来描述 JSON 类型。但为了避免造成不必要的困扰，通常我们更推荐使用已知的 MIME 类型来描述消息内容，例如 `application/json`、`application/xml` 等等。

Content Type 在需要支持多种数据类型的场景中非常有用。比如当我们在聊天软件中向对方发送图片，图片可能有 png，gif，jpeg 等多种格式，如何向对端指示我们发送的二进制数据所对应的图片格式？

在 5.0 之前，我们可能会选择在主题中包含图片格式，比如 `to/userA/image/png`。但显然，随着支持的图片格式的增加，系统中的主题也会泛滥成灾。而在 5.0 中，我们只需要将 Content Type 属性设置为 `image/png` 即可。

![MQTT Content Type](https://assets.emqx.com/images/33655d6d84dce7b65d5b468368750fe3.jpg)

## Payload Format Indicator 与 Content Type 必须一起使用吗？

Payload Format Indicator 和 Content Type 是否需要同时使用，主要取决于我们的应用场景。

对于订阅端来说，他可以根据 Content Type 属性的值来判断消息的内容应该是 UTF-8 字符串还是二进制数据，所以 Payload Format Indicator 属性的意义不大。

不过对于服务端来说，他并不了解 Content Type 的值的含义，所以如果我们希望服务端检查消息的有效载荷是否符合 UTF-8 编码规范，就必须借助 Payload Format Indicator 属性。

## 演示

1. 在 Web 浏览器上访问 [MQTTX Web](http://mqtt-client.emqx.com/)。

2. 创建一个名为 `pub` 的客户端连接用于发布消息，并且连接到免费的 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)：

   ![MQTTX 创建客户端](https://assets.emqx.com/images/3caf7341b589eb9c0f1ab86bf10006b0.png)

3. 以相同的方法创建一个名为 `sub` 的客户端连接并使用 Client ID 作为前缀订阅主题 `mqttx_89e3d55e/test`：

   ![MQTTX 创建名为 sub 的客户端](https://assets.emqx.com/images/7b14002dc798e92330d810385e190e95.png)

4. 然后回到 `pub` 客户端，点击消息栏的 Meta 按钮，将 Payload Format Indicator 设置为 `true`，Content Type 设置为 `application/json` 向主题 `mqttx_89e3d55e/test` 发布一条 JSON 格式的消息，然后修改为 `application/x-www-form-urlencoded` 再向同一主题发布一条 form 表单格式的消息：

   ![MQTTX Publish 消息](https://assets.emqx.com/images/426791206386f2495e2aa39983408a92.png)

   ![MQTTX Payload Format Indicator](https://assets.emqx.com/images/d57d53438bdbb57e7b61932ebc9bcfad.png)

5. 消息中的 Content Type 将原封不动地转发给订阅端，因此订阅端可以根据 Content Type 的值得知应该如何解析 Payload 中的内容：

   ![MQTTX 消息接收](https://assets.emqx.com/images/8152fe5fa6448c760ceff37dd0e4c51f.png)

6. 回到发布端，将 Payload Format Indicator 设置为 false，并将 Payload 的编码格式改为 Hex，然后输入 FF 作为 Payload 内容并发送，0xFF 是一个典型的非 UTF-8 字符：

   ![MQTTX Payload Format Indicator](https://assets.emqx.com/images/91b2e1059174351935e0d1bbf8869efa.png)

7. 虽然显示为乱码，但订阅端确实接收到了我们刚刚发送的 Payload 为 0xFF 的消息，这是因为出于性能考虑，EMQX 目前并未检查 Payload 格式：

   ![MQTTX 接收消息](https://assets.emqx.com/images/2362ab53295ecb87bc5b9d43cb0de22a.png)

在终端界面，我们还可以使用命令行工具 [MQTTX CLI](https://mqttx.app/zh/cli) 来完成以上操作，我们可以使用以下命令订阅主题：

```
mqttx sub -h 'broker.emqx.io' -p 1883 -t 'random-string/demo' --output-mode clean
```

然后使用以下命令在发布消息时设置 Payload Format Indicator 和 Content Type 属性：

```
mqttx pub -h 'broker.emqx.io' -p 1883 -t 'random-string/demo' \
--payload-format-indicator \
--content-type 'application/json' \
-m '{"msg": "hello"}'
```

以上就是 MQTT 5.0 中 Payload Format Indicator 和 Content Type 属性的使用方法，你还可以在 [这里](https://github.com/emqx/MQTT-Feature-Examples) 获取它们的 Python 示例代码。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
