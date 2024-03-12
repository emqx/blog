In this article, we will simulate temperature and humidity data and report it to the EMQX cloud on the GCP platform via the MQTT protocol, after which we will use the EMQX Cloud data integration to enable the NAT gateway and save the data to the InfluxDB Cloud over the public network.

## EMQX Cloud

[EMQX Cloud](https://www.emqx.com/en/cloud) is the world's first fully managed MQTT 5.0 public cloud service for IoT from EMQ. It provides a one-stop O&M colocation and a unique isolated environment for MQTT services. In the era of Internet of Everything, EMQX Cloud can help you quickly build industry applications and easily realize the collection, transmission, computation, and persistence of IoT data.

With the infrastructure provided by cloud providers, EMQX Cloud is available in dozens of countries and regions around the world, providing low-cost, secure, and reliable cloud services for 5G and Internet of Everything applications.

For more information, please go to the [EMQX Cloud website](https://www.emqx.com/en) or see the [EMQX Cloud documentation.](https://docs.emqx.com/en/cloud/latest/)

## InfluxDB Cloud

[InfluxDB Cloud](https://docs.influxdata.com/influxdb/v2.6//cloud/sign-up/) is a fully managed and hosted version of InfluxDB 2.0, the time series platform purpose-built to collect, store, process and visualize metrics and events. As an open source chronological database developed by InfluxData, focusing on high performance reading and writing; efficient storage and real-time analysis of massive chronological data, etc. It is ranked No.1 in the DB-Engines Ranking chronological database, and is widely used in DevOps monitoring, IoT monitoring, real-time analysis, and other scenarios. 

InfluxDB is simple to deploy and easy to use, taking full advantage of the Go language in its technical implementation, and can be deployed independently without any external dependencies. Provides a SQL-like query language with a friendly and easy-to-use interface. Rich aggregation and sampling capabilities, flexible Retention Policy to set the retention time and number of copies of data, while ensuring data reliability; timely deletion of expired data to free up storage space, and flexible continuous query to achieve the sampling of massive data. A wide range of protocols is supported. In addition to native protocols such as HTTP and UDP, it is also compatible with the communication protocols of components such as CollectD, Graphite, OpenTSDB, and Prometheus.

## Create Deployments

### Create EMQX Cluster

Create a GCP deployment of EMQX Cloud, other options default.

![Create EMQX Cluster](https://assets.emqx.com/images/1174e1b4affe999c0e935536066845e2.png)

When the status is Running, the creation of the deployment is complete.

![Running status](https://assets.emqx.com/images/f835885d158f3a51fbded858cbe8f9de.png)

### Create InfluxDB Cloud instances

If you are creating an InfluxDB Cloud instance for the first time, you can refer to the [help document](https://docs.influxdata.com/influxdb/v2.6//cloud/sign-up/). Go to the Load Data page and find a new token. You could choose to activate/deactivate the token.

![Create InfluxDB Cloud instances](https://assets.emqx.com/images/4c0fe0dfe5b449310a94074513a71ca9.png)

After logging in to InfluxDB's console, go to the Load Data page and create a new bucket. Name the bucket and click Create.

![Create InfluxDB Cloud instances](https://assets.emqx.com/images/e362605a32306b611e7738a434b172be.png)

## Enable NAT Gateway

[NAT gateways](https://docs.emqx.com/en/cloud/latest/vas/nat-gateway.html#service-activation) can provide network address translation services to provide Professional deployments with the ability to access public network resources without the need for VPC peering connections.

![Enable NAT Gateway](https://assets.emqx.com/images/400500776cc3fc48c72b26d7891cf59c.png)

## [Data Integrations](https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_confluent.html)

### 1. Create InfluxDB HTTP V2 resources

Go to the Data Integrations page. On the data integration page, click **InfluxDB HTTP V2** Service resources.

![Create Kafka resources](https://assets.emqx.com/images/90dd5e92a1e4998a475506817755b7de.png)

Fill in the InfluxDB Cloud connection details, and then click test. Please check the InfluxDB service if the test fails. Click the New button after the test is passed and you will see the Create Resource successfully message.

![Create Kafka resources](https://assets.emqx.com/images/b4414f5e97cc8336dab60f460a7632de.png)

### 2. Create a new rule

After the resource is successfully created, you can return to the data integration page and find the newly created resource, and click create rule. Our goal is that as long as the emqx/test topic has monitoring information, the engine will be triggered. Certain SQL processing is required here:

- Only target the topic "temp_hum/emqx"
- Get the three data we need: location, temperature, humidity

According to the above principles, the SQL we finally get should be as follows:

```
SELECT
    payload.location as location,
    payload.temp as temp,
    payload.hum as hum
FROM "temp_hum/emqx"
```

![Create a new rule](https://assets.emqx.com/images/f6ca1081f538d018eefd704043804fbe.png)

You can click SQL Test under the SQL input box to fill in the data:

- topic: temp_hum/emqx
- payload:

```
{
  "temp": 26.3,
  "hum": 46.4,
  "location":"Prague"
}
```

Click Test to view the obtained data results. If the settings are correct, the test output box should get the complete JSON data as follows:

![JSON data](https://assets.emqx.com/images/13535bfdaf0782247cabbcf9a057a76f.png)

If the test fails, please check whether the SQL is compliant and whether the topic in the test is consistent with the SQL filled in.

### 3. Add Action to Rule

After completing the rule configuration, click Next to configure and create an action. Then enter the fields and tags as follows:

```
Measurement: temp_hum
Fields: temp ${temp}, hum ${hum}
Tags: location ${location}
```

![Add Action to Rule](https://assets.emqx.com/images/619ed1845e598d6225060c5de066731f.png)

## Verification

### 1. Use MQTTX to simulate temperature and humidity data reporting

We recommend you to use [MQTTX](https://mqttx.app/), an elegant cross-platform MQTT 5.0 desktop client to subscribe/publish messages.

Click on the add button and fill in the deployment information to connect to the deployment. You need to replace `broker.emqx.io` with the created deployment [connection address](https://docs.emqx.com/en/cloud/latest/create/overview.html#view-deployment-information),  add [client authentication information](https://docs.emqx.com/en/cloud/latest/deployments/auth_overview.html#authentication) to the EMQX Cloud console.  Enter the topic name and payload message to publish the message.

![MQTT Client](https://assets.emqx.com/images/fe1ee590e24e224b90624c2017ba8aaf.png)

### 2. View rules monitoring

Check the rule monitoring and add one to the number of success.

![View rules monitoring](https://assets.emqx.com/images/db395bda8294d1af35be4bec93ed92c9.png)

### 3. View results in InfluxDB console

Go back to the InfluxDB console and go to the Data Explorer page. Select the bucket and filter the measurement, fields, then InfluxDB will generate the tables and graphs for you.

![View results in InfluxDB console](https://assets.emqx.com/images/c992698000f2f2c93722a8acd4c33296.png)

![View results in InfluxDB console](https://assets.emqx.com/images/15ce569eda5f1d9ccb8f8cf3fe8520d2.png)

![View results in InfluxDB console](https://assets.emqx.com/images/6b7c912f38f5ee3cc9b91d986d741304.png)

So far, we have used EMQX Cloud data integration based on the GCP platform to save the entire process of data to the InfluxDB cloud over the public network.


## Related resources

- [Integrating MQTT Data into InfluxDB for a Time-Series IoT Application](https://www.emqx.com/en/blog/building-an-iot-time-series-data-application-with-mqtt-and-influxdb)
- [MQTT Performance Benchmark Testing: EMQX-InfluxDB Integration](https://www.emqx.com/en/blog/mqtt-performance-benchmark-testing-emqx-influxdb-integration)
- [Getting Data from EMQX Cloud with InfluxDB Native Collector](https://www.emqx.com/en/blog/getting-data-from-emqx-cloud-with-influxdb-native-collector)
- [Supercharging IIoT with MQTT, Edge Intelligence, and InfluxDB](https://www.emqx.com/en/blog/supercharging-iiot-with-mqtt-edge-intelligence-and-influxdb)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
