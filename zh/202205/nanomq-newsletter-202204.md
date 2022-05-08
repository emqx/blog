>NanoMQ 是面向边缘计算的 MQTT 消息引擎+多协议消息总线。支持 MQTT 协议和 ZeroMQ 和 Nanomsg 等不同边缘常用总线协议，集成 broker 和 brokerless 消息模式，方便打造一站式边缘数据总线应用。
>
>社区站地址：[https://nanomq.io/zh](https://nanomq.io/zh) 
>
>GitHub 仓库：[https://github.com/emqx/nanomq](https://github.com/emqx/nanomq) 
>


NanoMQ v0.7.0 和 NanoSDK v0.4.0 于本月底正式发布（下载地址： [https://github.com/emqx/nanomq/releases/tag/0.7.0](https://github.com/emqx/nanomq/releases/tag/0.7.0) ），带来了 2 个重要的功能更新：SQLite 本地数据持久化和 nanomsg/ZeroMQ 消息桥接。同时，我们继续完善了 MQTT 5.0 的各项功能支持。

## 数据持久化+断网续传：SQLite3

**SQLite** 是遵守 [ACID](https://zh.wikipedia.org/wiki/ACID) 的关系数据库管理系统，实现了自给自足的、无服务器的、零配置的、事务性的 SQL 数据库引擎。其以库的方式提供，方便被集成在各式各样的服务中，一直以来深受广大用户喜爱。

NanoMQ v0.7.0 新增了 SQLite3 作为本地 MQTT 服务和内置桥接功能断网续传的可选项，将其作为会话保存和 QoS 消息缓存的数据库。若 MQTT 客户端连接时使用会话保存，并且订阅或发布了 QoS 1/2 的消息时，Broker 会自动将数据缓存在 SQLite 本地数据库中，并在触发定时器时重新进行发布尝试。

NanoSDK v0.4.0 也同步增加了这一功能。对于端侧设备来说，弱网环境下数据上传失败是经常发生的情况。而且由于各类网关或端侧设备的电源情况复杂，经常因为断电重启或环境和看门狗等原因进行软复位或者硬复位，这会导致内存中的数据丢失。而使用 NanoSDK + SQLite 的方式，SDK 会自动将飞行窗口里未上传成功的 QoS 消息和未收到 Broker 确认的 QoS 消息缓存在本地磁盘里，并自动重连 Broker，在连接重新建立时触发断网续传。

目前 SQLite 功能默认为关闭，需要用户在编译安装时设置编译选项打开：

```
cmake -G Ninja -DNNG_ENABLE_SQLITE=ON ..
```

这是为了限制 NanoMQ 默认安装包的大小，下一版本将会单独发布支持使用配置打开 SQLite 功能的安装包。

## 支持 MQTT 5.0 订阅标识符和订阅选项

订阅标识符是 MQTT 5.0 带来的一个重要特性，客户端可以在订阅时指定一个订阅标识数字，服务端将在订阅成功创建或修改时，建立和更新该客户端会话所订阅的主题与订阅标识符的映射关系。当有匹配该订阅的 PUBLISH 报文要转发给此客户端时，服务端会将与该订阅关联的订阅标识符随 PUBLISH 报文一并返回给客户端。这一功能在客户端想要知道因为订阅了哪一个主题而收到了消息时非常有用，有助于将消息处理程序和所订阅的主题进行映射。

![MQTT 5.0 订阅标识符和订阅选项](https://static.emqx.net/images/e9944e6ff0d9534a4fdebd7dc871a985.png)

关于订阅标识符的详细内容可以参阅 [订阅标识符与订阅选项 - MQTT 5.0 新特性](https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options) 。NanoMQ 不会因为 PUBLISH 报文携带多个订阅标识符而触发多次消息处理而带来性能损耗。这是因为NanoMQ所有的消息发布操作都是在传输层并行处理，对不同客户端同时进行发布消息时为异步，针对单个客户端是串行发布保证顺序。当有一个客户端因命中多个订阅标识符而需发布多条消息时，这些操作会在同一个线程中完成。

而且NanoMQ 内部对于消息进行了 Zero-Copy 处理， 也不会因为要修改消息内部的订阅标识符而复制该条 PUBLISH 消息，一条 PUBLISH 报文无论命中多少个主题和多少个客户端，该条消息都不会被复制。这在保证多核并行性能和低延时的同时也减少了内存消耗。

此外，NanoMQ v0.7.0 还支持了 MQTT 5.0 的其他订阅选项功能：

No Local 用于避免让服务端向客户端转发它自己发布的消息。

Retain As Publish 用来指定服务端向客户端转发消息时是否要保留其中的 RETAIN 标识，但这一选项不会影响[保留消息](https://www.emqx.com/zh/blog/message-retention-and-message-expiration-interval-of-emqx-mqtt5-broker)中的 RETAIN 标识。

Retain Handling 用来指定订阅建立时服务端是否向客户端发送保留消息：

- **Retain Handling 等于 0**，只要客户端订阅成功，服务端就发送保留消息。
- **Retain Handling 等于 1**，按照原消息格式的 retain 状态发布消息。
- **Retain Handling 等于 2**，即便客户订阅成功，服务端也不会发送保留消息。

## 其他优化

此外，NanoMQ v0.7.0 还有如下更新和优化：

- 修复了 TLS/SSL 和 WebSocket 服务的 MQTT 5.0 支持和兼容
- 为 HTTP REST API 增加 JWT 加密验证方式
- 优化了传输层的 Zero-Copy 特性，不再对主题内容进行复制，减少了内存消耗。
- 修复了 Windows 平台编译安装的兼容性问题。
- 修复了一个命令行工具 Pub 消息时偶发的崩溃问题。

## nanomsg/ZeroMQ 消息桥接网关

在边缘计算领域，特别是使用无线传感网络的场景里，大部分是使用 brokerless 的消息模式。而 nanomsg/nng 和 ZeroMQ 是最常用的两个 brokerless 网络消息库。NanoMQ 作为边缘消息总线，支持在节点部署消息桥接网关将 brokerless 消息转换成 MQTT 消息发送给云上或本地的中心 MQTT 服务端，为用户提供了一种将 broker 和 brokerless 两种网络模式合并的方法。

## 即将到来

应社区要求，NanoMQ 将于下个月正式发布 WebHook 拓展支持。目前此功能处于 Demo 阶段，在最新的主分支已可以使用。用户可以自行编译安装使用，欢迎尝鲜：[https://github.com/emqx/nanomq/](https://github.com/emqx/nanomq/) 。



<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a >
</section>
