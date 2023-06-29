## 为什么需要订阅标识符

在大部分 [MQTT 客户端](https://www.emqx.com/zh/mqtt-client-sdk)的实现中，都会通过回调机制来实现对新到达消息的处理。

但是在回调函数中，我们只能知道消息的主题名是什么。如果是非通配符订阅，订阅时使用的主题过滤器将和消息中的主题名完全一致，所以我们可以直接建立订阅主题与回调函数的映射关系。然后在消息到达时，根据消息中的主题名查找并执行对应的回调函数。

但如果是通配符订阅，消息中的主题名和订阅时的主题过滤器将是两个不同的字符串，我们只有将消息中的主题名与原始的订阅挨个进行主题匹配，才能确定应该执行哪个回调函数。这显然极大地影响了客户端的处理效率。

![MQTT Subscription](https://assets.emqx.com/images/5b3b24a4406e4d342355138f90dd438b.png)

另外，因为 MQTT 允许一个客户端建立多个订阅，那么当客户端使用通配符订阅时，一条消息可能同时与一个客户端的多个订阅匹配。

对于这种情况，MQTT 允许服务端为这些重叠的订阅分别发送一次消息，也允许服务端为这些重叠的订阅只发送一条消息，前者意味着客户端将收到多条重复的消息。

而不管是前者还是后者，客户端都不能确定消息来自于哪个或者哪些订阅。因为即使客户端发现某条消息同时与自己的两个订阅相匹配，也不能保证在服务端向自己转发这条消息时，这两个订阅是否都已经成功创建了。所以，客户端无法为消息触发正确的回调。

![MQTT Subscription](https://assets.emqx.com/images/3a86d62e52c9bfcef85ba590d14c4a19.png)

## 订阅标识符的工作原理

为了解决这个问题，MQTT 5.0 引入了订阅标识符。它的用法非常简单，客户端可以在订阅时指定一个订阅标识符，服务端则需要存储该订阅与订阅标识符的映射关系。当有匹配该订阅的 PUBLISH 报文要转发给此客户端时，服务端会将与该订阅关联的订阅标识符随 PUBLISH 报文一并返回给客户端。

![Subscription Identifier](https://assets.emqx.com/images/f9f1cf19de90a4e03647dbe52d69f7e7.png)

如果服务端选择为重叠的订阅分别发送一次消息，那么每个 PUBLISH 报文都应该包含与订阅相匹配的订阅标识符，而如果服务端选择为重叠的订阅只发送一条消息，那么 PUBLISH 报文将包含多个订阅标识符。

客户端只需要建立订阅标识符与回调函数的映射，就可以通过消息中的订阅标识符得知这个消息来自哪个订阅，以及应该执行哪个回调函数。

![MQTT Subscription](https://assets.emqx.com/images/7ba966d802c9ee39683870366f5fd7c7.png)

在客户端中，订阅标识符并不属于会话状态的一部分，将订阅标识符和什么内容进行关联，完全由客户端决定。所以除了回调函数，我们也可以建立订阅标识符与订阅主题的映射，或者建立与 Client ID 的映射。后者在转发服务端消息给客户端的网关中非常有用。当消息从服务端到达网关，网关只要根据订阅标识符就能够知道应该将消息转发给哪个客户端，而不需要重新做一次主题的匹配和路由。

一个订阅报文只能包含一个订阅标识符，如果一个订阅报文中有多个订阅请求，那么这个订阅标识符将同时和这些订阅相关联。所以请尽量确保将多个订阅关联至同一个回调是您有意为之的。

## 如何使用订阅标识符

1. 在 Web 浏览器上访问 [MQTTX Web](http://www.emqx.io/online-mqtt-client)。

2. 创建一个使用 WebSocket 的 MQTT 连接，并且连接免费的 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)：

   ![MQTT over WebSocket](https://assets.emqx.com/images/e1c10cbd018d0742f21f3b371ec89c6a.png)

3. 连接成功后，我们先订阅主题 `mqttx_4299c767/home/+`，并指定 Subscription Identifier 为 1，然后订阅主题 `mqttx_4299c767/home/PM2_5`，并指定 Subscription Identifier 为 2。由于公共服务器可能同时被很多人使用，为了避免主题与别人重复，这里我们将 Client ID 作为主题前缀：

   ![New Subscription 1](https://assets.emqx.com/images/f3c0aed851e02f20aae69cf100b167d6.png)

   ![New Subscription 2](https://assets.emqx.com/images/212728b6ae71b5baf73a860f75d4545a.png)

4. 订阅成功后，我们向主题 `mqttx_4299c767/home/PM2_5` 发布一条消息。我们将看到当前客户端收到了两条消息，消息中的 Subscription Identifier 分别为 1 和 2。这是因为 EMQX 的实现是为重叠的订阅分别发送一条消息：

   ![Receive MQTT Messages](https://assets.emqx.com/images/fd38994dea83422bb31a85b5c14711b1.png)

5. 而如果我们向主题 `mqttx_4299c767/home/temperature` 发布一条消息，我们将看到收到消息中的 Subscription Identifier 为 1：

   ![image.png](https://assets.emqx.com/images/f0a2dba909a1efa8fab0b07ea961a959.png)

到这里，我们通过 MQTTX 演示了如何为订阅设置 Subscription Identifier。如果你仍然好奇如何根据 Subscription Identifier 来触发不同的回调，可以在 [这里](https://github.com/emqx/MQTT-Feature-Examples)  获取 Subscription Identifier 的 Python 示例代码。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
