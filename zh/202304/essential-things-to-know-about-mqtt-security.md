物联网（IoT）深刻改变了我们与周围世界互动的方式。从智能家居到车联网，IoT 设备已经深入到我们生活的各个领域。

然而，物联网的广泛应用也带来了安全方面的挑战。不法分子可以利用漏洞未经授权地访问物联网设备、窃取数据，对物联网系统和终端用户的财产甚至人身安全带来威胁。此外，物联网设备的庞大数量和其互联性也为黑客发起大规模攻击提供了可乘之机。

作为物联网通信协议的事实标准，MQTT 协议提供了很多与安全相关的功能特性，以保障物联网系统的安全。为了帮助物联网开发者充分了解这些特性，从多维度构建更加安全可靠的物联网系统与应用，EMQ 特别推出了《MQTT 安全》专题系列文章。

该系列文章将包括：
- **[MQTT 安全解析：构建可靠的物联网系统](https://www.emqx.com/zh/blog/understanding-mqtt-security-a-comprehensive-overview)**
- 认证
  - **[用户名/密码认证](https://www.emqx.com/zh/blog/securing-mqtt-with-username-and-password-authentication)**：用户名/密码认证方法介绍，如何在 MQTT 中使用，以及该方法可能存在的隐患与解决办法。
  - **[SCRAM 增强认证](https://www.emqx.com/zh/blog/leveraging-enhanced-authentication-for-mqtt-security)**：增强认证的作用及用法，如何通过增强认证弥补用户名/密码认证方法的不足。
  - **[其他认证方法](https://www.emqx.com/zh/blog/a-deep-dive-into-token-based-authentication-and-oauth-2-0-in-mqtt)**：Token 认证如 JWT 等。
- **[授权](https://www.emqx.com/zh/blog/authorization-in-mqtt-using-acls-to-control-access-to-mqtt-messaging)**：权限控制与认证的区别，访问控制列表介绍。
- **[流量控制](https://www.emqx.com/zh/blog/improve-the-reliability-and-security-of-mqtt-broker-with-rate-limit)**：常见流量控制策略介绍。
- **[TLS/SSL](https://www.emqx.com/zh/blog/fortifying-mqtt-communication-security-with-ssl-tls)**：单向认证、双向认证、TLS PSK、一机一密讲解，TLS 使用注意事项。
- 基础设施安全：如何从基础设施方面加强物联网系统安全性。
- 报文加密：各类加密方式与密钥管理方法介绍。
- MQTT 模糊测试：如何通过模糊测试发现物联网系统中的安全漏洞。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
