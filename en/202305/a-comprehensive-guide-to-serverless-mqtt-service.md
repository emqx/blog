## Introduction

[EMQX Cloud](https://www.emqx.com/en/cloud) recently launched Serverless 1.0, a cost-effective solution designed to help developers and startups efficiently test and develop MQTT-based applications. By utilizing shared clusters, this version provides a convenient MQTT service that simplifies the development process. It only takes a few seconds to have a fully functional MQTT server with [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt). 

Besides, users can get 1 million free session minutes per month, which is enough for 23 devices to be online for a whole month, perfectly covering tiny IoT test scenarios.

This article will show you how to create a serverless deployment, simulate a client connection to the deployment via [MQTTX](https://mqttx.app/) and test how to send/receive messages, helping you quickly realize a basic connectivity test scenario.

## Prerequisites

Before you start, you need to:

- [Register an account](https://accounts.emqx.com/signup?continue=https%3A%2F%2Fcloud-intl.emqx.com%2Fconsole%2Fdeployments%2F0%3Foper%3Dnew) on EMQ official website.
- Make sure there are no overdue bills in your account if you already have one.

## Create a Deployment in 5 Seconds

1. Log in to the official website, select EMQX Cloud, choose the serverless edition, and click "Start for free".
   Compared with the dedicated edition, the usage and charges of serverless edition are slightly different, mainly in the following aspects.

   ![Compared with the dedicated edition](https://assets.emqx.com/images/7df75364594e1693eb49563e15dd9cf5.png)

   ![Create a Deployment](https://assets.emqx.com/images/270477f56cab1bc249ec02a23aa247f9.png)

2. Confirm the configuration details and set the spending limit, click "Deploy". Then read and agree to the terms and conditions.

   Also, you can suspend your service or keep billing with a reminder when you reach the spending limit.

   In this step, you should set the maximum amount you can spend after your usage exceeds the free monthly quota. This ensures that your spending is within a reasonable, predictable range.

   Also, you can suspend your service or keep billing with a reminder when you reach the spending limit.

   > Note: Now serverless can only be deployed in the AWS Virginia region.

   ![Set the spending limit](https://assets.emqx.com/images/cd0cfeae2305a50971d77e11f94da8fa.png)

   Click “Get Started” to enter the deployment creation process.

   ![Get Started](https://assets.emqx.com/images/cd0195198e07447f0231b990d39fb856.png)

   After waiting a few seconds, refresh the page, and you can see the deployment status changed from "Configuring emqx" to "Running", click the deployment card to enter the deployment overview page.

   ![Deployment status: Configuring emqx](https://assets.emqx.com/images/c3126afb239c2c0e9ad2cc5d4aba4cde.png)

   ![Deployment status: Running](https://assets.emqx.com/images/9df1239364915cf600e4934e33e6dcd8.png)


## Understand the Main Functions of Serverless Deployment

### Deployment Overview

On the Deployment Overview page, you can view information about the usage of the deployment, as well as the connection addresses and connection ports that may be used.

![Deployment Overview page](https://assets.emqx.com/images/d277fef6a3615e439f9a4f5874bc31c4.png)

### Authentication & ACL

On the Authentication page, you can add authentication information of a client or device by clicking "Add" and filling in "Username" and "Password" to add an authentication message.

On the ACL page, you can continue to set the access control privileges for the client by Client ID.

![Add Authentication](https://assets.emqx.com/images/dbb6fbe31e8c28a75c2c0764b6012dc9.png)

### Monitor

You can view real-time data such as the number of connections, TPS, subscriptions, and topics on the monitoring page. It also supports searching by specified criteria from clients or subscriptions level.
Specific search rules can be found at: [Monitors](https://docs.emqx.com/en/cloud/latest/deployments/monitors.html).

![Monitoring page](https://assets.emqx.com/images/2b87c4bca6df1f18a1ccdb5f651ca64d.png)

### Metrics

EMQX Cloud provides four types of incremental metrics: sessions, messages,  traffic, and dropped messages. You can view these charts corresponding to each metric and detailed information at a certain time. In the upper right corner, you can switch between the 1 hour, 1 day, 7 days, 1 month, and 6 months of data.

![Metrics page](https://assets.emqx.com/images/10f8df3b8cc7add9279b21bd15ee47ef.png)

### Alerts

This page allows you to configure alert messages sent by EMQX Cloud to your email address or integrate them with other third-party notification platforms. By receiving timely alerts, you can quickly respond to issues and take necessary measures to resolve them.

The specific alert events provided can be viewed at: [Alerts](https://docs.emqx.com/en/cloud/latest/deployments/alerts.html#alerts-event).

![Alerts page](https://assets.emqx.com/images/8644d769245f354795a24ea2c711c3b7.png)

### Online Test Tool

The online test tool provides an online web testing tool to debug the communication between clients online through a graphical interface, which can be used to test the connection quickly.

Username and password can be filled in with the information you just added to the authentication page. Give a connection name like "test" leave other information as default and click "connect", you will find the connection is successful.

![Online Test Tool](https://assets.emqx.com/images/41cdf3634dab55348576cd76e25bdf8e.png)

Before we publish the message, we should create a subscription. Click Subscribe to create a subscription.

![Click Subscribe](https://assets.emqx.com/images/0bbc5298f0b1e78c46e2b4d82e697e67.png)

Then you can publish a message. Here we use the default message. Of course, you can send any message you like, only if the message fits the message specification.

Click the "Publish".

![Click the "Publish"](https://assets.emqx.com/images/0f5a5ab4cc8c90f764c7ac5e2ec51ca6.png)

You can find the message you sent on the topic you created before has been received successfully.

![Receive and send messages](https://assets.emqx.com/images/2818b2febaae581bd58aefd0de2a3ba6.png)

### Client Connections Guide

This page provides you with a variety of ways to establish MQTT client connections, including client-side tools, various development languages, and third-party SDKs. You can choose the way you are familiar with and follow the guides to establish a connection. Any problems in establishing a connection can be feedback to the technical support team by submitting a ticket in the upper right corner of the console.

![Client Connections Guide](https://assets.emqx.com/images/06ee5691200bbb5712a5636e9a86c375.png)

## Using MQTTX to Test Connections to Serverless Deployment

In this tutorial, we choose [MQTTX](https://mqttx.app/) to test the connection. MQTT X is an elegant cross-platform MQTT 5.0 desktop client provided by EMQ. 

Download and Install: [https://www.emqx.com/en/try?product=MQTTX](https://www.emqx.com/en/try?product=MQTTX) 

### Create a new connection

1. Start MQTTX. Click “New Connection”.

2. Fill in the general information.

   - Name: Type “serverless”
   - Client ID: It is randomly generated.
   - Host and Port: Select the host and type the port based on the information on the deployment overview page. The port for mqtts:// is 8883 and wss:// is 8084.
   - Username and Password: Type the information based on what you have added in the Authentication page.

   ![Create a new connection](https://assets.emqx.com/images/21bf377f4a7116547bfd4da3c35fd397.png)

3. Enable the SSL/TLS and SSL Secure.

   > Note: EMQX Cloud serverless version needs to establish a secure connection based on TLS/SSL, if the client needs a CA file, you can go back to the deployment overview page to download it.

4. Click “Connect”.

   You can see on the deployment overview page that the connection is successful.

   You can fill in the Username and Password just added in the authentication, click "connect", and you can see the connection is successful.

   ![Download CA file](https://assets.emqx.com/images/61ca8298796efcc3039d64f5cf807998.png)

### Publish and Subscribe

1. Click "+ New Subscription"

   ![New Subscription](https://assets.emqx.com/images/272bdeef9e4f3801f6a71586b5e12c71.png)

2. Leave the topic name as the default, or you can type your own topic name.

3. Leave other settings as default. Click “Confirm”.

   ![Customize the topic name](https://assets.emqx.com/images/f2c5a5cd0395414fe427a0cc73bc9c45.png)

4. Use the same connection as a client to publish a preset message on the topic “testtopic”. Click the “send” icon.

   ![Test publishing message](https://assets.emqx.com/images/429ee323e38689f32d24f127d442efe4.png)

### View Monitoring Information and Metrics

You can view the metrics on the Console monitor and metrics page.

![View monitor information](https://assets.emqx.com/images/5e6b8857282a41e26173ace0ecf9864c.png)

![View metrics information](https://assets.emqx.com/images/b5314923c9fbdf12c750397cd68fb237.png)

## Conclusion

[EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) is a powerful tool that simplifies the deployment and management of your MQTT messaging infrastructure. With this guide, you can easily create serverless deployments, simulate MQTT client connections, and test message sending and receiving. By utilizing EMQX Cloud Serverless, you can streamline your development process and scale your infrastructure with ease.

[Learn more here.](https://www.emqx.com/en/cloud/serverless-mqtt)  If you have any questions or feedback, please feel free to [contact us](https://www.emqx.com/en/contact?product=cloud). 



<section class="promotion">
    <div>
        Try EMQX Cloud Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
