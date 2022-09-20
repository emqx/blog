Recently, [EMQX Cloud](https://www.emqx.com/en/cloud), the fully-managed cloud-native MQTT service from EMQ, officially supports the establishment of a secure and stable private connection to AWS services via AWS PrivateLink. This enables bi-directional connectivity between public cloud services and EMQX Cloud deployments via intranet IP addresses.

## What's AWS PrivateLink？

AWS PrivateLink provides private connectivity between VPCs, AWS services, and your on-premises networks, without exposing your traffic to the public internet. AWS PrivateLink makes it easy to connect services across different accounts and VPCs to significantly simplify your network architecture.

Compared with VPC peering, which is like normal routing between network segments, AWS PrivateLink allows you to publish an "endpoint" with which others can connect from their own VPC.

## Why use AWS PrivateLink?

**Secure your traffic**

It’s more secure and scalable to connect your VPCs to services in AWS with AWS PrivateLink. Network traffic that uses AWS PrivateLink doesn't traverse the public internet, reducing exposure to brute force and distributed denial-of-service attacks, along with other threats.

**Simplify network management**

You can connect services across different accounts and Amazon VPCs, with no need for firewall rules, path definitions, or route tables. There is no need to configure an Internet gateway, VPC peering connection, or manage VPC Classless Inter-Domain Routing (CIDRs).

**Accelerate your cloud migration**

AWS PrivateLink makes it easier to migrate traditional on-premises applications to SaaS offerings hosted in the cloud.  Since your data does not get exposed to the Internet where it can be compromised, you can migrate and use more cloud services with the confidence that your traffic remains secure. You no longer have to choose between using a service and exposing your critical data to the Internet.

## How to connect to EMQX Cloud via AWS PrivateLink

> Note: The feature is only available in the professional plan.

1. Log in to the console and create a Professional deployment. Then visit the deployment overview, click 「+ PrivateLink」

   ![PrivateLink](https://assets.emqx.com/images/b07782731acbc6dbbd1c00d7031004c0.png)
 
2. Follow the guideline, before you configure a private link connection, you need to make several prerequisites at AWS. Also, we provide the information you may need during the progress.

   ![PrivateLink 2](https://assets.emqx.com/images/63182ed9306bddffc940b21ecd83f95f.png)

3. Then enter the name of Endpoint Service. You can find the name you need to fill in according to the sample.

   ![PrivateLink 3](https://assets.emqx.com/images/6f8c99a96ccc3789fdef95180b3b3edb.png)

4. If you have set the Endpoint service at your AWS account, it will take 2-3 minutes to create the endpoint service connection.

   You can follow [VPC] - [Endpoint Service] - [Endpoint Connections] to find connection requests and click `Accept Endpoint Node Connection Request`.

   ![Endpoint Connections](https://assets.emqx.com/images/f5e42a385fa2f0a0e07731996de70fc8.png)

5. If you fail to create the connection, you can check the mistakes referred to our fail notifications.

> For more information, please click our help document: [https://docs.emqx.com/en/cloud/latest/deployments/privatelink.html](https://docs.emqx.com/en/cloud/latest/deployments/privatelink.html) 

## Conclusion

With the AWS PrivateLink feature update, in addition to VPC peering, you are able to choose a more secure and reliable way to connect your cloud service to EMQX Cloud, which will better secure your data. EMQX Cloud is dedicated to providing your IoT business with reliable, real-time IoT data transmission, processing, and integration as always.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
