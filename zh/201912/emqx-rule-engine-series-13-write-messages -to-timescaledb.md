## TimescaleDB 介绍

面对大规模快速增长的物联网传感器采集、交易记录等数据，时间序列数据累计速度非常快，时序数据库通过提高效率来处理这种大规模数据，并带来性能的提升，包括：更高的容纳率（Ingest Rates）、更快的大规模查询（尽管有一些比其他数据库支持更多的查询）以及更好的数据压缩。

TimescaleDB 是一款针对快速获取和复杂查询而优化的开源时间序列数据库。 它使用标准的 SQL 语句，并且像传统的关系数据库那样容易使用，像 NoSQL 那样可扩展。

TimescaleDB是在 PostgreSQL 数据库的基础上进行开发的，所以使用方法基本和传统数据库一致。它可以支持复杂的SQL查询，并针对时间序列数据的快速插入和复杂查询、持久存储进行了优化，特别适合用于监控，IoT，金融，物流等大数据领域。

## 场景介绍

该场景需要将 EMQX 指定主题下且满足条件的消息存储到 TimescaleDB。为了便于后续分析检索，消息内容需要进行拆分存储。

**该场景下客户端上报数据如下：**

- Topic：data/sensor

- Payload:

  ```json
  {
    "location": "bedroom",
    "temperature": 25,
    "humidity": 46.4
  }
  ```



## 准备工作

### 创建数据库

创建 tutorial 数据库，用户名为 postgres，密码为 password：

```shell
$ docker pull timescale/timescaledb

$ docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg11

$ docker exec -it timescaledb psql -U postgres

## 创建并连接 tutorial 数据库
> CREATE database tutorial;

> \c tutorial

## 使用 TimescaleDB 扩展数据库
> CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
```



### 创建数据表

创建 sensor_data 表并转换为 hypertable：

```sql
> CREATE TABLE sensor_data (
  time        TIMESTAMPTZ       NOT NULL,
  location    TEXT              NOT NULL,
  temperature DOUBLE PRECISION  NULL,
  humidity    DOUBLE PRECISION  NULL
);

> SELECT create_hypertable('sensor_data', 'time');
```



## 配置说明

### 创建资源

打开 EMQX Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，选择 TimescaleDB 资源类型并完成相关配置进行资源创建。

![image20190725121129697.png](https://static.emqx.net/images/f5a03d8bd27e4c8f8350a9488c4fee56.png)



### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **message.publish**，即在 EMQX 收到 PUBLISH 消息时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![image20190719112141128.png](https://static.emqx.net/images/5430aa165efedc4e10ab57aaf2d04762.png)



#### 筛选所需字段

规则引擎使用 SQL 语句过滤和处理数据。例如前文提到的场景中我们需要将 ``payload`` 中的字段提取出来使用，则可以通过 `payload.<fieldName>` 实现。同时我们仅仅期望处理 `data/sensor` 主题，那么可以在 WHERE 子句中使用主题通配符 `=~` 对 `topic` 进行筛选：`topic =~ 'data/sensor'`， 最终我们得到 SQL 如下：

```sql
SELECT
  payload.temperature as temperature,
  payload.humidity as humidity,
  payload.location as location
FROM
  "message.publish"
WHERE
  topic =~ 'data/sensor'
```



#### SQL 测试

借助 SQL 测试功能，我们可以快速确认刚刚填写的 SQL 语句能否达成我们的目的。首先填写用于测试的 payload 等数据如下：

![image20190725133827927.png](https://static.emqx.net/images/dcada3c8dac0a0fec9bb57888d9d972f.png)

然后点击 **测试** 按钮，我们得到以下数据输出：

```json
{
  "humidity": 46.4,
  "location": "bedroom",
  "temperature": 25
}
```

测试输出与预期相符，我们可以进行后续步骤。



### 添加响应动作，存储消息到 Timescale

SQL 条件输入输出无误后，我们继续添加响应动作，配置写入 SQL 语句，将筛选结果存储到 Timescale。

点击响应动作中的 **添加** 按钮，选择 **保存数据到 Timescale** 动作，选取刚刚创建的 `Timescale` 资源并填写 SQL 模板如下：

`insert into sensor_data(time, location, temperature, humidity) values (NOW(), ${location}, ${temperature}, ${humidity})`

最后点击 **新建** 按钮完成规则创建。

![image20190725134423471.png](https://static.emqx.net/images/1bcf17542a85a02b7506c2d3e20e7669.png)



## 测试

### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 客户端向 `data/sensor` 主题上报消息时，该消息将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. Timescale `tutorial` 数据库的 `sensor_data` 表中将增加一条数据，数据内容与消息内容一致。



### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具** --> **Websocket** 页面，使用任意信息客户端连接到 EMQX，连接成功后在 **消息** 卡片中发送如下消息：

- Topic：data/sensor

- Payload:

  ```json
  {
    "location": "bedroom",
    "temperature": 25,
    "humidity": 46.4
  }
  ```
![image20190725134813146.png](https://static.emqx.net/images/b3df2a5a3705e887c0e22b5b2974ceb6.png)

点击 **发送** 按钮，发送成功后可以看到当前规则已命中次数已经变为了 1。

然后检查 TimescaleDB，新的 data point 是否添加成功：

```
tutorial=# SELECT * FROM sensor_data LIMIT 100;
             time              | location | temperature | humidity 
-------------------------------+----------+-------------+----------
 2019-07-25 05:47:27.124415+00 | bedroom  |          25 |     46.4
(1 row)

```

至此，我们通过规则引擎实现了使用规则引擎存储消息到 Timescale 数据库的业务开发。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
