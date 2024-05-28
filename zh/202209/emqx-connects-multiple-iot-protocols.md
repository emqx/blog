## 引言：统一管理的网关框架

作为一款大规模分布式物联网 MQTT 消息服务器，EMQX 除了完整支持 MQTT 3.x 和 5.0，还支持  STOMP、[MQTT-SN](https://www.emqx.com/zh/blog/connecting-mqtt-sn-devices-using-emqx)、LwM2M/[CoAP](https://www.emqx.com/zh/blog/connecting-coap-devices-to-emqx)，JT/T 808 等多种主流协议接入。不仅提供了广泛的连接能力，以处理适用于各类场景的物联网设备；还为后端的物联网管理服务提供了统一接入平台和管理接口，以降低异构协议间的适配成本。

在[最新发布的 EMQX 5.0 ](https://www.emqx.com/zh/blog/emqx-v-5-0-released)中，我们重构了多协议接入的底层架构，统一了配置格式和管理接口，提供了一个全新的扩展网关框架。同时规范了各类网关的实现，使得各个网关功能定义更为清晰。

本文将对 EMQX 5.0 全新的网关框架及功能使用进行详细解读，帮助读者更好地利用 EMQX 强大的多协议接入支持能力连接各类协议设备，满足更多物联网场景的数据接入需求。

## EMQX 网关框架概述

由于设备的接入协议种类繁多，各个协议对连接登录、消息传输等拥有不同定义，这通常要求服务端部署各种协议的接入服务，导致软件和维护的成本急剧上升。EMQX 自发布以来就提供了多协议接入的支持，来屏蔽接入层协议的异构，以降低用户的开发和运营成本。

在 5.0 版本之前，EMQX 的多协议支持通过发布各类协议的接入插件来实现，这些独立的插件之间缺乏统一的定义和标准，相对来说有一定的使用难度。

为了给用户带来更加便捷易用的多协议支持，EMQX 5.0 对整个多协议接入架构进行了重构。所有非 MQTT 协议的接入都被统称为网关（Gateway）。所有网关由一个统一的框架提供通用操作的支持，包括：

- **统一的用户层接口：**该框架提供了风格统一的配置文件、HTTP API 和命令行接口。以监听器参数配置为例，4.x 版本中不同协议插件对于监听器暴露的参数各不相同，而在 5.0 版本中这些参数的风格都将是统一的。
- **统一的统计和监控指标：**提供了网关和客户端级别的统计指标，例如收发字节数、消息等。
- **独立的连接和会话管理：**每个网关都有在自己的客户端管理页面，且不同的网关允许使用相同的 Client ID ，而不是像 4.x 版本一样都混合在 MQTT 客户端列表中进行管理。
- **独立的客户端认证：**支持为每个网关配置独立的认证，不再像 4.x 像一样与 MQTT 客户端认证混合在一起。
- **易扩展和规格清晰化：**框架抽象了一套标准的概念和接口使自定义网关变得更加容易。

![多物联网协议网关统一框架](https://assets.emqx.com/images/8709d555d3a60f4e36aa99086704bd7b.png)

<center>网关统一框架</center>

 

每个网关内的实现，和之前类似：

- **监听器：**每个网关可以启动多个监听器来接受客户端的网络请求，监听器类型支持 TCP、SSL、UDP、DTLS。每类网关支持的监听器类型各有不同。
- **报文解析：**每个网关都有属于自己的报文解析模块，负责处理该协议的报文。
- **连接/会话：**负责创建连接、会话，并处理协议中定义的各种行为，例如登录认证、消息收发等。
- **消息模型转换：** 负责处理本网关与 MQTT PUB/SUB 消息模型的兼容。例如，将 LwM2M 中的消息转换为 EMQX 中带主题和 QoS 的消息。

![网关内部组件](https://assets.emqx.com/images/ceaf48c9c9c9f8896b14e38cbd753c66.png)

<center>网关内部组件</center>


## 网关通用行为规范

除了上述架构上的重构，EMQX 5.0 的网关还对**接入认证**和**消息收发**这类通用行为进行了统一。

### 接入认证：客户端信息

网关统一使用**客户端信息**进行认证，客户端信息由网关在处理该客户端接入时创建的，其中：

- 无论哪种网关，其客户端信息都包含通用字段，例如 Client ID、Username、Password 等（即使该协议无该字段的定义，网关会为其设置合适的默认值）同样也包括 Peername、ProtoName、Peercert 等
- 每种网关也有其特定的客户端信息，例如 LwM2M 有 Endpoint Name 和 Life Time 等。

因此，在执行客户端认证时，此类通用的客户端字段和特有的字段都可以作为参数传递给认证器执行验证。

### 消息收发：PUB/SUB 消息模型转换

为了适配 MQTT 的 PUB/SUB 消息模型，每类网关都必须完成对这种消息模型的兼容，以达到相互通信的目的。对于 PUB/SUB 类型的协议网关，例如 MQTT-SN、STOMP 通常定义了主题和消息负载的概念，则：

- 直接使用客户端指定的主题和消息内容
- 选择一个合适的值作为消息的 QoS。

但对于非 PUB/SUB 类型的协议，它缺少对主题、发布、订阅等概念的定义，则：

- 需要为其指定消息主题。例如 LwM2M 网关，用户可以配置各个类型消息的主题。
- 需要为其设计消息内容的格式。每种类型的网关都可能会使用不同的消息格式。

## EMQX 5.0 网关框架详解

### 客户端认证

EMQX 4.x 中每种类型设备都和 MQTT 使用相同的认证链，这种耦合导致在配置认证器时，需要考虑每种网关的异构情况：

![EMQX 4.x：不同类型网关认证耦合](https://assets.emqx.com/images/a29678572fdf86211ea3e8896a6e9e0b.png)

<center>EMQX 4.x：不同类型网关认证耦合</center>


在 EMQX 5.0，网关框架允许为每种类型的网关都配置专属于自己的认证器：


![EMQX 5.0:独立的客户端认证](https://assets.emqx.com/images/a20d49d9feafe7fa64de03b9e8fdd2dc.png)

<center>EMQX 5.0:独立的客户端认证</center>

 

### 消息模型转换

**消息模型转换不适用于已定义 PUB/SUB 等概念的网关。**例如 MQTT-SN 协议已经定了发布/订阅的行为，则 MQTT-SN 网关会：

- 将协议中的 PUBLISH 报文，作为消息发布，其主题和 QoS 都由该报文指定。
- 将协议中的 SUBSCRIBE 报文，作为订阅操作，其主题和 QoS 都由该报文指定。
- 将协议的 UNSUBSCRIBE 报文，作为取消订阅操作，其主题由该报文指定。

**消息模型转换也不适用于具有与 PUB/SUB 模型概念相近的网关。**例如 STOMP 协议完全兼容此消息模型，则 STOMP 网关会：

- 将协议中的 SEND 报文作为消息发布。其主题为 SEND 报文中的 `destination` 字段，消息内容为 SEND 报文的消息体内容，QoS 固定为 0。
- 将协议中的 SUBSCRIBE 报文作为订阅请求。其主题为 SUBSCRIBE 报文中的 `destination` 字段，QoS 固定为 0。且支持 MQTT 协议中定义的通配符。
- 将协议中 UNSUBSCRIBE 报文作为取消订阅请求。其主题为 UNSUBSCRIBE 报文中的 `destination` 字段。

**消息模型转换仅适用于未定义 PUB/SUB 等概念的网关。**例如 LwM2M 协议，则需要为其新增一些配置，来指定使用的主题格式，以及网关会内置一些规则来组织消息内容的格式：

```
gateway.lwm2m {

  mountpoint = "lwm2m/${endpoint_name}/"

  translators {  
    // 下行命令主题。
    // 对于每个成功上线的新 LwM2M 客户端，网关会创建一个订阅关系来接收下行消息并将其发送给客户端
    command {
      topic = "dn/#"
      qos = 0
    }                                         
    
    // 用于发布来自 LwM2M 客户端的注册事件的主题                   
    register {
      topic = "up/register"
      qos = 0
    }
    ...                                   
  } 
}
```

则，如果一个 `endpoint_name` 为 `epn1` 的客户端上线后：

- 网关会为其代理订阅 `lwm2m/epn1/dn/#` 主题，以期望接收下行的控制消息
- 网关会将该客户端的 REGISTER 消息，发布到 `lwm2m/epn1/up/register` 主题上。其消息格式由 LwM2M 网关的定义的数据转换规则决定，例如 REGISTER 消息的格式为：

```json
{ "msgType": "register",                                                
  "data": {                                                             
    "ep": "epn1",                                            
    "lt": 6400,                                                
    "sms": "sms_no_example",                                                 
    "lwm2m": "1.2",          
    "objectList": ["1/0", "3/0", "19/0"]                                       
  }                                                                     
} 
```

### 发布订阅授权

网关中无独立的主题授权管理，他们都集中于在 AuthZ 中。参考：[授权](https://www.emqx.io/docs/zh/v5.0/security/authz/authz.html#授权数据源) 

> 注：使用 PUB/SUB 模型转换 的网关无需对其设置的主题配置权限，因为这类客户端的主题规则是强制性的。

### 钩子支持性

EMQX 依赖钩子实现各种功能的扩展，例如上下线消息、规则引擎的触发。因此，网关必须将关键性的事件发布到钩子上，以获取与 EMQX 其他功能的兼容。

在 v4.x，每种钩子的支持并没有规范，v5.0 中我们对其进行了总结，以下为必须支持的钩子：

| **钩子名称**         | **说明**                         |
| :------------------- | :------------------------------- |
| **Client.\***        |                                  |
| client.connected     | 通知连接已建立事件               |
| client.disconnected  | 通知连接已断开事件               |
| client.authenticate  | 实现客户端接入认证               |
| client.authorize     | 实现 PUB/SUB 权限检查            |
| **Session.\***       |                                  |
| session.created      | 通知会话已创建                   |
| session.subscribed   | 通知订阅关系已创建               |
| session.unsubscribed | 通知订阅关系已取消               |
| session.resumed      | 通知会话已重新启用               |
| session.discarded    | 通知会话已被关闭（被丢弃）       |
| session.takeovered   | 通知会话已被关闭（被接管）       |
| session.terminated   | 通知会话已被关闭（被终止）       |
| **Messages.\***      |                                  |
| message.publish      | 处理即将发布到 Broker 的上行消息 |
| message.delivered    | 处理将要投递到 Socket 的下行消息 |
| message.acked        | 通知已收到消息的确认报文         |
| message.dropped      | 出现消息丢弃时触发               |

例如：

- LwM2M 网关支持了 `client.connected` 钩子，因此规则引擎可以通过 `$event/client_connected` 拿到每个 LwM2M 设备的上线事件。
- LwM2M 网关支持了 `client.authenticate` 钩子，因此 ExHook 可以通过挂载该钩子处理 LwM2M 的客户端的认证。

### 自定义认证

网关与 [MQTT 客户端](https://www.emqx.com/zh/mqtt-client-sdk)一样，也基于认证链分发认证请求，直到链上的某个认证器、插件或 ExHook 返回允许/拒绝：

![EMQX 5.0 认证链](https://assets.emqx.com/images/b06388ae87ca80d9639896c5bc99cb4d.png)

<center>5.0 认证链</center>


因此，同样可以通过**自定义认证插件或使用 ExHook** 来扩展对认证的支持。每个认证器的语义可简写为：

```
fun authenticate(ClientInfo, LastAuthResult)  // 入参为：客户端信息、和上次认证器的执行结果
    -> {stop, NewAuthResult}                  // 返回情况1：终止链执行，并返回新的认证结果
     | ignore                                 // 返回情况2：忽略，并继续执行链上的下一个认证器
```

> 注：所有协议都会将认证请求发布到该认证链上，所以需要通过 protocol 、listener_id 等字段区分客户端是来自于哪类网关和监听器

## 用户层接口

网关框架为所有的网关提供了统一的用户层接口，例如，可以使用网关的 HTTP API 达到：

- 对某网关的启用、停止和配置更新等
- 启用、关闭、更新某网关的认证器等
- 添加、删除、更新某网关的监听器等
- 查询、踢出某网关的客户端，或为某客户端添加、取消订阅等

![EMQX 5.0 网关 HTTP API 接口示例](https://assets.emqx.com/images/5b274912d4e1d6c3feb5d21f0663398a.png)

<center>EMQX 5.0 网关 HTTP API 接口示例</center>

本文中仅提供一些简单示例，详情可参考官网文档： [网关配置](https://www.emqx.io/docs/zh/v5.0/admin/cfg.html#gateway)、[网关 HTTP API ](https://www.emqx.io/docs/zh/v5.0/admin/api.html#/gateway) 

例1，通过配置文件启用一个 STOMP 网关：

```
gateway.stomp {

  mountpoint = "stomp/"

  listeners.tcp.default {
    bind = 61613
    acceptors = 16
    max_connections = 1024000
    max_conn_rate = 1000
  }
}
```

例2，通过 HTTP API 启用一个 MQTT-SN 网关：

```
curl -X 'POST' 'http://127.0.0.1:18083/api/v5/gateway' \
  -u admin:public \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "mqttsn",
  "enable": true,
  "gateway_id": 1,
  "mountpoint": "mqttsn/",
  "listeners": [
    {
      "type": "udp",
      "bind": "1884",
      "name": "default",
      "max_conn_rate": 1000,
      "max_connections": 1024000
    }
  ]
}'
```



## 未来展望

网关框架的全新升级为用户使用 EMQX 5.0 进行多协议设备接入带来了诸多便利，未来我们还将在以下方面持续优化这一功能：

- 监控信息支持输出到 Prometheus 和 StatsD，以增加可观测性。
- 各个协议实现的标准化测试。
- 完善个性化管理接口、客户端信息。例如针对 LwM2M 设备的资源模型进行操作。
- LwM2M 等 UDP 类型的协议接入，需要支持 NAT 网络下的会话识别。一旦设备休眠后，由于 NAT 转换会导致 LwM2M 的设备唤醒后，到服务端的地址和端口发生了变化，因此应该设计某类机制来识别这种变化。
- 为 ExProto 实现更轻量的设计，以降低 gRPC 的使用难度，提高运行效率。

## 结语

通过全新网关框架实现多种协议的接入和统一管理，进一步提升了 EMQX 的易用性。结合强大的数据集成、安全可靠的认证授权，以及亿级的水平扩展能力等诸多优势功能特性，各行业的物联网用户可以在多种业务场景中使用 EMQX 实现物联网实时数据的高效连接、移动与处理。



<section class="promotion">
    <div>
        现在试用 EMQX 5.0
    </div>
    <a href="https://www.emqx.com/zh/try?product=broker" class="button is-gradient px-5">立即下载 →</a>
</section>
