[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 4.4.23 版本现已正式发布！

这是一个维护版本，优化了节点通信性能、并修复了 2 个 BUG，进一步提高了产品的稳定性。

## 性能提升

优化了用于节点间 MQTT 消息传输的 `gen_rpc` 库，改进了其对通道中积压消息的处理能力，从而使系统更快地从流量高峰中恢复。

## BUG 修复

以下是 BUG 修复列表：

- 修复规则引擎无法连接到 [Upstash](https://upstash.com/) Redis 的问题。修复前，在与 Redis 服务建立 TCP 连接之后，EMQX 的 Redis 驱动程序使用 [inline commands](https://redis.io/docs/reference/protocol-spec/#inline-commands) 来发送 AUTH 和 SELECT 命令。但 Upstash Redis 服务不支持 inline commands，导致 EMQX 无法连接到 Upstash Redis 服务。 修复后，EMQX 的 Redis 驱动使用 RESP (Redis Serialization Protocol) 来发送 AUTH 和 SELECT 命令。
- 为 "离线消息保存到 Redis" 动作和 Redis 资源的某些参数增加了合法性校验。
  - 校验 "离线消息保存到 Redis" 动作的 "Redis Key 超期时间" 参数。
  - 校验 Redis 资源的 "Redis 数据库" 参数。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
