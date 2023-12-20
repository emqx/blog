Ports are digital communication endpoints that are needed for sending and receiving data across networks. [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) (Message Queuing Telemetry Transport) is a simple, lightweight messaging protocol based on a publish/subscribe model, which supports communication between resource-constrained network clients.

MQTT ports facilitate the communication between[ MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) and servers. They are the conduits through which MQTT messages travel. Each MQTT port corresponds to a unique service, and several ports can be active simultaneously. We’ll describe the port numbers commonly used in MQTT, how to configure ports, explain the risks involved in exposing MQTT ports, and provide best practices for securing your ports.

## Default MQTT Ports Numbers

The following port numbers are available in MQTT brokers by default:

### Standard MQTT Port (1883)

This port is used for unencrypted MQTT connections. It is the most commonly used MQTT port and is the default port for most MQTT brokers. Using this port, MQTT clients can publish messages, subscribe to topics, and receive published messages.

### MQTT over SSL/TLS (8883)

MQTT also supports secure connections through Transport Layer Security (TLS) or its predecessor, Secure Sockets Layer (SSL). The default port for MQTT over SSL/TLS is 8883. This port is used when the communication between the MQTT client and the server needs to be encrypted for enhanced security.

### MQTT over WebSocket (443)

MQTT can also operate over WebSockets, which use port 443 by default. This allows MQTT to leverage HTTP and HTTPS infrastructure. WebSocket is a protocol that provides full-duplex communication channels over a single TCP connection, suitable for real-time data transfer.

### MQTT over QUIC (14567)

[QUIC](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov) (Quick UDP Internet Connections) is a transport layer protocol designed to improve performance over TCP. It provides multiple streams of data over a single connection and has built-in TLS for security.

## Configuring MQTT Ports

