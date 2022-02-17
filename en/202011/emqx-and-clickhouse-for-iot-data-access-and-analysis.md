IoT data collection involves mass equipment access and a massive number of data transmission. The combined technology stack of [EMQ X MQTT Broker](https://www.emqx.com/en/products/emqx) and ClickHouse OLAP database is fully capable of IoT data collection, transmission, storage, analysis and processing business.

After storing the data in the database, we usually need other methods, for example, a data visualization system will count and display these data according to the rules for implementing data monitoring, indicators statistics and other business needs, to give full play to the value of the data. ClickHouse with open source software Grafana can quickly build IoT data analysis and visualization platform.

The above solution without code development, involving products can provide open-source software, enterprise services, cloud SaaS services different levels of delivery models, according to project requirements to achieve a free or enterprise version of the private landing and cloud deployment.

![image-20200916112653512](https://static.emqx.net/images/5ba8c46006e196b5ee8ca42cf60b2d86.png)



## Introduction to the solution

### Introduction to EMQ X

[EMQ  X ](https://www.emqx.com/en) is an open-source MQTT messaging broker developed on a highly concurrent Erlang/OTP language platform, supporting millions of connections and distributed cluster architecture, with a publish-subscribe model. EMQ X has many out-of-the-box features built-in, and **EMQ X Enterprise**, supports the storage of IoT message data to ClickHouse via a rules engine.


### Introduction to ClickHouse

[ClickHouse](https://clickhouse.tech/) is a fast open-source OLAP database management system. It is column-oriented and allows to generate analytical reports using SQL queries in real-time.


### Introduction to Grafana

[Grafana](https://grafana.com/) is a cross-platform, open-source metrics analysis and visualization tool that can query and process data from a variety of data sources for visual display. It can quickly and flexibly create client-side charts, panel plugins which have many different ways of visualizing metrics and logs, the official library has a wealth of dashboard plugins, such as heat maps, line graphs, charts and other display methods; support for InfluxDB, OpenTSDB, Prometheus, Elasticsearch, CloudWatch, KairosDB and other data sources, and support independent/hybrid query presentation of data items; custom alert rules can be created and notified to other message processing services or components.

Grafana 4.6+ supports installing Clickhouse data sources via plugin format. It is needed to install the ClickHouse plugin on Grafana before use.



## Business scenarios

In this article, we simulate a data collection scenario in an IoT environment, assuming that there are certain data collection points in the environment, and the data from all the collection points are transmitted to the collection platform via [MQTT protocol](https://www.emqx.com/en/mqtt), the MQTT topic is designed as follows:

```bash
sensor/data
```

The data sent by the sensor is in JSON format and includes data collected by the sensor such as temperature, humidity, noise volume, PM10, PM2.5, sulfur dioxide, nitrogen dioxide, carbon monoxide, sensor ID, zone, collection time, etc.

```json
{
    "temperature": 30,
    "humidity" : 20,
    "volume": 44.5,
    "PM10": 23,
    "pm25": 61,
    "SO2": 14,
    "NO2": 4,
    "CO": 5,
    "id": "10-c6-1f-1a-1f-47",
    "area": 1,
    "ts": 1596157444170
}
```

Now, the real-time storage is needed for viewing data at any subsequent time and the following requirements are proposed: 

- Each device reports every 5 seconds, and the database stores each piece of data for subsequent retrospective analysis.
- The raw data is stored via ClickHouse and used with Grafana for data analysis and visual presentation.



## Environmental preparation

Each component used in this article has a Docker image that can be quickly built and run. To facilitate development, Grafana is built using Docker, ClickHouse is installed using documented recommendations, and EMQ X uses the Zip package to install or directly use the online cloud service.

The released resources and tutorial of use can be referred to as the following websites:

 - EMQ X：[EMQ official website](https://www.emqx.com/en)
 - ClickHouse：ClickHouse products homepage  [https://clickhouse.tech/](https://clickhouse.tech/)
 - Grafana：Grafana official website [https://grafana.com/](https://grafana.com/) 



### Install EMQ X

#### Method 1: using EMQ X Cloud

EMQ provides [EMQ X Cloud - a fully managed IoT MQTT cloud service](https://www.emqx.com/en/cloud), on which users can create a highly available, exclusive instance EMQ X cluster in just a few minutes, and start prototyping and application development immediately without the need to pay attention to the subsequent operation and maintenance work. After the product goes live, the cluster can be expanded without downtime to cope with capacity expansion brought about by business growth, ensuring availability and maximizing cost savings.

EMQ X Cloud offers a 6-month free trial to newly registered users. After registering and logging in to create a trial deployment, click on **EMQ X Dashboard** in the deployment details to open the EMQ X Management Console.

> To use EMQ X Cloud you need to ensure that ClickHouse can be accessed via a public network address.

![WechatIMG4152.png](https://static.emqx.net/images/2bacab94e2fda212c1775d1ffdf3f400.png)



#### Method 2: private deployment installation

> If you are new to EMQ X, we recommend [EMQ X documentation](https://docs.emqx.io/broker/latest/en/) to get started quickly.

Access the [EMQ download](https://www.emqx.com/en/try?product=enterprise) page to download the appropriate package for your operating system. At the time of this writing, the Enterprise version of EMQ X is v4.1.2. The steps to download the zip package are as follows:

```bash
## Decompress the downloaded installation package
unzip emqx-macosx-v4.1.2.zip
cd emqx

## Start EMQ X in console mode for easy debugging
./bin/emqx console
```

After successful startup, the browser accesses [http://127.0.0.1:18083](http://127.0.0.1:18083) to access the EMQ X management console dashboard and completes the initial login using the `admin` `public` default username and password.



### Install ClickHouse

Using the installation method recommended by [ClickHouse documentation](https://clickhouse.tech/#quick-start). 

```bash
sudo yum install yum-utils
sudo rpm --import https://repo.clickhouse.tech/CLICKHOUSE-KEY.GPG
sudo yum-config-manager --add-repo https://repo.clickhouse.tech/rpm/clickhouse.repo
sudo yum install clickhouse-server clickhouse-client

sudo /etc/init.d/clickhouse-server start
clickhouse-client
```

**By default ClickHouse only listens on local ports, if remote access is required you need to change the configuration file**:

```xml
<!-- /etc/clickhouse-server/config.xml -->
<!-- Find this line, uncomment <listen_host>::</listen_host> and modify it to -->
<listen_host>0.0.0.0</listen_host>
```

Restart:

```bash
service clickhouse-server restart 
```



### Install Grafana

Install and enable Grafana through Docker using the following command:

```bash
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

After successful startup, access [http://127.0.0.1:3000](http://127.0.0.1:3000) in your browser to access the Grafana visualization panel and use the default username password `admin` `admin` to complete the initial login. After logging in, follow the prompts to change your password and log in with your new password to access the main interface.



## Configure EMQ X for storing data to the ClickHouse

Enable ClickHouse and go to the command line:

```bash
sudo /etc/init.d/clickhouse-server start
clickhouse-client
```

Creating the **test** database:

```sql
create database test;
use test;
```

The ClickHouse SQL syntax for creating a sensor_data table differs from that of a regular relational database, see [ClickHouse documentation-SQL-syntax](https://clickhouse.tech/docs/zh/sql-reference/syntax/):

> The DataTime and Date columns need to be added to the Grafana chronological display.

```sql
CREATE TABLE sensor_data (
 	temperature Float32,
  humidity Float32,
  volume Float32,
  PM10 Float32,
  pm25 Float32,
  SO2 Float32,
  NO2 Float32,
  CO Float32,
  sensor_id String, 
  area Int16,
  coll_time DateTime,
  coll_date Date
) engine = Log;

-- The ClickHouse command line does not support line feeds for table building statements, use the following SQL to execute:
CREATE TABLE sensor_data( temperature Float32, humidity Float32, volume Float32, PM10 Float32, pm25 Float32, SO2 Float32, NO2 Float32, CO Float32, sensor_id String, area Int16, coll_time DateTime, coll_date Date) engine = Log;
```



### Configure the EMQ X rule engine

Open EMQ X Dashboared and go to the **rule engine** -> **rules** page and click the **create** button to go to the create page.

#### Rule SQL

Rule SQL is used for EMQ X message and event filtering, the following SQL is used to filter payload data from the `sensor/data` topic.

```sql
SELECT
  payload
FROM
  "sensor/data"
```

Using the **SQL test function**, input test data and perform a filtering result test, and the test has result and the output content are as follows, indicating that the SQL is written correctly:

**Test data (actual data reported by the equipment):**

```json
{
    "temperature": 30,
    "humidity" : 20,
    "volume": 44.5,
    "PM10": 23,
    "pm25": 61,
    "SO2": 14,
    "NO2": 4,
    "CO": 5,
    "id": "10-c6-1f-1a-1f-47",
    "area": 1,
    "ts": 1596157444170
}
```

**The output of test**

```json
{
  "payload": "{\"temperature\":30,\"humidity\":20,\"volume\":44.5,\"PM10\":23,\"pm25\":61,\"SO2\":14,\"NO2\":4,\"CO\":5,\"id\":\"10-c6-1f-1a-1f-47\",\"area\":1,\"ts\":1596157444170}"
}
```

![1.png](https://static.emqx.net/images/9c500a52ab22bdf76d810c9020b54b82.png)



#### Response action

Using both EMQ X Enterprise and EMQ X Cloud, which support writing data to ClickHouse via the Rules Engine.

Configuring the response action requires two pieces of data, an associated resource and a SQL template.

- Associated resource: creates a ClickHouse resource and configures the connection parameters.
- SQL template: here is the INSERT SQL with data, note that we should specify the database name in the SQL.

```sql
INSERT INTO test.sensor_data VALUES(
  ${payload.temperature},
  ${payload.humidity},
  ${payload.volume},
  ${payload.PM10},
  ${payload.pm25},
  ${payload.SO2},
  ${payload.NO2},
  ${payload.CO},
  '${payload.id}',
  ${payload.area},
  ${payload.ts}/1000,
  ${payload.ts}/1000
)
```



#### Creation process

Click the **add** button under the response action and select **save data to the ClickHouse** in the pop-up box, and then click **new resource** to create a new ClickHouse resource.

Select **ClickHouse** for the resource type and fill in the resource name, server address and authentication information:

![2.png](https://static.emqx.net/images/d257825ce0987dbdd1f28e371b1f9f04.png)

On the response action creation page, select the new resource and fill in the SQL template.

![3.png](https://static.emqx.net/images/0296858c31bd1a6c504f50e8c06e7c37.png)



## Generate simulation data

The following script simulates a scenario in which 10 devices report simulated data every 5 seconds for the past 24 hours and send it to EMQ X.

Readers need to install Node.js. After installing Node.js and modifying the configuration parameters as needed, you can start it with the following command:

```bash
npm install mqtt mockjs --save --registry=https://registry.npm.taobao.org
node mock.js
```

P.S. Simulation data is generated and sent to EMQ X, please adjust the relevant parameters according to the cluster performance.

```javascript
// mock.js
const mqtt = require('mqtt')
const Mock = require('mockjs')

const EMQX_SERVER = 'mqtt://localhost:1883'
const CLIENT_NUM = 10
const STEP = 5000 // Simulation collection interval ms
const AWAIT = 500 // Sleep time after each send to prevent excessive message rate ms
const CLIENT_POOL = []

startMock()


function sleep(timer = 100) {
  return new Promise(resolve => {
    setTimeout(resolve, timer)
  })
}

async function startMock() {
  const now = Date.now()
  for (let i = 0; i < CLIENT_NUM; i++) {
    const client = await createClient(`mock_client_${i}`)
    CLIENT_POOL.push(client)
  }
  // last 24h every 5s
  const last = 24 * 3600 * 1000
  for (let ts = now - last; ts <= now; ts += STEP) {
    for (const client of CLIENT_POOL) {
      const mockData = generateMockData()
      const data = {
        ...mockData,
        id: client.options.clientId,
        ts,
      }
      client.publish('sensor/data', JSON.stringify(data))
    }
    const dateStr = new Date(ts).toLocaleTimeString()
    console.log(`${dateStr} send success.`)
    await sleep(AWAIT)
  }
  console.log(`Done, use ${(Date.now() - now) / 1000}s`)
}

/**
 * Init a virtual mqtt client
 * @param {string} clientId ClientID
 */
function createClient(clientId) {
  return new Promise((resolve, reject) => {
    const client = mqtt.connect(EMQX_SERVER, {
      clientId,
    })
    client.on('connect', () => {
      console.log(`client ${clientId} connected`)
      resolve(client)
    })
    client.on('reconnect', () => {
      console.log('reconnect')
    })
    client.on('error', (e) => {
      console.error(e)
      reject(e)
    })
  })
}

/**
* Generate mock data
*/
function generateMockData() {
 return {
   "temperature": parseFloat(Mock.Random.float(22, 100).toFixed(2)),
   "humidity": parseFloat(Mock.Random.float(12, 86).toFixed(2)),
   "volume": parseFloat(Mock.Random.float(20, 200).toFixed(2)),
   "PM10": parseFloat(Mock.Random.float(0, 300).toFixed(2)),
   "pm25": parseFloat(Mock.Random.float(0, 300).toFixed(2)),
   "SO2": parseFloat(Mock.Random.float(0, 50).toFixed(2)),
   "NO2": parseFloat(Mock.Random.float(0, 50).toFixed(2)),
   "CO": parseFloat(Mock.Random.float(0, 50).toFixed(2)),
   "area": Mock.Random.integer(0, 100),
 }
}
```



## Visual configuration

After the component is installed and the simulated data is written successfully, follow the instructions of the Grafana visualization interface to complete the data visualization configuration required by your business.

First you need to install the Grafana ClickHouse data source plugin: [view plugin installation steps](https://grafana.com/grafana/plugins/vertamedia-clickhouse-datasource/installation)

### Add data source

Add the data source, i.e. the data source information that is displayed. Select the **ClickHouse** type data source and input the connection parameters to configure it. By default, the key configuration information is as follows:

![image-20200916110233266](https://static.emqx.net/images/384986bdbaca56ab3bf8268fa9681ab4.png)



### New Dashboard

After you have added the data source, add the data dashboard information that needs to be displayed. After clicking **New Dashboard**, select **+ Query** to add the data dashboard by query.

### Average panel

Use Grafana's visual query builder to query the average of all devices.

When the ClickHouse plugin generates SQL, it will automatically populate a number of variables, and Grafana can recognize these variables when querying:

- $timeSeries: specified DateTime column and some conversion logic to ensure that the format we used in the data collection that Grafana can also use in the display.
- $table: table name in the database
- $timeFilter: automatically generated time series filter conditions

According to the needs, we need to add two new AVG-processed fields:

```sql
SELECT
    $timeSeries as t,
    avg(temperature) as temperature,
    avg(humidity) as humidity
FROM $table

WHERE $timeFilter

GROUP BY t

ORDER BY t
```

For charts with a time series, such as line charts, Grafana needs a DateTime column to select the time series. We must input a time series and the column must be of DateTime or Timestamp data type.

Click the edit button in the red box below to enter the table name, time column configuration:

![image-20200916110544930](https://static.emqx.net/images/ff07248e60a570409f1ee5bc64925fb4.png)

Select the database and data table. If there are DateTime and Date fields in the table, you can select them from Column:DateTime and Column:Date.

- Column:Date: used to filter data as Grafana drags the time range
- Column:DateTime: used as time data when the time-series is displayed.

<img src="https://static.emqx.net/images/07b9a092530b50bfa314447a189f8d4b.png" alt="image-20200916111101870" style="zoom:67%;" />

When you are done, click the edit button again, click the upper right corner of the icon to select a time range, make sure there is data in the time range, click the refresh icon to refresh the data and you will see the rendered average panel.

![image-20200916111420196](https://static.emqx.net/images/1eda9c065405599c21d9163d334e1a08.png)

After completing creation, click the Back button in the upper left corner. And then you successfully added a data panel in this Dashboard. Click on the **save** icon in the top navigation bar and input the Dashboard name to complete the creation of the Dashboard.



### Maximum value panel

Continuously click the **add panel** button on the Dashboard to add the maximum and minimum charts. The procedure is the same as adding an average value, but only adjust the **SELECT** statistic method field in the query to **AVG** function as **MAX**.

```sql
SELECT
    $timeSeries as t,
    max(temperature) as temperature,
    max(humidity) as humidity
FROM $table

WHERE $timeFilter

GROUP BY t

ORDER BY t
```



### Dashboard effect

Save the dashboard, drag and drop to adjust the size and position of each data panel, and finally get a better visual effect of the data dashboard. The upper right corner of the dashboard can select the time interval and automatic refresh time. At this time the device continues to send data collection data, the dashboard data values will change, achieving a better visualization effect.

![image-20200916112334081](https://static.emqx.net/images/684f512f88a96596d86e5590264e7ebe.png)



## Summary

So far, we use EMQ X + ClickHouse to complete IoT data transmission, storage, analysis and display the whole process of system construction. The reader can learn how EMQ X's extensive expansion capabilities and ClickHouse's leading data processing and analysis capabilities can be applied to IoT data collection. With a deeper understanding of Grafana's other functions, users can customize their improved data visualization analysis and even monitoring and alerting systems.
