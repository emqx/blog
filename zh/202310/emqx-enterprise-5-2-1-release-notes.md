[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 5.2.1 版本现已正式发布！

这是一个维护版本，包含了几项小更新，主要进行了多项 BUG 修复，进一步提高了产品的稳定性。

## 功能更新

1. 在规则引擎消息重发布规则动作中，支持设置 MQTT 5.0 发布属性与用户属性，以便实现更灵活的消息转发处理。该功能目前仅提供了 REST API，将在后续版本开发 Dashboard 的支持。
2. 客户端认证中，将认证器密码哈希 bcrypt 算法的工作因子 (work factor) 限制在 5-10 的范围内，避免较高的值会消耗太多 CPU 资源。同事更新了 Bcrypt 以允许并行哈希计算，提高认证性能。
3. 改进节点疏散功能，支持疏散所有断开连接的会话，而不仅仅是那些 `clean_start = false` 的客户端的会话，确保节点疏散适用于更多使用场景。
4. 改进了解析 MQTT 无效数据包时的错误消息，以提供更清晰的错误提示。

## BUG 修复

以下是主要 BUG 修复列表：

- 修复了 REST API 示例文档中 `POST /api/v5/publish`  API 错误响应的描述，之前的示例指出错误响应将返回一个列表，但实际情况并非如此。[#11493](https://github.com/emqx/emqx/pull/11493) 
- 修复了尝试下载不存在的日志追踪文件时，会下载一个空的文件的问题。修复后，服务器将返回 404 状态码以及以下 JSON 消息：`{"code":"NOT_FOUND","message":"Trace is empty"}`。[#11506](https://github.com/emqx/emqx/pull/11506) 
- 修复了 CLI 无法清理特定客户端 ID（例如客户端 ID 为纯数字）授权缓存的问题。[#11531](https://github.com/emqx/emqx/pull/11531) 
- 修复了在 Dashboard 中测试 SQL 时 `mongo_date` 函数无法正确输出结果的问题。现在`mongo_date` 函数将返回 `ISODate(*)` 格式的字符串（其中 `*` 是 ISO 日期字符串）。这个格式与 MongoDB 存储日期的格式保持一致。[#11401](https://github.com/emqx/emqx/pull/11401) 
- 修复了核心节点（Core）可能会卡在 `mria_schema:bootstrap/0` 状态，导致新节点加入集群失败的问题。[#11630](https://github.com/emqx/emqx/pull/11630) 

更多功能变更和 BUG 修复请查看 [EMQX Enterprise 5.2.1 更新日志](https://www.emqx.com/zh/changelogs/enterprise/5.2.1)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
