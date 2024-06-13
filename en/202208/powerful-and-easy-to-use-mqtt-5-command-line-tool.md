Recently, [MQTTX](https://mqttx.app/), the cross-platform desktop client for [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5), was released in version 1.8.0. MQTTX is designed to connect to MQTT brokers such as [EMQX](https://www.emqx.com/en/products/emqx). It makes it easy and quick to create multiple simultaneous [online MQTT client](http://mqtt-client.emqx.com/) connections and test the connection, publishing, and subscription functions of MQTT/TCP, MQTT/TLS, MQTT/WebSocket as well as other MQTT protocol features.

The latest release of v1.8.0 not only optimizes the experience with a quick connection duplication feature but also supports new use cases by adding two new interaction methods, namely CLI (command line) and browser. This makes MQTTX 1.8.0 the most complete MQTT test client in terms of supported scenarios. Depending on your needs, you can choose to download the desktop client, use the terminal command line, or quickly test MQTT connections in your web browser.

## MQTTX CLI: Rapidly develop and debug MQTT services and applications in the terminal

With the widespread use of the MQTT protocol in the IoT industry, more developers are choosing to use MQTTX for connectivity testing. 

In order to provide more choices and convenience for users to implement MQTT connection tests, MQTTX v1.8.0 adds the command line as a form of interaction - the [MQTTX CLI](https://mqttx.app/cli), a fully open source MQTT 5.0 command line client tool. **This allows developers to develop and debug MQTT services and applications faster using the command line without the graphical interface.** This enables the following usage goals:

- Test deployed MQTT services in the server terminal
- Quickly test MQTT services by editing and using command line scripts
- Use command line scripts to perform simple stress tests or automated tests 

> MQTTX CLI website: [https://mqttx.app/cli](https://mqttx.app/cli)
>
> MQTTX CLI 1.8.0 download: [https://github.com/emqx/MQTTX/releases/tag/v1.8.0](https://github.com/emqx/MQTTX/releases/tag/v1.8.0)
>
> MQTTX CLI GitHub repository: [https://github.com/emqx/MQTTX/tree/main/cli](https://github.com/emqx/MQTTX/tree/main/cli)

![MQTTX CLI](https://assets.emqx.com/images/ee9ee7ee619f209c725ef1c67f59d4ae.png)

## Dependency-free: Get up and running with no prerequisites required

### Installation

The MQTTX CLI can be quickly downloaded and installed on macOS, Linux, and Windows systems without any environmental dependencies, simply by executing commands in a terminal.

For macOS and Linux users, we provide a quick installation method using the command line to quickly download the binaries and install the latest stable version of MQTTX CLI on the operating system. Windows users can go to the MQTTX release page to find the exe package for the corresponding system architecture and manually download it for use.

> Note: When downloading and installing, please be careful to distinguish the CPU architecture of the current system environment

#### macOS

- **Homebrew**

   macOS users can quickly install and use the MQTTX CLI via Homebrew

   ```
   brew install emqx/mqttx/mqttx-cli
   ```

- **Intel Chip**

   ```
   curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-macos-x64
   sudo install ./mqttx-cli-macos-x64 /usr/local/bin/mqttx
   ```

- **Apple Silicon**

   ```
   curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-macos-arm64
   sudo install ./mqttx-cli-macos-arm64 /usr/local/bin/mqttx
   ```

#### Linux

- **x86-64**

   ```
   curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-linux-x64
   sudo install ./mqttx-cli-linux-x64 /usr/local/bin/mqttx
   ```

- **ARM64**

   ```
   curl -LO https://www.emqx.com/zh/downloads/MQTTX/v1.8.0/mqttx-cli-linux-arm64
   sudo install ./mqttx-cli-linux-arm64 /usr/local/bin/mqttx
   ```

#### Windows

Windows users should manually download the corresponding exe file from the MQTTX download page at: https://github.com/emqx/MQTTX/releases/tag/v1.8.0 

![MQTTX CLI Windows](https://assets.emqx.com/images/dccac8ea2f04693c55e77623ad507eba.png)

#### NPM

In addition to the above, we also provide an installation method using npm, so that you can quickly install and use it no matter what your current operating system environment is, as long as you have a Node.js environment on your system.

```
npm install mqttx-cli -g
```

### Quick Start

Once you have completed the download and installation, you can run and use the `mqttx` command by typing it directly into the terminal. You can verify that the MQTTX CLI has been installed successfully by adding the -V parameter, and when a version number is an output, the MQTTX CLI has been successfully installed.

```
$ mqttx -V
1.8.0
```

To test operation of the MQTTX CLI, you first need to connect to an MQTT server. In this article, we will use EMQ’s [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker), which runs on the fully managed [MQTT cloud](https://www.emqx.com/en/cloud), EMQX Cloud, with the following access information:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- WebSocket Port: **8083**

We can use the command line to connect to the MQTT server and publish or subscribe to messages from within the terminal. We start by editing the command to subscribe to a topic within a terminal window.

**Subscribe**

```
mqttx sub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883
```

Next, let’s try publishing a message to the topic we just subscribed to. Leave the listening subscriber running and create a new terminal window, then enter the command below.

**Publish**

```
mqttx pub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883 -m 'hello from MQTTX CLI!'
```

At this point, we can see a message that was just posted in the window of the Subscribe to Topic command.

![MQTTX CLI Publish](https://assets.emqx.com/images/db6f9c76559376f3e490c1cf46e6eff2.png)

**Publishing multiple messages**

The MQTTX CLI also supports a pub command to publish multiple messages, just add an -M parameter and an -s parameter to the command in the editor and separate each entry with a newline.

```
mqttx pub -t 'mqttx/cli' -h 'broker.emqx.io' -p 1883 -s -M
```

![Publishing multiple messages](https://assets.emqx.com/images/3d565168651086abf2540de4a826af55.png)

Finally, we test and verify the functionality of the MQTTX CLI by using the MQTTX desktop client to connect to the same MQTT service as the MQTTX CLI. We use the MQTTX CLI to publish a message, receive it through the MQTTX desktop client, and then reverse the process by using the MQTTX desktop client to send a message to the MQTTX CLI. At this point, we can see that both sides have received their respective incoming and outgoing messages.

![MQTTX desktop client ](https://assets.emqx.com/images/2a79737764ec04f5a1344ad84a06c3e5.png)

<center>MQTTX desktop client</center>

![MQTTX CLI](https://assets.emqx.com/images/4eff2f4b27c0de96b15bfb7878c9401a.png)

<center>MQTTX CLI</center>

## Summary

This concludes our testing and verification of the MQTT message publish-subscribe feature using the MQTTX CLI. In addition to the common features mentioned above, the MQTTX CLI also supports setting up last [will messages](https://www.emqx.com/en/blog/use-of-mqtt-will-message), using SSL/TLS to test mqtts connections, and more. MQTT 5.0 connectivity will also be supported in the future.

The release of the MQTTX CLI provides a new option for IoT developers to test MQTT connections. With complete support for command line calls, desktop client downloads, and online browsers, MQTTX 1.8.0 helps users with different use cases to complete the development and debugging of MQTT services or applications, improving their own business capabilities and stability. The easy-to-use test client tool, MQTTX, combined with the efficient, [reliable MQTT broker](https://github.com/emqx/emqx), EMQX, will help IoT developers build competitive IoT platforms and applications.

## Appendix: User Help

You can enter the --help parameter on the command line to get help or check the usage parameter table below to use the MQTTX CLI.

```
# Get help for the mqttx command
mqttx --help

# Get help for the sub command
mqttx sub --help

# Get help for the pub command
mqttx pub --help
```

### **Table of options**

| Options       | Description               |
| ------------- | ------------------------- |
| -V, --version | output the version number |
| -h, --help    | display help for command  |

| Command | Description                  |
| ------- | ---------------------------- |
| pub     | publish a message to a topic |
| sub     | subscribes to a topic        |

**Subscribe**

| Options                | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| -h, --hostname <HOST>  | the broker host (default: "localhost")                       |
| -p, --port <PORT>      | the broker port                                              |
| -i, --client-id <ID>   | the client id                                                |
| -q, --qos <0/1/2>      | the QoS of the message (default: 0)                          |
| --clean                | discard any pending message for the given id (default: true) |
| -t, --topic <TOPIC>    | the message topic                                            |
| -k, --keepalive <SEC>  | send a ping every SEC seconds (default: 30)                  |
| -u, --username <USER>  | the username                                                 |
| -P, --password <PASS>  | the password                                                 |
| -l, --protocol <PROTO> | the protocol to use, mqtt, mqtts, ws or wss                  |
| --key <PATH>           | path to the key file                                         |
| --cert <PATH>          | path to the cert file                                        |
| --ca                   | path to the ca certificate                                   |
| --insecure             | do not verify the server certificate                         |
| --will-topic <TOPIC>   | the will topic                                               |
| --will-message <BODY>  | the will message                                             |
| --will-qos <0/1/2>     | the will qos                                                 |
| --will-retain          | send a will retained message (default: false)                |
| -v, --verbose          | print the topic before the message                           |
| --help                 | display help for sub command                                 |

**Publish**

| Options                | Description                                         |
| ---------------------- | --------------------------------------------------- |
| -h, --hostname <HOST>  | the broker host (default: "localhost")              |
| -p, --port <PORT>      | the broker port                                     |
| -i, --client-id <ID>   | the client id                                       |
| -q, --qos <0/1/2>      | the QoS of the message (default: 0)                 |
| -t, --topic <TOPIC>    | the message topic                                   |
| -m, --message<MSG>     | the message body (default: "Hello From MQTTX CLI") |
| -r, --retain           | send a retained message (default: false)            |
| -s, --stdin            | read the message body from stdin                    |
| -M, --multiline        | read lines from stdin as multiple messages          |
| -u, --username <USER>  | the username                                        |
| -P, --password <PASS>  | the password                                        |
| -l, --protocol <PROTO> | the protocol to use, mqtt, mqtts, ws or wss         |
| --key <PATH>           | path to the key file                                |
| --cert <PATH>          | path to the cert file                               |
| --ca                   | path to the ca certificate                          |
| --insecure             | do not verify the server certificate                |
| --will-topic <TOPIC>   | the will topic                                      |
| --will-message <BODY>  | the will message                                    |
| --will-qos <0/1/2>     | the will qos (default: 0)                           |
| --will-retain          | send a will retained message (default: false)       |
| --help                 | display help for pub command                        |



<section class="promotion">
    <div>
       Try MQTTX
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Download Now →</a>
</section>
