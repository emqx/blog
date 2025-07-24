## **AI + IoT 的具象化：真正“懂你”的情感陪伴智能体**

智能硬件的发展经历了几个阶段：从最初的“能联网”，到后来“能听你说话”，再到今天，我们希望它不仅能理解你的话，还能回应你，甚至陪伴你。想象以下的几个场景：

- 下班回家，它主动问候你：“今天看起来有点疲惫，要不要帮你调暗灯光，放点轻音乐？”
- 孩子和它聊天，它能用不同角色的声音演绎小故事。
- 打开摄像头，它看看你的穿搭，并幽默回应：“今天这身很有气质！”

这并非只存在于科幻作品中，而是大模型（LLM）+ 多模态 AI + IoT 技术结合的必然趋势。

传统 IoT 设备大多依赖“命令式控制”，即系统通过硬编码或者预置规则的方式来对设备进行控制，无法智能感知设备状态的变化。而未来的设备将迈向语义交互和情感陪伴。情感陪伴智能体，正是这一趋势的缩影。

### **该系列文章适合谁？**

如果你符合以下任意一种特征，这个系列就是为你准备的：

- 智能硬件开发工程师：想探索 AI 如何赋能 IoT
- 嵌入式/物联网开发者：对接 AI 服务，实现语音、视觉交互
- 硬件发烧友 / 创客：想 DIY 一个“有灵魂”的智能小助手
- AI 应用开发者：希望从云端走向硬件，打通端到端体验

如果你曾经做过智能家居、机器人、AI 助手项目，这个系列能帮你提升到一个全新的交互层级。

### **背景知识要求**

别担心，你不需要成为全栈大神，但以下知识会让你更轻松：

- 硬件开发基础：会烧写 ESP32 程序（ESP-IDF）
- 网络通信基础：了解 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)的基本概念（发布/订阅）
- Python 基础：后续 LLM 和云端应用用到 Python SDK
- AI 应用概念（选修）：知道什么是大语言模型（LLM）、ASR（语音识别）、TTS（语音合成）

不会这些也没关系，系列文章会逐步讲解，并提供开箱即用的示例。

### **为什么要自己做？**

- 商用产品封闭无法定制，而我们希望用最经济、最简单的方式，构建一个功能强大的情感陪伴智能体
- 借助开源硬件（ESP32）+ 云端 AI 接口，个人开发者也能打造接近厂商级体验的智能体
- 这个过程不仅能让你玩出酷炫的 AI 硬件，还能深入理解 AI + IoT 的架构设计与实践

### **本系列教程的目标**

通过渐进式教程，带你从零搭建一个情感陪伴智能体，它将具备：

- 语音交互：听懂你的话，并用自然语气回答
- 设备控制：通过语义指令调节屏幕亮度、音量等
- 个性化人格：设定性格、喜好，具备一定记忆能力
- 视觉理解：识别图像内容，并生成趣味反馈

最终，你将实现这样的体验：

- “嘿，把屏幕调暗一点” → *“好的，已经帮你调暗，舒服点了吧？”*
- “你看一下我，觉得怎么样？” → 智能体拍摄照片并上传 → *“呦，今天这么好看，是想迷死谁啊？”*

### **本系列教程路线图**

| 篇章 | 功能                                                   | 难度 |
| :--- | :----------------------------------------------------- | :--- |
| 1    | 整体介绍：背景 + 环境准备 + 设备上线                   | ★    |
| 2    | 从“命令式控制”到“语义控制”：MCP over MQTT 封装设备能力 | ★★   |
| 3    | 接入 LLM，实现“自然语言 → 设备控制”                    | ★★   |
| 4    | 语音 I/O：麦克风数据上传 + 语音识别 + 语音合成回放     | ★★★  |
| 5    | 人格、情感、记忆：从“控制器”到“陪伴体”                 | ★★★  |
| 6    | 给智能体增加“眼睛”：图像采集 + 多模态理解              | ★★★  |

## **技术栈一览**

- ESP32：低成本 + Wi-Fi/Bluetooth + 丰富外设，智能硬件项目首选
- MQTT 协议：轻量、实时、跨平台，IoT 标配
- MCP (Model Context Protocol) Over MQTT
  - 让 LLM 通过“工具调用”直接控制硬件
  - 设备服务以“能力声明”方式注册，AI 调用自然、标准
- AI 能力：
  - LLM：处理自然语言、控制意图
  - ASR/TTS：语音识别与合成
  - VLM（多模态大模型）：视觉理解，生成有趣描述
