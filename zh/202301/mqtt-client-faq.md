大家好，这是一期社区专题 FAQ。我们整理了近期社区中关注度较高的问题，在这里进行统一汇总解答。

今后本系列内容将不定期推送，敬请关注。

同时，如果大家在使用 EMQX 的过程中遇到问题，欢迎通过以下方式进行解决：

- 查阅 EMQX 产品文档与博客文章：[https://www.emqx.io/docs/zh/v5.0/](https://www.emqx.io/docs/zh/v5.0/)，[https://www.emqx.com/zh/blog/category/emqx](https://www.emqx.com/zh/blog/category/emqx)。
- 如果在现有资料中未能查询到问题的解决办法，可以在问答社区中留言提问，我们会尽快解答您的问题：[https://askemq.com/](https://askemq.com/)  

### Q：向 MQTT Broker 发布多条消息，MQTT Broker 向订阅者转发这些消息的时候能否保证原始顺序？

MQTT Broker 一定会保证来自同一客户端的相同主题的消息按照到达顺序被转发，这与消息的 QoS 等级无关，QoS 等级不会影响转发顺序，不管是消息丢失，还是消息重复，也都不会导致消息失序。

对于不同主题的消息，MQTT Broker 不会提供转发顺序保证，我们可以将他们视为进入了不同的通道，比如主题 A 的消息先于主题 B 的消息到达 MQTT Broker，但最终可能主题 B 的消息会更早下发。

### Q：我的客户端无法连接到 EMQX/订阅失败/发布消息但是对端没有收到任何消息，出现这些情况怎么办？

A：其实 EMQX 的 Debug 日志基本已经记录了所有的行为和现象，通过阅读 Debug 日志我们能够知道客户端何时发起了连接，连接时指定了哪些字段，连接是否通过，被拒绝连接的原因是什么等等。但是由于 Debug 日志记录的信息过多，会带来额外的资源消耗，并且不利于我们针对单个客户端或主题进行分析。

所以 EMQX 提供了[日志追踪](https://www.emqx.io/docs/zh/v5.0/observability/tracer.html)功能，我们可以指定想要追踪的客户端或主题，EMQX 会将所有与该客户端或主题相关的 Debug 日志都输出到指定日志文件中。这样不管是自己分析调试，还是寻求社区帮助，都会方便许多。

需要注意的是，如果客户端是因为网络原因而无法连接到 EMQX 的话，日志追踪功能也是无法提供帮助的，因为此时 EMQX 尚未收到任何报文。这种情况很多时候是因为防火墙、安全组等网络配置原因导致服务器端口没有开放，这在使用云主机部署 EMQX 时尤为常见。所以除了日志追踪，我们可以通过检查端口占用、监听情况，检查网络配置等手段来排除网络方面的原因。

### Q：为什么会有 Client ID 为 CENSYS 的或者是其他我不认识的客户端？

A：CENSYS 是一款互联网探测扫描工具，它会周期性扫描 IPv4 地址空间，探测 HTTP、SSH、MQTT 等协议的默认端口。所以如果你发现有 Client ID 为 CENSYS 的或者其他未知的客户端接入了你的 MQTT Broker，这意味你目前处于相对较低的安全性保障下。以下措施可以有效帮助你避免这个问题：

1. 不要使用默认配置，例如 EMQX 用于验证 HTTP API 访问权限的 AppID 与 AppSecret 等
2. 启用认证，可以是用户名密码认证，也可以是 JWT 认证，避免只需要知道 IP 地址就可以登录的尴尬情况
3. 启用 TLS 双向认证，只有持有有效证书的客户端才能接入系统
4. 启用授权，避免非法设备登录后可以获取敏感数据
5. 配置你的防火墙，尽量关闭一些不需要的端口

### Q：EMQX 是一个主题一个消息队列吗？

A：不是。EMQX 中的每个客户端进程都会有一个消息队列，这个消息队列会存储所有因飞行窗口满或连接断开而暂时无法下发给客户端的消息。消息队列有最大长度限制，以避免消息无限制堆积，达到最大长度后，为了使新消息继续入队，EMQX 会陆续丢弃队列中最老的消息。消息队列最大长度由 `max_mqueue_len` 这个配置项指定。

### Q：EMQX 日志中出现 "Parse failed for function_clause" 是什么原因？

A：这个日志表示报文解析失败，可能因为这不是一个 [MQTT 报文](https://www.emqx.com/zh/blog/introduction-to-mqtt-control-packets)，我们遇到过很多向 MQTT 端口发送 HTTP 请求的情况，也可能因为报文中包含了非 UTF-8 字符等等。我们可以在这条 "Parse failed..." 日志中检索 `Frame data` 关键字以查看完整的报文，帮助我们分析解析失败的可能原因。

### Q：EMQX 日志中出现 "Context: maximum heap size reached" 是什么原因？

A：出现这个日志通常表示相应的客户端进程已经达到了最大堆栈内存占用限制，之后这个进程就会被 EMQX 强制 Kill。这一机制存在的原因是为了保证 EMQX 的可用性，避免客户端进程的内存占用无限制增长最终导致 EMQX OOM。客户端进程的堆栈占用主要来源于飞行窗口和消息队列中未完成确认或未投递的消息，而这两处消息堆积的主要原因通常是客户端消费能力不足，无法及时处理响应消息。

与此相关的配置项是 `force_shutdown_policy`，它的配置格式为 `<Maximum Message Queue Length>|<Maximum Heap Size>`，例如 `10000|64MB`。其中 `<Maximum Heap Size>` 就是限制每个客户端进程能够占用的最大堆栈内存。

我们见过一些用户为了不想客户端进程被强制关闭，不去提升客户端的消费能力，而是一味增大 `<Maximum Heap Size>`，这除了给 EMQX 带来 OOM 风险，也会使得消息的时延增加，往往得不偿失。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
