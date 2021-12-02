## MQTT v3.1.1 

MQTT v3.1.1 协议只有 10 种返回码，这些返回码所能表示的含义很少，且相同的返回码的值在不同的报文中可以有不同的含义。

### CONNACK 报文

在 CONNECT 报文中只有 6 种返回码，只有当服务器发回的 CONNACK 报文的返回码为 0时才表示连接建立成功。

|  值   |              返回码               |                        描述                         |
| :---: | :-------------------------------: | :-------------------------------------------------: |
|   0   |           0x00 接受连接           |                      接受连接                       |
|   1   |  0x01 拒绝连接，不支持的协议版本  |        服务器不支持该客户端请求的 MQTT 协议         |
|   2   |  0x02 拒绝连接， 拒绝的客户端 ID  | 客户端 ID 是正确的 UTF-8 字符串，但是不被服务器允许 |
|   3   |    0x03 拒绝连接，服务器不可用    |       网络连接已经建立，但是 MQTT 服务不可用        |
|   4   | 0x04 拒绝连接，损坏的用户名或密码 |         在用户名或密码中的数据是错误格式的          |
|   5   |       0x05 拒绝连接，未授权       |                客户端的连接未被授权                 |
| 6-255 |                                   |                   预留给将来使用                    |

### SUBACK 报文

在 SUBACK 报文中只有 4 种返回码

| 值   | 返回码    | 描述                  |
| ---- | --------- | --------------------- |
| 0    | 0x00 成功 | 最大允许 QoS 0 的消息 |
| 1    | 0x01 成功 | 最大允许 QoS 1 的消息 |
| 2    | 0x02 成功 | 最大允许 QoS 2 的消息 |
| 128  | 0x80 失败 | 失败                  |

SUBACK 报文有四种返回码，除了返回码 0x80 表示失败，其他返回码都表示订阅成功， 3 个值 0, 1, 2 分别代表订阅接收到的消息的最大 QoS 值。

## MQTT v5.0

MQTT v5.0 协议将返回码改名成了原因码，增加了用于表示更多类型的错误的原因码。

下表是原因码列表，分别表示的是原因码的值以及包含原因码的控制报文：

