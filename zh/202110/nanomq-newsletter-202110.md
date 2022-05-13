自 [NanoMQ](https://www.emqx.com/zh/products/nanomq) 首个版本发布已有近一年时间，这个十月，我们正式发布了项目首个稳定版本 v0.5.0。从该版本开始，NanoMQ 除了完整支持 [MQTT](https://www.emqx.com/zh/mqtt) 3.1.1 协议外，还将支持 [MQTT Over WebSocket](https://www.emqx.com/zh/blog/connect-to-mqtt-broker-with-websocket)。用户也可以通过配置文件或命令行参数修改 NanoMQ 的启动调优选项。此外还增加了内置的 HTTP 服务器，未来将提供更丰富的 HTTP APIs。

接下来我们主要致力于 NanoMQ/NNG 的 [MQTT SDK](https://www.emqx.com/zh/mqtt-client-sdk) 支持和桥接功能开发，此功能预计在 0.6.0 版本中提供。敬请期待。


## 启动调优选项修改

NanoMQ 自发布之始就具有高兼容性和易移植性等特点，但在 0.4.0 版本之前需要用户根据自有平台的硬件配置在编译阶段选择优化参数进行调优。0.5.0 版本进一步优化了两种配置方式的使用体验。调优指南和主要支持的配置参数如下（以配置文件为例）：

```
num_taskq_thread=4
max_taskq_thread=4 
```

据系统的 CPU 线程数来确定初始/最大 taskq 线程数量，默认为 4。此配置决定了 NanoMQ 的性能和 CPU 利用率，建议和 CPU 最大线程数保持一致。

```
parallel=32
```

为系统最大并行的逻辑线程数，根据系统实际压力设置为宜，影响消息时延和内存使用。建议为 CPU 线程数 2 倍。

```
msq_len=64
```

为内置每个客户端的消息队列缓存的初始长度，NanoMQ 支持消息队列自动伸缩，建议根据系统内存大小设置为 2 的幂数，低于 128Mb 内存的设备建议固定为 1024。

```
qos_duration=60
```

为 NanoMQ 服务内置全局定时器的颗粒度，这一选项影响对于连接健康度检测的最小时间差。如果有大量客户端并发的情况，会些许消耗 CPU，建议设置为 MQTT 连接的 keepalive 时间一致。

```
allow_anonymous=yes    是否允许匿名登录
daemon=no              是否以守护进程启动 
```

## Websocket 服务

MQTT Over Websocket 一直是 MQTT 的一个主要使用领域，特别在前端和小程序开发有广泛应用。现在 NanoMQ 可以通过以下配置选项：

```
websocket.enable=yes
websocket.url=ws://0.0.0.0:8083/mqtt 
```

来开启 Websokcet 端口。目前 Websocket 端口支持完整 MQTT 3.1.1协议。


## HTTP 服务

作为一款 [边缘端 MQTT 消息服务器](https://nanomq.io/zh)，NanoMQ 也致力于提供易用的 HTTP APIs 给用户。目前 HTTP 服务还只支持获取所有订阅主题列表一个功能，之后我们会尽快完善相关的统计功能。

```
http_server.enable=yes
http_server.username=admin
http_server.password=public 
```


## 社区 Issue 和 bug 修复

0.5.0 版本还修复了社区提交的几个重要安全相关漏洞。NanoMQ 团队将继续倾听用户的声音，为社区和行业交付稳定、强大和安全的边缘 MQTT 消息服务和消息总线。


<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a >
</section>
