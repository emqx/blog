## 介绍

Datadog 是一款基于云服务的可观测性和安全平台，提供自动化基础设施监控、应用程序性能监控、日志管理、真实用户监控等功能。它为应用程序提供统一、实时的可观测性和安全性解决方案，帮助开发人员轻松监控、分析和优化其应用程序的性能和可靠性。

近日，EMQX 正式支持与 Datadog 的[集成](https://docs.datadoghq.com/integrations/emqx/)，允许用户利用 Datadog 收集 EMQX 集群的设备连接、消息吞吐和延迟指标，以及节点性能和功能运行状态。通过这些数据，用户和运维人员可以更好地了解当前服务的状态，并监测和排除系统性能问题，更好地构建高效、可靠和实时数据传输的物联网应用。

本文将通过四个步骤向您详细展示如何将 EMQX 与 Datadog 集成。

## 第 1 步：安装 Datadog Agent

要开始使用 Datadog，请访问 [Datadog](https://www.datadoghq.com/) 创建一个帐户并登录进入 Datadog 控制台。

接下来，您需要在 EMQX 所在的服务器上安装 [Datadog Agent](https://docs.datadoghq.com/getting_started/agent/)。

[Datadog Agent](https://docs.datadoghq.com/getting_started/agent/) 用于收集 EMQX 指标并将指标发送到 Datadog 云端，需要部署在 EMQX 集群所在服务器或能够访问 EMQX 节点的服务器上。如果您还未安装 Agent，可以按照以下步骤进行操作：

1. 菜单栏选择 **Integrations** → **Agent** 打开 Agent 安装说明页面。

2. 根据实际情况，选择您对应操作系统版本，按照页面指引进行安装。

   ![Integrations → Agent](https://assets.emqx.com/images/f5dc4443f90dc32752c60012042d0c48.png)

## 第 2 步：在 Datadog 中添加 EMQX 集成

EMQX 提供了开箱即用的[ Datadog 集成](https://docs.datadoghq.com/integrations/emqx/)，您可以使用如下步骤，将其添加到您 Datadog 控制台中：

1. 菜单栏选择 **Integrations** → **Integrations** 打开集成页面。

2. 在 **Search Integrations** 搜索框中，输入 EMQX，找到同名且作者是 EMQX 的集成。

3. 打开集成，在弹出框中点击右上角 **Install Integration** 按钮，即可将集成添加到 Datadog 中。

   ![Click the Install Integration](https://assets.emqx.com/images/e2caea6a2bc01590b403b2c3bd271cbb.png)

1. 安装完成后，切换到 **Configure** 标签页查看 EMQX 集成的配置指引，配置所需的操作均在 Datadog Agnet 上进行。

   ![Configure tab](https://assets.emqx.com/images/a46f1e6438b018cbf461ae24567cfcde.png)

## 第 3 步：在 Datadog Agnet 上添加并启用 EMQX 集成

根据配置指引，在 Datadog Agent 上添加 EMQX 集成，以完成 EMQX 指标的采集与上报配置。

1. 在 Datadog Agent 所在服务器运行以下命令为 Agent 添加 EMQX 集成。此处使用的是 1.1.0 版本，请根据指引内容使用最新的版本。

   ```shell
   datadog-agent integration install -t datadog-emqx==1.1.0
   ```

2. 安装完成后，修改 Agnet 配置文件以启用 EMQX 集成：

   打开 Agent 配置目录（默认是 `/opt/datadog-agent/etc/conf.d/`），找到目录下的 `emqx.d` 目录，可以看到 `emqx.d` 目录下有一个示例配置文件 `conf.yaml.example`。

   在相同目录下复制一份该文件并重命名为 `conf.yaml`，修改文件中的以下配置项：

   ```shell
   instances:
     - openmetrics_endpoint: http://localhost:18083/api/v5/prometheus/stats?mode=all_nodes_aggregated
   ```

   `openmetrics_endpoint` 选项是 Datadog Agnet 提取 OpenMetrics 格式的指标数据的地址，这里设置的是 EMQX 的 HTTP API 地址。实际使用中，请修改为 Datadog Agent 能够访问到的地址。

   该 API 还支持通过 `mode` 查询参数指定拉取的指标范围，每个参数的含义如下：

   ![The meaning of each parameter](https://assets.emqx.com/images/90e6fd142c844c160d492c6f713265f2.png)

   为方便统一查看，此处使用 `mode=all_nodes_aggregated` 配置，Datadog 控制上将看到整个集群的值。

3. 参考此处[重启 Agent](https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent)，以 macOS 为例：

   ```shell
   launchctl stop com.datadoghq.agent
   launchctl start com.datadoghq.agent
   ```

4. 重启后使用以下命令检查 EMQX 集成是否成功启用，当看到 `Instance ID: ... [OK]` 时表示已经启用成功：

   ```shell
   $ datadog-agent status | grep emqx -A 4
       emqx (1.1.0)
       ------------
         Instance ID: emqx:1865f3a06d300ccc [OK]
         Configuration Source: file:/opt/datadog-agent/etc/conf.d/emqx.d/conf.yaml
         Total Runs: 17
         Metric Samples: Last Run: 166, Total: 2,822
         Events: Last Run: 0, Total: 0
         Service Checks: Last Run: 1, Total: 17
         Average Execution Time : 43ms
         Last Execution Date : 2024-05-11 17:35:41 CST / 2024-05-11 09:35:41 UTC (1715420141000)
         Last Successful Execution Date : 2024-05-11 17:35:41 CST / 2024-05-11 09:35:41 UTC (1715420141000)
   ```

至此，您已经完成 Datadog Agnet 端的所有配置，Agent 将定期收集 EMQX 运行数据，并发送到 Datadog 中。接下来，我们到 Datadog 控制台中查看指标是否正确收集。

## 第 4 步：在 Datadog 控制台上查看 EMQX 指标

Datadog Agnet 的 EMQX 集成提供了一个开箱即用的 Dashboard 图表，用于展示节点状态、消息状态信息，以及其他更深入的可观察性指标。我们可以通过以下步骤使用：

1. 菜单栏选择 **Integrations** → **Integrations** 打开集成页面。

2. 在已安装的集成中找到 EMQX 集成，点击打开。

3. 在弹出框中选择 **Monitoring Resources** 标签页，打开 **Dashboards** 下的 **EMQX Overview** 图表。

   ![Monitoring Resources tab](https://assets.emqx.com/images/330598b3ec6536a48a028143de23883c.png)

**图表包含以下内容**

- OpenMetrics Health: 活跃的指标收集器数量
- Total Connections：总连接数，包含已断开但保留会话的连接
- NodeRunning：集群中正在运行的节点数
- Active Topics：活跃主题数
- NodeStopped：集群中已停止的节点数
- Connection
  - Total：连接总数，包含已断开但保留会话的连接
  - Live：活跃连接数，即保持了 TCP 连接
- Topic
  - Total：主题总数
  - Shared：共享主题数
- Session：会话数
- Erlang VM：Erlang 虚拟机的 CPU、内存和队列使用情况
- Retainer&Delayed
  - Retained：保留消息数
  - Delayed：延迟消息数
- Message
  - Sent&Received：发送和接收消息速率
  - Delayed&Retained：延迟和保留消息速率
  - Publish&Delivered：发布和传递消息速率
  - Delivery Dropped：丢弃的传递消息数
- Client
  - Connected&Disconnected：连接和断开连接速率
  - Sub&UnSub：订阅和取消订阅速率
  - AuthN&AuthZ：认证和授权速率
  - Delivery Dropped：丢弃的传递消息数
- Mria：Mria 事务数量

以下是部分图表的截图，当 EMQX 负载和客户端情况发生变化后，相应的数值也会变化。

![Metrics Overview](https://assets.emqx.com/images/4ff04f0ce8a1195c5dcc6026060b2cd6.png)

<center>概览指标</center>

<br>

![Connection, Topic, and Session](https://assets.emqx.com/images/c45ccd37fb0dbaaf90951e071c92d565.png)

<center>连接、主题与会话数量</center>

 <br>

![The Rate of Sent and Received Messages, the Number of Retained/Delayed/Dropped Messages](https://assets.emqx.com/images/4be20e313d51ed7477d6117fa3c05b13.png)

<center>消息收发速率、保留消息/延迟消息以及丢弃消息数量</center>

<br> 

![Client Event](https://assets.emqx.com/images/affbe7832fe71e29334c3e915c7744bc.png)

<center>客户端事件</center>

## 下一步

Datadog 的 EMQX 集成内置的图表仅展示了部分关键的指标，您还可以查阅[此文档](https://docs.datadoghq.com/integrations/emqx/#metrics)，获取 EMQX 所有上报的指标，并基于此构建自己的监控图表。

接下来，您可以基于这些指标在 Datadog 上配置告警规则，以便在某些指标达到预设的阈值或发生异常情况时，通过 Datadog 发送通知及时提醒您采取必要的行动，从而最大限度地减少系统故障对业务的影响。

## 结语

本文展示了如何将 EMQX 与 Datadog 无缝集成来实时监测 EMQX 的运行状态。通过 EMQX 完善的指标和 Datadog 的强大功能，用户可以时刻了解 EMQX 的运行状况，包括连接数、消息速率、节点状态等关键指标，以便及时发现潜在的问题并采取相应的措施，从而保证系统的稳定性和可靠性。期待本文能为使用 Datadog 监控 EMQX 的用户提供一些有用的指导和参考。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
