## Introduction

Serverless MQTT offers IoT developers a managed MQTT service with an elastic infrastructure. With its pay-as-you-go pricing model, [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) enables users to reduce IoT expenses and swiftly initiate MQTT deployments.

> Further information about EMQX Cloud Serverless: [Next-Gen Cloud MQTT Service: Meet EMQX Cloud Serverless](https://www.emqx.com/en/blog/next-gen-cloud-mqtt-service-meet-emqx-cloud-serverless)

What’s more, EMQX Cloud Serverless even provides an opportunity to obtain a forever-free [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison). Let's explore how this remarkable offering is made possible in this blog.

## Billing Mode of EMQX Cloud Serverless

First of all, it’s essential to understand the billing mode of EMQX Cloud Serverless. 

It calculates the concurrent clients with sessions. To be more specific, the number of sessions = the number of connected clients + the disconnected clients with sessions retained in the broker. 

If you have no idea about retained sessions (or persistent sessions), [this article explains it well](https://www.emqx.com/en/blog/mqtt-session). 

With the definition of the session, EMQX Cloud Serverless’s billing units are Session Minutes and Traffic. 

- Session Minutes: One session minute stands for one session to the deployment in the span of a minute or part thereof. 
- Traffic: Both **inbound and outbound** traffic of deployment are measured.

## Free Quota

EMQX Cloud Serverless offers a free quota of billing units every month. You will never get charged if your usage is always within the free quota.

| **Billing unit** | **Free quota**                    | **Pricing**                       |
| :--------------- | :-------------------------------- | :-------------------------------- |
| Session minute   | 1 million session minutes / month | $2.00 per million session minutes |
| Traffic          | 1 GB / month                      | $0.15 / GB                        |

To give you a vivid idea of how much are 1 million session minutes and 1 GB of traffic:

If a single [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) remains connected for a whole month, it will consume approximately 43,200 session minutes. Based on this estimate, one million session minutes could support up to 23 clients remaining connected for a month. This number will increase if clients go online and offline periodically.

Assuming an average message size of 500 bytes, it is estimated that approximately 2,147,483 messages can be sent and received in a month. With 23 MQTT clients, each client could send and receive around 130 messages per hour continuously for a month. It is obvious that the free quota can support small-scale IoT scenarios with ease.

Best of all: No credit card is required.

 

## Spend Limit

You may want to ensure that you can always use the service without incurring any additional fees. Here comes the Spend Limit.

Spend Limit can control the monthly consumption of the serverless deployment within a set value or provide a reminder when the limit is approached. You can set a Spend Limit during the deployment creation process and make adjustments later.

![Edit Spend Limit](https://assets.emqx.com/images/891e3c4b66138d2015bc729dcf4b5c4b.png)

Spend Limit can be an integer between 0 to 10000:

- If it is set to 0, the deployment will only consume the free quota of 1 million connection minutes and 1 GB of traffic per month. When the free quota is used up, the deployment will be stopped.
- If it is set to an integer between 1 and 10,000, the user can decide whether to halt the deployment or send a reminder when the monthly consumption limit is reached.

You can obtain an MQTT broker forever free with the value set to zero. And if you are willing to pay for the extra session minutes or traffic, you don’t have to worry about overspending by setting a Spend Limit. 

## Summary

With the release of [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt), an even wider range of users can experience the convenience that EMQX Cloud provides. Whether you're a large enterprise or a start-up, you can rely on the stable and dependable data infrastructure services offered by EMQX Cloud to power your IoT business innovation.

[Register and get a forever free MQTT service](https://accounts.emqx.com/signup?continue=https%3A%2F%2Fcloud-intl.emqx.com%2Fconsole%2Fdeployments%2F0%3Foper%3Dnew) today!

You may also want to read:

- [A Comprehensive Guide to Serverless MQTT Service | EMQX Cloud](https://www.emqx.com/en/blog/a-comprehensive-guide-to-serverless-mqtt-service)
- [Serverless or Hosting? Choose a Suitable MQTT Service for Your Project](https://www.emqx.com/en/blog/serverless-or-hosting-choose-a-suitable-mqtt-service-for-your-project)



<section class="promotion">
    <div>
        Try EMQX Cloud Serverless
        <div class="is-size-14 is-text-normal has-text-weight-normal">Forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
