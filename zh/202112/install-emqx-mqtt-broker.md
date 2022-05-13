[EMQX](https://www.emqx.com/zh/products/emqx) 是基于 Erlang/OTP 平台开发的开源物联网 [MQTT 消息服务器](https://www.emqx.io/zh)，目前广泛应用于全球各行业物联网平台建设中。其设计目标是实现高可靠承载海量物联网终端的 [MQTT](https://www.emqx.com/zh/mqtt) 连接，支持在海量物联网设备间低延时消息路由。

本文将以 EMQX v4.3.10（开源版）为例，介绍 EMQX 在 Docker、Kubernetes、Windows 和 Linux 上的安装方法以及常见问题，为大家利用 MQTT 消息服务器快速搭建物联网平台提供帮助。

## 安装前检查

绝大多数情况下操作系统的环境依赖、监听端口都不会出现问题，测试环境下可以直接安装启动，EMQX 会检查可能存在的问题并停止启动、报出错误。

但是我们仍然建议当生产环境存在升级 EMQX 版本、升级其他服务等环境变动之后，再次启动 EMQX 前务必进行测试和检查，避免产生不必要的损失。

### 检查环境依赖

常见的由于环境依赖导致的问题如下：

- OpenSSL 版本不正确：常见于 CentOS 系统上，需要更新 OpenSSL 版本
- 缺失 MSVCRxxx.dll 文件：Windows 系统特有，需要安装对应的依赖库
- 安装包与操作系统不符：EMQX 需要对应操作系统和版本下载，否则无法启动并报 `cannot execute binary file` 错误

更多的问题和解决方法详见：[EMQX - 常见错误](https://docs.emqx.com/zh/emqx/v4.3/faq/error.html)

### 检查端口占用

端口占用会导致 EMQX 无法启动或部分功能异常，常见的症状有：

- 执行 `emqx start` 时提示启动超时
- 无法打开 Dashboard 或打开后一直报 404 Not Found 错误

出现以上情况，可以使用 `emqx console` 命令启动 EMQX，console 模式下可以打印详细的错误日志。

EMQX 默认情况下监听以下端口：

| **端口**     | **说明**                 |
| :----------- | :----------------------- |
| **集群通信** |                          |
| 4369-4380    | 集群通信                 |
| 5370-5380    | 集群 RPC 通信            |
| **协议接入** |                          |
| 1883         | MQTT 协议端口            |
| 11883        | MQTT 协议端口            |
| 8883         | MQTT/SSL 端口            |
| 8083         | MQTT/WebSocket 端口      |
| 5683         | LwM2M 端口               |
| **管理监控** |                          |
| 8081         | HTTP API 端口            |
| 18083        | Dashboard 管理控制台端口 |

## 使用 Docker 安装 EMQX

使用 Docker 不需要建立安装运行环境，可以更快安装启动 EMQX，Docker 安装教程请见 [Install Docker Engine](https://docs.docker.com/engine/install/) 。

### 运行单个 EMQX 节点

Docker 安装完成之后，可以通过 [Docker Hub](https://hub.docker.com/r/emqx/emqx) 获取 EMQX 镜像：

```shell
docker pull emqx/emqx:4.3.10
```

启动 Docker 容器，建立端口映射：

```shell
docker run -d --name emqx \
  -p 1883:1883 \
  -p 8081:8081 \
  -p 8083:8083 \
  -p 8084:8084 \
  -p 8883:8883 \
  -p 18083:18083 \
emqx/emqx:4.3.10

```

启动成功之后，访问 Dashboard 管理控制台 [http://localhost:18083。](http://localhost:18083/)

### docker-compose 简单集群

通过 docker-compose 可以在本地快速创建 [EMQX 集群](https://www.emqx.com/zh/blog/emqx-haproxy)。

创建 `docker-compose.yaml` 文件：

```shell
version: '3'

services:
    emqx1:
    image: emqx/emqx
    environment:
    - "EMQX_NAME=emqx"
    - "EMQX_HOST=node1.emqx.io"
    - "EMQX_CLUSTER__DISCOVERY=static"
    - "EMQX_CLUSTER__STATIC__SEEDS=emqx@node1.emqx.io, emqx@node2.emqx.io"
    healthcheck:
        test: ["CMD", "/opt/emqx/bin/emqx_ctl", "status"]
        interval: 5s
        timeout: 25s
        retries: 5
    networks:
        emqx-bridge:
        aliases:
        - node1.emqx.io

    emqx2:
    image: emqx/emqx
    environment:
    - "EMQX_NAME=emqx"
    - "EMQX_HOST=node2.emqx.io"
    - "EMQX_CLUSTER__DISCOVERY=static"
    - "EMQX_CLUSTER__STATIC__SEEDS=emqx@node1.emqx.io, emqx@node2.emqx.io"
    healthcheck:
        test: ["CMD", "/opt/emqx/bin/emqx_ctl", "status"]
        interval: 5s
        timeout: 25s
        retries: 5
    networks:
        emqx-bridge:
        aliases:
        - node2.emqx.io

networks:
    emqx-bridge:
    driver: bridge

```

启动 docker-compose 集群：

```shell
docker-compose -p my_emqx up -d
```

查看集群：

```shell
docker exec -it my_emqx_emqx1_1 sh -c "emqx_ctl cluster status"
Cluster status: #{running_nodes => ['emqx@node1.emqx.io','emqx@node2.emqx.io'],
                    stopped_nodes => []}

```

## 在 Kubernetes 上安装 EMQX

[EMQX Kubernetes Operator](https://www.emqx.com/zh/emqx-kubernetes-operator) 是 EMQ 推出的一种封装、部署和管理 EMQX 的方法，也是一个特定的应用控制器，允许 DevOps 人员在 Kubernetes 上编排 EMQX 集群，管理他们的生命周期。

EMQX Kubernetes Operator 可以帮助用户在 Kubernetes 的环境上快速创建和管理 EMQX 集群，不仅极大简化部署和管理流程，也降低了管理和配置的专业技能要求。

它将使部署和管理工作变成一种低成本、标准化、可重复性的能力，高效实现集群扩容、无缝升级、故障处理和统一监控。

详细的部署和使用方式请查看：[https://github.com/emqx/emqx-operator。](https://github.com/emqx/emqx-operator)

## 在 Windows 上安装 EMQX

> EMQX 生产部署建议使用 Linux 服务器，不推荐 Windows 服务器，EMQX 企业版中没有提供 Windows 版本，如需测试可以使用 Docker 或者虚拟机的方式安装。

通过 [EMQX 下载页面](https://www.emqx.com/zh/try?product=broker) 下载要安装的 EMQX 版本的 ZIP 包，解压安装包后，使用命令行进入解压目录运行即可：

```
cd D:\emqx

.\bin\emqx start

```

## 在 Linux 上安装 EMQX

### Linux 一键安装

EMQX 提供一键安装脚本进行安装，脚本将自动识别并下载对应操作系统的安装包进行安装：

```shell
curl https://repos.emqx.io/install_emqx.sh | bash
```

### Linux 二进制包安装

通过  [EMQX 下载页面](https://www.emqx.com/zh/try?product=broker) 下载要安装的 EMQX 版本的 ZIP 包，解压程序包后，使用命令行进入解压目录运行即可：

```shell
cd /opt/emqx
./bin/emqx start

```

### yum 包管理工具安装

安装所需要的依赖包

```shell
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```

使用以下命令设置稳定存储库，以 CentOS 7 为例

```shell
sudo yum-config-manager --add-repo https://repos.emqx.io/emqx-ce/redhat/centos/7/emqx-ce.repo
```

安装最新版本的 EMQX

```shell
sudo yum install emqx
```

### 其他包管理工具和操作系统安装

访问 [EMQX 安装文档](https://docs.emqx.com/zh/emqx/v4.3/getting-started/install.html) 查看更多安装教程。

## 部署说明

EMQX 支持不同的部署方式，您可以通过云服务或私有部署的方式来使用 EMQX。

EMQ 提供了全托管的云原生 [MQTT 消息服务 EMQX Cloud](https://www.emqx.com/zh/cloud)：自动化、全托管部署，无需管理服务器基础设施，可以为您的物联网应用带来轻松便捷的 MQTT 云服务。

如果您需要私有部署，EMQX 也提供了[企业版](https://www.emqx.com/zh/products/emqx)，支持在物理机、容器/K8s、私有云、混合云和公有云（如阿里云、华为云和 AWS ）中的任何地方运行，不受位置限制，不受厂商锁定。

EMQX Cloud 和 EMQX 企业版均提供免费试用服务和试用版版本，您可以在数分钟内完成部署，立即开始探索和测试更丰富的产品功能。

以下是不同版本之间的主要区别，您可以根据自身情况选择不同的部署方式。

![EMQX 版本区别](https://assets.emqx.com/images/173195442d69816513c2800f48121676.png)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
