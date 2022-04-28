# 在 Rainbond 中一键部署高可用 EMQ 集群

本文描述如何通过云原生应用管理平台 [Rainbond](https://www.rainbond.com/?channel=emqx) 一键安装高可用 [EMQ](https://www.emqx.com) 集群。这种方式适合不太了解 Kubernetes、容器化等复杂技术的用户使用，降低了在 Kubernetes 中部署 EMQ 的门槛。

## 一、背景信息

### 1.1 Rainbond 与 EMQ 的结合
[Rainbond](https://www.rainbond.com/?channel=emqx) 是一款易于使用的开源云原生应用管理平台。

借助于它，用户可以在图形化界面中完成微服务的部署与运维。

借助 Kubernetes 和容器化技术的能力，将故障自愈、弹性伸缩等自动化运维能力赋能给用户的业务。

这类用户不必再关心如何部署 EMQ 集群，Rainbond 团队将 EMQ 制作成为可以一键部署的应用模版，供开源用户免费下载安装。

这种安装方式极大的降低了用户使用 EMQ 集群的部署负担，目前支持最新版本 `4.4.3`。

### 1.2 关于应用模版

应用模版是面向 Rainbond 云原生应用管理平台的安装包，用户可以基于它一键安装业务系统到自己的 Rainbond 中去。无论这个业务系统多么复杂，应用模版都会将其抽象成为一个应用，裹挟着应用内所有组件的镜像、配置信息以及所有组件之间的关联关系一并安装起来。

## 二、前提条件

- 部署好的 Rainbond 云原生应用管理平台：例如 [快速体验版本](https://www.rainbond.com/docs/quick-start/quick-install/?channel=emqx)，可以在个人 PC 环境中以启动一个容器的代价运行。
- 可以连接到互联网。

## 三、快速开始

### 3.1 访问内置的开源应用商店

选择左侧的 **应用市场** 标签页，在页面中切换到 **开源应用商店** 标签页，搜索关键词 **EMQ** 即可找到 EMQ 应用。

![](https://static.goodrain.com/wechat/emqx/1.png)

### 3.2 一键安装

点击 EMQ 右侧的 **安装** 可以进入安装页面，填写简单的信息之后，点击 **确定** 即可开始安装，页面自动跳转到拓扑视图。



![](https://static.goodrain.com/wechat/emqx/2.png)

参数说明：

| 选择项   | 说明                                                      |
| -------- | --------------------------------------------------------- |
| 团队名称 | 用户自建的工作空间，以命名空间隔离                        |
| 集群名称 | 选择 EMQ 被部署到哪一个 K8s 集群                          |
| 选择应用 | 选择 EMQ 被部署到哪一个应用，应用中包含有若干有关联的组件 |
| 应用版本 | 选择 EMQ 的版本，目前可选版本为 4.4.3                     |

等待几分钟后，EMQ 集群就会安装完成，并运行起来。

![](https://static.goodrain.com/wechat/emqx/3.png)

### 3.3 验证 EMQ 集群

* 通过 Dashboard 验证查看集群节点。访问组件 `EMQX_Cluster-4.4.3` 的 `18083` 端口的对外服务域名，即可登录 EMQ Dashboard，在首页 Nodes 展示所有节点都处于 `Running` 状态。

  > 默认账户密码: admin/public ，可通过环境变量修改 `EMQX_DASHBOARD__DEFAULT_USERNAME` `EMQX_DASHBOARD__DEFAULT_PASSWORD`

![](https://static.goodrain.com/wechat/emqx/4.png)

* 通过命令行查看集群节点，进入组件 `EMQX_Cluster-4.4.3` 的Web终端，选择任意一个实例，执行以下命令：

```shell
emqx_ctl cluster status
```

![](https://static.goodrain.com/wechat/emqx/5.png)