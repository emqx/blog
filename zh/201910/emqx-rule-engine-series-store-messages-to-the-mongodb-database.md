## MongoDB 介绍

> 非关系数据库（NoSQL） 用于超大规模数据的存储，例如谷歌或 Facebook 每天为他们的用户收集万亿比特的数据。这些类型的数据存储不需要固定的模式，无需多余操作就可以横向扩展。

MongoDB 是一个介于关系数据库和非关系数据库之间的产品，是非关系数据库当中功能最丰富，最像关系数据库的。MongoDB 由 C++ 语言编写的，是一个基于分布式文件存储的开源数据库系统，MongoDB 旨在为数据存储提供可扩展的高性能数据存储解决方案，在高负载的情况下，可以轻松添加更多的节点保证服务性能。

MongoDB 将数据存储为一个文档，数据结构由键值 (key=>value) 对组成。MongoDB 文档类似于 JSON 对象。字段值可以包含其他文档，数组及文档数组。

MongoDB 下载地址：[https://www.mongodb.com/download-center/community](https://www.mongodb.com/download-center/community)



## 场景介绍

该场景需要将 EMQX 指定主题下满足某条件的消息存储到 MongoDB 数据库。为了便于后续分析检索，消息内容需要进行拆分存储。

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

### 创建管理用户

先使用具有创建用户的权限的账号登录 MongoDB，并为 `emqx_rule_engine_output` 添加用户：

```bash
> use emqx_rule_engine_output;

> db.createUser({user: "root", pwd: "public", roles: [{role: "readWrite", db: "emqx_rule_engine_output"}]});
```



### 创建数据表

使用新的用户登入，并创建数据集 `use_statistics`：

```sql
$ mongo 127.0.0.1/emqx_rule_engine_output -uroot -ppublic

> db.createCollection("use_statistics"); 
```



创建成功后确认数据表是否存在：

```bash
> show collections
use_statistics
```



## 配置说明

### 创建资源

打开 EMQX Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，选择 MongoDB 资源类型进行创建：

![mongrescreate2x.png](https://assets.emqx.com/images/44e47b97da67afc70e94cce2ba0da18f.png)



EMQX 集群中节点所在网络环境可能互不相同，资源创建成功后点击列表中 **状态按钮**，查看各个节点资源连接状况，如果节点上资源不可用，请检查配置是否正确、网络连通性，并点击 **重连** 按钮手动重连。

![mongresstatus2x.png](https://assets.emqx.com/images/ad6f6bca0c772445a750129c33561940.png)



### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **消息发布**，在消息发布时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![rulecondition2x.png](https://assets.emqx.com/images/3461003be069ad636be34c8066aba5a4.png)



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

![rulesqltest2x.png](https://assets.emqx.com/images/6e115960b2cef28d67243a3131e0f37b.png)



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



### 添加响应动作，存储消息到 MongoDB

SQL 条件输入输出无误后，我们继续添加响应动作，配置写入 SQL 语句，将筛选结果存储到 MongoDB。

点击响应动作中的 **添加** 按钮，选择 **保存数据到 MongoDB** 动作，选取刚刚选定的资源，我们使用 `${fieldName}` 语法填充操作语句，将数据插入到数据库，最后点击 **新建** 按钮完成规则创建。

**Collection** 配置为: `use_statistics`

**Selector** 配置为： 

```sql
msgid=${id}, client_id=${client_id}, speed=${speed}, tachometer=${tachometer}, ts=${ts}
```


![mongrulecreate2x.png](https://assets.emqx.com/images/426a140fe43174a116b8b0af95d2e6c3.png)



## 测试

#### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 设备向 `cmd/state/:id` 主题上报消息时，当消息中的 `tachometer` 数值超过 8000 时将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. MongoDB `emqx_rule_engine_output` 数据库的 `use_statistics` 表中将增加一条数据，数值与当前消息一致。



#### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具 => Websocket** 页面，使用任意信息客户端连接到 EMQX，连接成功后在 **消息** 卡片发送如下信息：

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


![websocket2x.jpg](https://assets.emqx.com/images/8748f93fcbc839bc87f1099563fdfb80.jpg)


点击 **发送** 按钮，此时消息体中的 `tachometer` 数值，满足上面设置的 `tachometer > 8000` 的条件，当前规则已命中统计值为加 1。

MongoDB 命令行中查看数据表记录得到数据如下：

![mongruleresult2x.png](https://assets.emqx.com/images/cc3b8eb17bcb604f8318df8fd8113e3b.png)

至此，我们通过规则引擎实现了使用规则引擎存储消息到 MongoDB 数据库的业务开发。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
