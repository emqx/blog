十年前，在 2012 年 12 月 17 日，源于个人对 Erlang、MQTT 和开源的热爱，[EMQX](https://github.com/emqx/emqx) 诞生于一家咖啡馆并作为开源项目在 GitHub 上发布了初次提交。十年后的今天，EMQX 已成长为 Erlang 生态中最具影响力的物联网开源基础软件项目，作为全球最具扩展性的 [MQTT 消息服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)在物联网、工业互联网、车联网等行业的关键业务场景中发挥着重要作用。目前，来自全球 50 多个国家的 20000 余家企业用户，通过 EMQX 连接着超过 1 亿台物联网设备，为自己的物联网平台与应用提供数据支撑。

![EMQX 诞生的咖啡馆](https://assets.emqx.com/images/3c179bf5303b62b1c71005d327977b67.png)

<center>EMQX 诞生的咖啡馆</center>

我们正处在一个快速变化的世界。在过去的十年里，开放源码逐渐主导了软件开发方式，使云计算蓬勃发展，并在商业机构中的认知度不断提升。2012 年，在 GitHub 上有 280 万开发者，一些公司主要使用开源项目来运行他们的互联网服务。而如今，有超过 9400 万的开发者在使用 GitHub，超过 90% 的公司在通过开源项目构建企业应用、创造价值。「物联网」作为一个曾经只是概念性的趋势，也正成为各垂直行业以及未来数十年全球商业数字化转型的关键。

EMQX 成长的这十年也是 MQTT 和物联网飞速发展的十年。我们见证了物联网、工业互联网、车联网的大规模应用。MQTT 因其轻量高效和可扩展性，迅速成为物联网消息传输协议的事实标准，是许多实时物联网应用构建的最佳选择。

而在 EMQX 发布之初，MQTT 消息服务器是一个尚未被熟知和普及的基础软件。但彼时 EMQX 就明确了物联网 MQTT 消息服务器的清晰定位，最早实现了当时的主流物联网协议 MQTT 3.1 和 3.1.1 的兼容支持。

![EMQX 在 GitHub 发布的初次提交](https://assets.emqx.com/images/9745b032b378bdb1171e342667dc537e.png)

<center>2012 年 12 月 17 日 EMQX 在 GitHub 发布的初次提交</center>

2016 年，MQTT 正式成为 OASIS 的开放标准后，作为组织成员之一的 EMQ 团队积极参与了 MQTT 5.0 版本的开发和讨论。早在该版本规范草案还在草拟阶段时，EMQX 便已创新性地在产品开发中引入了共享订阅功能。

2018 年，EMQX 3.0 发布。这是全球首个完整支持最新协议规范的 MQTT 5.0 消息服务器。

2020 年，EMQX 4.0 发布。这一版本内置了强大的基于 SQL 的规则引擎，支持提取、过滤、转换从设备到云以及从云到设备的数百万物联网事件，简化了物联网数据处理的方式。

2022 年，随着下一个亿级连接的物联网时代的到来，EMQX 发布了具有颠覆性突破的 5.0 版本。EMQX 5.0 全球首个实现了单集群 1 亿 MQTT 并发连接，时延低至毫秒级，成为目前世界上最具扩展性的开源 MQTT 消息服务器。同时开创性地将 [QUIC 协议引入 MQTT](https://www.emqx.com/zh/blog/mqtt-over-quic)，推动下一代物联网标准协议的发展，探索物联网消息传输场景的新可能。

![EMQX 5.0 1 亿 MQTT 连接测试结果](https://assets.emqx.com/images/621236d970d08a12daa16f461676b26d.png)

<center>EMQX 5.0 1 亿 MQTT 连接测试结果</center>

作为一个开源项目我们深知，如果没有全球社区用户的支持与贡献，EMQX 不会达成这样的成就。在过去的十年里，EMQX 深深根植于开源社区，与社区一同成长。EMQX 项目从开源社区中获得了超过 10K 的 star、2000 万+ 的下载量。在 GitHub 上 EMQX 的代码仓库中，有数千个 PR 被提交合并，数千个 issue 被提出和解决，这些来自社区用户的反馈与贡献，使得 EMQX 的功能愈发强大和完善，性能与可靠性持续提升。每月有超过 3 万个活跃的 EMQX 集群被部署在全球各类物联网场景。

深深受益于开源社区，我们也始终没有忘记开源初心，十年来一直坚持始于社区、回馈社区。EMQX 项目通过采用 RFC 流程 EMQX Improvement Proposals（EIP），让每一个来自社区的声音被听到、有回响；我们举办了 Demo Day、Open Day 以及其他各类主题直播等数百场社区布道活动，帮助开发者更加深入地了解 EMQX 与物联网；我们也积极支持其他优秀开源项目与基金会的良性运营和蓬勃发展，赞助了 NNG 项目与 Erlang 生态系统基金会（EEF）、OASIS、LF Edge 基金会。我们以实际行动践行着「通过世界级开源软件产品，服务人类未来产业与社会」的使命。

![EMQX GitHub Star 历史](https://assets.emqx.com/images/a6c352b6cf7e8512ab55175a0fdcf5b5.png)

<center>EMQX GitHub Star 历史</center>

始于开源社区的 EMQX 同样也在赋能行业。随着 EMQX 开源项目逐渐在全球范围内被广泛采用，越来越多的企业用户在实际生产中提出了大规模部署和企业级功能需求。2017 年，EMQ 公司成立。国内诸多顶级投资机构对我们的技术与开源愿景给予了认可与支持，为公司的发展提供了巨大动力。EMQ 为企业用户提供了基于 EMQX 开源项目的商业化版本：企业级 [MQTT 物联网接入平台 EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 和全托管的 [MQTT 消息云服务 EMQX Cloud](https://www.emqx.com/zh/cloud)，它们获得了包括 HPE、VMware、Verifone、上汽大众和爱立信等财富 500 强企业在内的 400 余家客户的信赖，助力这些企业在物联网关键业务场景中构建可靠平台与应用。

回望过去，EMQX 和所有社区贡献者、开源用户、商业客户以及投资机构共同走过了一段美好的十年旅程。是你们让 EMQX 成长为今天的 EMQX。上一个十年，我们共同见证了物联网与开源的日渐繁荣；下一个十年里，我们还将迎来开源理念更加深入人心的、更美好的万物互联时代。EMQ 将致力于把 EMQX 打造成为一个高性能、高可靠的开源物联网数据基础设施软件，作为值得信赖的技术伙伴和坚实后盾与所有用户站在一起，迎接一个开放、协作、创新的美好未来。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
