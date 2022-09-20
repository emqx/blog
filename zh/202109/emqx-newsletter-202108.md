这个 8 月，我们的开源团队正全力投入 EMQX 5.0 的功能开发之中。经过多次激烈讨论和快速迭代，EMQX 5.0 现已发布 alpha.5 版本。我们预计首个 beta 版很快就会发布。


## EMQX 5.0 管理用户界面速览

EMQX 5.0 将呈现全新设计的管理 UI (用户界面）。新设计的 UI 非常注重用户体验的改进，同时兼顾 UI 的清晰度和参数化能力。

下图是 [MQTT](https://www.emqx.com/zh/mqtt) 高级功能的新 UI 界面截图。

![MQTT 高级功能](https://assets.emqx.com/images/e638f39e3c4875aa19bae385f0536b50.png)

新 UI 将使[主题重写](https://www.emqx.com/zh/blog/rewriting-emqx-mqtt5-topic)、自动订阅、延迟发布和事件消息的管理变得轻而易举。



## 动态重新配置 EMQX

![Swagger UI](https://assets.emqx.com/images/0a952d8445d3cc4a59d0949d67e2b011.png)

在之前的 Newsletter 中我们提到，EMQX 5.0 使用 Open API 3.0 来管理 API。如果您访问 https://<emqx-host>:18083/api-docs，浏览器将带您进入 Swagger UI，您可以直接从 GUI（图形用户界面）尝试 API 调用，并查看 API 的详细文档。

我们在 8 月份添加了一个新的框架，它允许 EMQX 用户动态地重新配置集群。对于大多数配置更改，无需重新启动消息服务器即可使配置更改生效。



## Cluster Call 实现配置一致性

我们刚才介绍了动态配置更新和重新加载，那么如何确保更改应用于集群中的所有节点呢？为此我们实现了「Cluster Call 」功能。

在此之前我们一直在 EMQX 中使用 Erlang 的 Multi-call 功能将更改复制到集群中的所有节点。这种方式使用起来很简单，并且在大多数网络场景中都可以正常工作。但是，在回滚或故障处理方面存在不足。

「Cluster Call 」功能允许我们以异步方式复制更改，最终将在集群中的所有节点上应用相同的更改。

## 配置文档生成

在 EMQX 5.0 中，源代码将成为 API 和配置文档的唯一真实来源。借助于 [HOCON 模式功能](https://github.com/emqx/hocon/blob/master/SCHEMA.md)，使代码和文档保持同步将非常轻松。下面是监听器配置文档的示例。

![监听器配置文档示例](https://assets.emqx.com/images/8e3946d74c74a232d0a06afab61800c9.png)

图中是 QUIC 监听器生成的配置文件，正如我们在之前的更新中提到的：EMQX 现在已经有了一个基于 [QUIC](https://datatracker.ietf.org/doc/rfc9000/) 传输的 MQTT PoC 实现。


## RLog 现命名为 Mria

我们之前将异步 Mnesia 数据库复制项目命名为 RLog（即 Replicated Mnesia transaction Log），其作为 [ekka](https://github.com/emqx/ekka) 库的一部分来实施。

我们相信这个项目将使 Erlang/Elixir 社区受益，因此我们决定将其转移至其自身的存储库：[mria](https://github.com/emqx/mria)。

项目名称「mria」源自于世界上最大的飞机 [AN-225 MRIA](https://englishrussia.com/2011/03/17/an-225-mria-the-biggest-aircraft-in-the-world/)，同时也和它的源数据库 Mnesia 有相同的「-ia」后缀。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
