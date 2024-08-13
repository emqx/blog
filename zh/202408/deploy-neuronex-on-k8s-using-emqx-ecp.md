随着物联网、边缘计算技术的发展，实现边缘服务的快速部署对于分布式计算环境至关重要。它不仅可以显著降低延迟、节省带宽资源、增强数据的安全性和隐私保护，同时还能改善用户体验，支持动态变化的工作负载需求，提供更高的灵活性和可扩展性，并带来成本效益。

[EMQX ECP](https://www.emqx.cn/products/emqx-ecp) 作为一款工业互联数据平台，能够满足工业场景大规模数据采集、处理和存储分析的需求，提供边缘服务的快速部署、远程操作和集中管理等功能，以数据 + AI 驱动生产监测、控制和决策，实现智能化生产，提高效率、质量和可持续性。

7 月 12 日，EMQX ECP 发布了 2.3.0 版本，新增在 K8s 上的快速部署 [NeuronEX](https://www.emqx.cn/products/neuronex) 服务的功能，本文将详细介绍该功能的原理和使用方法，帮助用户在 ECP 中更便捷地管理 NeuronEX 服务。

## 功能介绍

![K8s 上安装 NeuronEX](https://assets.emqx.com/images/75560a50066567f875c946617882401e.png)

<center>K8s 上安装 NeuronEX</center>

<br>

如上图所示， 在 ECP 上添加 NeuronEX 的时候可以选择多种方式。包括添加一个现有服务，批量安装新服务，批量导入现有服务。本文主要讲解批量安装新服务中的 K8s 安装方式， 基于 Docker 的安装方式将在未来的文章中介绍。

首先，在批量安装方式中选择 K8s，可安装的服务类型目前只有 NeuronEX，给要安装的服务取一个名称簇，并指定要安装的服务数量，选择 NeuronEX 要使用的镜像版本。

其次，用户可以选择是否开启所安装 NeuronEX 服务的认证功能。选择开启，则访问 NeuronEX 的 API 需要 Jwt 鉴权， ECP 访问 NeuronEX 会自动添加 Jwt token；选择不开启， 则对 NeuronEX 的 API 访问不做限制。

此外，用户也可以结合实际的业务需求，给要安装的 NeuronEX 服务添加标签名和描述属性，填好属性值后，点击右上角的确认，即可开始安装过程。 

![批量安装结果](https://assets.emqx.com/images/a0fc49c2712baf173577b622e7e6043d.png)

<center>批量安装结果</center>

<br>

在弹出的批量安装结果页中，用户可以实时看到所有的 NeuronEX 的安装状态。安装完成后回到列表页， 可以看到刚刚安装好的 NeuronEX 服务。 从列表页，用户可以判断 NeuronEX 服务的离线、在线状态，版本和连接方式等信息。

在列表页中，用户还可以对这些 NeuronEX 服务执行重启、停止、删除、修改点位数等等功能。 其中，修改点位数功能可以动态调整对应 NeuronEX 的 License 中授权的 tag 数量。

![NeuronEX 列表页](https://assets.emqx.com/images/7753af2bbad1f55e2b8d6a739934b2e4.png)

<center>NeuronEX 列表页</center>

<br>

![ECP 集成 NeuronEX Dashboard](https://assets.emqx.com/images/6968ef27506245f74279942d394c7aa1.png)

<center>ECP 集成 NeuronEX Dashboard</center>

<br>

在列表页上点击对应 NeuronEX 的详情按钮， 也可以直接通过 ECP 的 Dashboard 访问到该 NeuronEX 的 Dashboard，效果和直接操作 NeuronEX 的 Dashboard 保持一致。

## 实现原理

为了能在 K8s 上部署 NeuronEX 服务， 我们开发了 NeuronEX-Operator 用于在 K8s 上维护 NeuronEX 服务的全生命周期。在K3s 等其它类 K8s 环境同样适用。 

![ECP 配置 KubeConfig 和硬件配额](https://assets.emqx.com/images/eaf561deecf56388681a92c80f8062b5.png)

<center>ECP 配置 KubeConfig 和硬件配额</center>

<br>

为了使 ECP 可以和 K8s API-Server 交互，使用该功能前，需要在 ECP 的系统设置中配置好 KubeConfig 文件，KubeConfig 中配置的用户需要有 Namespace \ NeuronEX \ Service 的list\create\delete\update\watch\get 权限，和 Pod \ Deployment \ StatefulSet 的 list\get\watch 权限。

除了 KubeConfig 文件外，用户也可以在 ECP 系统设置中配置 NeuronEX 的硬件资源使用限额(CPU\Memory\Storage)， 在执行批量安装操作的时，可以在右上角看到当前消耗的总的硬件资源量。

![ECP 配置镜像仓库和镜像版本](https://assets.emqx.com/images/8b8603e2a3909e5372307ecda4b1e632.png)

<center>ECP 配置镜像仓库和镜像版本</center>

<br>

如上图所示，用户可以在系统设置中配置服务的容器镜像仓库地址和仓库鉴权信息，当 K8s 拉取镜像时，会自动使用该权限信息。此外，还可以配置 NeuronEX 服务的镜像名和镜像版本，以供安装时选择。

![NeuronEX CR](https://assets.emqx.com/images/c23b5cf0f399c771e6b11f9642dbe1e1.png)

<center>NeuronEX CR</center>

<br>

NeuronEX-Operator 在 K8s 上定义了名为 NeuronEX 的 CRD 自定义资源对象。NeuronEX 这个 CRD 中定义了镜像版本、镜像拉取规则、Jwt 鉴权文件名和文件内容、持久化目录的大小。 其中 jwt 鉴权文件可以同时挂载多个并且同时生效。 当您在 ECP 上创建 NeuronEX 服务时， ECP 会根据用户的需求去创建 NeuronEX CRD 的资源对象，然后将其提交给 K8s, NeuronEX-Operator 探测到新的 NeuronEX CRD 的资源对象后会自动创建对应的 Deployment 和 Service 等资源， 具体内容见下图。

![K8s 上的资源对象](https://assets.emqx.com/images/f738ce51d75a14f1bdf49707c06974b6.png)

<center>K8s 上的资源对象</center>

<br>

NeuronEX 服务就绪后， ECP 会通过 K8s 的 Service 对象的内网域名去连接纳管该 NeuronEX 服务。 纳管时， ECP 会下发指标、告警、探活等的配置给 NeuronEX， 让 NeuronEX 可以按配置去定时上报自身的状态。 纳管成功后， ECP 服务列表页中可以看到对应的 NeuronEX 的状态为在线状态， 连接类型为托管-K8s 直连。

## 总结

上文介绍了 EMQX ECP 在 K8s 上快速部署 NeuronEX 的方法及其原理。部署完成后， ECP 会自动纳管这些 NeuronEX 服务， 用户可以直接在 ECP 的页面上对这些 NeuronEX 服务进行管理或业务配置和使用。此外， 用户还可以在 ECP 上对这些 NeuronEX 服务执行重启、停止、删除等生命周期管理，并统一根据业务需求动态分配所有 NeuronEX 服务 license 的 tag 数量，进一步提升运维效率。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
