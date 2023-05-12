## 概述

[MQTTX](https://mqttx.app/zh) 是由全球领先的 **开源物联网中间件** 提供商 [EMQ](https://www.emqx.com/zh) 开源的一款跨平台 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 桌面测试客户端，它支持 macOS，Linux，Windows。MQTTX 的用户界面借助聊天软件的形式简化了页面的操作逻辑，用户可以快速创建多个同时在线的 **MQTT 客户端，** 方便测试 MQTT/TCP、MQTT/TLS、MQTT/WebSocket  的连接/发布/订阅功能及其他 **MQTT 协议** 特性。

MQTTX 网站：[https://mqttx.app/zh](https://mqttx.app/zh)

MQTTX v1.5.2 版本下载：[https://github.com/emqx/MQTTX/releases/tag/v1.5.2](https://github.com/emqx/MQTTX/releases/tag/v1.5.2)

Mac 用户可在 App Store 中进行下载：[https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12](https://apps.apple.com/cn/app/mqttx/id1514074565?mt=12)

Linux 用户可在 Snapcraft 中进行下载：[https://snapcraft.io/mqttx](https://snapcraft.io/mqttx)

![mqttxpreview.png](https://assets.emqx.com/images/fdeeaa3093e114157fdbf46fd18bcd32.png)

## 脚本功能

**MQTTX 在 v1.4.2 版本后，加入了脚本功能，** 支持让用户使用脚本对 `Payload` 进行自定义转换，可用来模拟自定义测试场景，目前支持的脚本语言为 JavaScript。下文将通过两个简单的实例来介绍脚本功能的使用， **需注意：在 v1.4.2 版本中脚本功能属于开放性测试功能，使用流程、安全性和功能性还需后续继续优化提升和完善。** 也欢迎您到 MQTTX 的 [GitHub issue](https://github.com/emqx/MQTTX/issues) 区进行详细讨论，我们将会认真审阅和回复。

在编辑脚本功能中，全局只包含了一个 `execute` API，用户需要编写一个自定义函数，该函数接收一个 `value` 参数，即为 `Payload`, 函数中便可对 `value` 进行自定义修改转化，最后将该函数作为参数传入到 `execute` 中即可执行自定义编写的函数。

### 实例一

配合定时发送功能模拟温湿度数据上报。

例如，当用户使用 EMQX 时，需要使用规则引擎功能将数据保存到数据库。这时可以在配置完成后，使用 MQTT  X 连接到 EMQX，并使用脚本功能对其进行测试。这里假设用户需要保存上报的温湿度数据，且数据格式为 JSON 类型，我们可以使用下面的脚本对数据进行模拟。

```javascript
/**
 * Simulated temperature and humidity reporting
 * @return Return a simulated temperature and humidity JSON data - { "temperature": 23, "humidity": 40 }
 * @param value, MQTT Payload - {}
 */

function random(min, max) {
  return Math.round(Math.random() * (max - min)) + min
}

function handlePayload(value) {
  let _value = value
  if (typeof value === 'string') {
    _value = JSON.parse(value)
  }
  _value.temperature = random(10, 30)
  _value.humidity = random(20, 40)
  return JSON.stringify(_value, null, 2)
}

execute(handlePayload)
```

此时可将这段代码复制到脚本页面的代码编辑框内，点击右上角的 `保存` 按钮，设置脚本名称为 TempAndHum 并保存。我们在 Input 输入框内输入一个 `{}` 作为初始数据。点击 `测试` 按钮，在 Output 框内查看执行结果，如果结果符合预期，接下来将可以正常使用该脚本。

![mqttxhumtemp.png](https://assets.emqx.com/images/e8c56a968c89ae76bb6fb684ca73027b.png)

我们使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 新建一个连接，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

连接成功后，点击右上角的下拉功能菜单，选择 `使用脚本`，在弹出窗中，选择刚才保存好的 TempAndHum 脚本，然后选择应用类型为发送时，点击确认按钮后开启脚本功能。

![mqttxuse1.png](https://assets.emqx.com/images/0cdc5685eec2832049534beaf258fa57.png)

开启脚本后，我们再继续设置定时发送功能，同样点击右上角的下拉功能菜单，选择 `定时消息`，这里我们设置发送频率为 1 秒，点击确认后定时消息功能开启。

![mqttxtimed.png](https://assets.emqx.com/images/8cf5eaf54e3ab5596c03500012463cd7.png)

准备好后，便可以输入初始的 `Payload` 和需要发送到的`Topic`，点击发送成功一条消息后，便可以看到 MQTTX 将每秒自动发送了一次模拟数据。

![mqttxhumtempsuccess.png](https://assets.emqx.com/images/695bfda6171514106492d3543d884686.png)

这样避免了用户去手动输入和修改数据的麻烦，且使用脚本时模拟数据可控，模拟数据区间可在脚本的 `random` 函数中设定，如果有对保存的数据进行可视化图表测试需求或需要添加一定的数据量的数据来测试时，都较为方便和友好。

### 实例二

将接收到的 `Payload` 中的时间戳转化为正常时间。

在一些测试场景中，用户测试接收到的 `Payload` 内可能会包含时间戳信息，如果需要观察和测试对时间较为敏感的数据，可能需要复制出数据，再将时间戳转化时间，较为麻烦。此时可以使用脚本对接收到的数据进行自动转化，方便用户观察数据信息。我们可以使用下面的脚本对数据进行转化。依然假设接收到的数据为 JSON 类型，并且包含了 time 字段。

```javascript
/**
 * Convert timestamp to normal time.
 * @return Return the UTC time - { "time": "2020-12-17 14:18:07" }
 * @param value, MQTT Payload - { "time": 1608185887 }
 */

function handleTimestamp(value) {
  let _value = value
  if (typeof value === 'string') {
    _value = JSON.parse(value)
  }
  // East Eight District needs an additional 8 hours
  const date = new Date(_value.time * 1000 + 8 * 3600 * 1000)
  _value.time = date.toJSON().substr(0, 19).replace('T', ' ')
  return JSON.stringify(_value, null, 2)
}

execute(handleTimestamp)
```

此时可将这段代码复制到脚本页面的代码编辑框内，点击右上角的 `保存` 按钮，设置脚本名称为 Time 并保存。我们在 Input 输入框内输入一个 `{ "time": 1608365158 }` 作为初始数据。点击 `测试` 按钮，在 Output 框内查看执行结果，如果结果符合预期，接下来将可以正常使用该脚本。

![mqttxtime.png](https://assets.emqx.com/images/145b3c4b24a42bd52f44923fb0e272f9.png)

此时我们依然新建一个连接，使用上述中描述的方法来开启脚本。注意选择应用类型时，需要选择为接收时。

![mqttxuse2.png](https://assets.emqx.com/images/0d3d705ee8a79eecb483cb30ecd15c71.png)

脚本功能开启后，我们添加一个 `testtopic/time` 的 `Topic`，然后我们向该 `Topic` 发送一条包含时间戳信息的 `Payload`。然后查看接收到的 `Payload` 信息，可以看到已经自动帮时间戳转化为了正常时间。

![mqttxtimesuccess.png](https://assets.emqx.com/images/eee40a6a899c8c9912ee55ae9efbd56b.png)

## 总结

至此，我们完成了 MQTTX 的脚本实例使用的教程。该功能具有一定的扩展性和灵活性，需用户配合实际需求来进行使用。脚本使用实例可在 GitHub 仓库的 [/docs/script-example](https://github.com/emqx/MQTTX/tree/master/docs/script-example) 文件夹中查看，目前提供了两个内置脚本，时间戳转化和温湿度数据模拟。如果在您的使用中有更好的，更实用的脚本也可以提交您的代码到这里，方便让更多的人使用到。

该项目完全开源，您可以到 [GitHub](https://github.com/emqx/MQTTX/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc) 来提交使用过程中遇到的问题，或是 Fork MQTTX 项目向我们提交修改后的 PR，我们将会及时查阅和处理。也特此感谢社区中所有用户的贡献和反馈。
