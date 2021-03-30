## Cassandra 介绍与安装

Cassandra 是来自 Apache 的开源分布式数据库系统，它能在支持**线性扩展** 、 **高可用**的特性下，不损失原有的读写性能。目前广泛运用于各个大企业的后端服务中，例如 Netflix、Apple 等已部署上千个节点。



Cassandra 的安装参考：http://cassandra.apache.org/doc/latest/getting_started/installing.html



## 原理概览

通过配置规则引擎，EMQ X 可将指定主题下满足某条件的消息存储到 Cassandra 数据库。其消息流向简图如下：

![Artboard.png](https://static.emqx.net/images/f5edf360ac6d5bab6e364450d10a17c7.png)

其中：

- PUB/SUB：为 EMQ X 中的发布订阅处理逻辑。
- Rule：IoT 消息规则，提取、筛选、转换消息报文中的数据。
- Action: 为具体执行的动作。例如存数据库、写 Kafka 等。



## 场景介绍

为说明规则引擎在 Cassandra 数据库下的使用方式，我们以 `将发动机转速超过 8000 的车辆状态存入 Cassandra 中` 为例。

**假设车辆上报状态信息如下：**

- 上报主题：cmd/state/:id，主题中 id 代表车辆客户端识别码

- 消息体：

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22", // 客户端识别码
    "speed": 32.12, // 车辆速度
    "direction": 198.33212, // 行驶方向
    "tachometer": 3211, // 发动机转速，数值大于 8000 时才需存储
    "dynamical": 8.93, // 瞬时油耗
    "location": { // GPS 经纬度数据
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202 // 上报时间
  }
  ```



## 准备工作

### 创建数据库

创建 `emqx_rule_engine_output` 表空间以存储消息数据：

```bash
CREATE KEYSPACE emqx_rule_engine_output WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;
```



### 创建数据表

根据场景需求，创建数据表 `use_statistics` 结构及字段注释如下：

```sql
USE emqx_rule_engine_output;

CREATE TABLE use_statistics (
  msgid text,
  client_id text,
  speed double,
  tachometer int,
  ts int,
  PRIMARY KEY (msgid)
);
```



创建成功后确认数据表是否存在：

```bash
root@cqlsh:emqx_rule_engine_output> use emqx_rule_engine_output ;
root@cqlsh:emqx_rule_engine_output> desc use_statistics ;

CREATE TABLE emqx_rule_engine_output.use_statistics (
    msgid text PRIMARY KEY,
    client_id text,
    speed double,
    tachometer int,
    ts int
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
```



## 配置规则引擎



### 创建资源

打开 EMQ X Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，选择 Cassandra 资源类型进行创建：

![cassrescreate2x.png](https://static.emqx.net/images/7524eb9b668bd10c30d5d24ef773eb5a.png)



EMQ X 集群中节点所在网络环境可能互不相同，资源创建成功后点击列表中 **状态按钮**，查看各个节点资源连接状况，如果节点上资源不可用，请检查配置是否正确、网络连通性，并点击 **重连** 按钮手动重连。

![cassresstatus2x.png](https://static.emqx.net/images/9f56ce737134bd652d2dd93051f0796d.png)


### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **消息发布**，在消息发布时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![rulecondition2x.png](https://static.emqx.net/images/df2e101f3cf1524519745f01652dc099.png)



#### 筛选所需字段

规则引擎使用 SQL 语句处理规则条件，该业务中我们需要将 `payload` 中所有字段单独选择出来，使用 `payload.<fieldName>` 格式进行选择，还需要消息上下文的 `topic`、`qos`、`id` 信息，当前 SQL 如下：

```sql
SELECT
  payload.id as client_id, payload.speed as speed, 
  payload.tachometer as tachometer,
  payload.ts as ts, id
FROM
  "message.publish"
WHERE
  topic =~ 't/#'
```



#### 确立筛选条件

使用 SQL 语句 WHERE 字句进行条件筛选，该业务中我们需要定义两个条件：

- 仅处理 `cmd/state/:id` 主题，使用主题通配符 `=~` 对 `topic` 进行筛选：`topic =~ 'cmd/state/+'`
- 仅处理 `tachometer > 8000` 的消息，使用比较符对 `tachometer` 进行筛选：`payload.tachometer > 8000`

组合上一步骤得到 SQL 如下：

```sql
SELECT
  payload.id as client_id, payload.speed as speed, 
  payload.tachometer as tachometer,
  payload.ts as ts,
  id
FROM
  "message.publish"
WHERE
  topic =~ 'cmd/state/+'
  AND payload.tachometer > 8000
```



#### 使用 SQL 测试功能进行输出测试

借助 SQL 测试功能，我们可以实时查看当前 SQL 处理后的数据输出，该功能需要我们指定 payload 等模拟原始数据。

payload 数据如下，注意更改 `tachometer` 数值大小，以满足 SQL 条件：

```json
{
  "id": "NXP-058659730253-963945118132721-22",
  "speed": 32.12,
  "direction": 198.33212,
  "tachometer": 9001,
  "dynamical": 8.93,
  "location": {
    "lng": 116.296011,
    "lat": 40.005091
  },
  "ts": 1563268202
}
```



点击 **SQL 测试** 切换按钮，更改 `topic` 与 `payload` 为场景中的信息，点击 **测试** 按钮查看数据输出：

![rulesqltest2x.png](https://static.emqx.net/images/eea3ebd809866d6ad84c8ab53da01e29.png)



测试输出数据为：

```json
{
  "client_id": "NXP-058659730253-963945118132721-22",
  "id": "589A429E9572FB44B0000057C0001",
  "speed": 32.12,
  "tachometer": 9001,
  "ts": 1563268202
}
```

测试输出与预期相符，我们可以进行后续步骤。



### 添加响应动作，存储消息到 Cassandra

SQL 条件输入输出无误后，我们继续添加相应动作，配置写入 SQL 语句，将筛选结果存储到 Cassandra。

点击响应动作中的 **添加** 按钮，选择 **保存数据到 Cassandra** 动作，选取刚刚选定的资源，我们使用 `${fieldName}` 语法填充 SQL 语句，将数据插入到数据库，最后点击 **新建** 按钮完成规则创建。

动作的 SQL 配置如下： 

```sql
INSERT INTO use_statistics (msgid, client_id, speed, tachometer, ts) VALUES (${id}, ${client_id}, ${speed}, ${tachometer}, ${ts});
```


![cassrulecreate2x.png](https://static.emqx.net/images/d1745cdd45ee2cb9d30e79ed671995a2.png)



## 测试

#### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 设备向 `cmd/state/:id` 主题上报消息，当消息中的 `tachometer` 数值超过 8000 时将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. Cassandra `emqx_rule_engine_output` 数据库的 `use_statistics` 表中将增加一条数据，数值与当前消息一致。



#### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具 => Websocket** 页面，使用任意信息客户端连接到 EMQ X，连接成功后在 **消息** 卡片发送如下信息：

- 主题：cmd/state/NXP-058659730253-963945118132721-22

- 消息体：

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22",
    "speed": 32.12,
    "direction": 198.33212,
    "tachometer": 8081,
    "dynamical": 8.93,
    "location": {
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202
  }
  ```



![websocket2x.png](https://static.emqx.net/images/da3340a1ee6f88b0ada1560fd4ed8f53.png)



点击 **发送** 按钮，此时消息体中的 `tachometer` 数值，满足上面设置的 `tachometer > 8000` 的条件，当前规则已命中统计值为加 1。

Cassandra 命令行中查看数据表记录得到数据如下：
![cassruleresult2x.png](https://static.emqx.net/images/2e1437c76b8f8151167b530d740fb8c3.png)

至此，我们通过规则引擎实现了使用规则引擎存储消息到 Cassandra 数据库的业务开发。


