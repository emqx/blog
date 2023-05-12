In [the previous article](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-04), we described how to transfer data to GCP using VPC Network Peering. In addition to this approach, we have an even simpler one. In this article, we will describe how to use EMQX Cloud's data integration feature to bridge data to GCP pub/sub and then transfer data to other applications (e.g. data analytics, database services).


## Brief

In this article, we will simulate temperature and humidity data and report it to the EMQX Cloud via the MQTT protocol, after which we will use the EMQX Cloud data integration to bridge the data to the GCP Pub/Sub.

Tips:

1. Professional deployment on the GCP platform uses the private network by default; no additional network configuration is required.
2. But for professional deployment (AWS, Azure) users: Please complete the [NAT gateway](https://docs.emqx.com/en/cloud/latest/vas/nat-gateway.html#service-activation) first; all IPs mentioned below refer to the public IP of the resource.
3. So we recommend you use professional deployment on the GCP platform.


## GCP Pub/Sub Introduction

[GCP Pub/Sub](https://cloud.google.com/pubsub) is an asynchronous and scalable messaging service that decouples services producing messages from services processing those messages.

Pub/Sub allows services to communicate asynchronously, with latencies on the order of 100 milliseconds.

Pub/Sub is used for streaming analytics and data integration pipelines to ingest and distribute data. It's equally effective as a messaging-oriented middleware for service integration or as a queue to parallelize tasks.

Pub/Sub enables you to create systems of event producers and consumers, called publishers and subscribers. Publishers communicate with subscribers asynchronously by broadcasting events, rather than by synchronous remote procedure calls (RPCs).

Publishers send events to the Pub/Sub service, without regard to how or when these events are to be processed. Pub/Sub then delivers events to all the services that react to them. In systems communicating through RPCs, publishers must wait for subscribers to receive the data. However, the asynchronous integration in Pub/Sub increases the flexibility and robustness of the overall system.

To get started with Pub/Sub, check out the [Quickstart using Google Cloud console](https://cloud.google.com/pubsub/docs/publish-receive-messages-console). For a more comprehensive introduction, see [Building a Pub/Sub messaging system](https://cloud.google.com/pubsub/docs/building-pubsub-messaging-system).


## Create Deployments

### Create EMQX Cluster

Create a GCP deployment of EMQX Cloud, other options default.

![Create a GCP deployment of EMQX Cloud](https://assets.emqx.com/images/81ccd7b4b8e396871fd860957d12f902.png) 

When the status is Running, the creation of the deployment is complete.

![Status is Running](https://assets.emqx.com/images/958646e84454851a00516d4b390dfb72.png)
 
### Create GCP Pub/Sub instances

If you are using GCP Pub/Sub for the first time, you can refer to the [help document](https://cloud.google.com/pubsub/docs/publish-receive-messages-console).

#### Create a topic

Enter the GCP Pub/Sub console, click Create Topic, and enter the Topic ID named my-topic to successfully create a Topic.

![Create a topic](https://assets.emqx.com/images/5ed160df6af690ebf3ca03008f623860.png)

Click on the Topic ID to view the Topic details.

![view the Topic details](https://assets.emqx.com/images/a76c93c9810cc77eb0d7a077989a1b32.png)

Click Subscriptions to view the subscribed topic details and message forwarding results.

![Click Subscriptions](https://assets.emqx.com/images/5d05980c1dcf7d1fbd325c6c8feadbed.png)


## [**Data Integrations**](https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_confluent.html)

### 1. Create GCP Pub/Sub resources

Go to the Data Integrations page. On the data integration page, click **GCP Pub/Sub** resources.

![Integrations page](https://assets.emqx.com/images/c98d376f013429ce3505551d8737dc69.png)

Fill in the Service Account JSON and other details, and then click test. Please check the GCP Pub/Sub service if the test fails.

Tips: Service Account JSON : Go to the GCP console, select the appropriate project - IAM & Admin - Service Accounts - Email, enter the email details page, click KEYS, and generate a JSON file for identity authentication.

![Create Resource](https://assets.emqx.com/images/90dfce853d47f6306b41261ebd7f0242.png)

Click the New button after the test is passed and you will see the Create Resource successfully message.

![Data Integrations](https://assets.emqx.com/images/53847892ce94e57ca0ec81ee2dabdf9a.png)

### 2. Create a new rule

Put the following SQL statement in the SQL input field. The device reporting message time (up timestamp), client ID, and message body (Payload) will be retrieved from the temp hum/emqx subject in the SQL rule, and the device ambient temperature and humidity will be read from the message body.

```
SELECT 
timestamp as up_timestamp, 
clientid as client_id, 
payload.temp as temp,
payload.hum as hum
FROM
"temp_hum/emqx"
```

![Create a new rule](https://assets.emqx.com/images/2aefbcfa2d73fc82bee46c5da1d6c0fb.png)

You can click SQL Test under the SQL input box to fill in the data:

- topic: temp_hum/emqx
- payload:

```
{
  "temp": 35.5,
  "hum": 43.6
}
```

 

Click Test to view the obtained data results. If the settings are correct, the test output box should get the complete JSON data as follows:

![Click Test](https://assets.emqx.com/images/1d95cb379a7fa7f7f2936d50d6952229.png)

If the test fails, please check whether the SQL is compliant and whether the topic in the test is consistent with the SQL filled in.

### 3. Add Action to Rule

Click Next to add a GCP Pub/Sub forwarding action to the rule once the SQL test succeeds. To demonstrate how to forward the data reported by the device to GCP Pub/Sub, we'll utilize the following GCP Pub/Sub topic and message template.

```
# GCP Pub/Sub message template 
{"up_timestamp": ${up_timestamp}, "client_id": ${client_id}, "temp": ${temp}, "hum": ${hum}}
```

![Add Action to Rule](https://assets.emqx.com/images/40e2c754f561c06137b1e2e1ec896938.png)

After successfully binding the action to the rule, click View Details to see the rule SQL statement and the bound actions.

![click View Details](https://assets.emqx.com/images/30172688a2a5184fa1aa37c7d4c9d7f9.png)

To see the created rules, go to Data Integrations/View Created Rules. Click the Monitor button to see the detailed match data of the rule.

![Click the Monitor button](https://assets.emqx.com/images/58b5faddc9148ddbbca33f9c390e093b.png)


## Verification

### 1. Use MQTTX to simulate data reporting

We recommend you use [MQTTX](https://mqttx.app/), an elegant cross-platform MQTT 5.0 desktop client to subscribe/publish messages.

Click on the add button and fill in the deployment information to connect to the deployment. You need to replace `broker.emqx.io` with the created deployment [connection address](https://docs.emqx.com/en/cloud/latest/create/overview.html#view-deployment-information), and add [client authentication information](https://docs.emqx.com/en/cloud/latest/deployments/auth_overview.html#authentication) to the EMQX Cloud console. Enter the topic name and payload message to publish the message.

![MQTT Client](https://assets.emqx.com/images/717ab6bb315876b7f6a83b1c57ae2540.png)

### 2. View rules monitoring

Check the rule monitoring and add one to the "Success" number.

![View rules monitoring](https://assets.emqx.com/images/77891d34bf45146a419fdc474d2f339c.png)
 
### 3. View results in GCP Pub/Sub console

Go back to the GCP Pub/Sub console and go to the Subscriptions page. Select the messages, then GCP Pub/Sub will pull the results for you.

![View results in GCP Pub/Sub console](https://assets.emqx.com/images/7353a07efa350e3717ef99f820c6e352.png)
 

## Summary

So far, we have used EMQX Cloud data integration based on the public cloud to bridge the entire process of data to the GCP Pub/Sub.

Most GCP IoT Core users have built IoT applications with the data services provided by GCP. Although GCP IoT Core is about to shut down its business, you can still get your business ongoing without any changes after migrating your hosting service to EMQX Cloud and bridging the data to GCP Pub/Sub by data integration feature.

Enjoy your migration and new IoT journey with EMQX Cloud!



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>


## Other articles in this series

- [Migrate Your Business from GCP IoT Core 01 | Create Deployment and Connect Devices](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-01)
- [Migrate Your Business from GCP IoT Core 02 | Enable TLS/SSL over MQTT to Secure Your Connection](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-02)
- [Migrate Your Business from GCP IoT Core 03｜Use JSON Web Token (JWT) to Verify Device Credentials](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-03)
- [Migrate Your Business from GCP IoT Core 04 | VPC Network Peering and Transfer Data to GCP](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-04)
