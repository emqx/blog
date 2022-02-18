This chapter uses  a practical example from `CentOS 7.2` to illustrate how to store related information through PostgreSQL.

As an important member of open source relational databases, PostgreSQL claims to be the most advanced open source database in the world. Compared to other open source relational databases such as MySQL, PostgreSQL is a completely community-driven open source project, maintained by more than 1,000 contributors worldwide . PostgreSQL offers a single, full-featured version, unlike MySQL, which offers multiple different community, business, and enterprise versions. PostgreSQL is based on a free BSD / MIT license, and organizations can use, copy, modify, and redistribute code by providing a copyright notice.

PostgreSQL has a number of features and is well supported in the GIS world. Its "lock-free" feature is very prominent. It supports function and condition indexes, and has a mature clustering solution. PostgreSQL also has powerful SQL programming capabilities such as statistical functions and statistical syntax support. With the Timescaledb plugin, PostgreSQL can be transformed into a fully functional time-series database, Timescaledb.


## Functions overview

- Client online status storage
- Client Agent Subscription
- Persist publishing message
- Retain message persistence
- Message acknowledgement persistence
- Custom SQL
## Install and validate PostgreSQL server

Readers can refer to PostgreSQL [Official Documentation](https://www.postgresql.org/docs/) or  [Docker](https://hub.docker.com/_/postgres/) to download and install the PostgreSQL server. This article Use PostgreSQL 10.1 version.

To facilitate the management operation, you can download and use the free graphical management software  [Postico](https://eggerapps.at/postico/) (MacOS only) or [pgAdmin](https://www.pgadmin.org/).



## Configure EMQX MQTT broker

For [EMQX MQTT broker](https://www.emqx.com/en/try) installed by RPM, the PostgreSQL related configuration file is located in `/etc/emqx/plugins /emqx_backend_pgsql.conf`. If you only test the persistence function of PostgreSQL, most of the configuration does not need to be changed. You only need to fill in the user name, password and database:

```bash
backend.pgsql.pool1.server = 127.0.0.1:5432

backend.pgsql.pool1.pool_size = 8

backend.pgsql.pool1.username = root

backend.pgsql.pool1.password = public

backend.pgsql.pool1.database = mqtt

backend.pgsql.pool1.ssl = false
```

Leave the rest of the configuration file unchanged, and then you need to start the plugin. There are two ways to start the plugin: `command line` and ` console`. The reader can choose one of them.



### Start from the command line

```bash
emqx_ctl plugins load emqx_backend_pgsql
```



### Start through the management console

In the EMQX management console **plugin** page, find **emqx_backend_pgsql** plugin, click **start**.



## Client online status storage

When the client goes online and offline, the plugin will update the online status, online time, and node client list to the PostgreSQL database.

### Data sheet

Create the mqtt_client device online status table:

```sql
CREATE TABLE mqtt_client(
  id SERIAL primary key,
  clientid character varying(100),
  state integer, -- online status: 0 offline 1 online
  node character varying(100), -- Access node name
  online_at timestamp, -- online time
  offline_at timestamp, -- offline time
  created timestamp without time zone,
  UNIQUE (clientid)
);
```



### Configuration item

Open the configuration file and configure the Backend rule:

```bash
## hook: client.connected、client.disconnected
## action/function: on_client_connected、on_client_disconnected


## Client is online
backend.pgsql.hook.client.connected.1 = {"action": {"function": "on_client_connected"}, "pool": "pool1"}

## Client is offline
backend.pgsql.hook.client.disconnected.1 = {"action": {"function": "on_client_disconnected"}, "pool": "pool1"}
```



### Example

Opens  `http://127.0.0.1:18083`  EMQX management console through the browser, create a new client connection in **Tools ->  Websocket**, specify clientid as sub_client, click on **connect**, and disconnect manually after successful connection:

![image20181116105333637.png](https://static.emqx.net/images/8cf8ae74eb385c2582a20de5593a01c6.png)



View the `mqtt_client` table, at which point a client online and offline record will be written/updated:

![Example.png](https://static.emqx.net/images/80e6e3c8f15e2fed81db294cc2023f39.png)



## Client Agent Subscription

When the client is online, the storage module directly reads the preset to-be-subscribed list from the database, and the agent loads the subscription topic. In the scenario where the client needs to communicate (receive a message) through a preset topic, the application can set / change the agent subscription list from the data level.

### Data sheet

Create mqtt_sub agent subscription relational table:

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



### Configuration item

Open the configuration file and configure the Backend rule:

```bash
## hook: client.connected
## action/function: on_subscribe_lookup
backend.pgsql.hook.client.connected.2    = {"action": {"function": "on_subscribe_lookup"}, "pool": "pool1"}
```



### Example

When the `sub_client` device goes online, it needs to subscribe to the two QoS 1 topics of `sub-client/upstream` and `sub_client/downlink` :

1. Initially insert agent subscription topic information in the `mqtt_sub` table:

```sql
insert into mqtt_sub(clientid, topic, qos) values('sub_client', 'sub_client/upstream', 1);

insert into mqtt_sub(clientid, topic, qos) values('sub_client', 'sub_client/downlink', 1);
```

2. In the EMQX management console **WebSocket** page, create a new client connection with clientid `sub_client`, switch to **subscription** page, it can be seen that the current client automatically subscribes to the two QoS 1 topics of ` sub_client/upstream` and `sub_client/downlink`:

![image20181116110036523.png](https://static.emqx.net/images/a1743eaa61d8d9bb1663541d9af8dfd8.png)




3. Switch back to the management console **WebSocket** page and publish the message to the topic `sub_client/downlink`. You can receive the published message in the message subscription list.




## Persist publishing message

### Data sheet

Create mqtt_msg MQTT message persistence table:

```sql
CREATE TABLE mqtt_msg (
  id SERIAL primary key,
  msgid character varying(60),
  sender character varying(100), -- Message pub's clientid
  topic character varying(200),
  qos integer,
  retain integer, -- whether to retain the message
  payload text,
  arrived timestamp without time zone -- message arrived time(QoS > 0)
);
```



### Configuration item

Open the configuration file, configure Backend rules, support message filtering using the `topic` parameter, and use the wildcard # to store arbitrary topic messages:

```bash
## hook: message.publish
## action/function: on_message_publish

backend.pgsql.hook.message.publish.1     = {"topic": "#", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```



### Example

In the EMQX management console **WebSocket** page, use clientdi `sub_client` to establish a connection, publish multiple messages to the topic ` upstream_topic`, and EMQX persists the message list to the `mqtt_msg` table:

![image20181119162834606.png](https://static.emqx.net/images/a025af3fa62148737f176257b3149d5b.png)

>Only QoS 1 2 message persistence is supported for the time being.




## Retain Message persistence

### Table Structure

Create the mqtt_retain Retain message storage table:

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



### Configuration item

Open the configuration file and configure the Backend rule:

```bash
## Enable the following rules at the same time and start retain persistence for three life cycles

## When a non-empty retain message is published (stored)
backend.pgsql.hook.message.publish.2     = {"topic": "#", "action": {"function": "on_message_retain"}, "pool": "pool1"}

## Query retain message when device subscribes to topic
backend.pgsql.hook.session.subscribed.2  = {"topic": "#", "action": {"function": "on_retain_lookup"}, "pool": "pool1"}

## When an empty retain message is published (cleared)
backend.pgsql.hook.message.publish.3     = {"topic": "#", "action": {"function": "on_retain_delete"}, "pool": "pool1"}

```



### Example

After establishing a connection on the **WebSocket** page of the EMQX management console, publish the message and select **Reserve**:

![image20181119111926675.png](https://static.emqx.net/images/fd9fba3a1a64f2a9b84ca7020f95e650.png)



**Publish (message is not empty)**

When a non-empty retain message is published, EMQX will use topic as the unique key to persist the message to the `mqtt_retain` table. Different retain messages will be published under the same topic. Only the last message will be persisted:

![image20181119112306703.png](https://static.emqx.net/images/8059ea91aea1da218eb6f74301687e13.png)



**Subscribe**

After the client subscribes to the retain topic, EMQX will query the `mqtt_retain` data table to perform the post operation of retain message .



**Publish (message is empty)**

In the [MQTT protocol](https://www.emqx.com/en/mqtt), publishing an empty retain message will clear the retain record. At this time, the retain record will be deleted from the `mqtt_retain` table.





## Message acknowledgemen persistence

When message acknowledgement (ACK) persistence is enabled and a client subscribes to QoS 1 and QoS 2 topics, EMQX will initialize the ACK record in the database with clientid + topic as the unique key.



### Data sheet

Create the mqtt_acked message acknowledgement table:

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



### Configuration item

Open the configuration file and configure the backend rule. Use the **topic wildcard** to filter the messages to be applied:

```bash
## Initialize ACK records when subscribing
backend.pgsql.hook.session.subscribed.1  = {"topic": "#", "action": {"function": "on_message_fetch"}, "pool": "pool1"}


## Update arrival status when message arrives
backend.pgsql.hook.message.acked.1       = {"topic": "#", "action": {"function": "on_message_acked"}, "pool": "pool1"}

## Delete record rows when unsubscribing
backend.pgsql.hook.session.unsubscribed.1= {"topic": "#", "action": {"sql": ["delete from mqtt_acked where clientid = ${clientid} and topic = ${topic}"]}, "pool": "pool1"}
```



### Example

After establishing a connection in the EMQX Management Console **WebSocket** page, subscribe to topics with QoS> 0:

![image20181119140251843.png](https://static.emqx.net/images/ae8589fa59a057fadd396ea525a30c62.png)


At this point, the `mqtt_acked` table will be inserted with the initialization data row. At each time a message with a QoS> 0 is issued to the topic , the data row mid will increase by 1 when the message arrives:

![image20181119165248998.png](https://static.emqx.net/images/9bb256e8f7d635ebdd42450cc41c6218.png)

> Topics in the agent subscription that satisfy QoS> 0 will also initialize the records, and the related records will be deleted after the client cancels the subscription.





## Custom SQL

In addition to the built-in functions and table structure of the plugin, emqx_backend_pgsql also supports custom SQL statements. By using template syntax such as `${clientid}` to dynamically construct SQL statements, it can implement operations such as client connection history and updating custom data tables.

### SQL statement parameter description

| hook                 | Available parameters                 | Example ($ (name) in the SQL statement indicates the available parameters) |
| -------------------- | ------------------------------------ | ------------------------------------------------------------ |
| client.connected     | clientid                             | insert into conn(clientid) values(${clientid})               |
| client.disconnected  | clientid                             | insert into disconn(clientid) values(${clientid})            |
| session.subscribed   | clientid, topic, qos                 | insert into sub(topic, qos) values(\${topic}, ${qos})        |
| session.unsubscribed | clientid, topic                      | delete from sub where topic = ${topic}                       |
| message.publish      | msgid, topic, payload, qos, clientid | insert into msg(msgid, topic) values(\${msgid}, ${topic})    |
| message.acked        | msgid, topic, clientid               | insert into ack(msgid, topic) values(\${msgid}, ${topic})    |
| message.delivered    | msgid, topic, clientid               | insert into delivered(msgid, topic) values(\${msgid}, ${topic}) |



### Example of Updating custom data sheet

The existing device table `clients` has basic fields such as device connection authentication, device status record, and device management for other management services. Now we need to synchronize the EMQX device status to this table:

```sql
CREATE TABLE "public"."clients" (
    "id" serial,
    "deviceUsername" varchar(50), --  MQTT username
    "client_id" varchar(50), -- MQTT client_id
    "password" varchar(50), -- MQTT password
    "is_super" boolean DEFAULT 'false', -- Whetner it is ACL super client
    "owner" int, -- Create user
    "productID" int, -- Product
    "state" boolean DEFAULT 'false', -- Online status
    PRIMARY KEY ("id")
);

-- Sample data already exists in the initialization system, at this time state is false
INSERT INTO "public"."clients"("deviceUsername", "client_id", "password", "is_super", "owner", "productID", "state") VALUES('mqtt_10c61f1a1f47', 'mqtt_10c61f1a1f47', '9336EBF25087D91C818EE6E9EC29F8C1', TRUE, 1, 21, FALSE);

```



Custom UPDATE SQL statement:

```bash
##Configure custom UPDATE SQL in connected / disconnected hook
## You can configure multiple SQL statements "SQL": ["sql_a", "sql_b", "sql_c"]

## When connecting
backend.pgsql.hook.client.connected.3 = {"action": {"sql": ["update clients set state = true where client_id = ${clientid}"]}, "pool": "pool1"}

## when disconnecting
backend.pgsql.hook.client.disconnected.3 = {"action": {"sql": ["update clients set state = false where client_id = ${clientid}"]}, "pool": "pool1"}
```



When the client goes online, it will fill in and execute the preset SQL statement, and and update the `state` field of the device online status to `true`:

![image20181119170648517.png](https://static.emqx.net/images/171fac0ca78984bc7909f1ad8ed46a87.png)



## Advanced options

```bash
backend.pgsql.time_range = 5s

backend.pgsql.max_returned_count = 500
```




## Summary

After the reader understands the data structures stored in PostgreSQL and custom SQL, they can expand related applications.
