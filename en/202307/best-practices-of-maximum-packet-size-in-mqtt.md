## What is the Maximum Packet Size?

The theoretical maximum length of an [MQTT packet](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets) is 268,435,456 bytes, equivalent to 256 MB. However, it is evident that resource-constrained clients and some MQTT servers operating as edge gateways may not be able to handle packets of this size.

Considering that different clients may have significantly different capabilities in handling packets, sending excessively large packets can not only affect the normal business processing of the peer but may also directly overwhelm the peer. Therefore, we need to use the Maximum Packet Size property to negotiate the maximum packet length that the client and server can handle.

The client first specifies the maximum allowed packet length that the server can send to it by using the Maximum Packet Size in the CONNECT packet. On the other hand, the server specifies the maximum allowed packet length that the client can send to it using the Maximum Packet Size in the CONNACK packet.

![MQTT CONNECT packet](https://assets.emqx.com/images/1f64b4c59e8da8d446d823d6b8f20535.png)

Once the connection is established, both parties must adhere to this agreement when sending packets. Neither party is allowed to send packets that exceed the agreed length limit. Otherwise, the receiver will return a DISCONNECT packet with a Reason Code of 0x95 and close the network connection.

It is important to note that if the client sets a [Will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message) in the CONNECT packet, it may unknowingly cause the CONNECT packet to exceed the maximum packet length allowed by the server. In such cases, the server will respond with a CONNACK packet with a Reason Code of 0x95 and close the network connection.

## How Does the Sender Work Within the Limit?

For the client, whether it is publishing or subscribing, as the active sender, it can split a packet into multiple parts to be sent in order to avoid exceeding the length limit.

But for the server, it is only responsible for forwarding the message, and cannot determine the size of the message. So if it finds that the size of the message to be forwarded exceeds the maximum value that the client can receive, then it will drop this message. If it is a [shared subscription](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription), besides dropping, the server can also choose to send the message to other clients in the group that can receive the message.

In addition to the two strategies mentioned above, whether it is the client or the server, they can trim the packet's content to reduce the length. We know that the responder can include two properties, User Property and Reason String, in response packets such as CONNACK and PUBACK, to convey additional information to the peer.

However, the possibility of exceeding the maximum length limit in response packets is precisely caused by these two properties. Obviously, the priority of transmitting these properties is lower than ensuring the proper flow of the protocol. Therefore, the responder can remove these two properties from the packet when the length of the packet exceeds the limit, to maximize the chances of successfully transmitting the response packet.

I want to let you know that this only applies to response packets, not to PUBLISH packets. For PUBLISH packets, User Property is considered part of the packet, and the server should not attempt to remove it from the packet to ensure packet delivery.

## Demo

1. Open the installed [MQTTX](https://mqttx.app/).

2. Create an MQTT connection, set the Maximum Packet Size to 100, and connect to the [Free Public MQTT Server](https://www.emqx.com/en/mqtt/public-mqtt5-broker):

   ![Create an MQTT connection](https://assets.emqx.com/images/784f1078a559f75b0c9ed10f30a5a218.png)

3. After a successful connection, we can observe through the Wireshark packet capture tool that the Maximum Packet Size property in the CONNACK packet returned by the server is 1048576. This means that the client can only send a packet of up to 1 KB to the public MQTT server each time:

   ![Wireshark packet capture tool](https://assets.emqx.com/images/0d6c9d52f8dbb2c052119386f0bb10b3.png)

4. Go back to MQTTX and subscribe to the topic `mqttx_0c668d0d/demo`:

   ![Subscribe to the topic "mqttx_0c668d0d/demo"](https://assets.emqx.com/images/8653151cecd5a961b77ba24a40373a4a.png)

5. Then we publish two messages to the topic `mqttx_0c668d0d/demo`, one with a length of 5 bytes and another with a size of 172 bytes. We will observe that only the message with a length of 5 bytes will be received, while another message exceeding the 100-byte length limit will not be forwarded by the server:

   ![Publish two messages to the topic "mqttx_0c668d0d/demo"](https://assets.emqx.com/images/833e937b1195e1ca9e11f719e350053d.png)



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
