身份认证又称「验证」、「鉴权」，是指通过一定的手段，完成对用户身份的确认。身份认证是大多数应用的重要组成部分，启用身份认证能有效阻止非法客户端的连接。[EMQX Cloud](https://www.emqx.com/zh/cloud) 中的认证指的是当一个客户端连接到 EMQX Cloud 的时候，通过服务器端的配置来控制客户端连接服务器的权限。

随着用户量的增加，关于认证的用户需求变得越来越复杂。很多用户开始采用自建的认证中心，将认证这一环节保留在用户一侧，以保障数据的安全性，降低数据泄漏风险。这就需要 EMQX Cloud 可以提供连接用户自建认证中心的能力。同时，尽管 EMQX Cloud 支持批量导入添加认证信息，但在实际操作中，如果认证设备的数量增长迅速，出现问题修改或排查往往需要花费很长的时间。

针对以上需求，**EMQX Cloud 最近推出了 HTTP 自定义认证功能**。用户可以连接到自己的认证中心，通过返回的信息来判断终端的登录权限，以实现更加复杂的认证鉴权逻辑和 ACL 校验逻辑。目前，自定义认证功能支持权限认证以及访问控制认证。

### HTTP 认证原理

EMQX Cloud 在设备连接事件中使用当前客户端相关信息作为参数，向用户自定义的认证服务发起请求查询权限，通过返回的 HTTP 响应状态码 (HTTP statusCode) 来处理认证请求。

- 认证失败：API 返回 4xx 状态码
- 认证成功：API 返回 200 状态码
- 忽略认证：API 返回 200 状态码且消息体 ignore

### 如何配置 HTTP 自定义认证 

登录 EMQX Cloud，在部署中左侧点击「认证鉴权」-「自定义认证」，在初始界面中点击「配置认证」开始配置 HTTP 自定义认证。

![EMQX Cloud 配置 HTTP 自定义认证](https://assets.emqx.com/images/b4fc20b6537e4b57ef4bf277d68d825f.png)
 

进行身份认证时，EMQX Cloud 将使用当前客户端信息填充并发起用户配置的认证查询请求，查询出该客户端在 HTTP 服务器端的认证数据。

在表单页配置权限认证的必填参数，包括认证请求地址、认证请求参数、HTTP 请求方法和请求内容的类型。其余的参数如果没有特殊要求使用默认值即可。

![EMQX Cloud 配置 HTTP 自定义认证](https://assets.emqx.com/images/5538c96ad275646583cc48358c1348c3.png)
 

> 注：
>
> 如果当前部署为基础版，请求地址请填写公网服务验证地址
>
> 如果当前部署为专业版，请求地址请填写内网 IP 服务验证地址

 

通过 HTTP 自定义认证，用户可以更加灵活地将自建的认证中心与 EMQX Cloud 结合，大幅提高了认证的安全性，并解决了海量设备认证流程复杂的问题。

### 快速上手 EMQX Cloud

我们最近也在 EMQX Cloud 的整体使用流程上进行了很多优化，例如连接指引和帮助文档的优化，多语言 SDK 接入 Demo，帮助用户快速上手使用产品。

![EMQX Cloud 新手引导优化](https://assets.emqx.com/images/80e2b925616f735dee62f23966b2fd02.png)

<center>新手引导优化</center>

![EMQX Cloud 帮助文档结构优化](https://assets.emqx.com/images/7674ead69739d888ac542f9906aa5bf8.png)

<center>帮助文档结构优化</center>


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
