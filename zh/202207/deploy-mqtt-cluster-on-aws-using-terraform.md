Terraform 是由 HashiCorp 推出的一个基础设施即代码（IaC）工具，它包括了底层的组件如计算实例、存储和网络，以及高层的组件如 DNS、LBS 等。用户可以使用 Terraform 安全、高效地构建、改变和更新基础设施。

在传统的私有云或公有云部署方式中，用户需要先部署好基础设施（虚拟机、网络和存储等），之后才能开始部署 MQTT 集群。而如果使用 Terraform，用户则可以同时完成这两项工作。此外，同一套工具可以在不同的平台上进行部署，通过模版可重复、可预测的方式定义和配置资源，可大大减少人为因素导致的错误。

本文将以分布式物联网 [MQTT 消息服务器 EMQX](https://www.emqx.com/zh/products/emqx) 为例，采用 AWS 作为公有云平台，介绍如何使用 Terraform 快速部署一个高可用的 [MQTT 集群](https://www.emqx.com/zh/blog/tag/mqtt-broker-%E9%9B%86%E7%BE%A4)。

## Terraform 简介

作为一个管理服务生命周期的工具，Terraform 可以用状态文件记录和跟踪所有环境变化。默认状态是存储在本地的，通过 HCL 或者 JSON 来定义，HCL 是 HashiCorp 提供的模板语言。

![Terraform](https://assets.emqx.com/images/528180f1326cbeff8cf56d46f330f097.png)

- Coding：用 HCL 来编写基础设施代码。可以定义块，参数和表达式。
- Plan：运行 Terraform Plan 来检查执行计划是否符合期望。
- Apply：运行 Terraform Apply 来构建用户所需的基础设施

## 安装与准备

### 安装 Terraform

以 Mac 为例，通过 brew 安装。

```
brew tap hashicorp/tap 2brew install hashicorp/tap/terraform 
```

验证安装

```
terraform -help
```

具体参考[官方文档](https://learn.hashicorp.com/tutorials/terraform/install-cli)

### 安装 AWS Cli

以 Mac 为例

```
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

验证安装

```
which aws
aws --version
```

参考[官方文档](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### 添加用户

1. 进入 AWS 的 IAM 菜单，点击“添加用户”

   ![AWS 添加用户](https://assets.emqx.com/images/dc51ecef2988fb90e6c1c50bd387a9b6.png)

2. 在添加用户中，记得勾选“访问密钥”

   ![AWS 勾选“访问密钥”](https://assets.emqx.com/images/dd8fb8eaa3cd64a62b4254215e23b04d.png)

3. 选择“创建组”

   ![AWS 创建组](https://assets.emqx.com/images/cb273d488fa2e08704923f64ca0061e3.png)

4. 在创建组中添加“AdministratorAccess”策略

   ![添加 AdministratorAccess 策略](https://assets.emqx.com/images/5464a58c718537f0ff0602e03954c763.png)

5. 点击“创建用户”，完成用户添加

   ![AWS 创建用户](https://assets.emqx.com/images/0697c528cac2048c8740130beeab6af5.png)

6. 获取 Access Key 和 Secret

   ![获取 Access Key 和 Secret](https://assets.emqx.com/images/36c9a765bfc5f6c1e90d5cc4f300da58.png)

### 配置 AWS 的 Access Key

拿到上面创建好的access key和secret，设置环境变量

```
AWS_ACCESS_KEY_ID: ${anaccesskey}
AWS_SECRET_ACCESS_KEY: ${asecretkey}
```

## 使用 Terraform 在 AWS 上部署 EMQX 集群

### 下载 AWS 部署脚本

```
git clone "https://github.com/emqx/terraform-emqx-emqx-aws.git"
```

部署脚本说明：

- 暂时不支持 EMQX 5.X
- AWS CLI：aws-cli/2.2.41 Python/3.8.8 Darwin/21.4.0 exe/x86_64 prompt/off

脚本配置文件路径：

- 单机部署配置文件：services/emqx/terraform.tfvars
- 集群部署配置文件：services/emqx_cluster/terraform.tfvars

部署脚本默认使用以下配置，读者可根据实际情况自行修改 terraform.tfvars 文件：

- 默认 EMQX 版本：企业版 4.4.3 

> 如果要部署开源版，需要修改 `emqx_package` 值，比如部署开源版 4.4.3：`https://www.emqx.com/en/downloads/broker/v4.4.3/emqx-4.4.3-otp23.3.4.9-3-ubuntu20.04-amd64.zip`

- 默认AWS Region 为us-east-1
- 默认集群节点：3台`t3.small`

### 部署 EMQX 集群

> 用户可以通过修改terraform.tfvars文件，来更改默认的配置

```
cd services/emqx_cluster
terraform init
terraform plan
terraform apply -auto-approve
```

等待几分钟，部署完成的结果如下所示

![部署完成](https://assets.emqx.com/images/9aaeb4dd49ab191fe08c05c83ce94629.png)

## 验证 EMQX 集群部署结果

集群部署成功后，我们可以简单测试集群是否已正常运行。先从上图获取到集群的IP 地址，并通过以下信息访问 EMQX 企业版的 Dashboard。

> `http://tf-elb-nlb-5bff6976b15586dd.elb.us-east-1.amazonaws.com:18083`
>
> 用户名：`admin`
>
> 密码：`public`

![EMQX Dashboard](https://assets.emqx.com/images/62a0926bfd0d2590e31f13211cb87b5b.png)

从上图可以看到我们部署了 3 个节点，这时可以通过 Websocket 工具进行简单验证：

1. 左边菜单栏选择工具→WebSocket

   ![MQTT WebSocket](https://assets.emqx.com/images/e99796f46531ecb38f45616cd424c32a.png)

2. 点击“连接”

   ![MQTT 连接](https://assets.emqx.com/images/bc35ffaf2aaa7ce74d21180c076d1f00.png)

3. 订阅主题

   ![MQTT 订阅](https://assets.emqx.com/images/cda7430c0c8923d6e23151ad7428e6f2.png)

4. 点击发布，正常能看到如下结果

   ![MQTT 发布](https://assets.emqx.com/images/354e1fd665a977e15eca33bf6c44e23e.png)

## 结语

至此，我们完成了通过 Terraform 在 AWS 上快速部署 MQTT 集群的全部流程。读者可根据实际情况修改部署脚本，创建满足自己业务需求的 EMQX 集群，借助 EMQX 在物联网数据连接、移动与处理方面的优势构建具有竞争力的物联网平台与应用。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>

 

> **参考：**
>
> 代码仓库：<https://github.com/emqx/terraform-emqx-emqx-aws>
>
> EMQX Terraform模块官方文档：<https://docs.emqx.com/zh/emqx-terraform/latest/>
