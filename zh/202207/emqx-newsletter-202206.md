继 EMQX 5.0.0-rc.4 发布之后，v5.0 的开发工作已经接近尾声。除了继续优化 Dashboard 的 UI/UX 以提升使用体验，和测试并修复各项 Bug 以提升软件稳定性以外，EMQX 团队也在对用户文档进行全面的改进和更新，不久后即将为用户带来一个更加强大易用的 EMQX 5.0。

云服务方面，EMQX Cloud 本月新增了JWT 认证支持，用户进行认证鉴权时又多了一种选择。此外，在交易体验上也进行了优化。

## EMQX

### QUIC 改进：适配 MsQuic 2.0 & 内部资源管理重构

在 EMQX 5.0 中我们提供了全球首个 MQTT over QUIC 的实现，支持用户将 MQTT 的传输层协议从 TCP 或者 WebSocket 切换至 QUIC。此前我们的 [QUIC](https://github.com/emqx/quic) 项目是基于微软的开源项目 MsQuic 的 1.8 版本实现的。本月，我们适配了 MsQuic 2.0.2 的 API 实现并且重构了内部资源管理。相比于 MsQuic 1.8，2.0 版本带来了 OpenSSL 版本的升级和证书处理等方面的多项改进。这些改动将随 EMQX 5.0 正式版一并上线。

### 支持通过规则引擎将数据持久化到 HStreamDB

[HStreamDB](https://www.emqx.com/zh/products/hstreamdb) 作为 EMQ 推出的首个专为流数据设计的流数据库，拥有低时延且可靠的流数据持久化存储性能，能够轻松支持和管理大规模的数据流。本月，我们实现了 EMQX 与 HStreamDB 的集成，用户现在将可以通过规则引擎将数据持久化到 HStreamDB。目前，我们已经达成了 10w TPS 的写入性能测试，更高吞吐的压测仍在进行，目的是探索 EMQX 集成 HStream 的性能极限。此功能将在近期的版本更新中正式上线。

![持久化 MQTT 消息至 HStreamDB](https://assets.emqx.com/images/9bd389d45b9bed879de61a227c5b98cb.png)
 

### 支持 OCPP over WebSocket

本月我们启动了 OCPP 协议网关的开发，OCPP 是全世界应用最为广泛的开放式充电桩通信协议。我们正在实现的是基于 WebSocket 的 OCPP-J 1.6 协议。尽管 OCPP 的最新版本已经来到了 2.0.1，但 1.6 目前仍是商业部署协议中最受欢迎的版本。OCPP 网关将提供包括充电桩连接、认证授权和透明传输等能力，此功能将在近期的版本更新中上线。
 

### 支持 OCSP Stapling

随着广大用户网络安全意识的加强，我们有越来越多的用户选择使用 TLS 来加密客户端到 EMQX 的连接。而在实际使用过程中，可能会出现证书因为私钥泄漏等原因而被吊销的情况，因此客户端和服务端都需要能够及时知道对端使用的证书是否依然合法。为了解决这一问题，我们实现了对 OCSP Stapling 的支持，相比于 OCSP，OCSP Stapling 具有更好的隐私性和连接性能。我们支持 EMQX 将携带 OCSP 响应的证书返回给客户端（用于单向认证），也支持将客户端将携带 OCSP 响应的证书发送给 EMQX（用于双向认证）。

对于一些可能不支持 OCSP 的客户端，我们将提供对 CRL（证书吊销列表） 的支持，在这过程中，我们还修复了一个 Erlang/OTP CRL 相关代码中的一个 Bug。

以上功能目前都已开发完成，但仍在测试中，它们将会在未来的版本更新中上线。

### 支持 Kafka 的 SASL/GSSAPI（Kerberos） 认证

Kafka 支持 SASL/GSSAPI（Kerberos） 身份验证，相比于普通的用户名密码验证，它不会在网络中传递密码，并且能够提供服务端和客户端的相互认证，具有更强的安全性。

EMQX 团队在近期启动了 Kafka SASL/GSSAPI 认证机制的开发工作。目前，我们已经完成了驱动层的开发与验证，下一步我们将为规则引擎的 Kafka 资源添加对 SASL/GSSAP 的支持。此功能同样将在近期的版本更新中正式上线。

### 4.3 & 4.4 维护版本升级

EMQX 开源版 v4.3.15 & v4.4.4 以及企业版 v4.3.10 & v4.4.4 已经于月初正式发布，带来了 EMQX 在 Windows 下启动失败时无错误提示等多项问题的修复和支持将 JWT 用于授权的多项功能改进。

更多改动情况的介绍我们已经在上月的 Newsletter 中有所提及，可以前往查看：[https://www.emqx.com/zh/blog/emqx-newsletter-202205](https://www.emqx.com/zh/blog/emqx-newsletter-202205)

或者直接查看对应版本的 Release Note 以了解更详细的信息：[EMQX v4.4.4](https://www.emqx.com/zh/changelogs/broker/4.4.4)、[EMQX Enterprise v4.4.4](https://www.emqx.com/zh/changelogs/enterprise/4.4.4)。

4.3 & 4.4 下一维护版本的开发目前也已接近尾声，将于近期发布，敬请期待。

## EMQX Cloud

### 交易记录查询优化

用户现在可以通过交易时间进行搜索过滤，查找在某段时间之间的记录。同时，可以通过「交易方式」对交易记录过滤：国内用户可以查看支付宝、微信、余额或者线下汇款这四种方式过滤对应的交易记录，海外用户支持信用卡、余额、转账三种方式查询。此外，还可以通过查询交易单号找到某条记录。

![MQTT Cloud](https://assets.emqx.com/images/8b1a0bb4a9c59ac5231a80d69f722348.png)

### 外部认证支持 JWT 认证

Json web token (JWT) 是为了在网络应用环境间传递声明而执行的一种基于 JSON 的开放标准（[RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519))。该 token 设计紧凑且安全，特别适用于分布式站点的单点登录（SSO）场景。JWT 的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，以便于从资源服务器获取资源，也可以增加一些额外的其它业务逻辑所必须的声明信息，该 token 也可直接被用于认证或加密。

用户可以在 EMQX Cloud 部署详情的左侧菜单【认证鉴权】-【外部认证鉴权】中找到。使用 JWT 的方式可以通过 Username 或 Password 携带 JWT 作为认证信息，进行对设备的认证。同时也支持配置 JWKs 服务器地址，EMQX Cloud 将从 JWKs 服务器定期查询最新的公钥列表，并用于验证收到的 JWT 是否合法，适用于 RSA 或 ECDSA 算法签发的 JWT。

![MQTT Cloud JWT](https://assets.emqx.com/images/55b7670f2a6344905f60a32fac803e0d.png)

### 试用部署停止后可直接转包年

在 14 天免费试用结束之后，部署将被停止并保留数日。之前，试用部署停止后如果想转为包年部署，用户需要先充值到余额，启动部署之后才可以转包年部署。现在，用户可以直接将停用的试用部署转为包年并立刻使用。在【部署概览】-【专包年】，选择需要的包年时长，创建订单支付之后就可以将部署专为包年，操作更加便捷。

![MQTT Cloud](https://assets.emqx.com/images/1dfe8c66ecaa91e703955615ca911881.png)


## EMQX Kubernetes Operator

下月初即将发布的 EMQX Operator 1.2.1 版本将如下新功能：

### 功能更新

- 端口调整 pod 不会重启，对于服务稳定性进一步提升
- 通过 EMQX Dashboard 中调整 listener，无需更改 K8s 相关配置即可自动更新
- EMQX Plugin CRD 实现，对于插件管理更加简单方便
- 支持通过 EMQX API 查询 EMQX 集群状态，并更新 EMQX Custom Resource 的 Status
- 支持 EMQX 多协议监听器

### 完善优化

- 修复了 EMQX Plugin 未初始化配置 Dashboard 报错的问题

### 即将到来

大规模分布式物联网 MQTT 消息服务器 EMQX 即将发布 5.0 版本，带来无状态节点、自动伸缩等高可用特性，EMQX Operator 也将全面支持全新的 5.0 版本，敬请期待。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
