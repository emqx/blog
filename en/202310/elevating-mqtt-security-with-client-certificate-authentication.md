## **Introduction**

As the Internet of Things (IoT) continues to grow, so does the use of MQTT (Message Queue Telemetry Transport), a lightweight messaging protocol used for IoT applications. [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a popular protocol for IoT communication due to its simplicity, efficiency, and flexibility. However, with this popularity comes increased security risks. As the number of devices continues to grow exponentially, ensuring secure communication becomes paramount. This is where NGINX Plus and [EMQX Enterprise](https://www.emqx.com/en/products/emqx) shine, offering a robust solution for secure MQTT communications.

In this article, we will explore the security risks associated with MQTT and how mutual TLS (Transport Layer Security) and Client Certificate Authentication can be implemented to enhance its security.

## **Understanding MQTT and its Importance**

MQTT was developed in the late 1990s and has become one of the most popular protocols for IoT communication. It is a publish/subscribe messaging protocol designed to be lightweight and efficient, which is ideal for low-power devices and networks with limited bandwidth.

## **Security Risks of MQTT**

Despite its many advantages, MQTT is not devoid of vulnerabilities. Unauthorized access, data tampering, and eavesdropping are some of the glaring security threats that loom over MQTT networks. Such vulnerabilities can have dire repercussions, especially for organizations heavily reliant on MQTT. Malicious actors can exploit these weak points, gaining unauthorized access to [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and clients, tampering with transmitted data, or eavesdropping to extract valuable information.

## **A Primer on Mutual TLS**

Mutual TLS acts as the guardian of MQTT networks, offering end-to-end encryption and ensuring the authenticity of data transmission. It mandates both the client and server to present valid certificates, establishing a two-way authentication process. Once both parties are authenticated, they can initiate a secure and encrypted connection, safeguarding against unauthorized access, data breaches, and eavesdropping.

## **The Necessity of TLS Termination in MQTT**

At the heart of secure online interactions lies Transport Layer Security (TLS). It's the shield that ensures data remains encrypted and confidential during transmission. However, direct handling of TLS handshakes, encryption, and decryption by MQTT brokers can be taxing, potentially leading to performance issues. Enter NGINX Plus. By delegating these responsibilities to NGINX Plus, MQTT brokers can concentrate on their core duty: orchestrating message traffic. This delegation not only boosts performance but also streamlines the system's architecture, ensuring data flows securely and seamlessly.

## **Setting Up TLS Termination**

Before diving into the configuration, ensure you're equipped with NGINX Plus R29 or a newer version and the latest iteration of EMQX Enterprise. Start by configuring NGINX Plus for TLS termination. This involves specifying the paths for your SSL certificate and private key in the NGINX configuration. Once done, set up NGINX Plus to proxy the TLS-encrypted MQTT traffic from devices to EMQX Enterprise. For those looking to optimize performance, consider enabling SSL session caching in NGINX Plus.

Here's an example config for TLS termination in NGINX Plus:

```
stream {

  server {
    listen 8883 ssl;
    ssl_certificate /etc/nginx/certs/emqx.pem;
    ssl_certificate_key /etc/nginx/certs/emqx.key;
    ssl_client_certificate /etc/nginx/certs/ca.crt;
    ssl_session_cache shared:SSL:5m;
    ssl_verify_client on;
    proxy_pass 10.0.0.113:1883;
    proxy_connect_timeout 5s;
  }

}
```

This example enables Mutual TLS. It sets up NGINX to act as a secure proxy for MQTT traffic. Clients connecting to this server must use SSL/TLS (port 8883) and provide a valid client certificate signed by the trusted CA. NGINX will terminate the SSL/TLS connection, verify the client's certificate, and then forward the MQTT traffic to the actual MQTT broker at `10.0.0.113:1883`. This setup offloads the SSL/TLS termination and client certificate verification tasks from EMQX broker to NGINX, enhancing performance and security.

## **Elevating Security with Client Certificate Authentication**

While encryption is crucial, it's just one piece of the security puzzle. Authenticating clients—ensuring they are who they claim to be—is equally vital. Client certificate authentication offers a robust mechanism in this regard. It ensures that only authorized devices, those possessing a valid certificate issued by a trusted Certificate Authority (CA), can establish connections. Furthermore, transmitting the data embedded in a client certificate to the MQTT broker not only enhances authentication but can also pave the way for advanced authorization, elevating the security paradigm to unparalleled heights.

## **Rewriting the CONNECT Message for Enhanced Authentication**

With your client certificates ready, activate mutual TLS in NGINX Plus. This ensures a two-way street: both the server and client authenticate each other. Next, extract relevant data from the client's SSL certificate. This could be the Common Name (CN) or any other pertinent detail. Now, here's where the magic happens: use NGINX Plus to rewrite the MQTT CONNECT message's field with this extracted data from the certificate. Finally, configure EMQX Enterprise to recognize and authenticate these rewritten CONNECT messages. The result? Only legitimate devices with valid certificates can connect, ensuring an even more secure MQTT environment.

Here's an example of client certificate authentication in NGINX Plus:

```
stream {

  mqtt on;
 
  server {
    listen 8883 ssl;
    ssl_certificate /etc/nginx/certs/emqx.pem;
    ssl_certificate_key /etc/nginx/certs/emqx.key;
    ssl_client_certificate /etc/nginx/certs/ca.crt;
    ssl_session_cache shared:SSL:5m;
    ssl_verify_clienet on;

    proxy_pass 10.0.0.113:1883;
    proxy_connect_timeout 5s;

    mqtt_set_connect username $ssl_client_s_dn;
  }

}
```

 This config adds two more directives to the last example.  

1. “mqtt on”

   This directive enables MQTT protocol parsing within the stream block. This means NGINX will understand and be able to process MQTT-specific messages.

1. “mqtt_set_connect username $ssl_client_s_dn”

   This directive is used to rewrite the MQTT CONNECT message’s username field. '$ssl_client_s_dn' is a variable that contains the Subject Distinguished Name (DN) from the client's SSL certificate.

With the enhanced configuration, NGINX not only acts as a secure proxy for MQTT traffic but also parses MQTT messages. Clients connecting to this server must use SSL/TLS (port 8883) and provide a valid client certificate. NGINX will terminate the SSL/TLS connection, verify the client's certificate, and rewrite the MQTT CONNECT message's username field with the DN from the client's certificate. This allows for an additional layer of client identification and potential authorization at the EMQX broker level. The MQTT traffic is then forwarded to the actual EMQX broker at `10.0.0.113:1883`. This setup provides both enhanced security and the ability to use client certificate details for [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) identification and authentication.

## **Reaping the Benefits**

The integration of NGINX Plus and EMQX Enterprise offers a plethora of benefits. From enhanced security through robust TLS termination and client certificate authentication to offloaded encryption tasks, the synergy is evident. EMQX brokers, free from the burden of encryption, can focus solely on processing MQTT messages. The result is a scalable and flexible framework, ready to handle the demands of expansive MQTT connections.

## **Conclusion**

The world of IoT is vast and ever-evolving. As we continue to add more devices to this interconnected web, ensuring secure communications is non-negotiable. By harnessing the combined prowess of NGINX Plus and EMQX Enterprise, businesses can guarantee efficient, secure, and scalable MQTT communications, primed to cater to the demands of the modern IoT landscape.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
