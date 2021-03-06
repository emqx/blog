六月，XMeter 发布了企业版 3.2.3 版本。这个版本仍保留了非 Kubernetes 的测试机部署方式，即在多台物理机或虚机上预安装 XMeter 的测试代理 DCM，以构建可水平扩展的测试机集群。近期暂无计划使用 Kubernetes 容器集群的企业，可以继续延用 3.2 系列的 XMeter，以获取最新的产品优化和问题修复。

## 错误日志查看体验提升

3.2.3 版本中对错误日志进行了以下调整：

**优化现有错误日志树状展示结构**

3.2.3 版本之前的错误日志树状展示中，不同的测试机发压中产生的相同错误，也有可能展示为多个节点，并且每个节点都会附带容器 ID 信息。

考虑到这样的展示方式容易导致歧义，3.2.3 版本中对多个测试机中产生的相同错误进行了合并，树状展示结构中也不再包括容器信息，只包含线程组-事务-请求的层级结构。

![优化现有错误日志](https://assets.emqx.com/images/f652bf28d4244738cb6b5e95089f3dff.jpeg)
 

**新增错误分析统计表**

从测试报告页面的「错误日志」标签页中，即可查看该统计表。

错误分析统计表中，每个事务/请求下，不同的错误按出现次数从高到低依次展现。展现内容包括：该种错误出现的总次数、在所属事务/请求的全部错误中所占的比例、错误的响应码和响应内容等详细信息。

默认的统计表包含测试中的全部事务/请求，如果只希望查看部分事务/请求，可以通过点击「选择事务」按钮，勾选所需的事务/请求。

![新增错误分析统计表](https://assets.emqx.com/images/6cfd31261eff89c22b7b3dd6ee3a08c3.png)

## 测试报告图表优化

测试报告图表包含三部分：测试整体数据、多个维度的折线图、具体事务/请求的测试明细数据。经过最近几个版本的迭代，测试图表的优化内容主要有：

- 框选折线图时，支持三个部分的数据联动
- 折线图提供全选/反选功能
- 在测试运行中框选折线图，将暂停图表的定时刷新，以解决与框选功能的冲突；取消框选后自动恢复定时刷新
- 虚拟用户数折线图只展现所选的事务/请求所在的线程组虚拟用户
- 修复导出测试报告和导出电子表格报告时 csv 及截图不完整的问题

![XMeter 测试报告图表优化](https://assets.emqx.com/images/062587376c469c18c5c90b87d730b6f7.png)

## 其他优化与修复

- 阶梯测试插件、ZooKeeper、RabbitMQ 等依赖软件升级版本
- 修复压力机使用统计图表中时间戳不正确问题
- 修复重新上传过的脚本打开旧的测试报告有时无法正常显示的问题
- 修复吞吐量加压探索报警邮件发送频率有时与预设不一致的问题

## 即将到来

XMeter Cloud 测试服务的新版本开发也在进行中，即将上线。XMeter Cloud 希望为海内外客户提供易用的 IoT SaaS 测试服务，降低测试部署和运维成本。新版本将提供免费试用，以便大家快速体验性能测试服务，敬请期待。
