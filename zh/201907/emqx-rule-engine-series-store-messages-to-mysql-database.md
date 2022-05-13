## 场景介绍

该场景需要将 EMQX 指定主题下且满足条件的消息存储到 MySQL 数据库。为了便于后续分析检索，消息内容需要进行拆分存储。

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

### 创建数据库

创建 `iot_data` 数据库以存储消息数据，这里指定数据库编码为 `utf8mb4` 避免编码问题：

```bash
CREATE DATABASE `emqx_rule_engine_output` CHARACTER SET utf8mb4;
```



### 创建数据表

根据场景需求，创建数据表 `use_statistics` 结构及字段注释如下：

```sql
CREATE TABLE `use_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` varchar(100) DEFAULT NULL COMMENT '客户端识别码',
  `speed` float unsigned DEFAULT '0.00' COMMENT '当前车速',
  `tachometer` int(11) unsigned DEFAULT '0' COMMENT '发动机转速',
  `ts` int(11) unsigned DEFAULT '0' COMMENT '上报时间戳',
  `msg_id` varchar(50) DEFAULT NULL COMMENT 'MQTT 消息 ID',
  PRIMARY KEY (`id`),
  KEY `client_id_index` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```



创建成功后通过 MySQL 命令确认数据表是否存在：

```bash
Database changed
mysql> desc use_statistics;
+------------+------------------+------+-----+---------+----------------+
| Field      | Type             | Null | Key | Default | Extra          |
+------------+------------------+------+-----+---------+----------------+
| id         | int(11)          | NO   | PRI | NULL    | auto_increment |
| client_id  | varchar(100)     | YES  | MUL | NULL    |                |
| speed      | float unsigned   | YES  |     | 0       |                |
| tachometer | int(11) unsigned | YES  |     | 0       |                |
| ts         | int(11) unsigned | YES  |     | 0       |                |
| msg_id     | varchar(50)      | YES  |     | NULL    |                |
+------------+------------------+------+-----+---------+----------------+
6 rows in set (0.01 sec)
```



## 配置说明

### 创建资源

打开 EMQX Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，键入 MySQL 服务器信息进行资源创建。

![image20190716172916980.jpg](https://assets.emqx.com/images/cd98bf6f25d37665ebe185e72fa516fa.jpg)



EMQX 集群中节点所在网络环境可能互不相同，资源创建成功后点击列表中 **状态按钮**，查看各个节点资源连接状况，如果节点上资源不可用，请检查配置是否正确、网络连通性，并点击 **重连** 按钮手动重连。


![image20190716173259015.png](https://assets.emqx.com/images/52d840cf263d3b8e40d634253aa56b64.png)

### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **消息发布**，在消息发布时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：
![image20190716174727991.png](https://assets.emqx.com/images/65d55ad7fc53b063facdb97f4dea97ff.png)



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
![image20190716184242159.png](https://assets.emqx.com/images/c8df91e4ab54452916db4f1a7a2e8eae.png)



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



### 添加响应动作，存储消息到 MySQL

SQL 条件输入输出无误后，我们继续添加相应动作，配置写入 SQL 语句，将筛选结果存储到 MySQL。

点击响应动作中的 **添加** 按钮，选择 **保存数据到 MySQL** 动作，选取刚刚选定的资源，我们使用 `${fieldName}` 语法填充 SQL 语句，将数据插入到数据库，最后点击 **新建** 按钮完成规则创建。

动作的 SQL 配置如下： 

```sql
INSERT INTO 
	`use_statistics` (`client_id`, `speed`, `tachometer`, `ts`, `msg_id`)
VALUES 
	(${client_id}, ${speed}, ${tachometer}, ${ts}, ${id});
```

![image20190716182818011.png](https://assets.emqx.com/images/0a5173b0fa9661873d762762c078de9b.png)



## 测试

#### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 设备向 `cmd/state/:id` 主题上报消息是，当消息中的 `tachometer` 数值超过 8000 时将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. MySQL `iot_data`数据库的 `use_statistics` 表中将增加一条数据，数值与当前消息一致。



#### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具** --> **Websocket** 页面，使用任意信息客户端连接到 EMQX，连接成功后在 **消息** 卡片发送如下信息：

- 主题：cmd/state/NXP-058659730253-963945118132721-22

- 消息体：

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22",
    "speed": 32.12,
    "direction": 198.33212,
    "tachometer": 9002,
    "dynamical": 8.93,
    "location": {
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202
  }
  ```


![image20190716190238252.png](https://assets.emqx.com/images/b415e426539eba3115a590e4533780da.png)



点击 **发送** 按钮，发送成功后查看规则统计 **已命中** 数据统计值为 1 表明规则已成功命中，MySQL 命令行中查看数据表记录得到数据如下：

![image20190717141918330.png](https://assets.emqx.com/images/2d0749d647809b89b2f1d2784ebc3475.png)

至此，我们通过规则引擎实现了使用规则引擎存储消息到 MySQL 数据库的业务开发。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
