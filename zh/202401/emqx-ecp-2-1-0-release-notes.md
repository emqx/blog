EMQX ECP 工业互联数据平台 2.1.0 版本现已正式发布。新版本优化了安装过程、提升与边缘软件 NeuronEX 的集成能力，并强化监控告警体系，为用户提供更简单、强大的工业数字化解决方案。

## 优化安装部署流程

ECP 2.1.0 优化了安装包及安装过程，降低了部署 ECP 的复杂性。让用户可以更轻松地完成安装，并更快速地投入使用。

![新版 Docker Compose 安装步骤](https://assets.emqx.com/images/a5c201dc9dec6a0615b8bfe8dffbd83b.png)

<center>新版 Docker Compose 安装步骤</center>

<br>

新版本 ECP 安装包下载地址如下，欢迎下载试用：[https://www.emqx.com/zh/try?product=emqx-ecp](https://www.emqx.com/zh/try?product=emqx-ecp)。

## 强化与 NeuronEX 的集成

新版本引入了全新的架构和实现，使其能够更加方便、灵活地与工业边缘软件 NeuronEX 集成，为用户提供更一体化的工业互联体验。通过重新设计，实现了 ECP 与 NeuronEX 之间的探活机制，提升了两者之间的通信效率和稳定性。

## 优化监控告警体系

在 ECP 2.1.0 版本中， 我们重新设计了当前的告警及历史告警判断逻辑，支持用户自定义告警规则。这使得告警系统更加灵活，能够更好地满足不同用户的需求。同时，我们也优化了告警推送功能，现在可以通过标签分组推送告警信息，使用户能够更精准地获取关键信息。

![优化监控告警体系](https://assets.emqx.com/images/1fa4b6464e37adf692108c5a7759ced1.png)

## 边缘服务管理的优化

EMQX ECP 提供了对不同网络条件和不同接入方式的边缘服务，进行远程配置管理、实时状态监控、故障诊断、驱动及算法更新等操作的能力，简化现场运维工作。

ECP 2.1.0 版本针对”托管 - Docker 直连“类型的边缘服务进行了全面的优化升级，显著提升了边缘服务的性能和稳定性。此外，该版本还新增了边缘服务强制删除功能，使管理者可以更加灵活地进行服务管理。

![边缘服务管理的优化](https://assets.emqx.com/images/138ade47050105820947cd172d3c995f.png)

## 流程完善及易用性提升

本次更新还进一步优化了边缘服务的管理流程，包括对其纳入和取消管理的流程，使操作更加流畅和清晰。同时，我们对新安装的 ECP 配置项的默认设置进行了重新审视，以确保用户在初次使用时就能够获得最佳的体验。

## 结语

这次更新希望提升工业用户在数字化转型中的体验，帮助用户消除数据孤岛、降低运维成本、提升生产效率及质量。我们期待用户能够通过这一版本获得更多的便利和价值。欢迎前往 [ECP 官网](https://www.emqx.com/zh/products/emqx-ecp)下载最新版本，开始您的数字化之旅！

<section class="promotion">
    <div>
        免费试用 EMQX ECP
    </div>
    <a href="https://www.emqx.com/zh/try?product=emqx-ecp" class="button is-gradient px-5">开始试用 →</a>
</section>
