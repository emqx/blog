本月我们发布了 HStreamDB 0.12，更新了对应的 Java Client 支持，同时带来了 HStream Operator 的首个版本以及新的 HStream Gateway 组件。

## HStreamDB 0.12 发布

本月 HStreamDB 0.12 版本已经发布，主要带来了以下更新和问题修复：

- 新增支持基于本地文件的元数据存储，主要用于简化本地开发和测试环境下的部署
- 新增 advertised-listener 的 TLS 支持 
- 新增获取连接到订阅上的客户端信息（包括 IP、客户端 SDK 的类型和版本等）的 RPC 接口
- 新增用于获取订阅消费进度的 RPC 接口 
- 新增列出当前 ShardReader 的 RPC 接口
- 新增对内部存储消费进度的 stream 的副本数的配置支持
- 修复了某些情况下订阅的消费进度没有被正确保存的问题
- CLI 工具若干优化：部分命令选项简化、集群交互改进、请求重试、删除命令改进
- SQL 层切换到新的 planner 实现
  - 提升了稳定性和性能
  - 改进了对 FROM 语句中的子查询的支持
  - 新增 EXPLAIN 语句用于查看逻辑执行计划
  - 整体采用更为模块化的设计，方便后续扩展和优化

## Java Client 0.11&0.12 发布

本月 Java Client 发布了 0.11 和 0.12 两个版本，包括对 HStreamDB 0.11 和 0.12 新特性的支持，主要更新有：

- 新增支持获取 `stream` 和 `suscription` 的创建时间
- 新增支持从 `ReceviedRecord` 获取 record 的发布时间（指 HStreamDB 收到对应数据时间）
- `HStreamClient` 新增 `listConsumers` 方法
- `HStreamClient` 新增 `getSubscription` 方法
- 新增默认的请求超时配置
- 规范了连接 HStreamDB 的 URL 的 schema，包括 `hstream://`（plaintext 连接）和 `hstreams://` (TLS 连接)

## HStream Gateway

HStream Gateway 是 HStreamDB 的独立网关组件。在一般的使用场景中它不是必须的，但在某些场景下，比如跨网络访问，出于多种考虑不希望直接暴露 HStreamDB 的集群地址，或者客户端无法直连 HStreamDB 集群的场景，它是非常适用的。 由于 HStreamDB 有自己特定的客户端请求路由协议，无法直接前置通用的代理服务器或者负载均衡器，因此需要专门的 HStream Gateway。

目前 HStream Gateway 除了能够代理客户端到 HStreamDB 集群的所有请求，还提供了客户端认证、TLS 终结、请求限流等功能。此外，Gateway 可搭配通用的负载均衡器使用，也支持 gRPC 的客户端负载均衡协议。

## HStream Operator 首个版本发布

HStream Operator 是面向 Kubernetes 的 HStreamDB 自动部署和运维系统，旨在提供对 HStreamDB 的包括部署、扩缩容、配置更新、版本升级、备份恢复等过程的全生命周期自动化管理。通过 HStream Operator，HStreamDB 可以无缝运行在多个公有云或私有部署的 Kubernetes 环境下。

本月我们推出了 HStream Operator 的首个版本，该版本主要提供了自动化部署包括 HServer 和 HStore 等 HStreamDB 的核心组件以及 bootstrap 集群的能力，另外还支持通过配置 `PVC` 对数据进行持久化存储。
目前可参考[文档](https://github.com/hstreamdb/hstream-operator/blob/main/docs/zh_CN/getting-started/getting-started.md)使用 HStream Operator。

## 即将到来

HStream Platform 是我们即将推出的基于公有云的 **Serverless** 流数据平台服务，提供免部署、零运维、高可用、一站式的流数据存储、实时处理和分析服务。

本月 HStream Platform Alpha1 已进入内部测试阶段，内测完成后将很快发布公测版本，敬请期待！您也可以在 [https://hstream.io/cloud](https://hstream.io/cloud) 提前注册，第一时间获取上线通知。
