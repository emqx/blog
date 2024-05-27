## Mosquitto_pub/sub 概述

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种轻量级消息传递协议，在物联网项目中对设备通信至关重要。

Mosquitto 特别提供了 `mosquitto_pub` 和 `mosquitto_sub` 两个命令行工具，专为提升 MQTT 的测试和故障排查效率而设计。这些工具使得用户能够高效地与 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)进行互动：通过 `mosquitto_pub` 发布消息，以及通过 `mosquitto_sub` 订阅主题。这种高效的操作方式，极大方便了基于 MQTT 的应用的快速开发与调试。

您可以从官方网站下载包含 MQTT Broker 和客户端工具的 Mosquitto 软件包：[![img](https://mosquitto.org/favicon-16x16.png)Download](https://mosquitto.org/download/) 。

## Mosquitto_pub/sub 的优点

- **包含测试 MQTT 的基本功能：**Mosquitto_pub/sub 提供了适合各种测试场景的基本 MQTT 测试功能，包括订阅（sub）和发布（pub）消息。

  **示例**：

  ```shell
  mosquitto_sub -h broker.emqx.io -p 1883 -t 'testtopic/#'
  mosquitto_pub -h broker.emqx.io -p 1883 -t 'testtopic/1' -m 'hello'
  ```

- **轻量且易于使用**：设计精巧，安装简便，非常适合快速开发场景。

- **开源并享有社区支持**：在 [GitHub](https://github.com/eclipse/mosquitto) 上托管，能够得到开源项目所特有的充满活力的社区支持。

- **全面支持 MQTT 5.0**：完全支持 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 协议及其所有最新功能。

- **调试模式**：支持调试模式，能够帮助开发人员有效地诊断和解决问题。

## Mosquitto_pub/sub 的核心功能

Mosquitto_pub/sub 是用 C/C++ 语言开发的，它是 Mosquitto 更广泛生态系统的一部分，为物联网项目提供了简单的发布和订阅能力，从而便于 MQTT 消息的传递。其核心特性包括：

- **集成 Broker 和客户端工具**：Mosquitto 提供了完整的 MQTT 解决方案，包括集成的 Broker 和客户端工具（`sub` 和 `pub`），使得 MQTT 通信的设置和管理变得简单。

- **请求-响应命令**（`mosquitto_rr`）：除了基础的 `sub` 和 `pub` 功能，Mosquitto 还包含了适用于 MQTT v5/3.1.1 的 `mosquitto_rr` 命令。该命令利用请求-响应特性发布消息并等待回复。

  **示例**：

  ```shell
  mosquitto_rr -t request-topic -e response-topic -m message
  ```

  该客户端功能通过支持直接的请求-响应通信模式，增强了 MQTT 消息的传递能力，这对于动态数据交换和物联网交互尤为重要。

- **高级 TLS 支持：**Mosquitto_pub/sub 通过 `mosquitto-tls` 命令扩展了基础 TLS 功能，提供了更全面的 SSL/TLS 配置，确保了 MQTT 通信的安全。它提供了关于生成和应用 SSL 证书以实现加密连接和认证的详细指导，强调为 CA、服务器和客户端设置不同的证书参数以避免冲突。使用 `mosquitto-tls` 可以增强安全性，使 Mosquitto 成为安全 MQTT 部署的理想选择。

- **Mosquitto_pub/sub 中的增强连接特性：**Mosquitto_pub/sub 通过高级的网络功能，丰富了 MQTT 通信体验。

  - **-A bind-address** allows specifying network interfaces for targeted traffic flow, enhancing data security and transmission efficiency, as in `mosquitto_pub -A 192.168.1.5...`
  - **-L, --url** consolidates connection details into a single URL, streamlining setup processes, shown by `mosquitto_sub -L mqtt://...`
  - **--proxy** enables SOCKS5 proxy use, boosting privacy and offering network adaptability, demonstrated with `mosquitto_sub --proxy socks5h://...`
  - **-A 绑定地址** 允许指定网络接口，以针对性地管理流量，提高数据传输的安全性和效率，例如 mosquitto_pub -A 192.168.1.5...
  - **-L, --url** 将连接信息整合到一个 URL 中，简化了配置过程，例如 `mosquitto_sub -L mqtt://...`
  - **–proxy** 支持使用 SOCKS5 代理，增强了隐私保护并提供了网络适应性，例如 `mosquitto_sub --proxy socks5h://...`

  这些选项增强了对 MQTT 网络配置的控制，使通信更加简便和安全。

- **Mosquitto_pub/sub 中的高级消息传输特性：**Mosquitto_pub/sub 引入了强大的消息管理选项。

  - **--stdin-file | --file (pub)** allows publishing from files or stdin, simplifying automation and handling large payloads, as seen in mosquitto_pub --file /path/to/message.txt...
  - **--repeat (pub)** enables periodic message republishing, which is helpful for regular updates or testing. Mosquitto_pub... -repeat 5 -repeat-delay 10 demonstrates this.
  - **--filter-out | --random-filter (sub)** offers message filtering based on topics or randomness, enhancing subscription relevance, shown with mosquitto_sub --filter-out 'testtopic/ignore
  - **–stdin-file | --file (pub)** 允许从文件或标准输入发布消息，简化了自动化流程并能够处理大量数据，例如 `mosquitto_pub --file /path/to/message.txt...`
  - **–repeat (pub)** 支持定期重复发布消息，这对于定期更新或测试非常有用。例如 `mosquitto_pub... -repeat 5 -repeat-delay 10`
  - **–filter-out | --random-filter (sub)** 提供了基于主题或随机性的消息过滤功能，提升了订阅内容的相关性，例如 `mosquitto_sub --filter-out 'testtopic/ignore'`

  这些功能使发布和订阅过程更加高效，提高了 MQTT 工作流的效率。

除了这些关键功能，Mosquitto_pub/sub 还提供了更多选项，用于精细化的消息和订阅管理，例如处理保留消息、动态取消订阅、改进的输出格式等，增强了其在各种 MQTT 任务中的实用性。

## Mosquitto_pub/sub 的应用场景

Mosquitto_pub/sub 是为安全、高效的 MQTT 消息传递而设计的理想工具，它是对 Mosquitto Broker 的完美补充。对于物联网安全项目来说，它提供了 TLS 支持和多样化的网络功能。除了设备间的通信，它在测试和开发方面也显示出其强大的优势——通过诸如消息过滤和自动化等功能，它能够方便系统的详尽测试。

- **设备测试**：确保智能设备能够可靠地发布和接收 MQTT 消息。
- **系统调试**：利用 `-repeat` 和 `--filter-out` 进行反复测试，以精细调整物联网平台。

这些特性使得 Mosquitto_pub/sub 成为众多 MQTT 应用不可或缺的工具，它不仅加快了开发流程，还增强了系统的功能。

## Mosquitto_pub/sub 的局限性

Mosquitto_pub/sub 作为 MQTT 消息传递的强大工具，尽管在多数场合表现出色，但在某些特定场景下也存在一些局限：

- **功能方面**：它在基础的发布/订阅操作上表现优异，但对于更高级的数据处理和消息传输模式，如复杂的消息过滤或支持多种数据格式，可能功能不够全面。
- **捆绑安装**：Mosquitto_pub/sub 作为 Mosquitto 包的一部分，包含了 Broker。这意味着，仅寻求独立客户端测试的用户可能会不经意间安装了 Broker 组件，这可能会为他们的配置带来不必要的复杂性。
- **定制化和扩展性**：其定制选项主要是命令行参数，对于需要高度专业化的场景或需要集成到更复杂系统中的情况，可能缺乏所需的灵活性。

虽然 Mosquitto_pub/sub 是一个可靠且轻量级的工具，提供了强大的安全特性，但它的局限性意味着对于那些有着高级需求或需要独立客户端功能的用户来说，可能并不完全适合。在这种情况下，用户可能需要寻找其他选项或使用变通方法来满足他们的具体需求。

## MQTTX CLI：Mosquitto_pub/sub 的替代方案

[MQTTX CLI](https://mqttx.app/zh/cli) 是 MQTTX 的命令行版本，是一款功能强大的开源 MQTT 5.0 命令行客户端，专为 MQTT 服务和应用的快速开发与调试而设计。它提供了丰富的命令功能，包括发布消息、订阅主题、性能基准测试、调试模式以及物联网数据模拟，是 MQTT 开发不可或缺的工具。

MQTTX CLI 作为一个纯粹的客户端工具，并不包含任何 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 组件。它支持多种安装方式，包括本地系统安装、Docker、Homebrew 和 npm，确保在不同操作系统中都能轻松部署。

立即下载：[MQTTX Download](https://mqttx.app/zh/downloads) 

### MQTTX CLI 的高级特性

MQTTX CLI 继承了 Mosquitto_pub/sub 的所有优点，并增加了以下高级特性：

- **连接命令**：与专注于基本 `sub` 和 `pub` 功能的 Mosquitto_pub/sub 不同，MQTTX CLI 提供了一个直接的连接命令来测试网络连通性。

  **示例**：

  ```shell
  mqttx conn -h 'broker.emqx.io' -p 1883 -u 'admin' -P 'public'
  ```

  这个特定命令简化了验证 Broker 连接的流程，为开发者在进行更多 MQTT 操作之前快速确认配置是否正确提供了便利。

- **配置管理**：MQTTX CLI 引入了配置导入和导出的强大功能。用户可以将命令参数保存至本地文件，以便将来使用。

  **示例**：

  ```shell
  mqttx conn --save ../custom/mqttx-cli.json
  mqttx conn --config ../custom/mqttx-cli.json
  ```

  这一功能通过重复使用配置，提高了不同环境或项目设置的效率。它支持 JSON 和 YAML 格式，并提供默认路径，使得管理和应用多种配置变得简单而灵活。

- **增强的输出和日志记录**：MQTTX CLI 通过清晰的日志风格的输出，提升了用户体验，为用户提供了精确的 MQTT 通信信息。

  **示例**：

  ```shell
  ❯ mqttx sub -h broker.emqx.io -p 1883 -t 'testtopic/#'
  [3/1/2024] [3:59:44 PM] › …  Connecting...
  [3/1/2024] [3:59:45 PM] › ✔  Connected
  [3/1/2024] [3:59:45 PM] › …  Subscribing to testtopic/#...
  [3/1/2024] [3:59:45 PM] › ✔  Subscribed to testtopic/#
  [3/1/2024] [3:59:45 PM] › topic: testtopic/SMH/Yam/Home/GartenLicht/stat/POWER1
  qos: 0
  retain: true
  payload: { "msg": "hello" }
  ```

  详细且结构化的日志格式简化了问题诊断过程，提升了开发和调试的整体体验。这种详细程度确保开发者能够轻松排查问题。

- **基准测试工具**：MQTTX CLI 的连接、订阅和发布等基准测试工具，提供了开箱即用的详尽性能分析。

  **示例**：

  ```shell
  mqttx bench pub -h broker.emqx.io -t 'testtopic' -m 'hello' -c 100
  ```

  这些工具通过提供 MQTT 操作的吞吐量和延迟等信息，帮助进行性能优化，对于系统性能的微调至关重要。

- **模拟功能**：MQTTX CLI 支持 MQTT 应用的高级模拟，用户可以选择内置场景或通过脚本自定义场景。

  **示例**（使用内置场景）：

  ```
  mqttx simulate -h broker.emqx.io -p 1883 --scenario tesla -c 10
  ```

  **示例**（使用自定义脚本）：

  ```shell
  mqttx simulate -h broker.emqx.io -p 1883 -c 10 --file ./customScenario.js
  ```

  它通过模拟各种 MQTT 流量模式，为应用提供了全面的测试环境，这对于评估应用在各种场景下的弹性和性能至关重要，有助于确保应用为实际使用做好充分准备。

- **数据管道**：MQTTX CLI 简化了 MQTT 数据的管理和管道化，通过 Clean 模式以及与 `jq` 集成等功能，使得数据处理变得直接而简单。

  **示例**（从 [MQTT 报文](https://www.emqx.com/zh/blog/introduction-to-mqtt-control-packets)中提取有效载荷）：

  ```shell
  mqttx sub -t topic --output-mode clean | jq '.payload'
  ```

  **示例**（用额外细节重构数据）：

  ```shell
  mqttx sub -t topic --output-mode clean | jq '{topic, payload, retain: .packet.retain, userProperties: .packet.properties.userProperties}'
  ```

  这些示例展示了如何利用 MQTTX CLI 结合 `jq` 等工具轻松构建高效的数据管道，用于检索和操作物联网数据。这项功能极大地简化了数据管道的构建过程，无需复杂编程即可处理 MQTT 数据。

- **多样化的数据格式支持**：MQTTX CLI 支持多种数据格式，包括 JSON、Hex、Base64、Protobuf 和 CBOR，为数据处理提供了灵活性。

  **示例**：

  ```shell
  mqttx sub -h broker.emqx.io -p 1883 -t 'testtopic/json/data' --format json
  ```

  这使得数据的解释和操作变得多样化，满足了广泛的物联网应用需求。

## 选择适合您 MQTT 项目的工具

总的来说：

- **Mosquitto_pub/sub** 在需要轻量级、安全的 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)和 Broker 集成的场景中优势明显。它在性能和安全特性方面的卓越表现，使其成为全面 MQTT 解决方案的理想选择。
- **MQTTX CLI** 提供更广泛的功能，着重于用户体验和高级配置的便捷性。在需要处理多样化数据和进行深度定制的环境中，它展现出其独特的优势。

对于基础的 MQTT 客户端任务，以及那些需要更多高级特性的场景，MQTTX CLI 是更合适的选择。它提供了一个全面而灵活的工具集，以应对现代物联网开发的各种挑战。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
