## Introduction

Upstash is a cloud-based, serverless data platform that empowers developers to seamlessly integrate Redis databases and Kafka into their applications without the hassle of managing infrastructure. Offering a serverless architecture, Upstash allows users to enjoy the benefits of Redis, a high-performance, in-memory data store, and Kafka, without dealing with the complexities of deployment, scaling, or maintenance.

Recently, EMQX Cloud, a fully managed MQTT cloud service, has announced its integration support for  Upstash, a serverless Redis that can be used as a database, cache, and message broker.  This powerful combination allows for smooth integration between IoT devices that use MQTT and Redis for fast data access and processing, thus unlocking the full potential of IoT infrastructure for scalable and future-proof solutions.

In this tutorial, we'll show you step-by-step how to integrate Upstash with EMQX Cloud in four detailed steps.

## Step 1: Set up an Upstash for Redis

To begin using Upstash, visit [Upstash: Serverless Data for Redis® and Kafka®](https://upstash.com/)  and create an account. 

#### 1. Create a Serverless Redis Database

Once you have completed the sign-up process, proceed to create your first Upstash for Redis database. Select the region in which you would like your database to be deployed. To optimize performance, it is recommended to choose the region that is closest to your EMQX Cloud deployment region.

![Create Database](https://assets.emqx.com/images/83f29971b4b32f4da2ab7cb65931b7a9.png)

#### 2. View the Details for the Connection

We then enter the Redis console. The details page shows the endpoint, password, and port for connection.

![Redis console](https://assets.emqx.com/images/90f6ef77e5229f92b760f715b1837713.png)

Your serverless Redis Database is now set up and ready for data ingestion.

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

![New Deployment](https://assets.emqx.com/images/43639454e464670fa3694e1700921254.png)

For this tutorial, select ‘Professional’, choose the *N.Virginia* region with a specification for 1,000 sessions, and then click the 'Deploy' button.

![select ‘Professional’](https://assets.emqx.com/images/e4c0f2f84bf717d3ece8678129ac22d3.png)

#### 2. Add a Credential for the MQTT Connection

In the Cloud Console, navigate to ‘Authentication & ACL’ from the left menu, and then click *Authentication* in the submenu. Click the ‘Add’ button on the right and provide a username and password for the MQTT connection. For this example, we will use "emqx" as the username and "public" as the password for the MQTT client connection.

![Authentication & ACL](https://assets.emqx.com/images/e26921d52aa0651c38ff71b7a37dee05.png)

#### 3. Enable NAT Gateway

Before setting up data integration, we need to enable the NAT gateway. By default, the MQTT broker is deployed in a VPC, which cannot send data to other services over the public network.

There are two methods to enable external data transfer:

- **Enable the NAT** **Gateway**: this allows the broker to send data through the gateway.
- **Set up VPC Peering:** This method is contingent on whether the target cloud service supports VPC peering.

In this tutorial, we will opt for the first method. On the deployment overview page, navigate to the ‘NAT Gateway’ tab located at the bottom and enable the NAT Gateway service by clicking ‘Subscribe Now’.

![Enable NAT Gateway](https://assets.emqx.com/images/f54586d136b2c417b071d29b8cb2dd82.png)

With these steps, your MQTT broker is now operational and ready for use. Let’s now proceed to Step 3.

## Step 3: Set up EMQX Cloud Data Integration with Upstash for Redis

EMQX Cloud provides over 40 native data integrations. Previously, Redis resources were used to connect data to Redis-type resources. Our new customized integration makes connecting to Upstash more streamlined.

#### 1. Create a Upstash for Redis Resource

Go to the Data Integrations page and select ‘Upstash for Redis’.

![Upstash for Redis](https://assets.emqx.com/images/83d83bc6f827b25a90b57b17adc83a47.png)

On the settings page, enter the required information in the ‘Endpoints’ section for the ‘Redis Server’. Input the password generated into the ‘Password’ fields. Click ‘Test’ to verify the connection to the Upstash server.

![New Resource](https://assets.emqx.com/images/f6bc2d756f7cefa262d1f5543d0208c5.png) 

After passing the test, click the ‘New’ button. A confirmation message will appear indicating that the resource has been successfully created. Under ‘Configured Resources’, you will see the newly created Redis resource.

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

![New Rule](https://assets.emqx.com/images/8677c334fe03154ddb11314e397f268a.png)

Test the SQL rule by entering the test payload, topic, and client information, then click ‘SQL Test’. The results displayed below will indicate whether the SQL test was successful.

![Create a Rule](https://assets.emqx.com/images/c7ab0eb9081deb0f7046c46779206c32.png)

#### 3. Add an Action

Click ‘Next’ to add an action to the rule. We read the up_timestamp, client ID, temperature and humidity from the topic and save it to Redis. Click ‘Confirm’.

```
HMSET ${client_id} ${up_timestamp} ${temp}
```

![Edit Action](https://assets.emqx.com/images/c38584953180d2358e8c6e9024377514.png)

With these steps, you have successfully integrated Upstash and EMQX Cloud. The temperature data transmitted to EMQX Cloud should now be consistently relayed to the Redis database.

Let’s proceed to the final step to ensure everything is working as expected.

## Step 4: Verify with MQTTX

To publish messages, you can use any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) or [SDK](https://www.emqx.com/en/mqtt-client-sdk). In this tutorial, we’ll utilize [MQTTX](https://mqttx.app/), a comprehensive MQTT client tool offered by EMQ.

#### 1. Connect MQTTX

In MQTTX, click ‘New Connection’ and complete the connection form:

- **Name**: Enter a connection name of your choice.
- **Host**: This is the MQTT broker connection address, available on the EMQX Cloud overview page.
- **Port**: The MQTT broker connection port, also found on the EMQX Cloud overview page.
- **Username/Password**: Use the username and password specified in the EMQX Cloud Authentication settings.

![Connect MQTTX](https://assets.emqx.com/images/6a04049ab66783bd78e219b1ce56b54e.png)

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

![Publish MQTT Messages to EMQX Cloud](https://assets.emqx.com/images/aa3a3e4d3e1040b911ea14443aed3b56.png)

#### 3. Check Rule Status in EMQX Cloud

The data sent to EMQX Cloud should be automatically processed by the rule engine and transferred to Upstash, which can be verified in the EMQX Cloud Data Integration dashboard.

![Check Rule Status in EMQX Cloud](https://assets.emqx.com/images/63be90e0dac7250ae05132a97de1d400.png)

#### 4. Check the Data in Upstash Data Browser

Examine the data within the Upstash Console. In Data Browser, we select the client entry; then we can check the messages.

![Upstash Console](https://assets.emqx.com/images/f54438cb64eacd75f3238d7dcf7cb6d7.png)

## Conclusion

The integration of EMQX Cloud with Upstash’s new service unites the serverless high-performance, in-memory data store technology. This seamless connection between the two platforms allows businesses to efficiently collect, forward, and process data, unlocking valuable insights and propelling digital transformation initiatives forward. The partnership between EMQX Cloud and Upstash marks a significant step towards building a comprehensive ecosystem for managing and leveraging IoT data in the cloud.





<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
