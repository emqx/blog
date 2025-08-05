## **引言：IT 与 OT 数据的融合价值**

在工业数字化转型的进程中，IT（信息技术）与 OT（运营技术）的深度融合是释放数据价值的关键。来自 PLC、数控机床等 OT 设备的实时数据，只有与 IT 系统中的业务数据相结合，才能构成完整的决策视图。而这些 IT 系统（如 MES、ERP 或 WMS）的核心数据通常存储在 MySQL 等关系型数据库中，包含了生产工单、物料信息、质量标准等关键上下文信息。

将 OT 实时数据与 IT 业务数据进行有效关联，可以催生出一系列高价值的工业应用场景：

- **增强型质量追溯**：将设备的精确运行参数与特定的产品工单和批次进行绑定。
- **精细化生产分析**：通过结合工单计划与设备的实时产出数据，实现对 OEE（设备综合效率）的精准计量。
- **智能化维护策略**：依据 ERP 系统中的设备历史维护记录与实时工况，对预测性维护计划进行动态优化。

如何构建一座高效、可靠的数据桥梁，将存储在 MySQL 数据库中的 IT 数据，同步至工业物联网（IIoT）平台是一个普遍存在的难题。传统的固定周期全量轮询（`SELECT * FROM ...`）方案，不仅对生产数据库造成不必要的性能压力，还会产生大量的数据冗余。因此，寻求一种更为优雅且高效的解决方案至关重要。

本文将详细介绍如何运用工业边缘平台 NeuronEX，通过其内置的**增量查询**与**流式处理**能力，实现从 MySQL 到 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 高效、可靠的数据同步。

## **目标与架构**

本实践旨在构建一个具备以下能力的数据管道：

1. **自动化周期性采集**：从 MySQL 数据库表中自动拉取数据。
2. **增量数据获取**：仅采集新产生的数据，避免重复和冗余。
3. **标准化数据格式**：将拉取的数据统一转换为 JSON 格式。
4. **可靠的数据上报**：通过 MQTT 协议将数据发布至 IIoT 平台（本文以公共 EMQX 服务器为例）。
5. **高可用性**：具备故障恢复能力，在服务中断后可从断点处继续同步。

为实现此目标，技术架构将由三个核心组件构成：

- **MySQL**：作为业务数据的来源。
- **NeuronEX**：承担数据采集、增量状态管理、处理转换以及转发的核心引擎。
- **EMQX**：作为数据的汇聚点与分发中心。

## **实施步骤**

为便于快速验证，所有组件均通过 Docker 进行部署。您只需在本地环境中安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)。

### **环境准备**

请执行以下命令启动所需服务：

```
# 启动 NeuronEX
docker run -d --name neuronex -p 8085：8085 --log-opt max-size=100m --privileged=true emqx/neuronex：3.6.0

# 启动 MySQL
docker run -d --name mysql -p 3306：3306 -e MYSQL_ROOT_PASSWORD=123456  mysql：8.0
```

