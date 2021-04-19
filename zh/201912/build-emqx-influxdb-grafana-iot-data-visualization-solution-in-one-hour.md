

![画板 172x8.png](https://static.emqx.net/images/91d497420de71170fd69655588faeac5.png)



本文以常见物联网使用场景为例，介绍了如何利用 EMQ X MQTT 服务器 + InfluxDB + Grafana 构建物联网数据可视化平台，将物联网设备上传的时序数据便捷地展现出来。

在物联网项目中接入平台的设备数据和数据存储方案有以下特点：

- 数据采集的维度、频率、以及设备数量都比较多，采集的数据量比较大，对消息服务器的接入吞吐量、后端数据库的存储空间消耗有很大压力。
- 数据按照采集周期进行上报、传输、存储一般都按照时间序列。

因此在物联网项目中使用时序数据库是比较好的选择。 **时序数据库** 可以带来显著的性能提升，包括更高的容纳率、更快的大规模查询，以及更好的数据压缩率等。数据入库后，往往需要数据可视化平台将数据按照规则统计、展现出来，实现数据的监控、指标统计等业务需求，以便充分发挥数据的价值。



## 业务场景

假设现有一批设备，每个设备有一个 Client ID，所有设备均通过 [MQTT 协议](https://www.emqx.cn/mqtt) 往 [MQTT 服务器](https://www.emqx.cn/products/broker) 上相应的主题发送数据，主题的设计如下：

```bash
devices/{client_id}/messages
```

每个设备发送的数据格式为 JSON，发送的通过该传感器采集的温度与湿度数据。

```json
{
    "temperature": 30,
    "humidity" : 20
}
```

现在需要实时存储数据以便在后续任意时间查看，具体需求如下：

- 每个设备按照每 5 秒钟一次的频率进行数据上报，数据库需存储每条数据；
- 通过可视化系统查看 **任意时间区间内** 的温度/湿度平均值、最大值、最小值，与 **所有时间段内** 温度/湿度的平均值。

可视化平台最终的展示效果如下图。仪表盘右上角可以选择时间区间、自动刷新时间，此时设备持续发送数据，仪表盘数据值会随之变化，实现了功能比较全面的可视化效果。


![image20191125152935211.png](https://static.emqx.net/images/8da1266462ee04b19bc134414f3bc026.png)



## 方案介绍

目前市面上已有多款物联网消息中间件、时序数据库和数据可视化产品，结合数据的采集上报、联网接入、消息存储与可视化功能来看，EMQ X（高性能物联网 MQTT 消息中间件） + InfluxDB（时序数据库）+ Grafana（美观、强大的可视化监控指标展示工具）组合无疑是最佳的物联网数据可视化集成方案。

方案整体架构如下图所示：

![image20191125163959537.png](https://static.emqx.net/images/132d0cbb3f4166478a7c06dbcfa051d4.png)

- **EMQ X**：[EMQ X ](https://github.com/emqx/emqx) 是基于高并发的 Erlang/OTP 语言平台开发，支持百万级连接和分布式集群架构，发布订阅模式的开源 MQTT 消息服务器。EMQ X 内置了大量开箱即用的功能， **其企业版 EMQ X Enterprise 支持通过规则引擎或消息持久化插件将设备消息高性能地存储到 InfluxDB** ，开源用户需自行处理消息存储环节。
- **InfluxDB**：InfluxDB 是一个由 InfluxData 开源的时序型数据库。它由 Go 写成，着力于高性能地查询与存储时序型数据。InfluxDB 被广泛应用于存储系统的监控数据，IoT 行业的实时数据等场景。
- **Grafana**： Grafana 是一个跨平台、开源的度量分析和可视化工具，可以通过灵活的配置查询采集到的数据并进行可视化展示。它可以快速灵活的创建客户端图表，官方库中具有丰富的仪表盘插件，比如热图、折线图、图表等多种展示方式。支持 Graphite，InfluxDB，OpenTSDB，Prometheus，Elasticsearch，CloudWatch 和 KairosDB 等数据源。可以创建自定义告警规则并通知到其他消息处理服务或组件中。



## 实现步骤

本文所用各个组件均有 Docker 镜像，除 EMQ X 需要使用下载安装外（方便修改部分配置），InfluxDB 与 Grafana 均使用 Docker 搭建，详细的安装步骤本文不再赘述。

三大部件的官网均有不同操作系统的安装包资源与教程：

- [EMQ X 官网](https://www.emqx.cn/)
- [InfluxDB 官网](https://www.influxdata.com/)
- [Grafana 官网](https://grafana.com/) 

### EMQ X 安装

#### 安装

访问 [EMQ X 下载](https://www.emqx.cn/downloads) 页面下载适合您操作系统的安装包， **由于数据持久化是企业功能，您需要下载 EMQ X 企业版（可以申请 License 试用）** 。 写本文的时候 EMQ X 企业版最新版本为 v3.4.5，本教程需要使用该版本及以上版本，下载后的启动步骤如下 ：

```bash
## 解压下载好的安装包
unzip emqx-ee-macosx-v3.4.4.zip
cd emqx

## 将 License 文件复制到 EMQ X 指定目录 etc/, License 需自行申请试用或通过购买授权获取
cp ../emqx.lic ./etc

## 以 console 模式启动 EMQ X
./bin/emqx console
```

#### 修改配置

本文中需要用到的配置文件如下：

1. License 文件，EMQ X 企业版 License 文件，使用可用的 License 覆盖：

   ```
   etc/emqx.lic
   ```

2. EMQ X InfluxDB 消息存储插件配置文件，用于配置 InfluxDB 连接信息、选取入库 Topic：

   ```
   etc/plugins/emqx_backend_influxdb.conf
   ```

   根据部署实际情况填写插件配置信息如下：

   ```
   backend.influxdb.pool1.server = 127.0.0.1:8089
   
   backend.influxdb.pool1.pool_size = 5
   
   ## Whether or not set timestamp when encoding InfluxDB line
   backend.influxdb.pool1.set_timestamp = true
   
   ## Store Publish Message
   ## 由于业务仅需 devices/{client_id}/messages 主题，此处修改默认配置的主题过滤器
   backend.influxdb.hook.message.publish.1 = {"topic": "devices/+/messages", "action": {"function": "on_message_publish"}, "pool": "pool1"}
   ```

3. EMQ X InfluxDB 消息存储插件消息模板文件，用于定义消息解析入库模板：

   ```
   ## 模板文件
   data/templates/emqx_backend_influxdb_example.tmpl
   
   ## 重命名修改为
   data/templates/emqx_backend_influxdb.tmpl
   ```

   由于 MQTT Message 无法直接写入 InfluxDB,  EMQ X 提供了 emqx_backend_influxdb.tmpl 模板文件将 MQTT Message 转换为可写入 InfluxDB 的 DataPoint：

   ```
   {
     "devices/+/messages": {
       "measurement": "devices",
       "tags": {
         "client_id": "$client_id"
       },
       "fields": {
         "temperature": ["$payload", "temperature"],
         "humidity": ["$payload", "humidity"]
       },
       "timestamp": "$timestamp"
     }
   }
   ```

   > 关于 EMQ X InfluxDB 使用详细教程见 [ InfluxDB 数据存储](

### InfluxDB 安装

通过 Docker 进行安装，映射数据文件夹与 `8089` udp 端口与 `8086` 端口（Grafana 使用）：

> EMQ X 仅支持 InfluxDB UDP 通道，需要 influx_udp 插件支持，且数据库名称指定为 db

```bash
## 使用 influx_udp 插件
git clone https://github.com/palkan/influx_udp.git

## 进入插件目录
cd influx_udp

## 通过插件配置创建并启动容器
docker run --name=influxdb --rm -d -p 8086:8086 -p 8089:8089/udp \
	-v ${PWD}/files/influxdb.conf:/etc/influxdb/influxdb.conf \
  -e INFLUXDB_DB=db \
  influxdb:latest

## 启动后检查容器运行状态
docker ps -a

```

**至此，可以重启 EMQ X 并启动插件以应用以上配置**:

```bash
./bin/emqx stop

./bin/emqx start

## 或使用 console 模式可以看到更多信息
./bin/emqx console

## 启动插件
./bin/emqx_ctl plugins load emqx_backend_influxdb

## 启动成功后会有以下提示
Plugin emqx_backend_influxdb loaded successfully.

```

### Grafana 安装

使用以下命令通过 Docker 安装并启动 Grafana：

```bash
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

启动成功后浏览器访问 `http://127.0.0.1:3000` 访问 Grafana 可视化面板，使用 `admin` `admin` 默认用户名密码完成初次登录，登录后按照提示修改密码使用新密码登录进入主界面：

![image20191125100532923.png](https://static.emqx.net/images/f4dc1b6aa64a2c542b2ae052b75a5250.png)



## 写入模拟数据

进行可视化配置之前需要写入模拟数据，方便配置过程中进行效果预览。

以下脚本模拟完成了 100 个设备在过去 12 小时内、每隔 5 秒钟上报一条模拟温湿度数据并发送到 EMQ X 的场景，读者安装 Node.js 平台后可以通过以下命令启动：

```bash
npm install mqtt mockjs --save
node mock.js
```

模拟脚本执行完毕后，数据将写入 InfluxDB `db` 数据库中，通过以下命令进入 InfluxDB 容器并查看数据：

```bash
## 进入 docker 容器
docker exec -it influxdb bash

## 进入 influxdb 命令行
root@581bde65650d:/# influx

## 切换到 db 数据库
use db;

## 查询数据
select * from devices limit 1;

## 查询结果
name: devices
time                client_id      humidity temperature
----                ---------      -------- -----------
1574578725608000000 mock_client_1  54.33    98.5

```

附：模拟脚本如下：

```javascript
// Node.js
// mock.js
const mqtt = require('mqtt')
const Mock = require('mockjs')

class MockData {
  constructor(clientNum = 20) {
    this.EMQX_SERVER = 'mqtt://localhost:1883'
    this.clientNum = clientNum
    this.clients = {}
    this.startMock()
  }

  async startMock() {
    const now = Date.now()
    // last 12h every 5s
    for (let ts = now - 12 * 3600 * 1000; ts <= now; ts += 5 * 1000) {
      for (let i = 0; i < this.clientNum; i++) {
        const clientId = `mock_client_${i}`
        const client = this.clients[clientId] || await this.createClient(clientId)
        this.clients[clientId] = client
        const mockData = this.getMockData()
        client.publish(`devices/${clientId}/messages`, JSON.stringify(mockData))
        console.log(`${clientId} send temperature ${mockData.temperature} humidity ${mockData.humidity}`)
      }
    }
  }

  /**
   * Init a virtual mqtt client
   * @param {string} clientId ClientID
   */
  createClient(clientId) {
    return new Promise((resolve, reject) => {
      const client = mqtt.connect(this.EMQX_SERVER, {
        clientId,
      })
      client.on('connect', () => {
        console.log('client s% connected', clientId)
        resolve(client)
      })
      client.on('error', (e) => {
        reject(e)
      })
    })
  }

  /**
   * Generate mock data
   */
  getMockData() {
    return {
      temperature: parseFloat(Mock.Random.float(22, 100).toFixed(2)),
      humidity: parseFloat(Mock.Random.float(12, 86).toFixed(2)),
    }
  }
}

// startup
new MockData(100)

```



## 可视化配置

组件安装完成，模拟数据写入成功后，按照 Grafana 可视化界面的操作指引，完成业务所需数据可视化配置。

### 添加数据源（Add data source）

添加数据源，即显示的数据源信息。选取 **InfluxDB** 类型数据源，输入连接参数进行配置，默认情况下，关键配置信息如下：

- URL：填写 InfluxDB 连接地址，由于我们使用 Docker 安装，Grafana 由于 InfluxDB 容器网络不互通，此处可以输入当前服务器内网/局域网地址而非 `127.0.0.1` 或 `localhost`；
- Auth：InfluxDB 默认启动无认证方式，根据实际情况填写；
- Database：填写 `db` ，为 EMQ X 默认写入数据库名。 

### 添加仪表盘

添加好数据源后，添加需要显示的数据仪表盘信息。仪表盘为多个可视化面板的集合，点击 **New Dashboard** 后，选择 **Add Query** 通过查询来添加数据面板：

![image20191125135546283.png](https://static.emqx.net/images/ad69fdbc04d1284b234452e4e3231da7.png)



创建面板需要四个步骤，分别是 **Queries（查询）**、 **Visualization（可视化）** 、 **General（图表配置）** 、 **Alert（告警）** ，下面按照业务需求完成创建。

### 温、湿度平均值面板

使用 Grafana 的可视化查询构建工具，查询出所有设备的平均值：

- FROM：选取数据的 `measurement`，按照 `emqx_backend_influxdb.tmpl` 文件配置，此处 `measurement` 为 `devices`；
- SELECT：选取、计算的字段，此处两个查询需要使用 **Aggregation** 功能处理，分别选择 `temperature` `mean` 和 `humidity` `mean`，查询并计算温度、湿度字段的平均值；
- GROUP BY：默认使用时间区间聚合。
  - `time($__interval)` 函数表示取 `$__interval` 时间区间内的数据，如 `time(5s)` 表示从每 `5` 秒时间区间原始数据内取出值来进行计算（SELECT 中的计算）
  - `fill` 参数表示没有值时候的默认值，为 `null` 的时候该数据点不会在图表显示出来；
  - `tag` 可选，按照指定 tag 进行显示。
- ALIAS BY：该查询的别名，方便可视化查看。

**Visualization** 默认不做更改， **General** 里面修改面板名称为 `Device temperature and humidity mean value`，如果需要对业务进行监控告警，可以在 **Alert** 里编排告警规则，此处仅做可视化展示，不使用此功能。

![image20191125140117416.png](https://static.emqx.net/images/c7a4f990ef6dd23007c0f45ff9872049.png)



完成创建后，点击左上角返回按钮，该 Dashboard 里成功添加一个数据面板。点击顶部导航栏 **保存** 图标，输入 Dashboard 名称完成 Dashboard 的创建。

![image20191125144011475.png](https://static.emqx.net/images/ca04c7cfedeffd193f7ae1bd9290d7ef.png)




### 温、湿度最大、最小值面板

继续点击 Dashboard 的 **Add panel** 按钮，添加温度最大值、最小值图表。操作步骤同添加平均值，仅对查询中 **SELECT** 统计方法字段做出调整，调整为 **Selectors** 功能中的 `max` 和 `min` 方法。

### 温、湿度总平均值、数据条数面板

继续点击 Dashboard 的 **Add panel** 按钮，添加温、湿度总平均值，数据条数面板。操作步骤近似上面两个步骤，分别使用 `count` 和 `mean` 方法对指定字段操作，取消 **GROUP BY** 字段即可完成查询。 **Visualization** 配置中选择图表类型为 **Gauge(仪表)** 即可。

保存仪表盘，拖拽调整每个数据面板大小、位置，最终得到一个视觉效果较好的数据仪表盘。最终报表完成后，呈现的就是文章开头展示的效果。



## 总结

至此我们完成了 EMQ X + InfluxDB + Grafana 物联网数据可视化平台的搭建。通过本文，读者可以了解到利用 EMQ X 丰富的拓展能力在数据可视化解决方案里可以非常快速、灵活地开发出基于 InfluxDB + Grafana 的可视化系统，实现海量数据存储、计算分析与展现。深入学习掌握 Grafana 的其他功能后，用户可以定制出更完善的数据可视化乃至监控告警系统。

