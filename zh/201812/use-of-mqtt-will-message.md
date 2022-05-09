遗嘱消息是 [MQTT](https://www.emqx.com/zh/mqtt) 为那些可能出现 **意外断线** 的设备提供的将 **遗嘱** 优雅地发送给第三方的能力。意外断线包括但不限于：

- 因网络故障或网络波动，设备在保持连接周期内未能通讯，连接被服务端关闭
- 设备意外掉电
- 设备尝试进行不被允许的操作而被服务端关闭连接，例如订阅自身权限以外的主题等

遗嘱消息可以看作是一个简化版的 PUBLISH 消息，他也包含 Topic, Payload, QoS 等字段。遗嘱消息会在设备与服务端连接时，通过 CONNECT 报文指定，然后在设备意外断线时由服务端将该遗嘱消息发布到连接时指定的遗嘱主题（Will Topic）上。这也意味着服务端必须在回复 CONNACK 之前完成遗嘱消息的存储，以确保之后任一时刻发生意外断线的情况，服务端都能保证遗嘱消息被发布。

以下为遗嘱消息在 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 和 MQTT 3.1 & 3.1.1 的差异：

|                 | MQTT 5.0 | MQTT 3.1 & 3.1.1 |
| :-------------- | :------- | :--------------- |
| Will Retain     | Yes      | Yes              |
| Will QoS        | Yes      | Yes              |
| Will Flag       | Yes      | Yes              |
| Will Properties | Yes      | **No**           |
| Will Topic      | Yes      | Yes              |
| Will Payload    | Yes      | Yes              |

Will Retain、Will QoS、Will Topic 和 Will Payload 的用处与普通 PUBLISH 报文基本一致，这里不再赘述。

唯一值得一提的是 Will Retain 的使用场景，它是[保留消息](https://www.emqx.com/zh/blog/message-retention-and-message-expiration-interval-of-emqx-mqtt5-broker)与遗嘱消息的结合。如果订阅该遗嘱主题（Will Topic）的客户端不能保证遗嘱消息发布时在线，那么建议为遗嘱消息设置 Will Retain，避免订阅端错过遗嘱消息。

Will Flag 通常是 MQTT 协议实现方关心的字段，它用于标识 CONNECT 报文中是否会包含 Will Properties、Will Topic 等字段。

最后一个是 MQTT 5.0 新增的 Will Properties 字段，属性本身也是 MQTT 5.0 的一个新特性，不同类型的报文有着不同的属性，例如 CONNECT 报文有[会话过期间隔](https://www.emqx.com/zh/blog/message-retention-and-message-expiration-interval-of-emqx-mqtt5-broker)（Session Expiry Interval）、最大报文长度（Maximum Packet Size）等属性，SUBSCRIBE 报文则有[订阅标识符](https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options)（Subscription Identifier）等属性。

Will Properties 中的消息过期间隔（Message Expiry Interval）等属性与 PUBLISH 报文中的用法基本一致，只有一个遗嘱延迟间隔（Will Delay Interval）是遗嘱消息特有的属性。

遗嘱延迟间隔顾名思义，就是在连接断开后延迟一段时间才发布遗嘱消息。它的一个重要用途就是避免在设备因网络波动短暂断开连接，但能够快速恢复连接继续提供服务时发出遗嘱消息，并对遗嘱消息订阅方造成困扰。

需要注意的是，具体延迟多久发布遗嘱消息，除了遗嘱延迟间隔，还受限于会话过期间隔，取决于两者谁先发生。所以当我们将会话过期间隔设置为 0 时，即会话在网络连接关闭时过期，那么不管遗嘱延迟间隔的值是多少，遗嘱消息都会在网络连接断开时立即发布。

### 演示遗嘱消息的使用

接下来我们使用 [EMQX](https://www.emqx.io/zh) 和 [MQTT X](https://mqttx.app/zh) 来演示一下遗嘱消息的实际使用。

为了实现 MQTT 连接被异常断开的效果，我们需要调整一下 EMQX 的默认 ACL 规则与相关配置项：

首先在 `etc/acl.conf` 中添加以下 ACL 规则，表示拒绝本机客户端连接发布 test 主题。注意需要加在所有默认 ACL 规则之前，以确保这条规则能成功生效：

```
{deny, {ipaddr, "127.0.0.1"}, publish, ["test"]}.
```

然后修改 `etc/emqx.conf` 中 `zone.internal.acl_deny_action` 配置项，将其设置为 ACL 检查拒绝时断开客户端连接：

```
zone.internal.acl_deny_action = disconnect
```

完成以上修改后，我们启动 EMQX。

接下来，我们在 MQTT X 中新建一个名为 demo 的连接，Host 修改为 localhost，在 Advanced 部分选择 MQTT Version 为 5.0，并且将 Session Expiry Interval 设置为 10，确保会话不会在遗嘱消息发布前过期。

![MQTT X 创建连接](https://static.emqx.net/images/944beb7b3bade0f748ef8ba941b75b18.png)

然后在 Lass Will and Testament 部分将 Last-Will Topic 设置为 offline，Last-Will Payload 设置为 `I'm offline`，Will Delay Interval (s) 设置为 5。

![Lass Will and Testament](https://static.emqx.net/images/1a0b8deedbeb35560eeab52c56c5d569.png)

完成以上设置后，我们点击右上角的 Connect 按钮以建立连接。

然后我们再创建一个名为 subscriber 的客户端连接，并订阅 offline 主题。

![创建 subscriber 客户端](https://static.emqx.net/images/dff812179bd1fdd3c2e02d05f1561cdd.png)

接下来我们回到 demo 连接中，发布一个 Topic 为 test 的任意内容消息，这时连接会被断开，耐心等待五秒钟，我们将看到 subscriber 连接收到了一条内容为 `I‘m offline` 的遗嘱消息。

![发布消息](https://static.emqx.net/images/5ca474341ab19f2b1ea41a46b736bada.png)

### 进阶使用场景

这里介绍一下如何将 Retained 消息与 Will 消息结合起来进行使用。

1. 客户端 A 遗嘱消息内容设定为 `offline`，该遗嘱主题与一个普通发送状态的主题设定成同一个 `A/status`。
2. 当客户端 A 连接时，向主题 `A/status` 发送内容为 `online` 的 Retained 消息，其它客户端订阅主题 `A/status` 的时候，将获取到 Retained 消息为 `online`。
3. 当客户端 A 异常断开时，系统自动向主题 `A/status` 发送内容为 `offline` 的消息，其它订阅了此主题的客户端会马上收到 `offline` 消息；如果遗嘱消息设置了 Will Retain，那么此时如果有新的订阅 `A/status` 主题的客户端上线，也将获取到内容为 `offline` 的遗嘱消息。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
