本月我们发布了 HStreamDB 0.11，修复了多项已知问题。同时也在继续推进 HStream Platform 的开发，并计划于下月底上线首个 Alpha 版本。


## v0.11 发布

随着 HStreamDB 项目的日益成熟，为了更好地适应项目发展，我们决定逐渐缩短发版周期，以更快的速度进行迭代。因此，继上月底我们发布 v0.10 之后，本月我们又发布了 v0.11，主要带来了以下更新和问题修复：

- 调整 HServer 的启动参数 `host` 和 `address` 为 `bind-address` 和 `advertised-address` ，使它们更容易被理解和使用
- 移除 HServer 端的压缩选项，目前推荐使用端到端压缩功能
- 统一内的资源命名规则并改进了相应的资源命名校验
- 新增对获取 stream 和 subscription 的创建时间的支持
- 修复对部分 Client 的 RPC 请求的路由校验
- HStream CLI 新增 subscription 子命令
- 修复提交 subscripton 进度可能失败的问题
- 修复 query 的 join 可能产生错误结果的问题
- 修复写操作超时不可重试的问题


## hdt 新增对 ELK Stack 的部署支持

hdt 是 HStreamDB 的自动化集群部署工具，目前它除了能在多个节点上快速部署 HStreamDB 的核心组件外，还支持同时可选地部署 Promethus、HStream Exporter、Grafana 等监控组件。

为了更方便用户部署测试以及观测 HStreamDB 集群，本月 hdt 新增了支持通过部署 ELK Stack 来收集和查询 HStreamDB 的运行日志，如果启用了相应选项，hdt 在部署的过程中会自动配置好 Logstash 将 HStreamDB 集群的日志导入 ElasticSearch，并提供默认的 Kibana 面板。

![Kibana 面板](https://assets.emqx.com/images/f4386bda64016de907156916f5fd5316.png)


## HStream Platform 即将上线

HStream Platform 是我们即将推出的基于公有云的 **Serverless** 流数据平台服务，提供免部署、零运维、高可用、一站式的流数据存储、实时处理和分析服务。

HStream Platform 的首个 Public Alpha 版本计划将于**下月底**上线，届时将提供免费的注册试用，敬请期待！您也可以在 [![img](https://hstream.io/favicon-16x16.png)The Next-Gen Streaming Data Platform in the Cloud](https://hstream.io/cloud)  提前注册，第一时间获取上线通知。
