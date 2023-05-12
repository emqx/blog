十一月初，MQTTX 团队发布了 1.9.0 版本：MQTTX CLI 命令行客户端实现支持 MQTT 的性能测试，桌面端应用新增了关于学习 MQTT 的帮助页面等，此外还进行了一些使用优化和问题修复。

目前，团队正专注于 1.9.1 版本的开发。新版本中 MQTTX CLI 命令行客户端将支持自动重连，支持读取和存储本地配置文件，还可对于接收到的消息进行格式转换；桌面端应用支持设置滚动频率，并修复了一些使用上的问题。

最新版本下载：[https://www.emqx.com/zh/try?product=MQTTX](https://www.emqx.com/zh/try?product=MQTTX) 

## 桌面客户端

### 支持设置滚动频率

1.9.1 版本中我们新增了一个配置项：滚动频率。该配置项用于设置消息列表的滚动频率，需要在开启自动滚动时才可以配置。

在之前的版本中，当我们开启自动滚动时，消息列表会在接收到新的消息时自动滚动到底部，但是这样会导致消息列表的滚动速度过快，当接收到消息的速率过快时，用户无法马上查看到消息的具体内容。因此，我们新增了滚动频率的配置项，可以在设置页面中进行配置，滚动频率的单位为秒，用户可以根据自己的需求进行配置。设置完成后，当接收到新的消息时，消息列表会在滚动频率时间内滚动到底部，这样可以保证消息列表的滚动速度适中，用户可以在滚动前查看到消息的具体内容。

![设置滚动频率](https://assets.emqx.com/images/91d42fee8661daf7dcac64c7b445f6d0.png)

### 帮助页面调整

在之前的版本中，我们新增了帮助页面，用于帮助用户学习 MQTT。在这个版本中，我们将其设置成了一个独立的菜单，改名为「关于 MQTT 的一切」，方便用户快速点击到该菜单中，查看 MQTT 的相关知识，包括 MQTT 的基本概念、参数配置、主题消息、QoS 以及客户端编程等内容。

![帮助页面调整](https://assets.emqx.com/images/acfa3a94927df2d88e63215c31b4b1ca.png)

### 其它

- 用户属性配置支持添加多个重复的 key，并为其设置不同的 value，完全兼容 MQTT 协议
- UI 样式与交互上的优化
- 修复一些已知 BUG

## 命令行客户端

### 支持自动重连

在之前的版本中，当 MQTT 服务器出现异常时，MQTTX CLI 命令行客户端会自动断开连接并退出，这样会导致用户无法在 MQTT 服务器恢复后继续使用 MQTTX CLI，需要重新手动连接。因此，我们在该版本中新增了自动重连的功能，当 MQTT 服务器出现异常后，MQTTX CLI 命令行客户端断开连接后会自动重连。

![支持自动重连](https://assets.emqx.com/images/543f9f68d014fe3d30816dac773681f6.png)

每次重连有一个最大重连次数，当达到最大重连次数后，MQTTX CLI 命令行客户端会退出，以防止客户端在无法连接的情况下一直重连。自动重连的最大重连次数默认为 10 次，可以使用 `--maximun-reconnect-times` 参数进行配置。

```
# 以连接命令时的自动重连次数配置为例，修改为 5 次

mqttx conn -h 'broker.emqx.io' -p 1883 --maximun-reconnect-times 5
```

除重连次数外，我们还新增了重连间隔的配置项，当 MQTT 服务器出现异常后，MQTTX CLI 命令行客户端会在重连间隔时间内进行重连，重连间隔的单位为毫秒，默认为 1000 毫秒，可以使用 `--reconnect-period` 参数进行配置，

> 注意：当重连间隔设置为 0 时，表示关闭自动重连功能。

```
# 以连接命令时的重连间隔配置为例，修改为 5000 毫秒

mqttx conn -h 'broker.emqx.io' -p 1883 --reconnect-period 5000
```

同时支持在 `bench` 命令中使用自动重连功能。对于自定数量中的连接，会对每一个异常断开连接的进行自动重连。

![bench 支持自动重连](https://assets.emqx.com/images/7e78759b8dc40dbcaaab9bd2729731eb.png)

### 支持读取和存储本地配置文件

MQTTX CLI 命令行客户端在之前的版本中，每次连接都需要手动输入连接参数，这样会导致用户每次连接都需要输入一遍参数，比较繁琐。因此，我们在该版本中新增了读取和存储本地配置文件的功能。用户可以将连接参数保存到本地配置文件中，下次连接时可以直接读取本地配置文件中的参数，无需再次输入，且支持对所有 CLI 中的命令进行保存。

在运行命令时使用 `--save` 参数和保存文件的路径即可保存配置文件， 默认保存的文件名为 `mqttx-cli-config.json`，保存的文件路径为当前运行命令的目录下。

在运行命令时，使用 `--config` 参数和配置文件的路径即可读取配置文件。

> 注意：MQTTX CLI 本地存储的文件同时支持 JSON 和 YAML 格式，但是在使用 `--save` 参数时，需要指定文件的格式，如 `--save mqttx-cli-config.json` 或 `--save mqttx-cli-config.yaml`。

![支持读取和存储本地配置文件](https://assets.emqx.com/images/6f961defae3118d55cc6c46012447853.png)

### 支持消息的格式转换

在之前的版本中，MQTTX CLI 命令行客户端只支持发送字符串类型的消息，当用户发送 Hex 类型的消息时，接收到的消息转换为字符串显示时就会出现问题。因此 MQTTX CLI 命令行客户端在该版本中新增了消息格式转换的功能，用户可以在接收消息时指定消息的格式。

消息格式支持以下几种：

- String
- Hex
- Base64
- JSON

除 String 格式外，只需要在订阅命令时添加一个 `--format` 参数 即可指定消息的格式，如 `--format hex`。

![支持消息的格式转换](https://assets.emqx.com/images/4c8ad470255520c85930b12bfbd6dd0c.png)

## Web 客户端

MQTTX Web 客户端同步了 MQTTX 桌面端应用的相关功能修改与页面调整。

在线体验地址为：[http://www.emqx.io/online-mqtt-client/](http://www.emqx.io/online-mqtt-client/) 

## 未来规划

MQTTX 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网应用与服务的测试和开发提供便利。接下来我们将重点关注以下方面，敬请期待：

- 接收消息和存储时的性能优化，大量消息不卡顿
- MQTT Debug 功能
- 支持 Sparkplug B 格式
- 接收到的消息可以进行自动图表绘制
- 插件功能
- 脚本测试自动化（Flow）



<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>
