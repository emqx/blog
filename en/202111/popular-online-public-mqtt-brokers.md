Many MQTT projects and IoT services provide [online public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker). Users can directly use them for MQTT learning, testing, prototyping, and even small-scale applications without self-deployment, convenient and fast with time and energy saved.

However, due to different locations, network environments, and server loads, each public broker’s stability and message transmission delay are also different. Although almost all service providers declare that they are not responsible for the stability and security of their free services, users need to consider these factors when using them.

Therefore, this article sorts out some popular free online MQTT brokers, evaluates and compares them through accessibility, network delay, small-scale performance testing, and actual message transmission delay. We hope to provide a reference for your choice.


## Test object

This article selects the following commonly used public MQTT brokers:

| Name           | Broker Address            | TCP  | TLS        | WebSocket |
| :------------- | :------------------------ | :--- | :--------- | :-------- |
| EMQX (Global) | `broker.emqx.io`          | 1883 | 8883       | 8083,8084 |
| EMQX (CN)     | `broker-cn.emqx.io`       | 1883 | 8883       | 8083,8084 |
| Eclipse        | `mqtt.eclipseprojects.io` | 1883 | 8883       | 80, 443   |
| Mosquitto      | `test.mosquitto.org`      | 1883 | 8883, 8884 | 80, 443   |
| HiveMQ         | `broker.hivemq.com`       | 1883 | N/A        | 8000      |

### EMQX

