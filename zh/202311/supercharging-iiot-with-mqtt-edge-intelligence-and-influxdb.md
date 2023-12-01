## 前言

[工业物联网](https://www.emqx.com/zh/blog/iiot-explained-examples-technologies-benefits-and-challenges)的发展，需要一个能够处理复杂数据流、确保安全、并提供数据洞察的平台。跨多云的全托管 MQTT 云服务平台 EMQX Cloud 可以提供工业数字化转型中所需要的复杂数据服务。EMQX Cloud 提供从边缘到云的无缝连接，保证数据的实时传输、处理和分析。本文将探讨 EMQX Cloud 如何整合边缘计算的智能和 InfluxDB 的分析能力，为工业物联网新的提供数据驱动型业务模式。

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

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>

## **2. 从 NanoMQ 到 EMQX Cloud 到 InfluxDB** 

本文将演示如何在树莓派上部署 NanoMQ，并进一步将数据桥接到 EMQX Cloud，最后通过数据集成实现数据传输至 InfluxDB 3.0 为例，我们将执行以下三个主要任务：

**任务一：树莓派上安装 NanoMQ**

首先，我们会逐步说明如何在树莓派上安装和配置 NanoMQ。这是连接设备和 EMQX Cloud 的第一步，确保一切就绪。

**任务二：NanoMQ 数据桥接至 EMQX Cloud**

任务二涉及将树莓派上的 NanoMQ 与 EMQX Cloud 进行有效的数据桥接。我们将提供详细的指南，以确保连接正确设置。

**任务三：EMQX Cloud 数据桥接至 InfluxDB 3.0**

最后，我们将讨论如何设置 EMQX Cloud 以桥接数据至 InfluxDB 3.0。这将帮助您实现完整的数据流传输。

通过完成这三个任务，您将成功地在树莓派上部署 NanoMQ 并实现数据集成，将数据无缝传递至 InfluxDB 3.0。

## **3. 选择 NanoMQ 作为边缘 MQTT 代理的原因**

在部署边缘计算解决方案时，选择适当的工具和组件至关重要。NanoMQ 作为边缘 MQTT 代理的选择有其独特的优势。以下是一些关于为什么选择 NanoMQ 以及如何进行安装和验证的详细说明。

[NanoMQ](https://nanomq.io/zh) 是一款轻量级、高性能的 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 代理，特别适用于边缘计算场景。以下是选择 NanoMQ 的一些理由：

1. **轻量级和资源友好：** NanoMQ 被精心设计，以便在资源有限的边缘设备上运行，几乎不会对设备性能造成明显影响。
2. **支持 MQTT 5.0：** 它支持 MQTT 5.0 协议，提供了更多的功能和更好的性能，使您能够处理更复杂的通信需求。
3. **快速部署：** NanoMQ 提供了简化的部署过程，使您能够快速配置和启动 MQTT 代理，减少了部署和配置的复杂性。
4. **可靠性和稳定性：**NanoMQ 被广泛测试和验证，具有出色的稳定性和可靠性，确保在边缘环境中的持续运行。

### **在边缘设备上安装和配置 NanoMQ 的步骤**

1. **下载 NanoMQ：** 访问 EMQ 官方网站（[https://www.emqx.com/zh/try?product=neuron](https://www.emqx.com/zh/try?product=neuron)），下载适用于您的边缘设备的 NanoMQ 版本。

2. **安装 NanoMQ：** 根据设备的操作系统，执行 NanoMQ 安装程序。通常，这包括解压下载的文件并运行安装脚本。在本示例中，我们将使用 Apt 源在树莓派安装 NanoMQ。

   ```
   ## 下载仓库
   curl -s https://assets.emqx.com/scripts/install-nanomq-deb.sh | sudo bash
   
   ## 安装 NanoMQ
   sudo apt-get install nanomq
   ```

1. **配置 NanoMQ：** 配置 NanoMQ 桥接需修改默认路径下的配置文件 /etc/NanoMQ_bridge.conf，在配置文件中，您可以指定 MQTT 代理的参数，如监听端口、认证设置和其他选项，实现将接收到的指定 topic 的数据转发到到 EMQX Cloud。

   配置参数如下：

   - 远端 broker 地址
   - MQTT协议版本
   - 客户标识符 (默认缺省由 NanoMQ 自动分配)
   - 会话清除
   - Keep Alive
   - 用户名
   - 密码
   - 转发Topic (多个 topic 用逗号隔开)
   -  qos 等级
   - 客户端并行数

   本示例中配置文件 nanomq_bridge.conf。

   ```
   bridges.mqtt.name {
    ## TCP URL 格式:  mqtt-tcp://host:port
    ## TLS URL 格式:  tls+mqtt-tcp://host:port
    ## QUIC URL 格式: mqtt-quic://host:port
    server = "mqtt-tcp://x.x.x.x:1883"
    ## MQTT 协议版本 （ 4 ｜ 5 ）
    proto_ver = 4
    username = xxx
    password = xxx
    clean_start = true
    keepalive = 60s
    ## 如果通过 TLS 桥接将下面的代码取消注释
    ## ssl {
    ##  keyfile = "/etc/certs/key.pem"
    ##  certfile = "/etc/certs/cert.pem"
    ##  cacertfile = "/etc/certs/cacert.pem"
    ## }
    forwards = [
     {
      remote_topic = "emqx/test"
      local_topic = "emqx/test"
      qos = 0
     } ]
    max_parallel_processes = 2
    max_send_queue_len = 1024
    max_recv_queue_len = 1024
   }
   ```

1. **启动 NanoMQ：** 使用启动脚本或命令启动 NanoMQ。一旦启动，NanoMQ 将开始监听指定的端口并准备接受 MQTT 连接。

   ```
   nanomq start --conf /etc/nanomq_bridge.conf
   ```

   ![nanomq start](https://assets.emqx.com/images/3753b2f29ab0d32d512442b49310b02f.png)



### **验证 NanoMQ 的安装和功能**

要验证 NanoMQ 的安装和功能，可以执行以下操作：

1. **连接到 NanoMQ：** 使用 [MQTT 客户端工具](https://www.emqx.com/zh/blog/mqtt-client-tools)，如 [MQTTX](https://mqttx.app/zh) 或者 mosquitto_sub/mosquitto_pub，连接到 NanoMQ。

   ![**Connect to NanoMQ**](https://assets.emqx.com/images/0e3c186de5d1e75d767772994bf3d8ee.png)

1. **发布和订阅消息：** 发布一条消息并确保它可以被成功传递给订阅者。这可以验证代理的消息传递功能。

   ![Publish and Subscribe to Messages](https://assets.emqx.com/images/084277ddcbe19c07a310e154e07aeba5.png)

1. **监控和日志：** 查看 NanoMQ 的日志文件以确保没有错误或异常情况。这有助于确保代理正常工作。
2. **性能测试：** 可以使用性能测试工具来模拟高负载条件，以确保 NanoMQ 在边缘设备上具有良好的性能。

一旦您成功验证了 NanoMQ 的安装和功能，您就可以在边缘计算解决方案中信任它作为 MQTT 代理，以支持您的 IoT 通信需求。

## 4. 实现 EMQX Cloud 与边缘设备的无缝连接

为了实现 EMQX Cloud 与边缘设备之间的无缝连接，我们需要遵循以下步骤来配置边缘设备以连接到 EMQX Cloud，并确保数据传输的安全性。

### 配置边缘设备连接到 EMQX Cloud

1. **获取 SSL/TLS 证书（可选）：** 首先，确保你在 EMQX Cloud 上获得了有效的 SSL/TLS 证书。这些证书用于加密通信以确保数据传输的安全性。

2. **配置设备参数并建立连接：** 在边缘设备上，使用配置好的参数，边缘设备尝试连接到 EMQX Cloud 服务器。

   ![Configure Device Parameters and Establish Connection](https://assets.emqx.com/images/39d624c7a0310f61a732e7f0260f40d9.png)

3. **发布和订阅测试**：使用 MQTTX 连接到 EMQX Cloud，订阅主题 "emqx/test" ，查看是否收到来自 nanomq 的消息。

   ![Publish and Subscribe Testing](https://assets.emqx.com/images/f6aefc6a7aa15444e66fc4e617091224.png)

总之，配置边缘设备与 EMQX Cloud 的连接需要经过详细的设置，测试连接通过发布和订阅 MQTT 主题可帮助验证连接的可行性。这一过程为实现 EMQX Cloud 与边缘设备的无缝连接奠定了基础。

## 5. 整合 InfluxDB：配置、数据转换和持久化

### **选择 InfluxDB 作为时间序列数据库的原因**

InfluxDB 是一种高性能的时间序列数据库，它特别适用于存储和查询时间相关的数据，如传感器数据、监控指标、日志等。选择 InfluxDB 作为时间序列数据库的原因通常包括以下几点：

1. **性能和扩展性**：InfluxDB 经过优化，可以高效地处理大量时间序列数据。它支持水平扩展，使其能够应对不断增长的数据负载。
2. **数据模型**：InfluxDB的数据模型非常适合时间序列数据，它使用测量（Measurements）、标签（Tags）和字段（Fields）的结构，使数据存储和查询变得非常灵活。
3. **查询语言**：InfluxDB提供了强大的查询语言，如 InfluxQL 和Flux，用于执行复杂的时间序列数据分析和聚合操作。
4. **社区支持**：InfluxDB 有一个活跃的社区，提供了大量的文档、插件和工具，使其在各种应用场景中更易于使用。
5. **集成支持**：InfluxDB 支持各种集成方式，使其可以轻松与其他系统和应用程序集成，包括与 EMQX Cloud。

### **创建 InfluxDB Cloud Serverless 实例**

要在 EMQX Cloud 中设置 InfluxDB 集成，您可以按照以下步骤进行：

1. **登录控制台**

   首先，使用 InfluxDB Cloud 账户登录到 InfluxDB Cloud Serverless 控制台界面。

   ![Log in to the InfluxDB Cloud Serverless](https://assets.emqx.com/images/f44332d0238ca39f0aa39be18d39b73b.png)

1. **创建 bucket**

   登录到控制台后，进入 "Load Data" 页面并创建一个名为 "emqx" 的 bucket。

   ![Create a Bucket](https://assets.emqx.com/images/ca3d43e0ac57b021a39553259490c235.png)

1. **生成令牌**

   回到 "Load Data" 页面，点击 "Generate API TOKENS" 生成一个新的令牌。此时我们将生成一个具有全部权限的令牌。一旦令牌被创建，你可以自行选择激活/停用令牌。

   ![Generate an API Token](https://assets.emqx.com/images/6d48057aee8e40d00dfd171390221497.png)

### 在 EMQX Cloud 中设置 InfluxDB 集成

1. **开通 NAT 网关**

   [NAT 网关](https://docs.emqx.com/zh/cloud/latest/vas/nat-gateway.html) 为 EMQX Cloud 专业版的部署提供访问公网资源的能力，无需 VPC 对等连接。在连接 InfluxDB 前，请先开通 NAT 网关。

   ![Set up NAT Gateway](https://assets.emqx.com/images/b9a8b85008662953c821476cb64b07e9.png)

2. **新建资源**

   进入 [EMQX Cloud 控制台](https://emqx.atlassian.net/wiki/spaces/EXC/pages/622657578/InfluxDB+3.0#)，打开数据集成页面并选择 InfluxDB HTTP V2 服务。

   ![Access the EMQX Cloud console](https://assets.emqx.com/images/06923956a7cbdaea916fbd8a78152841.png)

   进入新建资源页面，依次填写配置项，请注意端口为 443，启用 HTTPS。

   ![Enter the configuration details ](https://assets.emqx.com/images/b33969b3bb37b87203511764ee23e3aa.png)

   配置完成后点击测试连接，确认资源可用后点击新建，如果资源初始化失败，请检查所填配置项是否无误。

3. **创建规则**
   资源创建成功后，回到数据集成页面，找到新创建的资源，并点击创建规则。

   ![创建规则](https://assets.emqx.com/images/9c20c4fb8da76cca9ff0de4edfe2f270.png)

   我们的目标是：只要 "emqx/test"主题有监控信息时，就会触发引擎。这里需要对 SQL 进行一定的处理：

   - 仅针对主题 "emqx/test"
   - 获取我们需要的三个数据 location、temperature、humidity

   根据上面的原则，我们最后得到的 SQL 应该如下：

   ```
   SELECT
       payload.location as location,
       payload.temp as temp,
       payload.hum as hum
   FROM "emqx/test"
   
   ```

   ![New rule](https://assets.emqx.com/images/9dbf31c9f9a4f8acb029765df275b740.png)

   这个 SQL 可以解读为：当 "emqx/test" 主题收到消息时，选取信息里的 location、data.temperature、data.humidity 三个字段。

   接下来，您可以点击 SQL 输入框下的 SQL 测试 ，填写以下数据：

   - topic: emqx/test
   - payload:

   ```
   {
   "location": "Prague",
   "temp": 26,
   "hum": 46.4
   }
   ```

   点击 SQL 测试，查看输出的数据结果，如果设置无误，测试输出框应该得到完整的 JSON 数据，如下：

   ![Click "SQL Test](https://assets.emqx.com/images/3427b77af9cb833bc8857c6946d0b4d4.png)

4. **创建动作**

   点击下一步，在新建动作页中，默认动作类型为保存数据到 InfluxDB，选择刚才创建的资源。

   其他字段可以参照下表。

| **参数**      | **必填** | **类型** | **意义**                                        |
| ------------- | -------- | -------- | ----------------------------------------------- |
| Measurement   | 是       | str      | 指定写入到 InfluxDB 的 measurement              |
| Fields        | 是       | str      | 指定写入到 InfluxDB 的 fields 的值从哪里获取    |
| Tags          | 否       | str      | 指定写入到 InfluxDB 的 tags 的值从哪里获取      |
| Timestamp Key | 否       | str      | 指定写入到 InfluxDB 的 timestamp 的值从哪里获取 |

针对我们的情况，这部分可以这样填写：

- Measurement 可以随意设置，我们这里填写 "temp_hum"
- Field Keys 填写我们需要记录的两个数据："temp" 和 "hum"
- Tag Keys 这里我们设置成 "location"
- Timestamp Key 默认为空

![Create an Action](https://assets.emqx.com/images/dca45f76f92356095909a00b3cd80bb2.png)

确认信息无误后，点击右下角的确认，完成数据集成的配置。通过这些步骤，您可以成功配置 InfluxDB 集成，将 MQTT 数据转化为适合时间序列数据库的结构，并验证数据的正确传输和存储。这将使您能够轻松地对时间序列数据进行分析和查询。

## 6. 深入数据分析：使用 InfluxDB 洞察数据

在这个任务中，我们将深入数据分析，使用 InfluxDB 来获得关于IIoT（工业物联网）数据的洞察。我们将讨论 InfluxDB 查询语言的特点，如何提取数据，创建简单的仪表板以实时监控数据，以及如何进行测试以验证数据的准确性和实时性。

### **InfluxDB 查询语言的特点**

InfluxDB 是一个开源的时间序列数据库，专门用于存储和查询时间相关的数据。其查询语言具有以下特点：

- **时间序列重点**：InfluxQL专注于时间序列数据，这使得它非常适用于处理实时和历史数据。您可以执行各种操作，如数据聚合、筛选、切片和分组，以提取有关时间序列的信息。
- **SQL风格的语法**：如果您熟悉SQL，学习InfluxQL会相对容易。它采用类似于SQL的语法，使得查询数据变得更加直观和容易。
- **内置函数**：InfluxQL提供了许多内置函数，用于执行数据处理操作，如平均值计算、求和、最小值和最大值查找。这些函数可以帮助您提取关键的数据统计信息。

### 创建简单的实时监控仪表板

实时监控是工业物联网的一个重要应用场景。您可以使用 InfluxDB 和相关工具来创建简单而强大的仪表板，以实时监控 IIoT 数据。

#### 步骤：

**1.数据源设置**

通过使用 InfluxDB 查询语言，您可以提取有关 IIoT 数据的洞察。例如，您可以执行以下查询来获取关于某个传感器的数据统计信息，这个 SQL 将返回最近 1 小时内工厂位置传感器温湿度，并按时间间隔进行分组。

```
SELECT *
FROM "temp_hum"
WHERE
time >= now() - interval '1 hour'
AND
("hum" IS NOT NULL OR "temp" IS NOT NULL)
AND
"location" = 'Prague'
```

**2.数据可视化**

您可以设置仪表板来显示温度、湿度、压力等数据，随着时间的推移以图表或仪表盘的形式展示。这有助于实时监控设备和过程状态。

![Data Visualization 1](https://assets.emqx.com/images/170c7d91ecb5fc6fbf71a6da8a14d8a0.png)

![Data Visualization 2](https://assets.emqx.com/images/8ca11d422cfd449f46c005c1de6bd6f7.png)

![Data Visualization 3](https://assets.emqx.com/images/e4d42dfe1b3cc5f3f030950437c3f692.png) 

**3.实时监控配置**

您也可以考虑设置实时监控模块，以定期查询 InfluxDB，并将最新数据显示在仪表板上。这可帮助您实时跟踪 IIoT 设备的状态和性能。

### **测试数据准确性和实时性**

为了验证数据的准确性和实时性，您可以执行以下操作：

1. **对比数据源**：将 InfluxDB 中的数据与原始数据源进行比较，确保它们一致。
2. **创建测试用例**：编写测试用例来模拟不同条件下的数据输入，并检查系统是否以正确的方式响应。
3. **实时性测试**：监视数据的时间戳，确保数据被及时传输和存储。
4. **数据质量监控**：使用仪表板来监控数据的异常值或缺失，以及数据的完整性。

通过深入数据分析，使用 InfluxDB 和相关工具，您可以获得有关 IIoT 数据的重要洞察，确保数据的准确性和实时性，并在需要时采取适当的措施。这对于工业物联网应用程序的成功非常重要。

## 结语

至此，我们已经顺利完成了在树莓派上部署 NanoMQ，并成功地建立了数据桥接，将数据传输至 EMQX Cloud，然后通过数据集成实现了数据桥接到 InfluxDB 3.0 的全部流程。EMQX Cloud 能满足工业数字化的各类底层数据需求，还能通过其与 MQTT 和 InfluxDB 的紧密集成，推动了工业物联网的创新。这种集成确保了从设备到数据库的无缝数据流，无论数据量多大、需求多么复杂。通过实践验证，EMQX Cloud 证明其在各种情况下都能保持高性能和可靠性，是构建和扩展工业物联网解决方案的理想选择。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
