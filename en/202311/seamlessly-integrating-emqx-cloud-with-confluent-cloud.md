## Introduction

Confluent Cloud is a managed cloud service offered by Confluent, the company behind Apache Kafka.  This service enables easy deployment, operation, and scaling of Apache Kafka clusters in the cloud. With Confluent Cloud, you can focus on building event-driven applications without worrying about managing the underlying infrastructure. It boasts features such as automatic scaling, data replication, and seamless integration with other components of the Confluent Platform.

Recently, [EMQX Cloud](https://www.emqx.com/en/cloud), a fully managed MQTT cloud service, has announced its integration support for  Confluent Cloud.  Organizations can now harness both EMQX Cloud for MQTT and Confluent Cloud for Kafka, enhancing MQTT communication and Kafka deployments for critical applications. This powerful combination allows for smooth integration between IoT devices that use MQTT and Kafka's stream processing capabilities, thus unlocking the full potential of IoT infrastructure for scalable and future-proof solutions.

In this tutorial, we'll show you step-by-step how to integrate Confluent Cloud with EMQX Cloud in four detailed steps.

<p>
<lite-youtube
  videoid="vJFqhi1AqFc"
/>
</p>

## Step 1: Set up a Confluent Cloud Cluster

To begin using Confluent Cloud, visit [confluent.io/get-started/](http://confluent.io/get-started/) and create an account. Upon signing up, you will receive a $400 credit to use within the first 30 days.

#### 1. Create a Confluent Cloud cluster

Once you have completed the sign-up process, proceed to create your first Confluent Cloud cluster. Select the plan that best suits your needs and follow the step-by-step instructions provided by Confluent Cloud. For this example, the default settings should suffice.

![Create cluster](https://assets.emqx.com/images/2022988a20259487a5d2007904b49f54.png)

#### 2. Generate an API Key

After creating your first Confluent Cloud cluster, navigate to the API Keys section within the cluster overview and select ‘Create Key’. Generate an API key with global access and store the generated key in a safe place. This API key is crucial for authenticating your EMQX Cloud deployment with your Confluent Cloud cluster, enabling seamless data integration between the two.

![Generate an API Key](https://assets.emqx.com/images/c89d93bd8055d64e03ab09764d2798d4.png)

#### 3. Define a Topic

We then need to create a topic where we want to store all the data produced by our MQTT devices. In the navigation menu, select ‘Topics’ and then create a topic using the default settings. For this tutorial, we named the topic `emqx`*.* It’s not necessary to create a schema for this example.

![Create topic](https://assets.emqx.com/images/a97ef568263a44d94ff082ee8d895a1c.png)

After creating your topic, navigate to the ‘Messages’ tab to monitor any incoming messages. Ensure that the browser tab remains open so that you can check for new messages at a later time.

![‘Messages’ tab](https://assets.emqx.com/images/40d0bf2dc6834980cc486a773328376b.png)

Your Confluent Cloud cluster is now set up and ready for data ingestion.

## Step 2: Set up an EMQX Cloud Deployment

[Register for an EMQX account](https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new) to access a 14-day free trial of a Dedicated deployment. No credit card is required. 

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

#### 1. Create a Dedicated Deployment

Log in to the Cloud Console and click the ‘New Deployment’ button to begin creating a new deployment. Select the ‘Dedicated’ plan to deploy a ‘Professional’ deployment.

![New Deployment](https://assets.emqx.com/images/8a8ec4e6256d77a36595d14ad53cda8c.png)

For this tutorial, select ‘Professional’, choose the *N.Virginia* region with a specification for 1,000 sessions, and then click the 'Deploy' button.

![Select Professional](https://assets.emqx.com/images/a0d871a3e97156f7bab9608b13cdfc92.png)

#### 2. Add a Credential for the MQTT Connection

In the Cloud Console, navigate to ‘Authentication & ACL’ from the left menu, and then click *Authentication* in the submenu. Click the ‘Add’ button on the right and provide a username and password for the MQTT connection. For this example, we will use "emqx" as the username and "public" as the password for the MQTT client connection.

![Add Authentication](https://assets.emqx.com/images/29a3a366afa8218b79876cb94393bed3.png)

#### 3. Enable NAT Gateway

Before setting up data integration, we need to enable the NAT gateway. By default, the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) is deployed in a VPC, which cannot send data to other services over the public network.

There are two methods to enable external data transfer:

- **Enable the NAT** **Gateway**: this allows the broker to send data through the gateway.
- **Set Up VPC Peering:** This method is contingent on whether the target cloud service supports VPC peering.

In this tutorial, we will opt for the first method. On the deployment overview page, navigate to the ‘NAT Gateway’ tab located at the bottom and enable the NAT Gateway service by clicking ‘Subscribe Now’.

![NAT Gateway](https://assets.emqx.com/images/ec8f7c42f23e98f30a8514989f5c3b14.png)

With these steps, your MQTT broker is now operational and ready for use. Let’s now proceed to Step 3.

## Step 3: Set up EMQX Cloud Data Integration with Confluent Cloud

EMQX Cloud provides over 40 native data integrations. Previously, Kafka resources were used to connect data to Confluent. Our new customized integration makes connecting to Confluent more streamlined.

#### 1. Create a Confluent Resource

Go to the Data Integrations page and select ‘Confluent’.

![Data Integrations page](https://assets.emqx.com/images/267d948ba05083ebdbbbc996a35f497b.png)

On the Confluent cluster settings page enter the required information in the ‘Endpoints’ section for the ‘Bootstrap Server’. Input the key and secret generated in the ‘Create API Key’ step into the ‘Key’ and ‘Secret’ fields. Click ‘Test’ to verify the connection to the Confluent server.

![New resource page](https://assets.emqx.com/images/653be2fbec84060087df25b444dcfa6e.png)

After passing the test, click the ‘New’ button. A confirmation message will appear indicating that the resource has been successfully created. Under ‘Configured Resources’, you will see the newly created Confluent resource.

#### 2. Create a Rule

Create a new rule by entering the following SQL statement in the SQL input field. This rule will process messages from the `temp_hum/emqx` topic, enriching the JSON object with ‘client_id’, ‘topic’, and ‘timestamp’ information.

- `up_timestamp`: the time when the message is reported
- `client_id`: the ID of the client that publishes the message
- `temp`: the temperature data in the message payload
- `Hum`: the humidity data in the message payload

```
SELECT 
  timestamp as up_timestamp, 
  clientid as client_id,
  payload.temp as temp,
  payload.hum as hum
FROM
  "temp_hum/emqx"
```

![New rule](https://assets.emqx.com/images/6d1859c5d300d58fda5663c8bb6fe9ff.png)

Test the SQL rule by entering the test payload, topic, and client information, then click ‘SQL Test’. The results displayed below will indicate whether the SQL test was successful.

![SQL rule](https://assets.emqx.com/images/f8604a5630b2dd68890feb51bb4afb78.png)

#### 3. Add an Action

Click ‘Next’ to add an action to the rule. Utilize the Kafka topic created in Step 1 along with the message template provided.

```
# kafka topic
emqx
   
# kafka message template 
{"up_timestamp": ${up_timestamp}, "client_id": ${client_id}, "temp": ${temp}, "hum": ${hum}}
```

![Add an action](https://assets.emqx.com/images/57625eb9482a94692b3c95aa512603b6.png)

With these steps, you have successfully integrated Confluent Cloud and EMQX Cloud. The temperature data transmitted to EMQX Cloud should now be consistently relayed to the Confluent Cloud topic.

Let’s proceed to the final step to ensure everything is working as expected.

## Step 4: Verify with MQTTX

To publish messages, you can use any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) or [SDK](https://www.emqx.com/en/mqtt-client-sdk). In this tutorial, we’ll utilize [MQTTX](https://mqttx.app/), a comprehensive MQTT client tool offered by EMQ.

#### 1. Connect MQTTX

In MQTTX, click ‘New Connection’ and complete the connection form:

- **Name**: Enter a connection name of your choice.
- **Host**: This is the MQTT broker connection address, available on the EMQX Cloud overview page.
- **Port**: The MQTT broker connection port, also found on the EMQX Cloud overview page.
- **Username/Password**: Use the username and password specified in the EMQX Cloud Authentication settings.

![MQTTX](https://assets.emqx.com/images/0eb0d772f3aaea996b0e40df4690bf2b.png)

#### 2. Publish MQTT Messages to EMQX Cloud

- Set the payload format to 'JSON'.
- Use `temp_hum/emqx` as the topic (the one set in the rule).
- JSON body:

```
{
     "temp": 19,
     "hum": 106
}
```

Click the ‘Send’ button on the right. You can change the temperature value and send additional data to EMQX Cloud.

![Publish MQTT Messages to EMQX Cloud](https://assets.emqx.com/images/7feb8be7f5d7268376cac3f3558b1482.png)

#### 3. Check Rule Status in EMQX Cloud

The data sent to EMQX Cloud should be automatically processed by the rule engine and transferred to Confluent Cloud, which can be verified in the EMQX Cloud Data Integration dashboard.

![Check Rule Status in EMQX Cloud](https://assets.emqx.com/images/aa39d8464000c47e36e660fc6d911d72.png)

#### 4. Check the Data in Confluent Topic

Examine the data within the Confluent Console.

![Check the Data in Confluent Topic](https://assets.emqx.com/images/a46d01a747b34d8d9356f5932ca2e37d.png)

## Conclusion

The integration of EMQX Cloud with Confluent’s new service unites the capabilities of real-time data and event streaming technology. This seamless connection between the two platforms allows businesses to efficiently collect, forward, and process data, unlocking valuable insights and propelling digital transformation initiatives forward. The partnership between EMQX Cloud and Confluent marks a significant step towards building a comprehensive ecosystem for managing and leveraging IoT data in the cloud.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
