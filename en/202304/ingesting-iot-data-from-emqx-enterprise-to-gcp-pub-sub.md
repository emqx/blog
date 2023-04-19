**Table of Contents**

- [Create and Manage Pub/Sub Topics](#create-and-manage-pub-sub-topics)
- [Forward MQTT Messages to Pub/Sub](#forward-mqtt-messages-to-pub-sub)
- [Testing and Verification](#testing-and-verification)
- [Summary](#summary)

You may have already successfully connected your IoT devices to [EMQX Enterprise](https://www.emqx.com/en/products/emqx) using the instructions provided in our [previous posts](https://www.emqx.com/en/blog/migrating-devices-from-gcp-iot-core-to-emqx-enterprise). This article will introduce how to ingest IoT data from EMQX Enterprise to GCP Pub/Sub service to help you complete the migration.


## Create and Manage Pub/Sub Topics

If Pub/Sub has not been enabled yet, you can create a topic by following these steps.

1. Open the [Pub/Sub console](https://console.cloud.google.com/cloudpubsub), click **CREATE TOPIC**, input a custom **Topic ID**, and click **CREATE** to create it.

   ![Topics](https://assets.emqx.com/images/1af6764b8a05c6dfc5745936a06b410c.png)

   ![Create Topic](https://assets.emqx.com/images/3819a535621743036f51c9afd043c131.png)

2. Navigate to the topic details page by clicking on the corresponding **Topic ID** from the list. Once on the page, create a subscription to store messages. Choose the Pull type and specify a message retention duration of 7 days.

   > Please refer to [GCP Pub/Sub subscription](https://cloud.google.com/pubsub/docs/subscriber) for comprehensive information regarding subscriptions.

   ![Create a subscription 1](https://assets.emqx.com/images/7f60890709ac695d7efcbbd687cf7aa1.png)

   ![Create a subscription 2](https://assets.emqx.com/images/be591a20512d20c3b3d933518664837f.png)

3. Click **Subscription ID** → **MESSAGES** → **PULL** to view the messages sent to the topic.

   ![Click Subscription ID](https://assets.emqx.com/images/444cc8dd168dd3961f7ed9571e7b0da6.png)

   ![Click PULL to view the messages](https://assets.emqx.com/images/b7803851608ab74b10ea750b1c8ef63e.png)

After successfully creating a Pub/Sub topic and gaining familiarity with its basic management operations, we can now use EMQX Enterprise to forward data to the newly created topic.

## Forward MQTT Messages to Pub/Sub

EMQX Enterprise offers GCP Pub/Sub integration for easy IoT Core migration. Even if you are not an IoT Core user, you can still forward client events and messages to the relevant Pub/Sub topics, integrating IoT data with applications and services on Google Cloud.

The following steps are to configure Pub/Sub integration on EMQX Enterprise.

### Create a Service Account JSON

The Service Account JSON is a file containing authentication and authorization credentials, and EMQX Enterprise must access Pub/Sub resources.

1. Go to the [GCP Console](https://console.cloud.google.com/welcome), input **IAM** in the search box, and go to the **IAM & Admin** page.

   ![Search IAM & Admin](https://assets.emqx.com/images/77f771f9effb89fcc7d9f244513e5c7f.png)

2. Navigate to the **IAM & Admin** page and click on **Service Accounts** → **Email**. Then select the appropriate email address and click on the **KEYS** tab. From there, click **ADD KEY** to create a new key in **JSON** format for authentication. Be sure to keep this file secure.

   ![Click Service Accounts](https://assets.emqx.com/images/efcf0f73347384a12e77841f2ce307d1.png)

### Create a Pub/Sub Resource

1. Open the EMQX Dashboard, go to **Rule Engine** → **Resources**, click **Create**, and select **GCP PubSub** on the pop-up box.

   ![EMQX Dashboard Rule Engine](https://assets.emqx.com/images/f1e424dde3e247c7e1d5f6818195c495.png)

2. Provide a Resource ID to identify the resource and paste the previously generated Service Account JSON into it. Before creating the resource, it is recommended to click on **Test** to ensure connectivity. If no issues are found during the connectivity test, click **Confirm** to complete the creation process.

   ![Create Resource](https://assets.emqx.com/images/ddaa51396fa214c910ba4531512e13c1.png)

3. Once the resource is successfully created, it will appear as available. The next step is to configure the rule for forwarding data to this resource.

   ![Resource list](https://assets.emqx.com/images/b9adea937b6c0f3bf6a556741026f5b2.png)

### Create a Rule to Forward Data to Pub/Sub

1. Click **Rule** → **Create** to enter the rule creation page. In the **SQL** field, input the following content.

   ```
   SELECT
     *
   FROM
     "t/#"
   ```

   The SQL statement will be executed when a message is received that matches the `t/#` topic. The SELECT clause will then retrieve the client context and message payload, which will be used in the action.

   For more SQL functions and use cases, please refer to the [EMQX Rule Engine](https://docs.emqx.com/en/enterprise/v4/rule/rule-engine.html).

   ![Create Rules](https://assets.emqx.com/images/76a3424ded7314f2adeb4ba024365b9a.png)

2. Click **Add action** at the bottom of the page, select the action type **Data forward**, choose **Data to GCP Pubsub**, and select the resource just created to forward the SQL output to Pub/Sub.

   ![Add action 1](https://assets.emqx.com/images/3578ea736ac4315314266808ed8484a8.png)

3. Input the pre-created **Topic ID** into the **GCP PubSub Topic** field, and construct the message that needs to be forwarded in the **Payload template**. By default, the payload template is empty and will forward the entire SQL output result. Once you have made the necessary changes, click on the **Confirm** button to complete the creation of the action.

   ![Add action 2](https://assets.emqx.com/images/e4b8dc8a7426474700fcfbaa8a5209a4.png)

4. After confirming everything is correct, click Create to complete rule creation.

   ![Click Create to complete rule creation](https://assets.emqx.com/images/7b8e58f885832cb3e726ca6e964fa675.png)

## Testing and Verification

In the previous steps, a rule was created to forward all messages that match the t/# topic to the **my-iot-core** topic in Pub/Sub.

Next, we will use the WebSocket tool to perform a verification test.

1. Go to the **Tool** → **WebSocket** page, establish a client connection, and publish several messages to the **t/1** topic.

   ![Tool → WebSocket page](https://assets.emqx.com/images/953d28df2b3fe4be654d77275931393b.png)

2. On the **Rule** page, click the Monitor icon in the table to view the statistics of the specified rule. You can see that **data_to_gcp_pubsub** has 4 records, indicating that the data has been successfully written to Pub/Sub.

   ![Click the Monitor icon](https://assets.emqx.com/images/145599fb22f0df6be25a451f871da715.png)

3. On the details page of the Pub/Sub subscription, you can view the corresponding message received by the topic.

   ![Details page of the Pub/Sub subscription](https://assets.emqx.com/images/d08f03cc53e2c82a6122068983b1fd95.png)

## Summary

We have covered the steps and procedures to migrate IoT Core services to an EMQX Enterprise cluster within the user's GCP environment. 

To learn more about what you can do with EMQX Enterprise, please visit [EMQX Enterprise Documentations](https://docs.emqx.com/en/enterprise/v4.4/#benefits) or [contact us](https://www.emqx.com/en/contact?product=emqx) to book a demo.

## Other Articles in This Series

- [3-Step Guide for IoT Core Migration 01 | How to Deploy EMQX Enterprise on Google Cloud](https://www.emqx.com/en/blog/how-to-deploy-emqx-enterprise-on-google-cloud)
- [3-Step Guide for IoT Core Migration 02 | Migrating Devices from GCP IoT Core to EMQX Enterprise](https://www.emqx.com/en/blog/migrating-devices-from-gcp-iot-core-to-emqx-enterprise)


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
