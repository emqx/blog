

MQTT 协议通过交换预定义的MQTT控制报文来通信。下面以 **[MQTTX](https://github.com/emqx/MQTTX)** 为例，展示如何通过 MQTT 报文实现发布订阅功能。

## Connect 连接

MQTT 协议基于 TCP/IP 协议，MQTT Broker 和 Client 都有需要有 TCP/IP 地址。

### Broker

![WX201911281137582x.png](https://static.emqx.net/images/fa35a1bc1853bc8862bfd9b826f8a2e0.png)

如果你暂时没有一个可用的 MQTT Broker，[EMQ X](https://github.com/emqx/emqx) 提供了一个公共 Broker 地址用于测试：`broker.emqx.io:1883`。

### Client

![WX201911281139012x.png](https://static.emqx.net/images/2d7c94b7259b93c461408601181d4626.png)

MQTTX 工具中 Client 的配置其实是 MQTT 协议中 Connect 报文的配置，下面解释一下相关配置项：

#### Client ID

服务端使用 ClientId 识别客户端。连接服务端的每个客户端都有唯一的 ClientId 。客户端和服务端都必须使用 ClientId 识别两者之间的 MQTT 会话相关的状态。

ClientId 必须存在，但是服务端可以允许客户端提供一个零字节的 ClientId，如果这样做了，服务端必须将这看作特殊情况并分配唯一的 ClientId 给那个客户端。然后正常处理这个 CONNECT 报文。

#### Username/Password

MQTT 可以通过发送用户名和密码来进行相关的认证和授权，但是，如果此信息未加密，则用户名和密码是以明文的方式发送的。EMQ X 不仅支持SSL/TLS 加密，还提供了 **[emqx-auth-username](https://github.com/emqx/emqx-auth-username)** 插件对密码进行加密。

#### Keep Alive

保持连接（Keep  Alive）是一个以秒为单位的时间间隔，它是指在客户端传输完成一个控制报文的时刻到发送下一个报文的时刻，两者之间允许空闲的最大时间间隔。客户端负责保证控制报文发送的时间间隔不超过保持连接的值。如果没有任何其它的控制报文可以发送，客户端必须发送一个PINGREQ报文。

如果 Keep Alive 的值非零，并且服务端在一点五倍的 Keep Alive 时间内没有收到客户端的控制报文，它必须断开客户端的网络连接，认为网络连接已断开。

#### Clean Session

客户端和服务端可以保存会话状态，以支持跨网络连接的可靠消息传输，这个标志告诉服务器这次连接是不是一个全新的连接。

客户端的会话状态包括：

- 已经发送给服务端，但是还没有完成确认的 QoS 1 和 QoS 2 级别的消息
- 已从服务端接收，但是还没有完成确认的 QoS 2 级别的消息。

服务端的会话状态包括：

- 会话是否存在，即使会话状态的其它部分都是空。
- 客户端的订阅信息。
- 已经发送给客户端，但是还没有完成确认的 QoS 1 和 QoS 2 级别的消息。
- 即将传输给客户端的 QoS 1和 QoS 2 级别的消息。
- 已从客户端接收，但是还没有完成确认的 QoS 2 级别的消息。
- 可选，准备发送给客户端的 QoS 0 级别的消息。 

如果 CleanSession 标志被设置为 1，客户端和服务端必须丢弃之前的任何会话并开始一个新的会话。会话仅持续和网络连接同样长的时间。

如果 CleanSession 标志被设置为 0，服务端必须基于当前会话（使用 ClientId 识别）的状态恢复与客户端的通信。如果没有与这个客户端标识符关联的会话，服务端必须创建一个新的会话。当连接断开后，客户端和服务端必须保存会话信息。

## Connack 确认连接请求

客户端发送 Connect 报文请求对服务器的连接，服务器必须发送 Connack 报文作为对 来自客户端的 Connect 报文的回应。如果客户端在合理的时间内没有收到服务端的CONNACK报文，客户端应该关闭网络连接。合理的时间取决于应用的类型和通信基础设施。在 **[MQTTX](https://github.com/emqx/MQTTX)** 中，可以通过 Connection Timeout 来设置合理的超时时间。

![Connect.png](https://static.emqx.net/images/67b64e84c52a7bb12474704f48954dcf.png)

Connack 报文包含 Session Present 和 Connect Return code 两个重要的标志。 

#### Session Present

Session Present 标志表示当前会话是否是一个新的会话，如果服务端收到 CleanSession 标志为1的连接，Connack报文中的 SessionPresent 标志为 0 。如果服务端收到一个 CleanSession 为0的连接，SessionPresent 标志的值取决于服务端是否已经保存了 ClientId 对应客户端的会话状态。如果服务端已经保存了会话状态，Connack 报文中的 SessionPresent 标志为 1，如果服务端没有已保存的会话状态，Connack 报文中的 SessionPresent 标志为 0.

#### Connect Return code 

Connect Return code 表示服务器对此次 Connect 的回应，0 表示连接已被服务器接受。如果服务端收到一个合法的 CONNECT 报文，但出于某些原因无法处理它，服务端应该尝试发送一个包含非零返回码（表格中的某一个）的 CONNACK 报文。如果服务端发送了一个包含非零返回码的CONNACK 报文，那么它必须关闭网络连接。

| **值** | **返回码响应**                       | **描述**                                          |
| ------ | ------------------------------------ | ------------------------------------------------- |
| 0      | 0x00连接已接受                       | 连接已被服务端接受                                |
| 1      | 0x01连接已拒绝，不支持的协议版本     | 服务端不支持客户端请求的MQTT协议级别              |
| 2      | 0x02连接已拒绝，不合格的客户端标识符 | 客户端标识符是正确的UTF-8编码，但服务端不允许使用 |
| 3      | 0x03连接已拒绝，服务端不可用         | 网络连接已建立，但MQTT服务不可用                  |
| 4      | 0x04连接已拒绝，无效的用户名或密码   | 用户名或密码的数据格式无效                        |
| 5      | 0x05连接已拒绝，未授权               | 客户端未被授权连接到此服务器                      |
| 6-255  |                                      | 保留                                              |

如果认为上表中的所有连接返回码都不太合适，那么服务端必须关闭网络连接，不需要发送CONNACK 报文。

## Subscribe 订阅主题

客户端向服务端发送 Subscribe 报文用于创建一个或多个订阅。每个订阅注册客户端关心的一个或多个主题。为了将应用消息转发给与那些订阅匹配的主题，服务端发送 Publish 报文给客户端。Subscribe 报文为每个订阅指定了最大的 QoS 等级，服务端根据这个发送应用消息给客户端。

![WX201911281425432x.png](https://static.emqx.net/images/24eb2af44dbe5c9b71dc8912144f08cf.png)

Subscribe 报文的有效载荷必须包含至少一对主题过滤器 和 QoS 等级字段组合。没有有效载荷的 Subscribe 报文是违反协议的。

使用 **[MQTTX](https://github.com/emqx/MQTTX)** 连接 `broker.emqx.io:1883` 的 Broker 并创建主题为`testtopic/#` ，Qos 等于 2 的订阅。

![WX201911281439252x.png](https://static.emqx.net/images/513810cc3ba2cdbc613ad9c662e25b80.png)

## Suback 订阅确认

服务端发送 Suback 报文给客户端，用于确认它已收到并且正在处理 Subscribe 报文。

![Subscribe.png](https://static.emqx.net/images/536d4ac3f53df2fdbc497d372f01febd.png)

Suback 报文包含一个原因码列表，用于指定授予的最大QoS等级或 Subscribe 报文所请求的每个订阅发生的错误,每个原因码对应 Subscribe 报文中的一个主题过滤器。Suback 报文中的原因码顺序必须与 Subscribe 报文中的主题过滤器顺序相匹配

允许的返回码值：

- 0x00 - 最大QoS 0
- 0x01 - 成功 – 最大QoS 1
- 0x02 - 成功 – 最大 QoS 2
- 0x80 - Failure  失败



## Publish 发布消息

Publish 报文是指从客户端向服务端或者服务端向客户端传输一个应用消息，服务器收到  Publish  报文后根据主题过滤器将消息转发给其他客户端。

![Publish.png](https://static.emqx.net/images/236e05ccee50fda64c4d0808fa2a39b4.png)

尝试使用 **[MQTTX](https://github.com/emqx/MQTTX)** 发布一条主题为 `testtopic/mytopic` ，内容为 `{"msg": "hello world"}` 的消息，由于之前已经订阅了 `testtopic/#` 这一主题，所以立即接收到了 Broker 转发回来的这条消息

![WX201911281441422x.png](https://static.emqx.net/images/70abc02e1ade4a4a49031c43bd9b8942.png)

#### Topic

主题名（Topic Name）用于识别消息应该被发布到哪一个会话，服务端发送给订阅客户端的 Publish 报文的主题名必须匹配该订阅的主题过滤器。

#### QoS

QoS 表示应用消息分发的服务质量等级保证

| **QoS值** | **Bit 2** | **Bit 1** | **描述**     |
| --------- | --------- | --------- | ------------ |
| 0         | 0         | 0         | 最多分发一次 |
| 1         | 0         | 1         | 至少分发一次 |
| 2         | 1         | 0         | 只分发一次   |
| -         | 1         | 1         | 保留位       |

Publish 报文不能将 QoS 所有的位设置为 1。如果服务端或客户端收到 QoS 所有位都为 1 的 Publish 报文，它必须关闭网络连接。

关于不同等级的QoS的工作原理，请查阅[MQTT 5.0 协议介绍 - QoS 服务质量](https://www.emqx.cn/blog/introduction-to-mqtt5-protocol-qos)。

#### Retain

如果客户端发给服务端的 Publish 报文的保留（RETAIN）标志被设置为 1，服务端必须存储这个应用消息和它的服务质量等级（QoS），以便它可以被分发给未来的主题名匹配的订阅者 。一个新的订阅建立时，对每个匹配的主题名，如果存在最近保留的消息，它必须被发送给这个订阅者。如果服务端收到一条保留（RETAIN）标志为1的Q消息，它必须丢弃之前为那个主题保留的任何消息，并将这个新的消息当作那个主题的新保留消息。

保留标志为 1 且有效载荷为零字节的 Publish 报文会被服务端当作正常消息处理，它会被发送给订阅主题匹配的客户端。此外，同一个主题下任何现存的保留消息必须被移除，因此这个主题之后的任何订阅者都不会收到一个保留消息

服务端发送 Publish 报文给客户端时，如果消息是作为客户端一个新订阅的结果发送，它必须将报文的保留标志设为 1。当一个 Publish 报文发送给客户端是因为匹配一个已建立的订阅时，服务端必须将保留标志设为 0，不管它收到的这个消息中保留标志的值是多少。

如果客户端发给服务端的 Publish 报文的保留标志位 0，服务端不能存储这个消息也不能移除或替换任何现存的保留消息。

#### Payload

有效载荷包含将被发布的应用消息。数据的内容和格式是应用特定的，可以发送图像，任何编码的文本，加密的数据以及几乎所有二进制数据。

