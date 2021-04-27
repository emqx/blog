
[MQTT X](https://mqttx.app/cn/) 是由 [EMQ](https://emqx.io/ ) 开源的一款跨平台 **MQTT 5.0** 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket 的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 官网：[https://mqttx.app](https://mqttx.app/cn/)

MQTT X v1.3.1 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.3.1](https://github.com/emqx/MQTTX/releases/tag/v1.3.1)



## 新功能预览

- 支持 MQTT 5.0 更多属性

  该版本中新增了对 MQTT 5.0 属性 `Topic Alias Maximu ` 的配置，即为主题别名最大值，表示由服务器发送的客户端将接受为主题别名的最大值。在新建连接中选择 MQTT 协议版本为 5.0 后即可配置该项。

![mqttxtopicaliasmax.png](https://static.emqx.net/images/414597f0a3dffe1a8ec12009d4ff86e4.png)

- 通过单击已订阅的 Topic 项实现消息过滤

  对于之前的版本，所有订阅的消息展示都在同一视图中，如果有多个消息主题的订阅，将非常不方便查看。因此在当前最新版中，实现了可点击左侧订阅列表中已经订阅的 Topic 项，来实现消息过滤，点击后，消息视图内将只显示订阅了当前主题的消息内容，再次点击即可取消过滤。

![mqttxtopicmessages.png](https://static.emqx.net/images/1095f94567b1b912d1d23b57d45e8591.png)

- 支持点击 Topic 名称后快速复制 Topic 信息

  当成功添加一个 Topic 后，在已订阅列表中点击 Topic 名称，即可快速复制当前的 Topic 信息。当需要向该 Topic 发送消息时，只需快速粘贴到消息栏的 Topic 输入框内进行修改，便可快速完成该操作。

![mqttxtopiccopy.png](https://static.emqx.net/images/2b2da8f80dd33f911fb569d1d21d6f5b.png)

- 添加启用严格的证书验证选项

  在创建 TLS/SSL 的安全连接时，选择证书卡片内加入了开启`严格证书验证`的选项，当开启该项后，会启用更完整的证书验证连接，一般推荐在需要测试正式环境时启用。

![mqttxtls.png](https://static.emqx.net/images/9981849ab9cf6a01238ec530553ad8ba.png)



## 优化和修复

- 允许消息框内直接发送空消息
- 修复了客户端接收到重复消息的问题
- 修复了证书未通过验证的问题



该项目完全开源，您可以到 [MQTT X GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。