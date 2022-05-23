> 开源之夏（OSPP）是由中科院软件所「开源软件供应链点亮计划」发起的、面向高校学生的暑期开源活动，旨在鼓励在校学生积极参与开源软件的开发维护，促进优秀开源软件社区的蓬勃发展，培养和发掘更多优秀的开发者。 
>
> 学生可自主选择感兴趣的项目进行申请，中选后将获得该软件资深维护者（社区导师）亲自指导。根据项目的难易程度和完成情况，参与者还将获取开源之夏活动奖金和结项证书。
>
> 开源之夏官方主页：[https://summer-ospp.ac.cn/](https://summer-ospp.ac.cn/) 

今年，EMQ 将携 EMQX、MQTT X、LF Edge eKuiper 三大开源项目首次参加开源之夏！

## 三大开源项目介绍

### EMQX ：开源云原生分布式物联网 MQTT 消息服务器

EMQX 是一款大规模可弹性伸缩的云原生分布式物联网 MQTT 消息服务器，高效可靠连接海量物联网设备，高性能实时处理消息与事件流数据。诞生至今，EMQX 获得 GitHub star 数量近 1 万，在全球范围内拥有 20,000+ 用户，累计连接超过 1 亿台物联网设备。在所有采用 Erlang 语言的开源项目中，EMQX 受欢迎程度位列全球前三。

GitHub 主页：[https://github.com/emqx/emqx](https://github.com/emqx/emqx) 

### MQTT X ：优雅的跨平台 MQTT 5.0 开源桌面客户端工具

MQTT X 是一款完全开源的 MQTT 5.0 跨平台桌面客户端。支持快速创建多个同时在线的 MQTT 客户端连接，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的连接、发布、订阅功能及其他 MQTT 协议特性。它基于 Electron 并使用 TypeScript 开发，前端框架使用的是 Vue.js，数据库采用的是 SQLite。

GitHub 主页：[https://github.com/emqx/MQTTX](https://github.com/emqx/MQTTX) 

### LF Edge eKuiper：超轻量物联网边缘数据流式分析引擎

LF Edge eKuiper 是 Golang 实现的轻量级物联网边缘分析、流式处理开源软件，可以运行在各类资源受限的边缘设备上。eKuiper 设计的一个主要目标就是将在云端运行的实时流式计算框架（比如 Apache Spark 、Apache Storm和 Apache Flink等）迁移到边缘端。该项目最初由 EMQ 发起，目前已正式加入 LF Edge 基金会。

GitHub 主页：[https://github.com/lf-edge/ekuiper](https://github.com/lf-edge/ekuiper) 

## 5 款课题开放申请

在本届「开源之夏」中，EMQ 团队根据以上三个开源项目的开发进度及未来发展规划，共开放了从基础到进阶 5 个难度不同的开发项目，涉及前端、SQL 语法、流式计算等多个方向供同学们选择。每个项目均由所属开源软件的核心研发工程师指导，这个夏天一起来见证物联网世界的美好改变吧！

### EMQX 旗下项目

**MQTT-SN 客户端实现**

项目描述：当前整个 Erlang 生态都没有 MQTT-SN 客户端库的实现。因此需要新增一个 Erlang 的客户端实现来完善 EMQX 对 MQTT-SN 测试和应用。

项目导师：何建波 （hejb@emqx.io）

项目难度：进阶/Advanced

申请地址：[https://summer-ospp.ac.cn/#/org/prodetail/226dc0339](https://summer-ospp.ac.cn/#/org/prodetail/226dc0339) 

**EMQX 规则引擎 SQL 语法增强**

项目描述：规则引擎是用于配置 EMQX 消息流与设备事件的处理、响应规则。其不仅提供了清晰、灵活的「配置式」的业务集成方案，简化了业务开发流程，提升用户易用性，降低业务系统与 EMQX 的耦合度；也为 EMQX 的私有功能定制提供了一个更优秀的基础架构。本项目将为 EMQX 规则引擎的 SQL 语法添加 Map/Reduce 语法。

项目导师：小新（[506895667@qq.com](mailto:506895667@qq.com)）

项目难度：进阶/Advanced

申请地址：[https://summer-ospp.ac.cn/#/org/prodetail/226dc0430](https://summer-ospp.ac.cn/#/org/prodetail/226dc0430) 

### MQTT X 旗下项目

**Electron 桌面客户端软件的自动更新**

项目描述：MQTT X 目前已经支持并提供了完整的 MQTT 协议的功能测试能力，需要一些针对前端和网络功能方面的优化，使其更加完整易用。本项目将为 MQTT X 添加一些可自动更新版本的功能，程序内更新后显示新版本的发布日志等的功能，用户可以减少一些手动操作来更快体验和使用到后续新版本的功能，从而提升整体的软件使用体验。

项目导师：ysfscream（[yusf@emqx.io](mailto:yusf@emqx.io)）

项目难度：基础/Basic 

申请地址：[https://summer-ospp.ac.cn/#/org/prodetail/22bbe0141](https://summer-ospp.ac.cn/#/org/prodetail/22bbe0141) 

### LF Edge eKuiper 旗下项目

**流式计算窗口函数优化探索**

项目描述：窗口函数是流式计算的核心概念之一，也是开源边缘流式计算引擎 eKuiper 常用的功能之一。eKuiper 实现了几种常见的时间窗口和计数窗口，但是目前对于较长时间的窗口的优化仍较为欠缺。流式计算窗口的使用场景多种多样，业界和学术界已有较多的研究和优化方案。本项目的目标是对任一窗口函数的性能和资源占用进行优化。完成项目可以帮助开发者更深入地理解流式计算、大数据领域和数据库 SQL 引擎等方面的通用知识并应用于今后的工作学习中。

项目导师：hjy（[huangjy@emqx.io](mailto:huangjy@emqx.io)）

项目难度：进阶/Advanced

申请地址：[https://summer-ospp.ac.cn/#/org/prodetail/2234b0180](https://summer-ospp.ac.cn/#/org/prodetail/2234b0180) 

**WASM 函数扩展**

项目描述：WebAssembly 或者 WASM 是一个可移植、体积小、加载快并且兼容 Web 的全新格式。目前，WASM 技术的应用越来越广泛，并逐步扩展到边缘计算应用（如 WasmEdge 应用）。本项目的目标是利用 WASM 的 go SDK，完成 eKuiper SQL 调用 WASM 函数的功能，方便用户使用 WASM 函数扩展 eKuiper 的处理能力。

项目导师：冉见祥（[rxan_embedded@163.com](mailto:rxan_embedded@163.com)）

项目难度：基础/Basic

申请地址：[https://summer-ospp.ac.cn/#/org/prodetail/2234b0182](https://summer-ospp.ac.cn/#/org/prodetail/2234b0182) 

## 如何参与「开源之夏」？

### 申请资格

- 本活动面向年满 18 周岁的在校学生。
- 暑期即将毕业的学生，只要在申请时学生证处在有效期内，就可以提交申请。
- 海外学生可提供录取通知书/学生卡/在读证明等证明学生身份。

### 参与方式

学生可以自由选择项目，与社区导师沟通实现方案并撰写项目计划书。所提交项目申请书被选中的学生，将在社区导师指导下按计划完成开发工作，并将成果贡献给社区。社区评估学生的完成度，主办方根据评估结果发放活动奖金给学生。

学生参与指南：[https://summer-ospp.ac.cn/help/student/](https://summer-ospp.ac.cn/help/student/) 

### 参与流程

![开源之夏参与流程](https://assets.emqx.com/images/80a35c3a4b7a8f1aae4953c2af644114.png)
 
如果你对以上项目开发感兴趣，欢迎通过邮件的方式联系项目相应的导师咨询项目详细信息，EMQ 期待与你相约在这个夏天！
