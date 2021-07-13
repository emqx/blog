本示例将演示如何通过 基于 ESP8266 的 NodeMCU，把通过 DHT11 传感器搜集到的温、湿度数据通过 MQTT 协议将其上报到云端的 MQTT 服务，并且展示应用端如何订阅到这些数据并对之进行处理的过程。本文使用 MQTT 协议的原因在于该协议比较轻量级，节约能耗，非常适合于物联网的相关使用场景；目前各大公有云云提供商基本上都开放了基于 MQTT 协议的 IoT Hub 服务。比如 AWS 的 IoT Core，以及 Azure 的 IoT Hub 等，通过 MQTT 协议可以非常方便的将这些数据直接接入这些公有云服务。

本示例的总体架构如下

![Artboard Copy 11.png](https://static.emqx.net/images/1d8de4c8e46b6e7e8d48ce64c3f46c64.png)


## 配置

### 硬件配置

- NodeMCU board x 1：NodeMCU 是一个开源的 IoT （硬件）开发平台，NodeMCU 包含了可以运行在 ESP8266 Wi-Fi SoC芯片之上的固件,以及基于 ESP-12 模组的硬件。“NodeMCU” 缺省一般指的是固件，而不是开发套件。固件使用 Lua 脚本语言。
- DHT11 temperature/humidity sensor x 1：DHT11 数字温湿度传感器是一款含有已校准数字信号输出的温湿度复合传感器
- 面包板（Breadboard ）x 1
- 跳线（Jumper wires）若干
- 连接图（Connection Graph）请参考如下截图

![689328937a9d2d8007ce11ea94eb9dd9c6c5c23c.png](https://static.emqx.net/images/ab1d6dee2e4870a45ada34fb584f8328.png)

### Arduino 配置

- 下载并安装 [CH340G USB](https://kig.re/downloads/CH34x_Install.zip) 驱动
- 安装 ESP8266模块
- 安装 PubSubClient 库 (by Nick O'Leary)
  Sketch -> Include Library -> Manage Libraries... -> Type PubSub in Search field -> Install

### MQTT 云服务配置

在本文中我们选用由 [EMQ X Cloud](https://cloud.emqx.cn/) 提供的公共 [MQTT Broker](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 服务作为 broker 接入地址，broker 接入信息如下:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

 

## ESP8266 代码编写

1. 首先我们将导入 **ESP8266WiFi** 和 **PubSubClient** 库，ESP8266WiFi  库能够将 ESP8266 连接到 Wi-Fi 网络，PubSubClient  库能使 ESP8266  连接到 MQTT 服务器发布消息及订阅主题。

   ```c
   #include <ESP8266WiFi.h>
   #include <PubSubClient.h>
   #include <ArduinoJson.h>
   #include "DHT.h"
   ```

2. 设置 Wi-Fi 名称和密码，以及 MQTT 服务器连接地址和端口

   ```c
   // WiFi
   const char *ssid = "mousse"; // Enter your WiFi name
   const char *password = "qweqweqwe";  // Enter WiFi password
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "temp_hum/emqx";
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

4. 设置 MQTT Broker 信息

   ```c
   //connecting to a mqtt broker
   client.setServer(mqtt_broker, mqtt_port);
   client.setCallback(callback);
   //connecting to a mqtt broker
   while (!client.connected()) {
       String client_id = "esp8266-client-";
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

5. MQTT 服务器连接成功后初始化温湿度传感器

   ```c
   dht.begin();
   ```

6. 读取温湿度传感器数据以 json 格式上报数据

   ```c
   float temp = dht.readTemperature();
   float hum = dht.readHumidity();
   // json serialize
   DynamicJsonDocument data(256);
   data["temp"] = temp;
   data["hum"] = hum;
   // publish temperature and humidity
   char json_string[256];
   serializeJson(data, json_string);
   // {"temp":23.5,"hum":55}
   Serial.println(json_string);
   client.publish(topic, json_string, false);
   ```

7. 完整代码

   ```c
   #include <ESP8266WiFi.h>
   #include <PubSubClient.h>
   #include <ArduinoJson.h>
   #include "DHT.h"
   
   // WiFi
   const char *ssid = "mousse"; // Enter your WiFi name
   const char *password = "qweqweqwe";  // Enter WiFi password
   
   // MQTT Broker
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "temp_hum/emqx";
   const char *mqtt_username = "emqx";
   const char *mqtt_password = "public";
   const int mqtt_port = 1883;
   
   // DHT11
   #define DHTPIN D4
   #define DHTTYPE DHT11   // DHT 11
   unsigned long previousMillis = 0;
   
   WiFiClient espClient;
   PubSubClient client(espClient);
   DHT dht(DHTPIN, DHTTYPE);
   
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
       //connecting to a mqtt broker
       while (!client.connected()) {
           String client_id = "esp8266-client-";
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
       // dht11 begin
       dht.begin();
   }
   
   
   void loop() {
       client.loop();
       unsigned long currentMillis = millis();
       // temperature and humidity data are publish every five second
       if (currentMillis - previousMillis >= 5000) {
           previousMillis = currentMillis;
           float temp = dht.readTemperature();
           float hum = dht.readHumidity();
           // json serialize
           DynamicJsonDocument data(256);
           data["temp"] = temp;
           data["hum"] = hum;
           // publish temperature and humidity
           char json_string[256];
           serializeJson(data, json_string);
           // {"temp":23.5,"hum":55}
           Serial.println(json_string);
           client.publish(topic, json_string, false);
       }
   }
   ```



### 运行测试

1. 请使用 [Arduino IDE](https://www.arduino.cc/en/Main/Software) 将完整代码上传到 ESP8266，并打开串口监视器

   ![esp_con.png](https://static.emqx.net/images/d5632144ec7cf22977b53519f4411227.png)

2. 建立 MQTT X 客户端 与 MQTT 服务器的连接, 并测试温湿度数据接收

   ![mqttx_sub.png](https://static.emqx.net/images/esp8266_temp_hum.png)

3. 使用 Python 客户端订阅温湿度数据

   ```python
   # python 3.x
   
   import random
   
   from paho.mqtt import client as mqtt_client
   
   
   BROKER = 'broker.emqx.io'
   PORT = 1883
   TOPIC = "temp_hum/emqx"
   # generate client ID with pub prefix randomly
   CLIENT_ID = "python-mqtt-tcp-sub-{id}".format(id=random.randint(0, 1000))
   USERNAME = 'emqx'
   PASSWORD = 'public'
   
   
   def on_connect(client, userdata, flags, rc):
       if rc == 0:
           print("Connected to MQTT Broker!")
           client.subscribe(TOPIC)
       else:
           print("Failed to connect, return code {rc}".format(rc=rc), )
   
   
   def on_message(client, userdata, msg):
       print("Received `{payload}` from `{topic}` topic".format(
           payload=msg.payload.decode(), topic=msg.topic))
   
   
   def connect_mqtt():
       client = mqtt_client.Client(CLIENT_ID)
       client.username_pw_set(USERNAME, PASSWORD)
       client.on_connect = on_connect
       client.on_message = on_message
       client.connect(BROKER, PORT)
       return client
   
   
   def run():
       client = connect_mqtt()
       client.loop_forever()
   
   
   if __name__ == '__main__':
       run()
   ```



### 总结

至此为止，完成了从 NodeMCU 采集数据，并上传到 EMQ 提供的 MQTT  云服务，最后由 Python 写的后端程序对数据进行处理的简单过程。但在实际的生产应用中，会需要更高的要求，比如，

- 更加安全的连接方式
- 对物联网数据进行实时处理
- 对数据进行持久化
- 更大规模的连接要求

[EMQ X 企业版](https://www.emqx.com/zh/products/emqx)，及其[物联网 MQTT 云服务](https://cloud.emqx.cn/)在解决上述问题已经提供了很好的解决方案，有兴趣的读者可以参考相关链接了解更多的信息。

为了实现数据的高安全性（避免上传到云端），降低业务处理时延，以及数据传输成本，在解决方案中可以考虑采用边缘计算。Azure IoT Edge 和 AWS 的 Greengrass 提供了在边缘端的解决方案。EMQ 也提供了开源的超轻量级边缘物联网实时数据分析 (IoT  Edge streaming analytics) 方案 [Kuiper](<https://github.com/lf-edge/ekuiper>)，读者可以参考[这篇文章](https://www.emqx.com/zh/blog/lightweight-edge-computing-emqx-kuiper-and-azure-iot-hub-integration-solution)以获取更详细的信息。
