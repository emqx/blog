本月，[MQTTX](https://mqttx.app/zh) 团队发布了 1.8.2 版本，目前正专注于 1.8.3 版本的开发。在 1.8.2 版本中，我们主要优化了使用体验并修复了 MQTTX 桌面端 1.8.1 版本中的一些使用问题，新增了使用 Docker 来安装和部署 MQTTX CLI 与 MQTTX Web，同时 MQTTX Web 支持了更多的 MQTT 5.0 属性配置。

## MQTTX 桌面端应用

### 支持在设置页面中开启或关闭多主题订阅

在之前的版本中，MQTTX 默认支持开启多主题订阅。使用方法是：在输入主题时，使用逗号来分割多个主题，但是当订阅的主题中包含了逗号时，就无法单个订阅此主题，这给存在这类特殊需求的用户带来了困扰。

在最新的 1.8.2 版本中，我们优化了这个问题，在设置页面新增了一个启用多主题订阅的开关，默认开启，当关闭后就可以订阅单个包含有逗号字符的主题。

![MQTT 多主题订阅](https://assets.emqx.com/images/cd29f9b0b3f74c805e844b1a8811d341.png)

### 其它使用问题优化

- 移除了在发布消息时，对包含有 `$` 符号的主题的验证

- 修复了无法在编辑连接内，修改用户属性的问题
- 修复了在编辑页面内，删除连接后页面跳转的问题
- 优化了订阅主题失败时的错误信息

## MQTTX Web

在线使用地址：[https://mqttx.app/web-client/](https://mqttx.app/web-client/) 

### 支持更多 MQTT 5.0 属性

支持在 MQTTX Web 中配置连接、发布时的用户属性，支持订阅选项等。

![MQTTX Web 支持更多 MQTT 5.0 属性](https://assets.emqx.com/images/d4fada751fd230ce202255c8caeea1a6.png)

### 支持使用 Docker 部署

除提供在线的公共访问地址外，MQTTX Web 还支持使用 Docker 来进行私有化部署。对于一些只能在内网环境，或想通过浏览器来访问和私有化使用 MQTTX Web 的用户来说，我们为其提供了更加方便和自由的使用方式，这使得用户无论在什么环境下都可以轻松访问 MQTTX Web 来更快地测试您的 MQTT 服务与应用。

使用 Docker 镜像部署 MQTTX Web：

```
docker pull emqx/mqttx-web

docker run -d --name mqttx-web -p 80:80 emqx/mqttx-web
```

## MQTTX CLI

### 支持使用 Docker 安装

在之前的版本中，MQTTX CLI 除提供了 macOS、Linux 和 Windows 上的的可执行文件外，还支持在 macOS 上使用 Homebrew，在包含 Node.js 环境的操作系统中使用 NPM 等方式来安装和使用 MQTTX CLI。

在最新的 1.8.2 版本中，我们还继续增加了支持 Docker 来安装和使用 MQTTX CLI。无论在什么操作系统环境，用户都能轻松安装并使用 MQTTX CLI，进行 MQTT 服务与应用的测试。

使用 Docker 镜像来安装 MQTTX CLI：

> 注意：使用如下 Docker 命令安装 MQTTX CLI 成功后，会自动进入到该容器内，您可以在容器内直接使用 mqttx 命令，使用完退出时，系统将自动删除容器

```
docker pull emqx/mqttx-cli

docker run -it --rm emqx/mqttx-cli
```

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



<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>
