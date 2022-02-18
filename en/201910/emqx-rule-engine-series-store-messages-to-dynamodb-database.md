## Amazon DynamoDB Introduction

Amazon DynamoDB is a fully hosted NoSQL database service that supports key values and document data structures.

Amazon DynamoDB is provided by Amazon as part of the AWS cloud portfolio, delivering fast, predictable performance and seamless scaling.

Amazon DynamoDB Service Address:

https://aws.amazon.com/dynamodb/

## Scenario Introduction

In this scenario, messages that meet the criteria under the EMQX specified topic are required to be stored in the DynamoDB database. In order to facilitate subsequent analysis and retrieval, the message content needs to be split and stored.

**In this scenario, the message reported by the device  is as follows:**

- Reported topic: cmd/state/:id, the topic id represents the vehicle client ID

- Message body:

  ```json
  {
    "id": "NXP-058659730253-963945118132721-22", // Client ID
    "speed": 32.12, // Vehicle speed
    "direction": 198.33212, // Driving direction
    "tachometer": 3211, // Engine speed, that is required to be stored when the value is greater than 8000
    "dynamical": 8.93, // Instantaneous fuel consumption
    "location": { // GPS latitude and longitude data
      "lng": 116.296011,
      "lat": 40.005091
    },
    "ts": 1563268202 // Reported time
  }
  ```

When the reported data of engine speed value is greater than `8000', the current information is stored for subsequent analysis of the user's vehicle usage.

## Preparation

### Define DynamoDB data table

According to the scenario requirements, define the data table `use_statistics` structure as follows:

use_statistics.json

```json
{
    "TableName": "use_statistics",
    "KeySchema": [
        { "AttributeName": "client_id", "KeyType": "HASH" },
        { "AttributeName": "id", "KeyType": "RANGE" }
    ],
    "AttributeDefinitions": [
        { "AttributeName": "client_id", "AttributeType": "S" },
        { "AttributeName": "id", "AttributeType": "S" }
    ],
    "ProvisionedThroughput": {
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }
}
```

### Create DynamoDB data table

Create  `use_statistics` data table with the aws cli command:

```bash
$ aws dynamodb create-table --cli-input-json file://use_statistics.json --endpoint-url http://localhost:8000
{
    "TableDescription": {
        "AttributeDefinitions": [
            {
                "AttributeName": "client_id",
                "AttributeType": "S"
            },
            {
                "AttributeName": "id",
                "AttributeType": "S"
            }
        ],
        "TableName": "use_statistics",
        "KeySchema": [
            {
                "AttributeName": "client_id",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "id",
                "KeyType": "RANGE"
            }
        ],
        "TableStatus": "ACTIVE",
        "CreationDateTime": 1563765603.777,
        "ProvisionedThroughput": {
            "LastIncreaseDateTime": 0.0,
            "LastDecreaseDateTime": 0.0,
            "NumberOfDecreasesToday": 0,
            "ReadCapacityUnits": 5,
            "WriteCapacityUnits": 5
        },
        "TableSizeBytes": 0,
        "ItemCount": 0,
        "TableArn": "arn:aws:dynamodb:ddblocal:000000000000:table/use_statistics",
        "BillingModeSummary": {
            "BillingMode": "PROVISIONED",
            "LastUpdateToPayPerRequestDateTime": 0.0
        }
    }
}
```

Confirm the existence of the data table through the aws cli command after the successful creation:

```bash
$ aws dynamodb list-tables --region us-west-2 --endpoint-url http://127.0.0.1:8000
{
    "TableNames": [
        "use_statistics"
    ]
}
```

## Configuration instructions

### Create resource

Open EMQX Dashboard, go to the **Resources** page on the left menu, click the **New** button, type DynamoDB server information for resource creation.

![image01.jpg](https://static.emqx.net/images/22f62479759058690bf6dd468e715a80.jpg)

The network environment of the nodes in the EMQX cluster may be different. After the resources are created successfully, click the **Status** button  in the list to check the connection status of each node. If the resources on the node are unavailable, check whether the configuration is correct and the network connectivity is correct, and click the **Reconnect** button to manually reconnect.

![image02.jpg](https://static.emqx.net/images/a5973e08b0b26d85eb60505610193714.jpg)

### Create rules

Go to the left menu of  **rules**  page, click  **new**  button to create rules. Select trigger event  of **message publishing** to trigger this rule for data processing when the message is published.

After selecting the trigger event, we can see the optional field and sample SQL in the interface:

![image03.jpg](https://static.emqx.net/images/1c72e2ec615041b9919dc28b500e5c98.jpg)

#### Screen the required fields

Rule engine uses SQL statements to process rule conditions. In this business, we need to select all the fields in `payload` separately, use the `payload.fieldName` format to select, and also need the topic context information of`topic`, `qos`, `id `. The current SQL is as follows:

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

#### Establish screening conditions

Conditional screening is done by using the SQL statement WHERE clause, in which we need to define two conditions:

- Only handle `cmd/state/:id` topic, use the topic wildcard `=~` to screen `topic`: `topic =~ 'cmd/state/+'
- Only process `tachometer > 8000` messages, use the comparator to screen `tachometer`: `payload.tachometer > 8000`

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

#### Output test is done with the SQL test function

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

Click the **SQL Test** toggle button, change `topic` and `payload` to be the information in the scenario, and click the **Test** button to view the data output:

![image04.jpg](https://static.emqx.net/images/dc409088b0c06d6aadf0863501d91132.jpg)

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

### Add a response action and store the message to DynamoDB

After the input and output of SQL condition  is correct, we continue to add the corresponding action, configure to write SQL statement, and store the screening result in DynamoDB.

Click the **Add** button in the response action, select the **Save data to DynamoDB** action, select the resource  just selected, fill the DynamoDB table name, Hash Key, and Range Key.

![image05.jpg](https://static.emqx.net/images/73ccf170e50c8caeaaa7134f4c573b6d.jpg)

## Test

#### Expected result

We successfully created a rule that contains a processing action, and expected result of the action is as follows:

1. When the device reports a message to the `cmd/state/:id` topic, it will hit SQL when the value of `tachometer` in the message exceeds 8000, and the number of **hit** in the rule list is increased by 1;
2. A piece of data will be added to the 'use_statistics' table in DynamoDB with the same value as the current message.

#### Test with the Websocket tool in Dashboard

Switch to **tools -> Websocket** page, connect to EMQX with any client, and send the following message to  **message**  card after successful connection:

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
![image06.jpg](https://static.emqx.net/images/c11f9cc66c213e5c9ceec676c6216328.jpg)

Click the **Send** button. After sending successfully, the statistic of hit under  current rule is 1.

View the data table records with the aws cli command to get the following data:

![image07.png](https://static.emqx.net/images/d19a7472d896f9822571908f6ad0651c.png)
So far, we have implemented the business development of using the rules engine to store messages to DynamoDB.
