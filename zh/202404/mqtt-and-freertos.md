## 什么是 RTOS？

在 2024 年的今天，我想没有人会对操作系统感到陌生，毕竟我们随时随地都能接触到各种操作系统，从个人电脑上的 Windows、macOS、Linux，到智能手机上的 iOS、Android 等等。但还有一种操作系统，虽然它同样遍布在我们的日常生活中，但很少会有人意识到它的存在，那就是实时操作系统（RTOS）。

顾名思义，实时操作系统与其他操作系统的核心区别就在于它的实时性。想象一下，如果车载操作系统从检测到严重撞击，到它实际控制安全气囊弹出的时间，可能相隔几毫秒到几十毫秒不等的话，那对车上人员来说，将是多么严重的安全风险。同样，航空航天、医疗器械、工业控制，都对任务的响应及时性有着非常高的要求，这都是只有实时操作系统才能够满足的。

## 什么是 FreeRTOS？

[FreeRTOS](https://freertos.org/)，就是一个开源的面向微控制器和小型微处理器的实时操作系统。它支持 ARM、PIC、x86 等多种处理器架构，支持抢占式和时间片轮询调度，支持互斥量、信号量等多种同步和通信机制。成熟且开放的[源码](https://github.com/FreeRTOS/FreeRTOS)、丰富的文档以及活跃的社区，都促使人们选择 FreeRTOS 来开发自己的嵌入式实时应用。

## 使用 MQTT 与 FreeRTOS 构建应用

作为一个轻量、紧凑的 RTOS，FreeRTOS 非常适合在资源有限的物联网设备中使用，比如工业控制系统、智能家居、机器人控制等。

这类物联网应用除了需要实现本地的实时控制逻辑，通常还需要具备与外部系统通信协作的能力，比如同步设备最新状态、响应远程指令等。而基于发布订阅的 MQTT 协议往往是这一场景下的最优选择。

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 的异步通信使通信双方得以解耦，使它们可以更专注在自身业务逻辑的实现上。此外，MQTT 支持组播、广播等多种消息分发模式，支持按需设置消息可靠性，允许设备短暂离线而不会丢失消息，支持为客户端设置遗嘱，这些特性极大地提升了应用开发的效率。

如果你还未尝试过同时使用 FreeRTOS 和 MQTT 构建应用，请继续阅读。本文将通过一个 Demo 为你展示如何在 FreeRTOS 中使用 MQTT 收发消息并与其他实时任务协作。

## Demo 介绍

在这个 Demo 中，我们将通过 MQTT 协议实现远程控制 RGB LED 的开关、色调、饱和度、亮度，以及在闪烁和彩虹循环两种显示模式之间切换，并通过 MQTT 协议接收设备返回的最新 LED 运行状态以便了解命令是否被正确执行。

![流程图](https://assets.emqx.com/images/e1f260ae986afa02d4ff4932c0674eba.png)

为了达到这一目标，我们在 FreeRTOS 中实现了一个 MQTT 事件回调函数用于维护连接、解析并处理 MQTT 消息；一个 LED 任务根据 MQTT 事件回调函数的通知更改 LED 的运行状态，并发布指示 LED 最新状态的 MQTT 消息；一个 Wi-Fi 事件回调函数实现 Wi-Fi 连接。

LED 任务可以被替换为其他任何实际应用，例如相机云台控制应用，无人机姿态控制应用等等。本 Demo 主要展示了 FreeRTOS 中 MQTT 库的基础用法，比如如何构建 MQTT 连接和收发消息，以及如何借助 FreeRTOS 的队列机制将解析后的指令同步给其他任务执行。

## 准备工作

### 硬件准备

在这个 Demo 中，我们需要用到一块集成了 2.4GHz Wi-Fi 通信模块的 ESP32 开发板，以便我们以无线方式连接到互联网。

我使用的是一块集成了 ESP32-S3-WROOM-1-N8R8 模组的开发板，你可以使用其他 ESP32 芯片来代替，例如 ESP32-S2 或者 ESP32-C3，S3 的主要变化是增加了双核和蓝牙支持。本示例已经通过 ESP-IDF 的 `CONFIG_FREERTOS_UNICORE` 选项启用了单核模式，可以直接运行在单核 CPU 上。

另外我们还需要用到一个由 WS2812 系列芯片（WS2812、WS2812B、WS2812C 均可）驱动的 RGB LED 光源，我们将使用 ESP32 的 RMT 外设来控制这个 LED 光源。

我使用的开发板上默认搭载了一个 WS2812B 驱动的 RGB LED，如果你的开发板没有这样的 LED，你可以外接一个 LED 模块，或者直接对 LED 任务代码进行一些修改，将其改为在串口打印相应的内容。

### 软件准备

想要开发和运行这个 Demo，我们需要用到以下软件：

1. [ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/index.html) v5.2.1，乐鑫官方推出的用于 ESP32 系列芯片应用开发的开发框架。推荐在 IDE 中安装 ESP-IDF，我使用的是 VS Code。
2. [EMQX](https://www.emqx.com/)，一个企业级 MQTT 平台，推荐使用 [EMQX Cloud Serverless](https://www.emqx.com/zh/cloud/serverless-mqtt)，免去自行部署服务器的步骤。
3. [MQTTX](https://mqttx.app/zh)，MQTT 客户端工具，用于向 ESP32 发送 LED 指令和接收 LED 状态。

EMQX Cloud Serverless 和 MQTTX 的部署非常简单，这里不再赘述，ESP-IDF 推荐以 IDE 扩展的方式安装，大致的安装步骤为：

1. 如果你的操作系统是 Linux 或 macOS，首先需要安装 Python3、CMake、Ninja 等依赖，详情可参考 [Step 1. Install Prerequisites](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/linux-macos-setup.html#step-1-install-prerequisites)。
2. 下载并安装 [Visual Studio Code](https://code.visualstudio.com/)。
3. 在 VS Code 的 Extensions 扩展视图中搜索 ESP-IDF 并安装。
4. 在 VS Code 的命令面板（组合键 Shift+Command+P 或 Shift+Ctrl+P）中选择 `ESP-IDF: Configure ESP-IDF Extension`，进入 ESP-IDF 的设置向导。
5. 选择 EXPRESS 设置模式，然后依次选择要下载的 ESP-IDF 版本、ESP-IDF 工具安装路径以及本地的 Python 可执行文件路径，最后点击安装并等待安装完成即可。

详细的安装步骤可参考 [ESP-IDF 官方文档](https://github.com/espressif/vscode-esp-idf-extension/blob/master/docs/tutorial/install.md)。

## Demo 代码解析

完整的示例代码已经上传到 GitHub，您可以在[此处](https://github.com/emqx/bootcamp/tree/main/mqtt-and-rtos/freertos-demo)下载。

### 目录结构

示例代码的目录结构如下：

```1c
|-- components
    |-- esp-mqtt
    |-- led_strip
|-- main
    |-- CMakeLists.txt
    |-- demo.c
    |-- demo.h
    |-- emqxsl_ca.crt
    |-- Kconfig.projbuild
|-- CMakeLists.txt
|-- sdkconfig
|-- sdkconfig.defaults
```

#### components 目录

`components` 目录下的 `esp-mqtt` 和 `led_strip` 组件均来自乐鑫官方。但在本示例中，这两个组件的默认行为无法满足我们的要求，所以我们直接将它们拷贝到 `components` 目录，修改后作为项目组件使用。

#### main 目录

`main` 目录与项目根目录下的 `CMakeLists.txt` 定义了项目和组件的构建规则，详情可参考 [ESP-IDF 官方文档](https://docs.espressif.com/projects/esp-idf/en/v5.2.1/esp32/api-guides/build-system.html#project-cmakelists-file)。

`demo.c` 和 `demo.h` 包含了本示例的所有主要代码，在下文中我们将详细介绍。

`emqx_sl_ca.crt` 是与 EMQX Cloud Serverless 建立 TLS 连接必需的 CA 证书，可以在 Serverless 部署的概览页面中下载：

![EMQX Cloud 部署信息](https://assets.emqx.com/images/b6028aa68dd40e559b547717cbddf2a1.png)

为了在代码中使用这个 CA 证书，我们可以在顶层的 `CMakeLists.txt` 中通过 `target_add_binary_data` 函数将其嵌入到固件中：

```makefile
target_add_binary_data(demo.elf "main/emqxsl_ca.crt" TEXT)
```

`target_add_binary_data` 函数不识别文件名中的短划线，所以我们需要手动将 CA 证书文件名中的短划线改为下划线。

最终我们可以在代码中通过以下方式来访问嵌入的文件内容：

```c
extern const uint8_t server_cacertificate_start[]  asm("_binary_emqxsl_ca_crt_start");
extern const uint8_t server_cacertificate_end[]  asm("_binary_emqxsl_ca_crt_end");
```

本示例也提供了另一种使用 CA 证书的方法，该方法将在后面的 **运行 Demo** 章节中介绍。

`Kconfig.projbuild` 包含了当前项目的自定义配置项。本示例中的 `Kconfig.probuild` 文件主要定义了 Wi-Fi SSID、Wi-Fi 密码、MQTT 服务器地址等配置项。

除此之外，组件配置在组件自己根目录下的 Kconfig 文件中定义，然后提供给依赖该组件的项目或其他组件使用，例如 `esp-mqtt` 组件就为我们提供了 MQTT 任务优先级、是否启用 MQTT 5.0 支持等配置项。

我们可以执行 `idf.py menuconfig` 或者在 VS Code 的命令面板中选择 `ESP-IDF: SDK Configuration editor (Menuconfig)` 进入配置菜单，该菜单包含了所有可修改的配置项。更改这些配置项的值，即可调整应用代码的行为。

#### sdkconfig 与 sdkconfig.defaults

更改后的完整配置将存储在 `sdkconfig` 文件中。`sdkconfig` 通常都是自动生成，不推荐手动修改。

最后的 `sdkconfig.defaults` 是一个可选文件。项目构建时将自动创建 `sdkconfig` 文件，并使用 `sdkconfig.defaults` 中的配置覆盖 `Kconfig` 和 `Kconfig.projbuild` 中定义的默认值。

本示例中的 `sdkconfig.defaults` 记录了保证本示例正确构建和运行的必要配置改动：

```ini
# 启用对 MQTT 5.0 的支持
CONFIG_MQTT_PROTOCOL_5=y
# 启用单核模式，以便在 ESP32-S2 等单核平台上运行
CONFIG_FREERTOS_UNICORE=y
```

当然，如果你不希望修改 `Kconfig.projbuild` 后重新生成的 `sdkconfig` 总是会丢失之前的配置改动，也可以将这些改动放入 `sdkconfig.defaults`。

Kconfig、sdkconfig 的详细介绍，可以参考 ESP-IDF 官方文档的 [构建系统](https://docs.espressif.com/projects/esp-idf/en/v5.2.1/esp32/api-guides/build-system.html) 章节。

### 功能实现

![功能实现](https://assets.emqx.com/images/e09749a7beac9b194b313a53500a5156.png)

#### 组件 esp-mqtt

`esp-mqtt` 是 ESP-IDF 的一个内部组件，它提供了一个 MQTT 客户端的实现，支持 MQTT 3.1.1 与 5.0，支持 TLS 的单双向认证，支持持久会话、完整的 3 个服务质量（QoS）等级等绝大部分的 MQTT 特性。

但由于这个组件对于 Reason Code 的实现还未完全适配 MQTT 5.0，比如它只将 0x80 视为订阅失败，而 MQTT 5.0 事实上提供了更多指示失败原因的 Reason Code。所以本示例修改了 `esp-mqtt/mqtt_client.c` 中的 `deliver_suback` 函数，具体改动如下：

```c
// Before
if ((uint8_t)msg_data[topic] == 0x80) {
// After
if ((uint8_t)msg_data[topic] >= 0x80) {
```

另外，由于 `esp-mqtt` 组件在接收消息前没有将内存清零，所以可能残留上一次的数据导致 `sscanf` 等函数无法正确解析数据。

将有效数据之后的一个字节设置为 `\0` 可以解决这一问题，但可能导致越界访问内存，所以我们需要在初始化时额外多申请一个字节内存，具体改动位于 `esp-mqtt/mqtt_client.c` 中的 `esp_mqtt_client_init` 函数：

```c
// Before
client->mqtt_state.in_buffer = (uint8_t *)malloc(buffer_size);
// After
client->mqtt_state.in_buffer = (uint8_t *)malloc(buffer_size + 1);
```

#### 组件 led_strip

`led_strip` 是 ESP-IDF 提供一个附件组件，它提供了 RMT 和 SPI 两种驱动 WS2812 等可寻址 LED 的方式，并且可以驱动一个灯带上的多个 LED。本示例使用的是 RMT 外设。

修改这一组件代码的原因是，理论上写入 WS2812 芯片的数据顺序应该为 GRB，而实际上我的硬件按照 RGB 的顺序来解析数据，所以我修改了 `led_strip/src/led_strip/rmt/dev.c` 中的 `led_strip_rmt_set_pixel` 函数，具体改动如下：

```c
// Before
rmt_strip->pixel_buf[start + 0] = green & 0xFF;
rmt_strip->pixel_buf[start + 1] = red & 0xFF;
// After
rmt_strip->pixel_buf[start + 0] = red & 0xFF;
rmt_strip->pixel_buf[start + 1] = green & 0xFF;
```

#### demo.c 中的 Wi-Fi 事件回调函数

Wi-Fi 和 MQTT 组件都采用了事件循环，事件循环的本质仍然是队列机制。但在事件循环中，我们只需要实现事件的回调函数，并将该回调函数注册到对应的事件中即可。

Wi-Fi 组件使用默认的事件循环任务，该默认循环任务的优先级为 20。Wi-Fi 组件自身还有一个任务，该任务的优先级默认为较高的 23。由于我们启用了单核模式，所以这些任务都只会在 CPU 核心 0 上运行。

本示例中的 Wi-Fi 事件回调函数 `wifi_event_handler`，仅处理了 `WIFI_EVENT_STA_START`、`WIFI_EVENT_STA_DISCONNECTED` 和 `IP_EVENT_STA_GOT_IP` 这三个事件，实现了 Wi-Fi 的首次连接与断开重连。

事件 `IP_EVENT_STA_GOT_IP` 来自 LwIP 的 TCP/IP 任务，该任务的优先级默认为 18。由于连接到 MQTT 服务器等套接字操作均依赖 IPv4 地址，所以我们需要等待 `IP_EVENT_STA_GOT_IP` 而不是 `WIFI_EVENT_STA_CONNECTED` 事件。

这里我们还用到了事件组，以便阻塞主线流程直到 Wi-Fi 事件回调函数设置了相应的位：

```jboss-cli
else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
    ...
    xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
}
```

一个健壮的网络应用还应当在回调函数中处理其他 Wi-Fi 事件，感兴趣的读者可以参考 ESP-IDF 的 [WiFi 驱动文档](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/wifi.html)。

#### demo.c 中的 MQTT 事件回调函数

MQTT 组件没有创建额外的事件循环任务，MQTT 事件的发布和事件处理程序的调度都在 MQTT 任务中完成，该任务由 `esp_mqtt_client_start` 函数隐式创建，其默认优先级为 5。

本示例中的 MQTT 事件回调函数 `mqtt5_event_handler`，主要处理了 `MQTT_EVENT_CONNECTED`、`MQTT_EVENT_DATA` 和 `MQTT_EVENT_ERROR` 事件。

`MQTT_EVENT_CONNECTED` 事件意味着成功连接，我们可以根据 `event->session_present` 判断是否需要重新订阅主题：

```c
if(event->session_present == false) {
    // Re-subscribe
    for(int i = 0; i < subscriptions->size; i++)
    {
        subscriptions->subscription[i].msg_id = esp_mqtt_client_subscribe(client, (char *)subscriptions->subscription[i].topic, 0);
        subscriptions->subscription[i].subscribed = false;
        ESP_LOGI(TAG, "subscribing to topic=%s, msg_id=%d",
            subscriptions->subscription[i].topic, subscriptions->subscription[i].msg_id);
    }
}
```

然后使用 QoS 为 1 的保留消息与 MQTT 服务器同步最新的 LED 状态：

```c
xSemaphoreTake(s_led_state_lock, portMAX_DELAY);
led_state_t led_state = s_led_state;
xSemaphoreGive(s_led_state_lock);
sync_led_state(client, &led_state);
```

保留消息是 MQTT 的一个重要特性，MQTT 服务器可以为每个主题存储且仅存储一条最新的保留消息，以便它可以交付给未来的订阅者。这可以在异步通信的前提下实现有效的状态同步。

将消息的 QoS 设置为 1 可以确保消息一定到达服务端：

```c
esp_mqtt_client_enqueue(client, TOPIC_STAT_HSB, s_msg, 0, QOS_1, RETAIN, true)
```

虽然 QoS 1 可能导致对端收到重复的消息，但因为本示例发送的状态消息以及收到的命令消息，指示的都是绝对状态，所以重复的消息是可以被接受的。

`MQTT_EVENT_DATA` 表示有消息到达，这里我们实现了一个非常简单的回调机制，即根据消息中的主题调用相应的消息回调函数：

```c
for(int i = 0; i < subscriptions->size; i++) {
    uint16_t len = strlen(subscriptions->subscription[i].topic);
    if(!strncmp(subscriptions->subscription[i].topic, event->topic, len < event->topic_len ? len : event->topic_len)) {
        subscriptions->subscription[i].handler(event->data, event->data_len);
        break;
    }
}
```

本示例实现的消息回调函数的逻辑基本相同，进一步解析消息的 Payload，并创建一个新的 LED 目标状态。该状态指示了 LED 该以何种方式运行，例如色调、饱和度、亮度等等，并通过队列同步给 LED 任务。

`MQTT_EVENT_ERROR` 事件表示发生了错误，本示例的处理比较简单，仅仅通过串口打印了详细的错误原因。

#### demo.c 中的 LED 任务

LED 任务的优先级默认为 4，可以通过 `Demo Configuration` 子菜单中的 `LED task priority` 配置项修改。

LED 任务每次循环都会首先检查队列是否有新的消息到达，如果有新消息到达，则根据该消息调整运行状态，否则继续保持原状态运行。

如果 LED 状态发生改变，则使用 QoS 为 1 的保留消息与 MQTT 服务器同步最新的 LED 状态，并将该状态通过 NVS 库保存到 Flash 中：

```c
store_led_state_in_nvs(handle, &led_state);
sync_led_state(client, &led_state);
```

这样下次上电时我们可以读取 Flash 中存储的 LED 状态，并直接以该状态运行：

```c
get_value_from_nvs(handle, "power", (void *)&s_led_state.power, NVS_TYPE_U8);
get_value_from_nvs(handle, "hue", (void *)&s_led_state.hue, NVS_TYPE_U16);
get_value_from_nvs(handle, "saturation", (void *)&s_led_state.saturation, NVS_TYPE_U8);
get_value_from_nvs(handle, "brightness", (void *)&s_led_state.brightness, NVS_TYPE_U8);
get_value_from_nvs(handle, "mode", (void *)&s_led_state.mode, NVS_TYPE_U8);
get_value_from_nvs(handle, "on_time", (void *)&s_led_state.on_time, NVS_TYPE_U16);
get_value_from_nvs(handle, "off_time", (void *)&s_led_state.off_time, NVS_TYPE_U16);
get_value_from_nvs(handle, "speed", (void *)&s_led_state.speed, NVS_TYPE_U8);
```

### 配置说明

本示例提供了一些自定义配置项（在 `Kconfig.projbuild` 中定义），它们可以在位于配置菜单顶层的 `Demo Configuration` 子菜单中找到。

这些配置项主要与您的运行环境相关，例如 Wi-Fi SSID 与密码、MQTT 服务器地址、LED 对应的 GPIO 引脚等等。

通过修改这些配置项，我们可以快速地让此示例在您的本地环境中运行。

![配置说明](https://assets.emqx.com/images/2268853cb131b2a7bee9e68e1e2b9ac0.png)

### MQTT 消息设计

#### 命令消息

本示例支持远程设置 LED 的开关状态、色调、饱和度、亮度、闪烁间隔以及彩虹模式下的循环速度，因此设计了四种命令消息。命令消息由主题 `cmnd/led/<command>` 和负载 `<param1>,[<param2>,...]` 组成。如果负载中存在多个参数，则参数之间统一使用逗号 `,` 分隔：

##### 1. 控制 LED 开关

**主题**：`cmnd/led/power`

**负载**：`<power>`

**参数说明**：

`<power>` = `on`，打开 LED。

`<power>` = `off`，关闭 LED。

**负载示例**：`on`

##### 2. 设置 LED 色调

**主题**：`cmnd/led/hue`

**负载**：`<hue>`

**参数说明**：

`<hue>` = `0..360`，设置 LED 色调。

**负载示例**：`360`

##### 3. 设置 LED 色调、饱和度与亮度

**主题**：`cmnd/led/hsb`

**负载**：`<hue>,<saturation>,<brightness>`

**参数说明**：

`<hue>` = `0..360`，设置 LED 色调。

`<saturation>` = `0..255`，设置 LED 饱和度。

`<brightness>` = `0..255`，设置 LED 亮度。

**负载示例**：`180,255,255`

##### 4. 设置 LED 的显示模式

**主题**：`cmnd/led/mode`

**负载**：`blink,<on>,<off>` 或 `hue_rainbow,<speed>`

**参数说明**：

`blink`：设置 LED 为闪烁模式。

`hue_rainbow`：设置 LED 为彩虹循环模式。

`<on>` = `0..65535`，设置闪烁模式下 LED 亮起的时长，单位：毫秒。

`<off>` = `0..65535`，设置闪烁模式下 LED 灭掉的时长，单位：毫秒。

`<speed>` = `slow | normal | quick`，设置彩虹循环模式下的循环速度。

**负载示例**：`blink,200,500`，`hue_rainbow,normal`

> 注意在彩虹循环模式下，对 LED 色调、饱和度以及亮度的更改将不会生效，但应用仍会记录最新设置，这些改动将在切换到闪烁模式时生效。

#### 状态消息

除了接受远程命令，本示例还会在连接建立和 LED 状态变更时以保留消息形式发送最新的 LED 状态。这类状态消息一共有三种，它们使用的主题分别是 `stat/led/power`、`stat/led/hsb` 和 `stat/led/mode`，消息格式与对应的 `cmnd/led/<command>` 命令相同。

## 运行 Demo

在 VS Code 中根据你的实际情况调整配置，例如 Wi-Fi SSID、Wi-Fi 密码等。

为了提供最佳的安全性，EMQX Cloud Serverless 强制启用 TLS 认证和用户名密码认证，所以你还需要配置 CA 证书以及连接时使用的用户名密码。

本示例提供了两种设置 CA 证书的方式，其中一种在前文中已经提及，即在 `CMakeLists.txt` 文件中通过 `target_add_binary_data` 函数将文件嵌入到固件中。如果使用这种方式，你需要将 `target_add_binary_data` 函数中的文件名修改为您实际的 CA 证书文件名，且证书必须为 PEM 格式。

另一种方式相对简单，可以直接在配置菜单中完成，在 `Demo Configuration` 子菜单中找到 `MQTT Broker certificate override` 配置项，将 CA 证书的 Base64 部分复制粘贴进去即可，注意不要包含任何换行符和空格：

![CA 证书的 Base64](https://assets.emqx.com/images/df1b88c0bbd0b7b42bbc43480ea64e47.png)

接下来是认证所需的用户名密码，在 EMQX Cloud Serverless 中，你可以快速地注册新设备， 通过控制台的左侧菜单进入 `认证` 页面，点击 `Add` 或者 `Import` 就可以快速地完成认证信息的添加：

![添加认证](https://assets.emqx.com/images/916c43754da0c43bb55582eec780040a.png)

添加完成后，回到 ESP-IDF 的配置菜单，将 MQTT Username 和 MQTT Password 修改为你刚刚添加的内容即可。

完成配置后，构建项目并将其烧写到 ESP32 中。如果 ESP32 的运行一切顺利，你将在串口控制台看到以下输出：

![串口控制台](https://assets.emqx.com/images/30d00ae38f422979c6f354faf0540a71.png)

现在，你可以打开 MQTTX，让它同样连接到你的 EMQX Cloud Serverless 实例，然后向 ESP32 发送命令改变其 LED 的运行状态：

![MQTTX](https://assets.emqx.com/images/cb416f63ed2036bb33e11c037984cbed.png)

## 总结

MQTT 为运行 FreeRTOS 的实时应用提供了强大的消息通信能力，本示例仅仅展示了 QoS 1 消息和保留消息的应用，QoS 1 确保消息不会丢失，保留消息确保我们在任何时间都能获取到该消息。MQTT 还有其他诸多特性，例如共享订阅、用户属性、请求响应等，都能为我们的应用开发带来极大的帮助。

实时应用所在的领域通常对于通信安全也有着较高的要求，而 MQTT 对 TLS 和认证机制的良好支持，使我们得以从传输层到应用层为数据安全提供全面的保护。

最后，再次推荐将 EMQX Cloud Serverless 作为您构建应用时的首选 MQTT Server，它的极速部署、可观的免费额度以及自动伸缩等特性，可以极大减少您需要在 MQTT Server 上投入的运维精力，使您可以尽可能地专注在应用的开发工作上。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
