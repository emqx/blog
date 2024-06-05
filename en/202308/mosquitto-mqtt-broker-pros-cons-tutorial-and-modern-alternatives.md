## What is the Eclipse Mosquitto MQTT Broker

Eclipse Mosquitto is an [open-source MQTT broker](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023) that uses the MQTT (Message Queuing Telemetry Transport) protocol. MQTT is a lightweight protocol designed for constrained devices with low-bandwidth, making it perfect for machine-to-machine (M2M) or internet of things (IoT) applications where network bandwidth is at a premium.

The Mosquitto MQTT broker was initially developed by Roger Light in 2009 and later donated to the Eclipse Foundation. It was probably the first open source MQTT project. The broker receives all messages from the clients, filters the messages, determines who is subscribed to each message, and then sends the message to these subscribed clients.

In the world of IoT, where devices need to communicate efficiently, Mosquitto’s ability to handle multiple connections and deliver messages in real-time is very useful.

This is part of a series of articles about [MQTT Protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt).

## Key Features of Mosquitto MQTT Broker

### Lightweight

One of the key features of Mosquitto MQTT is its lightweight design. This means it requires minimal system resources to run, making it ideal for small, resource-constrained devices like sensors, microcontrollers, and other IoT devices. Moreover, its efficient use of bandwidth means it can work well even in environments with unreliable or limited network connectivity.

However, Mosquitto has limited scalability. It can support up to thousands of connections, which is suitable for smaller-scale IoT deployments, but cannot scale up to millions of connections required for large scale deployments.

### Multi-Platform

Mosquitto MQTT can run on various operating systems, including Linux, Windows, macOS, and even on embedded systems like Raspberry Pi. It also supports Docker containers, but not Kubernetes or Terraform.

### Bridge Connections

Bridge connections allow Mosquitto MQTT brokers to connect with other [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), either from the same or different networks. The bridging feature is useful when you need to aggregate data from different networks or when you want to connect isolated networks.

### Message Storage

Mosquitto MQTT provides a message storage feature. This means that it can store messages that it receives when the intended recipients are not currently connected. Once those recipients come online, the stored messages are delivered to them. This ensures that no data is lost, even in cases of temporary disconnection.

This feature is particularly useful in IoT applications, where devices can go offline or become unreachable due to various reasons such as power loss or network issues.

## Mosquitto MQTT Limitations

Before diving in to learn how to use Mosquitto MQTT, it's important to understand its limitations. This knowledge will assist you in making informed decisions when implementing IoT solutions.

### No Built-in Web Interface

One of the significant limitations of Mosquitto MQTT is the lack of a built-in web interface. This means that you cannot easily manage and monitor your MQTT brokers and topics over the web. Instead, you would need to rely on command-line tools or third-party applications to perform these tasks. The absence of a web interface can be a significant drawback, as a graphical user interface enables easier management and monitoring.

### Limited Data Integration

Mosquito supports webhooks, but does not easily integrate with data processing tools like MySQL, MongoDB, Redis, etc. This makes it more difficult to use Mosquitto as part of a modern data infrastructure.

### Limited Cloud Support

Many organizations are transitioning to running MQTT infrastructure in the cloud. Mosquitto does not have built-in support for cloud services like AWS, Azure, or Google Cloud, making it incompatible with cloud-based IoT deployments.

### Limited Security Features

Another limitation of Mosquitto MQTT is its limited security features. While it does provide basic security features such as username/password authentication and SSL/TLS encryption, it lacks advanced security mechanisms. For instance, Mosquitto MQTT does not support role-based access control (RBAC), which allows for fine-grained control over who can publish or subscribe to specific topics. This can be a concern in scenarios where sensitive data is being transmitted, or where strict access controls are required.

### No Built-In Clustering or Redundancy Features

Mosquitto MQTT also lacks built-in clustering or redundancy features. In a clustered setup, multiple MQTT brokers work together to provide high availability and load balancing. If one broker goes down, others can take over, ensuring that the system remains operational. Unfortunately, Mosquitto MQTT does not natively support this feature. To achieve a clustered setup, you would need to implement it manually or use third-party tools, which can be complex and time-consuming.

### Limited Persistence Mechanism

Finally, Mosquitto MQTT has a limited persistence mechanism. It only supports file-based persistence, where it stores all the data (messages, subscriptions, etc.) in a single file. File-based persistence does not scale well, making it unsuitable for large-scale IoT deployments.

