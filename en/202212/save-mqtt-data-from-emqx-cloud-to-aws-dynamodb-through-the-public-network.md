[Amazon DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) is a fully managed NoSQL database service that provides fast and predictable performance with seamless scalability. DynamoDB lets you offload the administrative burdens of operating and scaling a distributed database so that you don't have to worry about hardware provisioning, setup and configuration, replication, software patching, or cluster scaling. DynamoDB also offers encryption at rest, which eliminates the operational burden and complexity involved in protecting sensitive data. 

In this article, we will simulate temperature and humidity data and report it to the EMQX Cloud via the MQTT protocol, after which we will use the EMQX Cloud data integration to enable NAT gateway and save the data to the AWS DynamoDB over the public network. 


## Introduction to EMQX Cloud

[EMQX Cloud](https://www.emqx.com/en/cloud) is the world's first fully managed MQTT 5.0 public cloud service for IoT from EMQ. EMQX Cloud provides a one-stop O&M colocation and a unique isolated environment for MQTT services. In the era of Internet of Everything, EMQX Cloud can help you quickly build industry applications and easily realize the collection, transmission, computation and persistence of IoT data.

![MQTT Cloud](https://assets.emqx.com/images/e9d345da71dafee76364773a52aa2d5b.png)

With the infrastructure provided by cloud providers, EMQX Cloud is available in dozens of countries and regions around the world, providing low-cost, secure, and reliable cloud services for 5G and Internet of Everything applications.

For more information, please go to the [EMQX Cloud website](https://www.emqx.com/en) or see the [EMQX Cloud documentation](https://docs.emqx.com/en/cloud/latest/).


## Create Deployments

### Create EMQX Cluster

Once logged in, click "Cloud Console" under the account menu and you will be able to see the green button to create a new deployment. EMQX Cloud offers a 14-day free trial of Standard and Professional plans. This tutorial uses the professional deployment as a demonstration.

![Standard and Professional plans](https://assets.emqx.com/images/a677465d0b1e4e3198dd40db0aa41302.png)

Create an AWS deployment of EMQX Cloud, other options default.

![Create an AWS deployment](https://assets.emqx.com/images/6a42f07776ec3ff43bb946c79fef53b4.png)

When the status is Running, the creation of the deployment is complete.

![status is Running](https://assets.emqx.com/images/8a510a043c0020ba4ba365543d277af6.png)

### Create DynamoDB instances

If you are creating a DynamoDB instance for the first time, you can refer to the [help document](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStartedDynamoDB.html). First, go to the DynamoDB console and click Create Table.

![Create DynamoDB instances](https://assets.emqx.com/images/636f8df7b4a76eb422e38b3b3d4fb799.png)

Fill in key information such as table name, partition key, and other defaults, which can be set according to your actual business needs.

![Create DynamoDB Table](https://assets.emqx.com/images/3840e3fe5a6e2b78b51440d23e34fc92.png)

Until the status of the table is active, it means that you have successfully created the table 'temp_hum'.

![the status of the table is active](https://assets.emqx.com/images/7171f7218d31572a1ded15b35cd7b597.png)


## Enable NAT Gateway

[NAT gateways](https://docs.emqx.com/en/cloud/latest/vas/nat-gateway.html#service-activation) can provide network address translation services to provide Professional deployments with the ability to access public network resources without the need for VPC peering connections.

![Enable NAT Gateway](https://assets.emqx.com/images/2fb42ab1f156ddcc0c68caaf8123a898.png)


## [**Data Integrations**](https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_confluent.html)

1. **Create DynamoDB resources**

   Go to the Data Integrations page. On the data integration page, click DynamoDB resources.

   ![Go to the Data Integrations page](https://assets.emqx.com/images/2a86021226602deb01c3798219015c54.png)

   Fill in the DynamoDB connection details, and then click test. Please check the DynamoDB service if the test fails. Click the New button after the test is passed and you will see the Create Resource successfully message.

   ![Fill in the DynamoDB connection details](https://assets.emqx.com/images/af520c4f69ab99db72e71751c9d84255.png)

2. **Create a new rule**

   After the resource is successfully created, you can return to the data integration page and find the newly created resource, and click create rule. Our goal is that as long as the temp_hum/emqx topic has monitoring information, the engine will be triggered. Certain SQL processing is required here:

   - Only target the topic "temp_hum/emqx"
   - Get the three data we need: temperature, humidity

   According to the above principles, the SQL we finally get should be as follows:

   ```
   SELECT 
   id as msgid,
   topic, 
   payload 

   FROM "temp_hum/emqx"
   ```

   ![Create a new rule](https://assets.emqx.com/images/c7306a3bf30d19b001b728fd411654f4.png)

   You can click SQL Test under the SQL input box to fill in the data:

   - topic: temp_hum/emqx
   - payload:

   ```
   {
     "temp": 26.3,
     "hum": 46.4
   }
   ```

   Click Test to view the obtained data results. If the settings are correct, the test output box should get the complete JSON data as follows:

   ![JSON data](https://assets.emqx.com/images/fb27de726b5ff92095e96d20c4e623ba.png)

   If the test fails, please check whether the SQL is compliant and whether the topic in the test is consistent with the SQL filled in.

3. **Add Action to Rule**

   After completing the rule configuration, click Next to configure and create an action. Then enter the fields and tags as follows:

   ```
    DynamoDB Table：temp_hum
    Hash Key：msgid
   ```

   ![Add Action to Rule](https://assets.emqx.com/images/ded28a8f05a43995295f78a966b46de4.png)


## Verification

1. **Use MQTTX to simulate data reporting**

   We recommend you to use [MQTT X](https://mqttx.app/), an elegant cross-platform MQTT 5.0 desktop client to subscribe/publish messages.

   Click on the add button and fill in the deployment information to connect to the deployment. You need to replace `broker.emqx.io` with the created deployment [connection address](https://docs.emqx.com/en/cloud/latest/create/overview.html#view-deployment-information), add [client authentication information](https://docs.emqx.com/en/cloud/latest/deployments/auth_overview.html#authentication) to the EMQX Cloud console. Enter the topic name and payload message to publish the message.

   ![MQTTX](https://assets.emqx.com/images/3d3ba6a7cf7228c0661beb4a15c5f20f.png)

2. **View rules monitoring**

   Check the rule monitoring and add one to the number of success.

   ![View rules monitoring](https://assets.emqx.com/images/06f122a35e4e61e877fb3a9db7681248.png)

3. **View results in NoSQL Workbench**

   [NoSQL Workbench](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.settingup.html) for Amazon DynamoDB is a cross-platform client-side GUI application for modern database development and operations. You can reach out to it to connect to DynamoDB.

   ![connect to DynamoDB](https://assets.emqx.com/images/77dc1296b979eba6802b06de15d5fa4c.png)

   Go to the Operation Builder page. Select the table 'temp_hum'. Here you can see the results of the temperature and humidity data forwarding.

   ![Go to the Operation Builder page](https://assets.emqx.com/images/26a7cb6c8ec5196ad5b2c7562d520e3c.png)


## Summary

So far, we have used EMQX Cloud data integration to save the entire process of data to the AWS DynamoDB over the public network. Then, you can integrate with AWS services to do more with your data, like using built-in tools to perform analytics, extract insights, and monitor traffic trends, which will save you more time to focus on building your IoT applications.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
