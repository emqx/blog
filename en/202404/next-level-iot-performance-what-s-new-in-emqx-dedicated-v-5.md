## Introduction

[EMQX Dedicated](https://www.emqx.com/en/cloud/dedicated), renowned for hosting MQTT clusters in an exclusive cloud environment, remains a cornerstone among EMQX's suite of products. It’s our pleasure to announce an upgrade to the latest version of EMQX Dedicated, introducing a wide array of new features and capabilities designed to support mission-critical IoT applications across various industries.

In this article, we will explore the notable improvements brought by version 5 (v5), comparing it with its predecessor, version 4 (v4).

## Significant Enhancements in EMQX Dedicated v5 Upgrade

### 1. The Dedicated v5 Difference: Enhancing Metrics and Observability

The upgraded monitoring system provides a comprehensive and sophisticated display of metrics, offering deeper insights into client connections, authentication, authorization, and data integration metrics.

**Client Metrics:**

The Dedicated v5 console organizes a wide array of metrics under categories such as Messages, Packets, and Bytes for each client connected to the service. This detailed segmentation facilitates in-depth analysis of client activities, presenting all relevant metrics in an intuitive chart format below.

![Client Metrics](https://assets.emqx.com/images/4a285afd04d6a269d91ff4a10ec88731.png)

**Authentication / Authorization Metrics:**

With EMQX Dedicated v5, we introduce detailed metrics that shed light on authentication and authorization processes, helping identify potential issues early on. The incorporation of new APIs for authentication enhances the management of authentication processes seamlessly and effectively, making them more seamless and effective.

![Authentication / Authorization Metrics](https://assets.emqx.com/images/b7271e54d07eaf6739697d084b327aaf.png)

**Data Integration Metrics:**

Previously, v4 offered limited metrics, providing little information for troubleshooting. V5 significantly expands the range of metrics related to rules and actions, broadening the scope of observable aspects and ensuring a comprehensive understanding of data processing activities.

![Data Integration Metrics](https://assets.emqx.com/images/4ba6e9b54cc64f0c1e90031fb12b6262.png)

### 2. New Features: Usability Enhancements

**Retained Messages Management:**

V5 introduces an advanced retained message management system in the console, a significant step up from v4, which only displayed the number of retained messages. This new system allows for detailed views of message topics, QoS, publish times, and payloads, offering options to delete individual messages or clear all retained messages simultaneously. This method offers a distinct improvement over the previous practice of sending empty messages to topics for removal.

![Retained Messages Management](https://assets.emqx.com/images/a485b732989ad66fae4ac3720c3b34ce.png) 

**Authentication / Authorization Data Source Sorting:**

V5 enables the configuration and sorting of extended authentication/authorization data sources, including the default ones. Users can now easily adjust the execution order of the authentication chain through a simple drag-and-drop interface, providing a clear and intuitive visualization of the authentication logic.

![Authentication / Authorization Data Source Sorting](https://assets.emqx.com/images/c443f9621c940bc9a7c1a550d8e2dc02.png)

### 3. Advanced Features: Delving into High-level Capabilities in v5 Dedicated

**MQTT over QUIC:**

Leveraging QUIC, the transport protocol underpinning the next-generation Internet protocol HTTP/3, v5 offers enhanced connectivity for the modern mobile Internet. This technology reduces connection overhead and message latency when compared to traditional TCP/TLS protocols, positioning EMQX Dedicated as a pioneer in utilizing this cutting-edge technology for MQTT communication.

**CRL (Certificate Revocation List):**

CRL is a list maintained by Certificate Authorities (CA), detailing revoked certificates with their serial numbers and revocation dates. With this feature, EMQX Dedicated checks during the SSL/TLS handshake phase if a client’s certificate has been revoked, ensuring secure connections.

**OCSP (Online Certificate Status Protocol) Stapling:**

This method offers another layer of certificate revocation checking. After enabling OCSP Stapling, EMQX Dedicated queries the OCSP server for certificate statuses and caches the results. During an SSL handshake, EMQX presents the OCSP data along with the certificate chain to the client for verification.

## Creating a v5 Dedicated Deployment

Setting up a v5 Dedicated deployment remains as straightforward as before. Simply log into the EMQX Platform Console, select your cloud provider and region, choose a suitable tier, and opt for v5 in the version selection – the default option. Follow our step-by-step instructions to finalize the deployment.

![Creating a v5 Dedicated Deployment](https://assets.emqx.com/images/2798ae11e25e0aee1aefcb21cba394da.png)

For those on v4 Dedicated deployments, EMQX offers tailored upgrade solutions. To begin the upgrade process, please contact our support team for detailed guidance and support to ensure a smooth transition to the latest version.

## Conclusion

With unmatched performance, enhanced monitoring metrics, and innovative features like MQTT over QUIC, EMQX Dedicated v5 establishes itself as the premier MQTT platform for innovation.

Elevate your IoT solutions with the power of EMQX Dedicated v5 and unlock the full potential of your IoT data management today.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
