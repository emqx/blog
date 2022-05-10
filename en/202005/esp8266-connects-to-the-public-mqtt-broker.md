[MQTT](https://www.emqx.com/en/mqtt) is a lightweight and flexible protocol to exchange IoT messages and deliver data. It dedicates to achieve a balance between flexibility and hardware/network resources for the IoT developer.

[ESP8266](https://www.espressif.com) provides a highly integrated Wi-Fi SoC solution. Its low-power, compact design, and high stability can meet user's requirements. ESP8266 has a complete and self-contained Wi-Fi network function, which can be applied independently or can run as a slave at another host MCU.

In this project, we will implement connecting ESP8266 to [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) operated and maintained by [EMQX MQTT Cloud](https://www.emqx.com/en/cloud), and programming ESP8266 by using Arduino IDE. EMQX Cloud is an **MQTT IoT cloud service platform with security** launched by [EMQ](https://www.emqx.com/en). It provides a one-stop operation and maintenance agency and [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) access service with a uniquely isolated environment.

## The required IoT components 

- ESP8266
- Arduino IDE
- [MQTT X](https://mqttx.app): Cross-platform MQTT 5.0 client tool
- The free public [MQTT broker](https://www.emqx.com/en/products/emqx)
  - Broker: **broker.emqx.io**
  - TCP Port: **1883**
  - Websocket Port: **8083**



## ESP8266 Pub/Sub

![project.png](https://static.emqx.net/images/35a817d8c8b74c0481983b8c9ac0fee7.png)


## The code

1. Firstly, we import libraries **ESP8266WiFi** and **PubSubClient**. ESP8266WiFi library can connect ESP8266 to the Wi-Fi network, PubSubClient library can enable ESP8266 to connect to MQTT broker for publishing messages and subscribing topics.

   ```c
   #include <ESP8266WiFi.h>
   #include <PubSubClient.h>
   ```

2. Set Wi-Fi name and password, and connection address and port of MQTT broker

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

3. Open a serial connection for facilitating to output of the result of the program and connecting to the Wi-Fi network.

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

4. Set MQTT broker, write callback function, and print connection information on the serial monitor at the same time.

   ```c
   client.setServer(mqtt_broker, mqtt_port);
   client.setCallback(callback);
   while (!client.connected()) {
       String client_id = "esp8266-client-";
       client_id += String(WiFi.macAddress());
       Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
       if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
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

5. After successfully connecting to the MQTT broker, ESP8266 will publish messages and subscribe to the MQTT broker.

   ```c
   // publish and subscribe
   client.publish(topic, "hello emqx");
   client.subscribe(topic);
   ```

6. Printing the topic name to the serial port and then print every byte of received messages.

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

7. The full code

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


## Run and test

1. Please use  [Arduino IDE](https://www.arduino.cc/en/Main/Software) to upload the complete code to ESP8266 and open the serial monitor

   ![esp_con.png](https://static.emqx.net/images/4c97b1546d31021cc22c64ae7ce4863b.png)

2. Establish the connection between MQTT X client and MQTT broker, and send messages to ESP8266

   ![mqttx_pub.png](https://static.emqx.net/images/daa2c401453155045f2c068bcd57d66a.png)

3. View the messages ESP8266 received in the serial monitor

   ![esp_msg.png](https://static.emqx.net/images/8c98d850cdfd5c98db94471d0f6a308f.png)


## Summary

So far, we have successfully connected ESP8266 to the free public MQTT broker provided by EMQX Cloud. In this project, we connect ESP8266 to the MQTT broker, which is one of the relatively basic capabilities of ESP8266. Besides that, ESP8266 can also connect to various IoT sensors, and report the sensor data to the MQTT broker.

We will release more articles related to IoT development and ESP8266. Stay tuned.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
