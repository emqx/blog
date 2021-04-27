物联网数据采集涉及到大量设备接入、海量的数据传输，[EMQ X 物联网消息中间件](https://www.emqx.cn/products/broker) 与 ClickHouse 联机分析 (OLAP) 数据库的组合技术栈完全能够胜任物联网数据采集传输与存储、分析处理业务。

数据入库后，往往需要其他方式如数据可视化系统将数据按照规则统计、展现出来，实现数据的监控、指标统计等业务需求，以便充分发挥数据的价值，ClickHouse 搭配开源软件 Grafana 可以快速搭建物联网数据分析可视化平台。

上述整套方案无需代码开发，涉及的产品均能提供开源软件、企业服务、云端 SaaS 服务不同层次的交付模式，能够根据项目需求实现免费版或企业版私有化落地以及云端部署。

![image-20200916112653512](https://static.emqx.net/images/5ba8c46006e196b5ee8ca42cf60b2d86.png)



## 方案介绍

### EMQ X 简介

[EMQ X ](https://www.emqx.cn/) 是基于高并发的 Erlang/OTP 语言平台开发，支持百万级连接和分布式集群架构，发布订阅模式的开源 MQTT 消息服务器。EMQ X 内置了大量开箱即用的功能，其 **企业版 EMQ X Enterprise** 支持通过规则引擎将物联网消息数据存储到 ClickHouse。


### ClickHouse 简介

[ClickHouse](https://clickhouse.tech/) 是一个用于数据分析（OLAP）的列式数据库管理系统（column-oriented DBMS），由俄罗斯搜索巨头 Yandex 公司开源。目前国内不少大厂在使用，包括腾讯、今日头条、携程、快手、虎牙等，集群规模多达数千节点。

- [今日头条](https://t.cj.sina.com.cn/articles/view/5901272611/15fbe462301900xolh) 内部用 ClickHouse 来做用户行为分析，内部一共几千个 ClickHouse 节点，单集群最大 1200 节点，日增原始数据 300TB 左右。
- [腾讯](https://www.jiqizhixin.com/articles/2019-10-25-3) 内部用 ClickHouse 做游戏数据分析，并且为之建立了一整套监控运维体系。
- [携程](https://www.infoq.cn/article/WZ7aiC27lLrB7_BcGJoL) 内部从 18 年 7 月份开始接入试用，目前 80% 的业务都跑在 ClickHouse 上。每天数据增量十多亿，近百万次查询请求。
- [快手](https://archsummit.infoq.cn/2019/beijing/presentation/2183) 内部也在使用 ClickHouse，存储总量大约 10PB， 每天新增 200TB， 90% 查询小于 3S。

在国外，Yandex 内部有数百节点用于做用户点击行为分析，优步、CloudFlare、Spotify 等头部公司也在使用，更多用户列表见 [ClickHouse 官网-用户列表](https://clickhouse.tech/docs/en/introduction/adopters/)。


### Grafana 简介

[Grafana](https://grafana.com/) 是一个跨平台、开源的度量分析和可视化工具，可以查询处理各类数据源中的数据，进行可视化的展示。它可以快速灵活创建的客户端图表，面板插件有许多不同方式的可视化指标和日志，官方库中具有丰富的仪表盘插件，比如热图、折线图、图表等多种展示方式；支持 InfluxDB, OpenTSDB, Prometheus, Elasticsearch, CloudWatch 和 KairosDB 等数据源，支持数据项独立/混合查询展示；可以创建自定义告警规则并通知到其他消息处理服务或组件中。

Grafana 4.6+ 版本支持通过插件的形式安装 Clickhouse 数据源，使用前需要在 Grafana 上额外安装 ClickHouse 插件。



## 业务场景

本文模拟物联网环境数据采集场景，假设现有一定数据的环境数据采集点，所有采集点数据均通过 [MQTT 协议](https://www.emqx.cn/mqtt) 传输至采集平台（MQTT Publish），主题设计如下：

```bash
sensor/data
```

传感器发送的数据格式为 JSON，数据包括传感器采集的温度、湿度、噪声音量、PM10、PM2.5、二氧化硫、二氧化氮、一氧化碳、传感器 ID、区域、采集时间等数据。

```json
{
    "temperature": 30,
    "humidity" : 20,
    "volume": 44.5,
    "PM10": 23,
    "pm25": 61,
    "SO2": 14,
    "NO2": 4,
    "CO": 5,
    "id": "10-c6-1f-1a-1f-47",
    "area": 1,
    "ts": 1596157444170
}
```

现在需要实时存储以便在后续任意时间查看数据，提出以下的需求：

- 每个设备按照每 5 秒钟一次的频率进行数据上报，数据库需存储每条数据以供后续回溯分析；
- 通过 ClickHouse 存储原始数据，配合 Grafana 进行数据分析并可视化展示。



## 环境准备

本文所用各个组件均有 Docker 镜像可以快速搭建运行，为方便开发，Grafana 使用 Docker 搭建，ClickHouse 使用文档推荐方式安装，EMQ X 采用安装包或在线云服务的形式集成使用。

相关资源与使用教程参照各自官网：

 - EMQ X：[EMQ 官网](https://www.emqx.cn/)
 - ClickHouse：ClickHouse 产品首页 [https://clickhouse.tech/](https://clickhouse.tech/)
 - Grafana：Grafana 官网 [https://grafana.com/](https://grafana.com/) 



### 安装 EMQ X

#### 方式一：使用 EMQ X Cloud

EMQ 提供了 [全托管的物联网 MQTT 云服务 - EMQ X Cloud](https://cloud.emqx.cn/)，在 EMQ X Cloud 上，用户仅需数分钟即可创建高可用、独享实例的 EMQ X 集群，立即开始原型设计与应用开发而无需关注后续的运维工作。产品上线后，集群可进行不停机扩容以应对业务增长带来的容量扩张，保证可用性的同时最大化节省使用成本。

EMQ X Cloud 为新注册用户提供 6 个月时长的免费试用，注册账号并登录创建试用部署后，点击部署详情中的 **EMQ X Dashboard** 即可打开 EMQ X 管理控制台。

> 使用 EMQ X Cloud 需要保证 ClickHouse 能够被通过公网地址访问。

![image-20200915150048492](https://static.emqx.net/images/2ea6c46681440051e3679a04498c1039.png)



#### 方式二：私有部署安装

> 如果您是 EMQ X 新手用户，推荐通过 [EMQ X 文档](https://docs.emqx.cn/broker/latest/) 快速上手

访问 [EMQ 下载](https://www.emqx.cn/downloads) 页面下载适合您操作系统的安装包，本文截稿时 EMQ X 企业版本为 v4.1.2，下载 zip 包的启动步骤如下 ：

```bash
## 解压下载好的安装包
unzip emqx-macosx-v4.1.2.zip
cd emqx

## 以 console 模式启动 EMQ X 方便调试
./bin/emqx console
```

启动成功后浏览器访问 [http://127.0.0.1:18083](http://127.0.0.1:18083) 访问 EMQ X 管理控制台 Dashboard，使用 `admin` `public` 默认用户名密码完成初次登录。



### 安装 ClickHouse

使用 [ClickHouse 文档](https://clickhouse.tech/#quick-start) 推荐的安装方式安装，本文仅做 Demo 演示，采用华为云 2 核 4GB 规格的云服务器进行安装使用：

```bash
sudo yum install yum-utils
sudo rpm --import https://repo.clickhouse.tech/CLICKHOUSE-KEY.GPG
sudo yum-config-manager --add-repo https://repo.clickhouse.tech/rpm/clickhouse.repo
sudo yum install clickhouse-server clickhouse-client

sudo /etc/init.d/clickhouse-server start
clickhouse-client
```

**默认情况下 ClickHouse 只监听本地端口，如果需要远程访问需要修改配置文件**：

```xml
<!-- /etc/clickhouse-server/config.xml -->
<!-- 找到这一行，取消注释 <listen_host>::</listen_host> 并修改为 -->
<listen_host>0.0.0.0</listen_host>
```

重新启动：

```bash
service clickhouse-server restart 
```



### Grafana 安装

使用以下命令通过 Docker 安装并启动 Grafana：

```bash
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

启动成功后浏览器访问 [http://127.0.0.1:3000](http://127.0.0.1:3000) 访问 Grafana 可视化面板，使用 `admin` `admin` 默认用户名密码完成初次登录，登录后按照提示修改密码使用新密码登录进入主界面。



## 配置 EMQ X 存储数据到 ClickHouse

> EMQ X 企业版支持通过规则引擎将设备事件与消息数据写入到各类数据库与消息中间件中（包括 ClickHouse），参考[文档](https://docs.emqx.cn/broker/latest/rule/rule-example.html#%E4%BF%9D%E5%AD%98%E6%95%B0%E6%8D%AE%E5%88%B0-clickhouse)。

### ClickHouse 创建数据库与数据表

启动 ClickHouse 并进入命令行：

```bash
sudo /etc/init.d/clickhouse-server start
clickhouse-client
```

创建 **test** 数据库:

```sql
create database test;
use test;
```

创建 sensor_data 表，ClickHouse SQL 语法与常规关系数据库有所差别，具体请参考 [ClickHouse 文档-SQL语法](https://clickhouse.tech/docs/zh/sql-reference/syntax/)：

> Grafana 时序显示时需要添加 DataTime 列与 Date 列

```sql
CREATE TABLE sensor_data (
 	temperature Float32,
  humidity Float32,
  volume Float32,
  PM10 Float32,
  pm25 Float32,
  SO2 Float32,
  NO2 Float32,
  CO Float32,
  sensor_id String, 
  area Int16,
  coll_time DateTime,
  coll_date Date
) engine = Log;

-- ClickHouse 命令行中不支持建表语句换行，选用以下 SQL 执行：
CREATE TABLE sensor_data( temperature Float32, humidity Float32, volume Float32, PM10 Float32, pm25 Float32, SO2 Float32, NO2 Float32, CO Float32, sensor_id String, area Int16, coll_time DateTime, coll_date Date) engine = Log;
```



### 配置 EMQ X 规则引擎

打开 EMQ X Dashboared，进入 **规则引擎** -> **规则** 页面，点击 **创建** 按钮进入创建页面。

#### 规则 SQL

规则 SQL 用于 EMQ X 消息以及事件筛选，以下 SQL 表示从 `sensor/data` 主题筛选出 payload 数据：

```sql
SELECT
  payload
FROM
  "sensor/data"
```

使用 **SQL 测试功能**，输入测试数据进行筛选结果测试，测试有结果且输出内容如下，表明 SQL 编写正确：

**测试数据（设备实际上报的数据）：**

```json
{
    "temperature": 30,
    "humidity" : 20,
    "volume": 44.5,
    "PM10": 23,
    "pm25": 61,
    "SO2": 14,
    "NO2": 4,
    "CO": 5,
    "id": "10-c6-1f-1a-1f-47",
    "area": 1,
    "ts": 1596157444170
}
```

**测试输出：**

```json
{
  "payload": "{\"temperature\":30,\"humidity\":20,\"volume\":44.5,\"PM10\":23,\"pm25\":61,\"SO2\":14,\"NO2\":4,\"CO\":5,\"id\":\"10-c6-1f-1a-1f-47\",\"area\":1,\"ts\":1596157444170}"
}
```

![image-20200915163114173](https://static.emqx.net/images/27a5b570c0cac5047c81b781584fecab.png)



#### 响应动作

使用 EMQ X 企业版与 EMQ X Cloud 均支持通过规则引擎写入数据到 ClickHouse，

配置响应动作需要两个数据，一个是关联资源，另一个是 SQL 模板。

- 关联资源：创建一个 ClickHouse 资源，配置连接参数
- SQL 模板：此处为携带数据的 INSERT SQL，注意我们应当在 SQL 中指定数据库名

```sql
INSERT INTO test.sensor_data VALUES(
  ${payload.temperature},
  ${payload.humidity},
  ${payload.volume},
  ${payload.PM10},
  ${payload.pm25},
  ${payload.SO2},
  ${payload.NO2},
  ${payload.CO},
  '${payload.id}',
  ${payload.area},
  ${payload.ts}/1000,
  ${payload.ts}/1000
)
```



#### 创建过程

点击响应动作下的 **添加** 按钮，在弹出框内选择 **保存数据到 ClickHouse**，点击 **新建资源** 新建一个 ClickHouse 资源。

资源类型选择 **ClickHouse**，填入资源名称，服务器地址与认证信息即可：

![image-20200915164110500](https://static.emqx.net/images/b1624cbb7e5665b6d0052f5c21d04f07.png)

在响应动作创建页面选择新建的资源，并填入 SQL 模板即可。

![image-20200915163932584](https://static.emqx.net/images/8ba4873997c3e8a8a7783287218cbab7.png)



## 生成模拟数据

以下脚本模拟了 10 个设备在过去 24 小时内、每隔 5 秒钟上报一条模拟数据并发送到 EMQ X 的场景。

读者安装 Node.js ，按需修改配置参数后可以通过以下命令启动：

```bash
npm install mqtt mockjs --save --registry=https://registry.npm.taobao.org
node mock.js
```

附：模拟生成数据并发送到 EMQ X 代码，请根据集群性能调整相关参数

```javascript
// mock.js
const mqtt = require('mqtt')
const Mock = require('mockjs')

const EMQX_SERVER = 'mqtt://localhost:1883'
const CLIENT_NUM = 10
const STEP = 5000 // 模拟采集时间间隔 ms
const AWAIT = 500 // 每次发送完后休眠时间，防止消息速率过快 ms
const CLIENT_POOL = []

startMock()


function sleep(timer = 100) {
  return new Promise(resolve => {
    setTimeout(resolve, timer)
  })
}

async function startMock() {
  const now = Date.now()
  for (let i = 0; i < CLIENT_NUM; i++) {
    const client = await createClient(`mock_client_${i}`)
    CLIENT_POOL.push(client)
  }
  // last 24h every 5s
  const last = 24 * 3600 * 1000
  for (let ts = now - last; ts <= now; ts += STEP) {
    for (const client of CLIENT_POOL) {
      const mockData = generateMockData()
      const data = {
        ...mockData,
        id: client.options.clientId,
        ts,
      }
      client.publish('sensor/data', JSON.stringify(data))
    }
    const dateStr = new Date(ts).toLocaleTimeString()
    console.log(`${dateStr} send success.`)
    await sleep(AWAIT)
  }
  console.log(`Done, use ${(Date.now() - now) / 1000}s`)
}

/**
 * Init a virtual mqtt client
 * @param {string} clientId ClientID
 */
function createClient(clientId) {
  return new Promise((resolve, reject) => {
    const client = mqtt.connect(EMQX_SERVER, {
      clientId,
    })
    client.on('connect', () => {
      console.log(`client ${clientId} connected`)
      resolve(client)
    })
    client.on('reconnect', () => {
      console.log('reconnect')
    })
    client.on('error', (e) => {
      console.error(e)
      reject(e)
    })
  })
}

/**
* Generate mock data
*/
function generateMockData() {
 return {
   "temperature": parseFloat(Mock.Random.float(22, 100).toFixed(2)),
   "humidity": parseFloat(Mock.Random.float(12, 86).toFixed(2)),
   "volume": parseFloat(Mock.Random.float(20, 200).toFixed(2)),
   "PM10": parseFloat(Mock.Random.float(0, 300).toFixed(2)),
   "pm25": parseFloat(Mock.Random.float(0, 300).toFixed(2)),
   "SO2": parseFloat(Mock.Random.float(0, 50).toFixed(2)),
   "NO2": parseFloat(Mock.Random.float(0, 50).toFixed(2)),
   "CO": parseFloat(Mock.Random.float(0, 50).toFixed(2)),
   "area": Mock.Random.integer(0, 100),
 }
}
```



## 可视化配置

组件安装完成，模拟数据写入成功后，按照 Grafana 可视化界面的操作指引，完成业务所需数据可视化配置。

首选需要安装 Grafana ClickHouse 数据源插件：[查看插件安装步骤](https://grafana.com/grafana/plugins/vertamedia-clickhouse-datasource/installation)

### 添加数据源 (Add data source)

添加数据源，即显示的数据源信息。选取 **ClickHouse** 类型数据源，输入连接参数进行配置，默认情况下，关键配置信息如下：

![image-20200916110233266](https://static.emqx.net/images/384986bdbaca56ab3bf8268fa9681ab4.png)



### 添加仪表盘 (New Dashboard)

添加好数据源后，添加需要显示的数据仪表盘信息。仪表盘为多个可视化面板的集合，点击 **New Dashboard** 后，选择 **+ Query** 通过查询来添加数据面板。

### 平均值面板

使用 Grafana 的可视化查询构建工具，查询出所有设备的平均值。

ClickHouse 插件生成 SQL 时自动填充了一些变量，Grafana 查询时可以识别这些变量：

- $timeSeries：指定的 DateTime 列以及一些转换逻辑，以确保数据采用 Grafana 可以在显示中使用的格式
- $table： 数据库表名
- $timeFilter：自动生成的时间序列过滤条件

我们按照需要，新增两个 AVG 处理后的字段即可：

```sql
SELECT
    $timeSeries as t,
    avg(temperature) as temperature,
    avg(humidity) as humidity
FROM $table

WHERE $timeFilter

GROUP BY t

ORDER BY t
```

对于折线图等带有时间序列的图表，Grafana 需要一个 DateTime 列来选择时间序列。我们必须输入时间序列，并且该列必须是 DateTime 或 Timestamp 数据类型。

点击下图红框中的 编辑 按钮，进入表名、时间列配置：

![image-20200916110544930](https://static.emqx.net/images/ff07248e60a570409f1ee5bc64925fb4.png)

选择数据库、数据表，如果数据表内有 DateTime 与 Date 字段，可以在 Column:DateTime 与 Column:Date 中识别选择出来。

- Column:Date：用于 Grafana 拖拽时间范围的时候过滤数据
- Column:DateTime：用于时序显示时作为时间数据

<img src="https://static.emqx.net/images/07b9a092530b50bfa314447a189f8d4b.png" alt="image-20200916111101870" style="zoom:67%;" />

完成后再次点击编辑按钮，点击图标右上角选择一个时间范围，确保时间范围内有数据，点击 刷新 图标刷新一下数据，即可看到渲染出来的平均值面板。

![image-20200916111420196](https://static.emqx.net/images/1eda9c065405599c21d9163d334e1a08.png)

完成创建后，点击左上角返回按钮，该 Dashboard 里成功添加一个数据面板。点击顶部导航栏 **保存** 图标，输入 Dashboard 名称完成 Dashboard 的创建。



### 最大值面板

继续点击 Dashboard 的 **Add panel** 按钮，添加最大值、最小值图表。操作步骤同添加平均值，仅对查询中 **SELECT** 统计方法字段做出调整，调整为 **AVG** 函数为 **MAX**：

```sql
SELECT
    $timeSeries as t,
    max(temperature) as temperature,
    max(humidity) as humidity
FROM $table

WHERE $timeFilter

GROUP BY t

ORDER BY t
```



### 仪表盘效果

保存仪表盘，拖拽调整每个数据面板大小、位置，最终得到一个视觉效果较好的数据仪表盘。仪表盘右上角可以选择时间区间、自动刷新时间，此时设备持续发送数据采集数据，仪表盘数据值会有所变动，实现了比较好的可视化效果。

![image-20200916112334081](https://static.emqx.net/images/684f512f88a96596d86e5590264e7ebe.png)



## 总结

至此我们借助 EMQ X + ClickHouse 完成了物联网数据传输、存储、分析展现整个流程的系统搭建，读者可以了解到 EMQ X 丰富的拓展能力与 ClickHouse 领先的数据处理分析能力在物联网数据采集中的应用。深入学习掌握 Grafana 的其他功能后，用户可以定制出更完善的数据可视化分析乃至监控告警系统。

