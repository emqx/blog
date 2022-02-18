EMQX Enterpeise（企业版） v4.4.0 于今日正式发布！

在全新的 4.4.0 版本中，我们新增了对 InfluxDB v2 API、SAP Event Mesh 以及 MatrixDB 的集成支持，增强了与 MongoDB Atlas 的集成能力，同时引入在线 Trace 和慢订阅统计两个全新功能以增强诊断能力，以及修复了各项问题以提升稳定性，改善产品使用体验。

最新版本下载地址：[https://www.emqx.com/en/try?product=enterprise](https://www.emqx.com/en/try?product=enterprise)

## 集成能力增强

### 支持 InfluxDB 2.0 & InfluxDB Cloud

规则引擎新增对 InfluxDB v2 API 的支持。至此，EMQX Enterprise 规则引擎将同时支持 InfluxDB 1.x 与 2.x 多个版本。在此基础上，我们还提供了对 InfluxDB Cloud 的支持，用户可以方便快捷地选择私有化部署或云服务。

### 支持 SAP Event Mesh

规则引擎新增对 SAP Event Mesh 的支持。

Event Mesh 是 [SAP BTP](https://www.sap.com/products/business-technology-platform.html) 重要的消息交换组件，SAP BTP 囊括了 SAP 的所有技术组合，例如 SAP HANA（内存计算平台）、 SAP Analytics Cloud（分析云）、SAP Integration 套件 （集成套件）和 SAP Extension 套件（扩展套件）。

从 4.4.0 版本开始，EMQX 的物联网数据可以通过此通道进入到 SAP BTP 平台的诸多产品中。

### 支持 MatrixDB

规则引擎新增对超融合时序数据库 MatrixDB 的支持。目前[已通过单机 21 万行/秒的写入量测试](https://www.emqx.com/zh/blog/emqx-and-matrixdb)，后续版本将进一步优化提升性能。

### 增强与 MongoDB Atlas 的集成能力

MongoDB 集成支持 DNS SRV 和 TXT Records 解析，可以与 MongoDB Altas 无缝对接，增强了与云服务的集成能力。

## 诊断能力提升

### 支持在线 Trace

现在用户能够直接在 Dashboard 上完成对客户端和主题的追踪操作，与指定客户端或主题相关的事件将被实时捕获到日志中，并且可以在 Dashboard 查看、下载和管理这些日志。这将极大改善用户自行排查、诊断客户端异常行为时的体验。

![EMQX 日志追踪](https://static.emqx.net/images/36b6022f50682f5346121669254a5abd.png)

### 支持慢订阅统计

支持通过慢订阅统计功能及时发现生产环境中消息堵塞等异常情况，提高了用户对此类情况的感知能力，方便用户及时调整相关服务。

![EMQX 慢订阅统计](https://static.emqx.net/images/4fb2f745e0f58962833442d3f2d630e6.png)

## 更加适应行业需求

### 支持动态修改 MQTT Keep Alive

新版本允许用户服务通过 HTTP API 随时更新客户端的 Keep Alive，该这一功能将为车联网行业 T-BOX 等设备在不同工况下的能耗策略切换场景提供便利。

## 稳定性再升一级

### 改进优化

- 支持配置是否将整型数据以浮点类型写入 InfluxDB
- 支持配置是否转发为空的保留消息，以适应仍在使用 MQTT v3.1 的用户
- 优化内置访问控制文件模块的使用交互
- 多语言钩子扩展（exhook）支持动态取消客户端消息的后续转发
- 支持在规则引擎 SQL 语句中使用单引号

### 问题修复

- 修复 RocketMQ 异步写入时数据乱码和统计计数不准的问题
- 修复超多节点的集群环境下 Dashboard 监控页面的显示问题
- 修复规则引擎保存数据到 MySQL 时可能出现较高失败率的问题
- 修复规则引擎 Clickhouse 离线消息功能不可用的问题
- 修复规则引擎 MongoDB 离线消息功能中 Max Returned Count 选项无法使用的问题
- 修复内存占用计算错误的问题
- 修复部分热配置失效的问题

## 未来规划

在 EMQX 的后续版本，我们将主要围绕以下目标继续迭代：

- 提升集群水平扩展能力。我们期望未来 EMQX 单个集群能够支撑数十节点的运行，目前已经提出和实现 Mria 方案，将继续深入测试。
- 提升集群稳定性。我们正在引入  Chaos Testing 以提前验证与确保 EMQX 在出现意外故障时的稳定运行能力。
- 性能优化。我们将陆续覆盖所有外部资源的集成性能测试，以及完成相应的性能优化工作。

 

EMQX Enterprise 现提供 **14 天免费试用**，欢迎点击链接 [https://www.emqx.com/zh/try?product=enterprise](https://www.emqx.com/zh/try?product=enterprise) 下载最新版本，体验最新功能。在产品使用过程中如有任何建议，欢迎通过 [https://www.emqx.com/zh/contact](https://www.emqx.com/zh/contact) 在线提交表单，向我们反馈。
