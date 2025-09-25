| **Chapter** | **Feature**                                                  | **Difficulty** |
| ----------- | ------------------------------------------------------------ | -------------- |
| 1           | [Overview: Background + Environment Setup + Device Online](https://www.emqx.com/en/blog/esp32-and-mcp-over-mqtt) | ★              |
| 2           | **From "Command-Based" to "Semantic Control": MCP over MQTT Encapsulation of Device Capabilities** | ★★             |
| 3           | [Integrating LLM for "Natural Language → Device Control"](https://www.emqx.com/en/blog/esp32-and-mcp-over-mqtt-3) | ★★             |
| 4           | [Voice I/O: Microphone Data Upload + Speech Recognition + Speech Synthesis Playback](https://www.emqx.com/en/blog/esp32-and-mcp-over-mqtt-4) | ★★★            |
| 5           | [Persona, Emotion, Memory: From "Controller" to "Companion"](https://www.emqx.com/en/blog/esp32-and-mcp-over-mqtt-5)   | ★★★            |
| 6           | [Giving the AI "Eyes": Image Acquisition + Multimodal Understanding](https://www.emqx.com/en/blog/esp32-and-mcp-over-mqtt-6) | ★★★            |



*This is the second piece of our “Building Your AI Companion with ESP32 & MCP over MQTT” series.*

## Recap

In the [previous article](https://www.emqx.com/en/blog/esp32-and-mcp-over-mqtt), we laid the foundational groundwork:

- Set up the development environment, flashed the **ESP32**, and successfully connected to an **[MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)**.
- Implemented device online heartbeats, allowing the cloud to monitor device presence.
- Gained an initial understanding of the **[ESP32 + MQTT](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker)** IoT communication pattern.

In this article, we'll extend the **MQTT** foundation from the previous post into an **MCP over MQTT** architecture. This approach allows various device capabilities to be registered, discovered, and invoked as "Tools," opening up new possibilities for intelligent interaction between AI and IoT devices.

## Why MCP for IoT?

Currently, most traditional IoT devices rely on a "command-based control" model:

- Applications publish commands via hardcoded topics, like `esp32/set/brightness`, specifying the brightness value in the message body.
- Each device and each command requires implementing this interface specification. Extending with new features later requires manual code updates.

When AI/LLMs directly interact with IoT devices, the following issues arise:

- How does AI know what capabilities a device has?
- How does it understand the format and range of parameters during invocation?
- How can it control devices as "naturally" as calling a function?

The **MCP over MQTT** solution effectively addresses these challenges:

- It provides standardized **Tool Schemas**, enabling AI to "discover" device capabilities.
- IoT devices simply declare "what I can do" (e.g., adjust volume, set screen text).
- AI queries the tool list and invokes tools via **MCP**, eliminating the need for additional adaptation layers.

### MCP SSE: LLM Interfacing with Devices via Encapsulated HTTP Interfaces

![Frame 3468604.png](https://assets.emqx.com/images/9d3cc4cf36b6bd73f1067d688f04e447.png)

Currently, **MCP** primarily interfaces with third-party services via **SSE (Server-Sent Events)** or standard input/output. The most convenient approach is to reuse existing **HTTP interfaces**, directly encapsulating device data and control capabilities (like the device model services commonly found in most IoT platforms) as **MCP Tools**. This solution is particularly suitable for users who already offer device control and status query capabilities via **HTTP APIs**.

**Pros:**

- **Rapid Integration:** No need for large-scale modifications to already shipped devices; just add an MCP adaptation layer on the server side to quickly integrate with LLMs.
- **High Compatibility:** An HTTP interface-adapted MCP layer can seamlessly reuse existing device models and API designs.

**Cons:**

- **Architectural Redundancy:** The LLM and device are separated by an HTTP device model service and an MCP adaptation service, leading to multiple protocol conversions between MQTT and HTTP, increasing latency and reducing real-time performance.
- **Increased Complexity:** Multiple adaptation layers make software development and debugging more difficult.
- **Security and Maintenance Pressure:** The current SSE solution requires redesigning authentication and authorization mechanisms, as it cannot directly reuse existing IoT platform authentication systems. This brings additional development, maintenance costs, and potential security risks.

### MCP over MQTT: LLM Directly Interfacing with Devices

To address the multi-layer forwarding, latency, and security complexities of the SSE solution, we propose the **MCP over MQTT architecture**. This approach allows devices to directly register their capabilities via MQTT, enabling LLMs or applications to discover and invoke these capabilities without needing an HTTP device model service or an MCP adaptation layer.

![Frame 3468603.png](https://assets.emqx.com/images/960c708672f6c352a2f30e04c21a6806.png)

**Pros:**

- **Simplified Architecture:** Removes the cloud-side "device model service" and "MCP service (SSE)," resulting in a lighter overall communication path.
- **Low-Latency Invocation:** Applications or LLMs can directly invoke device-side tools via MQTT, eliminating intermediate forwarding.
- **High Development Efficiency:** Reduces protocol conversions and adaptation logic, shortening development and debugging cycles and improving scalability.
- **Centralized Management:** MCP service registration, discovery, service type classification, MCP message flow, and permission control are all handled uniformly on the MQTT Broker.
- **Reusable Security:** Can directly inherit existing IoT platform authentication and authorization mechanisms, enhancing development efficiency.

**Cons:**

- **Device Upgrade Required:** For already shipped devices without built-in MCP support, a firmware reflash or upgrade is needed if they lack OTA capabilities.
- **Offline Issues:** Devices cannot be invoked when offline, requiring the design of offline task caching, failed retry mechanisms, or state synchronization.

### MCP SSE vs. MCP over MQTT

| **Comparison Aspect**       | **Solution 1: MCP SSE (Based on HTTP Interface)**            | **Solution 2: MCP over MQTT (Native AI Architecture)**       |
| --------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **Architecture Complexity** | High: Requires HTTP device model service + MCP adaptation service; redundant protocol stack | Low: Devices register tools directly, no intermediate adaptation layer |
| **Invocation Latency**      | Higher: Multiple MQTT ⇄ HTTP protocol conversions            | Low: Native MQTT communication, shorter invocation chain     |
| **Development Cost**        | High: Cloud needs to maintain the device model service and adaptation layer; device capability changes require synchronous updates | Low: No extra HTTP interface encapsulation; more efficient development and debugging |
| **Compatibility**           | High: Suitable for existing devices that expose control interfaces via HTTP | Medium: Requires device-side upgrade for MCP support (reflash if no OTA) |
| **Security**                | Weaker: Native SSE authentication/permissions are limited; requires extra security mechanism design | Stronger: Can directly reuse existing IoT platform authentication and authorization |
| **Scalability**             | Moderate: Each new device capability requires HTTP layer updates | Strong: Devices dynamically register tools; LLM can automatically discover capabilities |
| **Real-time Performance**   | Moderate: Higher latency, suitable for non-real-time tasks   | Strong: Native MQTT architecture, low-latency invocation     |

Currently, some solutions use **HTTP-based WebSocket** protocols for device-to-cloud communication. However, **MQTT** offers more advantages in IoT scenarios, particularly in terms of protocol lightweightness, transmission efficiency, and low power consumption.

Readers can refer to [this article](https://www.emqx.com/en/blog/mqtt-vs-websocket) for a detailed comparison of the two.

## Tutorial: Encapsulating Device Capabilities with MCP over MQTT

**Goal:** Encapsulate volume adjustment and screen display functionalities using **MCP over MQTT**.

**Hardware:**

- ESP32 S3 Development Board
- Audio Amplifier (2-3W) and Speaker
- SPI Interface LCD Display

**Software:**

- Develop two **MCP Tools** on the **ESP32** and register them with **EMQX Serverless**:
  - `display`: For adjusting display content.
  - `set_volume`: For adjusting volume, with a parameter range of 0 - 100.
- Develop an **MCP Client** in **Python** on the cloud:
  - List registered tools from the device side.
  - View tool descriptions.

## ESP32 MCP Tool Implementation Code (C Language)

**MCP over MQTT SDK**

Download the [MCP over MQTT SDK component](https://github.com/mqtt-ai/esp32-mcp-mqtt-tutorial/tree/main/samples/blog_2/components/mcp-over-mqtt).

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

The code above implements a simple MCP Server using MCP over MQTT, declaring two Tools. After connecting to the MQTT server, these two tools are registered. When an MCP Client comes online, it can retrieve these registered tools from the MCP Server and initiate connections and invoke related interfaces.

In the `mcp_server_init` function:

- You can change `mqtt://broker.emqx.io` to the server address you obtained from **EMQX Serverless**.
- Update the `username`, `password`, and `cert` according to your Serverless configuration.

The `mcp_server.h` header file defines the MCP over MQTT interfaces for ESP32. We will later incorporate this implementation into standard ESP libraries for easier user development of MCP services. For more detailed code, refer to: [ESP32 Demo](https://github.com/mqtt-ai/esp32-mcp-mqtt-tutorial/blob/main/samples/blog_2/main/main.c).

## Cloud MCP Client (Python Language)

On the cloud side, we provide the MCP over MQTT Python Client SDK. Download [here](https://github.com/emqx/mcp-python-sdk).

Then, refer to e`xamples/clients/mqtt-clients/client_apis_demo.py`.

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

This code implements an MCP Client using the MCP over MQTT SDK. It connects to the MQTT server and waits for the MCP Server to connect and register. Once the MCP Server is registered, the client retrieves and displays the Tools and Resources supported by the MCP Server, based on its capabilities.

In the `async def main():` function, you can change `broker.emqx.io` to the server address you obtained from EMQX Serverless.

```python
        mqtt_options = mcp_mqtt.MqttOptions(
            host="broker.emqx.io",
        )
```

**Debugging and Verification**

```shell
# Start the MCP Client to connect it to the MQTT Broker
$ uv run examples/clients/mqtt-clients/client_apis_demo.py
# Compile and flash the MCP Demo to your ESP32 device
$ idf.py build & idf.py flash
# Monitor the ESP32 output
$ idf.py monitor
```

**ESP32 Program Output**

```shell
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

 **Python Program Awaiting MCP Server Connection and Initialization Logs**

```shell
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

**Python Program Retrieving MCP Server Capabilities and Supported Tools Logs**

```shell
2025-07-30 02:15:49,402 - Capabilities of ESP32 Demo Server: experimental=None logging=None prompts=None resources=None tools=ToolsCapability(listChanged=True)
2025-07-30 02:15:49,405 - Got msg from session for server_id: esp32-demo-server-client, msg: root=JSONRPCRequest(method='tools/list', params=None, jsonrpc='2.0', id=1)
2025-07-30 02:15:49,538 - Received message on topic $mcp-rpc/mqtt_client_demo/esp32-demo-server-client/ESP32 Demo Server: {"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"set_volume","description":"Set the volume of the device, range 1 to 100","inputSchema":{"type":"object","properties":{"volume":{"description":"Volume level","type":"integer"}},"required":["volume"]}},{"name":"display","description":"Display a message on the device","inputSchema":{"type":"object","properties":{"message":{"description":"Message to display","type":"string"}},"required":["message"]}}]}}
2025-07-30 02:15:49,541 - Sending msg to session for server_id: esp32-demo-server-client, msg: root=JSONRPCResponse(jsonrpc='2.0', id=1, result={'tools': [{'name': 'set_volume', 'description': 'Set the volume of the device, range 1 to 100', 'inputSchema': {'type': 'object', 'properties': {'volume': {'description': 'Volume level', 'type': 'integer'}}, 'required': ['volume']}}, {'name': 'display', 'description': 'Display a message on the device', 'inputSchema': {'type': 'object', 'properties': {'message': {'description': 'Message to display', 'type': 'string'}}, 'required': ['message']}}]})
2025-07-30 02:15:49,544 - Tools of ESP32 Demo Server: [Tool(name='set_volume', description='Set the volume of the device, range 1 to 100', inputSchema={'type': 'object', 'properties': {'volume': {'description': 'Volume level', 'type': 'integer'}}, 'required': ['volume']}), Tool(name='display', description='Display a message on the device', inputSchema={'type': 'object', 'properties': {'message': {'description': 'Message to display', 'type': 'string'}}, 'required': ['message']})]
```

If you can see this information, congratulations! You've completed this task: your device services are encapsulated via **MCP**, and the cloud can discover and display them.

## Coming Up Next

In the next article, we'll enable LLMs to directly invoke these MCP Tools, controlling volume and displaying information through natural language. This is where the journey of injecting "soul" into hardware with AI truly begins!

## Resources

- MCP over MQTT Python SDK code and examples: [MCP over MQTT Python SDK](https://github.com/emqx/mcp-python-sdk)
- Relevant code for this article: [MCP over MQTT ESP32 component](https://github.com/mqtt-ai/esp32-mcp-mqtt-tutorial)
- LlamaIndex library for connecting to MCP services: [LlamaIndex](https://www.llamaindex.ai/)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
