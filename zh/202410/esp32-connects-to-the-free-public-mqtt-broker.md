## 引言

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种轻量级的物联网发布/订阅模式消息传递协议，提供可靠的实时通信，并且对代码和带宽的要求极低。它特别适合资源有限的设备和低带宽网络，广泛应用于物联网、移动互联网、车联网和电力行业。

ESP32 是 [ESP8266](https://www.emqx.com/zh/blog/esp8266-connects-to-the-public-mqtt-broker) 的升级版本，是一种低成本、低功耗的片上系统微控制器。除了 Wi-Fi 模块外，ESP32 还包括一个蓝牙 4.0 模块。其双核 CPU 的工作频率为 80 至 240 MHz，包含两个 Wi-Fi 和蓝牙模块以及各种输入输出引脚。

ESP32 是物联网项目的理想选择，在 ESP32 上使用 MQTT 具有多个优势：

- MQTT 是一种轻量级的消息传递协议，优化用于受限设备和网络，例如 ESP32 和 Wi-Fi，因此对功耗和带宽的影响最小。
- MQTT 支持不同级别的可靠性和服务质量（QoS），以适应 ESP32 的能力。这种灵活性使其在网络不稳定的情况下也能使用。
- ESP32 和 MQTT 在物联网应用中广泛使用，因此它们能够很好地集成到物联网解决方案中。MQTT 协议还设计简化了与云平台的集成，支持跨网络设备控制和数据监控。

总之，ESP32 和 MQTT 的结合非常适合需要无线连接和设备之间高效消息传递的物联网应用。本文将通过一个简单的演示，向您展示在 ESP32 上使用 Arduino IDE 发布 MQTT 消息和订阅主题的过程。

## 准备 MQTT Broker

在开始之前，请确保您有一个 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 用于通信和测试。我们建议使用 EMQX Platform 的 Serverless 版本。

[EMQX Platform](https://www.emqx.com/zh/cloud) 是一个全托管的 MQTT 消息云服务，可以无缝连接您的物联网设备到任何云端，无需维护基础设施。EMQX Serverless 在安全、可扩展的集群上提供 MQTT 服务，并采用按量计费的定价模式，是适合快速开启 MQTT 项目的灵活经济的解决方案。

为简化流程，本文将使用[免费的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)：

- 服务器：`broker.emqx.io`
- TCP 端口：`1883`
- WebSocket 端口：`8083`
- SSL/TLS 端口：`8883`
- 安全 WebSocket 端口：`8084`

## 在 ESP32 上使用 MQTT 入门

### Arduino 配置

Arduino 是一个基于易用硬件和软件的开源电子平台。它面向所有制作交互项目的开发者。Arduino 板可以读取输入——如传感器上的光、按钮上的手指或 Twitter 消息——并将其转换为输出——激活电机、点亮 LED 或在线发布内容。

在本项目中，我们将使用 Arduino 板将 ESP32 模块连接到计算机上。Arduino 将处理向 ESP32 上传代码，并提供 ESP32 与笔记本电脑之间的串行连接。

请参考[官方 Arduino 文档](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing)，了解有关安装 Arduino 的详细说明。

#### 安装 ESP32 开发板

ESP32 开发板在 ESP32 平台上使用 MQTT 时非常重要。它为开发和部署基于 MQTT 的项目提供了硬件和软件支持。凭借集成的 Wi-Fi 和蓝牙功能、用于与外部组件接口的 GPIO 引脚以及与 Arduino IDE 的兼容性，ESP32 开发板使基于 MQTT 的物联网应用能够轻松连接、原型设计和测试。

以下步骤将指导您在 Arduino IDE 中安装 ESP32 开发板：

1. 单击 Arduino IDE 菜单中的“工具”。
2. 选择“开发板”，然后选择“开发板管理器”。
3. 在开发板管理器中搜索“ESP32”。
4. 找到后，点击它，然后点击“安装”按钮。

![Install ESP32 development board](https://assets.emqx.com/images/99c502b39ef7d21dc75632e42aa89708.png)

#### 安装 PubSubClient

接下来，我们将安装 MQTT 客户端库 PubSubClient。PubSubClient 由 Nick O'Leary 开发，是一个为 Arduino 项目设计的轻量级 [MQTT 客户端库](https://www.emqx.com/zh/mqtt-client-sdk)。它为支持 MQTT 的服务器提供了简单的发布/订阅消息传递客户端。该库简化了 MQTT 通信，并实现了 Arduino 基于物联网应用的高效数据交换。

请按照以下步骤操作安装 PubSubClient 库：

1. 打开 Arduino IDE，然后在菜单栏中进入“项目”。
2. 选择“加载库”，然后选择“库管理器”。
3. 在库管理器中，在搜索栏中输入“PubSubClient”。
4. 找到 Nick O'Leary 的“PubSubClient”库，点击“安装”按钮。

![Install PubSub client](https://assets.emqx.com/images/cb7b0228aa91bf300eec5a725da159d3.png)

### 创建 MQTT 连接

#### TCP 连接

1. 首先，我们需要导入 WiFi 和 PubSubClient 库。WiFi 库允许 ESP32 与 Wi-Fi 网络建立连接，而 PubSubClient 库允许 ESP32 连接到 MQTT Broker 以发布消息和订阅主题。

   ```c
   #include <WiFi.h>
   #include <PubSubClient.h>
   
   ```

2. 配置以下参数：Wi-Fi 网络名称和密码、MQTT Broker 地址和端口、以及 `emqx/esp32` 主题。

   ```c
   // WiFi
   const char *ssid = "xxxxx"; // Enter your WiFi name
   const char *password = "xxxxx";  // Enter WiFi password
   
   // MQTT Broker
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "emqx/esp32";
   const char *mqtt_username = "emqx";
   const char *mqtt_password = "public";
   const int mqtt_port = 1883;
   ```

3. 建立与 Wi-Fi 网络的连接，并打开串行连接以显示程序结果。

   ```c
   // Set software serial baud to 115200;
   Serial.begin(115200);
   // Connecting to a Wi-Fi network
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
       delay(500);
       Serial.println("Connecting to WiFi..");
   }
   ```

4. 使用 PubSubClient 与 MQTT Broker 建立连接。

   ```c
   client.setServer(mqtt_broker, mqtt_port);
   client.setCallback(callback);
   while (!client.connected()) {
       String client_id = "esp32-client-";
       client_id += String(WiFi.macAddress());
       Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
       if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
           Serial.println("Public EMQX MQTT broker connected");
       } else {
           Serial.print("failed with state ");
           Serial.print(client.state());
           delay(2000);
       }
   }
   ```

#### TLS/SSL

在 MQTT 中使用 TLS 可以确保信息的机密性和完整性，防止信息泄露和篡改。

这个 ESP32 代码通过服务器根 CA 证书建立安全的 Wi-Fi 连接。`ca_cert` 变量包含 PEM 格式的根 CA 证书。`espClient` 对象通过 `setCACert()` 函数配置了服务器根 CA 证书。这种设置使 ESP32 客户端能够在 TLS 握手过程中验证服务器身份，确保传输数据的机密性和完整性。

```c
#include <WiFiClientSecure.h>

const char* ca_cert= \
"-----BEGIN CERTIFICATE-----\n" \
"MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh\n" \
"MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3\n" \
"d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD\n" \
"QTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT\n" \
"MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j\n" \
"b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG\n" \
"9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB\n" \
"CSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97\n" \
"nh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt\n" \
"43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P\n" \
"T19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4\n" \
"gdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO\n" \
"BgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR\n" \
"TLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw\n" \
"DQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr\n" \
"hMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg\n" \
"06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF\n" \
"PnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls\n" \
"YSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk\n" \
"CAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=" \
"-----END CERTIFICATE-----\n";

// init wifi secure client
WiFiClientSecure espClient;

espClient.setCACert(ca_cert);
```

完整的 TLS 连接代码请见：[GitHub](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-ESP32/esp32_connect_mqtt_via_tls.ino).

### 发布消息与订阅

成功连接到 MQTT Broker 后，ESP32 将向主题 `emqx/esp32` 发布消息，并订阅该主题。

```c
// publish and subscribe
client.publish(topic, "Hi, I'm ESP32 ^^");
client.subscribe(topic);
```

### 接收 MQTT 消息

设置回调函数，打印主题名称到串口，并打印从 `emqx/esp32` 主题接收到的消息。

```c
void callback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    for (int i = 0; i < length; i++) {
        Serial.print((char) payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");
}
```

### 完整代码

```c
#include <WiFi.h>
#include <PubSubClient.h>

// WiFi
const char *ssid = "xxxxx"; // Enter your Wi-Fi name
const char *password = "xxxxx";  // Enter Wi-Fi password

// MQTT Broker
const char *mqtt_broker = "broker.emqx.io";
const char *topic = "emqx/esp32";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
    // Set software serial baud to 115200;
    Serial.begin(115200);
    // Connecting to a WiFi network
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi..");
    }
    Serial.println("Connected to the Wi-Fi network");
    //connecting to a mqtt broker
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);
    while (!client.connected()) {
        String client_id = "esp32-client-";
        client_id += String(WiFi.macAddress());
        Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
        if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Public EMQX MQTT broker connected");
        } else {
            Serial.print("failed with state ");
            Serial.print(client.state());
            delay(2000);
        }
    }
    // Publish and subscribe
    client.publish(topic, "Hi, I'm ESP32 ^^");
    client.subscribe(topic);
}

void callback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message arrived in topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    for (int i = 0; i < length; i++) {
        Serial.print((char) payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");
}

void loop() {
    client.loop();
}
```

## 运行与测试

请按照以下步骤，使用 Arduino 上传完整代码并启动 ESP32：

1. 使用 USB 线将 ESP32 连接到计算机。

   1. 打开 Arduino IDE，从“工具”菜单中选择合适的开发板和端口。
   2. 将完整的代码复制并粘贴到 Arduino IDE 中。
   3. 点击“上传”按钮（或使用快捷键 Ctrl+U）来编译并将代码上传到 ESP32。
   4. 等待上传过程完成，确保没有错误。
   5. 代码上传完成后，从计算机上断开 ESP32。
   6. 通过连接适当的电源来为 ESP32 供电。

2. 打开串口监视器，并将波特率设置为 115200，然后通过监视器中的输出检查 ESP32 的连接状态。

   ![ESP32 serial monitor](https://assets.emqx.com/images/b3092b5bc576e59e3d964020cd73598f.png)

3. 使用 MQTTX 客户端与 MQTT Broker 建立连接，并向 ESP32 发布诸如“Hi, I'm MQTTX”之类的消息。

   > [MQTTX](https://mqttx.app/zh) 是一个优雅的跨平台 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 桌面客户端，支持 macOS、Linux 和 Windows 操作系统。其简洁的聊天式界面让用户可以轻松创建多个 MQTT/MQTTS 连接并订阅/发布 MQTT 消息。

   ![MQTTX Client](https://assets.emqx.com/images/d6af5f33eb8f550cf22705859ed9d59b.png)

4. 您将看到由 MQTTX 发布的消息。

   ![Messages published by MQTTX](https://assets.emqx.com/images/d192ba700151d83f7adc5376d5b4d374.png)

## 结语

在本文中，我们介绍了如何在 ESP32 上实现 MQTT。我们安装了必要工具，包括 ESP32 开发板和 PubSubClient 库。通过逐步操作，读者可以建立安全的 Wi-Fi 连接、连接到 MQTT Broker、发布消息并订阅主题。通过在 ESP32 上使用 MQTT，用户可以创建可靠且高效的物联网应用程序。

接下来，您可以查看由 EMQ 提供的《[MQTT 教程](https://www.emqx.com/zh/mqtt-guide)》系列，了解 MQTT 协议的特性，探索更多 MQTT 的高级应用，进行 MQTT 应用与服务开发。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