It is a free online [MQTT 5 broker](https://www.emqx.io/) provided by [EMQX Cloud](https://www.emqx.com/en/cloud). There are two access points provided, Global and CN, of which EMQX (Global) is deployed in AWS, Oregon, USA, and EMQX (CN) is deployed in Tencent Cloud, Shanghai.

Both access points are EMQX clusters composed of 2 nodes. Later, more nodes can be automatically added according to the actual access volume and load. According to the background display, the server is based on [EMQX Enterprise](https://www.emqx.com/en/products/emqx) 4.2.6, and the current running time is 128 days.

> Note: The two access points of EMQX (Global) and EMQX (CN) do not communicate with each other.

Related introduction: [Free Public MQTT 5 Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) 

### Eclipse

It is a free online MQTT broker provided by Eclipse IoT. The resolved IP shows that it is deployed in Azure, Virginia, USA. It’s worth noting that the previous access address of the server has always been `mqtt.eclipse.org`. For some reason, it has been changed to the current access address. At the time of writing this article, I used the old address and failed to access it. At one time, I thought the server had been stopped. Finally, when I accessed the original access point through HTTP, I found that 301 permanent redirection had been made.

According to the query of the `$SYS/#` system topic, the server is based on the Mosquitto 2.0.12, and the current running time is 71227 seconds. It is suspected that the service was restarted a day ago.

Related introduction: [mqtt.eclipseprojects.io](https://mqtt.eclipseprojects.io/) 

### Mosquitto

It is a free online MQTT broker provided by the Mosquitto community, and the resolved IP shows that it is deployed in the OVH, Roubaix region of French. In the test, it was found that the network delay of the access point is relatively high under normal conditions. Still, fortunately, the packet loss rate is relatively low, and connection failures may occur in some periods.

According to the query of the `$SYS/#` system topic, the server is based on the Mosquitto 2.0.12, and the current running time is 28519 seconds. It is suspected that the service was restarted within one day.

Related introduction: [test.mosquitto.org](https://test.mosquitto.org/) 

### HiveMQ

It is a free online MQTT broker provided by HiveMQ, and the resolved IP shows that it is deployed in the AWS, Frankfurt, Germany.

Because its `$SYS/#` system topic cannot be subscribed, it is impossible to get the type of Broker providing the service, the specific version, and the current running time.

Related introduction: [mqtt-dashboard.com](http://www.mqtt-dashboard.com/) 

## Test environment

- Network: US, AWS Oregon
- Operating system: macOS 10.15.7

> Note: Due to different locations, the network environment will be different, which may lead to differences in the test results of this article.

## Accessibility test

In this part, We used the [MQTT client tool - MQTT X](https://mqttx.app/) for this test. We try to establish a connection through TCP 1883. After repeated testing, all servers can be accessed. The overall results are as follows:

| Name      | Broker Address            | TCP  | Available |
| :-------- | :------------------------ | :--- | :-------- |
| EMQX     | `broker.emqx.io`          | 1883 | YES       |
| EMQX(CN) | `broker-cn.emqx.io`       | 1883 | YES       |
| Eclipse   | `mqtt.eclipseprojects.io` | 1883 | YES       |
| Mosquitto | `test.mosquitto.org`      | 1883 | YES       |
| HiveMQ    | `broker.hivemq.com`       | 1883 | YES       |

![MQTT X](https://assets.emqx.com/images/85637f1261315f2f218aadd671c8666e.png)

### Test Data

MQTT X has the function of connection, import and export. The following is the connection data used in the test of this article, which can be imported into MQTT X through data recovery.

- [MQTTX-backup-free-public-mqtt-broker.json](https://github.com/wivwiv/mqtt-explore/blob/master/MQTTX-backup-free-public-mqtt-broker.json)

![MQTT X Data recovery](https://assets.emqx.com/images/9c4fdada948c4cd3cab3dd1335bc217d.png)

## International network delay test

We check the network connectivity and network delay through network access. Because some services have disabled the ICMP protocol, and the network conditions in various places are different, the WebSocket address is used here. With the help of the HTTP speed function of the popular domestic speed measurement tool Webmaster Tools, we conduct the test:

| Name      | HTTP address (Click to test)                                 | WebSocket |
| :-------- | :----------------------------------------------------------- | :-------- |
| EMQX     | [http://broker.emqx.io:8083/mqtt](https://tool.chinaz.com/speedworld/http://broker.emqx.io:8083/mqtt) | 8083      |
| EMQX(CN) | [http://broker-cn.emqx.io:8083/mqtt](https://tool.chinaz.com/speedworld/broker-cn.emqx.io:8083/mqtt) | 8083      |
| Eclipse   | [http://mqtt.eclipseprojects.io/mqtt](https://tool.chinaz.com/speedworld/mqtt.eclipseprojects.io/mqtt) | 80        |
| Mosquitto | [http://test.mosquitto.org/mqtt](https://tool.chinaz.com/speedworld/test.mosquitto.org/mqtt) | 80        |
| HiveMQ    | [http://broker.hivemq.com:8000/mqtt](https://tool.chinaz.com/speedworld/broker.hivemq.com:8000/mqtt) | 8000      |

### Test result

- Resolution time: the time required for DNS resolution
- Connection time: the time required to establish a TCP connection

| **EMQX**       | **Resolution time** | **Connection time** |
| :-------------- | :------------------ | :------------------ |
| Los Angeles     | 15ms                | 33ms                |
| Tokyo           | -                   | -                   |
| China Hong Kong | -                   | -                   |
| Singapore       | 55ms                | 201ms               |
| South Korea     | -                   | -                   |
| Germany         | 15ms                | 160ms               |

| **EMQX(CN)**   | **Resolution time** | **Connection time** |
| :-------------- | :------------------ | :------------------ |
| Los Angeles     | <1ms                | 156ms               |
| Tokyo           | <1ms                | 90ms                |
| China Hong Kong | <1ms                | 35ms                |
| Singapore       | <1ms                | 102ms               |
| South Korea     | -                   | -                   |
| Germany         | 17ms                | 209ms               |

| **Mosquitto**   | **Resolution time** | **Connection time** |
| :-------------- | :------------------ | :------------------ |
|                 | <1ms                | 434ms               |
| Tokyo           | <1ms                | 703ms               |
| China Hong Kong | <1ms                | 629ms               |
| Singapore       | <1ms                | 538ms               |
| South Korea     | <1ms                | 817ms               |
| Germany         | 2ms                 | 59ms                |

| Eclipse         | **Resolution time** | **Connection time** |
| :-------------- | :------------------ | :------------------ |
| Los Angeles     | <1ms                | 72ms                |
| Tokyo           | <1ms                | 155ms               |
| China Hong Kong | 16ms                | 218ms               |
| Singapore       | <1ms                | 237ms               |
| South Korea     | <1ms                | 225ms               |
| Germany         | 184ms               | 88ms                |

| **HiveMQ**      | **Resolution time** | **Connection time** |
| :-------------- | :------------------ | :------------------ |
| Los Angeles     | 5ms                 | 151ms               |
| Tokyo           | 2ms                 | 248ms               |
| China Hong Kong | 7ms                 | 256ms               |
| Singapore       | 7ms                 | 194ms               |
| South Korea     | -                   | -                   |
| Germany         | 2ms                 | 2ms                 |


## Small-scale performance test

With the help of the open-source MQTT performance test tool [emqtt-bench](https://github.com/emqx/emqtt-bench), we test whether the client's [Pub/Sub](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) has a rate limit.

**For practicality considerations**, this test is not to explore the upper rate limit of each access point, but to consider that each access point can meet the conventional use intensity. The scenario designed in this round is that a single client’s Sub/Pub message is 1000 msg/s for 1 minute, and the message size is 256 Bytes. Then, we record whether each access point meets the standard and whether the speed is limited. The following figure shows the test architecture:

![test architecture](https://assets.emqx.com/images/0030af57d2d50b9a87ecf27a72ddfe5c.png)

After emqtt-bench is ready, each of the following Sub/Pub commands is executed in a different window:

| Name      | Broker address            | TCP  | Whether reach the standard(Pub)     | Whether reach the standard(Sub)        |
| :-------- | :------------------------ | :--- | :---------------------------------- | :------------------------------------- |
| EMQX     | `broker.emqx.io`          | 1883 | YES                                 | YES                                    |
| EMQX(CN) | `broker-cn.emqx.io`       | 1883 | YES                                 | YES                                    |
| Eclipse   | `mqtt.eclipseprojects.io` | 1883 | YES                                 | YES                                    |
| Mosquitto | `test.mosquitto.org`      | 1883 | The rate fluctuates around 50 msg/s | The rate fluctuates between 0-50 msg/s |
| HiveMQ    | `broker.hivemq.com`       | 1883 | YES                                 | The rate is stable at around 50 msg/s  |

```bash
# EMQX
## Sub
./emqtt_bench sub -t t/1 -c 1 -h broker.emqx.io
## Pub
./emqtt_bench pub -t t/1 -c 1 -h broker.emqx.io -I 1

# EMQX CN
## Sub
./emqtt_bench sub -t t/1 -c 1 -h broker-cn.emqx.io
## Pub
./emqtt_bench pub -t t/1 -c 1 -h broker-cn.emqx.io -I 1

# Eclipse
## Sub
./emqtt_bench sub -t t/1 -c 1 -h mqtt.eclipseprojects.io
## Pub
./emqtt_bench pub -t t/1 -c 1 -h mqtt.eclipseprojects.io -I 1


# Mosquitto
## Sub
./emqtt_bench sub -t t/1 -c 1 -h test.mosquitto.org
## Pub
./emqtt_bench pub -t t/1 -c 1 -h test.mosquitto.org -I 1

# HiveMQ
## Sub
./emqtt_bench sub -t t/1 -c 1 -h broker.hivemq.com
## Pub
./emqtt_bench pub -t t/1 -c 1 -h broker.hivemq.com -I 1
```

 

## Actual message transmission delay test

Purpose: Test the time required for the message to transmit from the Pub to the Sub, sample and analyze the transmission stability and average time required.

Test step: The client connects to the public server and publishes a time-stamped message every 5 seconds. After the subscriber receives the message, the timestamp in the message is subtracted from the current timestamp, and the message delay is calculated and recorded in the database. Sampling and analysis are performed after 30 minutes of statistics.

The test model is as follows:

![mqtt broker test model](https://assets.emqx.com/images/4fea7f9e1f965c546b3027d98f167394.png)

Test code: [free-online-public-broker-test.js](https://github.com/wivwiv/mqtt-explore/blob/master/free-online-public-broker-test.js)

### Time delay history

Count the client message delay and remove data with large errors (>5000ms):

![MQTT broker Time delay history](https://assets.emqx.com/images/73dd2167a1b6a8bd67b2b6e17f7a0817.png)

### Average delay

| Name      | Broker Address            | TCP  | Average delay |
| :-------- | :------------------------ | :--- | :------------ |
| EMQX     | `broker.emqx.io`          | 1883 | 207 ms        |
| EMQX(CN) | `broker-cn.emqx.io`       | 1883 | 164 ms        |
| Eclipse   | `mqtt.eclipseprojects.io` | 1883 | 250 ms        |
| Mosquitto | `test.mosquitto.org`      | 1883 | 378 ms        |
| HiveMQ    | `broker.hivemq.com`       | 1883 | 252 ms        |


## Summary

In several tests, each free online MQTT server has reached a usable level as a whole. However, there are still significant differences between the servers in the specific indicators. There are stability and usability issues like low rate limit, unstable network delay, or even some servers are suspected of having a scheduled restart mechanism, which will bring a bad experience to users even in simple testing and prototyping.

The above content also proves to a certain extent that the relevant performance of the IoT platform is affected by the geographic location of the device. Therefore, the EMQX free online MQTT service that provides nearby access points for users in different regions based on the network of high-quality cloud service providers has certain advantages in comparison, and the test data is relatively leading in all aspects.

We are delighted to see that more and more IoT devices worldwide are connected to the online MQTT server provided by EMQX, and thousands of messages are delivered per second on average. `broker.emqx.io:1883` also appears in various open-source projects and sample codes on GitHub ([https://github.com/search?q=broker.emqx.io&type=Code](https://github.com/search?q=broker.emqx.io&type=Code)).

EMQX online public broker is provided by [EMQX Cloud](https://www.emqx.com/en/cloud). EMQX Cloud is a fully managed cloud-native MQTT messaging service provided by EMQ, which supports commercial-level accessibility and stability. Business users can quickly start projects at zero cost and implement MQTT device access in a simple and fast way by using EMQX Cloud. In the later stage, it can be expanded as needed according to the business development. Users can create access points nearby worldwide and enjoy the 7 * 24 technical support provided by the EMQ professional team.

Whether it is a personal or corporate project, EMQ is committed to providing the most appropriate MQTT messaging service for all kinds of users. If you have any comments or questions when using EMQX, please feel free to give feedback to our team at any time.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
