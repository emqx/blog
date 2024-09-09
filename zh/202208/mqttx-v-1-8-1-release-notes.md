近日，MQTTX 发布了最新的 1.8.1 版本（下载地址：[https://github.com/emqx/MQTTX/releases/tag/v1.8.1](https://github.com/emqx/MQTTX/releases/tag/v1.8.1)），MQTTX 桌面端版本已支持自动更新，并对 MQTTX Web 页面进行了优化。目前已完成了 MQTTX CLI 对于 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 的连接支持及用户属性设置支持，并新增了一个 conn 命令来快速测试连接，后续还将添加 bench 命令，将支持部分场景下的 [MQTT 协议](https://www.emqx.com/zh/mqtt-guide)性能测试。

![MQTTX](https://assets.emqx.com/images/2df897d02b73e237048faad97688e51f.png)

## MQTTX 桌面客户端

### 自动更新功能

在之前每次的版本发布中，用户可以通过升级提示框的下载按钮跳转到最新版本下载页面，手动下载安装包完成对软件的更新。从 v1.8.1 开始，用户不再需要手动下载安装，只需在收到升级提示点击按钮，软件后台即可自动将版本升级至最新。自动更新功能可以让用户更快体验到最新功能，提升使用体验。

![MQTTX 自动更新](https://assets.emqx.com/images/c04d3beaf1dab9bfed47fef19d2c9c95.jpeg)

更新完成后，可以在弹出框内查看最新的发布日志，快速了解到当前版本的更新内容，提升使用体验。

![MQTTX 更新日志](https://assets.emqx.com/images/66063022ae15a278aa87e32f6f55e201.png)

### 默认 MQTT 5.0 连接

在之前的版本中，MQTTX 默认是 MQTT 3.1.1 连接。作为目前支持 MQTT 5.0 特性最为完整的 MQTT 客户端工具，我们在最新版本中将 MQTTX 默认连接时的 MQTT 版本修改为了 5.0，方便更多的用户快速使用和体验 MQTT 5.0 的新特性。

### 对 Topic 进行发布前的验证

当用户向带有通配符 +，# 这样的通配符的 Topic 发送消息时，会导致连接断开，很多新用户在不了解 MQTT 协议的时候，会经常出现这样的问题，导致断开连接而产生使用上的疑惑。在 1.8.1 版本中，为避免了这样的情况发生，我们在发布前对 Topic 进行了验证，只有在发布时使用这些不包含通配符的 Topic，才可以发布成功。

![MQTT Topic 验证](https://assets.emqx.com/images/403b1a09c39f1e8f38b427981baa443c.png)

## MQTTX CLI

### MQTT 5.0 支持

MQTTX CLI 1.8.1 目前已经完成了对于 MQTT 5.0 的连接支持，并在使用时默认使用 MQTT 5.0 连接。同时还新增了一个用户属性参数 `--user-properties`，支持在连接、发布、订阅时设置用户属性。例如：

```
mqttx pub -t 'hello' -h 'broker.emqx.io' -p 1883 -m 'from MQTTX CLI' -up "name: mqttx" "company: EMQ" 
```

### 新增 conn 命令

在当前 1.8.0 版本中，只支持 pub 和 sub 两个命令，即支持快速的发布与订阅。而对于一些只需要测试 MQTT 服务连通性的简单场景来说， conn 命令则更加便捷。

```
mqttx conn -h 'broker.emqx.io' -p 1883 -u 'admin' -P 'public'
```

## MQTTX Web

MQTTX Web 目前在线地址已修改为：[https://mqttx.app/web-client/](https://mqttx.app/web-client/) 

只需要访问上述地址，即可快速使用这款在线的 MQTT 5.0 客户端工具，通过 MQTT over WebSocket 连接到 MQTT Broker 并在浏览器中测试消息发布和接收，快速开发和调试您的 MQTT 服务与应用。

在 1.8.1 版本中，优化了页面样式，完善测试功能等。后续还将继续完善 MQTT 5.0 的属性配置功能。

![MQTTX Web](https://assets.emqx.com/images/108265b02b225ecb95f7001981d3978d.png)

## 修复及优化

除添加上述新特性外，本次更新还修复了很多已知问题，稳定性得到了进一步提升。

- 修复 MQTTX 在 macOS 系统中，意外退出的弹框提醒
- 修复 MQTTX 在消息列表中展示用户属性时的样式问题
- 修复 MQTTX CLI 下无效的 `--clean` 参数，使用 `--no-clean` 参数替代

## 未来规划

MQTTX 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网平台的测试和开发提供便利。

接下来我们将重点关注以下方面：

- 使用体验升级
- MQTTX CLI 将支持 bench 命令
- 插件系统（例如支持 SparkPlug B、集成 MQTTX CLI）
- 脚本功能优化
- 推出 MQTTX Mobile 移动端应用
- 完善 MQTTX Web 功能
- MQTT Debug 功能

## 附：连接命令的使用帮助

### 连接

```
mqttx conn --help
```

| 参数                                       | 描述                                           |
| :----------------------------------------- | :--------------------------------------------- |
| -V, --mqtt-version <5/3.1.1/3.1>           | MQTT 版本，默认为 5                            |
| -h, --hostname                             | MQTT Broker 的 Host 地址，默认为 localhost     |
| -p, --port                                 | MQTT Broker 的端口号                           |
| -i, --client-id                            | 客户端 ID                                      |
| --no-clean                                 | 取消 clean session 标志位，默认为 true         |
| -k, --keepalive                            | MQTT 的 Keep Alive，默认为 30                  |
| -u, --username                             | 连接到 MQTT Broker 的用户名                    |
| -P, --password                             | 连接到 MQTT Broker 的密码                      |
| -l, --protocol                             | 连接时的协议，mqtt、mqtts、ws or wss           |
| --key                                      | key 文件的路径                                 |
| --cert                                     | cert 文件的路径                                |
| --ca                                       | ca 证书的文件路径                              |
| --insecure                                 | 取消服务器的证书校验                           |
| -up, --user-properties <USERPROPERTIES...> | MQTT 5.0 用户属性，例如：-up "name: mqttx cli" |
| --will-topic                               | 遗嘱消息的 topic                               |
| --will-message                             | 遗嘱消息的 payload                             |
| --will-qos <0/1/2>                         | 遗嘱消息的 QoS                                 |
| --will-retain                              | 遗嘱消息的 retain 标志位                       |
| --help                                     | 展示 conn 命令的帮助信息                       |


<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>
