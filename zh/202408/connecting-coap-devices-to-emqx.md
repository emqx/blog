## 引言

[CoAP](https://www.emqx.com/en/blog/coap-protocol) 协议是一种支持在低功耗、低功率等受限设备间进行通信的物联网协议。这些设备往往都运行在受限网络中，因此 CoAP 协议设计得十分精炼，并采用 UDP 协议进行数据传输，能够很好的适应受限网络环境。 CoAP 通过类似于 HTTP 操作的方式，对设备上抽象的资源进行操作，这样能够十分简洁、高效地实现受限设备间同步、 异步的信息交流。

CoAP 是专为受限硬件、环境而设计的通信协议，在受限网络中能够良好的工作，但如果受限网络需要和外部网络进行沟通，CoAP 则不能很好地适应。另外，因为 CoAP 设计时更多考虑的是 M2M 网络模型，所以 CoAP 缺乏对资源处理中心的支持（基于 CoAP 的 LwM2M 协议为此专门引入了资源的注册、资源的服务等概念）。

以上问题可以通过 [EMQX](https://www.emqx.com/zh/products/emqx) 消息服务器得到解决。本文将介绍如何使用 EMQX 接入 CoAP 协议，实现 CoAP 协议设备与外部的沟通。

## EMQX 5.0 的 CoAP 协议接入方式

对于需要和外部进行沟通的 CoAP 设备，使用 EMQX 作为消息中间件，可以很方便地实现以下功能：

- 对设备进行认证，拒绝不可信设备的数据
- 对资源进行权限管理，可以指定不同的设备对某个资源拥有不同的读/写权限
- 可以作为不同网络 CoAP 设备间的信息传输中心
- 可以作为其他应用，比如 CoAP 管理应用、数据分析应用和 CoAP 设备、网络间的接入中间件

EMQX 中提供了两种不同的 CoAP 接入方式，涵盖了大多数 CoAP 的业务场景，且接入简单，支持良好，不需对 CoAP 协议本身进行改动。而对原有的 CoAP 设备、应用，接入 EMQX 的成本也很小。

### 连接模式

EMQX 5.0 中提供了连接模式以支持 CoAP 客户端的生命周期管理。例如：

- 使用 `clientid`、`username` 和 `password` 创建一个经过身份验证的 CoAP 连接，并返回一个授权的 Token。
- 使用 `clientid` 和`token`销毁 CoAP 连接。

其 URI 地址格式如下：

```
{Method} {Type}://{Host}:{Port}/mqtt/connection?{QueryString} 
```

例如，使用用户名和密码创建一个 CoAP 连接：

```
POST coap://127.0.0.1:5683/mqtt/connection?clientid=test&username=user1&password=pwd 
```

当不需要管理 CoAP 客户端时，连接模式是可选的。然而，当 CoAP 客户端与 EMQX 通过公共网络通信时，连接模式非常有用。通过使用连接创建时提供的用户名和密码，可以确保一定程度的安全性。

### PubSub 模式

这种模式允许 CoAP 客户端与 EMQX 中的 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)互操作。包括以下内容：

- CoAP 客户端向特定主题发布消息。
- CoAP 客户端订阅一个主题并从该主题接收消息。

在这种模式下，URI 地址的格式为：

```
{Method} {Type}://{Host}:{Port}/ps/{topic}?{QueryString} 
```

例如，要发布一条 `Hello, CoAP!` 的消息到主题 `test/topic` ，CoAP 客户端应使用以下格式：

```
POST coap://127.0.0.1:5683/ps/test/topic?qos=1

Hello, CoAP!
```

CoAP 客户端订阅并接收来自 `test/topic` 主题的消息的请求格式为：

```
GET coap://127.0.0.1/ps/test/test 
```

这种模式是 EMQX 为 CoAP 客户端提供与 MQTT 协议通信的主要方式。

## **在 EMQX 中配置 CoAP 网关**

在 EMQX 5.0 中，可以通过 Dashboard、HTTP API 和配置文件 `emqx.conf` 来配置和启用 CoAP 网关。本节将以 Dashboard 配置为例说明操作步骤。

### 非加密通信场景的默认配置

在 EMQX Dashboard 上，点击左侧导航菜单中的 “插件扩展” -> “网关”。该页面列出了所有支持的网关。找到 CoAP 并点击操作栏中的 “设置”。然后，您将进入初始化 CoAP 页面。

![EMQX Dashboard](https://assets.emqx.com/images/f59d9be10f2b1866edd99dad815bab71.png)

在这个基本配置页面上，我们可以选择是否启用连接模式。默认情况下，连接模式为关闭，即 `Connection Required = false`。

确认连接模式后，您可以继续进行设置。如果不需要大规模的自定义，您只需点击三次即可启用 CoAP 网关：

1. 在基本配置选项卡中点击“下一步”以接受所有默认设置。
2. 然后您将进入监听器选项卡，EMQX 已预配置了端口 5683 上的 UDP 监听器。再次点击“下一步”确认设置。
3. 最后点击“启用”按钮以激活 CoAP 网关。

### 加密通信场景

默认情况下，端口 5683 上已经配置了一个名为 `default` 的 UDP 监听器，它仅支持纯 UDP 数据传输。EMQX 的 CoAP 协议网关还支持 DTLS 安全传输层协议，可以配置单向/双向认证。

从 EMQX 5.0 开始，可以通过 EMQX Dashboard 轻松进行配置。您可以点击 CoAP 网关的“设置”按钮进行更多自定义设置，然后点击“添加监听器”以添加新的监听器。

 ![监听器](https://assets.emqx.com/images/153129215213e57b3e004b9d9af9e67c.png)

例如，我们添加了一个名为 `default-tls` 的 DTLS 类型监听器，并将其绑定到端口 5684：

![添加监听器](https://assets.emqx.com/images/87656110f1df590d1f763419838126e8.png)

您可以通过设置切换开关来决定是否启用“验证对等方”，以启用双向认证。但在此之前，您需要通过输入文件内容或使用“选择文件”按钮上传相关的 TLS 证书、TLS 密钥和 CA 证书信息进行配置。

## 测试和验证

### 安装 CoAP 测试用客户端

#### coap.me

如果在 EMQX 的 CoAP 协议网关上配置的是公网 IP，可以使用 [coap.me](https://coap.me/) 这个在线网站进行测试。具体使用方法见网站说明。

#### libcoap

libcoap 是一个 C 语言实现的、对 CoAP 所有相关标准都有完善支持的库，自带一个客户端应用，一般被视作 CoAP 的标准校验客户端。

在大多数 Linux 系统中，可以使用系统的包管理器进行安装，在 macOS 上可以使用 brew 进行安装，其他平台可能需要手动编译源代码。

本文我们使用了一个预先编译好的 libcoap 镜像：

```shell
$ docker run -it --rm --name libcoap --network host heeejianbo/my-libcoap:1.0 
```

通过在其中运行 `coap-client` 命令，我们可以查看当前使用的 CoAP 客户端版本：

```shell
$ coap-client
coap-client v4.3.1 -- a small CoAP implementation
Copyright (C) 2010-2022 Olaf Bergmann <bergmann@tzi.org> and others

Build: v4.3.1-4-g02b7647
TLS Library: OpenSSL - runtime 1.1.1t, libcoap built for 1.1.1t
(DTLS and TLS support; PSK, PKI, PKCS11, and no RPK support)

```

### 安装 MQTT 客户端

为了测试 CoAP 客户端与 MQTT 协议之间的交互，我们还需要安装一个 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)。我们推荐使用 MQTTX CLI。

具体安装方法请参见：[MQTTX Download](https://mqttx.app/zh/downloads) 

### 测试 PubSub 模式

#### 发布消息

我们可以测试 CoAP 作为发布者发送消息、MQTTX 作为订阅者接收消息的情况。

使用以下命令为 MQTTX 创建一个客户端，并订阅 `test/topic` 主题：

```shell
mqttx sub -h 127.0.0.1 -p 1883 -i sub -t test/topic -q 2 
```

然后使用 coap-client 向 `test/topic` 发布 3 条消息进行测试：

```shell
coap-client -m post -e "Hello, CoAP" "coap://127.0.0.1/ps/test/topic?qos=0" 
```

测试结果如下面的图所示。从左侧的图片可以看出，作为订阅者的 MQTTX 成功接收到了这三条不同 QoS 等级的消息。

![发布消息](https://assets.emqx.com/images/20f3b2a04fe0e4c47b169849df2029d1.png)

#### 接收消息

同样，我们也可以测试 MQTTX 作为发布者、CoAP 客户端作为订阅者接收消息的情况。

首先，使用以下命令创建一个 CoAP 订阅者，并等待 60 秒以接收 `test/topic` 主题上的消息：

```shell
coap-client -m get -s 60 -O 6,0x00 -o - -T "obstoken" "coap://127.0.0.1/ps/test/topic" 
```

然后，通过 MQTTX 向 `test/topic` 主题发布三条消息：

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/topic -q 2 
```

测试结果如下图所示，右侧的 CoAP 客户端成功接收到了这三条来自 MQTTX 的“Hello From MQTTX”消息。

![接收消息](https://assets.emqx.com/images/f37a8bd227658aeca1b18d9ae2be6675.png)

### 测试连接模式

在连接模式下，CoAP 客户端需要与 EMQX 创建连接，并获得授权凭证以进行后续的消息发布和接收，否则会出现权限错误。

#### 启用连接模式

进入 CoAP 网关的设置页面，将 `连接模式` 修改为 `true` 以启用连接模式，然后点击“更新”按钮以保存配置。

![连接模式](https://assets.emqx.com/images/7abe0a75ff7e8916e3e0b7483c0cc68f.png)

#### 创建连接

CoAP 客户端可以通过请求 `/mqtt/connection` 来创建连接，例如：

```shell
coap-client -m post -e "" "coap://127.0.0.1/mqtt/connection?clientid=123&username=adm in&password=public" 
```

连接成功创建后，将返回一个 Token。如下图所示，Token 为 `769721171`。

![返回一个 Token](https://assets.emqx.com/images/2696daf0c87713c8a04861d149ec816f.png)

#### 在连接模式下发送消息

在连接模式下发送消息需要提供 Token 和 ClientId 参数，例如：

```shell
coap-client -m post -e "Hi, Connection Mode" "coap://127.0.0.1/ps/test/topic?clientid=123& token=769721171" 
```

测试结果如下：

![测试结果](https://assets.emqx.com/images/85c21008187b16d0ae04a4a05e6226b8.png)

如果使用了错误的 Token，将返回 4.01，表示操作未经授权。

![返回 4.01](https://assets.emqx.com/images/6609b858da98ae12b00ae6c1977d50dc.png)

## 结语

至此，我们完成了 CoAP 协议设备接入 EMQX 的完整流程，实现了 CoAP 协议设备和 MQTT 协议设备的整合。作为一款强大的大规模分布式物联网消息服务器，EMQX 不仅完整支持 MQTT 协议，同时支持 CoAP、LwM2M 协议，为各类终端设备的接入提供便利。

关于使用 EMQX 的更多详细信息，请参考 [EMQX 文档](https://docs.emqx.com/zh/emqx/latest/)。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
