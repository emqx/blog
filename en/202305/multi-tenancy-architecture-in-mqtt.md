## Introduction

In the past decade, the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) has gained significant adoption in IoT areas. A scalable, flexible MQTT service is essential for some IoT service providers. Introducing multi-tenancy architecture in MQTT offers a new choice for them.

This article will discuss the multi-tenancy architecture in MQTT and its benefits and challenges to users.


## What is Multi-Tenancy Architecture

**Multi-tenancy** is a software architecture model where a single instance of an application serves multiple tenants (users or customers), each with its isolated data and configuration. 

In this architecture, several tenants share the same infrastructure, database, and cluster, but each tenant has access only to their isolated data and configuration. This means tenants can customize the application to meet their needs without affecting other tenants' data or configurations. At the same time, the providers can save on costs by hosting multiple tenants on a single infrastructure.

When it comes to [MQTT Brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), a multi-tenancy architecture offers an efficient and cost-effective solution for delivering MQTT services to multiple customers or teams.


## Understanding Multi-Tenancy in MQTT: Data Isolation for Each Tenant

The key to a multi-tenancy architecture of MQTT Broker is data isolation. This ensures that each tenant perceives themselves as the only user of the entire cluster and cannot access or interact with clients belonging to other tenants. It includes five essential aspects as follows:

- **No additional constraints on the client.** The client can freely use the Client ID, Username, and Password in the format it wants without interference from other tenants. Even different tenants can use the same Client ID to access simultaneously.
- **Authentication/Authorization data isolation.** Each tenant maintains separate authentication and authorization data to manage client login and topic publishing/subscribing permissions. Tenants can only manage their own records, which also only affects the client of that tenant.
- **Messaging isolation.** Clients from different tenants cannot communicate with each other. While tenants can use any desired topic, including those used by other tenants, the messages remain entirely isolated.
- **Independent user interface.** This includes Management Website and HTTP API. Tenants can only manage and view their own data and cannot modify the data of other tenants.
- **Differentiated configuration.** Independent configurations should be provided for different tenants to meet their unique resource and functional requirements.


## Benefits and Challenges of Implementing Multi-Tenancy in MQTT

IoT solution providers can benefit from MQTT Multi-tenancy mainly in two aspects:

- **Flexibility:** MQTT Multi-Tenancy offers greater flexibility compared to a dedicated architecture. This is evident in two ways: Firstly, it eliminates the need for setting up separate infrastructure for each tenant, enabling quick delivery of MQTT services. Secondly, it allows for flexible pricing plans tailored to individual tenants without disrupting service or requiring the reallocation of the underlying infrastructure.
- **Cost-saving:** MQTT Multi-Tenancy is a cost-effective alternative to dedicated architecture, enabling multiple tenants to share the same infrastructure. In contrast, dedicated architecture requires each tenant to have their own infrastructure, which can be costly both in terms of setup and maintenance.

At the same time, there are also some challenges to overcome:

- **Ensuring correct tenant data isolation.** Under any circumstances, a tenant can never access or manage the devices and data of any other tenant. Therefore, strict security measures must be implemented, including rigorous access control policies, proper authentication and authorization mechanisms, and role-based access control. Data encryption can also be used to ensure that data is protected in transit.
- **Effective management of resource competition.** Since multiple tenants share the same infrastructure, such as network bandwidth, CPU or memory on the same machine, resource competition among tenants is inevitable. The key is that the system must be able to limit a tenant's resource usage to avoid some resources being exhausted. Usually, we can set quota and rate limit policies for each tenant to regulate resource consumptions. For example, tenants can have maximum connection and subscription limits, as well as restrictions on message rates. Once the limit is reached, services can be declined to prevent excessive resource consumption by a tenant.


## EMQX Cloud Serverless: MQTT Service Based on Multi-Tenancy Architecture

EMQ has launched its serverless MQTT service based on innovative multi-tenant technology, the [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt). EMQX Cloud Serverless provides users with the blazing-fast deployment of MQTT services in just 5 seconds **without concerns about server infrastructure management or resource allocation when service scales**. It also offers a **forever free 1M session minutes/month**, minimizing IoT costs with the pay-as-you-go model.


## Conclusion

With the continuous burst of IoT devices and application scenarios, MQTT multi-tenancy has brilliant prospects in the future IoT market. Adopting this architecture allows enterprises to provide customers with more flexible MQTT Broker services, as well as reduce operating costs for them under large-scale deployment.



<section class="promotion">
    <div>
        Try EMQX Cloud Serverless
        <div class="is-size-14 is-text-normal has-text-weight-normal">Forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