Most [MQTT brokers](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) allow you to configure and customize MQTT ports. In each of the following sections, we’ll show how to configure ports in [EMQX](https://www.emqx.com/en/products/emqx).

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

### Set the Default Port

Most MQTT brokers automatically use port 1883 as the default port. However, you can change the default port number in the broker's configuration file. Any MQTT client that wants to connect to the broker must use this port number.

**Example in EMQX broker:**

To change the default MQTT port in EMQX, edit the emqx.conf file. Look for the line that specifies the MQTT listener and change the port:

```
listener.tcp.default = 1883
```

Change 1883 to your desired port, for instance, 1884:

```
listener.tcp.default = 1884
```

Restart the EMQX broker for the changes to take effect.

### Configure MQTT over TLS/SSL

This involves creating a secure connection between the MQTT client and the server. This is done by setting the port number to 8883 in the broker's configuration file. The client and server also need to exchange certificates to authenticate each other.

**Example in EMQX broker:**

Edit the `emqx.conf` file and look for the SSL listener configuration:

```
listener.ssl.external = 8883
```

Enable this by uncommenting the line (if necessary), and also specify the paths to your SSL certificates:

```
listener.ssl.external.keyfile = etc/certs/your_private_key.pem
listener.ssl.external.certfile = etc/certs/your_certificate.pem
```

Restart the EMQX broker for the changes to be applied.

### Multiple Ports

Running MQTT on multiple ports can enhance the system's flexibility. For example, you can run MQTT on both the standard port and the secure port, allowing both secure and non-secure connections. To do this, specify multiple port numbers in the broker's configuration file.

**Example in EMQX broker:**

Edit the `emqx.conf` file and specify multiple listeners:

```
listener.tcp.default = 1883
listener.ssl.external = 8883
```

Restart the broker to apply the changes.

### Test the Configuration

After configuring the MQTT ports, it's essential to test the configuration to ensure that everything is working correctly. This can be done using an MQTT client to connect to the broker and publish and subscribe to messages. If you can successfully send and receive messages, your configuration is correct.

**Example in EMQX Broker:**

1. Navigate to the EMQX Dashboard using your web browser. The URL is usually `http://broker_host:18083`. Log in using your credentials.
2. Once logged in, find the **Tools** menu on the sidebar and click on **Tester**.
3. In the **Tester** tab, you can simulate MQTT clients. Create a new connection by clicking the **New Connection** button.
4. Fill in the details such as the hostname (usually the IP address of the machine where EMQX is running) and port number. For standard MQTT, use `1883`; for MQTT over SSL, use `8883`.
5. After establishing the connection, use the **Publish** and **Subscribe** options within the Tester to send and receive messages on various topics.
6. Publish a test message and then subscribe to the same topic. If you receive the test message, then the port is configured correctly.

This method allows you to validate the port configurations, ensuring that your settings are correctly applied.

## Risks Associated with Exposing MQTT Ports

When you expose MQTT ports to the internet, it opens up opportunities for cybercriminals. They can exploit these ports in several ways, leading to significant security risks.

### Unauthorized Access

Hackers can gain unauthorized access to your network through open MQTT ports. They can eavesdrop on your communication, potentially gaining access to sensitive data. If the data being transmitted is not encrypted, the hacker can easily read the information. Adversaries can also manipulate this data, leading to misinformation and potentially catastrophic outcomes.

### Device Compromise

Once hackers gain access to your network, they can compromise the devices connected to it. They can install malware on these devices, turning them into bots. These bots can then be controlled remotely by the hackers, who can use them to carry out further attacks.

### Denial of Service (DoS) Attacks

Open MQTT ports can also lead to Denial of Service (DoS) attacks. In a DoS attack, the attacker floods the network with traffic, causing the system to slow down or even crash. This can lead to significant downtime, disrupting business operations. Furthermore, it can also lead to loss of data and potential revenue.

### Resource Depletion

Hackers can use these ports to send large amounts of data to your network. This data consumes a significant chunk of your network's resources, leaving little for your actual business operations. This can lead to a slowdown in operations.

## Best Practices for Securing MQTT Ports

In light of the risks we discussed above, it’s critical to secure your MQTT ports. Let's look into a few security best practices.

### Use SSL/TLS

Whenever possible, use port 8883 for secure communication over SSL/TLS. The MQTT broker should support encrypted communication over SSL/TLS.

### Use Strong Authentication

Your authentication measures should include a combination of username and password that is hard to guess. Consider implementing a two-factor authentication system. This adds an additional layer of security, making it harder for hackers to gain unauthorized access to your network.

### Implement Access Control

Restrict access to your MQTT ports to only those devices that need it. You can do this by using an access control list (ACL). An ACL is a list of devices that are allowed to access certain resources. By using an ACL, you can ensure that only authorized devices can access your MQTT ports.

### Use a Firewall

A firewall monitors and controls incoming and outgoing network traffic based on predefined security rules. It acts as a barrier between your trusted internal network and untrusted external networks. By using a firewall, you can prevent unauthorized access to your MQTT ports.

### Isolate the MQTT Broker

The MQTT broker is the server that handles the communication between devices. By isolating the MQTT broker, you can reduce the risk of device compromise. You can do this by placing the broker in a separate network segment, away from other business systems and with limited access to public networks.

## Improving MQTT Security with EMQX

Understanding and properly configuring MQTT ports are crucial steps in ensuring the security and functionality of your MQTT communications. As the world's most scalable open source MQTT Broker, EMQX opens standard ports such as TCP (1883) and SSL/TLS (8883) by default. You can also access the default port 14567 to establish an MQTT over QUIC connection. EMQX also provides complete listener management capabilities, allowing you to modify and close ports in the configuration file or Dashboard as needed, as well as adjust other behaviors of the listener.

Considering the possible risks caused by exposing the MQTT port to the Internet, such as unauthorized access and device compromise, EMQX protects you through rich authentication and authorization mechanisms and comprehensive SSL/TLS support. You can complete all the previously mentioned best practices in EMQX to enhance the security of MQTT communications and ensure reliable operation of the MQTT infrastructure.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