| 十进制 | 十六进制 | 名称                                                        | 报文                                                     |
| ------ | -------- | ----------------------------------------------------------- | -------------------------------------------------------- |
| 0      | 0x00     | 成功 (Success)                                              | CONNACK, PUBACK, PUBREC, PUBREL, PUBCOMP, UNSUBACK, AUTH |
| 0      | 0x00     | 准许 QoS 0 (Granted QoS 0)                                  | SUBACK                                                   |
| 1      | 0x01     | 准许 QoS 1 (Granted QoS 1)                                  | SUBACK                                                   |
| 2      | 0x02     | 准许 QoS 2 (Granted QoS 2)                                  | SUBACK                                                   |
| 4      | 0x04     | 以遗嘱消息断开连接 (Disconnect with Will Message)           | DISCONNECT                                               |
| 16     | 0x10     | 没有匹配的订阅者 (No matching subscribers)                  | PUBACK, PUBREC                                           |
| 17     | 0x11     | 没有订阅 (No subscription existed)                          | UNSUBACK                                                 |
| 24     | 0x18     | 继续认证 (Continue authentication)                          | AUTH                                                     |
| 25     | 0x19     | 重新认证 (Re-authenticate)                                  | AUTH                                                     |
| 128    | 0x80     | 未指定错误 (Unspecified error)                              | CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT    |
| 129    | 0x81     | 畸形报文 (Malformed Packet)                                 | CONNACK, DISCONNECT                                      |
| 130    | 0x82     | 协议错误 (Protocol Error)                                   | CONNACK, DISCONNECT                                      |
| 131    | 0x83     | 实现特有错误 (Implementation specific error)                | CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT    |
| 132    | 0x84     | 不支持的协议版本 (Unsupported Protocol Version)             | CONNACK                                                  |
| 133    | 0x85     | 客户端标识符无效 (Client Identifier not valid)              | CONNACK                                                  |
| 134    | 0x86     | 错误的用户名和密码 (Bad User Name or Password)              | CONNACK                                                  |
| 135    | 0x87     | 未授权 (Not authorized)                                     | CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT    |
| 136    | 0x88     | 服务器不可用 (Server unavailable)                           | CONNACK                                                  |
| 137    | 0x89     | 服务器繁忙 (Server busy)                                    | CONNACK, DISCONNECT                                      |
| 138    | 0x8A     | 禁止访问 (Banned)                                           | CONNACK                                                  |
| 139    | 0x8B     | 服务器关机中 (Server shutting down)                         | DISCONNECT                                               |
| 140    | 0x8C     | 错误验证方法 (Bad authentication method)                    | CONNACK, DISCONNECT                                      |
| 141    | 0x8D     | 保活超时 (Keep Alive timeout)                               | DISCONNECT                                               |
| 142    | 0x8E     | 会话被接管 (Session taken over)                             | DISCONNECT                                               |
| 143    | 0x8F     | 主题过滤器无效 (Topic Filter invalid)                       | SUBACK, UNSUBACK, DISCONNECT                             |
| 144    | 0x90     | 主题名无效 (Topic Name invalid)                             | CONNACK, PUBACK, PUBREC, DISCONNECT                      |
| 145    | 0x91     | 报文标识符在使用中 (Packet Identifier in use)               | PUBACK, PUBREC, SUBACK, UNSUBACK                         |
| 146    | 0x92     | 没有发现报文标识符 (Packet Identifier not found)            | PUBREL, PUBCOMP                                          |
| 147    | 0x93     | 超出接收最大值 (Receive Maximum exceeded)                   | DISCONNECT                                               |
| 148    | 0x94     | 主题别名无效 (Topic Alias invalid)                          | DISCONNECT                                               |
| 149    | 0x95     | 报文太大 (Packet too large)                                 | CONNACK, DISCONNECT                                      |
| 150    | 0x96     | 消息传输速率太高 (Message rate too high)                    | DISCONNECT                                               |
| 151    | 0x97     | 超出限额 (Quota exceeded)                                   | CONNACK, PUBACK, PUBREC, SUBACK, DISCONNECT              |
| 152    | 0x98     | 管理行为 (Administrative action)                            | DISCONNECT                                               |
| 153    | 0x99     | 有效载荷格式无效 (Payload format invalid)                   | PUBACK, PUBREC, DISCONNECT                               |
| 154    | 0x9A     | 不支持消息保留 (Retain not supported)                       | CONNACK, DISCONNECT                                      |
| 155    | 0x9B     | 不支持的QoS (QoS not supported)                             | CONNACK, DISCONNECT                                      |
| 156    | 0x9C     | 使用另一台服务器 (Use another server)                       | CONNACK, DISCONNECT                                      |
| 157    | 0x9D     | 服务器被移除 (Server moved)                                 | CONNACK, DISCONNECT                                      |
| 158    | 0x9E     | 不支持的共享订阅 (Shared Subscription not supported)        | SUBACK, DISCONNECT                                       |
| 159    | 0x9F     | 超出连接速率 (Connection rate exceeded)                     | CONNACK, DISCONNECT                                      |
| 160    | 0xA0     | 最大连接时间 (Maximum connect time)                         | DISCONNECT                                               |
| 161    | 0xA1     | 不支持的订阅标识符 (Subscription Identifiers not supported) | SUBACK, DISCONNECT                                       |
| 162    | 0xA2     | 不支持的通配符订阅 (Wildcard Subscription not supported)    | SUBACK, DISCONNECT                                       |

原因码是用来表明操作结果的一个单字节无符号值，小于 0x80 的原因码表明操作的结果是成功的，正常情况下，操作成功返回的原因码值为 0。 如果返回的原因码大于等于 0x80，就说明操作失败了。



CONNACK, PUBACK, PUBREC, PUBREL, PUBCOMP, DISCONNECT 和 AUTH 控制报文的原因码存在可变报头中。而 SUBACK 和 UNSUBACK 报文在有效载荷中包含了一张原因码的列表。
