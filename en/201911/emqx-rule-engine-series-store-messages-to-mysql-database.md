## Introduction of Scenario

In this scenario, it is required to store the messages that meet the criteria under EMQX in the MySQL database. In order to facilitate subsequent analysis and retrieval, the message content needs to be split for storage.

**The information reported by the device in this scenario is as follows:**

- Reported topic:cmd/state/:id，Topic id represents the vehicle client ID

- Message body:

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22", // Client identification code
    "speed": 32.12, // vehicle speed
    "direction": 198.33212, // driving direction
    "tachometer": 3211, // Engine speed, which is required for storage when the value is greater than 8000
    "dynamical": 8.93, // Instantaneous fuel consumption
    "location": { // GPS Latitude and longitude data
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202 // reporting time
  }
  ```

  

When the reported data of engine speed value is greater than `8000', the current information is stored for subsequent analysis of the user's vehicle usage.



## Preparation

### Create a database

Create the `iot_data` database to store the message data, specifying the database encoding as `utf8mb4` to avoid coding problems:

```bash
CREATE DATABASE `emqx_rule_engine_output` CHARACTER SET utf8mb4;
```



### Create a data table

According to the scenario requirements, create a data table `use_statistics` with structure and field comments as follows:

```sql
CREATE TABLE `use_statistics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` varchar(100) DEFAULT NULL COMMENT 'Client identification code',
  `speed` float unsigned DEFAULT '0.00' COMMENT 'current vehicle speed',
  `tachometer` int(11) unsigned DEFAULT '0' COMMENT 'engine speed',
  `ts` int(11) unsigned DEFAULT '0' COMMENT 'Reported timestamp',
  `msg_id` varchar(50) DEFAULT NULL COMMENT 'MQTT message ID',
  PRIMARY KEY (`id`),
  KEY `client_id_index` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```



After the creation is successful, confirm the existence of the data table with the following MySQL command:

```bash
Database changed
mysql> desc use_statistics;
+------------+------------------+------+-----+---------+----------------+
| Field      | Type             | Null | Key | Default | Extra          |
+------------+------------------+------+-----+---------+----------------+
| id         | int(11)          | NO   | PRI | NULL    | auto_increment |
| client_id  | varchar(100)     | YES  | MUL | NULL    |                |
| speed      | float unsigned   | YES  |     | 0       |                |
| tachometer | int(11) unsigned | YES  |     | 0       |                |
| ts         | int(11) unsigned | YES  |     | 0       |                |
| msg_id     | varchar(50)      | YES  |     | NULL    |                |
+------------+------------------+------+-----+---------+----------------+
6 rows in set (0.01 sec)
```



## Configuration instructions

### Create a resource

Open EMQX Dashboard, go to the **Resources** page on the left menu, click the **New** button, type MySQL server information for resource creation.

![image20190716172916980.jpg](https://static.emqx.net/images/7af5c43283b3605f61897dfd83eb4ca8.jpg)

The network environment of the nodes in the EMQX cluster may be different. After the resources are created successfully, click the **Status button ** in the list to check the connection status of each node. If the resources on the node are unavailable, check whether the configuration is correct and the network connectivity is correct, and click the **Reconnect** button to manually reconnect.

![image20190716173259015.jpg](https://static.emqx.net/images/c33b326610e84582d33d7a78466ff1f3.jpg)



### Create a rule

Go to the **Rules** page on the left menu and click the **New** button to create the rule. Select the trigger event **Publishing message** here,  which is triggered when the message is published for data processing.

After selecting the trigger event, we can see the optional fields and sample SQL on the interface:

![image20190716174727991.jpg](https://static.emqx.net/images/2bb72c48b0cb527dc619fe0f70c33ce5.jpg)



#### Filter the required fields

The rule engine uses SQL statements to process rule conditions. In this business, we need to select all the fields in `payload` separately, use the `payload.fieldName` format to select, and also need the topic context information of `topic`, `qos`, `id ` , the current SQL is as follows:

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

Conditional filtering is done by using the SQL statement WHERE clause, in which we need to define two conditions:

- Only handle `cmd/state/:id` topic, use the topic wildcard `=~` to filter `topic`: `topic =~ 'cmd/state/+'
- Only handle`tachometer > 8000` messages, use the comparator to filter `tachometer`: `payload.tachometer > 8000`

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



Click the **SQL Test** toggle button, change `topic` and `payload` into the information in the scenario, and click the **Test** button to view the data output:

![image20190716184242159.jpg](https://static.emqx.net/images/0f9b63a1ad40b2072a0838a7c4727df9.jpg)



The test output data is as follows:

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



### Add a response action and store the message to MySQL

After the input and output of SQL condition  is correct, we continue to add the corresponding action, configure to write SQL statement, and store the filtered result in MySQL.

We populate the SQL statement with the `${fieldName}` syntax, insert the data into the database, and finally click the **New** button to complete the rule creation.

The SQL configuration of the action is as follows:

```sql
INSERT INTO 
	`use_statistics` (`client_id`, `speed`, `tachometer`, `ts`, `msg_id`)
VALUES 
	(${client_id}, ${speed}, ${tachometer}, ${ts}, ${id});
```

![image20190716182818011.jpg](https://static.emqx.net/images/968c8abc7075fecdb02f536ad1f36ced.jpg)





## Test

#### Expected result

We successfully created a rule that contains a processing action, and expected result of the action is as follows:

1. When the device reports a message to the `cmd/state/:id` topic, it will hit SQL when the value of `tachometer` in the message exceeds 8000, and the number of **hit** in the rule list is increased by 1;
2. A piece of data will be added to the 'use_statistics' table in MySQL `iot_data` database with the same value as the current message.



#### Test with the Websocket tool in Dashboard

Switch to **tools -> Websocket** page, connect to EMQX with any client, and send the following message to  **message**  card after successful connection:

- Topic: cmd/state/NXP-058659730253-963945118132721-22

- Message body:

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22",
    "speed": 32.12,
    "direction": 198.33212,
    "tachometer": 9002,
    "dynamical": 8.93,
    "location": {
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202
  }
  ```


![image20190716190238252.jpg](https://static.emqx.net/images/5f022cfca5aceb231cba61b7014a3fe1.jpg)



Click the **Send** button to view the rule **hit** statistics after the successful transmission. The data statistic value of hit is 1 to indicate that the rule has been successfully hit. View the data table record  with the MySQL command line  to get the following data:

![image20190717141918330.png](https://static.emqx.net/images/a4606e0e73c431c5eccaa2a635610417.png)

So far, we have implemented the business development of using the rules engine to store messages to MySQL .
