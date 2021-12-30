本月，eKuiper 团队正式发布了 v1.4.0 版本，同时开始 fixpack 版本 v1.4.1 的开发，并进行了下一年度产品路线图的规划。

## eKuiper v1.4.0 正式发布

[eKuiper v1.4.0 版本于本月初正式发布](https://www.emqx.com/zh/blog/ekuiper-newsletter-202111)，该版本新增了规则流水线功能以及 Portable 插件支持，这让 eKuiper 的运行性能和开发效率得到了提升。

除了在 beta 版本中已提供的功能之外，正式版还添加了以下功能：

- sink 动态参数支持：部分参数支持以动态的数据值作为参数值而非固定的值。例如在 mqtt sink 中，topic 参数可设置为某一列的值，从而实现将结果发送到多个不同 topic 的功能。
- 认证支持：用户可配置基于 JWT 的认证。使用 Fabric 管理 eKuiper 时，认证功能将自动启用，并自动生成和管理证书从而自动完成 SSO 。
- UI 适配：添加 portable 插件管理和共享连接配置的管理界面。

在 12 月 21 日的 EMQ Demo Day 中，eKuiper 团队展示了 v1.4.0 的主要新功能。

视频回放：

<div style="position: relative; padding: 30% 45%;">
<iframe style="position: absolute; width: 100%; height: 100%; left: 0; top: 0;" src="https://player.bilibili.com/player.html?bvid=BV1y3411x7vK&page=1&as_wide=1&high_quality=1&danmaku=0" frameborder="no" scrolling="no"></iframe>
</div>

## eKuiper v1.4.1 进展

eKuiper v1.4.1 版本将致力于提高产品稳定性及性能。目前，该版本开发已接近尾声，预计在本月底或下月初发布。

该版本修复了一些问题，包括 UI 的进一步优化、portable 插件运行时稳定性的问题、共享源 metric 不准确的问题以及 rest sink 的证书配置问题。同时，我们与用户进行了性能优化的合作开发，在用户场景中进行性能测试和优化，使得运行时 CPU 占用继续下降。特别是在规则中处理超多点位（几千个 case 计算且数据点位几万级别）且大量使用别名的场景中，CPU 占用可以大幅度减少，在该用户的场景中减少了 90% 以上。

## 2022 路线图规划

本月，eKuiper 团队完成了 2022 路线图规划，并公布在官方 Github：[https://github.com/lf-edge/ekuiper/projects/18](https://github.com/lf-edge/ekuiper/projects/18)。

未来我们将开发包括分布式集群模式、与 [Neuron](https://www.emqx.com/zh/products/neuron) 整合互通、动态更新表等新功能。我们也欢迎大家在 GitHub 上与我们交流互动，提出需求，与我们共同打造更加强大的 eKuiper。
