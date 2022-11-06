十月初，MQTT X 团队发布了 1.8.3 版本。对桌面端应用实现了 MQTT 5.0 版本适配，MQTT X CLI 支持了多主题订阅，同时修复了多个已知问题。此外，团队正专注于 1.9.0 版本的开发，最主要的更新是为 MQTT X CLI 加入了新的命令 – `bench`，即 MQTT 性能测试命令，帮助用户可以创建、订阅和发布自定义数量的连接、主题与消息。安装或更新后即可快速使用，无需额外操作。

## 桌面端应用：添加帮助页面

作为一款强大的 MQTT 5.0 测试客户端工具，MQTT X 的愿景一直是帮助开发者可以更快地开发和调试 MQTT 服务与应用，同时也能在 MQTT 的研究与应用中更深入地理解 MQTT 协议及相关特性。

因此 MQTT X 除提供了简单高效的连接、发布和订阅等功能测试能力外，在目前正在开发的 1.9.0 版本中，还新增了一个帮助页面。该页面不仅提供了查看和使用 MQTT X 的文档链接，还提供了 MQTT 基础入门系列与实践编程系列的内容模块，帮助一些正在学习或初次接触到 MQTT 的用户快速了解 MQTT 协议，理解协议中的各项配置参数和使用方法，查看其使用场景与案例。此外还提供了各类编程语言、平台及框架下的丰富的客户端编程教程，助力用户使用 MQTT 协议快速完成物联网应用的开发。

![MQTT X 帮助页面](https://assets.emqx.com/images/3408df84e030aeacdaad134766aadd36.png)


## MQTT X CLI：新增性能测试工具

MQTT X CLI 作为一款强大的 MQTT 命令行测试工具，不仅方便安装，支持在各类操作系统和平台中使用，还提供了丰富且完善的各类测试命令和较为完整的 MQTT 配置参数，方便用户快速集成到一些测试脚本中。

在 1.9.0 版本中，我们继续增强其功能性，为用户带来一个**内置、开箱即用的性能测试命令** – `bench` 命令。用户只需简单安装或更新 MQTT X CLI 后，即可快速使用该命令，无需额外操作，方便易用。

> 如需大规模场景、深度定制化的测试服务推荐使用全托管 MQTT 负载测试云服务 [Xmeter](https://www.emqx.com/zh/products/xmeter) 

用户使用 `bench` 命令可以使用规定速率，创建自定义数量的连接，订阅自定义数量的主题，向单个或多个主题中发送自定义数量的消息，通过一行命令即可简单的测试单个或集群下的 MQTT 服务器的连接性能，消息吞吐量等。例如：

- 以每 10 毫秒创建一个连接的速率，创建 10000 个连接，客户端 ID 为 `mqttx-bench-%i`，`%i` 为索引占位符，即第一个客户端连接的客户端 ID 就为 `mqttx-bench-1`

   ```
   mqttx bench conn -c 10000 -i 10 -I "mqttx-bench-%i"
   ```

- 启动 5000 个订阅客户端连接，同时订阅主题 `mqttx/bench/t`

   ```
   mqttx bench sub -c 5000 -t mqttx/bench/t
   ```

- 最后启动 200 个发布客户端连接，向主题 `mqttx/bench/t` 发布消息，消息速率为每秒 200 条，消息内容为 `mqttx bench test`

   ```
   mqttx bench pub -c 200 -im 1000 -t mqttx/bench/t -m "mqttx bench test"
   ```

通过以上简单的性能测试中的连接、订阅和发布命令，就可以轻松实现一些简单自定义场景下的 MQTT 性能基准测试，并通过其结果来调试和优化您的 MQTT 服务与系统环境，从而进一步提升您的物联网应用与服务。

MQTT X CLI 的 `bench` 命令不仅使用简单易上手，其内容输出也非常简洁。对于大量的连接、订阅和发布的输出内容，我们优化了其显示方式，通过动态更新实时的数量，避免在使用过程中被大量输出日志刷屏。

![MQTT X CLI bench](https://assets.emqx.com/images/6ebb4dc5fb056fe349e565adf629f9fb.png)


## 未来规划

MQTT X 还在持续增强完善中，以期为用户带来更多实用、强大的功能，为物联网平台的测试和开发提供便利。接下来我们将重点关注以下方面：

- 使用体验升级
- 接收到的数据支持自定义图表化
- 插件系统（例如支持 SparkPlug B、集成 MQTT X CLI）
- 脚本功能优化
- 推出 MQTT X Mobile 移动端应用
- 完善 MQTT X Web 功能
- MQTT Debug 功能




<section class="promotion">
    <div>
        立即体验 MQTT X
    </div>
    <a href="https://www.emqx.com/zh/try?product=MQTTX" class="button is-gradient px-5">免费下载 →</a>
</section>
