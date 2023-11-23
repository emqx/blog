## **引言**

随着物联网（IoT）的不断发展，越来越多的应用场景采用了 MQTT 这一专为物联网设计的轻量级消息传输协议。由于其简洁、高效和灵活的特性，[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 成为物联网通信的热门选择。然而，这种广泛应用也带来了更多的安全挑战。随着设备数量呈指数级增长，确保通信安全变得至关重要。在这一背景下，NGINX Plus 和 [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 的结合为 MQTT 安全通信提供了强大的解决方案。

在本文中，我们将探讨 MQTT 所面临的安全风险，以及如何通过双向 TLS（传输层安全协议）和客户端证书认证来增强 MQTT 的安全性。

## **MQTT 及其所面临的安全风险**

MQTT 开发于 20 世纪 90 年代末，现已成为最流行的物联网通信协议之一。它是一种基于发布/订阅模式的消息传输协议，设计轻巧高效，非常适合低功耗设备和带宽有限的网络。

虽然 MQTT 具有众多优点，但并非没有安全隐患。未经授权的访问、数据篡改和窃听等问题是 MQTT 网络面临的一些常见安全威胁。这些漏洞可能会造成严重的后果，尤其是对那些高度依赖 MQTT 的组织而言。恶意攻击者可以利用这些漏洞侵入 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 和客户端、篡改传输的数据、或者进行窃听以获取重要信息。

## **双向 TLS 简介**

双向 TLS 可以有效保护 MQTT 通信，它能实现端到端的加密，并保证数据传输的真实性。它要求客户端和服务器都出示有效的证书，从而建立一个双向的认证过程。只有双方都通过认证，才能建立安全的加密连接，有效防止未授权的访问、数据泄露和窃听。

TLS 是确保在线交互安全的基础，它能保障数据在传输中的加密和安全。然而，直接由 MQTT Broker 处理 TLS 握手、加密和解密可能会消耗大量的资源，从而影响性能。这时，NGINX Plus 就能发挥关键作用，通过把这些任务交给 NGINX Plus，MQTT Broker 可以专注于它们的主要职责：管理消息流量。这样不仅能提升性能，还能优化系统的架构，保证数据的安全和流畅。

## **如何配置 TLS Termination** 

在进行配置之前，请确保已安装 NGINX Plus R29 或更新版本，以及最新版的 EMQX Enterprise。安装完成后，首先需要配置 NGINX Plus 以实现 TLS Termination，这需要在 NGINX 配置中指定 SSL 证书和私钥的路径。接着，配置 NGINX Plus，将来自设备的通过 TLS 加密的 MQTT 连接转发到 EMQX Enterprise。如果想要进一步优化性能，可以考虑在 NGINX Plus 中启用 SSL 会话缓存。

下面是一个在 NGINX Plus 中配置 TLS Termination 的示例：

```
stream {

  server {
    listen 8883 ssl;
    ssl_certificate /etc/nginx/certs/emqx.pem;
    ssl_certificate_key /etc/nginx/certs/emqx.key;
    ssl_client_certificate /etc/nginx/certs/ca.crt;
    ssl_session_cache shared:SSL:5m;
    ssl_verify_client on;
    proxy_pass 10.0.0.113:1883;
    proxy_connect_timeout 5s;
  }

}
```

这个示例展示了如何启用双向 TLS。它让 NGINX 充当 MQTT 连接的安全代理。连接到该服务器的客户端必须使用 SSL/TLS（端口 8883），并提供一个由可信 CA 签发的有效客户端证书。NGINX 会终止 SSL/TLS 连接，验证客户端的证书，然后把 MQTT 连接转发到位于 `10.0.0.113:1883` 的实际 MQTT Broker。这样做可以把 SSL/TLS Termination 和客户端证书验证的工作从 EMQX Broker 转移给 NGINX，从而提升性能和安全性。

## **通过客户端证书认证提升安全性**

加密固然至关重要，但它仅是安全问题的一部分。对客户端进行身份认证，确保客户的真实身份，同样非常重要。客户端证书认证是一种强有力的身份验证机制，它确保只有经过授权的设备，即拥有由可信证书颁发机构（CA）颁发的有效证书的设备，才能建立连接。而且，把客户端证书中的数据传输给 MQTT Broker，不仅能加强身份认证，还能实现更高级的授权，让安全性达到一个新的水平。

## **重写 CONNECT 消息实现增强认证**

准备好客户端证书后，就可以在 NGINX Plus 中开启双向 TLS，实现服务器和客户端的相互认证。然后，从客户端的 SSL 证书中提取相关的数据，如通用名称（CN）或其他有用的信息。接下来就是关键的一步：使用 NGINX Plus，用从证书中提取的数据重写 MQTT CONNECT 消息的字段。最后，配置 EMQX Enterprise 以识别和认证这些重写的 CONNECT 消息。这样，只有持有有效证书的合法设备才能连接，从而让 MQTT 环境更加安全。

下面是 NGINX Plus 中的一个客户端证书认证示例：

```
stream {

  mqtt on;
 
  server {
    listen 8883 ssl;
    ssl_certificate /etc/nginx/certs/emqx.pem;
    ssl_certificate_key /etc/nginx/certs/emqx.key;
    ssl_client_certificate /etc/nginx/certs/ca.crt;
    ssl_session_cache shared:SSL:5m;
    ssl_verify_clienet on;

    proxy_pass 10.0.0.113:1883;
    proxy_connect_timeout 5s;

    mqtt_set_connect username $ssl_client_s_dn;
  }

}
```

这个配置在上一个例子的基础上多了两个配置项。

1. “mqtt on”

   这个配置项让 NGINX 在数据流中开启 MQTT 协议解析。这意味着 NGINX 能够理解并处理 MQTT 消息。

2. “mqtt_set_connect username $ssl_client_s_dn”

   这个配置项让 NGINX 重写 MQTT CONNECT 消息的用户名字段。`$ssl_client_s_dn` 是一个变量，它存储的是客户端 SSL 证书中的主题专有名称（DN）。

通过这一优化配置，NGINX 不仅充当了 MQTT 连接的安全代理，还能解析 MQTT 消息。连接到该服务器的客户端必须使用 SSL/TLS（端口 8883），并提供有效的客户端证书。NGINX 会终止 SSL/TLS 连接，验证客户端证书，并使用客户端证书中的 DN 重写 MQTT CONNECT 消息的用户名字段。这样，在 EMQX Broker 层面就能额外增加一个客户端识别和授权机制。然后，NGINX 会把 MQTT 流量转发到位于 `10.0.0.113:1883` 的实际 EMQX Broker。这种配置既增强了安全性，又能利用客户端证书的信息进行 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)的识别和认证。

## NGINX Plus 与 EMQX Enterprise 集成的优势

无论是通过强大的 TLS Termination 和客户端证书认证功能提升安全性，还是通过解放加密任务提高性能，NGINX Plus 和 EMQX Enterprise 的协同效果都显而易见。EMQX Broker 在摆脱加密负担的同时，能够专注于处理 MQTT 消息。这种集成构建了一个可扩展和灵活的框架，能够应对大规模的 MQTT 连接需求。

## **结语**

物联网是一个广阔并且不断发展的领域。随着我们不断将更多设备连接到这个互联网络中，确保通信的安全性变得尤为重要。通过充分发挥 NGINX Plus 和 EMQX Enterprise 的优势，企业可以实现高效、安全和可扩展的 MQTT 通信，为迎接现代物联网的挑战做好充分准备。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