- 云端服务：
  - EMQX Serverless，或者本地安装的 EMQX
  - 开源 AI 框架：LangChain / LangFlow / LlamaIndex，本文选择的是 LlamaIndex

一句话概括架构：ESP32 做“硬件执行器”，云端 AI 做“大脑”，MQTT + MCP 做“神经通路”。

## **硬件清单**

为完成本教程所有相关的功能，推荐准备以下硬件：

- ESP32-S3-DevKitC（熟悉开发版的可以选择其他型号）
- INMP441 麦克风模块
- 功放 MAX98357A
- 喇叭 2-3W
- IIC 接口的液晶显示器
- OV2640 摄像头模块
- 400 孔面包板以及杜邦线一套

## **总体系统架构设计**

![image.png](https://assets.emqx.com/images/2d0152b47bd29e2d883575bd7c9c2c67.png)

- 硬件层：ESP32 + 麦克风 + 扬声器 + 摄像头 + 屏幕。
- 连接层：[MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)（EMQX） + MCP 协议。
- AI 服务层：自然语言处理、语音合成、视觉识别、人格逻辑

AI 服务方面，本文选择了阿里云的语音识别，语音合成，大模型以及多模态大模型的服务。

## **第一个目标：让设备上线**

本实践主要是为了把 ESP32 设备连接到服务器，并发送消息

![image.png](https://assets.emqx.com/images/ad358c414d6748ea4883bef28151e20a.png)

如图所示，

1. ESP32 连接 [EMQX Serveless](https://www.emqx.com/zh/cloud/serverless-mqtt) 服务
2. MQTTX（作为服务端的应用）也连接到 EMQX Serveless，订阅主题  `emqx/esp32`
3. ESP32 发布消息 `Hi EMQX I'm ESP32 ^^` 到主题 `emqx/esp32`
4. MQTTX 接收到上述消息

**硬件：**

- ESP32 开发板（推荐 DevKitC，带 USB 转串口）
- USB 数据线（注意必须支持数据传输）

**软件 ：**

1. **ESP-IDF**
   - 安装 ESP-IDF 
   - 安装 ESP-IDF 依赖，参考官方文档 - [ESP-IDF Getting Started | Espressif Systems](https://idf.espressif.com/)
   - 安装 [VS Code](https://code.visualstudio.com/)
   - VS Code 中安装 ESP-IDF 扩展
   - 参考 [配置开发环境](https://github.com/espressif/vscode-esp-idf-extension)
2. MQTT 客户端测试工具：[MQTTX: Your All-in-one MQTT Client Toolbox](https://mqttx.app/) 

**驱动注意：**

- Windows 用户可能需要安装 CP210x 或 CH340 串口驱动
- macOS/Linux 通常即插即用

### **注册 EMQX Serverless**

MQTT 作为智能体和云端大模型的传输协议，后续所有功能（语音、视觉、AI 控制）都依赖它与云端实时通信。为降低难度，避免本地安装和配置等复杂过程，推荐读者使用 EMQX MQTT 云服务。

1. 访问 EMQX Serverless - [安全、可伸缩的 Serverless MQTT 消息服务。](https://www.emqx.com/zh/cloud/serverless-mqtt)
2. 按照网站的提示创建，注册账号，创建 MQTT 服务实例，获取以下信息：
   - Broker 地址
   - 用户名 / 密码
   - 端口号（MQTT over TLS 推荐 8883）

> 注意：您也可以根据自己的情况，在本机或者内网中部署一个 EMQX Broker，这样做的好处是可以降低 ESP32 与远程服务器之间的网络时延 - [通过 Docker 运行 EMQX | EMQX 文档](https://docs.emqx.com/zh/emqx/latest/deploy/install-docker.html) 

![image.png](https://assets.emqx.com/images/1bbfb54fb08a2c9d9dbcb69daf071fee.png)

### **编译 & 烧录 ESP32 程序**

#### 代码目录

```
| - CMakeLists.txt
| - sdkconfig
| - main
| --- main.c
| --- CMakeLists.txt
```

#### CMakeLists.txt

```
# The following lines of boilerplate have to be in your project's
# CMakeLists in this exact order for cmake to work correctly
cmake_minimum_required(VERSION 3.16)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(main)
```

#### sdkconfig

```
CONFIG_MQTT_PROTOCOL_5=y
CONFIG_ESP_WIFI_SOFTAP_SUPPORT=n
```

#### main/main.c

```c
#include <stdio.h>

#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"
#include "freertos/task.h"

#include "esp_log.h"
#include "esp_mac.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "mqtt_client.h"
#include "nvs_flash.h"

#define PIN_NUM_SCLK 21
#define PIN_NUM_MOSI 47
#define PIN_NUM_MISO -1

#define LCD_H_RES 240

static EventGroupHandle_t s_wifi_event_group;
static int                s_retry_num = 0;
static esp_mqtt_client_handle_t client;

static const char *WIFI_SSID     = "wifi_ssid";
static const char *WIFI_PASSWORD = "wifi_password";
static const char *MQTT_BROKER =
    "mqtts://xxyyzzz:8883";
static const char *username = "user";
static const char *password = "password";
static const char *cert =
    "-----BEGIN CERTIFICATE-----\n"
    "MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh\n"
    "MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3\n"
    "d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD\n"
    "QTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT\n"
    "MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j\n"
    "b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG\n"
    "9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB\n"
    "CSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97\n"
    "nh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt\n"
    "43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P\n"
    "T19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4\n"
    "gdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO\n"
    "BgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR\n"
    "TLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw\n"
    "DQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr\n"
    "hMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg\n"
    "06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF\n"
    "PnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls\n"
    "YSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk\n"
    "CAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=\n"
    "-----END CERTIFICATE-----";

static void event_handler(void *arg, esp_event_base_t event_base,
                          int32_t event_id, void *event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT &&
               event_id == WIFI_EVENT_STA_DISCONNECTED) {
        if (s_retry_num < 5) {
            esp_wifi_connect();
            s_retry_num++;
            ESP_LOGI("wifi sta", "retry to connect to the AP");
        } else {
            xEventGroupSetBits(s_wifi_event_group, BIT1);
        }
        ESP_LOGI("wifi sta", "connect to the AP fail");
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t *event = (ip_event_got_ip_t *) event_data;
        ESP_LOGI("wifi sta", "ip: " IPSTR ", mask: " IPSTR ", gateway: " IPSTR,
                 IP2STR(&event->ip_info.ip), IP2STR(&event->ip_info.netmask),
                 IP2STR(&event->ip_info.gw));
        s_retry_num = 0;
        xEventGroupSetBits(s_wifi_event_group, BIT0);
    }
}

int wifi_init_sta(void)
{
    s_wifi_event_group = xEventGroupCreate();

    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    esp_netif_create_default_wifi_sta();
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;

    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        WIFI_EVENT, ESP_EVENT_ANY_ID, &event_handler, NULL, &instance_any_id));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(
        IP_EVENT, IP_EVENT_STA_GOT_IP, &event_handler, NULL, &instance_got_ip));

    wifi_config_t wifi_config = {
        .sta = {
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
            .sae_pwe_h2e = WPA3_SAE_PWE_BOTH,
            .sae_h2e_identifier = "",
        },
    };
    strcpy((char *) wifi_config.sta.ssid, WIFI_SSID);
    strcpy((char *) wifi_config.sta.password, WIFI_PASSWORD);
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI("wifi sta", "wifi init finished.");

    EventBits_t bits = xEventGroupWaitBits(s_wifi_event_group, BIT0 | BIT1,
                                           pdFALSE, pdFALSE, portMAX_DELAY);

    if (bits & BIT0) {
        ESP_LOGI("wifi sta", "connected to ap SSID: %s", CONFIG_WIFI_SSID);
    } else if (bits & BIT1) {
        ESP_LOGI("wifi sta", "Failed to connect to SSID: %s", CONFIG_WIFI_SSID);
    } else {
        ESP_LOGE("wifi sta", "UNEXPECTED EVENT");
    }

    return 0;
}

static void mqtt5_event_handler(void *handler_args, esp_event_base_t base,
                                int32_t event_id, void *event_data)
{
    char *TAG = "mqtt5";
    ESP_LOGD(TAG, "Event dispatched from event loop base=%s, event_id=%" PRIi32,
             base, event_id);
    esp_mqtt_event_handle_t  event  = event_data;
    esp_mqtt_client_handle_t client = event->client;
    int                      msg_id;

    ESP_LOGD(TAG, "free heap size is %" PRIu32 ", minimum %" PRIu32,
             esp_get_free_heap_size(), esp_get_minimum_free_heap_size());
    ESP_LOGI(TAG, "event_id=%" PRIi32, event_id);

    switch ((esp_mqtt_event_id_t) event_id) {
    case MQTT_EVENT_CONNECTED:
        msg_id = esp_mqtt_client_publish(client, "emqx/esp32",
                                         "Hi EMQX I'm ESP32 ^^", 0, 1, 0);
        ESP_LOGI(TAG, "sent publish successful, msg_id=%d", msg_id);
        break;
    case MQTT_EVENT_DISCONNECTED:
    case MQTT_EVENT_SUBSCRIBED:
    case MQTT_EVENT_PUBLISHED:
    case MQTT_EVENT_DATA:
        break;
    case MQTT_EVENT_UNSUBSCRIBED:
        esp_mqtt_client_disconnect(client);
        break;
    case MQTT_EVENT_ERROR:
        ESP_LOGI(TAG, "MQTT5 return code is %d",
                 event->error_handle->connect_return_code);
        if (event->error_handle->error_type == MQTT_ERROR_TYPE_TCP_TRANSPORT) {
            ESP_LOGI(TAG, "Last errno string (%s)",
                     strerror(event->error_handle->esp_transport_sock_errno));
        }
        break;
    default:
        ESP_LOGI(TAG, "Other event id:%d", event->event_id);
        break;
    }
}

int mqtt_init(void)
{
    esp_mqtt_client_config_t mqtt5_cfg = {
        .broker.address.uri                  = MQTT_BROKER,
        .session.protocol_ver                = MQTT_PROTOCOL_V_5,
        .network.disable_auto_reconnect      = true,
        .credentials.username                = username,
        .credentials.authentication.password = password,
        .broker.verification.certificate     = cert,
    };

    client = esp_mqtt_client_init(&mqtt5_cfg);
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID,
                                   mqtt5_event_handler, NULL);
    esp_mqtt_client_start(client);
    return 0;
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

    wifi_init_sta();
    mqtt_init();

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(3000));
        int msg_id = esp_mqtt_client_publish(client, "emqx/esp32",
                                             "Hi EMQX I'm ESP32 ^^", 0, 1, 0);
        ESP_LOGI("mqtt", "sent publish successful, msg_id=%d", msg_id);
    }
}
```

#### main/CMakeLists.txt

```
idf_component_register(SRCS "main.c"
                    PRIV_REQUIRES mqtt esp_wifi nvs_flash
                    INCLUDE_DIRS ".")
```

**修改 WIFI 以及 MQTT 服务相关配置 main/main.c 如下所示，替换为你自己的配置信息，**

- Wi-Fi 名称、密码
- 在 Serverless 上申请的地址，以及用户名和密码

```c
static const char *WIFI_SSID     = "wifi_ssid";
static const char *WIFI_PASSWORD = "wifi_password";
static const char *MQTT_BROKER =
    "mqtts://xxyyzzz:8883";
static const char *username = "user";
static const char *password = "password";
```

#### 编译代码并且烧录到 esp32 中  

```
idf.py build 
idf.py flash monitor
```

烧录完成后，ESP32 将每隔 3 秒发送 `Hi EMQX I'm ESP32 ^^` 到 `emqx/esp32` 主题。

### **验证**

打开 MQTTX，配置 MQTT 连接，如下图所示，

- Host 中填入你在 EMQX Serverless 申请的服务地址
- Username 和 Password 中输入连接的用户名和密码

![image.png](https://assets.emqx.com/images/d12a76daacc575471fc45eea5e74a3c9.png)

连接成功后，添加一个新的订阅，在主题中输入 `emqx/esp32`，如果看到以下内容：

![image.png](https://assets.emqx.com/images/a67b868b203bb1af0f1b9b874883f9fc.png)

恭喜！你的设备已经成功接入 MQTT。

**问题诊断：如果收不到消息，我该怎么办？**

可以登录到 EMQX Serverless 上看一下有没有你连接上来的 ESP32 设备。

- 如果没有，大概率是你的设备端有问题。
  - 再次检查一下源代码中指定的地址、用户名和密码。
  - 确定网络状态，以及 Wi-Fi 信息
- 如果有，那么可能是你的 MQTTX 指定的连接或者主题不对。
  - 再次检查一下 MQTTX 中指定的地址、用户名和密码。

## **下篇预告**

在下一篇中，我们将让 ESP32 “暴露”自己的控制能力，通过 MCP 协议注册亮度、音量调节接口，让 MCP 的客户端 Python 应用可以访问和列出所有在 ESP32 上安装的工具列表。

## **资源**

- MQTT 协议相关的基本材料：[开发者指南 | EMQX 文档](https://docs.emqx.com/zh/emqx/latest/connect-emqx/developer-guide.html) 
- EMQX Serverless 免费注册 - [安全、可伸缩的 Serverless MQTT 消息服务。](https://www.emqx.com/zh/cloud/serverless-mqtt) 
- MQTT 客户端工具：[MQTTX: Your All-in-one MQTT Client Toolbox](https://mqttx.app/)
- ESP32 官方网站：https://www.espressif.com.cn/en/products/socs/esp32



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
