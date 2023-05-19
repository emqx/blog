## v4.3 已发布！

这个五月，我们很高兴地宣布了 **[EMQX broker v4.3 的发布](https://www.emqx.com/zh/blog/emqx-4-3-0-release-notes)**。从社区收到的大量反馈证明了我们的努力是值得的。更多详情请前往 GitHub 查看发布说明：[https://github.com/emqx/emqx/discussions/4763](https://github.com/emqx/emqx/discussions/4763)。

一些原本计划在 v5.0 中进行的更新被提前到了 v4.3 中，与此同时，还有更多工作等待着我们去完成。

### 集群稳定性的提高：大规模的重新订阅

我们进行了大规模（200万个连接）的连接/重连测试，验证并解决了以前遇到的订阅通配符时的不稳定情况。

我们将在后续文章中分享更多详细情况，敬请关注。

### 集群稳定性增强：粘性会话负载平衡

感谢 Haproxy 团队，在社区版中，我们已有了第一个支持 [MQTT](https://www.emqx.com/zh/mqtt-guide) 协议的负载均衡器。在以 [MQTT 客户端](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library) ID 为键的 stick table 的帮助下，我们认为集群节点之间的 MQTT 会话接管/迁移的数量将大大减少。

它的启用也非常简单，举例如下：

```
backend emqx_tcp_back
mode tcp
# Create a stick table for session persistence
stick-table type string len 32 size 100k expire 30m
# Use ClientID / client_identifier as persistence key  stick on req.payload(0,0),mqtt_field_value(connect,client_identifier)
server emqx-1 node1.emqx.io:1883 check-send-proxy send-proxy-v2
server emqx-2 node2.emqx.io:1883 check-send-proxy send-proxy-v2
```



## 全速推进 v5.0 走向云原生

正如我们之前的 Newsletter 中所提到的，一些团队成员从今年年初就开始了 v5.0 的相关工作。云原生将是这一版本的关键主题。以下是我们正在准备的一些令人兴奋的新功能亮点。

### 基础设施作为代码

我们在 v5.0 中采用 HOCON 有两个原因。

- 它几乎是 EMQX 一直以来使用的 cuttlefish 格式的一个直接替代；

- 它是 “纯 JSON"，这是当在 HTTP API 中发布请求时唯一合理可用的格式。

HOCON 允许我们最终统一两个管理界面：配置文件和 HTTP-API。（未来的 CLI 将被包裹在 HTTP-API 中）。

有了新的配置和 API，我们将在 v5.0 中支持从基础设施作为代码部署的资源创建（如 ansible 模板、Kubernetes 配置地图等），以及支持 Dashboard UI 甚至脚本的 HTTP API。

### 无状态节点

自 2021 年 2 月，Rlog 项目启动以来，我们一直都在取得稳定的进展。

Rlog（复制事务日志的简称）将集群分成节点集的两个角色，核心节点和复制节点。核心节点将和我们现在形成集群的方式一样形成一个（网状）集群，复制节点将异步接收数据库的更新。

在之前的 EMQ Demo Day 中我们对其进行了演示与介绍，点击文末「阅读原文」可查看视频回放。

复制节点的无状态性质将使得在云中的部署变得简单。

### 认证授权

我们正在为 5.0 开发认证与授权功能，目前已实现基础框架并支持了部分资源。

全新设计后的认证与授权功能在使用上将更加灵活和简单，认证/授权链的概念得到延续，并再次强化，我们将允许您动态创建认证和授权服务，并且提供了强大的运行时管理能力。

在之前的 EMQ Demo Day 中我们对其进行了演示与介绍，点击文末「阅读原文」可查看视频回放。

### Connetor

我们将规则引擎、认证、授权等功能都需要用到的通用资源抽象为 Connector，并上升为全局概念。我们实现了 Connector 框架以提供 MySQL、HTTP Server 等外部资源的连接配置、健康检查等通用能力，以求在代码量和使用方式上都做到简洁。

### StatsD, etcd 3.4 与 HTTP API

团队成员在本月陆续完成了对 StatsD 和 etcd 3.4 的支持，分别扩展了 EMQX 的监控能力和集群能力。现在，我们正在设计更加规范更加 Restful 的 HTTP API，以提高对开发者的友好性。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
