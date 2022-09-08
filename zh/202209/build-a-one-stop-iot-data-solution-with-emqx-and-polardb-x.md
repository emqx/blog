## 前言

虽然物联网的应用场景很多，但总结来看各类场景都离不开对数据的采集-传输-存储-分析。按照数据特性和业务需求不同，物联网数据可以分为不同的种类:

- 元数据：设备最新的状态数据，如在线状态、当前传感器数值；
- 消息数据：设备发布的消息，包括上报数据和下发指令；
- 时序数据：持续变化的元数据和消息数据。

在物联网应用中，数据存储需求无处不在，数据只有经过传输、存储，再经由业务系统查询并处理才能实现各类业务需求，进一步发挥数据的价值。

物联网设备规模庞大，往往整体数据量也非常大，实践中通常有以下选型：

- 元数据需要频繁插入更新，并且支持结构化查询，所以推荐使用关系数据库进行存储。
- 消息数据不需要全量存储，只需要记录关键操作，或者提取消息数据的关键数据，应当根据业务情况适当的选型。
- 时序数据的特点是数据修改频次低，对写入速度和存储压缩比敏感，查询需求多样，因此推荐使用时序数据库。

数据库存储选型不是绝对的，用户可以综合数据特性、数据量以及后端业务需求来选择适合的数据库，在各种因素中达到平衡。

