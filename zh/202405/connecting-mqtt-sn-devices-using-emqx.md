## 前言

MQTT-SN（MQTT for Sensor Networks）是 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)的扩展，专为传感器网络而设计。它解决了资源受限设备的独特需求，使其成为各种物联网应用中的关键角色。

本文将全面解析 MQTT-SN 协议，通过对其架构的深入介绍、其与 MQTT 的对比、实际应用案例以及实施建议，帮助读者详细了解这一协议。

## 了解 MQTT-SN

### MQTT-SN 的优点

- **与 MQTT 协议兼容：** MQTT-SN 通信模型完全与 MQTT 相对应，例如发布、订阅、保留会话、[遗嘱消息](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)等。统一的模型有利于降低端到端的设计复杂度。
- **轻量：** 为了应对 WSN 网络中有限的传输带宽，协议设计非常精简。例如 PUBLISH 消息中的主题名称被一个短的、两字节长的 Topic ID 取代。
- **支持休眠：** MQTT-SN 协议新增了休眠逻辑，来应对低功耗的场景。例如设备进入到休眠后，所有发给它们的消息都会被缓存在服务器，并在唤醒后传递给它们。

### MQTT-SN 与 MQTT 的区别

- 网关发现：MQTT-SN 网关可以定期向网络广播其信息，或由客户端主动搜索网关地址。这一功能常用于局域网内 MQTT-SN 客户端和网关的自动组网。
- 使用 QoS Level-1 发布：该功能适用于只需向已知网关地址发送 PUBLISH 消息的基础客户端实现，无需额外的设置、注册或订阅，非常适合轻量级和简单的终端设备。
- 遗嘱消息更新：MQTT-SN 允许随时更新遗嘱消息的主题和内容，而 MQTT 协议中，遗嘱消息只能在初次连接建立时设置。
- 安全挑战：MQTT-SN 缺乏基于用户名/密码的身份验证连接。在连接到 MQTT-SN 网关时，只提供客户端ID，不支持用户名和密码。这在公共网络部署 MQTT-SN 服务时可能带来安全风险。有人通过使用双向 DTLS 解决这个问题，但这往往增加了设计和操作的复杂性。

## MQTT-SN 常见的部署结构

![MQTT-SN Architecture](https://assets.emqx.com/images/d9615f76aa0d90157285634651fc0914.png)

1. Client 和 Gateway 部署在同一个局域网中（例如 Zigbee）通过 MQTT-SN 协议进行通信，并且 Gateway 通过以太网和 MQTT 协议将数据上报到云端的 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)。
2. MQTT Broker 与 MQTT-SN Gateway 集成在一起，都部署在云端。Client 通过 UDP 和 MQTT-SN 直接与云端的 MQTT-SN 网关进行通信。
3. 第三种部署方式与第一种类似，不同的是使用 MQTT-SN 协议与云端的 MQTT-SN 网关进行交互。

相对比而言：

- 第一种方案是最为典型的 MQTT-SN 部署方案，该方案非常适用于终端无公网通信需求且需要部署网关来统一管理的场景，例如典型的智能家居场景。
- 第二种方案常见于终端设备都部署在室外，它们通过移动网络例如（NB-IoT) 直接与云端直连，中间无法部署网关来处理设备请求。
- 第三种部署比较少见，它仅是方案 1、2 的一种折中。仅在服务端仅能提供 MQTT-SN 接入服务时会用到。

## MQTT-SN 的应用场景

MQTT-SN 专为连接网络资源有限的传感器和嵌入式设备而设计，以满足物联网对低功耗、低带宽和低成本的要求。其主要应用场景有：

- 农业：监测土壤湿度、温度和光照数据，实现精确灌溉和作物管理。
- 工业监控：实时监控和控制生产线设备状态，以优化生产效率和资源利用。
- 智能电表：用于能源监测系统，实时监测电表、水表、煤气表等的能源消耗，帮助用户管理和节约能源。

## 使用 EMQX 接入 MQTT-SN 协议

EMQX 企业级 MQTT 物联网接入平台全面支持 MQTT 协议。此外，它还提供多协议网关，处理所有非 MQTT 协议的连接、认证和消息收发，并通过统一的用户界面提供便捷体验。

<section class="promotion">
    <div>
        免费试用 EMQX Enterprise
            <div>无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient">开始试用 →</a>
</section>

