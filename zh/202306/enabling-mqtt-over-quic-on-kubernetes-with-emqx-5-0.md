## 引言

作为全球领先的开源分布式 [MQTT Broker，EMQX](https://www.emqx.io/zh) 在 5.0 版本中引入了 [MQTT over QUIC](https://www.emqx.com/zh/blog/getting-started-with-mqtt-over-quic-from-scratch)，将 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 协议的优势与 [QUIC](https://www.emqx.com/zh/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov) 的特性相结合。通过充分利用 QUIC 协议低连接开销和多路复用的特点，MQTT over QUIC 为弱网络环境和不规则网络中的用户提供了一种非常有前景的解决方案。它能够应对诸如在山区或隧道等恶劣环境中运行的网联车辆等物联网场景中的连接中断和连接建立缓慢等问题。云原生技术的发展，让越来越多的用户选择在 Kubernetes 上部署 EMQX 集群，享受快速创建和便捷管理的优势。本文将介绍如何在 Kubernetes 上部署 EMQX 集群并开启 MQTT over QUIC 功能。

## 暴露 EMQX 服务

在 Kubernetes 上部署 EMQX 时，您可以使用 `LoadBalancer` 或 `NodePort` 将 EMQX 服务对集群外的客户端暴露。

- `LoadBalancer` 方式依赖云服务商提供的负载均衡器来提供服务。目前，云服务商的负载均衡器不支持 QUIC 的地址迁移特性。
- `NodePort` 方式依赖于 Kubernetes 的 [kube-proxy](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/) 组件来转发外部请求，它可以无缝连接到 EMQX 服务，并支持 QUIC 地址迁移特性。

在车联网场景中，车端的地址可能会频繁变化，QUIC 的地址迁移特性就显得非常重要。因此，在 Kubernetes 上部署具有 MQTT over QUIC 功能的 EMQX 5.0 时，我们建议选择以 `NodePort` 方式对外暴露服务。

下面，我们将介绍在 Kubernetes 上部署 EMQX 5.0 并启用 MQTT over QUIC 的具体步骤。同时，我们将以 `NodePort` 方式对外暴露服务并验证 QUIC 的地址迁移功能。

## 前提条件

在将 EMQX 5.0 部署到 Kubernetes 之前，请确保满足以下要求：

- [Kubernetes](https://kubernetes.io/docs/concepts/overview/) 版本 >= 1.27

  >当 K8s 版本低于 1.27 时，由于 kube-proxy [IPVS break UDP NodePort Services](https://github.com/kubernetes/kubernetes/issues/113802) 的 bug 导致 UDP 数据包被丢弃。目前这个 bug 已经在 K8s 1.27 版本中被修复，详情请参考：[Syncing IPVS conntrack cleaning with IPTables](https://github.com/kubernetes/kubernetes/pull/116171)。若您的 K8s 集群版本低于 1.27，推荐使用 iptables 模式的 kube-proxy。

- [Helm](https://helm.sh/) 版本 >= 3

## 安装 EMQX Operator

1. 安装并启动 `cert-manager`。

   `cert-manager` 版本需要等于或高于 `1.1.6`。如果已经安装并启动了 `cert-manager`，请跳过此步骤。

   ```
   $ helm repo add jetstack https://charts.jetstack.io
   $ helm repo update
   $ helm upgrade --install cert-manager jetstack/cert-manager \
   --namespace cert-manager \
   --create-namespace \
   --set installCRDs=true
   ```

   您也可以参考 [cert-manager 安装指南](https://cert-manager.io/docs/installation/)来进行安装。

2. 使用 Helm 安装 EMQX Operator。

   ```
   $ helm repo add emqx https://repos.emqx.io/charts
   $ helm repo update
   $ helm install emqx-operator emqx/ emqx-operator --namespace emqx-operator-system --create-namespace
   ```

3. 等待 EMQX Operator 准备就绪。

   ```
   $ kubectl wait --for=condition=Ready pods -l "control-plane=controller-manager" -n emqx-operator-system
   
   # 如果您得到类似以下的输出结果，说明 emqx-operator 已经就绪：
   pod/emqx-operator-controller-manager-57bd7b8bd4-h2mcr condition met
   ```

## 部署 EMQX 5.0 并启用 MQTT over QUIC

1. 将以下内容保存为 YAML 文件，并使用 `kubectl apply` 命令进行部署。

   ```
   apiVersion: apps.emqx.io/v2alpha1
   kind: EMQX
   metadata:
   name: emqx
   spec:
   image: emqx:5.0
   bootstrapConfig: |
     listeners.quic.default {
       enabled = true
       bind = "0.0.0.0:14567"
       max_connections = 1024000
       keyfile = "/opt/emqx/etc/certs/key.pem"
       certfile = "/opt/emqx/etc/certs/cert.pem"
     }
   coreTemplate:
     spec:
       replicas: 3
   replicantTemplate:
     spec:
       replicas: 3
   listenersServiceTemplate:
     spec:
       type: NodePort
       ports:
         - name: quic-default
           protocol: UDP
           port: 14567
           targetPort: 14567
   ```

   `listeners.quic.default` 表示启用 QUIC 监听器并绑定 UDP `14567` 端口。

2. 等待 EMQX 集群准备就绪。您可以通过 `kubectl get` 命令查看 EMQX 集群的状态，请确保 `STATUS` 为 `Running`。这可能需要一些时间。

   ```
   $ kubectl get emqx
   NAME   IMAGE      STATUS    AGE
   emqx   emqx:5.0   Running   10m
   ```

3. 获取 EMQX 集群的监听器服务。

   EMQX Operator 将创建两个 EMQX Service 资源，分别为 `emqx-dashboard` 和 `emqx-listeners`，用于 EMQX 控制台和 EMQX 监听端口。

   ```
   $ kubectl get service emqx-listeners
   NAME             TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)                         AGE
   emqx-listeners   NodePort   192.168.50.64   <none>        14567:30171/UDP,1883:32633/TCP   2m1s
   ```

   您可以看到服务中启用了 QUIC 监听器。

## 使用 eMQTT-Bench 测试 QUIC

[eMQTT-Bench](https://github.com/emqx/emqtt-bench) 是一款用 Erlang 编写的轻量级 MQTT 5.0 基准测试工具。您可以从 [eMQTT-Bench 发布页面](https://github.com/emqx/emqtt-bench/releases)下载并安装适合您平台的支持 QUIC 协议的 eMQTT-Bench。

1. 使用 QUIC 协议建立连接，并通过指定 `--quic` 选项进行订阅。这里有 10 个客户端订阅了 `t/test` 主题。

   ```
   $ ./emqtt_bench sub --quic -h ${node_ip} -p ${node_port} -t t/test -c 10
   ```

2. 打开另一个终端，使用 QUIC 协议进行连接并执行发布测试。

   ```
   $ ./emqtt_bench pub --quic -h ${node_ip} -p ${node_port} -t t/test -c 1
   ```

   此时，您可以从命令行的输出日志中看到订阅者和发布者的消息订阅发布速率。

   ![订阅者和发布者的消息订阅发布速率](https://assets.emqx.com/images/a6d187493b4bafe9f353f99b010ad6a6.png)

3. 进行地址迁移测试。

   我们在图中箭头标记的时间点切换客户端网络，并观察 EMQX 集群发送和接收消息的情况：

   ![观察 EMQX 集群发送和接收消息的情况](https://assets.emqx.com/images/6bb1a933e1dbea73d22c78df8cc9e2cf.png)

   从上图可以看出，在客户端网络变化时，QUIC 对消息的接收和发送没有造成影响。同时，客户端发布和订阅消息也没有出现任何异常，如下图所示：

   ![QUIC 对消息的接收和发送没有造成影响](https://assets.emqx.com/images/664a3d614b513e0032071ad9f7d245d7.png)

## 在 Kubernetes 上使用 QUIC 的挑战

目前，在 Kubernetes 上使用 QUIC 协议存在的主要问题是云服务商提供的负载均衡器对 QUIC 协议支持不完善，如不支持 IETF QUIC 协议和 QUIC 地址迁移特性。

## 结语

以上就是在 Kubernetes 上使用 EMQX 5.0 体验 MQTT over QUIC 的全部过程。可以看出，在 Kubernetes 上部署 EMQX 5.0 非常简单，只需要一个 YAML 文件即可完成。启用 MQTT over QUIC 后，您的设备可以基于 QUIC 协议与 EMQX 集群进行通信，充分利用其在物联网消息传输方面的优势。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
