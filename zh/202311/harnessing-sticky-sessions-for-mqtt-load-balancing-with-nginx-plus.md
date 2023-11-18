## **引言**

在快速发展的物联网世界中，设备之间高效的通信能力至关重要。[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是这个领域中轻量级消息传输协议的佼佼者。然而，随着部署规模的扩大，管理这些通信会变得越来越复杂。

粘性会话（Sticky Session）在物联网负载平衡中发挥着关键作用，确保客户端的后续连接路由到同一服务器 - 对于需要会话持久性的应用程序来说这是必须的。本文将深入探讨 [NGINX Plus](https://www.nginx.com/products/nginx/) 和 [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 共同提供的一种优化 MQTT 负载均衡的策略，介绍如何利用它们实现粘性会话，以及“Client ID”在其中的重要作用。

## **MQTT 与负载均衡**

MQTT 是一种基于发布-订阅模式的消息传输协议。它适用于低带宽、高延迟或网络不稳定的环境，是物联网设备的理想选择。但是，当 MQTT 生态系统中的设备数量增加时，增长的流量会产生更大的压力，带来效率降低和数据丢失的风险。这就凸显了负载均衡的必要性。负载均衡是一种可以将 MQTT 流量均匀分配到多个 Broker 上的机制，避免单个服务器承受过大的压力。

负载均衡策略是确保 MQTT 连接平稳分配的关键，不同的策略适应不同的部署需求。例如，轮询策略按照循环的顺序将连接分配给集群中的 各个 Broker 节点，实现公平的分配。最少连接策略将连接引导到最空闲的 Broker，这种策略在 Broker 的处理能力有较大差异的情况下很有效。IP 哈希策略则根据客户端的 IP 地址来确定连接的 Broker，保证固定的连接点。本文中，我们将介绍一种利用“Client ID”的全新策略。这种方法确保同一个客户端始终连接到同一个 Broker，简化数据流，降低连接开销。

## **NGINX Plus 与 EMQX Enterprise**

### NGINX Plus 中的 MQTT 功能

NGINX Plus 在 R29 版本中新增了对 MQTT 消息解析的原生支持。这不是一个简单的功能，而是一种革命性的能力。它可以创建粘性会话，从而提高数据流的效率，降低建立新连接的开销。

### EMQX Enterprise：不只是 MQTT Broker

EMQX Enterprise 以其强大的性能和企业级功能在众多 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 中脱颖而出。它具有高度的可扩展性，可以处理亿级并发 [MQTT 连接](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)，是大规模物联网部署的优选方案。

它与 NGINX Plus 的兼容性进一步增强了其功能，为用户带来了流畅的体验。

<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>

## **利用 NGINX Plus 和 EMQX Enterprise 实现粘性会话**

### **准备工作**

- 安装 R29 或更新版本的 NGINX Plus 以及最新版的 EMQX Enterprise。在本教程中，我们使用了由两个 EMQX Enterprise v5.2.0 节点组成的集群。
- 了解 MQTT 的基础知识和相关术语。

### **架构设计**

下图展示了将 EMQX 与 NGINX Plus 组合的架构设计，重点强调了使用“Client ID”来实现粘性会话：

![The architectural blueprint for integrating EMQX with NGINX Plus](https://assets.emqx.com/images/0da1203e7cbeba3a54e6dc63dae4cb29.png)

在这种方案中，客户端向 NGINX Plus 发送连接请求，NGINX Plus 根据客户端的“Client ID”将请求转发给适当的 EMQX 服务器。这样可以保证客户端的后续连接请求都被转发到同一个服务器，从而提高会话的持久性。

### **配置 NGINX Plus**

- 通过 `mqtt_preread` 配置项，开启 MQTT 解析功能。
- 从 CONNECT 消息中提取必要的字段，这是实现粘性会话的关键步骤。
- 创建粘性会话：这种方案的关键要素是客户端标识符，它作为 NGINX 配置中的哈希键，可以保证客户端始终连接到指定的 EMQX Enterprise Broker。

下面是一个详细的配置示例：

```
stream {
    mqtt_preread on;
    upstream emqx_backend {
        zone tcp_servers 64k;
        hash $mqtt_preread_clientid consistent;
        server 10.0.0.172:1883;
        server 10.0.0.174:1883;
    }
    server {
        listen 1880;
        status_zone tcp_server;
        proxy_pass emqx_backend;
        proxy_buffer_size 4k;
        proxy_protocol on;
    }
}
```

在这个示例中，我们定义了一个叫做“emqx_backend”的服务组，它包含两台 EMQX 服务器。我们还设定了粘性会话要基于“mqtt_preread_clientid”变量，这是 MQTT 协议中使用的客户端标识符。最后，我们让 NGINX 在 1880 端口监听并把请求转发给“emqx_backend”组。

这样的配置保证了具有相同 ID 的客户端始终被路由到同一个 Broker，达到了粘性会话的效果。

配置完成后，需要 `reload` 或 `restart` NGINX Plus。

### **配置 EMQX Enterprise**

要为 NGINX 在 EMQX 中启用协议代理，请打开配置文件中的“proxy_protocol”。

```
listeners.tcp.default {
  bind = "0.0.0.0:1883"
  proxy_protocol = true
}
```

或者通过 EMQX Dashboard 开启它。

![EMQX Dashboard](https://assets.emqx.com/images/3ee65cbaeaa98cfbee7f6c3dd9fc8414.png)

## **验证配置**

配置完成后，有必要验证设置是否正确。为了检验粘性会话配置是否有效，需要用到 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)，比如 [MQTTX](https://mqttx.app/) 或 Mosquitto 客户端，来模拟客户端连接到 EMQX 集群。可以在 EMQX Dashboard 查看连接状态，如果粘性会话配置正确，具有相同 Client ID 的客户端应该始终连接到同一个 EMQX Broker 节点上。

在本示例中，我们使用 [MQTTX](https://mqttx.app/) 作为 MQTT 客户端。

![MQTTX](https://assets.emqx.com/images/2ab67a5d16fd8f0a04f7c2a05e6c471e.png)

我们创建了一个Client ID 为“mqttx_client1”的客户端。在 EMQX Dashboard 上，可以进入“客户端”页面，查看连接到 EMQX 集群的客户端：

![View the clients connected to EMQX Cluster](https://assets.emqx.com/images/db452c6384345ef159b1d915bf7e03fd.png)

可以看到 mqttx_client1 已经连接到了 EMQX 集群。点击 ID，可以查看连接详情。

![Connection details](https://assets.emqx.com/images/ceb64cf892f8c0db4de5187ac5e1eacb.png)

在本示例中，“mqttx_client1”连接到了名为“emqx_node1”的节点。断开并重新连接客户端，会发现同一个 ID 的客户端会始终连接到这个 Broker。

## **使用“Client ID”的好处**

- 保证客户端的后续连接都被路由到同一台服务器，即使客户端更换了 IP 地址或端口号。
- 可以通过在后端组中增加更多的 EMQX 服务器来横向扩展应用，而不影响会话的持久性。
- 提供了一种简单而有效的负载均衡 MQTT 连接的方法。

## **结语**

利用 NGINX Plus 以及“Client ID”实现粘性会话，是在物联网应用中实现可扩展性和会话持久性的有效方法。通过这种配置，可以确保同一客户端的后续连接都被路由到同一台服务器，即使客户端更改了 IP 地址或端口号。NGINX Plus 和 EMQX Enterprise 的结合提供了一个强大的解决方案，用于管理大规模物联网部署中的 MQTT 连接。通过粘性会话，企业可以保证 MQTT 通信的高效、可靠和灵活，从而以满足现代物联网的需求。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
