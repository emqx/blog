在物联网业务场景中，往往涉及对海量物联设备产生数据的实时提取、过滤、分拆、转换等。EMQ 推出的全托管云原生 [MQTT 消息服务 EMQX Cloud](https://www.emqx.com/zh/cloud) 提供了高性能的内置数据集成功能，可以帮助用户实现与各种云服务（如 Kafka、MongoDB、AWS RDS、AWS DocumentDB、 AWS IoT 等）的连接，将物联网数据根据需求转存到各类第三方数据库、消息队列、数据系统中，从而简化物联网应用开发，加速业务交付。

本文将介绍如何使用 EMQX Cloud 数据集成功能通过公网桥接数据到 AWS IoT，从而借助 AWS IoT 轻松使用 AWS Lambda、Amazon Kinesis、Amazon S3、Amazon Machine Learning、Amazon DynamoDB、Amazon CloudWatch、AWS CloudTrail 和内置 Kibana 集成的 Amazon Elasticsearch Service 等 AWS 服务构建 IoT 应用程序。无需管理任何基础设施，即可实现对互连设备生成数据的收集、处理和分析等相关操作。

## AWS IoT 简介

### 什么是 AWS IoT

Amazon IoT Core 是一种托管的云平台，让互联设备可以轻松安全地与云应用程序和其他设备交互。Amazon IoT 可以支持数十亿台设备和数万亿条消息，并能处理这些消息并将其安全可靠地路由至亚马逊云科技终端节点和其他设备。借助 Amazon IoT，您的应用程序可以随时跟踪您的所有设备并与其通信，即使这些设备未处于连接状态也不例外。

![AWS IoT](https://assets.emqx.com/images/cd88449685a137579e66ead1185011a9.png)


### AWS IoT 平台的优势

（1）广泛而深入：AWS 拥有从边缘到云端的广泛而深入的 IoT 服务，提供本地数据收集和分析能力以及云上专为 IoT 设计的数据管理和丰富分析集成服务。                                 

（2）多层安全性：包括预防性安全机制（如设备数据的加密和访问控制）、持续监控和审核安全配置等。                   

（3）卓越的 AI 集成：AWS 将 AI 和 IoT 结合在一起，使设备更为智能化。支持多种机器学习框架。   

（4）大规模得到验证：AWS IoT 构建于可扩展、安全且经过验证的云基础设施之上，可扩展到数十亿种不同的设备和数万亿条消息。



## 使用 EMQX Cloud 桥接数据到 AWS IoT

### 开通 NAT 网关

在 EMQX Cloud 部署详情页面，开通增值服务 --- [NAT 网关](https://docs.emqx.com/zh/cloud/latest/vas/nat-gateway.html)，便于公网访问到 AWS IoT。

![EMQX Cloud 开通 NET 网关](https://assets.emqx.com/images/5f05769f59b57103e8e6939cd7d8cb07.png)


### 配置 AWS IoT

1. **创建事务**

   进入 AWS IoT 控制面板，找到管理-事务，点击创建事务，即可创建一个名为 emqx 的事务。

   ![AWS IoT 创建事务](https://assets.emqx.com/images/f53349734b85a10da917123f0f5da304.png)

2. **创建并下载证书**

   在创建好事务以后，可直接创建一个证书。

   ![AWS IoT 创建并下载证书](https://assets.emqx.com/images/161c54eb542bb7a24b889f45136000dc.png)

   证书创建完成以后，需要在该页面下载证书，用于设备连接时的双向认证。

   ![AWS IoT 下载证书](https://assets.emqx.com/images/65467bf36d67b60a3a11ad5cb5b700fa.png)

3. **创建策略并关联到证书**

   找到安全-策略，创建名为 emqx-bridge 的策略，编写策略，相关配置如下。

   ![创建策略](https://assets.emqx.com/images/0e9f66858969ad506f6dbf7951b2d4cb.png)

   ```
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": "iot:Connect",
         "Resource": "arn:aws:iot:us-east-1:845523974165:client/emqx-bridge_*"
       },
       {
         "Effect": "Allow",
         "Action": "iot:Publish",
         "Resource": "arn:aws:iot:us-east-1:845523974165:topic/emqx/bridge"
       },
       {
         "Effect": "Allow",
         "Action": "iot:Receive",
         "Resource": "arn:aws:iot:us-east-1:845523974165:topic/emqx/bridge"
       },
       {
         "Effect": "Allow",
         "Action": "iot:RetainPublish",
         "Resource": "arn:aws:iot:us-east-1:845523974165:topic/emqx/bridge"
       },
       {
         "Effect": "Allow",
         "Action": "iot:Subscribe",
         "Resource": "arn:aws:iot:us-east-1:845523974165:topicfilter/emqx/bridge"
       }
     ]
   }
   ```

   完成策略创建以后，需要关联到前一步创建好的证书。

   ![关联到证书](https://assets.emqx.com/images/ee00990c5d2a71dc67388c16008fb9f0.png)

4. **获取 AWS IoT 的公网连接地址**

   在设置获取到连接地址 endpoint，用于设备连接。

   ![获取 AWS IoT 的公网连接地址](https://assets.emqx.com/images/09c2e6cdf071b65e5aa3d39b55497b0d.png)

### 配置 EMQX Cloud 数据集成

进入 EMQX Cloud 的部署页面，点击数据集成 - MQTT Bridge。

![配置 EMQX Cloud 数据集成](https://assets.emqx.com/images/0531e3b369507373896bfe570dd8d95f.png)

在资源页面填写 AWS IoT 的资源详细信息。

![填写 AWS IoT 的资源详细信息](https://assets.emqx.com/images/34e0814bca529bf5f65e397bcff968af.png)

确认资源可用以后，进行规则配置，筛选并处理数据。

![规则配置](https://assets.emqx.com/images/140262d0ee9cba384c2ebe34d7649e74.png)

配置好规则以后，需要配置响应动作，即桥接数据到 AWS IoT。

![配置响应动作](https://assets.emqx.com/images/619b8c37bebb815a58eeaa4d481a73a1.png)

在完成创建资源 - 添加规则 - 添加动作以后，可在详情页面查看相关信息。

![查看详情](https://assets.emqx.com/images/acfde6b743081024171947ef69323ebc.png)

查看已创建的规则，点击监控，可查看到目前桥接成功监控次数为 0，即初始化状态。

![查看桥接成功监控次数](https://assets.emqx.com/images/59589fad2dd2e1cbfea38b07ed42459f.png)

## 测试验证

1. 使用 Python SDK 连接到 EMQX Cloud 部署，向主题 emqx/bridge 发送消息。

   ![向主题 emqx/bridge 发送消息](https://assets.emqx.com/images/6e1714bea4ab59a7dba550c8962995db.png)

2. 使用 MQTTX 连接到 AWS IoT，订阅 emqx/bridge，可以接收到来自 EMQX Cloud 部署的消息。

   ![使用 MQTTX 连接到 AWS IoT](https://assets.emqx.com/images/9eb19935bed890d83969d0ca6bb0c68f.png)

   ![使用 MQTTX 连接到 AWS IoT](https://assets.emqx.com/images/4eb9bd97882dab871eedf1cd252eee85.png)

3. 在 EMQX Cloud console 查看规则监控，可以检查桥接数据到 AWS IoT 成功与否。

   ![查看规则监控](https://assets.emqx.com/images/a0206f7e853b84bf110ccf52e4fe9f91.png)

## 结语

至此，我们完成了使用 EMQX Cloud 数据集成功能通过公网桥接数据到 AWS IoT 的全部流程。EMQX Cloud 灵活的数据集成功能，结合 AWS IoT 丰富的应用生态，用户在数分钟内即可创建一款物联网应用。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
