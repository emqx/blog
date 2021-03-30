> **我们荣幸地向大家宣布，EMQ X Broker 3.1 - Beta.2版本已经于2019年3月17日发布。**


杭州映云科技有限公司聚焦于消息和流处理技术领域，EMQ X Broker是映云科技的开源分布式IoT消息处理中间件。自发布以来，EMQ X Broker已经在世界各地被⼴泛应用。EMQ X Broker也以其完备的MQTT协议支持、高并发低延时、高可扩展性、易于部署和快速的版本迭代等特点，在物联网行业中占有重要的地位。



#### 该版本新增和增强了以下特性:

**EMQ X Broker** 核心功能

- 改进了Hooks功能。

  Hooks的返回机制做了改进。并将Password作为 credentials 数据结构的一部分。

- 支持在TLS/DTLS中使用PSK

- 更多的请求响应信息

  支持在CONNACK包中使用 Response-Information 消息属性。这个⼀个MQTT 5.0协议中的可选特性。

**EMQ X** 管理功能

- 增加了默认application secret
- 为所有插件增加了插件相关的HTTP API

**JWT Auth**插件

- 在之前版本中，⽤户只能将密码放在CONNECT包中传递。现在可以将⽤户名和密码放在JWT中传递，增加了易用性。

**emqx_auth_username**插件

- 为管理用户名新增了了CRUD操作的HTTP API接口。



#### 该版本修正了以下Bug:


**EMQ X Broker**核心功能

- Broker在集群中转发消息时崩溃。

- 在关闭时在卸载插件之前卸载emqx_alarm_handler。 

  该改动能避免一些在插件卸载时发生的崩溃。

- 修正了一些EMQ X桥接相关的Bug

- 减少了Inflight窗口满的错误

**EMQ X** 管理理功能

- 修正了在插件未启动时重载插件的错误 
- 修正了io/max_fds错误

**emqx_web_hook**插件

- 修正了消息格式相关的bug

其他 **Bug**

- 过滤掉了未加载的插件的API请求

- 修正了 gen_tcp 中raw socket标志位



请参阅版本发布日志以获取所有版本变动信息:

https://www.emqx.io/changelogs/broker/v3.1-beta.2