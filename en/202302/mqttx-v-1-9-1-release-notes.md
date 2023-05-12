MQTTX 1.9.1, an MQTT 5.0 client tool, is now available after two beta iterations.

This version has seen significant improvements in stability through extensive performance optimization and resolution of known issues. In particular, when handling a large number of messages, version 1.9.1 has significantly reduced CPU and memory usage by 80% compared to the previous version, resulting in greatly optimized overall performance and reduced risk of system crashes. The improved stability offers users a more dependable environment for conducting IoT performance testing and building IoT applications.

Download the latest version here: [https://www.emqx.com/en/try?product=MQTTX](https://www.emqx.com/en/try?product=MQTTX)  


## Desktop Client

### Performance Optimization

MQTTX 1.9.1 features numerous performance optimizations for the desktop client to enhance the efficiency of topic filtering when handling a large number of messages and to prevent any potential high consumption of CPU resources that could result in lagging. The previous issue of database crashes due to excessive message traffic on Windows has been resolved, providing a much-improved user experience.

### Comparison Test

A performance comparison was conducted between version 1.9.0 and version 1.9.1 of MQTTX using the bench command of the MQTTX CLI.

#### Test Scenario

To perform a benchmark test, a new local MQTT Broker connection was created and subscribed to an mqttx/bench topic. The bench command was then utilized to publish 1000 messages per second, each with a payload of "hello" and a QoS of 0, to the topic for 1 minute. During this scenario, where 1000 messages were being received per second, the CPU usage and memory usage changes were monitored using the debugging tools available in the MQTTX development environment.

![benchmark test](https://assets.emqx.com/images/cab9054e5e262ad6684d338988a361eb.png)

#### Test Results

> The JS heap size in the monitoring chart is the memory usage

#### **Analysis and Conclusion**

The results of the benchmark test revealed that in version 1.9.0, while receiving messages, the CPU usage consistently remained at 100% and the memory usage reached a peak of close to 2000MB, before settling at around 1000MB. Additionally, the pages were found to be unresponsive or laggy.

In version 1.9.1, during the receipt of a large number of messages, the average CPU usage was around 50%. The memory usage reached a peak of close to 200MB but was subsequently maintained at approximately 150MB. Additionally, the page refresh was observed to be smooth and without any lag.

A comparison of the memory and CPU usage reveals that the latest version of the MQTTX desktop client exhibits an optimization of approximately 80% in terms of performance. From a user's perspective, the issues of page stuttering or crashes have also been significantly mitigated.

Aside from performance optimizations in message reception, other optimizations have been made including improved performance in topic filtering and message searching, support for bulk storage of messages, and resolution of previous database crash issues.

### Interaction Enhancement

In previous versions of MQTTX, the default setting of automatically scrolling to the latest message when receiving a new one caused inconvenience for users who wanted to view historical messages. Deactivating this setting would also mean that users would miss out on the latest news in real-time.

The latest version, 1.9.1, enhances the user experience by introducing a new message alert displayed at the bottom of the message list. Upon receiving a new message, users can opt to remain on the current page and continue to view the historical messages or they can click on the alert to access the latest message, making their experience more seamless.

![MQTT Desktop Client](https://assets.emqx.com/images/f1ba900d95d9241a38bc6f78bcf06292.png)

### Bug Fixes and Optimizations

In addition to performance optimizations, this release also fixes and optimizes the following known issues:

- Fixes issues with the integrity and accuracy of importing and exporting data, and optimizes loading speed during import.
- Fixes the issue of having to enter a username when using client ID + password authentication.
- Fixes the issue that offline messages cannot be received after reconnection.
- Fixes the issue where the order of messages in the message list was incorrect in some cases.
- Fixes the issue of duplicate keys in user property configuration and ensures full compliance with the MQTT protocol.
- Fixes the issue that group icons disappear due to long group names, and supports the full display of long group names.
- Fixes the issue that the right-click menu displays beyond the window in the grouping list.
- Fixes the issue that other subscribed topics disappear after clicking traffic statistics and automatically subscribing to the system topic $SYS/#.
- Fixes the issue of not resetting the topic subscription configuration correctly in the topic subscription window
- Fixes the issue that caused the Payload editor to not fit the width correctly when manually resizing the window
- Fixes the issue of improper connection highlighting when opening a new window.
- Reorganizes the help page into a comprehensive "Everything about MQTT" section and place it as a top-level menu item for easier access and understanding of MQTT concepts.
- Improves status display on send button click to avoid confusion on send success/failure.
- Optimizes the alert of unconnected status when clicking the Subscribe button.
- Optimizes the hint of filling in the topic input box.

## MQTTX CLI

### Adjust the Date and Time Format

The output log in MQTTX CLI version 1.9.1 has been optimized by adding a new date and time format, enabling users to accurately view and log the current test time. The new format is as follows:

```
$ mqttx conn -h broker.emqx.io -p 1883
[2/2/2023] [2:54:50 PM] › … Connecting...
[2/2/2023] [2:54:53 PM] › ✔ Connected
```

In the future, we plan to offer users the ability to customize the date and time format in their configurations, enabling them to easily align their test results with their log files and facilitating central management and review.

### Other Updates

In addition to the date and time format, MQTTX CLI had integrated several new, user-friendly features in the 1.9.1 beta version, including:

- Support automatic reconnection. MQTTX CLI will automatically reconnect after any disconnections occur, even when using the bench command.
- Allow users to save their connection parameters to a local file and then easily read the parameters from the file when they want to connect. The feature also supports saving all CLI commands to the configuration file.
- Support specifying message format. Incoming messages can be effortlessly transformed into various formats, including String, Hex, Base64, and JSON, for more convenient viewing and logging.

All of the aforementioned enhancements can be found in the 1.9.1 release. For a comprehensive overview of the new features, please refer to the previous article [MQTTX newsletter 2022-11](https://www.emqx.com/en/blog/mqttx-newsletter-202211).

## Roadmap

MQTTX is undergoing constant improvements to offer more practical and powerful capabilities to its users, and make the testing and development of IoT applications and services more accessible. We are going to concentrate on certain areas, so keep an eye out for updates:

- Supports MQTT Debug
- Optimizes the output of system topics, allowing users to easily monitor and view data metrics of MQTT Broker using MQTTX
- Charts automatically based on incoming messages
- Adds Plugins
- Supports Sparkplug B format
- Supports automated test script (Flow)
- Adds more message formats



<section class="promotion">
    <div>
        Try MQTTX for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=MQTTX" class="button is-gradient px-5">Get Started →</a>
</section>
