云进入以「应用为中心」的云原生阶段，Operator 模式的出现，则为 Kubernetes 中的自动化任务创建配置与管理提供了一套行之有效的标准规范。通过将运维知识固化成高级语言 Go/Java 代码，使得运维知识可以像普通软件一样交付，并能支持高可靠、具备高级运维能力的有状态应用批量交付。

针对大规模分布式物联网 MQTT 消息服务器 EMQX 全生命期管理的自动化管理工具 EMQX Kubernetes Operator（本文中简称 EMQX Operator）应运而生。它作为 Kubernetes 上的自定义控制器运行，并与 Kubernetes API 服务器（kube-apiserver）进行通信，将高层描述转换为正常的 Kubernetes 资源，以保持所需的应用程序状态。

EMQX Operator 使 EMQX 的部署、调优和运维变成一种低成本、标准化、可重复性的能力，帮助用户高效实现集群扩容、无缝升级、故障处理和统一监控。

![EMQX Operator 集群](https://assets.emqx.com/images/61cf8997f1d54aff1cb0d012fda4e34b.png?imageMogr2/thumbnail/1520x)

本文章将以 EMQX 企业版为例，详细讲解如何使用 EMQX Operator 在 AWS EKS 上创建部署 MQTT 服务集群，并实现自动化管理与监控。

## 云平台简介: AWS EKS

Amazon Elastic Kubernetes Service(Amazon EKS)是 AWS 的 Kubernetes 托管服务，您可以使用它来在AWS 上运行 Kubernetes，而无需安装、操作和维护您自己的 Kubernetes 控制平面或节点。详细介绍请参考: [https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html) 

### 创建 EKS 服务

使用 EKS 服务，需通过以下两个步骤进行创建。

#### 创建 EKS 集群

登录 EKS 控制台， 点击添加集群。由于  EMQX Operator 要求 Kubernetes 版本 >= 1.20, 因此在进行集群配置时，Kubernetes 版本大于 1.20 即可。其他角色、权限、子网、VPC 等可根据需求添加。

![创建 EKS 集群 1](https://assets.emqx.com/images/5b2afa3d191ad07c0aa26004c447d82a.png)

![创建 EKS 集群 2](https://assets.emqx.com/images/391a71d66f02092d7d5be6258a3c239b.png)

#### 添加节点组与节点

集群创建成功后，进入集群详细页面，点击计算，选择添加节点组。

![配置节点组](https://assets.emqx.com/images/75eccfe693e4a5e41957cba5f8a2be3e.png)

![添加节点组](https://assets.emqx.com/images/9083ae9f8a166d937d25bf8e7f57c8e5.png)

![选择实例](https://assets.emqx.com/images/c0f4800279880ec458f62d79eac7423b.png)

此处的实例类型根据业务需求自行调整，本文为示例选择了较小的实例规格。详细操作可以参考 AWS 官方文档: [https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html) 

## 访问 Kubernetes 集群

创建 kubeconfig 文件，可使用 aws cli 来生成。初次使用，根据提示进行相关配置，如权限、区域等，配置好后通过如下命令生成 kubeconfig 文件。

```
aws eks update-kubeconfig --region region-code --name my-cluster
```

注：区域与集群名称需替换成自己所在区域与集群名字。

## LoadBalancer 相关

在 service 使用`LoadBalancer`, 需先安装  Load Balancer Controller， 安装手册详见 : [https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html](https://docs.aws.amazon.com/eks/latest/userguide/aws-load-balancer-controller.html) 

Load Balancer 介绍: [https://docs.aws.amazon.com/eks/latest/userguide/network-load-balancing.html](https://docs.aws.amazon.com/eks/latest/userguide/network-load-balancing.html) 

Annotations: [https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/service/annotations/](https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.4/guide/service/annotations/) 

## StorageClass 配置

在该方案里， 我们使用 EBS， 因此在使用前我们需安装 EBS CSI 驱动程序。在集群详情页面里，我们点击插件、新增，选择 Amazon EBD CSI 驱动程序进行添加。如下:

![StorageClass 配置 1](https://assets.emqx.com/images/ab79c96fa6531ab4ae1320ceb7645496.png)

![StorageClass 配置 2](https://assets.emqx.com/images/604c6b1538cf05212002e35b924d406d.png)

storageclass  yaml 示例:

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ebs-sc
provisioner: ebs.csi.aws.com
volumeBindingMode: Immediate
parameters:
  csi.storage.k8s.io/fstype: xfs
  type: io1
  iopsPerGB: "500"
  encrypted: "true"
allowedTopologies:
- matchLabelExpressions:
  - key: topology.ebs.csi.aws.com/zone
    values:
    - us-east-2c
```

执行以下命令

```
$ kubectl apply -f storageclass.yaml
```

权限设置参考: [https://docs.aws.amazon.com/eks/latest/userguide/csi-iam-role.html](https://docs.aws.amazon.com/eks/latest/userguide/csi-iam-role.html) 

ebs 插件安装参考: [https://docs.aws.amazon.com/eks/latest/userguide/managing-ebs-csi.html](https://docs.aws.amazon.com/eks/latest/userguide/managing-ebs-csi.html) 

## 使用 EMQX Operator 进行集群创建 

Operator 安装参考: [https://github.com/emqx/emqx-operator/blob/main/docs/en_US/getting-started/getting-started.md](https://github.com/emqx/emqx-operator/blob/main/docs/en_US/getting-started/getting-started.md) 

Operator 安装完成后，使用以下 yaml 在 AWS EKS 上进行部署 EMQX 集群

```
cat << "EOF" | kubectl apply -f -
apiVersion: apps.emqx.io/v1beta3
kind: EmqxEnterprise
metadata:
  name: emqx-ee
  labels:
    "foo": "bar"
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "external"
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "ip"
    service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
    service.beta.kubernetes.io/aws-load-balancer-attributes: load_balancing.cross_zone.enabled=true
    service.beta.kubernetes.io/aws-load-balancer-target-group-attributes: preserve_client_ip.enabled=true
    service.beta.kubernetes.io/aws-load-balancer-attributes: deletion_protection.enabled=true
spec:
  replicas: 3
  persistent:
     storageClassName: ebs-sc
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

## 使用 NLB 进行 TLS 终结

我们推荐在 NLB 上做 TLS 终结，可通过以下几个步骤实现：

### 证书导入

在 AWS 控制台（[https://us-east-2.console.aws.amazon.com/acm/home](https://us-east-2.console.aws.amazon.com/acm/home)），导入相关证书，证书导入后点击证书 ID，进入详情页面，复制 ARN 信息，如下图:

![复制 ARN 信息](https://assets.emqx.com/images/c66e3c85e922880b7c8f80226d5d8446.png)

### 修改部署 yaml

```
cat << "EOF" | kubectl apply -f -
apiVersion: apps.emqx.io/v1beta3
kind: EmqxEnterprise
metadata:
  name: emqx-ee
  labels:
    "foo": "bar"
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "external"
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: "ip"
    service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
    service.beta.kubernetes.io/aws-load-balancer-attributes: load_balancing.cross_zone.enabled=true
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: arn:aws:acm:us-west-2:arn:arn:aws:acm:us-east-1:609217282285:certificate/326649a0-f3b3-4bdb-a478-5691b4ba0ef3
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tcp
    service.beta.kubernetes.io/aws-load-balancer-ssl-ports: 1883,mqtt-tls
    service.beta.kubernetes.io/aws-load-balancer-target-group-attributes: preserve_client_ip.enabled=true
    service.beta.kubernetes.io/aws-load-balancer-attributes: deletion_protection.enabled=true
spec:
  replicas: 3
  persistent:
     storageClassName: ebs-sc
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

相比不使用 TLS 证书，我们在 Annotations 里增加了下面三项内容，其中 `service.beta.kubernetes.io/aws-load-balancer-ssl-cert` 的值为我们第一步中复制的 ARN 信息。

```
service.beta.kubernetes.io/aws-load-balancer-ssl-cert: arn:aws:acm:us-west-2:arn:arn:aws:acm:us-east-1:609217282285:certificate/326649a0-f3b3-4bdb-a478-5691b4ba0ef3
service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tcp
service.beta.kubernetes.io/aws-load-balancer-ssl-ports: 1883,mqtt-tls
```


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
