It has been nearly a year since the first version of [NanoMQ](https://www.emqx.com/en/products/nanomq) was released. This October, we officially released the first stable version of the project, v0.5.0. Since this version, NanoMQ will support not only [MQTT](https://www.emqx.com/en/mqtt) 3.1.1 protocol but also [MQTT Over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket). Users can modify NanoMQ's startup tuning options through configuration files or command line parameters. In addition, a built-in HTTP server has been added, and more HTTP APIs will be provided in the future.

Next, we will mainly focus on developing [MQTT SDK](https://www.emqx.com/en/mqtt-client-sdk) support and bridging function of NanoMQ/NNG, which is expected to be available in version 0.6.0. Be sure to stay tuned.

## Startup tuning options modification

NanoMQ has the features such as high compatibility and easy portability since its release. However, before version 0.4.0, users need to select optimization parameters for tuning in the compilation stage according to the hardware configuration of their own platform. NanoMQ 0.5.0 further optimizes the user experience of using the two configuration methods. The tuning guide and the main supported configuration parameters are as follows (taking the configuration file as an example):

```
num_taskq_thread=4 
max_taskq_thread=4 
```

The initial/maximum number of task threads is determined according to the number of CPU threads in the system. The default is 4. This configuration determines the performance and CPU utilization of NanoMQ, and it is recommended to keep the same with the maximum number of CPU threads.

```
parallel=32
```

It is the maximum number of parallel logical threads in the system. It is appropriate to be set according to the actual pressure of the system, which affects message delay and memory usage. It is recommended to be set to the double number of CPU threads.

```
msq_len=64
```

This is the initial length of the built-in [message queue](https://www.emqx.com/en/blog/mqtt5-feature-inflight-window-message-queue) buffer of each client. NanoMQ supports automatic scaling of the message queue. It is recommended to set it to a power of 2 according to the system memory size. For devices with less than 128Mb memory, it is recommended to fix it to 1024.

```
qos_duration=60
```

This is the granularity of the built-in global timer of the NanoMQ service. This option affects the minimum time difference for the connection of health detection. If there is a large number of concurrent clients, it will consume a little CPU. It is recommended to be consistent with the keepalive time of the MQTT connection.

```
allow_anonymous=yes   Whether to allow anonymous login
daemon=no             Whether to start as a daemon
```

## Websocket Service

MQTT Over Websocket has always been a major application field of MQTT, especially in front-end and applet development. Now, NanoMQ can open the Websokcet port through the following configuration options:

```
websocket.enable=yes
websocket.url=ws://0.0.0.0:8083/mqtt 
```

Currently, the Websocket port supports the complete MQTT 3.1.1 protocol.

## HTTP Service

As an [edge MQTT message server](https://nanomq.io), NanoMQ is also committed to providing users with easy-to-use HTTP APIs. At present, the HTTP service only supports the function of obtaining a list of all subscribed topics, and we will improve the related statistical functions as soon as possible.

```
http_server.enable=yes
http_server.username=admin
http_server.password=public 
```

## Community Issue and bug fixes

NanoMQ 0.5.0 also fixes several important security-related vulnerabilities submitted by the community. The NanoMQ team will keep listening to users and deliver stable, powerful, and secure edge MQTT message services and message buses to the community and industry.


<section class="promotion">
    <div>
        Try NanoMQ for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=nanomq" class="button is-gradient px-5">Get Started →</a >
</section>
