将 PLC 数据接入 MQTT 是现代工业数字化的第一步。MQTT 作为轻量级的消息传输协议，凭借其在弱网环境下的可靠传输能力，对实时数据流传输的支持，以及与主流云平台、数据分析工具和 MES 系统的原生兼容性，已成为工业物联网领域的事实标准。

然而，在真实的工厂环境中，将 PLC 数据接入 MQTT 却远比想象中复杂。不同厂商的 PLC 采用不同的通信协议（如 Modbus、OPC UA、西门子 S7、Ethernet/IP 等），传统方案需要为每种协议单独编写驱动程序，部署和维护成本高昂。

**本文将分享如何通过 NeuronEX 实现零代码接入，在 10 分钟内将任意 PLC 快速连接到 MQTT。**

## 为什么 PLC 到 MQTT 的转换如此困难？

在深入解决方案之前，让我们先梳理一下核心问题。

### 协议碎片化

工厂车间的设备来自不同的年代和厂商：

| **PLC 厂商** | **PLC 型号**                           | **协议**                     |
| :----------- | :------------------------------------- | :--------------------------- |
| **西门子**   | S7-200/300/400, S7-1200/1500           | Siemens S7，OPC UA           |
| **罗克韦尔** | MicroLogix, ControlLogix, CompactLogix | Ethernet/IP                  |
| **三菱**     | FX 系列，Q系列，A 系列                 | Mitsubishi 1E，Mitsubishi 3E |
| **欧姆龙**   | CS 系列，CJ 系列，CP 系列，NJ 系列     | Fins TCP，Fins UDP           |
| **倍福**     | CX 系列，C 系列                        | Beckhoff ADS，Modbus         |

每种协议都有自己的数据格式、寻址方式和通信机制。传统方案需要为每种协议开发和维护独立的驱动程序。

### 数据格式不统一

即使成功采集到数据，不同 PLC 的数据格式也千差万别：

- 寄存器地址：`40001`（Modbus）vs `DB1.DBD0`（Siemens）vs `N7:0`（Allen-Bradley）
- 数据类型：INT16、FLOAT、BOOL、STRING...
- 字节序：大端 vs 小端

这些数据需要经过标准化处理后才能发送到 MQTT。

### 部署和维护成本高

传统接入方案往往依赖专用硬件网关，不仅初始采购成本高，还需承担后续一系列隐性支出：硬件网关的部署和调试需要专业工程师现场操作，耗时耗力；针对不同 PLC 协议的驱动适配、固件升级与故障排查，均需支付额外的技术服务费用。

## NeuronEX：无缝连接 OT 和 IT 系统

NeuronEX 是一款专为工业场景设计的工业边缘网关软件，它将协议转换、数据处理和 MQTT 发布整合到一个轻量级的软件中。

NeuronEX 支持 100 多种工业协议，从 Modbus、OPC UA 到西门子 S7。作为通用的工业数据中枢，它从各种不同的工厂资产中收集数据，并将其标准化，以便进行分析和采取行动。

**支持的完整协议列表：**[数采插件列表 | EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/introduction/plugin-list/plugin-list.html) 

### 极致的易用性：零代码、自动化配置

NeuronEX 显著降低了 PLC 接入的技术门槛，使工程师能够专注于业务逻辑而非协议细节：

**自动化的点位发现**

针对 OPC UA 等现代协议，NeuronEX 支持一键扫描南向设备点位，自动识别并导入 PLC 内部的数据结构，无需手动输入寄存器地址。

**批量管理与快速迁移**

支持点位和驱动的批量导入与导出功能。对于拥有成千上万个点位的大型项目，工程师可以通过 Excel/CSV 模板快速完成配置，极大地提升了部署效率。

**直观的连通性诊断**

内置网络连接测试工具和驱动状态监控模块，可实时查看每个驱动的延时、发送/接收字节数及错误率，帮助运维人员在秒级定位通信故障。

**可视化监控与反控**

通过 Web 界面即可实时观察采集到的数据流，并支持对 PLC 寄存器的反向写入操作，实现闭环控制。

### 卓越的并发性能：高吞吐、低延迟

NeuronEX 不仅解决了「连得上」的问题，更在高负载工业环境下确保了「传得稳」：

**单节点 100,000+ 点位支持**

在典型测试场景下（如西门子 S7 驱动），NeuronEX 能够同时管理 10 个驱动，每个驱动配置 10 个采集组，每秒采集 10 万个浮点型点位，满足大规模产线的数据数采需求。

**极低的资源占用**

即便在处理 5 万个并发点位时，内存占用仅约 355MB，CPU 使用率保持在 25% 左右。这意味着 NeuronEX 可以轻松运行在树莓派、工业网关等各类轻量化边缘硬件上。

**毫秒级响应能力**

具备毫秒级的数据下发响应时间，确保了控制指令从云端或边缘侧到 PLC 执行机构的实时性。

