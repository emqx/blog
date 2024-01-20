## Introduction

The fully managed serverless MQTT service EMQX Cloud Serverless has now supported data integration capability.

In this blog, we will demonstrate a complete data integration workflow through the example of connecting simulated devices to a Serverless deployment and sending data to Kafka.

## Step 1: Set up a Kafka Cluster

We recommend using fully managed Kafka services such as [Confluent](https://www.confluent.io/) or [Upstash](https://upstash.com/). You can obtain a fully managed and secure Kafka application within minutes. In this tutorial, we will showcase the setup of a Confluent Cloud cluster.

### 1. Create a Confluent Cloud cluster

Once you have completed the sign-up process, proceed to create your first Confluent Cloud cluster. Select the plan that best suits your needs and follow the step-by-step instructions provided by Confluent Cloud. For this example, the default settings should suffice.

![Create a Confluent Cloud cluster](https://assets.emqx.com/images/2ee856e583d23eb5ef56d90a8648f2c8.png)

### 2. Generate an API Key

After creating your first Confluent Cloud cluster, navigate to the API Keys section within the cluster overview and select ‘Create Key’. Generate an API key with global access and store the generated key in a safe place. This API key is crucial for authenticating your EMQX Cloud deployment with your Confluent Cloud cluster, enabling seamless data integration between the two.

![Generate an API Key](https://assets.emqx.com/images/f6e43e04444def2a7fe5c577031cd5c6.png)

### 3. Define a Topic

We then need to create a topic where we want to store all the data produced by our MQTT devices. In the navigation menu, select ‘Topics’ and then create a topic using the default settings. For this tutorial, we named the topic `emqx`*.* It’s not necessary to create a schema for this example.

![Define a Topic](https://assets.emqx.com/images/ef1e7c9aba290dfd59fab397983dcab4.png)

After creating your topic, navigate to the ‘Messages’ tab to monitor any incoming messages. Ensure that the browser tab remains open so that you can check for new messages at a later time.

![Navigate to the ‘Messages’ tab](https://assets.emqx.com/images/96833c97435217df5bf4d62f6f9f6e78.png)

Your Confluent Cloud cluster is now set up and ready for data ingestion.

## Step 2: Set up an EMQX Cloud Serverless Deployment

Register for an account to access EMQX Cloud Console. No credit card is required. 

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

### 1. Create a Serverless Deployment

Log in to the Console and click the ‘New Deployment’ button to begin creating a new deployment. Select the ‘Serverless’ plan to deploy in the region close to your service.

![Create a Serverless Deployment](https://assets.emqx.com/images/32f77b8efbcad37d22d2b089d358475a.png)

Set the 'Spend Limit' to 0, which means we can have [a MQTT Serverless deployment for free](https://www.emqx.com/en/blog/how-to-get-a-forever-free-serverless-mqtt-service). Then, click 'Deploy' to initiate the serverless deployment.

![Click 'Deploy' to initiate the serverless deployment](https://assets.emqx.com/images/f586629c8883bcdad13cdf0ecc7531a1.png)

### 2. Add a Credential for the MQTT Connection

In the Console, navigate to ‘Authentication & ACL’ from the left menu, and then click *Authentication* in the submenu. Click the ‘Add’ button on the right and provide a username and password for the MQTT connection. For this example, we will use "emqx" as the username and "public" as the password for the MQTT client connection.

![Add a Credential for the MQTT Connection](https://assets.emqx.com/images/35aed7768623434a758dcce34eea25bf.png)

With these steps, your MQTT Serverless is now operational and ready for use.

## Step 3: Set up Data Integration with Confluent Cloud

### 1. Create a Kafka connector

Go to the Data Integrations page and select ‘Kafka’.

![Create a Kafka connector](https://assets.emqx.com/images/70951c8d460c6542da51db80fcf58ef1.png)

On the settings page, enter the required information in the ‘Bootstrap Server’. Input the key and secret generated in the ‘Create API Key’ step into the ‘Username’ and ‘Password’ fields. Click ‘Test’ to verify the connection to the Confluent server.

![New Connector](https://assets.emqx.com/images/92b8c8e721e3925aa6f1ddab63da6cad.png)

After passing the test, click the ‘New’ button. A confirmation message will appear indicating that the connector has been successfully created. Under ‘Connectors’, you will see the newly created Kafka connector.

![Connectors](https://assets.emqx.com/images/3b5f35532c32b0bdbce05460d553d1e7.png)

 

### 2. Create a Rule

Create a new rule by entering the following SQL statement in the SQL input field. This rule will process messages from the `temp_hum/emqx` topic, enriching the JSON object with ‘clientid’, ‘topic’, and ‘timestamp’ information.

- `timestamp`: the time when the message is reported
- `clientid`: the ID of the client that publishes the message
- `temp`: the temperature data in the message payload
- `Hum`: the humidity data in the message payload

```
SELECT 
   timestamp,
   clientid, 
   payload.temp as temp, 
   payload.hum as hum
FROM
   "temp_hum/emqx"
```

![New rule](https://assets.emqx.com/images/40f11cc5440514148c052ede5bdbdac5.png)

Test the SQL rule by entering the test payload, topic, and client information, then click ‘Test’. The results displayed in the output will indicate whether the SQL test was successful.

![Data source](https://assets.emqx.com/images/27cc47678bca28a3cc3d43ddf6123271.png)

### 3. Add an Action

Click ‘Next’ to add an action to the rule. Utilize the Kafka topic created in Step 1 along with the message template provided.

```
# kafka topic
emqx
   
# message value
{"temp": ${temp}, "hum": ${hum}}
```

![Add an Action](https://assets.emqx.com/images/b3581e9129bc08ff355476e80a88acab.png)

With these steps, you have successfully integrated Confluent Cloud. The temperature data transmitted to EMQX Cloud should now be consistently relayed to the Confluent Cloud topic.

Let’s proceed to the final step to ensure everything is working as expected.

## Step 4: Verification

To publish messages, you can use any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) or [SDK](https://www.emqx.com/en/mqtt-client-sdk). In this tutorial, we’ll utilize [MQTTX](https://mqttx.app/), a comprehensive MQTT client tool offered by EMQ.

### 1. Connect MQTTX

In MQTTX, click ‘New Connection’ and complete the connection form:

- **Name**: Enter a connection name of your choice.
- **Host**: This is the MQTT broker connection address, available on the EMQX Cloud overview page.
- **Port**: The MQTT broker connection port, also found on the Serverless deployment overview page.
- **Username/Password**: Use the username and password specified in the Authentication settings.

![Connect MQTTX](https://assets.emqx.com/images/12f3d32301e6e27fc8501d6091fb9f66.png)

### 2. Publish MQTT Messages to EMQX Cloud

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

![MQTTX](https://assets.emqx.com/images/c1828d0a965936b6f476479962ee2d6d.png)

### 3. Check Rule Status in EMQX Cloud

The data sent to EMQX Cloud should be automatically processed by the rule engine and transferred to Confluent Cloud, which can be verified in the Data Integration dashboard.

![Check Rule Status in EMQX Cloud](https://assets.emqx.com/images/8e2165d8e245ddb6c69084a66c0f70d5.png)

### 4. Check the Data in Confluent Topic

Examine the data within the Confluent Console.

![Confluent Console](https://assets.emqx.com/images/bfd2092ee17e0f5b64b12b796c6467d3.png)

## Conclusion

Data integration is a powerful tool that enables developers to collect, transmit and process data with ease. This tool unlocks valuable insights and propels digital transformation initiatives forward. With this feature, EMQX Cloud Serverless is one step closer to establishing a comprehensive ecosystem for managing and leveraging IoT data.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