EMQX 的 MQTT-SN 网关基于 [MQTT-SN 1.2](https://www.oasis-open.org/committees/download.php/66091/MQTT-SN_spec_v1.2.pdf) 版本实现。MQTT-SN 网关作为一个组件集成在 EMQX，可以允许将其部署在边缘或云端来实现上文提到的第一和第二种部署结构。

### 启用 MQTT-SN 网关

在 EMQX 5.0 中，可以通过 Dashboard、HTTP-API 或配置文件来启用 MQTT-SN 网关。

例如，开启并配置监听 UDP 1884 端口的 MQTT-SN 网关：

```
gateway.mqttsn {
  mountpoint = "mqttsn/"
  listeners.udp.default {
    bind = 1884
    max_connections = 10240000
    max_conn_rate = 1000
  }
}
```

### 客户端测试

使用 C 语言编写的 [MQTT-SN 客户端](https://github.com/njh/mqtt-sn-tools)，来测试发布订阅，例如：

Client ID `mqttsn1` 连接并订阅主题 `t/a`，

```shell
$ ./mqtt-sn-sub -i mqttsn1 -t t/a -p 1884 -d 
```

使用 Client ID 为 `mqttsn2` 登录到 MQTT-SN 网关，并对 `t/a` 主题发布消息 `Hi, This is mqttsn2` ：

```
$ ./mqtt-sn-pub -i mqttsn2 -p 1884 -t t/a -m 'Hi, This is mqttsn2' -d 
```

最终，能在 `mqtt-sn-sub` 端接收到该消息：

![mqtt-sn sub](https://assets.emqx.com/images/572f95ddaba4e4bef12850c51e8a001d.png)

## 更多高级功能配置

### 配置客户端接入认证

由于 MQTT-SN v1.2 协议的连接报文只定义了 Client ID，没有 Username 和 Password 。所以 MQTT-SN 网关目前仅支持 HTTP Server 认证

例如，通过配置文件，为 MQTT-SN 网关添加一个 HTTP 认证：

```
gateway.mqttsn {
  authentication {
    enable = true
    backend = "http"
    mechanism = "password_based"
    method = "post"
    connect_timeout = "5s"
    enable_pipelining = 100
    url = "<http://127.0.0.1:8080">
    headers {
      "content-type" = "application/json"
    }
    body {
      clientid = "${clientid}"
    }
    pool_size = 8
    request_timeout = "5s"
    ssl.enable = false
  }
}
```

在该认证方式中，将 Client ID 传递给 HTTP 服务，由 HTTP 服务来决定该客户端是否有接入系统的权限。

### 配置发布订阅权限

在 EMQX 5.0 中，所有主题的发布订阅权限都在**授权（Authorization）**中统一配置。例如，允许所有人发布订阅 `mqttsn/` 开头的主题：

![Configure permissions for Publish/Subscribe](https://assets.emqx.com/images/ee63792138471dc8a61b198af9bd9b73.png)

<center>在 Dashboard 中配置主题发布订阅权限</center>

### 获取上下线事件

MQTT-SN 网关会将所有设备的上下线事件发布到两个专用的主题：

- 上线事件主题：`$SYS/brokers/<node>/gateway/mqtt-sn/clients/<clientid>/connected`
- 下线事件主题：`$SYS/brokers/<node>/gateway/mqtt-sn/clients/<clientid>/disconnected`

例如，一条上线事件消息内容为：

```json
{
   "clientid": "abc",
   "username": "undefined",
   "ts": 1660285421750,
   "sockport": 1884,
   "protocol": "mqtt-sn",
   "proto_ver": "1.2",
   "proto_name": "MQTT-SN",
   "keepalive": 10,
   "ipaddress": "127.0.0.1",
   "expiry_interval": 7200000,
   "connected_at": 1660285421750,
   "clean_start": false
}
```

当然，也可以通过规则引擎中的 `$event/client_connected` 和 `$event/client_disconnected` 事件来获取 MQTT-SN 网关的上下线事件，具体可以参考：[Event topic available for FROM clause](https://www.emqx.io/docs/en/v5.0/data-integration/rule-sql-events-and-fields.html#mqtt-events)

## 结语

本文深入介绍了 MQTT-SN 协议及其应用。作为物联网中不可或缺的一环，MQTT-SN 为传感器网络提供了高效、可靠的通信协议。借助 MQTT-SN，我们可以实现对传感器数据的实时监测、远程控制和智能化管理，为各行业带来了极大的便利和效益。结合 EMQX 等领先物联网产品，我们能够进一步优化 MQTT-SN 的使用体验，拓展物联网的应用范围，促进物联网技术的发展和创新。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
