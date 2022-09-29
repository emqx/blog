本月我们实现了 HServer 支持 Rqlite 作为 MetaStore，并基于新的自研 Haskell gRPC 框架对 HServer 进行了重构，同时发布了新的 Rust Client 以及集群部署工具。此外，HStream Cloud 目前已支持提交注册申请早期访问。

## HServer 支持 Rqlite 作为 MetaStore

HStreamDB 依赖 MetaStore 组件来保存集群元数据，目前使用 Zookeeper 作为默认的 MetaStore 实现。 近期我们基于抽象的 MetaStore 接口对 HStreamDB 的架构进行了调整，使它能够支持多种 MetaStore 的实现，并新增了基于 Rqlite 的实现。 考虑到 Rqlite 相比 Zookeeper 更加轻量、易于部署管理且支持 SQL 接口和事务等，后续 HStreamDB 将使用 Rqlite 作为默认的 MetaStore 组件。

目前 HServer 和 HStream IO 已经完成了对 Rqlite 的适配（HStore 尚未完成），可使用 HStreamDB 的 latest 镜像[https://hub.docker.com/r/hstreamdb/hstream/tags](https://hub.docker.com/r/hstreamdb/hstream/tags) ，通过指定 HServer 的启动选项 `--metastore-uri rq://172.16.10.1`来使用。

## HServer gRPC 改进

如上期 [Newsletter](https://hstream.io/zh/blog/hstreamdb-newsletter-202208) 所述，出于稳定性和性能等多方面考虑，我们正在使用自研的 Haskell gRPC 库替换目前 HServer 使用的 gRPC 库。本月主要新增了对 gRPC 双向流的支持，并已经完成了整体的初步替换。后续将继续进行更多测试和问题修复，基于新的 gRPC 库的 HServer 将包含在 v0.10 并计划于下月正式发布。

## 新的集群部署工具

本月我们发布了一个新的 HStreamDB 集群部署工具[https://github.com/hstreamdb/deployment-tool](https://github.com/hstreamdb/deployment-tool) ，相比之前的部署脚本它提供了更简化的配置，并行的多节点部署支持并改进了易用性。它基于 Golang 编写，可直接下载[https://github.com/hstreamdb/deployment-tool/releases](https://github.com/hstreamdb/deployment-tool/releases) 使用，基本用法如下：

1. 通过 `hdt init` 生成部署模板

2. 根据实际环境修改部署配置

   ```
   global:
     user: "root"
     
   monitor:
     node_exporter_port: 9100
     cadvisor_port: 7000
     grafana_disable_login: true
   
   hserver:
     - host: 172.24.47.173
     - host: 172.24.47.174
     - host: 172.24.47.175
   
   hstore:
     - host: 172.24.47.173
       enable_admin: true
     - host: 172.24.47.174
     - host: 172.24.47.175
   
   meta_store:
     - host: 172.24.47.173
     - host: 172.24.47.174
     - host: 172.24.47.175
   
   prometheus:
     - host: 172.24.47.172
   
   grafana:
     - host: 172.24.47.172
   ```

3. 运行 `hdt start` 执行部署

   具体用法可参考 [https://github.com/hstreamdb/deployment-tool/blob/main/README.md](https://github.com/hstreamdb/deployment-tool/blob/main/README.md) 

## 新增 Rust Client

本月我们新发布了 HStreamDB 的 Rust 语言客户端库 [https://github.com/hstreamdb/hstreamdb-rust](https://github.com/hstreamdb/hstreamdb-rust) ，它主要基于 Rust 的异步运行时 [Tokio](https://docs.rs/tokio) 和 gRPC 库 [Tonic](https://docs.rs/tonic) 实现，目前支持 HStreamDB 0.9 及以上版本，包含了 stream 和 subscription 创建管理以及数据写入和消费等基本功能。下载和使用可参考：[https://crates.io/crates/hstreamdb](https://crates.io/crates/hstreamdb)。

后续我们计划基于 Rust Client 的 FFI 为更多尚未支持的语言开发对应的客户端，一方面可以降低多语言 Client 的维护成本，另一方面也能获得更好的性能。目前我们基于 [https://github.com/rusterlium/rustler](https://github.com/rusterlium/rustler) 开发了另一个实验性的 Erlang Client  [https://github.com/hstreamdb/hstreamdb_erl-rs](https://github.com/hstreamdb/hstreamdb_erl-rs)。

## HStream Cloud 体验申请开放

本月我们对 [HStreamDB 官网](http://hstream.io/) 进行了升级，目前您可以通过 [https://hstream.io/cloud#register](https://hstream.io/cloud#register) 提交注册申请，届时我们将第一时间邀请您进行免费试用。
