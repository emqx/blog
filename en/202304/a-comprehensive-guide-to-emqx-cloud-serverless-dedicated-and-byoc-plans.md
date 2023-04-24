## Introduction

[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed, cloud-native MQTT messaging service built on [EMQX Enterprise](https://www.emqx.com/en/products/emqx). EMQX Cloud offers three deployment plans to cater to various customer needs: [Serverless](https://www.emqx.com/en/cloud/serverless-mqtt), [Dedicated](https://www.emqx.com/en/cloud/dedicated), and [BYOC (Bring Your Own Cloud)](https://www.emqx.com/en/cloud/byoc).

This article briefly introduces the key differences among these three plans, and presents three user stories to help you better understand the suitable scenarios for each plan. This will help you to find the most appropriate solution based on your requirements.

>**TL;DR:**
>
>- If you're looking for a cost-effective and easily scalable MQTT cloud service, the Serverless plan is your top choice.
>- If you need a high-performance, customizable MQTT cloud service to support enterprise-level projects, the Dedicated plan is your ideal choice.
>- If you have specific data security and compliance requirements and want to deploy MQTT services on your cloud infrastructure, the BYOC plan will meet your needs.

## EMQX Cloud Serverless

[EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) is a serverless architecture where users don't have to worry about underlying infrastructure and resource management. It's particularly suitable for individual developers, small-to-medium projects, and development or testing environments.

### Benefits

- Low cost: Pay As You Go model, pay for actual usage without needing to purchase resources in advance.
- Auto-scaling: Adjust resources automatically based on business needs, without manual intervention.
- No underlying infrastructure management: Focus on application development while the EMQX Cloud professional team handles underlying operations.

### Suitable for:

- Individual developer projects or small-to-medium enterprise projects, development, and testing environments.
- No need for data integration, dedicated networks, or other features.
- Up to 1,000 devices online simultaneously and a maximum of 1,000 messages per second.

### User Story

Michael is a developer at a startup with a limited budget. Their project scale is not large, so they want a pay-as-you-go, cost-effective cloud service. They discover EMQX Cloud Serverless.

The Serverless plan provides Michael with an environment where he doesn't have to worry about the underlying infrastructure and is billed based on actual usage. It takes less than 3 minutes for Michael to create an account and have a fully functional standard MQTT service. Additionally, as the business grows, system resources can automatically scale up or down, allowing Michael to focus on application development. The Serverless plan meets Michael's needs, helping them build small-to-medium projects at a low cost.

## EMQX Cloud Dedicated

[The Dedicated plan](https://www.emqx.com/en/cloud/dedicated) provides customers with independently deployed EMQX Cloud instances, offering higher performance guarantees and customizability. It is suitable for enterprise-level projects with high performance and stability requirements.

### Benefits

- Independent deployment: Each customer has an independent instance, ensuring stable performance.
- Highly customizable: Supports customization based on customer needs.
- Fully managed: Enjoy professional technical support, reducing operational pressure.

### Suitable for:

- Enterprise-level projects with high performance and stability requirements.
- Offers different connection specifications with no upper limit.

### User Story

Christina is a digital transformation project manager at a large enterprise, and her project demands high performance and stability. She needs an independently deployed and customizable cloud service to ensure a stable system operation. After learning about EMQX Cloud Dedicated, she finds it the solution she's been looking for.

The Dedicated plan provides Christina with an independent instance, guaranteeing stable performance. Additionally, Christina can choose her preferred cloud service provider and deployment region and achieve reliable, secure connections with other internal services through VPC peering. The Dedicated plan also supports personalized customization, allowing adjustments based on project requirements. Moreover, the EMQX Cloud team offers professional technical support, allowing Christina to confidently deliver enterprise-level projects.

## EMQX Cloud BYOC

[The BYOC (Bring Your Own Cloud) plan](https://www.emqx.com/en/cloud/byoc) allows customers to deploy the EMQX cluster on their own cloud infrastructure while still being managed by the EMQX team, meeting specific security and compliance requirements.

### Benefits

- Choose your own cloud provider and infrastructure: Select one that suits your business needs and is wholly owned by your company.
- Meet specific security and compliance requirements: Addresses data security and compliance concerns.
- Fully utilize existing cloud resources: Maximize the use of current cloud resources to reduce costs.

### Suitable for:

- Enterprise-level projects with strict data security and compliance requirements.
- Already have a stable set of cloud resources.

### User Story

James is an operations director at a leading automotive company with strict data security and compliance requirements. They need to deploy cloud services on their chosen cloud provider and infrastructure to meet the company's security and compliance requirements. As a result, they choose EMQX Cloud BYOC.

The BYOC plan allows James to deploy EMQX Cloud on their selected cloud provider and infrastructure. This enables them to meet their unique security and compliance requirements while fully utilizing their existing cloud resources. For James, the BYOC plan is a secure and flexible solution that allows the company to confidently expand its business.

## Comparison and Selection of the Three Plans

We have summarized the costs, performance, and customization levels of each EMQX Cloud plan in the table below to help you compare them more intuitively:

|                   | **Serverless**                                               | **Dedicated**                                                | **BYOC**                                                     |
| :---------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Cost**          | Pay for actual usage, suitable for limited budget and smaller projects | Relatively higher cost but with independent deployment and professional support, suitable for projects with high performance and stability requirements | Customizable cloud provider and infrastructure, cost depends on specific circumstances, suitable for projects with special security and compliance requirements |
| **Performance**   | Automatically adjusts with business needs, suitable for small-to-medium projects, up to 1,000 concurrent connections | Independent deployment, higher performance guarantee, suitable for enterprise-level projects | Performance depends on the chosen cloud provider and infrastructure, suitable for projects with special performance requirements |
| **Customization** | Relatively low level of customization. Suitable for general use cases. Supports the standard MQTT protocol. | Highly customizable, suitable for enterprise-level projects with special requirements. | Allows choosing cloud provider and infrastructure, higher customization level, suitable for projects with special requirements |

## Conclusion

Through this article, we provide the following suggestions for choosing between the three EMQX Cloud plans:

- If you're like Michael, looking for a cost-effective and easily scalable cloud service, [the Serverless plan](https://www.emqx.com/en/cloud/serverless-mqtt) is your top choice.
- If you're like Christina, needing a high-performance, customizable cloud service to support enterprise-level projects, [the Dedicated plan](https://www.emqx.com/en/cloud/dedicated) is your ideal choice.
- Suppose you're like James, having specific data security and compliance requirements and wanting to deploy cloud services on your chosen cloud provider and infrastructure. In that case, [the BYOC plan](https://www.emqx.com/en/cloud/byoc) will meet your needs.

We hope this article helps you find the most suitable solution and efficiently carry out IoT business with EMQX Cloud.

For more information and support, please visit the [EMQX Cloud official website](https://www.emqx.com/en/cloud) or contact our technical support team. We are dedicated to providing you with the best assistance possible.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
