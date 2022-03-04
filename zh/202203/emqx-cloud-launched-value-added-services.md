[EMQX Cloud](https://www.emqx.com/zh/cloud) 致力于为千行百业不同规模的客户提供可靠、高效的全托管 MQTT 消息云服务，希望可以通过易用、标准化的 SaaS 产品，让用户可以像「搭乐高」般自由构建物联网应用。

面对客户不尽相同的个性化需求，EMQX Cloud 团队决定将在原有产品形态基础上，新设置增值功能板块，为用户提供更多高价值功能。未来用户将可以根据自身实际需求选择开通增值服务，节省不必要的成本支出，同时又能满足定制化需求。

试用地址：[全托管的物联网 MQTT 云平台](https://www.emqx.com/zh/cloud) 

## 两项增值功能新鲜开放

本次更新开放了内网负载均衡和 NAT 网关 2 个增值功能，并提供 14 天免费试用。

### 内网负载均衡

内网负载均衡是一种在内网中对流量进行按需分发的服务，通过将流量分发到不同的后端服务器来扩展应用系统的吞吐能力，并且可以消除系统中的单点故障，提升应用系统的可用性。

### NAT 网关

NAT 网关可以提供网络地址转换服务，为专业版部署提供访问公网资源的能力，无需 VPC 对等连接。

> 注：上述功能均需在专业版使用

## 开通流程

登陆 EMQX Cloud 控制台，通过 **顶部菜单栏 -> 增值服务**

![EMQX Cloud 增值服务](https://static.emqx.net/images/2ddf2595c67de64bd0c7803aa669da54.png)

或 **部署概览览底部开通指定增值服务**

![EMQX Cloud 开通指定增值服务](https://static.emqx.net/images/444796404167fbf655d0c323455598a1.png)

点击 **开通服务**，下拉选择增值服务所要绑定的部署，点击 **下一步**

![EMQX Cloud 开通服务选择部署](https://static.emqx.net/images/13281dc2234b4f7709926a9aecaf30ff.png)

确认服务信息，点击 **确认购买**

![EMQX Cloud 确认购买增值服务](https://static.emqx.net/images/657ae7f40653ee7c4443f5d4cf1afc86.png)

点击 **前往服务** 即可开始配置使用增值服务。

![EMQX Cloud 购买增值服务成功](https://static.emqx.net/images/f1a9f14c0e03a8b7cab37c3781114271.png)
 

> 注：不同版本部署仅显示该版本部署可使用及已开通的增值服务。

## 计费方法

NAT 网关及内网负载均衡开通之后会自动获得 **14 天免费试用**，在第一个试用实例结束或删除后，下一个创建的实例将收取费用。

试用结束后 NAT 网关和内网负载均衡功能将分别按照 **0.6 元 / 小时 和 0.1 元/小时** 计费，会在您 EMQX Cloud 主账号下的账户余额中按小时结算扣取费用。如果账户余额不足会自动删除该增值服务。

费用的相关明细可以在 **财务管理 -> 概览 -> 小时账单和历史账单** 中查看到扣费明细。

![EMQX Cloud 增值服务账单](https://static.emqx.net/images/1d7b2fdf8549afa911b8044f5b17bfc1.png)

> 注：当增值服务所在部署停止时，非试用增值服务会正常计费。为避免额外费用产生，请删除此部署下的增值服务。

## 配置说明

### 内网负载均衡配置

完成内网负载均衡增值服务购买后，您可在相应部署概览处看到内网负载均衡创建状态，等待创建完成。

![EMQX Cloud 内网负载均衡配置](https://static.emqx.net/images/0eb216ddb0b78297bb2c6589ae44f079.png)

当内网负载均衡的状态为 running 后，您可以将完成对等连接的 VPC 下终端通过内网地址的内网 IP 连接到该部署，连接端口和公网连接端口一致：mqtt 端口为 1883，websocket 端口为 8083。

### NAT 网关配置

完成 NAT 网关增值服务购买后，您可在相应部署概览处看到 NAT 网关创建状态，等待创建完成。

![EMQX Cloud NAT 网关配置](https://static.emqx.net/images/5052c77852973a04d82f7c030a52d7ef.png)

当 NAT 网关的状态为 running 后，该部署便可访问公网资源。

未开启 NAT 网关访问公网资源：

![未开启 NAT 网关访问公网资源](https://static.emqx.net/images/23e8e62a22cf840f266107416446ae13.png)

开启 NAT 网关后访问公网资源：

![开启 NAT 网关后访问公网资源](https://static.emqx.net/images/334d5fb30b8c099ca97fd9fb86ed38f4.png)
 

EMQX Cloud 产研团队将持续收集用户需求，推出更多增值服务以满足不同类型用户的个性化需求。若您有任何需求希望能在 EMQ X Cloud 中实现，欢迎点击[https://jinshuju.net/f/JRJkK5](https://jinshuju.net/f/JRJkK5)参与增值服务功能试用反馈活动，我们将抽取幸运用户送出 EMQ 惊喜周边礼包！
