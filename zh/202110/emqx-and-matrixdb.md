随着数据价值逐渐得到普遍认可，数据资产也成为一个重要议题。万物互联的物联网时代下，大量数据的采集、存储以及合理利用成为企业打造数字资产平台的三大难点。

作为一家[物联网数据基础设施软件提供商](https://www.emqx.com/zh)，**EMQ** 始终以物联网数据价值最大化为目标，构建为物联网数据特征而设计的基础软件，实现物联网数据的统一「连接、移动、处理、分析」，服务企业数字化、实时化、智能化转型。核心产品云原生分布式物联网接入平台 EMQX，以一体化的分布式 [MQTT 消息服务](https://www.emqx.com/zh/products/emqx)和强大的 IoT 规则引擎，为高可靠、高性能的物联网实时数据移动、处理和集成提供动力。

[MatrixDB](https://www.ymatrix.cn) 是由现代数据仓库领导者 yMatrix（北京四维纵横数据技术有限公司）自主研发的全球首款 PB 级超融合时序数据库，在稳定支撑传统数据库场景的同时，能够充分满足物联网场景下快速采集、高效存储、实时分析以及深度学习（ML+AI）的需求。

EMQX 与 MatrixDB 的组合技术栈能够胜任物联网场景中的各类数据需求，为万物互联的智能时代提供坚实、简洁的智能数据核心基础设施，针对物联网、车联网和工业互联网等领域打造完整解决方案，共同协助企业完成企业数字资产平台的建设。

![EMQ 物联网数据接入平台架构](https://assets.emqx.com/images/31113cabcf077ba6e8f4f16eee8a4d83.png)

## EMQX 对接 MatrixDB 具有以下四大优势：

- EMQX 稳定承载大规模的 MQTT 客户端连接，单服务器节点支持 50 万到 100 万连接。并且支持分布式节点集群，快速低延时的消息路由，单集群支持 1000 万规模的路由。
- EMQX 支持完整物联网协议，MQTT、MQTT-SN、CoAP、LwM2M、WebSocket 和私有协议。
- MatrixDB 吞吐量极强，能更高效消费 EMQX 的消息。
- MatrixDB 不仅是一款优秀的时序数据库，数据分析能力也很强，可以实现一库搞定数据接入与分析场景。

此外，我们也对该方案进行了性能评测。高性能物联网接入平台 EMQX 和高性能分布式时序数据库 MatrixDB 实现完美对接，JDBC INSERT 模式下单机吞吐量达到了 21  万行/秒。这一方案完美解决了高频数据端到端的高并发高可靠写入和高并发秒级查询两大难题，提供更加友好的体验，实现国产技术生态的完整闭环。我们相信，EMQX 与 MatrixDB 的强强联合，可以为更多企业带来不同场景下的物联网数字平台搭建方案，帮助企业牢牢把控数据、利用数据，从数据中获益。



**附：详细测试报告**

## 测试工具

本次测试工具使用 [XMeter](https://www.xmeter.net/) 性能测试平台。

XMeter 是基于开源测试工具 [JMeter](https://www.emqx.com/zh/blog/introduction-to-the-open-source-testing-tool-jmeter) 扩展的性能测试平台。针对物联网具有的接入规模大、弹性扩展要求、多种接入协议、混合场景等特点，XMeter 对 [JMeter](https://www.emqx.com/zh/blog/introduction-to-the-open-source-testing-tool-jmeter) 进行了改造，实现了百万级别并发测试支持，并对测试数据进行实时处理并图形化展示。

本次使用的版本是 XMeter 企业版 v3.0.0。

## 测试环境

华为云，北京四区 VPC 内网

EMQX 集群、MatrixDB 配置：

| 节点     | 数量 | 版本         | 操作系统 | CPU  | 内存 | 硬盘 |
| -------- | ---- | ------------ | -------- | ---- | ---- | ---- |
| EMQX    | 3    | 企业版v4.3.0 | CentOS7  | 32核 | 64G  | 40G  |
| MatrixDB | 1    | 企业版v4.0.2 | CentOS7  | 32核 | 64G  | 100G |
| XMeter   | 5    | 企业版v3.0.0 | CentOS7  | 16核 | 32G  | 40G  |

## 部署架构图

![部署架构图](https://assets.emqx.com/images/50a20795245eca1727291d00e98ec5d7.png)

## 测试方法

测试语句如下：

```
INSERT INTO
	emqx_data
VALUES
	(
		to_timestamp(${p.ts} / 1000),
		${p.tagid},
		${p.altitude},
		${p.azimuth},
		${p.uv1},
		${p.temperature},
		${p.humidity},
		${p.rainfall},
		${p.pressure},
		${p.wind},
		${p.wind_direction},
		${p.wind_direction_rotate},
		${p.visibility}
	)
```

payload 为 json 格式，如下所示：

![payload](https://assets.emqx.com/images/2814c9c6d0ffe4d585b093fd10ea528f.png)

## 规则引擎

### 1、资源设置

连接池大小32

![连接池大小32](https://assets.emqx.com/images/07bff69acb38621487c96f2b6695696c.png)

### 2、规则设置

启用批量插入，最大批量数1000，异步插入

![规则设置](https://assets.emqx.com/images/07c9342bf5330dd63fb991f1785bfc3c.png)

## 测试结果

### 1、吞吐量

从下图统计信息可以看出，EMQX 对接 MatrixDB 吞吐量达到了 21 万行/秒。

![吞吐量](https://assets.emqx.com/images/823baebd9ea5a10e7498e518467a2b4a.png)

### 2、机器资源消耗

| 节点     | CPU idle | CPU user | Memory free | Memory used                      |
| -------- | -------- | -------- | ----------- | -------------------------------- |
| EMQX    | 25%~30%  | 61%      | 59G         | 3.3G                             |
| MatrixDB | 28%      | 37%      | 1.6G        | 24G(数据库缓存+操作系统文件缓存) |

### 3、结论

- EMQX 对接单节点 MatrixDB，以直接 INSERT 方式插入数据，吞吐量可以达到每秒 21 万行
- EMQX 和 MatrixDB 所在机器的资源使用稳定

这些指标表明 EMQX 集群在使用 INSERT 方式向 MatrixDB 灌入数据时， 吞吐量很高。另外，MatrixDB 还提供了 MatrixGate 数据加载工具，相比使用 INSERT 方式加载数据，还有 10 倍- 100 倍的提升空间。



> **关于 yMatrix**
>
> 北京四维纵横数据技术有限公司（yMatrix）是全球超融合时序数据库的开创者，是现代数据仓库的领导者。基于多项专利技术自主研发的数据库产品 MatrixDB，为全球首款 PB  级超融合时序数据库，同时完美支持传统的关系型数据和物联网海量时序数据；在稳定支撑传统数据库场景的同时，能够充分满足物联网场景下快速采集、高效存储、实时分析以及深度学习（ML+AI）的需求，开创了现代实时数据仓库方向，为万物互联的智能时代提供坚实、简洁的智能数据核心基础设施。
>
> **关于 MatrixDB**
>
> MatrixDB  是全球首款同时支持在线事务处理（OLTP）、在线分析处理（OLAP）和物联网时序应用的超融合型分布式数据库产品，具备严格分布式事务一致性、水平在线扩容、安全可靠、成熟稳定、可视化管理、兼容 PostgreSQL/Greenplum  协议和生态等重要特性。为万物互联的智能时代提供坚实、简洁的智能数据核心基础设施，为物联网应用、工业互联网、智能运维、智慧城市、实时数仓、智能家居、车联网等场景提供一站式高效解决方案。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
