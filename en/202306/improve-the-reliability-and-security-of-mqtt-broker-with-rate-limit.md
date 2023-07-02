## Introduction

Rate limit generally refers to restricting data transfer rates within a network during a given period, ensuring network traffic remains within acceptable limits. This can prevent congestion and overload at the receiver side, avoiding effects on its stability and reliability.

This blog will look at another benefit of rate limit: how it can enhance the security of IoT platforms and applications.

## How Does Rate Limit Secure the System?

Rate limit typically involves managing the regular traffic within a network, which originates from legitimate access and varies based on user behavior. For example, during a user's waking hours, the system experiences increased incoming traffic, decreasing when the user is inactive. In this blog post, we will explore the impact of rate limits on mitigating **malicious traffic**.

While we might employ authentication and authorization services to minimize the risk of malicious attacks on our system, we must also acknowledge the possibility of user accounts being hacked or stolen. Without a rate limit policy, an attacker could exploit a compromised account to flood our system with malicious traffic, resulting in an excessive system load. During peak traffic periods, this overloading could potentially impair the system's ability to deliver fast and reliable services to legitimate users.

However, with an appropriate rate limit policy, even an attacker possessing a compromised account would only be able to access the system in a limited manner, ensuring that they cannot generate more traffic than the system can handle.

## Common Rate Limit Policies in MQTT

### Limit the Rate and Number of Client Connections

When a client establishes a connection, the server undertakes various tasks, including creating a new thread and registering the Client ID. If authentication services are enabled, each connection request triggers a server-side authentication process. This process may entail database lookups and CPU-intensive hash calculations, especially when employing more secure hash algorithms.

As a result, restricting the maximum connection rate of clients effectively prevents attackers from exhausting server resources by initiating a large number of connections within a short period of time.

Furthermore, maintaining connections on the server side incurs resource consumption in terms of CPU, memory, and other resources. Attackers can exploit this by attempting to establish a significant number of idle connections with the server, thereby disrupting its regular operations. Hence, it becomes imperative for the server to enforce limitations on the maximum number of connections.

A configuration example in EMQX:

```
listeners.tcp.default {
  max_connections = 1024000
  max_conn_rate = 1000
}
```

### Limit the Publish Rate or Set Quota

We need to restrict the publishing rate of individual clients by setting limits on the maximum number of messages they can publish per second or the total message size they can publish per second. The latter prevents attackers from quickly depleting server resources by flooding the system with a small number of large messages. Additionally, combined with permission management mechanisms, different rate limits can be assigned to clients based on their permission levels.

Another approach to governing client behavior is by setting quotas. For instance, a client may be allowed to send up to 100 messages per second but is subject to a daily limit of 5000 messages. Once the limit is reached, the client must wait until the next day to send additional messages.

To avoid the excessive use of system resources by different [QoS in MQTT](https://www.emqx.com/en/blog/introduction-to-mqtt-qos), we can limit the number of messages based on their QoS. For example, a client can only send 100 QoS 0 messages per second, but only 50 QoS 1 and 2 messages per second. This can stop attackers from exploiting higher QoS to drain the resources of the server quickly.

A configuration example in EMQX:

```
listeners.tcp.default {
  messages_rate = "1000/s"
  bytes_rate = "100KB/s"
}
```

### Limit the Subscription Rate of Clients

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) allows clients to subscribe to topics without prior registration. Instead, this step is deferred until the client establishes a connection with the server. When a client initiates a new subscription, the server must perform tasks such as updating the routing table. An attacker can exploit this by making the client subscribe to many topics in a short time, which can overload the server with writing operations and disrupt its normal service. To prevent this, we can set a limit on how many subscriptions a single client can make per second.

## Prevent Abnormal Behavior

The aforementioned attacks involve an attacker masquerading as a legitimate user and initiating malicious requests. However, there are instances where an attacker can disrupt our service without sending valid requests. For example, an attacker may attempt to publish messages to unauthorized topics. Even though the server does not relay these messages, the attacker can exploit this situation to consume the server's computational resources during the privilege verification process.

This type of attack is commonly called a DOS attack or DDOS attack. In MQTT, an attacker might employ a similar strategy by continuously establishing connections and initiating authentication requests. Although the attacker will eventually be thwarted by the maximum connection rate limit, this can still hinder other legitimate clients from establishing connections.

Therefore, the server needs to identify and respond to these potential security threats promptly. One common strategy involves maintaining a blacklist that includes the IP addresses or Client IDs associated with clients exhibiting abnormal behavior, effectively blocking their access.

## Conclusion

Rate limit can prevent attackers from maliciously consuming server resources and affecting service reliability by restricting and balancing traffic. It can also handle traffic fluctuations caused by normal business changes. However, some attacks do not require the attacker to send valid requests, which may bypass the rate limit. Therefore, the server side also needs to identify these potential security threats.

[EMQX](https://www.emqx.io/) is a widely used [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) offering high scalability and availability while prioritizing user security. In EMQX, you can easily set different rate limits for each listener and add the specified Client ID or IP to the backlist. For more information, please visit the [Rate Limit](https://www.emqx.io/docs/zh/v5.0/rate-limit/rate-limit.html) and [Blacklist](https://www.emqx.io/docs/zh/v5.0/access-control/blacklist.html) feature documentation of EMQX.





<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
