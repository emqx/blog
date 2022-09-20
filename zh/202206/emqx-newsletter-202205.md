五月，EMQX 5.0.0-rc.3 & rc.4 版本陆续发布，该版本为规则引擎新增了对 jq 语法的支持，大幅度精简了默认配置文件，并对 Dashboard 菜单栏做了进一步的调整优化。EMQX 5.0 的正式发布已经越来越近。同时，v4.3 与 v4.4 的下一维护版本也进入了测试阶段，即将发布。

云服务方面，EMQX Cloud 本月海外站新增了 AWS 私网连接以及更多地区部署支持，同时外部认证和数据集成服务也有了更多选择。

## EMQX

### EMQX 5.0.0-rc.3 & rc.4 版本概览

在之前的文章中，我们通过 EMQX 5.0.0-rc.2 [从 Dashboard 的角度对 EMQX 5.0 的部分新功能进行了介绍](https://mp.weixin.qq.com/s?__biz=Mzg3NjAyMjM0NQ==&mid=2247489693&idx=1&sn=037ca242c9f57e912bb54e0625a8cb1a&chksm=cf39c7bbf84e4eaddb1abb719425383b5b882c42aba5d1ebc3b92a32b9393fa935f32c874e55&token=1766001865&lang=zh_CN#rd)。目前 EMQX 5.0.0-rc.3 和 rc.4 也已发布，功能愈发完善稳定。

#### 规则引擎支持 jq 语法

现在，我们可以在规则引擎的 SQL 中使用 jq 语法来处理更加复杂的 JSON 数据。我们可以对 JSON 数组进行索引和切片，可以按条件过滤数据，可以对 Key 进行模糊查询，可以使用管道命令组合多个过滤器，可以使用内置函数计算 JSON 的数组的平均值，甚至可以自定义函数来进行更复杂的计算处理。jq 赋予了规则引擎 SQL 更强大的数据处理能力，我们可以访问 [jq Manual](https://stedolan.github.io/jq/manual/) 来了解更多用法。以下是 jq 在规则引擎 SQL 中的简单使用示例：

```
SELECT
  jq('.', payload) as example
FROM
  "t/#"
```

![EMQX 规则引擎](https://assets.emqx.com/images/75d50358e49e66b38afaef966ac3f3a0.png)

#### 默认配置文件精简

在 5.0.0-rc.4 版本中，我们将默认配置文件精简到了百行以内，额外的配置文件示例将帮助用户了解所有配置项的使用。这将有效帮助用户从大部分不常使用到的配置项中解放出来，仅关注必要的配置项，进一步降低其使用难度。

![EMQX 默认配置文件精简](https://assets.emqx.com/images/7f0130990a92de6514635e2660a3b77a.png)
 

#### 其他优化

- Dashboard 菜单栏调整优化
- Dashboard 支持相对路径或自定义访问路径，方便 NGINX 等反向代理
- 优化了 Dashboard 中速率限制功能的使用，现在可以为 Limiter 配置多个 Buckets，并且在 Listener 中选择 Limiter
- 优化了 Dashboard 中 TLS 证书的配置方式
- 优化了 Dashboard 中资源状态的展示逻辑
- 修复了内存占用计算不准确的问题
- 修复了手动离开集群将导致节点不可用的问题
- 修复了网关监听器的多个错误
- 修复了健康检查相关的多个错误

欲下载试用或了解更多的优化与错误修复信息，请访问 [EMQX 5.0.0-rc.3](https://github.com/emqx/emqx/releases/tag/v5.0.0-rc.3) & [EMQX 5.0.0-rc.4](https://github.com/emqx/emqx/releases/tag/v5.0.0-rc.4)。

### 4.3 & 4.4 维护版本升级预览

v4.3.15 等维护版本即将发布，预计将带来二十余项问题修复以及多项改进，包括 EMQX 支持在包含空格的路径下启动，改进 EMQX 在 Windows 下的启动以避免启动失败时无法看到错误信息，增加版本检查以避免跨大版本热升级等。此外，还有多项功能增强：

#### 规则引擎支持阿里云 TableStore

**包含版本：**企业版 v4.4.4

阿里云表格存储（Tablestore）是阿里云推出的一款云上的结构化数据存储产品，提供了物联网存储 IoTstore、宽表引擎、多元索引等能力来满足时序数据、消息数据、元数据场景的需求。

EMQX 与 Tablestore 团队针对产品高效对接都做了专项优化工作，实现了多元的 IoT 数据高效存储集成。通过 Tablestore 一体化架构，为 IoTstore 提供大规模、免运维的低成本、易扩展的一站式解决方案，有效解决了数据库产品的技术选型、分类存储等技术难点。

目前 EMQX 规则引擎 Tablestore 集成已经通过 10W TPS 吞吐性能测试，可以正式投入生产。

#### 规则引擎 SQL 支持更多函数

**包含版本：**开源版 v4.3.15、开源版 v4.4.4、企业版 v4.3.10、企业版 v4.4.4

1. 时间转换函数

   现在，我们可以在规则引擎 SQL 中使用 `format_date` 函数将传入的整型时间戳或自动换取当前时间戳转换为指定格式的时间字符串，或者使用 `date_to_unix_ts` 函数将指定格式的时间字符串转换为整型的时间戳。示例：

   ```
   SELECT
     format_date('nanosecond', '+08:00', '%y-%m-%d %H:%M:%S%Z') as date1
     format_date('nanosecond', '+08:00', '%y-%m-%d %H:%M:%S%Z', timestamp) as date2
   FROM
     "t/#"
   ```

2. 浮点输出精度控制函数

   增加 `float2str/2` 函数，支持指定浮点数的输出精度。


#### 为 Pulsar 添加 Basic 和 JWT 认证支持

**包含版本：**企业版 v4.3.10、企业版 v4.4.4

我们为 Pulsar 添加了 Basic 和 JWT 认证支持，与 TLS 配合使用，可以获得更佳的安全性。

#### 支持将 JWT 用于鉴权

**包含版本：**开源版 v4.3.15、开源版 v4.4.4、企业版 v4.3.10、企业版 v4.4.4

现在，客户端连接认证时使用的 JWT 可以继续用于鉴权，以获得更灵活的权限管理能力。此功能要求在 JWT 中携带符合格式要求的 acl 声明，详见官网使用文档。

#### 使用内置数据库（Mnesia）作为数据源的认证鉴权支持多条件过滤和模糊查询

**包含版本：**开源版 v4.3.15、开源版 v4.4.4、企业版 v4.3.10、企业版 v4.4.4

与查询客户端类似，现在使用内置数据库作为数据源的认证鉴权功能也提供了这些查询选项，例如 `_like_clientid`，`_like_username`，`topic` 等，其中 `_like_clientid` 和 `_like_username` 支持使用子串进行模糊查询。

#### 支持配置日志时间格式以兼容旧版本中的时间格式

新增 `log.formatter.text.date.format` 配置项，支持配置为 `rfc3339` 或格式化字符串，即 `YYYY-MM-DDTHH:mm:ss.SSSZZ` 的形式以兼容 4.2 等旧版本日志中的时间格式。

### 社区动态

EMQX 团队于 5 月 19-20 日参加了在瑞典斯德哥尔摩举行的 2022 Code BEAM 欧洲会议。

EMQ 软件工程师 William Yang 发表了题为“QUICER：BEAM 的下一代传输协议库”的启发性主题演讲，介绍了世界上第一个由 EMQ 提供支持的 MQTT over QUIC 实现以及为 BEAM 构建的新的开源 NIF 库 QUICER（[GitHub - emqx/quic：用于 Erlang 和 Elixir 的 QUIC 协议](https://github.com/emqx/quic)）。

![William Yang 演讲：QUICER：BEAM 的下一代传输协议库](https://assets.emqx.com/images/026c1aa79c9c2a3a20cadd0830d4097e.png)

EMQ 另一位数据工程师 Dmitrii Fedoseev 则讨论了如何使用 SNABBKAFFE 测试分布式一致性容错，介绍了 EMQ 如何成功地将基于跟踪的方法应用于生产中运行的实际应用程序。

![Dmitrii Fedoseev 分享如何使用 SNABBKAFFE](https://assets.emqx.com/images/61e33788925a071f0f01932fa9bad9e6.png)


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
 

## EMQX Cloud

### 海外站支持创建 AWS PrivateLink

私网连接（PrivateLink）能够实现 EMQX Cloud 部署所在的专有网络 （VPC）与公有云上的服务建立安全稳定的私有连接，简化网络架构，实现私网访问服务，避免通过公网访问服务带来的潜在安全风险。

EMQX Cloud 海外站本月新增支持了对 AWS 上部署的 PrivateLink 的连接，将部署所在的 VPC 和在 AWS（海外）资源所在 VPC 连接起来，相当于实现了同一个网络内的通信。

### 海外站支持更多区域部署

EMQX Cloud 海外站创建部署的区域选择中，AWS 新增香港地区，Google Cloud Platform 新增台湾地区，费用和海外其他地区保持一致。涉及出海业务的企业用户将有更多部署选择。

### 外部认证支持 Redis

新增支持用户使用存放在自己的 Redis 服务中的数据来进行客户端的认证和访问控制。目前 EMQX Cloud 共支持 HTTP、 MySQL、 PostgreSQL、Redis 四种服务用于认证的和访问控制。[了解更多关于外部认证的内容](https://docs.emqx.com/zh/cloud/latest/deployments/custom_auth.html)。

### 数据集成新增 TDengine 和 Lindorm

数据集成添加了新的资源连接： TDengine 和 Lindorm 。TDengine 是一款开源、高性能、分布式、支持 SQL 的时序数据库，目前国内站和海外站都已支持。Lindorm 是阿里云的一款支持宽表、时序、对象、文件、队列、空间等多种数据模型的数据库，目前暂时只支持国内站。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>


## EMQX Kubernetes Operator

五月，用于在 Kubernetes 上自动化部署、配置、管理 EMQX 集群的工具的 EMQX Operator 发布了 1.1.8 版本，提供了如下新功能： 

### 功能更新

1. 将 resource 操作日志完善为 events 事件记录
2. 将 EMQX Operator 中部分 log 转换成 event
3. EMQX Operator resource checklist 实现
4. Better EMQX Custom Resource Status

### 完善优化

1. 修复了镜像 tag 问题，支持基于私有仓库的 tag
2. 修复了更新 .spec.listener.certificate 后，restart listener 异常问题

### 测试验证

1. EMQX Operator 基于云环境实现 EMQX 100 万连接、50 万 TPS 的压力测试

### 即将到来

EMQX Operator 1.2 和 v1beta3 APIVersion 正在开发中，v1beta3 APIVersion 将带来更合理的 .spec 结构， 1.2 版本将引入更完善的事件日志以及集群状态描述。
