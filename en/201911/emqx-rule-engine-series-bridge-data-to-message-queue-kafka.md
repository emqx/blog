The EMQX 3.2 version introduces the ''Rules Engine'' feature that supports screening data reported by the EMQX Broker terminal, which is processed and streamed to the back-end database or other [message queues](https://www.emqx.com/en/blog/mqtt5-feature-inflight-window-message-queue). This article uses a specific scenario to explain "How to use the rules engine to forward messages to Kafka"



## Scenario introduction

This scenario requires bridging the message under the topic specified by EMQX and satisfying the condition to Kafka. In order to facilitate subsequent analysis and retrieval, the message content needs to be split.

**The information reported by the device in this scenario is as follows:**

- Reported topic: cmd/state/:id, the topic id represents the vehicle client ID

- Message body:

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22", // Client identification code
    "speed": 32.12, // Vehicle speed
    "direction": 198.33212, // Drive direction
    "tachometer": 3211, // Engine speed, storage is required when the value is greater than 8000
    "dynamical": 8.93, // Instantaneous fuel consumption
    "location": { // GPS Latitude and longitude data
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202 // Reporting time
  }
  ```



When the reported value of engine speed  is greater than `8000', the current information is stored for subsequent analysis of the user's vehicle usage.



## Preparation

### Create Kafka topic

```bash
./bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --topic 'emqx_rule_engine_output' --partitions 1 --replication-factor 1
```

> The topic must be created in Kafka before creating the Kafka Rule, otherwise the Kafka Rule creation fails.

## Configuration instructions

### Create resource

Open EMQX Dashboard, go to the **Resources** page on the left menu, click the **New** button, type Kafka server information for resource creation.

![WX201907181413252x.jpg](https://static.emqx.net/images/aecb8d35dc38dd3033415562f47ec306.jpg)


The network environment of the nodes in the EMQX cluster may be different. After the resources are created successfully, click the **Status button ** in the list to check the connection status of each node. If the resources on the node are unavailable, check whether the configuration is correct and the network connectivity is correct, and click the **Reconnect** button to manually reconnect.


![image20190716173259015.jpg](https://static.emqx.net/images/7fe37afb9ef62d21c330cc0c7da9772c.jpg)



### Create rule

Go to the **Rules** page on the left menu and click the **New** button to create the rule. Select the trigger event  of **publishing message**, which is triggered when the message is published for data processing.

After selecting the trigger event, we can see the optional fields and sample SQL on the interface:

![image20190716174727991.jpg](https://static.emqx.net/images/e802781b7ba9dfe7a12e11888c2531dd.jpg)



#### Filter the required fields

The rules engine uses SQL statements for processing/arranging terminal messages or connection events. In this business, we only need to filter out the key fields in `payload` for use.  We can use the `payload.<fieldname> ` format to select the fields in the payload. In addition to the contents of the payload, we also need to save the id information of the message. SQL can be configured in the following format:

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



#### Create filtering criteria

Conditional filtering can be done by using the SQL statement WHERE clause, in which we need to define two conditions:

- Only handle `cmd/state/:id` topic, use the topic wildcard `=~` to filter `topic`: `topic =~ 'cmd/state/+'
- Only handle `tachometer > 8000` messages, use the comparator to filter `tachometer`: `payload.tachometer > 8000`

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



#### Conducting output testing by using SQL test capabilities

With the SQL test function, we can view the current SQL processed data output in real time. This function requires us to specify the simulated raw data such as payload.

The payload data is as follows. Note to change the `tachometer` value to satisfy the SQL condition:

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



Click the **SQL Test** toggle button, change `topic` and `payload` to be the information in the scenario, and click the **Test** button to view the data output:
![image20190716184242159.jpg](https://static.emqx.net/images/aca92de316abf93fcea7ba541c9fc987.jpg)



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



### Add a response action, bridge the message to Kafka

After the SQL condition input and output is correct, we continue to add the corresponding action, configure the write SQL statement, and bridge the filtered result to Kafka.

Click the **Add** button in the response action, select the **Bridge data to Kafka** action, select the resource just selected, and fill the Kafka topic with the `emqx_rule_engine_output` created above.

![WX201907181416302x.jpg](https://static.emqx.net/images/e0aa5bd033c89350ecb9f0433608fd32.jpg)



## Test

#### expected outcome

We successfully created a rule that contains a processing action, and expected result is as follows:

1. The device reports to the `cmd/state/:id` topic that when the value of `tachometer` in the message exceeds 8000, it will hit SQL, and the number of hits in the rule list will increase by 1;
2. A message will be added to Kafka's `emqx_rule_engine_output` topic with the same value as the current message.



#### Test with the Websocket tool in Dashboard


Switch to the **Tools** --> **Websocket** page, use any client to connect to EMQX, after the connection is successful, sends the following information with **message** card:

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


![image20190716190238252.jpg](https://static.emqx.net/images/813fe6b0c89b9067da4b5ca6aa15cb20.jpg)



Click the **Send** button to see that the hit statistic value of the current rule is 1.

Then use the Kafka command to see if the message was produced successfully:

```
./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic emqx_rule_engine_output --from-beginning
{"client_id":"NXP-058659730253-963945118132721-22","id":"58DEE9D97711EF440000017B30002","speed":32.12,"tachometer":8081,"ts":1563268202}
```

So far, we have implemented business development of a rule engine bridging message to Kafka's through the rules engine.

The open source version of the rules engine only supports forwarding to Web Server, and the function to forward to Kafka is only available in the Enterprise Edition.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
