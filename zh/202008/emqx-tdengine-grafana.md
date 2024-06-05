物联网数据采集涉及到大量设备接入、海量的时序数据传输，EMQX [MQTT 服务器](https://www.emqx.com/zh/products/emqx) 与 TDengine 大数据平台的组合技术栈完全能够胜任场景中的海量时间序列监测数据的传输、存储和计算。

数据入库后，往往需要其他方式如数据可视化系统将数据按照规则统计、展现出来，实现数据的监控、指标统计等业务需求，以便充分发挥数据的价值，TDengine 搭配开源软件 Grafana 可以快速搭建物联网数据可视化平台。

上述整套方案无需代码开发，涉及的产品均能提供开源软件、企业服务、云端 SaaS 服务不同层次的交付模式，能够根据项目需求实现免费版或企业版私有化落地以及云端部署。

![image20200804111913555.png](https://assets.emqx.com/images/db641cd1e0ca859288f0ded6918e078c.png)



## 方案介绍

### EMQX 简介

[EMQX ](https://www.emqx.com/zh) 是基于高并发的 Erlang/OTP 语言平台开发，支持百万级连接和分布式集群架构，发布订阅模式的开源 MQTT 消息服务器。EMQX 内置了大量开箱即用的功能，其 **开源版 EMQX Broker** 及 **企业版 EMQX Enterprise** 均支持通过规则引擎将设备消息存储到 TDengine。

### TDengine 是什么 

[TDengine](https://www.taosdata.com/cn/) 是涛思数据专为物联网、车联网、工业互联网、IT 运维等设计和优化的大数据平台。除核心的快 10 倍以上的时序数据库功能外，还提供缓存、数据订阅、流式计算等功能，最大程度减少研发和运维的复杂度，且核心代码，包括集群功能全部开源。

TDengine 提供社区版、企业版和云服务版，安装/使用教程详见 [TDengine 使用文档](https://www.taosdata.com/cn/documentation20)。

### Grafana 简介

[Grafana](https://grafana.com/) 是一个跨平台、开源的度量分析和可视化工具，可以查询处理各类数据源中的数据，进行可视化的展示。它可以快速灵活创建的客户端图表，面板插件有许多不同方式的可视化指标和日志，官方库中具有丰富的仪表盘插件，比如热图、折线图、图表等多种展示方式；支持 Graphite，TDengine、InfluxDB，OpenTSDB，Prometheus，Elasticsearch，CloudWatch和 KairosDB 等数据源，支持数据项独立/混合查询展示；可以创建自定义告警规则并通知到其他消息处理服务或组件中。



## 业务场景

本文模拟物联网环境数据采集场景，假设现有一定数据的环境数据采集点，所有采集点数据均通过 [MQTT 协议](https://www.emqx.com/zh/mqtt-guide) 传输至采集平台（MQTT Publish），主题设计如下：

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
- 通过可视化系统查看 **任意区域、任意时间区间内** 的指标数据，如平均值、最大值、最小值。



## 环境准备

本文所用各个组件均有 Docker 镜像，除 EMQX 需要修改少数配置为了便于操作使用下载安装外，TDengine 与 Grafana 均使用 Docker 搭建。

安装包资源与使用教程参照各自官网：

 - EMQX：EMQ 官网 [https://www.emqx.com/zh/](https://www.emqx.com/zh)
 - TDengine：涛思数据官网 [https://www.taosdata.com/cn/](https://www.taosdata.com/cn/)
 - Grafana：Grafana 官网 [https://grafana.com/](https://grafana.com/) 

### 安装 EMQX

> 如果您是 EMQX 新手用户，推荐通过 [EMQX 文档](https://docs.emqx.com/zh/emqx/latest/) 快速上手

访问 [EMQX 下载](https://www.emqx.com/zh/try) 页面下载适合您操作系统的安装包，本文截稿时 EMQX 开源版最新版本为 v4.1.1，下载 zip 包的启动步骤如下 ：

```bash
## 解压下载好的安装包
unzip emqx-macosx-v4.1.1.zip
cd emqx

## 以 console 模式启动 EMQX 方便调试
./bin/emqx console
```

启动成功后浏览器访问 [http://127.0.0.1:18083](http://127.0.0.1:18083) 访问 EMQX 管理控制台 Dashboard，使用 `admin` `public` 默认用户名密码完成初次登录。

**EMQX 企业版 4.1.2 提供了原生 TDengine 写入插件，性能更好、使用更方便，请移步[规则引擎-写入数据到 TDengine](https://docs.emqx.com/zh/enterprise/latest/rule/rule-engine.html)查看**

### 安装 TDengine

为了方便测试使用通过 Docker 进行安装（需映射网络端口），也可以使用安装包的方式进行安装：

```bash
## 拉取并启动容器
docker run -d --name tdengine -p 6030-6041:6030-6041 tdengine/tdengine:latest

## 启动后检查容器运行状态
docker ps -a
```

### 安装 Grafana

使用以下命令通过 Docker 安装并启动 Grafana：

```bash
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

启动成功后浏览器访问 [http://127.0.0.1:3000](http://127.0.0.1:3000) 访问 Grafana 可视化面板，使用 `admin` `admin` 默认用户名密码完成初次登录，登录后按照提示修改密码使用新密码登录进入主界面：



## 配置 EMQX 存储数据到 TDengine

### TDengine 创建数据库与数据表

进入TDengine Docker 容器：

```bash
docker exec -it tdengine bash
```

创建 `test` 数据库:

```bash
taos
create database test;
```

创建 sensor_data 表，关于 TDengine 数据结构以及 SQL 命令参见 [TAOS SQL](https://www.taosdata.com/cn/documentation20/taos-sql/#表管理)：

```sql
use test;
CREATE TABLE sensor_data (
  ts timestamp,
  temperature float,
  humidity float,
  volume float,
  PM10 float,
  pm25 float,
  SO2 float,
  NO2 float,
  CO float,
  sensor_id NCHAR(255), 
  area TINYINT,
  coll_time timestamp
);
```

### 配置 EMQX 规则引擎

打开 EMQX Dashboared，进入 **规则引擎** -> **规则** 页面，点击 **创建** 按钮进入创建页面。

#### 规则 SQL

规则 SQL 用于 EMQX 消息以及事件筛选，以下 SQL 表示从 `sensor/data` 主题筛选出 payload 数据：

```sql
SELECT
  payload
FROM
  "sensor/data"
```

使用 **SQL 测试功能** ，输入测试数据进行筛选结果测试，测试有结果且输出内容如下，标明 SQL 编写正确：

```json
{
  "payload": "{\"temperature\":30,\"humidity\":20,\"volume\":44.5,\"PM10\":23,\"pm2.5\":61,\"SO2\":14,\"NO2\":4,\"CO\":5,\"id\":\"10-c6-1f-1a-1f-47\",\"area\":1,\"ts\":1596157444170}"
}
```

![image20200731104046137.png](https://assets.emqx.com/images/8472e8d9f9c52e551acf97c2d834f299.png)

#### 响应动作

为支持各种不同类型平台的开发，TDengine 提供符合 REST 设计标准的 API。通过 [RESTful Connector](https://www.taosdata.com/cn/documentation20/connector/#RESTful-Connector) 提供了最简单的连接方式，即使用 HTTP 请求携带认证信息与要执行的 SQL 操作 TDengine。

使用 EMQX 开源版中的 **发送到 Web 服务** 即可通过 RESTful Connector 写入数据到 TDengine。即将到来的 **EMQX 企业版** 4.1.1 版本将提供原生更高性能的写入 Connector。

发送到 Web 服务需要两个数据，一个是关联资源，另一个是消息内容模板。

- 关联资源：HTTP 服务器配置信息，此处为 TDengine 的 RESTful Connector
- 消息内容模板：此处为携带数据的 INSERT SQL，注意我们应当在 SQL 中指定数据库名，字符类型也要用单引号括起来， 消息内容模板为：

```sql
INSERT INTO test.sensor_data VALUES(
  now,
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
  ${payload.ts}
)
```

![image20200731145609393.png](https://assets.emqx.com/images/f73bb9afb9a4761684211fa679c269f5.png)

#### 创建过程

点击响应动作下的 **添加** 按钮，在弹出框内选择 **发送数据到 Web 服务**，点击 **新建资源** 新建一个 WebHook 资源。

![image20200731104403456.png](https://assets.emqx.com/images/e349ad825172d0061a1a5874e7792825.png)


资源类型选择 **Webhook**，请求 URL 填写 http://127.0.0.1:6041/rest/sql，请求方法选择 POST， **还需添加 Authorization 请求头作为认证信息** 。 

Authorization 的值为 Basic + TDengine 的 ` {username}:{password}` 经过 Base64 编码之后的字符串, 例如 `root:taosdata` 编码后实际填入的值为：`Basic cm9vdDp0YW9zZGF0YQ==`

在响应动作创建页面选择新建的资源，并填入消息模板内容即可。

![image20200804110459517.png](https://assets.emqx.com/images/cd2e8dd754f6b2717709113f7dbffa53.png)



## 生成模拟数据

以下脚本模拟了 10000 个设备在过去 24 小时内、每隔 5 秒钟上报一条模拟数据并发送到 EMQX 的场景。

- 总数据量： 24 * 3600 / 5 * 100 = 172 万条
- 消息 TPS： 20

读者安装 Node.js ，按需修改配置参数后可以通过以下命令启动：

```bash
npm install mqtt mockjs --save --registry=https://registry.npm.taobao.org
node mock.js
```

附：模拟生成数据并发送到 EMQX 代码，请根据集群性能调整相关参数

```javascript
// mock.js
const mqtt = require('mqtt')
const Mock = require('mockjs')

const EMQX_SERVER = 'mqtt://localhost:1883'
const CLIENT_NUM = 100
const STEP = 5000 // 模拟采集时间间隔 ms
const AWAIT = 5000 // 每次发送完后休眠时间，防止消息速率过快 ms
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
   "area": Mock.Random.integer(0, 20),
   "ts": 1596157444170,
 }
}
```



## 可视化配置

组件安装完成，模拟数据写入成功后，按照 Grafana 可视化界面的操作指引，完成业务所需数据可视化配置。

### 添加数据源(Add data source)

> Grafana 的 TDengine 数据源需要手动安装插件，具体安装范式以 TDengine 文档为准。

添加数据源，即显示的数据源信息。选取 **TDengine** 类型数据源，输入连接参数进行配置，默认情况下，关键配置信息如下：

![image20200804110612868.png](https://assets.emqx.com/images/0a42fece1ec3a769c2b2dc78479362a0.png)

### 添加仪表盘(New Dashboard)

> 在 EMQX Sample 仓库获取[Grafana 仪表盘导出文件](https://github.com/emqx/example/blob/master/RuleEngine-TDengine/Grafana-template.json)导入即可查看图表示例。

添加好数据源后，添加需要显示的数据仪表盘信息。仪表盘为多个可视化面板的集合，点击 **New Dashboard** 后，选择 **+ Query** 通过查询来添加数据面板。

创建面板需要四个步骤，分别是 **Queries(查询)** 、 **Visualization(可视化)** 、 **General(图表配置)** 、 **Alert(告警)** ，创建时间

### 平均值面板

使用 Grafana 的可视化查询构建工具，查询出所有设备的平均值。

以下 SQL 按照指定时间段（\$form \$to）、指定时间间隔(\$interval)，查询出数据中关键指标的平均值：

```sql
select avg(temperature), avg(humidity), avg(volume), avg(PM10), avg(pm25), avg(SO2), avg(NO2), avg(CO)  from test.sensor_data where coll_time >= $from and coll_time < $to interval($interval)
```

**Visualization** 默认不做更改， **General** 里面修改面板名称为 **历史平均值**，如果需要对业务进行监控告警，可以在 **Alert** 里编排告警规则，此处仅做可视化展示，不使用此功能。

![image20200803091833280.png](https://assets.emqx.com/images/a8407abf05af262989d8049cda3a4932.png)

完成创建后，点击左上角返回按钮，该 Dashboard 里成功添加一个数据面板。点击顶部导航栏 **保存** 图标，输入 Dashboard 名称完成 Dashboard 的创建。

### 最大值、最小值面板

继续点击 Dashboard 的 **Add panel** 按钮，添加最大值、最小值图表。操作步骤同添加平均值，仅对查询中 **SELECT** 统计方法字段做出调整，调整为 **AVG** 函数为 **MAX** 与 **MIN**：

```sql
select max(temperature), max(humidity), max(volume), max(PM10), max(pm25), max(SO2), max(NO2), max(CO), min(temperature), min(humidity), min(volume), min(PM10), min(pm25), min(SO2), min(NO2), min(CO)  from test.sensor_data where coll_time >= $from and coll_time < $to interval($interval)
```
![image20200803093314019.png](https://assets.emqx.com/images/92ffe66972f5e35bd6ddc087eb8255d8.png)

### 仪表盘效果

保存仪表盘，拖拽调整每个数据面板大小、位置，最终得到一个视觉效果较好的数据仪表盘。仪表盘右上角可以选择时间区间、自动刷新时间，此时设备持续发送数据采集数据，仪表盘数据值会有所变动，实现了比较好的可视化效果。



## FAQ

Q: 为什么 Grafana 中没有图标数据？
- 请拖动时间范围，检查、确保所选时段内有数据

Q: EMQX 开源版和 EMQX 企业版写入 TDengine 功能上有什么区别？
- 开源版使用 Webhook + TDengine RESTful Connector，两边都有一定的性能损耗，最大写入速度约为 700 条/秒
- 企业版使用 EMQX 原生插件，能够做到 20,000 条/秒写入

Q: 规则执行了，但是写入不了数据？
- 请检查认证信息是否配置正确，请求头、连接地址、端口等信息是否匹配 TDengin 版本



## 总结

至此我们借助 EMQX + TDengine 完成了物联网数据传输、存储、展现整个流程的系统搭建，读者可以了解到 EMQX 丰富的拓展能力与 TDengine 完备的大数据平台特性在物联网数据采集中的应用。深入学习掌握 Grafana 的其他功能后，用户可以定制出更完善的数据可视化乃至监控告警系统。

![image20200803093438116.png](https://assets.emqx.com/images/0d68e86dfb77cac91dc0911258fb873b.png)



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
