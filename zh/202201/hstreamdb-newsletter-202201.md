在之前的 Newsletter 中，我们对 [HStreamDB](https://hstream.io/zh) v0.7 正在开发或已经完成开发的一些新功能进行了简单介绍。HStreamDB v0.7 致力于改进 HServer 集群的稳定性与可用性以及引入新的透明分区功能，提高用户的使用体验。

本月我们完成了 HStreamDB v0.7 开发和发布的收尾工作，包括透明分区 Stage1 的实现、资源删除的逻辑改进、提供新的 Admin CLI，同时 Java Client 也包含透明分区支持等多项新功能和改进。

## 透明分区

经过之前的原型实现验证，本月我们已经将透明分区 Stage1 在主项目上实现，并将会包含在即将发布的 HStreamDB 的 v0.7 中。

从系统实现角度来看，分区是解决单点瓶颈、提升系统水平扩展能力的有效手段；但从使用者的角度来看，把分区直接暴露给用户，不仅破坏了上层的抽象，增加了用户的学习和使用成本，而且还要用户自己解决更复杂的分区数量变更、重平衡和数据顺序性等问题。透明分区在实现扩展性、保证需求的顺序性的同时，并没有将额外的复杂性暴露给用户，这将极大改善用户使用体验。

## 资源删除

资源删除一直是一个比较棘手的问题，在进行资源管理的过程中，不仅要保证系统可用和一致，同时要符合用户的使用直觉。为此，我们设计了一套 HStreamDB 资源删除的规范，来处理 HStreamDB 中的两种核心资源：Stream 和 Subscription，并规定了两种删除操作：常规删除与强制删除。

在 HStreamDB 中，一个 Subscription 是要依赖 Stream 而存在，因此在常规删除一个 Stream 时，需要确保 Stream 上并没有活跃的 Subscription。同理，在删除一个 Subscription 时需要这个订阅上保证没有活跃的消费者。而强制删除则需要通过 admin 操作，更加详细的文档会在月底 HStreamDB v0.7 发布后实时更新。

## Admin CLI 

为了让用户更方便运维和管理 HStreamDB，我们新增了一个 Admin Tool ，通过它不仅可以对 HStreamDB 内的各种资源进行查询和管理，包括 Stream、Subscription、Query、Connector 等，还可以查询和管理集群内的 Server 节点，以及查看当前的各项 Metrics。同时原来 HStream SQL Shell 中的部分运维和管控能力也迁移到了新的 Admin Tool 中，SQL Shell 之后也将主要专注于 HStreamDB 的使用交互上。总之，Admin Tool 适合 HStreamDB 的运维人员使用，SQL Tool 则主要给 HStreamDB 的用户使用。

## Java Client

### 新功能

- 新增 `BufferedProducer` 接口和实现。考虑到不同场景下用户会对写入的时延和吞吐有不同的要求，为了清晰起见，我们将原来的 `Producer`拆分成了两个独立的`BufferedProducer`和`Producer`，其中`BufferedProducer`主要面向高吞吐的场景，`Producer` 主要用于低延迟的场景。
- `BufferedProducer`新增两种 `flush` 模式。原来的 `Producer` 在 batch 模式下只支持按数据条数触发 flush，现在`BufferedProducer`新增了size-triggered 和 time-triggered 两种`flush` 模式，同时这三类触发条件可以同时起作用，能够更灵活的满足用户的使用需求。
- 新增对透明分区的支持。透明分区涉及 Client 和 Server 交互协议的较大改动和升级，同时包含一些用户层面接口的改动。对透明分区的支持将包含在即将发布的 Client v0.7 ，具体的接口变更请届时参考 Client v0.7 的文档。

### 主要改进

- 修复了 coroutine 可能被阻塞的 Bug
- 改进了 RPC 失败后的重试条件
- 改进了 `Consumer`发生异常时候的处理

## 集成测试

本月对之前集成测试用例进行了梳理和重构，并加入了更多正确路径上的的测试用例以及部分错误注入测试，能够在测试运行中通过随机杀节点等手段注入错误来检测系统实现的正确性和稳定性，同时也修复了测试过程中发现的问题，比如上述的 Client 的改进。

当前集成测试作为一个独立仓库也公开在 [Github](https://github.com/hstreamdb/integration-tests) 上，并通过 GitHub Action 和主仓库联动：在上游主仓库代码更新后会自动触发集成测试运行并生成测试报告。

另外，我们也面向开源社区提供了快速创建本地测试用镜像的脚本，开发者可以在贡献代码前先本地运行集成测试，确保新的代码符合测试规定的行为。

## 文档更新

我们改进了 Quick Start 中启动 HStreamDB 集群的方式，简化了 Quick Start 的流程。用户想要尝试使用 HStreamDB 时，不再需要任何额外的依赖，只要确保装有 Docker 和 Docker-compose 就能直接一行启动一个 HStreamDB 本地集群。
