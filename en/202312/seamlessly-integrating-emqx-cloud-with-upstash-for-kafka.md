## Introduction

Upstash is a cloud-based, serverless data platform that empowers developers to seamlessly integrate Redis databases and Kafka into their applications without the hassle of managing infrastructure. Offering a serverless architecture, Upstash allows users to enjoy the benefits of Redis, a high-performance, in-memory data store, and Kafka, without dealing with the complexities of deployment, scaling, or maintenance.

Recently, EMQX Cloud, a fully managed MQTT cloud service, has announced its integration support for  Upstash.  Organizations can now harness both EMQX Cloud for MQTT and Upstash for Kafka, enhancing MQTT communication and Kafka deployments for critical applications. This powerful combination allows for smooth integration between IoT devices that use MQTT and Kafka's stream processing capabilities, thus unlocking the full potential of IoT infrastructure for scalable and future-proof solutions.

In this tutorial, we'll show you step-by-step how to integrate Upstash with EMQX Cloud in four detailed steps.

## Step 1: Set up an Upstash for the Kafka Cluster

To begin using Upstash, visit [Upstash: Serverless Data for Redis® and Kafka®](https://upstash.com/)  and create an account. 

#### 1. Create a Kafka Cluster

Once you have completed the sign-up process, proceed to create your first Upstash for Kafka cluster. Select the type that best suits your needs and follow the step-by-step instructions provided by Upstash. For this example, ‘Single Replica’ should suffice.

![Create a Kafka Cluster](https://assets.emqx.com/images/96c89aea08dc6d8b40daed59143ae366.png)

#### 2. Define a Topic

We then need to create a topic where we want to store all the data produced by our MQTT devices. In the cluster console, select ‘Topics’ and then create a topic using the default settings. For this tutorial, we named the topic `emqx`*.*

![Define a Topic](https://assets.emqx.com/images/d888a60cbd8b31bee58a07a8884eb0b9.png)

#### 3. Generate Credentials

After creating the topic, navigate to the cluster overview and select ‘Credentials’. Generate a pair of username and password. This credential is crucial for authenticating your EMQX Cloud deployment with your Upstash cluster, enabling seamless data integration between the two.

![Generate Credentials](https://assets.emqx.com/images/56f3177735e38f2d952dc601c7fee2d9.png)

Your Upstash for Kafka cluster is now set up and ready for data ingestion.

## Step 2: Set up an EMQX Cloud Deployment

Register for an EMQX account to access a 14-day free trial of a Dedicated deployment. No credit card is required. 

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

#### 1. Create a Dedicated Deployment

Log in to the Cloud Console and click the ‘New Deployment’ button to begin creating a new deployment. Select the ‘Dedicated’ plan to deploy a ‘Professional’ deployment.

![New Deployment](https://assets.emqx.com/images/f0616f2287da8d9360665f8cfbfa2b65.png)

For this tutorial, select ‘Professional’, choose the *N.Virginia* region with a specification for 1,000 sessions, and then click the 'Deploy' button.

![Select ‘Professional’](https://assets.emqx.com/images/bdc50ccead24fd4a4304cc614fd69bf8.png)

#### 2. Add a Credential for the MQTT Connection

In the Cloud Console, navigate to ‘Authentication & ACL’ from the left menu, and then click *Authentication* in the submenu. Click the ‘Add’ button on the right and provide a username and password for the MQTT connection. For this example, we will use "emqx" as the username and "public" as the password for the MQTT client connection.

![Add a Credential for the MQTT Connection](https://assets.emqx.com/images/ce2a390987c504d6e99879d7112a112b.png)

#### 3. Enable NAT Gateway

Before setting up data integration, we need to enable the NAT gateway. By default, the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) is deployed in a VPC, which cannot send data to other services over the public network.

There are two methods to enable external data transfer:

- **Enable the NAT** **Gateway**: this allows the broker to send data through the gateway.
- **Set Up VPC Peering:** This method is contingent on whether the target cloud service supports VPC peering.

In this tutorial, we will opt for the first method. On the deployment overview page, navigate to the ‘NAT Gateway’ tab located at the bottom and enable the NAT Gateway service by clicking ‘Subscribe Now’.

![Enable NAT Gateway](https://assets.emqx.com/images/bf6f87ac1b03f61f984d484eebf79fba.png)

With these steps, your MQTT broker is now operational and ready for use. Let’s now proceed to Step 3.

## Step 3: Set up EMQX Cloud Data Integration with Upstash for Kafka

EMQX Cloud provides over 40 native data integrations. Previously, Kafka resources were used to connect data to Kafka-type resource. Our new customized integration makes connecting to Upstash more streamlined.

#### 1. Create a Upstash for Kafka Resource

Go to the Data Integrations page and select ‘Upstash for Kakfa’.

![Create a Upstash for Kafka Resource](https://assets.emqx.com/images/aef9990a638303b4877c8da03590d3d4.png)

On the settings page, enter the required information in the ‘Endpoints’ section for the ‘Kafka Server’. Input the Username and password generated in the ‘Generate Credentials’ step into the ‘Username’ and ‘Password’ fields. Click ‘Test’ to verify the connection to the Upstash server.

![New Resource](https://assets.emqx.com/images/f360f176a9b05f0ded385899bd75839c.png)

After passing the test, click the ‘New’ button. A confirmation message will appear indicating that the resource has been successfully created. Under ‘Configured Resources’, you will see the newly created Kafka resource.

#### 2. Create a Rule

Create a new rule by entering the following SQL statement in the SQL input field. This rule will process messages from the `temp_hum/emqx` topic, enriching the JSON object with ‘client_id’, ‘topic’, and ‘timestamp’ information.

- `up_timestamp`: the time when the message is reported
- `client_id`: the ID of the client that publishes the message
- `temp`: the temperature data in the message payload
- `hum`: the humidity data in the message payload

```
SELECT 
  timestamp as up_timestamp, 
  clientid as client_id,
  payload.temp as temp,
  payload.hum as hum
FROM
  "temp_hum/emqx"
```

![New Rule](https://assets.emqx.com/images/7e2484d487470a519bb59c10c9add175.png)

Test the SQL rule by entering the test payload, topic, and client information, then click ‘SQL Test’. The results displayed below will indicate whether the SQL test was successful.

![SQL Test](https://assets.emqx.com/images/a255261f3b6c60a23d443084d1cdc5a9.png)

#### 3. Add an Action

Click ‘Next’ to add an action to the rule. Utilize the Kafka topic created in Step 1 along with the message template provided.

```
# kafka topic
emqx
   
# kafka message template 
{"up_timestamp": ${up_timestamp}, "client_id": ${client_id}, "temp": ${temp}, "hum": ${hum}}
```

![Add an Action](https://assets.emqx.com/images/43d9e4401904d0ef69fbf68c0c76c43e.png)

With these steps, you have successfully integrated Upstash and EMQX Cloud. The temperature data transmitted to EMQX Cloud should now be consistently relayed to the kafka topic.

Let’s proceed to the final step to ensure everything is working as expected.

## Step 4: Verify with MQTTX

To publish messages, you can use any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) or [SDK](https://www.emqx.com/en/mqtt-client-sdk). In this tutorial, we’ll utilize [MQTTX](https://mqttx.app/), a comprehensive MQTT client tool offered by EMQ.

#### 1. Connect MQTTX

In MQTTX, click ‘New Connection’ and complete the connection form:

- **Name**: Enter a connection name of your choice.
- **Host**: This is the MQTT broker connection address, available on the EMQX Cloud overview page.
- **Port**: The MQTT broker connection port, also found on the EMQX Cloud overview page.
- **Username/Password**: Use the username and password specified in the EMQX Cloud Authentication settings.

![Connect MQTTX](https://assets.emqx.com/images/511347017f355731359dff07e90a65d1.png)

#### 2. Publish MQTT Messages to EMQX Cloud

- Set the payload format to 'JSON'.
- Use `temp_hum/emqx` as the topic (the one set in the rule).
- JSON body:

```
{
     "temp": 39.5,
     "hum": 46
}
```

Click the ‘Send’ button on the right. You can change the temperature value and send additional data to EMQX Cloud.

![MQTTX](https://assets.emqx.com/images/1df7081dcdcb21f6b756896818bfa3be.png)

#### 3. Check Rule Status in EMQX Cloud

The data sent to EMQX Cloud should be automatically processed by the rule engine and transferred to Upstash, which can be verified in the EMQX Cloud Data Integration dashboard.

![Check Rule Status in EMQX Cloud](https://assets.emqx.com/images/3133a30688d810aab78b48dcb0ac556d.png)

#### 4. Check the Data in Upstash Topic

Examine the data within the Upstash Console. In Topic, we select ‘emqx', click 'Messages’, then we can check the messages.

![Check the Data in Upstash Topic](https://assets.emqx.com/images/853301bfa0d9cb488e6063e863a70ccf.png)

## Conclusion

The integration of EMQX Cloud with Upstash’s new service unites the capabilities of real-time data and event streaming technology. This seamless connection between the two platforms allows businesses to efficiently collect, forward, and process data, unlocking valuable insights and propelling digital transformation initiatives forward. The partnership between EMQX Cloud and Upstash marks a significant step towards building a comprehensive ecosystem for managing and leveraging IoT data in the cloud.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
