![画板 172x8.png](https://assets.emqx.com/images/f8a1fbc68db40b2edeb4e257b2febc79.png)

## Background

Taking the common scenarios of Internet of things as an example, this article introduces how to use the EMQX message middleware and the open source data visualization solution of  InfluxDB + Grafana to  conveniently display a large amount of time-series data of IoT devices.

The device data and storage of the access platform in the IoT project have the following characteristics:

- The dimensions and frequency of data collection and number of devices  are relatively large. The amount of data collected is relatively large, which puts a lot of pressure on the throughput of the message server access point and the consumption of back-end database data storage space;
- Data is reported, transmitted, and stored in accordance with the collection cycle, which is generally in time series;

Therefore, it is a better choice to use time series database in IoT projects, which can bring significant performance improvements, including higher capacity, faster large-scale queries (some databases support more queries than other relational databases), and better data compression rates. . After the data is stored in the database, other method such as data visualization systems, are often required to statistics and display the data in accordance with the rules to achieve business requirements such as data monitoring and index statistics, which aimed to give full play to the value of data.

## Business Scenario

Assume that there is a batch of devices, and each device has a Client ID. All devices send data to the corresponding topic on the MQTT message server through the [MQTT protocol](https://www.emqx.com/en/mqtt-guide). The topic is designed as follows:

```bash
devices/{client_id}/messages
```

The data format sent by each device is JSON, and the temperature and humidity data collected by the sensor are sent.

```json
{
    "temperature": 30,
    "humidity" : 20
}
```

Now it needs real-time storage to view the data at any subsequent time. The following requirements are proposed:

- Each device reports data at a frequency of once every 5 seconds, and the database needs to store each piece of data;
- Through the visualization system, we can view the average value, maximum value, minimum value of temperature/humidity of any time interval , and the average temperature/humidity value of all data  .

### Final effect

![image20191125152935211.png](https://assets.emqx.com/images/40bd3a648d5bb97ca9b8f1ec13c4a91e.png)

The time interval and automatic refresh time can be selected in the upper right corner of the dashboard. At this time, the device continues to send data, and the data value of the dashboard will change accordingly, achieving a better visualization effect.

## Introduction of the solution

At present, there are many IoT message middleware, time series databases, and data visualization products on the market. In combination of data collection and reporting, network access, message storage and visualization functions, EMQX (high-performance IoT MQTT message middleware) + InfluxDB (time series database) + Grafana (beautiful and powerful visual monitoring indicator display tool) is undoubtedly the best IoT data visualization integration solution.

The overall architecture of the solution is shown in the following figure:

![image20191125163959537.png](https://assets.emqx.com/images/a6a6133516dd6f26f6b813f5500f96c8.png)

- **EMQX**：[EMQX ](https://github.com/emqx/emqx)is developed based on the highly concurrent Erlang / OTP language platform, and supports millions of connections and distributed cluster architecture. It is an open source MQTT message server with publish-subscribe mode. EMQX has a lot of built-in out-of-the-box features.  Its enterprise version of EMQX Enterprise supports high-performance storage of device messages to InfluxDB through a rule engine or message persistence plug-in. Open source users need to handle the message storage themselves.
- **InfluxDB :** InfluxDB is an open source time series database developed by InfluxData. Written by Go, it focuses on querying and storing time series data with high performance. InfluxDB is widely used in the scenarios of monitoring data in storage systems and real-time data in the IoT industry.
- **Grafana:**  Grafana is a cross-platform, open source measurement analysis and visualization tool, which can query and visualize the collected data. It can create client charts quickly and flexibly. The panel plug-in has many different ways to visualize indicators and logs. The official library has a wealth of dashboard plug-ins, such as heat chart, line chart and other display ways. It supports Graphite, InfluxDB , OpenTSDB, Prometheus, Elasticsearch, CloudWatch and KairosDB and other data sources, supports independent / hybrid query display of data items. You can create custom alarm rules and notify them to other message processing services or components.



## Implementation steps

### Install EMQX, InfluxDB and Grafana

Each component used in this article has a Docker image. Except for a few configurations that need to be modified for EMQX to download and install, both InfluxDB and Grafana are built using Docker. Detailed installation steps are not described in this article.

There are services or installation package resources and tutorials of different operating systems/platforms on the websites of the three major components:

 - EMQX：EMQ website [https://www.emqx.com/zh](https://www.emqx.com/zh)
 - InfluxDB：InfluxData website [https://www.influxdata.com/](https://www.influxdata.com/)
 - Grafana：Grafana website [https://grafana.com/](https://grafana.com/) 



### EMQX Enterprise  installation

####  Installation

> If you are new to EMQX, we recommend you getting started with [EMQX Guide](https://docs.emqx.com/en/emqx/v3.0/). 

Visit [EMQ website](https://www.emqx.com/en/try)  to download the installation package suitable for your operating system. As data persistence is an function of enterprise version, you need to download EMQX Enterprise (you can apply for a license trial). At the time of writing this article, the latest version of EMQX Enterprise is v3.4.5. This function requires this version and above. The startup steps for downloading the zip package are as follows:

```bash
## Extract the downloaded installation package
unzip emqx-ee-macosx-v3.4.4.zip
cd emqx

## Copy the license file to the EMQX designated directory etc /, you needs to apply for a trial of the license or obtain it through a purchase authorization
cp ../emqx.lic ./etc

## Launch EMQX in console mode
./bin/emqx console
```



#### Change configuration


The configuration files needed in this article are as follows:

1. License file, EMQX Enterprise License file, covered with available licenses:

```
etc/emqx.lic
```



2. EMQX InfluxDB message storage plug-in configuration file, which is used to configure InfluxDB connection information and select the storage topic:

```bash
etc/plugins/emqx_backend_influxdb.conf
```

Fill in the plug-in configuration information according to the actual situation of deployment:

```bash
backend.influxdb.pool1.server = 127.0.0.1:8089

backend.influxdb.pool1.pool_size = 5

## Whether or not set timestamp when encoding InfluxDB line
backend.influxdb.pool1.set_timestamp = true

## Store Publish Message
## Since the business only requires the devices / {client_id} / messages topice,topic filter with default configuration is modified here
backend.influxdb.hook.message.publish.1 = {"topic": "devices/+/messages", "action": {"function": "on_message_publish"}, "pool": "pool1"}
```



3. EMQX InfluxDB message store plugin message template file, used to define the message parsing template:

```bash
## template file
data/templates/emqx_backend_influxdb_example.tmpl

## renamed
data/templates/emqx_backend_influxdb.tmpl
```

Because MQTT Message cannot be written directly to InfluxDB, EMQX provides the emqx_backend_influxdb.tmpl template file to convert the MQTT Message into a DataPoint that can be written to InfluxDB:

```bash
{
  "devices/+/messages": {
    "measurement": "devices",
    "tags": {
      "client_id": "$client_id"
    },
    "fields": {
      "temperature": ["$payload", "temperature"],
      "humidity": ["$payload", "humidity"]
    },
    "timestamp": "$timestamp"
  }
}
```

### InfluxDB installation

Install through docker, map data folder and `8089` udp port and `8086` port (used by Grafana):

> EMQX only supports the InfluxDB UDP channel, which requires influx_udp plugin support, and the database name is specified as db

```bash
## use influx_udp plugin
git clone https://github.com/palkan/influx_udp.git

## Go to the plugin directory
cd influx_udp

## Create and startup container via plugin configuration
docker run --name=influxdb --rm -d -p 8086:8086 -p 8089:8089/udp \
	-v ${PWD}/files/influxdb.conf:/etc/influxdb/influxdb.conf \
  -e INFLUXDB_DB=db \
  influxdb:latest

## Check container running status after startup
docker ps -a
```



**At this point, you can restart EMQX and launch the plugin to apply the above configuration**:

```bash
./bin/emqx stop

./bin/emqx start

## Or use console mode for more information
./bin/emqx console

## launch plugin
./bin/emqx_ctl plugins load emqx_backend_influxdb

## After successful startup, there will be the following prompt
Plugin emqx_backend_influxdb loaded successfully.
```



### Grafana installation

Install and start Grafana via Docker using the following command:

```bash
docker run -d --name=grafana -p 3000:3000 grafana/grafana
```

After successful startup, visits `http://127.0.0.1:3000` to access the Grafana visualization panel, and use ` admin` `admin` as default username and password to complete the initial login. After login, follow the prompts to modify the password and log in to the main interface with the new password. :

![image20191125100532923.png](https://assets.emqx.com/images/26b9267ec7bc011f1222cef95c6d6a60.png)



## Write simulation data

The simulation data needs to be written before the visual configuration, which facilitates the effect preview during the configuration.

The following script simulates a scenario in which 100 devices report simulated temperature and humidity data and send it to EMQX every 5 seconds in the past 12 hours. After the Node.js platform is installed, the reader can start it with the following command:

```bash
npm install mqtt mockjs --save
node mock.js
```

After the simulation script is executed, the data will be written to the InfluxDB `db` database. Enter the InfluxDB container and view the data with the following command:

```bash
## enter docker container
docker exec -it influxdb bash

## Enter the influxdb command line
root@581bde65650d:/# influx

## Switch to the db database
use db;

## Query data
select * from devices limit 1;

## Query result
name: devices
time                client_id      humidity temperature
----                ---------      -------- -----------
1574578725608000000 mock_client_1  54.33    98.5
```



The simulation script is as follows:

```javascript
// Node.js
// mock.js
const mqtt = require('mqtt')
const Mock = require('mockjs')

class MockData {
  constructor(clientNum = 20) {
    this.EMQX_SERVER = 'mqtt://localhost:1883'
    this.clientNum = clientNum
    this.clients = {}
    this.startMock()
  }

  async startMock() {
    const now = Date.now()
    // last 12h every 5s
    for (let ts = now - 12 * 3600 * 1000; ts <= now; ts += 5 * 1000) {
      for (let i = 0; i < this.clientNum; i++) {
        const clientId = `mock_client_${i}`
        const client = this.clients[clientId] || await this.createClient(clientId)
        this.clients[clientId] = client
        const mockData = this.getMockData()
        client.publish(`devices/${clientId}/messages`, JSON.stringify(mockData))
        console.log(`${clientId} send temperature ${mockData.temperature} humidity ${mockData.humidity}`)
      }
    }
  }

  /**
   * Init a virtual mqtt client
   * @param {string} clientId ClientID
   */
  createClient(clientId) {
    return new Promise((resolve, reject) => {
      const client = mqtt.connect(this.EMQX_SERVER, {
        clientId,
      })
      client.on('connect', () => {
        console.log('client s% connected', clientId)
        resolve(client)
      })
      client.on('error', (e) => {
        reject(e)
      })
    })
  }

  /**
   * Generate mock data
   */
  getMockData() {
    return {
      temperature: parseFloat(Mock.Random.float(22, 100).toFixed(2)),
      humidity: parseFloat(Mock.Random.float(12, 86).toFixed(2)),
    }
  }
}

// startup
new MockData(100)
```



## Visual configuration

After the components are installed and the simulation data is successfully written, follow the Grafana visual interface operation guide to complete the visual configuration of the data required by the business.

### Add data source

Add a data source, that is the displayed data source information. Select the  **InfluxDB** type data source and enter the connection parameters to configure it. By default, the key configuration information is as follows:

- URL: Fill in the InfluxDB connection address. Since we use Docker installation, Grafana is not connected to the InfluxDB container network. Here you can enter the current server intranet/LAN address instead of `127.0.0.1` or` localhost`;
- Auth: InfluxDB startups without authentication by default, fill in according to the actual situation;
- Database: Fill in `db` which the default database name for EMQX.



### New Dashboard

After adding the data source, add the data dashboard information that needs to be displayed. The dashboard is a collection of multiple visualization panels. After clicking  **New Dashboard** , select **Add Query** to add a data panel by query:

![image20191125135546283.png](https://assets.emqx.com/images/10c568eea65264ba063ec193719012f9.png)





There are four steps required to create a panel, **Queries, Visualization, General (chart configuration), Alert**, and complete the following creation process following the business requirements :



### Temperature and humidity average value panel

Use Grafana's visual query builder to find the average value of all devices:

- FROM: Select the `measurement` of the data and configure it according to the `emqx_backend_influxdb.tmpl` file. Here, the `measurement` is `devices`.
- SELECT: The fields for selection and calculation. Here, the two queries need to be processed by the **Aggregation** function. Select the `temperature` `mean` and `humidity` `mean` to query and calculate the average value of the temperature and humidity fields.
- GROUP BY: Use time interval aggregation by default.
  -  `time($__interval)` function means to take the data in the `($__interval)`  time interval, for example, `time(5s)` means to take the value from the original data for every 5 second time interval for calculation (calculation in SELECT)
  -  The `fill` parameter indicates the default value when there is no value. When it is` null`, the data point will not be displayed on the chart;
  -  `tag` is Optional, which is displayed according to the specified tag.
- ALIAS BY: An alias for this query for easy visualization.

**Visualization** does not change by default,  the panel name is changed to `Device temperature and humidity mean value` in **General**. If you need to monitor and alarm the business, you can arrange alarm rules in **Alert**. This function is Only for visual display, not for use here.

![image20191125140117416.png](https://assets.emqx.com/images/722bf7a8c78edd0707480ddf39a6c303.png)


After the creation is complete, click the back button in the upper left corner, and a data panel is successfully added to the Dashboard. Click the **Save** icon in the top navigation bar, and enter the Dashboard name to complete the creation of Dashboard.


![image20191125144011475.png](https://assets.emqx.com/images/60fedfccc52a0162df1586be2a7e2f8b.png)




### Temperature and humidity minimum/maximum value panel

Continue to click the **Add panel** button on the Dashboard to add the maximum and minimum temperature  charts. The operation steps are the same as adding the average value, which only adjust the  **SELECT**  statistical method field in the query to the `max`  and ` min` methods.

### Temperature and humidity total average value/ data number panel

Continue to click the **Add panel** button on the Dashboard to add the panel of total average value of temperature and humidity, and the number of data. The operation steps are similar to the above two operations. Use the `count` and ` mean` methods to operate on the specified fields. Cancel the **GROUP BY** field to complete the query.  Select the chart type as  Gauge in **Visualization** configuration.

Save the dashboard, drag and adjust the size and position of each data panel, and finally get a data dashboard with better visual effects. After the final report is completed, the effect shown at the beginning of the article is presented.

## Summary

At this point, we have completed the implementation of the EMQX and InfluxDB + Grafana IoT data visualization integration solution. Through this article, readers can understand that the rich expansion capabilities of EMQX can be used to develop a visualization system based on InfluxDB + Grafana in a data visualization solution very quickly and flexibly to achieve mass data storage, calculation analysis and display. After deep learning and mastering other functions of Grafana, users can customize more perfect data visualization and monitoring/alarm system.

------

Welcome to our open source project [github.com/emqx/emqx](https://github.com/emqx/emqx). Please visit the [ documentation](https://docs.emqx.com/en/emqx/latest/) for details.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
