CoAP 协议是一种支持在低功耗、低功率等受限设备间进行通信的物联网协议，这些设备往往都运行在受限网络中，因此 CoAP 协议设计得十分精炼， 同时采用 UDP 协议进行数据传输，所以能够很好的适应受限网络环境。 CoAP 通过类似于 HTTP 操作的方式，在受限设备组成的 M2M 网络中，对设备上抽象的资源进行操作，这样能够十分简洁、高效地实现受限设备间同步、 异步的信息交流。

CoAP 是专为受限硬件、环境而设计的通信协议，在受限网络中能够良好的工作，但如果受限网络需要和外部网络进行沟通，CoAP 则不能很好的适应。另外，因为 CoAP 设计时更多考虑的是 M2M 网络模型，所以 CoAP 缺乏对资源处理中心的支持（基于 CoAP 的 LwM2M 协议为此专门引入了资源的注册、资源的服务等概念）。

以上问题可以通过 [EMQX](https://www.emqx.com/zh/products/emqx) 消息服务器得到很好的解决。本文就将介绍如何使用 EMQX 接入 CoAP 协议，实现 CoAP 协议设备与外部的沟通。

## EMQX 的 CoAP 协议接入方式

对于需要和外部进行沟通的 CoAP 设备，使用 EMQX 作为消息中间件，可以很方便地实现以下功能：

- 对设备进行认证，拒绝不可信设备的数据
- 对资源进行权限管理，可以指定不同的设备对某个资源拥有不同的读/写权限
- 可以作为不同网络 CoAP 设备间的信息传输中心
- 可以作为其他应用，比如 CoAP 管理应用、数据分析应用和 CoAP 设备、网络间的接入中间件

EMQX 中提供了两种不同的 CoAP 接入方式，涵盖了大多数 CoAP 的业务场景，且接入简单，支持良好，不需对 CoAP 协议本身进行改动。而对原有的 CoAP 设备、应用，接入 EMQX 的成本也很小。

### URL 模型

EMQX 通过 URL path 和 queryString 来实现对 CoAP 的接入，CoAP 接入时需要按照下面的规则组织 URL 模型:

```
coap 连接类型://Host:Port/模式/TopicName?c=客户端Id&u=用户名&p=密码
```

其中，**coap 连接类型**可以为:

- coap：使用普通的 UDP 进行传输
- coaps：启用安全传输层，关于如何启用 coaps (包括单向认证、双向认证)，详细见加密通信配置

**模式** 目前有: [MQTT](https://www.emqx.com/zh/mqtt-guide) 和 **PubSub** 两种，具体区别将会在下文详细介绍。

**TopicName** : EMQX 中使用 Topic 作为 CoAP 中的资源标识符，一个 Topic 就代表一个资源对象， 而 Topic 可以为任意 UTF8 字符串，允许多个层级，比如 coap/ 、coap/test/queryString。

URL 中的 c、u、p 三个字段是必须的，其中：

- c 代表客户端 ID，为任意字符串，理论上每个客户端 ID 都应该需要是唯一的
- u 和 p 分别代码用户名和密码，需要在 EMQ X 的认证模块中预先设置好

### MQTT 模式

MQTT 模式按照 MQTT 标准，对 CoAP 的 Method 进行转义，只有简单的 Pub/Sub 行为，转义对照表如下：

| Method | Token | MQTT        |
| ------ | ----- | ----------- |
| GET    | 0     | Subscribe   |
| GET    | 1     | UnSubscribe |
| GET    | _     | 非法操作    |
| PUT    | _     | Publish     |
| POST   | _     | 非法操作    |
| DELETE | _     | 非法操作    |

该模式适用于以下场景:

- 只需要使用 EMQX 进行消息、指令或者其他实时信息传输
- 如果需要长时间使用 **Observe** 功能， 则需要处于专用网络或者内网中
  这点比较重要，因为 UDP 是无连接的，所以在公网上产生的 UDP 链路是无法长时间保持的，这会导致 **Observe** 可能无法正常接受到数据
- 如果处于公网，则 **Observe** 只能用来做为 **PUT** 操作的结果监听机制，例如:
  假设一个 CoAP 设备需要通过 EMQX 向另外的其他设备发送指令、数据，并且根据返回的数据进行后续处理，则可以:
  1. 使用 **PUT** 方法向某个 Topic 发送指令
  2. 使用 **Observe** 方式监听这个 Topic
  3. 根据 EMQX 返回的数据进行处理
     鉴于公网中 UDP 链路的维持时间，Observe 的时间在 30s 以内是安全的，在 15s 内是足够安全的

### PubSub 模式

PubSub 模式相对于 MQTT 模式来说更加复杂些，但是也相对更符合 CoAP 中「资源」的概念，所有 Publish 的消息，会被当作「资源」存放在 EMQX 内，超时时间采用 CoAP 协议中的 **max-age** 可选字段进行控制，在超时前，消息都能通过 *GET* 方法获取到。

转义关系如下:

| Method | Token | MQTT        | Resouce                 |
| ------ | ----- | ----------- | ----------------------- |
| GET    | 0     | Subscribe   | _                       |
| GET    | 1     | UnSubscribe | _                       |
| GET    | _     | _           | 读取该 Topic 对应的消息 |
| PUT    | _     | Publish     | 更新该 Topic 对应的消息 |
| POST   | _     | Publish     | 更新该 Topic 对应的消息 |
| DELETE | _     | _           | 删除该 Topic 对应的消息 |

这种模式相当于上面的 **MQTT** 模式的扩展，除了上述适用场景外，还适用于以下场景:

- 使用 EMQX 作为数据、信息等资源的交换汇总中心的场景
  比如监控环境的 CoAP 设备,可以定时将自己采集到的数据 **PUT** 到 EMQX 中，而数据处理中心则通过订阅相关主题来接收这些数据，以此对环境状况进行分析；
  又比如 CoAP 设备可以定时将自身状态推送到 EMQX 中，用户则可以通过 EMQX 直接观察设备的运行状态。
- 消息传输的频率低、对时延容忍度高的场景
  这种场景中，可以使用 **PUT** 更新某个 Topic 的消息，而对该 Topic 感兴趣的客户端则可以按照自己的节奏，通过 **GET** 来获取最新的消息、数据等。

## 配置方法

EMQX 的 CoAP 协议网关相关配置在 emqx.conf 文件中，下面将会详细介绍。

### 非加密通信场景

对于数据敏感性不高，或者不需要传输链路保证通信安全的情况下，可以简单按照业务需求打开对应的端口进行监听即可。

比如下面的配置，在所有可用 IP 上监听 5683 端口，且在局域网 IP 192.168.1.2 上监听 5684 端口

```
coap.bind.udp.1 = 0.0.0.0:5683
coap.bind.udp.2 = 192.168.1.2:5684
```

### 加密通信场景

EMQX 的 CoAP 协议网关支持 DTLS 安全传输层协议，同时可配置单向/双向认证，默认配置会自动打开单向认证。

#### 单向认证

单向认证的配置如下，如果不需要启用加密通信，应该注释掉这些配置。

```
## DTLS 监听的端口, 配置方式和上面的udp模式一样,可用按照需要配置多个端口
coap.dtls.port1 = 5684
coap.dtls.port2 = 192.168.1.2:6585

## DTLS 的私钥
## Value: File
coap.dtls.keyfile = {{ platform_etc_dir }}/certs/key.pem

## DTLS 的证书文件
## Value: File
coap.dtls.certfile = {{ platform_etc_dir }}/certs/cert.pem
```

#### 双向认证

EMQX 的 CoAP 协议网关也支持双向认证，配置如下：

```
## 验证模式, 可选值为: verify_peer | verify_none
coap.dtls.verify = verify_peer

## 客户端没有发送证书时是否拒绝连接
coap.dtls.fail_if_no_peer_cert = false

## pem格式的CA证书
coap.dtls.cacertfile = {{ platform_etc_dir }}/certs/cacert.pem
```

**coap.dtls.verify** 用来决定是否开启双向认证, 可选值为:

- verify_peer 验证客户端
- verify_none 不验证客户端

当双向认证开启时， coap.dtls.fail_if_no_peer_cert 用来决定当客户端没有发送证书时,服务器是否拒绝连接。
coap.dtls.cacertfile 为 pem 格式的CA证书，用来对客户端进行验证。关于双向认证，具体可以参考[EMQX 启用双向 SSL/TLS 安全连接](https://www.emqx.com/zh/blog/enable-two-way-ssl-for-emqx)。

## 测试和验证

### 开启 CoAP 协议网关

#### 使用 Dashboard 开启

在 Dashboard 中的 插件 目录下，选择 emqx_coap 点击开启即可，如图:

![EMQX CoAP 插件](https://assets.emqx.com/images/685cbdd5e4490d07a53f6caf9d2e4ffd.jpeg)

#### 使用终端开启

在终端可使用下面的指令开启 emqx_coap 功能:

```
./bin/emqx_ctl plugins load emqx_coap
```

### 安装 CoAP 测试用客户端

#### coap.me 

如果在 EMQX 的 CoAP 协议网关上配置的是公网 IP，可以使用[https://coap.me/](https://coap.me/)这个在线网站进行测试。具体使用方法见网站说明。

#### libcoap

libcoap 是一个 C 语言实现的、对 CoAP 所有相关标准都有完善支持的库，自带一个客户端应用，一般被视作 CoAP 的标准校验客户端。

在大多数 Linux 系统中，可以使用系统的包管理器进行安装，在 macOS 上可以使用 brew 进行安装，其他平台可能需要手动编译源代码。

安装好后的客户端一般叫做：coap-client 或者 libcoap。

### 测试 PubSub 模式

下面使用 libcoap 演示，先向服务器 publish 一个消息后，再读取该 Topic 对应的最新消息

```
# 使用 PubSub 模式,以 put 方法向 coap/test Topic 推送一条 json 格式的消息
coap-client -m put -e '#{msg => "Hello, CoAP"}' -t json "coap://127.0.0.1:5683/ps/coap/test?c=clientid1234&u=admin&p=public"

# 读取 coap/test 这个 Topic 最后一条消息, 将会得到 #{msg => "Hello, CoAP"}
coap-client -m get  "coap://127.0.0.1:5683/ps/coap/test?c=clientid1234&u=admin&p=public"
```

下面的例子演示如何进行订阅:

```
## 订阅 coap/observe 这个 topic, Token 设置为"token", 订阅超时为 60s
coap-client -m get -s 60 -B 30 -o - -T "token" "coap://127.0.0.1:5683/ps/coap/observe?c=clientid1234&u=admin&p=public"

## 使用另外一个 CoAP 客户端进行推送, 也可以使用其他任意的 MQTT 客户端
coap-client -m post -e '#{msg => "This is Observe"}' -t json "coap://127.0.0.1:5683/ps/coap/observe?c=clientid1234&u=admin&p=public"

## 这个时候订阅者将会收到:
## #{msg => "This is Observe"}
```

### 测试 MQTT 模式

MQTT 模式的测试和上面一样，只不过只有 publish/subscribe 两种操作。例子如下:

```
## publish
coap-client -m put -e '#{msg => "Hello, CoAP"}' -t json "coap://127.0.0.1:5683/mqtt/coap/test?c=clientid1234&u=admin&p=public"

## subscribe
coap-client -m get -s 60 -B 60 -o - -T "token" "coap://127.0.0.1:5683/mqtt/coap/sub?c=clientid1234&u=admin&p=public"
```

## 结语

至此，我们完成了 CoAP 协议设备接入 EMQX 的完整流程，实现了 CoAP 协议设备和 MQTT 协议设备的整合。

作为一款强大的开源分布式云原生物联网消息服务器，EMQX 不仅完整支持 MQTT 协议，同时支持 CoAP、LwM2M 协议，为各类终端设备的接入提供便利。

关于 EMQX 的详细使用，可参考 [EMQX  企业版文档](https://docs.emqx.com/zh/enterprise/latest/)。也可访问 EMQX GitHub 项目地址：[https://github.com/emqx/emqx](https://github.com/emqx/emqx) 关注 EMQX 开源项目最新进展。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
