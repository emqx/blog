除了[前几篇文章](https://www.emqx.com/zh/blog/leveraging-enhanced-authentication-for-mqtt-security)中提到的认证方法，本文将对其他认证方法进行深入分析和探讨。

具体而言，我们将深入了解基于 Token 的认证和 OAuth 2.0，阐述它们的原理并展示它们在 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 中的应用。

## 基于 Token 的认证

让我们先来认识一下基于 Token 的认证，了解它相较于传统的[用户名和密码认证](https://www.emqx.com/zh/blog/securing-mqtt-with-username-and-password-authentication)的一些优势。

### 什么是基于 Token 的认证？

简单来说，基于 Token 的认证使用 Token 来验证客户端身份，而不是使用传统的凭据（如用户名和密码）。这个过程类似于使用电子门卡进入酒店房间。当您向前台出示身份证时，他们会提供一张电子门卡，让您能够打开酒店房门。这张电子门卡在您入住期间起到了 Token 的作用，您无需每次进入房间时都向前台证明身份，只需刷卡即可。

Token 的一个重要特性是其具备有效期限制，可以在到期后失效。例如，您的酒店门卡在退房后将失效。然而，您可能会入住另一家酒店并拿到新房间的门卡。因此，相较于用户名和密码，Token 更加灵活且易于管理。酒店房门上的电子门卡阅读器无需记录有效的用户名和密码，只需验证门卡上的房间号码和有效期即可。

下面我们将深入研究一些适用于 MQTT 的基于 Token 的认证方法。

### 基于 Token 的 MQTT 认证方法

在 MQTT 中，我们通常使用 JWT 来实现令牌认证。

JWT（JSON Web Token）是一种在 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 中验证客户端身份的简洁方式。客户端向 Broker 发送一个签名的 JWT Token，Broker 根据该 Token 验证客户端身份。Broker 不需要保存客户端的用户名和密码。

JWT Token 由以下部分组成：

- **头部：**用 Base64 编码 - 说明生成签名所采用的算法。
- **有效载荷：**用 Base64 编码 - 携带可以验证客户端身份的声明。
- **签名：**将头部和有效载荷连接后用 Base64 编码，再用密钥对其签名。

下图显示了 JWT 的结构：

![ JWT 的结构](https://assets.emqx.com/images/9d05f5ef051239d8ed1121d696393d85.jpeg?imageMogr2/thumbnail/1520x)

请注意，头部和有效载荷并没有加密，它们只是用 base64 二进制到文本编码函数进行了编码。这是一个可逆的函数，所以只要用 base64 解码函数就能轻松地看到内容。因此，不要在头部和有效载荷部分放置敏感信息。另外，最好使用 TLS 对客户端连接进行加密。JWT 使用 **密钥** 进行签名。

Broker 需要验证 JWT 是否有效。这可以通过两种方式实现：一种是在本地持有密钥，可以是一个和客户端共享的密钥，也可以是一个与签发 JWT 使用的私钥相对的公钥；另一种是使用 JWKS (JSON Web Key Set)，JWKS 是一组公钥，可以用来检验密钥是否有效。Broker 可以通过 JWKS 端点来获取公钥，而无需自己持有它。

JWT Token 在颁发后，就无法撤销，只能等到它过期。因此，一定要把它保存在安全的地方，如果落入他人之手，攻击者就可以利用它来访问 Broker。

可以通过使用认证服务器来获取 JWT Token。在这种情况下，客户端先连接到认证服务器，认证服务器核实其身份后，向客户端发放 JWT Token。客户端凭借这个令牌来连接 Broker。

下图展示了这个过程：

![Token-Based Authentication Method for MQTT](https://assets.emqx.com/images/221320c394fc5847be187cc31ab5b3e4.jpeg?imageMogr2/thumbnail/1520x)

下面是一个 JWT 有效载荷的例子。

```
{
 "clientid": "client1",
 "username": "user1",
 "iat": 1516239022,
 "nbf": 1678114325,
 "exp": 1709649185
}
```

除了 **clientid** 和 **username** 字段外，JWT 令牌还可以包含一些时间字段，用于表示令牌的有效期。这些时间字段以 Unix 时间的形式表示，即从 1970 年 1 月 1 日开始计算的秒数。

- **“iat”**：颁发时间 - Token 颁发的日期和时间。用 Unix 时间表示。
- **“nbf”**：生效时间 - Token 开始生效的日期和时间。用 Unix 时间表示。
- **“exp”**：过期时间 - Token 失效的日期和时间。用 Unix 时间表示。

请注意，通过使用 **nbf** 字段，您可以颁发一个在未来某个日期才生效的 JWT。

## OAuth 2.0

在上一节中，我们介绍了 JWT Token 的格式，但是并没有说明如何获取 Token。接下来，让我们看看如何将 OAuth 2.0 和 JWT 结合使用，以使客户能够访问 Broker。

### 什么是 OAuth 2.0？

OAuth 2.0 是一个框架，它让用户可以用他们在一个独立的认证和授权服务器（如 Google、Facebook、GitHub 等）注册的凭证来访问其他网站或应用的资源。这样，用户就不需要为每个网站或应用设置不同的密码，实现了单点登录（SSO）的效果。用户可以在不同的应用程序中使用相同的 Google 凭证。

最初，OAuth 2.0 被设计为一种授权框架，用于授予第三方应用程序对特定资源的有限访问权限。一个常见的例子是对 Gmail 联系人的只读权限。我们可以允许应用程序读取我们的联系人，但不希望它能够删除它们。OAuth 2.0 解决的一个问题是，它允许我们让第三方应用程序访问我们的联系人，而无需将我们的 Gmail 密码提供给该应用程序，从而提升了安全性。

为了方便使用 OAuth 2.0 协议进行认证，一个名为 OpenID Connect 的 OAuth 2.0 扩展应运而生。该扩展定义了使用 OAuth 2.0 进行认证的标准方法。考虑到认证是本文的主题，我们将 OAuth 2.0 和 OpenID Connect 结合起来使用，共同实现 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)访问 Broker 的授权机制。

### OAuth 2.0 如何与 MQTT 配合？

客户端可以利用 OAuth 2.0 和 OpenID Connect 来获取合适的 JWT，然后再将 JWT 发送给 Broker。参考上面的图片，第一步是 MQTT 客户端向认证服务器申请 JWT Token。我们这里假设认证服务器支持带有 OpenID Connect 扩展的 OAuth 2.0。OpenID Connect 规定了认证服务器返回的令牌必须是 JWT 格式。客户端拿到 JWT 后，就可以把它发送给 Broker。通常，JWT 放在 CONNECT 报文的密码字段里发送给 Broker。

## 结语

作为全球领先的 MQTT Broker，[EMQX](https://www.emqx.io/zh) 提供了多种认证方式，其中包括 [JWT 认证](https://docs.emqx.com/zh/emqx/v5.0/access-control/authn/jwt.html)。您可以选择 HMAC 作为签名方案，也可以选择更安全的 RSA，或者直接为 EMQX 配置一个 JWKS 端点来启用 JWT 认证。

通过使用这些额外的认证方式，您可以增强整个系统对未授权访问和潜在安全威胁的防护。随着技术的不断进步，与最新的认证技术保持同步将变得更加重要。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
