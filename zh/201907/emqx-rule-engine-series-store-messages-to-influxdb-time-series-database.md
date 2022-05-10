## 前言 

[InfluxDB](https://www.influxdata.com/) 是一个用于存储和分析时间序列数据的开源数据库，内置 HTTP API，类 SQL 语句的支持和无结构的特性对使用者而言都非常友好。它强大的数据吞吐能力以及稳定的性能表现使其非常适合 IoT 领域。

通过 EMQX 消息引擎，我们可以自定义 Template 文件，然后将 Json 格式的 MQTT 消息转换为 Measurement 写入 InfluxDB：
![Artboard.jpg](https://static.emqx.net/images/781e57b8706495ae9cfb144b12ccf0c4.jpg)

## 场景介绍

该场景需要将 EMQX 指定主题下且满足条件的消息存储到 InfluxDB 时序数据库。为了便于后续分析检索，消息内容需要进行拆分存储。

**该场景下客户端上报数据如下：**

- Topic：data/sensor

- Payload:

  ```json
  {
    "location": "bedroom",
    "data": {
      "temperature": 25,
      "humidity": 46.4,
      "pm2_5": 0.5
    }
  }
  ```



## 准备工作

### 数据库安装及初始化

创建 `db` 数据库并开放 8089 UDP 端口。

```shell
$ docker pull influxdb

$ git clone -b v1.0.0 https://github.com/palkan/influx_udp.git

$ cd influx_udp

$ docker run --name=influxdb --rm -d -p 8086:8086 -p 8089:8089/udp -v ${PWD}/files/influxdb.conf:/etc/influxdb/influxdb.conf:ro -e INFLUXDB_DB=db influxdb:latest
```



## 配置说明

### 创建资源

打开 EMQX Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，选择 InfluxDB 资源类型并完成相关配置进行资源创建。

![image20190719110910530.png](https://static.emqx.net/images/e377272c97ccaa4eb673e2af15e22d78.png)



### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。触发事件 选择 **message.publish**，即在 EMQX 收到 PUBLISH 消息时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![image20190719112141128.png](https://static.emqx.net/images/0f7df5a54f07b24fc2cf73f895d11e7f.png)



#### 筛选所需字段

规则引擎使用 SQL 语句过滤和处理数据。例如前文提到的场景中我们需要将 ``payload`` 中的字段提取出来使用，则可以通过 `payload.<fieldName>` 实现。同时我们仅仅期望处理 `data/sensor` 主题，那么可以在 WHERE 子句中使用主题通配符 `=~` 对 `topic` 进行筛选：`topic =~ 'data/sensor'`， 最终我们得到 SQL 如下：

```sql
SELECT
  payload.location as location,
  payload.data.temperature as temperature,
  payload.data.humidity as humidity,
  payload.data.pm2_5 as pm2_5
FROM
  "message.publish"
WHERE
	topic =~ 'data/sensor'
```



#### SQL 测试

借助 SQL 测试功能，我们可以快速确认刚刚填写的 SQL 语句是否能达到我们的目的。首先填写用于测试的 payload 等数据如下：

![image20190719113731130.png](https://static.emqx.net/images/522c9d849bea4eb8335dbdd9951bada0.png)

然后点击 **测试** 按钮，得到以下输出结果，与预期相符。

```json
{
  "humidity": 46.4,
  "location": "bedroom",
  "pm2_5": 0.5,
  "temperature": 25
}
```



### 添加响应动作，存储消息到 InfluxDB

SQL 条件输入输出无误后，我们继续添加响应动作，配置写入 SQL 语句，将筛选结果存储到 InfluxDB。

点击响应动作中的 **添加** 按钮，选择动作 **保存数据到 InfluxDB**，选取刚刚创建的 `InfluxDB` 资源，再按照实际需求将 `${fieldName}` 填写到 `Field Keys`, `Tag Keys` 和 `Timestamp Key` 中，`Measurement` 表示将数据写入 `InfluxDB` 时使用的 `Measurement`，最后点击 **新建** 按钮完成规则创建。

![image20190719115340429.png](https://static.emqx.net/images/0b5f6518dacde423e625b40a71179886.png)



## 测试

### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 客户端向 `data/sensor` 主题上报消息时，该消息将命中规则，规则列表中 **已命中** 数字将会增加 1；
2. InfluxDB 的 `db` 数据库中将会增加一条数据，数据内容与处理后的消息内容一致。



### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具** --> **Websocket** 页面，使用任意 Client ID 连接到 EMQX，连接成功后在 **消息** 卡片中发送如下消息：

- Topic：data/sensor

- Payload:

  ```json
  {
    "location": "bedroom",
    "data": {
      "temperature": 25,
      "humidity": 46.4,
      "pm2_5": 0.5
    }
  }
  ```

![image20190719133414535.png](https://static.emqx.net/images/8942e14397092ed1390362ae4e4c22d6.png)

点击 **发送** 按钮，发送成功后可以看到当前规则已命中次数已经变为 1。

然后检查 InfluxDB，新的 data point 是否添加成功：

```
$ docker exec -it influxdb influx

> use db
Using database db
> select * from "sensor_data"
name: sensor_data
time                humidity location pm2_5 temperature
----                -------- -------- ----- -----------
1561535778444457348 46.4     bedroom  0.5   25
```

至此，我们通过规则引擎实现了存储消息到 InfluxDB 数据库的业务开发。

在阅读该教程之前，假定你已经了解 [MQTT](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html)、[EMQX](https://github.com/emqx/emqx) 的简单知识。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
