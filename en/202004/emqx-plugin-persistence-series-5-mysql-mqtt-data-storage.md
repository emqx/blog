This article uses the practical example in `CentOS 7.2` to illustrate how to store related MQTT data through MySQL.

MySQL is a traditional relational database. Its open architecture makes users highly selective. With the gradual maturity of technology, MySQL supports more functions an platforms, and its performance constantly improved. n addition, the number of community developers and maintainers is also large. At the moment, MySQL is popular with users because of its stable function, excellent performance, and free use and modification under the premise of complying with the GPL agreement.

## Install and verify MySQL server

Readers can refer to MySQL  [Official Documentation](https://www.mysql.com/downloads/) or use  [Docker](https://hub.docker.com/_/mysql/)  to download and install MySQL server. This The article uses MySQL 5.6. 

To facilitate management operations, you can download and use the official free graphical management software  [MySQL Workbench](https://dev.mysql.com/downloads/workbench/).

> If the readers is using MySQL 8.0 or  above version , they need follow [ EMQX unable to connect MySQL 8.0](https://docs.emqx.io/faq/v3/cn/errors.html#emq-x-无法连接-mysql-80)Tutorial to specially configure MySQL.



## Preparation

### Initialize data table

The plugin operation depends on the following data tables, which needs to be created by the user. The table structure cannot be changed.

**mqtt_client to store device online status**

```sql
DROP TABLE IF EXISTS `mqtt_client`;
CREATE TABLE `mqtt_client` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `clientid` varchar(64) DEFAULT NULL,
  `state` varchar(3) DEFAULT NULL, -- online status 0 offline 1 online
  `node` varchar(100) DEFAULT NULL, -- Subordinated node
  `online_at` datetime DEFAULT NULL, -- online time
  `offline_at` datetime DEFAULT NULL, -- offline time
  `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `mqtt_client_idx` (`clientid`),
  UNIQUE KEY `mqtt_client_key` (`clientid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



**mqtt_sub to store topic subscription relationships of devices**

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



**mqtt_msg to store  MQTT message**

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
  `arrived` datetime NOT NULL, -- Whether to arrive（QoS > 0）
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```



**mqtt_retain to store Retain message**

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



**mqtt_acked to store client message acknowledgment**

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



## Configure EMQX server

For [EMQX](https://www.emqx.com/en) MQTT broker installed via RPM, MySQL related configuration files are located in `/etc/emqx/plugins/emqx_backend_mysql.conf`. This article only tests the persistence function of MySQL. Most of the configuration does not need to be changed. You only need to fill in the user name, password, and database:

```bash
backend.mysql.server = 127.0.0.1:3306

backend.mysql.username = root

backend.mysql.password = 123456

backend.mysql.database = mqtt
```

Leave the rest of the configuration file unchanged, and then you need to start the plugin. There are three ways to start the plugin: `command line`,` console` and `REST API`, and readers can choose one of them.


### Start from the command line

```bash
emqx_ctl plugins load emqx_backend_mysql
```

### Start from the console

Find the  **emqx_backend_mysql** plugin in the  **Plugins** page of EMQX Management Console, and click **Start**.

### Start from REST API 

Use `PUT /api/v4/nodes/:node/plugins/:plugin_name/load` API to start the plugin。



## MQTT client online status storage

When the MQTT client goes online or offline, the plug-in will update the online status, online and offline time, and node client list to the MySQL database.


### Configuration Item

Open the configuration file and configure the Backend rule:

```bash
## hook: client.connected、client.disconnected
## action/function: on_client_connected、on_client_disconnected


## Client goes online and offline
backend.mysql.hook.client.connected.1 = {"action": {"function": "on_client_connected"}, "pool": "pool1"}

backend.mysql.hook.client.disconnected.1 = {"action": {"function": "on_client_disconnected"}, "pool": "pool1"}
```


### Example

Opens `http://127.0.0.1:18083` EMQX management console through the browser, create a new client connection in **Tools ->  Websocket**, specify clientid as sub_client, click on **connect**, and disconnect manually after successful connection:

![image20181116105333637.png](https://static.emqx.net/images/7774360e24f62fc2c3dc996f7a1c7b1e.png)

View the `mqtt_client` table in MySQL Workbeanch , and a client online and offline record will be written/updated at this point :

![image20181119105034528.png](https://static.emqx.net/images/a467d97eae87ad25ce110156bd681221.png)




## MQTT client proxy subscription

When the MQTT client is online, the storage module directly reads the preset to-be-subscribed list from the database, and the agent loads the subscription topic. In the scenario where the client needs to communicate (receive a message) through a preset topic, the application can set / change the agent subscription list from the data level.

### Configuration item

Open the configuration file and configure the Backend rule:

```bash
## hook: client.connected
## action/function: on_subscribe_lookup
backend.mysql.hook.client.connected.2    = {"action": {"function": "on_subscribe_lookup"}, "pool": "pool1"}
```



### Example

When the `sub_client` device goes online, it needs to subscribe to the two QoS 1 topics of `sub-client/upstream` and `sub_client/downlink` :

1. Initially insert agent subscription topic information in the `mqtt_sub` table:

```sql
insert into mqtt_sub(clientid, topic, qos) values("sub_client", "sub_client/upstream", 1);
insert into mqtt_sub(clientid, topic, qos) values("sub_client", "sub_client/downlink", 1);
```

2. In the EMQX management console **WebSocket** page, create a new client connection with clientid `sub_client`. Switch to **subscription** page, and it can be seen that the current client automatically subscribes to the two QoS 1 topics of ` sub_client/upstream` and `sub_client/downlink`:

![WechatIMG2692.png](https://static.emqx.net/images/80baf3902be1d070a619caf35da10b33.png)



3. Switch back to the management console **WebSocket** page and publish the message to the topic `sub_client/downlink`. You can receive the published message in the message subscription list.




## Persist publishing message

### Configuration item

Open the configuration file, and configure the Backend rule. The `topic` parameter is supported for message filtering. We use the # wildcard to store arbitrary topic messages here:

```bash
## hook: message.publish
## action/function: on_message_publish

backend.mysql.hook.message.publish.1     = {"topic": "#", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```



### Example

In the EMQX management console **WebSocket** page, publish multiple messages to the topic ` upstream_topic`, and EMQX persists the message list to the `mqtt_msg` table:

![image20181119110712267.png](https://static.emqx.net/images/4dd20d779080afab2edf46a9421ee341.png)

>Only QoS 1 2 message persistence is supported for the time being.




## MQTT retain message persistence

### Configuration item

Open the configuration file and configure the Backend rule:

```bash
## Enable the following rules at the same time and start retain persistence for three life cycles

## When a non-empty retain message is published (stored)
backend.mysql.hook.message.publish.2     = {"topic": "#", "action": {"function": "on_message_retain"}, "pool": "pool1"}

## Query retain message when device subscribes to topic
backend.mysql.hook.session.subscribed.2  = {"topic": "#", "action": {"function": "on_retain_lookup"}, "pool": "pool1"}

## When an empty retain message is published (cleared)
backend.mysql.hook.message.publish.3     = {"topic": "#", "action": {"function": "on_retain_delete"}, "pool": "pool1"}

```



### Example

After establishing a connection on the **WebSocket** page of the EMQX management console, publish the message and select **Retain**:

![WechatIMG2691.png](https://static.emqx.net/images/85f3ecea4d45b295e72fa9d51c160917.png)



**Publish（Message is not empty）**

When a non-empty retain message is published, EMQX will use topic as the unique key to persist the message to the `mqtt_retain` table. Different retain messages will be published under the same topic. Only the last message will be persisted:

![image20181119164153931.png](https://static.emqx.net/images/5b0f0c250f7d518cb2d16e8cbbe0b424.png)

**Subscribe**

After the client subscribes to the retain topic, EMQX will query the `mqtt_retain` data table to perform the post operation of retain message .



**Publish (message is empty)**

In the [MQTT protocol](https://www.emqx.com/en/mqtt), publishing an empty retain message will clear the retain record. At this time, the retain record will be deleted from the `mqtt_retain` table.



## Message acknowledgement persistence

When message acknowledgement (ACK) persistence is enabled and a MQTT client subscribes to QoS 1 and QoS 2 topics, EMQX will initialize the ACK record in the database with clientid + topic as the unique key.

### Configuration item

Open the configuration file and configure the backend rule. Use the **topic wildcard** to filter the messages to be applied:

```bash
## Initialize ACK records when subscribing
backend.mysql.hook.session.subscribed.1  = {"topic": "#", "action": {"function": "on_message_fetch"}, "pool": "pool1"}


## Update arrival status when message arrives
backend.mysql.hook.message.acked.1       = {"topic": "#", "action": {"function": "on_message_acked"}, "pool": "pool1"}

## Delete record rows when unsubscribing
backend.mysql.hook.session.unsubscribed.1= {"topic": "#", "action": {"sql": ["delete from mqtt_acked where clientid = ${clientid} and topic = ${topic}"]}, "pool": "pool1"}
```



### Example

After establishing a connection in the EMQX Management Console **WebSocket** page, subscribe to topics with QoS> 0:

![WechatIMG2693.png](https://static.emqx.net/images/b9bd87a9a0908f4bb049886f657208e1.png)



At this point, the `mqtt_acked` table will be inserted with the initialization data row. At each time a message with a QoS> 0 is published to the topic , the data row mid will increase by 1 when the message arrives:

![image20181119140354855.png](https://static.emqx.net/images/f6a175ec34896406b5e2add4ec8d8e99.png)

> Topics in the agent subscription that satisfy QoS> 0 will also initialize the records, and the related records will be deleted after the client cancels the subscription.





## Custom SQL

In addition to the built-in functions and table structure of the plugin, emqx_backend_pgsql also supports custom SQL statements. By using template syntax such as `${clientid}` to dynamically construct SQL statements, it can implement operations such as client connection history and updating custom data tables.

### SQL statement parameter description

| hook                 | Available parameters                 | Example ($ (name) in the SQL statement indicates the available parameters) |
| -------------------- | ------------------------------------ | ------------------------------------------------------------ |
| client.connected     | clientid                             | insert into conn(clientid) values(${clientid})               |
| client.disconnected  | clientid                             | insert into disconn(clientid) values(${clientid})            |
| session.subscribed   | clientid, topic, qos                 | insert into sub(topic, qos) values(${topic}, ${qos})         |
| session.unsubscribed | clientid, topic                      | delete from sub where topic = ${topic}                       |
| message.publish      | msgid, topic, payload, qos, clientid | insert into msg(msgid, topic) values(\${msgid}, ${topic})    |
| message.acked        | msgid, topic, clientid               | insert into ack(msgid, topic) values(\${msgid}, ${topic})    |
| message.delivered    | msgid, topic, clientid               | insert into delivered(msgid, topic) values(\${msgid}, ${topic}) |



### Example of MQTT client connection log

The structure of the design table is as follows:

```sql
CREATE TABLE `mqtt`.`connect_logs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `clientid` VARCHAR(255) NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP, -- log time
  `state` INT NOT NULL DEFAULT 0,  -- log type： 0 offline 1 online
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

Custom SQL：

```bash
## Configure custom SQL in connected hook
## You can configure multiple SQL statements "SQL": ["sql_a", "sql_b", "sql_c"]

## When connecting
backend.mysql.hook.client.connected.3 = {"action": {"sql": ["insert into connect_logs(clientid, state) values(${clientid}, 1)"]}, "pool": "pool1"}

## When disconnecting
backend.mysql.hook.client.disconnected.3 = {"action": {"sql": ["insert into connect_logs(clientid, state) values(${clientid}, 0)"]}, "pool": "pool1"}
```



When the MQTT client goes online or offline, it will fill in and execute the preset SQL statement, and write the connection log to `connect_logs` table:

![image20181119154828728.png](https://static.emqx.net/images/529c2fa0048d7306ba55ae002ee6f82a.png)




## Advanced options

```bash
backend.mysql.time_range = 5s

backend.mysql.max_returned_count = 500
```




## Summary

The reader can use MySQL to expand related applications after understanding the stored data structures in MySQL, and custom SQL.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
