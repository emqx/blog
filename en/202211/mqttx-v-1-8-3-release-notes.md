Recently, MQTT X released the latest version [1.8.3](https://github.com/emqx/MQTTX/releases/tag/v1.8.3), The main optimization of function usage and the various problems encountered in the process of use are fixed. For example, the use of MQTT 5.0 Clean Start is optimized, and the default value of the Session Expiry Interval is added; the default output display of MQTT X CLI is optimized, and a more detailed and beautiful content display is provided.

## MQTT X Desktop

### Optimize Clean Start usage

MQTT X as an MQTT 5.0 Client tool, currently defaults to MQTT 5.0 connection testing. In MQTT 5.0, Clean Session is modified to Clean Start and needs to be used in conjunction with the Session Expiry Interval. However, in the current 1.8.2 version, when using the default connection, if the user does not set the Session Expiry Interval, the MQTT Broker will not be able to persist its session when the connection is disconnected. For many users who are not very familiar with the new features of MQTT 5.0, this brings some trouble.

The currently released 1.8.3 version optimizes this problem, and the display of Clean Session is modified to Clean Start. When Clean Start is closed, the Session Expiry Interval is set to never expire by default, and when it is opened, the default value is set to 0, which means that the session is not saved. At the same time, it also continues to support users to manually modify the value to meet the current test requirements. At the same time, the user is prompted: when Clean Start is closed, if the value is empty, the Session Expiry Interval needs to be set to ensure the correct use of its connection session.

### Other usage optimization

- Uniform true and false selectors to switch components
- Optimize the use of SSL/TLS switch
- Optimize the deletion of scripts that are in use
- Fix the problem that the retained message received when the connection is disconnected cannot be saved
- Fix the problem that the content will be truncated when Hex format appears spaces, and support formatted output of Hex data
- Fix the problem that the message cannot be received after setting the topic alias
- Fix some interval errors

## MQTT X Web

Online MQTT 5.0 Client Tool MQTT X Web has been updated as follows:

- Support storing historical messages sent
- Support single message copy and delete
- Support deployment to any URL path using Docker
- Support multi-topic subscription
- Support turning on and off auto-scroll
- Support setting subscription identifiers and subscription options
- Support setting the reconnect period

Online use address: [http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client) 

## MQTT X CLI

### Support multi-topic subscription

On the desktop client of MQTT X, we provide a multi-topic subscription function. In version 1.8.3, the command line tool MQTT X CLI also supports multi-topic subscriptions. As long as multiple --topic parameters are entered, multiple topics can be subscribed at the same time using a single command line to receive the message content under different topics to test and view data.

![Multi-topic subscription](https://assets.emqx.com/images/ed0e82a31cb7319dd3e4e54d923a0f56.png)

### Optimize CLI content output

On the terminal, we optimized the display content of MQTT X CLI. In version 1.8.3, we provided a time display for each step of the output content and refined its step display. For example, when using the sub and pub commands, you can also see the process of connecting and connecting. Using a log output method, can improve the user's reading experience and help users to view the process and content of the current connection test more clearly and conveniently.

![MQTT CLI](https://assets.emqx.com/images/d28d110dad3ee7a6bcf0e9ea0ca25820.png)

### Other optimizations

- Add topic verification, users cannot send messages to topics containing # and +, etc. with wildcards
- When using the --version parameter to output the version, the address with changelogs will be output, which is convenient for users to quickly view the latest features under this version
- Add the check command to check if there is a new version that can be updated
- Add more MQTT 5.0 properties configuration, such as supporting setting session expiry interval
- Fix the problem that user properties are set incorrectly in the pub and subcommands

## Roadmap

MQTT X is still in the process of continuous enhancement and improvement, to bring more practical and powerful functions to users and facilitate the testing and development of IoT platforms.

Next, we will focus on the following aspects:

- MQTT X CLI will support the bench command
- Improve the user experience of MQTT X Web
- Support custom charting of received data
- Plugin system (such as supporting SparkPlug B, integrating MQTT X CLI)
- Script function optimization
- Release MQTT X Mobile application
- Improve MQTT X Web function
- MQTT Debug function


<section class="promotion">
    <div>
        Try MQTT X Now
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Download →</a>
</section>
