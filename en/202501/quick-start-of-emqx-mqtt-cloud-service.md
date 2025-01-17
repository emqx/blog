EMQX Platform is a fully managed service for IoT messaging based on [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5). It offers reliable, scalable, and secure MQTT messaging for various IoT applications. With the EMQX Platform, you can quickly build industry applications and easily realize the collection, transmission, computation, and persistence of IoT data.

## Product Plan Overview

The EMQX Platform can be easily deployed on popular public clouds. The following product plans are available to offer you a tailored solution to meet your specific requirements:

- **Serverless**: Provides MQTT services on a secure, scalable cluster with pay-as-you-go pricing, making it a flexible and cost-effective solution for starting with [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt). The Serverless plan offers a 30-day free trial.
- **Dedicated**: The Dedicated Plan is designed for businesses that require enhanced performance and security with isolated resources The Dedicated plan offers a 14-day free trial.
- **Premium**: The Premium Plan offers all the advantages of the Dedicated Plan, along with additional features to support complex enterprise applications.
- **BYOC**: The BYOC Plan allows businesses to integrate the EMQX Platform with their existing cloud infrastructure. It keeps your data secure in your own cloud and manages it with EMQ’s expertise.

## Quick Guide

This guide will walk you through the process of setting up a stable MQTT 5.0 IoT platform on the EMQX Platform. By the end, you will learn how to:

- Deploy a Serverless deployment on the EMQX Platform.
- Configure the authentication for the deployment.
- Use an MQTT client tool to connect to the deployment.
- Publish and subscribe to MQTT messages.

### Step 1: Create an EMQX Platform Account

1. Visit the [sign-up](https://accounts.emqx.com/signup?continue=https%3A%2F%2Fcloud-intl.emqx.com%2Fconsole%2Fdeployments%2Fnew) page.
2. Complete the registration process.
3. Click on **Start free trial** to activate your account.

### Step 2: Create a Trial Deployment

1. Log in to the [EMQX Platform Console](https://accounts.emqx.com/signin?continue=https%3A%2F%2Fcloud-intl.emqx.com%2Fconsole%2Fdeployments%2F0%3Foper%3Dnew) using your account.

2. On the start page, click + **New Deployment**.

3. Select the **Serverless** plan and use the default settings.

   For detailed descriptions of deployment settings, refer to [Create a Deployment](https://docs.emqx.com/en/cloud/latest/create/overview.html) in the EMQX Platform documentation.

   Confirm your deployment information in the **Summary** section on the right and click the **Deploy** button at the bottom. This stage will prompt you to review and accept the *EMQX Platform Services Agreement*. It's important to thoroughly read the agreement and accept its terms to proceed.

![EMQX Platform Console](https://assets.emqx.com/images/3cedeaf9801f83666a0958d751c13a7e.png)

You have now completed the deployment creation process and need to wait for the deployment to be created. 

### Step 3: Access the Deployment Overview

Once the deployment status appears to **Running**, you can access the deployment overview page by clicking the deployment card just created.

On the Overview page, you can view the basic information of your deployment, such as real-time status and connection information. The address and port information are used for the client connection in later steps. From the deployment left menu, you can use and configure various functions provided by the deployment.

![Deployment Overview](https://assets.emqx.com/images/e5dfa0fe370e46bbfcda189923872d62.png)

### Step 4: Configure Authentication

To ensure the security of your data, you should add authentication information for this deployment before officially connecting from various clients/applications.

Follow the process below to add authentication:

1. Click **Access Control** → **Authentication** from the left menu.
2. On the Client Authentication page, select **+ Add**. 
3. Enter the authentication information, for example:
   - **Username**: `emqx`
   - **Password**: `public`
4. Click the **Confirm** button to complete.

Now, a record appears in the authentication list, which means that the authentication information has been added successfully.

### Step 5: Connect to the Deployment

So far, you have already had a Serverless deployment. There are many ways to connect a deployment. Usually, you can choose the programming method in formal use, such as using the MQTT client SDK of a certain programming language and establishing a connection for sending and receiving messages. You can also use [MQTT client tools](https://www.emqx.com/en/blog/mqtt-client-tools) with graphical interfaces to connect to the deployment. 

The following procedure shows you how to use a WebSocket client tool of the [MQTTX](https://mqttx.app/web) for connection.

1. Open the online interface of the [MQTTX Web](https://mqttx.app/web-client#/recent_connections).
2. Click + **New Connection**.
3. Enter the following information in the General part:
   - **Name**: Provide a name for your connection.
   - **Host**: Use the default `wss://` and enter the connection address of your deployment. You can find the address in the **Connection Information** area on the deployment Overview page shown in Step 3.
   - **Port**: Keep the default `8084`.
   - **Username** and **Password**: Enter the authentication information you added in Step 4.
4. Keep the other options as default and click **Connect**.

![MQTTX Web](https://assets.emqx.com/images/c1c03ff7c09bab79f5a26c1d7d80617d.png)

### Step 6: Publish and Subscribe to Messages

After you have successfully connected to the deployment, you can publish and subscribe to messages.

1. Click + **New Subscription** to open the **New Subscription** pop-up. 
2. Set the topic name to `test/1` and leave the other options as default. Click **Confirm.** The topic should be successfully subscribed. Next, publish a message on that topic to see if it can be received.
3. Select the connection you have created and enter the topic `test/1` in the lower publishing area. There is already a message in the message box. 
4. Send the message and observe it being received in real-time.

![Publish and Subscribe to Messages](https://assets.emqx.com/images/08d212c0659ef832304d0e2b69de8419.png)

## Conclusion

Congratulations! You have completed the operations of deployment creation, access control, and sending and receiving messages so far!

By following this guide, you have experienced the process of building an MQTT IoT platform from scratch. Of course, this is just the beginning. EMQX Platform offers advanced features for you to explore. For example, you can configure VPC peering connections so that your MQTT cluster can be integrated with other services deployed on the same public cloud platform in the same region. You can also use the powerful rule engine function to save the messages received by the MQTT cluster to different databases or forward them to other message queues according to the rules. These functions do not require you to write a line of code!

For any questions, comments, or suggestions, contact us at [cloud-support@emqx.io](mailto:cloud-support@emqx.io). Let the EMQX Platform help you develop your IoT business more smoothly!



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
