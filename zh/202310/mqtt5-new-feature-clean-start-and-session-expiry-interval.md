在本文中，我们将介绍 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 的会话机制，以及 Clean Start 和 Session Expiry Interval 这两个用于配置会话生命周期的连接参数。

## 为什么需要会话？

在物联网场景中，设备可能因为网络问题或者电源问题而频繁地断开连接。如果客户端和服务端总是以全新的上下文建立连接，那么将带来以下几个问题：

1. 客户端在重连后必须重新订阅主题才能继续接收消息，这会给服务器带来额外的开销。
2. 客户端将会错过离线期间的消息。
3. QoS 1 和 QoS 2 的服务质量将无法得到保证。

为了避免这些问题，MQTT 协议设计了会话机制，它也构成了 MQTT 通信的基础。

## 什么是 MQTT 会话？

[MQTT 会话](https://www.emqx.com/zh/blog/mqtt-session)本质上就是一组需要服务端和客户端额外存储的上下文数据，这些数据可以仅持续与网络连接一样长的时间，也可以跨越多个连续的网络连接存在。当客户端与服务端借助这些会话数据恢复通信时，可以让网络中断就像从未发生过一样。

以服务端为例，它需要存储客户端的订阅列表，那么不管当前客户端是否连接，只要会话没有过期，服务端就能够知道哪些消息是被该客户端订阅的，进而为它缓存这些消息。另外，客户端再次连接时也不需要重新发起订阅，这也减少了服务端的性能开销。

MQTT 为服务端和客户端分别定义了它们需要存储的会话状态。对于 **服务端** 来说，它需要存储以下内容：

1. 会话是否存在。
2. 客户端的订阅列表。
3. 已发送给客户端，但是还没有完成确认的 QoS 1 和 QoS 2 消息。
4. 等待传输给客户端的 QoS 0 消息（可选），QoS 1 和 QoS 2 消息。
5. 从客户端收到的，但是还没有完成确认的 QoS 2 消息。
6. [遗嘱消息与遗嘱过期间隔](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)。
7. 会话过期时间。

对于 **客户端** 来说，它需要存储以下内容：

1. 已发送给服务端，但是还没有完成确认的 QoS 1 和 QoS 2 消息。
2. 从服务端收到的，但是还没有完成确认的 QoS 2 消息。

显而易见的是，让服务端和客户端永久存储这些会话数据，不仅会带来很多额外的存储成本，而且在很多场景中也没有必要。譬如我们只是为了避免网络连接短暂中断导致的消息丢失，那么一般将会话数据设置为在连接断开后保留短暂的几分钟即可。

另外，当客户端与服务端会话状态不一致时，比如客户端设备因为重启导致会话数据丢失，那么它需要在连接时告知服务端丢弃原有的会话并创建一个全新的会话。

针对这两点，[MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 提供了 Clean Start 和 Session Expiry Interval 这两个连接字段来控制会话的生命周期。

## Clean Start 介绍

Clean Start 位于 CONNECT 报文的 [可变报头](https://www.emqx.com/zh/blog/introduction-to-mqtt-control-packets)，客户端在连接时通过这个字段指定是否复用已存在的会话，它只有 0 和 1 两个可取值。

**当 Clean Start 被设置为 0**，如果服务端存在与客户端连接时指定的 Client ID 关联的会话，那么它必须使用这个会话来恢复通信。

如果不存在任何与该 Client ID 关联的会话，则服务端必须创建一个全新的会话。这时，客户端使用的是旧的会话，服务端使用的是全新的会话，两边的会话状态出现了不一致。所以服务端必须将 CONNACK 报文中的 Session Present 字段设置为 0，以让客户端知晓它期望的会话不存在，如果客户端想要继续此网络连接，就必须丢弃它保存的会话状态。

**当 Clean Start 设置为 1**，客户端和服务端必须丢弃任何已存在的会话，并开始一个全新的会话。相应地，服务端也会把 CONNACK 报文中的 Session Present 字段设置为 0。

![MQTT Clean Start](https://assets.emqx.com/images/5aa78a5c038aacafdbd314930e060c67.jpg)

## Session Expiry Interval 介绍

Session Expiry Interval 同样位于 CONNECT 报文的可变报头，不过它是一个可选的连接 [属性](https://www.emqx.com/zh/blog/introduction-to-mqtt-control-packets)。它被用来指定会话在网络断开后能够在服务端保留的最长时间，如果到达过期时间但网络连接仍未恢复，服务端就会丢弃对应的会话状态。它有三个典型的值：

1. **没有指定此属性或者设置为 0**，表示会话将在网络连接断开时立即结束。
2. **设置为一个大于 0 的值**，则表示会话将在网络连接断开的多少秒之后过期。
3. **设置为 0xFFFFFFFF**，即 Session Expiry Interval 属性能够设置的最大值时，表示会话永不过期。

每个 MQTT 客户端都可以独立设置自己的 Session Expiry Interval，我们可以根据实际需要来灵活地设置过期时间，比如一部分客户端不需要持久会话，一部分客户端只需要会话保留几分钟来避免网络波动带来的影响，而另一部分客户端则可能需要会话保留更长的时间。

MQTT 还允许客户端在断开连接时更新会话过期时间，这主要依靠 DISCONNECT 报文中 Session Expiry Interval 属性实现。比较常见的一个应用场景是，客户端在上线时将会话过期时间设置为一个大于 0 的值，避免网络中断影响正常业务。然后在客户端完成所有业务主动下线时，将会话过期时间更新为 0，这样服务端也可以及时地释放会话。

![MQTT Session Expiry Interval](https://assets.emqx.com/images/d988dd62c980580f1cef76b0fe9d9b98.jpg)

## 会话与 Client ID

服务端使用 Client ID 来唯一地标识每个会话，如果客户端想要在连接时复用之前的会话，那么必须使用与此前一致的 Client ID。所以当我们使用服务端自动分配 Client ID 的功能时，客户端必须将 CONNACK 报文中返回的 Assigned Client Identifier 保存下来以供下次使用。

注意，MQTT 5.0 之前的协议版本并不支持服务端返回自动分配的 Client ID，所以在由服务端自动分配 Client ID 和使用持久会话之间，我们只能二选一。

## MQTT 3.1.1 中的 Clean Session

MQTT 3.1.1 中的会话机制，在灵活性上远不如 5.0。因为 3.1.1 只有一个 Clean Session 字段，且它只有 0 和 1 两个可取值。

在 MQTT 3.1.1 中将 Clean Session 设置为 0，等同于在 MQTT 5.0 中将 Clean Start 设置 0，并且将 Session Expiry Interval 设置为 0xFFFFFFFF，即会话永不过期。

在 MQTT 3.1.1 中将 Clean Session 设置为 1，等同于在 MQTT 5.0 中将 Clean Start 设置为 1，并且将 Session Expiry Interval 设置为 0，即会话的生命周期与网络连接保持一致。

![MQTT Clean Session](https://assets.emqx.com/images/ef56580a559b209bef5c60c2e8e4c435.jpg)

可以看到，在 MQTT 3.1.1 中，会话的生命周期只有两种选项：永不过期或与网络连接保持一致。

但是为所有客户端永久保留会话，无疑导致了服务端的资源浪费，这更像是 MQTT 3.1.1 在协议设计时的一个疏漏。所以 EMQX 提供了 `mqtt.session_expiry_interval` 配置项，这让我们可以为 MQTT 3.1.1 的客户端设置一个全局的会话过期时间，以便将服务端的资源消耗控制在一个可以接受的范围内。

另外，是否需要创建全新的会话，也与会话的生命周期强行绑定在了一起，在 MQTT 3.1.1 中，我们必须指定 Clean Session 为 1 和 0 各连接一次，才能让服务端创建一个全新的、持久的会话。

所以相比于 MQTT 3.1.1，MQTT 5.0 在会话方面的改进是巨大的。

## MQTT 持久会话的一些实践建议

在 MQTT 中，我们通常将生命周期长于网络连接的会话称为 **持久会话**。但是在使用持久会话时，我们有一些事项需要注意。

譬如，我们需要正确地评估持久会话对服务器资源的影响，会话过期时间越长，服务端需要花费的存储资源就可能越多。虽然服务端通常并不会无限制地为客户端缓存消息，以 [EMQX](https://www.emqx.io/zh) 为例，默认情况下每个客户端会话中能够缓存的最大消息数量为 1000，但考虑到客户端的数量，这仍然可能是一个客观的存储成本。如果你的服务器资源有限，那么你可能需要更谨慎地设置会话过期时间和会话的最大缓存。

另外，我们也需要评估客户端是否有必要在长时间离线后继续处理这些离线期间到达的消息。当然，设置较大的缓存以尽可能保存更多更久的消息，还是设置较小的缓存让客户端上线后仅处理最近一段时间到达的消息，主要取决于你的实际场景。

## 演示

1. 安装并打开 [MQTTX](https://mqttx.app/zh)，为了更好地演示 MQTT 的会话机制，首先我们来到 MQTTX 的设置页面，关闭自动重订阅功能：

   ![MQTTX](https://assets.emqx.com/images/c4468d62187f87ea1948ded7dc9cc6c1.png)

2. 创建一个名为 `sub` 的客户端连接，将 MQTT Version 设置为 5.0，开启 Clean Start，Session Expiry Interval 设置为 300 秒，然后连接到免费的 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 并订阅主题 `mqttx_290c747e/test`：

   ![MQTTX 创建客户端](https://assets.emqx.com/images/9c71204115d54271f12cad3ca86e4e30.png)

3. 创建一个名为 `pub` 的客户端连接向主题 `mqttx_290c747e/test` 发布消息，消息内容可以随意设置，我们将看到 `sub` 客户端收到这些消息。这时我们断开 `sub` 客户端的连接，然后继续通过 `pub` 客户端发布消息：

   ![创建一个名为 pub 的客户端](https://assets.emqx.com/images/2596d8ca90d3d83e3945a6f87cbbc430.png)

4. 接下来，我们将 `sub` 客户端的 Clean Start 选项关闭，并保持 Session Expiry Interval 为 300 秒，然后再次连接。我们将看到 `sub` 客户端陆续收到我们在它离线期间发布的消息：

   ![将 sub 客户端的 Clean Start 选项关闭](https://assets.emqx.com/images/c657006df302fdbf952cedeb867a536d.png)

   ![再次连接](https://assets.emqx.com/images/63ec97979353b2b2ada1e7fc74e56db4.png)

以上就是 MQTT 会话为离线客户端缓存消息的能力。在终端界面，我们还可以使用命令行工具 [MQTTX CLI](https://mqttx.app/zh/cli) 来完成以上操作。我们首先使用以下命令订阅主题，订阅成功后在终端输入 Ctrl+C 断开此客户端连接：

```
mqttx sub -h 'broker.emqx.io' --mqtt-version 5 --client-id mqttx_290c747e \
--session-expiry-interval 300 --topic mqttx_290c747e/test
…  Connecting...
✔  Connected
…  Subscribing to mqttx_290c747e/test...
✔  Subscribed to mqttx_290c747e/test
^C
```

然后使用以下命令向主题 `mqttx_290c747e/test` 发布一条消息：

```
mqttx pub -h 'broker.emqx.io' --topic mqttx_290c747e/test --message "hello world"
```

发布成功后恢复订阅端的连接，注意我们在下面的命令中保持 Client ID 与之前相同，并且设置了 `--no-clean` 选项，我们将看到订阅端在连接成功后立刻收到了我们在连接之前发布的消息：

```
mqttx sub -h 'broker.emqx.io' --mqtt-version 5 --client-id mqttx_290c747e \
--no-clean --session-expiry-interval 300 --topic mqttx_290c747e/test
…  Connecting... 
✔  Connected
…  Subscribing to mqttx_290c747e/test...
payload: hello world

✔  Subscribed to mqttx_290c747e/test
```

不管是 [MQTTX](https://mqttx.app/zh) 还是 [MQTTX CLI](https://mqttx.app/zh/cli)，它们作为 [MQTT 客户端工具](https://www.emqx.com/zh/blog/mqtt-client-tools)，主要目的是帮助大家快速上手 MQTT，所以并未提供一些非必要的特性，比如查看服务端返回的 Session Present，以及在断开连接时更新 Session Expiry Interval 等等。所以你对这一部分感兴趣，可以在 [这里](https://github.com/emqx/MQTT-Feature-Examples) 获取相应的 Python 示例代码以了解更多。





<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
