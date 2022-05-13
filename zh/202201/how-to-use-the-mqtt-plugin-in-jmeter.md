如《[JMeter 测试组件介绍](https://www.emqx.com/zh/blog/introduction-to-jmeter-test-components)》所述，JMeter 内置 HTTP/HTTPS、TCP 等支持多种协议，还具备插件扩展机制。

[MQTT 协议](https://www.emqx.com/zh/mqtt)身为物联网界的主流协议，虽然并非 JMeter 自带的协议类型，但在物联网测试场景中极为普遍。为了支持 MQTT 协议的规模测试，[EMQ 映云科技](https://www.emqx.com/zh/about)开发了基于 JMeter 的 MQTT 协议开源测试插件：[https://github.com/xmeter-net/mqtt-jmeter](https://github.com/xmeter-net/mqtt-jmeter) 。

经过几个版本的迭代，目前 JMeter MQTT 插件的最新版本为 2.0.2，支持连接、消息发布、消息订阅等多种采样器，并可通过组合构建更复杂的测试场景。

本文我们将具体介绍如何在 JMeter 中使用 MQTT 插件。

## 安装 MQTT 插件

MQTT 插件的安装方式与其他 JMeter 第三方插件类似。

1. 从 GitHub 上下载最新版本插件 [mqtt-xmeter-2.0.2-jar-with-dependencies.jar](https://github.com/xmeter-net/mqtt-jmeter/releases/download/v2.0.2/mqtt-xmeter-2.0.2-jar-with-dependencies.jar)，该插件支持 JMeter 3.2 及以上版本。
2. 将插件 jar 包拷贝到 JMeter 的插件目录：`$JMETER_HOME/lib/ext`
3. 重新启动 JMeter。

## MQTT 插件中的主要组件

### MQTT 连接采样器(MQTT Connect)

连接采样器模拟物联网设备，发起 MQTT 连接。

![JMeter MQTT 连接](https://assets.emqx.com/images/ebd5536794031cd01db488838013cc27.png)

**Server name or IP:** 指向被测 MQTT 服务器地址。

**Port number:** 以 [EMQX](https://www.emqx.io/zh) 为例，默认 TCP 连接的端口是 1883, SSL 连接则是 8883。具体的端口请参照服务器的具体配置。

**MQTT version**: 目前支持 MQTT 3.1及3.1.1版本。

**Timeout:** 连接超时设置，以秒为单位。

**Protocols:** 支持TCP、SSL、WS 和 WSS 方式连接 MQTT 服务器。当选择 SSL 或 WSS 加密通道连接时，可以选择单向或者双向认证(Dual)。如果希望进行双向认证，还需要指定相应的客户端证书(p12证书)，以及对应的文件保护密码(Secret)。

**User authentication:** 如果 MQTT 服务器配置了用户认证，需要提供相应的用户名(**User name**)和密码(**Password**)。

**ClientId:** 虚拟用户的标识。如果勾选了「Add random suffix for ClientId」，将会在 ClientId 的基础上给每个虚拟用户再添加一个 uuid 串作为后缀，整个作为虚拟用户标识。

**Keep alive(s):** 心跳信号发送间隔。例如，300 表示客户端每隔 300 秒向服务器发出 ping 请求，以保持连接活跃。

**Connect attempt max:** 第一次连接过程中，尝试重连的最大次数。超过该次数则认为连接失败。如果希望一直尝试重连，可以设为 -1。

**Reconnect attempt max:** 后继连接过程中，尝试重连的最大次数。超过该次数则认为连接失败。如果希望一直尝试重连，可以设为 -1。

**Clean session**: 如果希望在连接之间保留会话状态，可以将该选项设为 false。如果不希望在新的连接中保留会话状态，则将该项设为true。

### MQTT 消息发布采样器(MQTT Pub Sampler)

消息发布采样器复用连接采样器中建立的 MQTT 连接，向目标 [MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)发布消息。

![JMeter 发布 MQTT 消息](https://assets.emqx.com/images/71728f02bf2886a7ce5d1c15dbd66a2b.png)

**QoS Level:** 服务质量，取值为 0，1，2，分别代表 MQTT 协议规范里的至多一次（AT_MOST_ONCE），至少一次（AT_LEAST_ONCE），精确一次（EXACTLY_ONCE）

**Retained messages**: 如果希望使用[保留消息](https://www.emqx.com/zh/blog/message-retention-and-message-expiration-interval-of-emqx-mqtt5-broker)，可将该选项设为 true，MQTT 服务器端将会存储插件发布的保留消息及其 QoS，并在相应 topic 上发生订阅时，直接将最后一条保留消息投递给订阅端，使得订阅端不必等待即可获取发布端的最新状态值。

**Topic name:** 发布消息所属的主题。

**Add timestamp in payload:** 如果勾选，发布的消息体开头会附带当前时间戳，配合消息订阅采样器的 Payload includes timestamp 选项，可以在消息接收端计算消息达到的延时。如果不勾选则只发送实际的消息体。

**Payloads** **Message type:** 目前支持三种消息类型

- String: 普通字符串
- Hex String: 以 16 进制数值表示的串，比如字符串 Hello, 可以表示为 48656C6C6F (其中，48在ascii表中对应字母H，依次类推)。通常 16 进制串用来构造非文本的消息体，例如描述某些私有的协议交互和控制信息等等。
- Random string with fixed length: 按指定长度（单位为byte）生成随机串作为消息体。

### MQTT 消息订阅采样器(MQTT Sub Sampler)

消息发布采样器复用连接采样器中建立的 MQTT 连接，从目标 MQTT 服务器上订阅消息。

![JMeter MQTT 消息订阅](https://assets.emqx.com/images/d46ae48963d4690ecaaab85ec0f38e61.png)

**QoS Level:** 服务质量，含义与消息发布采样器相同。

**Topic name(s):** 订阅消息所属的主题。支持单个消息订阅采样器订阅多个主题，主题之间用逗号分隔。

**Payload includes timestamp:** 如果勾选，会从消息体开头处解析发送时间戳，配合消息发布采样器的 Add timestamp in payload 选项，可以用于计算消息的接收延时。如果不勾选则只解析实际的消息体。

**Sample on**: 采样方式，默认为"**specified elapsed time(ms)**"，即每隔指定的毫秒时间采样一次。也可以选择"**number of received messages**"，即每接收到指定的消息数采样一次。

**Debug response:** 如果勾选，消息内容会打印在 JMeter 的响应结果中。该选项主要用于调试目的，正式运行测试不建议勾选，以免影响测试效率。

### MQTT 断开连接采样器(MQTT DisConnect)

断开连接采样器中建立的 MQTT 连接。

![JMeter 断开 MQTT 连接](https://assets.emqx.com/images/9be500573f56629d38adab8e264bdbc2.png)

> 为灵活起见，上述采样器中的属性值都可以引用 JMeter 的系统或自定义变量。

本文我们介绍了 JMeter MQTT 插件的各测试组件，在下期文章中我们将针对不同的测试场景详细介绍如何用 MQTT 插件来构建测试脚本。

## 本系列中的其它文章

- [开源测试工具 JMeter 介绍 - 物联网大并发测试实战 01](https://www.emqx.com/zh/blog/introduction-to-the-open-source-testing-tool-jmeter)
 
- [JMeter 测试组件介绍 - 物联网大并发测试实战 02](https://www.emqx.com/zh/blog/introduction-to-jmeter-test-components)

- [JMeter MQTT 在连接测试场景中的使用 - 物联网大并发测试实战 04](https://www.emqx.com/zh/blog/test-mqtt-connection-with-jmeter)

- [如何在 JMeter 中使用 MQTT 插件 - 物联网大并发测试实战 05](https://www.emqx.com/zh/blog/the-use-of-jmeter-mqtt-in-subscription-and-publishing-test-scenarios)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
