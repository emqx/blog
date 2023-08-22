## 什么是消息过期间隔？

消息过期间隔是 MQTT 5.0 引入的一个新特性，它允许发布端为有时效性的消息设置一个过期间隔，如果该消息在服务端中停留超过了这个指定的间隔，那么服务端将不会再将它分发给订阅端。默认情况下，消息中不会包含消息过期间隔，这表示该消息永远不会过期。

[MQTT 的持久会话](https://www.emqx.com/zh/blog/mqtt-session)可以为离线客户端缓存尚未发送的消息，然后在客户端恢复连接时发送。但如果客户端离线时间较长，可能有一些寿命较短的消息已经没有必要必须发送给客户端了，继续发送这些过期的消息，只会浪费网络带宽和客户端资源。

以联网汽车为例，我们可以向车辆发送建议车速使它能够在绿灯期间通过路口，这类消息通常仅在车辆到达下一个路口之前有效，生命周期非常短暂。而前方拥堵提醒这类消息的生命周期则会更长一些，一般会在半小时到 1 小时内有效。

如果客户端在发布消息时设置了过期间隔，那么服务端在转发这个消息时也会包含过期间隔，但过期间隔的值会被更新为服务端接收到的值减去该消息在服务端停留的时间。

这可以避免消息的时效性在传递的过程中丢失，特别是在桥接到另一个 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)的时候。

![MQTT 消息过期间隔](https://assets.emqx.com/images/c671bad84e2bf4e348743d13b6d3c16a.png)

## 何时使用消息过期间隔？

消息过期间隔非常适合在以下场景下使用：

1. 与时间强绑定的消息。比如优惠还剩最后两小时这个消息，如果用户在两个小时后才收到它，不会有任何的意义。

2. 周期性告知最新状态的消息。仍然以道路拥堵提醒为例，我们需要周期性向车辆发送拥堵的预计结束时间，这个时间会随最新的道路情况而发生变化。所以当最新的消息到达后，之前还未发送的消息也没有必要继续发送了。此时消息的过期间隔将由我们实际的发送周期决定。

3. 保留消息。相比于需要再次发送 Payload 为空的保留消息来清除对应主题下的保留消息，为其设置过期时间然后由服务器自动删除显然更加方便，这也可以有效避免保留消息占用过多的存储资源。


## 演示

1. 在 Web 浏览器上访问 [MQTTX Web](http://www.emqx.io/online-mqtt-client)。

2. 创建一个名为 `pub` 的客户端连接用于发布消息，并且连接到免费的 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)：

   ![MQTTX](https://assets.emqx.com/images/4602b4d8091b573a3483f439a6453e3a.png)

3. 新建一个名为 `sub` 的客户端连接用于订阅，并将 Session Expiry Interval 设置为 300 秒表示这将是一个持久会话：

   ![MQTTX 新建连接](https://assets.emqx.com/images/3b4f14fbdf45d8cd4d489ccca3d3c886.png)

4. 连接成功后，我们订阅主题 `mqttx_a3c35d15/demo`，使用 Client ID 作为主题前缀可以有效避免与公共服务器中其他客户端使用的主题重复：

   ![MQTTX 新建订阅](https://assets.emqx.com/images/b924d0feff5ccad6e551575e44563786.png)

5. 订阅成功后，我们断开 `sub` 客户端与服务器的连接，然后切换到 `pub` 客户端，向主题 `mqttx_a3c35d15/demo` 发布以下两条 Message Expiry Interval 分别为 5 秒和 60 秒的消息：

   ![MQTTX 发布消息 1](https://assets.emqx.com/images/728e1e17bf79a305a84ff32880664d2a.png)

   ![MQTTX 发布消息 2](https://assets.emqx.com/images/bac6d68fe6b2a98c6f00ef508140d226.png)

6. 发布完成后，切换到 `sub` 客户端，将 Clean Session 设置为 false 表示想要恢复之前的会话，然后等待至少 5 秒再重新连接。我们将看到 `sub` 只收到了过期时间为 60 秒的消息，因为此时另一条消息已经过期：

   ![MQTT Clean Session](https://assets.emqx.com/images/2a2d1f661e8541a4d2dca0ba47b38e70.png)  ![MQTT Clean Session](https://assets.emqx.com/images/4640131ca940262ad195c25c7f96223a.png)


以上就是 Message Expiry Interval 的用法与效果，你还可以在 [这里](https://github.com/emqx/MQTT-Feature-Examples) 获取 Message Expiry Interval 的 Python 示例代码。





<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
