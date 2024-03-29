## 引言

在过去十年里，[MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)在物联网领域获得了广泛的应用。很多物联网服务提供商都需要灵活可扩展的 MQTT 服务，采用多租户架构的 MQTT 则为他们提供了一种新的选择。

本文将探讨 MQTT 多租户架构以及其为用户带来的优势和挑战。

## 什么是多租户架构？

**多租户（Multi-tenancy ）**是一种软件架构模式，它能让应用的单个实例同时为多个租户（用户或客户）提供服务，每个租户都拥有自己独立的数据和配置。

在这种架构下，多个租户共用同一套基础设施、数据库和集群，但每个租户只能访问属于自己的数据和配置。这意味着租户可以根据自己的需求定制服务，而不会影响其他租户的数据或配置。同时，提供商也可以通过在同一套基础设施上为多个租户提供服务来降低成本。

对于 [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) 而言，多租户架构是一种高效且经济的解决方案，可以同时为多个客户或团队提供 MQTT 服务。

## MQTT 中的多租户架构：实现每个租户的数据隔离

MQTT Broker 多租户架构的核心是数据隔离。这样可以确保每个租户都将自己视为整个集群的唯一用户，他们不能访问其他租户的客户端，更不能与其他租户的客户端互动。它包括以下五个主要方面：

- **无需对客户端限制。**客户端可以使用任意客户端 ID、用户名和密码，不受其他租户的影响。甚至不同的租户可以使用相同的客户端 ID 同时接入。
- **认证/授权数据隔离。**每个租户都有自己独立的认证和授权数据，用于控制客户端登录和主题的发布/订阅权限。租户只能操作自己的数据，而且这些数据只对该租户的客户端生效。
- **消息隔离。**不同租户的客户端不能相互通信。尽管租户可以使用任意主题，包括其他租户使用的主题，但是消息仍然完全隔离。
- **独立的用户层接口。**包括管理网站和 HTTP API。租户只能管理和查看自己的数据，不能修改其他租户的数据。
- **差异化配置。**应该为每个租户提供独立的配置，以满足他们特定的资源和功能需求。

## MQTT 多租户架构的优势和挑战

MQTT 多租户架构为物联网解决方案提供商带来了双重优势：

- **灵活性：**MQTT 多租户架构比专有架构更加灵活。这主要体现在两个方面：一是它无需为每个租户单独搭建基础设施，可以快速提供 MQTT 服务。二是它可以在不中断服务、不重新分配底层基础设施的情况下，为单个租户量身定做收费套餐。
- **节省成本：**MQTT 多租户架构是专用架构的低成本替代方案，可以让多个租户共享同一套基础设施。相反，专用架构要求每个租户都有自己的基础设施，这在建设和维护方面会带来高额的成本。

但同时，采用 MQTT 多租户架构也存在一些挑战：

- **保证正确隔离租户数据。**在任何情况下，租户都不能访问或管理其他租户的设备和数据。因此，必须采取严格的安全措施，包括严密的访问控制策略、合理的认证和授权机制、以及基于角色的访问控制。必要时采用数据加密来确保数据在传输过程中的安全。
- **有效管理资源竞争。**由于多个租户共享同一套基础设施，例如网络带宽、CPU 或内存等，租户之间必然存在资源竞争的情况。关键在于系统必须能够限制租户对资源的使用，以避免某资源被某个租户完全耗尽，而影响到其他租户的正常使用。通常情况下，我们可以通过为每个租户设置配额和速率限制策略来控制资源的消耗。例如，可以为租户设定最大连接数和订阅数的限制，以及消息速率的限制。一旦达到限制，服务可以拒绝请求，以防止租户对资源的过度消耗。

## EMQX Cloud Serverless：基于多租户架构的 MQTT 服务

EMQ 基于创新的多租户技术推出了一种 Serverless MQTT 服务 - [EMQX Cloud Serverless](https://www.emqx.com/zh/cloud/serverless-mqtt)。EMQX Cloud Serverless 可以让用户在几秒内快速部署 MQTT 服务，**无需担心服务器基础设施管理或服务扩展时的资源分配问题**。它还提供了**每月 100 万分钟的永久免费额度**，采用即用即付的收费模式，极大地降低了物联网成本。

## 结语

随着物联网设备不断增长，新应用场景不断涌现，MQTT 多租户架构在未来的物联网市场有着广阔的前景。采用这种架构，不但可以为客户提供更灵活的 MQTT Broker 服务，还可以在大规模部署时为客户降低运营成本。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
