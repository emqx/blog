阿里云私网连接 PrivateLink 是一款安全便捷的网络产品，配置灵活，可满足不同的应用场景，帮助您在专有网络 VPC 中通过私网稳定地访问云上服务，流量不经过互联网，避免通过公网访问服务带来的安全风险。

本文将使用阿里云私网连接 PrivateLink ，在专有网络 VPC 与阿里云上的服务建立安全稳定的私有连接，通过内网 IP 地址实现云服务与 EMQX Cloud 部署间的双向打通。

这种方式非常适用于以下类型的用户：

- 组织架构和业务比较复杂，网络需要根据业务进行调整；
- 不同业务之间的服务需要以安全的方式进行相互访问，或需要与外部供应商和客户进行安全可靠服务互访；
- 对数据的安全性或时延有较高的要求。

 
## EMQX Cloud 简介

[EMQX Cloud](https://www.emqx.com/zh/cloud) 是由 EMQ 推出的可连接海量物联网设备、集成各类数据库及业务系统的全托管云原生 MQTT 服务。作为全球首个全托管的 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 公有云服务，EMQX Cloud 提供了一站式运维代管、独有隔离环境的 MQTT 消息服务，可以帮助用户快速构建面向物联网领域的行业应用，轻松实现物联网数据的采集、传输、计算和持久化。

![EMQX Cloud 架构图](https://assets.emqx.com/images/ffd61b092d9165be0bd9c78d1e62a721.png)

借助云服务商提供的基础计算设施，EMQX Cloud 面向全球数十个国家与地区提供服务，为 5G 与万物互联应用提供低成本、安全可靠的云服务。

更多详情请访问 [EMQ X Cloud 官网](https://www.emqx.com/zh/cloud)，或查看 [EMQ X Cloud 文档](https://docs.emqx.com/zh/cloud/latest/)。

## 阿里云私网连接 PrivateLink 介绍

[私网连接 PrivateLink](https://help.aliyun.com/document_detail/161974.html)能够实现专有网络 VPC 与阿里云上服务建立安全稳定私有连接。

![私网连接 PrivateLink 架构图](https://assets.emqx.com/images/0270099cacf73228078e399554e676c6.png)

[PrivateLink](https://help.aliyun.com/document_detail/161973.html)具有以下**优势**：

- 私网通信

  通过 PrivateLink 访问终端节点服务，访问流量均在阿里云内网转发，不会通过公网，避免了通过公网访问服务带来的潜在安全风险。

- 安全可控

  通过 PrivateLink 访问云服务，可以对 VPC 网络中用于访问服务的弹性网卡添加安全组规则，提供更强的安全保障和控制手段。

- 低延迟和高质量

  通过 PrivateLink 访问云服务，访问请求会在同可用区内转发，提供最低延时方案。

- 管理简单

  灵活的跨账号和跨 VPC 服务访问方式，避免复杂的路由和安全配置。

## 操作流程

### 一、创建部署

[新建部署](https://docs.emqx.com/zh/cloud/latest/deployments/create_deployment.html#限制)，在 EMQX Cloud 概览开通增值服务-内网负载均衡。

![开通增值服务-内网负载均衡](https://assets.emqx.com/images/880a1e08979646760a3d6d37baab19f0.png)

### 二、开启双向 privatelink

#### 1、创建终端节点服务

1. 为实例配置 LB，开启监听端口，检查健康检查状态是否正常。

   ![为实例配置 LB](https://assets.emqx.com/images/2d87a56b539f9648a37ee0cbf68deca6.png)

2. 创建终端节点服务，选择服务资源所在可用区、LB。

   ![创建终端节点服务](https://assets.emqx.com/images/f4e2e9c39ba48fff16ff71e02b1fd9ff.png)

3. 将终端节点服务使用方阿里云 UID 添加服务白名单。

   ![阿里云 UID 添加服务白名单](https://assets.emqx.com/images/e38b316ab806694bf270a6702c97176c.png)

4. 等待终端节点服务使用方发起终端节点连接，点击允许。

   ![点击允许](https://assets.emqx.com/images/1795277c8489d7224eb02ccd676fe0b7.png)

#### 2、创建终端节点

1. 根据对方提供的终端节点服务名称选择可用服务。

   注：终端节点服务名称为终端节点服务实例 ID

   ![选择可用服务](https://assets.emqx.com/images/60e54e97f212eb896e86e305e5f4973e.png)

2. 选择专有网络为部署 VPC。

   ![选择专有网络为部署 VPC](https://assets.emqx.com/images/a563b626f3e3f5f266f7607413af657e.png)

3. 选择安全组为部署安全组。

   ![选择安全组为部署安全组](https://assets.emqx.com/images/ba58824414935ff7a3374ef0eb244c5b.png)

4. 选择可用区与交换机。

   ![选择可用区与交换机](https://assets.emqx.com/images/9d1d83ee1e6bf12163018407a485d9f3.png)

5. 检查服务状态是否正常，若为异常，需检查对方监听端口是否正常开启、是否允许连接。

   ![检查服务状态是否正常](https://assets.emqx.com/images/d2885c7fdf7696a352cd290313ef4649.png)

### 二、连接测试

EMQX Cloud 提供阿里云的终端节点连接 IP 地址或可用区域名，此 IP 地址为终端节点服务的 IP 地址，可在数据集成-资源配置时使用。

如图所示，EMQX Cloud 部署可通过 privatelink 的 IP 地址访问到终端节点服务提供方，即您云服务器上的 Redis 资源。

![访问 Redis 资源](https://assets.emqx.com/images/682949856bb918fb1f100c6f90857f3e.png) 

如图所示，在您的服务器上使用 privatelink 所提供的 IP 地址访问到 EMQX Cloud 部署，返回值为` `200，即成功访问到部署。

![curl 测试](https://assets.emqx.com/images/24ff021574d531384071fdf53fbaeed2.png) 

## 小结

至此，我们完成了借助 PrivateLink 与 EMQX Cloud 建立安全可靠连接的全部流程。

通过使用阿里云私网连接 PrivateLink 的方式，您可以实现 EMQX Cloud 部署所在专有网络 VPC 与阿里云上的服务建立双向、安全、稳定的私有连接，简化网络架构，实现私网访问服务，避免通过公网访问服务带来的潜在安全风险。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
