EMQX 开源版 v4.3.14、v4.4.3 与企业版 v4.3.9、v4.4.3 四个维护版本已经发布，修复了已知 BUG 并新增少量功能，支持使用[版本热更新](https://www.emqx.io/docs/zh/v4.4/advanced/relup.html)的方式升级使用。

此次发布中新增的功能包括规则引擎增连接确认、鉴权完成事件以及压缩、解压缩函数，编解码功能支持性能更好的 gRPC 方式，为 ExHook 提供更加灵活的使用方式。

欢迎前往下载使用：[https://www.emqx.com/zh/try?product=enterprise](https://www.emqx.com/zh/try?product=enterprise)

## 规则引擎新功能

### 规则引擎支持重置指定规则的统计指标

包含版本： 开源版 v4.4.3 企业版 v4.4.3

规则的使用统计指标反馈了业务负载情况，用户可以在排除规则故障、升级服务器规格之后希望重新开始统计规则执行数量与执行速度等指标，以便查看调整后的运行效果。

![在 Dashboard 中重置规则统计指标](https://assets.emqx.com/images/b580154abf7a6f889a3761908c3713b4.png)

<center>在 Dashboard 中重置规则统计指标</center>

### 规则引擎新增连接确认和鉴权完成事件

包含版本： 开源版 v4.4.3 企业版 v4.4.3

以往规则引擎只支持客户端连接成功与断开连接事件，本次新增两个事件用于观测客户端连接结果（成功 or 失败，可以在失败时获得失败原因）或和触发 ACL 检查的情况，使用此功能可以支撑安全审计相关的功能。

通过以下 SQL 语句使用此事件：

```
-- 连接确认事件
SELECT * FROM "$events/client_connack"

-- 鉴权完成事件
SELECT * FROM "$events/client_check_acl_complete"
```

### 规则引擎 SQL 支持 zip、gzip 等压缩和解压缩函数

包含版本： 开源版 v4.3.14 开源版 v4.4.3 企业版 v4.3.9 企业版 v4.4.3

在流量成本较高或传输大量可压缩数据的情况下可以对消息进行压缩/解压缩处理，以节省流量开销并获得更快的传输时间，支持 zip、gzip 压缩算法，以下是示例 SQL 语句：

```
SELECT 
  zip(payload) as p,
  unzip(p) as c,
  gzip(payload) as p2,
  gunzip(p2) as c2
FROM "t/#"
```

实际测试中，大量具有重复键值的 JSON 文本可以获得极高的压缩率，对于此类场景，计算能力充足的条件下可以使用压缩算法大大缩短传输时间。

值得一提的是我们注意到一种新的二进制数据格式 CBOR（[RFC 7049](https://datatracker.ietf.org/doc/html/rfc7049)）由于拥有良好压缩性和扩展性强非常适用于物联网传输，有人将其比喻为「二进制版本的 JSON」。我们计划在后续版本的规则引擎中提供此格式的编解码能力，以探索更快、更高效的物联网的数据传输可能性。

### 规则引擎 SQL 新增 mongo_date 函数，支持将时间戳保存为 MongoDB Date 对象

包含版本： e4.3.9 e4.4.3

此前通过规则引擎向 MongoDB 写入数据时，时间类型的数据只能以字符或整型的方式存储，本次更新我们新增 mongo_date 以支持此功能。

### 支持使用 TLS 连接到 Pulsar

包含版本： 企业版 v4.3.9 企业版 v4.4.3

此前的 企业版 v4.3.8 中我们提供了 [Pulsar Proxy](https://pulsar.apache.org/docs/2.11.x/administration-proxy/) 的支持，本次更新我们新增 Pulsar 资源 TLS 连接，为规则引擎数据集成提供更好的安全性。

### 编解码支持 gRPC 通道

包含版本： 企业版 v4.3.9 企业版 v4.4.3

编解码是规则引擎中的 UDF（用户自定义函数）能够扩展规则 SQL 函数，本次更新我们提供了 gRPC 通道，相比 HTTP 能够以更低的开销完成相同的需求，在 16 核 32GB 的服务器上，能够稳定实现 20K/s 的调用处理。

![gRPC 编解码性能测试 CPU 负载情况](https://assets.emqx.com/images/ebf05f5c8619d6e30d1ea5b85e0b7918.png)

<center>gRPC 编解码性能测试 CPU 负载情况</center>

## ExHook 新功能

### 支持为 ExHook 设置执行优先级

包含版本： 开源版 v4.3.14 开源版 v4.4.3 企业版 v4.3.9 企业版 v4.4.3

ExHook 允许用户使用其它编程语言（例如：Python、Java 等）直接向 EMQX 挂载钩子，以接收并处理 EMQX 系统的事件，达到扩展和定制 EMQX 的目的，类似于使用其他编程语言开发 EMQX 的插件。

在实际使用中，根据场景不同一部分用户需要使用 ExHook 接管现有 EMQX 插件，另一部分用户希望将 ExHook 置于插件之后作为插件能力的补充，ExHook 挂载钩子的顺序就成为实现这一目标的关键。尽管可以通过插件的启动顺序（ExHook 本身也是一个插件）设置 ExHook 相对插件的位置，但此操作比较繁琐且 EMQX 重启后会丢失顺序，因此我们迫切需要一个能够固定插件优先级的方式。

本次更新 EMQX 允许指定 ExHook 的优先级，以便更好的与插件和规则引擎配合使用。

- 对于企业版用户，可以在 模块 中使用 Web 界面设置 ExHook 优先级；

  ![使用 Web 界面设置 ExHook 优先级](https://assets.emqx.com/images/fe86ca9b49c4c125c2deb73919b7ec07.png)

- 对于开源版用户，emqx_exhook 插件的优先级配置项如下：

   ```
   ## plugin/emqx_exook.conf
   exhook.hook_priority = 0
   ```

### ExHook 回调接口字段新增集群名称

包含版本： 开源版 v4.3.14 开源版 v4.4.3 开源版 v4.3.9 开源版 v4.4.3

我们在 ExHook 回调接口字段中添加了集群名称，多个 EMQX 集群共用一个 ExHook gRPC 服务时，用户可以根据集群名称将请求路由到不同的业务逻辑。

## 其他新增功能

### 为共享订阅添加 local 策略以提升共享消息调度的效率

包含版本： 开源版 v4.3.14 开源版 v4.4.3 企业版 v4.3.9 企业版 v4.4.3

local 策略允许在集群环境下优先给消息流入的节点上的共享订阅者派发消息，这可能会对负载均衡带来一些影响，但是在某些场景下会提升共享消息调度的效率，尤其是在将 MQTT Bridge 配置为共享订阅时。

此外，EMQX 现在既可以配置全局的共享订阅分发策略，也可以为每个共享订阅组配置独立的分发策略，你可以在 emqx.conf 文件中找到以下配置项：

```
broker.shared_subscription_strategy = random
broker.your_group.shared_subscription_strategy = local
```

## BUG 修复

各版本 BUG 修复详情请查看：

- 开源版 v4.3.14：https://www.emqx.com/zh/changelogs/broker/4.3.14
- 开源版 v4.4.3：https://www.emqx.com/zh/changelogs/broker/4.3.14
- 企业版 v4.3.9：https://www.emqx.com/zh/changelogs/enterprise/4.3.9
- 企业版 v4.4.3：https://www.emqx.com/zh/changelogs/enterprise/4.3.9


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a >
</section>
