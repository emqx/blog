### Introduction

Although the publish-subscribe model fully decouples the publisher of the message from the subscriber, there is also an implicit problem that the subscriber cannot actively request the message from the publisher, and when the subscriber receives the message depends entirely on the publisher. This is inconvenient in some scenarios. For example, when a device periodically publishes its own GPS coordinates, it may take a few seconds for a subscriber to receive data from initiation of a subscription for the first time, or it may take ten minutes or more, which is not friendly. Therefore, [MQTT](https://www.emqx.com/en/mqtt) introduces the retained message.

### Retain message

![image20191014152158994.png](https://static.emqx.net/images/d57f8dd63bee941219594679e3469bf9.png)

When the server receives a PUBLISH packet with a Retain flag of 1, it will conduct the following operations:

1. If there are subscribers matching this topic name, it will forward them in normal logic and clear the Retain flag before forwarding. The Retain flag in the MQTT v3.1.1 protocol must be cleared, and a Retain As Publish field is added in the subscription option of MQTT v5.0 protocol. The client itself indicates whether the server needs to clear the Retain flag before forwarding.
2. If Payload is not empty, it will store this application message and replace it if a retained message already exists under this topic. If the Payload is empty, the server will not store this application message and clear the retained messages that already exist under this topic.

Whenever a subscriber establishes a subscription, the server will check if there is a retained message that matches the subscription, and if the retained message exists, it immediately forwards it to the subscriber. When a retained message is forwarded to the subscriber in this case, its Retain flag must remain at 1. Compared to MQTT v3.1.1, it makes a more detailed division of whether to send a retained message when the subscription is established in MQTT v5.0, and provides a Retain Handling field in the subscription option. For example, some clients may only want to receive a retained message when they subscribe for the first time, or they may not want to receive a retained message when the subscription is established, which can be adjusted by the Retain Handling option.

Although the retained message is stored in the server, it is not part of the session. That is to say, even if the session that published the retained message is terminated, the retained message will not be deleted. There are only two ways to delete a retained message:

1. As mentioned earlier, the client sends a retained message with a Payload empty to a topic, and the server deletes the retained message under this topic.
2. The message expiration interval attribute is also applicable in the retained message. If the client sets this attribute, the retained message will be deleted after the storage expiration time is due.

With retained messages, new subscribers can get the most recent status immediately, without waiting for unpredictable times, which is very important in many scenarios.
