## Reason Code

Reason Code 在 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 中的主要作用是为客户端和服务端提供更详细的反馈。比如我们可以在 CONNACK 报文中将用户名或密码错误对应的 Reason Code 反馈给客户端，这样客户端就能够知道自己无法连接的原因。

### MQTT 3.1.1 中的 Reason Code

虽然 MQTT 3.1.1 就已经支持了 Reason Code，但它并没有定义太多可用的 Reason Code。

在仅有的两个支持 Reason Code 的报文中，CONNACK 报文只有 5 个用于指示失败的 Reason Code，SUBACK 报文则仅仅只有一个用于指示失败的 Reason Code，无法进一步指示订阅失败的原因。而对于发布、取消订阅这些不支持 Reason Code 的操作，我们更是连操作是否成功都无法知晓。这不仅对于开发调试非常地不友好，也不利于实现健壮的代码。

### MQTT 5.0 中的 Reason Code

所以在 MQTT 5.0 中，可用的 Reason Code 被扩充到了 43 个，并且规定了小于 0x80 的 Reason Code 用于表示成功，大于等于 0x80 的 Reason Code 则用于表示失败。而不再像 MQTT 3.1.1 那样，小于 0x80 的 Reason Code 也可能表示失败。这使得客户端能够更轻松地判断操作是否成功。

另外 MQTT 5.0 中支持 Reason Code 的报文也扩展到了：CONNACK、PUBACK、PUBREC、PUBREL、PUBCOMP、SUBACK、UNSUBACK、DISCONNECT 以及 AUTH。现在，我们不仅可以知道消息发布是否成功，还可以知道失败的原因，例如当前不存在匹配的订阅者、或者无权向这个主题发布消息等等。

|            | **Reason Codes in MQTT 3.1.1** | **Reason Codes in MQTT 5.0** |
| :--------- | :----------------------------- | :--------------------------- |
| CONNACK    | ✅                          | ✅                        |
| DISCONNECT | ❌                               | ✅                        |
| PUBACK     | ❌                               | ✅                        |
| PUBREC     | ❌                               | ✅                        |
| PUBREL     | ❌                               | ✅                        |
| PUBCOMP    | ❌                               | ✅                        |
| SUBACK     | ✅                               | ✅                        |
| UNSUBACK   | ❌                               | ✅                        |
| AUTH       | ❌                               | ✅                        |



大部分报文都只会包含一个 Reason Code，除了 SUBACK 和 UNSUBACK。这是因为 SUBSCRIBE 和 UNSUBSCRIBE 报文可以包含多个主题过滤器，而每个主题过滤器都必须有一个对应的 Reason Code 来指示其操作结果，所以 SUBACK 和 UNSUBACK 报文也需要能够包含多个 Reason Codes。这也是为什么其他报文中的 Reason Code 都位于可变报头，而 SUBACK 和 UNSUBACK 的 Reason Code 则位于载荷部分。

