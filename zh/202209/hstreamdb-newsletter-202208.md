继月初 [HStreamDB 0.9](https://hstream.io/zh/blog/hstreamdb-v-0-9-release-notes) 正式发布之后，HStreamDB 团队投入了新的 v0.10 的开发周期。本月主要新增了端到端压缩、CLI 支持 TLS 等功能，并修复了多项已知问题，同时新的 Haskell gRPC 框架以及**云原生的全托管流数据库服务 HStream Cloud** 也正在开发中。

## 支持端到端压缩

之前版本的 HStreamDB 支持 HServer 端的数据压缩，即数据在发送给 HStore 之前可以被 HServer 先进行压缩，但从 client 到 HServer 的路径上尚不支持压缩。

本月我们新引入了端到端的压缩功能，即数据在写入时会在 client 端以 batch 为单位进行压缩，且压缩后的数据会被 HStore 直接进行存储。另外 client 端在消费的时候能够自动进行数据的解压，整个过程对用户无感知。

在高吞吐的场景下，通过启用端到端数据压缩能够显著缓解网络带宽瓶颈，提升读写性能，在我们的 benchmark 中显示会有 **4 倍**以上的吞吐提升，当然代价是会增加 client 端的 CPU 消耗。

目前此项功能尚未正式发布，但大家可以通过  HStreamDB 的 [latest 镜像](https://hub.docker.com/r/hstreamdb/hstream/tags) 抢先体验。[Java Client v0.10.0-SNAPSHOT](https://s01.oss.sonatype.org/content/repositories/snapshots/io/hstream/hstreamdb-java/0.10.0-SNAPSHOT/) 也已经包含了对端到端压缩的支持（目前仅支持 gzip 压缩），可通过如下代码使用：

```
BufferedProducer producer =
        client.newBufferedProducer()
            .stream(streamName)
            .compressionType(CompressionType.GZIP)
            .batchSetting(batchSetting)
            .flowControlSetting(flowControlSetting)
            .build();
```

## 新 Haskell gRPC 框架

HServer 使用 gRPC 和 client 进行通信，目前我们使用的 Haskell gRPC 框架是通过 Haskell 的 FFI  (Foreign Function Interface) 绑定到 gRPC C core lib 的。为了增强性能与稳定性，我们正在尝试开发一套新的 Haskell gRPC server 框架进行替换。

新框架受 [hsthrift](https://github.com/facebookincubator/hsthrift) 的启发，将基于 C++ gRPC server 来实现，并且基本不需要对目前的 Haskell 源代码进行改动。目前新框架还在开发和测试过程中，预计将在 v0.10 正式发布。

## HStream CLI 

本月 HStream CLI 也新增了对 TLS 的支持，可参考[文档](https://hstream.io/docs/en/latest/cli/cli.html)使用。

另外， CLI 还带来了以下新功能和改进：

- 新增了多行的 SQL 语句输入的支持
- 新增了  -e、--execute 选项用于非交互式地执行 SQL 语句
- 新增了对输入命令的历史记录的持久化支持
- 优化了执行 SQL 时的错误信息提示

## 其它问题修复和改进

- 更新了 HStream Helm chart 对 v0.9 的部署支持
- 修复了订阅可能会将分区分配给已经失效的 Consumer 的问题
- 修复了 gossip 模块使用  `withAsync` 引起的内存泄漏问题
- 修复了创建 view 时没有检查依赖的 stream 是否存在的问题
- 修复了新节点加入集群时可能会失败的问题
- 改进了 seed-nodes 重启的流程
- 改进了集群启动时对 address 的处理
- 优化了 gossip 模块的线程使用和调度

## HStream Cloud 即将上线

我们正在开发 HStream Cloud —— 基于公有云平台的 **Streaming-Database-as-a-Service** 服务。Early Access 版本即将上线，用户将无需部署和运维，即可快速上手使用 HStreamDB。敬请期待。
