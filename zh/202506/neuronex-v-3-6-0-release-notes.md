我们非常高兴地宣布，工业边缘网关软件 NeuronEX 3.6.0 版本正式发布！

本次升级带来了全新的「数据探索」功能，标志着 NeuronEX 从强大的工业数据采集网关，演进为集数据采集、边缘存储、智能分析与可视化于一体的综合性边缘智能平台。

在过往版本中，NeuronEX 专注于解决工业现场海量异构数据的实时采集与边缘流式计算难题。而在 3.6.0 版本中，NeuronEX 通过内置时序数据库、AI 赋能的数据分析以及高度可定制的可视化仪表盘，让用户在边缘端就能轻松理解和使用这些数据。全新的「数据探索」功能将原始工业数据转化为可驱动决策的深刻洞察，真正实现了从数据到价值的闭环。

此外，新版本还集成了 Node-RED 并增强了多项核心功能，为工业智能应用提供了更强大的技术支持。

## 数据探索，释放您的工业数据潜力

过去，NeuronEX 采集的数据需要转发到云端或中心化平台进行分析和可视化。现在，这一切都可以在边缘端轻松实现！全新的「数据探索」功能为您提供了一个从数据存储、查询分析到可视化监控的完整闭环，让数据价值触手可及。

该模块包含三大核心组件：

### 1. 内置时序数据存储：开箱即用的数据基石

NeuronEX 3.6.0 现已内置了 **Datalayers 时序数据库**，无需再为边缘数据的持久化进行复杂的选型和配置。

- **一键启用**：在系统配置中轻松开启或关闭 Datalayers 存储服务，并可灵活设置数据保留时长 (TTL)。
- **自动初始化**：服务首次启动时，NeuronEX 会自动创建所需的数据表，实现真正的开箱即用。
- **高效写入**：全新的 `DataStorage` 北向插件通过 gRPC 协议将采集点位数据批量写入 Datalayers，并提供缓存机制，确保高吞吐量下的系统稳定性。

### 2. AI 赋能的数据分析：让每个人都成为数据分析师

我们推出了统一的「数据分析」页面，它不仅仅是一个 SQL 查询工具，更是一个智能的数据交互工作台。

- **直观的数据浏览**：以树形目录清晰展示已存储的驱动、采集组及点位信息，并标注了数据类型，让您对数据结构一目了然。

  ![image.png](https://assets.emqx.com/images/b2cb15dbb3ec13c1eb0fe2fdf3b92d0a.png)

- **智能 SQL 编辑器**：提供关键字提示和语法高亮，让 SQL 编写更高效、更准确。

- **AI 数据分析助手**：您可以通过**自然语言**描述查询需求（例如：“查询过去一天中电机A `tag=MotorA-current` 每一小时的平均温度”），AI 助手即可为您生成精准的 SQL 语句，还可以在 SQL 执行出错时，智能分析错误并进行多轮迭代修正。这极大地降低了数据分析的门槛，让 OT 工程师和业务专家也能轻松从数据中挖掘价值。

  ![image.png](https://assets.emqx.com/images/3a9ee7706bca01f0850324bc92d9d29e.png)

### 3. 可视化仪表盘：打造您的专属监控中心

数据需要被看见才能产生影响力。全新的「仪表盘」功能，让您能够通过简单的拖拽和配置，创建数据可视化看板。

- **丰富的图表类型**：支持折线图（Line）、柱状图（Bar）、统计值（Stat）和表格（Table），满足不同的数据展示需求。
- **灵活的查询配置**：每个图表（Panel）都可以绑定一个或多个 SQL 查询，并通过别名（Alias）区分不同的数据曲线。
- **强大的时间控件**：支持全局时间范围选择（如最近1小时、自定义时间段）和自动刷新机制，确保您始终掌握最新动态。
- **自由的布局定制**：通过拖拽即可调整图表的位置和大小，并利用网格系统进行对齐，轻松打造符合您监控需求的个性化视图。

![image.png](https://assets.emqx.com/images/56e60a1ddff4a70bd4ea3af59ada4272.png)

## 集成 Node-RED ：增强自动化工作流

为了进一步提升 NeuronEX 的灵活性和可扩展性，3.6.0 版本在特定 Docker 镜像中**默认集成了低代码编程工具 Node-RED**。用户可以按需开启服务，通过 WebSocket 或 REST API 等方式将 NeuronEX 的数据轻松推送到 Node-RED，利用其丰富的节点和强大的流程编排能力，快速构建复杂的自动化工作流和应用逻辑。

![image.png](https://assets.emqx.com/images/3df14e980d597197e2e5616c394d9e35.png)

## NeuronHUB：Windows 平台数据采集的统一解决方案

为了解决特定工业协议（如 OPCDA）强依赖 Windows 环境的问题，3.6.0 版本正式推出了全新的辅助软件——**NeuronHUB**。作为原 NeuOPC 的重要升级，NeuronHUB 旨在提供一个统一的 Windows 平台数据采集方案。

- **统一的采集入口**：NeuronHUB 整合了多个需要在 Windows 平台上进行转换采集的驱动，包括 OPCDA、新代 CNC 和三菱 CNC。用户不再需要为不同的 Windows-based 协议部署多个分散的组件，实现了统一管理。
- **商业级功能支持**：针对广泛使用的 OPCDA 协议，NeuronHUB 引入了 License 管理机制，为企业用户的商业部署提供了更规范、更可靠的支持。
- **与 NeuronEX 无缝协同**：作为 NeuronEX 的官方辅助工具，NeuronHUB 旨在将 Windows 环境下的传统设备数据，安全、高效地桥接到 NeuronEX，进而利用 NeuronEX 强大的数据处理、存储和分析能力。

## 持续改进与驱动增强

- **驱动功能增强**：
  - BACnet/IP 驱动新增点位扫描功能。
  - OPCUA、DNP3、Siemens S7 驱动支持链路追踪，便于问题诊断。
  - SparkplugB 应用支持配置静态点位。
- **数据处理能力提升**：数据处理模块新增 Kafka Source 和 WebSocket Source，提供了更多的数据源接入选择。
- **UI/UX 优化**：南/北向节点列表页支持按状态筛选和排序；北向应用订阅页面支持关键字搜索，提升了配置和管理效率。

## 结语

欢迎升级并体验 NeuronEX 3.6.0，开启您的工业数据探索之旅。我们期待您的反馈，并会持续创新，为您的数字化转型提供最强大的边缘数据基础设施。

立即下载 NeuronEX 3.6.0 版本： [https://www.emqx.com/zh/try?tab=self-managed](https://www.emqx.com/zh/try?tab=self-managed)

NeuronEX 3.6.0 完整功能，请查阅文档：[NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/)



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
