[MQTT](https://www.emqx.com/zh/mqtt) 是轻量级的、灵活的物联网消息交换和数据传递协议，致力于为 IoT 开发人员实现灵活性与硬件/网络资源的平衡。

[ESP8266](https://www.espressif.com/zh-hans) 提供了⼀套⾼度集成的 Wi-Fi SoC 解决⽅案，其低功耗、 紧凑设计和⾼稳定性可以满⾜⽤户的需求。ESP8266 拥有完整的且⾃成体系的 Wi-Fi ⽹络功能，既能够独⽴应⽤，也可以作为从机搭载于其他主机 MCU 运⾏。

在此项目中我们将实现 ESP8266 连接到 [EMQ X MQTT Cloud](https://cloud.emqx.cn/) 运营和维护的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并使用 Arduino IDE 来对 ESP8266 进行编程。 EMQ X Cloud 是由 [EMQ](https://www.emqx.com/zh) 推出的安全的 MQTT 物联网云服务平台，它提供一站式运维代管、独有隔离环境的 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 接入服务。



## 所需物联网组件

* ESP8266
* Arduino IDE
* [MQTT X](https://mqttx.app/zh):  优雅的跨平台 MQTT 5.0 客户端工具
* 免费的公共 MQTT 服务器
  - Broker: **broker.emqx.io**
  - TCP Port: **1883**
  - Websocket Port: **8083**



## ESP8266 Pub/Sub 示意图

![project.png](https://static.emqx.net/images/8c533fd396ed33ac5a6daa872eced9ba.png)



## ESP8266 代码编写

1. 首先我们将导入 **ESP8266WiFi** 和 **PubSubClient** 库，ESP8266WiFi  库能够将 ESP8266 连接到 Wi-Fi 网络，PubSubClient  库能使 ESP8266  连接到 MQTT 服务器发布消息及订阅主题。

   ```c
   #include <ESP8266WiFi.h>
   #include <PubSubClient.h>
   ```

2. 设置 Wi-Fi 名称和密码，以及 MQTT 服务器连接地址和端口

   ```c
   // WiFi
   const char *ssid = "mousse"; // Enter your WiFi name
   const char *password = "qweqweqwe";  // Enter WiFi password
   
   // MQTT Broker
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "esp8266/test";
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

4. 设置 MQTT 服务器，并编写回调函数，同时将连接信息打印到串口监视器上

   ```c
   client.setServer(mqtt_broker, mqtt_port);
   client.setCallback(callback);
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

5. MQTT 服务器连接成功后，ESP8266 将向 MQTT 服务器发布消息和订阅主题

   ```c
   // publish and subscribe
   client.publish(topic, "hello emqx");
   client.subscribe(topic);
   ```

6. 将主题名称打印到串行端口，然后打印收到消息的每个字节

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

7. 完整代码

   ```c
   #include <ESP8266WiFi.h>
   #include <PubSubClient.h>
   
   // WiFi
   const char *ssid = "mousse"; // Enter your WiFi name
   const char *password = "qweqweqwe";  // Enter WiFi password
   
   // MQTT Broker
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "esp8266/test";
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
       // publish and subscribe
       client.publish(topic, "hello emqx");
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



### 运行和测试

1. 请使用 [Arduino IDE](https://www.arduino.cc/en/Main/Software) 将完整代码上传到 ESP8266，并打开串口监视器

   ![esp_con.png](https://static.emqx.net/images/d5632144ec7cf22977b53519f4411227.png)

2. 建立 MQTT X 客户端 与 MQTT 服务器的连接, 并向 ESP8266 发送消息

   ![mqttx_pub.png](https://static.emqx.net/images/b8df461f137bc73aeb3aff1ae1126549.png)

3. 在串口监视器查看 ESP8266 接收到的消息

   ![esp_msg.png](https://static.emqx.net/images/24132d64c2c19738f1a12b0acb3b217e.png)



### 总结

至此，我们已成功使 ESP8266 连接到 EMQ X Cloud 提供的公共 MQTT 服务器。 在本项目中我们简单的将 ESP8266 连接到 MQTT 服务器，这只是 ESP8266 较为基础的能力之一，ESP8266 其实还能与各类物联网传感器相连，并将传感器数据上报至 MQTT 服务器。

接下来我们将会陆续发布更多关于物联网开发及 ESP8266 的相关文章，敬请关注。
