With the progress of the 5G network technology, the IoT world is also developing rapidly. Today, countless IoT devices are shining in all corners of the world.

However, unlike the traditional Internet, end-to-end communication is always a difficult part of the IoT business. The differences in the IoT communication protocols used will cause a huge gap in communication between devices. It is just like people cannot communicate properly with each other if they speak different languages.

![WechatIMG14.png](https://assets.emqx.com/images/d1206132ad1e17d5ab2b8f50eb5cf9ce.png)
As an IoT message broker, EMQX Broker is on a mission to enable these devices to provide communication. Therefore, we have developed many IoT protocol plugins. Whether you prefer TCP-based long links such as MQTT, UDP-based connectionless such as [CoAP](https://www.emqx.com/en/blog/iot-protocols-mqtt-coap-lwm2m), or private protocols, in the world of EMQX we can help you find a 'soulmate' who can read you.

> About the MQTT protocol: [https://www.emqx.com/en/mqtt](https://www.emqx.com/en/mqtt-guide)

**This article will show you a「date」between MQTT client and CoAP client in the EMQX world**



### Step 1: Enable EMQX Broker, open the CoAP plugin and ensure that the plugin is running.

You can find help on how to install and run EMQX Broker [here](https://www.emqx.io/docs/en/latest/).

Open Dashboard, click on Plugin on the left, search for CoAP on the right, and click `Start` to run the `CoAP Plugin` (default port 5683).
![WechatIMG13.png](https://assets.emqx.com/images/3358349652fcf16052d5354bf8fa543f.png)
	

In the `PUB/SUB` model of MQTT, a `topic` is used as a bridge between devices to achieve end-to-end communication. We use the two `topics` `coap_to_mqtt` and `mqtt_to_coap`, as the message `topic` from CoAP to MQTT, and the message `topic` from MQTT to CoAP, respectively.

Both MQTT and CoAP support a publish/subscribe mechanism, with MQTT relying on the Topic field in the message, and the CoAP protocol class is based on a REST design. In the EMQX Broker:

`PUT`  and `GET`: as `Publish` and ` Subscribe`.

`URI`: path map topic, the rule is:  `topic_name` is converted to the path `/mqtt/topic_name`, i.e. `topic` plus the `/mqtt/` prefix.

`URI Query`: the path parameter carries information about the client, including the client id, username, and password.

```shell
# Example
put "coap://host:port/mqtt/$topic?c=$client&u=$username&p=$password"
get "coap://host:port/mqtt/$topic?c=$client&u=$username&p=$password"

# -m get | put | post ...
# method request method

# coap://host:port
# CoAP protocol path format, host and port, fill in the IP of the EMQX Broker deployment, and the port of the CoAP plugin (default 5683)

# /mqtt/$topic 
# Refers to the topic of mqtt and needs to be converted, rule:
# in CoAP, topic_name needs to be /mqtt/topic_name

# URI Query
# c :client id
# u :username
# p :password
```

So far, the preparations have been completed.



### Step 2：Invite the first participant, the MQTT client

Connect the [MQTT client - MQTTX](https://mqttx.app/) to your EMQX Broker and subscribe to the topic `coap_to_mqtt` for it.

![image20210410173501967.png](https://assets.emqx.com/images/776af3a1e1205e1fd99b33e695f876ca.png)


### Step 3：Invite the second participant, the CoAP client

The CoAP client used in this article is [libcoap](https://github.com/obgm/libcoap).

```sh
# Install libcoap first
# Download using git, or use the download link https://github.com/obgm/libcoap/archive/refs/tags/v4.2.1.zip
git clone https://github.com/obgm/libcoap.git
# If you download using the download link, unzip
# unzip libcoap-4.2.1.zip

# Go to the libcoap file directory
cd libcoap
# Switching to a stable version, the author is using v4.2.1
# If you use the download link in this article to download, there is no need to switch versions.
git checkout v4.2.1
# Install configuration
./autogen
# You may encounter some missing dependencies during the ./autogen process (e.g. autoconf and automake), just follow the instructions to install the dependencies.
./configure --enable-documentation=no --enable-tests=no
# Packaging
make
```



### Step 4：Start communication

After  the installation is complete, the CoAP client PUT message to the `coap_to_mqtt` topic.

```shell
# CoAP client sends the message 'hello EMQX world,  I am CoAP'，and topic is 'coap_to_mqtt'
./examples/coap-client -m put -e "hello EMQX world, I am CoAP" "coap://127.0.0.1/mqtt/coap_to_mqtt?c=coap20211&u=tom&p=secret"
# Replace 127.0.0.1 in the command with the address of your EMQX Broker deployment
```

We can see that MQTTX has received a greeting from CoAP.

![WechatIMG12.png](https://assets.emqx.com/images/15c80f669399ee8a47ea8a0fc8e43770.png)

Now subscribe to the `mqtt_to_coap` theme for CoAP terminals.

```shell
# CoAP client subscribes to the topic 'mqtt_to_coap'. -s 20 means that the subscription is maintained for 20 seconds 
./examples/coap-client -m get -s 20 "coap://127.0.0.1/mqtt/mqtt_to_coap?c=client1&u=tom&p=secret"
```

MQTTX sends `hello CoAP, I am MQTT, welcome to EMQX Wrold!`  to the topic `mqtt_to_coap`.

![WechatIMG11.png](https://assets.emqx.com/images/1b3ace0680fef3e3d088241a01fe7cba.png)

CoAP has also received a response from MQTT.

```shell
./examples/coap-client -m get -s 20 "coap://127.0.0.1/mqtt/mqtt_to_coap?c=client1&u=tom&p=secret"
hello CoAP, I am MQTT, welcome to EMQX Wrold!
```



**So far, we have completed an end-to-end communication process using the EMQX Broker as the medium, allowing MQTT and CoAP to successfully 'date' in the EMQX world.**



In EMQX World, not only are MQTT, CoAP, LwM2M, JT808, and much more different IoT protocol plugins which will be supported in the future, but we also provide you with [the development template for plugins](https://github.com/emqx/emqx-plugin-template). We expect that all IoT devices will meet here and collide to create dazzling sparks that will illuminate the world of IoT.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
