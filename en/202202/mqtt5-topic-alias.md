Compared to MQTT v3.1 and v3.1.1, MQTT v5 provides more new features. We will try to present these features in easy-to-understand ways and discuss their impact on developments. We have already discussed some of the [new features in MQTT v5](https://www.emqx.com/en/mqtt/mqtt5), and we will continue to discuss **Topic Alias** today.

## What is Topic Alias

Topic Alias allows users to reduce the possibly long and repeatedly used topic name to a 2-byte integer, so as to reduce the bandwidth consumption when publishing messages.

This 2-byte integer is encoded as an attribute field in the variable header of the `PUBLISH` packet. And it’s limited by [Topic Alias Maximum](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901051) exchanged between client and broker in`CONNECT` and `CONNACK` packets. As long as this limit is not exceeded, any topic name can be reduced to one integer.

## Why use Topic Alias

In MQTT v3 protocol, if the client needs to publish a large number of messages to the same topic (over the same MQTT connection), the topic name will be repeated in all `PUBLISH` packets, which causes a waste of bandwidth resources. At the same time, parsing the UTF-8 string of the same topic name every time is a waste of computing resources for the server.

As an example, a sensor reports temperature and humidity at a fixed frequency from location `A`: 
It publishes to topic `/location/A/temperature` (23 bytes) for each temperature messages
It also publishes to topic `/location/A/humidity` (20 bytes) for the humidity messages.
Without topic aliases, not only for the first published message, each subsequent `PUBLISH` packet needs to carry the topic names (53 bytes in total) through the connection over and over again. And for the broker, it’ll have to parse the location topics repeatedly.

As we can see, the purpose of introducing topic alias feature in MQTT v5.0 is mainly to reduce resource consumption, in both network resources and CPU resources.

## How are topic aliases used

### Topic Alias life cycle and scope

Topic aliases are managed respectively by the client and server, and the life cycle and scope are limited to the current connection. When the topic aliases needs to be used again after disconnected, the mapping relationship of `topic alias <=> topic name` has to be rebuilt.

### Topic Alias Maximum

Before the MQTT client or server can start using topic aliases, they need to agree on the maximum number of topic aliases allowed in the current connection. This part of the information exchange is done in the `CONNECT` packet and the `CONNACK` packet. The `Topic Alias Maximum` is encoded in the variable headers of the `CONNECT` and `CONNACK` packets as a message attribute.

![Set MQTT Topic Alias Maximum mutually](https://assets.emqx.com/images/9b49a3437044bc206b400d5b81c39204.png)

<center>Set Topic Alias Maximum mutually</center>

`Topic Alias Maximum` in the client's `CONNECT` packet indicates the maximum number of topic alias that the server can use in this connection. Similarly, in the `CONNACK` packet sent by the server, the value indicates the maximum number of topic alias that can be used by the opposite end (client) in the current connection.

A topic alias may range from `1` to `Topic Alias Maximum`. Setting `Topic Alias Maximum` to `0` for the peer to prohibit the usage of topic alias.

### Creating and using a topic alias

When a client (or server) sends a `PUBLISH` packet, it can use a one-byte identifier with a value of `0x23` in the attribute of the variable header to indicate that the next 2 bytes being the number of topic alias.

However, the topic alias number is not allowed to be 0, nor is it allowed to be greater than the `Topic Alias Maximum` set in the `CONNACK` (`CONNECT`) packet sent by the server (client).

After receiving a `PUBLISH` packet with a topic alias and a non-empty topic name, the receiving end will establish a mapping relationship between the topic alias and the topic name. In the `PUBLISH` packets sent after this, the topic alias with a length of 2 bytes can be used to publish a message, and the receiving end will use the previously built mapping relationship of `topic alias <=> topic name` to find the topic for the messages. 

Since such mapping is maintained on both ends respectively (i.e. does not have to be identical), the client and the server can publish to different topics using the same alias number.

![MQTT client and broker manage their aliases respectively](https://assets.emqx.com/images/bcb4fa762372b2e96d6a9d26864242f4.png)

<center>MQTT client and broker manage their aliases respectively</center>


### Using unknown Topic Alias

If a topic alias used in the `PUBLISH` packet is not created previously, that is, the receiving end has not built the mapping relationship between the current topic alias and a topic name, and the topic name field in the variable header of this message is empty, the receiving end should send a `DISCONNECT` packet with a REASON_CODE of `0x82` to close the connection.

![Unknown topic alias](https://assets.emqx.com/images/e80be18ba1fe38b628e436a32782c88c.png)

<center>Unknown topic alias</center>

### Recreating Topic Alias

An already built alias to topic name mapping can be re-built with a new `PUBLISH` packet with a topic alias and a non-empty topic name.

As an example in the following diagram, the topic alias `123` which is previously used for the temperature topic now is updated to represent the humidity topic.

![MQTT client and broker recreate topic aliases](https://assets.emqx.com/images/fdab5dab7d1fa257d80a6a4a9085abac.png)

<center>MQTT client and broker recreate topic aliases</center>

## Conclusion

As a new feature in MQTT v5, topic alias provides a more flexible way to use the pub-sub messaging model. For messages published repeatedly to a finite set of topics, especially at large volume, topic aliases can effectively save both network and computing resources.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT 5.0 service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
