[MQTT X](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTT X 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端**，方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTT X 网站：https://mqttx.app/zh

MQTT X v1.4.2 版本下载：https://github.com/emqx/MQTTX/releases/tag/v1.4.2

Mac 用户可在 App Store 中进行下载：https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12

Linux 用户可在 Snapcraft 中进行下载：https://snapcraft.io/mqttx

![mqttxpreview.png](https://assets.emqx.com/images/eae55fcaa5b4abd9b562bc2aa5fc9dd9.png)

## 新功能概览

### 脚本功能（Beta）

在该版本中，MQTT X 新增了脚本编辑功能，用户可实现编写自定义脚本（JavaScript）对发送和接收到的 `Payload` 进行自定义转化，配合定时发送功能，可实现例如模拟数据上报的自动化测试功能等。

> 注意：该功能目前属于测试 Beta 阶段。

点击左侧菜单栏中的 `脚本` 按钮，可进入到脚本编辑页面，在该页面中，用户可在最上方的代码编辑器中，编写 JavaScript 代码，全局只包含一个 `execute` API，用户需要编写一个脚本函数，该函数接收一个 `value` 参数，即为 `Payload`, 函数中便可对 `value` 进行自定义操作（需注意接收到的 `Payload` 的类型间的转化），最后将该函数作为参数传入到 `execute` API 中即可执行自定义编写的函数。

下方还包含了一个 `输入` 和 `输出` 框，可输入预想输入值，点击右边的 `测试` 按钮，便可在 `输出` 框中查看执行结果，输入的值的格式包含了 `JSON` 和 `Plaintext`，方便用户提前调试自定义编写的脚本功能。完成测试后，可点击最右上角的 `保存` 按钮，输入该脚本的名称后就可对该脚本进行保存。保存完成后就可以到连接页面进行使用了。保存完成的脚本还可进行编辑和删除。

编写完脚本后，就可切换到连接页面，点击右上角的下拉功能菜单，选择 `使用脚本`，在弹出窗中，选择你需要使用的预先保存好的脚本，然后选择应用类型，包含了，发送时，接收时和全部。选择完成后，根据数据类型选择发送或接收的数据格式，正常使用消息的收发，此时如果看到预期效果，便完成了一个完整的脚本使用的功能。如果用户需要取消脚本，可点击顶部状态栏中的红色的 `停止脚本` 按钮，便可停止使用脚本。

注意：该功能具有一定的扩展性和灵活性，需用户配合实际需求来进行使用。

![mqttxscript.png](https://assets.emqx.com/images/cd4daadad6483bd7c7a20805ac746933.png)

### Client ID 自动加入时间戳

为防止当输入了相同的 Client ID 的客户端进行连接后，出现互踢的情况。该版本中为此进行了优化，新增了一个自动为 Client ID 加入时间戳的功能，保证每次连接时的 Client ID 都可以不同。在创建连接时，用户只需要点击 Client ID 输入框后的时间按钮，当按钮图标颜色状态发生改变时，即开启了该功能，再次点击后即可取消该功能。

![mqttxclientidtime.png](https://assets.emqx.com/images/b16191291027f1f12229652979afc443.png)

## 修复及其优化

- 优化消息列表过长时，系统卡顿的问题
- 优化系统主题（$SYS）订阅失败时的错误提示
- 优化当客户端连接时，禁止编辑客户端信息
- 修复错误触发定时任务的问题
- 修复未读消息为 NaN 的问题
- 修复不能显示 `Payload` 编辑器的问题

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTT X 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。
