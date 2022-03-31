对于迫切希望开展物联网业务的企业来说，全托管云原生 [MQTT 消息服务 EMQX Cloud](https://www.emqx.com/zh/cloud) 的一大亮点就在于可以通过高性能的内置规则引擎实时提取、过滤、分拆、转换物联网数据，从而简化物联网应用开发，加速业务交付。基于规则引擎实现的开箱即用的数据桥接功能，也可以帮助用户实现与各种云服务的连接，如阿里云 RDS、Kafka、MongoDB、AWS RDS、AWS DocumentDB、 华为云 GaussDB、InfluxDB 等，将物联网数据根据需求转存到各类第三方数据库、消息队列、数据系统中。

规则引擎无疑是 EMQX Cloud 帮助用户实现数据灵活处理与集成的利器。为了让用户更加轻松上手，真正将这一杀手级功能的价值在实际项目应用中发挥出来，EMQX Cloud 团队近日对该功能进行了升级优化。

![EMQX Cloud 数据集成](https://static.emqx.net/images/1a40a7eb3f1b8f3da69f659d283a1e92.png)

规则引擎功能模块现已正式更名为「数据集成」，同时进行了更易于用户理解、操作、管理的 UI 改版升级。对比之前版本的规则引擎模块，新版本「数据集成」通过导航的方式一步步帮助用户快速熟悉资源与规则的创建。用户只需按照创建资源-创建规则-添加动作-测试运行的流程进行操作便可以完成对规则的配置，具体流程如下：

1. 首先在「创建资源」中明确自身业务的数据架构及需要与 EMQX Cloud 对接的数据集成系统，也就是要将数据转存到何种第三方数据库、消息队列或者业务系统接口中。通过此步骤创建相关集成系统的连接信息，以便后续步骤使用。
2. 在「创建规则」中使用 SQL 语句创建一个规则，根据您的业务需求匹配来自设备的数据，即定义「哪些数据需要被处理和集成」。
3. 在「添加动作」中选择定义好的资源，也就是将数据发送到哪个服务，即「处理后的数据到哪里去」。同时，通过消息内容模版定义消息存储与集成的格式，即「数据如何被处理」。

经过以上三步，用户即可完成对设备数据的处理转存的设置，进一步测试运行后完成数据集成。

![创建资源-创建规则-添加动作-测试运行](https://static.emqx.net/images/34bd231ffcafba504c35a84c412d9785.png)

全新改版的「数据集成」将使规则引擎的使用逻辑更加符合用户习惯，为用户利用 EMQX Cloud 搭建符合业务需求的物联网平台与应用提供便利。

EMQX Cloud 免费试用活动进行中，欢迎登录 EMQ 官网 [https://www.emqx.com/zh/cloud](https://www.emqx.com/zh/cloud) 体验新功能。

## 附：数据集成功能使用指南

### 准备工作

使用数据集成功能需要提前了解以下概念，在「数据集成」入门引导概览中，您可以遵循引导步骤进行操作。

![EMQX Cloud 入门](https://static.emqx.net/images/fe246a328f61415f6679b6db8a9111bf.jpeg)
 
同时请注意您使用的 EMQX Cloud 版本：

**基础版部署**

- 资源仅支持公网访问，因此在创建资源前您需要确保资源具有公网访问能力，同时开放安全组。无需创建 VPC 对等连接。
- 资源类型仅开放 Webhook 和 MQTT 桥接。

**专业版部署**

- 开通 NAT 网关前资源仅支持内网访问，因此在创建资源前您需要先配置 VPC 对等连接，同时开放安全组。
- 开通 NAT 网关后，即可支持公网访问。

### 使用教程

- 以使用 EMQX Cloud 数据集成功能，收集模拟温湿度数据并转存到 MySQL 为例：[https://docs.emqx.com/zh/cloud/latest/rule_engine/rule_engine_save_mysql.html](https://docs.emqx.com/zh/cloud/latest/rule_engine/rule_engine_save_mysql.html) 

- 参考文档：[https://docs.emqx.com/zh/cloud/latest/rule_engine/introduction.html](https://docs.emqx.com/zh/cloud/latest/rule_engine/introduction.html)
