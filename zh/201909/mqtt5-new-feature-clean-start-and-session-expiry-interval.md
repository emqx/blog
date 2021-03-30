
### 前言

MQTT v5.0 中的 Clean Start 与 Session Expiry Interval，对于有 MQTT v3.1.1 版本协议使用经验的朋友，一定不会感觉陌生，因为这两个字段与之前版本中的 Clean Session 非常相似。但它们在实际使用中远比 Clean Session 灵活，下文将详细介绍这几个字段的作用与区别。

### MQTT v3.1.1 版本的 Clean Session

> 如果 Clean Session 设置为 0，服务端必须使用与 Client ID 关联的会话来恢复与客户端的通信。如果不存在这样的会话，服务器必须创建一个新会话。客户端和服务器在断开连接后必须存储会话的状态。

> 如果 Clean Session 设置为 1，客户端和服务器必须丢弃任何先前的会话并创建一个新的会话。该会话的生命周期将和网络连接保持一致，其会话状态一定不能被之后的任何会话重用。

![1.png](https://static.emqx.net/images/0a1253b7c6915be73a459a107c67188c.png)

可以看出，MQTT 期望通过这种持久会话的机制避免客户端掉线重连后消息的丢失，并且免去客户端连接后重复的订阅流程。这一功能在带宽小，网络不稳定的物联网场景中非常实用。但 Clean Session 同时限定了客户端和服务器在连接和断开连接两种状态下的行为，这并不是一个很好的实现。此外，在某些场景下会话并不需要服务器永久保留自己的状态时，这个机制将会导致服务器资源的浪费。

### MQTT v5.0 版本的 Clean Start 与 Session Expiry Interval

> 如果 CONNECT 报文中的 Clean Start 为 1，客户端和服务端**必须**丢弃任何已存在的会话，并开始一个新的会话。
>
> 如果 CONNECT 报文中的 Clean Start 为 0 ，并且存在一个关联此客户端标识符的会话，服务端**必须**基于此会话的状态恢复与客户端的通信。如果不存在任何关联此客户端标识符的会话，服务端**必须**创建一个新的会话。

> Session Expiry Interval 以秒为单位，如果 Session Expiry Interval 设置为 0 或者未指定，会话将在网络连接关闭时结束。
>
> 如果 Session Expiry Interval 为 0xFFFFFFFF ，则会话永不过期。
>
> 如果网络连接关闭时（DISCONNECT 报文中的 Session Expiry Interval 可以覆盖 CONNECT 报文中的设置） Session Expiry Interval 大于0，则客户端与服务端**必须**存储会话状态 。

![2.png](https://static.emqx.net/images/3f3b5c920e0ed3a1bf587380dc1d401f.png)

现在，Clean Start 替代了原先的 Clean Session，但不再用于指示是否存储会话状态，仅用于指示服务端在连接时应该尝试恢复之前的会话还是直接创建全新的会话。会话状态在服务端的存储时长则完全交给 Session Expiry Interval 决定。

前面还提到，MQTT v5.0 支持客户端在断开连接时重新指定 Seesion Expiry Interval。这样我们可以非常容易地满足类似客户端网络连接异常断开时会话状态被服务器保留，客户端正常下线时会话则随着连接关闭而结束的场景，只需要客户端在断开连接时将 Session Expiry Interval 设置为 0 即可。即便是一个已经永不过期的会话，客户端也可以在下一次连接中通过设置 Clean Start 为 1 来 "反悔"。

Clean Start 与 Session Expiry Interval 不仅解决了 Clean Session 的遗留问题，同时也扩展了客户端的使用场景，使 MQTT 协议在受限的网络环境下更加实用。

