7月，[MQTTX](https://mqttx.app/zh) 团队专注于 1.8.1 版本的开发。v1.8.1 中 MQTTX 桌面端版本将支持自动更新，并对 [MQTTX Web](https://mqttx.app/zh/web) 页面进行了优化。目前已完成了 [MQTTX CLI](https://mqttx.app/zh/cli) 对于 MQTT 5.0 的连接支持及用户属性设置支持，并新增了一个 conn 命令来快速测试连接，后续还将添加 bench 命令，将支持部分场景下的 MQTT 协议性能测试。

## MQTTX 桌面端应用

### 自动更新功能

目前已经初步完成该功能的开发，正在进行最后的功能测试。在不同的操作系统下进行测试，不需要手动下载安装包也能完成对软件的更新，当用户收到升级提示时，只要点击更新即可在软件内自动将版本升级至最新，免去了手动下载安装包的繁琐操作。支持自动更新功能后，用户将更快体验到新功能，提升使用体验。该功能特性将在 v1.8.1 中正式发布。

### 默认 MQTT 5.0 连接

在之前的版本中，MQTTX 默认是 MQTT 3.1.1 连接。作为目前支持 MQTT 5.0 特性最为完整的 [MQTT 客户端工具](https://www.emqx.io/zh/mqtt-client)，我们在最新版本中将 MQTTX 默认连接时的 MQTT 版本修改为了 5.0，方便更多的用户快速使用和体验 MQTT 5.0 的新特性。

## MQTTX CLI

### MQTT 5.0 支持

MQTTX 目前已经完成了对于 MQTT 5.0 的连接支持，并在使用时默认使用 MQTT 5.0 连接。同时还新增了一个用户属性参数——User Properties，支持在连接、发布、订阅时设置用户属性。例如：

```
mqttx pub -t 'hello' -h 'broker.emqx.io' -p 1883 -m 'from MQTTX CLI' -up "name: mqttx" "company: EMQ" 
```

### 新增 conn 命令

在当前 1.8.0 版本中，只支持 pub 和 sub 两个命令，即支持快速的发布与订阅。而对于一些只需要测试 MQTT 服务连通性的简单场景来说， conn 命令则更加便捷。

```
mqttx conn -h 'broker.emqx.io' -p 1883 -u 'admin' -P 'public'
```

以上新增功能特性，都将在 MQTTX CLI 1.8.1 中正式发布。

## MQTTX Web

MQTTX Web 在线试用地址已修改为：[http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client)

只需要访问上述地址，即可快速使用这款在线的 MQTT 5.0 客户端工具，通过 MQTT over WebSocket 连接到 [MQTT Broker](https://www.emqx.io/zh) 并在浏览器中测试消息发布和接收，快速开发和调试您的 MQTT 服务与应用。

在 1.8.1 版本中，我们还将继续优化页面样式，完善测试功能等。

## 未来规划

MQTTX 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网平台的测试和开发提供便利。

接下来我们将重点关注以下方面：

- 使用体验升级
- MQTTX CLI 将支持 bench 命令
- 插件系统（例如支持 SparkPlug B，集成 MQTTX CLI）
- 脚本功能优化
- 推出 MQTTX Mobile 移动端应用
- 完善 MQTTX Web 功能
- MQTT Debug 功能



<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>
