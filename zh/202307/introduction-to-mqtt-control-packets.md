## 什么是 MQTT 控制报文？

MQTT 控制报文是 MQTT 数据传输的最小单元。[MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)和服务端通过交换控制报文来完成它们的工作，比如订阅主题和发布消息。

MQTT 目前定义了 15 种控制报文类型，如果按照功能进行分类，我们可以将这些报文分为连接、发布、订阅三个类别：

![01mqttpackettypes.png](https://assets.emqx.com/images/8ce487b52492c28c8dcba8595f67dbb9.png)

其中，CONNECT 报文用于客户端向服务端发起连接，CONNACK 报文则作为响应返回连接的结果。如果想要结束通信，或者遇到了一个必须终止连接的错误，客户端和服务端可以发送一个 DISCONNECT 报文然后关闭网络连接。

AUTH 报文是 MQTT 5.0 引入的全新的报文类型，它仅用于增强认证，为客户端和服务端提供更安全的身份验证。

PINGREQ 和 PINGRESP 报文用于连接保活和探活，客户端定期发出 PINGREQ 报文向服务端表示自己仍然活跃，然后根据 PINGRESP 报文是否及时返回判断服务端是否活跃。

PUBLISH 报文用于发布消息，余下的四个报文分别用于 QoS 1 和 2 消息的确认流程。

SUBSCRIBE 报文用于客户端向服务端发起订阅，UNSUBSCRIBE 报文则正好相反，SUBACK 和 UNSUBACK 报文分别用于返回订阅和取消订阅的结果。

## MQTT 报文格式

在 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 中，无论是什么类型的控制报文，它们都由固定报头、可变报头和有效载荷三个部分组成。

固定报头固定存在于所有控制报文中，而可变报头和有效载荷是否存在以及它们的内容则取决于具体的报文类型。例如用于维持连接的 PINGREQ 报文就只有一个固定报头，用于传递应用消息的 PUBLISH 报文则完整地包含了这三个部分。

![02packetformat.png](https://assets.emqx.com/images/e67b987e03842cb19ca7608b14977f36.png)

### 固定报头

固定报头由报文类型、标识位和报文剩余长度三个字段组成。

![03fixedheader.png](https://assets.emqx.com/images/0bd7652ec917098f720f27b2a739427b.png)

报文类型位于固定报头第一个字节的高 4 位，它是一个无符号整数，很显然，它表示当前报文的类型，例如 1 表示这是一个 CONNECT 报文，2 表示 CONNACK 报文等等。详细的映射关系可以参阅 [MQTT 5.0 规范 - MQTT 控制报文类型](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901022)。事实上，除了报文类型和剩余长度这两个字段，MQTT 报文剩余部分的内容基本都取决于具体的报文类型，所以这个字段也决定了接收方应该如何解析报文的后续内容。

固定报头第一个字节中剩下的低 4 位包含了由控制报文类型决定的标识位。不过到 MQTT 5.0 为止，只有 PUBLISH 报文的这四个比特位被赋予了明确的含义：

- Bit 3：DUP，表示当前 PUBLISH 报文是否是一个重传的报文。
- Bit 2,1：QoS，表示当前 PUBLISH 报文使用的服务质量等级。
- Bit 0：Retain，表示当前 PUBLISH 报文是否是一个保留消息。

其他所有的报文中，这 4 位都仍是保留的，即它们是一个固定的，不可随意变更的值。

最后的剩余长度指示了当前控制报文剩余部分的字节数，也就是可变报头和有效载荷这两个部分的长度。所以 MQTT 控制报文的总长度实际上等于固定报头的长度加上剩余长度。

![04remaininglength.png](https://assets.emqx.com/images/ade1adbc7d07386cc453f943451ce36e.png)

#### 可变字节整数

但固定报头长度并不是固定的，为了尽可能地减少报文大小，MQTT 将剩余长度字段设计成了一个可变字节整数。

在 MQTT 中，存在很多长度不确定的字段，例如 PUBLISH 报文中的 Payload 部分就用来承载实际的应用消息内容，而应用消息的长度显然是不固定的。所以我们需要一个额外的字段来指示这些不定长内容的长度，以便接收端正确地解析。

一个 2 兆大小，也就是总共 2,097,152 个字节的应用消息，我们就需要一个 4 字节长度的整数才能够指示它的长度。但并不是所有的应用消息都有这么大，更多情况下是几 KB 甚至几个字节。用一个 4 字节长度的整数来指示一个总共 2 个字节长度的应用消息，显然是过于浪费了。

所以 MQTT 的可变字节整数就被设计出来了，它将每个字节中的低 7 位用于编码数据，最高的有效位用于指示是否还有更多的字节。这样，长度小于 128 字节时可变字节整数只需要一个字节就可以指示。可变字节整数的最大长度为 4 个字节，所以最多可以指示长度为 (2^28 - 1) 字节，也就是 256 MB 的数据。

![05variablebyteinteger.png](https://assets.emqx.com/images/413a52130ff5d651e076c336a78e9bb2.png)

### 可变报头

可变报头的内容取决于具体的报文类型。例如 CONNECT 报文的可变报头按顺序包含了协议名、协议级别、连接标识、Keep Alive 和属性这五个字段。PUBLISH 报文的可变报头则按顺序包含了主题名、报文标识符和属性这三个字段。

![06variableheader.png](https://assets.emqx.com/images/4a67e1522ecfafc48943667a01ab7396.png)

需要注意这里提到的顺序，可变报头中字段出现的顺序必须严格遵循协议规范，因为接收端只会按照协议规定的字段顺序进行解析。我们也不能随意地遗漏某个字段，除非是协议明确要求或允许的。例如，在 CONNECT 报文的可变报头中，如果协议名之后直接就是连接标识，那么就会导致报文解析失败。而在 PUBLISH 报文的可变报头中，报文标识符就只有在 QoS 不为 0 的时候才能存在。

#### 属性

属性是 MQTT 5.0 引入的一个概念。属性字段基本上都是可变报头的最后一部分，由属性长度和紧随其后的一组属性组成，这里的属性长度指的是后面所有属性的总长度。

![07propertiesinvariableheader.png](https://assets.emqx.com/images/441b27821f4c063e275ad15abd38542c.png)

所有的属性都是可选的，因为它们通常都有一个默认值，如果没有任何属性，那么属性长度的值就为 0。

每个属性都由一个定义了属性用途和数据类型的标识符和具体的值组成。不同属性的数据类型可能不同，比如一个是双字节长度的整数，另一个则是 UTF-8 编码的字符串，所以我们需要按照标识符所声明的数据类型对属性进行解析。

![08property.png](https://assets.emqx.com/images/fcc24e1b8bbd592a01a09aa41d1e490a.png)

属性之间的顺序可以是任意的，这是因为我们可以根据标识符知道这是哪个属性，以及它的长度是多少。

属性通常都是为了某个专门的用途而设计的，比如在 CONNECT 报文中就有一个用于设置会话过期时间的的 Session Expiry Interval 属性，但显然我们在 PUBLISH 报文中就不需要这个属性。所以 MQTT 也严格定义了属性的使用范围，一个合法的 MQTT 控制报文中不应该包含不属于它的属性。

包含标识符、属性名、数据类型和使用范围的完整 MQTT 属性列表，请参阅 [MQTT 5.0 Specification - Properties](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901027)。

### 有效载荷

最后是有效载荷部分。我们可以将报文的可变报头看作是它的附加项，而有效载荷则用于实现这个报文的核心目的。

比如在 PUBLISH 报文中，Payload 用于承载具体的应用消息内容，这也是 PUBLISH 报文最核心的功能。而 PUBLISH 报文的可变报头中的 QoS、Retain 等字段，则是围绕着应用消息提供一些额外的能力。

SUBSCRIBE 报文也是如此，Payload 包含了想要订阅的主题以及对应的订阅选项，这也是 SUBSCRIBE 报文最主要的工作。

 

## MQTT 报文 - 进阶

在后续的博客中，我们将介绍不同类型报文中包含的字段及其主要作用，并且基于真实的报文来展示这些字段在报文中的分布。这些博客包括：

- [MQTT 5.0 报文解析 01：CONNECT 与 CONNACK](https://www.emqx.com/zh/blog/mqtt-5-0-control-packets-01-connect-connack)
- [MQTT 5.0 报文解析 02：PUBLISH 与 PUBACK](https://www.emqx.com/zh/blog/mqtt-5-0-control-packets-02-publish-and-response-packets)
- [MQTT 5.0 报文解析 03：SUBSCRIBE 与 UNSUBSCRIBE](https://www.emqx.com/zh/blog/mqtt-5-0-control-packets-03-subscribe-and-unsubscribe)
- [MQTT 5.0 报文解析 04：PINGREQ 与 PINGRESP](https://www.emqx.com/zh/blog/mqtt-5-0-control-packets-04-pingreq-and-pingresp)
- [MQTT 5.0 报文解析 05：DISCONNECT](https://www.emqx.com/zh/blog/mqtt-5-0-control-packets-05-disconnect)
- [MQTT 5.0 报文解析 06：AUTH](https://www.emqx.com/zh/blog/mqtt-5-0-control-packets-06-auth)



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
