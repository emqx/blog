## 前言

[工业物联网（IIoT）](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)正引领着一场数字化革命，重新定义着数据的采集、分析和利用方式。工业物联网这个由数亿设备构成的庞大网络中，实时数据流动是实现工业自动化、数字化和高效生产的关键。EMQX Cloud，跨多云全托管的 MQTT 云服务平台，是这场革命的关键基础设施软件，提供从边缘到云的无缝连接，保证数据的实时传输、处理和分析。

本文将深入探讨 EMQX Cloud 如何整合边缘计算的数据与 TimescaleDB 的数据洞察能力，为工业物联网提供关键数据基础服务。

## 1. EMQX Cloud 与其在 IIoT 中的位置

### **EMQX Cloud**

[EMQX Cloud](https://www.emqx.com/zh/cloud) 是一款专门设计用于处理大规模 IIoT 数据流的云端 MQTT 代理服务。它提供了可靠的消息传递和设备管理功能，以满足工业物联网领域的需求。该平台的核心功能包括高性能的 MQTT 消息代理、设备连接管理、数据路由、消息存储和实时监控。

### **在 IIoT 中的位置**

在工业物联网中，处理大数据量和设备管理是至关重要的，因为涉及到大量的传感器和设备，需要实时的数据传输、存储和监控。这些设备通常散布在广泛的区域，需要高度可靠的连接，以确保生产效率、质量控制和设备状态的实时监测。此外，数据的安全性也是一个不可忽视的因素，因为工业设备和传感器的数据通常包含敏感信息。

**挑战与解决方案**

1. **大数据量处理挑战：** IIoT 环境中，设备生成的数据量庞大，需要高性能的消息传递和数据路由。EMQX Cloud 通过其高性能 MQTT 消息代理和数据路由功能，能够有效地处理大规模的数据流，确保数据的实时传输和处理。
2. **设备管理挑战：** 管理大量设备的连接、状态和固件更新是挑战性的。EMQX Cloud 提供了强大的设备连接管理功能，允许实时监控设备的在线状态，支持设备的热更新和远程管理。
3. **可扩展性和可靠性挑战：** 随着设备数量的增加，系统的可扩展性和可靠性变得至关重要。EMQX Cloud 通过其云端部署和负载均衡技术，能够实现高度可扩展的架构，确保系统的可用性和稳定性。
4. **安全性挑战：** IIoT 数据的安全性至关重要，因为它可能包含敏感的工业信息。EMQX Cloud 通过支持TLS/SSL 加密和身份验证，提供了强大的数据安全保护，确保数据在传输和存储过程中的机密性。

总之，EMQX Cloud 在 IIoT 中扮演着关键角色，帮助解决了处理大数据量和设备管理等挑战。它通过其可扩展性、可靠性和安全性功能，为工业物联网环境提供了可靠的消息传递和设备管理解决方案。

## 2. 从 NanoMQ 到 EMQX Cloud 到 TimescaleDB

本文将演示在树莓派上部署 NanoMQ，并进一步将数据桥接到 EMQX Cloud，最后通过数据集成实现数据传输至 TimescaleDB。我们将执行以下三个主要任务：

**任务一：树莓派上安装 NanoMQ**

首先，我们会逐步说明如何在树莓派上安装和配置 NanoMQ。这是连接设备和 EMQX Cloud 的第一步，确保一切就绪。

**任务二：NanoMQ 数据桥接至 EMQX Cloud**

任务二涉及将树莓派上的 NanoMQ 与 EMQX Cloud 进行有效的数据桥接。我们将提供详细的指南，以确保连接正确设置。

**任务三：EMQX Cloud 数据桥接至 TimescaleDB**

最后，我们将讨论如何设置 EMQX Cloud 以桥接数据至 TimescaleDB。这将帮助您实现完整的数据流传输。

通过完成这三个任务，您将成功地在树莓派上部署 NanoMQ 并实现数据集成，将数据无缝传递至 TimescaleDB。

## 3. 部署边缘计算解决方案：NanoMQ 的设置

在部署边缘计算解决方案时，选择适当的工具和组件至关重要。NanoMQ 作为边缘 MQTT 代理的选择有其独特的优势。以下是一些关于为什么选择 NanoMQ 以及如何进行安装和验证的详细说明。

### **选择 NanoMQ 作为边缘 MQTT 代理的原因**

[NanoMQ](https://nanomq.io/zh) 是一款轻量级、高性能的 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 代理，特别适用于边缘计算场景。以下是选择 NanoMQ 的一些理由：

1. **轻量级和资源友好：** NanoMQ 被精心设计，以便在资源有限的边缘设备上运行，几乎不会对设备性能造成明显影响。
2. **支持 MQTT 5.0：** 它支持 MQTT 5.0 协议，提供了更多的功能和更好的性能，使您能够处理更复杂的通信需求。
3. **快速部署：** NanoMQ 提供了简化的部署过程，使您能够快速配置和启动 MQTT 代理，减少了部署和配置的复杂性。
4. **可靠性和稳定性：**NanoMQ 被广泛测试和验证，具有出色的稳定性和可靠性，确保在边缘环境中的持续运行。

### **在边缘设备上安装和配置 NanoMQ 的步骤**

1. **下载 NanoMQ：** 访问 EMQ 官方网站，下载适用于您的边缘设备的 NanoMQ 版本。

2. **安装 NanoMQ：** 根据设备的操作系统，执行 NanoMQ 安装程序。通常，这包括解压下载的文件并运行安装脚本。在本示例中，我们将使用 Apt 源在树莓派安装 NanoMQ。

   ```
   ## Download the repository
   curl -s https://assets.emqx.com/scripts/install-nanomq-deb.sh | sudo bash
   
   ## Install NanoMQ
   sudo apt-get install nanomq
   ```

1. **配置 NanoMQ：** 配置 NanoMQ 桥接需修改默认路径下的配置文件 /etc/NanoMQ_bridge.conf，在配置文件中，您可以指定 MQTT 代理的参数，如监听端口、认证设置和其他选项，实现将接收到的指定 topic 的数据转发到到 EMQX Cloud。

   配置参数如下：

   - 远端 broker 地址
   - MQTT 协议版本
   - 客户标识符 (默认缺省由 NanoMQ 自动分配)
   - 会话清除
   - Keep Alive
   - 用户名
   - 密码
   - 转发Topic (多个 topic 用逗号隔开)
   -  qos 等级
   - 客户端并行数

   本示例中配置文件 /etc/nanomq_bridge.conf。

   ```
   bridges.mqtt.name {
     server = "mqtt-tcp://x.x.x.x:1883"
     proto_ver = 4
     username = xxx
     password = xxx
     clean_start = true
     keepalive = 60s
     forwards = [
       {
         remote_topic = "emqx/test"
         local_topic = "emqx/test"
         qos = 0
       }
     ]
     max_parallel_processes = 2
     max_send_queue_len = 1024
     max_recv_queue_len = 1024
   }
   
   ```

1. **启动 NanoMQ：** 使用启动脚本或命令启动 NanoMQ。一旦启动，NanoMQ 将开始监听指定的端口并准备接受 MQTT 连接。

   ```
   nanomq start --conf /etc/nanomq_bridge.conf
   ```

   ![Start NanoMQ](https://assets.emqx.com/images/ec38d78a50dd4b984442814775694ed5.png)

### **验证 NanoMQ 的安装和功能**

要验证 NanoMQ 的安装和功能，可以执行以下操作：

1. **连接到 NanoMQ：** 使用 MQTT 客户端工具，如 MQTTX 或者 mosquitto_sub/mosquitto_pub，连接到 NanoMQ。

   ![Connect to NanoMQ](https://assets.emqx.com/images/65e801bffae9143af49a745c87fbc824.png)

2. **发布和订阅消息：** 发布一条消息并确保它可以被成功传递给订阅者。这可以验证代理的消息传递功能。

   ![Publish and Subscribe to Messages](https://assets.emqx.com/images/1393ca4be29f1862c6c0bb06cb81f5f4.png)

3. **监控和日志：** 查看 NanoMQ 的日志文件以确保没有错误或异常情况。这有助于确保代理正常工作。

4. **性能测试：** 可以使用性能测试工具来模拟高负载条件，以确保 NanoMQ 在边缘设备上具有良好的性能。

一旦您成功验证了 NanoMQ 的安装和功能，您就可以在边缘计算解决方案中信任它作为 MQTT 代理，以支持您的 IoT 通信需求。

## 4. 实现 EMQX Cloud 与边缘设备的无缝连接

为了实现 EMQX Cloud 与边缘设备之间的无缝连接，我们需要遵循以下步骤来配置边缘设备以连接到 EMQX Cloud，并确保数据传输的安全性。

### 配置边缘设备连接到 EMQX Cloud

1. **获取 SSL/TLS 证书（可选）：** 首先，确保你在 EMQX Cloud 上获得了有效的 SSL/TLS 证书。这些证书用于加密通信以确保数据传输的安全性。

2. **配置设备参数并建立连接：** 在边缘设备上，使用配置好的参数，边缘设备尝试连接到 EMQX Cloud 服务器。

   ![Configure Device Parameters and Establish Connection](https://assets.emqx.com/images/cfe8d45d6f03468fa705d868b86f9c07.png)

3. **发布和订阅测试**

   使用 MQTTX 连接到 EMQX Cloud，订阅主题 "temp_hum/emqx" ，查看是否收到来自 nanomq 的消息。

   ![Publish and Subscribe Testing](https://assets.emqx.com/images/5af5fbea88a0ab7d64ee9331a21b7dbd.png)

总之，配置边缘设备与 EMQX Cloud 的连接需要经过详细的设置，测试连接通过发布和订阅 MQTT 主题可帮助验证连接的可行性。这一过程为实现 EMQX Cloud 与边缘设备的无缝连接奠定了基础。

## 5. TimescaleDB 的整合：配置、数据转换和持久化

### 选择 TimescaleDB 作为时间序列数据库的原因

在这个任务中，我们将深入数据分析，使用 TimescaleDB 来获得关于 IIoT（工业物联网）数据的洞察。我们将讨论 TimescaleDB 查询语言的特点，如何提取数据，创建简单的仪表板以实时监控数据，以及如何进行测试以验证数据的准确性和实时性。

1. **专注于时间序列数据**：TimescaleDB 是一种专门设计用于处理时间序列数据的数据库系统。在工业物联网中，大量的数据是按时间戳记录的，例如传感器数据、事件日志等。因此，选择一个专注于时间序列数据的数据库系统，可以提供更高效的数据存储和查询。
2. **水平可扩展性**：工业物联网环境中，数据量可能会迅速增长。TimescaleDB 支持水平可扩展性，允许轻松地扩展存储容量，以适应不断增长的数据需求。这保证了系统在处理大规模时间序列数据时的性能和可靠性。
3. **复杂查询支持**：TimescaleDB 具有强大的查询功能，允许执行复杂的分析操作，如数据聚合、滑动时间窗口分析、时间序列插值等。这对于工业物联网应用中的数据分析和预测非常重要。
4. **数据保留策略**：工业物联网中的数据通常需要根据特定的保留策略来管理，以节省存储空间和维护成本。TimescaleDB提供了数据自动分区和数据过期策略，可以根据需求自动删除旧数据，同时保留必要的历史数据。
5. **与 EMQX Cloud 的集成**：由于 EMQX Cloud 与 TimescaleDB 的紧密集成，数据从边缘设备传输到数据库的流程更为顺畅，这有助于确保数据的实时性和完整性。
6. **社区支持和生态系统**：TimescaleDB是一个开源项目，拥有庞大的社区支持，因此可以从社区贡献的丰富功能和扩展中受益。此外，与其他工具和框架的整合也相对容易，构建更强大的数据分析和可视化工具。

总之，选择 TimescaleDB 作为时间序列数据库的原因包括其专门面向时间序列数据的特性、可扩展性、强大的查询支持、数据管理策略以及与EMQX Cloud的协同工作，使其成为处理工业物联网数据的理想选择。

### **创建** TimescaleDB Cloud **实例** 

登录 [Timescale Cloud](https://www.timescale.com/?utm_source=timescaledb-paid&utm_medium=google-search&utm_campaign=brand-2022&utm_content=homepage&utm_term=timescaledb&utm_term=timescaledb&utm_campaign=[Growth]+Brand&utm_source=adwords&utm_medium=ppc&hsa_acc=9017398448&hsa_cam=17990015160&hsa_grp=141555979882&hsa_ad=651034365787&hsa_src=g&hsa_tgt=kwd-387856548428&hsa_kw=timescaledb&hsa_mt=b&hsa_net=adwords&hsa_ver=3&gad_source=1&gclid=CjwKCAjws9ipBhB1EiwAccEi1Anq99FB2ubEmpP9mxYyEHughcnB3xCmwVnY38SU9PI5U7V9qEJ6yhoCyQoQAvD_BwE)，前往创建服务页面。

![Login to Timescale Cloud](https://assets.emqx.com/images/cf060c589fa325867db0fa73c98596c8.png)

在创建服务页面，从地域字段的下拉列表中选择地域。 单击页面底部的创建服务。

![Create Service page](https://assets.emqx.com/images/c8e0cd1e3e6a75049325bbfebf2a3601.png)

创建服务后，您可以按照此页面上的说明连接到您的服务。 或者，您可以按照以下步骤连接到您的服务。 妥善保存您的用户名和密码。

![service is created](https://assets.emqx.com/images/b713f484dea04da82afd304b5bbdcbff.png)

使用以下 SQL 语句创建新表 temp_hum 。 该表将用于保存设备上报的温度和湿度数据。

```
CREATE TABLE temp_hum (
up_timestamp TIMESTAMPTZ NOT NULL,
client_id TEXT NOT NULL,
temp DOUBLE PRECISION NULL,
hum DOUBLE PRECISION NULL
);
```

![CREATE TABLE](https://assets.emqx.com/images/eca566fd919823e387623ed570a287fd.png)

插入测试数据并查看。

```
INSERT INTO temp_hum(up_timestamp, client_id, temp, hum) values (to_timestamp(1603963414), 'temp_hum-001', 19.1, 55);
SELECT * FROM temp_hum;
```

![Insert test data](https://assets.emqx.com/images/27373a1516af6804642aaa6d402c4565.png)

连接到服务后，您可以转至服务概览页面，在该页面您可以看到您的连接信息。

![服务概览页面](https://assets.emqx.com/images/5768bb9f9f04d9b12f9efcec4cea4b40.png)

### 在 EMQX Cloud 中设置 TimeScale 集成

**1. 开通 NAT 网关**

[NAT 网关](https://docs.emqx.com/zh/cloud/latest/vas/nat-gateway.html) 为 EMQX Cloud 专业版的部署提供访问公网资源的能力，无需 VPC 对等连接。在连接 TimeScale 前，请先开通 NAT 网关。

![Enable NAT Gateway](https://assets.emqx.com/images/064abf5509b91e875c669cb61aa8b11d.png)

**2.新建资源**

点击左侧菜单栏`数据集成`，找到 TimescaleDB 资源类型。

![Create resources](https://assets.emqx.com/images/5f2c1ffa92bf84906447f54bcdb0b2af.png)

填入刚才创建好的  TimescaleDB 数据库信息，将连接池大小设置为 1，单击测试以测试连接。

- 如果连接失败，需要检查数据库配置是否正确。
- 如果连接成功，单击“新建”，创建 TimescaleDB 资源。

![Create resources](https://assets.emqx.com/images/b14b2ae65629ebda608102eeadf75337.png)

**3.创建规则**

在“配置的资源”下，选择 TimescaleDB 资源。 单击“新建规则”，输入以下规则来匹配 SQL 语句。 规则的 SELECT 部分包括以下字段：

- up_timestamp：消息上报的实时时间。
- 客户端ID：发送消息的设备的ID。
- Payload：temp_hum/emqx 主题消息的负载，包含温度和湿度数据。

```
SELECT
timestamp div 1000 AS up_timestamp, clientid AS client_id, payload.temp AS temp, payload.hum AS hum
FROM
"temp_hum/emqx"
```

![New rule](https://assets.emqx.com/images/5db0635e76b38a156a7b4266ef007373.png)

启用 SQL 测试，填写必填字段并单击 “SQL 测试” 以测试规则是否有效，您应该得到如截图所示的预期结果。

![Enable SQL Testing](https://assets.emqx.com/images/9e80ddbd6d6e4f48265cc9aec8200c79.png)

**4. 创建动作**

单击底部的 “下一步” 按钮以创建操作。 从下拉列表中选择之前创建的资源。 在 SQL 模板中，输入以下数据以将它们插入到 SQL 模板中。

```
INSERT INTO temp_hum(up_timestamp, client_id, temp, hum) VALUES (to_timestamp(${up_timestamp}), ${client_id}, ${temp}, ${hum})
```

![Create Actions](https://assets.emqx.com/images/9f6c255a9d640a4d9ed143c2cf2eddb1.png)

确认信息无误后，点击右下角的确认，完成数据集成的配置。通过这些步骤，您可以成功配置 TimescaleDB 集成，将 MQTT 数据转化为适合时间序列数据库的结构，并验证数据的正确传输和存储。这将使您能够轻松地对时间序列数据进行分析和查询。

## 6. 深入数据分析：使用 TimescaleDB 洞察数据

一旦数据已经成功集成到 TimescaleDB 中，下一步是通过查询和可视化工具来深入分析数据，获得有关工业物联网（IIoT）系统的洞察。以下是关于如何使用 TimescaleDB 进行数据分析的一些关键方面。

### TimescaleDB 查询语言的特点

TimescaleDB的查询语言扩展了标准SQL，以支持时间序列数据的特点。这包括时间窗口查询、数据插值、数据降采样和复杂的时间序列操作。以下是一些主要特点：

- **时间窗口查询**：您可以使用时间窗口函数来执行基于时间的操作，如滑动时间窗口聚合。这对于分析数据在不同时间段内的变化非常有用，比如每小时、每天或每月的数据趋势分析。
- **数据插值**：TimescaleDB 支持插值函数，允许您填充缺失的时间序列数据点。这对于处理不完整的数据集并生成平滑的曲线图表非常有帮助。
- **数据降采样**：如果您的原始数据非常细粒度，您可以使用降采样来减少数据量，以便更轻松地可视化和分析。降采样可以将数据汇总成更大的时间间隔。
- **复杂时间序列操作**：TimescaleDB 支持各种复杂的时间序列操作，如交叉连接时间序列、对时间序列进行数学计算和应用窗口函数等。这些操作使您能够执行更高级的分析任务。

### 使用简单的仪表板实时监控指标

仪表板是将分析结果可视化的一种强大方式，通过仪表板，您可以：

- **实时监控关键指标**：将重要的指标和数据趋势显示在仪表板上，以便工程师和运营人员能够随时了解系统的性能。

  ![Monitor Key Metrics in Real-Time](https://assets.emqx.com/images/a7662c5f91142a9e8e8328f7a299503a.png)

- **可视化数据**：使用图表、图形和地图等可视化工具将数据转化为易于理解的图像，以便更轻松地识别趋势和异常。

  ![Visualize Data](https://assets.emqx.com/images/09c7a52957e5adfcc0248b722cbe6a69.png)

- **自定义仪表板**：根据具体需求创建自定义仪表板，以确保关注的数据和指标得到突出显示。

  ![Customize Dashboards](https://assets.emqx.com/images/0b736170764f2b898ceaf84e74688151.png)

### 测试并验证数据的准确性和实时性

数据分析不仅包括了查询和可视化，还包括验证数据的准确性和实时性。这是确保 IIoT 系统正常运行的关键部分。为了测试和验证数据，您可以：

- **比对原始数据**：将查询结果与原始数据进行比对，以确保转换和存储过程未引入任何错误。

  ```
  SELECT * FROM temp_hum ORDER BY up_timestamp DESC LIMIT 10;
  ```

  ![Compare with Original Data](https://assets.emqx.com/images/8ac19c931740f8b57baaa11bc6b43641.png)

- **监控数据更新频率**：检查数据是否按照预期的频率更新。如果数据更新延迟，可能需要进行性能优化或故障排除。
- **定期进行数据验证**：建立自动化的数据验证流程，以确保数据一直保持准确性。这包括编写测试脚本来验证数据完整性。

通过深入的数据分析、仪表板监控和数据验证，您可以获得关于 IIoT 系统性能和运行状况的宝贵洞察，帮助您做出及时的决策和改进系统。 TimescaleDB 的灵活性和强大功能使其成为处理大规模时间序列数据的理想选择。

## 结语

工业数字化需要一个能够处理复杂数据流、确保安全、并提供深度洞察的平台。EMQX Cloud 不仅满足了这些需求，还通过其与 MQTT 和 TimescaleDB 的密切集成，推动了工业物联网的创新。这种集成确保了从设备到数据库的无缝数据流，无论数据量多大、需求复杂。通过实践验证，EMQX Cloud 证明了其在各种情况下都能保持高性能和可靠性，是构建和扩展工业物联网解决方案的理想选择。





<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
