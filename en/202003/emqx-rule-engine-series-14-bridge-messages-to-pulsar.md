##  Introduction to the Pulsar messaging system

Apache Pulsar is an enterprise-level pub-sub messaging system. Pulsar aims to replace Apache Kafka's dominance for many years. Pulsar provides faster throughput and lower latency than Kafka in many scenarios, and provides developers with a set of compatible  APIs.

Pulsar combines high-performance streams and flexible traditional queues into a unified message model and API to synchronize flow processing with queue processing.

For the installation and use of Pulsar, please refer to [Pulsar's website](https://pulsar.apache.org/). For more information about Pulsar's introduction and comparison of bridging solutions, please see:[compared with Kafka, what's good about Pulsar as a Big Data Analysis Rookie](https://www.infoq.cn/article/1UaxFKWUhUKTY1t_5gPq)

## Scenario introduction

In this scenario, it is required to bridge messages under the EMQ X specified topic that meet the criteria to the Pulsar . To facilitate subsequent analysis and retrieval, the message content needs to be split.

 **In this scenario, the information reported by the device is as follows:**

- reported topic: cmd/state/:id，Id in the topic represents the vehicle client identifier

- Message body:

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22", // client identifier
    "speed": 32.12, // vehicle speed
    "direction": 198.33212, // Driving direction
    "tachometer": 3211, // Engine speed, which only need to be stored when the value is greater than 8000
    "dynamical": 8.93, // Instantaneous fuel consumption
    "location": { // GPS Latitude and longitude data
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202 // Reporting time
  }
  ```

When the reported engine speed value is greater than `8000`, the current information is stored for subsequent analysis of vehicle usage.

## Preparation

### Create Pulsar topic

Create `emqx_rule_engine_output` topic:

```bash
./bin/pulsar-admin topics create-partitioned-topic -p 5 emqx_rule_engine_output
```

## Configuration instructions

### Create resources

Open EMQ X Dashboard, enter the **Resources** page on the left menu, click the **New** button, and enter the Pulsar server information for resource creation.

![WX201907181431432x.png](https://static.emqx.net/images/af365bd26f541a96206563aa2bdb548a.png)



The network environment of the nodes in the EMQ X cluster may be different from each other. After the resources are successfully created, click the  **Status button**  in the list to view the resource connection status of each node. If the resources on the nodes are not available, please check whether the configuration is correct and the network connectivity is OK, and click the **Reconnect**  button to reconnect manually.

![WX201907181432172x.png](https://static.emqx.net/images/3734b43f894d65884c4bcc6e132b247f.png)



### Create rules

Enter the **Rules** page on the left menu and click the **New** button to create a rule. Here we choose **Message publish** as the trigger event , and trigger the rule for data processing when the message is published.

After the trigger event is selected, we can see optional fields and sample SQL on the interface:

![image20190716174727991.png](https://static.emqx.net/images/0782fbb63d51c05cf947fb3aa28834e9.png)



#### Filter the required field

The rule engine uses SQL statements to process rule conditions. In this business, we need to select all the fields in the `payload` individually, use the ` payload.fieldName` format to select, and also need the message context information of `topic`, `qos`, `id`. the current SQL is as follows:

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



#### Establish filtering conditions

Conditional filtering is done by using the WHERE clause of the SQL statement. In this business we need to define two conditions:

- Only process `cmd/state/:id` topics, use topic wildcard` =~` to filter  topic: `topic =~'cmd/state/+'`
- Only process messages with `tachometer>8000`, use the comparator to filter ` tachometer`: `payload.tachometer>8000`

Combine the previous step to get the SQL as follows:

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



#### Output test is done by using SQL test function

With the SQL test feature, we can view the data output of the current SQL processing in real time, which requires us to specify payloads to simulate the raw data.

The payload data is as follows, pay attention to changing the value of `tachometer` to meet the SQL conditions:

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



Click the **SQL Test** toggle button, change the `topic` and `payload` to be the information in the scenario, and click the **Test** button to see the data output:

![image20190716184242159.png](https://static.emqx.net/images/13907e261529a96d3d26e475453ce701.png)



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



### Add response action, and bridge message to Pulsar

After the SQL condition input and output are correct, we continue to add response actions, configure to write SQL statements, and bridge the filtering results to Pulsar.

Click the **Add** button in the response action, select the action of **Bridge data to Pulsar**, select the resource just selected, and fill in the Pulsar topic with the `emqx_rule_engine_output`  created above

![WX201907181433432x.png](https://static.emqx.net/images/7e092a65d7891f352e7d818860109154.png)



## Test

#### Expected result

We have successfully created a rule that contains a processing action. The expected result of the action is as follows:

1. When the device reports a message to the topic `cmd/state/:id`, and the value of` tachometer` in the message exceeds 8000, it will hit SQL, and the number of **hits** in the rule list will increase by 1;
2. Pulsar's `emqx_rule_engine_output` topic will add a piece of message with the same value as the current message.

#### Test with Websocket tools in Dashboard

Switch to the **Tools ->  Websocket** page, use any information client to connect to EMQ X. After the connection is successful, send the following information in the **Message**  card:

- Topic: cmd/state/NXP-058659730253-963945118132721-22

- Message  body:

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



![image20190716190238252.png](https://static.emqx.net/images/c44066c3b547e6e609e9f0563de0220e.png)



Click the **Send** button to see that the hit statistics for current rule is 1.

Then, use the Pulsar command to see if the message was successfully produced:

```
./bin/pulsar-client consume emqx_rule_engine_output -s "sub-name" -n 1000
----- got message -----
{"client_id":"NXP-058659730253-963945118132721-22","id":"58DEEDE7CF3D4F440000019CA0003","speed":32.12,"tachometer":8081,"ts":1563268202}
```

So far, we have implement business development of using the rules engine to bridge messages to Pulsar.

------

Welcome to our open source project [github.com/emqx/emqx](https://github.com/emqx/emqx). Please visit the [ documentation](https://docs.emqx.io) for details.
