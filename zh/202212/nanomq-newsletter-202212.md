12 月，NanoMQ 继续保持稳步更新，最新的 0.15 版本将于一月初发布。这一版本增加了配置热更新功能和 Reload 命令；MQTT over QUIC 桥接再次得到升级，增加了拥塞控制和 QoS 消息优先传输；另外也为上一个版本新增的 HOCON 配置文件做了多项安全性和功能修复，并为硬实时翼辉（SylixOS）操作系统推出了能够兼容运行的版本。


## 配置热更新

如果要在 NanoMQ 服务运行过程中修改运行参数而不影响已经连接的客户端，就需要使用热更新功能。由于 NanoMQ 为纯 C 语言开发，无内置运行时，所以热更新功能仅支持配置文件中部分标注为「Hot updatable」的字段，目的在于提供用户一种可以实时调整 Broker 服务运行参数的方法。以 HOCON 格式配置文件为例，可支持热更新的参数如下：

```
mqtt.session {
    # # Property_size
    # # The max size for a MQTT user property
    # # MQTT 5.0 消息中最大可携带的用户属性长度
    # # Hot updatable
    # # Value: 1-infinity
    property_size = 32
    
    # # The max packet size of NanoMQ (Kbytes)
    # # Defines the max size of a packet that NanoMQ could accept
    # # 最大可接收的MQTT报文长度，单位为字节
    # # Hot updatable
    # # Value: 1 Byte-260 Mb
    max_packet_size = 1024
    
    # # The default max packet size of each client (Kbytes)
    # # Defines the default max size limit of sending packet to each client
    # # Will be overwrite if client set its own max size limit
    # # 最大允许向客户端转发的MQTT报文长度，单位为字节
    # # Hot updatable
    # # Value: 1 Byte-260 Mb
    client_max_packet_size = 1024
    
    # # msq_len
    # # The queue length in-flight window
    # # This is essential for performance and memory consumption
    # # NanoMQ内置的缓冲飞行队列长度，影响内存消耗和消费能力不足时消息是否丢失。
    # # Hot updatable
    # # Value: 1-infinity
    msq_len = 2048
    
    # # qos_duration (s)
    # # The nano qos duration which also controls timer interval of each pipe
    # # 全局定时器颗粒度，单位为秒
    # # Hot updatable
    # # Value: 1-infinity
    qos_duration = 10s
    
    # # anonymous
    # # allow anonymous login
    # # 是否允许匿名登录
    # # Hot updatable
    # # Value: true | false
    allow_anonymous = true
}
```

### HTTP 热更新

同时 NanoMQ 也支持使用 HTTP API 请求和命令行两种方式进行热更新，使用 HTTP 接口 + Basic 认证方式示例如下：

```
（此功能需要http server支持; 设置 http_server.enable=true）
$ curl --location --request POST 'http://localhost:8081/api/v4/reload' \
--header 'Authorization: Basic YWRtaW46cHVibGlj' \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "data": {
                "property_size": 32,
                "max_packet_size": 1024,
                "client_max_packet_size": 1024,
                "msq_len": 4096,
                "qos_duration": 20,
                "keepalive_backoff": 1250,
                "allow_anonymous": true
        }
    }
}'

{
    "code": 0
}
```

修改完成后，可以使用查询基本配置的接口来验证是否修改成功。

