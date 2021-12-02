## Pulsar 消息系统介绍

Apache Pulsar 是一个企业级的发布订阅（pub-sub）消息系统，Pulsar 旨在取代 Apache Kafka 多年的主宰地位。Pulsar 在很多情况下提供了比 Kafka 更快的吞吐量和更低的延迟，并为开发人员提供了一组兼容的 API。

Pulsar 将高性能的流和灵活的传统队列结合到一个统一的消息模型和 API 中，实现流处理与队列处理同步进行。

Pulsar 的安装与使用详见 [Pulsar 官网](https://pulsar.apache.org/) ，更多 Pulsar 介绍信息与桥接方案对比详见：[比拼 Kafka, 大数据分析新秀 Pulsar 到底好在哪](https://www.infoq.cn/article/1UaxFKWUhUKTY1t_5gPq)

## 场景介绍

该场景需要将 EMQ X 指定主题下且满足条件的消息桥接到 Pulsar 。为了便于后续分析检索，消息内容需要进行拆分。

**该场景下设备端上报信息如下：**

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

当上报数据发动机转速数值大于 `8000` 时，存储当前信息以便后续分析用户车辆使用情况。

## 准备工作

### 创建Pulsar主题

创建 `emqx_rule_engine_output` 主题：

```bash
./bin/pulsar-admin topics create-partitioned-topic -p 5 emqx_rule_engine_output
```

## 配置说明

### 创建资源

打开 EMQ X Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，键入 Pulsar 服务器信息进行资源创建。

![WX201907181431432x.png](https://static.emqx.net/images/8142d07b9a280b165e419b86853cb87c.png)


EMQ X 集群中节点所在网络环境可能互不相同，资源创建成功后点击列表中 **状态按钮**，查看各个节点资源连接状况，如果节点上资源不可用，请检查配置是否正确、网络连通性，并点击 **重连** 按钮手动重连。


![WX201907181432172x.png](https://static.emqx.net/images/0c6716fe98fc6edf3afc9acb69f34744.png)


### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **消息发布**，在消息发布时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![image20190716174727991.png](https://static.emqx.net/images/12c90b41c8648f1ad459baae912967a2.png)



#### 筛选所需字段

规则引擎使用 SQL 语句处理规则条件，该业务中我们需要将 `payload` 中所有字段单独选择出来，使用 `payload.fieldName` 格式进行选择，还需要消息上下文的 `topic`、`qos`、`id` 信息，当前 SQL 如下：

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

![image20190716184242159.png](https://static.emqx.net/images/1de031784a9bbb8da4baf7834e488ad5.png)


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



### 添加响应动作，桥接消息到 Pulsar

SQL 条件输入输出无误后，我们继续添加相应动作，配置写入 SQL 语句，将筛选结果桥接到 Pulsar。

点击响应动作中的 **添加** 按钮，选择 **桥接数据到Pulsar** 动作，选取刚刚选定的资源，Pulsar 主题填写上文创建的`emqx_rule_engine_output`

![WX201907181433432x.png](https://static.emqx.net/images/a621dc2bd38c9de77cccab730f2081b4.png)



## 测试

#### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 设备向 `cmd/state/:id` 主题上报消息时，当消息中的 `tachometer` 数值超过 8000 时将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. Pulsar 的 `emqx_rule_engine_output` 主题 将增加一条消息，数值与当前消息一致。

#### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具** --> **Websocket** 页面，使用任意信息客户端连接到 EMQ X，连接成功后在 **消息** 卡片发送如下信息：

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


![image20190716190238252.png](https://static.emqx.net/images/8c7ad5216d93fe1fdae6731a61bf3f94.png)



点击 **发送** 按钮，查看得到当前规则已命中统计值为 1。

然后通过 Pulsar 命令去查看消息是否生产成功:

```
./bin/pulsar-client consume emqx_rule_engine_output -s "sub-name" -n 1000
----- got message -----
{"client_id":"NXP-058659730253-963945118132721-22","id":"58DEEDE7CF3D4F440000019CA0003","speed":32.12,"tachometer":8081,"ts":1563268202}
```

至此，我们通过规则引擎实现了使用规则引擎桥接消息到 Pulsar 的业务开发。
