在本文中，我们将利用 EMQX Neuron 和 EMQX 提供从 OPC UA 到 MQTT 的桥接解决方案。

[EMQX Neuron](https://www.emqx.com/zh/products/emqx-neuron) 是一款云原生的工业连接网关，集 **100+ 协议采集、边缘流式分析与 AI 集成** 于一体，以低延迟、轻量部署的方式将工厂 OT 数据标准化并桥接至 EMQX 及主流云平台，为 AI-Ready 智能制造提供边缘数据基础设施。

EMQXneuron 部署在工业现场边缘，承担「**采集 - 分析 - 交付**」一体化能力：

- **采集**：支持 **100+ 工业协议**（Modbus、OPC UA、Siemens S7、CNC 等），毫秒级高频采集，单节点可支撑大规模点位接入；支持设备反控与多源数据集成（MES/ERP/数据库/视频等）。
- **分析**：内置基于 SQL 的**边缘流式计算引擎**，实现过滤、清洗、聚合、告警与多源融合；支持 Python/Go/JavaScript 插件及 ONNX 等 **AI/ML 边缘推理**，并集成 LLM 辅助的规则编写能力。
- **转发**：通过 MQTT、Sparkplug B、Kafka、WebSocket 等北向接口，将处理后的数据对接 **EMQX** 及 Azure、AWS、Microsoft Fabric、Snowflake 等现代数据与 AI 平台；与 EMQX 协同可构建企业级 **UNS（统一命名空间）** 架构。

相比传统仅做协议转换的连接软件，EMQX Neuron 强调 **软件定义、云原生部署**（Linux/Docker/K8s，内存占用约 200MB 级）、**边缘智能化**与 **更低 TCO 的多站点复制能力**，形成「边缘采集 - 云端管理 - 统一语义」的完整 EMQ 工业数据栈。

[EMQX](https://www.emqx.com/zh/products/emqx) 是一款大规模可扩展的云原生分布式物联网 MQTT 消息服务器。作为全球最具扩展性的 MQTT 消息服务器，EMQX 可为海量物联网设备提供高效可靠的连接，实现消息和事件流的高性能实时移动和处理，帮助用户快速构建关键业务的物联网平台与应用。

EMQX Neuron 的南向 OPC UA 驱动程序可采集和汇总 OPC UA 数据源，将其转换为 MQTT 协议，并传输到 EMQX MQTT Broker。然后，后者将其分发到各种分布式应用程序。

OPC UA 是工业自动化场景中的跨平台通信标准，支持统一的数据建模、安全通信与可靠订阅，常用于 PLC、SCADA、MES 与边缘网关之间的数据互联。结合 MQTT，OPC UA 可负责工业现场数据采集与语义建模，MQTT 则用于轻量化、可扩展的数据分发。更多协议特性、工作原理及与 MQTT 的结合方式，可参考 [OPC UA 协议详解](https://www.emqx.com/zh/blog/opc-ua-protocol)。

本文我们将演示使用 EMQX Neuron 从 Prosys OPC UA Simulator 收集数据，将收集到的数据上传到本地构建的 EMQX MQTT Broker（mqtt://192.168.10.174:1883），最后使用 MQTTX 订阅主题查看数据的变化。

| **应用**                        | **IP 地址**    | **端口** |
| :------------------------------ | :------------- | :------- |
| Prosys OPC UA Simulation Server | 192.168.10.174 | 53530    |
| EMQX Neuron                     | 192.168.10.174 | 7000     |
| EMQX                            | 192.168.10.174 | 1883     |
| MQTTX                           |                |          |

### 安装 OPC UA 模拟器



安装包可从 [Prosys OPC 网站](https://www.prosysopc.com/products/opc-ua-simulation-server/)下载。安装完成后，运行 Prosys OPC UA Simulation。确保 EMQX Neuron 与模拟器运行在同一局域网内。

点击 **Objects->Objects::FolderType->Simulation::FolderType** 查看数据，并选择 Counter::BaseDataVariableType.

![img](https://assets.emqx.com/images/5a4d4723a45d66d48327d45be58fd1e1.png)

### 启动 EMQX



执行以下命令安装并运行 EMQX 容器。有关如何安装 EMQX 容器的更多信息，请访问[安装指南](https://docs.emqx.com/zh/emqx/v5.0/deploy/install.html)。

```
docker pull emqx/emqx-enterprise:6.2.2
docker run -d --name emqx-enterprise -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx-enterprise:6.2.2
```

### 设置 Neuron



Neuron 提供多种安装方法，您可以在[安装指南](https://docs.emqx.com/zh/neuronex/latest/installation/introduction.html)中详细查看。本示例使用容器化部署，以便尽快开始体验 Neuron。执行以下命令安装并运行 Neuron 容器。

```
docker pull emqx/neuronex:3.9.1
docker run -d --name neuronex -p 8085:8085 --log-opt max-size=100m --privileged=true emqx/neuronex:3.9.1

```

打开网络浏览器，输入运行 Neuron 的网关地址和端口号，进入管理控制台页面。默认端口号为8085。通过浏览器访问 `http://localhost:8085`（可以用实际 IP 地址代替 localhost）。

#### 步骤 1：登录



页面打开后，进入登录界面，使用初始用户名和密码（初始用户名：admin，初始密码：0000）登录。

#### 步骤 2：添加南向设备



在**配置**菜单中选择**南向设备**，进入到南向设备界面，点击**添加设备**新增设备。

- 名称：填写设备名称，例如 opcua-195-prosys。
- 插件：下拉框选择 **OPC UA** 插件。

#### 步骤 3：设置南向设备参数



添加南向设备后自动进入设备配置界面，填写参数并提交。

- 端点 URL：填写 OPC UA Simulation Server 的连接地址，如：opc.tcp://192.168.10.174:53530/OPCUA/SimulationServer。
- 用户名：默认不用填写。
- 密码：默认不用填写。
- 证书：默认不用上传。
- 密钥：默认不用上传。

确保 Prosys OPC UA Simulation Server 已经切换到 Expert Mode （**Option->Switch to Expert Mode**），点击 **Certificates** 将左侧列表中的 NeuronClient@localhost 设置为 Trusted。

![Click Certificates](https://assets.emqx.com/images/18303ffbc9c775f0cbcb30243db9a401.png)

#### 步骤 4：在设备卡片中创建组



点击设备节点卡片任意空白处，进入组列表管理界面，点击 **创建** ，弹出 **创建组** 的对话框。填写参数并提交：

- 组名称：填写组名称，例如 group-1。
- 间隔：默认1000。

#### 步骤 5：在组中添加数据点位



进入点列表管理界面，点击**创建**，填写点参数并提交：

- 名称：填写点位名称，例如，Counter。
- 属性：下拉选择点位属性，例如，Read，Write。
- 类型：下拉选择数据类型，例如，INT32。
- 地址：填写驱动地址，例如，3!1001。3代表 OPC UA 模拟器中数据点的 Namespace，1001代表数据点的 Node ID。
- 描述、乘系数、精度不填。

除手动创建点位外，Neuron 还支持 OPC UA 点位扫描功能，可自动浏览并发现 OPC UA Server 中的可用节点。用户可以在扫描结果中直接勾选需要采集的点位，快速生成采集配置，从而减少手动填写节点地址和数据类型的工作量，提升 OPC UA 数据接入效率。更多操作说明请参考 [OPC UA 点位浏览文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/opc-ua/browse.html)。

![image.png](https://assets.emqx.com/images/9c860c9909643bda633d77114a9d3aca.png)

#### 步骤 6：数据监控中查看采集数据



选择**监控**→**数据监控**，进入数据监控界面，查看已创建点位读取到的数值，如下图所示。

- 南向设备：下拉框选择想要查看的南向设备，例如，选择已创建的 opcua-195-prosys。
- 组名称：下拉框选择想要查看所选南向设备下的组，例如，选择已创建的 group-1。
- 选择完成，页面将会展示读取到的组中所有点位的值。

![image.png](https://assets.emqx.com/images/d440f843390c82bdb3915eed8d9d0d0d.png)

#### 步骤 7：为应用程序添加北向插件模块



在**配置**菜单中选择**北向应用**，点击**添加应用**。

- 名称：填写应用名称，例如，MQTT。
- Plugin：下拉框选择 MQTT 插件。

#### 步骤 8：设置北向应用参数



- 客户端 ID：注意此 ID 要相互独立，重复 ID 会导致客户端被踢除。例如设置为，MQTT1999。
- QoS 等级：默认为 0。
- 上报数据格式：默认为 Values-format。
- 写请求主题：默认为/neuron/MQTT/write/req。
- 写响应主题：默认为/neuron/MQTT/write/resp。
- 离线缓存：默认关闭。
- 服务器地址：填写本地安装的 EMQX MQTT Broker 地址，地址为192.168.10.174，即您实际的 IP 地址。
- 服务器端口：默认1883。
- 用户名、密码：不填。
- SSL：默认关闭。

#### 步骤 9：订阅南向点位组



转到订阅组列表，然后单击**添加订阅**。

- 南向设备：下拉框选择已创建的南向设备，例如 opcua-195-prosys。
- 组：下拉框选择所要订阅的组，例如 group-1。
- 主题：MQTT 主题，本例中默认为/neuron/MQTT/group-1。接下来在 MQTTX 中订阅此主题并接收消息。

### 使用 MQTTX 查看数据



可进入 [MQTTX 官网](https://mqttx.app/zh)下载 MQTT X 并安装。安装好后启动 MQTTX 后添加连接，Host 设置为 `mqtt://192.168.10.174`，Port 设置为 `1883`，订阅主题 `/neuron/MQTT/group-1`，就可以接收到 OPC UA 端传输过来的数据了。

![MQTTX](https://assets.emqx.com/images/f72e055d59d5728b079df244ebdb6f0f.png)

## 结语



OPC UA 协议实现了设备之间的通信和数据交换，而 MQTT 则提供了一种高效、灵活和安全的消息传递机制。通过利用这两种协议的优势，该集成可将设备数据无缝传输到云端，从而促进高效、安全的远程监控。从设备和流程中获取实时信息的能力使企业能够优化运营、提高生产率并确保最高质量水平。采用这种创新方法不仅能提高工业系统的整体效率，还能为更智能的数据驱动型决策铺平道路，推动各行业走向更加互联和繁荣的未来。

如果希望进一步体验 EMQX Neuron 的 OPC UA 数据接入能力，可以下载产品并结合官方文档完成安装、配置与集成验证。

**下载 EMQX Neuron：**[下载 EMQX Neuron](https://www.emqx.com/zh/downloads-and-install/neuronex)

**EMQX Neuron 完整文档：**[EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/)



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
