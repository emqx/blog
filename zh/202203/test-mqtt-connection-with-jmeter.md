通过之前的文章，相信大家已经熟悉了 JMeter 及 MQTT 插件的使用等基础知识。从本文开始，我们利用这些测试工具进行测试实战。本文将介绍 MQTT 连接的测试。

### 连接场景分析

插件中 MQTT Connect 请求主要模拟设备与 MQTT 服务器（本文以 EMQX 为例）建立连接，并按指定间隔发送 [MQTT keep alive](https://www.emqx.com/zh/blog/mqtt-keep-alive) 报文，在物联网实际场景中经常需要海量设备连接并保持在线，大量设备同时上线及下线；本文脚本将模拟 400 个设备同时与 EMQX 建立连接，并保持连接 30 分钟后同时下线。

### 如何使用 MQTT 插件编写测试脚本

1. 在测试计划下创建线程组。

   ![JMeter 创建线程组](https://assets.emqx.com/images/fcc5e0c0ee577fed43d1d1bc1342c670.png)

2.  在线程组下添加“MQTT 连接采样器”（即"MQTT Connect"）

   ![JMeter 添加 MQTT 连接采样器](https://assets.emqx.com/images/c7a77e74d546b67c4966b6c5221f8086.png)

3. 在 MQTT 连接采样器下添加“同步定时器”，确保所有线程在同一时间开始建立连接。

   ![JMeter 添加同步定时器](https://assets.emqx.com/images/64f5464cd0dd7a770063443d70d1dae4.png)

4. 在线程组下添加“测试活动”，用于控制建立连接后连接保持的时间。

   ![JMeter 添加测试活动](https://assets.emqx.com/images/75450e1c5a31ed966b9b82987b82a2e5.png)

5. 在线程组下添加“MQTT 断开连接采样器” （即"MQTT DisConnect"），模拟设备同时断开连接。

   ![JMeter 添加 MQTT 断开连接采样器](https://assets.emqx.com/images/a1e93883a38797dfe27072b1c76f8358.png)

6. 在测试计划下创建“汇总报告”和“察看结果树”监听器，用于检查 JMeter 请求结果。

   ![JMeter 汇总报告](https://assets.emqx.com/images/8f2673be048ba9f57e1d9cb4583054ee.png)

   ![JMeter 察看结果树](https://assets.emqx.com/images/240ca231cd28ed208c4e00342b4fd51e.png)

### 测试的执行

对编写好的脚本进行调试验证，确认 MQTT Broker 的连通性及脚本运行逻辑符合预期后，将线程组页面的线程组数修改为 400，页面点击 Start 按钮执行测试。

![JMeter Start](https://assets.emqx.com/images/c3e75cb1b66194a937753b27f26df057.png)

查看连接结果，从汇总报告看出吞吐量为 394.9/s，即 400 客户端在 1 秒内同时连接。

![JMeter 汇总报告](https://assets.emqx.com/images/6a8828e982f535096d700ca28c2ba411.png)

![JMeter 查看采样器结果](https://assets.emqx.com/images/0a16086d1019ed7cedcda99b858a8b25.png)
 

登录 EMQX Dashboard 页面，显示如下：

![EMQX Dashboard](https://assets.emqx.com/images/9e914c2a4b028c2aba822303b58c920b.png)
 

### 附件：样例脚本

读者可[下载测试脚本](https://assets.emqx.com/data/MQTT_Connect.jmx)运行并查看结果。

## 本系列中的其它文章

- [开源测试工具 JMeter 介绍 - 物联网大并发测试实战 01](https://www.emqx.com/zh/blog/introduction-to-the-open-source-testing-tool-jmeter)
- [JMeter 测试组件介绍 - 物联网大并发测试实战 02](https://www.emqx.com/zh/blog/introduction-to-jmeter-test-components)
- [如何在 JMeter 中使用 MQTT 插件 - 物联网大并发测试实战 03](https://www.emqx.com/zh/blog/how-to-use-the-mqtt-plugin-in-jmeter)
- [如何在 JMeter 中使用 MQTT 插件 - 物联网大并发测试实战 05](https://www.emqx.com/zh/blog/the-use-of-jmeter-mqtt-in-subscription-and-publishing-test-scenarios)
