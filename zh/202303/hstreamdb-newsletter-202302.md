近两个月，HStreamDB 相继发布了 0.13 和 0.14 版本，包含多项已知问题修复。同时，我们也发布了全新的 HStream Console 组件，为 HStreamDB 带来了简洁友好的图形化管理界面，将帮助用户更轻松地使用和管理 HStreamDB.

## HStream Console

HStream Console 是一套基于 Web 的图形化的 HStream UI，用来管理 HStreamDB 集群内的各项资源和工作负载，目前支持的主要功能如下：

- stream 管理：包括查看、新建、删除 stream，以及管理 stream 包含的 shard
- subscription 管理：除基本的管理操作以外，还包括查看当前 subscription 上关联的消费客户端，以及查看 subscription 上的消费进度等
- records 查询：包含根据 recordId 查询指定 stream（shard）内的 records，以及在线的 records 写入等
- 查看 metrics：提供 stream 和 subscription 相关的多种指标的统计图展示，并支持查看不同时间范围的数据（目前 metrics 展示依赖 Promethus，后续 metrics 数据将直接保存在 HStreamDB 中）

![HStream Console](https://assets.emqx.com/images/73ff144e36ad2d614695cf27678701dc.png)

![HStream Console](https://assets.emqx.com/images/a0e1c3c0b6a6bf29785d44781a3b66ce.png)

![HStream Console](https://assets.emqx.com/images/3209eb573c5c2ec44d0ab6e935c7f3d5.png)

后续计划支持：

- 管理 streaming query：包括编辑 SQL，任务提交，显示结果，以及结果的数据可视化
- source 和 sink connectors：包括对多种数据库的支持，以及 IO Task 的创建和管理

## HStreamDB 0.14 发布

v0.14 主要包含以下更新和已知问题修复：

- HServer 默认切换到新的自研 Haskell GRPC 框架
- 新增对 CentOS 7 的部署支持
- 新增对 subscription 上 record 发送失败的指标统计
- 在协议中移除了 pushQuery 相关的 RPC
- 修复多个客户端消费同一个订阅时，由于其中一个退出或不回 ACK 引起其它客户端卡住的问题
- 修复 STM 可能造成 memory leak 的问题
- 修复集群 boostrap 后 status 可能错误的问题
- 修复在同一订阅上创建同名的 consumer 没有报错的问题
- 修复可以在不存在的 shard 上创建 reader 的问题
- 修复 IO check cmd 可能会卡住的问题

## HStream Platform

HStream Platform 是我们正在打造的以开源 HStreamDB 为核心的下一代一站式流数据平台，它将致力于为开发者运行和管理 streaming data workloads 提供真正友好的、统一的、现代化的产品体验。

目前基于公有云的 HStream Platform 的 Serverless 版本已在持续内测阶段，之后我们将推出免费的公测版本，同时 HStream Platform 也将提供 on-premises 部署支持， 欢迎通过 [https://hstream.io/zh/cloud](https://hstream.io/zh/cloud)  与我们联系，获取产品的早期访问以及更多产品动态。
