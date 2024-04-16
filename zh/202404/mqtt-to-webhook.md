## 引言

在物联网领域，实时监控各类设备数据和事件对于保障设备运行安全和效率至关重要。

企业级 MQTT 物联网接入平台 EMQX 提供了强大的 Webhook 数据集成功能，可以将 MQTT 设备事件和数据轻松集成到更多的外部系统中，比如分析平台、云服务等，实现多系统的数据分发，满足实时监控和事件响应的需求。

本文将演示如何利用 EMQX 采集各类设备数据，并与 Webhook 集成，实现数据的实时传输和处理。

## MQTT + Webhook 在物联网中的应用

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一个轻量级的发布/订阅消息协议，设计用于在网络上进行消息传递，特别适合于网络带宽有限、网络不稳定的环境。Webhook 是使用 HTTP 作为传输协议的回调机制，通过 Webhook，我们能够将 MQTT 消息跟客户端事件实时推送到指定的 Webhook/HTTP 服务器上，这种方式既可以实现设备数据的实时监控，也可以根据设备状态触发其他的业务流程，比如设备故障时自动发送报警信息。

![MQTT + Webhook](https://assets.emqx.com/images/ad51bbbfa3e8fa3f9c0881c8f17b95dd.png)

在物联网应用中，Webhook 具有以下独特优势：

- **将数据传递到更多的下游系统**：Webhook 可以将 MQTT 数据轻松集成到更多的外部系统中，比如分析平台、云服务等，实现多系统的数据分发。
- **实时响应并触发业务流程**：通过 Webhook，外部系统可以实时接收到 MQTT 数据并触发业务流程，实现快速响应。例如接收报警数据并触发业务工作流。
- **自定义处理数据**：外部系统可以根据需要对接收到的数据进行二次处理，实现更复杂的业务逻辑，不受 EMQX 功能限制。
- **松耦合的集成方式**：Webhook 使用简单的 HTTP 接口，提供了一种松耦合的系统集成方式。

总的来说，MQTT + Webhook 的组合为物联网应用提供了一种高效、灵活、实时的数据处理和传输方案。通过合理选择和配置数据集成方式，可以满足各种物联网应用的需求，提高物联网应用的效率和可用性。

## MQTT + Webhook 集成项目演示准备

### 前提条件

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

### 工作原理

这是一个简单而高效的架构，无需复杂的组件。主要包括以下关键组件：

| 组件名称                                                 | 版本   | 说明                                                         |
| :------------------------------------------------------- | :----- | :----------------------------------------------------------- |
| [EMQX Enterprise](https://www.emqx.com/en/products/emqx) | 5.5.0+ | 用于接入 MQTT 设备，并将设备事件与消息数据发送到 Webhook 服务的 MQTT Broker。 |
| [MQTTX CLI](https://mqttx.app/cli)                       | 1.9.3+ | 用于模拟设备连接到 EMQX 并发布消息的命令行工具。             |
| [Node.js](https://nodejs.org/)                           | 18.17  | 用于运行 Webhook 服务以处理来自 EMQX 的数据请求的运行环境。  |

### 下载示例项目到本地

使用 Git 将 [emqx/mqtt-to-webhook](https://github.com/emqx/mqtt-to-webhook) 存储库代码下载到本地：

```shell
git clone https://github.com/emqx/mqtt-to-webhook
cd mqtt-to-webhook
```

代码库由三部分组成：

- `emqx` 文件夹包含了 EMQX-Webhook 数据集成配置，可以在启动 EMQX 的时候自动创建规则和动作。
- `webserver` 文件夹包含了示例 Webhook 服务 Node.js 代码。
- `docker-compose.yml` 文件编排了所有组件，让您可以一键启动项目。

## 启动 MQTTX CLI、EMQX 和 Webhook 服务

请确保已经安装 [Docker](https://www.docker.com/)，完成安装后，可以使用以下命令， 通过 Docker Compose 在后台启动示例服务：

```shell
docker-compose up -d
```

此示例服务包含了几个关键部分，我们将在下文中详细介绍。

### 模拟设备订阅与消息发布

示例服务使用 MQTTX CLI 模拟设备的订阅与消息发布。

1. 使用 `sub` 命令，模拟一个设备订阅 `t/1`, `t/2` 2 个主题，对应的命令如下：

   ```shell
   mqttx sub -t t/1 t/2
   ```

2. 使用 [simulate](https://mqttx.app/zh/docs/cli/get-started#simulate) 命令，模拟一个设备接入到 EMQX 并以 5 秒间隔定期向 `mqttx/simulate/tesla/{clientid}` 主题发布消息，对应的命令如下：

   ```shell
   mqttx simulate -sc tesla -c 1 -im 5000
   ```

   使用任何 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)都可以订阅和接收模拟消息：

   ```shell
   mqttx sub -t mqttx/simulate/tesla/+
   ```

   此时，我们已经模拟了设备的行为，接下来我们将看到如何在 EMQX 上处理这些设备发送的消息和事件。

### 设备事件与消息处理

在模拟设备订阅和发布消息后，我们需要在 EMQX 上处理这些设备发送的消息和事件。这一部分将由 EMQX 上的 Webhook 数据集成完成。

EMQX 将创建 2 个 Webhook，分别用于处理设备发送的消息，以及连接/断开连接、订阅/取消订阅事件。您也可以参照 [Webhook 文档](https://docs.emqx.com/zh/enterprise/latest/data-integration/webhook.html)，处理更多客户端事件。

- **触发器**：这是触发 Webhook 的事件。对于消息，你需要选择 "消息发布" 并添加 `mqttx/simulate/#` 主题过滤消息；对于设备事件，需要勾选 "连接建立"、"连接断开"、"订阅完成"、"取消订阅" 这四个事件；
- **请求方法**：在这里需要选择 "POST" 方法；
- **URL**：这是 Webhook 服务的地址，需要填写 `http://webserver:3000/events/{event}`，其中 `{event}` 是一个占位符，会根据具体触发的事件动态替换；
- **请求头**：需要添加一个请求头，键为 `Authorization`，值为 `Bearer B53498D3-1752-4AA7-BACA-7013309B7468`，这用于在请求中进行 Webhook 服务的认证。

以上参数配置完成后，Webhook 就能正确地接收和处理来自 MQTT 客户端的事件和消息了。

EMQX 将通过 Webhook 数据集成功能，将事件和消息数据实时发送到 Webhook 服务。Webhook 数据集成提供了对 HTTP 请求参数的动态配置能力，包括 URL、认证方式、请求头、请求方法和请求 Body 等，从而能够灵活地对接各类 Webhook 服务。

### Webhook 服务数据处理

示例将启动一个基于 Node.js 的 Webhook 服务，接收来自 EMQX 的请求并进行数据处理。

1. 记录连接过的设备，并在连接/断开连接时更新其在线状态；
2. 记录设备事件历史，包括连接/断开连接、订阅/取消订阅的记录。

完整代码参照[此处](https://github.com/emqx/mqtt-to-webhook/blob/main/webserver/index.js)。

至此，我们已经完成了 EMQX MQTT 与 Webhook 的所有配置流程。Webhook 服务将把 EMQX 上 MQTT 设备的消息和事件处理后的数据存储到本地文件中。接下来，我们将介绍如何查看和理解这些数据。

## 查看 Webhook 服务记录的数据

我们可以通过 Webhook 服务提供的接口查看数据：

```shell
curl http://localhost:3000/events
```

返回的示例数据如下：

```json
{
  "devices": [
    {
      "clientId": "mqttx_1752c0ab",
      "username": "undefined",
      "connected": true,
      "ip": "192.168.228.4:43912",
      "connectedAt": "2024-02-19T09:42:12.952Z"
    },
    {
      "clientId": "mqttx_baf18c96_1",
      "username": "undefined",
      "connected": true,
      "ip": "192.168.228.5:58340",
      "connectedAt": "2024-02-19T09:42:13.020Z"
    }
  ],
  "eventsHistory": [
    {
      "event": "client.connected",
      "clientId": "mqttx_1752c0ab",
      "username": "undefined",
      "peername": "192.168.228.4:43912",
      "options": {
        "proto_ver": 5,
        "keepalive": 60,
        "clean_start": true,
        "node": "emqx@192.168.228.3"
      },
      "createdAt": "2024-02-19T09:42:12.952Z"
    },
    {
      "event": "session.subscribed",
      "clientId": "mqttx_1752c0ab",
      "username": "undefined",
      "options": {
        "topic": "t/2",
        "qos": 0,
        "node": "emqx@192.168.228.3"
      },
      "createdAt": "2024-02-19T09:42:12.963Z"
    },
    {
      "event": "client.connected",
      "clientId": "mqttx_baf18c96_1",
      "username": "undefined",
      "peername": "192.168.228.5:58340",
      "options": {
        "proto_ver": 5,
        "keepalive": 30,
        "clean_start": true,
        "node": "emqx@192.168.228.3"
      },
      "createdAt": "2024-02-19T09:42:13.020Z"
    }
  ],
  "messages": [
    {
      "topic": "mqttx/simulate/tesla/mqttx_baf18c96",
      "payload": "{\"car_id\":\"ZTGZJC1XPFN643051\",\"display_name\":\"Nova's Tesla\",\"model\":\"S\",\"trim_badging\":\"ad\",\"exterior_color\":\"lime\",\"wheel_type\":\"cumque\",\"spoiler_type\":\"aspernatur\",\"geofence\":\"West Ransom\",\"state\":\"online\",\"since\":\"2024-02-18T21:05:53.133Z\",\"healthy\":false,\"version\":\"9.6.6\",\"update_available\":true,\"update_version\":\"2.7.2\",\"latitude\":\"52.1216\",\"longitude\":\"78.0590\",\"shift_state\":\"R\",\"power\":-908,\"speed\":20,\"heading\":96,\"elevation\":1373,\"locked\":true,\"sentry_mode\":true,\"windows_open\":true,\"doors_open\":false,\"trunk_open\":true,\"frunk_open\":true,\"is_user_present\":false,\"is_climate_on\":true,\"inside_temp\":9.1,\"outside_temp\":29,\"is_preconditioning\":false,\"odometer\":744655,\"est_battery_range_km\":394.1,\"rated_battery_range_km\":281.3,\"ideal_battery_range_km\":138.5,\"battery_level\":47,\"usable_battery_level\":43,\"plugged_in\":true,\"charge_energy_added\":94.03,\"charge_limit_soc\":44,\"charge_port_door_open\":false,\"charger_actual_current\":72.98,\"charger_power\":43,\"charger_voltage\":234,\"charge_current_request\":36,\"charge_current_request_max\":25,\"scheduled_charging_start_time\":\"2028-04-25T11:27:22.090Z\",\"time_to_full_charge\":5.34,\"tpms_pressure_fl\":3,\"tpms_pressure_fr\":2.8,\"tpms_pressure_rl\":3.4,\"tpms_pressure_rr\":2.8,\"timestamp\":1708335738038}",
      "qos": 0,
      "clientId": "mqttx_baf18c96_1",
      "createdAt": "2024-02-19T09:42:18.046Z"
    }
  ]
}
```

- **deviceCount**：表示连接到 EMQX 服务器的设备数量。
- **messageCount**：表示 EMQX 服务器收到的消息数量。
- **eventsHistoryCount**：表示 EMQX 服务器记录的事件历史数量。
- **devices**：数组，包含了连接到 EMQX 服务器的所有设备的详细信息。
- **eventsHistory**：数组，包含了 EMQX 服务器记录的所有设备事件历史记录。
- **messages**：这是一个数组，其中包含了 MQTT 服务器收到的所有消息记录。

通过这些数据，我们可以获取整个应用的运行状态，包括设备连接情况、消息接收情况以及设备行为记录，这对于我们理解和优化 EMQX、利用客户端数据、进行设备管理和行为审计非常有帮助。

## 与 EMQX 其他集成方式对比

Webhook 的实时数据传输能力和灵活的接口使其能够轻松地与各种服务进行集成。开发者无需进行复杂的编程，就能实现各种实时事件处理，或者对接各类第三方服务，例如云服务的数据存储、函数计算、告警服务等。

然而，在处理大规模事件的情况下，Webhook 可能并不是最佳选择。由于其依赖于 HTTP 协议，处理大量数据时可能会遇到网络延迟、带宽限制等问题。如果服务器处理能力不足，还可能导致数据处理出现延迟或数据丢失。

因此，对于大规模的数据传输和消息存储，我们更推荐使用 EMQX 中的其他数据集成方式，比如直接将数据写入到数据库中。这种方式可以避免网络延迟和带宽限制的问题，同时也可以利用数据库的高效处理能力，确保数据的安全存储和高效处理。这样既能提高运营效率，又能保证系统的稳定性和安全性。

## 结语

在本文中，我们探讨了如何集成 EMQX 和 Webhook 来扩展物联网应用。通过使用 EMQX 作为实时 [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)，并将数据通过 Webhook 传输到外部系统，我们实现了一个端到端的解决方案，用于收集和处理设备数据。

在实际应用中，你可以根据自己的需求，调整 EMQX 和 Webhook 的配置，以满足你的特定需求。例如，你可以设置不同的 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)，以区分不同类型的设备数据；您也可以配置 Webhook，将数据发送到不同的外部系统，以便进行更深入的分析和处理。

总的来说，EMQX、MQTT 和 Webhook 提供了一种强大、灵活的解决方案，可以帮助您更好地扩展物联网应用。我们期待看到您利用这些功能，为您的物联网应用创造更多的可能性。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
