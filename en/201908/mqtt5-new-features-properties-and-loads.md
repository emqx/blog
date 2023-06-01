Compared with MQTT 3.1.1, MQTT 5.0 protocol adds many properties, which are distributed in variable headers and payloads of packet.

The packets carrying the payload in the MQTT 5.0 protocol include CONNECT packet, PUBLISH packet, SUBSCRIBE packet, SUBACK packet, UNSUBSCRIBE packet and UNSUBACK packet.

The payload of the PUBLISH packet is responsible for storing the message content, which is the same as the MQTT 3.1.1 protocol.

### CONNECT Packet

**The new properties of the variable header of the CONNECT packet are:**

![1.jpg](https://assets.emqx.com/images/52a7175d131df25693c1498c3f287658.jpg)

In the Payload of the CONNECT packet, some fields have changed, and the [Will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message) has become a Will Payload. Will properties are added to Payload to define the behavior of a will message.

**The new will properties are:**

![2.jpg](https://assets.emqx.com/images/29880f8724b075a58f27caca155c4b9a.jpg)

### CONNACK Packet

**CONNACK packet does not have Payload, and the properties contained in the variable header are:**

![3.jpg](https://assets.emqx.com/images/247af99b45d686958b8ca509be45aa6c.jpg)


### PUBLISH Packet

**The properties of the variable header of the PUBLISH message are:**

![PUBLISH 报文  .jpg](https://assets.emqx.com/images/804db596039856802b2073d95f4779a9.jpg)



### PUBACK, PUBREC, PUBREL, PUBCOMP, SUBACK, UNSUBACK PACKET

**PUBACK, PUBREC, PUBREL, PUBCOMP, SUBACK, UNSUBACK all have the following three properties:**

![PUBACK, PUBREC, PUBREL, PUBCOMP, SUBACK, UNSUBACK 报文.jpg](https://assets.emqx.com/images/d5fa746bdd091a885b2560884d6da0fc.jpg)


### SUBSCRIBE Packet

**The properties of the SUBSCRIBE message also exist in the variable header.**

![11.png](https://assets.emqx.com/images/b6b2ae013d4ca398689f9e87bc3ea536.png)


The Payload in the SUBSCRIBE packet in MQTT 5.0 contains the [Subscription Options](https://www.emqx.com/en/blog/subscription-identifier-and-subscription-options).

![SUBSCRIBE 报文2.jpg](https://assets.emqx.com/images/a019ca4b636fc8782087c8174854945c.jpg)



Bits 0 and 1 of the Subscription Options indicate the maximum QoS. This field gives the maximum QoS level that the server can send to client application messages. If the value of QoS  is 3, a protocol error is triggered.

Bit 2 of the subscription option indicates a option of No Local. If the value is 1, the application message will not be published to the publisher who has subscribed to the publishing topic and if the option is set to 1 in the [shared subscription](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription), a protocol error will be triggered.

Bit 3 of the subscription option indicates that Retain As Published is reserved. If the value is 1, the server shall set the RETAIN flag of the forwarded message to be the same as the RETAIN flag of the received PUBLISH packet. If the value is 0, the server needs to set the RETAIN flag of the forwarded message to 0 regardless of the value of the RETAIN flag in the received PUBLISH packet.

Bits 4 and 5 of the subscription option indicate Retain Handling. This option is used to control the sending of a retained message. When the value of the Retain Handling is 0, the server must forward the retained message to the topic that matches the subscription. When the value is 1, if the subscription no longer exists, the server needs to forward the retained message to the topic that matches the subscription. However, if the subscription exists, the server can no longer forward the retained message. When the value is 2, the server does not forward the retained message.

Bits 6 and 7 of the subscription option is reserved for future use. If any of the reserved bits of the payload are non-zero, the server treats the packet as a malformed packet.

### UNSUBSCRIBE Packet

UNSUBSCRIBE packet has only two properties: property length and user property.

The payload of the UNSUBSCRIBE packet is much simpler than the payload of SUBSCRIBE. It only contains a list of subject filters and does not contain a wide variety of subscription options.

The server will treat the packet as a malformed packet.

### DISCONNECT PACKET(new)

**The DISCONNECT packet is a new packet from MQTT 5.0. Its introduction means that the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) has the ability to actively disconnect. The properties of the DISCONNECT packet are:**

![DISCONNECT 报文新增.jpg](https://assets.emqx.com/images/fe76d0003f158a53f9fee55a67d1a794.jpg)


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
