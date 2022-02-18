本文以在 `CentOS 7.2`  中的实际例子来说明如何通过 MySQL 来存储相关的 MQTT 数据。

MySQL 属于传统的关系型数据库产品，其开放式的架构使得用户的选择性很强，而且随着技术的逐渐成熟，MySQL 支持的功能也越来越多，性能也在不断地提高，对平台的支持也在增多，此外，社区的开发与维护人数也很多。当下，MySQL 因为其功能稳定、性能卓越，且在遵守 GPL 协议的前提下，可以免费使用与修改，因此深受用户喜爱。

## 安装与验证 MySQL 服务器

读者可以参考 MySQL [官方文档](https://www.mysql.com/downloads/) 或使用 [Docker](https://hub.docker.com/_/mysql/) 来下载安装 MySQL 服务器，本文章使用 MySQL 5.6 版本。

为方便管理操作，可下载使用官方免费图形化管理软件 [MySQL Workbeanch](https://dev.mysql.com/downloads/workbench/)。

> 如果读者使用的是 MySQL 8.0 及以上版本，MySQL 需按照[ EMQX 无法连接 MySQL 8.0](https://docs.emqx.io/faq/v3/cn/errors.html#emq-x-无法连接-mysql-80) 教程特殊配置。



## 准备

### 初始化数据表

插件运行依赖以下几张数据表，数据表需要用户自行创建，表结构不可改动。

**mqtt_client 存储设备在线状态**

```sql
DROP TABLE IF EXISTS `mqtt_client`;
CREATE TABLE `mqtt_client` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `clientid` varchar(64) DEFAULT NULL,
  `state` varchar(3) DEFAULT NULL, -- 在线状态 0 离线 1 在线
  `node` varchar(100) DEFAULT NULL, -- 所属节点
  `online_at` datetime DEFAULT NULL, -- 上线时间
  `offline_at` datetime DEFAULT NULL, -- 下线时间
  `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `mqtt_client_idx` (`clientid`),
  UNIQUE KEY `mqtt_client_key` (`clientid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



**mqtt_sub 存储设备的主题订阅关系**

```sql
DROP TABLE IF EXISTS `mqtt_sub`;
CREATE TABLE `mqtt_sub` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `clientid` varchar(64) DEFAULT NULL,
  `topic` varchar(255) DEFAULT NULL,
  `qos` int(3) DEFAULT NULL,
  `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `mqtt_sub_idx` (`clientid`,`topic`(255),`qos`),
  UNIQUE KEY `mqtt_sub_key` (`clientid`,`topic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



**mqtt_msg 存储 MQTT 消息**

```sql
DROP TABLE IF EXISTS `mqtt_msg`;
CREATE TABLE `mqtt_msg` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `msgid` varchar(100) DEFAULT NULL,
  `topic` varchar(1024) NOT NULL,
  `sender` varchar(1024) DEFAULT NULL,
  `node` varchar(60) DEFAULT NULL,
  `qos` int(11) NOT NULL DEFAULT '0',
  `retain` tinyint(2) DEFAULT NULL,
  `payload` blob,
  `arrived` datetime NOT NULL, -- 是否抵达（QoS > 0）
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



**mqtt_retain 存储 Retain 消息**

```sql
DROP TABLE IF EXISTS `mqtt_retain`;
CREATE TABLE `mqtt_retain` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `topic` varchar(200) DEFAULT NULL,
  `msgid` varchar(60) DEFAULT NULL,
  `sender` varchar(100) DEFAULT NULL,
  `node` varchar(100) DEFAULT NULL,
  `qos` int(2) DEFAULT NULL,
  `payload` blob,
  `arrived` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mqtt_retain_key` (`topic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



**mqtt_acked 存储客户端消息确认**

```sql
DROP TABLE IF EXISTS `mqtt_acked`;
CREATE TABLE `mqtt_acked` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `clientid` varchar(200) DEFAULT NULL,
  `topic` varchar(200) DEFAULT NULL,
  `mid` int(200) DEFAULT NULL,
  `created` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mqtt_acked_key` (`clientid`,`topic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



## 配置 EMQX 服务器

通过 RPM 方式安装的 EMQX，MySQL 相关的配置文件位于 `/etc/emqx/plugins/emqx_backend_mysql.conf`，本文仅测试 MySQL 持久化的功能，大部分配置不需要做更改。填入用户名、密码、数据库即可：

```bash
backend.mysql.server = 127.0.0.1:3306

backend.mysql.username = root

backend.mysql.password = 123456

backend.mysql.database = mqtt
```

保持剩下部分的配置文件不变，然后需要启动该插件。启动插件的方式有 `命令行`、 `控制台` 和 `REST API` 三种方式，读者可以任选其一。


### 通过命令行启动

```bash
emqx_ctl plugins load emqx_backend_mysql
```

### 通过管理控制台启动

EMQX 管理控制台 **插件** 页面中，找到 **emqx_backend_mysql** 插件，点击 **启动**。

### 通过 REST API 启动

使用 `PUT /api/v4/nodes/:node/plugins/:plugin_name/load` API 可以启动插件。



## 客户端在线状态存储

客户端上下线时，插件将更新在线状态、上下线时间、节点客户端列表至 MySQL 数据库。


### 配置项

打开配置文件，配置 Backend 规则：

```bash
## hook: client.connected、client.disconnected
## action/function: on_client_connected、on_client_disconnected


## 客户端上下线
backend.mysql.hook.client.connected.1 = {"action": {"function": "on_client_connected"}, "pool": "pool1"}

backend.mysql.hook.client.disconnected.1 = {"action": {"function": "on_client_disconnected"}, "pool": "pool1"}
```


### 使用示例

浏览器打开 `http://127.0.0.1:18083` EMQX 管理控制台，在 **工具** -> **Websocket** 中新建一个客户端连接，指定 clientid 为 sub_client，点击连接，连接成功后手动断开:

![image20181116105333637.png](https://static.emqx.net/images/20f7a8592d5fdaa8d9db4a385f2fd964.png)



在 MySQL Workbeanch 中点击 `mqtt_client` 表查看，此时将写入 / 更新一条客户端上下线记录：

![image20181119105034528.png](https://static.emqx.net/images/2a1d3b6ed6e5b1ad2611d839f8484be9.png)




## 客户端代理订阅

客户端上线时，存储模块直接从数据库读取预设待订阅列表，代理加载订阅主题。在客户端需要通过预定主题通信（接收消息）场景下，应用能从数据层面设定 / 改变代理订阅列表。

### 配置项

打开配置文件，配置 Backend 规则：

```bash
## hook: client.connected
## action/function: on_subscribe_lookup
backend.mysql.hook.client.connected.2    = {"action": {"function": "on_subscribe_lookup"}, "pool": "pool1"}
```



### 使用示例

当 `sub_client` 设备上线时，需要为其订阅 `sub_client/upstream` 与 `sub_client/downlink` 两个 QoS 1 的主题：

1. 在 `mqtt_sub` 表中初始化插入代理订阅主题信息：

```sql
insert into mqtt_sub(clientid, topic, qos) values("sub_client", "sub_client/upstream", 1);
insert into mqtt_sub(clientid, topic, qos) values("sub_client", "sub_client/downlink", 1);
```

2. EMQX  管理控制台 **WebSocket** 页面，以 clientid `sub_client`  新建一个客户端连接，切换至**订阅**页面，可见当前客户端自动订阅了 `sub_client/upstream` 与 `sub_client/downlink` 两个 QoS 1 的主题：

![image20181116110036523.png](https://static.emqx.net/images/30b6bc892f1df5ba300fcbfe145345d5.png)




3. 切换回管理控制台 **WebSocket** 页面，向 `sub_client/downlink` 主题发布消息，可在消息订阅列表收到发布的消息。




## 持久化发布消息

### 配置项

打开配置文件，配置 Backend 规则，支持使用 `topic` 参数进行消息过滤，此处使用 `#` 通配符存储任意主题消息：

```bash
## hook: message.publish
## action/function: on_message_publish

backend.mysql.hook.message.publish.1     = {"topic": "#", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```



### 使用示例

在 EMQX 管理控制台 **WebSocket** 页面中，向主题 `upstream_topic` 发布多条消息，EMQX 将消息列表持久化至 `mqtt_msg` 表中：

![image20181119110712267.png](https://static.emqx.net/images/964dabfb8bf10ae868b69f117e849c9b.png)


>暂只支持 QoS 1 2 的消息持久化。




## Retain 消息持久化

### 配置项

打开配置文件，配置 Backend 规则：

```bash
## 同时开启以下规则，启用 retain 持久化三个生命周期

## 发布非空 retain 消息时 (存储)
backend.mysql.hook.message.publish.2     = {"topic": "#", "action": {"function": "on_message_retain"}, "pool": "pool1"}

## 设备订阅主题时查询 retain 消息
backend.mysql.hook.session.subscribed.2  = {"topic": "#", "action": {"function": "on_retain_lookup"}, "pool": "pool1"}

## 发布空 retain 消息时 (清除)
backend.mysql.hook.message.publish.3     = {"topic": "#", "action": {"function": "on_retain_delete"}, "pool": "pool1"}

```



### 使用示例

在 EMQX 管理控制台 **WebSocket** 页面中建立连接后，发布消息勾选**保留**：

![image20181119111926675.png](https://static.emqx.net/images/9460dfcbb0188867ad37aa7a36c1687b.png)



**发布（消息不为空）**

非空的 retain 消息发布时，EMQX 将以 topic 为唯一键，持久化该条消息至 `mqtt_retain` 表中，相同主题下发不同的 retain 消息，只有最后一条消息会被持久化：


![image20181119164153931.png](https://static.emqx.net/images/9b17858dedd4ed083c73c4678b26b769.png)


**订阅**

客户端订阅 retain 主题后，EMQX 将查询 `mqtt_retain` 数据表，执行投递 retain 消息操作。



**发布（消息为空）**

MQTT 协议中，发布空的 retain 消息将清空 retain 记录，此时 retain 记录将从 `mqtt_retain` 表中删除。



## 消息确认持久化

开启消息确认 (ACK) 持久化后，客户端订阅 QoS 1、QoS 2 级别的主题时，EMQX 将在数据库以 clientid + topic 为唯一键初始化 ACK 记录。

### 配置项

打开配置文件，配置 Backend 规则，可使用 **topic 通配符** 过滤要应用的消息：

```bash
## 订阅时初始化 ACK 记录
backend.mysql.hook.session.subscribed.1  = {"topic": "#", "action": {"function": "on_message_fetch"}, "pool": "pool1"}


## 消息抵达时更新抵达状态
backend.mysql.hook.message.acked.1       = {"topic": "#", "action": {"function": "on_message_acked"}, "pool": "pool1"}

## 取消订阅时删除记录行
backend.mysql.hook.session.unsubscribed.1= {"topic": "#", "action": {"sql": ["delete from mqtt_acked where clientid = ${clientid} and topic = ${topic}"]}, "pool": "pool1"}
```



### 使用示例

在 EMQX 管理控制台 **WebSocket** 页面中建立连接后，订阅 QoS > 0 的主题：

![image20181119140251843.png](https://static.emqx.net/images/0f102ddaa6b0f7de7ad74993e7df8895.png)



此时 `mqtt_acked` 表将插入初始化数据行，每向主题发布一条 QoS > 0 的消息，消息抵达后数据行 mid 将自增 1：

![image20181119140354855.png](https://static.emqx.net/images/05346a44ee99ff82d98116638619258b.png)

> 代理订阅中满足 QoS > 0 的 topic 也会初始化记录，客户端取消订阅后相关记录将被删除。





## 自定义 SQL

除去插件内置函数、表结构外，emqx_backend_mysql 还支持自定义 SQL 语句，通过使用如 `${clientid}` 模板语法动态构造 SQL 语句实现如客户端连接历史、更新自定义数据表等操作。

### SQL语句参数说明

| hook                 | 可用参数                             | 示例(sql语句中${name} 表示可获取的参数)                      |
| -------------------- | ------------------------------------ | ------------------------------------------------------------ |
| client.connected     | clientid                             | insert into conn(clientid) values(${clientid})               |
| client.disconnected  | clientid                             | insert into disconn(clientid) values(${clientid})            |
| session.subscribed   | clientid, topic, qos                 | insert into sub(topic, qos) values(${topic}, ${qos})         |
| session.unsubscribed | clientid, topic                      | delete from sub where topic = ${topic}                       |
| message.publish      | msgid, topic, payload, qos, clientid | insert into msg(msgid, topic) values(\${msgid}, ${topic})    |
| message.acked        | msgid, topic, clientid               | insert into ack(msgid, topic) values(\${msgid}, ${topic})    |
| message.delivered    | msgid, topic, clientid               | insert into delivered(msgid, topic) values(\${msgid}, ${topic}) |



### 客户端连接 log 示例

设计表结构如下：

```sql
CREATE TABLE `mqtt`.`connect_logs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `clientid` VARCHAR(255) NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP, -- 记录时间
  `state` INT NOT NULL DEFAULT 0,  -- 记录类型： 0 下线 1 上线
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

自定义 SQL：

```bash
## connected hook 中配置自定义 SQL
## 可以配置多条 SQL 语句 "SQL": ["sql_a", "sql_b", "sql_c"]

## 连接时
backend.mysql.hook.client.connected.3 = {"action": {"sql": ["insert into connect_logs(clientid, state) values(${clientid}, 1)"]}, "pool": "pool1"}

## 断开时
backend.mysql.hook.client.disconnected.3 = {"action": {"sql": ["insert into connect_logs(clientid, state) values(${clientid}, 0)"]}, "pool": "pool1"}
```



客户端上下线时将填充并执行预定的 SQL 语句，将连接记录写入 `connect_logs` 表。

![image20181119154828728.png](https://static.emqx.net/images/5fc04e622dc690074ffc096ce3354806.png)





## 高级选项

```bash
backend.mysql.time_range = 5s

backend.mysql.max_returned_count = 500
```




## 总结

读者在理解了 MySQL 中所存储的数据结构、自定义 SQL 之后，可以结合 MySQL 拓展相关应用。
