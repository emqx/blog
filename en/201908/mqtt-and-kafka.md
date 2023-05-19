MQTT is completely different from Kafka. MQTT is a protocol and a technical standard developed by members (mostly are top engineers at IBM and Microsoft) of the OASIS Technical Committee. Kafka is an open source streaming platform that has been implemented. It was firstly developed by LinkedIn. After incubated by Apache Incubator in 2011 after opening source, it has became the top project of the Apache Software Foundation.

The only existing connection between the two is that they are both related to the publish/subscribe pattern. MQTT is a messaging protocol based on the publish/subscribe pattern, while the production and consumption processes of Apache Kafka are also part of the publish/subscribe pattern. So if we implement a message broker based on the [MQTT protocol](https://www.emqx.com/en/mqtt-guide), is this [MQTT broker](https://www.emqx.io) equivalent to Kafka? The answer is still no!

**Although Kafka is also a messaging system based on publish/subscribe pattern, it is also called ''distributed commit log'' or "distributed streaming platform". Its main function is to achieve distributed persistent data preservation.** Kafka's data unit is a message that can be understood as a row of "data" or a piece of"record" in the database. Kafka conducts classification by topic. When Kafka's producers publish messages to a specific topic,  consumers consume messages on that specific topic. In fact, producers and consumers can be understood as publishers and subscribers and the topic is like a table in a database. Each topic contains multiple partitions, and the partitions can be distributed on different servers. That is to say, the distributed data is stored and read by this way. Kafka's distributed architecture facilitates the expansion and maintenance of the read-write system (for example, implementing redundant backups through backup servers and achieving performance  improvement by architecting multiple server nodes). In many large enterprises with big data analysis needs, Kafka will be used as the data stream processing platform.

**MQTT was originally designed for network access of IoT devices. Most IoT devices are computer devices with low-performance and low-power , and the quality of network connections is unreliable. Therefore, several key points need to be considered when designing protocols are as follows: **

1. The protocol should be lightweight enough to allow embedded devices to parse and respond quickly.
2. Be flexible enough to support the diversification of IoT devices and services.
3. It should be designed as an asynchronous message protocol instead of a synchronous protocol. This is because the network latency of most IoT devices is very likely to be very unstable. If  the synchronous messaging protocol is used, the IoT device needs to wait for the response from the server.  It is obviously very unrealistic to provide services for a large number of IoT devices.
4. Must be two-way communication, and the server and client should be able to send messages to each other.

The MQTT protocol perfectly addresses the above requirements, and the latest version of the MQTT v5.0 protocol has been optimized to make it more flexible and less bandwidth occupation than the previous version of v3.1.1.

In terms of the difference between mqtt-based message broker and Kafka,  Mr. EMQ believes that t it lies in their different focuses. Kafka focuses on the storage and reading of data, aiming at streaming data processing scenarios with high real-time performance, while MQTT broker focuses on communication between client and server.

The message exchange pattern adopted by MQTT broker and Kafka is so similar that it is obviously a good idea to combine them. In fact, some MQTT brokers, such as **EMQX**, have already implemented the bridging of MQTT broker and Kafka. MQTT broker is used to quickly receive and process messages from a large number of  IoT devices, and Kafka collects and stores these large amounts of data and sends them to data analysts to analyze and process messages.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
