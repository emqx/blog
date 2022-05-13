本月，NanoMQ 发布了 0.5.9 版本，除了例行的 Bug 修复外，我们基于上月的 MQTT 桥接功能和兼容原生 NNG 功能，为大家带来了高效易用的 [MQTT](https://www.emqx.com/zh/mqtt) 命令行工具包。同时我们也持续修复发现的 Bug 和用户反馈的 Issue，并积极维护 NanoMQ 的姊妹项目 NanoSDK。

## MQTT 命令行工具

无论日常 MQTT 开发和测试还是对 Broker 进行性能评估，一个简单易用且高性能的 MQTT 命令行工具(Command Line Toolkit)都是必不可少的。我们基于之前发布的 NanoSDK 为广大 MQTT 使用者开发了一套完整的 MQTT 客户端工具，其内部包含 MQTT 消息发布、订阅和连接功能。

### MQTT 消息发布

#### 使用方法

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

使用 NanoMQ Pub 工具向 [EMQ](https://www.emqx.com/zh) 提供的[公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 的 msg 主题每 10ms 发送一条 Payload 为 hello 的消息，当发送到 10000 条时停止。而且 NanoMQ Toolkit 还能够从文件中读取数据进行发送，方便用户进行定制自己的 Payload 来模拟业务测试。

### MQTT 消息订阅

#### 使用方法

```
Usage: nanomq sub { start | stop } <addr> [<topic>...] [<opts>...]

注：参数可选项和pub功能一致
```

#### Example

```
nanomq sub start --url "mqtt-tcp://broker.emqx.io:1883" -t msg
```

使用 NanoMQ Sub 命令连接并订阅 EMQ 提供的公共 MQTT Broker 的主题msg。

命令行工具都继承了 NanoSDK-NNG 的高性能特点，可以通过配置 `PARALLEL` 选项增加单个客户端的消息生产和消费性能，详情请参阅[ NanoMQ Newsletter 2021-11](https://www.emqx.com/zh/blog/nanomq-newsletter-202111)。同时考虑到大部分用户之前已经习惯了Mosquitto cli 的使用方式，所以我们保持了这一风格以尽量避免增加用户上手使用的困难。

虽然结合计时工具，NanoMQ Command Line Toolkit 能够完成部分的性能测试工作，但是 Pub/Sub 命令都只能基于一个 MQTT 客户端工作，难以满足完整的性能测试需求。我们已经计划在下个版本推出类似 Emqtt-bench 的性能测试工具，可以方便地对 MQTT 消息服务器进行压力测试。同时，为了照顾原先的 nanomsg 使用者，我们也会在 NanoMQ 中增加 NNG 的命令行工具。

## 修改配置方式

针对原先配置文件文档说明不够清晰的问题，新版本我们更新了许多原有 NanoMQ 的配置选项参数，并增补了文档说明。详情请参阅项目 [README 文件](https://github.com/nanomq/nanomq#configuration)。

另外我们也一直很重视和积极解决用户和社区的各方反馈，其中有一个多次收到的问题是：当以 Docker 方式使用 NanoMQ 时，不方便在容器外对 NanoMQ 的配置文件进行修改和设置。之前只能通过启动 Docker 时增加命令行参数或直接进入容器内部修改配置文件的方式对 NanoMQ 进行配置：

```
docker run -d -p 1883:1883 --name nanomq nanomq/nanomq:0.5.9 --conf "/etc/nanomq.conf" --url "broker+tcp://0.0.0.0:1883"
```

本次版本我们也增加了通过 Docker 环境变量配置选项的方式，用户可以在容器外部对 NanoMQ 实例进行重新配置。

```
docker run -d -p 1883:1883 --name nanomq nanomq/nanomq:0.5.9 -e NANOMQ_CONF_PATH="/usr/local/etc/nanomq.conf"
```

例如，以上就通过注册宿主机环境变量到容器内部来指定配置文件位置和 URL。具体支持的环境变量请参见：[https://github.com/nanomq/nanomq#nanomq-environment-variables](https://github.com/nanomq/nanomq#nanomq-environment-variables) 。

## NanoSDK

NanoSDK 上个月增加了 TLS 支持，SSL/TLS 是对链接加密，是建立安全的 MQTT 链接必不可少特性。和NNG一样，NanoSDK依赖 wolfssl 而不是 openssl。其使用方法和 Demo 请参照 [https://github.com/nanomq/nng/tree/jaylin/nng-mqtt-pr/demo/mqtt_async](https://github.com/nanomq/nng/tree/jaylin/nng-mqtt-pr/demo/mqtt_async)。

另外，许多用户喜欢在上线和下线的回调中进行一些业务操作，因此我们修改了连接和断开连接的回调方式，以支持用户在回调中进行阻塞等待形式的操作而不会影响 MQTT 连接本身，从而提高 NanoSDK 的使用灵活性。

> *但需要注意的是，这会消耗NanoSDK内部的线程数量，如果taskq线程耗尽还是会影响整个SDK的运行，请酌情使用。

## Bug 修复

本月 NanoMQ 修复了以下 Bug,请各位用户根据各个 Bug 的情况和触发场景进行升级。

1. 当进行超长文本发送时，会由于网卡分片导致无法在单个异步 I/O 中完成一个完整 MQTT 数据包的读写，从而造成下一个包的协议解析错误导致客户端断开。
2. 当有大量客户端同时断线时，发布离线消息到系统事件主题会因为资源竞争而导致 NanoMQ 错误退出。
3. 使用会话保持功能时，当客户端重连进行缓存消息再次发布时的一个空地址访问问题。
4. nanolib 模块的一个 makefile 拼写错误。
5. 修复了一个 NanoMQ 中强制退出会导致死锁的问题。之前当客户端使用 nng_close() 强制下线时可能造成死锁问题。
6. 重新整理了nanolib和 NNG 模块之间的依赖关系，使其各自可以独立编译和测试。

## 社区互动：关于 nanomsg 客户端与 NanoMQ 桥接模式的意见征集

NanoMQ 从 NNG 中诞生并成长，致力于在边缘端为开源社区提供更灵活完整的消息总线工具。我们一直重视倾听社区的问题和呼声，虽然 MQTT 一直是最广泛使用的物联网协议，但其只支持 Pub/Sub（[MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 支持 req/rep）模式使其不适合某些边缘场景内部点对点消息（brokerless）通信和 RPC 工作，而 nanomsg/nng 具有多种消息模式，在brokerless领域一直是广受用户喜爱的高性能库。

结合 nanomsg/nng 带来的多种消息模式，以及 RPC 功能能够拓宽 NanoMQ 的使用场景并方便用户构建更灵活的边缘网络拓扑这一优势，我们计划在 NanoMQ 中支持nanomsg客户端与 NanoMQ 的桥接。关于如何定义桥接模式、协议转换规约和配置方式，我们在此诚挚地向各位征求意见。欢迎大家在 GitHub 项目的 Discussion 页面（[https://github.com/nanomq/nanomq/discussions/298](https://github.com/nanomq/nanomq/discussions/298) ）给我们留言，期待您的宝贵意见和建议。


<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a >
</section>
