## What is TDEngine?

TDengine is an open source big data platform designed and optimized for Internet of Things, Internet of Vehicles, Industrial Internet, IT operation and maintenance, etc., launched by TAOS Data (Beijing TAOS Data Technology Co., Ltd.). In addition to the core timing database functions that are more than 10 times faster, it also provides functions such as caching, data subscription, and streaming computing to minimize the complexity of R & D, operation and maintenance.

As a timing processing engine, TDengine can greatly simplify the design of big data platform and reduce the R & D cost and operation cost without  Kafka, HDFS / HBase / Spark, Redis and other software. Because fewer open source components need to be integrated, the system can be more robust and easier to ensure data consistency.

TDEngine provides community edition, enterprise edition and cloud service edition. For installation / use tutorial, please refer to the TDEngine documentation https://www.taosdata.com/cn/products/



## Scenario introduction

This article uses the example of  accessing the smart door lock of EMQ X through [MQTT protocol](https://www.emqx.com/en/mqtt)

Smart door locks have become the focus of smart home products. In order to ensure a more secure unlocking experience for users, smart door locks can usually achieve fingerprint unlocking, password unlocking, IC card unlocking, key unlocking, remote unlocking and other functions. Each business link of the smart door lock involves the sending and transmission of operation-sensitive instructions and status data, which should be stored for subsequent audit use.

### Collection process

The issued instructions and reported data from smart door lock are transmitted via EMQ X through the MQTT protocol. Users can optionally use the rule engine to filter or set the consumer client for processing on EMQ X, and  write the data satisfying the conditions into TDEngine data platform. The whole data flow process is as follows:

![1.png](https://static.emqx.net/images/4c14b86b4b8b14b1c23eebcc9a136118.png)



In this scenario, the smart door lock is planned to report the operation receipt and status information through the topic of  `lock/:id/control_receipt` (id is the clientid of  connecting client of the door lock, and the id of door lock). The data format is the following JSON message:

```json
{
  "id": "51dc0c50f55d11e9a4fec59e26b058d5", // Door lock  id
  "longitude": 102.8622543, // Longitude of current position
  "latitude": 24.8614503, // Latitude of current position
  "command": "unlock", // Instruction
  "LockState": 0, // Door lock status
  "LockType": 0, // Unlock method
  "KeyNickName": "", // Nickname of key
  "KeyID": "c944c8d0f55e11e9a4fec59e26b058d5", // Key ID
  "ErrorCode": 0, // Error code
  "pid": "84a2e10f55d11e9a4fec59e26b058d5", // Issued instruction ID
  "alarm": "", // Current alarm information
  "ts": 1570838400000 // Exectuion time
}
```



## Preparation

Although TDEngine is a relational database model, each collecting device is required to create a separate table. Therefore, we create a table for each lock based on the door lock id. At the same time, the compression ratio of floating point data is poor compared to the integer data. Longitude and latitude are usually accurate to 7 decimal places. **Therefore, the longitude and latitude are increased by 1E7 times and converted to long integer for storage:**

The statement to create the database is:

```sql
create database db cache 8192 ablocks 2 tblocks 1000 tables 10000;
use db;
```

The SQL statement to create the super table is:

```sql
create table lock(
  ts timestamp,
  id nchar(50),
  pid nchar(50),
  longitude bigint,
  latitude bigint,
  command nchar(50),
  LockState smallint,
  LockType smallint,
  KeyNickName nchar(255),
  KeyID nchar(255),
  ErrorCode smallint,
  alarm nchar(255)
) tags(card int, model binary(10));
```

**TDEngine is a relational database model, but requires each collecting device to create a separate table** , with the door lock id as the collection table table name. For example, if the id is 51dc0c50f55d11e9a4fec59e26b058d5, then the statement to create the data table is:

```sql
-- specify which supertable it belongs to with using command 
create table "v_51dc0c50f55d11e9a4fec59e26b058d5" using lock tags('51dc0c50f55d11e9a4fec59e26b058d5', 0);
```

Under this data model, taking the door lock id 51dc0c50f55d11e9a4fec59e26b058d5 as an example, the SQL statement to write a record to the table v_51dc0c50f55d11e9a4fec59e26b058d5 is:

```sql
insert into v_51dc0c50f55d11e9a4fec59e26b058d5 values(
  1570838400000,
  '51dc0c50f55d11e9a4fec59e26b058d5',
  'e84a2e10f55d11e9a4fec59e26b058d5',
  1028622543,
  248614503,
  'unlock',
  0,
  0,
  '',
  'c944c8d0f55e11e9a4fec59e26b058d5',
  0,
  '[]',
);
```

> In actual use, please build a table for each smart door lock in turn.



## Data writing method

At present, the function of directly writing EMQ X message data to TDEngine is still under planning. Thanks to the many connectors provided by TDEngine, we use the following two methods to complete the data writing:

- Use  [RESTful Connector](https://www.taosdata.com/cn/documentation/connector/#RESTful-Connector) in TDEngine: through calling REST API, splice and combine data into SQL statements and send them to TDEngine to perform writing, and built-in expressions and functions from rule engine can preprocess data;
- Through the client library / connector provided by TDEngine, write code to obtain EMQ X messages through subscription / consumption, and forward them to TDEngine after processing.



## Writing data using the rules engine

### Resource preparation

In EMQ X Dashboard, click the main menu of **Rules**  , and create a new WebHook resource on the  **Resources** page to send data to the TDEngine RESTful Connector. Add a request header:

- Authorization: The value is s a string of `{username}: {password}` after Base64 encoding that TDEngine request TOKEN for connection authentication. It i.

See the RESTful Connector tutorial for details:[TDEngine RESTful Connector](https://www.taosdata.com/cn/documentation/connector/#RESTful-Connector)


![2.png](https://static.emqx.net/images/2174df7b9c7e132649c6be3c347ab421.png)

Click **Test Connection**. After the test passes, click the **OK**  button to complete the creation.



### Create rules

After the resources are created, we can create rules. In the **Rules Engine ->  Rules** page, Click the **New** button to enter the rule creation page.

Select the **Message publish** event to process the data when the sensor message is reported (published). According to the **Available Field**  tips, information such as sensors can be selected from `payload`.

Since you need to process floating point values as integers, we use simple calculations. Please pay attention to the comments in SQL. The final SQL statement is as follows:

```sql
SELECT
  -- JSON Data decoding
  json_decode(payload) as p,
  -- Latitude and longitude magnify 10E7 times for storage
  p.longitude * 10000000 as p.longitude,
  p.latitude * 10000000 as p.latitude
FROM
  "message.publish"
WHERE
  -- Filtering data sources by topic
  topic =~ 'lock/+/control_receipt' 
```



![3.png](https://static.emqx.net/images/852c8f21042ef89d377697777097366b.png)


Using the SQL test function, input the raw reported data and related variables, and get the following output results:

```json
{
  "p": {
    "ErrorCode": 0,
    "KeyID": "c944c8d0f55e11e9a4fec59e26b058d5",
    "KeyNickName": "",
    "LockState": 0,
    "LockType": 0,
    "alarm": "",
    "command": "unlock",
    "id": "51dc0c50f55d11e9a4fec59e26b058d5",
    "latitude": 248614503,
    "longitude": 1028622543,
    "pid": "84a2e10f55d11e9a4fec59e26b058d5",
    "ts": 1570838400000
  }
}
```

From the output results, the floating point values of latitude and longitude  have been converted to integers, indicating that this step is correct and subsequent operations can be performed.

### Response action

Click the **Add Action** button at the bottom of the creation page. In the pop-up **Add Action** box, select the action of **Send data to the Web service, Use resources**. Select the resources created in the previous step Resources. In the content template, use the `$ {}` syntax to extract the  data filtered by **conditional SQL**. The spliced written SQL statement is as follows:

```sql
insert into db.v_${p.id} values(
  ${p.ts},
  '${p.id}',
  '${p.pid}',
  ${p.longitude},
  ${p.latitude},
  '${p.command}',
  ${p.LockState},
  ${p.LockType},
  '${p.KeyNickName}',
  '${p.KeyID}',
  ${p.ErrorCode},
  '${p.alarm}',
);
```



Click **Create**  to complete the creation of the rules. The data will be written to DBEngine when the smart door lock reports the data. The whole work and business process are as follows:

- Smart door lock reports data to EMQ X
- The `message.publish` event triggers the rule engine and starts to match the data fields of `topic` and `payload` according to the `where` condition in the conditional SQL.
- After the rule is hit, the response action list is triggered, and the request parameters required for the action are spliced according to the message content template in the response action. In this rule, the request parameter is an SQL statement that contains the reported data information of the smart door lock.
- Initiate a request based on the type of action and resources used, call the RESTful API to send instructions to TDEngine for execution, and complete data writing.





## Writing data using the TDEngine SDK

TDEngine provides SDK applicable for multiple language platforms. The program can obtain data reported by smart door locks to EMQ X by subscribing to MQTT topics or consuming message middleware data, and then stitch the data into SQL and finally write it to TDEngine.

This article uses the method of subscribing to the [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) to obtain smart door lock reporting data. Considering that the amount of messages may grow to an amount that a single subscription client cannot afford, we use the **shared subscription** method to consume data.

> In a shared subscription, clients subscribing to the same topic will receive messages under this topic in turn. That is to say, the same message will not be sent to multiple subscribers, thereby achieving load balancing among multiple nodes on the subscription side. .



### Code example

This example uses the Node.js platform to implement data writing operations using TDEngine's RESTful Connector.

Using method: Install Node.js, install npm, install dependencies, modify corresponding parameters and run execution.

```js
// index.js
const mqtt = require("mqtt");
const axios = require("axios");

/**
 * Execute TDEngine operations via RESTful Connector
 * @param {string} sql to be executed
 */
function exec(sql = "") {
  return axios({
    method: "post",
    url: "http://127.0.0.1:6020/rest/sql",
    auth: {
      username: "root",
      password: "taosdata"
    },
    data: sql
  });
}

// MQTT processing subscription message callback
async function handleMessage(topic, message) {
  try {
    // JSON to Object
    const p = JSON.parse(message.toString());
    // Handling floating point data
    p.longitude = p.longitude * 10e7;
    p.latitude = p.latitude * 10e7;
    const resp = await exec(`
      INSERT INTO db.v_${p.id} values(
        ${p.ts},
        '${p.id}',
        '${p.pid}',
        ${p.longitude},
        ${p.latitude},
        '${p.command}',
        ${p.LockState},
        ${p.LockType},
        '${p.KeyNickName}',
        '${p.KeyID}',
        ${p.ErrorCode},
        '${p.alarm}',
      );`);
    console.log(`Exec success:`, resp.data);
  } catch (e) {
    console.log(
      "exec insert error:",
      e.message,
      e.response ? e.response.data : ""
    );
  }
}

function createConsumer(config = {}) {
  const client = mqtt.connect("mqtt://127.0.0.1:1883", config);

  client.on("connect", () => {
    // Use share subscription $ share / prefix
    client.subscribe("$share//lock/+/control_receipt", (err, granded = []) => {
      if (!err && granded[0].qos <= 2) {
        console.log("Consumer client ready");
      }
    });
  });

  client.on("message", handleMessage);
}

// Create 10 shared subscription consumers
for (let i = 0; i < 10; i++) {
  createConsumer();
}

```



## Test

With the built-in MQTT client (WebSocket) of EMQ X Dashboard, it can quickly simulate test rule availability. Open the **Tools-> WebSocket** page, establish the connection according to the smart door lock connection information, enter the reported topic and reported data in the **publish** function, click publish to simulate the test:

- Publish topic：`lock/${id}/control_receipt`

- Payload：

  ```json
    {
      "id": "51dc0c50f55d11e9a4fec59e26b058d5",
      "longitude": 102.8622543,
      "latitude": 24.8614503,
      "command": "unlock",
      "LockState": 0,
      "LockType": 0,
      "KeyNickName": "", 
      "KeyID": "c944c8d0f55e11e9a4fec59e26b058d5",
      "ErrorCode": 0,
      "pid": "84a2e10f55d11e9a4fec59e26b058d5",
      "alarm": "",
      "ts": 1570838400000
    }
  ```

  



![4.jpg](https://static.emqx.net/images/d8301c71bf8ad2138189fc6c76f4b4c5.jpg)

After Published multiple times,  click the  **Monitor** icon in the **Rules Engine** list to quickly view the execution data of current rule . As can be seen from the figure below, 4 messages are hit by 3 times and succeeded for 3 times:

![5.png](https://static.emqx.net/images/a89a298132167ed1a519005ea173ded1.png)

View the data in `db.v_51dc0c50f55d11e9a4fec59e26b058d5` in the TDEngine dashboard, and there are three pieces of data:

```sql
use db;
select count(*) from v_51dc0c50f55d11e9a4fec59e26b058d5;

taos> select count(*) from v_51dc0c50f55d11e9a4fec59e26b058d5;
      count(*)       |
======================
                    3|
Query OK, 1 row(s) in set (0.000612s)
```



Delete the rule, start the TDEngine SDK to write code, and repeat the above test operation. We can see that the program prints the log as follows:

```bash
{ status: 'succ', head: [ 'affected_rows' ], data: [ [ 1 ] ], rows: 1 }
{ status: 'succ', head: [ 'affected_rows' ], data: [ [ 1 ] ], rows: 1 }
{ status: 'succ', head: [ 'affected_rows' ], data: [ [ 1 ] ], rows: 1 }
```



So far, the entire function of writing EMQ X data to TDEngine has been developed / configured.
