## Introduction

InfluxData recently announced the availability of Native Collectors, bringing native data collection to the InfluxDB Cloud. This will provide developers with the fastest way to get data from third-party MQTT brokers such as EMQX Cloud into the InfluxDB Cloud without the need for additional software or new code.

While integrating with a private MQTT broker is always possible, this is an easier way to do cloud-to-cloud integration.

In this tutorial, I'll show you step-by-step how to integrate InfluxDB Cloud with EMQX Cloud, a leading MQTT service provider, using this new native collector.

## Four steps integration

The integration only needs 4 steps:

1. Create an MQTT broker on EMQX Cloud – 3 mins
2. Create a bucket on InfluxDB Cloud – 3 mins
3. Config the native collector – 2 mins
4. Verification – 1 min

Yes! You will get data from EMQX Cloud to InfluxDB Cloud in less than 10 minutes!

Now, let’s check it out.

## Step 1: Create an MQTT broker on EMQX Cloud.

Creating a dedicated MQTT broker on EMQX Cloud is as easy as a few clicks.

#### Get an account

Go to [EMQX Cloud](https://www.emqx.com/en/cloud) and click start free to register an account if you are new to EMQX Cloud.

#### Create an MQTT cluster

Once logged in, click "Cloud Console" under the account menu and you will be able to see the green button to create a new deployment.

![Create an MQTT instance on EMQX Cloud](https://assets.emqx.com/images/91dd6aab2d0f99a82bc45bd13fd409b0.jpeg)

<center>Create an MQTT instance on EMQX Cloud</center>

EMQX Cloud offers a 14-day free trial of Standard and Professional plans. While the Pro plan offers more features, the Standard plan is more than enough for this tutorial.

![This tutorial uses Standard Plan](https://assets.emqx.com/images/b493525c1d7348fd74e22c077ec89b0a.jpeg)

<center>This tutorial uses Standard Plan</center>

Click "Create Now" and follow a step-by-step walkthrough to complete the deployment. After clicking the final "Deploy" button, you will see the instance created as follows:

![Creating MQTT instance](https://assets.emqx.com/images/312366cddaeb3ab4e17f6fceb3ab2397.jpeg)

<center>Creating MQTT instance</center>

It will take a few minutes to get a running instance.

![Instance in running status](https://assets.emqx.com/images/f1dabe608d193b5d699affe040621975.jpeg)

<center>Instance in running status</center>

Once the status changes to Running, click the card to go to the cluster overview.

#### Get Connection Adress and Port

On the overview page, you will see the instance details. Note the connection address and connection port here, which is required when we configure the integration on InfluxDB Cloud.

![MQTT Broker Connection Details](https://assets.emqx.com/images/ace95719204e18152b1d139de3c985e0.jpeg)

<center>MQTT Broker Connection Details</center>

Each EMQX Cloud instance creates four listeners for MQTT connections (MQTT, MQTT with TLS, [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket), and MQTT over WebSocket with TLS). However, InfluxDB Cloud currently only supports the MQTT protocol, so you only need to note the first port.

#### Add Credentials for MQTT connection

The last thing on EMQX Cloud is to create credentials for the MQTT connection. Click Authentication and ACLs on the left menu, then click Authentication in the submenu.

![Authentication Page](https://assets.emqx.com/images/cb71dc1a319b30d99ff8ef4159fdcc9f.jpeg)

<center>Authentication Page</center>

Click the "Add" button on the right and provide the username and password for the mqtt connection later. Here I will use "test" and "influxdb" as username and password.

![Add Credentials](https://assets.emqx.com/images/d79d927ff838b1f3cbf29406b5a096ee.jpeg)

<center>Add Credentials</center>

Click ‘Confirm’ and everything is settled down on EMQX Cloud side.

Now you have a running MQTT broker provided by EMQX Cloud. Let’s move on to Step 2.

## Step 2: Create a bucket on InfluxDB Cloud

#### Create an InfluxDB Cloud account

If you are using [InfluxDB Cloud](https://www.influxdata.com/products/influxdb-cloud/) for the first time, you will also need to create an account.`

#### Create a Bucket for data persistence

Once logged in, go to the console page and click the "Buckets" button in the menu.

![Go to the Buckets page](https://assets.emqx.com/images/45df0c7d8cd9862cee8a742605952c31.jpeg)

<center>Go to the Buckets page</center>

Click ‘Create Bucket’ on the right side and fill out the form.

![Create a new bucket](https://assets.emqx.com/images/11e74c950c499393f1b1bb7581c49feb.jpeg)

<center>Create a new bucket</center>

I will use "emqxcloud" as the bucket name here. Click "Create".

OK, now you have your bucket ready. Let's try out the new Native Collector.

## Step 3: Config the native collector

#### Go to the Native Subscriptions page

Click the ‘NATIVE SUBSCRIPTIONS’ tab on the bucket page.

![Native subscriptions page](https://assets.emqx.com/images/f41ca2ca97beec67f4d3870cf8733e1d.jpeg)

<center>Go to the native subscriptions page</center>

*Please note that this feature is available with usage-based plans only. So you need to upgrade your account by linking a credit card. Luckily, InfluxDB Cloud offers $250 credits for new users.*

#### Create a Subscription

Go ahead and click Create Subscription.

![Create an MQTT subscription](https://assets.emqx.com/images/a40642c4d132d380f81df3ad4b1a6fce.jpeg)

<center>Create an MQTT subscription</center>

On the integration configuration page, there are 5 sections:

- Config Broker Details
- Config Security Details
- Subscribe to a Topic
- Set write destination
- Define data parsing rules.

Don't worry, let's go through them one by one.

#### Config Broker Connection

To create a subscription, InfluxDB first needs to connect to the target MQTT broker on EMQX Cloud. 

Here we will use the connection details we created on EMQX Cloud.

![Config Broker Details](https://assets.emqx.com/images/12da6b51e9307af46ac448960a4953d1.jpeg)

<center>Config Broker Details</center>

This part has 4 inputs:

1. Subscription Name: Name your subscription as desired. I use ‘EMQX’ in this example.
2. Description: (Optional) Give this subscription a short description.
3. Hostname or IP Address: The connect address you got from EMQX Cloud in Step 1.
4. Port: The connect port you got from EMQX Cloud in Step 1.

#### Config Security Details

Choose BASIC in ‘SECURITY DETAILS’ and set the username and password you created in EMQX Cloud.

![Add credentials for the MQTT connection](https://assets.emqx.com/images/e2293fc6db0b1087bacf506de9def0d6.jpeg)

<center>Add credentials for the MQTT connection</center>

***Double check the address, port, and username/password. They are essential for establishing a successful MQTT connection to EMQX cloud.***

#### Subscribe to a Topic

Once the connection is configured, we need to tell InfluxDB Cloud which topics it should listen to.

![Add a subscription topic](https://assets.emqx.com/images/96639440a9c149d889241723997f1123.jpeg)

<center>Add a subscription topic</center>

Just give the topic name here. I used "influxdb" for this demo. It's easy to understand. All data sent to this topic will be forwarded to InfluxDB Cloud.

While we've used an explicit topic name here, InfluxDB Cloud Native Collector do support wildcards like "+" and "#". Using wildcards is more practical in real use cases. Check [InfluxDB Cloud’s doc](https://docs.influxdata.com/influxdb/v2.6//cloud/) for more information.

#### Set Write Destination

In the "WRITE DESTINATION" section, leave it as default as there is only one Bucket. However, if you have multiple buckets, make sure to select the right one.

![Select the write destination bucket](https://assets.emqx.com/images/6c3d7d76d22438018f5c7e6a1577b4b5.jpeg)

<center>Select the write destination bucket</center>

#### Define Data Parsing Rules

Now, the last part: Define Data Parsing Rules.

InfluxDB Cloud Native Collector supports three data formats. In this demo, we will use the JSON format. It's easier to read in a demo.


![Define a data parsing rule](https://assets.emqx.com/images/0f6dbc2b7ce34fcfb5c58acd20a3adad.jpeg)

<center>Define a data parsing rule</center>

In the data parsing rules, you need to provide information on how to convert JSON data into measurements and fields in InfluxDB.

In the demo, I will use a very simple message with only one temperature data. 

Sample JSON payload:

```
{
  "temperature":25
}
```

To convert this JSON message to meric in InfluxDB Cloud, we need to perform the following mapping:

#### TIMESTAMP: 

Timestamp is optional. If not provided, it will use the server's timestamp as default value when inserting data.

#### MEASUREMENT:

Measurement can be parsed from JSON or a static name. To keep this demo as simple as possible, I use the static name "room_temperature" in this demo.

#### FIELD:

In this demo, I used a JSON message containing only temperature, so I used "temperature" as the name and the JSON path "$.temperature" to get the data from the JSON body. InfluxDB Cloud uses JSONPath to fetch data from a JSON object. Check [JSONPath’s](https://jsonpath.com/) doc for its syntax.

#### Save Subscription

Last but not least, don’t forget to save the subscription.

![Save the subscription](https://assets.emqx.com/images/0a3d895cf64f951194b56769fc635e38.jpeg)

<center>Save the subscription</center>

Click ‘SAVE SUBSCRIPTION’ And THAT’S IT!

#### Verify the subscription is running

![Native subscription is running](https://assets.emqx.com/images/472905ccc18a0a057f482b26e139e466.jpeg)

<center>Native subscription is running</center>

It should show up running on the native subscriptions list.

#### Everything is settled

Congratulations! You should have successfully integrated InfluxDB Cloud and EMQX Cloud. The temperature data sent to EMQX Cloud should be continuously persisted to the target bucket on InfluxDB Cloud.

Now, let’s move on to the last Step. Check out if it’s working as expected.

## Step 4: Verification

How to know if the integration is a success?  Simple answer: Let’s send a message to the MQTT broker on EMQX Cloud and see if it appears on the dashboard of InfluxDB cloud!

#### Choose an MQTT client

Use can use any MQTT client as you like. In this tutorial, I will use [MQTTX](https://mqttx.app/), a user-friendly MQTT desktop application that is good for testing purposes.

![Create New Connection](https://assets.emqx.com/images/0a1b227fb93b3a9c9a39cde30f00cf9f.jpeg)

<center>Create New Connection</center>

#### Connect to EMQX Cloud

Click ‘New Connection’ on MQTTX and fill out the connection form:

![Set Connection Details](https://assets.emqx.com/images/006caa8977541d5da34f6887adf99dac.jpeg)

<center>Set Connection Details</center>

1. Name: The connection name. Use whatever name you want.
2. Host: The MQTT broker connection address. Same as you used in InfluxDB Cloud setup.
3. Port: MQTT broker connection port. Same as you used in InfluxDB Cloud setup.
4. Username/Password: In the demo, I use the same credentials as in InfluxDB Cloud Configuration. You can add new credentials in EMQX Cloud if you want.

Click the "Connect" button in the upper right corner and the connection should be set up.

#### Send messages to EMQX Cloud

Now you can use this tool to send messages to the MQTT broker on EMQX Cloud.

![Send messages to EMQX Cloud](https://assets.emqx.com/images/c1eb827964cb4cd76ddf6315415ea4cd.jpeg)

<center>Send messages to EMQX Cloud</center>

Inputs:

1. Set payload format to “JSON”.

2. Set the topic: influxdb (the topic of the InfluxDB subscription we just set up)

3. JSON body: 

   ```
   {"temperature": 25}
   ```

   

Click the Send icon on the right. You can change the temperature value and send more data to the MQTT broker. The more data, the richer the chart will be displayed on the dashboard.

#### Check the data on InfluxDB Cloud

Now, it's time to view the data on InfluxDB Cloud. Ideally, the data you send using MQTTX will go into EMQX Cloud and then be persisted to the target bucket in InfluxDB Cloud.

![Go to Data Explorer](https://assets.emqx.com/images/9637a3dd3ff93d0afa9784221b8f833c.jpeg)

<center>Go to Data Explorer</center>

Let’s go back to InfluxDB Cloud and Open the data explorer by clicking the ‘Data Explorer' icon on the left menu.

![Make a Query to Fetch the Data](https://assets.emqx.com/images/8f9e088b096f9357b8e54e9a9aa10b76.jpeg)

<center>Make a Query to Fetch the Data</center>

Create a query on the UI by setting FROM, MEASUREMENT, and click the submit button and you should be able to see the data chart. This proves that the data you sent to EMQX Cloud has been successfully persisted to InfluxDB Cloud.

## Summary

Well, without a single line of code, now you can use EMQX Cloud to fetch data from any device or clients using standard MQTT protocol and focus on writing your IoT application with data persisted in InfluxDB Cloud.

In less than 10 minutes, you can leverage services from EMQX Cloud and InfluxDB Cloud with the new Native MQTT collector for a complete data flow from ingestion to persistence.


## Related resources

- [Integrating MQTT Data into InfluxDB for a Time-Series IoT Application](https://www.emqx.com/en/blog/building-an-iot-time-series-data-application-with-mqtt-and-influxdb)
- [MQTT Performance Benchmark Testing: EMQX-InfluxDB Integration](https://www.emqx.com/en/blog/mqtt-performance-benchmark-testing-emqx-influxdb-integration)
- [Supercharging IIoT with MQTT, Edge Intelligence, and InfluxDB](https://www.emqx.com/en/blog/supercharging-iiot-with-mqtt-edge-intelligence-and-influxdb)
- [Save MQTT Data from EMQX Cloud on GCP to InfluxDB Cloud through the public network](https://www.emqx.com/en/blog/save-mqtt-data-from-emqx-cloud-on-gcp-to-influxdb-cloud-through-the-public-network)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
