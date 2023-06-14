在本系列[之前的文章](https://www.emqx.com/zh/blog/securing-mqtt-with-username-and-password-authentication)中我们提到，借助 MQTT CONNECT 报文中的 Username 和 Password 字段，我们可以实现一些简单的认证，比如密码认证、Token 认证等。为了进一步保障物联网系统的安全，在本期文章中，我们将一起了解另一种认证机制：增强认证。

## 什么是增强认证？

增强认证是 MQTT 5.0 新引入的认证机制。事实上，我们用认证框架来形容它更为适合，因为它允许我们套用各种比密码认证更加安全的身份验证方法。

不过更安全，另一方面则意味着更复杂，这类身份验证方法例如 SCRAM 通常都要求一次以上的认证数据往返。这导致由 CONNECT 与 CONNACK 报文提供的一次往返的认证框架变得不再适用，所以 MQTT 5.0 专门为此新增了 AUTH 报文，它能够支持任意次数的认证数据的往返。这使得我们可以将质询-响应风格的 SASL 机制引入到 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 中。

## 增强认证解决了什么问题？

在我们谈论这个问题之前，我们需要知道，为什么密码认证仍然不够安全？

事实上，即使我们已经使用加盐与哈希的方式来存储密码，尽可能提升了密码存储的安全性。但是为了完成认证，客户端不得不在网络中明文传输密码，这就使密码有了被泄漏的风险。即使我们使用 TLS 加密了通信，也仍有可能因为使用了较低的 SSL 版本、不够安全的密码套件、不合法的 CA 证书等等原因导致被攻击者窃取到密码这类敏感数据。

另外，简单的密码认证只能让服务端验证客户端的身份，却不能让客户端验证服务端的身份，这使得攻击者有机会冒充服务端来获取客户端发送的敏感数据。而这就是我们通常所说的中间人攻击。

而通过增强认证，我们可以选择使用 SASL 框架下的安全性更强的认证方法，它们有些可以避免在网络中传输密码，有些可以让客户端和服务端互相验证对方的身份，有些则两者皆备，这仍取决于我们最终选择的认证方法。

## 常见的可用于增强认证的 SASL 机制

### DIGEST-MD5

DIGEST-MD5 是在简单认证安全层（SASL）框架下的一种身份验证机制。它基于 MD5（Message Digest 5）散列算法，使用质询-响应机制来验证客户端和服务器之间的身份。它的优点在于客户端不需要在网络上传输明文密码。

简单来说，就是当客户端请求访问受保护资源时，服务端将返回一个 Challenge，其中包含了一次性的随机数和一些必要参数，客户端需要使用这些参数加上自己持有的用户名密码等数据，生成一个响应并返回给服务端，服务端将使用完全相同的方式生成期望的响应，然后与收到的响应进行比较，如果两者匹配，则身份验证通过。这免去了密码因为遭到网络窃听而泄漏的风险，并且由于连接时使用的是一次性的随机数，所以也增强了对重放攻击的防御能力。

但需要注意，DIGEST-MD5 只提供了服务端对客户端的身份验证，但没有提供客户端对服务端的身份验证，所以它并不能防止中间人攻击。另外，由于 MD5 目前已经不再安全，所以更推荐使用 SHA-256 这类抗碰撞能力更强的哈希函数来替代它。

### SCRAM

SCRAM 同样是 SASL 框架下的一种身份验证机制，它的核心思想与 DIGEST-MD5 类似，同样是使用一次性的随机数要求客户端生成响应，所以客户端同样无需在网络上传输明文密码。但与 DIGEST-MD5 不同的是，SCRAM 引入了盐值（Salt）和迭代次数（Iterations），并且使用了 SHA-256、SHA-512 这些更安全的哈希算法，这带来了更高的安全性，使 SCRAM 能够更加安全地存储密码，并且减少被离线攻击、重放攻击或其他攻击破解的风险。

另外，SCRAM 使用了更复杂的质询-响应流程，它增加了一个服务端向客户端发送证明的过程，客户端可以通过这个证明来确认服务端是否持有正确的密码，这就实现了客户端对服务端的身份验证，降低了中间人攻击的风险。

当然，SCRAM 使用的 SHA256 等哈希算法，也在性能上带来了一些额外的开销，这可能会对一些资源受限的设备造成一定的影响。

### Kerberos

Kerberos 引入了一个可信的第三方 Kerberos 服务器来提供身份验证服务，Kerberos 服务器向通过验证的用户授予票据，用户再使用票据访问资源服务器。这带来的一个好处是用户只要通过一次身份验证，就可以获得多个系统和服务的访问权限，即实现了单点登录（SSO）的功能。

Kerberos 服务器授予的票据的生命周期是有限的，客户端只能在有限时间的内使用这个票据访问服务，这可以避免因票据泄漏而导致的安全问题。当然，虽然较短的有效期可以有效地提高安全性，但在使用的便利性上可能不太友好，我们需要自行权衡这两者。

Kerberos 的核心是对称加密算法，服务端使用本地存储的密码哈希加密认证数据，然后返回给客户端。客户端对自己持有的密码进行哈希然后解密这些认证数据，这样的好处是无需在网络上明文传输密码，又能够让服务端和客户端相互验证对方都持有正确的密码。以这种通过对称加密交换数据的方式，服务端和客户端还能够安全地完成会话密钥的共享，这个密钥可以被用于后续通信数据的加密，以提供对通信数据的安全保护。

Kerberos 在提供较强安全性的同时，也带来了相当的复杂性，它的实现和配置都存在一定的门槛，另外多达六次的握手对于网络延迟和可靠性也提出了比较高的要求，所以通常 Kerberos 主要在企业的内网环境中使用。

## 增强认证在 MQTT 中是如何运行的？

以 SCRAM 机制为例，我们来看一下在 MQTT 中增强认证是如何进行的。至于 SCRAM 的具体原理本文不作展开，在这里，我们只需要知道，SCRAM 需要传递四次消息才能完成认证：

- client-first-message
- server-first-message
- client-final-message
- server-final-message

![MQTT 增强认证](https://assets.emqx.com/images/0e5a173ff8a357054f5f57aacec41bc6.png)

首先，客户端仍然需要发送 CONNECT 报文来发起认证，只是需要将 Authentication Method 属性设置为 SCRAM-SHA-256 表示想要使用 SCRAM 认证，其中 SHA-256 表示准备使用的哈希函数，同时使用 Authentication Data 属性存放 client-first-message 的内容。Authentication Method 决定了服务端应该如何解析和处理 Authentication Data 中的数据。

如果服务端不支持 SCRAM 认证，或者发现 client-first-message 的内容不合法，那么它将返回包含指示认证失败原因的 Reason Code 的 CONNACK 报文，然后关闭网络连接。

反之服务端就会继续进行下一步：返回一个 AUTH 报文，并且将 Reason Code 设置为 0x18，表示继续认证。报文中的 Authentication Method 将与 CONNECT 报文相同，而 Authentication Data 属性将包含 server-first-message 的内容。

客户端在确认 server-first-message 的内容无误后，同样返回一个 Reason Code 为 0x18 的 AUTH 报文，Authentication Data 属性将包含 client-final-message 的内容。

在服务端确认 client-final-message 的内容无误后，服务端就已经完成了对客户端身份的验证。所以这次服务端将不再是返回 AUTH 报文，而是返回一个 Reason Code 为 0 的 CONNACK 报文以表示认证成功，并通过报文中的 Authentication Data 属性传递最终的 server-final-message。客户端需要根据这个消息的内容来验证服务端的身份。

如果服务端的身份通过了验证，那么客户端就可以开始订阅主题或者发布消息了，而如果没有通过验证，客户端将会发送 DISCONNECT 报文来终止这一次的连接。

## 结语

增强认证为用户提供了引入更多身份验证方法的可能性。您可以选择适合您特定需求的认证方法，进一步增强系统的安全性。

作为广泛使用的 [MQTT Broker](https://site-ip.mqttce.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)，[EMQX](https://www.emqx.io/zh) 在以其高可扩展性和可用性著称的同时，也始终将确保用户安全放在首位。除了基于密码的认证，EMQX 也支持增强认证。用户可以通过 EMQX 启用 SCRAM 认证，以提高其 MQTT 基础设施的安全级别。

更多信息请查看：[MQTT 5.0 增强认证](https://www.emqx.io/docs/zh/v5.0/access-control/authn/scram.html)



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
