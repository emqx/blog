## Introduction

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) (Message Queuing Telemetry Transport) is a popular lightweight publish-subscribe messaging protocol, ideal for connecting Internet of Things (IoT) or machine-to-machine (M2M) devices and applications over the Internet. [NGINX Plus](https://www.nginx.com/products/nginx/) and [EMQX Enterprise](https://www.emqx.com/en/products/emqx) are two powerful tools that can help optimize and secure your MQTT-based applications.

In this blog, we will discuss how to use the Client ID Substitution feature of NGINX Plus with EMQX Enterprise. 

## Overview of NGINX Plus and EMQX Enterprise

NGINX Plus is a software load balancer, reverse proxy, web server, and content cache built on top of the open-source NGINX project. It offers features such as load balancing, session persistence, SSL/TLS termination, and client certificate authentication. One of its new features released in NGINX Plus R29 is the ability to parse and rewrite portions of MQTT CONNECT messages, which enables the Client ID Substitution feature.

EMQX Enterprise is a scalable and reliable MQTT messaging platform that can be used to connect, move, and process data in business-critical scenarios for the IoT era. It is an all-in-one distributed [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) with multiple protocol gateways and a powerful built-in SQL-based IoT rule engine.

## What is Client ID Substitution?

Client ID substitution is a technique that allows [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) to connect to an MQTT broker using a substitute client ID. This substitute client ID is used instead of the original client ID provided by the client. The substitute client ID is created by the NGINX Plus and is used to identify the client in subsequent messages.

## The Need for Client ID Substitution

Security is of utmost importance in MQTT communications. Devices often send sensitive data such as serial numbers as part of an MQTT CONNECT message. Storing client-identifiable information in the MQTT broker’s database can pose security risks. Client ID Substitution is a feature that allows us to replace a device’s identifier with other values set in the NGINX Plus config.

## Configuring NGINX Plus and EMQX for Client ID Substitution

To configure NGINX Plus for Client ID Substitution, you need to modify the NGINX configuration file. Here is an example configuration: 

```
stream {
    mqtt on;

    server {
        listen 2883 ssl;
        ssl_certificate /etc/nginx/certs/emqx.pem;
        ssl_certificate_key /etc/nginx/certs/emqx.key;
        ssl_client_certificate /etc/nginx/certs/ca.crt;      
        ssl_session_cache shared:SSL:10m;
        ssl_verify_client on;
        proxy_pass 10.0.0.113:1883;
        proxy_connect_timeout 1s;  

        mqtt_set_connect clientid $ssl_client_serial;
    }
}
```

In this example, we extract a unique identifier from a device’s client SSL certificate and use it to mask its MQTT client ID. Client certificate authentication (mutual TLS) is controlled with the ‘ssl_verify_client’ directive. When set to the ‘on’ parameter, NGINX ensures that client certificates are signed by a trusted Certificate Authority (CA). The list of trusted CA certificates is defined by the ssl_client_certificate directive.

After setting the config, a ‘reload’ or ‘restart’ is needed for the NGINX Plus service.

To configure EMQX for NGINX proxy, you will need to enable ‘proxy_protocol’ in the configuration file:

```
listeners.tcp.default {
  bind = "0.0.0.0:1883"
  proxy_protocol = true
}
```

Or you can enable it on the EMQX Dashboard:

![EMQX Dashboard](https://assets.emqx.com/images/2586cec680dc612980a44c2552ca5b88.png)

In this example, we configure EMQX Enterprise to accept connections on port `1883`. We also enabled Proxy Protocol.

## Testing the Configuration

To test the configuration, you can use an MQTT client to connect to the NGINX Plus proxy and send an MQTT CONNECT message. You can then check the client connection on the EMQX Enterprise Dashboard to ensure that the Client ID Substitution is working as expected.

In this blog, we use [MQTTX](https://mqttx.app/) to verify the Client ID Substitution. 

![MQTTX](https://assets.emqx.com/images/ee021fe6efcc4b3a7ae40ef16866b703.png)

In the example, we use `client123` as the Client ID for the connection.

![EMQX Dashboard](https://assets.emqx.com/images/0ac36427aec829668029f75ad0cafefa.png)

After connecting to EMQX Enterprise, you can go to the ‘Client’ page to verify the ID substitution.

## Conclusion

In this blog post, we discussed the importance of security in MQTT communications and how the Client ID Substitution feature of NGINX Plus can help secure your MQTT-based applications. We also provided a guide on configuring NGINX Plus and EMQX Enterprise for Client ID Substitution and verifying it with MQTTX.

We hope you found this blog post helpful. If you are ready to have a try, download EMQX Enterprise here today.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
