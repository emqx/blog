[EMQX Cloud](https://www.emqx.com/zh/cloud) 是跨多云的全托管 MQTT 云服务，提供一站式运维代管、独有隔离环境的 MQTT 消息服务。近日，EMQX Cloud 上线了 SSO 登录服务。

单点登录（Single Sign On），简称为 SSO，是比较流行的企业业务整合的解决方案之一。SSO 是指在多个应用系统中，用户只需要登录一次就可以访问所有相互信任的应用系统。在 EMQX Cloud 集成之后，平台用户便可以通过企业账号来登录使用 EMQX Cloud。下面就为大家介绍什么是 SSO 以及如何在 EMQX Cloud 控制台开启和整合 SSO 功能。

## 什么是 SSO（单点登录）？

SSO 是 Single Sign-On 的缩写，指的是一种身份验证机制，允许用户使用一组凭据（例如用户名和密码）登录到多个相关但独立的软件系统或应用程序中，而无需在每个系统中单独进行身份验证。这减少了用户需要记住的凭据数量，提高了安全性，并简化了管理和维护过程。 

### SSO 工作原理

单点登录基于一组有关联的、可信的应用、网站和服务，即**服务提供商 （Service Provider）**与 **SSO 解决方案**，即 **Identify Provider** 之间的数字信任关系。

1. 用户使用 SSO 登录凭证登录到一个可信的应用或连接所有可信应用的 SSO 解决方案网站。
2. 用户成功通过身份验证后，SSO 解决方案将生成一个会话身份验证令牌，其中包含关于用户身份（用户名、电子邮件地址等）的特定信息。 该令牌会存储在用户的 Web 浏览器或者 SSO 解决方案服务器上。
3. 用户尝试访问其他可信的应用时，该应用会向 SSO 服务器核实，确定用户是否通过会话身份验证。 若通过，SSO 解决方案会使用由数字证书签署的身份验证令牌来验证用户，并为用户提供该应用的访问权限。 若未通过，则会提示用户重新输入登录凭证。

SSO 方案减少了用户需要记住的凭据数量，提高了安全性，并简化了管理和维护过程。

### SSO 优势

SSO 可以为用户节省时间，带来便利。 以企业用户为例：使用 SSO，他们通常只需登录一次公司内部网或外部网，之后全天都可以访问需要使用的每个应用，无需每天在多个应用中进行多次登录。通过大幅减少用户需要记住的密码数量和管理员需要管理的用户帐户数，SSO 还可以增强组织的安全态势。

具体来说， SSO 具有以下优势：

- **用一个高强度密码代替多次填写造成的密码疲劳：** 需要管理大量密码的用户经常会为每个应用设定相同的安全性弱的短密码，或者只是稍有不同的密码。 黑客破解其中一个密码之后，就可以轻松访问多个应用。 SSO 通常可以将数十个长度短、安全性弱的密码缩减为一个复杂且安全性强的长密码，这样用户更容易记住，黑客更难以破解。
- **帮助预防不安全的密码存储习惯：** SSO 可以减少或消除对密码管理器、在电子表格中存储密码、使用便笺等其他记忆辅助工具来记录密码的需求，这些方式都更容易导致密码被其他人窃取或偶然看到。
- **降低被黑客攻击的概率：** 根据 IBM 的《2021 年数据泄露成本报告》，凭证泄露是数据泄露最常见的初始攻击媒介，在所有数据泄露中占 20%，而凭证泄露引起的泄露事件导致受害者平均损失 431 万美元。 密码更少意味着潜在攻击媒介更少。
- **简化用户帐户的管理、配置和停用：** 借助 SSO，管理员可以更集中地控制身份验证要求和访问权限。 在用户离开组织时，管理员删除权限以及停用用户帐户的步骤减少。
- **帮助简化监管合规过程：** SSO 有助于符合或更容易符合一些法规要求：关于个人身份信息保护 (PII) 和数据访问控制以及某些法规（如 HIPAA）中有关会话超时的特定要求。

### 相关技术

SSO 可使用任何一种身份验证协议和服务来实现，目前比较主流的方案有：

**SAML/SAML 2.0**

SAML（安全性断言标记语言）是使用时间最长的开放标准协议，用于在身份提供程序和多个服务提供程序之间交换加密的身份验证和授权数据。 SAML 比其他协议更能控制安全性，因此通常用于在企业或政府应用域内部和二者之间实施 SSO。

**OAuth/OAuth 2.0**

OAuth/OAuth 2.0（开放授权）是一个开放的标准协议，用于交换应用之间的授权数据，而不会暴露用户的密码。 OAuth 支持使用单点登录来简化通常需要分别登录的应用之间的交互。 例如，借助 OAuth，LinkedIn 可以在您的电子邮件联系人中搜索潜在的新网络成员。

**OpenID Connect (OIDC)**

OICD 也是一个开放标准协议，使用 REST API 和 JSON 身份验证令牌，允许网站或应用通过另一个服务提供商对用户进行身份验证，以此授予用户访问权限。

OICD 位于 OAuth 上层，主要用于实现对第三方应用、购物车等的社交登录。 OAuth/OIDC 是一种轻量级的实现，通常由 SAML 用于跨 SaaS（软件即服务）和云应用、移动应用和物联网 (IoT) 设备实施 SSO。

**LDAP**

LDAP（轻量级目录访问协议）定义一个用于存储和更新用户凭证的目录，以及一个针对该目录对用户进行身份验证的过程。 LDAP 于 1993 年推出，目前仍然是许多实施 SSO 的组织所青睐的身份验证目录解决方案，这是因为 LDAP 支持他们提供对目录访问的细粒度控制。

EMQX Cloud 支持通过 OIDC 来实现和 SSO 解决方案的整合对接。

## 如何在 EMQX Cloud 使用 SSO 

### 开启和配置 SSO

首先我们需要在 EMQX 官网 注册账号并且登录到 EMQX Cloud 控台。在右上角的用户菜单选择 “SSO”，进入到 SSO 配置页面。

![开启 SSO](https://assets.emqx.com/images/1803dbda2492718cf7c83eb60e7e439b.png)

在本篇文章中，我们使用 Microsoft Entra ID (Azure Active Directory)（简称 Azure AD） 作为示例来集成。而 EMQX Cloud 也可以和其他支持 OIDC 协议的身份提供商完成对接。

![Azure AD](https://assets.emqx.com/images/d7356c53718f409568efd71092cc14ba.png)

第一步：在 Microsoft Entra ID (Azure Active Directory) 创建应用

![EMQX Azure AD 配置项](https://assets.emqx.com/images/3b448d1330b0fb091f0c66b0078c29ff.png)

第二步：在 EMQX Azure AD 配置项中配置 Tenant ID, Client ID 和 Client Secret。

![配置 SSO](https://assets.emqx.com/images/41ec11099806b0342821369cf16312a1.png)

第三步：当成功配置之后，EMQX Cloud 的 SSO 登录功能就成功开启了。但是想要完成子账号的登录，还需要分别在 Azure AD 创建并授权子账号以及在 EMQX Cloud 创建子账号。

![成功启用 SSO](https://assets.emqx.com/images/4098842dcd5ca55f5de914e750170f93.png)

第四步：在 Microsoft Entra ID (Azure Active Directory) 创建子账号并授权应用。

![创建子账号并授权应用](https://assets.emqx.com/images/37339d694e9b934f201c77649ed2e025.png)

第五步：EMQX Cloud 创建子账号并授权项目

![创建子账号并授权项目](https://assets.emqx.com/images/332fba539533a606cc7ac9def3c44e9e.png)

请查看帮助中心文档来了解详细的配置说明以及功能介绍。【[EMQ Documentation](https://docs.emqx.com/zh/cloud/latest/feature/sso_overview.html)】

### 总结

在 EMQX Cloud 开启 SSO 能力之后，用户可以方便地使用企业账号管理系统登录到部署控制台，将 EMQX Cloud 作为一个应用登录，而无需单独进行身份验证，节省了时间和精力，提高了效率和体验。同时减少了安全风险，并且方便大规模的企业做账号管控以及达到合规方面的要求。

 

**参考**

- [Identity Providers (IdPs): What They Are and Why You Need One | Okta](https://www.okta.com/identity-101/why-your-company-needs-an-identity-provider/) 

- [Single Sign On (SSO) | IBM](https://www.ibm.com/cn-zh/topics/single-sign-on)



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
