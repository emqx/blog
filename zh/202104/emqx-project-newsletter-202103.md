> 本文内容来自 EMQ 欧洲研发团队



三月份我们工作的重点是 EMQX 4.3 版本的收尾工作和 5.0 版本的产品设计。历经长达三周的马拉松式讨论，我们最终确定了 5.0 版本的详细需求列表，这是个令人兴奋的消息，标志着我们即将开始 5.0 的开发工作。



## **4.3.0 即将发布**

我们的项目在团队的努力下快速推进，现已发布了 4.3-beta.1、4.3-rc.1、4.3-rc.2、4.3-rc.3，4.3.0 正式版即将来临，敬请期待。



## **安全性**

三月，EMQ 与知名安全公司 Synopsys Software Integrity Group 开展合作，旨在进一步提升 EMQ 的产品和服务安全性。



## **社区动态**

- 为了使我们的开源项目以更具创新、更加积极的状态高效迭代快速推进，EMQX 团队开始正式采用 RFC 流程，以收集来自社区的意见，持续完善产品功能。我们将管理该流程的存储库命名为 EIP，全称为： **EMQX Improvement Proposals。** 项目地址：[https://github.com/emqx/eip](https://github.com/emqx/eip)。
- 我们本月上线了 EMQ 中文问答社区 [askemq.com](https://askemq.com/)，这个社区可以帮助中国大陆的用户更方便地进行协作和分享。
- 线上 DEMO 会议按照每两周一次的频率持续进行, 得到了多个开发团队及社区成员支持。
- EMQX 团队即将在杭州 Ofiice 举办第一次线下 Open Day 活动，敬请关注。



## **项目进展**

- 成立了专门的测试团队，该团队将为 EMQX 项目在 GitHub CI 中提供更多的自动化集成测试。
- 我们的主项目 [emqx/emqx.git](https://github.com/emqx/emqx) 已经全部通过了 rebar dialyzer 检查。
- [Quicer](https://github.com/emqx/quic) (QUIC 协议的 Erlang/Elixir 支持) 提供了 macOS 上的构建；增加了类似 inet/gen_tcp 风格的 APIs，开始了 MQTT-on-QUIC 的试验性功能实现。
- 开始了Rlog 项目，该项目旨在提高 EMQX 集群的伸缩能力。Rlog 是 [ekka](https://github.com/emqx/ekka) 库的一部分，将提供一种 Mnesia 数据库的异步复本复制功能，详情请参见 [EIP-0004](https://github.com/emqx/eip/blob/main/implemented/0004-async-mnesia-change-log-replication.md)。
- jq.erl。 [jq](https://stedolan.github.io/jq/) 是 JSON 处理的事实标准。基于其开源内核，我们将提供一个 Erlang 的 NIF 实现。它将被应用于 EMQX 规则引擎中，为 JSON 数据流处理提供灵活强大的扩展。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
