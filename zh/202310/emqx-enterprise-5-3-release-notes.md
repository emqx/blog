[EMQX Enterprise](https://www.emqx.com/zh/products/emqx) 5.3.0 版本现已正式发布！

新版本带来多个企业特性的更新，包括审计日志，Dashboard RBAC 权限控制，以及基于 SSO（单点登录）的一站式登录，提升了企业级部署的安全性、管理性和治理能力。此外，新版本还进行了多项改进以及 BUG 修复，进一步提升了整体性能和稳定性。

## 审计日志

审计日志（Audit Logs）是记录软件或系统关键操作活动的功能，EMQX 新增审计日志支持，能够让您实时跟踪集群管理与配置过程中的重要操作，助力企业用户满足合规要求。

EMQX 新增的审计日志支持记录来自 [Dashboard](https://docs.emqx.com/zh/enterprise/v5.3/dashboard/introduction.html) 、[REST API](https://docs.emqx.com/zh/enterprise/v5.3/admin/api.html) 以及[命令行](https://docs.emqx.com/zh/enterprise/v5.3/admin/cli.html)的所有变更性操作，例如用户登录，对客户端、访问控制以及数据集成等资源的修改。审计日志会记录每项操作的操作对象，发起用户、来源 IP、浏览器特性、关键参数以及操作结果，企业用户可以方便地进行索引与查看，以实现运营过程中的合规性和安全性审计。

当前版本 EMQX 仅支持将记录写入到日志文件中，后续版本将在 Dashboard 上提供搜索与查看功能，实现开箱即用的审计管理功能。

## Dashboard RBAC 访问权限控制

EMQX Dashboard 是管理和配置 EMQX 集群的关键组件。对于大型企业用户，团队成员之间通常有不同的工作划分。根据团队成员的角色，只为他们分配 Dashboard 的最低访问权限是一种安全性最佳实践。

本次发布 Dashboard 中引入了基于角色的访问控制（RBAC）权限管理功能。RBAC 可以根据用户在组织中的角色，为用户分配不同的访问权限。这一功能简化了权限管理，通过限制访问权限提高了安全性，并提升了组织的合规性，是 Dashboard 不可或缺的安全管理机制。

目前，Dashboard 预设了两个角色：

**管理员（Administrator）**

管理员拥有对 EMQX 所有功能和资源的完全管理访问权限，包括客户端管理、系统配置、API 密钥以及用户管理。

**查看者（Viewer）**

查看者只能以只读的方式访问 EMQX 的数据和配置信息，例如查看客户端列表、获取集群指标与状态、查看数据集成配置，无权进行创建、修改和删除操作。

在后续的版本中，EMQX 将开放 REST API 的 RBAC 权限管理，并增加更多的预设角色，支持创建自定义角色。这将满足用户对访问控制的更细粒度需求，将帮助 EMQX 更好地适应大规模企业用户的复杂管理需求。

## Dashboard SSO 一站登录

单点登录（SSO）是一种身份验证机制，它允许用户使用一组凭据（例如用户名和密码）登录到多个应用程序或系统中，而无需在每个应用程序中单独进行身份验证。 

本次发布中，EMQX Dashboard 提供了基于 LDAP 和 SAML 2.0 的单点登录功能。启用单点登录后，用户可以方便地使现有企业账号管理系统登录到 Dashboard，减少用户需要记住的密码数量，以减少密码泄露和被黑客攻击的概率；而企业则能集中管理用户身份和权限，简化用户帐户的管理、配置和停用流程。

目前，EMQX Dashboard 支持集成例如 [OpenLDAP](https://www.openldap.org/)、[Microsoft Entra ID](https://azure.microsoft.com/en-in/products/active-directory)（原 Azure Active Directory） 提供的 LDAP 单点登录服务，以及 [Okta](https://www.okta.com/)、[OneLogin](https://www.onelogin.com/) 等身份提供商的 SAML 2.0 单点登录服务。

## 更多更新

- 增加了集群优化配置项，根据部署情况调优，能够极大地减少复制节点（Replica）的启动时间。
- 添加一个新的规则 SQL 函数 `bytesize` 以获取字节字符串的大小。

## BUG 修复

以下是主要 BUG 修复列表：

- 修复了将文件日志中处理程序轮换大小设置为 `infinity` 时日志记录停止的问题。[#11682](https://github.com/emqx/emqx/pull/11682) 
- 修复了日志格式 `log.{handler}.formatter` 设置为 `json` 时，日志行不是有效的 JSON，而是以时间戳字符串和日志级别作为前缀的问题。[#11661](https://github.com/emqx/emqx/pull/11661)

更多功能变更和 BUG 修复请查看 [EMQX Enterprise 5.3.0 更新日志](https://www.emqx.com/zh/changelogs/enterprise/5.3.0)。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
