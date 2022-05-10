## Cassandra introduction and installation

Cassandra is an open source distributed database system from Apache that supports **linear extension**, **high availability** without losing the original read and write performance. At present, it is widely used in the back-end services of large enterprises, such as Netflix, Apple and so on, which have deployed thousands of nodes.



Installation Reference of Cassandra：https://cassandra.apache.org/doc/latest/getting_started/installing.html



## Principle overview

By configuring the rules engine, EMQX stores messages that meet certain criteria under a given topic into the Cassandra database. The message flow diagram is as follows:
![Artboard.png](https://static.emqx.net/images/347f6b4787038e60ff443409df36b76a.png)

among them:

- PUB/SUB: Publish and subscribe processing logic for EMQX.
- Rule: IoT message rules that extract, filter, and transform data in message packet.
- Action: An action for specific execution. For example, store into databases, write Kafka, etc.



## Scenario introduction

To illustrate the use of rule engine in Cassandra database, we take the example of ``storing the vehicle state with engine speed over 8000 in Cassandra`'.

**Assume that vehicle status information is reported as follows:**

- Report topic: cmd/state/:id, the id of the topic represents the vehicle client ID

- Message body:

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22", // client ID
    "speed": 32.12, // vehicle speed
    "direction": 198.33212, // Driving direction
    "tachometer": 3211, // Engine speed, value greater than 8000 need to be stored
    "dynamical": 8.93, // Instantaneous fuel consumption
    "location": { // GPS Longitudinal and Latitude Data
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202 // Reporting time
  }
  ```



## Preparation

### Create a database

Create a `emqx_rule_engine_output` tablespace to store message data:

```bash
CREATE KEYSPACE emqx_rule_engine_output WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;
```



### Create a data table

According to the scenario requirements, create the data table `use_statistics` structure and field annotations as follows:

```sql
USE emqx_rule_engine_output;

CREATE TABLE use_statistics (
  msgid text,
  client_id text,
  speed double,
  tachometer int,
  ts int,
  PRIMARY KEY (msgid)
);
```



Confirm the existence of the data table after successful creation:

```bash
root@cqlsh:emqx_rule_engine_output> use emqx_rule_engine_output ;
root@cqlsh:emqx_rule_engine_output> desc use_statistics ;

CREATE TABLE emqx_rule_engine_output.use_statistics (
    msgid text PRIMARY KEY,
    client_id text,
    speed double,
    tachometer int,
    ts int
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
```



## Configure rule engine



### Create a resource

Open the EMQX Dashboard, go to the **Resources** page of the left menu, click the **New** button, select the Cassandra resource type to create:

![cassrescreate2x.jpg](https://static.emqx.net/images/4b22f6ad34e1d1fccf392bb7f5d2d64b.jpg)



The network environment of the nodes in the EMQX cluster may be different. After the resources are created successfully, click the **Status button ** in the list to check the connection status of each node. If the resources on the node are unavailable, check whether the configuration is correct and the network connectivity is correct, and click the **Reconnect** button to manually reconnect.


![cassresstatus2x.jpg](https://static.emqx.net/images/45a380b895ca101d9dd722eccba84306.jpg)


### Create a rule

Go to the **Rules** page on the left menu and click the **New** button to create the rule. Select the trigger event  **message release**, which is triggered when the message is published for data processing.

After selecting the trigger event, we can see the optional fields and sample SQL on the interface:

![rulecondition2x.jpg](https://static.emqx.net/images/a700543920da98477e073a5e05d6376c.jpg)

#### Screen the required fields

The rule engine uses SQL statements to process rule conditions. In this business, we need to select all the fields in `payload` separately, use the `payload.<fieldName>` format to select, and also also need ``topic,qos, id` information in message context. The current SQL is as follows:

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



#### Establish screening criteria

Conditional screening using the SQL statement WHERE clause, in which we need to define two conditions:

- Only cmd/state/:id topics are processed, and `topic` is filtered by using the topic wildcard `= ~': `topic = `cmd/state/+'.`
- Only tachometer > 8000 messages are processed, and `tachometer` is filtered with comparator: `payload. tachometer > 8000`

Combine the previous step to get the following SQL:

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



#### Output testing is done by using the SQL test function

With the SQL test function, we can view the current data output processed  by SQL  in real time. This function requires us to specify the simulated raw data such as payload.

The payload data is as follows, note to change the `tachometer` value to satisfy the SQL condition:

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



Click the **SQL Test** toggle button, change `topic` and `payload` to the information in the scenario, and click the **Test** button to view the data output:

![rulesqltest2x.jpg](https://static.emqx.net/images/b635b3c57aa0a9f2528c29c3fe259fbc.jpg)



The test output data is:

```json
{
  "client_id": "NXP-058659730253-963945118132721-22",
  "id": "589A429E9572FB44B0000057C0001",
  "speed": 32.12,
  "tachometer": 9001,
  "ts": 1563268202
}
```

The test output is as expected and we can proceed to the next step.



### Add a response action and store the message to Cassandra

After the input and output of SQL condition  is correct, we continue to add the corresponding action, configure to write SQL statement, and store the screening result in Cassandra.

Click the **Add** button in the response action, select the **Save data to Cassandra** action, select the resource just selected, we populate the SQL statement with the `${fieldName}` syntax, insert the data into the database, and finally click the **New** button to complete the rule creation.

The SQL configuration of the action is as follows:

```sql
INSERT INTO use_statistics (msgid, client_id, speed, tachometer, ts) VALUES (${id}, ${client_id}, ${speed}, ${tachometer}, ${ts});
```


![cassrulecreate2x.jpg](https://static.emqx.net/images/37d7961092f8690847197561d07ca8be.jpg)



## Test

### Expected results

We successfully created a rule that contains a processing action, and the expected result of action  is as follows:

1. The device reports the message to the `cmd/state/:id` topic. When the value of `tachometer` in the message exceeds 8000, it will hit SQL. The number of hits in the rule list is increased by 1;
2. A data is added to the `use_statistics` table of the Cassandra `emqx_rule_engine_output` database, the value is the same as the current message.



### Test with the Websocket tool in Dashboard

Switch to the **Tools => Websocket** page and use any information client to connect to EMQX. After the connection is successful, the **message**  card sends the following message:

- Topic: cmd/state/NXP-058659730253-963945118132721-22

- Message body:

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


![WechatIMG2206.png](https://static.emqx.net/images/f3aeefde473e6ea328bb31b313fd6b17.png)



Click the **Send** button. At this time, the value of `tachometer` in the message body satisfies the condition of `tachometer > 8000` set above. The current rule has been hit and the statistic value plus one.

View the data table records in the Cassandra command line to get the following data:
![cassruleresult2x.png](https://static.emqx.net/images/9ef015e4beb934fc94ba3581b042efa1.png)

So far, we have implemented a business development to store messages to the Cassandra database through the rules engine.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
