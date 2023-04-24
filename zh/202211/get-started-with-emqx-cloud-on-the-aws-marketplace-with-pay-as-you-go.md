近日，全球领先的开源物联网数据基础设施软件供应商 EMQ 旗下的全托管 MQTT 消息云服务 EMQX Cloud 正式上架全球云端事业领导者亚马逊 AWS Marketplace，与国际各大云端软件并列销售。

在 AWS Marketplace 中即付即用的 EMQX Cloud 的推出，将为开发人员带来简化的订阅体验。亚马逊全球客户可以更快速地通过 AWS Marketplace 选项卡检索到 EMQX 产品项，并通过 AWS Marketplace 控制台实现更加便捷的购买和软件订阅管理。

## 如何通过 AWS Marketplace 订阅 EMQX Cloud？

### 准备

1. 首先您需要拥有一个 AWS 账户，通过该账户登陆 [AWS Marketplace](https://aws.amazon.com/marketplace) 并订阅 EMQX Cloud。AWS 账户注册：https://portal.aws.amazon.com/billing/signup#/start/email
2. 如果您曾经使用某个邮箱注册并商用过 EMQX Cloud，您必须使用一个不同的电子邮件地址通过 AWS Marketplace 订阅 EMQX Cloud。
3. 如果您曾经使用某个邮箱注册过 EMQX Cloud 中国站，该邮箱也不支持从 AWS Marketplace 直接订阅 EMQX Cloud。

### 订阅流程

1、登陆 [AWS Marketplace](https://aws.amazon.com/marketplace) 并搜索 "EMQX Cloud"。

   ![在 AWS Marketplace 上搜索 EMQX Cloud](https://assets.emqx.com/images/f8e23c502a94447de5567526708796b2.png)

2、找到 EMQX Cloud 并点击 **Continue to Subscribe**。

   ![订阅 EMQX Cloud](https://assets.emqx.com/images/df466c21b822a148f63cb2aa0de12013.png)

   为了支持从 AWS Marketplace 上直接支付 EMQX Cloud 的消费账单，EMQX Cloud 会通过 AWS Marketplace Metering Service 中的 BatchMeterUsage 每小时发送计量记录，每个单位等于 0.01 美元。

   ![EMQX Cloud 账单](https://assets.emqx.com/images/2b07f7ee84f978488f7446cc381ddb01.png)

   最终消费账单和您直接使用 EMQX Cloud 按小时计费的价格一致，具体价格可参考 [EMQX Cloud Pring Details](https://docs.emqx.com/en/cloud/latest/price/pricing.html#price-details)。

   ![EMQX Cloud 账单](https://assets.emqx.com/images/cfdd965de2b4bd5574c7a5d89de6766a.png)

3. 确认定价细节并点击 **Subscribe**。

   ![点击订阅](https://assets.emqx.com/images/b8bac5b457a97a8be9e58fb612946c62.png)

4. 点击 **Set Up Your Account**。

   ![设置账户](https://assets.emqx.com/images/322cb5988773965d0bdeef65f53936bb.png)

5. 提供注册必要的信息，然后点击 **Start free trial**。

   ![开始试用](https://assets.emqx.com/images/a38526451dda7718f7288cf29a3ff676.png)

   您会收到一封来自 EMQX Cloud 的电子邮件，要求验证您的电子邮件地址有否有效。验证完成后，您会自动登录到 EMQX Cloud 控制台。

   > 注意：如果您已经使用该邮箱注册并商用了EMQX Cloud，您会看到下面的提示，这意味着您应该使用一个不同的电子邮件地址来通过 AWS Marketplace 订阅 EMQX Cloud。

   ![邮箱已被使用](https://assets.emqx.com/images/0d263a8c01c8f0a562a0b0caba2ee170.png)

6. 进入 EMQX Cloud Console 后，您可获得 14 天基础版（Standard）和专业版（Professional）版本的免费试用。超过 14 天后将会按照正常的小时计费模式进行计价。

   ![14天免费试用](https://assets.emqx.com/images/93c02f7a327748b64b3d21e83b0a3e6c.png)


## EMQX Cloud 快速上手

经过上面的简单步骤，您现在就可以通过 AWS Marketplace 订阅使用 EMQX Cloud了，所有的消费账单将通过 AWS Marketplace 进行支付。

关于如何学习上手使用 EMQX Cloud，可参考如下教程：

- [Have an overview of EMQX Cloud deployment](https://docs.emqx.com/en/cloud/latest/create/overview.html)
- [How to connect to the deployment with MQTT X](https://docs.emqx.com/en/cloud/latest/connect_to_deployments/mqttx.html)
- [How to configure TLS/SSL](https://docs.emqx.com/en/cloud/latest/deployments/tls_ssl.html)
- [VAS Introduction](https://docs.emqx.com/en/cloud/latest/vas/vas-intro.html)
- [Various ways to connect to your device](https://docs.emqx.com/en/cloud/latest/connect_to_deployments/overview.html)



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
