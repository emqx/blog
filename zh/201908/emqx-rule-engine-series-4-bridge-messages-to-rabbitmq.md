## 场景介绍

该场景需要将 EMQX 指定主题下且满足条件的消息存储到 RabbitMQ。

RabbitMQ 是一个由 Erlang 开发的 AMQP 消息中间件的开源实现，主要用于组件之间的解耦，消息的发送者无需知道消息使用者的存在，反之亦然。RabbitMQ 用于在分布式系统中存储转发消息，在易用性、吞吐量、扩展性、高可用性等方面表现不俗。EMQX 百万级消息吞吐的场景下，RabbitMQ 是最佳的持久化/桥接方案之一。

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

RabbitMQ 的本地安装详见 [下载和安装RabbitMQ](https://www.rabbitmq.com/download.html) 教程，开发使用推荐下载独立二进制包，解压后进入软件目录通过命令行启动 rabbitmq-server:

```bash
./sbin/rabbitmq-server
```



## 配置说明

### 创建资源

打开 EMQX Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，键入 RabbitMQ 服务器信息进行资源创建。

![image01.png](https://static.emqx.net/images/c4e1ebdc3c256d3a3e0c812c5e23fce5.png)


EMQX 集群中节点所在网络环境可能互不相通，资源创建成功后点击列表中 **状态按钮**，查看各个节点资源连接状况，如果节点上资源不可用，请检查配置是否正确、网络连通性，并点击 **重连** 按钮手动重连。

![image02.png](https://static.emqx.net/images/78f57557431885fb1082fee5b86a9e35.png)


### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **消息发布**，在消息发布时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![image03.png](https://static.emqx.net/images/dafa015734e66b8ed2aba2806140d90c.png)


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

![image04.png](https://static.emqx.net/images/b50e78510458782bae0a67fc335a2638.png)


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

### 添加响应动作，桥接消息到 RabbitMQ

SQL 条件输入输出无误后，我们继续添加响应动作，配置写相关参数，将筛选结果存储到 RabbitMQ。

点击响应动作中的 **添加** 按钮，选择 **桥接数据到 RabbitMQ** 动作，选取刚刚选定的资源，填充

RabbitMQ Exchange，Exchange Type 以及 Routing Key。

![image05.png](https://static.emqx.net/images/3d8fea8a2549b38e92a5d7e12e73dc6f.png)

## 测试

#### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 设备向 `cmd/state/:id` 主题上报消息时，当消息中的 `tachometer` 数值超过 8000 时将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. RabbitMQ 的订阅者将收到一条数据，数值与当前消息一致。


#### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具** --> **Websocket** 页面，使用任意信息客户端连接到 EMQX，连接成功后在 **消息** 卡片发送如下信息：

- 主题：cmd/state/NXP-058659730253-963945118132721-22

- 消息体：

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

![image06.png](https://static.emqx.net/images/1313100c9a4f4c57e5955802e3236483.png)

点击**发送**按钮，发送成功后查看得到当前规则已命中统计值为 1。

使用命令行中查看数据表记录得到数据如下：

![image07.png](https://static.emqx.net/images/236ff1abc0759a361a8eac6bc0aa358c.png)

至此，我们通过规则引擎实现了使用规则引擎桥接消息到 RabbitMQ 的业务开发。
