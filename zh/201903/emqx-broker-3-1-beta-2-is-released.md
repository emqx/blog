


我们荣幸地向⼤大家宣布，EMQ X Broker 3.1 - Beta.2版本已经于2019年年3⽉月17⽇日发布。 

杭州映云科技有限公司聚焦于消息和流处理理技术领域，EMQ X Broker是映云科技的开源分布式IoT消息 处理理中间件。⾃自发布以来，EMQ X Broker已经在世界各地被⼴广泛应⽤用。EMQ X Broker也以其完备的 MQTT协议⽀支持、⾼高并发低延时、⾼高可扩展性、易易于部署和快速的版本迭代等特点，在物联⽹网⾏行行业中占 有重要的地位。 

### 该版本新增和增强了了⼀一下特性: 

EMQ X Broker 核⼼心功能 

- 改进了了Hooks功能。 
  Hooks的返回机制做了了改进。并将Password作为 credentials 数据结构的⼀一部分。 
- ⽀支持在TLS/DTLS中使⽤用PSK 
- 更更多的请求响应信息 
  ⽀支持在CONNACK包中使⽤用 Response-Information 消息属性。这个⼀一个MQTT 5.0协议中的可选 特性。 

**EMQ X 管理理功能**

- 增加了了默认application secret
- 为所有插件增加了了插件相关的HTTP AP

**JWT Auth插件** 

- 在之前版本中，⽤用户只能将密码放在CONNECT包中传递。现在可以将⽤用户名和密码放在JWT中传 递，增加了了易易⽤用性。 

**emqx_auth_username插件** 

- 为管理理⽤用户名新增了了CRUD操作的HTTP API接⼝口。 

### 该版本修正了了以下Bug: 

**EMQ X Broker核⼼心功能** 

- Broker在集群中转发消息时崩溃 
- 在关闭时在卸载插件之前卸载emqx_alarm_handler。 该改动能避免⼀一些在插件卸载时发⽣生的崩溃。 
- 修正了了⼀一些EMQ X桥接相关的Bug 
- 减少了了Inflight窗⼝口满的错误 

**EMQ X 管理理功能** 

- 修正了了在插件未启动时重载插件的错误 
- 修正了了io/max_fds错误 

emqx_web_hook插件 

- 修正了了消息格式相关的bug 
  **其他Bug** 
- 过滤掉了了未加载的插件的API请求 
- 修正了了 gen_tcp 中raw socket标志位 

```
请参阅版本发布⽇日志以获取所有版本变动信息:
```



https://www.emqx.cn/changelogs/broker/v3.1-beta.2

