云进入以「应用为中心」的云原生阶段，Operator 模式的出现，则为 Kubernetes 中的自动化任务创建配置与管理提供了一套行之有效的标准规范。通过将运维知识固化成高级语言 Go/Java 代码，使得运维知识可以像普通软件一样交付，并能支持高可靠、具备高级运维能力的有状态应用批量交付。

针对大规模分布式物联网 MQTT 消息服务器 EMQX 全生命期管理的自动化管理工具 EMQX Kubernetes Operator（本文中简称 EMQX Operator）应运而生。它作为 Kubernetes 上的自定义控制器运行，并与 Kubernetes API 服务器(kube-apiserver)进行通信，将高层描述转换为正常的 Kubernetes 资源，以保持所需的应用程序状态。

EMQX Operator 使 EMQX 的部署、调优和运维变成一种低成本、标准化、可重复性的能力，帮助用户高效实现集群扩容、无缝升级、故障处理和统一监控。

![部署 MQTT 集群](https://assets.emqx.com/images/08fc9081538630861caa91675ab9f579.png)

本文章将以 EMQX 企业版为例，详细讲解如何使用 EMQX Operator 在腾讯云 TKE 公有云平台上创建部署 MQTT 服务集群，并实现自动化管理与监控。

 
## 云平台简介：腾讯云 TKE

TKE：腾讯云容器服务（Tencent Kubernetes Engine，TKE）基于原生 kubernetes 提供以容器为核心的、高度可扩展的高性能容器管理服务。腾讯云容器服务完全兼容原生 kubernetes API ，扩展了腾讯云的云硬盘、负载均衡等 kubernetes 插件，为容器化的应用提供高效部署、资源调度、服务发现和动态伸缩等一系列完整功能，解决用户开发、测试及运维过程的环境一致性问题，提高了大规模容器集群管理的便捷性，帮助用户降低成本，提高效率。

 
## 创建 TKE 集群

### 创建 Kubernetes 群集

登录腾讯云, 选择云产品 -> 容器服务，点击创建， 选择标准集群，EMQX Operator 要求 Kubernetes 版本>=1.20.0，因此我们在此选择 Kubernetes 选择 1.22.5 ,网络与其他资源信息根据自身需求来制定。具体创建步骤参考： [创建标准集群](https://cloud.tencent.com/document/product/457/32189)

### 访问 Kubernetes 集群

![访问 Kubernetes 集群](https://assets.emqx.com/images/7e43db7341480071cec1ab09b6e9d95a.png)

集群创建完成之后，在基本信息页面开启外网访问或者内网访问，即会生成 kubeconfig 文件，可以使用kubectl 和 kubeconfig 文件访问集群。

 
## LoadBalancer 配置

非直连模式下 CLB 和 Service 存在两层 CLB，性能有一定损失，开启 CLB 直连 pod 可以提升请求转发性能，需要在 Service 的 annotations 里面添加以下注解： [直连模式配置说明](https://cloud.tencent.com/document/product/457/41897)

```
service.cloud.tencent.com/direct-access: "true" 
```

**备注**: 开启直连模式需要在 kube-system/tke-service-controller-config ConfigMap 中新增 GlobalRouteDirectAccess: "true" 以开启 GlobalRoute 直连能力。


## 创建 StorageClass

点击集群名称进入集群详情页面，点击存储 -> StorageClass 创建需要的StorageClass, 具体步骤参考：[创建StorageClass](https://console.cloud.tencent.com/tke2/cluster/sub/create/storage/sc?rid=16&clusterId=cls-mm0it4nz)

 
## 使用 EMQX Operator 部署 EMQX 集群

### 部署 cert-manager

参考 cert-manager安装文档：[![img](https://cert-manager.io/favicons/favicon-16x16.png)Installation](https://cert-manager.io/docs/installation/)

### 部署 EMQX Operator

```
kubectl apply -f "https://github.com/emqx/emqx-operator/releases/download/1.2.6/emqx-operator-controller.yaml"
```

### 部署 EMQX 企业版集群

这里 service type 采用 LoadBalancer

```
cat << EOF | kubectl apply -f -
apiVersion: apps.emqx.io/v1beta3
kind: EmqxEnterprise
metadata:
  name: emqx-ee
  labels:
    "apps.emqx.io/instance": "emqx-ee"
  annotations:
    service.cloud.tencent.com/direct-access: "true" ##开启 CLB 直连 Pod
spec:
  emqxTemplate:
    image: emqx/emqx-ee:4.4.6
    serviceTemplate:
      metadata:
        name: emqx-ee
        namespace: default
        labels:
          "apps.emqx.io/instance": "emqx-ee"
      spec:
        type: LoadBalancer
        selector:
          "apps.emqx.io/instance": "emqx-ee"
  persistent:
    accessModes: 
      - ReadWriteOnce
    resources:
        requests:
          storage: 10Gi 
    storageClassName: emqx-test
EOF
``` 

### 查看集群状态

```
$ kubectl get pods  
NAME              READY   STATUS    RESTARTS   AGE  
emqx-ee-0   2/2     Running   0          22m  
emqx-ee-1   2/2     Running   0          22m  
emqx-ee-2   2/2     Running   0          22m  

$ kubectl exec -it emqx-ee-0 -c emqx -- emqx_ctl status  
Node 'emqx-ee@emqx-ee-0.emqx-ee-headless.default.svc.cluster.local' 4.4.6 is started  

$ kubectl exec -it emqx-ee-0 -c emqx -- emqx_ctl cluster status  
Cluster status: #{running_nodes =>
                   ['emqx-ee@emqx-ee-0.emqx-ee-headless.default.svc.cluster.local',
                    'emqx-ee@emqx-ee-1.emqx-ee-headless.default.svc.cluster.local',
                    'emqx-ee@emqx-ee-2.emqx-ee-headless.default.svc.cluster.local'],
               stopped_nodes => []}
```

EMQX Operator 和 EMQX 集群安装参考: [https://github.com/emqx/emqx-operator/blob/main/docs/en_US/getting-started/getting-started.md](https://github.com/emqx/emqx-operator/blob/main/docs/en_US/getting-started/getting-started.md)

 
## 使用 LB 终结 TCP mTLS 方案

目前腾讯云 CLB 支持 终结 TCP TLS ，如需要使用 LB 终结 TCP mTLS 请参考这篇文档：[LB 终结 TCP mTLS 方案](https://github.com/emqx/emqx-operator/discussions/312)

> **备注**： 此文档详细解释了使用 EMQX Operator 在腾讯云 TKE 上部署 EMQX 集群的步骤，另外还支持配置 LB 直连 Pod，进一步提升转发性能。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
