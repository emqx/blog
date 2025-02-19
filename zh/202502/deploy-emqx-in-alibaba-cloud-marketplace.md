作为全球领先的 MQTT 消息接入平台，EMQX Platform 已正式入驻阿里云 Marketplace，支持以按量计费模式使用服务，助力企业快速构建高并发、低时延的物联网应用。

本文将为您介绍如何将 EMQX 账户与阿里云计费账户关联，以及如何取消对已有服务的订阅。

## 前提条件

**开始前请确保：**

- 您拥有一个有效的阿里云账户，该账户允许您使用 EMQX Platform 并通过阿里云直接计费。
- 登录阿里云云市场，并确保您的阿里云账户已由您的计费管理员启用购买权限。
- 一个阿里云账户只能关联一个 EMQX 账户，反之亦然。若关联过其他账户，则可能导致账户关联失败。

## 将阿里云计费账户关联到 EMQX 平台

**1、登录到您的阿里云控制台。**

**2、导航到** [**阿里云市场**](https://market.aliyun.com/)**。**

**3、搜索 EMQX 产品。**

您可以在搜索栏中输入「EMQX Platform (Pay as you go)」搜索产品；也可以点击 EMQX Platform [登录和注册](https://accounts.emqx.com/signup?continue=https%3A%2F%2Fcloud-intl.emqx.com%2Fconsole%2F)页面底部的「阿里云 Marketplace」进入目标页面。

![搜索产品](https://assets.emqx.com/images/d4f0df11f686a4e4746974929de7021f.png)

**4、确认定价信息。**
阿里云 Marketplace 启用了 EMQX 部署计价单元，每个单位等于 0.01 元。阿里云 Marketplace 中的定价与 EMQX 平台直接按量购买定价相同。

![确认定价信息](https://assets.emqx.com/images/d925a519050f9a01d0ad8a753e010d0f.png)

**5、开通 EMQX 服务。**

- 在产品页面，点击 **立即开通**。

- 开通成功后，点击 **前往控制台**。

  ![开通成功](https://assets.emqx.com/images/0a3e973c6bf2c512a4ff6117be381b53.png)

- 在已购买的服务中找到 EMQX Platform 的服务，点击 **详情**。

- 在 **应用信息** 中点击 **前台地址** 重定向到 EMQX Platform 网站。

  ![应用信息](https://assets.emqx.com/images/3a2d5c5ecec8abccd4848fe390f649cb.png)

**6、设置 EMQX 账户。**

- 已有 EMQX 账户

  登录现有 EMQX 账户，您将自动重定向到索引页面。一个模态框将显示与您的阿里云计费账户关联的状态。

- 没有 EMQX 账户

  填写信息注册 EMQX 账户，单击 **开始试用** 按钮，您会收到一封来自 EMQX 平台的电子邮件，通过验证后您将自动登录 EMQX 控制台。

  ![注册 EMQX Cloud](https://assets.emqx.com/images/2274c40276c5742de39e64d1e9108de4.png)

**7、创建 EMQX 部署。**

![创建 EMQX 部署](https://assets.emqx.com/images/f25e89213b0b65daeb2f42ce7dccae00.png)

## 从阿里云市场取消关联 EMQX 平台

**在您取消关联 EMQX 平台前，请注意：**

- 取消订阅将停止您正在运行的部署，但试用部署除外。您可以继续使用试用部署，直到试用期结束。
- 停止的部署将在 3 天后被删除，请提前备份数据。

**取消关联操作步骤如下：**

1、登录您的阿里云控制台。

2、导航到[阿里云市场](https://market.aliyun.com/) - [买家控制台](https://market.console.aliyun.com/?spm=5176.product-detail.J_6jfoaFkLejSR8rOBKjs6f.d_1_main_1.384820045O47Ma#/?_k=3b8zx9)。

3、在 **已购买的服务** 中选择您希望取消关联的 **EMQX Platform (Pay as You Go)** 订阅，点击**关闭**。

![点击关闭](https://assets.emqx.com/images/7098fe6119faa4c48cc849089ed4f811.png)

4、系统会弹出一个窗口询问是否确认关闭。如果您确认取消订阅，请点击 **确认关闭**。

## **结语**

通过阿里云 Marketplace 部署 EMQX，企业可快速获得高效、稳定的物联网连接能力，无需运维配置，5 分钟即可完成服务上线，同时享受弹性计费与全球化部署优势。  

[**立即体验，在阿里云 Marketplace 中使用 EMQX Platform**](https://market.aliyun.com/products/9000000210/cmgj00069406.html?spm=5176.730005.result.2.8640414avVwPlF&innerSource=search_emqx)



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
