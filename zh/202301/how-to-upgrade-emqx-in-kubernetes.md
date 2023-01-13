## 背景

为了降低 EMQX 在 Kubernetes 上的部署、运维成本，我们将一些日常运维能力进行总结、抽象并整合到代码中，以 [EMQX Kubernetes Operator](https://github.com/emqx/emqx-operator) 的方式帮助用户实现 EMQX 的自动化部署和运维。

此前，EMQX Kubernetes Operator v1beta1、v1beta2、v1beta3 的升级策略均为滚动升级，相关升级流程如下:

![EMQX Kubernetes 升级流程](https://assets.emqx.com/images/1f6f633cda953e116d11d85c9cd147db.png)


## 问题分析

滚动升级在生产环境中可能会面临以下问题：

1. 升级过程中会逐个销毁旧的节点再创建新的节点，因此可能导致客户端多次断连（最糟糕的情况下断连次数与节点数量一致），从而影响用户体验。
2. 当集群处于较高连接的情况下，一个节点被销毁，那么该节点上面的连接会在瞬间断开，由客户端重试逻辑来进行重连；当单节点连接数较大时，如果大量客户端进行重连，则可能会给服务端造成压力导致过载。
3. 升级完成后，各节点间的负载不均衡（如上图：emqx-ee-0 在升级过程中，客户端可能会进行重连，此时由于 emqx-ee-0 还未就绪，因此可能连接到 emqx-ee-1 或者 emqx-ee-2，升级完成后 emqx-ee-0 上可能只有较少负载或者无负载），从而打破业务容量模型的规划，可能影响到服务。
4. 由于使用 StatefulSets 进行部署，在升级过程中提供服务的节点会比实际节点要少一个（影响到用户的业务模型），这可能会增加服务端的一些压力。

如果上面几个步骤的问题叠加（多次断连与大量断连的客户端不停的重试连接），则可能会放大客户端重连的规模，从而造成服务端过载或雪崩。

下图是在现有升级模式下连接数的监控图（在不同的业务中会存在差异，比如后端依赖的不同资源、服务器配置、客户端重连或重试策略等，均会带来一些不同的影响）。其中：

- sum：总的连接数，图中最上面的一条线
- emqx-ee-a：前缀表示的是升级前 3 个 EMQX 节点
- emqx-ee-b：前缀表示的是升级后 3 个 EMQX 节点

![EMQX 升级](https://assets.emqx.com/images/1afcb48b6ddd3bafa5a893519eacaf20.png)

在上图中，当我们开始执行滚动升级时，首先 emqx-ee-a-emqx-ee-2 进行销毁，并创建新的 emqx-ee-b-emqx-ee-2，此时仅有 emqx-ee-a-emqx-ee-1、emqx-ee-a-emqx-ee-0 能够提供服务，当客户端进行重连时，LB 会将流量转移到 emqx-ee-a-emqx-ee-0、emqx-ee-a-emqx-ee-1 上面，因此我们能够看到 emqx-ee-a-emqx-ee-1、emqx-ee-a-emqx-ee-0 有明显的流量上升，当后面更新这两个 pod 时，意味着客户端可能多次断连。由于新 pod 建立的过程存在着时间差，以上图为例，emqx-ee-a-emqx-ee-0 最后升级，当升级完成后，可能客户端已经完成重试、重连，此时主要连接已经被另两个 pod 接纳，因此会导致 pod 之间流量不均衡，从而影响到用户业务模型的评估，或者影响到服务。

为了方便展示，我们未压测大量连接模拟重连、导致服务端过载的场景（在实际生产环境中可能遇到，TPS 超过云端规划的容量模型），但从连接数监控图上，我们依然看到一个大缺口，说明对业务产生了较大影响。因此我们需制定一种方案来规避以上几个问题，保障升级过程中的平滑稳定。


## 问题解决

### 目标

1. 升级过程中实现连接数可控迁移（可根据服务端处理能力设置相应的迁移速率）。
2. 升级过程中减少连接断开的次数（一次断连）。
3. 在整个升级的过程中始终保持预期的节点来提供服务。
4. 升级完成后，不需要集群负载重平衡，各节点间的连接相对均衡（与 LB 调度策略有一定关系）。

### 方案设计

蓝绿发布是一种同时运行两个版本应用的发布策略。EMQX Kubernetes Operator 近日在 [2.1.0](https://github.com/emqx/emqx-operator/releases/tag/2.1.0) 版本中实现了 EMQX Enterprise 的蓝绿发布，即从现有的 EMQX Enterprise 集群开始，创建一套新版本的 EMQX Enterprise 集群，在这一过程中不停止掉老版本，等新版本集群运行起来后，再将流量逐步平滑切换到新版本上。

从 4.4.12 版本开始，EMQX 企业版本支持**节点疏散**功能。节点疏散功能允许用户在关闭节点之前强制将连接和会话以一定速率迁移到其他节点，以避免节点关闭带来的会话数据丢失。

> 关于节点疏散更多信息请参考: https://docs.emqx.com/zh/enterprise/v4.4/advanced/rebalancing.html

在 Kubernetes 上我们通过模拟蓝绿发布以及结合节点疏散功能，实现了连接可控迁移，极大减少了断连的次数（仅断连一次）。相关升级流程图如下：

![升级流程图](https://assets.emqx.com/images/e5443836664d0ca1549c1c592350620b.png) 

整个升级流程大致可分为以下几步:

1. 升级时（镜像、Pod 相关资源修改调整）我们会先创建一个同规格的节点加入到现有集群中。
2. 当新节点全部就绪后，我们将 service 全部指向新创建的节点，此时新节点开始接受新的连接请求。
3. 将旧节点从 service 中摘出，此时旧节点不再接收新的连接请求。
4. 通过 EMQX 节点疏散功能，逐个对节点上的连接进行可控迁移，直至连接全部完成迁移，再对节点进行销毁。

### 操作流程

节点疏散是 EMQX Enterprise 4.4.12 开始支持的新特性，EMQX Kubernetes Operator 在 2.1 版本中对该能力进行适配，如需使用该能力，请将 EMQX 升级到企业版 v4.4.12，EMQX Kubernetes Operator 升级到 v2.1。

- 配置蓝绿升级

```
apiVersion: apps.emqx.io/v1beta4
...
spec:
   blueGreenUpdate:
    initialDelaySeconds: 60
    evacuationStrategy:
      waitTakeover: 5
      connEvictRate: 200
      sessEvictRate: 200
...
```

`initialDelaySeconds` ：所有的节点就绪后（蓝绿节点），开始节点疏散前的等待时间 （由于切换 Service 后，LoadBalancer 需要时间来处理 service 与 pod 的关系）（单位：秒）

`waitTakeover` ：所有连接断开后，等待客户端重连以接管会话的时间（单位：秒）

`connEvictRate` ：客户端每秒断开连接速度

`sessEvictRate`：`waitTakeover` 之后每秒会话疏散速度

Operator 详细文档请参考：[https://github.com/emqx/emqx-operator/blob/main/docs/en_US/getting-started/getting-started.md](https://github.com/emqx/emqx-operator/blob/main/docs/en_US/getting-started/getting-started.md) 

升级过程中连接数监控图如下（本次测试以 10 万连接进行）：

![升级过程中连接数监控图](https://assets.emqx.com/images/4fb3f674de5f9ed9875d2e9c63de23d8.png)

sum：总的连接数，图中最上面的一条线

emqx-ee-86d7758868：前缀表示的是升级前的 3 个 EMQX 节点

emqx-ee-745858464d：前缀表示升级后的 3 个 EMQX 节点

如上图，我们通过 EMQX Kubernetes Operator 的蓝绿发布在 Kubernetes 中实现了优雅升级，通过该方案升级，总连接数未出现较大抖动（取决于迁移速率、服务端能够接收的速率、客户端重连策略等），能够极大程度保障升级过程的平滑，有效防止服务端过载，减少业务感知，从而提升服务的稳定性。

> 注：由于升级后的集群，三个节点负载较平均，因此上图三条线重叠在了一起。


## 结语

通过采用节点疏散功能结合模拟蓝绿发布，本文所提供的方案解决了普通升级导致的多次断连和可能的服务过载与负载不均问题，实现了在 Kubernetes 上优雅的升级。

作为一个自动化管理工具，EMQX Kubernetes Operator 旨在帮助用户轻松创建和管理 EMQX 集群，充分享受 EMQX 的强大产品能力。通过本文方案完成 EMQX 的升级，用户可以进一步体验 EMQX 的最新特性，构建创新物联网应用。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
