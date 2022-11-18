EMQX Kubernetes Operator 是 EMQ 发布的一个封装、部署和管理工具，也是一个特定的应用控制器，方便 DevOps 人员在 Kubernetes 上编排 EMQX MQTT 消息服务集群，管理其生命周期。

华为云原生基础设施（云容器引擎 CCE、容器镜像服务 SWR、容器洞察引擎 CIE、智能边缘平台 IEF 等）通过云原生服务中心 (Operator Service Center，OSC) 对外开放云原生能力，包括弹性伸缩、多云部署、云边协同、应用级自动化运维等，全面支持企业架构云原生化。

本文将介绍如何使用 EMQX Operator 在 OSC 上快速发布并提供基于大规模分布式物联网消息服务器 EMQX 的 MQTT 订阅服务，实现运维的代码化、自动化、智能化。

## OSC 介绍

OSC 是华为云面向服务提供商和服务使用者的云原生服务生命周期治理平台，提供大量开箱即用的云原生服务，支持服务的开发、发布、订阅、部署、升级、更新等，帮助用户简化云原生服务的生命周期管理。

![商品服务生命周期](https://assets.emqx.com/images/5537eba909bc7c1fa6119d6dc5728c24.png)


<center>商品服务生命周期</center>

OSC 具有以下优势：

- **开箱即用**

  OSC 联合生态伙伴提供了大量开箱即用的云原生服务，包括数据库、消息、缓存等通用中间件，以及新技术领域的 AI、大数据、高性能计算、边缘等应用，用户可以根据业务需要订阅。

- **全域部署**

  随着业务的发展，企业使用云服务部署场景在横向和纵向上都在不断拓展，横向上跨云部署成为业务常态，纵向上服务全域部署能力变得越来越重要，从核心区域和热点区域一直延伸到本地机房和业务现场。通过 OSC，用户可以将服务部署到与华为云连接的基础设施，例如部署在公有云不同 region 的容器集群和边缘集群。

- **高效开发、自动运维**

  容器化只是服务云原生化的第一步，服务部署之后需要治理，不仅包括监控、日志、告警等基本运维能力，还包括弹性伸缩、数据备份恢复、故障迁移、故障恢复等高级运维能力，这些能力是服务高 SLA 的必要条件。OSC 提供开箱即用的云原生运维能力，支持服务声明式对接，无需修改业务代码。

- **应用级视图**

  传统的运维方式应用比较原始，都聚焦在资源层级，没有应用统一视图。OSC 在实例详情页面可以查看本实例状态信息、配置信息、日志、监控信息，方便用户在一个页面查看实例相关的基础信息，无需切换到不同的运维平台。

- **兼容社区服务规范**

  OSC 服务规范兼容 Helm 和 Operator Framework 社区服务规范，Helm 和 Operator framework 是Kubernetes 生态中最常用的服务管理方式，很多已有的服务都是基于这两种方式开发，为了方便这些已有服务快速发布或者快速迁移到 OSC，使用 OSC 管理，OSC 的服务规范兼容 Helm 和 Operator Framework。

![OSC 与其他华为云服务的关系](https://assets.emqx.com/images/67d4c6b5943e867e0dee02bff6768af1.png)

<center>OSC 与其他华为云服务的关系</center>


## EMQX 介绍

### EMQX 企业版介绍

EMQX 企业版是一款「随处运行，无限连接，任意集成」企业级 MQTT 物联网接入平台，提供一体化的分布式 MQTT 消息服务和强大的 IoT 规则引擎，为高可靠、高性能的物联网实时数据移动、处理和集成提供动力，助力企业快速构建关键业务的 IoT 平台与应用。

![EMQX 企业版](https://assets.emqx.com/images/31e72d0e740305969042ce3a62d5c10e.png)

其具有如下特性：

- 多协议支持

  通过 MQTT、CoAP、LwM2M、WebSocket 或专有协议连接任何设备。

- 一站式接入

  将大规模分布式的 MQTT Broker 与强大的内置 IoT 规则引擎相结合。

- 关键业务可靠性

  为关键业务的物联网应用提供可靠的高性能数据移动、处理与集成。

- 灵活数据集成

  轻松、灵活地集成物联网数据到 Kafka、RDS，以及 SAP 等企业系统。

### EMQX Operator 介绍

Kubernetes Operator 是一种封装、部署和管理 Kubernetes 应用的方法。它使部署和运行应用所依赖的基础服务变得更简单。

![EMQX Operator](https://assets.emqx.com/images/48e136ef0354dc1f720593b90896a6c4.png)

EMQX Operator 实现了对 EMQX 生命周期的管理，其具有如下特性：

- 动态更新 EMQX 集群

   EMQX 集群运行时，更改集群实例配置，无需手动重启实例，服务无中断完成配置更新

- 弹性高可用

   可以在不中断业务的情况下扩展 EMQX 集群

- 热更新

   EMQX Operator 可以在不中断服务的情况下，帮助您快速、安全地升级 EMQX 集群

- 运维简单

   EMQX Operator 可以对接 Prometheus，同时也支持把监控指标导出到 Prometheus 中


## 在 OSC 上部署 EMQX 服务

部署环境说明：

- CCE 节点的操作系统为 Ubuntu 
- CCE 节点的规格 ≥ 2C8G 
- CCE 节点可以访问外网

> **注**：这里的价格只是为了演示，不是真实的价格

### 订阅 cert-manager

**查找服务**

登录 OSC 控制台，在服务目录中输入cert-manager，找到 cert-manager 证书管理。

![查找服务](https://assets.emqx.com/images/8f0793c8067939179b1225495eb42ec4.png)

**订阅和购买**

进入 cert-manager 证书管理，点击“订阅”。

![订阅和购买](https://assets.emqx.com/images/559ec03e58ea3ff03b6813afe4fb206f.png) 

点击“立即购买”。

![立即购买](https://assets.emqx.com/images/56b4e3ff3b9bcf577e790a4d8dd3e2af.png)

完成支付。

![完成支付](https://assets.emqx.com/images/51f0543ac1c4b55becf20da68d2244b9.png)

最终在“已购买的服务”里面会显示刚刚的购买的 cert-manager。

![已购买的服务](https://assets.emqx.com/images/c887c119cbb6f13f414bb203fec8e3c8.png)

### 部署 cert-manager

**创建实例**

在“我的服务”点击创建实例

![点击创建实例](https://assets.emqx.com/images/f6812bc70f57980d54aa2c5ca710b76e.png)
 
**填写基本信息**

选择容器集群和选择要部署的命名空间，如果显示不存在则点击“创建容器集群”或者“创建命名空间”，然后选择下一步。

> 注：确保容器集群的节点可以访问外网

![填写基本信息](https://assets.emqx.com/images/b15aecbc9ef338b32676cde8d9b06cbe.png)

**填写实例参数**

选中”installCRDs“，然后选择下一步。

![填写实例参数](https://assets.emqx.com/images/4707592ee273fa84d73ab08247b916d5.png)

**确认信息并提交**

![确认信息并提交](https://assets.emqx.com/images/def15aa0dcda06a416c0276bd36550c0.png)

稍等片刻，可以看到 cert-manager 服务实例创建成功。

![服务实例创建成功](https://assets.emqx.com/images/a0be16a1bb91ed879a3a9823afcc2b7b.png)

### 订阅 EMQX Operator

**查找服务**

在“服务目录”中输入 emqx，找到 EMQX 消息中间件 Operator。

![查找服务](https://assets.emqx.com/images/a3823f5388441e4b0db30c83c21c9558.png)

**订阅和购买**

进入 EMQX 消息中间件 Operator，点击“订阅”。

![订阅和购买](https://assets.emqx.com/images/d52108b9e2e388fb22e440c244e7481c.png)

点击“立即购买”。

![立即购买](https://assets.emqx.com/images/0f67ced30553ee809bce346eaa9fad55.png)

完成支付。

![完成支付](https://assets.emqx.com/images/5aa2f3cb850d5de4212d7f64095a8f34.png)

最终在“已购买的服务”里面会显示刚刚的购买的 EMQX 消息中间件 Operator。

![已购买的服务](https://assets.emqx.com/images/c364ea849ab3a35ed1446211e439e8ce.png)

### 部署 EMQX Operator

**创建实例**

在“我的服务”中点击“创建实例”。

![创建实例](https://assets.emqx.com/images/7418855df5f8ac3f0f7926fe1270a112.png)

**填写基本信息**

选择容器集群和选择要部署的命名空间，如果不存在则点击“创建容器集群”或者“创建命名空间”，然后选择下一步。

> 注：确保容器集群的节点可以访问外网

![填写基本信息](https://assets.emqx.com/images/5db9779f76b0cc62034a9d721a2e07c1.png)

**填写实例参数**

选中”installCRDs“，然后选择下一步

![填写实例参数](https://assets.emqx.com/images/172f16290fa797ddb2c0fe4aff7b8cbd.png)

**确认信息并提交**

![确认信息并提交](https://assets.emqx.com/images/0a6bc4718c6b4e2e9598c20941cf07c9.png)

稍等片刻，EMQX 消息中间件 Operator 实例就可以成功创建。

![Operator 实例创建成功](https://assets.emqx.com/images/41a36bba65d05319bc3b0ee2efebe1ee.png)

**查看实例信息**

点击 emqx operator 服务。

![点击 emqx operator 服务](https://assets.emqx.com/images/941a629e1e25e18325eb97b2f1832b9c.png)

可以看到服务的基本信息。

![服务的基本信息](https://assets.emqx.com/images/06a44292d178dfbf81c55d7388c4763a.png)

### 部署 EMQX 企业版实例

**连接”云容器引擎”**

登陆云容器引擎 CCE，在”集群管理“下点击进入集群。

![点击进入集群](https://assets.emqx.com/images/d2da25d849aced925c7042605de68506.png)

在集群信息中，点击“CloudShell”图标，连接集群

![连接集群](https://assets.emqx.com/images/4c47d46caf00a2eca2dfefab3be22c34.png)

**部署 EMQX 企业版实例**

实例的 yaml 文件如下：

```
cat << "EOF" | kubectl apply -f -
apiVersion: apps.emqx.io/v1beta3
kind: EmqxEnterprise
metadata:
  name: emqx-ee
  labels:
    "foo": "bar"
spec:
  persistent:
    storageClassName: csi-disk
    resources:
      requests:
        storage: 1Gi
    accessModes:
    - ReadWriteOnce
  emqxTemplate:
    image: emqx/emqx-ee:4.4.5
    serviceTemplate:
      metadata:
        annotations:
          kubernetes.io/elb.pass-through: "true"
          kubernetes.io/elb.class: union
          kubernetes.io/elb.autocreate:
              '{
                "type": "public",
                "name": "emqx",
                "bandwidth_name": "cce-emqx",
                "bandwidth_chargemode": "bandwidth",
                "bandwidth_size": 200,
                "bandwidth_sharetype": "PER",
                "eip_type": "5_bgp"
              }'
      spec:
        type: LoadBalancer
EOF
```

**检查 EMQX 企业版状态**

```
kubectl get pods
kubectl exec -it emqx-ee-0 -c emqx -- emqx_ctl status
kubectl exec -it emqx-ee-0 -c emqx -- emqx_ctl cluster status
```

![检查 EMQX 企业版状态](https://assets.emqx.com/images/dd0f53b39cf5480715e87faaebf06626.png)

**连接 EMQX 企业版**

![连接 EMQX 企业版](https://assets.emqx.com/images/72bfb736e4bc7c2464c07d7900e39c27.png)

> 用户名：admin 密码：public Dashboard: ${EXTERNAL-IP}:18083

![连接 EMQX 企业版](https://assets.emqx.com/images/1248d7cfc8fc0ed21d2df6ccb428b266.png)

## 总结

OSC 兼容 Helm、Operator Framework 等第三方生态作为服务包，可以降低已有业务搬迁的门槛，实现从服务开发、基本服务实例部署到后续实例生命周期维护和运维操作的完整覆盖。通过 OSC 平台，服务提供商可以方便快捷地发布服务，服务使用者则只需要订阅和部署，实现开箱即用。

而 EMQX Operator 提供了对 EMQX 的全生命周期管理，除了对持久化数据进行备份和恢复的基础能力，害提供了对 EMQX Plugin 的独立部署、管理、配置持久化能力。用户可以动态更新 Licence 和 SSL 等，实现包括高可用、扩容、异常处理的自动化运维。

OSC 与 EMQX Operator 的结合，为用户提供了一种更加便捷的选择，极大降低了 EMQX 企业版的部署和运维成本。

> **参考：** [https://github.com/emqx/emqx-operator](https://github.com/emqx/emqx-operator)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
