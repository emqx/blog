随着物联网技术的发展与普及，越来越多的智能设备具备了网络连接与数据传输能力。

物联网场景中设备大多都是资源限制型的，比如 CPU、RAM、Flash、网络宽带等。尤其是由电池供电的设备，对传输协议的功耗以及带宽非常敏感，直接使用 TCP 和 HTTP 协议来实现设备与平台之间的数据交换无法满足设备对低功耗的要求。

为了让这部分设备能够顺利接入网络，CoAP 协议应运而生。作为致力于为物联网各类场景提供数据连接能力的全托管 MQTT 消息服务，[EMQX Cloud](https://www.emqx.com/zh/cloud) 也支持 CoAP 协议的设备接入，允许符合某种定义的 CoAP 消息格式向 EMQX Cloud 执行发布、订阅、和接收消息等操作。

本文将介绍如何使用 EMQX Cloud 实现 CoAP 协议设备的接入。

## CoAP 协议简介

由于物联网场景复杂多样，设备端硬件条件、网络稳定性、流量限制、设备功耗以及设备连接数量等多方面因素造成物联网设备的消息传递与传统互联网场景有着很大不同，也因此产生了多种物联网通讯协议。

CoAP 协议网关作为一种在物联网世界的类 HTTP 的协议，使用在资源受限的物联网设备上，它的详细规范定义在 RFC 7252。

### 协议特性

CoAP 参考了很多 HTTP 的设计思路，同时也根据受限资源限制设备的具体情况改良了诸多设计细节，增加了很多实用的功能。如：

- 基于消息模型
- 传输层基于 UDP 协议，支持受限设备
- 使用类似 HTTP 请求的请求/响应模型，HTTP 是文本格式，CoAP 为二进制格式，且比 HTTP 更加紧凑
- 支持双向通信
- 轻量、低功耗
- 支持可靠传输，数据重传，块传输，确保数据可靠到达
- 支持 IP 多播
- 支持观察模式
- 支持异步通信

### 市场状况

相比于 [MQTT](https://www.emqx.com/zh/mqtt)，CoAP 更加轻量、开销更低，在某些特定的设备和网络环境下更为合适，EMQX Cloud 以及部分公有云物联网平台都提供提供了 CoAP 接入能力。

## CoAP 协议接入 EMQX Cloud

### 创建部署

[新建部署](https://docs.emqx.com/zh/cloud/latest/create/overview.html#限制)，在 EMQX Cloud 部署页面，获取到公网连接地址：120.77.x.x。

![EMQX Cloud 创建部署](https://assets.emqx.com/images/ea55ccbe53315026bec4f2a05fa3cd07.png)

### 开通 CoAP 接入网关

CoAP 接入网关目前处于内测阶段，您可以提交工单开启接入能力。开通后 CoAP 接入网关地址是您的部署连接地址，即 120.77.x.x，端口为 udp 5683 。

### 连接到部署、发布订阅消息

[libcoap](https://github.com/obgm/libcoap) 是一个非常易用的 CoAP 客户端库，此处我们使用它作为 CoAP 客户端来测试 EMQX Cloud CoAP 接入网关的功能。

安装部署可参考如下示例。

```shell
git clone http://github.com/obgm/libcoap
cd libcoap
./autogen.sh
./configure --enable-documentation=no --enable-tests=no
make
```

#### 1、发布示例

我们使用 libcoap 往 EMQX Cloud 部署发布一条消息：

- 主题名称为："topic1"
- Client ID 为："client1"
- 用户名为："emqx"
- 密码为："public"
- Payload 为："hello,EMQX Cloud"

```shell
# CoAP 终端发送消息 "hello EMQX Cloud"，topic 为 topic1
./examples/coap-client -m put -e "hello,EMQX Cloud" "coap://120.77.x.x:5683/mqtt/topic1?c=client1&u=emqx&p=public" 
```

![CoAP 消息发送](https://assets.emqx.com/images/d7b4f28d0d0d9223eaf59b9a8ccb6194.png)

接下来，我们使用 [MQTT X](https://mqttx.app/zh) 订阅对应主题 topic1，即可看到消息已成功发布。

![MQTT X 消息接收](https://assets.emqx.com/images/2d3a34b5c2678b77be69a08e409f0b43.png)

#### 2、订阅示例

我们使用 libcoap 订阅一个主题：

- 主题名称为："topic1"
- Client ID 为："client1"
- 用户名为："emqx"
- 密码为："public"
- Payload 为："hello,EMQX Cloud"

接下来，我们使用 MQTT X 发送 "hello,EMQX Cloud" 给 `topic1` 主题。

![MQTT X 消息发送](https://assets.emqx.com/images/0a12db9e69ea71637541339313da231d.png)

```shell
# CoAP 终端订阅 topic1 主题，-s 20表示订阅维持20秒
 ./examples/coap-client -m get -s 20 "coap://120.77.x.x:5683/mqtt/topic1?c=client1&u=emqx&p=public"
```

在这期间，如果主题 topic1 上有消息产生，libcoap 便会收到该条消息。

![CoAP 消息接收](https://assets.emqx.com/images/e0881e98563d4f1d2228bbbccc6b3f75.png)

## **小结**

至此，我们完成了使用 CoAP 协议网关接入 EMQX Cloud 的全部流程。

当前物联网协议呈现多元化发展，不同行业和场景适用不同的协议，在相同的场景下也能够有多个协议可供选择，没有任何协议能够在市场上占有统治地位，各种协议之间存在一定的互补效应。因此，要实现物联网设备和数据的互联互通，关键点并不在与协议的统一，而在于不同协议之间的互联互通、上层业务应用层协议的统一。CoAP 协议网关则为解决物联网设备数据连接问题提供了新的可能性。而 EMQX Cloud 支持多协议接入，通过开放标准的物联网协议 MQTT、MQTT over WebSocket、CoAP/LwM2M 将数以亿计的物联网设备可靠地连接到 EMQX Cloud，让物联网数据发挥出更大的价值。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
