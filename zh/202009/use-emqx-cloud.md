## 摘要

在数分钟内创建全托管高可用 [MQTT 集群](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-3-challenges-and-solutions-of-emqx-horizontal-scalability)，快速接入物联网设备并立即开始产品原型设计与应用开发，将物联网数据存储到华为云上的 Kafka 与数据库中。

## 实验属性

- 难易程度：初级
- 实验时长：120分钟

## 实验目标与基本要求

使用户快速了解 EMQX Cloud 物联网云服务的优势与特性，完成账号注册与试用部署创建，接入物联网设备进行消息收发，存储设备数据到华为云 Kafka 与数据库中

## 实验摘要

1. 登录 EMQX Cloud
2. 创建 华为云鲲鹏 试用部署
3. 初始化客户端信息
4. 接入设备进行消息收发
5. 打通华为云-EMQX Cloud VPC 网络
6. 将物联网数据存储到华为云 Kafka
7. 将物联网数据存储数据到云数据库 GaussDB(for Mongo)



## 实验步骤

### 领取代金券，购买华为云 Kafka 与数据库

领券链接：[点击前往领取100元代金券](https://account.huaweicloud.com/usercenter/#/getCoupons?activityID=P2008240947144281K3W0ZA1RV2D2C&contentID=PCP2008240946236230RRLRX51AFLQE1)

<div style="width: 100%; margin: 10px 0; width: 260px;padding: 6px;border: 1px solid #34c388;">
<div style="font-size: 12px">领券失败？微信添加 EMQ 小助手处理</div><img src="https://assets.emqx.com/images/f78798015e84cc54e66e14ba7a8e854d.jpg" style="width: 80px"/>
</div>


### 1. 登录 EMQX Cloud

EMQX Cloud MQTT 公有云服务来自于 EMQ 服务客户总结的一些最佳实践， 致力于提供快速部署、轻松管理、弹性扩展、跨多云部署的物联网 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 服务。

点击右上角 登录 按钮，使用实验室提供的账号登录 EMQX Cloud，点击 控制台 进入 EMQX Cloud 控制台页面。



### 2. 创建华为云部署

在控制台 部署 页面点击 创建 部署，选择 华为云，选择试用部署，完成部署创建。等待 2~3 分钟后部署完全启动后即可正常使用。

![img](https://assets.emqx.com/images/21f06cad6643ece29ff887b437b26b95.png)            



完全启动后，可以看到当前部署的状态以及对应的规格、MQTT 接入信息。

![img](https://assets.emqx.com/images/3edfe03d1e6f7db84db4434ce025ef4c.png)            



### 3. 初始化客户端信息

#### 3.1 客户端认证信息

EMQX Cloud 采用 MQTT 用户名、密码认证方式，客户端需携带正确信息才能成功连接。

在 EMQX Cloud 部署详情页面，点击 认证鉴权 选项卡，在 认证 部分输入用户名与密码，点击 添加 按钮完成客户端信息初始化。

- 用户名为：emqx_u
- 密码：123321

![img](https://assets.emqx.com/images/3c4bdab838487a7a2fe137d1562573b5.png)            

#### 3.2 客户端 ACL 信息

对于安全级别较高的物联网应用，可以设置客户端的发布订阅 ACL，“所有客户端，禁止向 cmd/# 主题发布消息” 的 ACL 规则设置如下：

- 用户名：全部用户($all)
- 主题：cmd/#
- 是否允许：不允许
- 主题动作：pub

![img](https://assets.emqx.com/images/3151a9ee3be85a0e10f088ee48b20f4c.png)            



### 4. 接入设备进行消息收发

EMQ 提供一个在线 MQTT 测试工具，访问 <http://tools.emqx.io/>，使用部署提供的连接信息和 3 步骤中初始化的客户端信息进行连接。

![img](https://assets.emqx.com/images/fd6ed545c76bf0a4decf91b82ba97779.png)            

连接成功后订阅相应的主题，进行发布、订阅测试：

![img](https://assets.emqx.com/images/a6eb6219d5da3c3ed3b2112a2d9157bc.png)            

### 5. 打通华为云-EMQX Cloud VPC 网络



> 提示：EMQX Cloud 试用部署不支持打通 VPC，可以直接使用公网地址连接。


**什么是 VPC**

VPC (Virtual Private Cloud)，也叫专有网络、私有网络。在同一个 VPC 中的所有资源相互连通，不同 VPC 的资源之间默认相互隔离。

正常情况下，你拥有的云资源和 EMQX Cloud 资源是在两个不同的 VPC 中，彼此无法连通。为了使用规则引擎，你需要使用对等连接，连通两个 VPC。

**注意事项**

1. EMQX Cloud 只支持同一区域创建对等连接
2. EMQX Cloud 不支持 10.10.0.0/24 ～ 10.32.255.0/24 范围内的网段，请合理规划您的 VPC 网段
3. 对等连接与资源相互绑定，创建资源前请先创建对等连接

#### 操作步骤

1. 在部署 详情 选项卡，点击 +VPC 对等连接 按钮，记录 EMQX Cloud 上的 VPC 信息：
  
    注意：暂时不要关闭该页面

    - 部署 VPC ID
    - EMQX Cloud 账户 ID
    - 部署 VPC 网段

    ![img](https://assets.emqx.com/images/dbd8afeb9ac1672f316a292a317a8567.png)            



2. 使用实验室提供的华为云账号登录华为云，进入控制台 -> 虚拟私有云 VPC

    ![img](https://assets.emqx.com/images/d84584cc19dfcd58edacd1bd95fa518a.png)            


3. 点击 对等连接 -> 创建对等连接，选择其它账户。填入刚才在 [EMQX Cloud 控制台](https://cloud.emqx.io/console) 记录的信息，点击确定创建对等连接请求

    - 对端项目 ID == EMQX Cloud 账户 ID
    - 对端VPC ID == 部署 VPC ID

    ![img](https://assets.emqx.com/images/438b387bf3206296a4ed930bb362874f.png)            



4. 在对等连接信息界面，记录下以下 3 个值

    - 1 为 对等连接 ID
    - 2 为 VPC 网段
    - 3 为 VPC ID

    ![img](https://assets.emqx.com/images/626f7154ddd5718b34d8c71209ff0146.png)            


    ![img](https://assets.emqx.com/images/3ba507d10fc8bc79c75a2e035d8a30cf.png)            



5. 找到 我的凭证，记录下用户 ID

    ![img](https://assets.emqx.com/images/e0b5f7b4219a55bb2673970e724911ba.png)            



6. 回到 [EMQX Cloud 控制台](https://cloud.emqx.io/console)。填写步骤 4 记录的对等连接 ID，VPC 网段，VPC ID 和步骤 5 记录的用户 ID。点击确定，完成对等连接

    ![img](https://assets.emqx.com/images/17il0vgku77fgdpfoyzep4yrdw8rsl5d.png)            



7. 在华为云控制台，打开 虚拟私有云 VPC -> 路由表，将步骤 1 中的部署 VPC 网段加入到对应 VPC 的路由表中

    注意：下一跳类型为 对等连接

    ![img](https://assets.emqx.com/images/77b594cf38acbdc53e3929a140015712.png)            



8. 在华为云控制台里配置安全组，允许 EMQX Cloud 网段访问您的 VPC

    ![img](https://assets.emqx.com/images/228f5241d4122035289857eb96036f53.png)             

至此 EMQX Cloud 与华为云 VPC 网络已经打通，



### 6. 将物联网数据存储到华为云 Kafka

[Kafka](https://kafka.apache.org/) 是由 Apache 软件基金会开发的一个开源流处理平台。该项目的目标是为处理实时数据提供一个统一、高吞吐、低延迟的平台，是一个“按照分布式事务日志架构的大规模发布/订阅消息队列”，这使它作为企业级基础设施来处理流式数据非常有价值。

通过 EMQX Cloud 规则引擎，你可以将数据桥接到 Kafka 服务，也可以设定消息模板，在 Kafka 服务中生产特定的消息。

#### 6.1 初始化分布式消息服务 Kafka

使用实验室提供的华为云账号登录华为云，打开 https://www.huaweicloud.com/product/dmskafka.html 华为云分布式消息服务 Kafka 产品页面，选择 立即购买，注意以下几点信息，其他可自行设置：

- 区域：选择 EMQX Cloud 部署相同的区域，如 华南-广州
- 虚拟私有云：选择上一步中创建的 VPC，选择对应的子网
- 安全组：确保 Kafka 能够被访问，建议开放 TCP 9092 端口全部访问权限

点击 立即购买 完成创建，进入 https://console.huaweicloud.com/dms/?engine=kafka&region=cn-south-1#/queue/manager/newKafkaList 查看创建进程，等待创建完成后查看并记录连接地址

![img](https://assets.emqx.com/images/1932b445bdd78e39bce057b292c2baca.png)            

![img](https://assets.emqx.com/images/f457090f28087a1b83f29573e32c9bd8.png)            

#### 6.2 设置规则引擎的筛选条件

在部署页面，选择规则引擎，点击创建。

![img](https://assets.emqx.com/images/496e984d1b36dd683880d3516c9a7550.png)            

我们的目标是：当主题 greet 收到 msg 为 hello 字符时，就会触发引擎。这里需要对 SQL 进行一定的处理：

- 针对 greet 主题，即 'greet/#'
- 对 payload 中的 msg 进行匹配，当它为 'hello' 字符串再执行规则引擎

- 根据上面的原则，我们最后得到的 SQL 应该如下：

```sql
SELECT
  payload.msg as msg
FROM
  "greet/#"
WHERE
  msg = 'hello'
```

可以点击 SQL 输入框下的 SQL 测试 ，填写数据：

- topic: greet

payload:

```
{
"msg":"hello"
}
```

点击测试，查看得到的数据结果，如果设置无误，测试输出框应该得到完整的 JSON 数据，如下：

```
{
  "msg":"hello"
}
```


注意：如果无法通过测试，请检查 SQL 是否合规，测试中的 topic 是否与 SQL 填写的一致。

#### 6.3 创建资源和动作

点击添加动作，在选择动作页，选择 桥接数据到 Kafka，点击下一步，在配置动作页面，点击创建资源。

![img](https://assets.emqx.com/images/6c4483a5922e4e530115e09721f86ce2.png)            

![img](https://assets.emqx.com/images/d8da0ad1095a8f5509f677cdf7aacc0a.png)            

在创建资源页面里，资源类型选择 Kafka，在 Kafka 服务器框里填写 6.1 步骤中保存的连接地址。点击测试，右上角返回 “测试资源创建成功” 表示测试成功。

![img](https://assets.emqx.com/images/489401abf7ae1cadf35ea31d6f5db5df.png)            

注意：如果测试失败，请检查是否完成对等连接，详情请看 [VPC 对等连接](https://docs.emqx.cn/cloud/latest/deployments/vpc_peering.html)，并检查 URL 是否正确。

点击确定，返回到配置动作页面，Kafka 主题填写刚刚创建的 testTopic 主题，在消息内容模板里填写 "hello from emqx cloud"，资源 ID 默认，点击确定。

![img](https://assets.emqx.com/images/84f20037ed55ae79a9c2ac45f88bf6fb.png)            

创建好的动作会显示在响应动作一栏里，确认信息无误后，点击右下角的确认，完成规则引擎的配置。
![img](https://assets.emqx.com/images/8e6648cd122bcaad45d73993b04bedaa.png)

#### 6.4 测试

如果您是第一次使用 EMQX Cloud 可以前往[部署连接指南](https://docs.emqx.cn/cloud/latest/connect_to_deployments/introduction.html)，查看 MQTT 客户端连接和测试指南

我们尝试向 home/sensor 主题发送下面的数据

```
{
  "msg":"hello"
}
```
在规则引擎页中，点击监控可以看到动作指标数的成功数变为 1。

![img](https://assets.emqx.com/images/d4729bc87fdd005ad7ad740b5724cbce.jpg)            

 至此，规则命中时在 Kafka 实例中消费者可以接收到 EMQX Cloud 转发过来的消息。


**添加小助手微信，进入 EMQ & 华为云技术交流群，与更多技术牛人深入交流、共同成长。**
![EMQX 微信小助手](https://assets.emqx.com/images/237cdd1601705d7fc794253c757c1d65.png)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
