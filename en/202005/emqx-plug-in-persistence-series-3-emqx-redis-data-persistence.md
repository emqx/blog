## Introduction to EMQX Data Persistence

The main usage scenarios of data persistence include recording the client's online and offline status, subscribing topic information, message content and operations of sending message receipt after the message arrives to various databases such as Redis, MySQL, PostgreSQL, directing, Cassandra, AWS DynamoDB, which helps the external service query quickly or retaining the current running status in the service outage/client abnormal offline period, and restoring the previous status when the connection is restored. Persistence can also be used for the client proxy subscription. When the device client goes online, the persistence module directly loads the preset topic from the database and completes the proxy subscription, reduces the complexity of system design and reduces the communication cost of client subscription.

Users can also implement similar functions by subscribing to related topics. However, these persistent supports built into the enterprise version are more efficient and reliable, which greatly reduce the developer's workload and improves system stability.

> Data persistence is an important  EMQX function and only supported in the Enterprise Version.



## Persistence design

The principle of persistence is to call the processing function (action) when the configuration event hook is triggered. After the processing function obtains the corresponding data, it processes according to the configured instructions to implement the addition, deletion, modification and checking of the data. The same event hooks have the same available parameters in different databases, but the processing function (action) will be different because of the different database characteristics. The overall persistence mode and process is as follows:

### One-to-one message storage

