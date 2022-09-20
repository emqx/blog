## MQTT Retained message

When the MQTT broker server receives a PUBLISH message with a Retain flag of 1, it treats the message as a retained message. Except for normal forwarding, the retained message is stored on the server. Only one retained message can exist under each topic. If another retained message for the same topic already exists, the original retained message is replaced.

When a client establishes a subscription, if there are retained messages on the server that matches the topic , these retained messages will be sent to the client immediately. With retained messages, new subscribers can immediately get the most recent status without waiting for unexpected period, which is important in many scenarios.

Although the retained message is stored on the server, it is not part of the session. That is to say, even if the session that published this retained message ends, the retained message will not be deleted. There are only two ways to delete retained messages:

1. The client sends a retained message with a blank Payload to a certain topic, and the server deletes the retained message under this topic.
2. If the PUBLISH packet containing the retained message has set the message expiration interval attribute, the retained message will be deleted after it has been stored on the server for the time longer than the expiration time.

## MQTT Message expiration interval

The message expiration interval can be set for A PUBLISH packet. The message expiration interval is a four-byte integer, which indicates the life cycle of the application message with the unit of second.

If the message expiration interval is not set for A PUBLISH packet, the application message will not expire.

If the message expiration interval is set for A PUBLISH packet, the messages have expired, and the server has not started delivering the message to the matching subscribers, the server must delete the message.

## Retained messages of the EMQX

The message retention function of [EMQX MQTT Broker](https://www.emqx.com/en) is implemented by the `emqx_retainer` plugin, which is enabled by default. By modifying the configuration of the` emqx_retainer` plugin, you can adjust the EMQX Broker's retention message Location, restrict the number of retained messages and maximum payload length, and adjust the expiration time of retained messages.

`emqx_retainer` is enabled by default，and configuration path of the plugin is `etc/plugins/emqx_retainer.conf`

+ retainer.storage_type

  In terms of storage location of retained messages, EMQX Broker can choose to store retained messages only in memory, only in hard disk, or both in memory and hard disk, which can be flexibly determined by the user's business characteristics.

  For example, users who want to collect meter readings may decide to use QoS Level 1 messages because it is unacceptable for them if data is lost during transmission on the network. However, they may think the data of client and server can be stored in memory (volatile memory ). That is because the power supply system is very reliable, there is not much risk of data loss.

  In contrast, providers of parking bill payment applications may decide that payment data can not be lost under any circumstances. Therefore, they require that all data be written to a hard disk (non-volatile memory) before being transmitted over the network.

+ retainer.max_retained_messages、retainer.max_payload_size

  `retainer.max_retained_messages` specifies the maximum number of retained messages that EMQX Broker can store. 0 means no limit. When the number of retained messages exceeds the maximum limit, existing retained messages can be replaced, but retained messages cannot be stored for new topics.

  `retainer.max_payload_size` specifies the maximum Payload value of retained messages that EMQX Broker can receive. After the payload size exceeds the maximum value, the EMQX message server will treat the received retained message as a normal message and will not store this message anymore.

  These two configurations set an upper limit for retained messages that EMQX Broker can receive and store, which ensures that EMQX Broker does not occupy excessive resources to store and process retained messages.

+ retainer.expiry_interval

  For expiration time of retained messages, 0 means never expired. If the message expiration interval is set in the PUBLISH packet, it will be taken as the standard.

  When the retained message expires, EMQX Broker deletes the message.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
