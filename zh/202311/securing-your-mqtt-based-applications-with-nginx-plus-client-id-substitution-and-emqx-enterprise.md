## 引言

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种流行的轻量级发布-订阅模式的消息传输协议，非常适用于连接物联网或是互联网环境下的机器对机器（M2M）设备和应用下。[NGINX Plus](https://www.nginx.com/products/nginx/) 和 [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 是两款强大的工具，它们能够为您的 MQTT 应用提供性能优化和安全保障。

本文将探讨如何将 NGINX Plus 的 Client ID 替换功能与 EMQX Enterprise 结合使用。

## NGINX Plus 和 EMQX Enterprise 简介

NGINX Plus 是基于开源 NGINX 项目的软件负载均衡器、反向代理、Web 服务器和内容缓存。它支持负载均衡、会话持久性、SSL/TLS Termination 以及客户端证书验证等功能。NGINX Plus R29 版本的一个新特性是能够解析和修改 MQTT CONNECT 消息的部分内容，以实现 Client ID 替换功能。

EMQX Enterprise 是一款可靠且可扩展的 MQTT 消息平台，适用于物联网关键业务场景中的数据连接、移动和处理。它是个一体化的分布式 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，具备多个协议网关和内置的基于 SQL 的强大物联网规则引擎。

## Client ID 替换简介

Client ID 替换是一种允许 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)使用替代的客户端 ID 连接到 MQTT Broker 的技术。这个由 NGINX Plus 创建的 Client ID 将代替客户端原本提供的 Client ID，用于在后续通信中识别客户端。

安全性在 MQTT 通信中至关重要。设备通常会在 MQTT CONNECT 消息中发送序列号等敏感信息。在 MQTT Broker 的数据库中存储用来识别客户端的信息可能会带来安全风险。Client ID 替换这项功能可以允许我们使用 NGINX Plus 配置中设置的其他值来替代设备标识符。

## 为 Client ID 替换配置 NGINX Plus 和 EMQX

要为 Client ID 替换配置 NGINX Plus，需要修改 NGINX 配置文件。下面是一个配置示例：

```
stream {
    mqtt on;

    server {
        listen 2883 ssl;
        ssl_certificate /etc/nginx/certs/emqx.pem;
        ssl_certificate_key /etc/nginx/certs/emqx.key;
        ssl_client_certificate /etc/nginx/certs/ca.crt;      
        ssl_session_cache shared:SSL:10m;
        ssl_verify_client on;
        proxy_pass 10.0.0.113:1883;
        proxy_connect_timeout 1s;  

        mqtt_set_connect clientid $ssl_client_serial;
    }
}
```

在这个示例中，我们从设备的客户端 SSL 证书中提取一个唯一标识符，并用它来代替 MQTT Client ID。客户端证书的验证（双向 TLS）由“ssl_verify_client”配置项控制，当该配置项设置为“on”时，NGINX 会确保客户端证书是由受信任的证书颁发机构（CA）签署的。受信任的 CA 证书列表由“ssl_client_certificate”配置项定义。

配置完成后，需要 `reload` 或 `restart` NGINX Plus 服务。

要为 NGINX 在 EMQX 中开启协议代理，需要在配置文件中启用“proxy_protocol”：

```
listeners.tcp.default {
  bind = "0.0.0.0:1883"
  proxy_protocol = true
}
```

或者也可以在 EMQX Dashboard 中启用它：

![EMQX Dashboard](https://assets.emqx.com/images/2586cec680dc612980a44c2552ca5b88.png?)

在本示例中，我们将 EMQX Enterprise 配置为在端口 `1883` 上接受连接。我们还启用了代理协议。

## 测试配置

为了测试配置，需要将 MQTT 客户端连接到 NGINX Plus 代理，然后发送 MQTT CONNECT 消息。最后，可以在 EMQX Enterprise Dashboard 上检查客户端连接，查看 Client ID 替换功能是否按照预期运行。

在本文中，我们使用 [MQTTX](https://mqttx.app/zh) 来验证 Client ID 替换功能。

![MQTTX](https://assets.emqx.com/images/ee021fe6efcc4b3a7ae40ef16866b703.png?)

在本示例中，我们使用 `client123` 作为连接的客户端 ID。

![EMQX Dashboard](https://assets.emqx.com/images/0ac36427aec829668029f75ad0cafefa.png?)

打开 EMQX Enterprise 后，可以进入“客户端”页面，验证 Client ID 替换功能是否正常工作。

## 结语

在本文中，我们探讨了 MQTT 通信安全的重要性，以及 NGINX Plus 的 Client ID 替换功能如何帮助确保 MQTT 应用的安全性。我们还提供了一份配置指南，详细说明了如何设置 NGINX Plus 和 EMQX Enterprise 来实现 Client ID 替换功能，以及如何使用 MQTTX 工具来进行验证。

<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
