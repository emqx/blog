本月，MQTTX 团队专注于 1.8.3 版本的开发。主要对功能使用进行了优化，并修复了使用过程中所出现的各类问题。例如，优化 MQTT 5.0 Clean Start 的使用方式，为会话过期间隔添加默认值；优化 MQTTX CLI 的默认输出显示，提供更加细致美观的内容展示。

## MQTTX 桌面端应用

### 优化 Clean Start 使用

[MQTTX](https://mqttx.app/zh) 作为一款 MQTT 5.0 客户端工具，目前默认使用 MQTT 5.0 连接测试。在 MQTT 5.0 中，`Clean Session` 修改为了 `Clean Start`，并需要搭配会话过期间隔一起来使用。而在当前 1.8.2 版本中，当使用默认连接时，如果用户未设置会话过期间隔，断开连接时 MQTT Broker 将无法持久化其会话。对于很多不太了解 MQTT 5.0 新特性使用的用户来说，这带来了一些困扰。

目前开发的 1.8.3 版本优化了该问题，将 `Clean Session` 的显示修改为了 `Clean Start`，并为会话周期间隔设置了 `永不过期` 的默认值，也继续支持用户手动修改该值，来满足当前测试需求。同时提示用户：当关闭 `Clean Start` 时，如果该值为空，还需设置会话过期间隔来保证其连接会话的正确使用。

### 其它使用问题优化

- 修复当断开连接时，retain 消息未能保存的问题
- 修复当 Hex 格式出现空格时，内容会被截断的问题
- 修复使用中的脚本无法删除的问题
- 修复当设置了主题别名后，无法接收到消息的问题
- 修复一些内部错误

## MQTTX Web

在线 MQTT 5.0 客户端工具 MQTTX Web 进行了如下更新：

- 支持存储发送过的历史消息
- 支持单条消息复制和删除
- 支持使用 Docker 部署到任意 URL 路径下
- 支持多主题订阅
- 支持开启和关闭自动滚动
- 支持设置订阅标识符和订阅选项
- 支持设置重连周期

在线使用地址：[http://www.emqx.io/online-mqtt-client](http://www.emqx.io/online-mqtt-client) 

## MQTTX CLI

### 支持多主题订阅

在 MQTTX 的桌面客户端中，我们提供了多主题订阅功能。在 1.8.3 版本中，命令行工具 MQTTX CLI 同样支持了多主题订阅，只要输入多个 `--topic` 参数，即可在使用一条命令行的情况下同时订阅多个主题，接收不同主题下的消息内容来测试和查看数据。

![MQTTX CLI](https://assets.emqx.com/images/dac76f6944bc7aa31f4d514548e3642a.png)

### 优化 CLI 的内容输出

在命令行终端内，我们优化了 MQTTX CLI 的显示内容。在 1.8.3 版本中，我们为每一个步骤输出的内容都提供了时间显示，并细化其步骤显示。例如，当使用 `sub` 和 `pub` 命令时，也能看到连接中和已连接的过程。使用类似于日志输出的方式，可以提高用户的阅读体验，帮助用户更加清晰方便地查看当前连接测试的过程与内容。

![优化 MQTTX CLI 的内容输出](https://assets.emqx.com/images/6e95a502f0a226c3d380e7fc51aa77bb.png)

### 其它优化

- 添加主题验证，用户不能向包含有 # 和 + 等，带有通配符的主题发送消息
- 当使用 `--version` 参数来输出版本时，将输出带有 change logs 的地址，方便用户快速查看该版本下的最新功能
- 添加更多的 MQTT 5.0 properties 配置，例如支持设置会话过期间隔
- 修复用户属性设置错误的问题

## 官网文档优化

除上述产品内容更新外，我们还在持续调整优化 MQTTX 文档。本月新增了 MQTTX CLI 和 MQTTX Web 的产品介绍和使用文档，帮助用户更好的上手和使用不同交互形态的 MQTTX。

## 未来规划

MQTTX 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网平台的测试和开发提供便利。

接下来我们将重点关注以下方面：

- 使用体验升级
- MQTTX CLI 将支持 bench 命令
- 接收到的数据支持自定义图表化
- 插件系统（例如支持 SparkPlug B、集成 MQTTX CLI）
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
