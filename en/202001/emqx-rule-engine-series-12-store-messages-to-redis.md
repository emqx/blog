

## Redis Introduction

Redis is a fully open source, high-performance key-value database that adheres to the BSD protocol for free.

Compared with other key-value cache products, Redis has the following characteristics:

- Redis has extremely high performance, and supports 100,000 levels of reading and writting speeds with a single machine .
- Redis supports data persistence. You can save the data in memory to disk, and it can be loaded and used again when restarting.
- Redis not only supports simple key-value type data, but also provides storage of data structures such as list, set, zset, and hash.
- Redis supports data backup in master-slave mode.

Readers can refer to Redis official Quick Start (https://redis.io/topics/quickstart) to install Redis (as of this writing, Redis version is 5.0), and use the redis-server command to start the Redis server.

## Scenario introduction

In this scenario, messages that meet the conditions under the specified topic of EMQ X need to be stored in Reids. In order to facilitate subsequent analysis and retrieval, the message content needs to be split and stored.

**The information reported by the device in this scenario is as follows:**

- Reported subject: `cmd/state/:id`, where id represents the vehicle client ID

- Message body:

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22", // Client ID
    "speed": 32.12, // vehicle speed
    "direction": 198.33212, // driving direction
    "tachometer": 3211, //Engine speed, only need to be stored when the value is greater than 8000
    "dynamical": 8.93, // Instantaneous fuel consumption
    "location": { //GPS latitude and longitude data
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202 // reporting time
  }
  ```



When the reported engine speed value is greater than `8000`, the current information is stored for subsequent analysis of user's vehicle usage.

## Configuration instructions

### Create a resource

Open EMQ X Dashboard, enter the **Resources**  page of the left menu, click the  **New** button, and enter the Redis server information to create a resource.

![s.png](https://static.emqx.net/images/84dda5c0c71dbd073ada895a83f54120.png)



The network environment of the nodes in the EMQ X cluster may be different from each other. After the resources are successfully created, click the **Status button** in the list to view the resource connection status of each node. If the resources on the nodes are not available, please check whether the configuration is correct and the network connectivity, and click the **Reconnect** button to reconnect manually.

![v.png](https://static.emqx.net/images/9b071cec91b5f05999aa13b0c66c3e35.png)



### Create a rule

Enter the **Rules** page on the left menu and click the **New** button to create a rule. Here we choose to trigger event  of **message.publish**, which means when EMQ X receives the message of PUBLISH , the rule is triggered for data processing.

After the trigger event is selected, we can see optional fields and sample SQL on the interface:

![image20190716174727991.png](https://static.emqx.net/images/b3866a53196eb9013302b244c16ed016.png)


#### Filter required fields

The rule engine uses SQL statements to process rule conditions. In this business, we need to select all the fields in the `payload` individually, use the` payload.fieldName` format to select, and also need the `topic`, ` qos`,  `id` information of the message context.  The current SQL is as follows:

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

In this business of conditional filtering using the WHERE clause of the SQL statement, we need to define two conditions:

- Only process `cmd/state/:id` topics, use topic wildcard` =~ `to filter` topic`: `topic = ~ 'cmd/state/+'`
- Only process messages with `tachometer> 8000`, use the comparator to filter` tachometer`: `payload.tachometer> 8000`

Combine the previous steps results in the following SQL:

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



#### Output test using SQL test function

With the SQL test function, we can view the current SQL processed data output in real time. This function requires us to specify the payload to simulate raw data.

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

Click the **SQL Test** toggle button, change the `topic and payload` to the information in the scenario, and click the **Test** button to see the data output:

![SQL1.png](https://static.emqx.net/images/576ed3c7454d922d42b415338d3f5fae.png)


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



### Add response action, and store message to Redis

After the SQL condition input and output are correct, we continue to add corresponding actions, configure to write SQL statements, and store the filtered results in Redis.

Click the **Add** button in the response action, select the action of **Save Data to PostgreSQL** , select the resource just selected, we use the `${fieldName}` syntax to fill the SQL statement, insert the data into the database, and finally click the **New** button to complete the rule creation.

The SQL configuration for the action is as follows:

```sql
HMSET test client_id "${client_id}" speed "${speed}" tachometer "${tachometer}" ts "${ts}" msg_id "${msg_id}"
```

Create a hash table using Redis' hash table structure with message id as the name of the table.

![WX201907181049302x.png](https://static.emqx.net/images/1dc598bb55cc60056914e8021bfeb116.png)


## Test

#### Expected outcome

We have successfully created a rule that contains a processing action. The expected outcome of the action is as follows:

1. When the device reports a message to the topic `cmd/state/:id`, and the value of ` tachometer` in the message exceeds 8000, it will hit SQL, and the number of **hits** in the rule list will increase by 1;
2. Redis will add a hash table named with the current message id , and the value is the same as the current message.



#### Test with Websocket tools in Dashboard

Switch to the **Tools ->  Websocket**  page, use any information client to connect to EMQ X. After the connection is successful, send the following message in the  **message** card:

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
![image20190716190238252.png](https://static.emqx.net/images/263afcad19634033c8294d806173d74f.png)



Click the **Send** button, and we can see that the number of hits of the current rule has changed to 1.

The data obtained by viewing the hash table records on the Redis command line is as follows:

![WX201907181142402x.png](https://static.emqx.net/images/ea5cf04f77cbbc8b76d58965a4ba856a.png)

So far, we have used the rule engine to implement business development to store messages to Reids.


