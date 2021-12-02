EMQ X Enterprise 企业级物联网 MQTT 消息平台，支持百万级物联网设备一站式接入、MQTT&CoAP 多协议处理、低时延实时消息通信。支持基于 SQL 的内置规则引擎，灵活处理/转发消息到后端服务，存储消息数据到各种数据库，或桥接 Kafka、RabbitMQ 等企业中间件。

EMQ X Enterprise 适用于各种物联网应用场景，助力企业快速构建物联网应用，并支持公有云、私有云、物理机、容器/K8S 任意部署。

网址：https://www.emqx.com/zh/products/emqx

下载：无需提供任何信息， 立即[下载试用](https://www.emqx.com/zh/downloads?product=enterprise)

![enterprisemqttbroker.png](https://static.emqx.net/images/4b87d5ae6dc17bb84f6414e4d8fc504c.png)

## 概览

EMQ X Enterprise v4.2.2 版本规则引擎可以选择同步/异步方式存储数据，部分资源提供批处理启用开关，用户可根据需要选择不同的数据处理模式，平衡数据处理性能与数据时序问题。

同时，该版本提高了 LwM2M 协议易用性，可以通过 Dashboard 可视化界面与 REST API 单独管理 LwM2M 连接，包括通过 LwM2M 协议接入 EMQ X 的客户端列表以及对应的 Object 和 Resource。

详细更新日志：https://www.emqx.com/zh/changelogs/enterprise/v4.2.2

## 功能

### 规则引擎

[EMQ X 规则引擎](https://docs.emqx.cn/broker/latest/rule/rule-engine.html)用于配置消息流与设备事件的处理、转发规则， **支持将数据转发到包括 Apache Kafka、Clickhouse 在内的多种数据库、流处理与数据分析系统中，快速构建一站式物联网数据集成，清洗，存储，分析，可视化平台。**

作为 EMQ X 重磅功能，规则引擎基于 SQL 提供了清晰、灵活的 "配置式" 的业务集成方案，简化了业务开发流程，提升用户易用性并降低业务系统与 EMQ X 的耦合度。

4.2.2 版本中规则引擎新增以下功能：

#### 新增支持 Oracle、MS SQL Server、DolphinDB 数据库

Oracle、MS SQL Server 均是商业关系型数据库阵营中的杰出代表，拥有较高的市场占有率，此次更新填补了技术栈完整性的不足，覆盖了更多的客户群体。

[DolphinDB](https://www.dolphindb.cn/) 是由浙江智臾科技有限公司研发的一款高性能分布式时序数据库，集成了功能强大的编程语言和高容量高速度的流数据分析系统，为海量结构化数据的快速存储、检索、分析及计算提供一站式解决方案，适用于量化金融及工业物联网等领域。EMQ X 结合 DolphinDB 为金融、工业网物联网提供更多的数据处理选择。



#### 可为动作配置同步/异步两种数据处理方式

此前出于时序考虑，规则引擎仅支持使用同步模式处理设备数据，以 Publish 为例，规则引擎数据入库时会阻塞 Publish 流程，等待入库之后才将消息发布到指定主题。

消息量较大的情况下，如果用户不希望阻塞正常的 Pub/Sub 及其他流程，可以在创建规则引擎的时候选择异步模式，异步模式可以将设备消息通信与数据处理分离，避免规则引擎阻塞客户端正常行为。

> 实际使用中两者的时序差别基本不会影响到业务，规则引擎动作优先推荐使用异步模式。



#### 更多动作支持批处理并提供启用配置

此前规则引擎只有少数动作如 保存数据到 MySQL 支持批处理，并且默认启用了批处理功能无法关闭。

目前支持批处理的资源：MySQL、PostgreSQL、ClickHouse、TDengine、Cassandra、SQL Server、Oracle、DolphinDB。

**启用批处理能够带来数倍的性能提升，但是也存在相应的问题**。以 MySQL 为例，规则引擎执行动作时不会立即写入数据库，而是会等待进行批处理：

- 原理：将一定条数或一段时间内的多个 INSERT 操作将合并为一个，以便提高插入效率
- 满条数执行（批量数）：待执行的 INSERT 操作满 100 条，合并为一条插入，重置计时器
- 到时间执行（批量间隔）：如果等待 10ms 还未满 100 条，合并为一条插入，重置计时器

> 批量数与批量间隔可在创建动作时自行设置。

这个过程中存在的问题是：

- 落库有延迟：受批量间隔与批量数影响，数据不是实时入库的
- 批量插入部分失败：部分数据错误可能导致整批数据丢失，如约束错误、类型错误，MySQL 中有对应的处理方式但是容易被用户忽略
- 操作审计问题：批量插入可能使数据库 SQL 审计变得复杂

此次更新后，用户可以决定是否在动作上启用批处理功能来规避以上问题。

![1.png](https://static.emqx.net/images/32a742d0794b9027561bb05972b86b06.png)





### 支持 LwM2M 可视化与 REST API 管理

LwM2M 是由 Open Mobile Alliance(OMA) 定义的一套适用于物联网的轻量级协议，它提供了设备管理和通讯的功能，尤其适用于资源有限的终端设备。

EMQ X-LwM2M 实现了 LwM2M 的大部分功能，应用程序和 MQTT 客户端可以通过 EMQ X-LwM2M 访问支持 LwM2M 的设备，设备也可以往 EMQ X-LwM2M 上报 notification，实现数据双向通信。

![image20201208112020883.png](https://static.emqx.net/images/0833d7b92d6ac8814dac5e19fd0e59e5.png)

EMQ X v4.2.2 中，用户可以通过 Dashboard 可视化界面与 REST API 单独管理 LwM2M 连接，获取 Lw 连接的 IMEI、LifeTime、objectList 等信息，帮助企业快速实现安全可靠的设备互联、IoT 平台及垂直行业应用开发。


> 早在 2017 年 EMQ X 就提供了对 CoAP 和 LwM2M 协议的支持，并成功应用在商业项目上（参见 [NB-IoT 爆发期，EMQ 助力企业开启亿级物联网连接时代](https://www.emqx.com/zh/blog/emqx-nb-iot-access-solution)）。此次更新后相关功能易用性迈上了一个台阶， **EMQ X 已跻身全球范围内少数可商用且功能完备的 LwM2M Server 行列。**



### 优化 Auth HTTP 性能

EMQ X 可以向用户自定义的认证 HTTP 服务发起请求，查询认证与 ACL 权限，认证服务通过返回的 HTTP **响应状态码** (HTTP statusCode) 来控制认证结果。

相比于数据库认证、JWT 等认证方式，HTTP 认证能够实现更为复杂的认证鉴权逻辑，本次更新优化了 EMQ X 认证请求 HTTP 性能，能够承载更高的连接、发布/订阅速率。



### 功能调整

- 新增 SSL 支持配置CA证书的 depth



### 问题修复

- 修复 规则引擎 动作异步模式计数不准的问题
- 修复 在热升级中的异常问题

### 联系

如果对 EMQ X 企业版有任何问题，请随时通过 [contact@emqx.io](mailto:contact@emqx.io) 与我们联系。
