This month, NanoMQ 0.5.9 was released. In addition to routine bug fixes, we have brought you an efficient and easy-to-use MQTT command-line toolkit based on the MQTT functions of bridging and compatible with native NNG which was developed last month. At the same time, we also continue to fix bugs found and issues reported by users, and actively maintain NanoSDK which is NanoMQ's sister project.

## MQTT command line toolkit

Whether for daily MQTT development and test or performance evaluation of brokers, an easy-to-use and high-performance MQTT command-line toolkits are essential. Based on the previously released NanoSDK, we have developed a complete set of MQTT client tools for the majority of MQTT users, which include MQTT message publishing, subscription and connection.

### MQTT message publishing

#### User guide

```
Usage: nanomq pub { start | stop } <addr> [<topic>...] [<opts>...] [<src>]

<addr> must be one or more of:
  --url <url>                      The url for mqtt broker ('mqtt-tcp://host:port' or 'tls+mqtt-tcp://host:port') 
                                   [default: mqtt-tcp://127.0.0.1:1883]

<topic> must be set:
  -t, --topic <topic>              Topic for publish or subscribe

<opts> may be any of:
  -V, --version <version: 3|4|5>   The MQTT version used by the client [default: 4]
  -n, --parallel                 The number of parallel for client [default: 1]
  -v, --verbose                  Enable verbose mode
  -u, --user <user>                The username for authentication
  -p, --password <password>        The password for authentication
  -k, --keepalive <keepalive>      A keep alive of the client (in seconds) [default: 60]
  -m, --msg <message>              The message to publish
  -C, --count <num>                Max count of publishing message [default: 1]
  -i, --interval <ms>              Interval of publishing message (ms) [default: 0]
  -I, --identifier <identifier>    The client identifier UTF-8 String (default randomly generated string)
  -q, --qos <qos>                  Quality of service for the corresponding topic [default: 0]
  -r, --retain                     The message will be retained [default: false]
  -c, --clean_session <true|false> Define a clean start for the connection [default: true]
  --will-qos <qos>                 Quality of service level for the will message [default: 0]
  --will-msg <message>             The payload of the will message
  --will-topic <topic>             The topic of the will message
  --will-retain                    Will message as retained message [default: false]
  -s, --secure                     Enable TLS/SSL mode
      --cacert <file>              CA certificates file path
      -E, --cert <file>            Certificate file path
      --key <file>                 Private key file path
      --keypass <key password>     Private key password

<src> may be one of:
  -m, --msg  <data>                
  -f, --file <file>
```

#### Example

```
nanomq pub start --url "mqtt-tcp://broker.emqx.io:1883" -t msg -m hello -i 10 -c 10000
```

The NanoMQ Pub tool is used to send a message with a Payload of hello every 10ms to the msg topic of the public MQTT Broker provided by EMQ, and it is stopped when 10,000 messages are sent. In addition, NanoMQ Toolkit can also read data from files and send them, which is convenient for users to customize their own Payloads to simulate business tests.

### MQTT Message subscription

#### User guide

```
Usage: nanomq sub { start | stop } <addr> [<topic>...] [<opts>...]

Note: available parameters of sub are consistent with pub function
```

#### Example

```
nanomq sub start --url "mqtt-tcp://broker.emqx.io:1883" -t msg
```

