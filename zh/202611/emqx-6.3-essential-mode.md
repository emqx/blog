轻量级、高可用是实际场景中常见的部署需求，例如部署在边缘网关上的 MQTT Broker，需要与并行运行的应用共享资源。数据采集、本地处理和存储都会争用内存与计算资源，因此，Broker 的资源占用是部署时需要考虑的重要因素。

以这样一台网关为例：数据采集器通过 MQTT 发布测量数据，本地应用订阅这些数据，另一个独立服务负责存储和向上游通信。在这种架构下，Broker 只需要提供可靠的消息路由和访问控制即可，像数据库连接器（Connector）和 Web 管理控制台这类功能则并非必需。

**通过** [**EMQX Enterprise 6.3**](https://www.emqx.com/zh/blog/emqx-6-3-0-release-notes) **的 Feature Gates（功能门控），用户现在可以自由控制 Broker 启动时启用哪些功能。**其中，**ESSENTIAL 模式**能让 EMQX 仅加载核心 MQTT 功能、身份验证及授权模块，默认关闭所有可选应用。无需切换或下载单独的发行版，即可为资源受限的部署场景带来更轻量的初始资源占用。

## ESSENTIAL 模式保留了哪些功能



ESSENTIAL 模式面向只需要核心 MQTT Broker、无需完整 EMQX 应用套件的部署。下表为该模式下可用的功能以及默认禁用的模块，用户可据此评估其是否适合当下的业务需求：

| 功能                                  | ESSENTIAL 模式 |
| :------------------------------------ | :------------- |
| 核心 MQTT Broker、身份验证和授权      | 可用           |
| 保留消息、配置系统和 CLI              | 可用           |
| Dashboard 和管理 REST API             | 默认禁用       |
| 规则引擎、连接器和数据桥接            | 默认禁用       |
| Prometheus 导出器、非 MQTT 网关和插件 | 默认禁用       |

无论选择哪种功能组合，核心应用始终可用。当业务需要时，可以通过自定义配置随时扩展可选功能。

在前文的网关示例中，各应用仍可通过 MQTT 发布和订阅消息，并按需配置身份验证和主题权限。由于禁用了 Dashboard 和管理 REST API，运维人员可通过配置文件、日志和 CLI 工具对 Broker 进行日常管理。

## ESSENTIAL 模式如何减少资源占用



### 按需加载代码



首先，停止可选应用节省了运行时的额外开销。此外，ESSENTIAL 模式还会指示 Erlang 虚拟机仅在需要时才动态加载代码模块，而非在启动时预加载发行版中的所有模块。未使用的功能代码将保留在磁盘上，从而显著降低常驻内存。EMQX 会为 ESSENTIAL 预设自动选择这种代码加载方式。

### 减少单连接的后台开销



在 EMQX 6.3.0 中，当禁用 Dashboard 后，系统还会自动跳过仅供 Dashboard 客户端信息 API 使用的单连接定期统计上报。这直接消除了以往跨所有连接重复执行的后台任务开销。

在 ESSENTIAL 模式下，EMQX 的**空载启动内存占用可降至 100 MB 以下**（注：实际内存会随连接数、TLS 加密、订阅关系及排队消息增加而变动，且受运行环境影响）。

在共享网关上，应使用有代表性的流量，让 Broker 与其他应用一同运行并测量资源占用。测试负载中应包括慢订阅和重连场景，静态启动时的内存测算无法反映真实高负载下的极限。

## 如何开启 ESSENTIAL 模式



只需在 EMQX 进程启动前，设置以下环境变量即可：

```
export EMQX_FEATURES=ESSENTIAL
```

**Docker Compose / Kubernetes**：将该变量写入 Broker 的部署定义文件中。

**RPM / DEB 安装包**：可将其持久化写入 `/etc/emqx/emqx.env` 文件：

```
EMQX_FEATURES=ESSENTIAL
```

EMQX 会优先读取 `emqx.env`，其赋值会覆盖继承的环境变量，请保持配置一致。修改配置后需重启节点。

启动后，可以查看 `feature_gates_resolved` 日志条目，确认已启用的预设以及开启/禁用的功能列表。在 ESSENTIAL 模式下，管理 API 已被禁用，请直接通过日志了解系统状态。

## 实测：在 100 MB 内存限制的 Docker 中运行



以下本地测试在 1 CPU、100 MB 内存限制且禁用 Swap 的环境（Docker）中启动 EMQX 6.3.3，并通过 MQTTX CLI 完成一次 QoS 1 消息收发。

> **测试准备**：请使用 Linux 容器模式的 Docker，并在宿主机安装 [MQTTX CLI](https://mqttx.app/docs/cli/downloading-and-installation)，确保客户端运行在 Broker 的内存限制之外。MQTT 端口仅映射至 `localhost`。

启动全新容器：

```
docker run -d --name emqx-essential-demo \
  --cpuset-cpus=0 --cpus=1 \
  --memory=100m --memory-swap=100m \
  --restart=no --no-healthcheck \
  -e EMQX_FEATURES=ESSENTIAL \
  -p 127.0.0.1:1883:1883 \
  emqx/emqx-enterprise:6.3.3
```

Broker 会在后台启动。如果端口 1883 已被占用，请换一个主机端口，并在下面两条 MQTTX 命令中使用该端口。

Docker 中的 `100m` 表示 100 MB，约为 104.9 MB。将 `--memory` 与 `--memory-swap` 设置为相同数值可禁用容器 Swap 交换区。CPU 参数限制容器仅运行在逻辑 CPU 0 上，且配额为 1 个 CPU 时间。

在当前终端中持续查看内存占用：

```
docker stats \
  --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}' \
  emqx-essential-demo
```

在第二个终端中，以 QoS 1 订阅主题：

```
mqttx sub -h 127.0.0.1 -p 1883 -t essential/demo -q 1
```

等待 MQTTX 显示 `Subscribed to essential/demo`。这表示 Broker 已就绪，订阅也已生效。然后在第三个终端中发布消息：

```
mqttx pub -h 127.0.0.1 -p 1883 -t essential/demo -q 1 \
  -m 'Hello from ESSENTIAL'
```

订阅端会显示：

```
topic: essential/demo, qos: 1
Hello from ESSENTIAL
```

在一次本地 Linux ARM64 测试中，Docker 显示容器启动后内存占用约为 90 MB；订阅端连接后，内存占用降至 84–85 MB。

```
NAME                  CPU %     MEM USAGE / LIMIT
emqx-essential-demo   0.15%     85.76MiB / 100MiB
```

Broker 在不使用 swap、没有 OOM 终止或容器重启的情况下完成了消息收发。根据 [Docker 的内存显示说明](https://docs.docker.com/reference/cli/docker/container/stats/)，Docker 展示的内存值会扣除非活动文件缓存；内核记录的总内存峰值达到了 100 MB 上限。可将此测试作为启动和消息传递检查，但生产环境仍应根据有代表性的流量评估资源需求。

按 Ctrl-C 停止订阅端和内存监控，然后移除演示容器及其匿名数据卷和日志卷：

```
docker stop emqx-essential-demo
docker rm -v emqx-essential-demo
```

## 按需选择功能



如果网关业务发生变化，需要将 EMQX 的遥测数据直接写入数据库，则可以将配置调整为启用数据集成：

```
export EMQX_FEATURES=data_integration
```

使用此设置重启后，EMQX 除了启动核心 Broker 外，还会启动规则引擎、连接器（Connectors）、动作（Actions）和数据源（Sources），并自动激活所依赖的 `schema_registry` 功能。此时 Dashboard 和 Prometheus 导出依然保持禁用。数据库连接器和对应的规则需要另外配置。

同样的机制也适用于需要远程管理或 Prometheus 监控的 Broker：

| **部署需求**                                       | `EMQX_FEATURES` **设定值**           |
| -------------------------------------------------- | ------------------------------------ |
| 核心 MQTT 与访问控制                               | `ESSENTIAL`                          |
| 核心功能 + 数据集成（及其依赖的 Schema Registry）  | `data_integration`                   |
| 核心功能 + Dashboard 及 REST API                   | `dashboard`                          |
| 核心功能 + Prometheus 导出（及其依赖的 Dashboard） | `metrics`                            |
| 数据集成 + Dashboard + Prometheus 导出             | `dashboard,data_integration,metrics` |
| 开启全部功能                                       | `FULL`                               |

系统支持自动依赖解析（例如选择 `metrics` 会自动启用 `dashboard`）。无论选择哪种组合，身份验证与授权作为核心功能均始终保持开启。

配置时可以使用预设名称，也可以指定功能名称列表。 `ESSENTIAL,metrics` 为无效配置，若需要该功能，应直接指定 `metrics`。若填入无效配置，系统将无法启动；若未设置或为空，则默认开启 `FULL`（全部功能）。

> **注意**：自动按需加载代码功能为 ESSENTIAL 模式专享，自定义功能列表不会自动继承该机制。开启自定义功能组合后，请务必在对应业务负载下进行内存测算。

## 支持边缘高可用集群部署



ESSENTIAL 模式不仅适用于单节点边缘网关，同样完整支持集群部署，非常适合需要在边缘构建高可用架构的场景。

相比单节点模式需要独立处理所有连接与数据，集群架构可以在多个边缘节点间动态分担消息负载；当某个节点发生硬件或网络故障时，集群能够自动将流量重路由至健康节点，确保物联网服务持续不中断。

在 ESSENTIAL 模式下组建集群，既能享受核心 MQTT Broker 的极低资源占用，又能具备支撑关键业务的高可用与弹性扩展能力，为边缘侧的大规模 MQTT 消息平台提供既轻量又可靠的底层支撑。

## 将功能选择纳入部署配置



功能开关属于**部署级别的配置**，修改选择必须重启节点，且无法在运行时通过 Dashboard、REST API 或 CLI 进行动态修改。集群中的所有节点必须保持配置一致，以确保管理端点和后台服务行为统一。

这也使得功能选择成为了部署评审中的重要一环。计划新增数据库集成时，变更内容应明确包含 Broker 启用的功能、连接器配置和资源需求。团队可以在上线前一并测试这些内容。

对于仅处理本地 MQTT 流量的边缘网关，ESSENTIAL 模式是一个精简高效的起点。当业务扩展时，你可以按需开启所需的功能。**从核心需求起步，在真实负载下测试，并将最终配置纳入部署规范。**

- 了解完整功能列表与部署细节，请参阅 EMQX Feature Gates 官方文档：[功能门控 | EMQX 企业版 文档](https://docs.emqx.com/zh/emqx/latest/get-started/deploy/feature-gates.html) 
- 立即体验 EMQX Enterprise 6.3：[下载 EMQX 企业版](https://www.emqx.com/zh/downloads-and-install/enterprise) 



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