> Related content: Read our guide to [MQTT protocol in IoT](https://www.emqx.com/en/blog/what-is-the-mqtt-protocol)

## Mosquitto MQTT Tutorial

Now that we've discussed the limitations of Mosquitto MQTT, let's move on to the tutorial. This section will guide you through the basics of installing Mosquitto, starting the broker, publishing a message, subscribing to a topic, and testing your setup.

### Installing Mosquitto

The exact steps for installing Mosquitto will depend on your operating system, but for most Linux distributions, you can use the package manager for installation. For instance, on Ubuntu, you can install Mosquitto by running the following command: 

```
sudo apt-get install mosquitto mosquitto-clients
```

For Windows or macOS, you can download the installer from the Mosquitto website and follow the instructions provided.

### Starting the Mosquitto Broker

Once you have installed Mosquitto, the next step is to start the MQTT broker. On Linux, you can start the broker by running the command: 

```
sudo systemctl start mosquitto
```

On Windows, the broker should start automatically after installation. If it doesn't, you can start it manually from the Services app.

### Publishing a Message

To publish a message, you can use the `mosquitto_pub` command-line tool that comes with the Mosquitto package. The basic syntax is: 

```
mosquitto_pub -h <hostname> -t <topic> -m <message>
```

Let’s review the options used in this command:

- The `-h` option specifies the hostname of the MQTT broker.

- The `-t` option specifies the topic to which the message should be published.

- The `-m` option specifies the message to be published.

### Subscribing to a Topic

Subscribing to a topic is just as easy. You can use the `mosquitto_sub` command-line tool, with the basic syntax being:

```
mosquitto_sub -h <hostname> -t <topic>
```

Let’s review the options:

- The `-h` option specifies the hostname of the MQTT broker.

- The `-t` option specifies the topic to which you want to subscribe.

### Testing Your Setup

After publishing a message and subscribing to a topic, you should test your setup to ensure it's working correctly. You can do this by publishing a test message and checking if the subscriber receives it. If everything is working as expected, you should see the test message printed on the console of the subscriber.

## EMQX: A Modern Alternative to Mosquitto MQTT Broker

Mosquitto fully supports the MQTT protocol features but does not support clustering, which makes it difficult to meet the performance requirements of IoT for large-scale mass connectivity. Therefore, Mosquitto is not suitable for MQTT servers for large-scale services. Specifically, it cannot support enterprise solutions requiring millions of connections for a large fleet of IoT devices. Most importantly, Mosquitto lacks the necessary enterprise features, so it is not possible to build a flexible, truly reliable IoT application using Mosquitto.

[EMQX](https://www.emqx.com/en/products/emqx), a highly scalable distributed MQTT messaging broker, can support millions of concurrent connections on a single cluster. A large-scale distributed MQTT message broker for IoT, EMQX can efficiently and reliably connect to massive amounts of IoT devices, with up to 100 million concurrent connections per cluster, processing and distributing messages and event flow data in real-time. EMQX nodes can be bridged by other types of MQTT servers and MQTT cloud services for cross-platform message subscription & sending.

While EMQX and Mosquitto both support Docker-based containerized deployments, EMQX additionally supports Kubernetes Operators and Terraform, making it easy to deploy and operate on all public cloud platforms. 

In addition, while Mosquitto does not support cloud deployment, EMQX offers [serverless](https://www.emqx.com/en/cloud/serverless-mqtt), [dedicated](https://www.emqx.com/en/cloud/dedicated), and [Bring Your Own Cloud (BYOC)](https://www.emqx.com/en/cloud/byoc) MQTT messaging services on AWS, Google Cloud, and Microsoft Azure.

![Bridge Mosquitto MQTT messages](https://assets.emqx.com/images/e21c44b85b64bbde4e79d05340521c98.png)

<center>Extend connectivity of Mosquitto with EMQX</center>

**Next steps:**

- [Open MQTT Benchmarking Comparison: EMQX vs Mosquitto](https://www.emqx.com/en/blog/open-mqtt-benchmarking-comparison-emqx-vs-mosquitto)
- [Learn How to Bridge Mosquitto MQTT Messages to EMQX](https://www.emqx.com/en/blog/bridging-mosquitto-to-emqx-cluster)
- [Learn More About EMQX Cloud](https://www.emqx.com/en/cloud)





<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
