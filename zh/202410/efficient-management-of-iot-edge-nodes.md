配置管理是 IIoT 系统中不可或缺的组成部分，能够确保设备的安全性、可靠性和一致性。随着 IIoT 系统的规模和复杂性不断增加，配置管理的重要性愈加凸显。企业可以通过自动化、集中化的配置管理系统，优化设备管理，简化运维流程，提升管理效率，增强系统的灵活性和扩展性，并确保符合各类法规要求，最终实现更高效的工业物联网系统。

EMQ 自主研发的[工业互联数据平台 EMQX ECP](https://www.emqx.cn/products/emqx-ecp)，能够满足工业场景大规模数据采集、处理和存储分析的需求，提供边缘服务的快速部署、远程操作和集中管理等功能，助力工业领域数据互联互通，以数据 + AI 驱动生产监测、控制和决策，实现智能化生产，提高效率、质量和可持续性。

本文将详细介绍如何通过 EMQX ECP 边缘服务配置的版本管理与参数化下发功能，高效、灵活地管理工业物联网边缘节点。

### 准备工作

首先我们进到 ECP 的服务列表页面，点击「添加边缘服务」按钮，添加两个 NeuronEX 边缘服务。这里以添加现有服务为例，分别添加两个名为 test1、test2 的边缘服务。

![添加边缘服务](https://assets.emqx.com/images/3a79176b64b995a1320ce4e0e7057aa7.png)

添加完成后回到边缘服务列表页面，可以看到列出了 test1、test2 这两个新添加的边缘服务。

![边缘服务列表页面](https://assets.emqx.com/images/ee28bb896e77470ec16e68d5f41bb7b5.png)

### 配置模版的版本管理

**1、生成配置模版**

在 test2 边缘服务一行数据里，点击操作一栏中的「更多」按钮，然后在弹出框里点击「生成配置模版」。

![生成配置模版](https://assets.emqx.com/images/f86966a6464459927ed81bb5d5b10fee.png)

在生成配置模版对话框里，填入模版名称、模版版本；选择需要生成配置的驱动，如果模版类型选择的是「规则」，对应的也可以选择需要生成配置的规则。这里我们以生成一个名称为 temp1，模版版本为 v1.0.0 的配置模版为例，配置好后点击「确认」按钮。

![填入模版名称、模版版本](https://assets.emqx.com/images/3f6d30d97f1945d683f7ce0465032516.png)

进入到配置管理 - 配置模版，可看到刚才生成的 temp1 配置模版。

![配置管理 - 配置模版](https://assets.emqx.com/images/33ba3e1d8f40cede23e1b2d76f377b61.png)

**2、上传一个新版本的配置模版**

在配置模版页面，点击 temp1 模版对应的版本管理按钮。

![配置模版页面](https://assets.emqx.com/images/599155dffb2eea675455ad8ea3a36df1.png)

在模版版本管理对话框里，列出了我们刚生成的 v1.0.0 版本，点击「上传新版本」按钮来上传一个新的版本。

![上传新版本](https://assets.emqx.com/images/187bdfc0da3fdbca4db89ae3b6da0a76.png)

在上传新版本对话框里，填入需要上传的新模版版本，这里以 v1.0.1 为例，同时上传对应的配置模版文件，然后点击「确认」按钮。

![填入需要上传的新模版版本](https://assets.emqx.com/images/e7cccc2c6fafff694f0e74a1b360d51d.png)

上传完成后回到模版版本管理，可看到列出了刚新上传的 v1.0.1 版本。

![模版版本管理](https://assets.emqx.com/images/3a267f420b6309d84d59322b83d42c93.png)

### 配置模版的参数化下发

1、可以在模版版本管理或配置模版列表中点击需要下发模版的「下发」按钮，需要注意的是，在配置模版列表中点击「下发」按钮，此时下发的是配置模版最新的版本。

![下发](https://assets.emqx.com/images/51fc6a04718e86f2219221b369a1950d.png)

2、编辑配置模版内容，将需要参数化的值进行参数化标识替换，这里以 `password` 和 `username` 字段为例，参数化标识为 `${参数名}`。需要注意的是相同的参数名，下发的时候会填入相同的值。编辑完成后点击「下一步」。

![编辑配置模版内容](https://assets.emqx.com/images/6f592af5d863d5f970b85fc78f801079.png)

3、边缘服务选择 `test1`，点击「下一步」进入到参数编辑。在参数编辑这一步，可以看到上一步选中的边缘服务 `test1`，以及在编辑配置模版内容时我们标识的两个参数化参数名 `password_param` 和 `username_param`。这里以 test1 对应的 password_param 填入 public 为例，username_param 不填；default 对应的 username_param 填入 test 为例，若边缘服务的 username_param 没有配置值，则下发的时候会自动填入 default 中 username_param 配置的值。配置好后可以点击「预览」按钮查看实际下发的配置模版内容。

![配置下发](https://assets.emqx.com/images/0f5a3bdff801f3322e6f9f87bad8e4d4.png)

4、在配置预览里，可看到参数化标识已经替换成我们配置的值。

![配置预览](https://assets.emqx.com/images/fcafff9441e8ba524a42031ee86fac55.png)

5、预览没问题后，回到配置下发，点击「执行」按钮开始下发配置，下发执行完成后，可查看执行结果。

![查看执行结果](https://assets.emqx.com/images/22a4fb2e7308617959a1e0f825947c7d.png)

6、回到边缘服务列表页面，点击 test1 边缘服务的「详情」按钮，可看到刚下发的配置已经生效，创建了一个名为 test1 的 OPC UA 设备。

![详情](https://assets.emqx.com/images/8588cc96bf221a43c13a23a7715c2267.png)

7、进入到该设备的设备配置页面，可看到用户名为我们配置的 test。

![设备配置页面](https://assets.emqx.com/images/e0a2b66b99f0315dbd4487f159d8660a.png)

### 总结

至此，我们已经完整介绍了 EMQX ECP 边缘服务配置的版本管理与参数化下发功能。借助边缘服务配置的版本管理与参数化下发功能，用户可以快速下发配置到各个边缘服务，并且能高效地处理配置内容的差异化，从而实现边缘服务的一体化管理，提高工业现场运维效率，加快 IIOT 项目的快速部署实施及落地。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
