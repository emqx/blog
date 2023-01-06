前不久，Google 宣布其旗下的 GCP IoT Core 即将在 2023 年 8 月 16 日停止提供服务。这意味着大量使用 GCP IoT Core 的用户可能需要将他们的 IoT 应用迁移到其他物联网云服务。除了云服务的迁移，很多用户也在直接利用谷歌云生态，使用 GCP 上丰富的数据服务来处理物联网数据。

作为和 GCP IoT Core 一样基于 MQTT 的全托管消息云服务，EMQX Cloud 支持部署在 GCP 多个区域，是替代 IoT Core 的理想选择。此外，**EMQX Cloud 新增的 GCP Pub/Sub 数据桥接支持**，可以帮助用户轻松无缝连接之前在 GCP 其他数据服务中创建的物联网应用，快速完成迁移且不影响现有业务。


## GCP Pub/Sub 介绍

GCP Pub/Sub 是 Google Cloud Platform (GCP) 中的一项消息传递服务，可以让用户在应用程序之间进行实时数据流传递。它提供了丰富的 API，用户可通过各种语言对消息进行发布和订阅。此外，GCP Pub/Sub 还提供了丰富的数据处理工具，帮助用户对接收到的消息进行复杂的处理和分析。

### 充分利用 GCP 的大数据能力

GCP Pub/Sub 提供了丰富的数据处理服务，EMQX Cloud 支持数据桥接到 GCP Pub/Sub 后，用户就可以利用 GCP 的大数据分析能力，对物联网设备的数据进行更深入的分析，为物联网应用提供更为丰富的信息支持。同时，之前使用 GCP IoT Core 的用户，很有可能已经在 GCP 的数据处理服务中建立了完整的应用，那么此时更换云平台，只需建立数据连接，就可以使用之前创建的服务。

### 更强的数据处理能力

GCP Pub/Sub 提供了丰富的 API，用户可以通过编程方式对数据进行更精细的控制，实现更复杂的数据处理。

### 为出海用户提供更多便利

使用 EMQX Cloud，您可以得到最高 7*24 来自 EMQX Cloud 技术支持工程师的帮助，相较于和 GCP 海外的工作人员使用邮件沟通，效率会大大提升。并且 EMQX Cloud 提供了丰富的帮助文档和教学视频，助您轻松上手使用。

总之，支持数据桥接到 GCP pub/sub 后，EMQX Cloud 可以为用户提供更为丰富的数据集成能力，让物联网应用更好地与 GCP 平台集成，为之前使用 GCP IoT Core 相关服务的物联网出海用户提供了极大的便利。

更多关于 Pub/Sub 的信息及使用方式，可以参考：[用于应用和数据集成的 Pub/Sub  | Google Cloud](https://cloud.google.com/pubsub?hl=zh-cn) 


## 如何使用数据集成功能桥接数据到 GCP Pub/Sub

如您需要使用 GCP Pub/Sub 服务，请访问 EMQX Cloud [海外站点](https://www.emqx.com/en/try?product=cloud)注册账号使用，并且推荐您选择 GCP 平台创建部署。

### 创建 GCP 平台的专业版部署

![创建 GCP 平台的专业版部署](https://assets.emqx.com/images/2c7097644cfb2f385dcbcf60bb8444aa.png)

选择云平台为 GCP，并按需选择规格，创建部署。

### 配置 GCP Pub/Sub

访问 GCP Pub/Sub 控制台，创建一个新的 topic。在此我们设置 Topic ID 为 my-topic。

![配置 GCP Pub/Sub](https://assets.emqx.com/images/92c83e557f3dda831e7112dee3df4906.png)

### 配置数据集成桥接数据到 GCP Pub/Sub

1. 访问 EMQX Cloud 控制台，在 Data Integration 页面中选择 GCP PubSub。

   ![EMQX Cloud 控制台](https://assets.emqx.com/images/74609df5ae8f75e82f14c3371085613b.png)

2. 填写 Service Account JSON 和其他信息，并测试是否资源可用。

   您可以在 GCP 控制台中，通过如下操作创建 Service Account JSON

   选择 appropriate project - IAM & Admin - Service Accounts - Email， 点击 KEYS，生成一个用于身份验证的 JSON 文件。

   ![填写 Service Account JSON 和其他信息](https://assets.emqx.com/images/95fbacbb3063cd3b1dfd83e6a1a39805.png)

3. 编写 SQL 规则并添加相关动作。

   在此提供一段示例，您可以使用以下 SQL 语句创建新规则

   ```
   SELECT 
   timestamp as up_timestamp, 
   clientid as client_id, 
   payload.temp as temp,
   payload.hum as hum
   FROM
   "temp_hum/emqx"
   ```

   ![编写 SQL 规则并添加相关动作](https://assets.emqx.com/images/f1605527e0cd8e4629328089efc4598c.png)

   测试规则是否成立。填写测试用 payload、topic 和 client 信息，点击 SQL Test 进行测试。

   ![测试规则是否成立](https://assets.emqx.com/images/37f59f3b1c731d9822c7b518534339db.png)

   添加动作。在此我们使用上述创建的 GCP Pub/Sub topic 和信息模版。

   ```
   # GCP Pub/Sub message template 
   {"up_timestamp": ${up_timestamp}, "client_id": ${client_id}, "temp": ${temp}, "hum": ${hum}}
   ```

   ![将动作绑定到规则上](https://assets.emqx.com/images/fe226a011047432fdcfa874b1382fec0.png)

   将动作绑定到规则上后，点击 View details 可查看刚才创建的 SQL 语句规则和动作。

   ![查看刚才创建的 SQL 语句规则和动作](https://assets.emqx.com/images/083583e04d9093c20a3b0d46da9c622b.png) 

4. 使用 MQTT X 进行消息收发测试。

   您需要替换 `broker.emqx.io` 为您创建的部署的连接地址（可以在 Deployment Overview 页面找到），并添加设备认证信息。

   测试结果如下，您也可以在 EMQX Cloud 控制台和 GCP 控制台看到相应的消息处理和数据转发情况。

   ![MQTT 桌面客户端](https://assets.emqx.com/images/002277d5241d22238c12688693e3b93e.png)

   在 EMQX Cloud 创建规则的监控页面看到数据转发成功。

   ![在 EMQX Cloud 创建规则的监控页面看到数据转发成功](https://assets.emqx.com/images/70de545505dd0e78b1423b8043f93f6d.png)

   在 GCP Pub/Sub 控制台看到消息转发结果。

   ![在 GCP Pub/Sub 控制台看到消息转发结果](https://assets.emqx.com/images/c7dfe2f0165bfb8ad02e980706328dbb.png)

更多操作步骤及注意点，可参考：[帮助文档](https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_gcp_pubsub.html)。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
