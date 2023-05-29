## Introduction

[EMQX Cloud](https://www.emqx.com/en/cloud) provides a fully managed MQTT service that facilitates infrastructure management for IoT solution providers.

In the latest version, we are thrilled to introduce an array of enhanced MQTT monitor metrics. These metrics are designed to elevate observability and empower you with deeper insights into your MQTT deployments. This blog post will explore the new MQTT monitor metrics and the other update in EMQX Cloud.

## New MQTT Monitor Metrics

The latest release of EMQX Cloud introduces exciting enhancements that further strengthen our MQTT monitoring capabilities. Alongside existing metrics, the focus of this release is to provide a more comprehensive view of your MQTT deployments. This will enable you to make informed decisions and optimize your system's performance. 

There are three new metrics:

- **MQTT Retained Message Metrics**: [MQTT retained message](https://www.emqx.com/en/blog/mqtt5-features-retain-message) is the message with the retained flag set to true. The broker stores the last retained message and the corresponding QoS for that topic. You can dive into the MQTT monitoring dashboard to analyze the retained message volume and identify anomalies. These metrics empower you to understand message persistence better and take proactive steps to ensure reliable message delivery.
- **Shared Subscription Metrics**: Shared subscriptions are a powerful feature in MQTT, enabling efficient message distribution across multiple subscribers. You can monitor the performance and usage of shared subscriptions with metrics such as subscription count. Leverage these insights to optimize shared subscription configurations, balance message load, and enhance the overall efficiency of your MQTT deployments.
- **Total TPS (Transactions Per Second) Metrics**: Monitoring the throughput of your MQTT traffic is vital for maintaining optimal performance. With the addition of Total TPS metrics, you gain visibility into the volume of transactions processed per second. Analyze message rates, identify peak periods, and assess the impact of your system's scaling. These metrics allow you to review your EMQX Cloud instance specification, ensuring it can handle the desired load and deliver messages promptly.

![EMQX Cloud New MQTT Monitor Metrics](https://assets.emqx.com/images/b8e98c38bc122465e57f745b5d1f92d7.png)

## Conclusion

The enhanced monitor metrics that EMQX Cloud newly introduces take its observability to new heights. With the MQTT retained message, shared subscription, and total TPS metrics, you can gain deeper insights into your EMQX Cloud deployments, optimize performance, and ensure seamless message delivery. Leverage these powerful tools and unlock the full potential of your EMQX Cloud instances today! 



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
