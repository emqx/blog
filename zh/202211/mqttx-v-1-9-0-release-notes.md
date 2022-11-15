近日，MQTT 5.0 客户端工具 MQTT X 1.9.0 正式发布。

新版本针对桌面客户端优化了一些细节上的 UI 样式与交互方式，新增了一个可以帮助用户更加快速和系统学习 MQTT 协议相关知识的页面，同时也修复了一些已知问题；针对命令行客户端新增了 `bench` 命令，帮助用户创建、订阅和发布自定义数量的连接、主题与消息，轻松完成 MQTT 服务的性能测试。

最新版本下载：[https://www.emqx.com/zh/try?product=MQTTX](https://www.emqx.com/zh/try?product=MQTTX) 

![MQTT 客户端](https://assets.emqx.com/images/cc8af08d253160ad08fe29999c92160c.png)


## 命令行客户端

### 新增开箱即用的 bench 命令

在 1.9.0 版本中，MQTT X CLI 提供了一个**内置、开箱即用**的性能测试命令工具 -- `mqttx bench`，可以帮助用户快速进行简单的性能和压力测试。用户只需简单安装或更新 MQTT X CLI 后，即可快速使用该命令，无需额外操作，方便易用。

> 如需大规模场景、深度定制化的测试服务推荐使用全托管 MQTT 负载测试云服务 [XMeter](https://www.emqx.com/zh/products/xmeter)

用户使用 `bench` 命令可以使用规定速率，创建自定义数量的连接，订阅自定义数量的 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)，向单个或多个主题中发送自定义数量的消息，通过一行命令即可简单地测试单个或集群下的 MQTT 服务器的连接性能、消息吞吐量等。例如：

1. 以每 10 毫秒创建一个连接的速率，创建 10000 个连接，客户端 ID 为 `mqttx-bench-%i`，`%i` 为索引占位符，即第 N 个客户端连接的客户端 ID 就 `mqttx-bench-n`：

   ```
   mqttx bench conn -c 10000 -i 10 -I "mqttx-bench-%i"
   ```

2. 启动 5000 个订阅客户端连接，同时订阅主题 `mqttx/bench/t`：

   ```
   mqttx bench sub -c 5000 -t mqttx/bench/t
   ```

3. 最后启动 200 个发布客户端连接，向主题 `mqttx/bench/t` 发布消息，消息速率为每秒 200 条，消息内容为 `mqttx/bench/test`：

   ```
   mqttx bench pub -c 200 -im 1000 -t mqttx/bench/t -m "mqttx bench test"
   ```

通过以上简单的性能测试中的连接、订阅和发布命令，就可以轻松实现一些简单自定义场景下的 MQTT 性能基准测试，并通过其结果来调试和优化您的 MQTT 服务与系统环境，从而进一步提升您的物联网应用与服务。

MQTT X CLI 的 bench 命令不仅使用简单易上手，其内容输出也非常简洁。对于大量的连接、订阅和发布的输出内容，我们优化了其显示方式，通过动态更新实时的数量，避免在使用过程中被大量输出日志刷屏。

![MQTT Bench](https://assets.emqx.com/images/6d942b32742bf859ef66a93abb216860.png)

### 添加 Retain 消息标识

此外，MQTT X CLI 新增了 [MQTT Retain](https://www.emqx.com/zh/blog/mqtt5-features-retain-message) 消息标识，用户可以通过查看接收到的消息中是否包含有 `retain: true` 来判断是否为 Retain 消息。Retain 消息标识可以帮助用户更好地理解消息的来源为实时消息还是保留消息，从而验证消息的正确性。

![MQTT Retain](https://assets.emqx.com/images/4e5635e47b07ccbaab54eb1f9195dda0.png)


## 桌面客户端

### 脚本功能增强

在之前的版本中，MQTT X 只能对于收发消息进行简单的静态数据处理，例如使用随机函数模拟数据，对于特定数据格式的消息模版做一些格式转化或提取关键数据等。

在 v1.9.0 中，我们增强了脚本功能，让用户可以实现一些动态的数据的模拟操作。例如当用户在定时发送中，需要动态地切换两种消息内容，分别为开关指令的打开和关闭，此时可以使用脚本中新增的 `index` 的参数，通过发送的步长判断，来动态地将两个消息内容进行交替切换，帮助用户来快速测试不同命令切换时其系统的稳定性。除此之外我们还为脚本函数新增了一个 `msgType` 参数，通过消息类型参数，可以扩展更多的消息转换能力。

> 注意：index 参数仅在使用定时消息发送时可以接收到。

![脚本功能增强](https://assets.emqx.com/images/23716622e8e7fec28f0ebd4a98a14b68.png)

### MQTT 协议帮助页面

除了提供强大的测试客户端工具帮助开发者快速开发和调试 MQTT 服务与应用，我们也希望开发者能在这一过程中更加深入地理解 MQTT 协议并充分运用其相关特性。

因此，MQTT X 1.9.0 为用户新增了一个帮助页面，提供包括基础知识、快速使用、连接参数说明、客户端编程教程等 MQTT 协议相关的各类内容，帮助用户快速搭建自己的 MQTT 物联网应用。MQTT X 通过满足用户测试需求的各项功能，以及系统知识与实用案例详解参考，成为用户搭建和设计 MQTT 物联网应用的坚实后盾。

![MQTT 协议帮助页面](https://assets.emqx.com/images/f48ce43f7561ee6908d4f53ae3a56e7d.png)

### UI 与交互优化

我们对于 MQTT X 的 UI 与交互也进行了一些细节上的调整与优化，以提升用户体验。

在左侧连接列表的顶部，我们将新建分组按钮修改为了一个单一的添加按钮，通过点击新建按钮，我们可以选择快速新建一个连接，或为连接快速创建一个分组，避免了用户混淆创建分组与创建连接；同时优化了连接按钮样式显示等。

![新建 MQTT 连接](https://assets.emqx.com/images/d8f92bbb3d393069338d09f1632cc5b7.png)

在交互方面，我们新增了一些更加实用的快捷键，例如在连接列表中可以通过 `Ctrl or Cmd + N` 快捷键来新建一个连接，通过使用 `Ctrl or Cmd + B` 快捷键来快速跳转到关于页面，查看 MQTT X 的一些基础信息。这些快捷键将使用户操作变得更加方便。

### 其它

- 客户端顶部的系统菜单栏中，进行了国际化显示，而非纯英文显示
- 修复了在重新连接后，无法接收到已订阅过主题的消息的问题
- 移除了一些不正确的配置项单位

## 未来规划

MQTT X 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网应用与服务的测试和开发提供便利。接下来我们将重点关注以下方面，敬请期待：

1. MQTT X CLI 支持自动重连
2. 接收消息和存储时的性能优化，大量消息不卡顿
3. CLI 支持使用配置文件来进行连接、发布和订阅
4. MQTT Debug 功能
5. 支持 Sparkplug B 格式
6. 接收到的消息可以进行自动图表绘制
7. 插件功能
8. 脚本测试自动化（Flow）





<section class="promotion">
    <div>
        立即体验 MQTT X
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>
