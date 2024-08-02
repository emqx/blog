## OCPP 简介

**开放充电桩协议**（Open Charge Point Protocol, OCPP）是一种应用协议，旨在实现电动汽车充电站与中央管理系统之间的通信，通过交换充电会话、状态更新和其他操作数据，促进充电业务的高效管理。

作为电动汽车充电站与中央管理系统之间的事实标准，OCPP 在电动汽车充电行业的采用率显著上升。许多国家和公司正在将 OCPP 纳入其基础设施，以确保电动汽车充电网络的无缝衔接和扩展。

OCPP 协议标准化了信息交换，支持多种操作：

1. **启动通知**：充电桩连接到中央系统时发送启动通知，进行自我注册并提供初始状态信息。
2. **心跳**：充电桩定期向中央系统发送心跳信息，以表明其仍处于连接和运行状态。
3. **授权**：充电会话开始前，充电桩向中央系统发送授权请求，以验证用户或车辆身份。
4. **启动和停止交易**：充电桩报告充电会话的开始和结束，提供仪表读数、会话持续时间和能源消耗等数据。
5. **状态通知**：充电桩发送状态更新，告知中央系统其当前状态，如可用、占用或故障。
6. **固件管理**：中央系统可通过发送更新命令来管理充电桩的固件。
7. **数据传输**：该协议支持在充电桩和中央系统之间传输各种运行数据，以便进行监控和分析。

这些操作可确保中央系统能够有效地监测、控制和管理电动汽车充电站网络。

OCPP 协议通过两种规范在网络上传输信息：

- **OCPP-J**：通过 WebSockets 使用 JSON 进行 OCPP 通信。具体的 OCPP 版本以 J 扩展名标示，如 OCPP1.6J 表示 1.6 版的 JSON/WebSockets 实现。
- **OCPP-S**：通过 SOAP 和 HTTP 进行 OCPP 通信。从 1.6 版本开始，S 必须明确标示。旧版本默认使用 S（除非另有说明），例如 OCPP 1.5 与 OCPP1.5S 相同。

OCPP-J 规范中的 `BootNotification.req` 消息格式如下：

```js
[
  // MessageTypeId, 2 表示这是客户端向服务器发送的请求消息
  2,
  // UniqueId，消息的唯一 ID，用于标识消息
  "19223201",
  // 操作，表示传输的信息类型
  "BootNotification",
  // 有效载荷，信息正文
  {"chargePointVendor": "VendorX", "chargePointModel": "SingleSocketCharger"}
]
```

## EMQX 5 中的 OCPP 网关

EMQX 是一个可以无限连接、任意集成、随处运行的大规模分布式物联网 MQTT 接入平台。它提供了一个多协议网关，用于处理所有非 MQTT 协议的连接、身份验证和消息收发。

