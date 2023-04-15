随着 Kubernetes（K8s）的全面成熟，越来越多的组织开始大规模地基于 K8s 构建基础设施层。

根据 Sysdig 在容器编排领域的调研报告，K8s 在市场上的占有率高达 75%。在 K8s 部署运维工具中，Operator 和 Helm 是较为主流的两种。但由于 Helm 缺少对生命周期的管理，所以 Operator 在全生命期的管理中成为了唯一的选择。

K8s Operator 是一种特定于应用的控制器，能持续监听 K8s 资源对象的变化事件，进行全生命期的监控响应，高可靠地完成部署交付。Operator 提供了一个框架，通俗来说就是把运维的经验沉淀为代码，实现运维的代码化、自动化、智能化。

为了对云原生分布式 [MQTT 消息服务器 EMQX](https://www.emqx.com/zh/products/emqx) 进行全生命期管理， [EMQX Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 应运而生。 使用 EMQX Operator，即使在网络和存储环境复杂的 K8s 环境中，也可以轻松搭建百万连接的 MQTT 集群。本文将使用 EMQX Operator 进行基于 K8s 的百万级 MQTT 连接服务搭建，并通过测试验证搭建结果。

## 什么是 EMQX Operator

[EMQX](https://www.emqx.com/zh/products/emqx) 是基于 Erlang/OTP 平台开发的云原生分布式 MQTT 消息服务器。随着云原生理念的深入，以及 K8s 和 Operator 概念的普及，我们开发了 [EMQX Operator](https://github.com/emqx/emqx-operator)，它可以在 Kubernetes 的环境上快速创建和管理 EMQX 集群，实现对 EMQX 生命周期的管理，大大简化部署和管理 EMQX 集群的流程。其主要有以下功能优势:

- 降低 EMQX 在 K8s 环境中部署成本
- 提供对持久化数据备份和恢复的基础能力
- 提供对 EMQX Plugin 独立部署、管理、配置持久化的能力（即将支持）
- 动态更新 Licence 和 SSL 等
- 自动化运维（高可用、扩容、异常处理）

## 使用 EMQX Operator 搭建基于 K8s 的百万级 MQTT 集群

### 内核参数调优

为了发挥 EMQX 的最大性能，我们在 worker node 节点上调整了内核参数。

> sudo vi /etc/sysctl.conf

```
#!/bin/bash
echo "DefaultLimitNOFILE=100000000" >> /etc/systemd/system.conf
echo "session required pam_limits.so" >> /etc/pam.d/common-session
echo "*      soft    nofile      10000000"  >> /etc/security/limits.conf
echo "*      hard    nofile      100000000"  >> /etc/security/limits.conf

# lsmod |grep -q conntrack || modprobe ip_conntrack

cat >> /etc/sysctl.d/99-sysctl.conf <<EOF
net.ipv4.tcp_tw_reuse=1
fs.nr_open=1000000000
fs.file-max=1000000000
net.ipv4.ip_local_port_range=1025 65534
net.ipv4.udp_mem=74583000 499445000 749166000

net.core.somaxconn=32768
net.ipv4.tcp_max_sync_backlog=163840
net.core.netdev_max_backlog=163840

net.core.optmem_max=16777216
net.ipv4.tcp_rmem=1024 4096 16777216
net.ipv4.tcp_wmem=1024 4096 16777216
net.ipv4.tcp_max_tw_buckets=1048576
net.ipv4.tcp_fin_timeout=15
net.core.rmem_default=262144000
net.core.wmem_default=262144000
net.core.rmem_max=262144000
net.core.wmem_max=262144000
net.ipv4.tcp_mem=378150000  504200000  756300000

# net.netfilter.nf_conntrack_max=1000000
# net.netfilter.nf_conntrack_tcp_timeout_time_wait=30
EOF

sysctl -p
```

### 部署安装

部署 5 个 EMQX Pod

1. 安装 Cert Manager 依赖

   ```
   $ kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.8.0/cert-manager.yaml
   ```

2. 安装 EMQX Operator

   ```
   $ helm repo add emqx https://repos.emqx.io/charts
   $ helm repo update
   $ helm install emqx-operator emqx/emqx-operator \
      --set installCRDs=true \
      --namespace emqx-operator-system \
      --create-namespace
   ```

3. 检查 EMQX Operator 控制器状态

   ```
   $ kubectl get pods -l "control-plane=controller-manager" -n emqx-operator-system
   NAME                                                READY   STATUS    RESTARTS   AGE
   emqx-operator-controller-manager-68b866c8bf-kd4g6   1/1     Running   0          15s
   ```

4. 部署 EMQX

   ```
   cat << "EOF" | kubectl apply -f -
   apiVersion: apps.emqx.io/v1beta2
   kind: EmqxEnterprise
   metadata:
     name: emqx-ee
     labels:
       cluster: emqx
   spec:
     image: emqx/emqx-ee:4.4.1
     env:
       - name: "EMQX_NODE__DIST_BUFFER_SIZE"
         value: "16MB"
       - name: "EMQX_NODE__PROCESS_LIMIT"
         value: "2097152"
       - name: "EMQX_NODE__MAX_PORTS"
         value: "1048576"
       - name: "EMQX_LISTENER__TCP__EXTERNAL__ACCEPTORS"
         value: "64"
       - name: "EMQX_LISTENER__TCP__EXTERNAL__BACKLOG"
         value: "1024000"
       - name: "EMQX_LISTENER__TCP__EXTERNAL__MAX_CONNECTIONS"
         value: "1024000"
       - name: "EMQX_LISTENER__TCP__EXTERNAL__MAX_CONN_RATE"
         value: "100000"
     emqxTemplate:
       license: "your license string"
       listener:
         type: LoadBalancer
         annotations:
           service.beta.kubernetes.io/alibaba-cloud-loadbalancer-address-type: "intranet"
           service.beta.kubernetes.io/alibaba-cloud-loadbalancer-spec: "slb.s3.large"
   EOF
   ```

5. 查看 EMQX 部署状态

   ```
   $ kubectl get pods 
   ```

EMQX 集群由 5 个 Pod 组成，每个 Pod 的资源限额如下：

```
$ kubectl get emqx-ee emqx-ee -o json | jq ".spec.replicas"
5
$ kubectl get emqx-ee emqx-ee -o json | jq ".spec.resources"
{
  "limits": {
    "cpu": "20",
    "memory": "20Gi"
  },
  "requests": {
    "cpu": "4",
    "memory": "4Gi"
  }
}
```

## 搭建结果验证

### 测试环境

本次测试使用阿里云 ACK 专有服务，网络插件为 Flannel，使用 3 台规格为 ecs.c7.2xlarge、操作系统为 centos7.9 的实例作为 master 节点，5 台规格为 ecs.c7.16xlarge、操作系统为 centos7.9 的实例作为 worker node 节点，测试工具使用 XMeter，压力机与 ACK 的负载均衡在同一个 VPC 网络中。

### 测试场景

1. 100 万个客户端使用 MQTT 5.0 协议连接 EMQX
2. publish 客户端和 subscribe 客户端各 500k
3. 每个 publish 客户端每秒发布一条 QoS 1、payload size 1k 的消息
4. 相应的每个 subscribe 客户端每秒消费一条消息

### 测试结果

如下图 EMQX Enterprise Dashboard 监控显示，本次测试被测集群共 5 个 worker 节点，集群接入量实际达到 1M 连接和 500k 订阅，消息流入(发布)消息流出(消费)都达到了每秒 50 万：

![MQTT Dashboard](https://assets.emqx.com/images/13e1800309956fb5f3ab33aff02cf708.png)

消息吞吐期间 EMQX Enterprise Pods 的资源消耗如下：

![EMQX Enterprise Pods 的资源消耗](https://assets.emqx.com/images/ed135d55d4eef23211e13d6a2ae2bdc7.png) 

XMeter 测试工具结果详情如下：

![XMeter 测试工具结果](https://assets.emqx.com/images/a3a460fb17de1f832ef9851f4c826e6e.png)

## 结语

通过上文的验证，我们可以看到基于 [EMQX Operator](https://github.com/emqx/emqx-operator) 在 K8s 部署的 EMQX 集群可以轻松处理百万 MQTT 连接。随着 K8s 的普及，将会有更多的用户选择 Operator 在 K8s 上部署和运维云原生应用。EMQ 将持续优化 EMQX Operator，帮助用户简化部署和管理 EMQX 集群的流程，在云原生时代充分享受云带来的便利，发掘 EMQX 为物联网实时数据移动、处理和集成带来的强大能力。


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
