## **本系列教程路线图**

| 篇章 | 功能                                                   | 难度 |
| :--- | :----------------------------------------------------- | :--- |
| 1    | 整体介绍：背景 + 环境准备 + 设备上线                   | ★    |
| 2    | 从“命令式控制”到“语义控制”：MCP over MQTT 封装设备能力 | ★★   |
| 3    | **接入 LLM，实现“自然语言 → 设备控制”**                | ★★   |
| 4    | 语音 I/O：麦克风数据上传 + 语音识别 + 语音合成回放     | ★★★  |
| 5    | 人格、情感、记忆：从“控制器”到“陪伴体”                 | ★★★  |
| 6    | 给智能体增加“眼睛”：图像采集 + 多模态理解              | ★★★  |

## 回顾：MCP over MQTT 封装设备能力

在上一篇文章中，我们介绍了如何使用 MCP over MQTT 协议，完成 ESP32 设备能力开发，并向 EMQX 注册与发现。

- 开发  MCP Server，完成音量工具的封装，并向 EMQX 注册；
- 云端的 MCP 客户端应用可以通过 Python SDK 拉取设备注册的工具能力；
- 打通了“我知道你能做什么”的第一步。

本篇将在此基础上，让大模型接管控制逻辑，实现「你说我做」的效果。

## 本篇目标：让大模型能「自然」地控制设备

本篇将介绍如何借助大语言模型（以下简称：LLM），实现通过自然语言对设备的控制。例如：

- “声音太吵了” → 推理出需调用 `set_volume(40)`
- “刚才那个声音再调低一点” → 支持上下文和多轮对话

具体目标是：

- 利用自然语言触发 MCP 中注册的工具函数；
- 通过 LLM 的 MCP 调用自动转化为对应的 MQTT 消息；
- 构建一个具备上下文理解能力的交互式设备控制智能体。

## 为什么要接入大语言模型？

在 LLM 出现之前，设备控制主要依赖结构化输入：

- 用户必须点击预设选项或输入固定命令；
- 逻辑死板，缺乏上下文理解；
- 每新增一个功能，都需增加 UI 或代码逻辑，扩展成本高。

即便语音识别结合 API 调用能实现部分「智能控制」，但一旦语句稍有偏差或接口发生变化，就容易“失灵”，造成用户挫败感。相比之下，LLM 天然具备语义理解与上下文保持能力，能带来：

- 更自然的交互方式；
- 更强的指令容错能力；
- 更低的开发和维护成本。

接入 LLM 后，设备控制的智能化能力大幅提升。它不仅能根据模糊语言推断对应函数调用，还能灵活应对不同厂商，以及硬件升级导致的接口变化，让设备的智能体验更加流畅丝滑。

## 程序执行过程

