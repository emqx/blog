## Node-RED 简介

Node-RED 是一款编程工具，用于连接硬件设备、应用程序接口（API）和在线服务。它提供了一个基于浏览器的编辑器，使用户能够轻松地通过拖放各种节点来创建和管理流程。创建的流程可以一键部署到运行环境中。

Node-RED 支持 MQTT 协议，其中使用 `mqtt-in` 节点来接收数据，使用 `mqtt-out` 节点来发送数据。

**Node-RED 的主要特性包括**：

- **基于流程的编程**：通过可视化地连接节点来构建应用程序。
- **丰富的节点库**：提供多种节点，用于处理不同类型的输入、输出和任务。
- **通过消息通信**：节点通过相互传递消息进行通信。
- **基于浏览器的编辑器**：易于使用的界面，用于创建和部署流程。
- **可扩展性**：支持创建自定义节点，扩展功能以满足特定需求。
- **社区驱动开发**：基于 JSON 的流程可以轻松地导入和导出，并且能够通过在线流程库进行分享。

## MQTT 简介

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)（Message Queuing Telemetry Transport）是一种轻量级、基于发布-订阅模式的消息传输协议，特别适合资源受限的设备以及低带宽、高延迟或不稳定的网络环境。它在物联网（IoT）应用中非常流行，常用于传感器、执行器和其他设备之间的高效通信。

