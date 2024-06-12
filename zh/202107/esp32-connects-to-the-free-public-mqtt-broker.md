[MQTT](https://mqtt.org/) 是轻量级的、灵活的物联网消息交换和数据传递协议，致力于为 IoT 开发人员实现灵活性与硬件/网络资源的平衡。

[ESP32](https://www.espressif.com/zh-hans/products/socs/esp32)  是 ESP8266 的升级版本，除了Wi-Fi模块，该模块还包含蓝牙4.0模块。双核CPU工作频率为80至240 MHz，包含两个Wi-Fi和蓝牙模块以及各种输入和输出引脚， ESP32 是物联网项目的理想选择。

在此项目中我们将实现 ESP32 连接到 EMQX [MQTT Cloud](https://www.emqx.com/zh/cloud) 运营和维护的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并使用 Arduino IDE 来对 ESP32 进行编程。 EMQX Cloud 是由 EMQ 推出的安全的 MQTT 物联网云服务平台，它提供一站式运维代管、独有隔离环境的 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 接入服务。


## 所需物联网组件

* ESP32
* Arduino IDE
* [MQTT 5.0 客户端工具 - MQTTX](https://mqttx.app/zh)
* 部署在 [EMQX Cloud](https://www.emqx.com/zh/cloud) 上的免费的公共 MQTT 服务器
  - Broker: **broker-cn.emqx.io**
  - TCP Port: **1883**
  - Websocket Port: **8083**


## Arduino 配置

### 安装 ESP32 开发板

点击 工具 -> 开发板 -> 开发板管理 -> 搜索 ESP32 -> 点击安装

![安装 ESP32 开发板](https://assets.emqx.com/images/082b895a83d44063af2da5161e1916d2.png)

### 安装 PubSub client

项目 -> 加载库 -> 管理库... -> 搜索 PubSubClient -> 安装 PubSubClient by Nick O’Leary

![安装 PubSub client](https://assets.emqx.com/images/99a1b042e8e54fb487752cf1f0dff75e.png)



## ESP32 Pub/Sub 示意图

![ESP32 Pub/Sub 示意图](https://assets.emqx.com/images/601c4415dc368b9eb245ca92fb6b60f4.jpg)

## ESP32 代码编写

### 分步骤连接 MQTT

1. 首先我们将导入 **WiFi** 和 **PubSubClient** 库，ESP8266WiFi  库能够将 ESP32 连接到 Wi-Fi 网络，PubSubClient  库能使 ESP32  连接到 MQTT 服务器发布消息及订阅主题。

   ```c
   #include <WiFi.h>
   #include <PubSubClient.h>
   ```

2. 设置 Wi-Fi 名称和密码，以及 MQTT 服务器连接地址和端口，并这是 topic 为 "esp32/test"

   ```c
   // WiFi
   const char *ssid = "mousse"; // Enter your WiFi name
   const char *password = "qweqweqwe";  // Enter WiFi password
   
   // MQTT Broker
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "esp32/test";
   const char *mqtt_username = "emqx";
   const char *mqtt_password = "public";
   const int mqtt_port = 1883;
   ```

3. 打开一个串行连接，以便于输出程序的结果并且连接到 Wi-Fi 网络

   ```c
   // Set software serial baud to 115200;
   Serial.begin(115200);
   // connecting to a WiFi network
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
       delay(500);
       Serial.println("Connecting to WiFi..");
   }
   ```

4. 使用 PubSubClient 连接到公共 MQTT Broker。

   ```c
   client.setServer(mqtt_broker, mqtt_port);
   client.setCallback(callback);
   while (!client.connected()) {
       String client_id = "esp32-client-";
       client_id += String(WiFi.macAddress());
       Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
       if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
           Serial.println("Public emqx mqtt broker connected");
       } else {
           Serial.print("failed with state ");
           Serial.print(client.state());
           delay(2000);
       }
   }
   ```

5. MQTT 服务器连接成功后，ESP32 将向 MQTT 服务器 `esp/test` 发布消息和订阅 `esp/test` 主题消息。

   ```c
   // publish and subscribe
   client.publish(topic, "Hi EMQX I'm ESP32 ^^");
   client.subscribe(topic);
   ```

6. 设置回调函数将主题名称打印到串行端口并打印从 `esp32/test` 主题接收的消息。

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
const char *ssid = "mousse"; // Enter your WiFi name
const char *password = "qweqweqwe";  // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "broker.emqx.io";
const char *topic = "esp32/test";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
 // Set software serial baud to 115200;
 Serial.begin(115200);
 // connecting to a WiFi network
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.println("Connecting to WiFi..");
 }
 Serial.println("Connected to the WiFi network");
 //connecting to a mqtt broker
 client.setServer(mqtt_broker, mqtt_port);
 client.setCallback(callback);
 while (!client.connected()) {
     String client_id = "esp32-client-";
     client_id += String(WiFi.macAddress());
     Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
     if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
         Serial.println("Public emqx mqtt broker connected");
     } else {
         Serial.print("failed with state ");
         Serial.print(client.state());
         delay(2000);
     }
 }
 // publish and subscribe
 client.publish(topic, "Hi EMQX I'm ESP32 ^^");
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


## 运行和测试

1. 使用 Arduino 上传完整代码，并将 esp32 上电

2. 打开串口监视器，选择 115200 波特率，查看 ESP32 连接情况

	![查看 ESP32 连接情况](https://assets.emqx.com/images/f8cb5792593d29b5b29b0feacd03a26c.png)

3. 使用 MQTTX 客户端 连接到公共 MQTT 服务器, 并向 ESP32 发送消息

	![使用 MQTTX 客户端向 ESP32 发送消息](https://assets.emqx.com/images/2dc50309dbba7bdc8a65ec9b4b082b8c.png)


## 总结

至此，我们已成功使 ESP32 连接到 [EMQX Cloud](https://www.emqx.com/zh/cloud) 提供的公共 MQTT 服务器。 在本项目中我们简单的将 ESP32 连接到 MQTT 服务器，这只是 ESP32 较为基础的能力之一，ESP32 其实还能与各类物联网传感器相连，并将传感器数据上报至 MQTT 服务器。

接下来，读者可访问 EMQ 提供的 [MQTT 入门与进阶](https://www.emqx.com/zh/mqtt-guide)系列文章学习 MQTT 主题及通配符、保留消息、遗嘱消息等相关概念，探索 MQTT 的更多高级应用，开启 MQTT 应用及服务开发。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
