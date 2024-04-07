[CoAP](https://www.emqx.com/en/blog/coap-protocol) is an IoT protocol that supports communication between low-consumption, low-power devices, which often run on constrained networks. For these reasons, CoAP is designed to be very concise and uses the UDP protocol for data transmission, allowing it to be well-adapted to constrained network environments. CoAP operates on abstracted resources in an M2M network, similar to HTTP operations, which enables synchronous and asynchronous information exchange between constrained devices in a very simple and efficient way.

CoAP is designed for restricted hardware and environments, and works well in restricted networks, but does not work well when the restricted network needs to communicate with external networks. In addition, CoAP lacks support for resource processing centers because it was designed with the M2M network model in mind (the CoAP-based LwM2M protocol introduces concepts such as resource registration and resource services).

This problem can be solved using the [EMQX](https://www.emqx.com/en/products/emqx) message broker. This article describes how to use EMQX to access the CoAP protocol and enable the communication of CoAP devices with external networks.

## CoAP protocol access methods in EMQX

For CoAP devices that need to communicate with external networks, using EMQX as a broker makes it easy to:

- Authenticate devices and reject data from untrustworthy devices.
- Manage resource permissions, including specifying different resource read/write permissions for different devices.
- Establish a data transfer hub between CoAP devices on different networks.
- Integrate with other applications, such as CoAP management applications, data analysis applications, and data access between CoAP devices and networks.

Two different CoAP access methods are provided in EMQX, covering most CoAP business scenarios. They provide simple access methods and good support without any changes to the CoAP protocol itself. The cost of accessing EMQX is minimal for existing CoAP devices and applications.

### CoAP URL model

EMQX implements access to CoAP through a URL path and query string according to the following rules:

```
CoAP connection type: //Host:Port/Mode/TopicName?c=ClientId&u=Username&p=Password
```

The **CoAP connection type** can be:

- coap: Uses normal UDP for transmission.
- coaps: Enables a secure transport layer. For details on how to enable coaps (including one-way authentication and two-way authentication), refer to the Encrypted Communication Configuration section below.

There are presently two access **modes**: [MQTT](https://www.emqx.com/en/mqtt-guide) and PubSub. The differences will be described in detail later.

**TopicName**: EMQX uses Topic as the resource identifier in CoAP. A Topic represents a resource object, which can be any UTF-8 string and allows multiple levels, such as coap/ and coap/test/queryString.

The **c**, **u** and **p** fields in the URL are mandatory, where:

- c represents the client ID, which is an arbitrary string, and in theory, each client ID should be unique;
- u and p represents the code username and password, respectively, which need to be set in the EMQX authentication module.

### MQTT mode

The MQTT mode follows the MQTT standard, mapping [JE1] the methods of CoAP to a simple Pub/Sub model through the following mapping: 

| Method | Token | MQTT        |
| ------ | ----- | ----------- |
| GET    | 0     | Subscribe   |
| GET    | 1     | Unsubscribe |
| GET    | _     | Illegal     |
| PUT    | _     | Publish     |
| POST   | _     | Illegal     |
| DELETE | _     | Illegal     |

This mode is suitable for the following scenarios:

- EMQX is only needed for messages, commands, or other real-time information transfers.
- If you need to use Observe for a prolonged period of time, you need to be on a private network or intranet. This is important, because UDP is connectionless. A UDP link generated on a public network cannot be maintained for a prolonged period of time, and this may prevent Observe from properly receiving the data.
- When in a public network, Observe can only be used as a listening mechanism for PUT operations. For example, if a CoAP device needs to send commands and data to another device via EMQX, and follow up on the returned data, it can:
  1. Use the PUT method to send commands to a Topic;
  2. Listen to this Topic using the Observe method;
  3. Process the data returned by EMQX. Given the maintenance time of UDP links in the public network, the Observe time is safe within 30 seconds, and sufficiently safe within 15 seconds.

### PubSub mode

The PubSub mode is more complex than the MQTT mode, but it is also more in line with the concept of a “resource” in CoAP. All Publish messages are stored as “resources” in EMQX, and the timeout is controlled by the optional max-age field in the CoAP protocol.

The mapping is as follows:

| Method | Token | MQTT        | Resouce                                        |
| ------ | ----- | ----------- | ---------------------------------------------- |
| GET    | 0     | Subscribe   | _                                              |
| GET    | 1     | Unsubscribe | _                                              |
| GET    | _     | _           | Read the message corresponding to this Topic   |
| PUT    | _     | Publish     | Update the message corresponding to this Topic |
| POST   | _     | Publish     | Update the message corresponding to this Topic |
| DELETE | _     | _           | Delete the message corresponding to this Topic |

PubSub mode is an extension of the MQTT mode, and is applicable for the following scenarios, in addition to those above:

- EMQX is used as a clearinghouse for aggregating data, information, and other resources. For example, a CoAP device that monitors the environment can periodically PUT the data it collects into EMQX, and the data processing center can receive the data by subscribing to relevant topics in order to analyze environmental conditions. Another example is where CoAP devices can regularly push their status to EMQX, and users can directly observe the operating status of devices through EMQX.
- Low frequency of message transmission and high tolerance for latency. In these scenarios, PUT can be used to update the messages of a Topic, and clients interested in the Topic can obtain the latest messages, data, etc. at their own pace through GET.

## **Configuration method**

The configuration of EMQX’s CoAP protocol gateway is described in detail in the “emqx.conf” file.

### Unencrypted communication scenarios

For less sensitive data, or when you do not need a secure transport link, you can simply open the corresponding ports to listen on, according to your business requirements.

For example, the following configuration listens to port 5683 on all available IPs, and port 5684 on LAN IP 192.168.1.2.

```
coap.bind.udp.1 = 0.0.0.0:5683
coap.bind.udp.2 = 192.168.1.2:5684
```

### Encrypted communication scenarios

EMQX’s CoAP protocol gateway supports the DTLS secure transport layer protocol, which can be configured with one-way/bidirectional authentication. This is automatically turned on by default.

#### **One-way Authentication**

The one-way authentication configuration is, as follows. If you do not need to enable encrypted communication, you should comment out these configurations.

```
## DTLS listening ports, configured in the same manner as the UDP mode above, and can be configured with as many ports as needed.
coap.dtls.port1 = 5684
coap.dtls.port2 = 192.168.1.2:6585

## DTLS private key
## Value: File
coap.dtls.keyfile = {{ platform_etc_dir }}/certs/key.pem

## DTLS certificate
## Value: File
coap.dtls.certfile = {{ platform_etc_dir }}/certs/cert.pem
```

#### **Bidirectional Authentication**

EMQX’s CoAP protocol gateway also supports bidirectional authentication, and is configured, as follows:

```
## Verification mode, the optional values are: verify_peer | verify_none
coap.dtls.verify = verify_peer

## Whether to reject the connection when the client does not send a certificate
coap.dtls.fail_if_no_peer_cert = false

## CA certificates in pem format
coap.dtls.cacertfile = {{ platform_etc_dir }}/certs/cacert.pem
```

The coap.dtls.verify is used to determine whether two-way authentication is enabled, with the optional value of:

- verify_peer Verifies the client;

- verify_none Does not verify the client.

When bidirectional authentication is enabled, coap.dtls.fail_if_no_peer_cert is used to determine whether the server will reject the connection when the client does not send a certificate. The coap.dtls.cacertfile is a CA certificate in .pem format, which is used to verify the client. For more information about bidirectional authentication, please refer to [Enable SSL/TLS for EMQX](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide).

## Testing and Verification

### Enabling the CoAP Protocol Gateway

#### Using Dashboard

In Dashboard, under the Plugins directory, select emqx_coap and click Enable, as shown in the figure:

![EMQX Dashboard](https://assets.emqx.com/images/513a8b45a147014ca07643c5b5436cd7.jpeg)

#### Using the terminal

The emqx_coap feature can be enabled in the terminal using the following command:

```
./bin/emqx_ctl plugins load emqx_coap
```

### Installing the CoAP test client

#### coap.me 

If a public IP is configured on EMQX’s CoAP protocol gateway, you can use the online website https://coap.me/  to test it. Refer to the website for details on how to use this.

#### libcoap

Libcoap is a C library with full support for all CoAP-related standards. This comes with a client application and has generally been regarded as the standard validation client for CoAP.

On most Linux systems, this can be installed using the system package manager. On macOS, this can be installed using brew. On other platforms, this may require manual compilation of the source code.

The installed client is usually called: coap-client or libcoap.

### Testing the PubSub mode

Here is a demonstration using libcoap to publish a message to the server and subsequently read the latest message corresponding to that Topic.

```
# Using PubSub mode, push a message in JSON format to the coap/test Topic with the put method.
coap-client -m put -e '#{msg => "Hello, CoAP"}' -t json "coap://127.0.0.1:5683/ps/coap/test?c=clientid1234&u=admin&p=public"

# Read the last message of the coap/test Topic, and you will get #{msg => "Hello, CoAP"}.
coap-client -m get  "coap://127.0.0.1:5683/ps/coap/test?c=clientid1234&u=admin&p=public"
```

The following example shows how to subscribe:

```
## Subscribe to the coap/observe topic, Token is set to "token", and the subscription timeout is 60 seconds.
coap-client -m get -s 60 -B 30 -o - -T "token" "coap://127.0.0.1:5683/ps/coap/observe?c=clientid1234&u=admin&p=public"

## Push using another CoAP client or any other MQTT client.
coap-client -m post -e '#{msg => "This is Observe"}' -t json "coap://127.0.0.1:5683/ps/coap/observe?c=clientid1234&u=admin&p=public"

## The subscriber will receive at this point:
## #{msg => "This is Observe"}
```

### Testing the MQTT mode

The test for MQTT mode is the same as above, except that only publish/subscribe is available. An example is given as follows:

```
## publish
coap-client -m put -e '#{msg => "Hello, CoAP"}' -t json "coap://127.0.0.1:5683/mqtt/coap/test?c=clientid1234&u=admin&p=public"

## subscribe
coap-client -m get -s 60 -B 60 -o - -T "token" "coap://127.0.0.1:5683/mqtt/coap/sub?c=clientid1234&u=admin&p=public"
```

## Conclusion

At this point, we have completed the process of connecting CoAP devices to EMQX, successfully integrating CoAP and MQTT protocol devices.

As a powerful open-source distributed cloud-native message broker, EMQX not only fully supports the MQTT protocol but also supports CoAP and LwM2M protocols, providing convenient access to a variety of end devices.

For more details on using EMQX, please refer to the [EMQX Enterprise documentation](https://docs.emqx.com/en/enterprise/v4.4/). You can also visit EMQX GitHub project at [https://github.com/emqx/emqx](https://github.com/emqx/emqx) to follow the latest updates on the EMQX open-source project.


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
