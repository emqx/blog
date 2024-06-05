在 [MQTT 发布/订阅模式介绍](https://www.emqx.com/zh/blog/mqtt-5-introduction-to-publish-subscribe-model) 这篇博客中，我们已经了解到，我们需要先向服务端发起订阅，才能从服务端接收对应的消息。如果说订阅时指定的主题过滤器决定了服务端将向我们转发哪些主题下的消息，那么订阅选项则是允许我们进一步定制服务端的转发行为。

在本文中，我们将重点介绍在 MQTT 中哪些订阅选项可供我们使用，以及它们的使用方法。

## 订阅选项

在 MQTT 中，一个订阅由一个 [主题过滤器](https://emqx.atlassian.net/wiki/spaces/Community/pages/592936998/Subscription+Options#) 和对应的订阅选项组成。所以理论上，我们可以为每个订阅都设置不同的订阅选项。

MQTT 5.0 提供了 4 个订阅选项，分别是 QoS、No Local、Retain As Published、Retain Handling，而 MQTT 3.1.1 则仅提供了 QoS 这一个订阅选项。不过这些 MQTT 5.0 新增的订阅选项的默认行为，仍与 MQTT 3.1.1 保持一致，如果你正准备从 MQTT 3.1.1 升级到 MQTT 5.0，这会非常地友好。

现在，让我们一起看看这些订阅选项的作用吧。

### QoS

QoS 是最常用的一个订阅选项，它表示服务端在向订阅端发送消息时可以使用的最大 QoS 等级。

客户端可能会在订阅时指定一个小于 2 的 QoS，因为它的实现不支持 QoS 1 或者 QoS 2。而如果服务端支持的最大 QoS 小于客户端订阅时请求的最大 QoS，那么显然服务端将无法满足客户端的要求，这时服务端就会通过订阅的响应报文（SUBACK）告知订阅端最终授予的最大 QoS 等级，订阅端可以自行评估是否接受并继续通信。

![qos down grade when subscribe](https://assets.emqx.com/images/b1cc97bc6d3fd75d7a36d896dd96eeb4.png)

一个简单的计算公式：

```
服务端最终授予的最大 QoS = min ( 服务端支持的最大 QoS, 客户端请求的最大 QoS )
```

但是，我们在订阅时请求的最大 QoS，并不能限制发布端发布消息时使用的 QoS。当我们订阅时请求的最大 QoS，小于消息发布时的 QoS 时，为了尽可能地投递消息，服务端不会忽略这些消息，而是会在转发时对这些消息的 QoS 进行降级处理。

![qos down grade when publish](https://assets.emqx.com/images/37dda6930ee7cabbf0867a59de3a415e.png)

同样，我们也有一个简单的计算公式：

```
消息被转发时的 QoS = min ( 消息原始的 QoS, 服务端最终授予的最大 QoS )
```

### No Local

No Local 只有 0 和 1 两个可取值，为 1 表示服务端不能将消息转发给发布这个消息的客户端，为 0 则相反。

这个选项通常被用在桥接场景中。桥接本质上是两个 MQTT Server 建立了一个 MQTT 连接，然后相互订阅一些主题，Server 将客户端的消息转发给另一个 Server，而另一个 Server 则可以将消息继续转发给它的客户端。

![no local](https://assets.emqx.com/images/dbeae9e7cd1106d4bcf82bf56fb990e6.png)

那么最简单的一个例子，我们假设两个 MQTT Server 分别是 Server A 和 Server B，它们分别向对方订阅了 `#` 主题。现在，Server A 将一些来自客户端的消息转发给了 Server B，而当 Server B 查找匹配的订阅时，Server A 也会位于其中。如果 Server B 将消息转发给了 Server A，那么同样 Server A 在收到消息后又会把它们再次转发给 Server B，这样就陷入了无休止的转发风暴。

而如果 Server A 和 Server B 在订阅 `#` 主题的同时，将 No Local 选项设置为 1，就可以完美地避免这个问题。

### Retain As Published

Retain As Published 同样只有 0 和 1 两个可取值，为 1 表示服务端在向此订阅转发应用消息时需要保持消息中的 Retain 标识不变，为 0 则表示必须清除。

Retain As Published 与 No Local 一样，同样也是主要适用于桥接场景。我们知道当服务端收到一条保留消息时，除了将它存储起来，还会将它像普通消息一样转发给当前已经存在的订阅者，并且在转发时会清除消息的 Retain 标识。

这在桥接场景下带来了一些问题。我们继续沿用前面的设定，当 Server A 将保留消息转发给 Server B 时，由于消息中的 Retain 标识已经被清除，Server B 将不会知道这原本是一条保留消息，自然不会再存储它。这就导致了保留消息无法跨桥接使用。

那么在 MQTT 5.0 中，我们可以让桥接的服务端在订阅时将 Retain As Published 选项设置为 1，来解决这个问题。

![retainas published](https://assets.emqx.com/images/57787f3d84987f4c7270e13a6a3e00af.png)

### Retain Handling

Retain Handling 这个订阅选项被用来向服务端指示当订阅建立时，是否需要发送保留消息。

我们知道默认情况下，只要订阅建立，那么服务端中与订阅匹配的保留消息就会下发。

但某些时候，客户端可能并不想接收保留消息，比如客户端在连接时复用了会话，但是客户端无法确认上一次连接中是否成功创建了订阅，所以它可能会再次发起订阅。如果订阅已经存在，那么可能保留消息已经被消费过了，也可能服务端已经在会话中缓存了一些离线期间到达的消息，这时客户端可能并不希望服务端发布保留消息。

另外，客户端也可能在任何时刻都不想收到保留消息，即使是第一次订阅。比如我们将开关状态作为保留消息发送，但对某个订阅端来说，开关事件将触发一些操作，那么在这种情况下不发送保留消息是很有用的。

这三种不同的行为，我们可以通过 Retain Handling 来选择。

将 Retain Handling 设置为 0，表示只要订阅建立，就发送保留消息；

将 Retain Handling 设置为 1，表示只有建立全新的订阅而不是重复订阅时，才发送保留消息；

将 Retain Handling 设置为 2，表示订阅建立时不要发送保留消息。

## 演示

### 订阅选项 QoS 的演示

1. 在 Web 浏览器上访问 [MQTTX Web](http://mqtt-client.emqx.com/)。

2. 创建一个使用 WebSocket 的 MQTT 连接，并且连接免费的 [公共 MQTT 服务器](http://broker.emqx.io/)：

   ![MQTTX](https://assets.emqx.com/images/1eff007c799cd5e9ed9d65c3a2b1d826.png)

3. 连接成功后，我们订阅主题 `mqttx_4299c767/demo`，并指定 QoS 为 0。由于公共服务器可能同时被很多人使用，为了避免主题与别人重复，我们可以将 Client ID 作为主题前缀：

   ![Subscribe to the topic "mqttx_4299c767/demo"](https://assets.emqx.com/images/7d6598089ff051feadae673734b5be68.png)

4. 订阅成功后，我们向主题 `mqttx_4299c767/demo` 发布一条 QoS 1 消息，这时我们将看到，我们发出的是 QoS 1 消息，但收到的却是 QoS 0 消息，这说明发生了 QoS 降级：

   ![Publish a QoS 1 message](https://assets.emqx.com/images/4b1a7d69d8344ba6efc2c7fe22370b17.png)

### 订阅选项 No Local 的演示

1. 在 Web 浏览器上访问 [MQTTX Web](http://mqtt-client.emqx.com/)。

2. 创建一个使用 WebSocket 的 MQTT 连接，并且连接免费的 [公共 MQTT 服务器](http://broker.emqx.io/)。

3. 连接成功后，我们订阅主题 `mqttx_4299c767/demo`，并且将 No Local 设置为 true：

   ![Subscribe to the topic "mqttx_4299c767/demo"](https://assets.emqx.com/images/9255fa97ed59e71be6b7fac0e7d2fed4.png)

4. 订阅成功后，与前面 QoS 的演示一样，我们还是由订阅端自己来发布消息，但这一次我们会发现订阅端将无法收到消息：

   ![Publish MQTT Message](https://assets.emqx.com/images/933d4e0147c2b1720124d8d3e36c55a1.png)

### 订阅选项 Retain As Published 的演示

1. 在 Web 浏览器上访问 [MQTTX Web](http://mqtt-client.emqx.com/)。

2. 创建一个使用 WebSocket 的 MQTT 连接，并且连接免费的 [公共 MQTT 服务器](http://broker.emqx.io/)。

3. 连接成功后，我们先订阅主题 `mqttx_4299c767/rap0`，并且将 Retain As Published 设置为 false，然后订阅主题 `mqttx_4299c767/rap1`，并且将 Retain As Published 设置 true：

   ![Subscribe to the topic "mqttx_4299c767/rap0"](https://assets.emqx.com/images/3d9cb0512df37e95a1be40ec82384f93.png)

   ![Subscribe to the topic "mqttx_4299c767/rap1"](https://assets.emqx.com/images/627c5a3984d401f7e3cb01a160e593a0.png)

4. 订阅成功后，我们分别向主题 `mqttx_4299c767/rap0` 和 `mqttx_4299c767/rap1` 发布一条保留消息，我们将看到前者收到的消息中 Retain 标识被清除，而后者收到的消息中 Retain 标识被保留：

   ![Receive messages](https://assets.emqx.com/images/8e23176543eb78b1f5ee77f6ba98add1.png)

### 订阅选项 Retain Handling 的演示

1. 在 Web 浏览器上访问 [MQTTX Web](http://mqtt-client.emqx.com/)。

2. 创建一个使用 WebSocket 的 MQTT 连接，并且连接免费的 [公共 MQTT 服务器](http://broker.emqx.io/)。

3. 连接成功后，我们先向主题 `mqttx_4299c767/rh` 发布一条保留消息。然后订阅主题 `mqttx_4299c767/rh`，并且将 Retain Handling 设置为 0：

   ![Publish a retained message to the topic "mqttx_4299c767/rh"](https://assets.emqx.com/images/9b0a0bfa76836e9e4bfc30d6576b25f6.png)

4. 订阅成功后，我们将收到服务端发送的保留消息：

   ![Receive the retained message](https://assets.emqx.com/images/1630db5d1e44c7eec81fcd37e7ca0969.png)

5. 取消当前订阅，重新订阅主题 `mqttx_4299c767/rh`，并且将 Retain Handling 设置为 2。不过这一次订阅成功后，我们将不会收到服务端发送的保留消息：

   ![Retain Handling set to 2](https://assets.emqx.com/images/2032a4e178b18b0bcfd2866b9f377f75.png)

在 MQTTX 中，我们没有办法演示 Retain Handling 设置为 1 时的效果。不过你可以在 [这里](https://github.com/emqx/MQTT-Feature-Examples) 获取订阅选项的 Python 示例代码。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
