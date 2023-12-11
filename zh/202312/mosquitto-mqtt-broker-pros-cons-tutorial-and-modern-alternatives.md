## Eclipse Mosquitto MQTT Broker 简介

Eclipse Mosquitto 是一个采用 MQTT（Message Queuing Telemetry Transport）协议的开源消息 Broker。[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种轻量级协议，专为带宽受限的设备设计，特别适用于网络带宽有限的机器对机器（M2M）或物联网（IoT）应用。

Mosquitto MQTT Broker 最初由 Roger Light 在 2009 年开发，并于后来捐赠给了 Eclipse 基金会。它可能是第一个开源的 MQTT 项目。Broker 负责接收、过滤和分发来自客户端的所有消息，并根据订阅关系将消息发送给相应的客户端。

在物联网世界中，设备之间需要高效地通信，Mosquitto 可以同时处理多个连接并实时传输消息，功能非常强大。

## Mosquitto MQTT Broker 的主要特点

### 轻量级

Mosquitto 的一个显著特点是其轻量级设计。这表示它在运行时对系统资源的需求非常少，因此非常适合小型、资源受限的设备，例如传感器、微控制器以及其他物联网设备。此外，它能够有效地利用网络带宽，在网络不稳定或受限的环境中也能够良好运行。

不过，Mosquitto 的可扩展性相对有限。它最多只能支持几千个连接，适用于小规模的物联网应用，无法满足拥有百万级连接的大规模应用需求。

### 多平台

Mosquitto 支持多种操作系统，包括 Linux、Windows、macOS，以及树莓派这类嵌入式系统。它也支持 Docker 容器，但不支持 Kubernetes 或 Terraform。

### 桥接

通过桥接功能，Mosquitto 能够与其他 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 建立连接，无论这些 Broker 来自同一网络还是不同网络。桥接功能在需要从不同网络聚合数据或者想要连接孤立的网络时非常有用。

### 消息存储

Mosquitto 提供了消息存储功能，能够在消息接收者当前无连接的情况下暂时为它们保存消息。一旦这些接收者重新上线，存储的消息就会被发送给它们，从而确保即使在短暂的断开连接后数据也不会丢失。

这个功能在物联网应用中特别有用，因为物联网设备可能由于各种原因（如电源故障或网络问题）而离线或无法访问。

## Mosquitto MQTT Broker 的局限性

### 没有内置的 Web 界面

Mosquitto 的一个明显局限性是缺乏内置的 Web 界面。这意味着不能轻松地通过 Web 管理和监控 MQTT Broker 和主题。相反，需要依赖命令行工具或第三方应用来执行这些任务。缺少 Web 界面可能被视为一个重要缺陷，因为图形用户界面能让管理和监控更容易。

### 数据集成有限

Mosquito 支持 webhook，但与 MySQL、MongoDB、Redis 等数据处理工具集成比较困难。这使得将 Mosquitto 很难融入现代数据基础设施。

### 云支持有限

许多企业正在转向在云中运行 MQTT 基础设施。Mosquitto 并未内置支持 AWS、Azure 或 Google Cloud 等云服务，因此不能兼容基于云的物联网部署。

### 安全功能有限

Mosquitto 的另一个局限性在于其安全性相对有限。尽管它提供了基本的安全功能，如用户名/密码认证和 SSL/TLS 加密，但缺乏高级的安全机制。例如，Mosquitto 不支持基于角色的访问控制（RBAC），而 RBAC 能够对特定主题的发布者或订阅者进行细粒度的控制。对于 RBAC 支持的缺失在传输敏感数据或需要进行严格访问控制的场景中可能带来问题。

### 不支持集群

Mosquitto MQTT 缺少内置的集群或冗余功能。在集群中，多个 MQTT Broker 可以协同工作，提供高可用性和负载均衡，如果其中一个 Broker 发生故障，其他 Broker 能够接管，从而确保系统持续运行。遗憾的是，Mosquitto 并不支持这一特性。要为 Mosquitto 实现集群功能，用户需要手动实施或使用第三方工具，这会非常复杂和耗时。

### 持久化机制有限

最后，Mosquitto 的持久化机制有限。它只支持基于文件的持久化，即它将所有的数据（消息、订阅等）存储在一个单独的文件中。基于文件的持久化不具备良好的可扩展性，不适用于大规模物联网部署。

## Mosquitto MQTT Broker 使用教程

### 安装 Mosquitto

安装 Mosquitto 的具体步骤取决于您的操作系统，对于大多数 Linux 发行版，可以使用包管理器进行安装。例如，在 Ubuntu 上，可以通过运行以下命令来安装 Mosquitto：

```
sudo apt-get install mosquitto mosquitto-clients
```

对于 Windows 或 macOS，可以从 Mosquitto 网站下载安装程序并按照提供的说明进行安装。

### 启动 Mosquitto Broker

安装好 Mosquitto 之后，下一步是启动 MQTT Broker。在 Linux 上，可以通过运行以下命令来启动 Broker：

```
sudo systemctl start mosquitto
```

在 Windows 上，Broker 应该在安装后自动启动。如果没有，可以从服务应用程序手动启动它。

### 发布消息

要发布消息，可以使用 Mosquitto 软件包自带的 `mosquitto_pub` 命令行工具。基本语法如下：

```
mosquitto_pub -h <主机名> -t <主题> -m <消息>
```

这个命令中的选项含义如下：

- `-h` 选项指定 MQTT Broker 的主机名。
- `-t` 选项指定要发布消息的主题。
- `-m` 选项指定要发布的信息。

### 订阅主题

订阅主题也很简单。可以使用 `mosquitto_sub` 命令行工具，其基本语法是：

```
mosquitto_sub -h <主机名> -t <主题>
```

这些选项的含义如下：

- `-h` 选项指定 MQTT Broker 的主机名。
- `-t` 选项指定要订阅的主题。

### 测试您的设置

在发布消息和订阅主题之后，应该进行测试来确保它能正常工作。可以通过发布一条测试消息并检查订阅者是否收到它来进行测试。如果一切正常，应该能在订阅者的控制台上看到输出的测试消息。

## EMQX: 替代 Mosquitto MQTT Broker 的更优选择

Mosquitto 完全支持 MQTT 协议的所有特性，但它不具备集群功能，因此无法满足物联网对大规模连接的高性能需求。所以，Mosquitto 不适合作为大规模服务的 MQTT 服务器。更具体地说，它无法应对需要为大量物联网设备提供数百万连接的企业级解决方案。此外，Mosquitto 缺乏必要的企业级功能，导致无法利用 Mosquitto 构建灵活且可靠的物联网应用。

[EMQX](https://www.emqx.com/zh/products/emqx) 是一个专为物联网而设计的大规模分布式 MQTT Broker。EMQX 能够高效且可靠地连接海量的物联网设备，单个集群可以承载高达 1 亿的并发连接，实时处理和分发消息和事件流数据。EMQX 节点还可以与其他类型的 MQTT 服务器和 MQTT 云服务进行桥接，实现跨平台的消息订阅和发布。

除了和 Mosquitto 一样都支持基于 Docker 的容器化部署之外，EMQX 还支持 Kubernetes Operators 和 Terraform，使其可以轻松地在各种公有云平台上部署和运维。

此外，与 Mosquitto 对云部署支持的缺乏不同，EMQX 在 AWS、Google Cloud 和 Microsoft Azure 上提供了 [Serverless](https://www.emqx.com/zh/cloud/serverless-mqtt)、[Dedicated](https://www.emqx.com/zh/cloud/dedicated) 和 [Bring Your Own Cloud (BYOC)](https://www.emqx.com/zh/cloud/byoc) 等多种 MQTT 消息传输服务。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
