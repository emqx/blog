## **本系列教程路线图**

| 篇章 | 功能                                                       | 难度 |
| :--- | :--------------------------------------------------------- | :--- |
| 1    | 整体介绍：背景 + 环境准备 + 设备上线                       | ★    |
| 2    | **从“命令式控制”到“语义控制”：MCP over MQTT 封装设备能力** | ★★   |
| 3    | 接入 LLM，实现“自然语言 → 设备控制”                        | ★★   |
| 4    | 语音 I/O：麦克风数据上传 + 语音识别 + 语音合成回放         | ★★★  |
| 5    | 人格、情感、记忆：从“控制器”到“陪伴体”                     | ★★★  |
| 6    | 给智能体增加“眼睛”：图像采集 + 多模态理解                  | ★★★  |

## 回顾

在[上一篇文章](https://www.emqx.com/zh/blog/esp32-and-mcp-over-mqtt)中，我们已经完成了基础准备工作：

- 搭建了开发环境，烧录 ESP32 并成功连接 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)
- 实现了设备上线心跳，让云端可以感知设备是否在线
- 初步了解了 ESP32 + MQTT 的 IoT 通信模式

然而，传统的 IoT 控制是「命令式」的，存在明显的局限性。开发者必须事先定义主题（topic）、硬编码命令格式，这让 AI 难以「理解」和「调用」设备的真实能力。

如果我们想让大模型直接与设备对话，就需要让 AI 突破以下限制：

1. 自动「发现」设备具备哪些功能（例如：调节音量、设定屏幕文字）。
2. 通过统一的工具调用接口调用这些功能，而不是依赖硬编码指令。

在本文中，我们将前文搭建的 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 基础扩展为 MCP over MQTT 架构，让设备的各种能力将以「工具（Tool）」的形式被注册、发现和调用，为 AI 与物联网设备的智能交互开辟新的可能。

## 为什么 IoT 需要 MCP？

目前，传统 IoT 设备大多依赖「命令式控制」模式：

- 应用通过硬编码主题 (topic) 发布指令，如 `esp32/set/brightness`，在消息体中指定设定的亮度的值。
- 每个设备、每个命令都需要实现该接口规范，后续扩展新功能时需要手动更新代码。

在 AI 大模型直接与 IoT 设备对话的过程中，会出现以下问题：

- AI 怎么知道设备有哪些能力？
- 调用时怎么理解参数的格式和范围？
- 如何做到像调用函数一样「自然」地控制设备？

MCP over MQTT 方案可以有效地解决这些问题：

- 它提供了标准化的工具描述（Tool Schema），让 AI 能「发现」设备能力。
- IoT 设备只需声明「我能做什么」（例如：调节音量、设定屏幕文字）。
- AI 通过 MCP 查询工具列表、调用工具，无需额外适配层。

### MCP SSE：大模型通过封装的 HTTP 接口对接设备

