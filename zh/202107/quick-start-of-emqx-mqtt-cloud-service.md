[EMQX Cloud](https://www.emqx.com/zh/cloud) 是 [EMQ 公司](https://www.emqx.com/zh/about)提供的一款全托管的物联网 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 云服务产品。通过该产品，我们可以快速搭建出一个稳定可靠、功能完整、性能优异的 MQTT 5.0 物联网平台，帮助各类设备数据快速上云，进行后续的分析。

在本教程中，我们将带您一步一步搭建一个物联网平台。在完成本教程后，您将了解:

1. 如何快速在 EMQX Cloud 部署一个 [MQTT 集群](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-3-challenges-and-solutions-of-emqx-horizontal-scalability)。

2. 如何配置 MQTT 集群的认证鉴权与访问控制。

3. 如何使用客户端工具连接 MQTT 集群。

4. 如何发布与订阅消息。

   

## 第一步：创建 EMQX Cloud 账号

首先我们前往 [EMQX Cloud](https://www.emqx.com/zh/cloud)，点击 “开始免费试用” 按钮。根据页面提示信息，完成用户注册流程。



## 第二步： 创建试用部署

在完成注册后，您可以返回首页，点击 “登录” 并进入控制台。

点击页面中间的“创建部署”按钮，开始部署流程。

![选择类型](https://assets.emqx.com/images/afbeb89427fe2f1a9821a2fcbd988439.png)


EMQX Cloud 提供三个版本供您选用，分别适用于不同的使用场景。

- 基础版：适用于 MQTT 协议或 EMQX Broker 产品的学习和体验，及轻量级物联网应用的开发。基础版提供 30 天免费试用。
- 专业版：适用于构建关键任务的物联网应用，本版本提供了数据持久化，消息分发，VPC 对等连接等高级功能。专业版提供 14 天免费试用。
- 旗舰版：适用于企业级物联网平台的构建，提供多地域及独享硬件部署的支持，并增加了设备管理、设备影子、物模型等功能。

在这里我们选择专业版进行部署，点击 “立即创建” 后，您可以进一步选择部署区域、最大连接数和TPS。

![配置](https://assets.emqx.com/images/de52eba8fc3ab4a8f3923f8d1f3b1b69.png)

在选择所需的产品规格后，点击“下一步”，可以进一步确认所选规格的集成信息、功能列表以及预估费用。

![确认](https://assets.emqx.com/images/db13585fde483bb247bea7bb5996cc3e.png)

点击 “立即部署”，等待几分钟后，您就可以拥有属于您的专享 MQTT 集群了。

## 第三步： 进入集群管理界面

在集群列表页面，您可以随时查看集群的部署进度。

![集群列表](https://assets.emqx.com/images/e14d4b3ebe6b32d8c96578e13075b78c.png)


当部署完成后，我们可以看到集群的运行状态为：运行中。此状态表明集群已经可以正常使用了。这时候我们点击集群即可进入集群管理界面。

![集群管理界面](https://assets.emqx.com/images/dbf89228789e10e052bd99a81c8e09f6.png)

进入管理界面后，我们可以直观地看到界面概览信息，包括集群的状态、连接情况，连接地址等信息。在左侧菜单栏中，可以查看集群所提供的各种配置和功能。

此时，我们可以记下集群的连接地址和连接端口，以便后续使用。

当然，在正式连接到集群前，我们还需要做一件重要的事情：设置客户端访问所需的认证信息和权限控制。

## 第四步： 添加认证

添加认证鉴权的过程非常简单，我们点击左侧菜单栏中的认证鉴权，此时会展开二级菜单，我们可以看到有两个栏目：“认证”与“访问控制”。

我们首先点击“认证”。在右侧页面，我们可以看到集群所添加的所有认证信息。此刻为空，说明目前集群还没有添加过认证。

![点击认证](https://assets.emqx.com/images/09f2690625ce27735c16adbb8130d589.png)

我们在右侧输入框中分别输入用户名 “test”和密码 “test” （您也可以输入任意期望的用户名和密码以供后续连接使用），点击添加。

![认证界面](https://assets.emqx.com/images/b8e30bc29e4d343429db61727ae13a5d.png)

此时我们可以看到，列表中出现了一条记录，代表刚才的认证信息已进添加成功。

您可以通过该界面，添加其他所需的认证信息。如果是商用集群，您还可以点击“导入”按钮，将设备认证信息批量导入到集群配置中去。



## 第五步：连接 MQTT 集群

至此，我们已经拥有了一个 MQTT 集群。连接 MQTT 集群有很多方式。通常正式使用的时候我们会选择用编程的方式，选择某个编程语言的 [MQTT 客户端 SDK](https://www.emqx.com/zh/mqtt-client-sdk)，建立连接并收发消息。我们也可以使用一些带有图像化界面的 [MQTT 客户端工具](https://www.emqx.com/zh/blog/mqtt-client-tools)来连接到 MQTT 集群。在本教程中，我们使用左侧导航提供的在线调试工具。

我们在 Host 和 Port 输入框中输入我们前面所部属集群的连接地址和端口（这些信息可以在集群管理的概览页面找到）。在 Username 和 Password 输入框中输入之前添加的认证信息 （本次教程中使用的“test/test”, 或者您自定义的用户名密码），点击“连接”即可。

![连接MQTT集群](https://assets.emqx.com/images/ab5a024a88e3fae55abbea3af80d0635.png)



## 第六步：发布与订阅消息

接着，我们先创建一个订阅。在这里我们设置主题名为“test/1”，点击“订阅”并展开。

![创建订阅](https://assets.emqx.com/images/ca6fc8db23a276ebebe61bc45b2884dc.png)

此时我们可以看到我们已经成功订阅了“test/1”主题。那么接下来，我们试着往该主题发布一条消息看是否能收到。我们首先将主题名称修改成“test/1”，然后选择我们之前设置的连接。

![发布](https://assets.emqx.com/images/cf4fbba8ec7873cca8b9f0b0babf04cf.png)

此时点击“发布”即可成功发布我们预设好的信息。

![发布成功](https://assets.emqx.com/images/04bfb979fd2c602cbab5dae0e7a8ae25.png)



至此，如果您跟着我们的教程一步一步操作，那么您已经成功的完成了集群创建、访问控制和收发消息的操作！

在本教程中，我们体验了从零开始构建一个 MQTT 物联网平台的过程。当然，这只是一个开始，EMQX Cloud 还有很多非常强大的功能等待您去尝试。例如，您可以配置 VPC 对等连接，使得您的 MQTT 集群可以与部署在同一个公有云平台同地域的其他服务集成。您也可以使用强大的规则引擎功能，将 MQTT 集群接收到的消息根据规则保存到不同的数据库中或者转发到其他消息队列中，而这些功能无需您编写一行代码！

在您使用 EMQX Cloud 产品的过程中，如有任何问题、意见或者建议，欢迎随时与我们取得联系：[cloud-support@emqx.io](mailto:cloud-support@emqx.io) 。希望 EMQX Cloud 可以帮助您的物联网业务更加顺利地开展。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
