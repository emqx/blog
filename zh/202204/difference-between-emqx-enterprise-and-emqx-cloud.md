作为一家开源物联网数据基础设施软件供应商，EMQ 通过全球领先的开源云原生 [MQTT 消息服务器 EMQX](https://www.emqx.io/zh)，为来自全球 50 余个国家的 20000+ 企业用户提供了云边端海量物联网数据高可靠、高性能的实时连接、移动与处理。

始于开源项目，EMQX 现已陆续发展出了私有部署版 [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 和 SaaS 云服务版 [EMQX Cloud](https://www.emqx.com/zh/cloud)，以满足不同类型和规模的企业业务需求，服务企业数字化、实时化、智能化转型。

本文将从产品架构、功能特性、适用场景等方面对 EMQX Enterprise 和 EMQX Cloud 进行详细对比解读，读者可以根据本文了解如何为自身业务场景选择更加合适的物联网数据接入软件产品。

## 产品概况

EMQX Enterprise 是基于 Erlang/OTP 开发的云原生分布式物联网接入平台，具有一体化分布式 MQTT 消息服务和强大的 IoT 规则引擎，支持多种物联网标准协议和行业私有协议。可实现高可靠、支持承载海量物联网终端的 MQTT 连接，支持在海量物联网设备间低延时消息路由。

EMQX Cloud 是 EMQ 推出的全球首个全托管的 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 公有云服务，提供一站式运维代管、独有隔离环境的 MQTT 消息服务。EMQX Cloud 可以帮助您快速构建面向物联网领域的行业应用，轻松实现物联网数据的采集、传输、计算和持久化。

两者都是在 EMQX Broker 的基础上，对支持协议、规则引擎、数据持久化等方面作出一定扩展，帮助连接物联网设备、采集物联网数据的工具。工作流都是采集设备端产生的数据，通过消息路由和消息验证对数据进行保密传输，再通过规则引擎转存到各类第三方数据系统中，进行二次加工处理展现。

![EMQX Enterprise 产品架构](https://assets.emqx.com/images/1088ec1c2865482d88b1ca54f0da5f9a.png)

<center>EMQX Enterprise 产品架构</center>

![EMQX Cloud 产品架构](https://assets.emqx.com/images/3f91c095d5d94ad3be939b0007f4f080.png)

<center>EMQX Cloud 产品架构</center>


**简单来说，二者最大的区别在于交付方式的不同，** EMQX Enterprise 是企业级的私有部署产品，适用于拥有较为完善的运维团队，可以自我管理的企业。EMQX Cloud 是全托管的云原生 MQTT 消息服务，支持部署托管在阿里云、华为云、腾讯云以及亚马逊中国等公有云平台（海外更换为aws、azure、gcp），更加适用于大部分业务架构在云端、需要自动化全托管运维监控的中小型企业。

## 功能对比

| **功能与服务**         | **EMQX Cloud**                                               | **EMQX Enterprise**                                          |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| EMQX消息中间件基础功能 | 完整支持                                                     | 完整支持                                                     |
| 高可用集群             | 支持                                                         | 支持                                                         |
| 监控                   | EMQX Cloud 监控控制台                                        | EMQX 集群监控 Dashboard                                      |
| 规则引擎与数据持久化   | 完整支持                                                     | 完整支持                                                     |
| 部署环境               | 公有云，包括：（国内）阿里云、华为云、腾讯云、亚马逊云科技；（海外）AWS，Azure，Google Cloud | 企业私有环境，支持公有云、私有云、企业私有机房等各类基础架构 |
| 告警集成               | 内置将告警转发到 Slack、Webhook、PagerDuty                   | 需要基于 EMQX API 或者规则引擎消息开发集成                   |
| 日志跟踪               | 在线查看日志                                                 | 日志文件查看                                                 |
| 多账号多项目管理       | 支持                                                         | 不支持                                                       |
| 运维与支持服务         | 7*24 全托管服务运维服务                                      | 多等级在线/现场技术支持服务                                  |
| 认证数据库             | EMQX 内置数据库，外置数据库需要开工单支持                    | 支持内置与外置数据库                                         |
| 模块与插件扩展         | 需要提交工单后支持                                           | 支持                                                         |

## 适用对象对比

EMQX Enterprise 适用于对部署有严格要求，需要部署在指定部署环境尤其是私有环境中。同时企业拥有比较完整的运维支撑团队，具备日常的基础软件运维能力。

EMQX Cloud 则更加适用于公司业务系统已经或计划部署在公有云平台上，对基础架构软件 SLA 有较强需求，并且希望通过购买代运维服务方式减轻团队运维压力，对产品采购流程与付费模式相对灵活的企业。EMQX Cloud 也提供了多项目、多角色的管理能力，为企业项目管理人员提供管理能力。

## 价格及服务支持对比

EMQX Enterprise 和 EMQX Cloud 均由全球支持团队提供 5x8/7x24、线上/线下等不同规格、不同形式的技术支持，同时提供定制开发、架构咨询、项目集成等商业化的服务。 

在价格方面，EMQX Cloud 针对不同版本规格有非常灵活透明的报价，更有按量付费、包年预付两种形式，有不同程度的优惠力度。您可以在这里选择版本规格，进行价格预估：[https://www.emqx.com/zh/cloud/pricing](https://www.emqx.com/zh/cloud/pricing) 

EMQX Enterprise 的价格方案会根据最大连接数上限、使用时长、企业使用场景给出不同的价格模式，详细报价可以点击链接获取：[https://www.emqx.com/zh/contact](https://www.emqx.com/zh/contact) 

## 总结

通过本文，相信读者对于 EMQX Enterprise 和 EMQX Cloud 有了更加清晰的了解。您可根据企业自身的发展状况、业务形态、业务需求等多方面考虑进行选择。同时 EMQX Enterprise 和 EMQX Cloud 均提供一定时长的免费试用，欢迎试用体验，为您的业务做出更加合适的选择。

EMQX Enterprise：[免费下载试用 ->](https://www.emqx.com/zh/try?product=enterprise) 

EMQX Cloud：[免费试用 ->](https://www.emqx.com/zh/try?product=cloud)
