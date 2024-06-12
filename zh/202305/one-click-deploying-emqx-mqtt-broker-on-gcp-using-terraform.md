## 引言

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种轻量级的消息传递协议，适用于物联网应用实现设备间通信。 作为一款主流的[开源 MQTT Broker，EMQX](https://github.com/emqx/emqx) 能够提供高扩展性、可靠性和安全性的 MQTT 消息传递服务。

借助广泛应用的基础设施即代码（IaC）工具 Terraform，您可以轻松在 GCP 上自动部署 EMQX MQTT Broker，从而简化和规范 MQTT 基础设施的设置和管理。

本文将指导您如何设置 GCP 项目、创建服务账户、编写 Terraform 配置文件，实现轻松部署 EMQX MQTT Broker。

## 准备工作

在开始之前，请做好以下准备：

- 注册 Google Cloud Platform 账户
- 在您的本地机器上安装 Google Cloud SDK
- 在您的本地机器上安装 Terraform
- 对 GCP、Terraform 和 MQTT 有基本的了解

## 配置 GCP 环境

按照以下步骤配置 GCP 环境：

1. 创建新的 GCP 项目或使用已有的项目（Project）。
2. 为您的项目启用所需的 API（Compute Engine API）。
3. 为 Terraform 创建具有所需权限的服务账户。建议使用 Compute Engine Admin 角色。
4. 下载 JSON 密钥文件。

## 使用 Terraform 在 GCP 上部署 EMQX

### 配置 Terraform

在您的 Terraform 代码中配置 GCP Provider，并使用服务账户密钥文件进行认证。

```
provider "google" {
  credentials = file("<PATH-TO-KEY-FILE>")
  project     = "<PROJECT-ID>"
  region     = "<REGION>"
  zone       = "<ZONE>"
}
```

### 配置网络

这一步需要了解 GCP 相关的三个基本术语：项目、VPC 和子网（Subnet）。这些术语的定义如下：

- 项目是 GCP 中的顶层组织单元，包含所有的资源。
- VPC 是在 GCP 项目内定义的私有网络，允许您创建和管理 IP 地址、子网和路由表。
- 子网是将 VPC 网络划分为更小、更易于管理的部分的一种方式。它们可以为特定的资源分配 IP 地址，并定义不同的网络段。

它们之间的关系可以用下图来说明：

![项目、VPC 和子网（Subnet）](https://assets.emqx.com/images/8eb84c7861685fdfbdcdc657217a1218.png)

**创建 VPC 网络**

我们需要创建一个 VPC 网络，为您的网络相关资源提供连接，其中包括：

- Compute Engine 虚拟机实例
- Container Engine 容器
- App Engine Flex 服务
- 其他网络相关资源

```
resource "google_compute_network" "vnet" {
  project                 = "<PROJECT>"
  name                    = "<NAME>"
  auto_create_subnetworks = false
}
```

**在 VPC 中创建子网**

每个 VPC 网络都被划分为若干子网，这里我们创建一个子网。

```
resource "google_compute_subnetwork" "sn" {
  name          = "<NAME>"
  ip_cidr_range = cidrsubnet(var.address_space, 8, 1)

  region  = var.region
  network = google_compute_network.vnet.id
}
```

**创建防火墙规则**

每个网络都有自己的防火墙，控制着实例之间以及实例与外部的访问。除非创建防火墙规则允许访问实例，否则所有到实例的流量，包括来自其他实例的流量，都会被防火墙阻止。

“ports” 定义了一些与 MQTT 相关的端口，例如 “1883”、“8883”、“8083”、“8084”。

```
resource "google_compute_firewall" "fw" {
  name          = "<NAME>"
  network       = google_compute_network.vnet.name
  source_ranges = ["0.0.0.0/0"]

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = "<PORTS>"
  }
}
```

### 配置 EMQX 集群

**为每个 EMQX 节点创建虚拟机实例**

虚拟机实例可以用于部署应用、运行服务或执行计算任务。

在下面的示例中，我们创建了一个名为 example-instance 的 google_compute_instance 资源，并指定了 name、machine_type、boot_disk、network_interface 属性。

```
resource "google_compute_instance" "example" {
  name         = "example-instance"
  machine_type = "n1-standard-1"

  boot_disk {
    initialize_params {
      image = ""ubuntu-os-cloud/ubuntu-2004-lts""
    }
  }

  network_interface {
    network = google_compute_network.example.name
    subnetwork = google_compute_subnetwork.example.name
    access_config {
      // Ephemeral external IP
    }
  }
}
```

**启动 EMQX 节点**

创建虚拟机实例后，需要初始化每个 EMQX 节点。首先，您必须初始化并复制 [init.sh](http://init.sh/) 到每个节点。然后下载 EMQX 包并在每个节点上执行刚才复制的 [init.sh](http://init.sh/)。最后，分别启动 EMQX。

```
resource "null_resource" "init" {
  depends_on = [google_compute_instance.example]

  count = "<INSTANCE-COUNT>"
  connection {
    type        = "ssh"
    host        = "<HOST-LIST>"
    user        = "ubuntu"
    private_key = "<YOUR-PRIVATE-KEY>"
  }

  # config init script
  provisioner "file" {
    content = templatefile("${path.module}/scripts/init.sh", { local_ip = <PRIVATE-IPS>[count.index],
      emqx_lic = <EMQX-LICENSE>, emqx_ca = <EMQX-CA> emqx_cert = <EMQX-CERT>, emqx_key = <PRIVATE-KEY> })
    destination = "/tmp/init.sh"
  }

  # download EMQX package
  provisioner "remote-exec" {
    inline = [
      "curl -L --max-redirs -1 -o /tmp/emqx.zip <EMQX-PACKAGE-URL>"
    ]
  }

  # init system
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/init.sh",
      "/tmp/init.sh",
      "sudo mv /tmp/emqx <HOME>",
    ]
  }

  # start EMQX 
  provisioner "remote-exec" {
    inline = [
      "sudo <HOME>/bin/emqx start"
    ]
  }
}
```

**将 EMQX 节点加入集群**

随机选择 EMQX 集群中的一个节点，然后逐个将其他节点加入该节点。

```
resource "null_resource" "emqx_cluster" {
  depends_on = [null_resource.init]

  count = "<INSTANCE-COUNT>-1"

  connection {
    type        = "ssh"
    host        = <OTHERS>[count.index % <OTHERS>]
    user        = "ubuntu"
    private_key = "<YOUR-PRIVATE-KEY>"
  }

  provisioner "remote-exec" {
    inline = [
      "/home/ubuntu/emqx/bin/emqx_ctl cluster join emqx@${local.another_emqx}"
    ]
  }
}
```

### 配置负载均衡

![配置负载均衡](https://assets.emqx.com/images/b35cf6e813263646fc5587c5c45ed967.png)

在上面的示例中：

1. 创建了一个 google_compute_http_health_check 资源，用于配置健康状态检查。
2. 创建了一个 google_compute_target_pool 资源，它引用了实例组和健康状态检查。
3. 创建了一个 google_compute_forwarding_rule 资源，它设置了转发规则，将 1883 端口的入站流量路由到目标池。
4. 还可以为其它端口（“8883”、“8083”、“8084”、“18083”）添加更多的 google_compute_forwarding_rule。

```
resource "google_compute_http_health_check" "example" {
  name               = "example-health-check"
  check_interval_sec = 30
  timeout_sec        = 5
  port         = 8081
  request_path = "/status"
}

resource "google_compute_target_pool" "example" {
  name = "example-target-pool"

  instances = [
    google_compute_instance_group.example.self_link
  ]

  health_checks = [
    google_compute_http_health_check.example.name
  ]
}

resource "google_compute_forwarding_rule" "example-1883" {
  name       = "example-forwarding-rule"
  target     = google_compute_target_pool.example.self_link
  port_range = "1883"
  ip_protocol = "TCP"
}

resource "google_compute_forwarding_rule" "example-8883" {
  ...
}
```

## 初始化并应用 Terraform

```
terraform init
terraform plan
terraform apply
```

应用成功后，将输出以下内容：

```
Outputs:
loadbalancer_ip = ${loadbalancer_ip}
tls_ca = <sensitive>
tls_cert = <sensitive>
tls_key = <sensitive>
```

您现在可以通过相应的端口访问不同的服务了。

```
Dashboard: ${loadbalancer_ip}:18083
MQTT: ${loadbalancer_ip}:1883
MQTTS: ${loadbalancer_ip}:8883
WS: ${loadbalancer_public_ip}:8083
WSS: ${loadbalancer_public_ip}:8084
```

## 结语

使用 Terraform 在 GCP 上部署 EMQX，可以让您轻松管理物联网基础设施，专注于创造物联网应用。按照本文的指引，您可以在 GCP 上快速搭建出具有强大扩展性和高可靠性的 MQTT Broker，为您的物联网项目提供支持。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
