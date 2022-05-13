九月里，EMQX 团队收获颇丰。

EMQX 获得了来自海外知名 IIoT 社区 4.0 Solutions 的赞誉，被称为「目前为止市场上最好的企业级 MQTT  消息中间件」，团队成员也受邀参与了社区交流活动。来自社区的肯定转化为项目推进的动力——v5.0 的首个 beta  版迎来了正式发布，又为用户带来了一些振奋人心的新功能。

撒下种子，总有收获的一天。

## 感受来自 IIoT 社区的热情

9 月初，受 IIoT 社区 4.0 Solutions 的邀请，EMQX 团队的技术专家参与了其举办的线上直播活动，向在线用户展示了 EMQ 的先进技术与产品。

4.0 Solutions 社区专注于通过大数据、云平台、人工智能 (AI) 和工业物联网 (IIoT) 等技术帮助企业实现数字化工厂。打造工业物联网的核心是通过 MQTT 消息服务器（集群）连接海量设备，而 EMQX 则正是这一宏伟蓝图中的完美选择，也因此受到了 4.0 Solutions 社区的高度认可。

能够深入 IIoT 社区与成员们交流让我们感到十分荣幸。在一个小时的活动中，我们就有关 EMQ 公司及产品的许多迫切问题进行了一一解答。

![IIoT 社区](https://assets.emqx.com/images/b709690f73732fa72e5038a0ba7a4460.png)

视频回放链接：[https://www.youtube.com/watch?v=nP7JAlpyvfo](https://www.youtube.com/watch?v=nP7JAlpyvfo) 

## EMQX v5.0-beta.1 正式发布

在九月，我们非常激动和自豪地宣布了 EMQX 5.0 版的首次预发布。

在这一版本中主要**新增了以下功能**：

- 统一认证、授权和网关管理
- 统一的数据桥接和规则引擎功能
- 新的配置管理（HOCON）
- 异步数据库复制 (Mria) ，使集群更具扩展性
- MQTT over QUIC：一个前沿研究项目

详细信息请查看发布说明。新功能已经公开，用户可以进行体验和评估。

更多 beta 版本推出在即，我们热切欢迎和期待每一个用户充分表达自己的期望或需求，你的意见或将成为影响 EMQX 未来发展的关键要素。

## 更多期待的 beta.2

在 beta.2 版本中，我们的工作重点是将仪表板（此功能在 beta.1 中进行了隐藏）在前台呈现，此外很多涉及少量 UI 更改的功能也将有所调整。

### 过载保护

在高负载下，一个理想的稳健系统应该能够在侦测到过载后开始向输入方增加反向压力，而不是降低服务质量甚至崩溃宕机。有了过载保护功能，相较于设置连接总数等硬性限制，EMQX 可以更好地实现自我保护，离「理想的稳健系统」更近了一步。

### 插件直接安装

EMQX 是高度可扩展的。

正如我们之前在博客中介绍过的那样，插件可以实现独立安装。从 5.0 版开始，EMQX 开源用户将能够通过直接安装扩展包升级到企业版。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
