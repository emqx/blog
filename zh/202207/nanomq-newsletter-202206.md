NanoMQ 继续保持稳步更新，0.9.0 将于 7 月初正式发布。此版本为大家带来了 2 个重要的功能更新：规则引擎和支持 QUIC 的 NanoSDK。同时还增加了离线数据缓存配置，各项性能优化和缺陷修复也在持续进行中。

## 轻便易用的嵌入式规则引擎

规则引擎是 EMQX 深受广大用户喜爱的一项功能，NanoMQ 也根据用户需求推出了相同的功能，用户现在可以方便地通过编写 SQL 规则对消息进行处理后重新发布或存入数据库进行持久化。

NanoMQ 的规则引擎由统一消息接口和各种不同目标插件组成，不同插件各自享有独立的配置文件。目前只有 SQLite 插件作为数据持久化选项，未来会增加更多的可选插件。

使用规则引擎需要先在全局配置/etc/nanomq_rule.conf 里开启 SQLite 插件功能：

```
## Rule engine option, when persistence with 
## rule engine, this option is must be ON.
## 
## Value: ON | OFF
rule_option=ON

## Rule engine plugins option
## Choose a plugin to enable
## 
## Value: enable/disable
rule_option.sqlite=enable

## Rule engine option database config path
## Rule engine plugin config path, default is exec path.
## 
## Value: File nanomq_rule_sqlite.conf
rule_option.sqlite.conf.path=/etc/nanomq_rule_sqlite.conf
```

然后再对应的插件配置文件 /etc/nanomq_rule_sqlite.conf中配置对应的 SQL 语句和数据库参数：

```
## Rule engine option SQLite3 database path
## Rule engine db path, default is exec path.
## 
## Value: File
rule.sqlite.path=/tmp/sqlite_rule.db

## Rule engine option SQLite3 database table name
## Rule engine db table name.
## 
## Value: String
rule.sqlite.table=broker

## Rule engine option sql
## Rule engine sql clause.
## 
## Value: String
SELECT * FROM "abc" WHERE payload.x.y = 10
```

如此配置，NanoMQ 就会使用配置中的 SQL 处理所有的 Publish 消息后持久化到对应的 SQLite 数据库表中。

例如此时我们发布两条不同的消息到 abc 主题：

```
msg1: "{"x": {"y": 10}, "z": "str1", "a": 1111}
msg2: "{"x": {"y": 11}, "z": "str1", "a": 1111}
```

然后就能在 SQLite 数据库中看到：

```
sqlite> SELECT * FROM Broker;
RowId|Qos|Id|Topic|Clientid|Username|Password|Timestamp|Payload
1|1|1|abc|nanomq-57a0d6ab|abc|(null)|1656066147|{"x": {"y": 10}, "z": "str1", "a": 1111}
2|1|1|abc|nanomq-9c1ca526|abc|(null)|1656066147|{"x": {"y": 10}, "z": "str1", "a": 1111}
3|1|1|abc|nanomq-7ff24b6f|abc|(null)|1656066147|{"x": {"y": 10}, "z": "str1", "a": 1111}
4|1|1|abc|nanomq-83e7ff63|abc|(null)|1656066147|{"x": {"y": 10}, "z": "str1", "a": 1111}
```

可见只有符合规则的消息 msg1 被持久化到了数据库中。规则引擎目前支持标准 JSON 解析和常用的 SQL 语句和符号，具体详情请参阅文档。

目前 NanoMQ 的规则引擎运行顺序是在处理完 MQTT 消息之后串行执行，如果规则耗时过多的话会影响 Broker 本身的性能和消息吞吐。如果有许多数据需要通过规则引擎进行持久化，建议将/etc/nanomq.conf中的 parallel=32 数量提高以增加逻辑线程数以支持更多规则和消息的并行处理。

## 边缘数据缓存配置

边缘服务往往运行在弱网或者恶劣环境中，断网断电的情况时常发生。在之前的版本中，NanoMQ 的桥接功能支持了将未收到确认的 QoS 1/2 消息缓存在本地 SQLite 中并自动重发来避免数据丢失。此次发布的 v0.9.0 增加了对桥接连接断开的处理，并且针对边缘场景增加了许多配置选项，以避免由于缓存的数据过大写满 Flash 或者写入次数过多导致 Flash 寿命耗尽。

/etc/nanomq_bridge.conf的新增配置选项有：

