本章节以在 `CentOS 7.2` 中的实际例子来说明如何通过 PostgreSQL 来存储相关的信息。

作为开源关系数据库重要一员，PostgreSQL 标榜自己是世界上最先进的开源数据库，相比于其他开源关系数据库如 MySQL，PostgreSQL 是完全由社区驱动的开源项目，由全世界超过 1000 名贡献者所维护。PostgreSQL 提供了单个完整功能的版本，而不像 MySQL 那样提供了多个不同的社区版、商业版与企业版。PostgreSQL 基于自由的 BSD/MIT 许可，组织可以使用、复制、修改和重新分发代码，只需要提供一个版权声明即可。

PostgreSQL 具有诸多特性，在 GIS 领域有较多支持，其“无锁定”特性非常突出，支持函数和条件索引，有成熟的集群方案。PostgreSQL 还具备及其强悍的 SQL 编程能力如统计函数和统计语法支持，通过 Timescaledb 插件，PostgreSQL 可以转变为功能完备的时序数据库 Timescaledb 。

## 功能概览

- 客户端在线状态存储
- 客户端代理订阅
- 持久化发布消息
- Retain 消息持久化
- 消息确认持久化
- 自定义 SQL
## 安装与验证 PostgreSQL 服务器

读者可以参考 PostgreSQL [官方文档](https://www.postgresql.org/docs/) 或 [Docker](https://hub.docker.com/_/postgres/) 来下载安装PostgreSQL 服务器，本文章使用 PostgreSQL 10.1 版本。

为方便管理操作，可下载使用免费图形化管理软件 [Postico](https://eggerapps.at/postico/)（仅限 MacOS）或 [pgAdmin](https://www.pgadmin.org/)。



## 配置 EMQX 服务器

通过 RPM 方式安装的 EMQX，PostgreSQL 相关的配置文件位于 `/etc/emqx/plugins/emqx_backend_pgsql.conf`，如果只是测试 PostgreSQL 持久化的功能，大部分配置不需要做更改，填入用户名、密码、数据库即可：

```bash
backend.pgsql.pool1.server = 127.0.0.1:5432

backend.pgsql.pool1.pool_size = 8

backend.pgsql.pool1.username = root

backend.pgsql.pool1.password = public

backend.pgsql.pool1.database = mqtt

backend.pgsql.pool1.ssl = false
```

保持剩下部分的配置文件不变，然后需要启动该插件。启动插件的方式有 `命令行`和 `控制台`两种方式，读者可以任选其一。



### 通过命令行启动

```bash
emqx_ctl plugins load emqx_backend_pgsql
```



### 通过管理控制台启动

EMQX 管理控制台 **插件** 页面中，找到 **emqx_backend_pgsql** 插件，点击 **启动**。



## 客户端在线状态存储

客户端上下线时，插件将更新在线状态、上下线时间、节点客户端列表至 PostgreSQL 数据库。

### 数据表

创建 mqtt_client 设备在线状态表:

```sql
CREATE TABLE mqtt_client(
  id SERIAL primary key,
  clientid character varying(100),
  state integer, -- 在线状态: 0 离线 1 在线
  node character varying(100), -- 接入节点名称
  online_at timestamp, -- 上线时间
  offline_at timestamp, -- 下线时间
  created timestamp without time zone,
  UNIQUE (clientid)
);
```



### 配置项

打开配置文件，配置 Backend 规则：

```bash
## hook: client.connected、client.disconnected
## action/function: on_client_connected、on_client_disconnected


## 客户端上下线
backend.pgsql.hook.client.connected.1 = {"action": {"function": "on_client_connected"}, "pool": "pool1"}

## 客户端下线
backend.pgsql.hook.client.disconnected.1 = {"action": {"function": "on_client_disconnected"}, "pool": "pool1"}
```



### 使用示例

浏览器打开 `http://127.0.0.1:18083` EMQX 管理控制台，在 **工具** -> **Websocket** 中新建一个客户端连接，指定 clientid 为 sub_client，点击连接，连接成功后手动断开:

![image20181116105333637.png](https://assets.emqx.com/images/21b922d468e1c3be5ec2e16a7ab87654.png)



 查看 `mqtt_client` 表，此时将写入 / 更新一条客户端上下线记录：

![1.png](https://assets.emqx.com/images/cb22c4bf8120a69b34e52f61668fa40e.png)



## 客户端代理订阅

客户端上线时，存储模块直接从数据库读取预设待订阅列表，代理加载订阅主题。在客户端需要通过预定主题通信（接收消息）场景下，应用能从数据层面设定 / 改变代理订阅列表。

### 数据表

创建 mqtt_sub 代理订阅关系表:

```sql
CREATE TABLE mqtt_sub(
  id SERIAL primary key,
  clientid character varying(100),
  topic character varying(200), -- topic
  qos integer, -- QoS
  created timestamp without time zone,
  UNIQUE (clientid, topic)
);
```



### 配置项

打开配置文件，配置 Backend 规则：

```bash
## hook: client.connected
## action/function: on_subscribe_lookup
backend.pgsql.hook.client.connected.2    = {"action": {"function": "on_subscribe_lookup"}, "pool": "pool1"}
```



### 使用示例

当 `sub_client` 设备上线时，需要为其订阅 `sub_client/upstream` 与 `sub_client/downlink` 两个 QoS 1 的主题：

1. 在 `mqtt_sub` 表中初始化插入代理订阅主题信息：

```sql
insert into mqtt_sub(clientid, topic, qos) values('sub_client', 'sub_client/upstream', 1);

insert into mqtt_sub(clientid, topic, qos) values('sub_client', 'sub_client/downlink', 1);
```

2. EMQX  管理控制台 **WebSocket** 页面，以 clientid `sub_client`  新建一个客户端连接，切换至**订阅**页面，可见当前客户端自动订阅了 `sub_client/upstream` 与 `sub_client/downlink` 两个 QoS 1 的主题：

![image20181116110036523.png](https://assets.emqx.com/images/b334ec22b58478ecb23cb940ef537a8f.png)



3. 切换回管理控制台 **WebSocket** 页面，向 `sub_client/downlink` 主题发布消息，可在消息订阅列表收到发布的消息。



## 持久化发布消息

### 数据表

创建 mqtt_msg MQTT 消息持久化表:

```sql
CREATE TABLE mqtt_msg (
  id SERIAL primary key,
  msgid character varying(60),
  sender character varying(100), -- 消息 pub 的 clientid
  topic character varying(200),
  qos integer,
  retain integer, -- 是否 retain 消息
  payload text,
  arrived timestamp without time zone -- 消息抵达时间(QoS > 0)
);
```



### 配置项

打开配置文件，配置 Backend 规则，支持使用 `topic` 参数进行消息过滤，此处使用 `#` 通配符存储任意主题消息：

```bash
## hook: message.publish
## action/function: on_message_publish

backend.pgsql.hook.message.publish.1     = {"topic": "#", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```



### 使用示例

在 EMQX 管理控制台 **WebSocket** 页面中，使用 clientdi `sub_client` 建立连接，向主题 `upstream_topic` 发布多条消息，EMQX 将消息列表持久化至 `mqtt_msg` 表中：

![websocket.png](https://assets.emqx.com/images/b81198d32658909aeed6f759c89065bf.png)

> 暂只支持 QoS 1 2 的消息持久化。



## Retain 消息持久化

### 表结构

创建 mqtt_retain Retain 消息存储表:

```sql
CREATE TABLE mqtt_retain(
  id SERIAL primary key,
  topic character varying(200),
  msgid character varying(60),
  sender character varying(100),
  qos integer,
  payload text,
  arrived timestamp without time zone,
  UNIQUE (topic)
);
```



### 配置项

打开配置文件，配置 Backend 规则：

```bash
## 同时开启以下规则，启用 retain 持久化三个生命周期

## 发布非空 retain 消息时 (存储)
backend.pgsql.hook.message.publish.2     = {"topic": "#", "action": {"function": "on_message_retain"}, "pool": "pool1"}

## 设备订阅主题时查询 retain 消息
backend.pgsql.hook.session.subscribed.2  = {"topic": "#", "action": {"function": "on_retain_lookup"}, "pool": "pool1"}

## 发布空 retain 消息时 (清除)
backend.pgsql.hook.message.publish.3     = {"topic": "#", "action": {"function": "on_retain_delete"}, "pool": "pool1"}

```



### 使用示例

在 EMQX 管理控制台 **WebSocket** 页面中建立连接后，发布消息勾选**保留**：

![image20181119111926675.png](https://assets.emqx.com/images/6499f454eebced1149341d12c73565ec.png)



**发布（消息不为空）**

非空的 retain 消息发布时，EMQX 将以 topic 为唯一键，持久化该条消息至 `mqtt_retain` 表中，相同主题下发布不同的 retain 消息，只有最后一条消息会被持久化：

![image20181119112306703.png](https://assets.emqx.com/images/be54769f62f8d60acd4c43fe9122b50c.png)


**订阅**

客户端订阅 retain 主题后，EMQX 将查询 `mqtt_retain` 数据表，执行投递 retain 消息操作。



**发布（消息为空）**

MQTT 协议中，发布空的 retain 消息将清空 retain 记录，此时 retain 记录将从 `mqtt_retain` 表中删除。





## 消息确认持久化

开启消息确认 (ACK) 持久化后，客户端订阅 QoS 1、QoS 2 级别的主题时，EMQX 将在数据库以 clientid + topic 为唯一键初始化 ACK 记录。



### 数据表

创建 mqtt_acked 消息确认表:

```sql
CREATE TABLE mqtt_acked (
  id SERIAL primary key,
  clientid character varying(100),
  topic character varying(100),
  mid integer,
  created timestamp without time zone,
  UNIQUE (clientid, topic)
);
```



### 配置项

打开配置文件，配置 Backend 规则，可使用 **topic 通配符** 过滤要应用的消息：

```bash
## 订阅时初始化 ACK 记录
backend.pgsql.hook.session.subscribed.1  = {"topic": "#", "action": {"function": "on_message_fetch"}, "pool": "pool1"}


## 消息抵达时更新抵达状态
backend.pgsql.hook.message.acked.1       = {"topic": "#", "action": {"function": "on_message_acked"}, "pool": "pool1"}

## 取消订阅时删除记录行
backend.pgsql.hook.session.unsubscribed.1= {"topic": "#", "action": {"sql": ["delete from mqtt_acked where clientid = ${clientid} and topic = ${topic}"]}, "pool": "pool1"}
```



### 使用示例

在 EMQX 管理控制台 **WebSocket** 页面中建立连接后，订阅 QoS > 0 的主题：

![image20181119140251843.png](https://assets.emqx.com/images/b0300b43d42beb9f6232722a71ab56aa.png)



此时 `mqtt_acked` 表将插入初始化数据行，每向主题发布一条 QoS > 0 的消息，消息抵达后数据行 mid 将自增 1：

![image20181119165248998.png](https://assets.emqx.com/images/c7eef4287ea6a7f66f644d36729e3497.png)

> 代理订阅中满足 QoS > 0 的 topic 也会初始化记录，客户端取消订阅后相关记录将被删除。





## 自定义 SQL

除去插件内置函数、表结构外，emqx_backend_pgsql 还支持自定义 SQL 语句，通过使用如 `${clientid}` 模板语法动态构造 SQL 语句实现如客户端连接历史、更新自定义数据表等操作。

### SQL语句参数说明

| hook                 | 可用参数                             | 示例(sql语句中${name} 表示可获取的参数)                      |
| -------------------- | ------------------------------------ | ------------------------------------------------------------ |
| client.connected     | clientid                             | insert into conn(clientid) values(${clientid})               |
| client.disconnected  | clientid                             | insert into disconn(clientid) values(${clientid})            |
| session.subscribed   | clientid, topic, qos                 | insert into sub(topic, qos) values(\${topic}, ${qos})        |
| session.unsubscribed | clientid, topic                      | delete from sub where topic = ${topic}                       |
| message.publish      | msgid, topic, payload, qos, clientid | insert into msg(msgid, topic) values(\${msgid}, ${topic})    |
| message.acked        | msgid, topic, clientid               | insert into ack(msgid, topic) values(\${msgid}, ${topic})    |
| message.delivered    | msgid, topic, clientid               | insert into delivered(msgid, topic) values(\${msgid}, ${topic}) |



### 更新自定义数据表示例

应用现有设备表 `clients`，具有设备连接认证、设备状态记录、设备管理等基本字段用于其他管理业务，现需要将 EMQX 设备状态同步至该表中：

```sql
CREATE TABLE "public"."clients" (
    "id" serial,
    "deviceUsername" varchar(50), --  MQTT username
    "client_id" varchar(50), -- MQTT client_id
    "password" varchar(50), -- MQTT password
    "is_super" boolean DEFAULT 'false', -- 是否 ACL super 客户端
    "owner" int, -- 创建用户
    "productID" int, -- 所属产品
    "state" boolean DEFAULT 'false', -- 在线状态
    PRIMARY KEY ("id")
);

-- 初始化系统中已存在示例数据，此时 state 为 false
INSERT INTO "public"."clients"("deviceUsername", "client_id", "password", "is_super", "owner", "productID", "state") VALUES('mqtt_10c61f1a1f47', 'mqtt_10c61f1a1f47', '9336EBF25087D91C818EE6E9EC29F8C1', TRUE, 1, 21, FALSE);

```



自定义 UPDATE SQL 语句：

```bash
## connected / disconnected hook 中配置自定义 UPDATE SQL
## 可以配置多条 SQL 语句 "SQL": ["sql_a", "sql_b", "sql_c"]

## 连接时
backend.pgsql.hook.client.connected.3 = {"action": {"sql": ["update clients set state = true where client_id = ${clientid}"]}, "pool": "pool1"}

## 断开时
backend.pgsql.hook.client.disconnected.3 = {"action": {"sql": ["update clients set state = false where client_id = ${clientid}"]}, "pool": "pool1"}
```



客户端上线时将填充并执行预定的 SQL 语句，更新设备在线状态 `state` 字段为 `true`：

![image20181119170648517.png](https://assets.emqx.com/images/8f27a4f09d4af2f2d9f10d05cd31c2c2.png)


## 高级选项

```bash
backend.pgsql.time_range = 5s

backend.pgsql.max_returned_count = 500
```



## 总结

读者在理解了 PostgreSQL 中所存储的数据结构、自定义 SQL 之后，可以结合 PostgreSQL 拓展相关应用。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
