在万物互联的数字化浪潮中，海量设备连接与实时数据处理成为诸多企业面临的两大困扰。

EMQX 与 TDengine 作为物联网连接与大数据处理领域的领军产品，正在通过技术协同构建端到端的物联网/工业大数据解决方案。为工业互联网、车联网、能源管理、运维监控等诸多场景提供高效可靠的技术支撑。

## **EMQX：企业级 MQTT + AI 平台**

EMQX 是一款云原生分布式 MQTT 接入平台，兼容多种消息传输协议，具备高可用性和扩展性，单节点支持 500 万 MQTT 连接，能够处理大规模并发消息传输，并提供端到端数据加密和细粒度访问控制功能，充分利用数据价值的同时，全面满足企业数据的合规性需求，为物联网（IoT）和人工智能应用提供可靠的实时消息传输和设备连接解决方案。

## **TDengine：企业级时序大数据平台**

TDengine 是一款专为物联网、工业互联网等场景设计并优化的大数据平台，其核心模块是高性能、集群开源、云原生、极简的时序数据库。它能安全高效地将大量设备每天产生的高达 TB 甚至 PB 级的数据进行汇聚、存储、分析和分发，并提供 AI 智能体对数据进行预测与异常检测，提供实时的商业洞察。

## 强强联手，云端合作

作为核心合作伙伴，TDengine 与 EMQX 的私有化部署早已完成深度生态适配。在 SaaS 领域，双方合作再进一步：TDengine Cloud 此前已全面支持 MQTT 数据源接入，实现与 EMQX/EMQX Cloud 时序数据的无缝对接。最新发布的 EMQX Cloud 5.2.13 版本内置了 TDengine Cloud 原生连接器，补齐了双方数据交互的最后一个环节。

**该原生连接器的主要优势为：**

- 简化配置流程：这⼀功能显著简化了时序数据接入 TDengine 的流程，使⽤户⽆需再通过繁琐的 HTTP 连接器配置过程，只需在图形化界面进行简单的配置就可以连接两⼤云服务平台，为业务轻松赋能。
- 原⽣协议⽀持：直接使⽤ TDengine Cloud 的原⽣协议传输数据，避免了 HTTP 连接的额外开销，提升了性能与稳定性。
- ⾼性能数据传输：优化的数据传输机制，确保物联⽹数据能够快速可靠地存储到 TDengine Cloud。
- 灵活的数据处理：强⼤的规则引擎⽀持，可根据业务需求对数据进⾏筛选、转换和处理。
- ⼀站式配置：⽆需分别管理 EMQX 和 TDengine 的连接参数，统⼀在 EMQX Cloud 控制台完成所有配置。
- 可视化监控：集成的数据流监控功能，轻松了解数据流转状态与性能指标。

接下来，我们向大家介绍如何使用该连接器实现 MQTT 数据接入 TDengine Cloud ：

## **EMQX Cloud** 配置操作步骤

以下是配置 EMQX Cloud 与 TDengine Cloud 原⽣连接的详细步骤指南：

### 前置准备

