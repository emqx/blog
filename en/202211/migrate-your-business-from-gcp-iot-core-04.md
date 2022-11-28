As you have set up the connection to [EMQX Cloud](https://www.emqx.com/en/cloud) under the guide in our previous articles, it's time to send the data back to the services in GCP(If you are using databases or data analytics in GCP). This tutorial will demonstrate the VPC Network Peering between EMQX Cloud and GCP to help you with data transmission.


## VPC Peering Setup

Log in to EMQX Cloud console, go to the deployment overview, click the + VPC Peering Connection, fill in the information and keep the information for further use:

- VPC Network Name of deployment
- Project ID of EMQX Cloud
- CIDR of deployment

![VPC Peering Setup](https://assets.emqx.com/images/3382a423a09d17e7f3ff9d9b3113ab12.png)

The Project ID and VPC Network Name can be found in your GCP Control Panel - **VPC network peering**.

Log in to your GCP console, create the peering connection.

1. In the Google Cloud Console, click **VPC network peering**.
2. Click CREATE PEERING CONNECTION, and click Continue.
3. In Name, enter a name for your peering connection.
4. In Your VPC Network, enter the name of your GCP VPC network.
5. In Peered VPC network, select **In another project**.
6. In **Project ID**, enter EMQX Cloud Project ID. You can find this name in the VPC Peering view in EMQX Cloud.
7. In **VPC network name**, enter your EMQX Cloud VPC Network Name. You can find this name in the VPC Peering view in EMQX Cloud.
8. Click CREATE. 

![create the peering connection](https://assets.emqx.com/images/e466b3214e8569a4962bd3b9c6785ac8.png)

Fill the following information in the VPC Network Peering into the EMQX Cloud VPC configration panel.

![Fill the following information](https://assets.emqx.com/images/b2894cfff81d009a5f809be5a1d23dc6.png)

- **Project ID**: GCP Project ID of your peering VPC
- **VPC Network Name**: Your VPC network

![Fill the following information](https://assets.emqx.com/images/78fed5dfc319eb459bc38c9143442aea.png)

You will see the status of peering connection is **Active** if everything goes well. 

![peering connection is **Active**](https://assets.emqx.com/images/be9443bc16916f503da6a8f7d5f6203b.png)

and you will see the status of VPC Peering on EMQX Cloud is **running**. 

![EMQX Cloud is running](https://assets.emqx.com/images/3309320688c6a6d5d848106ce5cf6e03.png)

Create Firewall to allow your EMQX Cloud deployment to access your GCP network.

1. Click **Firewall**, and Click **CREATE FIREWALL RULE.**
2. In **Network**, select your GCP network.
3. In **Targets**, select All instances in the network, or you can select other option according to your situation.
4. In **Source IP ranges**, fill in the CIDR of EMQX Cloud VPC in step 1.
5. Seletc your **Protocols** and **ports**.

![Create Firewall](https://assets.emqx.com/images/136dd42e21396d76692994c41e2ccbcc.png)

 
## Data Integration

I will create a VM instance in GCP console and use Docker to install Redis for data storage.

### 1. Redis Configuration

Start a Redis container on the server with the following command.

```
docker run -itd --name redis -p 6379:6379 redis:latest
docker exec -it redis redis-cli  
```

Once Redis is ready, it's time to start the configuration of the EMQX Cloud data integration!

![docker exec redis](https://assets.emqx.com/images/2483a85a43a3a724c87daedce488f800.png)

### 2. Save device data to Redis

Enter Data Integration, and choose the Redis Single Mode card.

![choose the Redis Single Mode card](https://assets.emqx.com/images/f425acb30f96db2f3aa06fd74d9a18f2.png)

**Create Redis Single Mode Resource**

In the Create Resource page, set Redis Server (IP address and port of the server) as follows:

![set Redis Server](https://assets.emqx.com/images/62de0aa6cda78d7803dbce5bf56433bd.png)

Click Test button when the configuration is complete, then click New button to create a resource when it is available. If it's shown that init resource failed, you need to check your **VPC peering** and **Firewall** configuration. You can view more on the log details page.

**Create Rule**

After the resource is available, click New to enter the create rule page.

Our goal is to trigger the engine when the client sends a temperature and humidity message to the **temp_hum/emqx** topic. Here you need a certain process of SQL:

- Only for 'temp_hum/emqx'

Based on the above principles, our final SQL should look like this.

```
SELECT
    timestamp div 1000 as up_timestamp, clientid as client_id, payload as temp_hum
FROM
    "temp_hum/emqx"
```

![Create Rule](https://assets.emqx.com/images/4d42641bd7c801c281c1833c9aeb272b.png)

![SQL Test](https://assets.emqx.com/images/50fd0316bd27e2315a0f4266dd4303f9.png)

**Create Action**

After completing the rule configuration, click Next to configure and create an action. We read the up_timestamp, client ID, temperature and humidity from the topic and save it to Redis.

```
HMSET ${client_id} ${up_timestamp} ${temp_hum}
```

![Create Action](https://assets.emqx.com/images/729993298d3b38b9143f10968c3eab8c.png)


## Test

1. Use [MQTT X](https://mqttx.app/) to connect the deployment

   You need to replace broker.emqx.io with the created deployment connection address, and add client authentication information to the EMQX Cloud console.

   ![connect the deployment](https://assets.emqx.com/images/181cf696ebf797ca39da452f73d3c393.png)

2. View the data saving results

   ```
   keys *
   HGETALL <client_id>
   ```

   ![View the data saving results](https://assets.emqx.com/images/1b61e8ee29bac99b2ffacd6008b9df74.png)

3. View rules monitoring

   Under View rule monitoring, the number of data dumping successes has increased.

   ![View rules monitoring](https://assets.emqx.com/images/c4f342f3089afed6a45f4b52553ab753.png)

 
## Summary

At this point, I hope you have successfully forwarded the data to GCP and integrated EMQX Cloud with other cloud services you have.

With this series of tutorials, you can enjoy a smooth migration of your business from GCP IoT Core to its alternative, EMQX Cloud. EMQX Cloud also provides some other excellent features, such as Shadow Service which implements IoT applications quickly through Topics and APIs. Readers are welcome to explore more in your IoT development journey with EMQX Cloud. 



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
