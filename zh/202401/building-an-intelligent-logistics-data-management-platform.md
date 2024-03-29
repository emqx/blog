顺丰科技与 EMQ 成功举办了关于智慧物流的线上研讨会，讨论顺丰如何利用工业物联网技术来管理物流行业分散复杂的数据，为物流行业数字化转型做出创新尝试。

**顺丰科技物联网平台负责人胡典钢**，分享了物流企业应该如何利用工业物联网技术，实现对物流场景中各类设备、系统、环境、人员，进行全面的数据采集、分析和可视化，为物流企业搭建智慧物流所需要的底层数据基座。

**EMQ 的解决方案总监王凡**，从数据基础软件供应商的角度，探讨了物流行业如何借助最新的物联网技术来利用实时数据去驱动业务决策、提升用户体验、预计降本增效 。以及 EMQ 的企业级消息服务器 EMQX 如何帮助顺丰处理大并发、高吞吐的实时数据。

![顺丰科技胡典钢（右上）在研讨会上分享顺丰对数据平台的性能要求](https://assets.emqx.com/images/38c8739ce8aaefb5f67566429da01d21.png)

<center>顺丰科技胡典钢（右上）在研讨会上分享顺丰对数据平台的性能要求</center>

## 顺丰面临的挑战 

随着顺丰业务规模不断快速增长，以及物流行业本身时空跨度大的特点，顺丰在物流场景中典型的 “收派 - 中转 - 运输” 各环节逐渐面临新的管理风险和运营效率挑战。这其中蕴含大量的物联网业务场景，因此，如何利用物联网实时且真实的数据，持续提升物流运营的效率和质量，成为顺丰非常迫切的需求。以下是顺丰面临的几大挑战：

- **常态化运营监控:** 对于高价值设备和资产，其常态化运营监控数据存在缺失。无法准确了解这些设备或资产在哪些地点、是否正在使用以及使用效果如何。
- **效能提升:** 各类物流中的生产要素如设备、车辆和人员等效率难以量化与提升。缺乏全局性的数据洞察，无法准确评估这些生产要素的效能水平。
- **风险质量控制:** 作业质量与安全风险控制能力需持续改善。包括驾驶安全、快件安全以及作业安全等方面。
- **改善客户体验:** 客户的个性化服务需求响应时效存在问题，同时高价值货物追踪也是需要关注。为了提高客户满意度，需要优化服务流程并加强货物追踪能力。

## 智慧物流与供应链物联网平台价值  

顺丰建立的云边协同智慧物流与供应链物联网平台，帮助公司在设备管理、人员效能管理、以及风险管控几大领域中得到显著、可量化的提升。

- **设备资产管理：**顺丰通过数字化监控与智能化管理，助力标准化运营与自动化生产，实现自动化效益管控。
- **人员效能提升：**通过更精细的计提分摊方法，实现人员效能量化。将原有的“吃大锅饭”的分配方式转变为“多劳多得”的激励机制。
- **风险质量控制：**实时监测与干预 “收派 - 中转 - 运输” 过程中的快件安全、作业安全、司机驾驶安全。降低事故率、减少快件遗失破损。

## **EMQX 助力顺丰科技处理高并发、实时数据接入**

物流场景中的数据处理通常面临海量设备连接数、大并发和高吞吐量数据、以及复杂的网络环境。同时，由于物流行业时效性敏感的特质，企业对这些数据通常也有较高的实时性和准确性的要求。EMQ 企业级的物联网 MQTT 消息服务器 EMQX Enterprise （下文简称 EMQX）帮助顺丰科技更好的接入大并发、高吞吐的实时数据。平台同时提供超过 40 个以上标准的数据库和消息队列的集成，方便物流企业灵活适配其数据处理架构。

![EMQX Platform](https://assets.emqx.com/images/4bea9829885cc75d7c53bffe2c793653.png)

- **高并发消息处理**
  - 部署在云端平台侧、基于 MQTT 协议，EMQX 采用分布式高可用集群架构， 拥有全球领先的 MQTT 数据接入、消息转发分发能力，帮助物流公司处理大吞吐量的实时数据。
  - 单节点支持 500 万 MQTT 设备连接。
  - 集群可水平扩展至支持 1 亿并发的 MQTT 连接。
- **规则引擎与数据集成**
  - EMQX 可与超过 40 种数据存储服务、消息队列、云平台和应用无缝集成。帮助物流平台架构师灵活地去选择数据如何和其他的 IT 中间件、数据库进行适配，完成其架构设计。
  - ﻿﻿EMQX 内置灵活的规则引擎，可以基于设备数据进行实时数据预处理和转发。支持数据过滤、转换、聚合和持久化等操作，帮助物流企业根据业务需求进行分析和决策。
- **高可用和易运维**
  - EMQX 的集群架构能灵活支持动态水平扩展，适应物流业务的扩张。
  - ﻿支持热升级、热配置，保证系统高水平 SLA。
- **安全和认证**
  - EMQX 提供强大的安全功能，包括 TLS/SSL 加密传输、客户端认证和访问控制。支持多种认证方法，如用户名/密码、X.509 证书和 OAuth，确保物联网通信的安全性。
- **可视化监控和管理**
  - EMQX 还提供直观的可视化监控和管理界面，允许用户实时监控物联网设备和消息传输。用户可以查看连接状态、消息流量和其他指标，还可以进行设备管理、故障排除和系统配置操作。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
