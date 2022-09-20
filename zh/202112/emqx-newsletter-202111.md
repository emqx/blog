本月 EMQX 各团队针对近期发现的各项问题及用户反馈对产品进行了修复及功能升级。[EMQX 开源版](https://emqx.io/zh)发布了 v4.3.10，[EMQX 企业版](https://www.emqx.com/zh/products/emqx)发布了 v4.2.9 与 v4.3.5，进行了基于内置数据库的 ACL 性能优化、集群间调用可能导致客户端进程失去响应的问题修复等更新。[EMQX Cloud](https://www.emqx.com/zh/cloud) 本月上线了多个基于用户实际需求的新功能，持续完善产品体验。

## EMQX ：企业版 v4.4 问世在即，开源版 v5.0-beta.2 进入测试阶段

### EMQX 企业版 v4.4 完成开发

企业版 v4.4 的开发工作目前已经全部完成，版本测试工作正在紧锣密鼓地进行当中，正式版将在十二月与大家见面。

本次发布距上一版本已时隔半年，结合在此期间我们收到的众多企业客户的需求，4.4 版本将为大家带来以下主要功能：

- 规则引擎适配 InfluxDB Cloud (InfluxDB 2.0)
- MongoDB 相关功能均已支持 SRV Record，能够无缝对接 MongoDB Atlas，强化了与云服务的集成能力
- 规则引擎支持与 SAP Event Mesh 直接集成，打通物联网数据与 SAP BTP 平台连接通道

  > 相关新闻：[助力碳中和，EMQ 与 SAP 共同构建绿色 IoT 解决方案](https://www.emqx.com/zh/news/emq-and-sap-iot-solution)

- 规则引擎新增支持 MatrixDB 超融合时序数据库，EMQX 单机通过了 21 万行/秒写入量测试，后续版本还将进一步优化提升性能

  > 相关新闻：[EMQX + MatrixDB 一站式方案助力搭建企业数字资产平台](https://www.emqx.com/zh/blog/emqx-and-matrixdb)

以下功能会同时在后续的开源版中陆续提供：

- 支持动态修改客户端 keepalive，适配车联网 T-BOX 等设备不同工况下的能耗策略切换
- 支持在线 Trace 捕获 DEBUG 级别的日志，方便排查并诊断指定客户端或 Topic 的异常行为
- 支持慢订阅（Slow Subscription）统计，可以及时发现生产环境中消息阻塞等异常情况
- 多语言钩子扩展（exhook）支持动态丢弃客户端 Publish 的消息
- Dashboard 静态资源使用相对路径加载，方便配置反向代理置于网站子目录之下

### EMQX 开源版 v5.0-beta.2 即将发布

5.0-beta.2 现已进入测试阶段，计划于 12 月初发布，在这一版本中主要新增了以下功能：

- 规则引擎重构 Data Bridge 的配置文件结构和 HTTP API
- 规则引擎支持 Data Bridge 的成功/失败、速率等统计计数
- 新增对网关和网关下监听器的认证数据管理接口
- Lwm2m 新增指令下发接口
- 修复认证鉴权的一些问题
- 统一 HTTP API 相关行为
- 引入客户端强制踢除机制
- 支持 CROS
- 支持通过 HTTP API 进行 Trace 操作
- 补充更多测试用例以提高稳定性
- 规范统一的占位符，认证鉴权等功能与规则引擎使用相同的语法、相同的变量

在接下来的 beta.3 版本中，我们将在 Dashboard 上开放更多功能，通过可视化的方式配置所有底层功能，其他一些功能也将同步提供，以下是所有功能列表：

1. 支持在 Dashboard 上配置管理规则引擎
2. 支持在 Dashboard 上查看与配置集群参数，支持运行时热配置
3. 支持 Plugins 管理，无需从代码编译，EMQX 能够安装独立的插件包
4. 提供 Application 与 Exhook 功能
5. 企业版 4.4 中的慢订阅（Slow Subscription） 和在线 Trace、Dashboard 静态资源使用相对路径加载等功能将在此版本中开放

我们热切欢迎和期待每一个用户充分表达自己的期望或需求，你的意见或将成为影响 EMQX 未来发展的关键要素。

### 未来展望

在版本发布的同时，我们也在进行相关技术调研和更新：

1. 将同时发行基于 OTP23 和 OTP24 的版本
2. 将支持滚动升级
3. 高可靠性持久会话的开发分支并入主干，现已经展开性能测试工作
   在5.0之前，EMQX 就已经提供了 MQTT 会话持久化的能力。但是这些会话没有同步到集群里的其他节点。本月，支持高可靠性持久会话的开发分支终于合并进入主干分支，并已开始着手性能测试。
4. 基于 CDK 的 EMQX 集群部署
   本月 EMQX 欧洲研发团队开源了一个集群部署的内部工具 [cdk-emqx-cluster](https://github.com/emqx/cdk-emqx-cluster)，该工具基于 AWS 的 [CDK](https://aws.amazon.com/cdk/) 开发包，有能力部署并配置 EMQX集群以及周边集成的服务，例如 etcd，Kafka 用于跑压力测试的 load generator，以及用于监控的 Prometheus，并自带一个完备的 Grafana Dashboard。

   ![EMQX Grafana Dashboard](https://assets.emqx.com/images/49e918ea98315414d4c1022381bef520.png)

   ![EMQX Grafana Dashboard](https://assets.emqx.com/images/18e291801e09a72ccbf83c74faed1e8d.png)

## EMQX Cloud：关注用户痛点，持续体验优化

### 子账号管理功能上线

为了应对企业内部不同部门和组织独立管理部署、独立核算的需求，[EMQX Cloud 在本月上线了子账号管理功能](https://www.emqx.com/zh/blog/emqx-cloud-launches-sub-account-management)。类似阿里云的 RAM 账号和 AWS 的 IAM 账号，根用户可以创建同一账号体系下的子用户。并通过为子用户分配不同的预置角色（管理员、项目管理员、项目使用者、财务、审计）来分管不同的功能或模块。结合项目管理的功能，可以实现不同的账号管理不同项目中的部署。

通过该功能，用户将可以更精细化管理资源，同时符合了财务、审计上的合规要求。 

### 国内包年部署支持自动续费

国内包年用户在选择自动续费选项后，在余额支持扣除下一年费用的情况下可实现自动续费，并增加相应可开票的余额。自动续费节约了某些客户在财务审批流程上的成本，同时降低了因为没有及时续费而造成停机带来的损失。

### 监控模块新增设备大量离线告警

设备大量离线的情况可能是由一些外在突发事件造成，开发运维人员需要第一时间获得告警信，以避免造成不必要的损失。在最新版本的 EMQX Cloud 中，设置了如下设备离线监控规则：当前连接数与上一次时间记录的连接数的差值大于规格总连接数十分之一时，会在监控中提示消息，告知开发和运维人员及时查看。这将进一步提高系统稳定性。

### 创建海外云服务提示优化

当国内用户需要创建 AWS、Azure 或 GCP 的云服务时，新增了需要前往 EMQX Cloud 海外平台的提示。相比之前直接跳转并登录的流程优化了用户使用体验。

### 规则引擎新增保存数据到阿里云 MongoDB

EMQX Cloud 支持将数据转发到非关系型数据库。目前规则引擎的资源配置新增了阿里云 MongoDB 支持，可以使用规则引擎将数据持久化保存到阿里云的 MongoDB 上。为业务开发者实现数据持久化提供更多选择，更方便地落地业务。

 

为了完成「通过世界级开源软件产品服务人类未来产业与社会」的使命，敬请期待一个更优秀的 EMQX。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
