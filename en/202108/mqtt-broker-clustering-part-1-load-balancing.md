This post gives a quick introduction for MQTT message broking, the challenges of clustering, and then load balancing.


## MQTT the protocol

Maybe you are not that familiar with MQTT protocol, you probably know HTTP protocol very well. Like HTTP, MQTT works at the same network (transport) layer TCP/TLS (well, it can actually work on top of HTTP, but that’s a topic for another day).

Here is the quote from [https://mqtt.org/](https://mqtt.org/) 

> MQTT is an OASIS standard messaging protocol for the Internet of Things (IoT). It is designed as an extremely lightweight publish/subscribe messaging transport that is ideal for connecting remote devices with a small code footprint and minimal network bandwidth. MQTT today is used in a wide variety of industries, such as automotive, manufacturing, telecommunications, oil and gas, etc.

[MQTT clients](https://www.emqx.com/en/blog/introduction-to-the-commonly-used-mqtt-client-library) are also similar to HTTP clients: they establish TCP connections to a server and send and receive data. The difference is that HTTP uses a request/response model, while MQTT uses a publish/subscribe model.

A real life example: a temperature sensor in the living room periodically publishes its readings to an [MQTT broker](https://www.emqx.io), a smart-home application may subscribe to the temperature readings and make smart-home decisions for you. For example: turn on the AC when it’s above 32 celsius degrees.



## The scalability challenges

A temperature sensor at home is only an example close enough to everybody. To serve smart home devices, a single MQTT broker, e.g. EMQ X edge edition running on a Raspberry PI should be more than enough, not to mention that a single EMQ X node can handle up to 2 million connections.

Now imagine these examples: millions of cars all over the world; millions of street lights all over the country; and so on and so on, the amount of devices (MQTT clients) and data volume can be a very large scale, large enough to overwhelm any single MQTT broker can handle. 

This is one of the reasons why we need to create a cluster of MQTT brokers. But it also creates more challenges such as:

- MQTT broker discovery: how should clients know which broker endpoint to connect;
- MQTT subscriber session takeover in case a client disconnect from one node and reconnect to another;
- Global routing table has to be consistently shared across all nodes in the cluster

The first two challenges can be well addressed by putting a load balancer in front of the cluster.



## MQTT load balancing

![MQTT load balancing](https://static.emqx.net/images/017284bd21723e22993d75f2305jjsjajs.png)

<p align="center">MQTT load balancing</p>


To meet the above challenges, a load balancer should be able to help clients to decide which broker to connect based on configured balancing strategies. The primary functions of a load balancer for MQTT broker cluster are:

- Broker endpoint discovery. The clients only need to care about the address of the load balancer, but not the individual brokers. This also creates flexibility for brokers to relocate, scale up or down.
- TLS termination. Many MQTT broker users choose to terminate TLS in the LB, so the resources in brokers can be well dedicated for message processing.
- Evenly distribute the load among the brokers. Load balancers are typically configurable for balancing strategies, such as random, round-robin (which has various weighted versions), and most interestingly: sticky dispatch.

Since MQTT is a protocol on top of TCP/IP, load balancing can be done at the transport layer. As a matter of fact, unlike many different choices we have when it comes to HTTP, most of the load-balancing products today (Aug. 2021) are still working at the transport layer. For instance, AWS NLB, Nginx and HAProxy.

In additional to transport layer load-balancing, HAProxy 2.4 and NGINX plus and also provide application level MQTT load-balancing.

NGINX Plus is an application delivery platform built on NGINX, an open-source web server and reverse proxy for high-traffic sites. [This article ](https://www.nginx.com/blog/nginx-plus-iot-load-balancing-mqtt/)from Nginx Plus gives a nice introduction to its MQTT load balancing solution.

Equally excellent as NGINX, HAProxy is a free, open source software that provides a high availability load balancer and proxy server for TCP and HTTP-based applications, (and now MQTT too). As of August 2021, HAProxy is the only free load-balancer which has MQTT protocol awareness. There is a brief introduction to the feature in their [release note](https://www.haproxy.com/blog/announcing-haproxy-2-4/). 

In the next post of “MQTT broker clustering” series, we will use HAProxy 2.4 + EMQ X 4.3 to demonstrate a full provisioning in more details.

## Other articles in this series

- [MQTT broker clustering part 2: Sticky session load balancing](https://www.emqx.com/en/blog/mqtt-broker-clustering-part-2-sticky-session-load-balancing)
- [MQTT broker clustering part 3: Challenges and Solutions of EMQ X horizontal scalability](https://www.emqx.com/en/blog/mqtt-broker-clustering-part-3-challenges-and-solutions-of-emqx-horizontal-scalability)
