[EMQX](https://www.emqx.com/zh/products/emqx) 是一款云原生分布式物联网接入平台，通过一体化的分布式 MQTT 消息服务和强大的 IoT 规则引擎，为高可靠、高性能的物联网实时数据移动、处理和集成提供动力，「随处运行，无限连接，任意集成」，助力企业快速构建关键业务的 IoT 平台与应用。

官网地址：[http://www.emqx.com/zh/products/emqx](https://www.emqx.com/zh/products/emqx)

EMQX 团队近日宣布：EMQX 开源版 v4.3.15、开源版 v4.4.4 与企业版 v4.3.10、企业版 v4.4.4 四个维护版本现已正式发布！

此次发布进一步完善了规则引擎，为其新增了多个 SQL 函数、新的持久化数据库集成等，同时支持客户端使用 JWT 携带权限信息。此外还修复了多项目前的已知 BUG，欢迎下载使用：[https://www.emqx.com/zh/try?product=enterprise](https://www.emqx.com/zh/try?product=enterprise)

## 规则引擎新功能

### 为规则引擎 SQL 增加更多的时间转换函数

包含版本 开源版 v4.3.15 开源版 v4.4.4 企业版 v4.3.10 企业版 v4.4.4

规则引擎支持更多时间转换函数，用于支持时间与日期格式转换处理，更多使用方式请参照 [文档](https://docs.emqx.com/zh/enterprise/v4.4/rule/rule-engine_buildin_function.html#时间与日期函数)。

```
now_timestamp() = 1650874276
now_timestamp('millisecond') = 1650874318331
now_rfc3339() = '2022-04-25T16:08:41+08:00'
now_rfc3339('millisecond') = '2022-04-25T16:10:10.652+08:00'
unix_ts_to_rfc3339(1650874276) = '2022-04-25T16:11:16+08:00'
unix_ts_to_rfc3339(1650874318331, 'millisecond') = '2022-04-25T16:11:58.331+08:00'
rfc3339_to_unix_ts('2022-04-25T16:11:16+08:00') = 1650874276
rfc3339_to_unix_ts('2022-04-25T16:11:58.331+08:00', 'millisecond') = 1650874318331
format_date('second', '+0800', '%Y-%m-%d %H:%M:%S%:z', 1653561612) = '2022-05-26 18:40:12+08:00'
format_date('second', 'local', '%Y-%m-%d %H:%M:%S%:z') = "2022-05-26 18:48:01+08:00"
format_date('second', 0, '%Y-%m-%d %H:%M:%S%:z') = '2022-05-26 10:42:41+00:00'
date_to_unix_ts('second', '%Y-%m-%d %H:%M:%S%:z', '2022-05-26 18:40:12+08:00') = 1653561612
date_to_unix_ts('second', 'local', '%Y-%m-%d %H-%M-%S', '2022-05-26 18:40:12') = 1653561612
date_to_unix_ts('second', '%Y-%m-%d %H-%M-%S', '2022-05-26 10:40:12') = 1653561612
```

### 为规则引擎 SQL 增加 float2str/2 函数，支持指定浮点输出精度

包含版本 开源版 v4.3.15 开源版 v4.4.4 企业版 v4.3.10 企业版 v4.4.4

将浮点型数字以指定精度转换为字符串：

```
float2str(20.2, 10) = '20.2'
float2str(20.2, 17) = '20.19999999999999928'
```

### 规则引擎支持消息持久化到 Alibaba TableStore

包含版本 企业版 v4.4.4

表格存储（Tablestore）是阿里云推出的一款云上的结构化数据存储产品，通过 EMQX 的规则引擎实现与 Tablestore 集成，用户可以利用可视化的规则引擎配置界面，快速便捷实现设备元数据、时序数据、消息数据快速集成入库。

### 规则引擎支持使用 Basic 和 JWT 认证连接 Pulsar

包含版本 企业版 v4.3.10 企业版 v4.4.4

Pulsar 支持使用基于 [JSON Web 令牌](https://jwt.io/introduction/)( [RFC-7519](https://tools.ietf.org/html/rfc7519) ) 的 token 对客户端进行身份验证。本次更新支持 Basic 和 JWT 认证，用户可在创建 Pulsar 资源时指定。

![规则引擎](https://assets.emqx.com/images/da6f9640dbf08eb308dc638d51366993.png)

### 规则引擎支持 Oracle Database RAC

包含版本 企业版 v4.3.10 企业版 v4.4.4

Oracle Real Application Clusters (RAC) 支持用户跨多个服务器运行单一 Oracle 数据库，访问共享存储，最大限度提高可用性和水平可扩展性。连接至 Oracle RAC 实例后，无需修改应用，用户会话即可执行故障切换，安全重播中断期间的变更请求，最终用户完全不会感知到中断。

EMQX 提供 service_name 选项可以连接至 Oracle RAC 集群。

## 其他主要新增功能

### 支持 JWT 携带客户端权限信息

包含版本 开源版 v4.3.15 开源版 v4.4.4 企业版 v4.3.10 企业版 v4.4.4

此前 EMQX 支持将 JWT 用于客户端认证，此版本中我们扩展该功能，为 JWT Payload 添加额外的字段 acl 用于存放客户端发布/订阅权限，实现身份认证与权限管理一体。

以下是示例 Payload，声明使用该 Token 的客户端允许订阅 a/b c/+ %u/%c 主题，允许向 a/b c/+ %u/%c 主题：

```
{
  "sub": "emqx",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516239122,
  "acl": {
    "sub": [
      "a/b",
      "c/+",
      "%u/%c"
    ],
    "pub": [
      "a/b",
      "c/+",
      "%u/%c"
    ]
  }
}
```

**特别说明：**

- %u %c 是变量占位符，实际运行时将分别被替换为当前客户端的用户名和客户端 ID。
- 优先级：JWT 鉴权 > 其他鉴权插件。
- 目前 JWT 鉴权仅支持白名单模式，需要设置 acl_nomatch = deny 确保拒绝权限列表外的操作。

### 内置数据库认证鉴权 REST API 支持多条件查询参数

包含版本 开源版 v4.3.15 开源版 v4.4.4 企业版 v4.3.10 企业版 v4.4.4

内置数据库认证授权功能（emqx_auth_mnesia 插件）相关 REST API 支持用户名、客户端 ID 模糊搜索和主题精确搜索，以便用户从大量数据中检索需要的数据，详细 API 请参照 [文档](https://docs.emqx.com/zh/enterprise/v4.4/modules/mnesia_authentication.html#http-api)。

认证数据支持查询参数：

| Name           | Type   | Required | Description                    |
| -------------- | ------ | -------- | ------------------------------ |
| _like_clientid | String | False    | 客户端标识符，子串方式模糊查找 |
| _like_username | String | False    | 客户端用户名，子串方式模糊查找 |

ACL 数据支持查询参数：

| Name           | Type   | Required | Description                    |
| -------------- | ------ | -------- | ------------------------------ |
| access         | Enum   | False    | 是否允许 deny, allow           |
| action         | Enum   | False    | 动作 可取值有：pub,sub,pubsub  |
| topic          | String | False    | MQTT 主题                      |
| _like_clientid | String | False    | 客户端标识符，子串方式模糊查找 |

### 客户端 REST API 新增消息队列长度和丢弃消息数量过滤参数

包含版本 开源版 v4.3.15 开源版 v4.4.4 企业版 v4.3.10 企业版 v4.4.4

此功能旨在于对发生过消息丢弃的客户端进行快速定位和问题排查，用户可以通过 REST API 查找出队列已满/即将满(mqueue_len 参数)、出现过消息丢弃现象(mqueue_dropped 参数)的客户端：

![客户端 REST API](https://assets.emqx.com/images/a6df233977e34df86ec35f2ff25f7412.png)

## 更多功能优化

- 改进认证相关指标，降低其理解难度
- 支持将 REST API 的监听器（8081 端口）绑定到指定的 IP 地址上
- 企业版支持通过 Dashboard 上传更新 License
- 支持配置日志时间格式
- 当 use_username_as_clientid 配置为 true 且客户端连接时未指定 username，现在将拒绝连接并返回 0x85 原因码
- App secret 从部分随机改为完全随机，提供更高的安全性
- 通过 CLI 进行备份恢复时，不再要求备份文件必须位于 EMQX 数据目录的 backup 文件夹下
- 热升级检查，现在不兼容版本之间的热升级将被拒绝
- 允许 EMQX 的安装路径中有空格
- 无效的节点将在启动时报错，并提供可读的错误信息

## BUG 修复

各版本 BUG 修复详情请查看：

- 开源版 v4.3.15： [https://www.emqx.com/zh/changelogs/broker/4.3.15](https://www.emqx.com/zh/changelogs/broker/4.3.15)
- 开源版 v4.4.4： [https://www.emqx.com/zh/changelogs/broker/4.4.4](https://www.emqx.com/zh/changelogs/broker/4.4.4)
- 企业版 v4.3.10：[https://www.emqx.com/zh/changelogs/enterprise/4.3.10](https://www.emqx.com/zh/changelogs/enterprise/4.3.10)
- 企业版 v4.4.4： [https://www.emqx.com/zh/changelogs/enterprise/4.4.4](https://www.emqx.com/zh/changelogs/enterprise/4.4.4)


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
