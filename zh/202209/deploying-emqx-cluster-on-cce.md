云进入以「应用为中心」的云原生阶段，Operator 模式的出现，则为 Kubernetes 中的自动化任务创建配置与管理提供了一套行之有效的标准规范。通过将运维知识固化成高级语言 Go/Java 代码，使得运维知识可以像普通软件一样交付，并能支持高可靠、具备高级运维能力的有状态应用批量交付。

针对大规模分布式物联网 MQTT 消息服务器 EMQX 全生命期管理的自动化管理工具 EMQX Kubernetes Operator（本文中简称 EMQX Operator）应运而生。它作为 Kubernetes 上的自定义控制器运行，并与 Kubernetes API 服务器（kube-apiserver）进行通信，将高层描述转换为正常的 Kubernetes 资源，以保持所需的应用程序状态。

EMQX Operator 使 EMQX 的部署、调优和运维变成一种低成本、标准化、可重复性的能力，帮助用户高效实现集群扩容、无缝升级、故障处理和统一监控。

![EMQX Operator 集群](https://assets.emqx.com/images/61cf8997f1d54aff1cb0d012fda4e34b.png)

本文章将以 [EMQX 企业版](https://www.emqx.com/zh/products/emqx)为例，详细讲解如何使用 [EMQX Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 在华为云 CCE 公有云平台上创建部署 MQTT 服务集群，并实现自动化管理与监控。

## 云平台简介：华为云 CCE

云容器引擎（Cloud Container Engine，简称CCE）提供高度可扩展的、高性能的企业级 Kubernetes 集群，支持运行 Docker 容器。借助云容器引擎，您可以在华为云上轻松部署、管理和扩展容器化应用程序，详见：[成长地图_云容器引擎 CCE_华为云](https://support.huaweicloud.com/cce/index.html) 

## 创建 CCE 集群

### 购买 CCE 集群

登录华为云 CCE控制台，购买“Turbo 集群”或者“CCE 集群”，EMQX Operator 要求Kubernetes 版本>=1.20.0 ，因此我们在此选择 Kubernetes 1.21，网络与其他资源信息根据自身需求来制定。

![购买 CCE 集群](https://assets.emqx.com/images/09b17b409cc9deb46b494cb4d05a02f7.png)

### 创建节点池（直接添加节点也可以）

![创建节点池](https://assets.emqx.com/images/783acd713e1289fff48c479e98e7f0f5.png)

这里添加的节点必须可以访问外网（可以通过加 NAT 网关解决）

节点安装的操作系统建议是 Ubuntu，否则有可能会缺少必要的库（socat）

![节点选择 Ubuntu](https://assets.emqx.com/images/6d2c7e6ccb04646d609c019213acd4f5.png)

细节请参考：[快速创建Kubernetes集群_云容器引擎 CCE_快速入门_华为云](https://support.huaweicloud.com/qs-cce/cce_qs_0008.html?utm_source=cce_Growth_map&utm_medium=display&utm_campaign=help_center&utm_content=Growth_map) 

## 访问 Kubernetes 集群

点击 Cloud Shell

![Cloud Shell](https://assets.emqx.com/images/4766a249b1df9477ce99be803ebe1b5f.png)

详情参考：[通过 kubectl 连接集群_云容器引擎 CCE_用户指南_集群管理_旧版UI_访问集群_华为云](https://support.huaweicloud.com/usermanual-cce/cce_01_0107.html) 

## StorageClass 配置

查看当前的 StroageClass

```
kubectl get sc
```

![查看当前的 StroageClass](https://assets.emqx.com/images/8c66fe787c19b325e2ccbda4da660972.png)


这里我们用 csi-disk，其他 StorageClass 可参考：[存储类StorageClass_云容器引擎 CCE_用户指南_新版UI_存储管理-CSI_华为云](https://support.huaweicloud.com/usermanual-cce/cce_10_0380.html) 

## 使用 EMQX Operator 部署 EMQX 集群

### 部署 cert-manager

参考 cert-manager 安装文档：[https://cert-manager.io/docs/installation/](https://cert-manager.io/docs/installation/) 

### 部署 EMQX Operator

```
kubectl apply -f "https://github.com/emqx/emqx-operator/releases/download/1.2.6/emqx-operator-controller.yaml"
```

### 部署 EMQX 企业版集群

这里 service type 采用 `LoadBalancer`

```
cat << "EOF" | kubectl apply -f -
apiVersion: apps.emqx.io/v1beta3
kind: EmqxEnterprise
metadata:
  name: emqx-ee
  labels:
    "foo": "bar"
spec:
  persistent:
    storageClassName: csi-disk
    resources:
      requests:
        storage: 1Gi
    accessModes:
    - ReadWriteOnce
  emqxTemplate:
    image: emqx/emqx-ee:4.4.6
    serviceTemplate:
      metadata:
        annotations:
          kubernetes.io/elb.pass-through: "true"
          kubernetes.io/elb.class: union
          kubernetes.io/elb.autocreate:
              '{
                "type": "public",
                "name": "emqx",
                "bandwidth_name": "cce-emqx",
                "bandwidth_chargemode": "bandwidth",
                "bandwidth_size": 5,
                "bandwidth_sharetype": "PER",
                "eip_type": "5_bgp"
              }'
      spec:
        type: LoadBalancer
EOF
```

**Load Balancer参数说明**

- bandwidth_chargemode

  >带宽付费模式。
  >bandwidth：按带宽计费
  >traffic：按流量计费
  >默认类型：bandwidth

- bandwidth_size

  > 带宽大小，默认 1Mbit/s~2000Mbit/s，请根据 Region 带宽支持范围设置。

- bandwidth_sharetype

  > 带宽共享方式。
  > PER：独享带宽

- eip_type

  > 弹性公网IP类型
  > 5_telcom：电信
  > 5_union：联通
  > 5_bgp：全动态BGP
  > 5_sbgp：静态BGP

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

annotations 的说明参考：[通过Kubectl命令行添加ELB Ingress_云容器引擎 CCE_用户指南_新版UI_网络管理_Ingress_华为云](https://support.huaweicloud.com/usermanual-cce/cce_10_0252.html) 

## 关于 LoadBalancer 终结 TLS

由于华为 ELB 不支持 TCP 证书，所以请参考这篇文档解决 TCP 证书终结问题：[https://github.com/emqx/emqx-operator/discussions/312](https://github.com/emqx/emqx-operator/discussions/312) 

## 结语

至此，我们完成了在华为云 CCE 上部署 EMQX 集群的全部流程。EMQX Operator 可以帮助用户在 Kubernetes 环境上快速创建和管理 EMQX 集群，不仅极大简化部署和管理流程，也降低了管理和配置的专业技能要求，是用户快速体验云原生的最佳选择。


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
