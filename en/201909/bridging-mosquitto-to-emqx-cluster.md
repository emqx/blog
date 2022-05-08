EMQX nodes can be bridged by other types of MQTT broker to achieve cross-platform message subscription and post. In this article, we present a configuration example to illustrate how to configure the bridge from Mosquitto to EMQX.

Mosquitto is a small, lightweight, open source MQTT Broker written in C/C++ language. Mosquitto uses a single core and single thread architecture to support embedded devices deployed in limited resources, access a small number of MQTT device terminals, and implement [MQTT  5.0](https://www.emqx.com/en/mqtt/mqtt5) and 3.1.1 protocols.

Both EMQX and Mosquitto fully support the [MQTT protocol](https://www.emqx.com/en/mqtt) feature, but EMQX supports more communication protocols and private protocol access. In terms of functional extension of the application, Mosquitto lacks the  out-of-the-box business-related functions, such as certification authentication, rules engine, data persistence and high-performance message bridging (EMQX enterprise editions). In the aspect of monitoring operation, maintenance and visualization management, EMQX has full existing features and extended solution support.  In terms of the basic function, Mosquitto clustering is weak, and neither official nor third-party clustering solutions can support the performance requirements of large-scale massive connectivity of IoT.

Therefore, Mosquitto is not suitable for the [MQTT broker](https://www.emqx.com/en/products/emqx) for large-scale services. However, since it is lightweight and compact, it can run on any low-power microcontroller including embedded sensors, mobile devices, embedded microprocessors, and message access at the edge of the Internet of Things. It is a better technology choice for edge message access in the IoT, and the message can be processed locally and passed to the cloud  by combining bridging function

## Scene description

Assuming we have an EMQX server'emqx1'and a Mosquitto server, we need to create a bridge on Mosquitto to forward all ''sensor" topic messages to the'emqx1' server and subscribe to all "control" topics from EMQX.


![Artboard.jpg](https://static.emqx.net/images/7a8cbb9dec7ef185338b5e577861b627.jpg)


**EMQX**  

| Node  |      Node name      | Listening port |
| :---: | :-----------------: | :------------: |
| emqx1 | emqx1@192.168.1.100 |      1883      |

**Mosquitto**

|    Address    | Listening port |
| :-----------: | :------------: |
| 192.168.1.101 |      1883      |

## Configure  Mosquitto MQTT server

Configuring Mosquitto's bridging requires modifying the `mosquitto.conf` file after installation. For each bridge, the basic content that needs to be configured is:

- the address and port of the remote EMQX server;
- MQTT protocol parameters, such as protocol version, keepalive, clean_session, etc. (if not configured, the default value is used);
- Client login information required by EMQX;
- the topic of the message that needs to be bridged;
- Configure bridging topic mapping (no mapping by default).

### Create a new MQTT bridge

Open the `mosquitto.conf` file and add a `connection` to create a new bridge. The string after the `connection` keyword is also the client id used on the remote node:

```
connection emqx1
```

### Configure the address and port of the bridged remote node

```
address 192.168.1.100:1883
```

### Configure MQTT protocol version

The [MQTT protocol](https://www.emqx.com/en/mqtt) version used by Mosquitto bridge defaults to 3.1, and the 3.1.1 protocol needs to be specified in the configuration for use.

```
bridge_protocol_version mqttv311
```

### Configure the remote node username

```
remote_username user
```

### Configure the remote node password

```
remote_password passwd
```

### Specify MQTT topics that need to be bridged

The configuration format of the bridged topic is `topic topic mode direction QoS local prefix remote prefix`, which defines the rules for bridging forwarding and receiving. among them:

- The topic mode specifies the topics that need to be bridged, supporting wildcards;
- The direction can be in, out or both
- QoS is the QoS level of the bridge. If not specified, the original QoS of the forwarded message is used.
- Local and remote prefixes are used for topic mapping, with prefixes on the topic of the forwarded and received messages so that the application can identify the source of the message.

The following configuration example adds two bridging rules:

```
topic sensor/# out 1
topic control/# in 1
```

After the configuration is complete, Mosquitto  needs to be restarted to make the bridge configuration take effect.

## Configuring the EMQX MQTT server

After the EMQX MQTT server is installed, in order to make the Mosquitto bridge accessible, it is necessary to decide whether to configure the corresponding user certification and authentication information. Or in the experimental phase, in order to simplify testing,  anonymous login is allowed and acl_nomatch can skip certification and authentication.

## Test configuration

We use the `mosquitto_sub` and `mosquitto_pub` tools to test if the bridging configuration was successful.

### Test the out direction of the bridge

Subscribe to the 'sensor/#' topic on 'emqx1', which will receive data reported by Mosquitto:

```
$ mosquitto_sub -t "sensor/#" -p 1883 -d -q 1 -h 192.168.1.100

Client mosqsub|19324-Zeus- sending CONNECT
Client mosqsub|19324-Zeus- received CONNACK
Client mosqsub|19324-Zeus- sending SUBSCRIBE (Mid: 1, Topic: sensor/#, QoS: 1)
Client mosqsub|19324-Zeus- received SUBACK
Subscribed (mid: 1): 1
```

Post a message on Mosquitto:

```
mosquitto_pub -t "sensor/1/temperature" -m "37.5" -d -h 192.168.1.101 -q 1
Client mosqpub|19325-Zeus- sending CONNECT
Client mosqpub|19325-Zeus- received CONNACK
Client mosqpub|19325-Zeus- sending PUBLISH (d0, q1, r0, m1, 'sensor/1/temperature', ... (4 bytes))
Client mosqpub|19325-Zeus- received PUBACK (Mid: 1)
Client mosqpub|19325-Zeus- sending DISCONNECT
```

This message should be received on 'emqx1':

```
Client mosqsub|19324-Zeus- received PUBLISH (d0, q1, r0, m1, 'sensor/1/temperature', ... (4 bytes))
Client mosqsub|19324-Zeus- sending PUBACK (Mid: 1)
37.5
```



### Test the in direction of the bridge

Subscribe to the 'control/#' topic on Mosquitto, which will receive messages posted on EMQX:

```
$ mosquitto_sub -t "control/#" -p 1883 -d -q 1 -h 192.168.1.101
Client mosqsub|19338-Zeus- sending CONNECT
Client mosqsub|19338-Zeus- received CONNACK
Client mosqsub|19338-Zeus- sending SUBSCRIBE (Mid: 1, Topic: control/#, QoS: 1)
Client mosqsub|19338-Zeus- received SUBACK
Subscribed (mid: 1): 1
```

Post a message on 'emqx1', the message will be passed on 'emqx1' and bridged to Mosquitto local:

```
$ mosquitto_pub -t "control/1" -m "list_all" -d -h 192.168.1.100 -q 1
Client mosqpub|19343-Zeus- sending CONNECT
Client mosqpub|19343-Zeus- received CONNACK
Client mosqpub|19343-Zeus- sending PUBLISH (d0, q1, r0, m1, 'control/1', ... (8 bytes))
Client mosqpub|19343-Zeus- received PUBACK (Mid: 1)
Client mosqpub|19343-Zeus- sending DISCONNECT
```

This message should be received on Mosquitto:

```
Client mosqsub|19338-Zeus- received PUBLISH (d0, q1, r0, m2, 'control/1', ... (8 bytes))
Client mosqsub|19338-Zeus- sending PUBACK (Mid: 2)
list_all
```


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
