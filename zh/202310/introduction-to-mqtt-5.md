[MQTT（Message Queuing Telemetry Transport）](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)是一种为资源有限的设备和低带宽、高延迟的网络设计的轻量级消息传输协议。它特别适用于需要较小代码占用空间或网络带宽有限的远程连接。

MQTT 5 是该协议的最新版本，相比之前的版本有了很多改进。新增功能包括：原因代码、会话过期间隔、主题别名、用户属性、订阅选项、请求/响应功能和共享订阅等。本文将探讨这些新功能，介绍主流 Broker 和客户端 SDK 对 MQTT 5.0 协议的支持情况，以及从 MQTT 3.1.1 迁移到 MQTT 5 时的一些关键注意事项。

## MQTT 5 的发展历程

MQTT 是在上世纪 90 年代末由 IBM 的 Andy Stanford-Clark 博士和 Arcom（现 Eurotech）的 Arlen Nipper 开发，用于通过卫星网络监测石油管道。最初的 MQTT 3.1 版本非常轻量级和易于实现，适用于各种物联网设备。

MQTT 3.1.1 于 2014 年发布，是一个 OASIS 标准，其中包括一些微调，增强了其清晰性和互操作性。它能够在资源有限的网络上高效地传输消息，因此在物联网应用中广受欢迎。

然而，随着物联网行业的发展，应用的需求也在不断变化。为了适应这些新的需求，在 2019 年发布了 MQTT 5，其中加入了一些新功能。MQTT 5 也因此能够更好地满足现代物联网应用的复杂需求。

## MQTT 5 的 7 个新功能

### 1. 原因代码：了解断开连接或失败原因

MQTT 5 与之前的版本不同，它能够为每个确认报文提供一个原因代码，帮助我们了解断开连接或发生故障的原因。

这一改进有利于故障排除和更精细的错误处理。比如，如果客户端连接服务器失败，服务器会返回一个原因代码，解释连接不成功的原因。这可能是各种原因导致的，比如登录凭证错误或者服务器不在线。