![image.png](https://assets.emqx.com/images/4974c33e504ed3e44bbb3a37cda9cd88.png)

## 10 分钟实战：Modbus PLC 到 MQTT

让我们通过一个完整的实战案例来演示整个连接流程。

### 架构概览

![image.png](https://assets.emqx.com/images/c301a65d25c9f47dc560858dfa5f2cbe.png)

### 前提条件

- **PLC 或模拟器**：本例使用 Modbus TCP 模拟器（PeakHMI Slave Simulators）
- **NeuronEX**：通过 Docker 快速部署
- **MQTT Broker**：使用公共 Broker `broker.emqx.io`
- **MQTT 客户端**：使用 [MQTTX](https://mqttx.app/zh) 验证数据

### 步骤 1：启动 NeuronEX

```shell
# 拉取 Docker 镜像
docker pull emqx/neuronex:latest

# 启动容器
docker run -d --name neuronex -p 8085:8085 --log-opt max-size=100m --privileged=true emqx/neuronex:latest
```

访问 `http://localhost:8085`

使用默认账号登录：用户名：`admin`；密码：`0000`

![image.png](https://assets.emqx.com/images/d773d460e480ccd01a328cd992d4f2d2.png)

### 步骤 2：添加南向设备（数据源）

南向设备是 NeuronEX 与 PLC 之间的连接。

1. 进入「**数据采集**」→「**南向设备**」
2. 点击「**添加设备**」
3. 配置设备参数：
   - **名称**：`modbus-tcp-1`
   - **插件**：选择「Modbus TCP」
   - **IP 地址**：填写模拟器的 IP（如 `192.168.1.100`）
   - **端口**：`502`（Modbus TCP 默认端口）
   - 其他参数保持默认
4. 点击「**添加设备**」

![image.png](https://assets.emqx.com/images/6c0f86d3c255470a118c7570d5b5dad1.png)

### 步骤 3：创建采集组和点位

采集组用于将数据点分组，每个组可以设置独立的采集频率。

#### 创建采集组

1. 点击刚创建的 `modbus-tcp-1` 设备卡片
2. 点击「**创建组**」
3. 配置组参数：
   - **组名称**：`group-1`
   - **采集间隔**：`1000`（毫秒，即每秒采集一次）

#### 添加数据点位

1. 点击 `group-1` 组的「**点位列表**」
2. 点击「**添加点位**」
3. 配置点位参数：

| 点位名称     | 属性 | 数据类型 | 地址    | 说明       |
| :----------- | :--- | :------- | :------ | :--------- |
| temperature  | Read | FLOAT    | 1!40001 | 温度传感器 |
| pressure     | Read | INT16    | 1!40003 | 压力传感器 |
| motor_status | Read | BIT      | 1!00001 | 电机状态   |

**地址格式说明**：

- `1!40001`：`1` 是站点号，`40001` 是保持寄存器地址
- `1!00001`：`1` 是站点号，`00001` 是线圈地址

4. 点击「**创建**」

   ![image.png](https://assets.emqx.com/images/10281b0ef0dd419880d85daa13b0eb6a.png)

完成点位创建后，设备状态会自动变为「**已连接**」。

### 步骤 4：验证数据采集

1. 进入「**数据采集**」→「**数据监控**」
2. 选择南向设备：`modbus-tcp-1`
3. 选择组：`group-1`
4. 查看实时数据

![image.png](https://assets.emqx.com/images/214db3045d29da990a32b6e071519cc6.png)

在这里，您将看到每个点位的实时值。

### 步骤 5：配置北向应用（MQTT 发布）

北向应用用于将采集到的数据发送到外部系统。

#### 创建 MQTT 应用

1. 进入「**数据采集**」→「**北向应用**」
2. 点击「**添加应用**」
3. 配置应用参数：
   - **名称**：`mqtt-broker`
   - **插件**：选择「MQTT」

![image.png](https://assets.emqx.com/images/b7d76927d409b89f8141f5f01f27389b.png)

#### 配置 MQTT 连接

1. 在应用配置页面填写：
   - **服务器地址**：`broker.emqx.io`（公共 MQTT Broker）
   - **服务器端口**：`1883`
   - **客户端 ID**：`neuron-client-001`（可选）
   - **用户名/密码**：留空（公共 Broker 无需认证）
2. 点击「**提交**」

应用状态会变为「**运行中**」。

#### 订阅南向数据组

1. 点击 `mqtt-broker` 应用的「**添加订阅**」
2. 配置订阅参数：
   - **主题**：`factory/line1/modbus-tcp-1/data`（自定义主题）
   - **订阅南向驱动数据**：选择 `modbus-tcp-1` → `group-1`

3. 点击「**提交**」

   ![image.png](https://assets.emqx.com/images/7161a08bf9eb0e6419e4b04e59080b20.png)

### 步骤 6：验证 MQTT 数据

使用 MQTTX 客户端验证数据是否成功发布到 MQTT Broker。

1. 打开 MQTTX，创建新连接：
   - **名称**：`Test Connection`
   - **Host**：`broker.emqx.io`
   - **Port**：`1883`
2. 添加订阅：
   - **Topic**：`factory/line1/modbus-tcp-1/data`
3. 查看接收到的数据：

```
{
  "timestamp": 1706745600000,
  "node_name": "modbus-tcp-1",
  "group_name": "group-1",
  "values": {
    "temperature": 23.3,
    "pressure": 88,
    "motor_status": 1
  }
}
```

![image.png](https://assets.emqx.com/images/5e714f916eb366e8f2cd254ec9bca9e8.png)

**恭喜！您已经在 10 分钟内完成了从 Modbus PLC 到 MQTT 的完整数据链路。**

## 进阶功能：支持更多 PLC 协议

以上示例通过 Modbus 模拟器演示了数据采集流程。实际上，NeuronEX 支持超过 100 种工业协议，且连接过程均如本文所示般简单直观。您可以在这里找到详细教程：

- 西门子 S7-1200 PLC：[10 分钟快速入门：使用 NeuronEX 将西门子 S7-1200 PLC 数据接入 MQTT](https://www.emqx.com/zh/blog/connecting-siemens-s7-1200-plc-to-mqtt)  
- 欧姆龙 NX1P 系列 PLC：[Omron NX1P 连接示例 | Neuron 文档](https://docs.emqx.com/zh/neuron/latest/configuration/south-devices/omron-fins/example/nx1p/nx1p.html) 
- 西门子 S7300 系列 PLC：[Siemens S7300 PLC 连接示例 | EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/siemens-mpi/s7300.html)  
- 三菱 FX 系列 PLC：[FX5U 连接示例 | EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/mitsubishi-3e/fx5u.html) 
- 三菱 Q 系列 PLC：[Q03UDE 连接示例 | EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/mitsubishi-3e/q03ude.html) 
- 倍福 CX 系列 PLC：[采集 PLC 数据 | EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/ads/plc-ads/ads.html) 
- 汇川 Easy 系列 PLC：[Easy521 连接示例 | EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/configuration/south-devices/modbus-hc-tcp/example/autoshop/autoshop-modbus.html) 

## 进阶功能：边缘数据处理

NeuronEX 不仅能采集和转发数据，还能在边缘端进行实时数据处理。

### 使用场景

- **数据过滤**：只上传超过阈值的数据（如温度 > 80°C）
- **数据转换**：单位转换（PSI → Bar）、数值计算（+1、×0.9）
- **数据聚合**：计算平均值、最大值、最小值
- **告警触发**：实时检测异常并发送告警

### 快速示例：温度超限告警

**场景**：当温度超过 80°C 时，发送告警到独立的 MQTT 主题。

#### 1. 订阅数据到数据处理模块

在「**数据采集**」→「**北向应用**」中，找到默认的 `DataProcessing` 应用，添加订阅：

- 订阅 `modbus-tcp-1` → `group-1`

数据会自动流入数据处理模块的 `neuronStream` 数据流。

#### 2. 创建处理规则

进入「**数据处理**」→「**规则**」，点击「**新建规则**」：

**SQL 语句**：

```
SELECT
  timestamp,
  node_name,
  values.temperature as temp
FROM neuronStream
WHERE values.temperature > 80
```

#### 3. 配置动作（Sink）

在「**动作**」模块点击「**添加**」，选择「MQTT」：

- **服务器地址**：`broker.emqx.io:1883`
- **主题**：`factory/alerts/high-temperature`
- **数据模板**：

```
{
  "alert_type": "high_temperature",
  "device": "{{.node_name}}",
  "temperature": {{.temp}},
  "timestamp": {{int64 .timestamp}}
}
```

#### 4. 验证告警

在 MQTTX 中订阅 `factory/alerts/high-temperature`，当温度超过 80°C 时，你会收到告警消息。

## 立即开始

将 PLC 连接到 MQTT 不应该是一个复杂、昂贵且耗时的项目。NeuronEX 通过以下方式简化了整个流程：

- **100+ 协议开箱即用**：无需为每种 PLC 编写驱动
- **零代码配置**：Web 界面可视化操作，10 分钟完成配置
- **轻量级部署**：Docker 容器，200MB+ 镜像，256MB 内存
- **边缘计算能力**：SQL 流计算 + AI 算法集成

立即开始您的工业数字化之旅，让数据流动起来。

### 下载安装

**Docker 部署**（推荐）：

```shell
docker pull emqx/neuronex:latest
docker run -d --name neuronex -p 8085:8085 --log-opt max-size=100m --privileged=true emqx/neuronex:latest
```

**其他安装方式**：

- 下载页面：[下载 EMQX Neuron](https://www.emqx.com/zh/downloads-and-install/neuronex) 
- 安装文档：[安装 NeuronEX | EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/installation/introduction.html) 

### 学习资源

- **快速入门**：[快速开始 | EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/quick-start/quick-start.html) 
- **驱动列表**：[数采插件列表 | EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/introduction/plugin-list/plugin-list.html) 
- **最佳实践**：[最佳实践 | EMQX Neuron 文档](https://docs.emqx.com/zh/neuronex/latest/best-practise/overview.html) 

### 获取支持

- **技术支持**：support@emqx.io
- **商务咨询**：sales@emqx.com

### 免费试用

申请 30 天免费试用 License：[免费申请 NeuronEX License](https://www.emqx.com/zh/apply-licenses/neuronex)
