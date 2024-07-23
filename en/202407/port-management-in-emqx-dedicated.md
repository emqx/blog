## Introduction

The EMQX Console offers comprehensive port management capabilities specifically designed for EMQX Dedicated deployments, allowing users to directly control the accessibility of each port. This article explores various port configurations and management scenarios to provide a thorough understanding of this feature.

## Understanding Ports and Protocols in EMQX Dedicated

- **1883 Port: MQTT over TCP** 

  MQTT over TCP uses the lightweight MQTT protocol over a TCP connection, designed for efficient communication in various network conditions.

- **8883 Port: MQTT over TLS/SSL**

  [MQTT over TLS/SSL](https://www.emqx.com/en/blog/fortifying-mqtt-communication-security-with-ssl-tls) encrypts MQTT communication, ensuring confidentiality, data integrity, and authentication of client and broker identities to prevent security threats.

- **8083 Port: MQTT over WebSocket** 

  [MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket) allows MQTT communication over a WebSocket connection, simplifying bi-directional data exchange, especially useful in browser environments.

- **8084 Port: WebSocket over TLS/SSL (WSS)** 

  WebSocket over TLS/SSL provides secure, real-time communication channels over a single TCP connection, ensuring privacy and data integrity. It is commonly used for MQTT in browser-based applications.

## Significance of Port Management in EMQX Dedicated

Effective port management is crucial for securing network connections and maintaining data integrity. We strongly advocate using ports secured with TLS/SSL for accessing deployments. MQTT over TLS provides essential security benefits: encrypting data to ensure confidentiality, preventing tampering to maintain data integrity, and authenticating client and broker identities to thwart man-in-the-middle attacks.

For enhanced security, we advise disabling non-encrypted ports as a precaution against potential attacks from unauthorized clients. These ports can be re-enabled as needed for deployment or testing purposes, providing flexibility while safeguarding network integrity.

## Effectively Managing Ports in EMQX Dedicated

In the EMQX Console's Dedicated deployment overview page, navigate to the **Connection Information** section to manage accessibility settings for each port.

![Port management 1](https://assets.emqx.com/images/ea5d2a1f663f4970c781b1fb376d2453.png)

![Port management 2](https://assets.emqx.com/images/8af59390a4c1c278fd2c6015a24cf287.png)

## Wrap-Up

The EMQX Console provides robust port management capabilities tailored for EMQX Dedicated deployments, enabling users to directly control port accessibility. Effective port management is crucial for network security and data integrity, emphasizing the use of TLS/SSL to protect deployments. Disabling non-encrypted ports mitigates potential security risks, offering flexibility for deployment and testing while upholding network integrity.

 

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