![image.png](https://assets.emqx.com/images/ca524c807c9c0607848e269176e3ba8d.png)

1. 通过自然语言表达意图，LLM 负责理解语义。
2. 将用户意图转化为结构化 MCP 工具调用（Tool Call）， 并且提供合适的参数。
3. 工具调用通过 MCP 协议被封装成标准的 MQTT 消息，经由 EMQX 转发到对应的 ESP32 设备。
4. ESP 执行具体的控制逻辑代码。
5. 将工具的调用结果传给 LLM，由 LLM 给用户返回相关的调用结果，并由 APP 展示给用户。

整个链路简单直接，并且具备良好的解耦性和可扩展性，便于快速集成多种设备。

## 自然语言调用 MCP 工具

### 硬件

与[上一篇文章](https://www.emqx.com/zh/blog/esp32-and-mcp-over-mqtt-2)所需硬件一致，无需调整。

### 软件

- LlamaIndex 相关的 MCP tools 调用库文件。
- MCP over MQTT 相关的库文件。
- 大模型：本文选择的是 DeepSeek R1，是由 SiliconFlow 提供的公有服务；读者也可以根据自己的情况换成别的 LLM 服务提供商的服务，比如：阿里云提供的通义千问服务。

#### SiliconFlow API 密钥申请

- 进入 [SiliconFlow](https://www.siliconflow.cn/) 官网([硅基流动 SiliconFlow - 致力于成为全球领先的 AI 能力提供商](https://www.siliconflow.cn/)) ，注册账号并登陆。
- 登陆后在左侧，账户管理 → API 密钥中新建密钥即可。

### ESP32 控制音量 MCP 服务

```c#
#include <math.h>
#include <stdio.h>

#include "freertos/FreeRTOS.h"

#include "esp_log.h"
#include "esp_system.h"
#include "nvs_flash.h"

#include "mcp.h"
#include "mcp_server.h"
#include "radio.h"
#include "wifi.h"

const char *set_volume(int n_args, property_t *args)
{
    if (n_args < 1) {
        return "At least one argument is required";
    }

    if (args[0].type != PROPERTY_INTEGER) {
        return "Volume argument must be an integer";
    }

    int volume = (int) args[0].value.integer_value;
    if (volume < 0 || volume > 100) {
        return "Volume must be between 0 and 100";
    }

    esp_err_t ret = max98357_set_volume_percent((uint8_t) volume);
    if (ret != ESP_OK) {
        return "Failed to set volume";
    }

    ESP_LOGI("mcp server", "Setting volume to: %d%%", volume);
    return "Volume set successfully";
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

    ret = max98357_init();
    if (ret != ESP_OK) {
        ESP_LOGE("main", "MAX98357 init error: %s", esp_err_to_name(ret));
    }

    max98357_set_volume_percent(50);

    wifi_station_init("wifi_ssid", "wifi_password");

    vTaskDelay(pdMS_TO_TICKS(1000));
    mcp_server_t *server = mcp_server_init(
        "ESP32 Demo Server", "A demo server for ESP32 using MCP over MQTT",
        "mqtt://broker.emqx.io", "esp32-demo-server-client", NULL, NULL, NULL);

    mcp_tool_t tools[] = {
        { .name           = "set_volume",
          .description    = "Set the volume of the device, range 0 to 100",
          .property_count = 1,
          .properties =
              (property_t[]) {
                  { .name                = "volume",
                    .description         = "Volume level (0-100)",
                    .type                = PROPERTY_INTEGER,
                    .value.integer_value = 50 },
              },
          .call = set_volume },
    };

    mcp_server_register_tool(server, sizeof(tools) / sizeof(mcp_tool_t), tools);

    mcp_server_run(server);
}
```

使用 MCP Over MQTT Component 注册调整音量的 Tool，初始化 MCP Server 与 音频播放模块，注意修改 MCP Server 的参数，连接到 Serverless，以及修改 WIFI 的 SSID 与 Password。更多详细代码请参考 [ESP32 Demo](https://github.com/mqtt-ai/esp32-mcp-mqtt-tutorial/tree/main/samples/blog_3)。

###  云端 MCP Client 对接大模型调用 MCP 工具 - agent.py

```python
import asyncio
import anyio
import logging
import os
from typing import List, Optional, Union, cast
from dataclasses import dataclass

import mcp.client.mqtt as mcp_mqtt
from mcp.shared.mqtt import configure_logging
import mcp.types as types

from llama_index.llms.siliconflow import SiliconFlow
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.agent import AgentRunner
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.settings import Settings

configure_logging(level="DEBUG")
logger = logging.getLogger(__name__)


async def on_mcp_server_discovered(client: mcp_mqtt.MqttTransportClient, server_name):
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

client = None
api_key = "sk-***"

async def get_mcp_tools(mcp_client: mcp_mqtt.MqttTransportClient) -> List[BaseTool]:
    all_tools = []
    try:
        try:
            tools_result = await mcp_client.list_tools("ESP32 Demo Server")
            
            if tools_result is False:
                return all_tools
            
            list_tools_result = cast(types.ListToolsResult, tools_result)
            tools = list_tools_result.tools
            
            for tool in tools:
                logger.info(f"tool: {tool.name} - {tool.description}")
                
                def create_mcp_tool_wrapper(client_ref, server_name, tool_name):
                    async def mcp_tool_wrapper(**kwargs):
                        try:
                            result = await client_ref.call_tool(server_name, tool_name, kwargs)
                            if result is False:
                                return f"call {tool_name} failed"
                            
                            call_result = cast(types.CallToolResult, result)
                            
                            if hasattr(call_result, 'content') and call_result.content:
                                content_parts = []
                                for content_item in call_result.content:
                                    if hasattr(content_item, 'type'):
                                        if content_item.type == 'text':
                                            text_content = cast(types.TextContent, content_item)
                                            content_parts.append(text_content.text)
                                        elif content_item.type == 'image':
                                            image_content = cast(types.ImageContent, content_item)
                                            content_parts.append(f"[image: {image_content.mimeType}]")
                                        elif content_item.type == 'resource':
                                            resource_content = cast(types.EmbeddedResource, content_item)
                                            content_parts.append(f"[resource: {resource_content.resource}]")
                                        else:
                                            content_parts.append(str(content_item))
                                    else:
                                        content_parts.append(str(content_item))
                                
                                result_text = '\n'.join(content_parts)
                                
                                if hasattr(call_result, 'isError') and call_result.isError:
                                    return f"tool return error: {result_text}"
                                else:
                                    return result_text
                            else:
                                return str(call_result)
                                
                        except Exception as e:
                            error_msg = f"call {tool_name} error: {e}"
                            logger.error(error_msg)
                            return error_msg
                    
                    return mcp_tool_wrapper
                
                wrapper_func = create_mcp_tool_wrapper(mcp_client, "ESP32 Demo Server", tool.name)
                
                try:
                    llamaindex_tool = FunctionTool.from_defaults(
                        fn=wrapper_func,
                        name=f"mcp_{tool.name}",
                        description=tool.description or f"MCP tool: {tool.name}",
                        async_fn=wrapper_func
                    )
                    all_tools.append(llamaindex_tool)
                    logger.info(f"call tool success: mcp_{tool.name}")
                    
                except Exception as e:
                    logger.error(f"create tool {tool.name} error: {e}")
                    
        except Exception as e:
            logger.error(f"Get tool list error: {e}")
                
    except Exception as e:
        logger.error(f"Get tool list error: {e}")
    
    return all_tools

class ConversationalAgent:
    def __init__(self, mcp_client: Optional[mcp_mqtt.MqttTransportClient] = None):
        self.llm = SiliconFlow(api_key=api_key, model="deepseek-ai/DeepSeek-R1", temperature=0.6, max_tokens=4000, timeout=180)
        Settings.llm = self.llm
        
        self.mcp_client = mcp_client
        self.tools = []
        
        self.agent = AgentRunner.from_llm(
            llm=self.llm,
            tools=self.tools,
            verbose=True
        )
        
        self.mcp_tools_loaded = False
        
    async def load_mcp_tools(self):
        if not self.mcp_tools_loaded and self.mcp_client:
            try:
                mcp_tools = await get_mcp_tools(self.mcp_client)
                if mcp_tools:
                    self.tools.extend(mcp_tools)
                    self.agent = AgentRunner.from_llm(
                        llm=self.llm,
                        tools=self.tools,
                        verbose=True
                    )
                    logger.info(f"load {len(mcp_tools)} tools")
                    self.mcp_tools_loaded = True
            except Exception as e:
                logger.error(f"load tool error: {e}")
        
    async def chat(self, message: str) -> str:
        try:
            if not self.mcp_tools_loaded:
                await self.load_mcp_tools()
            
            logger.info(f"user input: {message}")
            user_message = ChatMessage(role=MessageRole.USER, content=message)
            
            response = await self.agent.achat(message)
            logger.info(f"Agent response: {response}")
            return str(response)
            
        except Exception as e:
            error_msg = f"error: {e}"
            logger.error(error_msg)
            return error_msg
    

async def main():
    try:
        async with mcp_mqtt.MqttTransportClient(
            "test_client",
            auto_connect_to_mcp_server=True,
            on_mcp_server_discovered=on_mcp_server_discovered,
            on_mcp_connect=on_mcp_connect,
            on_mcp_disconnect=on_mcp_disconnect,
            mqtt_options=mcp_mqtt.MqttOptions(
                host="broker.emqx.io",
            )
        ) as mcp_client:
            await mcp_client.start()
            await anyio.sleep(3)
            
            agent = ConversationalAgent(mcp_client)
            
            print("input 'exit' or 'quit' exit")
            print("input 'tools' show available tools")
            print("="*50)
            
            while True:
                try:
                    user_input = input("\nuser: ").strip()
                    
                    if user_input.lower() in ['exit', 'quit']:
                        break
                    
                    if user_input.lower() == 'tools':
                        print(f"available tools: {len(agent.tools)}")
                        for tool in agent.tools:
                            tool_name = getattr(tool.metadata, 'name', str(tool))
                            tool_desc = getattr(tool.metadata, 'description', 'No description')
                            print(f"- {tool_name}: {tool_desc}")
                        continue
                    
                    if not user_input:
                        continue
                    
                    response = await agent.chat(user_input)
                    print(f"\nAgent: {response}")
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"error: {e}")
                    
    except Exception as e:
        print(f"agent init error: {e}")
        

if __name__ == "__main__":
    anyio.run(main)

```

上述代码基于 [MCP over MQTT Python SDK](https://github.com/emqx/mcp-python-sdk) 实现。

首先，初始化 MCP Client 并连接到 MQTT Broker（请将其中的 Broker 地址替换为你申请的 EMQX Serverless 实例地址）。客户端会自动发现并连接到已注册的 MCP Server。

随后，代码将 MCP Server 中注册的工具封装为 LlamaIndex 可调用的函数接口，供 LLM 使用。同时，还实现了一个简易的对话示例，用于展示可用工具列表及 LLM 的推理与调用过程。

- 注意替换 **api_key** 为 SiliconFlow 官网申请的 API 密钥。
- LlamaIndex 已经封装好了很多的大模型调用，可以参考 [LlamaIndex 支持的 LLM 文档](https://docs.llamaindex.ai/en/stable/api_reference/llms/)获取更多信息。

### ESP32 程序运行和部署

```shell
# ESP32 程序编译以及烧录
$ idf.py build & idf.flash
# ESP32 监控设备输出
$ idf.py monitor

# 运行 Agent 代码，使用 uv 运行
$ uv run agent.py
```

### 云端 MCP Client 展示可用 MCP 工具

```
# 运行 agent.py 后，先输入任意内容，触发 Agent 更新连接的 MCP Server 信息
# 然后输入 tools 查看可用的 MCP Tools

2025-08-06 02:29:39,958 - Agent response: Hello! How can I assist you today?

Agent: Hello! How can I assist you today?

user: tools
available tools: 1
- mcp_set_volume: Set the volume of the device, range 0 to 100
```

如上述所示，查询到一个 Tool，在 ESP32 上提供的调整设备的音量的工具。

### **示例对话 1：模糊控制**

> 用户：设备声音太小了
> LLM：调用 `set_volume(80)`
> ESP32：音量已调高

**Agent 端日志输出：**Agent 识别到用户的意图，调用 set_volume 调整音量到 80。

```
user: 设备声音太小了
2025-08-06 02:37:29,134 - user input: 设备声音太小了
> Running step 0701ab58-6c7e-41be-8a2e-210eab9b870f. Step input: 设备声音太小了
Thought: The current language of the user is Chinese. I need to use a tool to adjust device volume since they reported it's too low.
Action: mcp_set_volume
Action Input: {'kwargs': AttributedDict([('volume', 80)])}
2025-08-06 02:38:24,926 - Got msg from session for server_id: esp32-demo-server-client, msg: root=JSONRPCRequest(method='tools/call', params={'name': 'set_volume', 'arguments': {'kwargs': {'volume': 80}}}, jsonrpc='2.0', id=3)
2025-08-06 02:38:25,076 - Received message on topic $mcp-rpc/4d75d589169a41849fb86b51953110e3/esp32-demo-server-client/ESP32 Demo Server: {"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"Volume set successfully"}]}}
2025-08-06 02:38:25,079 - Sending msg to session for server_id: esp32-demo-server-client, msg: root=JSONRPCResponse(jsonrpc='2.0', id=3, result={'content': [{'type': 'text', 'text': 'Volume set successfully'}]})
Observation: Volume set successfully
> Running step 71688059-5007-4087-84e1-a98993000ff7. Step input: None
Thought: The user reported that the device sound is too low. I've successfully increased the volume to 80. Now I can respond directly in Chinese without further tools.
Answer: 已成功将设备音量调整到80，请检查是否合适。如果还需要进一步调整，请随时告诉我！
```

**ESP32 端日志输出：**ESP32 接收到 set_volume 的工具调用，并把音量调整为 80。

```
I (503477) mcp_server: MCP client initialized: 4d75d589169a41849fb86b51953110e3
I (503487) mcp_server: MCP client initialized: 4d75d589169a41849fb86b51953110e3
I (503747) mcp_server: tools/list request received from $mcp-rpc/4d75d589169a41849fb86b51953110e3/esp32-demo-server-client/ESP32 Demo Server
I (508897) mcp_server: tools/list request received from $mcp-rpc/4d75d589169a41849fb86b51953110e3/esp32-demo-server-client/ESP32 Demo Server
I (585187) mcp_server: tools/call request received from $mcp-rpc/4d75d589169a41849fb86b51953110e3/esp32-demo-server-client/ESP32 Demo Server
I (585187) MAX98357: Set volume to 80%, 0
I (585197) mcp server: Setting volume to: 80%
```

### 示例对话2：多轮对话

为了支持“声音有点大”这类模糊指令，需要 LLM 保持对话上下文，设置正确的参数进行调整。

- 框架记住上次调整的音量是 80；
- 当前语义推导为调整 -15；
- 最终调用 `set_volume(65)`。

**Agent 输出：**Agent 识别到用户意图，调整音量为 65，并调用 set_volume 调整音量。

```
user: 声音有点大了
2025-08-06 02:38:58,092 - user input: 声音有点大了
> Running step be73cc62-e732-4209-8421-2bccdd09cd70. Step input: 声音有点大了
Thought: The current language of the user is Chinese. I need to adjust the volume lower since the user mentioned it's a bit loud. I'll decrease it from the previous setting (80) to a more comfortable level.
Action: mcp_set_volume
Action Input: {'kwargs': AttributedDict([('volume', 65)])}
2025-08-06 02:39:40,075 - Got msg from session for server_id: esp32-demo-server-client, msg: root=JSONRPCRequest(method='tools/call', params={'name': 'set_volume', 'arguments': {'kwargs': {'volume': 65}}}, jsonrpc='2.0', id=4)
2025-08-06 02:39:40,236 - Received message on topic $mcp-rpc/4d75d589169a41849fb86b51953110e3/esp32-demo-server-client/ESP32 Demo Server: {"jsonrpc":"2.0","id":4,"result":{"content":[{"type":"text","text":"Volume set successfully"}]}}
2025-08-06 02:39:40,237 - Sending msg to session for server_id: esp32-demo-server-client, msg: root=JSONRPCResponse(jsonrpc='2.0', id=4, result={'content': [{'type': 'text', 'text': 'Volume set successfully'}]})
Observation: Volume set successfully
```

**ESP32 端打印的日志内容：**ESP32 设备接收到 set_volume 调用，并把音量调整为 65。

```
I (660347) mcp_server: tools/call request received from $mcp-rpc/4d75d589169a41849fb86b51953110e3/esp32-demo-server-client/ESP32 Demo Server
I (660357) MAX98357: Set volume to 65%, 0
I (660357) mcp server: Setting volume to: 65%
```

您也可以试试其他模糊的对话方式，充分了解一下 LLM 对于自然语言的理解，以及把语义理解转换为工具调用的能力。

恭喜你，完成了本次任务：使用 LLM 实现用自然语言对设备进行控制。

## 下篇预告

通过本篇内容，我们打通了自然语言控制的完整路径：LLM 理解并调用部署在 ESP32 设备上的 MCP 工具，MCP 将调用转为 MQTT 指令发送给硬件设备，智能设备响应并执行对应指令。

下一篇中，我们将为智能硬件设备引入语音能力，结合语音识别和语音合成等第三方服务，探索如何在 ESP32 中实现真正的自然语音对话。

## 资源

- 硅基流动：[硅基流动 SiliconFlow - 致力于成为全球领先的 AI 能力提供商](https://siliconflow.cn/)  
- 本文相关源码：https://github.com/mqtt-ai/esp32-mcp-mqtt-tutorial/tree/main/samples/blog_3 



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