![MQTT packets](https://assets.emqx.com/images/88c20ac1b674ba912d68c0045043ff8e.png)

在本文最后的 Reason Code 速查表中，我们详细地解释了 MQTT 5.0 每个 Reason Code 的含义和使用场景，您可以自行查阅。

#### 向客户端指示连接断开的原因

在 MQTT 3.1 和 3.1.1 中，DISCONNECT 报文只能由客户端发布。所以当客户端违反某些限制时，服务端只能直接关闭网络连接，而无法向客户端传递更多信息，这导致调查连接断开原因变得困难重重。

而在 MQTT 5.0 中，服务端可以在关闭网络连接之前向客户端发送 DISCONNECT 报文，而客户端则可以通过 DISCONNECT 报文中的 Reason Code 了解连接被断开的原因，比如报文过大、服务器正忙等等。

## Reason String

Reason String 是 MQTT 5.0 对 Reason Code 的一个补充，它是一个为诊断而设计的人类可读的字符串。虽然 Reason Code 已经能够指示大部分的错误原因，但对于开发者或运维人员来说，可能仍然缺少更直观的上下文信息。

比如当服务端通过 Reason Code 向客户端指示主题过滤器不合法（0x8F）时，开发者仍然无从知晓具体的原因，是主题层级过多？还是包含了不被服务端接受的字符？而如果服务端可以返回一个内容类似于 "The number of topic levels exceeds the limit, the maximum is 10." 的 Reason String，那么开发者很快就能够知道原因并做出调整。

在实际使用中，Reason String 的内容取决于客户端和服务端的具体实现，所以一个实现正确的接收端不应该尝试解析 Reason String 的内容，推荐的使用方式包括但不限于在抛出异常时使用 Reason String，或者将它写入日志。

最后，Reason String 是一个可选的功能，是否会收到 Reason String 取决于对端是否支持。

 

## MQTT 5.0 Reason Code 速查表

| **Reason Code** | **Name**                               | **Packets**                                              | **Details**                                                  |
| :-------------- | :------------------------------------- | :------------------------------------------------------- | :----------------------------------------------------------- |
| 0x00 (0)        | Success                                | CONNACK, PUBACK, PUBREC, PUBREL, PUBCOMP, UNSUBACK, AUTH | 这个 Reason Code 可以用在所有存在 Reason Code 的报文中，例如 CONNACK、DISCONNECT 报文等等。它通常用于表示成功，比如连接成功、取消订阅成功、消息接收成功和认证成功等等。 |
| 0x00 (0)        | Normal disconnection                   | DISCONNECT                                               | 在 DISCONNECT 报文中，0 则表示连接正常断开，这种情况下遗嘱消息不会被发布。 |
| 0x00 (0)        | Granted QoS 0                          | SUBACK                                                   | 0，1，2 在 SUBACK 这个订阅确认报文中，用来指示订阅结果，它们都表示订阅成功，同时向订阅端指示最终被授予的最大 QoS 等级，0，1，2 正好对应了三个 QoS 等级。 这是因为服务端最终授予的最大 QoS 等级，可能小于订阅时请求的最大 QoS 等级。比如订阅时请求的最大 QoS 等级是 2，但服务端最高仅支持 QoS 1 等等。 |
| 0x01 (1)        | Granted QoS 1                          | SUBACK                                                   | -                                                            |
| 0x02 (2)        | Granted QoS 2                          | SUBACK                                                   | -                                                            |
| 0x04 (4)        | Disconnect with Will Message           | DISCONNECT                                               | 仅用于 DISCONNECT 报文，适用于客户端希望正常断开连接但服务端仍然需要发布遗嘱消息的情况，比如客户端希望会话过期时可以对外发出通知。 |
| 0x10 (16)       | No matching subscribers                | PUBACK, PUBREC                                           | 这个 Reason Code 用于向发送方指示，消息已经收到，但是当前没有匹配的订阅者，所以只有服务端可以使用这个 Reason Code。我们可以通过收到 Reason Code 为 0x10 的响应报文得知当前没有人会收到自己的消息，但是不能通过没有收到 Reason Code 为 0x10 的响应报文来假定所有人都会收到自己的消息，除非最多只会存在一个订阅者。但需要注意，没有匹配的订阅者时使用 0x10 替代 0x00，并不是一个必须实现的行为，这取决于服务端的具体实现。 |
| 0x11 (17)       | No subscription existed                | UNSUBACK                                                 | 仅用于 UNSUBACK 报文，表示取消订阅时没有发现匹配的订阅。     |
| 0x18 (24)       | Continue authentication                | AUTH                                                     | 仅用于 AUTH 报文，表示继续认证，通过这个 Reason Code，客户端和服务端之间可以进行任意次数的 AUTH 报文交换，以满足不同的认证方法的需要。 |
| 0x19 (25)       | Re-authenticate                        | AUTH                                                     | 仅用于 AUTH 报文，在增强认证成功后客户端可以随时通过发送 Reason Code 为 0x19 的 AUTH 报文发起重新认证。重新认证期间，其他报文收发会正常继续，如果重新认证失败，连接就会被关闭。 |
| 0x80 (128)      | Unspecified error                      | CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT    | 表示未指明的错误。当一方不希望向另一方透露错误的具体原因，或者协议规范中没有能够匹配当前情况的 Reason Code 时，那么它可以在报文中使用这个 Reason Code。 |
| 0x81 (129)      | Malformed Packet                       | CONNACK, DISCONNECT                                      | 当收到了无法根据协议规范正确解析的控制报文时，接收方需要发送 Reason Code 为 0x81 的 DISCONNECT 报文来断开连接。如果是 CONNECT 报文存在问题，那么服务端应该使用 CONNACK 报文。当控制报文中出现固定报头中的保留位没有按照协议要求置 0、QoS 被指定为 3、UTF-8 字符串中包含了一个空字符等等这些情况时，都将被认为是一个畸形的报文。 |
| 0x82 (130)      | Protocol Error                         | CONNACK, DISCONNECT                                      | 在控制报文被按照协议规范解析后检测到的错误，比如包含协议不允许的数据，行为与协议要求不符等等，都会被认为是协议错误。接收方需要发送 Reason Code 为 0x81 的 DISCONNECT 报文来断开连接。如果是 CONNECT 报文存在问题，那么服务端应该使用 CONNACK 报文。常见的协议错误包括，客户端在一个连接内发送了两个 CONNECT 报文、一个报文中包含了多个相同的属性，以及某个属性被设置成了一个协议不允许的值等等。但是当我们有其他更具体的 Reason Code 时，就不会使用 0x81 (Malformed Packet) 或者 0x82 (Protocol Error) 了。例如，服务端已经声明自己不支持保留消息，但客户端仍然向服务端发送保留消息，这本质上也属于协议错误，但我们会选择使用 0x9A (Retain not supported) 这个能够更清楚指明错误原因的 Reason Code。 |
| 0x83 (131)      | Implementation specific error          | CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT    | 报文有效，但是不被当前接收方的实现所接受。                   |
| 0x84 (132)      | Unsupported Protocol Version           | CONNACK                                                  | 仅用于 CONNACK 报文。对于支持了 MQTT 5.0 的服务端来说，如果不支持客户端当前使用的 MQTT 协议版本，或者客户端指定了一个错误的协议版本或协议名。例如，客户端将协议版本设置为 6，那么服务端可以发送 Reason Code 为 0x84 的 CONNACK 报文，表示不支持该协议版本并且表明自己 MQTT 服务端的身份，然后关闭网络连接。当然服务端也可以选择直接关闭网络连接，因为使用 MQTT 3.1 或 3.1.1 的 MQTT 客户端可能并不能理解 0x84 这个 Reason Code 的含义。这两个版本都是在 CONNACK 报文使用 0x01 来表示不支持客户端指定的协议版本。 |
| 0x85 (133)      | Client Identifier not valid            | CONNACK                                                  | 仅用于 CONNACK 报文，表示 Client ID 是有效的字符串，但是服务端不允许。可能的情形有 Clean Start 为 0 但 Client ID 为空、或者 Client ID 超出了服务端允许的最大长度等等。 |
| 0x86 (134)      | Bad User Name or Password              | CONNACK                                                  | 仅用于 CONNACK 报文，表示客户端使用了错误的用户名或密码，这也意味着客户端将被拒绝连接。 |
| 0x87 (135)      | Not authorized                         | CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT    | 当客户端使用 Token 认证或者增强认证时，使用 0x87 来表示客户端没有被授权连接会比 0x86 更加合适。当客户端进行发布、订阅等操作时，如果没有通过服务端的授权检查，那么服务端也可以在 PUBACK 等应答报文中指定 0x87 这个 Reason Code 来指示授权结果。 |
| 0x88 (136)      | Server unavailable                     | CONNACK                                                  | 仅用于 CONNACK 报文，向客户端指示当前服务端不可用。比如当前服务端认证服务异常无法接入新客户端等等。 |
| 0x89 (137)      | Server busy                            | CONNACK, DISCONNECT                                      | 向客户端指示服务端正忙，请稍后再试。                         |
| 0x8A (138)      | Banned                                 | CONNACK                                                  | 仅用于 CONNACK 报文，表示客户端被禁止登录。例如服务端检测到客户端的异常连接行为，所以将这个客户端的 Client ID 或者 IP 地址加入到了黑名单列表中，又或者是后台管理人员手动封禁了这个客户端，当然以上这些通常需要视服务端的具体实现而定。 |
| 0x8B (139)      | Server shutting down                   | DISCONNECT                                               | 仅用于 DISCONNECT 报文，并且只有服务端可以使用。如果服务端正在或即将关闭，它可以通过主动发送 Reason Code 为 0x8B 的 DISCONNECT 报文的方式告知客户端连接因为服务端正在关闭而被终止。这可以帮助客户端避免在连接关闭后继续向此服务端发起连接请求。 |
| 0x8C (140)      | Bad authentication method              | CONNACK, DISCONNECT                                      | 当服务端不支持客户端指定的增强认证方法，或者客户端在重新认证时使用了和之前认证不同的认证方法时，那么服务端就会发送 Reason Code 为 0x8C 的 CONNACK 或者 DISCONNECT 报文。 |
| 0x8D (141)      | Keep Alive timeout                     | DISCONNECT                                               | 仅用于 DISCONNECT 报文，并且只有服务端可以使用。如果客户端没能在 1.5 倍的 Keep Alive 时间内保持通信，服务端将会发送 Reason Code 为 0x8D 的 DISCONNECT 报文然后关闭网络连接。 |
| 0x8E (142)      | Session taken over                     | DISCONNECT                                               | 仅用于 DISCONNECT 报文，并且只有服务端可以使用。当客户端连接到服务端时，如果服务端中已经存在使用相同 Client ID 的客户端连接，那么服务端就会向原有的客户端发送 Reason Code 为 0x8E 的 DISCONNECT 报文，表示会话被新的客户端连接接管，然后关闭原有的网络连接。不管新的客户端连接中的 Clean Start 是 0 还是 1，服务端都会使用这个 Reason Code 向原有客户端指示会话被接管。 |
| 0x8F (143)      | Topic Filter invalid                   | SUBACK, UNSUBACK, DISCONNECT                             | 主题过滤器的格式正确，但是不被服务端接受。比如主题过滤器的层级超过了服务端允许的最大数量限制，或者主题过滤器中包含了空格等不被当前服务端接受的字符。 |
| 0x90 (144)      | Topic Name invalid                     | CONNACK, PUBACK, PUBREC, DISCONNECT                      | 主题名的格式正确，但是不被客户端或服务端接受。               |
| 0x91 (145)      | Packet Identifier in use               | PUBACK, PUBREC, SUBACK, UNSUBACK                         | 表示收到报文中的 Packet ID 正在被使用，例如发送方发送了一个 Packet ID 为 100 的 QoS 1 消息，但是接收方认为当前有一个使用相同 Packet ID 的 QoS 2 消息还没有按成它的报文流程。这通常意味着当前客户端和服务端之前的会话状态不匹配，可能需要通过设置 Clean Start 为 1 重新连接来重置会话状态。 |
| 0x92 (146)      | Packet Identifier not found            | PUBREL, PUBCOMP                                          | 表示未找到对应的 Packet ID，这只会在 QoS 2 的报文交互流程中发生。比如当接收方回复 PUBREC 报文时，发送方未找到使用相同 Packet ID 的等待确认的 PUBLISH 报文，或者当发送方发送 PUBREL 报文时，接收方未找到使用相同 Packet ID 的 PUBREC 报文。这通常意味着当前客户端和服务端之间的会话状态不匹配，可能需要通过设置 Clean Start 为 1 重新连接来重置会话状态。 |
| 0x93 (147)      | Receive Maximum exceeded               | DISCONNECT                                               | 仅用于 DISCONNECT 报文，表示超出了接收最大值。MQTT 5.0 增加了流控机制，客户端和服务端在连接时通过 Receive Maximum 属性约定它们愿意并发处理的可靠消息数（QoS > 0）。所以一旦发送方发送的没有完成确认的消息超过了这一数量限制，接收方就会发送 Reason Code 为 0x93 的 DISCONNECT 报文然后关闭网络连接。 |
| 0x94 (148)      | Topic Alias invalid                    | DISCONNECT                                               | 仅用于 DISCONNECT 报文，表示主题别名不合法。如果 PUBLISH 报文中的主题别名值为 0 或者大于连接时约定的最大主题别名，接收方会将此视为协议错误，它将发送 Reason Code 为 0x94 的 DISCONNECT 报文然后关闭网络连接。 |
| 0x95 (149)      | Packet too large                       | CONNACK, DISCONNECT                                      | 用于表示报文超过了最大允许长度。客户端和服务端各自允许的最大报文长度，可以在 CONNECT 和 CONNACK 报文中通过 Maximum Packet Size 属性约定。当一方发送了过大的报文，那么另一方将发送 Reason Code 为 0x95 的 DISCONNECT 报文，然后关闭网络连接。由于客户端可以在连接时设置遗嘱消息，因此 CONNECT 报文也有可能超过服务端能够处理的最大报文长度限制，此时服务端需要在 CONNACK 报文中使用这个 Reason Code。 |
| 0x96 (150)      | Message rate too high                  | DISCONNECT                                               | 仅用于 DISCONNECT 报文，表示超过了允许的最大消息发布速率。需要注意它与 Quota exceeded 的区别，Message rate 限制消息的发布速率，比如每秒最高可发布多少消息，Quota 限制的是资源的配额，比如客户端每天可以发布的消息数量，但客户端可能在一小时内耗尽它的配额。 |
| 0x97 (151)      | Quota exceeded                         | CONNACK, PUBACK, PUBREC, SUBACK, DISCONNECT              | 用于表示超出了配额限制。服务端可能会对发布端的发送配额进行限制，比如每天最多为其转发 1000 条消息。当发布端的配额耗尽，服务端就会在 PUBACK 等确认报文中使用这个 Reason Code 提醒对方。另一方面，服务端还可能限制客户端的连接数量和订阅数量，当超出这一限制时，服务端就会通过 CONNACK 或者 SUBACK 报文向客户端指示当前超出了配额。一些严格的客户端和服务端，在发现对端超出配额时，可能会选择发送 DISCONNECT 报文然后关闭连接。 |
| 0x98 (152)      | Administrative action                  | DISCONNECT                                               | 仅用于 DISCONNECT 报文，向客户端指示连接因为管理操作而被关闭，例如运维人员在后台踢除了这个客户端连接等等。 |
| 0x99 (153)      | Payload format invalid                 | CONNACK, PUBACK, PUBREC, DISCONNECT                      | 当消息中包含 Payload Format Indicator 属性时，接收方可以检查消息中 Payload 的格式与该属性是否匹配。如果不匹配，接收方需要发送 Reason Code 为 0x99 的确认报文。一些严格的客户端或者服务器，可能会直接发送 DISCONNECT 报文然后关闭网络连接。如果是 CONNECT 报文中的遗嘱消息存在问题，服务端将发送 Reason Code 为 0x99 的 CONNACK 报文然后关闭网络连接。 |
| 0x9A (154)      | Retain not supported                   | CONNACK, DISCONNECT                                      | 当服务端不支持保留消息，但是客户端发送了保留消息时，服务端就会向它发送 Reason Code 为 0x9A 的 DISCONNECT 报文然后关闭网络连接。由于客户端还可以在连接时将遗嘱消息设置为保留消息，所以服务端也可能在 CONNACK 报文中使用这个 Reason Code。 |
| 0x9B (155)      | QoS not supported                      | CONNACK, DISCONNECT                                      | 用于表示不支持当前的 QoS 等级。如果客户端在消息（包括遗嘱消息）中指定的 QoS 大于服务端支持的最大 QoS，服务端将会发送 Reason Code 为 0x9B 的 DISCONNECT 或者 CONNACK 报文然后关闭网络连接。在大部份情况下，这个 Reason Code 都是由服务端使用。但是在客户端收到不是来自订阅的消息，并且消息的 QoS 大于它支持的最大 QoS 时，它也会发送 Reason Code 为 0x9B 的 DISCONNECT 报文然后关闭网络连接。这种情况通常意味着服务端的实现可能存在问题。 |
| 0x9C (156)      | Use another server                     | CONNACK, DISCONNECT                                      | 服务端在 CONNACK 或者 DISCONNECT 报文中通过这个 Reason Code 告知客户端应该临时切换到另一个服务端。如果另一个服务端不是客户端已知的，那么这个 Reason Code 还需要配合 Server Reference 属性一起使用，以告知客户端新的服务端的地址。 |
| 0x9D (157)      | Server moved                           | CONNACK, DISCONNECT                                      | 服务端在 CONNACK 或者 DISCONNECT 报文中通过这个 Reason Code 告知客户端应该永久切换到另一个服务端。如果另一个服务端不是客户端已知的，那么这个 Reason Code 还需要配合 Server Reference 属性一起使用，以告知客户端新的服务端的地址。 |
| 0x9E (158)      | Shared Subscriptions not supported     | SUBACK, DISCONNECT                                       | 当服务端不支持共享订阅，但是客户端尝试建立共享订阅时，服务端可以发送 Reason Code 为 0x9E 的 SUBACK 报文拒绝这次订阅请求，也可以直接发送 Reason Code 为 0x9E 的 DISCONNECT 报文然后关闭网络连接。 |
| 0x9F (159)      | Connection rate exceeded               | CONNACK, DISCONNECT                                      | 用于表示客户端已超过连接速率限制。服务端可以对客户端的连接速率做出限制，客户端连接过快时，服务端可以发送 Reason Code 为 0x9F 的 CONNACK 报文来拒绝新的连接。当然这并不是绝对的情况，考虑到不是所有的客户端都会等待一段时间再重新发起连接，一些服务端实现可能会选择暂时挂起连接而不是返回 CONNACK。 |
| 0xA0 (160)      | Maximum connect time                   | DISCONNECT                                               | 仅用于 DISCONNECT 报文，并且只有服务端可以使用。出于安全性的考虑，服务端可以限制单次授权中客户端的最大连接时间，比如在使用 JWT 认证时，客户端连接不应在 JWT 过期后继续保持。这种情况下，服务端可以发送 Reason Code 为 0xA0 的 DISCONNECT 报文，向客户端指示连接因为超过授权的最大连接时间而被关闭。客户端可以在收到包含这个 Reason Code 的 DISCONNECT 报文后，重新获取认证凭据然后再次请求连接。 |
| 0xA1 (161)      | Subscription Identifiers not supported | SUBACK, DISCONNECT                                       | 当服务端不支持订阅标识符，但是客户端的订阅请求中包含了订阅标识符时，服务端可以发送 Reason Code 为 0xA1 的 SUBACK 报文拒绝这次订阅请求，也可以直接发送 Reason Code 为 0xA1 的 DISCONNECT 报文然后关闭网络连接。 |
| 0xA2 (162)      | Wildcard Subscriptions not supported   | SUBACK, DISCONNECT                                       | 当服务端不支持通配符订阅，但是客户端的订阅请求中包含了主题通配符时，服务端可以发送 Reason Code 为 0xA2 的 SUBACK 报文拒绝这次订阅请求，也可以直接发送 Reason Code 为 0xA2 的 DISCONNECT 报文然后关闭网络连接。 |


## 加入 EMQ 社区

EMQ 致力于用软件改造数字世界。十多年来，EMQ 一直致力于开源项目的研发（包括 [EMQX](https://github.com/emqx/emqx)、[MQTTX](https://github.com/emqx/mqttx)、[Neuron](https://github.com/emqx/neuron)、[NanoMQ](https://github.com/nanomq/nanomq) 等项目）。我们真诚地邀请您加入 EMQ 开发者社区。让我们用开源软件创造一个美好的数字未来。您可以在 [GitHub](https://github.com/emqx)、[论坛](https://askemq.com/)上找到我们。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
