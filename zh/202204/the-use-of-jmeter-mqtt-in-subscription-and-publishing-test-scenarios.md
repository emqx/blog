通过之前的文章，相信大家已经熟悉了 JMeter 及 MQTT 插件的使用等基础知识。本文我们将介绍 JMeter MQTT 插件在订阅与发布测试场景中的使用。

## 订阅、发布场景介绍

**发布场景**

使用 MQTT Connect 请求模拟设备与 MQTT 服务器（本文以 EMQX 为例）建立连接，随后使用MQTT Pub Sampler 请求模拟设备发布消息到 MQTT Broker，在 MQTT Pub Sampler 后添加固定定时器模拟定时发布消息。

**订阅发布场景**

使用 MQTT Connect 请求模拟与 MQTT Broker 建立连接，其中订阅者订阅指定主题，发布者发布消息到指定主题。

## 使用 MQTT 插件编写测试脚本

### 发布脚本

1. 在测试计划下创建线程组。

   ![创建线程组](https://assets.emqx.com/images/1345aa6d58cab0ef4b3b9c47222cc9bd.png)

2. 在线程组下添加仅一次控制器及“MQTT 连接采样器”（即"MQTT Connect"）。

   ![添加 MQTT 连接采样器](https://assets.emqx.com/images/dfbc4a122b94de8a06be953564619f77.png)

3. 在 MQTT 连接采样器后添加 MQTT Pub Sampler，用于发布消息。

   - QoS Level 为消息级别，支持0、1、2

   - Retained Mesages 为是否保留消息，支持 true、false

   - Topic name 为主题名称

   - Add timestamp in payload  在报文中加入时间戳

   - Message type : String 可填写自定义字符串报文

   - Message type : Hex string 可填写自定义十六进制报文

   - Message type : Randmom string with fixed length 为固定长度随机字符，后面Length为指定长度

      ![MQTT Pub Sampler](https://assets.emqx.com/images/cfa684bde4b5f27bc9e889f7e658f5b1.png)

4. 在 MQTT Pub Sampler 下添加“固定定时器”，用于控制发布消息频率。

   ![添加固定定时器](https://assets.emqx.com/images/5fc1e2e38c555519d5aeee421bc85c9b.png)
 

### 订阅脚本

1. 在测试计划下增加线程组。

   ![增加线程组](https://assets.emqx.com/images/75c241792a50d6fe279c9debeebca6fb.png)

2. 在线程组下添加仅一次控制器及“MQTT 连接采样器”（即"MQTT Connect"）

   ![添加 MQTT 连接采样器](https://assets.emqx.com/images/d8608efc01ca297fdc218ca4358a284c.png)

3. 在 MQTT Connect 后添加 MQTT Sub Sampler，模拟订阅消息。

   - Qos Level 消息级别，支持0、1、2

   - Topic name(s) 订阅主题名称，支持+/#通配符共享订阅

   - Payload includes timestamp 报文是否包含时间戳

   - Sample on : specified elapsed time(ms)  按毫秒时间统计订阅到消息

   - Sample on : number of received messages 按次数统计订阅到消息

   - Debug response 调试返回信息，即在察看结果树中显示详细订阅报文

      ![MQTT Sub Sampler](https://assets.emqx.com/images/28c0452a731920d4d082b90d0a33c3c1.png)

## 测试的执行

对编写好的脚本进行调试验证，确认 MQTT Broker 的连通性及脚本运行逻辑是否符合预期。

将线程组页面的线程组数分别修改为 50，设置循环次数为 1000，页面点击 Start 按钮执行测试。

![执行测试](https://assets.emqx.com/images/8ff44110b48db12c42ccf8242b4e7312.png)

查看测试结果，点击“察看结果树”可查看发布及订阅报文内容。

![察看结果树](https://assets.emqx.com/images/360fadfb1674d46fa8fa8558d2cf1948.png)

从汇总报告看出 Pub 和 Sub 吞吐量为 161.5/s，50 发布者与 50 订阅者消息数都是 50*1000，即发布订阅吞吐与消息数量都一致。

![测试汇总报告](https://assets.emqx.com/images/37e48fce9bcc1e3d2d686d3678bf198e.png)
 

登录 EMQX Dashboard 页面，显示如下：

![EMQX Dashboard](https://assets.emqx.com/images/2d1975568e5dec9b98164990564a55a8.png)
 

## 附件

读者可[下载测试脚本](https://assets.emqx.com/data/MQTT_Pub_Sub.jmx)运行并查看结果。

## 本系列中的其它文章

- [开源测试工具 JMeter 介绍 - 物联网大并发测试实战 01](https://www.emqx.com/zh/blog/introduction-to-the-open-source-testing-tool-jmeter)
- [JMeter 测试组件介绍 - 物联网大并发测试实战 02](https://www.emqx.com/zh/blog/introduction-to-jmeter-test-components)
- [如何在 JMeter 中使用 MQTT 插件 - 物联网大并发测试实战 03](https://www.emqx.com/zh/blog/how-to-use-the-mqtt-plugin-in-jmeter)
- [JMeter MQTT 在连接测试场景中的使用 - 物联网大并发测试实战 04](https://www.emqx.com/zh/blog/test-mqtt-connection-with-jmeter)
