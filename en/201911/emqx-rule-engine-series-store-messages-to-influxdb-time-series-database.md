## Overview 

[InfluxDB](https://www.influxdata.com/) is an open source database for storing and analyzing time series data， with built-in HTTP API, and the support for SQL-like statements and unstructured features are very friendly for users. Its powerful data throughput and stable performance make it ideal for the IoT area.

With the EMQ X messaging engine, we can customize the Template file and then convert the Json-formatted MQTT message into  Measurement to write to InfluxDB:

![Artboard.jpg](https://static.emqx.net/images/09b103dd807d6fd009fa102c7bcf7d09.jpg)

## Introduction of  Scenario

In this scenario, it is required to store the messages that meet the criteria under EMQ X in the InfluxDB time series database. In order to facilitate subsequent analysis and retrieval, the message content needs to be split for storage.

**The data reported by the device in this scenario is as follows:**

- Topic：data/sensor

- Payload:

  ```json
  {
    "location": "bedroom",
    "data": {
      "temperature": 25,
      "humidity": 46.4,
      "pm2_5": 0.5
    }
  }
  ```



## Preparation

### Database installation and initialization

Create a `db` database and open the 8089 UDP port.

```shell
$ docker pull influxdb

$ git clone -b v1.0.0 https://github.com/palkan/influx_udp.git

$ cd influx_udp

$ docker run --name=influxdb --rm -d -p 8086:8086 -p 8089:8089/udp -v ${PWD}/files/influxdb.conf:/etc/influxdb/influxdb.conf:ro -e INFLUXDB_DB=db influxdb:latest
```



## Configuration instructions

### Create a resource

Open EMQ X Dashboard, go to the **Resources** page on the left menu, click the **New** button, type MySQL server information for resource creation, select the InfluxDB resource type and complete the relevant configuration for resource creation.

![image20190719110910530.jpg](https://static.emqx.net/images/4acb4de9937bdd0a460086eba0ae750b.jpg)



### Create a rule

Go to the **Rules** page on the left menu and click the **New** button to create the rule. Select the trigger event **message.publish** ,  which is triggered when the message is published for data processing.

After selecting the trigger event, we can see the optional fields and sample SQL on the interface:

![image20190719112141128.jpg](https://static.emqx.net/images/8a566c0567231b6586c62f005c35fcce.jpg)



#### Filter the required fields

The rules engine uses SQL statements to filter and process data. For example, in the scenario mentioned above, we need to extract the fields in ``payload``, which can be implemented by `payload.<fieldName>`. At the same time we only expect to handle the `data/sensor` topic, then we can use the topic wildcard `=~` to filter the `topic` in the WHERE clause: `topic =~ 'data/sensor'`, and finally we get the SQL as follows:

```sql
SELECT
  payload.location as location,
  payload.data.temperature as temperature,
  payload.data.humidity as humidity,
  payload.data.pm2_5 as pm2_5
FROM
  "message.publish"
WHERE
	topic =~ 'data/sensor'
```



#### SQL Test

With the SQL test function, we can quickly confirm whether the SQL statement just filled in can achieve our goal. We  firstly fill in the payload and other data for testing as follows:

![image20190719113731130.jpg](https://static.emqx.net/images/156769eaf8720cd4b79c2dba7a929a9f.jpg)

Then click the **Test** button and get the following output, which is as expected.

```json
{
  "humidity": 46.4,
  "location": "bedroom",
  "pm2_5": 0.5,
  "temperature": 25
}
```



### Add a response action and store the message to InfluxDB

After the input and output of SQL condition  is correct, we continue to add the corresponding action, configure to write SQL statement, and store the filtered result in MySQL.

Click the **Add** button in the response action, select action of **Save Data to InfluxDB**, select the `InfluxDB` resource  just created, and then fill the `${fieldName}` into `Field Keys` according to actual needs. In `Tag Keys` and `Timestamp Key`, `Measurement` represents the `Measurement` used when writing data to `InfluxDB`. Finally, click the **New** button to complete the rule creation.

![image20190719115340429.jpg](https://static.emqx.net/images/5586dd983614fbdfc426304af396902b.jpg)



## Test

### Expected result

We successfully created a rule that contains a processing action, and expected result of the action is as follows:

1. When the client reports a message to the `data/sensor` topic, it will hit the rule, and the number of **hit** in the rule list is increased by 1;
2. A piece of data will be added to the db database in InfluxDB, and the data content is consistent with the processed message content



### Test with the Websocket tool in Dashboard

Switch to the **Tools** --> **Websocket** page, connect to EMQ X with any Client ID, and send the following message in the **Message** card after the connection is successful:

- Topic：data/sensor

- Payload:

  ```json
  {
    "location": "bedroom",
    "data": {
      "temperature": 25,
      "humidity": 46.4,
      "pm2_5": 0.5
    }
  }
  ```

![image20190719133414535.jpg](https://static.emqx.net/images/603bd675ce6ee7275f69876d44f4e484.jpg)

Click the **Send** button. After the transmission succeeds, you can see that number of hits for current rule has changed to 1.

Then check InfluxDB and see if the new data point is added successfully:

```
$ docker exec -it influxdb influx

> use db
Using database db
> select * from "sensor_data"
name: sensor_data
time                humidity location pm2_5 temperature
----                -------- -------- ----- -----------
1561535778444457348 46.4     bedroom  0.5   25
```

So far, we have implemented the business development of using the rules engine to store messages to InfluxDB  .

Before reading this tutorial, assume that you already know simple knowledge about  [MQTT](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html),[EMQ X](https://github.com/emqx/emqx) .