![image.png](https://assets.emqx.com/images/bc7b2cfee625688cfb070b395d4d0b30.png)

目前 MCP 主要通过 SSE（Server-Sent Events）或标准输入/输出来对接第三方服务。最便捷的方式是复用现有 HTTP 接口，将设备数据和控制能力（如大部分物联网平台中已有的物模型服务）直接封装为 MCP 工具。该方案特别适用于已经通过 HTTP API 提供设备控制和状态查询能力的用户。

**优点**

- **快速集成：**无需对已出厂设备进行大规模改造，只需在服务器端增加 MCP 适配层，即可快速接入大模型。
- **兼容性高：**适配 HTTP 接口的 MCP 层可无缝复用已有物模型和 API 设计。

**不足**

- **架构冗余：**大模型与设备之间隔着 HTTP 物模型服务和 MCP 适配服务，导致消息在 MQTT 与 HTTP 之间需要多次协议转换，增加延迟并降低实时性。
- **复杂度上升：**多层适配让软件开发与调试难度增大。
- **安全与维护压力：**当前 SSE 方案需要重新设计认证与权限控制机制，无法直接复用 IoT 平台的原有认证体系，带来额外的开发、维护成本及潜在安全隐患。

### **MCP over MQTT：LLM 直接对接设备**

针对 SSE 方案存在的多层转发、延迟和安全复杂性，我们提出 MCP over MQTT 架构。该方案让设备直接通过 MQTT 注册自身能力，大模型或应用可直接发现和调用这些能力，无需经过 HTTP 物模型服务或 MCP 适配层。

![image.png](https://assets.emqx.com/images/95430e8f7d98895c74d1e2ed4d1c8bfa.png)

**优点**

- **架构更简化：**移除了云端「物模型服务」和「MCP 服务 (SSE)」，整体链路更轻量。
- **低延迟调用：**App 或 LLM 可直接通过 MQTT 调用设备端工具，无需中间转发。
- **开发效率高：**减少了协议转换和适配逻辑，缩短开发和调试周期，提高可扩展性。
- **集中化管理：**MCP 服务的注册、发现、服务类型归类，以及 MCP 消息流转、权限控制等功能统一在 MQTT Broker 上完成。
- **安全可复用：**可直接继承现有物联网平台的认证与权限控制机制，提高开发效率。

**不足**

- **设备需升级：**对于未内置 MCP 支持的已出厂设备，若无 OTA 能力，需要重新烧录或升级固件。
- **离线问题：**设备离线时无法调用，需要设计离线任务缓存、失败重试或状态同步机制。

### **MCP SSE vs. MCP MQTT**

| **对比维度**   | **方案 1：MCP SSE（基于 HTTP 接口）**                    | **方案 2：MCP over MQTT（原生 AI 架构）**     |
| :------------- | :------------------------------------------------------- | :-------------------------------------------- |
| **架构复杂度** | 高：需 HTTP 物模型服务 + MCP 适配服务，协议栈较冗余      | 低：设备直接注册工具，去掉中间适配层          |
| **调用延迟**   | 较高：MQTT ⇄ HTTP 多次协议转换                           | 低：MQTT 原生通信，调用链更短                 |
| **开发成本**   | 高：云端需维护物模型服务和适配层，设备能力变动需同步更新 | 低：无需额外 HTTP 接口封装，开发和调试更高效  |
| **兼容性**     | 高：适用于已通过 HTTP 暴露控制接口的存量设备             | 中：需设备端升级支持 MCP（无 OTA 需重新烧录） |
| **安全性**     | 弱：SSE 原生认证/权限较弱，需额外设计安全机制            | 强：可直接复用 IoT 平台原有认证与权限控制     |
| **扩展性**     | 一般：每新增设备能力都需更新 HTTP 层                     | 强：设备动态注册工具，LLM 可自动发现设备能力  |
| **实时性**     | 一般：延迟较高，适合非强实时任务                         | 强：MQTT 原生架构，低延迟调用                 |

目前还有一些方案采用基于 HTTP 的 WebSocket 协议实现设备到云端的通信，但相比之下，MQTT 在物联网场景中更具优势，尤其在协议轻量性、传输效率和低功耗等方面表现更优。

读者可参考：[MQTT 与 WebSocket：关键差异与应用场景](https://www.emqx.com/zh/blog/mqtt-vs-websocket)一文，了解二者的详细对比。

## **MCP over MQTT 封装能力**

目标：通过 MCP over MQTT 封装调整音量以及让屏幕显示信息。

### 硬件

- ESP32 S3 开发版
- 功放 2-3W 以及 喇叭
- SPI 接口液晶显示屏

### 软件

- 在 ESP32 上开发两个 MCP 工具，并向 EMQX Servless 进行注册
  1. `display`，用于调整显示内容
  2. `set_volume`，用于调整音量，参数可以设定为 0 - 100
- 云端开发使用 Python 实现的 MCP 客户端
  - 列出设备端注册的工具列表
  - 查看工具描述

## **ESP32 MCP 工具实现代码 (C 语言实现)**

**MCP over MQTT SDK** 

下载 [MCP over MQTT SDK component](https://github.com/mqtt-ai/esp32-mcp-mqtt-tutorial/tree/main/samples/blog_2/components/mcp-over-mqtt)

```c
#include <stdio.h>

#include "freertos/FreeRTOS.h"

#include "esp_log.h"
#include "esp_system.h"
#include "nvs_flash.h"

#include "mcp.h"
#include "mcp_server.h"
#include "wifi.h"

const char *set_volume(int n_args, property_t *args)
{
    if (n_args < 2) {
        return "At least two arguments are required";
    }

    for (int i = 0; i < n_args; i++) {
        if (args[i].type != PROPERTY_INTEGER) {
            return "All arguments must be integers";
        }
        ESP_LOGI("mcp server", "Setting volume to: %lld\n",
                 args[i].value.integer_value);
    }
    return "Volume set successfully";
}

const char *display(int n_args, property_t *args)
{
    if (n_args < 1) {
        return "At least one argument is required";
    }
    for (int i = 0; i < n_args; i++) {
        if (args[i].type != PROPERTY_STRING) {
            return "All arguments must be strings";
        }
        ESP_LOGI("mcp server", "Display: %s\n", args[i].value.string_value);
    }
    return "Message displayed successfully";
}

void app_main(void)
{
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    wifi_station_init("wifi_ssid", "wifi_password");

    vTaskDelay(pdMS_TO_TICKS(1000));
    mcp_server_t *server = mcp_server_init(
        "ESP32 Demo Server", "A demo server for ESP32 using MCP over MQTT",
        "mqtt://broker.emqx.io", "esp32-demo-server-client", NULL, NULL, NULL);

    mcp_tool_t tools[] = {
        { .name           = "set_volume",
          .description    = "Set the volume of the device, range 1 to 100",
          .property_count = 1,
          .properties =
              (property_t[]) {
                  { .name                = "volume",
                    .description         = "Volume level",
                    .type                = PROPERTY_INTEGER,
                    .value.integer_value = 30 },
              },
          .call = set_volume },
        { .name           = "display",
          .description    = "Display a message on the device",
          .property_count = 1,
          .properties =
              (property_t[]) {
                  { .name               = "message",
                    .description        = "Message to display",
                    .type               = PROPERTY_STRING,
                    .value.string_value = "Hello, MCP!" },
              },
          .call = display },
    };

    mcp_server_register_tool(server, sizeof(tools) / sizeof(mcp_tool_t), tools);

    mcp_server_run(server);
}
```

上述代码使用 MCP over MQTT 实现了一个简单的 MCP Server，声明了两个 Tools，连接到 MQTT 服务器后，注册了这两个工具，当 MCP Client 上线后，可以获取到 MCP Server 已经注册的两个工具，发起初始化以及调用相关接口。

- mcp_server_init 函数中，
  - 可以将 `mqtt://broker.emqx.io` 更改为在 EMQX Serverless 中申请的服务器地址；
  - username、password 以及 cert 根据 Serverless 的配置更改；

其中头文件 `mcp_server.h` 中定义的是 MCP over MQTT 在 ESP 上的接口，后续我们会将此实现放到标准的 ESP 库中，用户就可以更方便地基于此来实现相关的 MCP 服务，更多详细代码请参考 [ESP32 Demo](https://github.com/mqtt-ai/esp32-mcp-mqtt-tutorial/blob/main/samples/blog_2/main/main.c)。

## **云端 MCP 客户端 (Python 语言实现)**

在云端，我们提供了 MCP over MQTT 的 Python 客户端 SDK，下载安装 [MCP over MQTT SDK](https://github.com/emqx/mcp-python-sdk)，参考 `examples/clients/mqtt-clients/client_apis_demo.py`

```python
import logging
import anyio
import mcp.client.mqtt as mcp_mqtt
from mcp.shared.mqtt import configure_logging

configure_logging(level="DEBUG")
logger = logging.getLogger(__name__)

async def on_mcp_server_discovered(client, server_name):
    logger.info(f"Discovered {server_name}, connecting ...")
    await client.initialize_mcp_server(server_name)

async def on_mcp_connect(client, server_name, connect_result):
    capabilities = client.get_session(server_name).server_info.capabilities
    logger.info(f"Capabilities of {server_name}: {capabilities}")
    if capabilities.prompts:
        prompts = await client.list_prompts(server_name)
        logger.info(f"Prompts of {server_name}: {prompts}")
    if capabilities.resources:
        resources = await client.list_resources(server_name)
        logger.info(f"Resources of {server_name}: {resources}")
        resource_templates = await client.list_resource_templates(server_name)
        logger.info(f"Resources templates of {server_name}: {resource_templates}")
    if capabilities.tools:
        toolsResult = await client.list_tools(server_name)
        tools = toolsResult.tools
        logger.info(f"Tools of {server_name}: {tools}")

async def on_mcp_disconnect(client, server_name):
    logger.info(f"Disconnected from {server_name}")

async def main():
    async with mcp_mqtt.MqttTransportClient(
        "test_client",
        auto_connect_to_mcp_server = True,
        on_mcp_server_discovered = on_mcp_server_discovered,
        on_mcp_connect = on_mcp_connect,
        on_mcp_disconnect = on_mcp_disconnect,
        mqtt_options = mcp_mqtt.MqttOptions(
            host="broker.emqx.io",
        )
    ) as client:
        await client.start()
        while True:
            logger.info("Other works while the MQTT transport client is running in the background...")
            await anyio.sleep(10)

if __name__ == "__main__":
    anyio.run(main)
```

上述代码使用 MCP over MQTT SDK 实现了 MCP Client, 连接到 MQTT 服务器，等待 MCP Server 的连接注册，MCP Server 连接注册后，根据 MCP Server 的能力，获取展示了 MCP Server 支持的 Tools 以及 Resources。

在以下的函数 `async def main():` 里，可以将 `broker.emqx.io` 更改为在 EMQX Serverless 申请的服务器地址。

```python
mqtt_options = mcp_mqtt.MqttOptions(
    host="broker.emqx.io",
)
```

**调试与验证**

```shell
# 启动 MCP Client，使 MCP Client 连接到 MQTT Broker。
$ uv run examples/clients/mqtt-clients/client_apis_demo.py

# 编译并烧录 MCP Demo 到 ESP32 设备
$ idf.py build & idf.py flash

# 监控 ESP32 输出
$ idf.py monitor
```

 

**ESP32 程序输出**

```
I (789) wifi:dp: 1, bi: 102400, li: 3, scale listen interval from 307200 us to 307200 us
I (789) wifi:set rx beacon pti, rx_bcn_pti: 0, bcn_timeout: 25000, mt_pti: 0, mt_time: 10000
I (819) wifi:AP's beacon interval = 102400 us, DTIM period = 1
I (959) wifi:<ba-add>idx:0 (ifx:0, 80:3f:5d:f1:ab:4a), tid:0, ssn:3, winSize:64
I (3849) esp_netif_handlers: sta ip: 192.168.10.130, mask: 255.255.255.0, gw: 192.168.10.1
I (3849) wifi sta: ip: 192.168.10.130, mask: 255.255.255.0, gateway: 192.168.10.1
I (3849) wifi sta: connected to ap SSID: wifi_ssid
I (4849) mcp_server: Registered tool: set_volume
I (4849) mcp_server: Registered tool: display
I (4849) mcp_server: Connecting to MQTT broker: mqtt://broker.emqx.io
I (4849) main_task: Returned from app_main()
I (12399) mcp_server: MQTT client connected
I (12809) mcp_server: MCP client initialized: mqtt_client_demo
I (13229) mcp_server: tools/list request received from $mcp-rpc/mqtt_client_demo/esp32-demo-server-client/ESP32 Demo Server
```

 

**Python 程序等待 MCP Server 连接并初始化日志**

```
2025-07-30 02:15:47,009 - Connected to MQTT broker_host at broker.emqx.io:1883
2025-07-30 02:15:47,065 - Received message on topic $mcp-server/presence/esp32-demo-server-client/ESP32 Demo Server: {"jsonrpc":"2.0","method":"notifications/server/online","params":{"server_name":"ESP32 Demo Server","description":"A demo server for ESP32 using MCP over MQTT","meta":{"rbac":{"roles":[]}}}}
2025-07-30 02:15:47,066 - Server ESP32 Demo Server with id esp32-demo-server-client is online
2025-07-30 02:15:47,068 - Discovered ESP32 Demo Server, connecting ...
2025-07-30 02:15:47,123 - Subscribed to topics for server_name: ESP32 Demo Server, server_id: esp32-demo-server-client
2025-07-30 02:15:47,124 - Created new session for server_id: esp32-demo-server-client
2025-07-30 02:15:47,124 - initialize: ESP32 Demo Server
2025-07-30 02:15:47,126 - Got msg from session for server_id: esp32-demo-server-client, msg: root=JSONRPCRequest(method='initialize', params={'protocolVersion': '2024-11-05', 'capabilities': {'sampling': {}, 'roots': {'listChanged': True}}, 'clientInfo': {'name': 'mcp', 'version': '0.1.0'}}, jsonrpc='2.0', id=0)
2025-07-30 02:15:47,127 - Received message on topic $mcp-rpc/mqtt_client_demo/esp32-demo-server-client/ESP32 Demo Server: {"jsonrpc":"2.0","id":2,"error":{"code":-32601,"message":"Method not found"}}
2025-07-30 02:15:47,128 - Sending msg to session for server_id: esp32-demo-server-client, msg: root=JSONRPCError(jsonrpc='2.0', id=2, error=ErrorData(code=-32601, message='Method not found', data=None))
2025-07-30 02:15:49,390 - Received message on topic $mcp-rpc/mqtt_client_demo/esp32-demo-server-client/ESP32 Demo Server: {"jsonrpc":"2.0","id":0,"result":{"protocolVersion":"2024-11-05","serverInfo":{"name":"mcp","version":"0.0.1"},"capabilities":{"tools":{"listChanged":true}}}}
2025-07-30 02:15:49,393 - Sending msg to session for server_id: esp32-demo-server-client, msg: root=JSONRPCResponse(jsonrpc='2.0', id=0, result={'protocolVersion': '2024-11-05', 'serverInfo': {'name': 'mcp', 'version': '0.0.1'}, 'capabilities': {'tools': {'listChanged': True}}})
2025-07-30 02:15:49,399 - Got msg from session for server_id: esp32-demo-server-client, msg: root=JSONRPCNotification(method='notifications/initialized', params=None, jsonrpc='2.0')
2025-07-30 02:15:49,399 - Session initialized for server_id: esp32-demo-server-client
```


**Python 程序获取 MCP Server 支持的能力以及支持的 Tools 日志**

```
2025-07-30 02:15:49,402 - Capabilities of ESP32 Demo Server: experimental=None logging=None prompts=None resources=None tools=ToolsCapability(listChanged=True)
2025-07-30 02:15:49,405 - Got msg from session for server_id: esp32-demo-server-client, msg: root=JSONRPCRequest(method='tools/list', params=None, jsonrpc='2.0', id=1)
2025-07-30 02:15:49,538 - Received message on topic $mcp-rpc/mqtt_client_demo/esp32-demo-server-client/ESP32 Demo Server: {"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"set_volume","description":"Set the volume of the device, range 1 to 100","inputSchema":{"type":"object","properties":{"volume":{"description":"Volume level","type":"integer"}},"required":["volume"]}},{"name":"display","description":"Display a message on the device","inputSchema":{"type":"object","properties":{"message":{"description":"Message to display","type":"string"}},"required":["message"]}}]}}
2025-07-30 02:15:49,541 - Sending msg to session for server_id: esp32-demo-server-client, msg: root=JSONRPCResponse(jsonrpc='2.0', id=1, result={'tools': [{'name': 'set_volume', 'description': 'Set the volume of the device, range 1 to 100', 'inputSchema': {'type': 'object', 'properties': {'volume': {'description': 'Volume level', 'type': 'integer'}}, 'required': ['volume']}}, {'name': 'display', 'description': 'Display a message on the device', 'inputSchema': {'type': 'object', 'properties': {'message': {'description': 'Message to display', 'type': 'string'}}, 'required': ['message']}}]})
2025-07-30 02:15:49,544 - Tools of ESP32 Demo Server: [Tool(name='set_volume', description='Set the volume of the device, range 1 to 100', inputSchema={'type': 'object', 'properties': {'volume': {'description': 'Volume level', 'type': 'integer'}}, 'required': ['volume']}), Tool(name='display', description='Display a message on the device', inputSchema={'type': 'object', 'properties': {'message': {'description': 'Message to display', 'type': 'string'}}, 'required': ['message']})]
```

如果你能看到这些信息，恭喜你完成了本次任务：**设备服务通过 MCP 封装，云端可以发现并展示。**

## **下篇预告**

在下一篇中，我们将让 LLM（大模型）直接调用这些 MCP 工具，通过自然语言控制音量和显示信息，开启 AI 给硬件注入「灵魂」之旅！

## 资源

- MCP over MQTT 的 Python SDK 代码，以及样例：[MCP over MQTT Python SDK ](https://github.com/emqx/mcp-python-sdk)
- 本篇文章的相关代码：[MCP over MQTT ESP32 component](https://github.com/mqtt-ai/esp32-mcp-mqtt-tutorial)
- 连接 MCP 服务相关的 LlamaIndex 库： [LlamaIndex](https://www.llamaindex.ai/) 



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
