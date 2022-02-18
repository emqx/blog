[EMQX Cloud](https://www.emqx.com/zh/cloud) 作为一款全托管的 MQTT 服务，致力于为用户提供可靠、实时的物联网数据移动、处理和集成能力，通过完善、自动化的监控运维，免除用户的管理维护负担，加速物联网应用开发。

通过 EMQX Cloud，用户在数分钟内即可创建高可用的 MQTT 集群，进行设备接入。随后的整个使用周期中，EMQ 全球服务支持团队将提供最高 7*24 不间断的技术支持和运维服务。在使用过程中遇到任何问题，用户可以随时通过工单、电子邮件、电话等方式快速获得响应。

除了全天候的售后服务支持，EMQX Cloud 也提供种类丰富的自动化告警提醒和告警集成，以实现故障问题预警，方便运维人员及时作出相应处理，防止因为诸如部署消息流失等原因造成的不必要的损失。

近期，**EMQX Cloud 团队针对自动化告警功能进行了进一步优化更新，增加了新的告警集成模式**，这将使整个产品的自动化预警功能模块更加完善，为用户带来更稳定保障。

## 丰富的告警模式与告警事件

EMQX Cloud 目前支持以下几种告警模式，其中 Webhook 告警为本次新增：

1. 邮箱告警集成，通过添加邮箱接收告警信息
2. PagerDuty 事件告警集成
3. Webhook 告警集成，将告警信息发送到通信软件或用户自己的服务中

同时配置了丰富的告警事件：

| **类型**                 | **级别** | **信息**                                                     | **解决**                                               |
| ------------------------ | -------- | ------------------------------------------------------------ | ------------------------------------------------------ |
| 连接数过高               | warning  | 部署连接数过高：{当前连接数}                                 | 升级部署规格                                           |
| 流量使用过高             | warning  | 过去24小时内部署流量过高：{过去24小时流量总数}               | 检查设备流量是否正常，正常则需升级部署规格             |
| 证书过期告警             | warning  | 部署证书将在 {num} 天后过期，请及时更新!                     | 及时更新部署证书                                       |
| 客户端认证失败           | warning  | 部署出现大量认证失败的客户端连接                             | 检查客户端认证配置是否正确                             |
| 客户端 ACL 认证失败      | warning  | 部署出现大量 ACL 认证失败的客户端消息发布                    | 检查部署访问控制配置是否正确                           |
| 部署非标准 MQTT 协议连接 | warning  | 部署出现大量非标准 MQTT 协议的客户端连接                     | 检查客户端连接使用的 MQTT 协议是否为标准 MQTT 协议     |
| 部署消息丢弃告警         | warning  | 部署由于客户端长期离线或主题未被订阅导致大量消息丢弃         | 客户端设置 clean session 为 False 或客户端设置自动重连 |
| 部署 TPS 超过限制告警    | warning  | 部署超过限制请及时调整客户端发送速率，否则您将无法发送新的消息 | 及时调整客户端发送速率，使发送速率小于部署限制的 TPS   |
| vpc 对等连接异常         | error    | Vpc 对等连接状态异常：{状态}                                 | 检查部署对等账户对等连接账户                           |
| 规则引擎 xxx 资源异常    | error    | 部署规则引擎 xxx 资源异常                                    | 检查部署规则引擎中 xxx 资源配置是否正确                |

具体告警提示如下：

![EMQX Cloud 告警提示信息](https://static.emqx.net/images/fec1d88211a87b30f49abc381105398a.png)

## 如何设置告警集成

进入EMQX Cloud 控制台，左侧菜单栏，点击「告警」，即可开始设置告警集成。

### 邮箱告警集成

只需添加接受告警信息的邮箱，当部署产生告警时即可第一时间向邮箱发送告警提醒。

![EMQX Cloud 邮箱告警集成](https://static.emqx.net/images/f97be1c58f54e17cb4519f90732a0e39.png)
 

### PagerDuty 告警集成

将告警信息发送到 PagerDuty 中的事件，并且通过 PagerDuty 指定通知方法。

1. 在 PagerDuty 创建告警服务

	![在 PagerDuty 创建告警服务](https://static.emqx.net/images/9cb64e8a45ad0b50493ddcc4d51e420d.png)

2. 添加 api v2 集成，并复制集成秘钥

	![添加 api v2 集成](https://static.emqx.net/images/351025ab452229d20292d80ca0e5ca20.png)

3. 在 EMQX Cloud 中复制集成秘钥即可

	![复制集成秘钥](https://static.emqx.net/images/75fe0a9e6bbcad76d1c35693ad9182df.png)

### Webhook 告警集成

通过 Webhook 告警集成，您可以将告警发送到通信软件或是自己的服务中，同时可以通过消息检测的功能测试 Webhook 是否正确配置，高度灵活自由，适配您正在使用的 IM 工具。

#### 向企业微信发送告警消息

在企业微信群中创建机器人(需要是群主身份才能创建)，选择「添加机器人」->「新创建一个机器人」-> 「添加机器人」。详细请参考 [群机器人设置说明](https://developer.work.weixin.qq.com/document/path/91770)。

1. 完成微信机器人的创建，复制链接； 

	![完成微信机器人的创建](https://static.emqx.net/images/5b12d44fbeff1842be16a1e28b7cd709.png)
 
2. 在 Webhook 告警中，选择企业微信，并填入告警名称和 Webhook 地址，完成配置；

	![填写告警名称和 Webhook 地址](https://static.emqx.net/images/caa149e6415000cf8e3a58dcea797c76.png)
 
3. 验证配置，可以通过测试功能，选择配置好的 Webhook 告警，即可发送默认消息检测是否配置成功。

	![检测是否配置成功](https://static.emqx.net/images/df69020156aa15d3790ef56a14f3bc31.png)


#### 向钉钉发送告警消息

1. 在钉钉中创建 Webhook 机器人，请参考[官方文档](https://open.dingtalk.com/document/robots/custom-robot-access)创建；

	![在钉钉中创建 Webhook 机器人](https://static.emqx.net/images/1b944afecf2da10831c3c854d4ae1a82.png)
 
2. 复制机器人的 Webhook 地址，在告警配置中，选择钉钉，并填入告警名称和 Webhook 地址，完成配置。

3. 验证配置，可以通过测试功能，选择配置好的 Webhook 告警，即可发送默认消息检测是否配置成功。

#### 向 Slack 发送告警消息

1. 在 Slack 创建Webhook，获取 Webhook URL 地址。更多信息，请参见 [Sending messages using Incoming Webhooks](https://api.slack.com/messaging/webhooks?spm=a2c4g.11186623.0.0.2fa63db5J0PRQp)；

2. 复制 Webhook API 地址，在告警配置中，选择 Slack，并填入告警名称和 Webhook 地址，完成配置。

   ![向 Slack 发送告警消息](https://static.emqx.net/images/aa041eb3d44ddb294e0a5bcf42e51034.png)

3. 验证配置，可以通过测试功能，选择配置好的 Webhook 告警，即可发送默认消息检测是否配置成功。

#### 向自定义服务发送告警消息

除了向通讯软件中的机器人发送告警消息，我们还可以向自己的服务通过 Webhook 发送消息。

1. 首先需要搭建好服务能接收和处理请求，在新建对话框中选择 「通用 Webhook 」。

2. 在新建对话框中填入 Webhook 服务的请求地址。同时也可以额外添加请求头的键和值。

	![向自定义服务发送告警消息](https://static.emqx.net/images/98c7be871386ae04b7ce17a65bb8f7cc.png)

3. 验证配置，可以通过测试功能，选择配置好的 Webhook 告警，即可发送默认消息检测是否配置成功。


通过以上丰富的告警模式，您可以灵活自由的设置不同告警事件进行故障告警，在异常发生时可以第一时间处理，保障业务的稳定性。

EMQX Cloud 现提供 14 天 免费试用，欢迎大家访问 [EMQX Cloud 官网](https://www.emqx.com/zh/cloud)试用新功能并向我们提出宝贵意见。