此外，请准备 MQTT 客户端（例如 [MQTTX](https://mqttx.app/zh)）用于后续的数据验证。

### **步骤一：初始化数据源 MySQL**

首先，在 MySQL 数据库中创建一张模拟数据表。该表的设计包含了两个关键字段：一个自增的 `id` 主键和一个 `Time` 时间戳。这两个字段将作为后续实现增量查询的基础。

```
-- 连接到 MySQL
-- docker exec -it mysql mysql -u root -p

-- 创建数据库和表
CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;
CREATE TABLE DeviceData （ 
    id INT AUTO_INCREMENT PRIMARY KEY,
    Time TIMESTAMP NOT NULL, 
    DeviceName VARCHAR（100） NOT NULL, 
    Current INT, 
    Voltage INT  
）;

-- 插入初始数据
INSERT INTO DeviceData （Time, DeviceName, Current, Voltage） VALUES （'2025-07-23 09：00：00', 'moter_A', 100, 200）;
INSERT INTO DeviceData （Time, DeviceName, Current, Voltage） VALUES （'2025-07-23 09：00：05', 'moter_B', 120, 210）;
INSERT INTO DeviceData （Time, DeviceName, Current, Voltage） VALUES （'2025-07-23 09：00：10', 'moter_C', 150, 220）;
```

![image.png](https://assets.emqx.com/images/b7688d92e617887ad5812f18013b4792.png)

### **步骤二：配置 NeuronEX 实现增量查询**

**此步骤是本方案的技术核心。**我们将利用 NeuronEX 的 **SQL Source** 功能，实现智能化的增量数据采集。

首先，创建一个代表从 MySQL 持续流入数据的流。

#### **1. 创建 SQL 连接器**： 

在 NeuronEX 的「**数据处理 -> 配置**」界面，创建一个指向 MySQL 实例的数据库连接器。

![image.png](https://assets.emqx.com/images/9613307680a096e60d2747157f1d736c.png)

#### **2. 定义增量查询流**：

在「**数据处理 -> 源管理**」界面，创建一个新的 SQL 流 `mysql_stream2`，并进行以下关键配置：

- **查询模板（Query Template）**：使用带有占位符的模板化 SQL 语句，NeuronEX 将在运行时动态填充。

```
SELECT * FROM DeviceData WHERE id > {{.id}};
```

- **索引字段名（Index Field）**：指定 `id` 字段作为增量查询的依据。
- **索引字段格式（Index Field Type）**：指定索引字段名的数据类型。
- **索引字段初始值（Index Init Value）**：定义首次查询的起始点，此处为 `0`。

![image.png](https://assets.emqx.com/images/c4198c14682745b7ee3ee40b2817cf40.png)

#### **3. 工作原理剖析：**

NeuronEX 的增量查询机制具备状态记忆功能。在执行首次查询（`WHERE id > 0`）后，系统会自动记录返回结果集中的最大 `id` 值（例如 `3`）。在下一个查询周期，NeuronEX 会用该值替换查询模板中的 `{{.id}}` 占位符，从而动态生成并执行新的查询语句（`WHERE id > 3`）。这一设计使其成为一个有状态的数据采集器，确保了仅拉取新增数据，从而显著降低了源数据库的负载和网络开销。

此外，NeuronEX 同样支持基于**时间戳字段**的增量查询，提供了灵活的配置选项以适应不同的表结构设计，详情请查阅[文档](https://docs.emqx.com/zh/neuronex/latest/best-practise/sql-data.html)。

### **步骤三：数据转发与验证**

数据流成功建立后，下一步是将其路由至目标系统。

**创建规则与 Sink**：在 NeuronEX 的「**数据处理 -> 规则**」界面，创建一个用于处理数据的规则：

```
SELECT * FROM mysql_stream2 -- mysql_stream2 为上一步创建的流名称
```

为该规则添加一个 **MQTT Sink**，并配置目标 MQTT Broker 的地址（`tcp：//broker.emqx.io：1883`）和主题（`topic/mysql`）。

![image.png](https://assets.emqx.com/images/3a48b4c4ff72fca6e9b5ffb1db62ecaa.png)

**结果验证**：

1. 使用 MQTTX 客户端订阅 `topic/mysql` 主题。

2. 在 MySQL 中插入3条新的记录：

   ```
   INSERT INTO DeviceData （Time, DeviceName, Current, Voltage） VALUES （'2025-07-23 09：00：30', 'moter_c', 601, 701）;
   INSERT INTO DeviceData （Time, DeviceName, Current, Voltage） VALUES （'2025-07-23 09：00：40', 'moter_c', 602, 702）;
   INSERT INTO DeviceData （Time, DeviceName, Current, Voltage） VALUES （'2025-07-23 09：00：50', 'moter_c', 603, 703）;
   ```

1. 观察 MQTTX 客户端，几秒内即可接收到这条新增的数据。

   ![image.png](https://assets.emqx.com/images/b664817c8a2e7ff7224ea479ff91cf32.png)

### **提升系统可靠性：Checkpoint 机制**

为保证系统在重启或网络异常等情况下的数据一致性，NeuronEX 提供了 **Checkpoint** 机制。

在规则选项中，将**流的 QoS** 设置为 `At-Least-Once`  或 `Exactly-Once`，并配置适当的**检查点间隔**。NeuronEX 将周期性地将增量查询的索引值（`id` 或时间戳）持久化保存，从而实现故障后的无缝恢复。

![image.png](https://assets.emqx.com/images/25a8140bcddbdf3509212921b84bb3e4.png)

## **结论**

通过本次实践，我们展示了如何利用 NeuronEX 平台，构建一个从 MySQL 数据库到 IIoT 平台的实时、高效且可靠的数据桥梁。其核心优势在于通过有状态的增量轮询机制，以极低的系统开销实现了准实时的数据同步。

请参照文档，自行动手实践这份最佳实践方案：

[NeuronEX 最佳实践：集成 MySQL 数据到您的 IIoT 平台 | NeuronEX 文档](https://docs.emqx.com/zh/neuronex/latest/best-practise/sql-data.html)

除了 MySQL，NeuronEX 还支持对 `SQLServer`、`PostgreSQL`、`SQLite` 和 `Oracle` 等数据库的数据拉取。在实际的工业场景中，用户可以进一步利用 NeuronEX 强大的流式计算能力，对来自不同数据源的数据进行实时的清洗、转换、聚合以及关联分析（例如，将 MySQL 的工单数据与 PLC 的设备状态数据进行 JOIN 操作），最终将附带丰富业务上下文的高价值数据，输送至上层应用系统。

NeuronEX 致力于打破工业场景下的数据孤岛，为企业构建统一、高效的数据基础设施，从而加速其数字化转型进程。

欢迎下载 NeuronEX：[下载 NeuronEX](https://www.emqx.com/zh/downloads-and-install/neuronex) 





<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
