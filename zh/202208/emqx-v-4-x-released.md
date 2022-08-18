近日，EMQX 开源版 v4.3.17、v4.3.18、v4.4.6、v4.4.7，与企业版 v4.3.12、v4.3.13、v4.4.6、v4.4.7 八个维护版本正式发布。

此次发布包含了多个功能更新：规则引擎 RocketMQ 支持 ACL 检查、Kafka 支持 SASL/SCRAM 与 SASL/GSSAPI 认证以适配更多部署方式，提升规则引擎 TDengine 写入性能以及 [MQTT 共享订阅](https://www.emqx.com/zh/blog/introduction-to-mqtt5-protocol-shared-subscription)性能，同时在 CLI 中提供了配置文件检查命令，方便用户修改 EMQX 配置。此外还修复了多项已知 BUG。

欢迎下载使用：[https://www.emqx.com/zh/try](https://www.emqx.com/zh/try?product=enterprise)

## 规则引擎新功能

### RocketMQ 支持携带用户信息实现 ACL 检查

包含版本 `企业版 v4.3.12` `企业版 v4.4.6`

RocketMQ 在 4.4.0 版本开始支持 ACL，通过创建多个用户并为其赋予不同的 Topic 和消费组权限，以达到用户之间的权限隔离。开启 ACL 访问控制会导致没有配置认证信息的客户端连接中断。

本次发布 EMQX 新增了 RocketMQ ACL 支持，在资源创建页面填入用户信息即可连接至启用 ACL 的 RocketMQ 示例，以实现更安全的数据集成。

### Kafka 支持 SASL/SCRAM 与 SASL/GSSAPI 认证

包含版本 `企业版 v4.4.6`

SCRAM 是 SASL 机制家族的一种，是针对 SASL/PLAIN 方式的不足而提供的另一种认证方式。这种方式能够支持动态添加用户，同时使用 sha256 或 sha512 对密码加密，安全性相对会高一些。SASL/GSSAPI 主要是给 Kerberos 使用的。

新增的两种认证方式让 EMQX 能够用于更多的 Kafka 环境，满足企业用户不同的安全配置需求。

### 提升规则引擎中 TDengine 的写入性能

包含版本 `企业版 v4.3.12` `企业版 v4.4.6`

优化底层驱动实现 TDengine 写入性能的提升，同时写入数据到 TDengine 的动作中新增 `db_name` 字段以改善对超级表的支持。

### 规则引擎支持分页和搜索

包含版本 `开源版 v4.3.17` `开源版 v4.4.6` `企业版 v4.3.12` `企业版 v4.4.6`

规则引擎列表查看 REST API 支持分页与模糊搜索包括规则的 SQL、Topics 列表、动作列表等。此特性旨在于让用户更方便地管理规则，尤其是规则数量较多的时候。

> 本次更新默认兼容旧版本 API，仅在 Query 中携带指定参数才会返回分页格式数据。

Query 查询参数：

| Name              | Type    | Required | Description                                                  |
| :---------------- | :------ | :------- | :----------------------------------------------------------- |
| enable_paging     | Boolean | False    | 是否支持分布功能，如果开启，则返回带分页的元信息             |
| enabled           | Boolean | False    | 过滤条件：规则是否开启状态                                   |
| for               | String  | False    | 返回 topic 完全匹配的规则                                    |
| _like_id          | String  | False    | 根据 id 子串方式模糊查找                                     |
| _like_for         | String  | False    | 根据 Topic 子串方式模糊查找                                  |
| _match_for        | String  | False    | 根据 Topic 匹配查询，比如: t/# 包括 t/1, t/2                 |
| _like_description | String  | False    | 根据描述子串方式模糊查找                                     |
| _page             | Integer | False    | 页码                                                         |
| _limit            | Integer | False    | 每页显示的数据条数，未指定时由 `emqx-management` 插件的配置项 `max_row_limit` 决定 |

## 通过 CLI 检查配置是否正确

包含版本 `开源版 v4.3.17` `开源版 v4.4.6` `企业版 v4.3.12` `企业版 v4.4.6`

在重启 EMQX 之前使用 CLI 命令测试当前配置是否正确，能够检测包括配置语法、配置文件格式、配置项引起的错误，避免应用配置时因为配置错误 block EMQX 启动。

```
./bin/emqx check_conf
```

## Dashboard 支持清除历史告警

包含版本 `企业版 v4.3.12` `企业版 v4.4.6`

EMQX 内置监控告警功能，支持监控 CPU 占用率、（系统/进程）内存占用率、进程数量、规则引擎资源状态、集群脑裂与愈合并进行告警。

此前 EMQX 已经支持历史告警清除 REST API，本次发布在 Dashbaord 实现了告警清除能力。

![EMQX Dashbaord](https://assets.emqx.com/images/bf5da016b92c2b4458c694c02c051733.png)

## 新增 TLS 垃圾回收配置

包含版本 `开源版 v4.3.18` `开源版 v4.4.7` `企业版 v4.3.13` `企业版 v4.4.7`

允许配置连接进程在 TLS 握手完成后进行垃圾回收以减少内存占用，这可以使每个 SSL 连接减少大约 35% 的内存消耗，但相应地会增加 CPU 的消耗。

## 其他重要变更

- 优化共享订阅性能
- 开源版 v4.3.13 升级了 OTP 版本以解决 OTP Bug 导致的随机进程失去响应的问题（出现概率较低），建议仍在使用 v4.3 的用户升级到此版本
- 允许配置 TLS 握手日志的日志等级以便查看详细的握手过程
- 从下一版本起，我们将停止对 macOS 10 的支持，转为提供 macOS 11 的安装包

## BUG 修复

各版本 BUG 修复详情请查看：

- 开源版 v4.3.17： https://www.emqx.com/zh/changelogs/broker/4.3.17  
- 开源版 v4.3.18： https://www.emqx.com/zh/changelogs/broker/4.3.18   
- 开源版 v4.4.6： https://www.emqx.com/zh/changelogs/broker/4.4.6
- 开源版 v4.4.7： https://www.emqx.com/zh/changelogs/broker/4.4.7 
- 企业版 v4.3.12：https://www.emqx.com/zh/changelogs/enterprise/4.3.12 
- 企业版 v4.3.13：https://www.emqx.com/zh/changelogs/enterprise/4.3.13  
- 企业版 v4.4.6： https://www.emqx.com/zh/changelogs/enterprise/4.4.6 
- 企业版 v4.4.7： https://www.emqx.com/zh/changelogs/enterprise/4.4.7



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
