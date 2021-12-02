## Concept of Bridge

Bridge is a way to connect multiple EMQ X or other MQTT message middleware. Unlike clusters, topic trees and routing tables are not replicated between nodes operating in bridge mode. What the bridge mode does is:

- Forward messages to the bridge node according to the rules;
- Subscribe to the topic from the bridge node and forward the message in the node/cluster after receiving the message.

![WX20191108094216.png](https://static.emqx.net/images/ec8720b15fa3ce2f51b1549fa04f9ab6.png)

There are different application scenarios for working in the bridge mode and working in the cluster mode. The bridge can complete some functions that cannot be realized by using the cluster alone:

- Deploy across VPCs. Since the bridge does not need to duplicate the topic tree and the routing table, the requirements for network stability and delay are lower than those of the cluster. Different nodes in the bridge mode can be deployed on different VPCs, and the client can select physically close node for connections, so as to improve the coverage of the entire application.
- Support for heterogeneous nodes. Since the essence of bridge is the forwarding and subscription of messages, in theory, all message middleware supporting the MQTT protocol can be bridged to EMQ X. Even for some message services using other protocols, if there is a protocol adapter, the message can also be forwarded through the bridge.  
- Increase the service limit for individual application. Due to internal overhead, a single EMQ X has a upper limit  of nodes. If multiple clusters are bridged and bridging rules is designed according to the business requirements, the application's service limit can be increased by one level.

In a specific application, a bridged originating node can be approximated as a client of a remote node.



## Scenario introduction

This scenario requires bridging messages under EMQ X specified topics and satisfying conditions to EMQ X or other MQTT Broker.

**Reporting information on the device side in this scenario is as follows: **

- Reported topic: cmd/state/:id,  id for vehicle client ID

- Message body:

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22", // Client identification code
    "speed": 32.12, // vehicle speed
    "direction": 198.33212, // Driving direction
    "tachometer": 3211, // Engine speed, which is required for storage  when the value is greater than 8000
    "dynamical": 8.93, // Instantaneous fuel consumption
    "location": { // GPS Latitude and longitude data
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202 // Reporting time
  }
  ```

When the reported data of engine speed value is greater than `8000`,  part of the data  is bridged to the designated server.



## Bridging EMQ X to Mosquitto 

### Preparation

#### Modify `mosquitto.conf`

In order to avoid port conflicts with the local emqx, temporarily modify the local port number of mosquitto.

```bash
port 1882
```

#### Start `mosquitto`

```bash
$ mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
```

### Configuration instructions

#### Create a resource

Open EMQ X Dashboard, go to the **Resources** page on the left menu, click the **New** button, type Mosquitto server information to create a resource.

![image01.jpg](https://static.emqx.net/images/c1c7f02109bc77b9df69011b67e27ac2.jpg)

The network environment of the nodes in the EMQ X cluster may not be connected to each other. After the resource is created successfully, click the **Status button ** in the list to check the resource connection status of each node. If the resources on the node are unavailable, check whether the configuration is correct and the network connectivity is correct, and click the **Reconnect** button to manually reconnect.

![image02.jpg](https://static.emqx.net/images/169d0ba48bab14af6b496cbb403b5446.jpg)


#### Create a rule

Go to the **Rules** page on the left menu and click the **New** button to create the rule. Select the trigger event **message publish**, which is triggered when the message is published for data processing.

After selecting the trigger event, we can see the optional fields and sample SQL on the interface:

![image03.jpg](https://static.emqx.net/images/92b57950543da05e7c9981199e28d07b.jpg)

#### Filter the required fields

The rule engine uses SQL statements to process rule conditions. In this business, we need to select all the fields in `payload` separately with  `payload.fieldName` format, and also need the `topic`, `qos`, `id ` information of message context. The current SQL is as follows:

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

#### Establish filtration criteria

Conditional filtering is done by using the SQL statement WHERE clause, in which we need to define two conditions:

- Only handle `cmd/state/:id` topic, and use the topic wildcard `=~` to filter `topic`: `topic =~ 'cmd/state/+'
- Only handle `tachometer > 8000` messages, and use the comparator to filter `tachometer`: `payload.tachometer > 8000`

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

#### Output testing is done by using SQL test function

With the SQL test function, we can view the current SQL processed data output in real time. This function requires us to specify the simulated raw data such as payload.

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

Click the **SQL Test** toggle button, change `topic` and `payload` to be the information in the scene, and click the **Test** button to check the data output:

![image04.jpg](https://static.emqx.net/images/a33a26df264dc3eee90aaf958e49a398.jpg)

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

#### Add a response action, bridge the message to Mosquitto

After the SQL condition input and output is correct, we continue to add the  response action, configure to write SQL statement, and bridge the filter result to Mosquitto.

Click the **Add** button in the response action, select the **Bridge data to MQTT Broker** action, and select the resource just selected.

![image05.jpg](https://static.emqx.net/images/9d2912218ef2cc86c949c46302316145.jpg)

### Test

#### The expected results

We successfully created a rule that contains a processing action, and the expected result of the action is as follows:

1. When the device reports a message to the `cmd/state/:id` topic, it will hit SQL when the value of `tachometer` in the message exceeds 8000, and the number of **hits** in the rule list is increased by 1;
2. The Mosquitto subscriber will receive a piece of data with the same value as the current message.

#### Test with the Websocket tool in Dashboard

Switch to the **Tools** --> **Websocket** page, use any information client to connect to EMQ X. After the connection is successful, the **message**  card sends the following information:

- Topic: cmd/state/NXP-058659730253-963945118132721-22
- Message body:

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

![image06.jpg](https://static.emqx.net/images/fd95228a9f6b28120b79f3c06c494daa.jpg)

Click the **send** button  , after sending successfully, the statistical value of  current rule hit is 1.

View the data table records in the command line to get the following data:

![image07.png](https://static.emqx.net/images/1631addf2ba5dbf56a2b5518d07aaea8.png)

So far, we have implemented business development using the rules engine to bridge messages to the MQTT Broker through the rules engine.



## RPC bridging

### Preparation

Prepare another emqx node and enable two emqx.

### Configuration instructions

#### Create a resource

Open EMQ X Dashboard, go to the **Resources** page on the left menu, click the **New** button, type EMQ X server information for resource creation.

![image01.jpg](https://static.emqx.net/images/b039915b5a3344cd31d6ac2b90258749.jpg)

The network environment of the nodes in the EMQ X cluster may not be connected to each other. After the resource is created successfully, click the **Status button ** in the list to check the resource connection status of each node. If the resources on the node are unavailable, check whether the configuration is correct and the network connectivity is correct, and click the **Reconnect** button to manually reconnect.

![image02.jpg](https://static.emqx.net/images/e8a1e9b8fe12623ee6e66419ebb031d3.jpg)

#### Create a rule

Go to the **Rules** page on the left menu and click the **New** button to create the rule. Select the trigger event **message publish**, which is triggered when the message is published for data processing.

After selecting the trigger event, we can see the optional fields and sample SQL on the interface:

![image03.jpg](https://static.emqx.net/images/78e78b1e5aea8c76388a066ab7f727b4.jpg)

#### Filter the required fields

The rule engine uses SQL statements to process rule conditions. In this business, we need to select all the fields in `payload` separately with  `payload.fieldName` format, and also need the `topic`, `qos`, `id ` information of message context. The current SQL is as follows:

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

#### Establish filtration criteria

Conditional filtering is done by using the SQL statement WHERE clause, in which we need to define two conditions:

- Only handle `cmd/state/:id` topic, and use the topic wildcard `=~` to filter `topic`: `topic =~ 'cmd/state/+'
- Only handle `tachometer > 8000` messages, and use the comparator to filter `tachometer`: `payload.tachometer > 8000`

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

#### Output testing is done by using SQL test function

With the SQL test function, we can view the current SQL processed data output in real time. This function requires us to specify the simulated raw data such as payload.

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

Click the **SQL Test** toggle button, change `topic` and `payload` to be the information in the scene, and click the **Test** button to check the data output:

![image04.jpg](https://static.emqx.net/images/67b7f260a34ac11be15247850bd5af74.jpg)

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

#### Add a response action, bridge the message to another EMQ X

After the SQL condition input and output is correct, we continue to add the  response action, configure to write SQL statement, and bridge the filter result to another EMQ X.

Click the **Add** button in the response action, select the **Bridge data to MQTT Broker** action, and select the resource just selected.

![image05.jpg](https://static.emqx.net/images/5eeab650e0640cc46edaad9138f0000e.jpg)



### Test

#### The expected results

We successfully created a rule that contains a processing action, and the expected result of the action is as follows:

1. When the device reports a message to the `cmd/state/:id` topic, it will hit SQL when the value of `tachometer` in the message exceeds 8000, and the number of **hits** in the rule list is increased by 1;
2. The EMQ X subscriber will receive a piece of data with the same value as the current message.

#### Test with the Websocket tool in Dashboard

Switch to the **Tools** --> **Websocket** page, use any information client to connect to EMQ X. After the connection is successful, the **message**  card sends the following information:

- Topic: cmd/state/NXP-058659730253-963945118132721-22
- Message body:

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

![image16.jpg](https://static.emqx.net/images/7716752ea559b750d4fa86a2a0aa3a6f.jpg)

Click the **send** button  , after sending successfully, the statistical value of  current rule hit is 1.

View the data table records in the command line to get the following data:

![image17.png](https://static.emqx.net/images/1f7d506e2efc9990008d2d1eba0356f3.png)



So far, we have implemented business development using the rules engine bridge message through the rules engine.
