Terraform 是由 HashiCorp 推出的一个基础设施即代码（IaC）工具，它包括了底层的组件如计算实例、存储和网络，以及高层的组件如 DNS、LBS 等。用户可以使用 Terraform 安全、高效地构建、改变和更新基础设施。

在传统的私有云或公有云部署方式中，用户需要先部署好基础设施（虚拟机、网络和存储等），之后才能开始部署 MQTT 集群。而如果使用 Terraform，用户则可以同时完成这两项工作。此外，同一套工具可以在不同的平台上进行部署，通过模版可重复、可预测的方式定义和配置资源，可大大减少人为因素导致的错误。

本文将以分布式物联网 [MQTT 消息服务器 EMQX](https://www.emqx.com/zh/products/emqx) 为例，采用阿里云作为公有云平台，介绍如何使用 Terraform 快速部署一个高可用的 MQTT 集群。

## Terraform 简介

作为一个管理服务生命周期的工具，Terraform 可以用状态文件记录和跟踪所有环境变化。默认状态是存储在本地的，通过 HCL 或者 JSON 来定义，HCL 是 HashiCorp 提供的模板语言。

![Terraform 工作原理](https://assets.emqx.com/images/35350040d0528109d84270578cf6deed.png)

<center>Terraform 工作原理</center>

- Coding：用 HCL 来编写基础设施代码。可以定义块，参数和表达式。
- Plan：运行 Terraform Plan 来检查执行计划是否符合期望。
- Apply：运行 Terraform Apply 来构建用户所需的基础设施

## 准备与安装

### 安装 Ali Cloud SDK for Go

```
go get -u github.com/aliyun/alibaba-cloud-sdk-go/sdk
```

### 安装 Terraform

以 Mac 为例，通过 brew 安装。

```
brew tap hashicorp/tap 2brew install hashicorp/tap/terraform 
```

验证安装

```
terraform -help
```

具体可参考[官方文档](https://learn.hashicorp.com/tutorials/terraform/install-cli)。

## 使用 Terraform 部署 EMQX 集群

### 下载阿里云部署脚本

```
git clone https://github.com/emqx/terraform-emqx-emqx-alicloud.git
```

### 部署脚本说明

**脚本配置文件路径：**

- 单机部署配置文件：`services/emqx/terraform.tfvars`
- 集群部署配置文件：`services/emqx_cluster/terraform.tfvars`

**部署脚本默认使用以下配置，读者可根据实际情况自行修改：**

- Ali Cloud SDK: v1.61.1608

  > 老版本 SDK 可能会导致 ELB 部署失败

- 默认 EMQX 版本：企业版 4.4.3 

  如果要部署开源版，需要修改 `terraform.tfvars` 文件末尾的 `emqx_package` 值，比如部署开源版 5.0.3：

  `emqx_package = https://www.emqx.com/en/downloads/broker/5.0.3/emqx-5.0.3-ubuntu20.04-amd64.tar.gz`

- 默认阿里云 Region 为：`cn-shenzhen`
- 默认集群节点：2 台 `ecs.t6-c1m1.large`

### 配置阿里云 AccessKey

进入阿里云 AccessKey 页面

![阿里云 AccessKey 页面](https://assets.emqx.com/images/bacf5e7d02f816c231eb83648be98656.png)

拿到创建好的 AccessKey 和 Secret，设置环境变量

```
export ALICLOUD_ACCESS_KEY=${anaccesskey}
export ALICLOUD_SECRET_KEY=${asecretkey}
export ALICLOUD_REGION=${region}
```

### 部署 EMQX 企业版集群

> 用户可以通过修改 `terraform.tfvars` 文件，来更改默认的配置

```
cd services/emqx_cluster
terraform init
terraform plan
terraform apply -auto-approve
```

等待几分钟后，可以看到部署完成的结果如下：

![部署完成](https://assets.emqx.com/images/d39b89724d1dfa84d6170a6683ffd489.png)

## 验证集群部署结果

集群部署成功后，我们可以简单测试集群是否已正常运行。先上图获取到集群的 IP 地址（emqx_cluster_address = "120.79.163.50"），并通过以下信息访问 EMQX 企业版的 Dashboard。

> `http://120.79.163.50:18083`
>
> 用户名：`admin`
>
> 密码：`public`

![EMQX Dashboard](https://assets.emqx.com/images/91897103297195423ee7e819a98aa9df.png)

从上图可以看到我们部署了 2 个节点，这时可以通过 WebSocket 工具进行简单的验证：

1. 左边菜单栏选择工具→WebSocket

   ![MQTT WebSocket](https://assets.emqx.com/images/3d1f9dc058ac7d40bf48a479a4f49fd3.png)
 
2. 点击“连接”

   ![MQTT WebSocket: 连接](https://assets.emqx.com/images/2fc73ab008e87690b9a51b998f452040.png)

3. 订阅主题

   ![MQTT WebSocket: 订阅主题](https://assets.emqx.com/images/a1acc3431474129a94208ffa03b4d0ad.png)

4. 点击发布，正常能看到如下结果

   ![MQTT WebSocket: 发布](https://assets.emqx.com/images/15a43e714ab770ac3f1837707c2a8751.png)
 

## 结语

至此，我们完成了通过 Terraform 在阿里云上快速部署 MQTT 集群的全部流程。读者可根据实际情况修改部署脚本，创建满足自己业务需求的 EMQX 集群，借助 EMQX 在物联网数据连接、移动与处理方面的优势构建具有竞争力的物联网平台与应用。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
 

> **参考资料**
>
> 代码仓库: [https://github.com/emqx/terraform-emqx-emqx-alicloud](https://github.com/emqx/terraform-emqx-emqx-alicloud) 
>
> EMQX Terraform 模块官方文档：[https://docs.emqx.com/zh/emqx-terraform/latest](https://docs.emqx.com/zh/emqx-terraform/latest)
