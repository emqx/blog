物联网场景中，各类设备终端的种类繁杂，所使用的通信协议各异，从而使得应用层的数据格式也各不相同。为了帮助用户实现统一数据格式，**EMQX Cloud 最近推出了自定义函数功能**：根据用户自定义的脚本对设备上报的数据进行预处理，并将脚本返回的任意符合用户使用场景需求类型的数据流流转至消息订阅方。

这一功能可用于多种设备端上报数据预处理场景，如将指定范围内的数据进行数据持久化，或是将非标准格式数据处理为符合应用标准的格式，以便应用层直接使用等。在[之前的文章](https://www.emqx.com/zh/blog/data-codec-using-custom-functions)中，我们以数据编解码、格式处理与业务告警等场景为例，向大家介绍了自定义函数是如何在具体业务场景中发挥价值的。

在本篇文章中，我们将对这一功能的使用操作进行详细讲解，帮助大家更好地在实际项目中快速使用。

![自定义函数流程](https://assets.emqx.com/images/4dc662d24248f4da1a820153f755ff94.png)


## 开通自定义函数

自定义函数功能为 EMQX Cloud 增值服务，目前仅在专业版提供，且用户需要创建在阿里云（张家口之外的地区）的专业版部署开通该增值服务。

您可以通过以下两个入口开通自定义函数。

**方式一**：登录 EMQX Cloud 控制台，在顶部菜单栏点击「增值服务」，找到自定义函数，点击「开通服务」，并在提示弹框中点击确认。

![开通自定义函数](https://assets.emqx.com/images/5cce58d7f43836d93fe8fd8b2cd10fb2.png)

**方式二**：在部署详情页面的左侧菜单栏找到「自定义函数」并点击「开通服务」，并在提示弹框中点击确认。

![开通自定义函数](https://assets.emqx.com/images/36f7b57ef65ac8df4964491dac4b983e.png)

选择您需要开通自定义函数服务的部署（注：仅阿里云专业版非张家港区域部署可开通）

![选择您需要开通自定义函数服务的部署](https://assets.emqx.com/images/c66221a77571ca4d7805427b2eef946d.png)

在完成服务开通流程后， 等待约 2-3 分钟即可开通配置成功。

![等待约 2-3 分钟即可开通配置成功](https://assets.emqx.com/images/2502daac4396953c3bce89507d5ba92b.png)

**计费说明**

自定义函数服务主要通过函数的调用次数来计算费用，计费规则如下：

1. **创建函数不收取任何费用**，一个部署下可以创建最多 **20** 个函数。
2. 成功创建的函数将在数据集成的规则当中被引用和调用，**每成功调用一次**计入一次调用次数。
3. 每一个创建了函数计算的部署，**每月**都将获得 **5 万次的免费调用次数**，免费调用次数将在**每月初更新**。
4. 当月的免费调用次数用完之后，将会以 **¥0.03 / 万次**的价格在帐户余额中扣取，费用可以在满 1 万次的时间点小时账单中查看到。
5. 调用次数将会在每月底进行重置，不足 1 万次以 1 万次计价。

计费示例：

某用户当月调用次数为 506,500 次，扣除免费的 5 万次调用次数，付费调用次数为 456,500 次，前 450,000 次计费为 45 * ¥ 0.03 = ¥ 1.35 收费，最后的 6500 次由于不足 1 万次，将在月底以 1 万次的价格（0.03）进行结算，所以当月的总费用为 ¥ 1.38。

## 使用自定义函数

功能开通成功后，您可以通过下列流程配置使用自定义函数。

1、点击「新建」，创建函数，并设置自定义函数数据转化规则。

   ![创建函数](https://assets.emqx.com/images/b0572be4feff3169f70aa846088a6028.png)

2、输入函数名称，该名称将在之后创建的规则中被引用，一旦创建后，该名称将不可修改。

   ![输入函数名称](https://assets.emqx.com/images/869d009b37e4e4c44857811fe8869172.png)

3、在脚本输入框中输入 JS 脚本函数

- 脚本函数的入口函数名称为 codec，**入口函数名称不能改变**；
- 输入参数为 payload，在规则中调用函数时候输入的参数；
- codec 函数中需要返回函数运算之后的值，无 return 值将无法通过测试；
- 脚本执行时间**不能超过 3 秒**，否则将无法通过验证，不建议在脚本中编写高耗时的操作；
- 自定义函数支持 ECMAScript 5.1 及部分 ECMAScript 6 的语法，请参考以下 ES6 方法箭头函数
  - Promise
  - 解构符
  - Class
  - 模版符号

4、选择 payload 输入类型，目前自定义函数支持 3 种数据类型的输入：Byte、JSON、字符串。

   ![选择 payload 输入类型](https://assets.emqx.com/images/7dea0e6dec5b79a06b2d862ac8b371b5.png)

具体转化示例请参考自定义函数帮助文档：[https://docs.emqx.com/zh/cloud/latest/vas/codec.html#创建函数](https://docs.emqx.com/zh/cloud/latest/vas/codec.html#创建函数) 

5、新建成功后，可按照函数名称、状态搜索找到设置好的自定义函数，可进行修改、删除操作。

![查看自定义函数](https://assets.emqx.com/images/6da88c1b104dbf78e0c604089a0eab86.png)

6、调用函数

   函数定义完成后，您可在数据集成的规则中进行调用。

   如果需要快速验证自定义函数脚本是否成功配置，您可以通过新建空动作调用定义好的函数。

   具体调用规范可查看：[https://docs.emqx.com/zh/cloud/latest/vas/codec.html#调用函数](https://docs.emqx.com/zh/cloud/latest/vas/codec.html#调用函数) 

7、检查错误日志

   您可以在日志模块中筛选自定义函数相关的错误日志进行查看，根据错误日志提示快速定位自定义函数配置的错误并解决问题。

   ![检查错误日志](https://assets.emqx.com/images/51adfa39b220cd6eddd53892853f07b6.png)

更多关于使用自定义函数的场景案例，可查看：[https://docs.emqx.com/zh/cloud/latest/vas/codec_demo.html](https://docs.emqx.com/zh/cloud/latest/vas/codec_demo.html) 

## 结语

通过本文，用户可以使用自定义函数这一最新功能实现满足自身需求的物联网数据格式转换，更加轻松地为上层应用提供数据支持。

目前自定义函数功能已开放免费试用，欢迎点击文末「阅读原文」体验与反馈您的宝贵意见！

原文链接：https://cloud.emqx.com/console/services/new?type=codec



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
