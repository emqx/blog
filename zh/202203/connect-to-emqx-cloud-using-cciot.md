云连接器是阿里云物联网上云解决方案中新推出的一款关键设备，为物联网设备数据上云提供了一种更安全、更稳定的选择。它即开即用，按量计费，简单易用的同时也大幅降低了用户的上云成本。通过安全可信的专网连接，可实现全链路监控，可视化运维。

本文将使用阿里云云连接器 cciot ，通过专用 APN 在物联网终端和 EMQX Cloud 之间建立定向网络连接。

## EMQX Cloud 简介

[EMQX Cloud](https://www.emqx.com/zh/cloud) 是由 [EMQ](https://www.emqx.com/zh) 公司推出的可连接海量物联网设备，集成各类数据库及业务系统的全托管云原生 MQTT 服务。作为全球首个全托管的 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 公有云服务，EMQX Cloud 提供了一站式运维代管、独有隔离环境的 MQTT 消息服务。

在万物互联的时代，EMQX Cloud 可以帮助用户快速构建面向物联网领域的行业应用，轻松实现物联网数据的采集、传输、计算和持久化。

![EMQX Cloud 架构图](https://static.emqx.net/images/ffd61b092d9165be0bd9c78d1e62a721.png)

借助云服务商提供的基础计算设施，EMQX Cloud 面向全球数十个国家与地区提供服务，为 5G 与万物互联应用提供低成本、安全可靠的云服务。

更多详情请访问 [EMQ X Cloud 官网](https://www.emqx.com/zh/cloud)，或查看 [EMQ X Cloud 文档](https://docs.emqx.com/zh/cloud/latest/)。


## 云连接器 cciot 介绍

[云连接器](https://help.aliyun.com/document_detail/323473.html)通过专用 APN 在物联网终端和阿里云之间建立定向网络连接。您也可以通过云上组网，实现物联网终端到物联网应用或本地数据中心 IDC（Internet Data Center）的定向连接。通过专用 APN 在物联网终端和阿里云之间建立定向网络连接。

![物联网专用 APN](https://static.emqx.net/images/51b81906161bd2eb01aae8e851339acf.png)

[云连接器](https://help.aliyun.com/document_detail/323473.html)具有以下**优势**

- 安全可靠

  云连接器通过专用APN实现物联网终端到专有网络VPC的连接，进而实现私网访问VPC内的云服务，构建了一张端到端安全可靠的物联网专网。

- 弹性伸缩

  拥有从运营商网络到阿里云的超宽上云通道，可以保障在业务突发和高峰期物联网终端的稳定连接。

- 海量连接

  支持海量物联网终端上云连接和云上管理，支持端到端链路监控和告警。

- 简单易用

  云连接器配置简单，能够快速开通和配置上云专网。

 
## 阿里云云连接器 cciot 连接到 EMQX Cloud

### 一、EMQX Cloud 相关配置

1. 通过[快速入门](https://docs.emqx.com/zh/cloud/latest/quick_start/create_free_trial.html)创建部署 EMQX Cloud

2. 开通[内网 SLB](https://docs.emqx.com/zh/cloud/latest/vas/intranet-lb.html)，获取内网连接地址

   ![开通内网 SLB](https://static.emqx.net/images/7169c5aea99a1305e74a7f746e84132a.png)

### 二、云连接器 cciot 服务相关配置

1. 购买并激活物联网卡

2. 创建云连接器实例

   ![创建云连接器实例](https://static.emqx.net/images/c127d903bad7f53553abb00bd4d80ce0.png)

3. 添加 IP

   填入物联网卡 IP。

   ![填入物联网卡 IP](https://static.emqx.net/images/642486b81430b9a50da47e88dfc7c02f.png)

4. 配置授权规则

   填入专有网络 vpc 对应网段。

   ![填入专有网络 vpc 对应网段](https://static.emqx.net/images/a84e37236b030bb5035c896e40ec0a21.png)

### 三、连接测试

1. wifi 连接到专网

   将 SIM 卡插入网关，通过 WiFi 连接到专网，即可使用服务器私网地址访问到 EMQX Cloud 所开放的服务和对应端口。

2. 测试连通性

   将物联网卡插入物联网终端设备。

   1. 使用物联网终端设备执行ping命令，测试物联网终端和物联网平台的连通性。如果能接收到回复报文，表示连接成功。

   2. ping 命令，测试物联网终端和 ECS 的连通性。如果能接收到回复报文，表示连接成功。即：ping <ECS的私网IP地址>
   
      ![ping 命令测试](https://static.emqx.net/images/ede381687f2c174d688e1d0838e27464.png)

3. 查看 EMQX Cloud 监控对应的客户端、订阅，即可看到客户端 mqttx_13af315a 已经成功连接到部署，并且订阅了 topic 为 test、QoS 为 0 的消息。

   ![EMQX Cloud 客户端监控](https://static.emqx.net/images/d083fcfd5029e326cfba04c3b6c609ea.png)

4、查看云连接器监控

   ![查看云连接器监控](https://static.emqx.net/images/04160f9753126f3e710b623c00f1bbc4.png)

## 小结

至此，我们完成了阿里云云连接器 cciot 连接到 EMQX Cloud 的全部流程。

通过使用阿里云 cciot 连接到 EMQX Cloud 部署，您的终端设备可以不需要 VPN 或者别的 ssh tunnel，直接用 EMQX Cloud 专业版的内网地址就能链接，相当于将您的终端设备和 mqtt 集群置于同一个网络下。相较于公网连接，更安全，性能更好。
