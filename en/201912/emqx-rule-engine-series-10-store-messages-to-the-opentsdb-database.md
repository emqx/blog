## Introduction to OpenTSDB 

OpenTSDB is an extensible distributed time series Database database, whose bottom layer relies on HBase and makes full use of HBase's features of distributed column storage to support millions of reads and writes per second.

Facing large-scale and rapid growth of IoT sensor acquisition, transaction records and other data, time series data accumulates very quickly. The time series database processes this large-scale data by improving efficiency and brings performance improvements, including higher Ingest Rates, faster large-scale queries, and better data compression.

## Install and verify OpenTSDB server

Readers can refer to the official OpenTSDB document (https://opentsdb.net) or Docker (https://hub.docker.com/r/petergrace/opentsdb-docker/) to download and install the OpenTSDB server. This article uses OpenTSDB 2.4.0 .



## Introduction to secnario

In this scenario, it is required to store the messages that meet the conditions under the topic specified by EMQ X to the OpenTSDB database. In order to facilitate subsequent analysis and retrieval, the message content needs to be split and stored.

**The data reported by the client in this scenario is as follows:** 

- Topic：stat/cpu

- Payload:

  ```json
  {
    "metric": "cpu",
    "tags": {
      "host": "serverA"
    },
    "value":12
  }
  ```



## Preparation

### Start OpenTSDB Server

Start OpenTSDB Server and open port 4242.

```shell
$ docker pull petergrace/opentsdb-docker

$ docker run -d --name opentsdb -p 4242:4242 petergrace/opentsdb-docker
```



## Configuration instructions

### Create resources

Open EMQ X Dashboard, enter the **Resources** page on the left menu, click the **New** button, select the OpenTSDB resource type and complete the related configuration to create the resources.

![image20190725110536094.png](https://static.emqx.net/images/559e3c15ade4859fde9a4450a7ec44be.png)

### Create rules

Enter the **Rules** page on the left menu and click the **New** button to create a rule. Here we choose **message.publish** as the trigger event. When EMQ X receives the PUBLISH message, the rule is triggered for data processing.

After the trigger event is selected, we can see optional fields and sample SQL on the interface:

![image20190719112141128.png](https://static.emqx.net/images/c7403006b9e6c66eb93147635fdec72a.png)



#### Filter required fields

The rules engine uses SQL statements to filter and process data. For example, in the scenario mentioned above, when we need to extract the fields in `` payload`` , it can be achieved by `payload. <FieldName>`. At the same time, we only want to deal with the topic `stat / cpu`, so we can use the topic wildcard` = ~ `in the WHERE clause to filter the topic:` topic = ~ 'stat / cpu'`, and finally we get the following SQL:

```sql
SELECT
  payload.metric as metric, payload.tags as tags, payload.value as value
FROM
  "message.publish"
WHERE
	topic =~ 'stat/cpu'
```



#### SQL Test

With the SQL test feature, we can quickly confirm whether the SQL statement we just filled out can achieve our purpose. We firstly fill in the payload and other data for testing as follows:

![image20190725110913878.png](https://static.emqx.net/images/36998b39ec573e870a02025ae4b75f16.png)

Then click the **Test**  button, we get the following data output:

```json
{
  "metric": "cpu",
  "tags": {
    "host": "serverA"
  },
  "value": 12
}
```

The test output is as expected and we can proceed to the next step.



### Add response action, and store message to OpenTSDB

After the SQL condition input and output are correct, we continue to add corresponding actions, configure to write SQL statements, and store the filtered results in OpenTSDB.

Click the **Add** button in the response action, select the  action of **Save Data to OpenTSDB**, select the `OpenTSDB` resource just created and complete the remaining parameter settings. Several parameters that OpenTSDB requires for operation are:

1. Details. Whether OpenTSDB Server is required to return data points and reasons for failure. The default is false.
2. Summary information. Whether OpenTSDB Server is required to return data points to store the number of successes and failures. The default is true.
3. Maximum number of batches processing. How many Data Points the driver is allowed to read from the queue at one time to merge into one HTTP request when the message request is frequent . It is a performance optimization parameter. The default value is 20.
4. Whether to call synchronously. Configures whether OpenTSDB Server waits for all data to be written before returning results. The default is false.
5. Synchronous call timeout. The maximum time that the OpenTSDB Server waits for data to be written. The default is 0, that means times out never happens.

Here we all use the default configuration, click the  **New** button to complete the rule creation.

![image20190725111158382.png](https://static.emqx.net/images/5ccaba525195b33764e628aedbe0642f.png)



## Test

### Expected result

We have successfully created a rule that contains a processing action. The expected effect of the action is as follows:

1. When the client reports a message to the topic `stat / cpu`, the message will hit SQL and the number of **hits** in the rule list will increase by 1;
2. A piece of data will be added to the OpenTSDB Server, and the data content is consistent with the message content.



### Test with Websocket tools in Dashboard

Switch to the **Tools ->  Websocket** page, use any information client to connect to EMQ X. After the connection is successful, send the following message in the **Message** card:

- Topic：stat/cpu

- Payload:

  ```json
  {
    "metric": "cpu",
    "tags": {
      "host": "serverA"
    },
    "value":12
  }
  ```

![image20190725112738414.png](https://static.emqx.net/images/55010e5898747458016a572307f41272.png)

Click the **Send** button. After sending successfully, we can see that the number of hits of the current rule has changed to 1.

Then, send a query request to OpenTSDB through Postman. When we get the following response, it means the new data point has been added successfully:

![image20190725113422461.png](https://static.emqx.net/images/8f5bf630e3efebdad766a27d778dad82.png)

So far, we have implemented business development to store messages to the OpenTSDB database through the rule engine.
