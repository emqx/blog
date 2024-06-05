Google Cloud 的 IoT Core 产品将于 2023 年 8 月 16 日停止服务，随着这一日期的临近，许多用户正在为他们现有的物联网业务寻找新的解决方案，而 EMQX 企业版是实现这一目标的理想选择。

[EMQX 企业版](https://www.emqx.com/zh/products/emqx)是一款大规模分布式 MQTT 消息服务平台，能够通过多种方式部署到 Google Cloud Platform（GCP） 上。您可以轻松地将 IoT Core 上的设备迁移到 EMQX Enterprise，然后继续与 GCP 中的数据服务无缝集成，实现快速迁移而不影响现有业务。

本文将指导您如何在 GCP 上部署 EMQX 企业版，并完成物联网消息发布订阅测试。

## 在 GCP 上创建并启动虚拟机实例

在部署 EMQX 企业版之前，我们先在 GCP 上创建一个 Virtual Machine。

GCP 的 Virtual Machine Instances 允许用户轻松部署和管理应用程序，而无需在本地创建和管理服务器。以下是在 GCP 上创建 Virtual Machine 的步骤，你还可以参考 [Create and start a VM instance](https://cloud.google.com/compute/docs/instances/create-start-instance#console)。

1. 登录 [GCP 控制台](https://console.cloud.google.com/) 并点击 **Create a VM。**

   ![Create a VM](https://assets.emqx.com/images/44b3b8d91de89a2226526b346cf8df48.png)

2. 如果您之前没有创建过 Virtual Machine，将跳转到 **Compute Engine API** 详情页面，点击 **ENABLE** 启用 Compute Engine API 以继续创建过程。

   ![点击 ENABLE](https://assets.emqx.com/images/6e00419c9a643b4f8029d0f515defa6c.png)

3. 勾选 **New VM instance** 选项并开始实例创建配置。

   选择合适的 Region 与 Zone 并确定 Machine configuration。此处使用 E2 系列的服务器，Machine type 选择 Custom，分配 2 核 vCPU、4GB 内存。

   在此规格下，单个 EMQX 节点能够承载 10,000 MQTT 连接以及 5,000 TPS 的并发消息。

   ![机器配置 1](https://assets.emqx.com/images/445054ca2fce0f3eccf26bdba75dfa37.png)

   在 Boot disk 配置中，选择 Ubuntu 20.04 LTS 操作系统，并更改磁盘大小为 30GB。

   ![机器配置 2](https://assets.emqx.com/images/3016bcfd0657d52ad23bce596e71de5d.png)

   ![Boot disk](https://assets.emqx.com/images/1d188c1b692841c57cc9ce1daa53d5d6.png)

4. 其余配置保持默认，点击 **CREATE** 开始创建 Instance。

## 安装 EMQX 企业版

我们将使用 GCP 的 SSH 连接到 VM  instance 以部署 EMQX 企业版。在此之前，我们需要获取 EMQX 企业版的下载地址和安装命令。

在这个例子中，我们需要在 **Ubuntu 20.04** 上部署 **EMQX 4.4.16**，你可以从 [下载 EMQX Enterprise](https://www.emqx.com/zh/try?product=enterprise) 页面获取所需信息。

![EMQX 企业版下载](https://assets.emqx.com/images/b1f102630a26ff20ce8e731b720e999d.png)

![EMQX 企业版下载](https://assets.emqx.com/images/8eee3b2f4503fd752eb9b5e1f343d053.png)

1. 登录 [GCP 控制台](https://console.cloud.google.com/)，点击 **Navigation menu** → **PRODUCTS** → **COMPUTE** → **Compute Engine** → **VM Instances** 进入到 VM instances 列表。

   ![VM instances 列表](https://assets.emqx.com/images/b5456818e4398a40349dcbf97d52fd48.png)

2. 找到创建的 VM instance，您可以看到 GCP 已经为它分配了一个唯一的外部 IP，单击 **SSH** 打开您的 SSH 终端。

   ![打开 SSH 终端](https://assets.emqx.com/images/5c317a682d2b5f50b384a1c8a3b68508.png)

3. 在 SSH 终端中进入根目录，并按照以下命令进行安装：

   进入根目录：

   ```
   sudo su
   cd ../../
   ```

   使用 `wget` 命令下载 EMQX 企业版：

   ```
   wget https://www.emqx.com/en/downloads/enterprise/4.4.16/emqx-ee-4.4.16-otp24.3.4.2-1-ubuntu20.04-amd64.deb
   ```

   ![命令行下载 EMQX 企业版](https://assets.emqx.com/images/1213599ae653851400022ff9d6be94bb.png)

   安装 EMQX 企业版：

   ```
   sudo apt install ./emqx-ee-4.4.16-otp24.3.4.2-1-ubuntu20.04-amd64.deb
   ```

   ![安装 EMQX 企业版](https://assets.emqx.com/images/00ec22a12650db74fcd56e1c65c46e34.png)

   启动 EMQX 企业版：

   ```
   sudo systemctl start emqx
   ```

恭喜您，您已经完成 EMQX 企业版在 GCP VM instance 上的安装。

## 在 GCP 上打开防火墙端口

在 GCP 上安装服务或应用程序后，您需要手动开放所需的端口才能够从外部访问它，请按照以下步骤在 GCP 上打开所需端口。

1. 登录 [GCP 控制台](https://console.cloud.google.com/)，点击 **Navigation menu**  → **PRODUCTS** → **VPC network** →  **Firewall** 进入到 **Firewall** 页面。

   ![Firewall 页面](https://assets.emqx.com/images/a4ce3dae6592eddf1ff158d69e612c5f.png)

2. 点击 **CREATE FIREWALL RULE。**

   ![CREATE FIREWALL RULE](https://assets.emqx.com/images/60d55a9a3e5dd99bd1420b2482023eaa.png)

3. 填入以下字段以创建防火墙规则：

   - **Name：**输入规则名称
   - **Network**：选择 **default**
   - **Priority**：规则优先级，数字越小优先级越高，此处输入 **1000**
   - **Direction of traffic**: 选择 **Ingress**，表示在特定端口上接收数据
   - **Action on match**: 选择 **Allow**，表示允许流量通过
   - **Targets:**  选择 **All instances in the network**，将规则应用于网络中所有实例
   - **Source filter:** Choose the source filter as **IPv4 ranges** if you want to receive data from all networks or users
   - **Source IPv4 ranges:** IP 地址 **0.0.0.0/0** 表示任何一个都可以发送数据，您也可以配置从特定 IP 地址接收数据的规则
   - **Protocols and ports**: 如果要打开所有端口，请选择 **Allow all**。此处打开指定 TCP 端口即可，您可以通过分隔逗号同时打开多个端口，此处输入 1883, 8883, 8083, 8084, 18083, 8081。

   ![配置防火墙规则](https://assets.emqx.com/images/9926fcd7f237be282edd601d38d36f8d.png)

4. 点击最下方 **CREATE** 完成防火墙规则创建，您可以在列表中看到您创建的规则。

   ![完成防火墙规则创建](https://assets.emqx.com/images/231d4e10a6b78048e519f84a20344717.png)

## 通过 MQTTX 快速测试

至此，您已经在 GCP 上完成 EMQX 企业版的安装并开通了所有需要的端口，对应的连接信息如下：

| 服务器地址             | 34.xxx.xxx.xxx <br>(请替换为实际的 VM Instance 公共 IP 地址) |
| :--------------------- | ------------------------------------------------------------ |
| TCP 端口               | 8883                                                         |
| WebSocket 端口         | 8083                                                         |
| SSL/TLS 端口           | 8883                                                         |
| WebSocket SSL/TLS 端口 | 8084                                                         |
| Dashboard 访问端口     | 18083                                                        |
| REST API 端口          | 8081                                                         |

下面我们使用 MQTTX 模拟物联网 MQTT 设备的接入，快速测试服务器是否可用。

> [MQTTX ](https://mqttx.app/zh)是 EMQ 开源的一款跨平台 MQTT 5.0 客户端工具，它支持 macOS、Linux、Windows，具有丰富的功能，您可通过 MQTTX 一键式的连接方式和图形界面，轻松测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 连接。
>
> [MQTTX Web](https://mqttx.app/zh/web) 是 MQTTX 的浏览器版本，可以免除下载与安装，打开浏览器即可通过 WebSocket 快速连接至 MQTT 服务器。

1. 访问 [MQTTX Web](http://mqtt-client.emqx.com/#/recent_connections) 页面，点击 **New Connection** 或菜单栏 **+** 图标创建连接。

   ![New Connection](https://assets.emqx.com/images/f761642f67fe59fb0b36cd7196635b1a.png)

2. 配置并建立 MQTT 连接，您只需配置：

   - **Name**: 连接名称，如 **GCP EMQX Enterprise**

   - **Host**

     - 选择连接类型为 **ws://**，MQTTX Web 仅支持 WebSocket 协议，如希望测试 SSL/TLS 认证连接，请下载 [MQTTX 客户端](https://mqttx.app/zh)
     - 填入 VM instance 公共 IP 地址

   - **Port**: 填入 **8083**, 即 WebSockets 协议对应的端口

     其他选项保持默认配置，你也可以根据具体业务场景修改，对应的配置说明可参考 [MQTTX 手册 - 快速建立连接](https://mqttx.app/zh/docs/get-started)

   配置完成后，点击页面右上角的 **Connect** 建立连接。

   ![建立连接](https://assets.emqx.com/images/fdd865fa9c801cb60569f12c7d25131b.png)

3. 订阅主题并发布消息，完成消息发布订阅测试

   - 点击 **New Subscription，**在弹出框中输入 `testtopic/#` 主题并订阅
   - 在消息发送框输入` testtopic/1` 主题，其他字段使用默认值
   - 点击 Payload 输入框右下角发送按钮，可以在聊天窗口中看到消息已成功发送
   - 几乎同时，聊天窗口中收到一条新消息，表示发布订阅测试已经完成

   ![订阅主题并发布消息](https://assets.emqx.com/images/4ff3fa6c3a0e115ed6f5da790ae94e42.png)

完成设备连接以及消息发布订阅测试后，您还可以通过浏览器打开 `http://<ip>:18083`，使用默认用户名 **admin** 与密码 **public** 登录 EMQX Dashboard。

在 Dashboard 上您可以轻松管理和监控 EMQX，管理设备列表，并配置安全、数据集成等各项功能。

![EMQX Dashboard](https://assets.emqx.com/images/a43e9c2071b91c9a040cc387ab7bf465.png)


## 写在最后

现在我们已经了解了如何在 GCP 上部署 EMQX 企业版。如需在生产中使用 EMQX 企业版，建议您继续通过 [VPC 网络](https://cloud.google.com/vpc/docs/vpc)创建 [EMQX 集群](https://docs.emqx.com/zh/enterprise/v4.4/advanced/cluster.html)，以获得更好的扩展性和可用性。

除了手动安装外，您还可以通过 [EMQX Kubernetes Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 与 [EMQX Terraform](https://www.emqx.com/zh/emqx-terraform) 在 GCP 上部署 EMQX 企业版，我们也强烈推荐全托管的 MQTT 消息云服务 [EMQX Cloud](https://www.emqx.com/zh/cloud)。

在本系列的后续博客中，我们将继续向您介绍如何将设备从 GCP IoT Core 迁移到 EMQX 企业版，以及如何通过 EMQX 企业版的 GCP Pub/Sub 集成无缝迁移 IoT Core 服务。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
