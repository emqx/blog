## 什么是 OPC UA？

OPC UA（OPC Unified Architecture）是一个独立于平台、面向服务、开放和安全的通信架构。它被设计用来实现不同供应商的工业自动化设备、系统和软件应用的互操作性。OPC UA 信息模型定义了使用各种传输协议交换数据的编码规格。

OPC UA 和其前身——开放平台通信（OPC）是由同一个基金会所开发，但两者有显著不同，基金会继续开发 OPC UA 的目的是为了发展比原来 OPC 通讯更理想的架构，也更符合正在发展中的工业自动化需求。

OPC UA 规范的第一个版本于2006年问世，截止到目前 OPC UA 最新的版本是1.05。除了 Client-Server（Subscriptions）模式以外，OPC UA 还加入了 Pub-Sub 的机制，可以通过 UDP 协议、[MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)或者 [AMQP 协议](https://www.emqx.com/zh/blog/mqtt-vs-amqp-for-iot-communications)推送 JSON 规格的数据结构（也可以使用其标准定义的二进制规格——UADP）。

通过 MQTT 协议提供的快速、安全和可靠的传输通道，OPC UA 可以直接运用 Internet 进行数据传输，同时保留了 OPC UA 端到端的安全性和标准化数据建模的关键优势。

![OPC UA](https://assets.emqx.com/images/f4582b4676a6867f6beefa40c055fae2.png)

## OPC UA 的特点

**功能对等性**：所有 OPC Classic 规范都映射到 UA，OPC UA 包含 OPC Classic 中的 DA、A&E 和 HDA 功能：

| 功能     | 说明                                                         |
| -------- | ------------------------------------------------------------ |
| 发现     | 在本地 PC 或网络上查找可用的 OPC UA 服务器                   |
| 地址空间 | 所有数据都是分层表示的（例如文件和文件夹），允许 OPC UA 客户端发现、利用简单和复杂的数据结构 |
| 按需     | 基于访问权限读取和写入数据/信息                              |
| 订阅     | 监视数据/信息，并且当值变化超出客户端的设定时报告异常        |
| 事件     | 基于客户端的设定通知重要信息                                 |
| 方法     | 客户端可以基于在服务器上定义的方法来执行程序等               |

**安全性：**信息加密、身份验证和审核，企业在选择技术标准时最重要的考虑之一是安全性。OPC UA 在通过防火墙时通过提供一套控制方案来解决安全问题：

| 功能       | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| 传输       | 定义了许多协议，提供了诸如 OPC 二进制传输或更通用的 SOAP-HTTPS 等选项 |
| 会话加密   | 信息以128位或256位加密级别安全地传输                         |
| 信息签名   | 信息接收时的签名与发送时必须完全相同                         |
| 测序数据包 | 通过排序消除了已发现的信息重放攻击                           |
| 认证       | 每个 UA 的客户端和服务器都要通过 OpenSSL 证书标识，提供控制应用程序和系统彼此连接的功能 |
| 用户控制   | 应用程序可以要求用户进行身份验证（登录凭据，证书等），并且可以进一步限制或增强用户访问权限和地址空间“视图”的能力 |
| 审计       | 记录用户和/或系统的活动，提供访问审计跟踪                    |

**综合信息建模：**用于定义复杂信息，OPC UA 信息建模框架将数据转换为信息，通过完全面向对象的功能，即使是最复杂的多级结构也可以建模和扩展，数据类型和结构可在配置文件中定义。

![OPC UA Information Modelling Framework](https://assets.emqx.com/images/1161f4a8f02d771efa813f234c8515a9.png)

## OPC UA 的信息模型

OPC UA 信息模型是节点的网络（Network of Node），或者称为结构化图（Graph），由节点（Node）和引用（Reference）组成，这种结构图称之为 OPC UA 的地址空间。地址空间以标准形式表示对象——地址空间中的模型元素被称为节点，对象及其组件在地址空间中表示为节点的集合，节点由属性描述并由引用相连接。OPC UA 建模其实就是建立节点以及节点间的引用。

### 对象模型

OPC UA 使用了对象作为过程系统表示数据和活动的基础。对象包含了变量，事件和方法，它们通过引用来互相连接。

![OPC UA Object Model](https://assets.emqx.com/images/313bb04eebc2beaacc6c359eba0e17d8.png) 

### 节点模型

![OPC UA Node Model](https://assets.emqx.com/images/185c6a8d55d470c5e558bd3afd76a0ca.png) 

- 属性（Attribute）用于描述节点，不同的节点类有不同的属性（属性集合）。节点类的定义中包括属性的定义，因此地址空间中不包括属性。

- 引用（Reference）表示节点之间的关系。引用被定义为引用类型节点的实例，存在于地址空间中。

- 节点模型的通用属性如下：

| Name                | Use | Data Type              | Description                                |
  | ------------------- | --- | ---------------------- | ------------------------------------------ |
  | **Attributes**      |     |                        |                                            |
  | NodeId              | M   | NodeId                 | See 5.2.2                                  |
  | NodeClass           | M   | NodeClass              | See 5.2.3                                  |
  | BrowseName          | M   | QualifiedName          | See 5.2.4                                  |
  | DisplayName         | M   | LocalizedText          | See 5.2.5                                  |
  | Description         | O   | LocalizedText          | See 5.2.6                                  |
  | WhiteMask           | O   | AttributeWhiteMask     | See 5.2.7                                  |
  | UserWriteMask       | O   | AttributeWriteMask     | See 5.2.8                                  |
  | RolePermissions     | O   | RolePermissionsType[]  | See 5.2.9                                  |
  | UserRolePermissions | O   | RolePermissionsType[]  | See 5.2.10                                 |
  | AccessRestrictions  | O   | AccessRestrictionsType | See 5.2.11                                 |
  | **References**      |     |                        | No References specified for this NodeClass |

### 引用模型

包含引用的节点为源节点，被引用的节点称目标节点。引用的目标节点可以与源节点在同一个地址空间，也可以在另一个 OPC 服务器的地址空间，甚至是目标节点可以不存在。

![OPC UA Reference Model](https://assets.emqx.com/images/3b484967bea36515325de244dda332bd.png)

### 节点类型

在 OPC UA 中，最重要的节点类别是对象，变量和方法。

- 对象节点，对象节点用于构成地址空间，不包含数据，使用变量为对象公开数值，对象节点可用于分组管理对象，变量或方法（变量和方法总属于一个对象）。

- 变量节点，变量节点代表一个值，值的数据类型取决于变量，客户端可以对值进行读写和订阅。

- 方法节点，方法节点代表服务器中一个有客户端调用并返回结果的方法，输入参数和输出结果以变量的形式作为方法节点的组成部分，客户端指定输入参数，调用后获得输出结果。

## 为什么将 OPC UA 桥接到 MQTT？

MQTT（Message Queuing Telemetry Transport）是一种为物联网设备和应用程序设计的消息协议，采用发布与订阅模型，具有轻量、高效、可靠，支持实时通讯等优点。 MQTT 非常适合资源受限的环境，特别是需要高效使用电力和带宽的场景。

业界在 MQTT 3.1.1 的基础上建立了名为 SparkplugB 的工业物联网数据规范，在保证灵活和效率的前提下，提供了基础的数据统一建模能力。得益于 MQTT 协议的优秀设计，SparkPlugB 提供了良好的网络状态感知能力，并且能够为设备和系统提供强大的互操作性。

OPC UA 和 MQTT 在功能上有一定程度的重叠，但它们的使用场景却截然不同：

- OPC UA 是一种用于工业场景的通信协议，可使来自不同制造商的不同设备和系统使用标准化语言进行无缝通信。

- MQTT 是一种物联网协议，专为基于互联网的传感器数据传输而设计，既能满足低带宽和不可靠的网络条件，又能有效处理连续的实时数据。它的订阅/发布机制为使用提供了极大的灵活性。

在工业场景中，MQTT 擅长在分布式系统中发送信息，而 OPC UA 则侧重于提供互操作性。通过将两者结合，可以使用 OPC UA 对业务数据进行抽象和聚合，而 MQTT 则可以利用其强大的连接能力，以分布式方式实现无缝数据交换。

## OPC UA over MQTT

OPC 基金会在最新的 OPC UA 规范中提出的 Pub-Sub 模型允许使用 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 将数据变更推送给订阅者。

![OPC UA over MQTT](https://assets.emqx.com/images/e3772239f0f42b2f622996c721d7e57f.png)

Pub-Sub 的安全性比客户端/服务器中的安全性要复杂一些，而且规范没有那么细致。在 MQTT 网络中，安全性基于 SSL/TLS，MQTT Broker 除了可以为传输启用 SSL/TLS，还可以定义应用程序级身份验证，原则上，对于每个可以加入网络的订阅端和发布端，这些安全模式要么全有，要么全无。新的 OPC UA 标准化仍在进行中，丰富的 OPC UA 信息模型如何以最佳方式映射到 MQTT 目前尚不明确。

## 通过 Neuron 将 OPC UA 桥接到 MQTT

[Neuron](https://www.emqx.com/zh/products/neuron) 是一款现代的工业物联网连接服务器，可以连接多种使用标准协议或者设备专有协议的工业设备，实现了工业物联网平台与海量设备的互联。作为一款轻量级的工业协议网关软件，Neuron 可以运行在各种有限资源的物联网边缘硬件设备上，其主要目标是应对以统一方式访问以数据为中心的自动化设备的挑战，从而为智能制造提供必要的支持。

[EMQX](https://www.emqx.io/zh) 是一款大规模可扩展的云原生分布式物联网 MQTT 消息服务器。作为全球最具扩展性的 MQTT 消息服务器，EMQX 可为海量物联网设备提供高效可靠的连接，实现消息和事件流的高性能实时移动和处理，帮助用户快速构建关键业务的物联网平台与应用。

Neuron 的南向 OPC UA 驱动程序可采集和汇总 OPC UA 数据源，将其转换为 MQTT 协议，并传输到 EMQX MQTT Broker。然后，后者将其分发到各种分布式应用程序。

在本文中，我们将利用 Neuron 和 EMQX 提供从 OPC UA 到 MQTT 的桥接解决方案。我们将演示使用 Neuron 从 Prosys OPC UA Simulator 收集数据，将收集到的数据上传到本地构建的 EMQX MQTT Broker（mqtt://192.168.10.174:1883），最后使用 MQTTX 订阅主题查看数据的变化。

| **应用**                        | **IP 地址**    | **端口** |
| ------------------------------- | -------------- | -------- |
| Prosys OPC UA Simulation Server | 192.168.10.174 | 53530    |
| Neuron                          | 192.168.10.174 | 7000     |
| EMQX                            | 192.168.10.174 | 1883     |
| MQTT X                          |                |          |

### 安装 OPC UA 模拟器

安装包可从 [Prosys OPC 网站](https://www.prosysopc.com/products/opc-ua-simulation-server/)下载。安装完成后，运行 Prosys OPC UA Simulation。确保 Neuron 与模拟器运行在同一局域网内。

点击 **Objects->Objects::FolderType->Simulation::FolderType** 查看数据，并选择 Counter::BaseDataVariableType.

![Select Counter::BaseDataVariableType](https://assets.emqx.com/images/5a4d4723a45d66d48327d45be58fd1e1.png)

### 启动 EMQX

执行以下命令安装并运行 EMQX 容器。有关如何安装 EMQX 容器的更多信息，请访问[安装指南](https://www.emqx.io/docs/zh/v5.0/deploy/install.html)。

```
docker pull emqx/emqx:5.1.0
docker run -d --name emqx -p 1883:1883 -p 8081:8081 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083
```

### 设置 Neuron

Neuron 提供多种安装方法，您可以在[安装指南](https://neugates.io/docs/zh/latest/installation/installation.html)中详细查看。本示例使用容器化部署，以便尽快开始体验 Neuron。执行以下命令安装并运行 Neuron 容器。

```
$ docker pull emqx/neuron:latest
$ docker run -d --name neuron -p 7000:7000 --privileged=true --restart=always emqx/neuron:latest
```

打开网络浏览器，输入运行 Neuron 的网关地址和端口号，进入管理控制台页面。默认端口号为7000。通过浏览器访问 `http://localhost:7000`（可以用实际 IP 地址代替 localhost）。

#### 步骤 1：登录

页面打开后，进入登录界面，使用初始用户名和密码（初始用户名：admin，初始密码：0000）登录。

#### 步骤 2：添加南向设备

在**配置**菜单中选择**南向设备**，进入到南向设备界面，点击**添加设备**新增设备。

- 名称：填写设备名称，例如 opcua-195-prosys。

- 插件：下拉框选择 **OPC UA** 插件。

#### 步骤 3：设置南向设备参数

添加南向设备后自动进入设备配置界面，填写参数并提交。

- 端点 URL：填写 OPC UA Simulation Server 的连接地址，如：opc.tcp://192.168.10.174:53530/OPCUA/SimulationServer。

- 用户名：默认不用填写。

- 密码：默认不用填写。

- 证书：默认不用上传。

- 密钥：默认不用上传。

确保 Prosys OPC UA Simulation Server 已经切换到 Expert Mode （**Option->Switch to Expert Mode**），点击 **Certificates** 将左侧列表中的 NeuronClient@localhost 设置为 Trusted。

![Click **Certificates**](https://assets.emqx.com/images/18303ffbc9c775f0cbcb30243db9a401.png)

#### 步骤 4：在设备卡片中创建组

点击设备节点卡片任意空白处，进入组列表管理界面，点击 **创建** ，弹出 **创建组** 的对话框。填写参数并提交：

- 组名称：填写组名称，例如 group-1。

- 间隔：默认1000。

#### 步骤 5：在组中添加数据点位

进入点列表管理界面，点击**创建**，填写点参数并提交：

- 名称：填写点位名称，例如，Counter。

- 属性：下拉选择点位属性，例如，Read，Write。

- 类型：下拉选择数据类型，例如，INT32。

- 地址：填写驱动地址，例如，3!1001。3代表 OPC UA 模拟器中数据点的 Namespace，1001代表数据点的 Node ID。

- 描述、乘系数、精度不填。

#### 步骤 6：数据监控中查看采集数据

选择**监控**→**数据监控**，进入数据监控界面，查看已创建点位读取到的数值，如下图所示。

- 南向设备：下拉框选择想要查看的南向设备，例如，选择已创建的 opcua-195-prosys。

- 组名称：下拉框选择想要查看所选南向设备下的组，例如，选择已创建的 group-1。

- 选择完成，页面将会展示读取到的组中所有点位的值。

  ![Neuron Dashboard](https://assets.emqx.com/images/cfdde4aa2e321cbe37c55a373e9a18c8.png)

#### 步骤 7：为应用程序添加北向插件模块

在**配置**菜单中选择**北向应用**，点击**添加应用**。

- 名称：填写应用名称，例如，MQTT。

- Plugin：下拉框选择 MQTT 插件。

#### 步骤 8：设置北向应用参数

- 客户端 ID：注意此 ID 要相互独立，重复 ID 会导致客户端被踢除。例如设置为，MQTT1999。

- QoS 等级：默认为 0。

- 上报数据格式：默认为 Values-format。

- 写请求主题：默认为/neuron/MQTT/write/req。

- 写响应主题：默认为/neuron/MQTT/write/resp。

- 离线缓存：默认关闭。

- 服务器地址：填写本地安装的 EMQX MQTT Broker 地址，地址为192.168.10.174，即您实际的 IP 地址。

- 服务器端口：默认1883。

- 用户名、密码：不填。

- SSL：默认关闭。

#### 步骤 9：订阅南向点位组

转到订阅组列表，然后单击**添加订阅**。

- 南向设备：下拉框选择已创建的南向设备，例如 opcua-195-prosys。

- 组：下拉框选择所要订阅的组，例如 group-1。

- 主题：MQTT 主题，本例中默认为/neuron/MQTT/group-1。接下来在 MQTTX 中订阅此主题并接收消息。

### 使用 MQTTX 查看数据

可进入 [MQTT X 官网](https://mqttx.app/zh)下载 MQTT X 并安装。安装好后启动 MQTTX 后添加连接，Host 设置为 `mqtt://192.168.10.174`，Port 设置为 `1883`，订阅主题 `/neuron/MQTT/group-1`，就可以接收到 OPC UA 端传输过来的数据了。

![MQTTX](https://assets.emqx.com/images/f72e055d59d5728b079df244ebdb6f0f.png)

## 结语

OPC UA 协议实现了设备之间的通信和数据交换，而 MQTT 则提供了一种高效、灵活和安全的消息传递机制。通过利用这两种协议的优势，该集成可将设备数据无缝传输到云端，从而促进高效、安全的远程监控。从设备和流程中获取实时信息的能力使企业能够优化运营、提高生产率并确保最高质量水平。采用这种创新方法不仅能提高工业系统的整体效率，还能为更智能的数据驱动型决策铺平道路，推动各行业走向更加互联和繁荣的未来。



<section class="promotion">
    <div>
        免费试用 Neuron
      <div class="is-size-14 is-text-normal has-text-weight-normal">连接海量异构工业设备从边缘到云端。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
