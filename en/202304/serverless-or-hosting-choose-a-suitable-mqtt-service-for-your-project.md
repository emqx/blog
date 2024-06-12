## Introduction

Suppose you are involved in planning, developing, or managing an IoT application that uses MQTT protocol on the public cloud. In that case, you need to consider the best option for your specific use case and requirements. Serverless and Hosting MQTT services are two typical cloud-based MQTT services. Both provide a managed MQTT Broker but differ in their architecture, scalability, security, pricing models, data integration, and so on.

In this article, we will compare these two services based on the above aspects to help you determine which service best fits your project.

## What are Hosting and Serverless MQTT services?

In a Hosting architecture, the MQTT broker is hosted on dedicated servers and cloud infrastructure resources that the service provider provides, configures, and manages. The user is responsible for ensuring that the selected service specification has sufficient capacity to handle the expected traffic and needs to adjust the service specification for scaling up or down as needed.

On the other hand, a Serverless architecture provides the MQTT broker service through multi-tenant shared clusters. The user does not need to manage any infrastructure or worry about scaling up or down as traffic changes. The service provider automatically manages the infrastructure required to run the broker and scales it up or down based on demand.

<section class="promotion">
    <div>
        Try EMQ’s Serverless MQTT Service
        <div class="is-size-14 is-text-normal has-text-weight-normal">Get forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

In summary, **the key difference between Hosting and Serverless architecture is that Hosting requires the user to be aware of the underlying usage, while Serverless does not.**

## How to choose the right MQTT service for your IoT project?

We will provide a comprehensive comparison of these two options based on the following perspectives:

### Scalability

[Serverless MQTT service](https://www.emqx.com/en/cloud/serverless-mqtt) is designed to scale automatically based on demand. It can automatically allocate infrastructure resources based on usage, and releases them when they are no longer required.

In contrast, Hosting MQTT services typically require manual scaling, meaning that the user needs to manually select a suitable specification with specific servers and network capacity to handle different traffic. The user must also monitor the traffic and predict when additional resources will be needed to avoid performance degradation or service interruption.

Therefore, **Serverless MQTT is a better option for applications with frequent connectivity changes and varying traffic demands.**

### Security

From an architectural perspective, Hosting services are based on a dedicated environment for each deployment. This dedicated environment provides better environmental and data isolation capabilities than the shared cluster architecture used in Serverless services. As a result, **Hosting services can provide more secure services, making them better suited for critical applications that require high levels of security and data privacy.**

From a functional perspective, Serverless and Hosting services offer [secure MQTT](https://www.emqx.com/en/blog/essential-things-to-know-about-mqtt-security) communication with TLS encryption, basic authentication, and ACL features. Due to their independent deployment architecture, hosting services are better equipped to provide advanced authentication and ACL functions, such as custom TLS certificates, external Auth & ACL, etc. **If you require greater security features and customized policies, a Hosting service is also a better choice.**

### Integration

Hosting services typically offer more flexibility and customization options for data integration compared to serverless services. This is because the user has more control over the underlying infrastructure and can implement custom data integration processes. 

<section class="promotion">
    <div>
        Integrate your data with Redis, MySQL, Kafka, or 3rd party database services smoothly.
    </div>
    <a href="https://docs.emqx.com/en/cloud/latest/rule_engine/introduction.html" class="button is-gradient px-5">Learn More →</a>
</section>

Serverless services usually provide a more limited set of data integration features. Serverless services typically provide basic MQTT subscription and HTTP API, allowing users to integrate data with other applications and services.

### Pricing

Hosting MQTT service uses a subscription-based pricing model. Users pay a fee based on their needed resources, such as server instances, storage, bandwidth, and other features like support and maintenance. The subscription cost varies depending on the resources required, the number of clients or connections, and included features.

In contrast, MQTT Serverless services typically offer a pay-as-you-go pricing model, where the user is charged based on the actual usage of the service, such as the number of messages sent, the duration of connections, and other usage metrics. 

MQTT Hosting generally **suits consistent traffic with predictable pricing, while MQTT Serverless accommodates variable traffic with flexible pricing.**

> See an example here to better understand the pricing of both services.
>
> [EMQX Cloud – Plans & Pricing](https://www.emqx.com/en/cloud/pricing)

## Conclusion

Serverless is a more cost-effective and scalable option for smaller-scale IoT projects. Hosting provides more granular security control and more flexibility in data integration, which is a better option for larger-scale projects that require more control over the infrastructure and configuration. Choosing between the two editions will ultimately depend on your specific needs and budget.

As a fully-managed MQTT cloud service trusted by hundreds of customers worldwide, [EMQX Cloud](https://www.emqx.com/en/cloud) offers both Serverless and Hosting MQTT services to meet the specific needs of various users. Learn more [here ](https://www.emqx.com/en/cloud/pricing)or [consult our experts](https://www.emqx.com/en/contact?product=cloud) to find the best solution for your project.

> See [a comprehensive comparison of EMQX Cloud Serverless, Dedicated, and BYOC Plans](https://www.emqx.com/en/blog/a-comprehensive-guide-to-emqx-cloud-serverless-dedicated-and-byoc-plans).


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