> 有关 EMQX 多协议网关的更多信息，请参阅：[EMQX 5.0 全新网关框架：轻松实现多物联网协议接入](https://www.emqx.com/zh/blog/emqx-connects-multiple-iot-protocols)

EMQX 5 中提供了一个支持 OCPP-J 1.6 协议的 OCPP 网关：

![OCPP 网关](https://assets.emqx.com/images/04142322c686436d2ac4010decafeca6.png)

其工作原理如下：

- OCPP 网关启动一个 WebSocket 服务器端口，处理所有充电桩设备的连接、信息接收和信息传送。
- **第三方服务**是由用户实现的后端服务，它根据 MQTT 消息传递模式处理 OCPP 请求。
- OCPP 网关将来自设备的所有上行信息转换为相应的 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)和有效载荷，并将其发送至第三方服务。同时，它接收来自第三方服务的 MQTT 控制消息，将其转换为 OCPP 格式消息，并发送到相应的充电桩。

本文将介绍如何使用 EMQX 5.0 中的 OCPP 网关集成 OCPP 设备，实现不同制造商和服务提供商之间的互操作性。

## 配置 OCPP 网关

首先，我们要安装最新的 EMQX Enterprise。请参阅 [EMQX Enterprise 入门指南| EMQX Enterprise 文档](https://docs.emqx.com/zh/emqx/latest/getting-started/getting-started.html#%E5%AE%89%E8%A3%85-emqx)。

或者，也可以直接使用以下命令，通过 Docker 启动最新版本的 EMQX 容器：

```bash
docker run -p 18083:18083 -p 1883:1883 -p 33033:33033 emqx/emqx-enterprise:latest
```

在 EMQX 仪表板，点击左侧导航菜单中的**管理** -> **网关**。在**网关**页面上，列出了所有支持的网关。找到 **OCPP**，然后单击**操作**列中的 **配置**。接下来，将进入**初始化 OCPP** 页面。

![初始化 OCPP 页面](https://assets.emqx.com/images/e2a3a921019ec0ce0f04d05462d41844.png)

为了简化配置过程，EMQX 为**网关**页面上的所有必填字段提供了默认值。我们只需要：

1. 将`消息格式检查`改为`Disable`。
2. 在**基本参数**选项卡中点击**下一步**，接受所有默认设置。
3. 然后，您将被引导至**监听器**选项卡，EMQX 已预先配置了一个 33033 端口的 WebSocket 监听器。再次单击**下一步**确认设置。
4. 最后，单击**启用**按钮激活 OCPP 网关。

完成网关激活过程后，返回**网关**页面，可以看到 OCPP 网关现在显示**启用**状态。

![OCPP 网关启用成功](https://assets.emqx.com/images/7f319fae329b25d5e5e5f13734f551ec.png)

## 连接 OCPP 客户端

OCPP 网关启动后，可以使用 OCPP 客户端工具来测试连接，并验证设置是否正确。

以 ocpp-go 为例，以下是如何在 EMQX 中将 [**ocpp-go**](https://github.com/lorenzodonini/ocpp-go) 客户端连接到 OCPP 网关的步骤。

首先，准备一个 MQTT 客户端用于与 OCPP 网关交互。例如，使用 [**MQTTX**](https://mqttx.app/zh/downloads)，配置其连接到 EMQX 并订阅主题 `ocpp/#`。

![MQTTX](https://assets.emqx.com/images/d5aa77eb60827ead090b1bd9483728c6.png)

然后，运行 ocpp-go 客户端并与 OCPP 网关建立连接。

**注**：请将以下命令中的 `<host>` 替换为 EMQX 服务器的地址。

```bash
docker run -e CLIENT_ID=chargePointSim -e CENTRAL_SYSTEM_URL=ws://<host>:33033/ocpp -it --rm --name charge-point ldonini/ocpp1.6-charge-point:latest
```

连接成功后，将看到类似以下的日志输出：

```bash
INFO[2023-12-01T03:08:39Z] connecting to server logger=websocketINFO[2023-12-01T03:08:39Z] connected to server as chargePointSim logger=websocketINFO[2023-12-01T03:08:39Z] connected to central system at ws://172.31.1.103:33033/ocppINFO[2023-12-01T03:08:39Z] dispatched request 1200012677 to server logger=ocppj
```

接下来，检查 MQTTX 是否收到如下格式的消息：

```js
Topic: ocpp/cp/chargePointSim
Payload
{
  "UniqueId": "1200012677",
  "Payload": {
    "chargePointVendor": "vendor1",
    "chargePointModel": "model1"
  },
  "Action": "BootNotification"
}
```

此消息表示 ocpp-go 客户端已连接到 OCPP 网关并发起了 `BootNotification` 请求。

在 MQTTX 中，向主题 `ocpp/cs/chargePointSim` 发送包含以下内容的消息。

**注**：请将 `UniqueId` 替换为上一条消息中收到的 UniqueId。

```json
{
  "MessageTypeId": 3,
  "UniqueId": "***",
  "Payload": {
    "currentTime": "2023-12-01T14:20:39+00:00",
    "interval": 300,
    "status": "Accepted"
  },
  "Action": "BootNotification"
}
```

随后，MQTTX 将收到一条 `StatusNotification` 状态报告。这表明 OCPP 客户端已成功与 OCPP 网关建立连接。

```js
Topic: ocpp/cp/chargePointSim
​
Payload:
{
  "UniqueId": "3062609974",
  "Payload": {
    "status": "Available",
    "errorCode": "NoError",
    "connectorId": 0
  },
  "MessageTypeId": 2,
  "Action": "StatusNotification"
}
```

至此，OCPP 客户端已成功连接到 EMQX 的 OCPP 网关，并与第三方服务进行了通信。

## 结语

EMQX 5.0 的 OCPP 网关可以实现 OCPP 设备的轻松接入，为构建统一的电动汽车充电网络提供了便利。企业从而可以高效监控和管理其电动汽车充电基础设施，为实现更具可持续性和互联性的未来铺平道路。