![backends_1.png](https://assets.emqx.com/images/0edbae21eb4896cb464dee52e7d3ce5b.png)

1. PUB publishes a message;
2. Backend records the message in the database;
3. Subscribe to the topic;
4. Backend gets the message of the topic from the database;
5. Send a message to the Subscriber;
6. After the Subscriber confirms, Backend removes the message from the database;



### One-to-many message storage

![backends_2.png](https://assets.emqx.com/images/f275b5024c3abf8102b388817c0cc134.png)

1. PUB publishes a message;

2. Backend records the message in the database;

3. SUB1 and SUB2  subscribe to topics;

4. Backend gets the message of the topic from the database;

5. Send the message to SUB1 and SUB2;

6. Backend records the location of the SUB1 and SUB2 read messages, as the  starting location when getting the message next time.

    

##  Redis Data persistence

This article uses practical examples to describe how to store relevant information through Redis.

Redis is a high-performance key-value database that is fully open source for free and obeys the BSD protocol.

Redis has the following characteristics compared to other key-value cache products:

- Redis has extremely high performance and supports 100,000-level read and write speeds in a single machine.
- Redis supports data persistence. It can save the data in memory to disk and load it again when it is restarted.
- Redis not only supports simple key-value data, but also provides storage for data structures such as list, set, zset, and hash.
- Redis supports backup of data, which is data backup in master-slave mode.

Readers can refer to Redis official [Quick Start](https://redis.io/topics/quickstart) to install Redis (at the time of writing this article, Redis version is 5.0), and start the Redis server through the `redis-server` command.



### Configure EMQX Enterprise server

In terms of the [EMQX Enterprise](https://www.emqx.com/en/products/emqx) installed via RPM, the Redis-related configuration files are located in `/etc/emqx/plugins/emqx_backend_redis.conf`. If only test Redis persistence function, most configurations do not need to be changed. The only place that needs to be changed is the Redis server address: If the Redis installed by the reader is not on the same server as EMQX, please specify the correct Redis server address and port. As shown in the  following:

```bash
## Redis Server 127.0.0.1:6379, Redis Sentinel: 127.0.0.1:26379
backend.redis.pool1.server = 127.0.0.1:6379
```

Remain the rest of the configuration file unchanged and start the plugin:

```bash
emqx_ctl plugins load emqx_backend_redis
```



## MQTT Client online status storage

When the client is online or offline, update the online status, online or offline time, and update the node client list to the Redis database.

Although [EMQX](https://www.emqx.com/en) itself provides the device online status API, it is more efficient to obtain the record directly from the database than to call the EMQX API in the scenarios that the client online status and online/offline time need to be obtained frequently.


### Configuration item

Open the configuration file and configure the Backend rule:

```bash
## Online
backend.redis.hook.client.connected.1    =  { "action": { "function": "on_client_connected" }, "pool": "pool1"}

## Offline
backend.redis.hook.client.disconnected.1 = {"action": {"function": "on_client_disconnected"}, "pool": "pool1"}
```

### Example

Open  `http://127.0.0.1:18083` EMQX management console from the browser, and create a new client connection in **Tools** -> **Websocket**, specifying clientid as sub_client:

![31.png](https://assets.emqx.com/images/26b00b949463fe0c824c70342f90d04a.png)

Open the `redis-cli` command line window and execute the command `keys *`. The result is as shown below. The reader can see that Redis store two keys:

```bash
127.0.0.1:6379> keys *
1) "mqtt:node:emqx@127.0.0.1"
2) "mqtt:client:sub_client"
```



### Connection list

The plugin records the client list and connection timestamp information under nodes by using the key which format is `mqtt:node:{node_name}`.The equivalent operation is as follows:

```bash
## redis key is mqtt:node:{node_name}
HMSET mqtt:node:emqx@127.0.0.1 sub_client 1542272836
```

Fields description:

```bash
## Online device information under the node
127.0.0.1:6379> HGETALL mqtt:node:emqx@127.0.0.1
1) "sub_client1" # clientid
2) "1542272836" # Timestamp of online time
3) "sub_client"
4) "1542272836"
```



### Connection details

The plug records the online status and online time of the client by using the key which format is 'mqtt: client: {client {ID}'. Equivalent operation is as follows:

```bash
## redis key is mqtt:client:{client_id}
HMSET mqtt:client:sub_client state 1 online_at 1542272854
```

Fields description:

```bash
## Client online status
127.0.0.1:6379> HGETALL mqtt:client:sub_client
1) "state"
2) "0" # 0 offline 1 online
3) "online_at"
4) "1542272854" # online timestamp
5) "offline_at"
6) "undefined" # offline timestamp
```



## Client proxy subscription

When the client goes online, the storage module reads the preset subscription list directly from the database, and will proxy loading the subscription topic. In the scenario that the client needs to communicate through a preset topic (receiving message), the application can set/change the proxy subscription list from the data layer.

### Configuration item

Open the configuration file and configure the Backend rule:

```bash
## hook: client.connected
## action/function: on_subscribe_lookup
backend.redis.hook.client.connected.2    = {"action": {"function": "on_subscribe_lookup"}, "pool": "pool1"}
```

### Example

When the `sub_client` device goes online, it needs to subscribe the two QoS 1 topics (`sub_client/upstream` and `sub_client/downlink`):

1. The plugin initializes the proxy subscription to Hash in Redis by using the key which format is `mqtt:sub:{client_id}`:

```bash
## redis key is mqtt:sub:{client_id}
## HSET key {topic} {qos}
127.0.0.1:6379> HSET mqtt:sub:sub_client sub_client/upstream 1
(integer) 0

127.0.0.1:6379> HSET mqtt:sub:sub_client sub_client/downlink 1
(integer) 0
```

2. In the EMQX management console **websocket** page, create a new client connection by using the clientid `sub_client`  and switch to the **subscription** page. It can be seen that the current client automatically subscribes the two QoS 1 topics (`sub_client/upstream` and `sub_client/downlink`):

![111111.png](https://assets.emqx.com/images/f1c77641b0ed3cd43c20173002351bc6.png)




3. Switch back to the management console **WebSocket** page and publish the message to the topic `sub_client/downlink`. You can receive the published message in the message subscription list. 



## Persist publishing message

### Configuration item

Open the configuration file, configure the Backend rule. The `topic` parameter is supported for message filtering. We use the `#` wildcard to store arbitrary topic message here:

```bash
## hook: message.publish
## action/function: on_message_publish

backend.redis.hook.message.publish.1 = {"topic": "#", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```



### Example

In the EMQX management console **WebSocket** page, use clientid `sub_client` to establish the connection and publish multiple messages to the topic `upstream_topic`. For each message, EMQX will persists the two records(the message list and the message details).



### Message list

EMQX persists the message list as the message id to the `mqtt:msg:{topic}` Redis collection:

```bash
## Obtain all message id in the upstream_topic topic collection
127.0.0.1:6379> ZRANGE mqtt:msg:upstream_topic 0 -1
1) "2VFsyhDm0cPIQvnY9osj"
2) "2VFszTClyjpVtLDLrn1u"
3) "2VFszozkwkYOcbEy8QN9"
4) "2VFszpEc7DfbEqC97I3g"
5) "2VFszpSzRviADmcOeuXd"
6) "2VFszpm3kvvLkJTcdmGU"
7) "2VFt0kuNrOktefX6m4nP"
127.0.0.1:6379>
```



### Message details

Each message detail will be stored in Redis Hash as the key in `mqtt:msg:{message_id}` format:

```bash
## Obtain the message details with the message id of 2VFt0kuNrOktefX6m4nP
127.0.0.1:6379> HGETALL mqtt:msg:2VFt0kuNrOktefX6m4nP
 1) "id"
 2) "2VFt0kuNrOktefX6m4nP" ## message id
 3) "from"
 4) "sub_client" ## client id
 5) "qos"
 6) "2"
 7) "topic"
 8) "up/upstream_topic"
 9) "payload"
10) "{ \"cmd\": \"reboot\" }"
11) "ts"
12) "1542338754" ## pub timestamp
13) "retain"
14) "false"
```



## Get offline messages

### Configuration item

Open the configuration file and configure the Backend rule:

```bash
## hook: session.subscribed
## action/function: on_message_fetch_for_queue、on_message_fetch_for_pubsub

## One-to-one offline message
backend.redis.hook.session.subscribed.1  = {"topic": "queue/#", "action": {"function": "on_message_fetch_for_queue"}, "pool": "pool1"}

## One-to-many offline message
backend.redis.hook.session.subscribed.2  = {"topic": "pubsub/#", "action": {"function": "on_message_fetch_for_pubsub"}, "pool": "pool1"}

```



### Example

The MQTT offline message need to meet the following conditions:

1. Connect with clean_session = false
2. Subscribe to QoS > 0
3. Publish QoS > 0

Establish a connection in the EMQX management console with the following configuration:

![WX20200515175900.png](https://assets.emqx.com/images/9cfc2151a8641d0d2697ad0baef2c57b.png)



## MQTT retain message persistence

### Configuration item

Open the configuration file and configure the Backend rule:

```bash
## hook: message.publish
## action/function: on_client_connected、on_message_retain

backend.redis.hook.message.publish.2     = {"topic": "#", "action": {"function": "on_message_retain"}, "pool": "pool1"}

backend.redis.hook.message.publish.3     = {"topic": "#", "action": {"function": "on_retain_delete"}, "pool": "pool1"}
```

### Message list

EMQX persists the message list as the message id to `mqtt:retain:{topic}` Redis Hash:

```bash
## Obtain all the message id in the upstream_topic topic collection
127.0.0.1:6379> ZRANGE mqtt:retain:upstream_topic 0 -1
1) "2VFsyhDm0cPIQvnY9osj"
127.0.0.1:6379>
```



### Message details

Each message detail will be stored in Redis Hash as the key in `mqtt:msg:{message_id}` format:

```bash
## Obtain the message details with the message id of 2VFt0kuNrOktefX6m4nP
127.0.0.1:6379> HGETALL mqtt:msg:2VFt0kuNrOktefX6m4nP
 1) "id"
 2) "2VFt0kuNrOktefX6m4nP" ## message id
 3) "from"
 4) "sub_client" ## client id
 5) "qos"
 6) "2"
 7) "topic"
 8) "up/upstream_topic"
 9) "payload"
10) "{ \"cmd\": \"reboot\" }"
11) "ts"
12) "1542338754" ## pub timestamp
13) "retain"
14) "false"
```



## Summary

The reader can read related information by using various [Redis client](https://redis.io/clients)  after understanding the data structure stored in Redis.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
