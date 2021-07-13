

9 月正式开启，EMQ 发布了 EMQ X Enterprise 3.4.0 正式版。该版本强化了管理配置和规则引擎功能，新增消息编解码、集群热配置及车联网协议支持，设计了全新的管理监控 Dashboard 页面，是目前企业应用推荐使用的稳定版本。

相关安装包已在 [EMQ 官网](https://www.emqx.com/zh/downloads) 开放下载，同时官网提供 License 免费自助申请试用、在线购买 License 授权服务。



> EMQ X Enterprise 企业级物联网 MQTT 消息平台，支持百万级物联网设备一站式接入、MQTT&CoAP 多协议处理、低时延实时消息通信。支持基于 SQL 的内置规则引擎，灵活处理/转发消息到后端服务，存储消息数据到各种数据库，或桥接 Kafka、RabbitMQ、Pulsar 等企业中间件。
>
> EMQ X Enterprise 适用于各种物联网应用场景，助企业快速构建物联网应用，并支持公有云、私有云、物理机、容器/K8S 任意部署。



### 全新的 Dashboard UI

在以往版本的 EMQ X 里 EMQ 围绕 MQTT 消息接入，拓展了一系列方便快速构建物联网应用的基础功能，如认证鉴权/ACL，数据持久化和消息桥接（企业版）并集成至 Dashboard 中。

为了支撑更多新功能的引入及功能引入后系统易用性、监控管理能力的同步改进提升，EMQ 开发团队率先针对企业版设计了全新的 Dashboard UI，对界面风格、操作性、应用结构和数据展示重点进行了调整，致力于打造一个功能全面的 IoT Hub 管理平台：

- 实现对 EMQ X 集群状态全面掌控，增加关键运行指标实时展示界面；
- 提供运行指标汇聚统计与持久化记录并前端展示，集群历史消息、连接、主题、订阅指标一目了然；
- 强化商业功能，展示 License 授权信息包括签发公司、授权线数、到期日期，企业运维使用更加方便快捷；
- 实现基础的设备管理功能，简化连接信息，支持在线踢出设备、查看并管理设备订阅信息，手动添加订阅关系等；
- 优化规则创建步骤、提供创建向导方便企业快速学习掌握，明确规则引擎应用关系；
- 新增告警管理，全局展示当前告警条数，提供历史告警记录排查，便于发现问题、解决问题规避告警带来的风险。

![Dashboard UI.png](https://static.emqx.net/images/6f3c03f102056172d84aab29afc654ae.png)



### Dashboard 支持热配置参数

在 3.4.0 之前所有对 EMQ X 主要配置 `etc/emqx.conf` 进行的修改都需要重启才能应用，比如匿名认证(allow_anonymous)、ACL 开关与策略（enable_acl）、连接统计（enable_stats）等等都存在不停机更改的需求。

EMQ 评估后列举了数十项不会影响系统稳定性但是存在热配置需求的配置项，同时在 Dashboard 与 REST API 中提供了热配置功能。

![repeizhi.png](https://static.emqx.net/images/6c574ccd67fece63188cb2a83ea61c84.png)



### Dashboard 支持集群管理

此版本中 Dashboard 新增了针对集群的管理操作功能，可视化界面在手动集群模式下提供集群的邀请加入、踢出功能；其他自动集群的模式下下展示了集群参数，极大的方便了监控管理和新节点的参考配置工作。

![jiqun.png](https://static.emqx.net/images/048fc753ea01ddfabe89b6867b292e21.png)



### 强大的 Schema Registry 

物联网应用中为了兼顾网络传输性能与设备处理能力，很多底层设备通信依赖的消息数据都是较为底层、精简的格式，Broker 需要处理编解码各种压缩的二进制数据格式、行业专有的数据格式甚至是私有数据格式。

以往的处理方案是将这类数据桥接到应用系统中，应用系统编解码处理后再发送回 Broker 进行处理，整个架构集成起来十分复杂，存在处理时延较高、处理逻辑不清晰的问题。

为解决这一痛点 EMQ 设计开发出一套 Broker 内置的、实时的编解码系统 Schema Registry 。Schema Registry 支持 Avro, Protocol Buffers 和第三方编解码服务报文解析。

Schema 与规则引擎结合使用示意图：
![Schema Registry .png](https://static.emqx.net/images/1f442d7acbb906ef9ba6874ebe074e59.png)



目前 EMQ X 支持三种协议解析方式：

- Avro 是一种远程过程调用和数据序列化框架，是在 Apache 的 Hadoop 项目之内开发的。它使用 JSON 来定义数据类型和通讯协议，使用压缩二进制格式来序列化数据，EMQ X Enterprise 内置支持；
- Protocol Buffers 是一种轻便高效的结构化数据存储格式，可以用于结构化数据串行化，或者说序列化。它很适合做数据存储或 RPC 数据交换格式。可用于通讯协议、数据存储等领域的语言无关、平台无关、可扩展的序列化结构数据格式，EMQ X Enterprise 内置支持；
- 第三方编解码服务是通过 TCP、HTTP 通信向外置编解码服务传递原始报文数据，等待返回编解码后的数据而后进行后续逻辑，第三方服务可以是自建的编解码网关甚至可以是目前云计算中火热的 Serverless 应用。


![3.png](https://static.emqx.net/images/528ce7fdc0f13c8f953717a62330ae6f.png)


上图所示我们新建了一个编解码服务，该服务在规则引擎中这样使用：

```sql
SELECT decode('schema:1.0', payload) as payload
FROM 
	"message.publish"
WHERE
	topic =~ 't/#'
```

使用 Schema Registry 结合规则引擎功能，在规则引擎中直接通过 decode、encode 函数调用创建好的编解码规则，这一过程极大的简化消息应用的集成能力。



### 车联网中国国标协议 JT/T808 的支持

新增车联网协议接入 JT/T808，全称 《JT/T 808 - 2013 道路运输车辆卫星定位系统 北斗兼容车载终端通讯协议技术规范》，该协议是行业性较强的通信协议。通过该协议的适配，EMQ 建立起了完整的行业/私有协议接入开发模式，为后续其他协议定制开发提供了成功的模板。

 JT/T808 协议接入架构示意图：

![ JT:T808.png](https://static.emqx.net/images/e7458c830281660b826a3f9e3eb115c4.png)





### 新版本功能规划

未来版本中，Dashboard 的功能将被继续增强，计划持续进行调整优化实现以下功能改进：

- 优化插件配置功能：出于安全性考虑目前 Dashboard 上进行的插件配置不会持久化至 Broker，稳定的配置需要调试成功后手动写入到配置文件。随着 Dashboard 及相关 API 安全性的提升，后续 EMQ 计划将界面上的插件配置进行持久化，大部分场景下无需再对配置文件进行额外操作；
- 提供插件功能管理界面：目前 Dashboard 对插件的管理仅限于进行配置，众多插件如 emqx_auth_clientid、emqx_auth_username、emqx_configs 除了基础配置外还有相应的业务功能和使用方式，EMQ 将逐一在 Dashboard 中适配开发，提供插件的配置与使用界面；
- 插件热安装与热升级：在 Dashboard 中上传二进制插件包，实现不停机的插件安装、升级，热安装热升级主要用于应对 EMQ X 的重要修复和小规模功能升级；
- 自定义告警实现：后续将支持用户自定义告警规则与告警触发方式，实现告警提醒不离线。

------

欢迎关注我们的开源项目 [github.com/emqx/emqx](https://github.com/emqx/emqx) ，详细文档请访问 [官方文档](https://docs.emqx.io/broker/cn)。

![二维码](https://static.emqx.net/images/b99a97727d6f86a9912846e145b8b124.jpg)


