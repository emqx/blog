[MQTT](https://mqtt.org/) is a lightweight and flexible IoT message exchange and data transmission protocol, which is dedicated to achieving the balance between flexibility and hardware/network resources for IoT developers.

[ESP32](https://www.espressif.com/en/products/socs/esp32) is an upgraded version of ESP8266. In addition to the Wi-Fi module, this module also includes a Bluetooth 4.0 module. The dual-core CPU operates at a frequency of 80 to 240 MHz. It contains two Wi-Fi and Bluetooth modules and various input and output pins. ESP32 is an ideal choice for IoT projects.

In this project, we will connect ESP32 to the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) operated and maintained by EMQX [MQTT Cloud](https://www.emqx.com/en/cloud), and use the Arduino IDE to program the ESP32. EMQX Cloud is a secure MQTT IoT cloud service platform launched by [EMQ](https://www.emqx.com/en). It provides [MQTT 5.0 ](https://www.emqx.com/en/mqtt/mqtt5) access service with one-stop operation and maintenance management and a unique isolation environment.



## Required IoT Components

* ESP32
* Arduino IDE
* [MQTT 5.0 client tool - MQTTX](https://mqttx.app)
* A [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) deployed on [EMQX Cloud](https://www.emqx.com/en/cloud)
  - Broker: **broker.emqx.io**
  - TCP Port: **1883**
  - Websocket Port: **8083**


## Arduino Configuration

### Install ESP32 development board

Click Tools -> Development Board -> Development Board Management -> Search ESP32 -> Install

![Install ESP32 development board](https://assets.emqx.com/images/99c502b39ef7d21dc75632e42aa89708.png)

### Install PubSub client

Project -> Load library -> Library manager... -> Search PubSubClient -> Install PubSubClient by Nick O’Leary

![Install PubSub client](https://assets.emqx.com/images/cb7b0228aa91bf300eec5a725da159d3.png)



## ESP32 Pub/Sub Diagram 

![ESP32 Pub/Sub diagram](https://assets.emqx.com/images/f806ce3df585c26ca01fd1aa3711be46.jpg)

## Programming ESP32 Board with Arduino IDE

### Connect to MQTT step by step

1. First, we will import the **WiFi** and **PubSubClient** libraries. The ESP8266WiFi library can connect ESP32 to Wi-Fi networks, and the PubSubClient library can connect ESP32 to the MQTT server to publish messages and subscribe to topics.

   ```c
   #include <WiFi.h>
   #include <PubSubClient.h>
   ```

2. Set the Wi-Fi name and password, as well as the MQTT server connection address and port, and set the topic to "esp32/test".

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

3. Open a serial connection to output the results of the program and connect to the Wi-Fi network.

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

4. Use PubSubClient to connect to the [public MQTT broker](https://www.emqx.com/en/blog/popular-online-public-mqtt-brokers).

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

5. After the MQTT server is successfully connected, ESP32 will publish messages to the MQTT server of `esp/test` and subscribe to the topic messages of `esp/test`.

   ```c
   // publish and subscribe
   client.publish(topic, "Hi EMQX I'm ESP32 ^^");
   client.subscribe(topic);
   ```

6. Set the callback function to print the topic name to the serial port and print the message received from the `esp32/test` topic.

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

### Full Code

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


## Running and Testing

1. Use Arduino to upload the complete code and power on the esp32.

2. Open the serial monitor, select 115200 baud rate, and check the ESP32 connection status.

   ![check the ESP32 connection status](https://assets.emqx.com/images/08d1cf506e708f40861f4d2ea4776c1f.png)

3. Use the MQTTX client to connect to the public MQTT server and publish messages to ESP32.

   ![MQTTX client](https://assets.emqx.com/images/2dc50309dbba7bdc8a65ec9b4b082b8c.png)


## Summary 

So far, we have successfully connected ESP32 to the public MQTT server provided by [EMQX Cloud](https://www.emqx.com/en/cloud). In this project, we simply connect ESP32 to the MQTT server. This is just one of ESP32's basic capabilities. ESP32 can actually connect to various IoT sensors and report sensor data to the MQTT server.

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt) series of articles provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