1. **EMQX Cloud** 专有版部署：需要在 EMQX Cloud 平台（[全托管的 MQTT 消息云服务](https://www.emqx.com/zh/cloud) ）注册并创建 EMQX Cloud 专有版部署 。（可免费体验）
2. **TDengine Cloud** 账户：需要在 TDengine Cloud 平台 (https://cloud.taosdata.com/) 注册并创建数据库实例。（可免费体验）
3. ⽹络配置：需要为 EMQX Cloud 专有版部署开通 NAT ⽹关，允许 EMQX Cloud 部署通过公⽹访问 TDengine Cloud 实例。

### 步骤 **1**：**TDengine Cloud** 准备⼯作

1. 登录 TDengine Cloud 控制台 (https://cloud.taosdata.com/)

2. 创建并部署 TDengine Cloud 服务实例

3. 进⼊实例后，在左侧菜单栏中点击"数据浏览器"

4. 创建数据库，例如 "iot_data"

5. 在数据库中创建表：

   ```sql
   CREATE TABLE iot_data.temp_hum (
    ts TIMESTAMP,
    clientid NCHAR(256),
    temp FLOAT,
    hum FLOAT
   ); 
   ```

   ![image.png](https://assets.emqx.com/images/b7b62b8fcd239624ff8a823b7b653cbc.png)

6. 在 TDengine Cloud 控制台获取连接 URL 和访问令牌：TDENGINE_CLOUD_URL、TDENGINE_CLOUD_TOKEN的值以备后⽤。

![image.png](https://assets.emqx.com/images/d51f1fd9935217d5bd75df30ac442d7d.png)

### 步骤 **2**：在 **EMQX Cloud** 创建**TDengine**连接器

1. 登录 EMQX Cloud 控制台

1. 在部署菜单中选择"数据集成"，在数据持久化分类下选择 TDengine

1. 点击"新建连接器"，填写以下信息：

   - 连接器名称：为连接器指定⼀个名称，如 "TDengine Cloud"

   - 主机列表：填写 TDengine Cloud 提供的连接 （TDENGINE_CLOUD_URL的值）

   - Token：填⼊从 TDengine Cloud 获取的访问令牌 （TDENGINE_CLOUD_TOKEN的值）

   - 根据需要配置⾼级设置（可选）

1. 点击"测试连接"按钮验证连接状态，成功后会显示"连接器可⽤"提示 。

   ![image.png](https://assets.emqx.com/images/58ef34da6c5513cd267a6cb043258ffe.png)

5. 点击"新建"按钮完成连接器的创建

### 步骤 **3**：创建数据集成规则

1. 点击刚创建的连接器列表中"操作"列下的"新建规则"图标，或在"规则列表"中点击"新建规则"

2. 在 SQL 编辑器中输⼊规则，定义需要处理的消息，例如：

   ```sql
   SELECT
    now_timestamp('millisecond') as ts,
    payload.temp as temp,
    payload.hum as hum,
    clientid
   FROM
   "devices/temp_hum"
   ```

3. 点击"SQL示例"和"启⽤调试"按钮可以学习和测试规则 SQL 的结果（可选）

4. 点击"下⼀步"开始创建动作 ：

![image.png](https://assets.emqx.com/images/b6b05dc19003d72ed97c62e0be4a1897.png)

### 步骤 **4**：配置动作

1. 从"使⽤连接器"下拉框中选择您刚才创建的 TDengine 连接器

1. 数据库名字：填写在 TDengine Cloud 中创建的数据库名称，如 "iot_data"

1. 配置SQL模板，⽤于将数据写⼊ TDengine Cloud：

   ```sql
   INSERT INTO iot_data.temp_hum(ts, temp, hum, clientid) VALUES (${ts}, ${temp}, ${hum}, '${clientid}')
   ```

1. 启⽤"未定义变量作为 NULL"选项，确保规则引擎在变量未定义时能正确处理 。

1. 根据业务需求配置⾼级选项，如同步/异步模式、批量参数等。（可选）

   注：对消息延迟不敏感（延迟⼩于1s）的情况，可以将最⼤批量请求⼤⼩从 1 修改为 100，从⽽提⾼写⼊性能。

1. 点击"确认"按钮完成动作配置

   ![image.png](https://assets.emqx.com/images/40c25bf52c4a083102a5d7cf012c53d1.png)

1. 在弹出的"成功创建规则"提示框中点击"返回规则列表"，完成整个数据集成配置。

### 步骤 **5**：模拟数据上报

1. 在 EMQX Cloud 部署菜单中选择”在线调试“，并点击连接 。

1. 订阅主题 devices/temp_hum 。

1. 向主题 devices/temp_hum 发送温湿度数据 ：`{"temp": 23, "hum": 90}`

   ![image.png](https://assets.emqx.com/images/c4031b7c891e894e300429f0eeed2a9f.png)

### 步骤 **6**：在 **TDengine Cloud** 查询上报的数据

1. 访问 TDengine Cloud 数据浏览器 。

1. 查询上报数据结果 。

   ```sql
   SELECT * from iot_data7.temp_hum;
   ```

   ![image.png](https://assets.emqx.com/images/164f6ec42e732d2b9b56cc9ee47df0e2.png)

可以看到，数据已经经由 EMQX Cloud 写入了 TDengine Cloud 当中。

关于TDengine Cloud 连接器更具体的使用，可以参考：[将 MQTT 数据写入到 TDengine Cloud | EMQX Platform 文档](https://docs.emqx.com/zh/cloud/latest/data_integration/tdengine_cloud.html) 

## **TDengine Cloud** 配置操作步骤

关于 TDengine Cloud 一侧，同样可以通过部署 MQTT 数据源实现对 EMQX Cloud 的数据接入，具体操作参考TDengine 官方文档：[https://docs.taosdata.com/cloud/data-in/ds/mqtt/](https://docs.taosdata.com/cloud/data-in/ds/mqtt/)，

以及该博客：[https://www.taosdata.com/tdengine-engineering/27256.html](https://docs.taosdata.com/cloud/data-in/ds/mqtt/)

## 写在最后

目前， EMQX Cloud 只支持通过公网将数据接入 TDengine Cloud 当中，后续还会更新以支持私有连接（private link）方式，进一步提升 EMQX Cloud 和 TDengine Cloud 用户的使用体验。

面对数据洪流的挑战与机遇，EMQX 与 TDengine 的深度合作为行业带来了突破性的技术解决方案。不仅构建了支撑海量数据处理的超高性能技术底座，更通过创新性的架构设计，重塑工业互联网与物联网的数据基础设施标准范式，助力企业在数智化转型浪潮中获得关键竞争优势，开启智能化发展的新篇章。
