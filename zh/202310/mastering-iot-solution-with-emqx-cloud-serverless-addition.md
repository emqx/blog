[EMQX Cloud Serverless](https://www.emqx.com/zh/cloud/serverless-mqtt) 自从4月正式上线以来，受到广大开发者的很多好评。 作为物联网数据基础设施软件供应商，EMQ 主旨一直是帮助更多的物联网开发者和中小企业用最低的成本构建安全稳定的物联网应用。 EMQX Cloud Serverless 开创性地采用弹性多租户技术，用户无需关心服务器基础设施和服务规格伸缩所需资源，仅用三秒即可极速创建 MQTT 部署，并根据业务需求进行无感知自动化弹性伸缩、按实际使用量付费，实现全自动化的 MQTT 接入服务，专注物联网业务逻辑和实现。

10月，Serverless 迎来了发布后的重大的更新。Serverless 内核升级到 EMQX 最新的 5.1 版本，从性能上更进一步，支持更多的用户和海量的设备平稳顺畅入云。同时新增支持 API 对部署的管理和监控，并且可以批量上传认证和鉴权的信息，方便用户做大规模的设备认证。

## Serverless API

Serverless 提供了 EMQX 5.1 版本最新的 API 接口，用户通过在控制台创建应用的 APP Key 和 APP Secret 之后，来调用 Serverless 的 API。使用 API 来管理部署并可以获取到客户端、订阅信息等。用户可以更自由灵活地使用 Serverless 部署功能。

### API 能用于什么样的场景？

EMQX 专注于物联网的数据层，EMQX Cloud 帮助用户解决运营维护基础云设施的烦恼，助力各类开发者和企业轻松上云。从一套完整的物联网方案来看，除了设备端，连接层以外，还需要大量的管理平台和应用支撑。EMQX 提供的 API 可以将 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 的一些能力轻松整合到用户自己的平台和应用中，而无需通过登录到 EMQX Console 来获取到部署的相关信息。

#### Serverless 支持的 API 类别

| **API 类别** | **说明**                                                 |
| :----------- | :------------------------------------------------------- |
| 认证控制     | 可对认证信息进行增删查改控制                             |
| 访问控制     | 可对访问控制信息进行增删查改控制                         |
| 客户端管理   | 客户端管理包括查看连接的客户端的详细信息，踢除指定客户端 |
| 主题订阅     | 获取指定客户端的订阅信息，管理所有订阅                   |
| 消息发布     | 对指定主题发布消息，支持批量消息发布                     |

系统接入了以上的能力之后，业务系统就可以管理客户端的访问控制、查看客户端信息、通过 HTTP 方式完成指令的下发等。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud Serverless
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>

### 如何开通和使用 API？

EMQX Serverless 开通和使用 API 非常的简单，当你完成了部署的创建之后，在部署详情页开启 AK / SK 管理。点击“创建应用”，系统会生成一对 AK / SK。HTTP API 使用 [Basic 认证](https://zh.m.wikipedia.org/zh-hans/HTTP基本认证)方式，id 和 password 须分别填写 AppID 和 AppSecret。 

![Serverless API](https://assets.emqx.com/images/3b05620179140612376db602d21a8a75.png)

请求地址由以下几个部分组成

{API}/{resource-path}?{query-string}

您可以在 [Serverless 的 API 文档](https://docs.emqx.com/zh/cloud/latest/api/serverless.html)中找到每个类型的请求和响应格式。

## 批量上传验证和访问控制信息

EMQX Serverless 支持 1000 以下的设备连接，对于某些设备连接场景，每个设备需要单独设置用户名密码，或者单独的访问的控制。在控制台不支持批量上传的时候，这无疑是非常头疼的。目前这个问题已经迎刃而解。用户可以在控制台非常方便创建批量导入的 CSV 文件，再批量导入到平台中即可。

![Batch Upload Authentication and Access Control](https://assets.emqx.com/images/0fd691ddecb8db297e27dbdfd7e21e9e.png)

目前支持一次导入 1000 条的信息，最多支持 2000 条的认证信息和访问控制信息。对于每个设备需要单独管理的场景，这无疑是非常便利的功能。

## 总结

EMQX Serverless 通过按量计费、自动伸缩的创新模式，为开发者和企业提供了最便捷的物联入云方案。在新增了 API 和认证批量导入的功能之后，能更好满足可用户生产环境的完备的解决方案，基于全托管的平台，为物联网数字化转型提供更多可能。欢迎体验 EMQX Cloud Serverless。



<section class="promotion">
    <div>
        咨询 EMQX Cloud 专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