```
```shell
$ curl --location --request GET 'http://127.0.0.1:8081/api/v4/configuration/basic' \
--header 'Authorization: Basic YWRtaW46cHVibGlj'
```

### Reload 命令

也可以直接使用命令行工具来重载选定的配置文件，需要启动的时候开启 enable_ipc_internal=true，然后修改原配置文件或新的配置文件中支持热更新的参数，最后执行指令：

```
# 若修改的是原文件，可不带配置文件路径
$ nanomq reload 
# 若使用新的配置文件，需要带上配置文件路径
$ nanomq reload --conf /tmp/nanomq2.conf
```


## MQTT over QUIC 桥接再升级

QUIC 桥接功能一经推出得到了热烈反响，许多用户都在各种复杂的弱网环境下尝试使用了该功能来完成数据到云端的上传同步。根据从各位用户和各种测试场景收集的数据，本次 NanoMQ 版本发布着重优化升级了 MQTT over QUIC 桥接功能在弱网环境下的表现，增加了拥塞控制算法的支持，并为 QoS 消息设置了更高的优先传输级别。

### 拥塞控制算法支持

每当网络环境突然变差，而消息上传的速率却并没有降低，上行数据通道就会发生拥塞。这时候如果还想保持连接，并且最大限度有效利用剩余的带宽，就需要拥塞控制算法出场了。拥塞控制是 TCP/QUIC 协议的一个基础部分，多年来经过一个个版本的迭代（如 Tahoe、Reno、Vegas 等），拥塞控制算法得到了持续的提升。本文不对算法做详细介绍，简而言之通过实时侦测和改变发送滑动窗口的大小来完成慢启动、拥塞避免、快速重传和快速恢复等功能，NanoMQ 的 QUIC 桥接功能依赖于 MsQUIC，目前支持的有比较流行的两种拥塞控制算法：CUBIC 和 BBR。一般使用中建议开启 BBR。开启方式很简单，只需在配置文件中打开即可：

```
bridges.mqtt {
	nodes = [
		{
			name = emqx
			enable = false
			connector {
                  ......
			}
			......
			## 此处设置 cubic/bbr 字符串来选择拥塞控制算法即可
			congestion_control = cubic
			subscription = [
				{
					topic = "cmd/topic1"
					qos = 1
				},
				{
					topic = "cmd/topic2"
					qos = 2
				}
			]
			......
```

### QoS 消息优先级分级

由于 IoT 数据具有强烈的时空伴随特性，我们发现，在遇到网络突然变差时，用户往往希望优先保证一些重要的数据传输不受到影响，但可以接受一些普通的采集数据因为弱网而丢失。同时如果一条数据因为多次重传、拥塞排队或尝试过久而造成极大的消息延时，这样就算最终达到了云端，也会因为延时过大而失去了原有的价值，而只能被云端丢弃。这样既浪费了带宽，还影响了其他更有价值数据的传输。

针对这一情况，NanoMQ 特地在 QUIC 桥接模式上推出了 QoS 消息优先传输的功能，用户发布到桥接通道内的 QoS 1/2 级别的消息会先于 QoS 0 的数据被处理和调度，在传输 QoS 0 的消息时若发现拥塞队列过长，则不会再继续尝试将此消息入队待发送而是直接丢弃。如此最终就可达到让重要数据优先使用有限带宽的效果。

测试场景：

1. 施加 2s 延迟 + 40% 丢包的网络参数
2. 同时往 2 个桥接主题，以同样 50 条消息/s 的速率发送长度为 128 字节的 QoS 0 和 QoS 1 消息，各 2000 条。
3. 在对端 Broker 以非弱网模式接收消息并记录最大延时

测试中 QUIC 连接都未发生重连。

| **桥接传输方式**                   | QoS 0                            | **QoS 1**                        |
| :--------------------------------- | :------------------------------- | :------------------------------- |
| 无划分优先级传输，有丢弃规则       | 收到 933 条，最大延迟约为 8 秒   | 收到 959 条，最大延迟约为 14 秒  |
| 无划分优先级传输，无丢弃规则       | 收到 2000 条，最大延迟约为 14 秒 | 收到 2000 条，最大延迟约为 23 秒 |
| QoS 1/2 优先，有丢弃，开启拥塞控制 | 收到 562 条，最大延迟为 2.5 秒   | 收到 2000 条，最大延迟为 2.8 秒  |

可以发现，在使用优先级传输模式并开启用拥塞控制时，能保证 QoS 1 的消息得到优先传输。

为了适配更多的使用场景，我们为这三种模式都预留了配置选项。


## 其他优化

### 完善修复 HOCON 配置文件支持，并提高安全性

NanoMQ 0.14 版本引入 HOCON 配置文件后，继续对背后使用的纯 C 语言开发的 HOCON 解析器进行完善和提高安全性工作，通过模糊测试和使用 AFL 工具测试发现并修复了许多问题。欢迎用户试用这一小巧精简的 HOCON 解析库。

### 新增操作系统兼容支持

NanoMQ 自诞生之初就具备极强的可移植性和兼容性，现在兼容的操作系统列表上又新增了一个成员：翼辉（SylixOS）操作系统。

[SylixOS](https://www.acoinfo.com/product/108/?category=42&subCategory=262&curCategory=108) 是一个嵌入式实时操作系统，支持 SMP 多核实时调度，可运行于多种 CPU 架构目标平台。具有卓越实时性和可靠性，提供丰富的功能，可为不同行业的嵌入式设备提供理想的软件开发平台。NanoMQ 响应基础软件国产化浪潮，也正式适配了其 2.1.6 版本。

针对 [SylixOS 嵌入式系统](https://www.acoinfo.com/product/108/?category=42&subCategory=262&curCategory=108)，我们为 NanoMQ 和 NanoSDK 都移植了专用的版本，并且对基础的 MQTT Broker 功能都进行了完整测试，若您对在 SylixOS 上使用 NanoMQ 有兴趣，欢迎与我们联系。


## 问题修复

1. 修复了 HOCON 格式配置文件中配置规则引起不生效的问题。
2. 修复了若干使用 Reload 命令重载异常配置文件会导致服务中止的问题。
3. 修复了使用 MQTT over QUIC 桥接时，在大量数据传输时网络突然断开可能造成的数据竞争问题。


## 即将到来

在接下来的两个月，NanoMQ 项目会继续提高 MQTT over QUIC 桥接的体验，通过引入 Multi-Stream 模式来实现各个主题数据的隔离调度。还会为 NanoMQ 加入 DDS 协议的转换网关，以支持用户将 DDS 的数据通过 NanoMQ 来完成跨域传输并通过 MQTT 和云端互通。



<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
