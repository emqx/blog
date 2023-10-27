## MQTT 连接

我们知道，在 [MQTT 协议](https://www.emqx.com/zh/mqtt-guide)中，存在客户端和 Broker 两种角色，但客户端不能直接相互连接，必须连接至 Broker，由 Broker 完成消息路由。连接只能由客户端发起，首先客户端需要与 Broker 建立 TCP 连接，然后发送 CONNECT 报文，Broker 则响应 CONNACK 报文以表示是否接受此连接。

CONNECT 报文包含客户端标识符（Client Identifier）、用户名（User Name）、密码（Password）等字段，这些字段提供了连接时的必要信息：

**协议名（Protocol Name）、协议版本（Protocol level）**

协议名固定为 MQTT，可用于防火墙识别 MQTT 流量；协议版本标识当前使用的 MQTT 协议版本，Broker 可以根据这个字段判断自己能否为此客户端提供服务。

**保持连接（Keep Alive）**

表示客户端的最大报文发送时间间隔，如果客户端未能在保持连接时间内保持通讯，那么 Broker 将会断开当前连接。在 MQTT 5.0 中，Broker 返回的 CONNACK 报文中可能包含服务器保持连接（Server Keep Alive）字段，它的主要作用是通知客户端 Broker 将会比客户端指定的保持连接更快地断开非活动的客户端，此时客户端应当将 Broker Keep Alive 的值作为连接建立后的最大报文发送时间间隔。

**Clean Start**

表明是否需要 Broker 为当前连接复用已存在的会话，详见 [全新开始标识与会话过期间隔](https://www.emqx.com/zh/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)。

**客户端标识符（Client Identifier）**

将被 Broker 用于唯一标识客户端以及客户端的当前状态，例如客户端的订阅列表，报文收发状态等。客户端断开重连时，Broker 将根据 Client ID 来完成会话的恢复。

**用户名（User Name）、密码（Password）**

可选字段，用于 Broker 进行身份验证和授权。

**遗嘱主题（Will Topic）、遗嘱载荷（Will Payload） 等字段**

可选字段，用于指定遗嘱消息主题、QoS、Payload 等内容，详见 [MQTT 遗嘱消息](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)。

## MQTT 5.0 连接属性

除了以上字段，[MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 新引入了属性概念，不同类型报文拥有不同的属性，进一步增强了协议的可扩展性。

### 能力协商

CONNECT 和 CONNACK 报文中新增的属性字段，主要是增强了客户端与 Broker 之间的协商能力。例如可以通过最大报文长度（Maximum Packet Size）属性协商 Client 和 Broker 各自能够接受的最大报文长度，Broker 可以通过最大 QoS （Maximum QoS）属性告知 Client 自己能够支持的最大服务质量，以便 Client 决定更改后续 PUBLISH 报文的 QoS 亦或是断开连接。

与最大报文长度（Maximum Packet Size）属性类似的，还有会话过期间隔（Session Expiry Interval）、接收最大值（Receive Maximum）和主题别名最大值（Topic Alias Maximum）属性，这些属性同时存在于 CONNECT 和 CONNACK 报文中，因此可以在连接过程中相互告知对方自己的处理能力，使对方能够按照自己的期望提供服务。

### 可选的服务端功能

考虑到不是所有 MQTT Broker 都是完整实现，可能无法提供完整的 MQTT 5.0 功能，因此 MQTT 5.0 还支持了可选的服务端功能。CONNACK 报文中的 Retain Available 属性可用于声明是否支持[保留消息](https://www.emqx.com/zh/blog/message-retention-and-message-expiration-interval-of-emqx-mqtt5-broker)，Wildcard Subscription Available 属性可用于声明是否支持通配符订阅，Subscription Identifier Available 属性可用于声明是否支持订阅标志符，Shared Subscription Available 属性可用于声明是否支持[共享订阅](https://www.emqx.com/zh/blog/introduction-to-mqtt5-protocol-shared-subscription)。客户端应当遵循这些声明进行后续的操作。

### 自动分配 Client ID

通过 CONNACK 报文中的 Assigned Client Identifier 属性，MQTT 5.0 还提供了一个非常便捷的功能，即允许由 Broker 统一为 Client 分配 Client ID，而不是由 Client 自行指定，毕竟提前为 Client 分配一个全局唯一的 Client ID 在某些场景下不是一件容易的事情。这个全新特性的使用也非常简单，只要 Client 在连接时提供一个零字节的 Client ID，Broker 就会在响应的 CONNACK 报文中携带 Assigned Client Identifier 属性，该属性的值就是自动分配的 Client ID。Client 可以一直持有和使用这个 Client ID，直到会话过期。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
