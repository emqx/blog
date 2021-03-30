![画板 172x.png](https://static.emqx.net/images/596a4e5f5875b53d706eb59ce09b5591.png)

## Introduction to PostgreSQL Database

As an important open source relational databases, PostgreSQL claims to be the most advanced open source database in the world. Compared to other open source relational databases such as MySQL, PostgreSQL is a completely community-driven open source project, maintained by more than 1,000 contributors worldwide. PostgreSQL provides a single full-featured version, that is unlike MySQL which offers multiple different versions for  community, business, and enterprise. PostgreSQL is based on a free BSD / MIT license, and organizations can use, copy, modify, and redistribute its code with a copyright notice.

PostgreSQL has many features, and has more support in the field of GIS. Its "lock-free" feature is very prominent, supports function and condition indexes, and has a mature clustering solution. PostgreSQL also has powerful SQL programming capabilities such as statistical functions and statistical syntax support. With the Timescaledb plugin, PostgreSQL can be transformed into a full-featured time-series database Timescaledb.



## Scenario introduction

Under this scenario, it is required to store the messages that meet the conditions under the topic specified by EMQ X to the PostgreSQL database. In order to facilitate subsequent analysis and retrieval, the message content needs to be split and stored.

**The data reported by the client in this scenario is as follows:** 

- Topic：testtopic

- Payload:

  ```
  {"msg":"Hello, World!"}
  ```

## Preparation

### Create a database

Create a tutorial database with a username of postgres and a password of password:

```shell
$ docker pull postgres

$ docker run --rm --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=password -d postgres:latest

$ docker exec -it postgres psql -U postgres

> CREATE database tutorial;

> \c tutorial
```



### Create a data table

Create `t_mqtt_msg`  table：

```sql
CREATE TABLE t_mqtt_msg (
  id SERIAL primary key,
  msgid character varying(64),
  sender character varying(64),
  topic character varying(255),
  qos integer,
  retain integer,
  payload text,
  arrived timestamp without time zone
);
```



## Configuration instructions

### Create a resource

Open EMQ X Dashboard, enter the **Resources**  page of the left menu, click the  **New** button, select the PostgreSQL resource type and complete the related configuration for resource creation.

![image20190725142933513.png](https://static.emqx.net/images/e71375bc88c1006c15cd8bd0b530a4fc.png)



### Create a rule

Enter the **Rules** page on the left menu and click the **New** button to create a rule. Here we choose to trigger event  of **message.publish**, which means when EMQ X receives the message of PUBLISH , the rule is triggered for data processing.

After the trigger event is selected, we can see optional fields and sample SQL on the interface:

![image20190719112141128.png](https://static.emqx.net/images/77c447a399f12a0e2bc083289830a139.png)



#### Filter required fields

The rules engine uses SQL statements to filter and process data. Here we need data such as msgid, topic, payload, and we want to match messages from all topics. Therefore, we only need to delete the WHERE clause based on the default SQL. In the end, we get the following SQL:

```sql
SELECT
  *
FROM
  "message.publish"
```



#### SQL Test

With the SQL test feature, we can quickly confirm whether the SQL statement we just filled out can achieve our purpose. First we fill in the payload and other data for test as follows:

![image20190725145617081.png](https://static.emqx.net/images/5cb6cc54c7a2495335c32e0d0cb019d0.png)

After clicking the  **Test**  button, we get the following data output:

```json
{
  "client_id": "c_emqx",
  "event": "message.publish",
  "id": "589A429E9572FB44B0000057C0001",
  "node": "emqx@127.0.0.1",
  "payload": "{\"msg\":\"Hello, World!\"}",
  "peername": "127.0.0.1:50891",
  "qos": 1,
  "retain": 0,
  "timestamp": 1564037750692,
  "topic": "testtopic",
  "username": "u_emqx"
}
```

The test output contains all the required data and we can proceed to the next steps.



### Add response action, and store message to PostgreSQL

After the SQL condition input and output are correct, we continue to add corresponding actions, configure to write SQL statements, and store the filtered results in PostgreSQL.

Click the **Add** button in the response action, select the action of **Save Data to PostgreSQL** , select the `PostgreSQL` resource you just created and fill in the SQL template as follows:

`insert into t_mqtt_msg(msgid, topic, qos, retain, payload, arrived) values (${id}, ${topic}, ${qos}, ${retain}, ${payload}, to_timestamp(${timestamp}::double precision /1000)) returning id`

Finally, click the **New** button to complete the rule creation.

![image20190725144256942.png](https://static.emqx.net/images/d6ffcd695037cfbf0edd0f86ae08181e.png)



## Test

### Expected outcome

We have successfully created a rule that contains a processing action. The expected outcome of the action is as follows:

1. When the client reports a message, the message will hit SQL and the number of **hits** in the rule list will increase by 1;
2. A piece of data will be added to the `t_mqtt_msg` table of the PostgreSQL` tutorial` database. The data content is consistent with the message content.



### Test with Websocket tools in Dashboard

Switch to the **Tools ->  Websocket**  page, use any information client to connect to EMQ X. After the connection is successful, send the following message in the  **message** card:

- Topic：testtopic

- Payload:

  ```json
  {"msg":"Hello, World!"}
  ```

![image20190725145805279.png](https://static.emqx.net/images/9b9e11efbab8f3b466b01ad4305c40da.png)

Click the **Send** button. After sending successfully, we can see that the number of hits of the current rule has changed to 1.

Then check PostgreSQL to see if the new data point was added successfully:

![image20190725145107685.png](https://static.emqx.net/images/84514d56fd8c388e713bc7dba245412a.png)

So far, we have used the rule engine to implement business development to store messages to a PostgreSQL database.

