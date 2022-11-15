Recently, MQTT X 1.9.0, an MQTT 5.0 client tool, has been released.

For the desktop client, some UI / UE has been optimized, a new page has been added to help users learn MQTT protocol knowledge more quickly and systematically, and some known issues have been fixed; for the command-line client, the `bench` command has been added to help users create, subscribe and publish the custom number of connections, topics and messages, and easily complete MQTT service performance testing.

Download the latest version here: [https://www.emqx.com/en/try?product=MQTTX](https://www.emqx.com/en/try?product=MQTTX) 

![MQTT Client](https://assets.emqx.com/images/cc8af08d253160ad08fe29999c92160c.png)


## MQTT X CLI Client

### Out-of-the-box bench command

In v1.9.0, MQTT X CLI provides an out-of-the-box benchmark tool -- `mqttx bench`, which can help users quickly perform simple performance and pressure testing. After installing or updating MQTT X CLI, users can soon use the command without additional operations, which is convenient and easy to use.

> For users who need large-scale scenarios and deep customization of testing services, we recommend using the fully hosted MQTT load testing cloud service [XMeter](https://www.emqx.com/en/products/xmeter)

Users can use the `bench` command to create a custom number of connections at a specified rate, subscribe to a custom number of topics, publish the custom number of messages to single or multiple topics, and test the connection performance and message throughput of a single or cluster MQTT broker through a single command. For example:

1. Create 10000 connections at a rate of 10 milliseconds per connection, and the client ID is `mqttx-bench-%i`, where `%i` is the index placeholder, that is, the client ID of the first client connection is mqttx-bench-1:

   ```
   mqttx bench conn -c 10000 -i 10 -I "mqttx-bench-%i"
   ```

2. Start 5000 subscription client connections, and subscribe to the topic `mqttx/bench/t` at the same time:

   ```
   mqttx bench sub -c 5000 -t "mqttx/bench/t"
   ```

3. Start 200 publishing client connections, and publish messages to the topic `mqttx/bench/t`, the message rate is 200 messages per second, and the message content is mqttx bench test:

   ```
   mqttx bench pub -c 200 -im 1000 -t mqttx/bench/t -m "mqttx bench test"
   ```

The above simple performance test of the connection, subscription, and publishing commands can easily achieve some simple custom scenario MQTT performance benchmark testing. You can debug and optimize your MQTT service and system environment through the testing results, to further improve your IoT application and service.

For MQTT X CLI, the `bench` command is easy to use and concise in its content output. For a large number of connections, subscriptions, and publications, we optimized its display method by dynamically updating the real-time number to avoid being overwhelmed by a large number of output logs in the process of use.

![MQTT Bench](https://assets.emqx.com/images/6d942b32742bf859ef66a93abb216860.png)

### Retain Message Flag

In addition, MQTT X CLI adds the Retain message flag, which allows users to determine whether the received message contains `retain: true` to determine whether it is a Retain message. The Retain message flag helps users better understand whether the message is a real-time message or a retained message, thus verifying the correctness of the message.

![MQTT Retain Message](https://assets.emqx.com/images/4e5635e47b07ccbaab54eb1f9195dda0.png)


## MQTT X Desktop Client

### Enhancement of Script function

In previous versions, MQTT X could only perform simple static data processing on received and sent messages, such as using random functions to simulate data, performing some format conversions, or extracting critical data for specific message templates.

In v1.9.0, we enhanced the script function to enable users to implement dynamic data simulation operations. For example, when users need to dynamically switch between two message content in the scheduled sending, respectively, the open and close of the switch instruction. You can now use the index parameter in the script, through the step length of the sent message, to dynamically switch between the two message content. This will help users quickly test the stability of their system when switching different commands.

In addition, the script function also added a `msgType` parameter, which can extend more message conversion capabilities through the message type parameter.

> Note: the index parameter can only be received when using the Timed Message publishing function.

![Enhancement of Script function](https://assets.emqx.com/images/23716622e8e7fec28f0ebd4a98a14b68.png)

### MQTT Protocol Help Page

In addition to providing powerful testing client tools to help developers quickly develop and debug MQTT services and applications, we also hope that developers can better understand MQTT protocol in this process and fully apply its related features.

Therefore, MQTT X 1.9.0 adds a help page that provides various contents related to MQTT protocol, including basic knowledge, quick start, connection parameter description, client programming tutorial, etc., to help users quickly build their own MQTT IoT applications. By satisfying users' various testing needs and providing system knowledge and practical case reference, MQTT X will become a solid backstop for users to build and design MQTT IoT applications.

![MQTT Protocol Help Page](https://assets.emqx.com/images/f48ce43f7561ee6908d4f53ae3a56e7d.png)

### UI / UE Optimization

We also made some adjustments and optimizations to the UI and interaction of MQTT X to improve the user experience.

On the left side of the connection list, we modified the new group button to a single add button. By clicking the new button, we can choose to quickly create a connection or a group for the connection without confusion; also, the connection button style display is optimized.

On the interaction side, we added some more practical shortcuts. You can now create a new connection through the `Ctrl or Cmd + N` in the connection list or directly go to the about page through the `Ctrl or Cmd + B` shortcut key to view some basic information about MQTT X. These shortcuts will make user operations more convenient.

![UI / UE Optimization](https://assets.emqx.com/images/d8f92bbb3d393069338d09f1632cc5b7.png)

### Other

- Client top system menu bar, internationalized display, not pure English display
- Fixed the problem that the message cannot be received after reconnection when the topic has been subscribed
- Removed some incorrect configuration item units

## Roadmap

MQTTX is still continuously improving and perfecting, to bring more practical and powerful features to users, and to provide convenience for the testing and development of IoT applications and services. In the future, we will focus on the following aspects：

- MQTT X CLI supports automatic reconnection
- Receive message and storage performance optimization, a large number of messages do not block
- MQTT X CLI supports using configuration files to connect, publish and subscribe
- Supports MQTT Debug
- Supports Sparkplug B format
- The received message can be automatically charted
- Plugins
- Script test automation (Flow)

Please look forward to it！



<section class="promotion">
    <div>
        Try MQTT X for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Get Started →</a>
</section>
