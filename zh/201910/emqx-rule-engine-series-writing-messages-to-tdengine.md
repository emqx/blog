## TDEngine 是什么

TDengine 是涛思数据（北京涛思数据科技有限公司）推出的一款开源的专为物联网、车联网、工业互联网、IT 运维等设计和优化的大数据平台。除核心的快 10 倍以上的时序数据库功能外，还提供缓存、数据订阅、流式计算等功能，最大程度减少研发和运维的复杂度。

TDengine 作为时序处理引擎，可以完全不用 Kafka、HDFS/HBase/Spark、Redis 等软件，大幅简化大数据平台的设计，降低研发成本和运营成本。因为需要集成的开源组件少，因而系统可以更加健壮，也更容易保证数据的一致性。

TDEngine 提供社区版、企业版和云服务版，安装/使用教程详见 TDEngine 使用文档 https://www.taosdata.com/cn/products/



## 场景介绍

本文以通过 MQTT 协议接入 EMQX 的智能门锁为例进行说明。

智能门锁已经成为了[智能家居](https://www.emqx.com/zh/blog/tag/%E6%99%BA%E8%83%BD%E5%AE%B6%E5%B1%85)的重点关注产品，为了保证用户更安全的开锁体验，智能门锁通常可以实现指纹开锁、密码开锁、IC卡开锁、钥匙开锁、远程开锁等功能。智能门锁每个业务环节都涉及到操作敏感指令和状态数据的发送、传输，这些数据在应当存储起来以备后续审计使用。

### 采集流程

智能门锁下发指令与上报数据通过 MQTT 协议经 EMQX 传输，可选在 EMQX 上使用规则引擎筛选或设置消费客户端处理，将满足条件的数据写入 TDEngine 数据平台，整个数据流转流程如下：



![1.png](https://assets.emqx.com/images/6c81643568e7740ccf7104d7698e3f26.png)



该场景中拟设智能门锁通过 `lock/:id/control_receipt` 主题( id 为门锁连接客户端的 clientid，同门锁 id) 上报操作回执与状态信息，数据格式为如下 JSON 消息：

```json
{
  "id": "51dc0c50f55d11e9a4fec59e26b058d5", // 门锁 id
  "longitude": 102.8622543, // 当前位置经度
  "latitude": 24.8614503, // 当前位置纬度
  "command": "unlock", // 指令
  "LockState": 0, // 门锁状态
  "LockType": 0, // 开锁方式
  "KeyNickName": "", // 钥匙昵称
  "KeyID": "c944c8d0f55e11e9a4fec59e26b058d5", // 钥匙 ID
  "ErrorCode": 0, // 执行故障代码
  "pid": "84a2e10f55d11e9a4fec59e26b058d5", // 下发的指令 ID
  "alarm": "", // 当前告警信息
  "ts": 1570838400000 // 执行时间
}
```



## 准备

尽管 TDEngine 是关系型数据库模型，但要求每个采集设备单独建表，因此我们按照门锁 id 每个门锁建表一张，同时浮点数据压缩比相对整型数据压缩比很差，经度纬度通常精确到小数点后 7 位，**因此将经度纬度增大 1E7 倍转为长整型存储**：

创建数据库的语句为：

```sql
create database db cache 8192 ablocks 2 tblocks 1000 tables 10000;
use db;
```

创建超级表的SQL语句为：

```sql
create table lock(
  ts timestamp,
  id nchar(50),
  pid nchar(50),
  longitude bigint,
  latitude bigint,
  command nchar(50),
  LockState smallint,
  LockType smallint,
  KeyNickName nchar(255),
  KeyID nchar(255),
  ErrorCode smallint,
  alarm nchar(255)
) tags(card int, model binary(10));
```

**TDEngine 是关系型数据库模型，但要求每个采集设备单独建表**，以门锁 id 作为采集表表名，例如 id 为 51dc0c50f55d11e9a4fec59e26b058d5，那么创建数据表的语句为：

```sql
-- 使用 using 指定其所属 超级表
create table "v_51dc0c50f55d11e9a4fec59e26b058d5" using lock tags('51dc0c50f55d11e9a4fec59e26b058d5', 0);
```

在该数据模型下，以门锁 id 51dc0c50f55d11e9a4fec59e26b058d5 为例，写入一条记录到表 v_51dc0c50f55d11e9a4fec59e26b058d5 的 SQL 语句为：

```sql
insert into v_51dc0c50f55d11e9a4fec59e26b058d5 values(
  1570838400000,
  '51dc0c50f55d11e9a4fec59e26b058d5',
  'e84a2e10f55d11e9a4fec59e26b058d5',
  1028622543,
  248614503,
  'unlock',
  0,
  0,
  '',
  'c944c8d0f55e11e9a4fec59e26b058d5',
  0,
  '[]',
);
```

> 实际使用中请先依次给每个智能门锁建表



## 数据写入方式

目前 EMQX 消息数据直接写入 TDEngine 的功能还在规划中，但得益于 TDEngine 提供了诸多连接器，我们选用以下两种方式完成数据写入：

- 使用 TDEngine 的 [RESTful Connector](https://www.taosdata.com/cn/documentation/connector/#RESTful-Connector)：通过 REST API 调用，将数据拼接为 SQL 语句发送到 TDEngine 执行写入，规则引擎内置表达式与函数可以预处理数据；
- 通过 TDEngine 提供的客户端库/连接器，编写代码通过订阅/消费的方式获取 EMQX 消息，处理后转发写入到 TDEngine 中。



## 使用规则引擎写入数据

### 资源准备

EMQX Dashboard 中点击 **规则** 主菜单，在 **资源** 页面新建一个 WebHook 资源，用于向 TDEngine RESTful Connector 发送数据，新增请求头：

- Authorization：值为 TDEngine 请求 TOKEN 用于连接认证，为 `{username}:{password}` 经过 Base64 编码之后的字符串。

有关 RESTful Connector 使用教程详见：[TDEngine RESTful Connector](https://www.taosdata.com/cn/documentation/connector/#RESTful-Connector)


![2.png](https://assets.emqx.com/images/1b25136d72e0be66b69d12c97187a3b3.png)

点击 **测试连接**，测试通过后点击 **确定** 按钮完成创建。



### 创建规则

资源创建完毕后我们可以进行规则创建，**规则引擎** --> **规则** 页面中点击 **新建** 按钮进入规则创建页面。

选择 **消息发布** 事件，处理传感器消息上报(发布)时的数据。根据 **可用字段** 提示，传感器等信息可以从 `payload` 中选取。

由于需要将浮点值处理为整型，我们使用简单计算功能，请留意 SQL 中的注释项，最终整个 SQL 语句如下：

```sql
SELECT
  -- JSON 数据解码
  json_decode(payload) as p,
  -- 经纬度放大 10E7 倍存储
  p.longitude * 10000000 as p.longitude,
  p.latitude * 10000000 as p.latitude
FROM
  "message.publish"
WHERE
  -- 通过 topic 筛选数据源
  topic =~ 'lock/+/control_receipt' 
```


![3.png](https://assets.emqx.com/images/f229f71dd099286311209c2f6d2e08bf.png)



使用 SQL 测试功能，输入原始上报数据与相关变量，得到如下输出结果：

```json
{
  "p": {
    "ErrorCode": 0,
    "KeyID": "c944c8d0f55e11e9a4fec59e26b058d5",
    "KeyNickName": "",
    "LockState": 0,
    "LockType": 0,
    "alarm": "",
    "command": "unlock",
    "id": "51dc0c50f55d11e9a4fec59e26b058d5",
    "latitude": 248614503,
    "longitude": 1028622543,
    "pid": "84a2e10f55d11e9a4fec59e26b058d5",
    "ts": 1570838400000
  }
}
```

从输出结果看，经纬度浮点值已经转为整型，说明该步操作正确，可以进行后续操作。



### 响应动作

点击创建页面下方 **添加动作** 按钮，在弹出的 **新增动作** 弹框里动作类型选择 **发送数据到 Web 服务**，**使用资源** 选择上一步中创建的资源，**消息内容模板** 内容模板里面，使用 `${}` 语法提取 **条件 SQL** 筛选出来的数据，拼接写入 SQL 语句如下：

```sql
insert into db.v_${p.id} values(
  ${p.ts},
  '${p.id}',
  '${p.pid}',
  ${p.longitude},
  ${p.latitude},
  '${p.command}',
  ${p.LockState},
  ${p.LockType},
  '${p.KeyNickName}',
  '${p.KeyID}',
  ${p.ErrorCode},
  '${p.alarm}',
);
```



点击 **创建** 完成规则的创建，智能门锁上报数据时数据将写入到 DBEngine，整个工作和业务流程如下：

- 智能门锁上报数据至 EMQX
- `message.publish` 事件触发规则引擎 ，开始按照条件 SQL 中的 `where`  条件匹配 `topic` 和 `payload` 数据字段
- 规则命中后触发响应动作列表，按照响应动作中的消息内容模板拼接出该动作所需请求参数，在这个规则中请求参数是一个 SQL 语句，包含有智能门锁的上报数据信息
- 按照动作类型和使用的资源发起请求， 调用 RESTful API 将指令发送到 TDEngine 执行，完成数据写入。





## 使用 TDEngine SDK 写入数据

TDEngine 提供多种语言平台适用的 SDK，程序可以通过订阅 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)或消费消息中间件数据获取智能门锁上报到 EMQX 的数据，随后将数据拼接成写入 SQL 最终写入到 TDEngine 中。

本文使用订阅 MQTT 主题的方式获取智能门锁上报数据。考虑到消息量可能增长到单个订阅客户端无法承受的数据量，我们使用 **共享订阅** 的方式来消费数据。

> 在共享订阅中，订阅同一个主题的客户端会轮流的收到这个主题下的消息，也就是说同一个消息不会发送到多个订阅者，从而实现订阅端的多个节点之间的负载均衡。



### 代码示例

该示例使用 Node.js 平台，借助 TDEngine 的 RESTful Connector 实现数据写入操作。

使用方式：安装 Node.js、安装 npm、安装依赖、修改相应参数并运行执行

```js
// index.js
const mqtt = require("mqtt");
const axios = require("axios");

/**
 * 通过 RESTful Connector 执行 TDEngine 操作
 * @param {string} 需要执行的 sql
 */
function exec(sql = "") {
  return axios({
    method: "post",
    url: "http://127.0.0.1:6020/rest/sql",
    auth: {
      username: "root",
      password: "taosdata"
    },
    data: sql
  });
}

// MQTT 处理订阅消息回调
async function handleMessage(topic, message) {
  try {
    // JSON 转对象
    const p = JSON.parse(message.toString());
    // 处理浮点数据
    p.longitude = p.longitude * 10e7;
    p.latitude = p.latitude * 10e7;
    const resp = await exec(`
      INSERT INTO db.v_${p.id} values(
        ${p.ts},
        '${p.id}',
        '${p.pid}',
        ${p.longitude},
        ${p.latitude},
        '${p.command}',
        ${p.LockState},
        ${p.LockType},
        '${p.KeyNickName}',
        '${p.KeyID}',
        ${p.ErrorCode},
        '${p.alarm}',
      );`);
    console.log(`Exec success:`, resp.data);
  } catch (e) {
    console.log(
      "exec insert error:",
      e.message,
      e.response ? e.response.data : ""
    );
  }
}

function createConsumer(config = {}) {
  const client = mqtt.connect("mqtt://127.0.0.1:1883", config);

  client.on("connect", () => {
    // 使用共享订阅 $share/ 前缀
    client.subscribe("$share//lock/+/control_receipt", (err, granded = []) => {
      if (!err && granded[0].qos <= 2) {
        console.log("Consumer client ready");
      }
    });
  });

  client.on("message", handleMessage);
}

// 创建 10 个共享订阅消费者
for (let i = 0; i < 10; i++) {
  createConsumer();
}

```



## 测试

通过 EMQX Dashboard 内置的 MQTT 客户端（WebSocket）可以快速模拟测试规则可用性。打开 **工具 -> WebSocket** 页面，输入按照智能门锁连接信息建立连接，在 **发布** 功能里面输入上报主题、上报数据点击发布进行模拟测试：

- 发布主题：`lock/${id}/control_receipt`

- Payload：

  ```json
    {
      "id": "51dc0c50f55d11e9a4fec59e26b058d5",
      "longitude": 102.8622543,
      "latitude": 24.8614503,
      "command": "unlock",
      "LockState": 0,
      "LockType": 0,
      "KeyNickName": "", 
      "KeyID": "c944c8d0f55e11e9a4fec59e26b058d5",
      "ErrorCode": 0,
      "pid": "84a2e10f55d11e9a4fec59e26b058d5",
      "alarm": "",
      "ts": 1570838400000
    }
  ```

  


![4.png](https://assets.emqx.com/images/3a6f185ee995d4b0746b0a6d3843f1a8.png)

发布多次，在 **规则引擎** 列表里，点击 **监控** 图标可以快速查看当前规则执行数据，由下图可见 4 条消息命中 3 次，成功 3 次：


![5.png](https://assets.emqx.com/images/06b823bf6fbcb2397a041ee174c8ce75.png)

在 TDEngine 控制台查看 `db.v_51dc0c50f55d11e9a4fec59e26b058d5` 中的数据，此时有 3 条数据:

```sql
use db;
select count(*) from v_51dc0c50f55d11e9a4fec59e26b058d5;

taos> select count(*) from v_51dc0c50f55d11e9a4fec59e26b058d5;
      count(*)       |
======================
                    3|
Query OK, 1 row(s) in set (0.000612s)
```



删除该条规则，启动 TDEngine SDK 写入代码，重复该上述测试操作，可以看到程序打印日志如下：

```bash
{ status: 'succ', head: [ 'affected_rows' ], data: [ [ 1 ] ], rows: 1 }
{ status: 'succ', head: [ 'affected_rows' ], data: [ [ 1 ] ], rows: 1 }
{ status: 'succ', head: [ 'affected_rows' ], data: [ [ 1 ] ], rows: 1 }
```



至此，写入 EMQX 数据到 TDEngine 的整个功能已开发/配置完成。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