[EMQX](https://www.emqx.com/zh/products/emqx) 是由 EMQ 开发的一款大规模分布式物联网 MQTT 消息服务器。作为专门针对低带宽和不稳定网络环境的物联网应用设计的协议，MQTT 基于发布/订阅模式，具有简单易实现、支持 QoS、报文小等特点。完整支持 MQTT 协议的 EMQX 则可以连接海量物联网设备，提供高可靠、高性能的实时数据移动、处理和集成，充当设备与设备、设备与应用之间的桥梁。

PolarDB-X 是由阿里巴巴自主研发的云原生分布式数据库，是一款基于云架构理念，并同时支持在线事务处理与在线分析处理 (Hybrid Transactional and Analytical Processing, HTAP）的融合型分布式数据库。其具备金融级数据高可用、分布式水平扩展、混合负载、低成本存储和极致弹性等能力，专注解决海量数据存储、超高并发吞吐、大表瓶颈以及复杂计算效率等数据库瓶颈难题。

本文将介绍[开源版 EMQX](https://www.emqx.io/zh) 与 PolarDB-X 打造的集成方案，可以实现关键物联网数据的一站式采集、传输、存储。

## EMQX+PolarDB-X 集成方案详情

使用 EMQX 接入物联网设备，通过 EMQX 数据集成组件来处理并分发数据到 MQTT 汇聚主题，第三方脚本通过 MQTT 订阅的方式从汇聚主题中获取数据，并代理写入到 PolarDB-X，以下是整体架构图：

![EMQX + PolarDB-X](https://assets.emqx.com/images/5ab5e6985e8ac6e987e5b4fe1defb1f7.png)


### 数据集成简介

数据集成是 EMQX 在发布订阅模型的基础之上的数据处理与分发组件，通过简单的可视化的配置，即可实时处理 EMQX 的消息以及设备事件并将其与 Kafka/RabbitMQ 等消息中间件、以及各类 SQL/NoSQL/时序数据库等数据系统集成。

其中消息是指设备端的上报或者云端的下发消息，设备生命周期事件是指整个设备在运行过程中的事件，这些事件对物联网的应用开发有很大作用，围绕此可以实现设备管理、安全审计、设备影子等业务，以及更精细化的控制 MQTT 消息传输过程。

### 共享订阅简介

[MQTT 共享订阅](https://www.emqx.com/zh/blog/introduction-to-mqtt5-protocol-shared-subscription)是在多个订阅者之间实现负载均衡的订阅方式，相当于订阅端的负载均衡功能。

例如在 EMQX 集群中，如果某个节点挂了，利用共享订阅功能同时订阅多个节点则可以避免某个节点故障导致数据丢失。

![MQTT 共享订阅](https://assets.emqx.com/images/a70956010557ecc41dc5482a5eec23b7.png)

用户可以通过使用 $share/{group}/{topic} 或 $queue/{topic} 格式的主题，发起共享订阅。

### 第三方脚本

由于 EMQX 开源版中不具备直接写入 PolarDB-X 的能力，因此需要提供第三方的脚本来实现数据写入。

EMQX -  脚本进程之间可以使用 MQTT 共享订阅连接，避免消息量过大时单个 MQTT 连接的处理能力成为方案瓶颈，同时充分使用[连接池](https://polardbx.com/document)与批处理技术，提高写入 PolarDB-X 的吞吐。

利用 EMQX 海量设备数据接入能力和数据集成能力，以及 PolarDB-X 的超高并发写入和海量存储支持能力，这一集成方案可以应对连接数规模与采集点数量庞大的物联网场景。

## EMQX + PolarDB-X 方案搭建步骤

接下来我们通过几个场景看一下如何进行方案搭建。

### 场景介绍

#### 存储设备在线状态

在上下线时更新设备状态，并记录上线/下线时间，如果设备是初次连接则先将设备信息插入数据库。

需要使用 EMQX 的客户端上下线事件，对应的事件主题为 $event/client_connected 与 $event/client_disconnected。

PolarDB-X 表结构如下：

```
-- 设备在线状态表
create table clients (
  `id` bigint(11) auto_increment NOT NULL,
  `clientid` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `ip_address` varchar(255) DEFAULT NULL,
  `status` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  primary key (`id`),
  unique key(`clientid`)
) engine = InnoDB default charset = utf8 partition by hash(id) partitions 2;
```

#### 记录设备事件

记录设备上下线历史、订阅/取消订阅事件，需要记录设备客户端 ID、事件发生时间等关键新轩逸，订阅/取消订阅事件还需要记录操作的主题。

EMQX 中对应的事件主题为$event/client_connected 、$event/client_disconnected 、$event/session_subscribed 、$event/session_unsubscribed。

PolarDB-X 表结构如下：

```
-- 设备历史事件表
create table client_events (
  `id` bigint(11) auto_increment NOT NULL,
  `clientid` varchar(255) DEFAULT NULL,
  `event` char(20) DEFAULT NULL,
  `topic` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  primary key (`id`)
) engine = InnoDB default charset = utf8 partition by hash(id) partitions 2;
```

#### 存储设备消息

将指定主题的消息存储到数据库当中，需要记录设备客户端 ID、消息主题、消息 Payload 信息。

PolarDB-X 表结构如下：

```
-- IoT 数据记录表
create table messages (
  `id` bigint(11) auto_increment NOT NULL,
  `clientid` varchar(255) DEFAULT NULL,
  `topic` varchar(255) DEFAULT NULL,
  `payload` BLOB DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  primary key (`id`)
) engine = InnoDB default charset = utf8 partition by hash(id) partitions 2;
```

### 操作步骤

具体的操作步骤如下：

1. 首先需要部署 PolarDB-X，按照文档中的[快速入门指南](https://polardbx.com/document)部署即可。

2. 通过 MySQL Client 连接到 PolarDB-X 并使用场景中提供的 SQL 创建数据表。

3. 在本地启动 EMQX，启动成功之后，访问 http://localhost:18083 打开 Dashboard。如果需要中文显示可以到 **System → Settings** 中将语言更改为简体中文。

   ![EMQX Dashboard 修改语言](https://assets.emqx.com/images/127b6f6abb48d4d8722a35a9b157b941.png)

4. 在数据集成中创建规则，创建一条能够处理场景中所需事件以及 t/# 消息主题的规则。

   EMQX 的客户端事件通过事件主题触发，客户端会在连接成功时触发执行规则 SQL，规则可以从上下文中获取当前客户端中相关信息，包括 客户端 ID、事件名称、连接时间、连接属性等，通过调试功能可以查看规则执行结果。

   规则 SQL：

   ```
   SELECT
     *
   FROM
     "$events/client_connected",
     "$events/client_disconnected",
     "$events/session_subscribed",
     "$events/session_unsubscribed",
     "t/#"
   ```

   ![EMQX 规则引擎](https://assets.emqx.com/images/07fda4539090f275ab7ff1bbc8a84c97.png)

5. 添加动作，选择消息重发布动作，将规则处理结果转发至 emqx_polardb 主题由第三方脚本处理。除此之外，可以添加一个控制台输出动作用于调试，在企业版中还可以可以配置将结果直接写入 PolarDB-X。

   ![添加动作](https://assets.emqx.com/images/0bd24d7539f670a73947b450e28f7414.png)

6. 接下来，使用 Dashboard 上的 WebSocket 客户端进行测试，订阅 emqx_polardb 主题确认是否可以从中获取到数据。

   ![MQTT WebSocket](https://assets.emqx.com/images/8f6c3af7e5093ea664a6250959a93653.png)

7. 在第三方脚本中实现 PolarDB-X 数据插入逻辑，关键代码如下：

   ```
   // 消息处理函数
   async function handleMessage(topic, payload) {
     let data = null
     try {
       data = JSON.parse(payload)
     } catch (e) {
       console.log('message not a JSON')
     }
     if (data === null) {
       return
     }
     // 根据事件类型处理
     const event = data.event
     // 上下线记录
     if (event === 'client.connected' || event === 'client.disconnected') {
       const status = event === 'client.connected' ? 1 : 0
       
       // 更新设备在线状态
       // 借助 ON DUPLICATE KEY UPDATE 特性实现
       await connection.execute(
         `INSERT INTO clients (clientid, username, ip_address, status) VALUES
       ('${data.clientid}', '${data.username}', '${data.sockname}', ${status}) ON DUPLICATE KEY UPDATE status = ${status}, ip_address = '${data.sockname}'`)
       
       // 保存设备上下线记录
       await connection.execute(`INSERT INTO client_events (clientid, event, topic) VALUES
       (?, ?, '')`, [data.clientid, data.event])
   
     } else if (event === 'message.publish') {
       
       // 保存设备消息
       await connection.execute(`INSERT INTO messages(clientid, topic, payload) VALUES
          (?, ?, ?);`, [data.clientid, data.topic, data.payload])
     } else {
       
       // 保存设备订阅/取消订阅记录，记录操作的主题
       await connection.execute(`INSERT INTO client_events (clientid, event, topic) VALUES
       (?, ?, ?)`, [data.clientid, data.event, data.topic])
     }
     console.log(`event ${event} saved ok`)
   }
   ```

8. 启动第三方脚本，将整个方案运行起来。

   ```
   $ node worker.js
   client 0 ready...
   event session.subscribed saved ok
   client 1 ready...
   event client.connected saved ok
   event session.subscribed saved ok
   client 2 ready...
   event client.connected saved ok
   event session.subscribed saved ok
   client 3 ready...
   event session.subscribed saved ok
   event client.connected saved ok
   client 4 ready...
   event client.connected saved ok
   event session.subscribed saved ok
   client 5 ready...
   event client.connected saved ok
   client 6 ready...
   event client.connected saved ok
   event session.subscribed saved ok
   event session.subscribed saved ok
   client 7 ready...
   event client.connected saved ok
   event session.subscribed saved ok
   event client.connected saved ok
   client 8 ready...
   event session.subscribed saved ok
   event client.connected saved ok
   client 9 ready...
   event session.subscribed saved ok
   ```

### 附录：第三方脚本完整示例

此处使用 Node.js 来实现消息的订阅与 PoarDB-X 插入，第三方脚本可以是任意语言编写的应用，建议与 EMQX、PolarDB-X 部署在同一个内网网络。

```
// worker.js
const mqtt = require('mqtt')
const mysql = require('mysql2')

const config = {
  host: 'localhost',
  port: 10743,
  username: 'polardbx_root',
  password: '****',
  database: 'emqx_iot'
}

// 建立与 PolarDB-X 的连接
const connection = mysql.createConnection({
  host: config.host,
  user: config.username,
  password: config.password,
  database: config.database,
  port: config.port,
})

function createClient() {
  return new Promise((resolve, reject) => {
    const client = mqtt.connect('mqtt://localhost:1883')
    client.on('connect', () => {
      resolve(client)
    })
  })
}

async function handleMessage(topic, payload) {
  let data = null
  try {
    data = JSON.parse(payload)
  } catch (e) {
    console.log('message not a JSON')
  }
  if (data === null) {
    return
  }
  const event = data.event
  // 上下线记录
  if (event === 'client.connected' || event === 'client.disconnected') {
    const status = event === 'client.connected' ? 1 : 0
    // 写入 or 更新设备表
    await connection.execute(
      `INSERT INTO clients (clientid, username, ip_address, status) VALUES
    ('${data.clientid}', '${data.username}', '${data.sockname}', ${status}) ON DUPLICATE KEY UPDATE status = ${status}, ip_address = '${data.sockname}'`)
    // 插入历史表
    await connection.execute(`INSERT INTO client_events (clientid, event, topic) VALUES
    (?, ?, '')`, [data.clientid, data.event])
  } else if (event === 'message.publish') {
    // 插入消息表
    await connection.execute(`INSERT INTO messages(clientid, topic, payload) VALUES
       (?, ?, ?);`, [data.clientid, data.topic, data.payload])
  } else {
    // 订阅/取消订阅记录
    await connection.execute(`INSERT INTO client_events (clientid, event, topic) VALUES
    (?, ?, ?)`, [data.clientid, data.event, data.topic])
  }
  console.log(`event ${event} saved ok`)
}

async function main() {
  // 初始化 10 个订阅客户端
  for (let i = 0; i < 10; i++) {
    const client = await createClient()
    client.subscribe('$share/1/emqx_polardb')
    client.on('message', handleMessage)
    console.log(`client ${i} ready...`)
  }
}

main()
```

## 结语

PolarDB-X 的分布式特性以及存储计算分离架构为其带来了水平扩展、分布式事务、混合负载等能力，与同样是分布式的 MQTT 消息服务器 EMQX 结合使用，可以打造真正的可伸缩物联网应用，应对从数千到数千万的设备接入。

除了本文分享的开源版方案， EMQX 企业版以及全托管的云服务版本 EMQX Cloud 中还提供了 MySQL 数据集成能力，可以直接通过 PolarDB-X 兼容语法完成数据集成，更加简单高效地实现物联网数据一站式连接、移动与存储分析。


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
