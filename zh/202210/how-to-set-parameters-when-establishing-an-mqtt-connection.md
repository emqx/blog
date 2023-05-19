建立一个 MQTT 连接是使用 MQTT 协议进行通信的第一步。为了保证高可扩展性，在建立连接时 MQTT 协议提供了丰富的连接参数，以方便开发者能创建满足不同业务需求的物联网应用。本文将详细讲解 MQTT 中各个连接参数的作用，帮助开发者迈出使用 MQTT 的第一步。



## MQTT 连接的基本概念

MQTT 连接由客户端向服务器端发起。任何运行了 MQTT 客户端库的程序或设备都是一个 [MQTT 客户端](http://mqttx.app/zh)，而 [MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)则负责接收客户端发起的连接，并将客户端发送的消息转发到另外一些符合条件的客户端。

客户端与服务器建立网络连接后，需要先发送一个 `CONNECT ` 数据包给服务器。服务器收到 `CONNECT` 包后会回复一个 `CONNACK` 给客户端，客户端收到 `CONNACK` 包后表示 MQTT 连接建立成功。如果客户端在超时时间内未收到服务器的 ` CONNACK` 数据包，就会主动关闭连接。

大多数场景下，MQTT 通过 TCP/IP 协议进行网络传输，但是 MQTT 同时也支持通过 WebSocket 或者 UDP 进行网络传输。

### MQTT over TCP

TCP/IP 应用广泛，是一种面向连接的、可靠的、基于字节流的传输层通信协议。它通过 ACK 确认和重传机制，能够保证发送的所有字节在接收时是完全一样的，并且字节顺序也是正确的。

MQTT 通常基于 TCP 进行网络通信，它继承了 TCP 的很多优点，能稳定运行在低带宽、高延时、及资源受限的环境下。

### MQTT over WebSocket

近年来随着 Web 前端的快速发展，浏览器新特性层出不穷，越来越多的应用可以在浏览器端通过浏览器渲染引擎实现，Web 应用的即时通信方式 WebSocket 也因此得到了广泛的应用。

很多物联网应用需要以 Web 的方式被使用，比如很多设备监控系统需要使用浏览器实时显示设备数据。但是浏览器是基于 HTTP 协议传输数据的，也就无法使用 MQTT over TCP。

MQTT 协议在创建之初便考虑到了 Web 应用的重要性，它支持通过 MQTT over WebSocket 的方式进行 MQTT 通信。关于如何使用 MQTT over WebSocket，读者可查看博客[使用 WebSocket 连接 MQTT 服务器](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket)。



## MQTT 连接参数的使用

### 连接地址

MQTT 的连接地址通常包含 ：服务器 IP 或者域名、服务器端口、连接协议。

**基于 TCP 的 MQTT 连接**

`mqtt` 是普通的 TCP 连接，端口一般为 1883。

`mqtts` 是基于 TLS/SSL 的安全连接，端口一般为 8883。

比如 `mqtt://broker.emqx.io:1883` 是一个基于普通 TCP 的 MQTT 连接地址。

**基于 WebSocket 的连接**

`ws` 是普通的 WebSocket 连接，端口一般为 8083。

`wss` 是基于 WebSocket 的安全连接，端口一般为 8084。

当使用 WebSocket 连接时，连接地址还需要包含 Path，[EMQX](http://www.emqx.io/) 默认配置的 Path 是 `/mqtt`。比如 `ws://broker.emqx.io:8083/mqtt` 是一个基于 WebSocket 的 MQTT 连接地址。

### 客户端 ID（Client ID）

MQTT 服务器使用 Client ID 识别客户端，连接到服务器的每个客户端都必须要有唯一的 Client ID。Client ID 的长度通常为 1 至 23 个字节的 UTF-8 字符串。

**如果客户端使用一个重复的 Client ID 连接至服务器，将会把已使用该 Client ID 连接成功的客户端踢下线。**

### 用户名与密码（Username & Password）

MQTT 协议可以通过用户名和密码来进行相关的认证和授权，但是如果此信息未加密，则用户名和密码将以明文方式传输。如果设置了用户名与密码认证，那么最好要使用 `mqtts` 或 `wss` 协议。

大多数 MQTT 服务器默认为匿名认证，匿名认证时用户名与密码设置为空字符串即可。

### 连接超时（Connect Timeout）

连接超时时长，收到服务器连接确认前的等待时间，等待时间内未收到连接确认则为连接失败。

### 保活周期（Keep Alive）

保活周期，是一个以秒为单位的时间间隔。客户端在无报文发送时，将按 Keep Alive 设定的值定时向服务端发送心跳报文，确保连接不被服务端断开。

在连接建立成功后，如果服务器没有在 Keep Alive 的 1.5 倍时间内收到来自客户端的任何包，则会认为和客户端之间的连接出现了问题，此时服务器便会断开和客户端的连接。

更多细节可查看博客：[MQTT 协议中的 Keep Alive 机制](https://www.emqx.com/zh/blog/mqtt-keep-alive)。

### 清除会话（Clean Session）

为 `false` 时表示创建一个[持久会话](https://www.emqx.com/zh/blog/mqtt-session)，在客户端断开连接时，会话仍然保持并保存离线消息，直到会话超时注销。为 `true` 时表示创建一个新的临时会话，在客户端断开时，会话自动销毁。

持久会话避免了客户端掉线重连后消息的丢失，并且免去了客户端连接后重复的订阅开销。这一功能在带宽小，网络不稳定的物联网场景中非常实用。

服务器为持久会话保存的消息数量取决于服务器的配置，比如 EMQ 提供的[免费的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)设置的离线消息保存时间为 5 分钟，最大消息数为 1000 条，且不保存 QoS 0 消息。

> **注意：** 持久会话恢复的前提是客户端使用固定的 Client ID 再次连接，如果 Client ID 是动态的，那么连接成功后将会创建一个新的持久会话。

### 遗嘱消息（Last Will）

遗嘱消息是 MQTT 为那些可能出现**意外断线**的设备提供的将**遗嘱**优雅地发送给其他客户端的能力。设置了遗嘱消息消息的 MQTT 客户端异常下线时，MQTT 服务器会发布该客户端设置的遗嘱消息。

> **意外断线包括**：因网络故障，连接被服务端关闭；设备意外掉电；设备尝试进行不被允许的操作而被服务端关闭连接等。

遗嘱消息可以看作是一个简化版的 MQTT 消息，它也包含 Topic、Payload、QoS、Retain 等信息。

- 当设备意外断线时，遗嘱消息将被发送至遗嘱 Topic；
- 遗嘱 Payload 是待发送的消息内容；
- 遗嘱 QoS 与普通 MQTT 消息的 QoS 一致，详细请见[MQTT QoS（服务质量）介绍](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)。
- 遗嘱 Retain 为 `true` 时表明遗嘱消息是保留消息。MQTT 服务器会为每个主题存储最新一条保留消息，以方便消息发布后才上线的客户端在订阅主题时仍可以接收到该消息。详细请见[MQTT 保留消息是什么？如何使用？](https://www.emqx.com/zh/blog/mqtt5-features-retain-message)

更多关于遗嘱消息的介绍可查看博客：[MQTT 遗嘱消息（Will Message）的使用](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)。

### 协议版本

使用较多的 MQTT 协议版本有 MQTT v3.1、MQTT v3.1.1 及 MQTT v5.0。目前，MQTT 5.0 已成为绝大多数物联网企业的首选协议，我们建议初次接触 MQTT 的开发者直接使用该版本。

感兴趣的读者可查看 EMQ 提供的 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 系列文章，了解 MQTT 5.0 相关特性的使用。

### MQTT 5.0 新增连接参数

**Clean Start & Session Expiry Interval**

MQTT 5.0 中将 Clean Session 拆分成了 Clean Start 与 Session Expiry Interval。

Clean Start 用于指定连接时是创建一个全新的会话还是尝试复用一个已存在的会话。为 `true` 时表示必须丢弃任何已存在的会话，并创建一个全新的会话；为 `false` 时表示必须使用与 Client ID 关联的会话来恢复与客户端的通信（除非会话不存在）。

Session Expiry Interval 用于指定网络连接断开后会话的过期时间。设置为 0 或未设置，表示断开连接时会话即到期；设置为大于 0 的数值，则表示会话在网络连接关闭后会保持多少秒；设置为 0xFFFFFFFF 表示会话永远不会过期。

更多细节可查看博客：[Clean Start 与 Session Expiry Interval](https://www.emqx.com/zh/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)。

**连接属性（Connect Properties）**

MQTT 5.0 还新引入了连接属性的概念，进一步增强了协议的可扩展性。更多细节可查看博客：[MQTT 5.0 连接属性](https://www.emqx.com/zh/blog/mqtt5-connect-properties)。



## 如何建立一个安全的 MQTT 连接？

虽然 MQTT 协议提供了用户名、密码、Client ID 等认证机制，但是这对于物联网安全来说还远远不够。基于传统的 TCP 通信使用明文传输，信息的安全性很难得到保证，数据也会存在被**窃听**、**篡改**、**伪造**、**冒充**的风险。

SSL/TLS 的出现很好的解决了通信中的风险问题，其以非对称加密技术为主干，混合了不同模式的加密方式，既保证了通信中消息都以密文传输，避免了被窃听的风险，同时也通过签名防止了消息被篡改。

不同 MQTT 服务器启用 SSL/TLS 的步骤都各有不同，EMQX 内置了对 TLS/SSL 的支持，包括支持单/双向认证、X.509 证书、负载均衡 SSL 等多种安全认证。

单向认证是一种仅通过验证服务器证书来建立安全通信的方式，它能保证通信是加密的，但是不能验证客户端的真伪，通常需要与用户名、密码、Client ID 等认证机制结合。读者可参考博客[EMQX MQTT 服务器启用 SSL/TLS 安全连接](https://www.emqx.com/zh/blog/emqx-server-ssl-tls-secure-connection-configuration-guide)来建立一个安全的单向认证 MQTT 连接。

双向认证是指在进行通信认证时要求服务端和客户端都提供证书，双方都需要进行身份认证，以确保通信中涉及的双方都是受信任的。 双方彼此共享其公共证书，然后基于该证书执行验证、确认。一些对安全性要求较高的应用场景，就需要开启双向 SSL/TLS 认证。读者查看博客[EMQX 启用双向 SSL/TLS 安全连接](https://www.emqx.com/zh/blog/enable-two-way-ssl-for-emqx)了解如何建立一个安全的双向认证 MQTT 连接。

感兴趣的读者也可查看以下博客来学习物联网安全相关知识：

- [如何保障物联网平台的安全性与健壮性](https://www.emqx.com/zh/blog/how-to-ensure-the-security-of-the-iot-platform)
- [灵活多样认证授权，零开发投入保障 IoT 安全](https://www.emqx.com/zh/blog/securing-the-iot)
- [车联网通信安全之 SSL/TLS 协议](https://www.emqx.com/zh/blog/ssl-tls-for-internet-of-vehicles-communication-security)

> **注意：** 如果在浏览器端使用 MQTT over WebSocket 进行安全连接的话，目前还暂不支持双向认证通信。



## 结语

至此，相信读者已对 MQTT 连接的建立及各个连接参数的作用有了深刻的理解。接下来，可访问 EMQ 提供的 [MQTT 入门与进阶](https://www.emqx.com/zh/mqtt-guide)系列文章学习 MQTT 主题及通配符、保留消息、遗嘱消息等相关概念，探索 MQTT 的更多高级应用，开启 MQTT 应用及服务开发。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
