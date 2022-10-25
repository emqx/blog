NanoMQ continued to update steadily in September, and the latest [v0.12.1](https://github.com/emqx/nanomq/releases/tag/0.12.1) has been officially released recently. This version still brings rich updates: the bridging feature adds the ability to monitor online/offline events and connection status; the original log system is reconstructed and upgraded; configuration files are simplified to consolidate into a unified single file.

## **Bridge connection status event messages**

In IoT applications, network instability often occurs in weak network state, which requires a reliable way to detect the current device's network state and connectivity with the cloud. Therefore, NanoMQ provides the ability to use bridge connections to detect network connection status. When users use NanoMQ to bridge to the cloud at the edge, NanoMQ will create an MQTT connection to the specified cloud broker. Based on the long connection feature of MQTT, devices in the local network can use this connection to judge the network status.

When a bridge connection is broken due to a local network outage or other failures, NanoMQ will detect the disconnection of the bridge connection and convert it into a client online/offline event message to publish to the system topic. After the network is restored, the bridge connection is automatically reconnected, and an online event message is also published in the system topic. The local client and other services can perform corresponding emergency processing according to the received message, and can also configure multiple bridge targets as alternative services to avoid misjudgment caused by cloud service outages.

### **How to obtain bridge online/offline event messages**

At present, NanoMQ's bridge status events support all bridge modes, including MQTT 3.1.1/5.0 and MQTT over QUIC. The system topics of online/offline event messages are $SYS/brokers/connected and $SYS/brokers/disconnected respectively. Event messages can also be obtained as a standard Publish message in the way of WebHook. Here we take an MQTT over QUIC bridge configuration as an example to demonstrate how to obtain the online/offline messages of bridge connection:

If the bridge is configured as (only relevant excerpts):

```
bridge.mqtt.emqx.clientid=quic_client
bridge.mqtt.emqx.keepalive=5
bridge.mqtt.emqx.quic_keepalive=120
bridge.mqtt.emqx.clean_start=false
bridge.mqtt.emqx.username=quic_bridge
bridge.mqtt.emqx.password=passwd
```

Use the NanoMQ command line tool to subscribe to the corresponding topic. The bridge break will be triggered when the local network is down:

```
nanomq_cli sub --url mqtt-tcp://localhost:1883 -t '$SYS/brokers/connected'
connect_cb: mqtt-tcp://localhost:1883 connect result: 0 
$SYS/brokers/connected: {"username":"quic_bridge", "ts":1664277443551,"proto_name":"MQTT","keepalive":5,"return_code":"0","proto_ver":4,"client_id":"quic_client", "clean_start":0}
```

When the local network is restored, the bridge reconnection will be triggered:

```
nanomq_cli sub --url mqtt-tcp://localhost:1883 -t '$SYS/brokers/disconnected'
connect_cb: mqtt-tcp://localhost:1883 connect result: 0 
$SYS/brokers/disconnected: {"username":"quic_bridge","ts":1664277394014,"reason_code":"8b","client_id":"quic_client"}
```

It can be seen that the client ID and user name/password in the online/offline event messages are consistent with those in the bridge configuration, which can be used to distinguish local clients from bridge clients. At present, bridge connection status shares the same system topic with ordinary MQTT clients. NanoMQ also considers setting up a separate system topic for the bridge network status and adding a standard network health monitoring feature as the cloud edge message bus. Users are welcome to submit relevant issues and function applications.

### **New Keep Alive parameter configuration for QUIC transport layer**

QUIC has a built-in connection maintenance mechanism. To enable users to control the timeout of MQTT and QUIC in finer granularity, the bridging function of NanoMQ exposes both timeout settings as settable and more QUIC transport layer parameters will be made available later for users to tune.

```
## Ping: interval of a downward bridging connection via QUIC.
bridge.mqtt.emqx.quic_keepalive=120
```

## Configuration file **simplification**

Before v0.12, each module of NanoMQ had an independent configuration file and it was necessary to open each file separately to modify configuration, which was tedious to start. Starting from v0.12, we will formally consolidate all configuration items into nanomq.conf, and add separate groups for each module.

Note that the function of specifying the path of the bridge configuration file and the username and password file in the previous command line parameters is obsolete.

```
--bridge <path>           The path of a specified bridge configuration file 
--auth <path>             The path of a specified authorize configuration file
```

This modification does not affect the configuration file of ZeroMQ Gateway (nanomq_gatewaty.conf belongs to nanomq_cli) and the way configuration files are specified through environment variables when the container is deployed.

## **Log system reconstruction**

The old log system of NanoMQ supports three modes: command line, file, and Syslog. However, it cannot be switched through configuration, does not support hierarchical output, and needs to be enabled by modifying CMake parameters in the compilation stage, which make debugging and O&M analysis difficult. In v0.12, we reconstructed the entire log system. In addition to maintaining compatibility with the original three output targets and the Syslog standard, we added five log levels (ie. trace,debug, info, warn,error, fatal) as well as log file paths and log file rolling updates.

Log configuration example:

```
## ------------------ Logging Config ------------------ ##
## - file: output logs to file
## - console: output logs to the command line
## - syslog: output logs to the syslog system
## Value: file | console | syslog supports parallel configuration
log.to=file,console,syslog

## Value: trace | debug | info | warn | error | fatal
## Set log level
##
## Default: warn
log.level=warn

## If "Output Log to File" is configured, specify the file path here
log.dir=/tmp

## If "Output Log to File" is configured, specify the file name here
log.file=nanomq.log

## The maximum size of a single log file. Rolling update will be performed if it exceeds the limit
## Supported parameters unit: KB | MB | GB
log.rotation.size=10MB

## Maximum number of saved rolling update log files
log.rotation.count=5
```

## **NanoSDK adds more API**

Previously, the API of the NanoSDK was mostly NNG style, requiring users to assemble and send MQTT messages themselves to complete subscription and contact subscriptions. Starting from NanoSDK 0.7.5, the following more convenient and more encapsulated MQTT APIs have been added to the NanoSDK:

| nng_mqtt_subscribe()         | perform a subscribe request synchnously     |
| ---------------------------- | ------------------------------------------- |
| nng_mqtt_subscribe_async()   | perform a subscribe request asynchnously    |
| nng_mqtt_unsubscribe()       | perform an unsubscribe request synchnously  |
| nng_mqtt_unsubscribe_async() | perform an unsubscribe request asynchnously |
| nng_mqtt_disconnect()        | Disconnect an MQTT client                   |

Please refer to the [NanoSDK Doc](https://github.com/emqx/NanoSDK/blob/0.7.5/docs/man/libnng.3.adoc#mqtt-message-handling) for specific usage.

## **Upcoming**

The message republication feature and rule hot update of the rule engine will be officially released in the next version. At the same time, the Reload command will be added to NanoMQ for hot update of configuration files. Fallback to TCP will be automatically switched for the MQTT over QUIC bridge after multiple reconnection failures, to ensure that the bridge connection is normal in networks that do not support QUIC.




<section class="promotion">
    <div>
        Try NanoMQ for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=nanomq" class="button is-gradient px-5">Get Started →</a>
</section>
