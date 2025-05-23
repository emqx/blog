EMQX 迎来了发展历程中的重要转折点！

我们很高兴地宣布：自 5.9 版本起，EMQX 社区版与企业版将统一为功能完整的 **EMQX Platform**，并采用商业源码许可证 (Business Source License，BSL) 1.1。

这一战略调整源于我们对 MQTT 与 AI 融合创新的坚定承诺。我们相信，MQTT 将成为连接物理世界与人工智能的"神经系统"，而此次变革将助力 EMQX 引领这一未来。

## 回顾：双版本服务全球用户

多年来，EMQX 一直采用双许可证模式，提供两个独立版本：

- **EMQX 社区版（EMQX Community**）：采用 Apache 2.0 开源许可，是全球开发者广泛使用的开源 MQTT 消息服务器
- **EMQX 企业版（EMQX Enterprise**）：在社区版基础上提供增强功能，包括高级数据处理、50+ 数据集成、企业级安全特性（单点登录 SSO、基于角色的访问控制 RBAC 等）、高级集群管理和专业技术支持。

## 变革：加速创新与生态共赢

尽管双版本模式取得了良好成效——EMQX 企业版已赢得全球 1000 多家客户的信赖，但长期来看，其逐渐显现出制约创新速度的挑战：

- **开发复杂性**：维护两套代码库消耗大量资源，拖慢整体创新速度和迭代周期。
- **社区局限性**：社区用户无法使用企业版中已有的高级数据集成、增强的高可靠性等生产就绪的功能特性，经常被迫进行“重复造轮子”的工作。
- **愿景驱动**：为充分释放 MQTT + AI 的潜力，我们需集中资源实现技术突破及影响最大化。

而在统一平台下采用 BSL 许可证将带来以下优势：

- **提升研发效率**：专注单一代码库，加速功能迭代与问题修复，为用户交付更加稳定的版本。
- **加大技术投入**：构建可持续商业模式，强化 MQTT 核心技术与 AI 集成研发。
- **保持开放透明**：BSL 仍属源码可用（source-available）许可证，用户可在条款要求下自由查看、修改和分发代码。

## 解读：商业源码许可证（BSL 1.1）

BSL 由 MariaDB 等企业首创，已在开源生态中广泛应用，是非常适合现代软件生态格局的一种源码可用许可。其核心特点包括：

- **源码开放**：允许在符合要求的情况下，自由查看、下载、修改和编译源代码。
- **免费使用**：符合特定条件的场景可免费使用（详见下文）。
- **商业限制**：禁止将软件作为托管服务商用或嵌入竞品。

BSL 既保持了开放透明协作的优势，又为长期商业投入于创新提供了一种可持续性发展的模式，尤其适合快速发展的云计算与 AI 时代。

## 共赢：全生态用户收益一览

所有 EMQX 用户都将从此次变革中获得显著价值：

- **对于社区用户**，您能在开发测试和非受限场景中免费使用包括高级数据集成（50+ connectors）、增强安全模块（SSO、RBAC）、可视化的 Flow 设计器等原企业版专属特性。
- **对于企业客户**，通过代码库统一与研发流程优化，您将更快获得新功能推送、性能增强与安全更新。这种模式不仅可以保障关键业务部署的可靠性，还将通过加速创新周期和专属支持体系，持续赋能您的数据基础设施。

## EMQX 5.9+ 的 BSL 许可模式详解

新版许可证在保持灵活性的同时，确保不同规模、不同场景的用户都能便捷获取 EMQX 的价值。以下为 EMQX 5.9 及以上版本在 BSL 1.1 许可证下的使用授权详情：

**免费使用场景**：

在以下条件下，您可以免费使用 EMQX Platform：

- **单节点生产环境**：允许在生产环境中的单节点实例上运行 EMQX，但不得将 EMQX 作为托管服务或嵌入商业产品提供给第三方，无论您是否向第三方收费。
- **教育/非营利机构**：经认可的学术机构和注册的非营利组织可以在生产环境中无节点限制地运行 EMQX，但需符合非商业用途定义（详见完整许可证文本）。
- **所有非生产环境**：您可以在开发、测试等任何非生产环境免费使用 EMQX 5.9.0 及以上版本。

请注意，映云科技不对商业源码许可证下的免费部署提供服务级别保障，也不承担任何形式的赔付责任。

**需购买商业许可的场景**：

如果您的使用涉及以下情况，您需要申请 EMQX 商业许可证（联系 EMQ 销售团队获取）：

- **多节点集群部署**：在生产环境中以集群形式（两个或更多节点）运行 EMQX 处理业务负载。
- **商用 SaaS 或托管服务**：以托管服务形式向第三方提供 EMQX 或基于 EMQX 构建的 SaaS 产品。
- **商用产品嵌入或分发**：将 EMQX 集成至软件或硬件产品中，通过商业渠道向终端用户销售。

完整条款请参阅 EMQX 5.9 及后续版本附带的 BSL 1.1 许可证文本。

## 统一平台：四大版本应对全场景需求

整合为统一平台后，以核心 EMQX Platform 为基础，我们通过四个不同版本，为全体用户提供灵活的部署与管理方案：

1. **EMQX Serverless：**多租户、按量计费、可自动扩展的 MQTT 服务。适合快速开发、原型验证与轻量化应用场景。提供免费额度，可轻松快速开启使用。
2. **EMQX Dedicated：**部署于主流公有云（阿里云、火山引擎、华为云等）的全托管单租户 EMQX 集群。提供资源独占保障、增强安全防护与成本可预测性，专为关键业务场景设计。
3. **EMQX BYOC：**在用户自有公有云账户中部署的专属集群，由 EMQ 团队负责运维。在享受托管服务便利性的同时，实现数据主权与合规性管控。
4. **EMQX Enterprise：**基于 BSL 1.1 授权的自托管软件包（多节点生产/SaaS/嵌入场景需商业许可），支持在自有硬件、私有云或公有云平台灵活部署，满足极致定制化需求。

## 展望：MQTT + AI 的无限可能

我们相信，MQTT 将成为物理世界与人工智能连接的基石。此次向基于 BSL 许可的统一平台的战略转型，标志着 EMQ 朝这一愿景迈出了重要一步——通过持续加大研发投入，构建支撑下一代智能应用的 MQTT+AI 平台，赋能从车联网到工业自动化等各领域的数字化转型。

我们期待新篇章的开启，并将全力协助社区用户和企业客户完成这一关键转变，打造一个更统一、更具创新能力、更强大的 EMQX Platform，为全球开发者与组织创造可持续的技术价值。

## **了解更多**

- 加入讨论：[https://github.com/emqx/emqx/discussions](https://github.com/emqx/emqx/discussions)
- 功能探索：[https://www.emqx.com/zh/platform](https://www.emqx.com/zh/platform)
- 商业许可咨询：[https://www.emqx.com/zh/contact](https://www.emqx.com/zh/contact)

感谢您与 EMQX 同行，共创万物互联的未来！



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
