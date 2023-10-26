[EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) has gained significant popularity among IoT developers due to its simplicity and cost-effectiveness since its release in April 2023. It enables users to create a deployment effortlessly **in 5 seconds** and enjoy the service with minimal cost according to the actual consumption.

EMQX Cloud Serverless recently rolled out a major update to the latest EMQX 5.3 with enhanced performance and features. This release introduces APIs for deployment management and monitoring and the batch import user credentials feature for simplified large-scale device authentication.

## Serverless API

EMQX Cloud Serverless now offers the latest API version of EMQX 5.1. To access it, users must first create an APP Key and APP Secret for their application in the console. With the API, users can easily manage deployment and obtain client and subscription information, allowing for greater flexibility and freedom in using Serverless.

### What Can You Do with API?

The EMQX broker is designed to connect, move, process, and integrate your IoT data in real-time , while EMQX Cloud paves the way to the cloud for businesses by eliminating the burden of infrastructure maintenance. A complete IoT solution often requires many management platforms and applications. This is where Serverless API comes in - users can easily integrate [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) capabilities into their own platforms using API without having to log in to the EMQX  Cloud Console to obtain deployment-related information.

At present, EMQX Cloud Serverless offers the following APIs:

| **APIs**                  | **Description**                                              |
| :------------------------ | :----------------------------------------------------------- |
| Authentication Management | Manage the creation, deletion, and updating of the authentication information. |
| ACL Management            | Manage the creation, deletion, and updating of the access control. |
| Client Management         | View online client information, kick off clients, client subscribe, unsubscribe, bulk subscribe, and bulk unsubscribe. |
| Subscription Information  | View subscription information.                               |
| Message Publishing        | Publish messages, batch message publish.                     |

<section class="promotion">
    <div>
        Try EMQX Cloud Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

### How to Use API？

Using Serverless API is very simple. Open the deployment overview page after starting the deployment. Click "Create Application", and the system will generate a pair of AK/SK. The HTTP API uses basic authentication, and the ID and password should be filled in with the AppID and AppSecret respectively.

![Serverless API](https://assets.emqx.com/images/3b05620179140612376db602d21a8a75.png)

The request address is composed of several parts as follows.

{API}/{resource-path}?{query-string}

You can find the request and response for each type in [the API documentation of Serverless](https://docs.emqx.com/en/cloud/latest/api/serverless.html).

## Batch Import User Credentials

When each device requires unique usernames, passwords, or access controls, setting them up individually can be time-consuming. However, users can now create a batch import CSV file in the console and import it into the platform in bulk, solving this problem with ease.

![Batch Upload Authentication and Access Control](https://assets.emqx.com/images/0fd691ddecb8db297e27dbdfd7e21e9e.png)

The system supports importing up to 1000 pieces of information at a time and up to 2000 pieces of authentication and access control information. This is undoubtedly a very convenient feature for scenarios where each device needs to be managed separately.

## Summary

EMQX Serverless provides the most convenient IoT cloud solution for developers and enterprises through innovative models of pay-as-you-go and automatic scaling. With the addition of API and bulk import user credentials, it can better meet the needs of users' production environments and provide a complete solution for IoT digital transformation based on a fully managed platform.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
