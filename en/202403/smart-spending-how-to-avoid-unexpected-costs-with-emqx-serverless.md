## Introduction

Serverless services offer developers a hassle-free cloud solution, featuring an elastic infrastructure and a pay-as-you-go pricing model. This approach means that users only pay for the resources they actually use. However, there have been instances that highlight a potential downside: unexpected events such as DDoS attacks or unusual client connections can result in users facing unexpectedly high bills.

Choosing the EMQX Platform Serverless edition alleviates this concern. Thanks to its flexible pricing and cutting-edge Serverless MQTT technology, EMQX Serverless allows you to enjoy a seamless, advanced, fully-managed MQTT cloud service without financial surprises.

## Understanding the Billing Model of EMQX Serverless

EMQX Serverless employs a pay-as-you-go billing model, based on three key components: session minutes, traffic (bandwidth), and rule actions.

- Session Minutes: Calculated per session initiated within a minute or part thereof.
- Traffic (Bandwidth): Encompasses both inbound and outbound messages processed by the deployment.
- Rule Actions: Pertains to the total number of actions performed within Data Integration.

For comprehensive details on EMQX Serverless Pricing, please visit our [pricing page](https://www.emqx.com/en/pricing).

## Spend Limit Feature: Maintain Control Over Your Costs

The "Spend Limit" feature provided by EMQX Serverless is a pivotal cost-control mechanism, allowing you to set a monthly budget for your serverless deployment. This feature ensures you can keep your monthly expenses within a pre-defined limit and receive alerts as you near this threshold.

The Spend Limit is adjustable from 0 to 10,000:

- Set to 0: The deployment will operate within the free quota only. Once this quota is depleted, the deployment will pause.
- Set between 1 and 10,000: Offers the flexibility to either pause the deployment or receive an alert when the monthly limit is reached.

![image.png](https://assets.emqx.com/images/bedc1b9736d2f158bbd5e3bdd14b01b4.png)

By setting a Spend Limit, you can mitigate concerns about unexpected expenses due to additional session minutes or traffic.

## A Special Offer: Free Quota

EMQX Serverless includes a monthly free quota of billing units, ensuring you can enjoy a complimentary MQTT service as long as your usage stays within this quota.

| **Billing Unit** | **Free Quota**                    | **Pricing**                       |
| :--------------- | :-------------------------------- | :-------------------------------- |
| Session minute   | 1 million session minutes / month | $2.00 per million session minutes |
| Traffic          | 1 GB / month                      | $0.15 / GB                        |
| Rule action      | 1 million rule actions            | $0.25 per million rule actions    |

By setting the Spend Limit to 0 and utilizing the free quota, you can streamline your operations without any initial costs and without the need for a credit card.

## Build Your Hassle-Free MQTT Infrastructure Today

With its adaptable billing model and the Spend Limit feature, EMQX Serverless delivers a scalable infrastructure for MQTT solutions, protecting you from unforeseen billing issues. Experience the benefits for yourself and enhance your cloud experience by trying it today.



<section class="promotion">
    <div>
        Try EMQX Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
