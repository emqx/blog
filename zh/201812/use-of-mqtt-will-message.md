


## 简介

当客户端断开连接时，发送给相关的订阅者的遗嘱消息。以下情况下会发送 Will Message：

- 服务端发生了I/O 错误或者网络失败；
- 客户端在定义的心跳时期失联；
- 客户端在发送下线包之前关闭网络连接；
- 服务端在收到下线包之前关闭网络连接。

遗嘱消息一般通过在客户端 CONNECT 的时候指定。如下所示，在连接的时候通过调用 `MqttConnectOptions` 实例的 `setWill` 方法来设定。任何订阅了下面的主题的客户端都可以收到该遗嘱消息。

```
//方法1MqttConnectOptions.setWill(MqttTopic topic, byte[] payload, int qos, boolean retained)//方法2MqttConnectOptions.setWill(java.lang.String topic, byte[] payload, int qos, boolean retained)
```

## 使用场景

在客户端 A 进行连接时候，遗嘱消息设定为”offline“，客户端 B 订阅这个遗嘱主题。当 A 异常断开时，客户端 B 会收到这个”offline“的遗嘱消息，从而知道客户端 A 离线了。

### Connect Flag 报文字段

| Bit    | 7              | 6             | 5           | 4        | 2         | 1           | 0        |
| ------ | -------------- | ------------- | ----------- | -------- | --------- | ----------- | -------- |
|        | User Name Flag | Password Flag | Will Retain | Will QoS | Will Flag | Clean Start | Reserved |
| byte 8 | X              | X             | X           | X        | X         | X           | X        |

遗嘱消息在客户端正常调用 disconnect 方法之后并不会被发送。

## Will Flag 作用

简而言之，就是客户端预先定义好，在自己异常断开的情况下，所留下的最后遗愿（Last Will），也称之为遗嘱（Testament）。这个遗嘱就是一个由客户端预先定义好的主题和对应消息，附加在CONNECT的可变报文头部中，在客户端连接出现异常的情况下，由服务器主动发布此消息。

当Will Flag位为1时，Will QoS和Will Retain才会被读取，此时消息体中要出现Will Topic和Will Message具体内容，否则Will QoS和Will Retain值会被忽略掉。

当Will Flag位为0时，则Will Qos和Will Retain无效。

## 命令行示例

下面是一个Will Message的示例：

1. Sub端clientid=sub预定义遗嘱消息:

   ```
   mosquitto_sub --will-topic test --will-payload die --will-qos 2 -t topic -i sub -h 192.168.1.1
   ```

2. 客户端 clientid=alive 在 192.168.1.1（EMQ服务器) 订阅遗嘱主题

   ```
   mosquitto_sub -t test -i alive -q 2 -h 192.168.1.1
   ```

3. 异常断开Sub端与Server端（EMQ服务器）连接，Pub端收到Will Message 。

## 高级使用场景

这里介绍一下如何将 Retained 消息与Will 消息结合起来进行使用。

1. 客户端 A 遗嘱消息设定为”offline“，该遗嘱主题与一个普通发送状态的主题设定成同一个 `A/status`；
2. 当客户端 A 连接时，向主题 `A/status` 发送 “online” 的 Retained 消息，其它客户端订阅主题 `A/status`的时候，获取 Retained 消息为 “online” ；
3. 当客户端 A 异常断开时，系统自动向主题 `A/status` 发送”offline“的消息，其它订阅了此主题的客户端会马上收到”offline“消息；如果遗嘱消息被设定了 Retained 的话，这时有新的订阅`A/status`主题的客户端上线的时候，获取到的消息为“offline”。




