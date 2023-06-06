## Introduction

The need for efficient and scalable database solutions has become paramount in a world where data is growing unprecedentedly. [Timescale](https://timescale.com/), a well-known player in the time-series database industry, has recently made a significant announcement, transforming itself into a cloud company with a robust database product. 

This blog will explore how [EMQX Cloud](https://www.emqx.com/en/cloud), a leading MQTT cloud service, integrates seamlessly with the new Timescale service, providing a powerful and comprehensive solution for managing time series data.

## Timescale Cloud: A Shift in Focus 

Timescale has been recognized for its database expertise, particularly with its open-source PostgreSQL extension, TimescaleDB. However, with their recent transformation, Timescale has emerged as a cloud company, placing their cloud product, formerly known as Timescale, at the forefront of their offering. By embracing the cloud-first approach, Timescale aims to empower businesses with a scalable, reliable, and flexible infrastructure for managing their data.

![Timescale Cloud](https://assets.emqx.com/images/1b015a07295112f8886c1a7df0034639.png)

## EMQX Cloud: Seamless Integration for Timescale

[EMQX Cloud](https://www.emqx.com/en/cloud), on the other hand, is a reputable MQTT cloud service that specializes in handling large-scale, real-time data streams. EMQX Cloud provides a one-stop O&M colocation and a unique isolated environment for MQTT services. In the era of the Internet of Everything, EMQX Cloud can help you quickly build industry applications and easily realize the collection, transmission, computation, and persistence of IoT data.

The integration between EMQX Cloud and the new Timescale service brings together the strengths of both platforms, providing a comprehensive solution for managing time series data. With EMQX Cloud's robust MQTT connectivity and Timescale's scalable, high-performance database capabilities, businesses can unlock the full potential of their time series data.

## Key Benefits of Integrating EMQX Cloud with Timescale

- **Scalability and Performance**: Timescale's architecture enables horizontal scalability, allowing businesses to handle ever-growing data volumes effortlessly. EMQX Cloud complements this by efficiently processing and managing real-time data streams, ensuring optimal performance.
- **Advanced Time Series Capabilities**:  By leveraging this powerful database technology, businesses can perform complex analytics and queries on their time series data. EMQX Cloud seamlessly integrates with TimescaleDB, providing a unified solution for storing and analyzing MQTT data.
- **Simplified Data Management:** Integrating EMQX Cloud and Timescale simplifies data management processes. With EMQX Cloud securely collecting and processing MQTT data, and Timescale storing and organizing this data, businesses can focus on extracting valuable insights rather than worrying about infrastructure management.
- **Enhanced Reliability and Security**: EMQX Cloud and Timescale prioritize reliability and security. EMQX Cloud ensures reliable message delivery, even in challenging network conditions, while Timescale provides robust security measures to protect sensitive time series data. Together, they offer a highly reliable and secure environment for critical IoT applications.

## 5 Steps to Integrate EMQX Cloud with Timescale

Now let's see how to get data from EMQX Cloud to the new Timescale service. 

### Step1: Create a Timescale Service

Login to the Timescale and click go to Create a Service page, select a Region and then click `Create service` button:

![Create a Timescale Service](https://assets.emqx.com/images/68bf60006f981389c4fa017feddb826c.png)

Now, a new Timescale service has been created. You can download the cheatsheet to initiate your Timescale deployment.

![Initiate Your Timescale Deployment](https://assets.emqx.com/images/d27502ca5c186d33123e2a47c6978108.png)

### Step 2: Create an EMQX Deployment

Creating a dedicated MQTT broker on EMQX Cloud is as easy as a few clicks.

#### **Get an EMQX Cloud Account**

Go to [EMQX Cloud](https://www.emqx.com/en/cloud) and click start free to register an account if you are new to EMQX Cloud.

#### **Create an EMQX Cloud Dedicated Professional Deployment**

Once logged in, click on "Cloud Console" under the account menu, and you will see the green button to create a new deployment.

![Create an EMQX Cloud Dedicated Professional Deployment](https://assets.emqx.com/images/33e5fb0aae340147452561ac7ca068f8.png)

Select Dedicated Edition.

![Select Dedicated Edition](https://assets.emqx.com/images/3c9419fe1b78d4c6dff63c91cf272247.png)

Select the 'Profession', choose the 'N.Virginial’ region, and click the 'Create Now' button.

![click the 'Create Now'](https://assets.emqx.com/images/481b9797b75d430b210d96e5ca18931b.png)

In just a few minutes, you will get a fully managed [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison).

![Created successfully](https://assets.emqx.com/images/d5e36f220c2bdbf15a4bdeb09cbfb28d.png)

### Step 3: Setup NAT Gateway for Your EMQX Cloud Deployment

Before setting up the Timescale integration, we need to enable the NAT gateway. By default, the MQTT broker is deployed in a private VPC, which can not send data to third-party systems over the public network. 

There are two ways to resolve this: 

- One is to enable the NAT gateway and allow the broker to send data to Timescale through that gateway. 
- The other is to set up VPC peering, which depends on whether the target cloud service supports VPC peering. 

In this tutorial, we will use the first solution.

Go to the VAS page and scroll down to the bottom, where you will see the [NAT Gateway](https://docs.emqx.com/en/cloud/latest/vas/nat-gateway.html) widget. 

![NAT Gateway](https://assets.emqx.com/images/77ec27d82b15b245800c91b009b0eeff.png)

Click the Subscribe button and follow the instructions to create a NAT Gateway.

![Click the Subscribe button](https://assets.emqx.com/images/842060905f350060f78df7f817e88e0f.png)

When the status of the NAT gateway is running, the deployment can access public network resources.

### Step 4: Setup EMQX Cloud Data Integration with Timescale

EMQX Cloud offers more than 30 native data integrations with popular data systems. Timescale is one of them.

![Timescale Integration](https://assets.emqx.com/images/f5733ab6e995684ca6a26f6397361526.png)

#### **Create Timescale Resource**

Click 'Data Integrations' on the left menu and 'View All Resouces'. You will find the TimescaleDB in the list.

Click the TimescaleDB card to create a new resource, then you will go to the resource configuration page:

![Create Timescale Resource](https://assets.emqx.com/images/9740a16037707e7143f5381496c8c035.png) 

1. Server: this is the address of your Timscale service. Remember, don't forget the port.
2. Database: The database name we created in the previous steps, and the default is 'tsdb'.
3. User: the username for connecting to your Timescale service, and the default is 'tsdbadmin'.
4. Password: the password for the connection, and you can find it in the cheatsheet file.
5. Click the 'Test' button to ensure the database can be connected.

#### **Create A New Rule**

EMQX Cloud provides a powerful rule engine to transform and enrich the raw MQTT message before sending it to third-party systems. You can learn more info about the usage of the rule engine [here](https://docs.emqx.com/en/cloud/latest/rule_engine/rules.html).

During the resource creation, you will see a popup, and clicking 'New' will lead you to the rule creation page. 

![Create A New Rule](https://assets.emqx.com/images/a54859c3267944d06e1d8caf3ce2e603.png)

The SQL defines how to select data from specific MQTT topics and payload : 

```
SELECT
timestamp div 1000 AS up_timestamp, clientid AS client_id, payload.temp AS temp, payload.hum AS hum
FROM
"temp_hum/emqx"
```

And you can also test your SQL to see if anything is incorrect.

Then we create an 'Action' with the following script:

```
INSERT INTO temp_hum(up_timestamp, client_id, temp, hum) VALUES (to_timestamp(${up_timestamp}), ${client_id}, ${temp}, ${hum})
```

This defines how we insert data into the Timescale database;  Now Click on the ""“NEXT""“ button to finish creating the Rule. 

#### **View Rules Details**

![View Rules Details](https://assets.emqx.com/images/5006d91a4ce77c8bbd0f0d0d5c5f7e6d.png)

Now, you can see a rule of Timescale data integration created and defines how to insert data from the MQTT topic `temp_hum/emqx` into your Timescalse database.

### Step5: Verify Your Integration

#### **Simulate an MQTT Client to Connect to EMQX Cloud via MQTTX**

You can use any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) or [SDK](https://www.emqx.com/en/mqtt-client-sdk) to publish the message. In this tutorial, we will use [MQTTX](https://mqttx.app/), a powerful MQTT client application provided by EMQ.

Click 'New Connection' on MQTTX and fill out the connection form:

![Click 'New Connection'](https://assets.emqx.com/images/2fb5cfecd691adbb8f2f57fddecc435e.png)

1. Name: Connection name. Use whatever name you want.
2. Host: the MQTT broker connection address. You can get it from the EMQX Cloud overview page.
3. Port: MQTT broker connection port. You can get it from the EMQX Cloud overview page.
4. Username/Password: The username/password we defined in [EMQX Cloud Authentication](https://docs.emqx.com/en/cloud/latest/deployments/auth_serverless.html#authentication) settings.

#### **Publish MQTT Messages** to EMQX Cloud

1. Set payload format to 'JSON'.

2. Set to topic: `temp_hum/emqx` (the topic we just set in the rule)

3. JSON body:

   ```
   {
        "temp": "45.5",
        "hum": "27.5"
   }
   ```

Click the send button on the right. You can change the temperature value and send more data to the EMQX Cloud.

![Click the send button](https://assets.emqx.com/images/dea02e0058fd9421f591bc56da930f29.png)

#### Check Rule Status in EMQX Cloud

The data sent to EMQX Cloud should be processed by the rule engine and inserted into Timescale automatically, and we can check it from the EMQX Cloud Data Integration dashboard:

![Check Rule Status in EMQX Cloud](https://assets.emqx.com/images/b16927edc0a012d9b1ba17af9b9519a5.png)

#### **Check the Data Persisted in Timescale**

Now it's time to take a look at the data on the Timescale. Ideally, the data you send from MQTTX will go to the EMQX Cloud and persist to the Timescale database with data integration.

You can connect to the SQL console on the Timescale Console or use any client tool to fetch data from your timescale database. 

![Check the Data Persisted in Timescale](https://assets.emqx.com/images/5d90870818c24a58dc2e81e812c5b0b7.png)

Run SQL to query the specific table we defined in the EMQX Cloud data integration rule, and you can see the data has been inserted correctly.

![Run SQL](https://assets.emqx.com/images/9d4aac12445da023431ece42926a38ed.png)

## Conclusion

The integration of EMQX Cloud with the new Timescale service brings together the power of real-time data streams and scalable time series database technology. By seamlessly connecting these two platforms, businesses can efficiently collect, store, and analyze their time series data, unlocking valuable insights and accelerating their digital transformation initiatives. The collaboration between EMQX Cloud and Timescale represents a significant step towards building a comprehensive ecosystem for managing and leveraging time series data in the cloud.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