```
## Enable sqlite cache
## Whether to enable sqlite cache
## 是否开启SQLite离线消息缓存功能
## Value: boolean
bridge.sqlite.enable=false

## Max message limitation for caching
## ( 0 means ineffective )
## Value: 1-infinity
## 最大缓存到磁盘/Flash的消息条数限制
bridge.sqlite.disk_cache_size=102400

## Mounted file path
## SQLite数据库文件路径
## Value: path
#bridge.sqlite.mounted_file_path=/tmp/

## The threshold of flushing messages to flash.
## flush msg to disk when reach this number
## Value: 1-infinity
## 数据刷盘的缓存窗口（消息条数），建议根据消息大小设置为 消息条数 * 消息大小 = page size
bridge.sqlite.flush_mem_threshold=100

## Resend interval (ms)
## The interval for resending the messages after failure recovered. (not related to trigger)
## 缓存消息的重发间隔
## Value: 1-infinity
bridge.sqlite.resend_interval=5000
```

同时 0.9.0 版本也不再需要用户自行修改编译参数来启用 SQLite，现在可以通过配置文件控制 Broker 和桥接功能是否启用 SQLite 作为缓存选项。另外我们也对 SQLite 的使用做了优化，开启了 WAL 模式，并采用了全同步方式避免文件系统损坏。而且从这一个版本开始，桥接的离线缓存功能配置选项和 Broker 的 QoS 消息默认缓存分离，建议只需要对云端桥接进行断网数据自动缓存和续传的用户不用开启 /etc/nanomq.conf 的 SQLite 功能。



## NanoSDK： 首个 C 语言的 MQTT over QUIC SDK

6 月 11 日，IETF 正式颁布了 HTTP/3 RFC 技术标准文档，QUIC 正式成为了传输层标准之一。IoT 应用经常会遇到诸如网络漫游、弱网环境频繁重连和网络拥塞等问题，利用 QUIC 的流式多路复用、分路流控、更低的连接建立延迟等特性，这些问题都可以得到显著改善。NanoSDK 0.6.0 基于 MsQuic 项目率先实现了 C 语言的第一个 MQTT over QUIC SDK。建议搭配全球首个支持 MQTT over QUIC 的 Broker——EMQX 5.0 一同使用。

![NanoSDK 与 EMQX 之间通过 QUIC 进行消息收发](https://assets.emqx.com/images/76f7b3b1ee315901bd32acdee9d8fd40.png)

<center>NanoSDK 与 EMQX 之间通过 QUIC 进行消息收发</center>

NanoSDK 通过为 NNG 的传输层增加 QUIC 支持，使 MQTT、nanomsg 等协议能够从 TCP 转为 UDP，从而提供更好的物联网连接体验。其内部将 QUIC Stream 和 MQTT 连接映射绑定，并内置实现了 0RTT 快速握手重连功能。

![QUIC： 0RTT 快速重连](https://assets.emqx.com/images/5bb75bbc17789dee5dc476b3324569c1.png)

<center>QUIC： 0RTT 快速重连</center>

API 方面保持了之前的使用习惯，一行代码即可基于 QUIC 创建 MQTT 客户端：

```
## Create MQTT over Quic client with NanoSDK
nng_mqtt_quic_client_open(&socket, url);
```

消息示例代码请参考：

[https://github.com/nanomq/NanoSDK/tree/main/demo/quic](https://github.com/nanomq/NanoSDK/tree/main/demo/quic) ，编译后可以通过以下命令连接 EMQX 5.0 的 14567 端口进行测试。

```
quic_client sub/pub mqtt-quic://54.75.171.11:14567 topic msg
```

## 其他功能优化及 Bug 修复

此外，NanoMQ 0.9.0 还有如下 bug 修复和更新优化：

1. 增加了最大接收消息长度和最大可转发消息长度的配置选项，方便进行大消息收发。
2. 修复了nanomq broker restart重启命令不生效的情况。
3. 取消了对 C++ compiler 的编译要求。
4. 修复了收到客户端 Disconnect 消息不会清理会话和遗愿消息的问题。
5. 修复了 v0.8.0 中 MQTT over WebSocket 服务无法正常工作的问题。
6. 修复了客户端 unsub 会导致服务停止的问题。
7. 修复了客户端大量发布消息导致积压时，Sub 客户端突然端断开导致的数据竞争问题。

## 即将到来

NanoMQ 将于下个月正式发布 0.10 stable release 版本，并支持 MQTT 多路桥接功能。目前此功能处于 Demo 阶段，在最新的主分支已可以使用。用户可以自行编译安装使用，欢迎尝鲜：[https://github.com/emqx/nanomq/](https://github.com/emqx/nanomq/) 。



<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
