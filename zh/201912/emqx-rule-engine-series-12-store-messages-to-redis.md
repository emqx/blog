## Redis 介绍

Redis 是完全开源免费遵守 BSD 协议的高性能 key-value 数据库。

相比其他 key-value 缓存产品 Redis 有以下特点：

- Redis 性能极高，单机支持十万级别的读写速度。
- Redis 支持数据的持久化，可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用。
- Redis 不仅仅支持简单的 key-value 类型的数据，同时还提供 list，set，zset，hash 等数据结构的存储。
- Redis 支持数据的备份，即 master-slave 模式的数据备份。

读者可以参考 Redis 官方的 Quick Start (https://redis.io/topics/quickstart) 来安装 Redis（写本文的时候，Redis 版本为5.0），通过 redis-server 命令来启动 Redis 服务器。

## 场景介绍

该场景需要将 EMQ X 指定主题下且满足条件的消息存储到 Reids。为了便于后续分析检索，消息内容需要进行拆分存储。

**该场景下设备端上报信息如下：**

- 上报主题：`cmd/state/:id`，主题中 id 代表车辆客户端识别码

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

## 配置说明

### 创建资源

打开 EMQ X Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，键入 Redis 服务器信息进行资源创建。

![1.png](https://static.emqx.net/images/d570071aae47948a56347d1ed5974ed9.png)



EMQ X 集群中节点所在网络环境可能互不相同，资源创建成功后点击列表中 **状态按钮**，查看各个节点资源连接状况，如果节点上资源不可用，请检查配置是否正确、网络连通性，并点击 **重连** 按钮手动重连。

![WX201907181032132x.png](https://static.emqx.net/images/c0bf4e9651c4913966747c83f0dc6697.png)



### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **消息发布**，在消息发布时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![image20190716174727991.png](https://static.emqx.net/images/f6c0de2b38aa8f8ccc226c346a2d26a8.png)



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

![SQL1.png](https://static.emqx.net/images/a0a2c5c426db172d11963cc6b48b4db6.png)



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



### 添加响应动作，存储消息到 Redis

SQL 条件输入输出无误后，我们继续添加相应动作，配置写入 SQL 语句，将筛选结果存储到 Redis。

点击响应动作中的 **添加** 按钮，选择 **保存数据到 Redis** 动作，选取刚刚选定的资源，我们使用 `${fieldName}` 语法填充 SQL 语句，将数据插入到数据库，最后点击 **新建** 按钮完成规则创建。

动作的 SQL 配置如下： 

```sql
HMSET test client_id "${client_id}" speed "${speed}" tachometer "${tachometer}" ts "${ts}" msg_id "${msg_id}"
```

使用 Redis 的哈希表结构，以 message id 为表明创建哈希表

![WX201907181049302x.png](https://static.emqx.net/images/ffbfc8caf7e355047bb306debcf80732.png)



## 测试

#### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 设备向 `cmd/state/:id` 主题上报消息时，当消息中的 `tachometer` 数值超过 8000 时将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. Redis 将增加一个以当前 message id 命名的哈希表，数值与当前消息一致。



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


![image20190716190238252.png](https://static.emqx.net/images/7c5636c4638f97bc9842f0fd577b2aa6.png)



点击 **发送** 按钮，查看得到当前规则已命中统计值为 1。

Redis 命令行中查看哈希表记录得到数据如下：

![WX201907181142402x.png](https://static.emqx.net/images/45ccb0d06301d333abda2adca6186be6.png)

至此，我们通过规则引擎实现了使用规则引擎存储消息到 Reids的业务开发。




