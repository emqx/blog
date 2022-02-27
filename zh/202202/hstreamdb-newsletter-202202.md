本月，我们发布了 HStreamDB v0.7， 该版本致力于提升 HServer 集群的稳定性、可用性以及可扩展性。v0.8 将延续这一主要目标，并提供更多客户端，为更多用户的开发和使用带来便利，同时将加强安全特性。

[HStreamDB](https://hstream.io/zh) 正在变得愈发成熟、稳定、可用，未来将在越来越多的实际生产项目中发挥价值。欢迎大家体验试用：[https://github.com/hstreamdb/hstream](https://github.com/hstreamdb/hstream)。

## v0.7 版本发布

[本月 11 日的推送文章中](https://www.emqx.com/zh/blog/hstreamdb-v-0-7-release-notes)，我们详细介绍了 v0.7 版本新增的有效缓解单点流量瓶颈的透明分区功能、全新运维管理工具 HAdmin 、支持服务端集群和透明分区的新版 hstreamdb-java、基于一致性哈希的集群负载均衡算法等新的特性，以及一些使用和部署方面的改进等。

详细的使用方法可以阅读我们的文档：[https://hstream.io/docs/en/latest/start/quickstart-with-docker.html](https://hstream.io/docs/en/latest/start/quickstart-with-docker.html) 

## 本月开发进展

### Golang Client

为了方便不同技术栈和编程语言背景的用户使用 HStreamDB，我们将为多种主流语言提供 HStreamDB Client，包括：Java、Python、Golang 等。其中 Java 客户端是我们最早支持的客户端，各项功能目前也比较完善，也在持续改进和维护中。

本月我们新启动了 Golang Client 的开发工作，目前基本的功能已经实现完毕，首个版本预计下月正式发布。

Python Client 也将在后续发布。

其它更多语言的支持也在陆续规划中，欢迎大家进行建议和反馈。由于 HStreamDB 采用 GRPC 和客户端进行通信，得益于 GRPC 广泛的语言支持和工程便利性，使得开发新语言客户端的成本大大降低，也欢迎社区的伙伴们尝试开发新客户端。

### 基于 TLS 的连接加密、身份认证等安全特性

此前 HStreamDB 主要聚焦于核心功能的开发，还没有对安全方面的特性进行相关支持。考虑到用户在生产环境（比如公有云，私有云等）部署时的安全性需求，本月开始我们启动了相关安全功能的开发，主要涉及连接加密、身份认证和权限管理等方面。

目前已经初步完成了基于广泛使用的安全协议 TLS 的连接加密，双向身份验证的功能支持，这些功能预计在 v0.8 和大家正式见面。

### 提高测试覆盖率，搭建长期测试加强产品稳定性

在开发新功能的同时，我们也始终致力于提升 HStreamDB 的稳定性：通过增加更多的功能测试和行为测试，覆盖更多使用场景，同时也将进一步遵循 chaos engineering 的理念，加强多种条件下的随机错误注入测试，并提高对应的错误注入频率。

为了模拟 HStreamDB 在生产环境中的表现，确保实际的稳定可用，本月我们开始着手搭建和维护一个长期运行的 HStreamDB 集群，并开发一套用户日常应用的模拟程序，通过这个程序 7 x 24 小时持续操 HStreamDB 集群。我们将持续监控这个集群的长期运行状态，提前发现并解决可能存在的问题，提升 HStreamDB 的长期稳定性。

### 基于 Terraform 的快速部署

此前 HStreamDB 提供了快速[集群部署的脚本](https://hstream.io/docs/zh/latest/deployment/quick-deploy-ssh.html)以及对基于 k8s 部署的初步支持[[link](https://hstream.io/docs/en/latest/deployment/deploy-k8s.html)]。为进一步方便用户基于云环境快速部署和测试 HStreamDB，本月我们新开发了基于 Terraform 的部署方案，稍后会将具体的部署指引更新在文档上。

Terraform 是一款由 HashiCorp 主导开发的开源「基础设施即代码」工具，可以帮助开发及运维人员以自动化和可重现的方式来管理基础架构和资源，高效管理云服务。通过 Terraform，不仅可以快速实验和测试，还能更方便地将 HStreamDB 部署到多种公有云和私有云上，并且由于 Terraform 的不可变基础架构设计，可以避免配置偏离。
