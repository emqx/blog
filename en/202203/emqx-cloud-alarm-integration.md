As a fully managed MQTT service, [EMQX Cloud](https://www.emqx.com/en/cloud) is committed to providing users with reliable and real-time IoT data movement, processing and integration capabilities. Through perfect and automatic monitoring on operation and maintenance, EMQX cloud can relieve users from the burden of management and maintenance and accelerate the development of IoT applications.

Through EMQX Cloud, users can create a highly available [MQTT cluster](https://www.emqx.com/en/blog/tag/mqtt-broker-clustering) for device access in a few minutes. Throughout the subsequent lifecycle, the EMQ global service support team will provide up to 7*24 uninterrupted technical support and operation and maintenance services. In case of any problem encountered during use, users can quickly get a response at any time by means of work order, e-mail, telephone, etc.

In addition to 7*24 after-sales service support, EMQX Cloud also provides a wide range of automatic alerts reminders and alerts integration to realize early alerts of faults, which can facilitate the operation and maintenance personnel to deal with them on time to prevent unnecessary losses caused by reasons such as the loss of deployment messages.

Recently, **EMQX Cloud team has further optimized and updated the automatic alerts function and added a new alerts integration mode**, which will make the automatic early alerts function module of the entire product more perfect and more stable for users.

## Rich alerts modes and alerts events

EMQX Cloud currently supports the following alerts modes, of which the Webhook alerts is newly added:

1. Mailbox alerts integration, which receives alerts information by adding mailboxes
2. PagerDuty event alerts integration
3. Webhook alerts integration, which sends alerts information to communication software or users' own services

At the same time, rich alerts events are configured:

| **Type**                                                | **Level** | Description                                                  | Solution                                                     |
| :------------------------------------------------------ | :-------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| Excessive connections                                   | warning   | Too many connections for the deployment: {current connections} | Upgrade deployment specifications                            |
| Excessive traffic usage                                 | warning   | Excessive traffic in the past 24 hours for the deployment: {Total traffic in the past 24 hours} | Check whether the device traffic is normal. If it is normal, it is required to upgrade the deployment specifications. |
| Certificate expiration alarm                            | warning   | The deployment certificate will expire in {num} days, please update it! | Update deployment Certificate in time                        |
| Client authentication failed                            | warning   | A large number of client connections with authentication failures for the deployment | Check whether the client authentication configuration is correct |
| Client ACL authentication failed                        | warning   | A large number of client messages with failed ACL authentication are published for the deployment | Check whether the deployment access control configuration is correct |
| Connections with non-standard MQTT protocol connections | warning   | There are a large number of client connections with non-standard MQTT protocol | Check whether the MQTT protocol used by the client connection is the standard MQTT protocol |
| Deployment message discard                              | warning   | A large number of messages are discarded because the client is offline for a long time or the topic is not subscribed | Set clean session to False or set automatic reconnection for clients |
| Deployment TPS Exceeds Limit                            | warning   | When the deployment TPS exceeds the limit, please adjust the client sending rate in time, otherwise you will not be able to send new messages | Adjust the client sending rate in time so that the sending rate is less than the deployment TPS limit - |
| Abnormal Vpc peer connection                            | error     | Abnormal status of Vpc peer connection: {status}             | Check peer connection account of deployment peer account     |
| Abnormal xxx resource of rule engine                    | error     | Abnormal xxx resource of deployment rule engine              | Check whether the xxx resource configuration of rule engine in the deployment is correct |

The specific warning prompts are as follows:

![EMQX Cloud Alerts List](https://assets.emqx.com/images/cde3aef6b6dbaa68a934ebd99b829b42.png)

## How to set alerts integration

Enter the EMQX Cloud console, click 「Alerts」 on the left menu bar to start setting alerts integration.

### Mailbox alerts integration

You just need to add the mailbox that accepts the alerts information. When the deployment generates a alert, the alerts reminder can be sent to the mailbox as soon as possible.

![EMQX Cloud Mailbox alerts integration](https://assets.emqx.com/images/2ddd29ab2c46e3834e9a1efd969cae9a.png)
 

### PagerDuty alerts integration

It sends the alerts to the event in PagerDuty and specifies the notification method via PagerDuty.

1. Create alert service in PagerDuty

	![EMQX Cloud Create alert service in PagerDuty](https://assets.emqx.com/images/2f482f2c10d01eb9a93127b319827d5d.png)
 
2. Add api v2 integration and copy the integration key

	![EMQX Cloud Add api v2 integration](https://assets.emqx.com/images/6e24f9335779f40d3dff46921c81ced1.png)
 
3. Fill in the Integration key on EMQX Cloud

	![Fill in the Integration key on EMQX Cloud](https://assets.emqx.com/images/266896882af3819bcfef98629272f264.png)

### Webhook alerts integration

Through the Webhook alerts integration, you can send alerts to communication software or your own service. At the same time, you can test whether the Webhook is configured correctly through the function of message detection, which is highly flexible and adapts to the IM tool you are using.

#### Send alert messages to Slack

1. Create a webhook in Slack and get the webhook URL address. For more information, see [Sending messages using Incoming Webhooks](https://api.slack.com/messaging/webhooks?spm=a2c4g.11186623.0.0.2fa63db5J0PRQp);

2. Copy the Webhook API address, and in the alarm configuration, select Slack and fill in the name and Webhook address to complete the configuration.

	![EMQX Cloud Slack integration](https://assets.emqx.com/images/3fb039362fc3ee7d2f3774dc8e85be46.png)
    
3. To verify the configuration, you can use the test function to send a default message to check if the configuration is successful by selecting Slack item.

#### Send alert messages to custom services

In addition to sending alerts messages to robots in communication software, we can also send messages to our own services via Webhook.

1. First, you need to set up a service that can receive and process requests. In the new dialog box, select 「General Webhook 」.

2. Fill in the request address of the Webhook service in the new dialog box. At the same time, additional keys and values of request headers can be added.

	![EMQX Cloud Webhook](https://assets.emqx.com/images/1d8a406423f407a00e3aed3faf4ec135.png)  

3. To verify the configuration, you can use the test function to send a default message to check if the configuration is successful by selecting the configured Webhook alerts.

 
Through the above rich alerts modes, you can flexibly and freely set different alerts events for fault warning, and deal with the abnormality as soon as possible to ensure the stability of the business.

EMQX Cloud now offers a 14-day free trial. Don’t hesitate to click the link [Fully managed IoT MQTT cloud platform](https://www.emqx.com/en/cloud) to try out new features and give us your valuable advice.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
