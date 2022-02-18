在阅读该指南之前，假定你已经了解 [MQTT](https://www.emqx.com/zh/mqtt) 与 EMQX [MQTT 服务器](https://www.emqx.com/zh/products/emqx) 的简单知识。

EMQX Broker 从 V3 版本开始支持速率限制功能，包括了对 **PUBLISH 报文接收速率** 与 **TCP 数据包接收速率** 的限制，本文将详细介绍该功能的配置与使用。



## 配置项

#### MQTT PUBLISH 报文接收速率

该配置位于 `emqx.conf`：

`zone.external.publish_limit = 10,1m`

配置格式为：`<Number>,<Duration>`，表示在 `<Duration>` 时间段内，最多允许接收 `<Number>` 数量的 PUBLISH 报文。

#### TCP 数据包接收速率

该配置位于 `emqx.conf`：

`listener.tcp.external.rate_limit = 1024,4096`



配置格式为：`<Rate>,<Burst>`，它表示允许的数据包接收的平均速率为 `<Rate>` 。但它允许的的最大峰值由` <Burst>` 值决定。详细的内容见下节： **速率限制算法令牌桶 — 算法**

#### active_n

该配置位于 `emqx.conf`：

`listener.tcp.external.active_n = 100`

 `active_n` 实际上表示的是：在底层的异步 I/O 中允许读取的数据报条数，每当异步的读操作到达该限制时，便暂时的切换为同步模式。每当切换为同步模式时，则会执行一次速率限制的检查。**因此，该值越大，系统的吞吐性能越好；该值越小，速率检查越精准，流入的流量越平稳，系统的安全性更高。**

## 速率限制算法 - 令牌桶

#### 简介

上述所提到 `publish_limit` 和 `rate_limit` 都使用 **令牌桶算法** 实现，其算法逻辑如下图：

![画板2x.jpg](https://static.emqx.net/images/774c97d301a252790e77e52af992b92a.jpg)

1. 存在一个最多可容纳 `burst` 数量令牌 (Token) 的桶 (Bucket)。
2. 我们将以每秒 N 个的速率向这个桶添加令牌，桶满时则不再向桶添加令牌，这个速率我们记为 `rate`。
3. 每当有请求抵达，则从桶中取出相应数量的令牌。如果桶为空则阻塞，直到足够数量的令牌被放入。

#### 作用

通过 **令牌桶** 算法，我们能够：

- 在长时间运行的情况下，被限制的请求速率的平均值等于令牌添加的速率，即 `rate`。
- 允许一定程度的峰值流量。如果请求速度为 `M`，且大于 `rate`，则令牌减少的速率为 `M - rate`，那么一个满的桶被取完令牌需要的时间为 `burst / (M - rate)`，而在此期间接受的请求数量为 `burst / (M - rate) * M`。

总之，可以简单理解 `rate` 为平均请求速率，`burst`为瞬间最大请求速率。



## EMQX 速率限制实现

基于以上的 *令牌桶* 算法下，EMQX 对速率限制的实现逻辑如下：

![画板1232x.jpg](https://static.emqx.net/images/874ae38a1c06a8919d2109d148adf177.jpg)

其含义为：

1. socket 每接收 n 个 TCP 数据报文，便进行一次速率检查，将收到的 n 个 TCP 数据报文的总长度记为 s。
2. 令牌桶中的剩余令牌数大于等于 s，则更新对应令牌桶的令牌数量，并继续激活 socket 执行 active_n。
3. 令牌桶中的剩余令牌数 r 小于 s，则等待 `(s - r) / rate` 秒再激活 socket。

## 速率限制配置示例

#### 速率限制配置

```properties
listener.tcp.external.active_n = 100
listener.tcp.external.rate_limit = 1024,1024000
```

以上配置表示：

- 每收到 100 个 TCP 报文进行速率检查。
- 平均速率限制为 1024 byte/s。
- 桶大小为 1000 KB，如果这 100 个 TCP 报文的总长度大于 1000KB，那么将会触发速率限制。

因此，用户需要根据实际报文大小来设置 `<Burst>`, EMQX 推荐配置为 `(max_packet_size * active_n) / 2`，以避免频繁发生阻塞。

```properties
listener.tcp.external.active_n = 100
zone.external.publish_limit = 10,1m
```

以上配置表示：

- 每收到 100 个 TCP 报文进行速率检查。
- 1 分钟内仅允许接收 10 个 PUBLISH 报文。

可以将 `<Number>,<Duration>` 转换为 `<Rate>,<Burst>` 的形式，即 `<Number> / <Duration>, <Numebr>`。

#### 其他配置

此外，除了这以上的 *Rate Limit* 限制外，在 `etc/emqx.conf` 配置中，还支持对 TCP、WebSocket 等连接进行以下限制：

`
listener.tcp.external.max_connections = 1024000
`

允许同时存在的最大连接数量，即最大同时在线客户端数量。

`
listener.tcp.external.max_conn_rate = 1000
`

每秒允许的最大并发连接数。
