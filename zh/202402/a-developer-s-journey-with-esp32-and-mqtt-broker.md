作为一名后端开发人员，我经常需要同时运行多个 Jetbrains IDE （集成开发环境），所以经常面临笔记本电脑过热问题。我曾尝试过各种散热方法，从传统的风扇到更先进的半导体冷却系统，但这些方法都带来了新的问题，如噪音和耗电等。

因此，我设计了一个智能的液冷散热解决方案：通过引入外部水冷系统、利用微控制器 ESP32、MQTT 服务器 EMQX Cloud Serverless 以及容器化的部署平台 [Fly.io](http://fly.io/) 来实时监测和控制水温。以下是该解决方案的详述，希望能为其他物联网开发者带来灵感：

![物联网智能液冷散热系统](https://assets.emqx.com/images/01e79e675c0348f3a0f885042077b543.png)

<center>作者 DIY 的物联网智能液冷散热系统</center>

## 技术选型

我希望这套系统不仅有功能性，还具备可靠性和效率，以确保水温监控系统的稳定运行。以下是我挑选的技术栈：

- **ESP32：**在多种选择中，ESP32 微控制器因其集成了 Wi-Fi 和蓝牙功能，以经济高效的特点而脱颖而出。这款芯片为物联网项目提供了强大的性能支持，同时成本可控又不牺牲功能性。
- **DS18B20 水温传感器：**对于温度监控，DS18B20 是我的首选，因为它提供了精确的数字温度读数和出色的耐水性能。这款传感器与 ESP32 可协同工作，确保了水温监控系统的准确性和稳定性。
- **EMQX Cloud Serverless MQTT Broker：**在众多消息中间件中，[EMQX Cloud](https://www.emqx.com/zh/cloud) 因其高性能、可靠性以及 Serverless MQTT 服务在处理大量并发连接和消息路由方面的卓越表现而受到青睐，这些特性对于确保设备间通信的顺畅至关重要。
- **Python 和 Flask：**选择 Python 是因为它的表达力强且库函数丰富，Flask 则轻量级且高度灵活，能适应快速开发和部署的需求，这对于迅速实现项目原型至关重要。
- [Fly.io](http://fly.io/)：Fly.io 的全球分布式边缘托管服务能够将容器转换为微虚拟机，提供了一个独特的平台。这不仅加快了应用的部署速度，还大大减少了数据传输的延迟，为用户提供了接近实时的体验。

## 项目实施

项目的实施阶段是一个将创意转化为实际解决方案的过程。在这个过程中，首先要确保 EMQX Cloud Serverless 的正确配置，然后是硬件的集成，后端服务的开发，最后是系统的部署和测试。

### Serverless MQTT Broker 配置

[EMQX Cloud Serverless](https://www.emqx.com/zh/cloud/serverless-mqtt) 提供免费配额，对于我们的应用场景来说，这些配额完全能够覆盖所需的成本，这也是我选择 EMQX Cloud Serverless 部署的主要原因之一。另外，它默认支持传输层安全协议（TLS），为我们的数据传输提供了强有力的加密保障，确保数据在传输过程中的机密性、完整性和身份验证，降低了数据泄露或被篡改的风险。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud Serverless
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>

以下是配置 EMQX Cloud Serverless 的具体步骤：

1. **创建 Serverless MQTT Broker:**
   - 登录到 EMQX Cloud 控制台，并导航至 "Create Deployment" 页面。
   - 选择 "Serverless" 部署类型，并按需配置部署。例如区域、SpendLimit 等。
   - 完成配置后，点击 "Create" 按钮，系统会自动创建 Serverless MQTT Broker。
2. **添加认证信息:**
   - 在 MQTT Broker 创建成功后，进行认证信息的配置，确保只有授权的客户端可以连接到 Broker。
3. **使用 MQTTX 连接测试:**
   - 下载并安装 MQTTX 客户端（[MQTTX：全功能 MQTT 客户端工具](https://mqttx.app/zh)），然后使用之前配置的认证信息测试与 MQTT Broker 的连接，确保一切工作正常。

通过以上步骤，我成功地配置了 EMQX Cloud Serverless MQTT Broker，为我们的项目提供了一个安全、可靠且成本效益高的消息中间件。它不仅简化了物联网基础设施的管理和扩展，还通过 TLS 支持确保了数据的安全传输，为项目打下了良好的基础。

### 硬件集成

在项目中，我们使用 ESP32 微控制器和 DS18B20 水温传感器来监测水温，并将数据发送到云端。通过这种集成，我们实现了一个能夠实时监测并传输水温数据的系统，高效且安全，同时为水冷系统提供了智能化的监控。

1. **Wi-Fi 连接配置：** 首先，ESP32 被配置为通过 Wi-Fi 连接到互联网。这是通过在代码中设置 Wi-Fi 的 SSID 和密码来实现的。
2. **传感器初始化：**我们通过 GPIO 25 将 DS18B20 水温传感器连接到 ESP32，并在代码中初始化了传感器，设置了温度读取的分辨率。
3. **安全的 MQTT 通信：** 使用 MQTT 协议，通过 EMQX Cloud Serverless 来安全地传输数据。我们配置了 MQTT broker 的详细信息，并使用了 SSL/TLS 加密来保证数据传输的安全。
4. **温度数据读取与发送：** 系统每分钟读取一次水温，并将读数格式化为 JSON 后，通过 MQTT 协议发布到云端。

### 使用 Python 和 Flask 开发后端服务

在这个项目中，我们使用 Python 和 Flask 构建了后端服务，以处理来自 ESP32 的温度数据并展示在网页上。整个后端的设计旨在高效处理数据、提供实时反馈，并易于维护。通过这种方式，我们构建了一个既能实时处理来自物联网设备的数据，又能提供用户友好界面的后端服务。这不仅加强了项目的实用性，也为未来的扩展和优化提供了良好的基础。

1. **配置和 MQTT 集成**：我们的 Flask 应用配置了 MQTT 代理设置，使用 `flask_mqtt` 库实现与 MQTT 代理的直接通信。当接收到来自 `emqx/esp32/telemetry` 主题的消息时，后端会通过特定函数处理并存储数据。
2. **数据库管理**：使用 SQLite 数据库存储温度数据，通过 Flask 的应用上下文管理数据库连接，并确保数据的安全存储和访问。
3. **Web 界面和 API**：后端提供了简单的 Web 界面和一个 API 端点。主页链接到一个显示温度图表的页面，而数据 API 端点返回最近一段时间的温度数据。

### 系统部署

项目的部署阶段至关重要，我们通过 Docker 和 Fly.io 的配置将 Flask 应用容器化并托管于 Fly.io。这一流程不仅实现了 Flask 应用的云端部署，还确保了服务的快速、安全和高效提供。借助 Fly.io 平台，应用可以根据需求轻松扩展，享有稳定的运行环境。

1. **Docker 容器化**：首先，我们编写 Dockerfile，使用 Python 3.8 作为基础镜像，并将应用代码复制到容器的 `/app` 工作目录。然后，通过 `pip` 安装必要依赖，例如 Flask 和 Flask-MQTT，并暴露 8080 端口。容器启动时会自动执行 `CMD ["python", "app.py"]`，运行 Flask 应用。
2. **Fly.io 配置**：在 `fly.toml` 文件中，我们定义了应用的运行方式，包括应用名称、主部署区域（如新加坡），构建及挂载点设置。
   - **挂载点**：设定挂载点存储数据库文件，保证数据在容器重新部署时的持久性。
   - **HTTP 服务配置**：配置内部端口为 8080，强制使用 HTTPS，并设定启动、停止策略和最小运行机器数量。
   - **健康检查**：通过定期访问 `/ping` 路由，检查应用运行状态，保障服务稳定。
3. **部署应用**：
   1. **创建 Fly.io 应用**：使用 `flyctl apps create` 命令，通过 Fly.io 的 CLI 工具创建新应用。
   2. **部署应用**：执行 `flyctl deploy` 命令，在 Fly.io 上自动构建 Docker 容器镜像并部署。
   3. **验证部署**：部署完成后，访问 Fly.io 提供的应用 URL，检验 Flask 应用是否成功运行。

## 项目成果

### 实时温度监控系统

利用 ESP32 微控制器和 DS18B20 水温传感器的强大功能，我们设计并实现了一个能够实时监控和调控水冷系统温度的系统。现在，我的笔记本电脑不再因高温而过热，能够稳定运行，而我也可以在任何时候，无论是在咖啡馆的露台上还是在家中的书桌前，享受平静而舒适的工作环境。

### 稳定的数据传输

通过 EMQX Cloud Serverless，我们实现了从 ESP32 到云端的数据传输的安全性和可靠性。EMQX Cloud Serverless 是一款高性能的 MQTT 代理，具有低延迟特性，能够实时接收和处理温度数据。这确保了系统能够迅速做出反应，并保持高效运行。

### 功能丰富的 Web 界面

Python 和 Flask 的强大组合为我们提供了一个简洁而直观的 Web 界面，使用户能够轻松查看实时温度数据和历史温度曲线。这不仅提升了用户体验，也使得温度监控更为直观、更易于管理。

![功能丰富的 Web 界面](https://assets.emqx.com/images/e3a9da581f21259d989ccd3aaa34c53b.png)

### 全球分布式云端部署

借助 Fly.io 的全球分布式服务，我们的 Flask 应用得以在云端高效运行。这种部署方式不仅确保了应用的高可用性和稳定性，也极大地减少了数据传输的延迟，为用户提供了近乎实时的体验。

![截图](https://assets.emqx.com/images/1a6d3a7d1ff24dbf2aca23db1ee95f5b.png)

 

## 总结与展望

从最初遇到的笔记本过热问题，到构建一个实时的水温监控系统，这个项目充分展示了现代物联网技术是如何帮我们解决生活中的实际问题。

通过整合 ESP32、DS18B20 水温传感器、EMQX Cloud Serverless MQTT Broker、Python、Flask 以及 Fly.io 云平台的能力，我们成功地开发出一个既实用又高效的系统。这个系统不仅提高了我的工作效率，也为类似问题提供了一个创新的解决方案。

对这个项目感兴趣或希望深入了解技术细节的读者，可以在 GitHub 上的 [EMQX 的 MQTT 客户端示例](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-ESP32/esp32_DS18B20_temp_chart)中找到完整的代码和更多实现细节。这个资源库不仅是学习和实践的宝库，还可能激发你对物联网和云计算的新想法和创造力。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
