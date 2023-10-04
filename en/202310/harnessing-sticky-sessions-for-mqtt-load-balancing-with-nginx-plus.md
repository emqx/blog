## **Introduction**

In the rapidly evolving world of the Internet of Things (IoT), the ability to communicate efficiently between devices is of utmost importance. [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) stands out as a leading protocol for lightweight message exchange in this arena. Yet, as deployments expand, managing these communications becomes increasingly intricate. This is where the synergy between [NGINX Plus](https://www.nginx.com/products/nginx/) and [EMQX Enterprise](https://www.emqx.com/en/products/emqx) shines, offering a streamlined approach to optimize MQTT traffic and guarantee consistent client-broker connections. 

Sticky sessions play a pivotal role in IoT load balancing, ensuring that a client's subsequent connections are routed to the same server - a must for applications needing session persistence. This post delves into harnessing NGINX Plus and EMQX to achieve sticky sessions, spotlighting 'Client ID' as the linchpin.

## **MQTT Essentials and the Need for Load Balancing**

MQTT, or Message Queuing Telemetry Transport, operates fundamentally as a publish-subscribe messaging protocol. Crafted for environments with low bandwidth, high latency, or unreliable networks, it's an ideal fit for IoT devices. However, as the device count escalates in an MQTT ecosystem, traffic can swiftly become a choke point, ushering in inefficiencies and potential data loss scenarios. This underscores the necessity for load balancing, a mechanism to evenly distribute incoming MQTT traffic across multiple brokers, ensuring no single entity bears the brunt of the load.

Load balancing strategies are pivotal in ensuring the smooth distribution of MQTT traffic, and different strategies cater to varying deployment needs. The round-robin approach, for instance, cyclically assigns incoming connections to brokers in the cluster, ensuring equitable distribution. Conversely, the Least Connections method funnels traffic to the least occupied broker, a strategy that shines when brokers have disparate capacities. IP Hashing, on the other hand, uses the client's IP as a determinant for broker connection, ensuring a stable connection point. Today, we spotlight a novel strategy that leverages the 'Client Id'. This approach guarantees that a client invariably connects to the same broker, streamlining data flow and minimizing connection overhead.

## **A Glimpse into NGINX Plus's MQTT Capabilities**

With the advent of its R29 release, NGINX Plus ushered in native support for MQTT message parsing. This isn't just a superficial feature; it's a transformative capability. It allows for the creation of sticky sessions, a mechanism where clients maintain a consistent connection to the same broker, thus optimizing the flow of data and reducing the overhead of establishing new connections.

## **EMQX Enterprise: More Than Just an MQTT Broker**

While there are several [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) available, EMQX Enterprise distinguishes itself with its robustness and enterprise-focused features. Built for scalability, it can handle millions of simultaneous [MQTT connections](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection), making it an ideal choice for large-scale IoT deployments. Its compatibility with NGINX Plus further amplifies its capabilities, offering a seamless experience for users.

## **Crafting Sticky Sessions with NGINX Plus and EMQX Enterprise**

### **Prerequisites**

- Equip yourself with NGINX Plus R29 or newer and the latest iteration of EMQX Enterprise. For this walkthrough, we've deployed a cluster comprising two EMQX Enterprise v5.2.0 instances.
- Acquaint yourself with foundational MQTT concepts and terminologies.

### **Architecture**

The architectural blueprint for integrating EMQX with NGINX Plus, emphasizing sticky sessions using 'Client ID', is illustrated below:

![The architectural blueprint for integrating EMQX with NGINX Plus](https://assets.emqx.com/images/0da1203e7cbeba3a54e6dc63dae4cb29.png)

In this setup, the client forwards a connection request to NGINX Plus, which subsequently proxies the request to an appropriate EMQX server, determined by the client's 'Client ID'. This ensures that subsequent client connection requests are consistently routed to the same server, fortifying session persistence.

### **Configuring NGINX Plus**

- Activate MQTT parsing via the `mqtt_preread` directive.
- Extract essential fields from CONNECT messages, a pivotal step for crafting sticky sessions.
- Establishing Sticky Sessions: The linchpin of this setup is the client identifier, which, when used as a hash key in the NGINX configuration, ensures clients consistently connect to a designated EMQX Enterprise broker.

Here's an in-depth configuration snippet:

```
stream {
    mqtt_preread on;
    upstream emqx_backend {
        zone tcp_servers 64k;
        hash $mqtt_preread_clientid consistent;
        server 10.0.0.172:1883;
        server 10.0.0.174:1883;
    }
    server {
        listen 1880;
        status_zone tcp_server;
        proxy_pass emqx_backend;
        proxy_buffer_size 4k;
        proxy_protocol on;
    }
}
```

In this example, we have defined an upstream group called 'emqx_backend' that includes two EMQX servers. We have also specified that the sticky session should be based on the ' mqtt_preread_clientid' variable, which is the client identifier used by the MQTT protocol. Finally, we configure NGINX to listen on port 1880 and proxy requests to the 'emqx_backend' group.

This configuration ensures clients with identical IDs are invariably routed to the same broker, actualizing the sticky session paradigm. 

After configuration, a 'reload' or 'restart' of NGINX Plus is required.

### **Configuring EMQX Enterprise**

To tailor EMQX for the NGINX proxy, activate the ‘proxy_protocol’ in the configuration file.

```
listeners.tcp.default {
  bind = "0.0.0.0:1883"
  proxy_protocol = true
}
```

Alternatively, activate it via the EMQX Dashboard.

![EMQX Dashboard](https://assets.emqx.com/images/3ee65cbaeaa98cfbee7f6c3dd9fc8414.png)

## **Verifying Your Configuration**

Post-configuration, it's crucial to validate the setup. To test the effectiveness of our sticky session configuration, we need [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) like [MQTTX](https://mqttx.app/) or Mosquitto client to simulate clients connecting to our EMQX cluster. We can monitor the connections on the EMQX Dashboard. If the sticky session configuration is correct, clients with the same client ID should consistently connect to the same EMQX broker. 

In this demo, we use [MQTTX](https://mqttx.app/) to act as the MQTT client.

![MQTTX](https://assets.emqx.com/images/2ab67a5d16fd8f0a04f7c2a05e6c471e.png)

We created a client with ‘mqttx_client1’ as the Client ID. On EMQX dashboard, you can go to ‘Clients’ page to view the clients connected to EMQX Cluster:

![View the clients connected to EMQX Cluster](https://assets.emqx.com/images/db452c6384345ef159b1d915bf7e03fd.png)

You can see the mqttx_client1 is connected to the EMQX cluster. Click the id and check the connection details.

![Connection details](https://assets.emqx.com/images/ceb64cf892f8c0db4de5187ac5e1eacb.png)

In this demo, ‘mqttx_client1’ is connected to the node ‘emqx_node1’. Disconnect and reconnect the client, and you will see the client with the same id will connect to this broker consistently.

## **Benefits of Using 'Client ID' as the Magic Key**

Using the 'Client ID' as the magic key for sticky sessions has several benefits. 

- First, it ensures that subsequent connections from a client are directed to the same server, even if the client reconnects with a different IP address or port number. 
- Second, it allows us to scale our application horizontally by adding more EMQX servers to the backend group without losing session persistence. 
- Finally, it provides a simple and efficient mechanism for load-balancing MQTT traffic.

## **Conclusion**

Implementing sticky sessions with NGINX Plus and 'Client ID' as the magic key is an effective way to achieve both scalability and session persistence in IoT applications. By using this configuration, we can ensure that subsequent connections from a client are directed to the same server, even if the client reconnects with a different IP address or port number.  The combination of NGINX Plus and EMQX Enterprise offers a robust solution for managing MQTT traffic in large-scale IoT deployments. By implementing sticky sessions, businesses can ensure efficient, reliable, and scalable MQTT communications, ready to meet the demands of the modern IoT landscape.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
