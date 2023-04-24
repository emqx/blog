云进入以「应用为中心」的云原生阶段，Operator 模式的出现，则为 Kubernetes 中的自动化任务创建配置与管理提供了一套行之有效的标准规范。通过将运维知识固化成高级语言 Go/Java 代码，使得运维知识可以像普通软件一样交付，并能支持高可靠、具备高级运维能力的有状态应用批量交付。

针对大规模分布式物联网 MQTT 消息服务器 EMQX 全生命期管理的自动化管理工具 EMQX Kubernetes Operator（本文中简称 EMQX Operator）应运而生。它作为 Kubernetes 上的自定义控制器运行，并与 Kubernetes API 服务器(kube-apiserver)进行通信，将高层描述转换为正常的 Kubernetes 资源，以保持所需的应用程序状态。

EMQX Operator 使 EMQX 的部署、调优和运维变成一种低成本、标准化、可重复性的能力，帮助用户高效实现集群扩容、无缝升级、故障处理和统一监控。

![部署 MQTT 集群](https://assets.emqx.com/images/4d7529046f45b32e0b2d374ba1a13965.png)

本文章将以 EMQX 企业版为例，详细讲解如何使用 EMQX Operator 在 Azure AKS 公有云平台上创建部署 MQTT 服务集群，并实现自动化管理与监控。


## 云平台简介：Azure AKS

AKS: Azure Kubernetes 服务 (AKS) 通过将操作开销卸载到 Azure，简化了在 Azure 中部署托管 Kubernetes 群集的过程。 作为一个托管的 Kubernetes 服务，Azure 可以自动处理运行状况监视和维护等关键任务。 由于 Kubernetes 主节点由 Azure 管理，因此你只需要管理和维护代理节点。详见：[Introduction to Azure Kubernetes Service - Azure Kubernetes Service](https://learn.microsoft.com/en-us/azure/aks/intro-kubernetes)

## 创建 AKS 集群

### 创建 Kubernetes 群集

登录Azure Kubernetes 服务，选择创建 Kubernetes 集群，注意EMQX Operator 要求Kubernetes 版本>=1.20.0 

![创建 Kubernetes 群集](https://assets.emqx.com/images/a85cca3c6cebf3939d672e7e2e00843a.png)

其他根据需要配置

![创建 Kubernetes 群集 2](https://assets.emqx.com/images/814e9325366fd5785ee71202242bc15c.png)

点击创建，完成创建 Kubernetes 集群

细节请参考：[Quickstart: Deploy an AKS cluster by using the Azure portal - Azure Kubernetes Service](https://learn.microsoft.com/en-us/azure/aks/learn/quick-kubernetes-deploy-portal?tabs=azure-cli)


## 访问 Kubernetes 集群

建议通过 Azure 提供的 Cloud Shell 连接

![访问 Kubernetes 集群](https://assets.emqx.com/images/b893e36b4a755de1d7fb2ad577173102.png)

细节请参考：[Azure Cloud Shell overview](https://learn.microsoft.com/en-us/azure/cloud-shell/overview)


## StorageClass 配置

这里采用 NSF 文件存储。其他 StorageClass 可参考：[Use Container Storage Interface (CSI) driver for Azure Files on Azure Kubernetes Service (AKS) - Azure Kubernetes Service](https://learn.microsoft.com/en-us/azure/aks/azure-files-csi)

创建 StroageClass

```
cat << "EOF" | kubectl apply -f -
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azurefile-csi-nfs
provisioner: file.csi.azure.com
allowVolumeExpansion: true
parameters:
  protocol: nfs
mountOptions:
  - nconnect=8
EOF

```

查看该 StroageClass 是否创建成功

```
kubectl get sc
```

![查看该 StroageClass 是否创建成功](https://assets.emqx.com/images/67b2d728372932e63e2b6ca0e6577478.png)

 
## 使用 EMQX Operator 部署 EMQX 集群

### 部署 cert-manager

参考cert-manager安装文档：[https://cert-manager.io/docs/installation/](https://cert-manager.io/docs/installation/) 

### 部署 EMQX Operator

```
kubectl apply -f "https://github.com/emqx/emqx-operator/releases/download/1.2.6/emqx-operator-controller.yaml"
```

### 部署 EMQX 企业版集群

这里 service type采用`LoadBalancer`

```
cat << "EOF" | kubectl apply -f -
apiVersion: apps.emqx.io/v1beta3
kind: EmqxEnterprise
metadata:
  name: emqx-ee
  labels:
    "foo": "bar"
spec:
  replicas: 3
  persistent:
     storageClassName: azurefile-csi-nfs
     resources:
       requests:
         storage: 4Gi
     accessModes:
     - ReadWriteOnce
  emqxTemplate:
    image: emqx/emqx-ee:4.4.6
    serviceTemplate:
      spec:
        type: LoadBalancer
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
Node 'emqx-ee@emqx-ee-0.emqx-ee-headless.default.svc.cluster.local' 4.4.7 is started  

$ kubectl exec -it emqx-ee-0 -c emqx -- emqx_ctl cluster status  
Cluster status: #{running_nodes =>
                   ['emqx-ee@emqx-ee-0.emqx-ee-headless.default.svc.cluster.local',
                    'emqx-ee@emqx-ee-1.emqx-ee-headless.default.svc.cluster.local',
                    'emqx-ee@emqx-ee-2.emqx-ee-headless.default.svc.cluster.local'],
               stopped_nodes => []}
```

EMQX Operator 和 EMQX 集群安装参考: [https://github.com/emqx/emqx-operator/blob/main/docs/en_US/getting-started/getting-started.md](https://github.com/emqx/emqx-operator/blob/main/docs/en_US/getting-started/getting-started.md)


## 关于 LoadBalancer 终结 TLS

由于 Azure LoadBalancer 不支持 TCP 证书，所以请参考这篇文档解决 TCP 证书终结问题：[https://github.com/emqx/emqx-operator/discussions/312](https://github.com/emqx/emqx-operator/discussions/312)


## 结语

至此，我们完成了在 Azure AKS 上部署 EMQX 集群的全部流程。EMQX Operator 可以帮助用户在 Kubernetes 环境上快速创建和管理 EMQX 集群，不仅极大简化部署和管理流程，也降低了管理和配置的专业技能要求，是用户快速体验云原生的最佳选择。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
