NanoMQ 是面向边缘计算的 MQTT 消息引擎+多协议消息总线。支持 MQTT 协议和 ZeroMQ 和 Nanomsg 等不同边缘常用总线协议，集成 broker 和 brokerless 消息模式，方便打造物联网边缘计算应用。

社区站地址：[https://nanomq.io/zh](https://nanomq.io/zh)

GitHub 仓库：[https://github.com/emqx/nanomq](https://github.com/emqx/nanomq)

NanoMQ 项目一直保持着每月一个小版本+一个重要新功能的稳步迭代速度，v0.8.0 已于五月底正式发布（下载地址：[https://github.com/emqx/nanomq/releases/tag/0.8.0](https://github.com/emqx/nanomq/releases/tag/0.8.0)）。此次我们为大家带来了 2 个重要的功能更新：Event WebHook 以及可以与第三方 HTTP API 集成的连接认证接口。同时还新增了查看主题树结构的 HTTP API，各项性能优化和缺陷修复也在持续更新中。

## 高效易用的边缘 WebHook 系统

WebHook 是 EMQX 深受广大开源用户喜爱的一项功能，NanoMQ 也应社区呼声推出了相同的功能方便用户与第三方边缘计算应用集成。

NanoMQ 的 WebHook 系统与 EMQX 一脉相承，采用相同风格的配置方式。Webhook 的配置文件默认查找的路径为 /etc/nanomq_web_hook.conf，也可以通过命令行指定路径读取配置文件启动。具体配置项可查看 NanoMQ Docs ：[https://nanomq.io/docs/zh/latest/web-hook.html#配置项](https://nanomq.io/docs/zh/latest/web-hook.html#配置项) 。

```
web.hook.enable=true
## 格式示例
web.hook.rule.<Event>.<Number>=<Rule>
```

在设置中启用 WebHook 功能后，可以根据自己的需要配置触发规则，如需要将客户端上下线事件和所有匹配到 ”webhook/msg/#” 通配符主题的消息都转发到对应 HTTP API，则配置方式如下：

### 触发规则配置

在 etc/nanomq_web_hook.conf 可配置触发规则，其配置的格式如下：

```
## 示例
web.hook.enable=true
web.hook.url=http://127.0.0.1:8888
web.hook.headers.content-type=application/json
web.hook.body.encoding_of_payload_field=plain
web.hook.pool_size=32
web.hook.rule.client.connack.1={"action": "on_client_connack"}
web.hook.rule.client.disconnected.1={"action": "on_client_disconnected"}
web.hook.rule.message.publish.1={"action": "on_message_publish", "topic": "webhook/msg/#"}
```

如此设置就能让 NanoMQ 自动捕获并吐出客户端上下线和消息发布的数据到对应的 HTTP API 了。目前 HTTP 请求的数据格式示例如下：

```
## HTTP json格式示例
Connack（客户端连接成功事件）:
{
  "proto_ver": 4,
  "keepalive": 60,
  "conn_ack": "success",
  "username": "undefined",
  "clientid": "nanomq-6ecb0b61",
  "action": "client_connack"
}

Publish（消息发布）:
{
  "ts": 1650609267000,
  "topic": "webhook/msg/123",
  "retain": false,
  "qos": 0,
  "action": "message_publish",
  "from_username": "undefined",
  "from_client_id": "nanomq-6ecb0b61",
  "payload": "hello"
}

Disconnect（客户端连接断开事件）:
{
  "reason": "normal",
  "username": "undefined",
  "clientid": "nanomq-6ecb0b61",
  "action": "client_disconnected"
}
```

目前 NanoMQ 的 WebHook 系统支持以下事件：

| 名称                | 说明                | 执行时机                     |
| ------------------- | ------------------- | ---------------------------- |
| client.connack      | MQTT 客户端连接成功 | 服务端准备下发连接应答报文时 |
| client.disconnected | MQTT 客户端连接断开 | 客户端连接层在准备关闭时     |
| message.publish     | MQTT 消息发布       | 服务端在发布（路由）消息前   |

如需要更多的消息事件请在 NanoMQ 项目的 [Github 页面](https://github.com/emqx/nanomq)提交功能申请 Issue，我们会第一时间安排增加。

需要强调的是，NanoMQ 的 WebHook 功能是全异步操作，所有的匹配到的事件消息都会通过高效的内部 IPC 通道进入独立的专有线程进行处理，与 Broker 功能隔离，不会阻塞原有服务器里正常的消息流转，非常高效可靠。

![NanoMQ WebHook](https://assets.emqx.com/images/2b94a37e4267d9b924a1c28cdba2c159.png)


关于 WebHook 具体的配置信息和方式，以及如何调优请期待之后的 NanoMQ 系列教程文章。

## HTTP 连接认证 API

HTTP 连接认证是另一个常用到的集成功能，能够方便地与第三方认证服务器集成完成客户端的连接请求验证。另一个常用开源项目 Mosquitto 的同类型插件已经废弃不再维护，NanoMQ 的此项功能则填补了这一空白，而且也保持了和 EMQX 相同的功能和配置风格，方便用户上手。

### 认证规则配置

Authentication HTTP API 接口的配置文件读取方式与 NanoMQ 的其他配置文件相同。内部包含的配置项有：

```
## 是否开启HTTP Auth 插件
## Value: true | false
auth.http.enable = true

## Auth请求的目标HTTP URL
auth.http.auth_req.url = http://127.0.0.1:80/mqtt/auth

## HTTP Auth Request 请求方式
## Value: post | get
auth.http.auth_req.method = post

## HTTP Request Headers for Auth Request
auth.http.auth_req.headers.content_type = application/x-www-form-urlencoded

## Parameters used to construct the request body or query string parameters
auth.http.auth_req.params = clientid=%c,username=%u,password=%P
```

配置完成后，NanoMQ 就会根据配置设置的请求格式将客户端 Connect 包的信息请求对应的 HTTP URL。并根据返回码判断是否允许客户端连接成功（Code 200 表示成功）。更详细的配置方式请参阅官网配置文档[https://nanomq.io/docs/en/latest/config-description/v014.html#parameter-description](https://nanomq.io/docs/en/latest/config-description/v014.html#parameter-description)。

## 其他功能优化及 Bug 修复

此外，NanoMQ 0.8.0 还有如下更新和优化：

1. 更正客户端上下线时间消息中的时间戳 timestamp 字段为 UNIX 标准时间戳，之前为启动计时器。
2. 修改了 NanoMQ 命令行工具的使用方式，去除了默认必须使用 “start/stop” 的限制。
3. 增加 ZeroMQ 代理消息网关的文档。
4. 修复了桥接连接被远端频繁关闭时导致的锁竞争问题。
5. 修复了客户端大量发布消息导致积压时，Sub 客户端突然端口导致的数据竞争问题。
6. 不再默认对遗愿消息内容进行 UTF-8 检查，只当客户端要求是才进行。
7. 修复了一个使用 Retain As Published 消息时若消息属性为空会导致崩溃的故障。

## 即将到来

NanoMQ 将于下个月正式发布规则引擎，以及纳入新的数据库作为边缘数据全量持久化选项。目前此功能处于 Demo 阶段，在最新的主分支已可以使用。用户可以自行编译安装使用，欢迎尝鲜：[https://github.com/emqx/nanomq/](https://github.com/emqx/nanomq/) 。

NanoSDK 将于下个月发布 MQTT over QUIC 的 RC 版本，这是业界首个基于 C 语言的完整支持 MQTT 3.1.1 和 QUIC 功能的 MQTT SDK，敬请期待。


<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
