本月，HStreamDB 团队[正式发布了 v0.8](https://hstream.io/zh/blog/hstreamdb-v-0-8-release-notes)，并启动了 v0.9 的开发工作，v0.9 将在集群、外部系统集成、分区等方面带来重大改进。本月我们主要完成了新的集群机制和数据集成框架 HStream IO 的设计和初步开发工作，并启动了新的 Python 客户端开发。同时正式发布了 Erlang 客户端的 0.1 版本，以及新增了 Helm 和阿里云的部署支持。

## HServer 集群机制改进

在 v0.8 以及之前版本，HServer 集群主要采用的是基于 ZooKeeper 的中心化集群机制，通过 ZooKeeper 来做 HServer 节点的注册和发现以及节点之间的协调等，各个 HServer 节点之间不进行直接通信。这种集群方案被大量分布式系统采用，相对比较成熟，主要的缺点是需要依赖像 ZooKeeper 这样的外部系统，不够灵活，而且扩展性方面也有一些限制。

为了支持更大的集群和更好的扩展性，以及减少对外部系统的依赖，v0.9 将采用去中心化的集群机制，新的集群方案将主要基于 SWIM[1] 论文，其核心包括一套高效的 failure dectation 算法和 gossip style 的集群消息传播机制，类似的方案已经应用在 Consul、Cassandra 等分布式系统中。目前新集群相关功能还在研发过程中，将在 v0.9 正式发布。

## 全新数据集成框架 HStream IO

为了满足多种不同的业务需求，目前企业内部往往存在多套数据系统或者数据平台，包括但不限于：在线事务库、离线分析库、缓存系统、搜索系统、批处理系统、实时处理系统、数据湖等等。**HSteamDB 在专注于精简和重塑实时数据栈的同时，作为一个新兴的流数据库，也肩负着促进数据在整个数据栈内高效流转以及推动企业数据栈现代化和实时化的使命，因此无缝对接和集成众多外部系统的能力对于 HStreamDB 来说也非常重要。**

HStream IO 是 HStreamDB 内部的数据集成框架，它包含 source connectors、sink connectors、IO Runtime 等组件，能够将外部系统的数据通过 source connectors 导入到 HStreamDB，也可以通过 sink connectors 将 HStreamDB 内的数据导出给外部系统。另外值得注意的是，HStream IO 将基于 Airbyte spec 来实现，这意味者我们将能够完全复用 Airbyte 社区的大量开源 connectors，快速实现将 HStreamDB 和任意系统集成。本月 HStream IO 已经完成设计和前期开发工作，并将在 v0.9 中正式发布。

## 客户端更新

### 新增 Python 客户端

本月我们也启动了 HStreamDB 的 Python 客户端 hstreamdb-py 的研发工作，支持 Python3.7 及以上版本，并将于下月正式发布。

### hstreamdb-erlang v0.1 发布

本月 HStreamDB 的 Erlang 客户端 hstreamdb-erlang 正式发布 v0.1，具体使用可参考 [https://github.com/hstreamdb/hstreamdb-erlang/blob/main/README.md](https://github.com/hstreamdb/hstreamdb-erlang/blob/main/README.md) 

## 部署方式更新

### 新增基于 Helm 的部署支持

Helm ([https://helm.sh/](https://helm.sh/)) 能够帮助用户更容易的安装和管理 K8s 应用，本月 HStreamDB 也提供了基于 Helm 的部署支持，具体可参考文档 [https://hstream.io/docs/en/latest/deployment/deploy-helm.html#building-your-kubernetes-cluster](https://hstream.io/docs/en/latest/deployment/deploy-helm.html#building-your-kubernetes-cluster) 

### 新增阿里云 Terraform 部署支持

此前我们提供了基于 Terraform 在 AWS 和 华为云上部署 HStreamDB 的教程，本月我们又新增了对阿里云的部署支持，具体可参考文档 [https://hstream.io/docs/zh/latest/deployment/deploy-terraform-aliyun.html](https://hstream.io/docs/zh/latest/deployment/deploy-terraform-aliyun.html) 

> [1]：Das, A., Gupta, I. and Motivala, A., 2002, June. Swim: Scalable weakly-consistent infection-style process group membership protocol. In *Proceedings International Conference on Dependable Systems and Networks* (pp. 303-312). IEEE.
