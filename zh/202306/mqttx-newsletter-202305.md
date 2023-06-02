> MQTTX 是一个功能强大的跨平台 MQTT 5.0 桌面和命令行客户端工具，帮助用户简单快速的学习、探索和开发 MQTT 应用。它作为一个全面的 MQTT 客户端工具箱，为开发人员和用户提供了友好的界面和一系列强大的功能。
>
> 社区：[https://mqttx.app/zh](https://mqttx.app/zh)
>
> GitHub： [MQTTX: Powerful cross-platform MQTT 5.0 Desktop, CLI, and WebSocket client tools](https://github.com/emqx/MQTTX) 



在五月中旬，MQTTX 团队发布了全新的 1.9.3 版本。此版本正式将 **MQTT X 更名为 MQTTX**，进一步统一品牌标识。与此同时，MQTTX 命令行客户端中引入了一项**物联网场景数据模拟**的新功能，该功能允许开发者根据自身的测试场景需求来模拟数据，从而显著提升开发和测试效率。在 Docker 镜像方面，我们通过优化实现了显著的体积减小，为用户节省了宝贵的存储空间。MQTTX 一直致力于提供最佳的用户体验，为全球 MQTT 服务和应用的开发者提供最佳客户端工具。

最新版本下载地址：[Release v1.9.3 · emqx/MQTTX](https://github.com/emqx/MQTTX/releases/tag/v1.9.3) 

## 命令行客户端

### 物联网场景数据模拟

在这次的 1.9.3 版本中，MQTTX 命令行客户端增加了一个名为 `simulate` 的新命令，用于模拟特定场景下的 MQTT 发布消息。这个功能对于开发者进行系统测试尤为重要，它允许开发者根据自身的测试场景需求来模拟数据，比如模拟各类设备发送的数据，从而显著提升了开发和测试效率。这个命令基本上与发布基准（benchmark pub）命令有着相同的选项，以下只列出了新的或改变的选项。

用户可以通过运行 `help` 命令获取更多信息：

```
mqttx simulate --help
```

此功能的主要参数有：

- `-sc, --scenario`：模拟内置场景的名称
- `-f, --file`：本地自定义场景脚本的文件路径
- `-t, --topic`：消息主题，可选，支持变量，如%u（用户名），%c（客户端id），%i（索引），%sc（场景）。默认主题格式是 `mqttx/simulate/%sc/%c`

必须指定 `--scenario` 和 `--file` 参数中的一个，如果两者都指定，则优先考虑 `--file` 参数。

开发者可以编写自定义的物联网数据脚本来模拟特定的场景。例如，下面这段脚本生成了随机的温度和湿度数据：

```
function generator (faker, options) {
  return {
    message: JSON.stringify({
      temp: faker.datatype.number({ min: 20, max: 80 }),  // Generate a random temperature between 20 and 80.
      hum: faker.datatype.number({ min: 40, max: 90 }),   // Generate a random humidity between 40 and 90.
    })
  }
}
module.exports = {
  name: 'myScenario',  // Name of the scenario
  generator,          // Generator function
}
```

更多的例子和详细的编辑指南可以参考 MQTTX 的 GitHub 仓库中的 [scripts-example](https://github.com/emqx/MQTTX/tree/main/scripts-example/IoT-data-scenarios) 文件夹，或查看如何使用 [faker.js](https://fakerjs.dev/) 生成各种类型的随机数据。

MQTTX 命令行客户端内置了一些常见的场景，可以通过 `--scenario` 参数来指定。例如，运行 `mqttx simulate --scenario tesla` 即可模拟特斯拉汽车的数据。你也可以使用` mqttx ls --scenarios` 命令列出所有的内置场景。这个命令将输出一个表格，显示每个内置场景的名称和描述，如果你想在  simulat e命令中使用其中一个场景，只需要在 `--scenario` 选项中指定场景名称即可：

```
mqttx simulate --scenario <SCENARIO_NAME>
```

内置的场景包括：

- tesla：模拟特斯拉汽车数据
- IEM：模拟工业能源监控数据
- smart_home：模拟智能家居数据
- weather：模拟气象站数据

最后，新增了 `ls` 命令提供了可用资源的概览，不过当前，它支持列出内置的场景。

```
mqttx ls --help
```

例如，假设你想模拟一个场景，其中 10 个智能家庭设备正在向指定的主题发布数据。你可以运行以下命令：

```
mqttx simulate -sc smart_home -c 10 -h broker.emqx.io -t testtopic/smart_home
```

这个命令将启动 10 个模拟器（由 `-c 10` 参数指定），它们都将向 `testtopic/smart_home` 主题（由 `-t testtopic/smart_home` 参数指定）发布数据，模拟智能家庭设备的行为。这个数据将由内置的 `smart_home` 场景生成（由 `-sc smart_home` 参数指定）。同时，这些模拟器将连接到 `broker.emqx.io` 服务器（由 `-h broker.emqx.io` 参数指定）。在订阅了这个主题后，我们就能看到以下这样的数据：

```
{"home_id":"e5ee7759-464f-4df8-9b68-2afc906da39a","owner_name":"Dustin Hessel","address":"8850 Ona Circle","rooms":[{"room_type":"living room","temperature":19,"humidity":45,"lights_on":true,"window_open":false},{"room_type":"bedroom","temperature":23,"humidity":33,"lights_on":true,"window_open":false,"bed_occupancy":false},{"room_type":"kitchen","temperature":23,"humidity":50,"lights_on":false,"window_open":false,"fridge_temperature":5,"oven_on":true},{"room_type":"bathroom","temperature":23,"humidity":46,"lights_on":true,"window_open":true,"water_tap_running":false,"bath_water_level":68}],"timestamp":1684810770255}
```

此数据展示了一个智能家庭环境的状态，包含各个房间的温度、湿度、灯光状态等信息。

### Docker 镜像优化，提升部署效率

在 MQTTX 1.9.3 版本中，我们同时对 MQTTX CLI 和 MQTTX Web 客户端的 Docker 镜像进行了显著的优化。我们采用了多阶段构建（Multi-stage builds）技术，并切换到了基于 Alpine Linux 的 Node.js 环境（node:16-alpine）。这两项改动显著地减少了约 81.3% 左右的 Docker 镜像的体积。具体来说，MQTTX CLI Docker 镜像的大小从原来的 1.07GB 减少到了 200.52MB，而 MQTTX Web 客户端的 Docker 镜像体积也从原来的 886.75MB 减少到了 146.4MB。

这些优化不仅大幅度减少了用户的存储使用，也加快了镜像的下载速度，从而降低了用户的使用成本。优化后的镜像保持了功能完整，同时也提升了其运行效率。此外，这一改进也降低了网络传输的压力，使得在 Docker 环境下私有化部署 MQTTX Web 客户端更为简便、高效。

![MQTTX CLI Docker](https://assets.emqx.com/images/9bae879e41a12bc51b8527266b693d5f.png)

![MQTTX Web Docker](https://assets.emqx.com/images/2bcfc24dd6d7a5b14829bef63c6dc05c.png)

## 桌面客户端

### 自动重连功能

连接默认开启了自动重连的功能。如果由于网络问题或其他原因，MQTTX 桌面客户端与 MQTT 服务器的连接中断，那么客户端将会尝试自动重新连接。

### 连接状态下禁止编辑

在连接状态下，为了防止误操作和确保数据的一致性，我们禁止了用户进行编辑。

### 修复 Ubuntu 启动问题

我们修复了在 Ubuntu 系统上无法启动 MQTTX 的问题。现在 Ubuntu 用户可以正常使用我们的桌面客户端了。

### **Logo 更新**

我们优化了应用的标志，将 MQTT X 改为了 MQTTX，使其更加简洁和更具识别性。

![MQTTX](https://assets.emqx.com/images/4525c916a22af3be4e64655b7f58548c.png)

<center>New Logo Preview</center>

## 未来规划

- 将物联网场景数据模拟功能同步到桌面客户端中
- 提升对于特殊数据格式，如 JSON 在显示消息框内的高亮显示
- 支持 Protobuf 的消息格式
- 支持 Sparkplug B
- 可配置忽略 QoS 0 的消息存储，以减少存储空间的占用
- MQTT Debug 功能
- 接收到的消息可以进行自动图表绘制
- 插件功能（协议扩展 CoAP，MQTT-SN 等）
- 脚本测试自动化（Flow）



<section class="promotion">
    <div>
        立即体验 MQTTX
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>
