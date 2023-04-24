## 引言

[EMQX Cloud](https://www.emqx.com/zh/cloud) 是基于 [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 构建的一款全托管云原生 MQTT 消息服务。为了满足不同客户的需求，EMQX Cloud 提供了三种版本供客户选择：[Serverless 版](https://www.emqx.com/zh/cloud/serverless-mqtt)、[专有版](https://www.emqx.com/zh/cloud/dedicated)和 [BYOC 版](https://www.emqx.com/zh/cloud/byoc)。

本文将简要介绍这三个版本的核心区别，并通过三个用户故事，帮助您更轻松地了解不同版本的适用场景，并根据自己的需求找到最适合的方案。

>**太长不看版：**
>
>- 如果您正在寻找一种成本可控、易于扩展的 MQTT 云服务，那么 Serverless 版是您的不二之选。
>- 如果您需要一个高性能、可定制的 MQTT 云服务来支持企业级项目，专有版将是您的理想选择。
>- 如果您对数据安全和合规性有特殊要求，希望在自选的云服务商和基础设施上部署 MQTT 服务，BYOC 版将满足您的需求。

## EMQX Cloud Serverless 

[EMQX Cloud Serverless](https://www.emqx.com/zh/cloud/serverless-mqtt) 是一种无服务器架构，用户无需关心底层基础设施和资源管理，特别适用于个人开发者和中小型项目和开发测试环境。

了解详情：[EMQX Cloud Serverless 正式上线：三秒部署、按量计费的 Serverless MQTT 云服务](https://www.emqx.com/zh/blog/emqx-cloud-serverless-launched)

### 优势

- 低成本：Pay As You Go 模式，完全按实际使用量付费，无需提前购买资源。
- 自动扩展和缩减：根据业务需求自动调整资源，无需手动干预。
- 无需管理底层基础设施：专注于应用开发，让 EMQX Cloud 专业团队处理底层运维工作。

### 适用范围

- 适合个人开发者项目或企业的中小型项目，开发和测试环境。
- 不支持数据集成、专有网络等功能。
- 最高仅支持 1000 设备同时在线，每秒消息吞吐不超过 1000 条。

### 用户故事

Michael 是一位初创公司的开发者，公司预算有限。他们的项目规模不大，因此希望能找到一种按需付费、成本可控的云服务。这时，他们发现了 EMQX Cloud Serverless。

Serverless 版为 Michael 提供了一个无需关心底层基础设施的环境，按实际使用量计费。Michael 从创建账号，到拥有一个功能完备的标准 MQTT 服务仅花了不到 3 分钟。此外，随着业务的发展，系统资源可以自动扩展和缩减，让 Michael 更专注于应用开发。Serverless 版很好地满足了 Michael 的需求，帮助他们以低成本轻松搭建中小型项目。

## EMQX Cloud 专有版

[Dedicated 版](https://www.emqx.com/zh/cloud/dedicated)为客户提供了独立部署的 EMQX Cloud 实例，具有更高的性能保障和可定制性。适用于对性能、稳定性要求较高的企业级项目。

### 优势

- 独立部署：每个客户都拥有独立的实例，性能稳定。
- 高度可定制：支持针对客户需求进行个性化定制。
- 完全托管：享受专业的技术支持，降低运维压力。

### 适用范围

- 适合对性能、稳定性要求较高的企业级项目。
- 提供不同连接数的规格，无上限。

### 用户故事

Christina 是一家大型企业的数字化转型项目经理，她负责的项目对性能和稳定性有很高要求。为了确保系统稳定运行，她需要一个独立部署且可定制的云服务。在了解了 EMQX Cloud 专有后，她发现这正是她在寻找的解决方案。

专有版为 Christina 提供了一个独立部署的实例，保证了性能稳定。并且，Christina 可以决定希望使用的底层云服务商以及部署地域，并通过 VPC 对等连接的功能实现和企业内部其他服务的可靠、安全对接。同时，专有版还支持个性化定制，可以根据项目需求进行调整。此外，EMQX Cloud 团队还提供专业的技术支持，让 Christina 放心地交付企业级项目。

## EMQX Cloud BYOC

[BYOC (Bring Your Own Cloud)](https://www.emqx.com/zh/cloud/byoc) 版允许客户将 EMQX Cloud 部署到自己的云服务商和基础设施上，满足特殊安全和合规要求。

了解详情：[EMQX Cloud BYOC 版本发布：在您的云上体验全托管的 MQTT 消息服务](https://www.emqx.com/zh/blog/deploy-the-most-powerful-mqtt-server-in-your-own-cloud) 

### 优势

- 自定义云服务商和基础设施：选择符合企业需求的云服务商和基础设施。
- 满足特殊安全和合规要求：充分考虑数据安全和合规性。
- 充分利用已有云资源：最大化利用现有云资源，降低成本。

### 适用范围

- 适合对数据安全、合规性要求严格的企业级项目。

### 用户故事

James 是一家头部车企的运维总监，公司对数据安全和合规性有严格要求。他们需要将云服务部署到自选的云服务商和基础设施上，以满足公司的安全和合规要求。于是，他们选择了 EMQX Cloud BYOC。

BYOC 版让 James 能够在自己选择的云服务商和基础设施上部署 EMQX Cloud。这使得他们能够满足特殊的安全和合规要求，同时充分利用已有的云资源。对于 James 来说，BYOC 版是一个既安全又灵活的解决方案，能让公司放心地进行业务扩展。

## 三种版本的比较与选择

我们将 EMQX Cloud 各版本在成本、性能、定制化程度这几个方面的情况总结如下表，方便大家更加直观地进行对比：

|                | **Serverless 版**                                        | **专有版**                                                   | **BYOC 版**                                                  |
| :------------- | :------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **成本**       | 按实际使用量付费，适合预算有限、需求较小的项目。         | 相对较高的成本，但提供独立部署和专业技术支持，适合对性能和稳定性有较高要求的项目。 | 自定义云服务商和基础设施，成本视具体情况而定，适合对安全和合规性有特殊要求的项目。 |
| **性能**       | 随业务需求自动调整，适合中小型项目，最高 1000 并发连接。 | 独立部署，性能保障较高，适合企业级项目。                     | 性能取决于自选的云服务商和基础设施，适合对性能有特殊要求的项目。 |
| **定制化程度** | 定制化程度较低，适合通用场景，支持标准 MQTT 协议。       | 高度可定制，适合有特殊需求的企业级项目。                     | 允许自选云服务商和基础设施，定制化程度较高，适合有特殊要求的项目。 |

## 总结

通过本文的介绍，针对 EMQX Cloud 三种版本的选择，我们为您提供以下建议：

- 如果您像 Michael 一样，正在寻找一种成本可控、易于扩展的云服务，那么 [Serverless 版](https://www.emqx.com/zh/cloud/serverless-mqtt)是您的不二之选。
- 如果您像 Christina 一样，需要一个高性能、可定制的云服务来支持企业级项目，[专有版](https://www.emqx.com/zh/cloud/dedicated)将是您的理想选择。
- 如果您像 James 一样，对数据安全和合规性有特殊要求，希望在自选的云服务商和基础设施上部署云服务，[BYOC 版](https://www.emqx.com/zh/cloud/byoc)将满足您的需求。

希望本文可以帮助您找到最适合自己的方案，借助 EMQX Cloud 高效开展物联网业务。

如需获取更多信息和支持，请访问 [EMQX Cloud 官方网站](https://www.emqx.com/zh/cloud)或[联系我们的技术支持团队](https://www.emqx.com/zh/contact?product=cloud)，我们将竭诚为您提供帮助。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
