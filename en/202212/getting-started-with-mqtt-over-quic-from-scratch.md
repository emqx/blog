## Preface

QUIC([RFC9000](https://datatracker.ietf.org/doc/html/rfc9000)) is the underlying transport protocol of the next-generation internet protocol HTTP/3. Compared with TCP/TLS protocols, it **provides an efficient and flexible transport layer for the mobile internet that reduces network overhead and messaging latency.**

EMQX 5.0 is the first innovative product to introduce QUIC to MQTT. We found that the features of QUIC were perfectly suitable for some scenarios in the IoT when we were supporting customers and developing technologies, so we attempted to replace the transport layer of MQTT with QUIC, which led to the MQTT over QUIC.

As described in the [previous article](https://www.emqx.com/en/blog/mqtt-over-quic), the QUIC has the features of low network overhead and the capability of multiplexing which give it a great advantage in IoT scenarios where networks are unstable and connections switch frequently. Test data show that MQTT over QUIC can effectively enhance the user’s experience in spotty networks with weak signals and unstable connections based on QUIC's ability of 0 RTT/1 RTT reconnect/new.

As the [Foundational Sponsor](https://www.emqx.com/en/news/emq-becomes-oasis-opens-newest-foundational-sponsor) of OASIS, a world-renowned open source and open standards organization, EMQ actively supports the standardization of MQTT over QUIC. Some customers have already tried to use this new feature, and we have received good feedback. This article will help you to get started exploring the MQTT Over QUIC feature in EMQX 5.0.

## Enable MQTT over QUIC

The MQTT over QUIC is supported from EMQX 5.0. Please download and install the latest version of EMQX here: [https://www.emqx.com/en/try?product=broker](https://www.emqx.com/en/try?product=broker) 

This is an experimental feature. For CentOS 6, macOS, and Windows, you need to compile QUIC from the source. Please set BUILD_WITH_QUIC=1 while compiling. 

MQTT over QUIC is disabled by default. You can enable it manually following the steps below.

1. Open the configuration file etc/emqx.conf, and uncomment the listeners.quic.default block (add it manually if it does not exist):

   ```
   # etc/emqx.conf
   listeners.quic.default {
     enabled = true
     bind = "0.0.0.0:14567"
     max_connections = 1024000
     keyfile = "etc/certs/key.pem"
     certfile = "etc/certs/cert.pem"
   }
   ```

2. This configuration enables the QUIC listener on UDP port 14567. After it has been successfully saved, restart EMQX to activate the configuration.

   You can also enable the QUIC feature with env vars while starting the EMQX：

   ```
   EMQX_LISTENERS__QUIC__DEFAULT__keyfile="etc/certs/key.pem" \
   EMQX_LISTENERS__QUIC__DEFAULT__certfile="etc/certs/cert.pem" \
   EMQX_LISTENERS__QUIC__DEFAULT__ENABLED=true
   ```

3. Uses the emqx_ctl listeners command to see the status of the QUIC listener:

   ```
   > emqx_ctl listeners
   quic:default
   listen_on       : :14567
   acceptors       : 16
   proxy_protocol : undefined
   running         : true
   ssl:default
   listen_on       : 0.0.0.0:8883
   acceptors       : 16
   proxy_protocol : false
   running         : true
   current_conn   : 0
   max_conns       : 512000
   ```

   You can also use Docker for a quick experience, setting UDP port 14567 as the QUIC port through an environment variable:

   ```
   docker run -d --name emqx \
   -p 1883:1883 -p 8083:8083 \
   -p 8084:8084 -p 8883:8883 \
   -p 18083:18083 \
   -p 14567:14567/udp \
   -e EMQX_LISTENERS__QUIC__DEFAULT__keyfile="etc/certs/key.pem" \
   -e EMQX_LISTENERS__QUIC__DEFAULT__certfile="etc/certs/cert.pem" \
   -e EMQX_LISTENERS__QUIC__DEFAULT__ENABLED=true \
   emqx/emqx:5.0.10
   ```

## Clients and tools for MQTT over QUIC

The clients and the tools for MQTT over QUIC are not feature-complete as regular MQTT client.

On the basis of scenarios suitable for the MQTT, we are planning to provide clients in multiple languages, such as C, Java, Python, and Golang. These clients will be developed in priority order, so that the appropriate scenarios, such as the embedded hardware, will be able to benefit from QUIC as quickly as possible.

### **Available client SDKs**

- [NanoSDK](https://github.com/nanomq/NanoSDK/): An MQTT SDK based on C, released by the NanoMQ team at EMQ. In addition to MQTT over QUIC, it also supports other protocols, such as WebSocket and nanomsg/SP.
- [NanoSDK-Python](https://github.com/wanghaEMQ/pynng-mqtt): The Python binding of NanoSDK.
- [NanoSDK-Java](https://github.com/nanomq/nanosdk-java): The Java JNA binding of NanoSDK.
- [emqtt](https://github.com/emqx/emqtt): A MQTT client library, developed in Erlang, supporting QUIC.

In addition to a client library, EMQ provides the capability of bridging for MQTT over QUIC in the edge computing product, NanoMQ. NanoMQ can be used to bridge the data from the edge to the cloud through QUIC, so that MQTT over QUIC can be used with zero coding.

### **Problems and solutions**

Many carriers have specific network rules for packets from UDP, which can lead to failure to connect to QUIC or packet drop since the QUIC is UDP-based.

Therefore, the MQTT over QUIC client is designed with the ability to fall back: you can develop services through unified APIs, while the transport layer can be changed in real time according to the network condition. If QUIC is not available, it switches automatically to TCP/TLS 1.2 to make sure that the services can be properly used in different networks.

## Connect MQTT over QUIC via NanoSDK

[NanoSDK](https://github.com/nanomq/NanoSDK/) is based on the MsQuic project. It's the first SDK for MQTT over QUIC in C, and it's fully compatible with EMQX 5.0. The key features of the NanoSDK include: the asynchronous I/O, the mapping of MQTT connection to a QUIC stream, the 0RTT handshake with low latency, and the parallel processing of multiple cores.

![NanoSDK](https://assets.emqx.com/images/4b4205bb4c8400b41c76829fc8b2c617.png)

### NanoSDK examples

The API follows a similar style to the previous one. You can create an MQTT client on the basis of QUIC in one line of code:

```
## Create MQTT over Quic client with NanoSDK
nng_mqtt_quic_client_open(&socket, url);
```

For the sample code please refer to: [https://github.com/nanomq/NanoSDK/tree/main/demo/quic_mqtt](https://github.com/nanomq/NanoSDK/tree/main/demo/quic_mqtt).

After the compiling is completed, you will be able to run the command below to connect to port 14567 for testing.

```
quic_client sub/pub mqtt-quic://54.75.171.11:14567 topic msg
```

NanoSDK also provides Java binding and Python binding. For examples please refer to: [MqttQuicClient.java](https://github.com/nanomq/nanosdk-java/blob/main/demo/src/main/java/io/sisu/nng/demo/quicmqtt/MqttQuicClient.java) and [mqttsub.py](https://github.com/wanghaEMQ/pynng-mqtt/blob/master/examples/mqtt_tcp_sub.py).

## Bridge MQTT 3.1.1/5.0 and MQTT over QUIC via NanoMQ

[NanoMQ](https://nanomq.io/) is an ultra-lightweight, high-performance, and cross-platform MQTT broker for IoT edge. It can be used as a message bus for many protocols, and it can bridge the MQTT and the MQTT over QUIC. It relays MQTT packets over QUIC protocol, which are sent to the EMQX on the cloud. Therefore, the edge devices that can't be integrated with the MQTT over QUIC SDK or can’t find the appropriate MQTT over QUIC SDK and the embedded devices whose firmware can't be modified can take advantage of the [QUIC protocol](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov) in IoT scenarios. This will be very convenient for the user.

![NanoMQ](https://assets.emqx.com/images/29f87fcca9842bc1ffc22422178c6ca6.png)

Since NanoMQ has the capability to handle many protocols, it is very useful in IoT scenarios, where data is synchronized with the cloud services. It can be used as the message bus and storage system for the common broker/brokerless messaging protocols, such as HTTP, MQTT 3.1.1/5.0, WebSocket, nanomsg/nng, and ZeroMQ. NanoMQ's 'actor', a powerful and built-in model for the processing of messages, converts the data of these protocols into standard messages from the MQTT protocol, and they are sent to the Cloud through QUIC.

This fully uses the capacities of the MQTT over QUIC, like 0RTT fast reconnection, and passive address switching, to solve common problems in the IoT connection, such as network roaming, the weak transmission of networks, and the head-of-line blocking of TCP. You can also redirect, cache, or persist data through the Rule Engine of NanoMQ.

Based on the Cloud-Edge messaging architecture of EMQX+NanoMQ, users can quickly and cheaply collect and synchronize data anytime and anywhere in the Pan IoT scenarios.

It is worth mentioning that NanoMQ can switch automatically to standard MQTT over TCP/TLS when the QUIC connection fails, to make sure your device is not affected by the network environment.

### NanoMQ bridging example

Download and install NanoMQ:

```
git clone https://github.com/emqx/nanomq.git
cd nanomq ; git submodule update --init --recursive

mkdir build && cd build
cmake -G Ninja -DNNG_ENABLE_QUIC=ON ..
sudo ninja install
```

After compiling and installing NanoMQ which enabled QUIC, you can configure MQTT over QUIC and related topics in the configuration file /etc/nanomq.conf. Using mqtt-quic as the URL prefix means using QUIC as the transport layer for MQTT:

```
## Bridge address: host:port .
##
## Value: String
## Example: ## Example: mqtt-tcp://broker.emqx.io:1883 (This is standard MQTT over TCP)
bridge.mqtt.emqx.address=mqtt-quic://54.75.171.11:14567
```

### MQTT over QUIC CLI tools

NanoMQ also provides nanomq_cli which contains the client tools for MQTT over QUIC for users to test the MQTT over QUIC of EMQX 5.0:

```
nanomq_cli quic --help
Usage: quic conn <url>
       quic sub  <url> <qos> <topic>
       quic pub  <url> <qos> <topic> <data>

## subscribe example
nanomq_cli quic sub mqtt-quic://54.75.171.11:14567 2 msg
```

In conclusion, you can integrate NanoSDK directly into your projects, or use the client tools, both of which be able to connect the devices to a cloud through QUIC.

## Use emqtt-bench for performance testing of QUIC

[emqtt-bench](https://github.com/emqx/emqtt-bench) is a benchmarking tool for performance testing of MQTT, which supports QUIC. We used it to conduct the performance test [MQTT over QUIC vs TCP/TLS](https://www.emqx.com/en/blog/mqtt-over-quic#quic-vs-tcp-tls-测试对比). It can be used to benchmark applications or verify the performance and benefits of MQTT over QUIC in real world.

### Compile emqtt-bench

Compiling requires Erlang. Take macOS for example, to install Erlang and Coreutils:

```
brew install coreutils
brew install erlang@24
```

Compile emqtt-bench from source

```
git clone https://github.com/emqx/emqtt-bench.git
cd emqtt-bench
CMAKE_BUILD_TYPE=Debug BUILD_WITH_QUIC=1 make
```

The following prompts are displayed for a successful compiling:

```
...
===> Warnings generating release:
*WARNING* Missing application sasl. Can not upgrade with this release
===> Release successfully assembled: _build/emqtt_bench/rel/emqtt_bench
===> Building release tarball emqtt_bench-0.3+build.193.ref249f7f8.tar.gz...
===> Tarball successfully created: _build/emqtt_bench/rel/emqtt_bench/emqtt_bench-0.3+build.193.ref249f7f8.tar.gz
```

> The following errors may occur, which can be ignored:

```
/Users/patilso/emqtt-bench/scripts/rename-package.sh: line 9: gsed: command not found
/Users/patilso/emqtt-bench/scripts/rename-package.sh: line 9: gsed: command not found
/Users/patilso/emqtt-bench/scripts/rename-package.sh: line 9: gsed: command not found
/Users/patilso/emqtt-bench/scripts/rename-package.sh: line 9: gsed: command not found
```

### Test QUIC

Go to the output directory of compiling:

```
cd _build/emqtt_bench/rel/emqtt_bench/bin
```

You can use QUIC through the option --quic to initiate a connection and to subscribe, here 10 clients subscribe to topic t/1.

```
./emqtt_bench sub -p 14567 --quic -t t/1 -c 10
```

Open a new window, and also use QUIC to connect and test the Publish.

```
./emqtt_bench pub -p 14567 --quic -t t/1 -c 1
```

A performance test will be carried out for '1 pub 10 sub':

![performance test](https://assets.emqx.com/images/798b7d952bbc2cfa23bfbfe90e46449f.png)

Check the usage of local UDP port 14567:

```
$ lsof -nP -iUDP | grep 14567

com.docke 29372 emqx   76u  IPv6 0xea2092701c033ba9      0t0  UDP *:14567
beam.smp  50496 emqx   39u  IPv6 0xea2092701c014eb9      0t0  UDP [::1]:52335->[::1]:14567
beam.smp  50496 emqx   40u  IPv6 0xea2092701c017689      0t0  UDP [::1]:56709->[::1]:14567
beam.smp  50496 emqx   41u  IPv6 0xea2092701c0151c9      0t0  UDP [::1]:52175->[::1]:14567
beam.smp  50496 emqx   42u  IPv6 0xea2092701c0157e9      0t0  UDP [::1]:54050->[::1]:14567
beam.smp  50496 emqx   43u  IPv6 0xea2092701c015af9      0t0  UDP [::1]:58548->[::1]:14567
beam.smp  50496 emqx   44u  IPv6 0xea2092701c013639      0t0  UDP [::1]:52819->[::1]:14567
beam.smp  50496 emqx   45u  IPv6 0xea2092701c016119      0t0  UDP [::1]:57351->[::1]:14567
beam.smp  50496 emqx   46u  IPv6 0xea2092701c017999      0t0  UDP [::1]:52353->[::1]:14567
beam.smp  50496 emqx   47u  IPv6 0xea2092701c017ca9      0t0  UDP [::1]:57640->[::1]:14567
beam.smp  50496 emqx   48u  IPv6 0xea2092701c014ba9      0t0  UDP [::1]:55992->[::1]:14567
beam.smp  51015 emqx   39u  IPv6 0xea2092701c017069      0t0  UDP [::1]:64686->[::1]:14567
```

To learn more about the emqtt-bench, please refer to the help:

```
./emqtt_bench pub –help

./emqtt_bench conn –help

./emqtt_bench --help
```

## Summary

That's a first glance at the MQTT over QUIC. As you can tell, the client libraries and EMQX are capable of achieving the same experience as MQTT at the API level and management level. The ability to take full advantage of the QUIC feature by simply replacing the transport layer is a great convenience for developers and has contributed to the popularity of MQTT over QUIC. Besides, NanoMQ's support for MQTT over QUIC bridging also provides another flexible solution.

With MQTT over QUIC being used widely in the real world, users can also experience advanced features such as congestion control, smooth migration of connections, end-to-end encryption, and low-latency handshake. Stay tuned for more detailed explanations of the techniques and best practices behind these features.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
