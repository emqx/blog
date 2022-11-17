云进入以「应用为中心」的云原生阶段，Operator 模式的出现，则为 Kubernetes 中的自动化任务创建配置与管理提供了一套行之有效的标准规范。通过将运维知识固化成高级语言 Go/Java 代码，使得运维知识可以像普通软件一样交付，并能支持高可靠、具备高级运维能力的有状态应用批量交付。

针对大规模分布式物联网 MQTT 消息服务器 EMQX 全生命期管理的自动化管理工具 EMQX Kubernetes Operator（本文中简称 EMQX Operator）应运而生。它作为 Kubernetes 上的自定义控制器运行，并与 Kubernetes API 服务器(kube-apiserver)进行通信，将高层描述转换为正常的 Kubernetes 资源，以保持所需的应用程序状态。

EMQX Operator 使 EMQX 的部署、调优和运维变成一种低成本、标准化、可重复性的能力，帮助用户高效实现集群扩容、无缝升级、故障处理和统一监控。

![MQTT 集群](https://assets.emqx.com/images/a96cd1e651c42a6bb136089e2cf53f5b.png)

本文章将以 EMQX 企业版为例，详细讲解如何使用 EMQX Operator 在阿里云 ACK 公有云平台上创建部署 MQTT 服务集群，并实现自动化管理与监控。


## 云平台简介：阿里云 ACK

ACK：容器服务 Kubernetes 版（简称 ACK）提供高性能可伸缩的容器应用管理能力，支持企业级容器化应用的全生命周期管理；其整合了阿里云虚拟化、存储、网络和安全能力，助力企业高效运行云端 Kubernetes容器化应用。详见：[什么是容器服务Kubernetes版](https://help.aliyun.com/document_detail/86737.html?spm=5176.181001.J_5253785160.4.69c04e26ijwe5I)

 

## 创建 ACK 集群

### 创建 Kubernetes 群集

登录阿里云 容器服务-Kubernetes，选择创建集群，注意 EMQX Operator 要求 Kubernetes 版本>=1.20.0 

![创建 Kubernetes 群集](https://assets.emqx.com/images/f225e6e12624ceabdb1c1f31abf2e24e.png)

根据需要选择合适的配置

![根据需要选择合适的配置](https://assets.emqx.com/images/9c1bdc79c30feabf8a62ceadf886f04b.png)

细节参考： [创建Kubernetes托管版集群](https://www.alibabacloud.com/help/zh/container-service-for-kubernetes/latest/create-an-ack-managed-cluster)

### 访问 Kubernetes 群集

![Kubernetes 群集](https://assets.emqx.com/images/53aa602c7298767f3bcb327d0a7badda.png)

集群创建完成之后，在连接信息页面有 kubeconfig 文件信息，可以使用 kubectl 和 kubeconfig 文件访问集群。


## LoadBalancer 配置

支持在 Terway 网络模式下，通过 annotation 将 Pod 直接挂载到 CLB 后端，提升网络转发性能。[通过Annotation配置负载均衡](https://www.alibabacloud.com/help/zh/container-service-for-kubernetes/latest/use-annotations-to-configure-load-balancing-1)

```
service.beta.kubernetes.io/backend-type："eni"
```

 
## StorageClass 配置

使用如下命令查看当前集群可用的 storageClass：

```
kubectl get sc
```

可以看到集群默认创建了多个可用的 storageClass, 本文档部署 EMQX 时选取的第一个 storageClass: alibabacloud-cnfs-nas，其他 StorageClass 可参考文档 [存储-CSI](https://help.aliyun.com/document_detail/127551.html)

 
## 使用 EMQX Operator 部署 EMQX 集群

### 部署 cert-manager

参考 cert-manager 安装文档：[![img](https://cert-manager.io/favicons/favicon-16x16.png)Installation](https://cert-manager.io/docs/installation/)

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
    service.beta.kubernetes.io/backend-type："eni"
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
    storageClassName: alibabacloud-cnfs-nas
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

 

## LoadBalancer 终结 TLS

由于阿里云 CLB 不支持 TCP 证书（NLB发布后，我们会更该该项内容），所以请参考这篇文档解决 TCP 证书终结问题：[LB 终结 mTLS 方案](https://github.com/emqx/emqx-operator/discussions/312)

> **备注**： 此文档详细解释了使用 EMQX Operator 在阿里云 ACK 上部署 EMQX 集群的步骤，另外还支持配置 LB 直连 Pod，进一步提升转发性能。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