> 详细教程请参考：[MQTT 5.0 Reason Code 介绍与使用速查表](https://www.emqx.com/zh/blog/mqtt5-new-features-reason-code-and-ack)

### 2. 会话过期间隔：管理会话的生命周期

这个功能允许客户端指定服务器在客户端断开连接后应将会话保持多长时间。在之前的 MQTT 版本中，会话要么在断开连接后立即结束，要么无限期地保持下去。使用 MQTT 5，您可以指定一个具体的时间段，在断开连接后，会话仍然有效。这样可以更灵活地管理会话的生命周期，并节省服务器的资源。

> 详细教程请参考：[Clean Start 与 Session Expiry Interval 介绍与示例 | MQTT 5.0 特性详解](https://www.emqx.com/zh/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)

### 3. 主题别名：减少消息头部的开销

MQTT 5 引入了主题别名，以减少消息头部的开销。在之前的版本中，每个消息都需要包含主题名称，导致数据包过大。

使用主题别名，可以为主题分配一个简短的数字别名。这个别名可以在后续的消息中替代完整的主题名称，大大减少了 MQTT 头部的大小，从而节省了网络带宽。

> 详细教程请参考：[主题别名 - MQTT 5.0 新特性](https://www.emqx.com/zh/blog/mqtt5-topic-alias)

### 4. 用户属性：MQTT 头部中的自定义元数据

这个功能让用户可以在 MQTT 报文的头部添加自定义的元数据。这对于需要在 MQTT 消息中携带额外信息的应用非常有用，比如消息的时间戳、设备位置或其他应用相关的数据。用户属性增加了 MQTT 消息传输的灵活性和控制力。

> 详细教程请参考：[用户属性 - MQTT 5.0 新特性](https://www.emqx.com/zh/blog/mqtt5-user-properties)

### 5. 订阅选项：细粒度的订阅控制

MQTT 5 让客户端可以指定如何接收每个订阅主题的消息。比如，客户端可以指定他们是否接收某个订阅的保留消息，或者是否接收和订阅具有相同 QoS（服务质量）级别的消息。

> 详细教程请参考：[MQTT 订阅选项的使用](https://www.emqx.com/zh/blog/an-introduction-to-subscription-options-in-mqtt)

### 6. 请求/响应：允许客户端回复指定主题

请求/响应功能让客户端可以指定一个主题，供服务器直接回复。

在早期的 MQTT 版本中，如果客户端想要回复一条消息，它必须把回复发布到一个主题，而原始发送者必须订阅那个主题才能收到回复。使用 MQTT 5 的请求/响应功能，客户端和服务器之间的通信变得更高效和简洁。

> 详细教程请参考：[请求响应 - MQTT 5.0 新特性](https://www.emqx.com/zh/blog/mqtt5-request-response)

### 7. 共享订阅：订阅者负载均衡功能

这个功能让多个客户端可以共享一个订阅。当一条消息发布到一个共享主题时，服务器会把消息分发给共享订阅中的某个客户端，从而实现消息的负载均衡。

这个功能在有多个服务实例运行，并且想要平均分配工作量的场景中非常有用。

## 现有 Broker 和客户端 SDK 对 MQTT 5.0 协议的支持情况

MQTT 5.0 协议得到了物联网社区的广泛欢迎，许多 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 和客户端软件开发工具包（SDK）都实现了对其的支持。[EMQX](https://www.emqx.io/)、[Mosquitto](https://www.emqx.com/zh/blog/mosquitto-mqtt-broker-pros-cons-tutorial-and-modern-alternatives) 和 [NanoMQ](https://nanomq.io/) 等主流 MQTT Broker 已经在其平台上集成了 MQTT 5.0 的功能，让用户可以充分利用新协议的优势。

在客户端 SDK 方面，像 Paho 这样有众多用户的库也支持 MQTT 5.0。这意味着开发者现在可以在他们的物联网应用中使用 MQTT 5.0 的新功能。其他支持 MQTT 5.0 的客户端 SDK 还有 [MQTT.js](https://www.emqx.com/zh/blog/mqtt-js-tutorial) 和 [MQTTnet](https://www.emqx.com/en/blog/connecting-to-serverless-mqtt-broker-with-mqttnet-in-csharp)。

## 从 MQTT 3.1.1 迁移到 MQTT 5 的注意事项

如果您目前使用的是 MQTT 3.1.1，那么可能是时候升级到 MQTT 5 了。在迁移之前，需要考虑以下几点。

### 1. 更新 MQTT Broker

在评估了现有的基础设施并决定进行迁移后，下一步就是更新 MQTT Broker。这意味着要安装支持 MQTT 5.0 的最新版本的 MQTT Broker。uced in MQTT 5.0.

升级 Broker 应该谨慎进行，因为它会影响所有的 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)。建议先在非生产环境中测试新的 Broker，然后再在生产环境中部署。另外，确保对 Broker 的配置进行必要的更新，以支持 MQTT 5.0 中引入的新功能。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>

### 2. 更新客户端库

在更新了 MQTT Broker 之后，还需要更新 MQTT 客户端库。和更新 Broker 一样，应该先在测试环境中试用新的客户端库。同时，要确保应用代码能够适应 MQTT 5.0 的新功能。注意，这可能需要一些代码重构。

### 3. 处理安全问题

MQTT 5.0 在带来多项改进的同时，也引入了一些新的安全风险。比如，有了新的用户属性功能，客户端可以向 Broker 发送自定义数据。这是一个强大的功能，但如果使用不当可能会造成问题。因此，要从安全的角度检查所有的新功能。

可以采取以下措施来提高安全性：使用新的增强验证功能来加强安全性，限制客户端只能发送必要的用户属性，以及持续监测任何可疑的活动。

> 要了解更多信息，请参考我们详细的[ MQTT 安全指南](https://www.emqx.com/zh/blog/essential-things-to-know-about-mqtt-security)。

### 4. 迁移后的监测

在迁移到 MQTT 5.0 并使用了它的功能后，仍然需要持续监测您的系统。监测不只是关注技术方面，如消息传输或客户端连接。也要监测应用中新 MQTT 5.0 功能的使用效果。这样才能知道这些功能如何优化了您的应用，以及还有哪些提升空间。

## 和 EMQX 一起拥抱 MQTT 5

EMQX 是世界上最具扩展性的[开源 MQTT Broker](https://www.emqx.com/zh/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)，它完全兼容 MQTT 5.0 的所有功能。任何 MQTT 协议版本的设备都可以直接连接到 EMQX 并进行通信。

EMQX 具有完善的认证和授权机制，以及对 SSL/TLS 的全面支持，能够保障通信的安全。基于 SQL 的规则引擎具有数据桥接功能，无需编写代码即可实现一站式物联网数据提取、过滤、转换、存储和处理。

EMQX 还具有高性能，单个 EMQX 5.0 集群可以支持高达 1 亿个 MQTT 并发连接。单个 EMQX 服务器可以达到每秒数百万条消息的吞吐量。

我们围绕 MQTT Broker 构建了丰富的功能，帮助您方便地使用该协议，例如跨平台的 [MQTT 客户端工具 - MQTTX](https://mqttx.app/)、面向物联网边缘的[超轻量级 MQTT Broker - NanoMQ](https://nanomq.io/)、以及完全托管的 [MQTT 云服务 - EMQX Cloud](https://www.emqx.com/zh/cloud)。所有这些工具都完全支持 MQTT 5.0。





<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
