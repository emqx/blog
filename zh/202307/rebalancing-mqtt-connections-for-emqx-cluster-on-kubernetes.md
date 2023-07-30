## 引言

[MQTT 连接重平衡](https://docs.emqx.com/zh/enterprise/v4.4/advanced/rebalancing.html#motivation)是 [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 的一个核心功能，它通过把客户端连接和会话从负载过高的节点转移到负载较轻的节点，达到负载均衡的目的。该功能可以自动计算需要迁移的连接数量，并进行相应的迁移操作。这个过程通常会在新节点加入集群或节点重新启动后执行，以保障集群的负载保持均衡。EMQX 会将 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)连接和 [MQTT 会话](https://www.emqx.com/zh/blog/mqtt-session)一起迁移，以防止会话丢失。

MQTT 连接重平衡主要有以下两个好处：

- **增强系统的扩展性：**由于 MQTT 连接是基于 TCP/IP 协议的长连接，当集群扩容后，旧节点的连接不会自动迁移到新节点上。如果希望新节点承载旧节点上部分负载，可以通过重平衡功能，将旧节点上的负载平滑地迁移到新节点上，从而使整个集群负载更加均衡，提高系统的吞吐量，响应速度以及资源利用率，使系统更好地扩展。
- **减少运维开销：**如果系统中某些节点负载过高或过低，需要对这些节点进行手动调整，而通过重平衡，可以自动调整节点的负载，降低运维成本。

> 只有 EMQX Enterprise 4.4.12 及以后的版本才支持群集负载重平衡功能。
>
> 深入了解全球最具扩展性的 MQTT Broker：[EMQX Enterprise：大规模企业级 MQTT 平台](https://www.emqx.com/zh/products/emqx)

在本文中，我们将介绍如何在 Kubernetes 上启用 EMQX 的 [MQTT 连接](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)重平衡功能。

## MQTT 连接重平衡的工作流程

[EMQX Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 提供了一种名为 `Rebalance` 的自定义资源类型，让用户可以方便地执行 MQTT 连接重平衡。要在 EMQX 集群中进行 MQTT 连接重平衡，只需部署一个新的 `Rebalance` 资源，EMQX Operator 会监听提交的资源，并根据情况启动 EMQX 的重平衡任务。

EMQX 在开始重平衡任务之前，会把集群中的节点划分为源节点和目标节点。

- 源节点是连接数过多的节点，不会再接受新连接。
- 目标节点是连接数较少的节点。

EMQX Operator 会把源节点从 Endpoints 中移除，让新连接只分配给目标节点。连接到源节点的客户端会被 EMQX 逐步断开，直到源节点和目标节点的平均连接数达到平衡。接着，源节点的会话也会迁移到目标节点。重平衡任务完成后，EMQX 会把源节点恢复正常状态。最后，EMQX Operator 把源节点重新加入到 Endpoints，结束重平衡任务。

## MQTT 连接重平衡与传统负载平衡器对比

传统的负载平衡器可以把 MQTT 连接分配到可用节点。但是，由于长连接是基于 TCP/IP 协议的，集群扩容时，旧节点上的 MQTT 连接不会自动迁移到新节点上。因此可以采用最少连接数（Least Connection）的负载平衡策略，让每个节点上的连接数相对均衡。

不过，大部分云供应商的负载平衡器都不支持 `Least Connection` 策略。所以，传统的负载平衡器并不能很好地解决 EMQX 集群 MQTT 连接不平衡的问题。同时，MQTT 连接重平衡需要负载平衡器把重连的连接导向目标节点。因此，可以把这两种方法结合起来，以达到更好的效果。正确配置它们可以让 EMQX 集群的 MQTT 负载更加均衡，从而提升系统的可用性和可靠性。

## 示例：在 Kubernetes 上重新平衡 MQTT 连接

接下来，我们将介绍如何在 Kubernetes 上进行 MQTT 连接重平衡，并给出一个 `Rebalance` 配置示例，展示 MQTT 连接重平衡的效果。

### 先决条件

在 Kubernetes 上部署 EMQX 之前，请确保满足以下要求：

- [Kubernetes](https://kubernetes.io/docs/concepts/overview/)：版本 >= 1.24
- [Helm](https://helm.sh/)：版本 >= 3

### 安装 EMQX Operator

1. 安装并启动 cert-manager

   要求 cert-manager 1.1.6 或以上版本。如果已经安装并运行了 cert-manager，可以跳过这一步。

   ```
   $ helm repo add jetstack https://charts.jetstack.io
   $ helm repo update
   $ helm upgrade --install cert-manager jetstack/cert-manager \
     --namespace cert-manager \
     --create-namespace \
     --set installCRDs=true
   ```

   您也可以按照 [cert-manager 安装指南](https://cert-manager.io/docs/installation/)进行安装。

2. 通过 Helm 安装 EMQX Operator

   ```
   $ helm repo add emqx https://repos.emqx.io/charts
   $ helm repo update
   $ helm install emqx-operator emqx/  emqx-operator --namespace emqx-operator-system --create-namespace
   ```

3. 等待 EMQX Operator 就绪

   ```
   $ kubectl wait --for=condition=Ready pods -l "control-plane=controller-manager" -n emqx-operator-system
   
   # If you get output results similar to the following, it indicates that emqx-operator is ready:
   # 如果得到类似下面的输出结果，表示 emqx-operator 已经就绪：
   pod/emqx-operator-controller-manager-57bd7b8bd4-h2mcr condition met
   ```

### 安装 EMQX Enterprise

1. 将下面的 YAML 配置文件保存为 `emqx.yaml`。

   ```
   apiVersion: apps.emqx.io/v1beta4
   kind: EmqxEnterprise
   metadata:
      name: emqx-ee
   spec:
      template:
        spec:
          emqxContainer:
            image:
              repository: emqx/emqx-ee
              version: 4.4.19
   ```

   并使用 `kubectl apply` 命令来部署 EMQX。

   ```
   $ kubectl apply -f emqx.yaml
   ```

2. 等待 EMQX 集群就绪。

   ```
   $ kubectl get emqxenterprises
   
   NAME      STATUS   AGE
   emqx-ee   Running  8m33s
   ```

### 重新平衡 MQTT 连接

1. 集群负载（重平衡前）

   在重平衡之前，我们搭建了一个负载不平衡的集群。并用 Grafana 和 Prometheus 监控 EMQX 集群的负载情况。

   ![Rebalance MQTT Connections](https://assets.emqx.com/images/c86d6232261c42b3a8c9aa9bb5403315.png)

   从图中可以看出，当前集群中有四个 EMQX 节点，其中三个节点的连接数总计 10,000 个，剩下一个节点的连接数是 0。接下来，我们将演示如何进行重平衡操作，让四个节点的负载达到均衡。

2. 将以下内容保存为 YAML 文件，然后使用 kubectl apply 命令进行部署

   ```
   apiVersion: apps.emqx.io/v1beta4
   kind: Rebalance
   metadata:
      name: test-0
   spec:
      instanceName: emqx-ee
      instanceKind: EmqxEnterprise
      rebalanceStrategy:
        connEvictRate: 10
        sessEvictRate: 10
        waitTakeover: 10
        waitHealthCheck: 10
        absConnThreshold: 100
        absSessThreshold: 100
        relConnThreshold: "1.1"
        relSessThreshold: "1.1"
   ```

   有关 Rebalance 的配置，请参阅[文档](https://file+.vscode-resource.vscode-cdn.net/Users/raoxiaoli/reference/v1beta4-reference.md#rebalancestrategy)。

3. 执行以下命令查看 EMQX 群集的重平衡状态

   ```
   $ kubectl get rebalances rebalance-sample -o json | jq '.status.rebalanceStates'
   {
    "state": "wait_health_check",
    "session_eviction_rate": 10,
    "recipients":[
        "emqx-ee@emqx-ee-3.emqx-ee-headless.default.svc.cluster.local",
    ],
    "node": "emqx-ee@emqx-ee-0.emqx-ee-headless.default.svc.cluster.local",
    "donors":[
        "emqx-ee@emqx-ee-0.emqx-ee-headless.default.svc.cluster.local",
        "emqx-ee@emqx-ee-1.emqx-ee-headless.default.svc.cluster.local",
        "emqx-ee@emqx-ee-2.emqx-ee-headless.default.svc.cluster.local"
    ],
    "coordinator_node": "emqx-ee@emqx-ee-0.emqx-ee-headless.default.svc.cluster.local",
    "connection_eviction_rate": 10
   }
   ```

4. 等待重平衡任务完成

   ```
   $ kubectl get rebalances rebalance-sample
   NAME               STATUS      AGE
   rebalance-sample   Completed   62s
   ```

   重平衡有三种状态： 处理中、完成和失败

   1. 处理中：表示重平衡任务正在执行。
   2. 完成：表示重平衡任务已经完成。
   3. 失败：表示重平衡任务失败了。

5. 集群负载（重平衡后）

   ![Cluster load (after rebalancing)](https://assets.emqx.com/images/70180f7da40d983fd10bb1c8bb606b9e.png)

   图中展示了集群在重新平衡后的负载状况。从图中可以明显看出，重平衡的过程非常平稳。集群的总连接数没有变化，仍然是 10,000 个，和重平衡之前相同。四个节点的连接数有所调整，其中三个节点的一部分连接转移到了第四个节点上。重平衡完成后，四个节点的负载均匀稳定，每个节点的连接数大约是 2,500 个，将不会再发生波动。

   ```
   avg(source node connection number) < avg(target node connection number) + abs_conn_threshold
   或者
   avg(source node connection number) < avg(target node connection number) * rel_conn_threshold
   ```

   根据配置的重平衡参数和连接数，可以得出 `avg(2553 + 2553+ 2554) < 2340 * 1.1`，这说明集群负载已经平衡，重平衡任务有效地调整了集群负载。

## 结语

重新平衡 MQTT 连接是一种有效的管理分布式系统中 MQTT 连接的方法，可以实现 MQTT 连接的负载均衡，保证 MQTT 会话的持续性。如果您使用 EMQX 集群，建议您在集群扩容或节点重启后重新平衡 MQTT 连接，以达到更优化的集群状态。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
