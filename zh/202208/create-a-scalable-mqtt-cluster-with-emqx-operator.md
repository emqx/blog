## 引言：拥抱云原生的 EMQX 5.0 

云原生理念逐渐深入到各企业关键业务的应用开发中。对于一个云原生应用来说，水平扩展和弹性集群是其应具备的重要特性。

作为积极拥抱云原生的大规模分布式开源[物联网 MQTT 消息服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，[EMQX 最新发布的 5.0 版本](https://www.emqx.com/zh/blog/emqx-v-5-0-released)采用了新的后端存储架构 Mria 数据库，并重构了数据复制逻辑，增加了 Replicant 节点角色，使用户可以摆脱有状态节点的限制，对 EMQX 集群进行更加弹性的水平扩展，打造更加符合云原生理念的物联网应用。

> 详情请查看：[《Mria + RLOG 新架构下的 EMQX 5.0 如何实现 1 亿 MQTT 连接》](https://www.emqx.com/zh/blog/how-emqx-5-0-achieves-100-million-mqtt-connections)

用户可以通过 EMQ 发布的管理工具 [EMQX Kubernetes Operator](https://www.emqx.com/zh/emqx-kubernetes-operator)，利用 EMQX 5.0 的 Replicant 节点特性，在 Kubernetes 上通过 Deployment 资源实现无状态节点的部署，快速创建并管理可以承载大规模 MQTT 连接和消息吞吐的 EMQX 集群。

本文将通过对 EMQX Kubernetes Operator 核心特性及应用实操的详细讲解，帮助读者进一步掌握如何快速创建部署及自动化管理可弹性伸缩的 EMQX 集群，充分利用 EMQX 5.0 对云原生的支持特性，拥抱云原生。

## 什么是 EMQX Kubernetes Operator

相信大家对于 Kubernetes（K8s）已并不陌生。它是一个用于自动化部署、扩展和管理容器化应用程序的广泛使用的开源平台。

在 Kubernetes 上，Operator 是对 Kubernetes API 的软件扩展，它使用自定义资源定义（CRD）来提供一个特定于应用程序的 API。Operator 遵循基本的 Kubernetes 原则，如使用 Controllers（ Controller loops ）来调节系统的状态。

Operator 模式结合了自定义资源（CRD）和自定义控制器，将应用程序的领域知识编码为 Kubernetes API 的扩展，可以自动完成常见的协调任务。

![Kubernetes MQTT](https://assets.emqx.com/images/17b4ceffc999286badc02cff2db3c2c4.png)

EMQX Kubernetes Operator 则是一个特定于 EMQX 的控制器，它允许 DevOps 在 Kubernetes 中管理 EMQX 集群部署的生命周期。EMQX Kubernetes Operator 作为 Kubernetes 上的自定义控制器运行，并与 Kubernetes API 服务器（kube-apiserver）进行通信，将高层描述转换为正常的 Kubernetes 资源，以保持所需的应用程序状态。

简单来讲，EMQX Kubernetes Operator 可以帮助用户在 Kubernetes 环境上快速创建和管理 EMQX 集群，不仅极大简化部署和管理流程，也降低了管理和配置的专业技能要求。

EMQX 历经多年迭代，我们也积累了丰富的 EMQX 部署、调优和运维的经验。EMQX Kubernetes Operator 便是我们将这些经验转换为代码的一种成果体现。它使部署和管理工作变成一种低成本、标准化、可重复性的能力，帮助用户高效实现集群扩容、无缝升级、故障处理和统一监控。

## EMQX Kubernetes Operator VS EMQX Helm Chart 

对大多数人来说，手工编写 YAML 文件并不有趣，而且每次需要在 Kubernetes 集群中部署应用或修改配置设置时都要手工编写自定义 YAML，这是一项复杂而且容易出错的工作。

Kubernetes 中的 Helm Chart 和 Operator 则解决了这一难题。这两种用于自动化任务的便捷工具为管理员提供了一种简单的方法，将应用程序或配置部署到 Kubernetes 集群中。这样一来，他们就可以更好地利用 Kubernetes。不过，尽管它们做类似的事情，并不意味着它们是完全可以互换的。

除了 Operator，EMQX 在 Kubernetes 上也提供了 Helm Chart 部署方式，用户可以根据自己的需求选择更合适的部署方式：

- **EMQX Helm Chart**

  Helm 是 Kubernetes 的包管理系统。使用称为 Helm Chart 的打包格式，某人可以将应用程序（例如 Apache HTTP）打包成任何其他人都可以通过几条命令部署到 Kubernetes 集群上的格式，同时只需很少或无需手动更改 YAML 文件。

  如果您熟悉 Linux 环境中的包管理，Helm 图表应该很容易理解。它们类似于 Debian 或 RPM 软件包，而 Helm 本身类似于 apt 或 dnf。就像你可以在 Ubuntu 上 `apt-get install [some package] `一样，你可以在 Kubernetes 上` helm install [some package]` 来让应用程序快速启动并运行。

  EMQX 从 4.0 版本开始就提供了 EMQX Helm Chart，通过 EMQX Helm Chart ，用户可以快速在 Kubernetes 上部署一套 EMQX 集群，并完成初始化操作。Helm Chart 的使用足够简单，适合第一次接触 EMQX 的用户部署和尝鲜。

  不过，Helm Chart 虽然容易上手，但是它只能提供最基本的部署能力。对于 EMQX 这种有状态集群的运维，Kubernetes Operator 是个更好的选择。

- **EMQX Kubernetes Operator**

  如上文所述，通过 Kubernetes 自定义资源（CRD），用户可以使用声明式 API 描述 EMQX 集群，EMQX Kubernetes Operator 会不停调度 Kubernetes 的资源，使 EMQX 集群最终与用户所声明的保持一致。其中大量的运维和更新操作是由 EMQX Kubernetes Operator 自动完成的，用户并不需要关心。

  EMQX Kubernetes Operator 可以让我们更灵活地管理和运维 EMQX 集群，可以让我们摆脱掉复杂而且容易出错的配置修改工作，从而节约大量成本。

  EMQX Helm Chart 与 EMQX Kubernetes Operator 并不是互相竞争，而是互补的关系。EMQX 同时提供这两种部署方式，就是为了让用户可以在不同的场景下选择最适合自己的那一种。

## 随 EMQX 5.0 一同升级的 EMQX Kubernetes Operator

随着 EMQX 5.0 在全新 HOCON 格式配置、Replicant 角色节点等方面的更新，我们也为用户在 Kubernetes 的复杂环境中轻松部署和运维 EMQX 提供了捷径——即将发布的 EMQX Kubernetes Operator 2.0 可以完美支持 EMQX 5.0 的部署管理，在集群策略、配置格式等方面进行了优化升级：

- 全新的集群策略

  EMQX Kubernetes Operator 2.0 依然使用了 Statefulset 资源部署 EMQX Core 节点，这与之前的特性是保持一致的。用户依然可以通过 StoreClass 等 Kubernetes 资源持久化 EMQX 的业务数据，并保证节点的有序性。

  与之前有所不同的是，EMQX Kubernetes Operator 2.0 利用了 Deployment 资源来部署 EMQX Replicant 节点。相比于 Core 节点，Replicant 节点彼此独立，只向 Core 节点发起请求并组成集群，Replicant 节点没有绑定任何持久化的资源，这意味着他们可以随时被销毁和重建。用户可以通过修改 EMQX 自定义资源快速的伸缩 Replicant 节点的数量，更灵活地处理自己的业务。

  ![EMQX 集群策略](https://assets.emqx.com/images/e3af2fec5dee478d4c4fd652ab37f931.png)

  EMQX Kubernetes Operator 2.0 会将所有的管理请求（如 Dashboard、API）路由到 Core 节点，同时将所有的业务请求路由到 Replicant 节点，提高集群的稳定性。

- 全新的配置格式

  在之前的版本中，EMQX Kubernetes Operator 是通过环境变量将配置传递给 EMQX 的，这意味着如果修改配置就会导致 Pod 的重启，而且需要用户熟练掌握 EMQX 的配置与环境变量的转换规则，并不十分友好。EMQX Kubernetes Operator 2.0 将利用 EMQX 全新的 HOCON 配置和 Dashboard 的热配置功能，允许用户将原生的 EMQX 配置写入 EMQX 自定义资源中，并鼓励用户在 EMQX 运行时通过 EMQX Dashboard 的热配置功能来修改 EMQX 的配置。这些配置都会在整个集群中生效，并且会在新的节点加入集群时将配置同步过去，保证所有节点的一致性。

- 全新的升级管理

  在 EMQX 5.0 中，因为引入了不同的集群角色，所以集群升级/降级变得更加复杂。用户需要先升级 EMQX Core 节点，等待所有的 Core 节点升级完毕并且恢复集群后，再升级 Replicant 节点。

  为了简化这一流程，EMQX Kubernetes Operator 2.0 提供了升级管理的能力，当用户想升级 / 降级 EMQX 时，只需要直接修改 EMQX 自定义资源中的 Image，EMQX Kubernetes Operator 就会自动完成所有的工作。

## 使用 EMQX Kubernetes Operator 快速部署 EMQX 5.0

  通过 EMQX Kubernetes Operator，只需要简单的数行 YAML 就可以部署一个 EMQX 集群。

```
$ cat << "EOF" | kubectl apply -f -                
  apiVersion: apps.emqx.io/v2alpha1
  kind: EMQX
  metadata:
    name: emqx 
  spec:                      
    emqxTemplate:   
      image: emqx/emqx:5.0.6
EOF
emqx.apps.emqx.io/emqx applied
```

EMQX Kubernetes Operator 默认部署 3 个 Core 节点以及 3 个 Replicant 节点，用户可以通过修改 EMQX 自定义资源来伸缩节点的数量。

```
$ kubectl get pods 
NAME                              READY   STATUS    RESTARTS        AGE
emqx-core-0                       1/1     Running   0               75s
emqx-core-1                       1/1     Running   0               75s
emqx-core-2                       1/1     Running   0               75s
emqx-replicant-6c8b4fccfb-bkk4s   1/1     Running   0               75s
emqx-replicant-6c8b4fccfb-kmg9j   1/1     Running   0               75s
emqx-replicant-6c8b4fccfb-zc929   1/1     Running   0               75s
```

```
$ kubectl get emqx emqx -o json | jq ".status.emqxNodes"
[
  {
    "node": "emqx@172.17.0.11",
    "node_status": "running",
    "otp_release": "24.2.1-1/12.2.1",
    "role": "replicant",
    "version": "5.0.6"
  },
  {
    "node": "emqx@172.17.0.12",
    "node_status": "running",
    "otp_release": "24.2.1-1/12.2.1",
    "role": "replicant",
    "version": "5.0.6"
  },
  {
    "node": "emqx@172.17.0.13",
    "node_status": "running",
    "otp_release": "24.2.1-1/12.2.1",
    "role": "replicant",
    "version": "5.0.6"
  },
  {
    "node": "emqx@emqx-core-0.emqx-headless.default.svc.cluster.local",
    "node_status": "running",
    "otp_release": "24.2.1-1/12.2.1",
    "role": "core",
    "version": "5.0.6"
  },
  {
    "node": "emqx@emqx-core-1.emqx-headless.default.svc.cluster.local",
    "node_status": "running",
    "otp_release": "24.2.1-1/12.2.1",
    "role": "core",
    "version": "5.0.6"
  },
  {
    "node": "emqx@emqx-core-2.emqx-headless.default.svc.cluster.local",
    "node_status": "running",
    "otp_release": "24.2.1-1/12.2.1",
    "role": "core",
    "version": "5.0.6"
  }
]
```

## 结语

除了更强大的水平扩展能力，EMQX 5.0 还通过[全新改版的 Dashboard](https://www.emqx.com/zh/blog/an-easy-to-use-and-observable-mqtt-dashboard) 提供了更清晰全面的数据监控与管理能力，提升了可观测性。此外，对 [MQTT over QUIC](https://www.emqx.com/zh/blog/mqtt-over-quic) 支持的实现，将使得基于 QUIC 协议的 MQTT 连接 在 Pod 被调度时可以做到无感知切换到另一个 Pod 上，从而进一步提高集群的可用性。这些都将使用户可以借助 EMQX 5.0 构建更加云原生的应用。

EMQX Kubernetes Operator 则为用户创建和管理 EMQX 集群提供了更加便捷的途径，帮助用户更轻松地体验到 EMQX 5.0 的云原生特性。

未来 EMQ 将持续在云原生方向发力，将 EMQX 进化为一个弹性的、无状态的 MQTT Broker，同时配合 eKuiper、Neuron 等 EMQ 边缘计算产品，进一步探索分布式云原生的落地。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
