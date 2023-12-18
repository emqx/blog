[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 5.3.2 版本现已正式发布！

这是一个维护版本，包含了几项小更新，主要进行了多项 BUG 修复，进一步提高了产品的稳定性。

## 功能更新

1. MQTT 文件传输能力得到了增强，现在客户端可以使用异步的方式进行文件传输：客户端可以通过 `$file-async/...` 主题进行文件传输，并通过 `$file-response/{clientId}` 主题订阅命令执行结果。相比于此前仅能通过 MQTT 5.0 专有特性 PUBACK 原因码获取传输结果而言，异步模式可以更好的用于 MQTT v3.1/v3.1.1 客户端，以及 MQTT 桥接传输的场景。
2. 将核心-复制数据库同步的默认 RPC 驱动从 `gen_rpc` 更改为 `rpc`，提升了核心副本数据复制的速度。

- 提升了 `emqx` 命令的性能。
- 为 Redis 授权数据源中的 Redis 命令添加了验证功能。此外，此次改进优化了认证和授权过程中 Redis 命令的解析，现在的解析符合 `redis-cli` 兼容性标准，并支持引号参数。

## BUG 修复

以下是 BUG 修复列表：

- [#11785](https://github.com/emqx/emqx/pull/11785) 拥有“查看者”角色的用户具有更改自己密码的权限，但无权更改其他用户密码。

- [#11757](https://github.com/emqx/emqx/pull/11757) 修复了下载不存在的追踪文件时返回的错误响应码。现在，响应码会返回 `404` 而不是 `500`。

- [#11762](https://github.com/emqx/emqx/pull/11762) 修复了 EMQX 中 `built_in_database` 授权数据源的一个问题。现在在删除数据源时，所有 ACL 记录都会被彻底移除，解决了数据库残留的记录在重新创建授权数据源时仍然存在的问题。

- [#11771](https://github.com/emqx/emqx/pull/11771) 修复了通过 API/Dashboard 进行身份验证管理时 Bcrypt 盐轮次(salt rounds)的验证问题。

- [#11780](https://github.com/emqx/emqx/pull/11780) 修复了 `pbkdf2` 密码哈希算法中 `iterations` 字段的验证问题。现在，`iterations` 必须是严格正数。之前，`iterations` 可以被设置为 0，这会导致验证器无法正常工作。

- [#11791](https://github.com/emqx/emqx/pull/11791) 修复了 EMQX CoAP 网关中的一个问题，即心跳没有有效地维持连接的活跃状态。此修复确保心跳机制正确维持 CoAP 网关连接的活跃状态。

- [#11797](https://github.com/emqx/emqx/pull/11797) 修改了管理 `built_in_database` 授权数据源的 HTTP API 行为。如果未将 `built_in_database` 设置为授权数据源，这些 API 现在将返回 `404` 状态码，替换了以前的 `20X` 响应。

- [#11965](https://github.com/emqx/emqx/pull/11965) 优化了 EMQX 服务的停止过程，确保即使在存在不可用的 MongoDB 资源的情况下，也能够实现优雅停止。

- [#11975](https://github.com/emqx/emqx/pull/11975) 此修复解决了由于对端和服务器同时关闭套接字时发生竞争条件导致的冗余错误日志问题。以前，由操作系统和 EMQX 触发的并发套接字关闭事件会导致不必要的错误记录。通过改进事件处理，本次修复消除了不必要的错误信息。

- [#11987](https://github.com/emqx/emqx/pull/11987) 修复了在尝试设置 TCP/SSL 套接字的 `active_n` 选项时连接崩溃的问题。

  在此修复之前，如果在连接过程中尝试设置 `active_n` 选项时套接字已经关闭，会导致 `case_clause` 崩溃。

- [#11754](https://github.com/emqx/emqx/pull/11754) 改进了 PostgreSQL 桥接的日志格式化功能，针对驱动程序返回的错误消息中的 Unicode 字符进行了处理。

更多功能变更和 BUG 修复请查看 [EMQX Enterprise 5.3.2 更新日志](https://www.emqx.com/zh/changelogs/enterprise/5.3.2)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
