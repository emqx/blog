本月，XMeter 团队致力于企业版 3.2.5 的研发。XMeter 3.2.5 版本将推出新的基于 Docker 的安装方式，降低安装难度，简化部署步骤，助力用户以更便捷的方式使用 XMeter 企业版。此外，企业版的测试数据处理引擎也将进行升级，还对测试报告页面进行了改进。

## 基于 Docker 的全新部署方式

XMeter 企业版由主控和压力机集群组成。主控通常包含 master 和 asteroid 两台服务器（如果只用于小规模性能测试，也可将 master 和 asteroid 安装在同一台服务器上），提供测试管理、测试调度、测试数据收集处理的功能。压力机集群中部署多台服务器，接收主控的调度，执行具体的压测任务，并将原始结果数据上报到主控。

在 XMeter 企业版 3.2.4 及更早版本中，主控的压力机集群都是直接安装部署在虚拟机或物理机上，实际执行测试时，每台压力机根据测试任务的大小，启动若干个容器，容器中将运行改造过的 JMeter 应用，完成分配到的测试任务部分。XMeter 企业版为了提供完善的测试管理与测试执行的功能，使用了不少开源组件用于数据存储、高速缓存、消息交互、日志收集、报告展现，在安装时需要依次安装各个依赖组件和 XMeter 测试服务，处理好各组件与服务之间的依赖关系，并对文件系统进行相应的配置。这为 XMeter 企业版的安装带来了一定难度。

为帮助用户解决企业版部署困难的难题，3.2.5 版本将简化安装作为产品重心。我们将使用 Docker 来部署各个依赖组件和 XMeter 测试服务，将整个 XMeter 企业版划分为 master、asteroid、压力机三个容器集群。每个容器集群都使用 Docker-compose 对其中的多个容器进行编排管理。

如果需要在内网环境中进行安装，用户只需确保 XMeter 依赖的开源组件容器镜像存在于内网镜像仓库中，并下载获取 XMeter 的容器镜像，将安装参数针对实际需要进行必要的适配调整，运行 Docker-compose 命令即可快捷地完成 XMeter 企业版的部署。

如果需要在公有云上进行安装，我们还为主要的公用云提供了使用 Terraform 进行部署的方式，快速定义编排基础资源，并在基础资源创建完成后，自动部署 Docker-compose 中的各个容器集群，从零开始，轻松完成 XMeter 企业版的安装。

## 测试数据处理引擎优化

3.2.5 版本中，修复了汇总数据在某些偶发情况下的统计错误，对 90 百分位响应时间的处理进行了优化，并新增了 50 百分位、75 百分位、95 百分位、99 百分位等多个分位的响应时间数据，用户可通过我们提供的 Grafana 仪表面板查看这些分位的相关数据。

## 其他更新

进行复杂场景测试时，测试中有可能会包含很多个事务或请求。为方便用户快速切换希望查看的事务请求相关数据折线图，测试报告页面「自定义选择事务」功能新增了名称筛选框，帮助用户从大量事务请求中定位所需的内容。

对失败数极少、失败占比极低的事务请求，我们也对测试明细数据的展示进行了优化，以更直观的方式呈现这些测试中的失败率、成功率。



<section class="promotion">
    <div>
        免费试用 XMeter Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 负载测试云服务，无需部署，一键提交测试</div>
    </div>
    <a href="https://www.emqx.com/zh/products/xmeter" class="button is-gradient px-5">开始试用 →</a>
</section>