使用 MQTT 需要一个中央 Broker，例如 [EMQX](https://github.com/emqx/emqx)，它能确保可靠的消息传递并有效地扩展系统。

![MQTT PUB SUB](https://assets.emqx.com/images/f9a84128b10250dcd609b1748c5ef4dd.png)

## MQTT 与 Node-RED 结合使用的优势

将 MQTT 与 Node-RED 结合使用，为各种应用提供了强大的解决方案，尤其在物联网和实时数据处理方面。

1. **高效的数据处理**：Node-RED 能够实时处理 MQTT 消息，可以对传感器数据和其他输入作出快速反应。
2. **使用简便**：Node-RED 提供可视化编程界面，使复杂工作流的创建和部署变得简单，无需深入了解编程知识。
3. **适用于物联网**：Node-RED 的灵活性和丰富的节点库，使其能够无缝连接和处理各种物联网设备的数据。MQTT 提供的[服务质量（QoS）](https://www.emqx.com/zh/blog/introduction-to-mqtt-qos)级别、[保留消息](https://www.emqx.com/zh/blog/mqtt5-features-retain-message)和[遗嘱消息（LWT）](https://www.emqx.com/zh/blog/use-of-mqtt-will-message)功能，确保了在低带宽、高延迟或不可靠网络中的高效通信。
4. **广泛适用性**：Node-RED 不仅限于物联网应用，还适用于家庭自动化、工业自动化、数据可视化以及与云服务集成。
5. **可扩展性**：Node-RED + MQTT 支持构建可扩展的解决方案，能够高效处理大量设备和数据。

通过将 Node-RED 的可视化流程开发与 MQTT 的强大功能和轻量特性相结合，您可以在多个领域快速构建出具有可扩展性、可靠性和高效性的应用程序。

## 安装 Node-RED

Node-RED 可以安装在个人电脑、树莓派或云服务器等设备上，安装过程简单快捷。以下是两种常见的安装方法：

使用 `npm` 进行全局安装：

```shell
npm install -g --unsafe-perm node-red
```

使用 `Docker` 进行安装：

```shell
docker run -it -p 1880:1880 --name mynodered nodered/node-red
```

## 启动 Node-RED

如果通过 npm 全局安装 Node-RED，安装完成后，只需运行 node-red 命令，就能立即启动 Node-RED。

无论使用 Docker 还是 npm，成功启动后，只需在浏览器中输入当前地址和端口号 1880，即可访问 Node-RED 的编辑界面。例如，如果在本地运行，打开浏览器并输入 `http://127.0.0.1:1880`。当看到下图所示的页面时，表示 Node-RED 已成功启动：

![Node-RED](https://assets.emqx.com/images/cd66e004a35d9588c000d3f7e21ab5c2.png)

## 在 Node-RED 中使用 MQTT

在本文中，我们将使用 EMQ 提供的[免费公共 MQTT Broker](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该 Broker 基于 [EMQX](https://www.emqx.com/zh/products/emqx) Platform 构建。服务器详细信息如下：

- TCP 端口: **1883**
- SSL/TLS 端口: **8883**
- WebSocket 端口: 8083
- SSL/TLS 端口: 8883
- Secure WebSocket 端口: 8084

下面将分两部分介绍如何在 Node-RED 中使用 MQTT，基础部分介绍如何配置 MQTT 节点并连接到 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，进阶部分将讨论如何处理数据。

### 基础部分：配置 MQTT 节点并连接到 MQTT Broker

首先，打开浏览器并访问 `http://host:1880`，创建默认的 `Flow 1`。然后按照以下步骤操作：

#### 1. 配置订阅节点：消息输入

1.1. **添加 MQTT-in 节点**：从调色板中拖拽 `mqtt-in` 节点到中央画布，然后双击该节点打开配置页面。

1.2. **配置 MQTT Broker**：点击 `Server` 旁的编辑按钮，添加新的 MQTT Broker，输入 Broker 地址 `broker.emqx.io` 及其他连接详细信息，然后点击 `Add` 以保存 Broker 配置。

![Configure MQTT Broker](https://assets.emqx.com/images/f8fa66022aa1f0491b177e84a4245b07.png)

1.3. **订阅主题**：输入您想订阅的主题，如 `test/node_red/in`，选择合适的 QoS 级别，然后单击 `Done` 保存节点配置。

![Subscribe to a Topic](https://assets.emqx.com/images/118fb4eeca1cb5878feaef57aa9051e4.png)

#### 2. 配置发布节点：消息输出

2.1. **添加 MQTT-out 节点**：将 `mqtt-out` 节点拖到中央画布上，然后双击打开配置页面。

2.2. **配置 MQTT Broker**：确保选择了先前配置的 MQTT Broker。

2.3. **发布到主题**：输入您要发布的主题，如 `test/node_red/out`，选择适当的 QoS 级别，配置是否保留消息，然后单击 `Done` 保存节点配置。

![Publish to a Topic](https://assets.emqx.com/images/e88d164bd19825d95579dea943b6570b.png)

#### 3. 部署和测试

3.1. **连接节点**：将画布上的 `mqtt-in` 节点连接到 `mqtt-out` 节点，然后点击右上角的 `Deploy` 按钮来部署流程。

![Connect Nodes](https://assets.emqx.com/images/32a9d4ac3509a86ae3b2c53bf9c9f6d0.png)

3.2. **验证连接**：部署后，您应在每个节点下看到 `connected` 状态，表明已成功连接到 MQTT Broker。

3.3. **使用 MQTTX 客户端测试**：使用 [MQTTX](https://mqttx.app/zh) 作为您的 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)进行测试。向 `test/node_red/in` 主题发布消息，并订阅 `test/node_red/out` 主题，以验证消息接收情况。

![Test with MQTTX Client](https://assets.emqx.com/images/ea54db1af038429058dce11a315e6410.png)

按照上述步骤，您将成功在 Node-RED 中配置 MQTT 节点来处理消息的接收和发送。接下来，我们将探讨如何处理接收到的数据。

### 进阶部分：处理 MQTT 数据

#### 1. 数据访问

1.1. **添加 JSON 节点**：将 `JSON` 节点拖拽到画布上，并双击打开其配置页面。

1.2. **配置 JSON 转换**：将 `Action` 设置为 `Always Convert to JavaScript Object`，确保接收到的消息被正确转换为 JSON 格式。

1.3. **连接节点**：将 `JSON` 节点连接到 `mqtt-in` 节点。

![Connect Nodes](https://assets.emqx.com/images/2ac771a50e8247483530e0435631e8e1.png)

#### 2. 数据过滤

2.1. **添加过滤器节点**：将 `filter` 节点拖拽到画布上，并双击打开其配置页面。

2.2. **配置过滤规则**：将 `Mode` 设置为 `block unless value changes`，将 `Property` 设置为 `msg.payload.temperature`，以便根据温度值过滤消息。

2.3. **连接节点**：将 `filter` 节点连接到 `JSON` 节点。

![Connect the filter node to the JSON node](https://assets.emqx.com/images/41175ed585059d2141d46cde5eeeb753.png)

#### 3. 使用模板

3.1. **添加模板节点**：将 `Template` 节点拖拽到画布上，并双击打开其配置页面。

3.2. **配置模板**：输入模板内容来格式化过滤后的数据。

3.3. **可选步骤**：如果希望直接输出结果，可以跳过添加模板节点的步骤。

![Optional Step](https://assets.emqx.com/images/9fdd854b48233c53ad13dfe91eca084d.png)

#### 4. 发送处理后的数据

4.1. **添加 MQTT-out 节点**：在画布上拖拽一个 `mqtt-out` 节点，并双击打开其配置页面。

4.2. **配置 MQTT Broker**：确保选择了之前配置的 MQTT Broker。

4.3. **配置主题**：输入用于发布处理后数据的主题，例如 `test/node_red/out`，并设置所需的 QoS 级别。

4.4. **连接节点**：将 `MQTT-out` 节点连接到 `Template` 节点。

![Connect the MQTT-out node to the template node](https://assets.emqx.com/images/4c0918593a74410bdfadc874468215cf.png)

#### 5. 部署和测试

5.1. **部署该流程**：单击右上角的 `Deploy` 按钮进行部署。

5.2. **使用 MQTTX 客户端进行测试**：

- 向 `test/node_red/in` 主题发布一条消息，让 Node-RED 接收该数据。
- 订阅 `test/node_red/out` 主题，验证已处理的消息是否按照设定的模板接收。
- 检查 Node-RED 中的过滤逻辑，确保重复发送相同消息时不会重复接收。只有在温度值发生变化时，才会收到新的信息。

![Test with MQTTX Client](https://assets.emqx.com/images/c9af327ef1496f6e630c26fb84f766f0.png) 

通过这些步骤，您可以成功配置 Node-RED 来处理、过滤 MQTT 数据，并将处理后的数据通过 MQTT 发送出去。

## 结语

至此，我们完成了安装 Node-RED、连接 MQTT 云服务、过滤和处理 MQTT 消息，并最终发送处理后的数据的整个过程。Node-RED 的用户界面简化了业务逻辑的描述，降低了非专业开发人员的入门门槛。用户可以利用可视化工具，通过连接简单的节点，快速创建复杂的任务，这在物联网应用场景中尤为有用。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
