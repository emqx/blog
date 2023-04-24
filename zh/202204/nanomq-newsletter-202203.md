三月初春，万物复苏，NanoMQ 项目[https://github.com/emqx/nanomq](https://github.com/emqx/nanomq) 也迎来了一个重大更新：第一个长期支持（LTS）版本 v0.6.6 正式发布。

在未来的一年里，这一版本会和主分支同时维护并得到所有重要的功能更新。在 0.6.6 版本里我们增加了内置性能测试工具，丰富了 HTTP APIs 的支持，这也是第一个能够较完整同时兼容支持 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) & 3.1.1 特性的版本。

## nano_bench 工具

[在一月的 Newsletter 中](https://www.emqx.com/zh/blog/nanomq-newsletter-202202)我们预告了压力测试工具。本月它如期而至。nano_bench 是我们基于 NanoSDK 开发的性能测试工具，类似于 emqtt_bench。这是其第一个正式版本，欢迎用户试用并提出意见。

### 编译&安装

nano_bench 工具在默认的发行版里并不携带，需要您通过设置`-DBUILD_BENCH=ON`参数来编译安装以启用：

```
$ cmake -G Ninja -DBUILD_BENCH=ON .. 
$ Ninja 
```

编译完成后，执行以下命令确认可以正常使用：

```
$ nanomq
available applications:
   * broker
   * pub
   * sub
   * conn
   * bench
   * nngcat

EMQ X Edge Computing Kit v0.6.6-3
Copyright 2022 EMQ X Edge Team
```

```
$ nanomq bench start
Usage: nanomq bench start { pub | sub | conn } [--help]
```

`bench` 有以下三个子命令：

- `pub`：用于创建大量客户端来执行发布消息的操作。
- `sub`：用于创建大量客户端订阅主题和接收消息。
- `conn`：用于创建大量连接。

### Pub 发布

执行 `nanomq bench start pub --help` 时，您将获得可用的参数输出。

| Parameter         | Abbreviation | Optional value | Default value  | Description               |
| :---------------- | :----------- | :------------- | :------------- | :------------------------ |
| --host            | -h           | -              | localhost      | 服务端地址                |
| --port            | -p           | -              | 1883           | 服务端端口                |
| --version         | -V           | 3 4 5          | 5              | MQTT 协议版本             |
| --count           | -c           | -              | 200            | 客户端数量                |
| --interval        | -i           | -              | 10             | 创建客户端的时间间隔 (ms) |
| --interval_of_msg | -I           | -              | 1000           | 发布消息时间间隔          |
| --username        | -u           | -              | none; optional | 客户端用户名              |
| --password        | -P           | -              | none; optional | 客户端密码                |
| --topic           | -t           | -              | none; required | 发布主题                  |
| --size            | -s           | -              | 256            | 消息负载的大小            |
| --qos             | -q           | -              | 0              | QoS 服务级别              |
| --retain          | -r           | true false     | false          | 保留消息标示位            |
| --keepalive       | -k           | -              | 300            | 保活时间                  |
| --clean           | -C           | true false     | true           | 保留会话标示位            |
| --ssl             | -S           | true false     | false          | SSL 使能位                |
| --certfile        | -            | -              | none           | 客户端 SSL 证书           |
| --keyfile         | -            | -              | none           | 客户端私钥                |
| --ws              | -            | true false     | false          | 是为建立 WebSocket 连接   |

例如，我们启动 10 个连接，每秒向主题 t 发送 100 条 QoS0 消息，其中每个消息负载的大小为 16 字节：

```
$ nanomq bench start pub -t msg -h broker.emqx.io -s 16 -q 0 -c 10 -I 100
```

### Sub 订阅

执行 `nanomq bench start sub --help` 以获取此子命令的所有可用参数。它们的解释已包含在上表中，不同在于没有了发送频率参数，此处不再赘述。

例如，我们启动 500 个连接，每个连接使用 QoS0 订阅 `t` 主题：

```
$ nanomq bench start sub -t msg -h broker.emqx.io -c 500
```

### Conn 连接

执行 `nanomq bench start conn --help` 以获取此子命令的所有可用参数。参数选项与其他命令大致相同。此处不再赘述。

例如，我们启动 1000 个客户端去连接公用的 EMQX 服务器：

```
$ nanomq bench start conn -h broker.emqx.io -c 1000
```

### SSL 连接

`bench` 也支持建立 SSL 安全连接来执行测试。

单向认证

```
$ nanomq bench start sub -c 100 -i 10 -t bench -p 8883 -S
$ nanomq bench start pub -c 100 -I 10 -t bench -p 8883 -s 256 -S
```

双向认证

```
$ nanomq bench start sub -c 100 -i 10 -t bench -p 8883 --certfile path/to/client-cert.pem --keyfile path/to/client-key.pem
$ nanomq bench start pub -c 100 -i 10 -t bench -s 256 -p 8883 --certfile path/to/client-cert.pem --keyfile path/to/client-key.pem
```

结合之前 NanoMQ 的 Pub/Sub/Conn 工具，现在只需要安装 NanoMQ 命令行工具套装就能轻松获得 MQTT  3.1.1 的全套测试能力。

## MQTT 5.0 特性支持

在 v0.6.6 之前的版本里，NanoMQ 无法兼容 MQTT 5.0 和 3.1.1 客户端进行通信。现在我们完善了 MQTT  5.0 的特性支持和兼容性，能够在内部进行不同版本客户端的消息互通和转换。

目前已支持以下重要且常用的 MQTT 5.0 特性：

1. Shared Subscription 共享订阅
2. User Property 用户属性 
3. Will Delay Interval 遗愿消息延时间隔 
4. MQTT 5.0 CONNECT/PUBLISH/PUBACK/PUBREL/PUBCOMP/SUBSCRIBE/SUBACK/DISCONNECT 等基础功能

以下 MQTT 5.0 特性将在后续版本中陆续支持：

1. Authentication 认证服务
2. Response Topic & Correlation Data 响应主题
3. Subscription Identifier 订阅标识符
4. Reason String 原因字符串
5. Message expiry interval 消息过期间隔时间

这些特性在之后的版本里会逐步完善。

> 注：NanoMQ 的上下线事件主题和消息仍然保留为 MQTT 3.1.1。

## HTTP API

完善的 HTTP API 系统是用户控制和监控 Broker 的一个重要途径。0.6.6 版本我们也新增了 2 组重要的HTTP APIs。下面将对其进行简单介绍：

NanoMQ 的 HTTP API 使用 [Basic 认证 (opens new window)](https://en.wikipedia.org/wiki/Basic_access_authentication)方式。`username` 和 `password` 须分别填写。 默认的`username` 和 `password` 是：`admin/public`。 可通过 `etc/nanomq.conf` 配置文件修改 `username` 和 `password` 。

第一组是统计信息 API。

**Parameters (JSON)**

| Name | Type    | Required | Value  | Description                                                  |
| :--- | :------ | :------- | :----- | :----------------------------------------------------------- |
| req  | Integer | Required | 2      | 请求码 *2*。                                                 |
| seq  | Integer | Required | Unique | seq 是全局唯一的，请求/响应信息都会携带该信息，可以通过该值确定对应的请求响应。 |

**Success Response Body (JSON)**

| Name              | Type    | Description                                                  |
| :---------------- | :------ | :----------------------------------------------------------- |
| code              | Integer | 请求结果，0 表示成功                                         |
| seq               | Integer | seq 是全局唯一的，请求/响应信息都会携带该信息，可以通过该值确定对应的请求响应。 |
| rep               | Integer | rep 是 2 作为 req 2 的响应。                                 |
| data.client_size  | Integer | 订阅客户端的数量。                                           |
| data.message_in   | Integer | NanoMQ 流入的消息数量。                                      |
| data.message_out  | Integer | NanoMQ 流出的消息数量。                                      |
| data.message_drop | Integer | NanoMQ 丢弃的消息数量。                                      |

#### **Examples**

```
$ curl -i --basic -u admin:public -X POST "http://localhost:8081/api/v1" -d '{"req": 2,"seq": 1}'
{"code":0,"seq":1,"rep":2,"data":{"client_size":1,"message_in":4,"message_out":0,"message_drop":4}}
```

#### 主题信息：返回客户端标识符对应的主题和 QoS 信息。

**Parameters (JSON)**

| Name | Type    | Required | Value  | Description                                                  |
| :--- | :------ | :------- | :----- | :----------------------------------------------------------- |
| req  | Integer | Required | 4      | 请求码 *4*。                                                 |
| seq  | Integer | Required | unique | seq 是全局唯一的，请求/响应信息都会携带该信息，可以通过该值确定对应的请求响应。 |

**Success Response Body (JSON)**

| Name                           | Type    | Description                                                  |
| :----------------------------- | :------ | :----------------------------------------------------------- |
| code                           | Integer | 请求结果，0 表示成功                                         |
| seq                            | Integer | seq 是全局唯一的，请求/响应信息都会携带该信息，可以通过该值确定对应的请求响应。 |
| rep                            | Integer | rep 是 4 作为 req 4 的响应。                                 |
| data[0].client_id              | String  | 客户端订阅标识符。                                           |
| data[0].subscriptions[0].topic | String  | 订阅的主题。                                                 |
| data[0].subscriptions[0].qos   | Integer | 订阅的 QoS                                                   |

#### **Examples**

```
$ curl -i --basic -u admin:public -X POST "http://localhost:8081/api/v1" -d '{"req": 4,"seq": 1111111}'
{"code":0,"seq":1111111,"rep":4,"data":[{"client_id":"nanomq-ebd54382","subscriptions":[{"topic":"a/b/c","qos":0}]}]}
```

#### 客户端信息：返回所有的客户端信息。

**Parameters (JSON)**

| Name | Type    | Required | Value  | Description                                                  |
| :--- | :------ | :------- | :----- | :----------------------------------------------------------- |
| req  | Integer | Required | 5      | 请求码 *5*。                                                 |
| seq  | Integer | Required | unique | seq 是全局唯一的，请求/响应信息都会携带该信息，可以通过该值确定对应的请求响应。 |

**Success Response Body (JSON)**

| Name                    | Type    | Description                                                  |
| :---------------------- | :------ | :----------------------------------------------------------- |
| code                    | Integer | 请求结果，0 表示成功                                         |
| seq                     | Integer | seq 是全局唯一的，请求/响应信息都会携带该信息，可以通过该值确定对应的请求响应。 |
| rep                     | Integer | rep 是 5 作为 req 5 的响应。                                 |
| data[0].client_id       | String  | 客户端订阅标识符。                                           |
| data[0].username        | String  | 用户名。                                                     |
| data[0].keepalive       | Integer | 保活。                                                       |
| data[0].protocol        | Integer | 协议版本。                                                   |
| data[0].connect_status  | Integer | 连接状态。                                                   |
| data[0].message_receive | Integer | 该客户端接受的消息。                                         |

#### **Examples**

```
$ curl -i --basic -u admin:public -X POST "http://localhost:8081/api/v1" -d '{"req": 5,"seq": 1111111}'
{"code":0,"seq":1111111,"rep":5,"data":[{"client_id":"nanomq-ebd54382","username":"nanmq","keepalive":60,"protocol":4,"connect_status":1,"message_receive":0}]
```

 

另一组是通过 HTTP API 来修改 NanoMQ 的配置参数，主要用于提供服务端远程管理 NanoMQ 的能力。

#### 设置配置参数：设置 Broker 配置参数。

**Parameters (JSON)**

| Name | Type    | Required | Value  | Description                                                  |
| :--- | :------ | :------- | :----- | :----------------------------------------------------------- |
| req  | Integer | Required | 12     | 请求码 *12*。                                                |
| seq  | Integer | Required | unique | seq 是全局唯一的，请求/响应信息都会携带该信息，可以通过该值确定对应的请求响应。 |
| data | Object  | Required |        | 同获取配置一致[data](https://nanomq.io/docs/zh/latest/http-api/v4.html#获取当前配置)。 |

**Success Response Body (JSON)**

| Name | Type    | Description                                                  |
| :--- | :------ | :----------------------------------------------------------- |
| code | Integer | 请求结果，0 表示成功                                         |
| seq  | Integer | seq 是全局唯一的，请求/响应信息都会携带该信息，可以通过该值确定对应的请求响应。 |
| rep  | Integer | rep 是 12 作为 req 12 的响应。                               |

> 注意：远程修改配置后，需要重启 NanoMQ 以生效。

关于其他 HTTP API 支持以及返回码和状态码具体细节请参阅 [https://nanomq.io/docs/zh/latest/http-api/v4.html](https://nanomq.io/docs/zh/latest/http-api/v4.html)。

## Bug 修复

本月，NanoMQ 继续收集社区反馈并积极修复问题。修复了如下重要 Bug，请使用旧版本的用户酌情升级。

1. 修复桥接连接在极高吞吐时会进入无响应状态的问题。
2. 修复了一个 NanoSDK 0.3 版本里的死锁问题。
3. 修复共享订阅和通配符共用时导致的无法收到消息的问题。

## 其他动态

NanoMQ 0.7.0 版本将会引入 SQLite 作为 QoS+ 会话保持/消息持久化缓存的选项。敬请关注。


<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a >
</section>
