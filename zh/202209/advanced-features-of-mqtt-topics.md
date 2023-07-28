## 什么是 MQTT 主题？

MQTT 主题本质上是一个 UTF-8 编码的字符串，是 MQTT 协议进行消息路由的基础。MQTT 主题类似 URL 路径，使用斜杠 `/` 进行分层：

```
chat/room/1
sensor/10/temperature
sensor/+/temperature
sensor/#
```

为了避免歧义且易于理解，通常不建议主题以 `/` 开头或结尾，例如 `/chat` 或 `chat/`。

不同于消息队列中的主题（比如 Kafka 和 Pulsar），MQTT 主题不需要提前创建。[MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)在订阅或发布时即自动的创建了主题，开发者无需再关心主题的创建，并且也不需要手动删除主题。

下图是一个简单的 MQTT 订阅与发布流程， `APP 1` 订阅了`sensor/2/temperature` 主题后，将能接收到 `Sensor 2` 发布到该主题的消息。

![MQTT 发布订阅](https://assets.emqx.com/images/0c35bfdb730f1d29b7f1b7a249c62f8b.png)


## MQTT 主题通配符

MQTT 主题通配符包含单层通配符 `+` 及多层通配符 `#`，主要用于客户端一次订阅多个主题。

> **注意**：通配符只能用于订阅，不能用于发布。

### 单层通配符

加号 (“+” U+002B) 是用于单个主题层级匹配的通配符。在使用单层通配符时，单层通配符必须占据整个层级，例如：

```
+ 有效
sensor/+ 有效
sensor/+/temperature 有效
sensor+ 无效（没有占据整个层级）
```

如果客户端订阅了主题 `sensor/+/temperature`，将会收到以下主题的消息：

```
sensor/1/temperature
sensor/2/temperature
...
sensor/n/temperature
```

但是不会匹配以下主题：

```
sensor/temperature
sensor/bedroom/1/temperature
```

### 多层通配符

井字符号（“\#” U+0023）是用于匹配主题中任意层级的通配符。多层通配符表示它的父级和任意数量的子层级，在使用多层通配符时，它必须占据整个层级并且必须是主题的最后一个字符，例如：

```
# 有效，匹配所有主题
sensor/# 有效
sensor/bedroom# 无效（没有占据整个层级）
sensor/#/temperature 无效（不是主题最后一个字符）
```

如果客户端订阅主题  `senser/#`，它将会收到以下主题的消息：

```
sensor
sensor/temperature
sensor/1/temperature
```


## 以 $ 开头的主题

### 系统主题

以 `$SYS/` 开头的主题为系统主题，系统主题主要用于获取 [MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)自身运行状态、消息统计、客户端上下线事件等数据。目前，MQTT 协议暂未明确规定 `$SYS/` 主题标准，但大多数 MQTT 服务器都遵循该[标准建议](https://github.com/mqtt/mqtt.org/wiki/SYS-Topics)。

例如，EMQX 服务器支持通过以下主题获取集群状态。

| 主题                                 | 说明              |
| ------------------------------------ | ----------------- |
| $SYS/brokers                         | EMQX 集群节点列表 |
| $SYS/brokers/emqx@127.0.0.1/version  | EMQX 版本         |
| $SYS/brokers/emqx@127.0.0.1/uptime   | EMQX 运行时间     |
| $SYS/brokers/emqx@127.0.0.1/datetime | EMQX 系统时间     |
| $SYS/brokers/emqx@127.0.0.1/sysdescr | EMQX 系统信息     |

EMQX 还支持客户端上下线事件、收发流量、消息收发、系统监控等丰富的系统主题，用户可通过订阅 `$SYS/#` 主题获取所有系统主题消息。详细请见：[EMQX 系统主题文档](https://www.emqx.io/docs/zh/v5.0/advanced/system-topic.html)。

### 共享订阅

共享订阅是 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 引入的新特性，用于在多个订阅者之间实现订阅的负载均衡，MQTT 5.0 规定的共享订阅主题以 `$share` 开头。

>虽然 MQTT 协议在 5.0 版本才引入共享订阅，但是 EMQX 从 MQTT 3.1.1 版本开始就支持共享订阅。

下图中，3 个订阅者用共享订阅的方式订阅了同一个主题 `$share/g/topic`，其中`topic` 是它们订阅的真实主题名，而 `$share/g/` 是共享订阅前缀（`g/` 是群组名，可为任意 UTF-8 编码字符串）。

![MQTT 共享订阅](https://assets.emqx.com/images/c248e9334ff6d32cbec0ed71cde98b1f.png)

另外，对于 MQTT 5.0 以下的版本，EMQX 还支持不带群组的共享订阅前缀 `$queue`，关于共享订阅的更多详情请查看 [EMQX 共享订阅](https://www.emqx.io/docs/zh/v5.0/advanced/shared-subscriptions.html)文档。


## 不同场景中的主题设计

### 智能家居

比如我们用传感器监测卧室、客厅以及厨房的温度、湿度和空气质量，可以设计以下几个主题：

- `myhome/bedroom/temperature`
- `myhome/bedroom/humidity`
- `myhome/bedroom/airquality`
- `myhome/livingroom/temperature`
- `myhome/livingroom/humidity`
- `myhome/livingroom/airquality`
- `myhome/kitchen/temperature`
- `myhome/kitchen/humidity`
- `myhome/kitchen/airquality`

接下来，可以通过订阅 ` myhome/bedroom/+` 主题获取卧室的温度、湿度及空气质量数据，订阅 `myhome/+/temperature` 主题获取三个房间的温度数据，订阅 ` myhome/#` 获取所有的数据。

### 充电桩

充电桩的上行主题格式为 `ocpp/cp/${cid}/notify/${action}`，下行主题格式为 `ocpp/cp/${cid}/reply/${action}`。

- `ocpp/cp/cp001/notify/bootNotification`

  充电桩上线时向该主题发布上线请求。

- `ocpp/cp/cp001/notify/startTransaction`

  向该主题发布充电请求。

- `ocpp/cp/cp001/reply/bootNotification`

  充电桩上线前需订阅该主题接收上线应答。

- `ocpp/cp/cp001/reply/startTransaction`

  充电桩发起充电请求前需订阅该主题接收充电请求应答。

### 即时消息

- `chat/user/${user_id}/inbox`

  **一对一聊天**：用户上线后订阅该收件箱主题 ，将能接收到好友发送给自己的消息。给好友回复消息时，只需要将该主题的 `user_id` 换为好友的的 id 即可。

- `chat/group/${group_id}/inbox`

  **群聊**：用户加群成功后，可订阅该主题获取对应群组的消息，回复群聊时直接给该主题发布消息即可。

- `req/user/${user_id}/add`

  **添加好友**：可向该主题发布添加好友的申请（`user_id` 为对方的 id）。

  **接收好友请求**：用户可订阅该主题（`user_id` 为自己的 id）接收其他用户发起的好友请求。

- `resp/user/${user_id}/add`

  **接收好友请求的回复**：用户添加好友前，需订阅该主题接收请求结果（`user_id` 为自己的 id）。

  **回复好友申请**：用户向该主题发送消息表明是否同意好友申请（`user_id` 为对方的 id）。

- `user/${user_id}/state`

  **用户在线状态**：用户可以订阅该主题获取好友的在线状态。

  
## MQTT 主题常见问题及解答

### 主题的层级及长度有什么限制吗？

MQTT 协议规定主题的长度为两个字节，因此主题最多可包含 **65,535** 个字符。

建议主题层级为 7 个以内。使用较短的主题名称和较少的主题层级意味着较少的资源消耗，例如 `my-home/room1/data` 比 `my/home/room1/data` 更好。

### 服务器对主题数量有限制吗？

不同消息服务器对最大主题数量的支持各不一致，目前 EMQX 的默认配置对主题数量没有限制，但是主题数量越多将会消耗越多的服务器内存。考虑到连接到 MQTT Broker 的设备数量一般较多，我们建议一个客户端订阅的主题数量最好控制在 10 个以内。

### 通配符主题订阅与普通主题订阅性能是否一致？

通配符主题订阅的性能弱于普通主题订阅，且会消耗更多的服务器资源，用户可根据实际业务情况选择订阅类型。

### 重叠订阅了普通主题和通配符主题时如何接收消息?

假如客户端同时订阅了 `#` 和 `test` 主题，当向 `test` 主题发送消息时，是否会收到两条重复消息？这取决于 MQTT broker 的实现，例如 EMQX 会为每个匹配的订阅发送消息。但是用户可以使用 MQTT 5.0 中的订阅标识符来区分消息来源，然后在客户端中根据订阅标识符来处理这类重复的消息。

### 同一个主题能被共享订阅与普通订阅同时使用吗？

可以，但是不建议同时使用。

### 常见的 MQTT 主题使用建议有哪些？

- 不建议使用 `#` 订阅所有主题；
- 不建议主题以 `/` 开头或结尾，例如 `/chat` 或 `chat/`；
- 不建议在主题里添加空格及非 ASCII 特殊字符；
- 同一主题层级内建议使用下划线 `_` 或横杆 `-` 连接单词（或者使用驼峰命名）；
- 尽量使用较少的主题层级；
- 当使用通配符时，将唯一值的主题层（例如设备号）越靠近第一层越好。例如，`device/00000001/command/#` 比`device/command/00000001/#` 更好。


## 结语

至此，相信读者已对 MQTT 主题及通配符有了深刻的理解。接下来，可访问 EMQ 提供的 [MQTT 入门与进阶](https://www.emqx.com/zh/mqtt-guide)系列文章了解 MQTT 协议的其他特性，探索 MQTT 的更多高级应用，开启 MQTT 应用及服务开发。
  

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
