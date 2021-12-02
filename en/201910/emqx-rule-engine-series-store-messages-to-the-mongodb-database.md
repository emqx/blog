## Introduction of MongoDB 

> Non-relational databases (NoSQL) are used for the storage of very large-scale data, such as Google or Facebook, which collects trillions of bits of data per day for their users. These types of data storage do not require a fixed pattern and can be scaled horizontally without redundant operations.

MongoDB is a product between relational database and non-relational database. Among non-relational databases, MongoDB has the most abundant functions and most resembles relational database.  MongoDB is written in C++ and is an open source database system based on distributed file storage. MongoDB is designed to provide a scalable, high-performance data storage solution for data storage. It can easily add more nodes under high load to ensure service performance.

MongoDB stores data as a document, and the data structure consists of key => value pairs. MongoDB documents are similar to JSON objects. Field values can contain other documents, arrays, and document arrays.

MongoDB download address：[https://www.mongodb.com/download-center/community](https://www.mongodb.com/download-center/community)



## Introduction of scenario

This scenario requires that messages satisfying certain conditions under the EMQ X specified topic to be stored in the MongoDB database. In order to facilitate subsequent analysis and retrieval, message content needs to be split and stored.

**In this scenario, The information reported by the device is as follows:**

- Reported topic: cmd/state/:id, the topic id represents the vehicle client ID

- Message body:

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22", // Client identification
    "speed": 32.12, // Cehicle speed
    "direction": 198.33212, // Driving direction
    "tachometer": 3211, // Engine speed, than is required to be stored when the value is greater than 8000
    "dynamical": 8.93, // Instantaneous fuel consumption
    "location": { // GPS latitude and longitude data
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202 // Time for reporting
  }
  ```

When the reported data of engine speed value is greater than `8000`, the current information is stored for subsequent analysis of the user's vehicle usage.



## Preparation

### Create administrative users

At first, log in to MongoDB with an account that has permissions to create users, and add users to `emqx_rule_engine_output`:

```bash
> use emqx_rule_engine_output;

> db.createUser({user: "root", pwd: "public", roles: [{role: "readWrite", db: "emqx_rule_engine_output"}]});
```



### Create data table

Log in with the new user and create the data set `use_statistics`:

```sql
$ mongo 127.0.0.1/emqx_rule_engine_output -uroot -ppublic

> db.createCollection("use_statistics"); 
```



Confirm the existence of the data table after successful creation:

```bash
> show collections
use_statistics
```



## Configuration instructions

### Create  resource

Open the EMQ X Dashboard, go to the **Resources** page on the left menu, click the **New** button, select the MongoDB resource type to create:

![mongrescreate2x.jpg](https://static.emqx.net/images/f5a5355598d874242fa945c932da2e05.jpg)



The network environment of the nodes in the EMQ X cluster may be different. After the resources are created successfully, click the **Status button ** in the list to check the resource connection status of each node . If the resources on the node are unavailable, check whether the configuration is correct and the network connectivity is correct, and click the **Reconnect** button to manually reconnect.

![mongresstatus2x.jpg](https://static.emqx.net/images/066ae8a4c6247e8481c39c39f97f3953.jpg)



### Create rules

Go to the **Rules** page on the left menu and click the **New** button to create the rule. Select the trigger event  **message publish**, which is triggered when the message is published for data processing.

After selecting the trigger event, we can see the optional fields and sample SQL on the interface:

![rulecondition2x.jpg](https://static.emqx.net/images/ce4640622eaa46be537dd6f96ac15253.jpg)



#### Filter the required fields

The rule engine uses SQL statements to process rule conditions. In this business, we need to select all the fields in `payload` separately, use the `payload.<fieldName>` format to select, and also need the information of `topic`, `qos`, `id` in topic context. The current SQL is as follows:

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



#### Establish filtering criteria

Using the SQL statement WHERE clause for conditional filtering, in which we need to define two conditions:

- Only handle `cmd/state/:id` topic, use the theme wildcard `=~` to filter `topic`: `topic =~ 'cmd/state/+'
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



#### Use SQL test capabilities for output testing

With the SQL test function, we can check the current SQL processed data output in real time. This function requires us to specify the simulated raw data such as payload.

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



Click the **SQL Test** switch button, change `topic` and `payload` as the information in the scenario, and click the **Test** button to check the data output:

![rulesqltest2x.jpg](https://static.emqx.net/images/3e4e10c03dfa317522b0c8608e1a9a8f.jpg)



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



### Add response action, store the message to MongoDB

When the  input and output of SQL condition is correct, we continue to add response actions, configure to write SQL statement, and store the filtered results in MongoDB.

Click the **Add** button in the response action, select the **Save data to MongoDB** action, select the resource just selected, we fill the action statement with the `${fieldName}` syntax, insert the data into the database, and finally Click the **New** button to complete the rule creation.

**Collection** is configured as: `use_statistics`

**Selector** is configured as： 

```sql
msgid=${id}, client_id=${client_id}, speed=${speed}, tachometer=${tachometer}, ts=${ts}
```



![mongrulecreate2x.jpg](https://static.emqx.net/images/e7b5bc31031d5ec42be2eacb501d993d.jpg)



## Test

#### Expected result

We successfully created a rule that contains a processing action, and the expected result of action is as follows:

1. When the device reports a message to the `cmd/state/:id` topic, it will hit SQL when the value of `tachometer` in the message exceeds 8000, and the number of hits in the rule list is increased by 1;
2. The  `use_statistics` table in MongoDB `emqx_rule_engine_output` database will  be added with a piece of data, and the value is consistent with the current message.



#### Test with the Websocket tool in Dashboard

Switch to the **Tools => Websocket** page and use any information client to connect to EMQ X. After the connection is successful, the sends the following message with the **message** card:

- Topic: md/state/NXP-058659730253-963945118132721-22

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


![websocket2x.jpg](https://static.emqx.net/images/8748f93fcbc839bc87f1099563fdfb80.jpg)



Click the **Send** button. At this time, the value of `tachometer` in the message body satisfies the condition of `tachometer > 8000` set above , and  the hit statistic value of current rule  is increased by one.

Check the data table records in the MongoDB command line to get the following data:

![mongruleresult2x.png](https://static.emqx.net/images/36df9f59d523863ac7cd4e27fe3724be.png)

So far, we have implemented a business development using the rules engine to store messages to the MongoDB database.