NanoMQ Sub command is used to connect and subscribe to the topic msg of the [public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by [EMQ](https://www.emqx.com/en).

All the command-line tools inherit the high-performance features of NanoSDK-NNG. You can increase the message production and consumption performance of a single client by configuring the PARALLEL option. For details, please refer to [NanoMQ Newsletter 2021-11](https://www.emqx.com/en/blog/nanomq-newsletter-202111). At the same time, considering that most users have been used to the Mosquitto cli before, we have maintained this style to avoid increasing the difficulty for users to get started.

Combined with timing tools, the NanoMQ Command Line Toolkit can complete part of the performance test. However, the Pub/Sub commands can only work based on one MQTT client, which is difficult to meet the complete performance test requirements. We have planned to launch a performance test tool similar to Emqtt-bench in the next version, which can easily perform a stress test on the MQTT broker. At the same time, in order to take care of the original nanomsg users, we will also add NNG command-line tools in NanoMQ.

## Modify configuration method

In response to the problem that the original configuration file documentation was not clear enough, we have updated many configuration option parameters of the original NanoMQ and added documentation for description in the new version. For details, please refer to the [project ReadME](https://github.com/nanomq/nanomq#configuration).

In addition, we always value the feedback from users and actively solved the issues brought by the community. One of the problems we have heard many times is that when using NanoMQ in Docker mode, it is inconvenient to modify and set NanoMQ configuration files outside the container. Previously, NanoMQ could only be configured by adding command line parameters when starting Docker or directly entering the container to modify the configuration file:

```
docker run -d -p 1883:1883 --name nanomq nanomq/nanomq:0.5.9 --conf "/etc/nanomq.conf" --url "broker+tcp://0.0.0.0:1883"
```

In this version, we have also added a way to configure options through Docker environment variables, so that users can reconfigure NanoMQ instances outside the container.

```
docker run -d -p 1883:1883 --name nanomq nanomq/nanomq:0.5.9 -e NANOMQ_CONF_PATH="/usr/local/etc/nanomq.conf"
```

For example, the above example specifies the configuration file location and URL inside the container by registering host environment variables. For specific supported environment variables, please refer to [https://github.com/nanomq/nanomq#nanomq-environment-variables](https://github.com/nanomq/nanomq#nanomq-environment-variables).

## NanoSDK

Support for TLS was added in NanoSDK last month. SSL/TLS is the encryption of links and an essential feature for establishing secure MQTT links. Like NNG, NanoSDK relies on wolfssl instead of openssl. For its user guide and Demo, please refer to [https://github.com/nanomq/nng/tree/jaylin/nng-mqtt-pr/demo/mqtt_async](https://github.com/nanomq/nng/tree/jaylin/nng-mqtt-pr/demo/mqtt_async).

In addition, many users like to add self-defined behavior in the callback of online and offline. Therefore, we modified the callback method of connection and disconnection to allow users to perform blocking and waiting operations in the callback without affecting the MQTT connection itself, so as to improve the flexibility of NanoSDK.

> However, it should be noted that this will consume the number of threads inside the NanoSDK. If the taskq thread is exhausted, it will still affect the operation of the entire SDK. Please use it cautiously.

## Bug fixes

The following bugs were fixed in NanoMQ. Please upgrade it according to your specific situation according to the triggering scenarios.

1. When sending ultra-long text, it will be impossible to complete the reading and writing of a complete MQTT data packet in a single asynchronous I/O due to the fragmentation of the network card, resulting in the protocol parsing error of the next packet and the disconnection of the client.
2. When a large number of clients are disconnected at the same time, publishing offline messages to the system event topic will cause NanoMQ to exit in error due to resource competition.
3. When using the session persistence function, an empty address access problem occurs as the client reconnects to publish the cached message again,
4. A makefile of the nanolib module is misspelled.
5. Fixed a deadlock caused by the forced exit in NanoMQ. Previously, when the client used nng_close() to force offline, it could cause a deadlock problem.
6. Reorganized the dependencies between nanolib and NNG modules so that they can be compiled and tested independently.

## Community Interaction: collect opinions on Nanomsg Client and NanoMQ bridge mode

Born and grown from NNG, NanoMQ is committed to providing a more flexible and complete message bus tool for the open-source community at the edge. We have always attached great importance to the questions and voices of the community. Although MQTT has always been the most widely used IoT protocol, it only supports Pub/Sub (MQTT5.0 supports req/rep) mode, making it unsuitable for internal brokerless communication and RPC work in some edge scenarios, while nanomsg/nng has a variety of message patterns and has always been a popular high-performance library in the brokerless field.

Combined with the multiple message modes brought by nanomsg/nng and the advantages of RPC function that can broaden the usage scenarios of NanoMQ and facilitate users to build more flexible edge network topologies, we plan to support the bridge between nanomsg client and NanoMQ in NanoMQ. We sincerely ask for your opinions on how to define bridge mode, protocol conversion and configuration method. Welcome to leave us a message on the [Discussions page](https://github.com/nanomq/nanomq/discussions/298) of the GitHub project. We look forward to your valuable comments and suggestions.


<section class="promotion">
    <div>
        Try NanoMQ for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=nanomq" class="button is-gradient px-5">Get Started →</a >
</section>
