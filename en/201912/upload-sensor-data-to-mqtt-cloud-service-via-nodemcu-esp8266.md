### Introduction

This example will demonstrate how to report the temperature and humidity data collected by the DHT11 sensor to the MQTT service in the cloud through the MQTT protocol and the NodeMCU based on ESP8266 , and show how the application subscribes to and processes the data. The reason why mqtt protocol is used in this article is that it is lightweight and energy-saving, which is very suitable for the use scenarios of the Internet of things. At present, all major public cloud providers have basically opened IOT hub services based on MQTT protocol. For example, the IOT Core of AWS and the IOT Hub of Azure can easily access these data to these public cloud services through MQTT protocol.

The overall architecture of this example is as follows:

![Artboard Copy 11.png](https://static.emqx.net/images/1d8de4c8e46b6e7e8d48ce64c3f46c64.png)



### Configuration

#### Hardware Configuration

- NodeMCU board x 1: NodeMCU is an open source IoT platform. It includes firmware which runs on the ESP8266 Wi-Fi SoC, and hardware which is based on the ESP-12 module. The term "NodeMCU" by default refers to the firmware rather than the development kits . The firmware uses the Lua scripting language.
- DHT11 temperature / humidity sensor x 1: DHT11 digital temperature and humidity sensor is a  composite sensor with calibrated digital signal output
- Breadboard x 1
- Several jumper wires
- Please refer to the following screenshot for Connection Graph

![689328937a9d2d8007ce11ea94eb9dd9c6c5c23c.png](https://static.emqx.net/images/ab1d6dee2e4870a45ada34fb584f8328.png)

#### Arduino Configuration

- Download and install  [CH340G USB](https://kig.re/downloads/CH34x_Install.zip) driver

- Install ESP8266 module

- Install PubSubClient library (by Nick O'Leary)

  Sketch -> Include Library -> Manage Libraries... -> Type PubSub in Search field -> Install

#### MQTT Cloud Service

After the data is successfully collected through NodeMCU, it needs to be sent to the MQTT cloud service in the cloud. This article uses the MQTT cloud service provided by EMQX. Readers can also choose other MQTT cloud services according to their own circumstances, such as Azure IoT Hub or AWS IoT Core. Each cloud service needs to provide different authentication methods when accessing. Therefore, when connecting to the MQTT service in the cloud via NodeMCU, it is required to set the connection method according to the security requirements of the target cloud service. For the sake of simplicity, this article uses a non-secure connection method. In a formal production environment, a connection with a secure authentication method must be set.

- Click [EMQX Cloud](<https://accounts.emqx.io/signin?continue=https://cloud.emqx.io>)  registration address to register
- After registration, click  [EMQX Cloud](<https://cloud.emqx.io/console/deployments/0?oper=new>)  to apply for a free trial of 15-day deployment

![69518124b89a0e800f9111ea9203d65d445c3f06.png](https://static.emqx.net/images/de696779fd64a2fb880e69893ed2dab5.png)

- View the broker connection address

![69527781f86bf0800fa711ea9f9e64147e13591f.png](https://static.emqx.net/images/504ec89295d41afc72daa8e1ebcdc302.png)



### Coding

```c
#include <ESP8266WiFi.h>

#include <PubSubClient.h>

#include "DHT.h"

#define DHTPIN D4     // what pin we're connected to
#define wifi_ssid "xxxxx"
#define wifi_password "xxxxx"

#define mqtt_server "broker-internet-facing-f1429d8cb54ca4a7.elb.us-east-1.amazonaws.com"  // MQTT Cloud address
#define humidity_topic "humidity"
#define temperature_topic "temperature"

#define DHTTYPE DHT11   // DHT 11

WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(mqtt_server, 1883);
    dht.begin();
}

void setup_wifi() {
    delay(10);
    WiFi.begin(wifi_ssid, wifi_password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
}

void reconnect() {
    // Loop until we're reconnected
    while (!client.connected()) {
        Serial.print("Attempting MQTT connection...");
        if (client.connect("nodeMcuDHT11")) {
            Serial.println("connected");
        } else {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

bool checkBound(float newValue, float prevValue, float maxDiff) {
    return newValue < prevValue - maxDiff || newValue > prevValue + maxDiff;
}

long lastMsg = 0;
float temp = 0.0;
float hum = 0.0;
float diff = 1.0;

void loop() {
    if (!client.connected()) {
        reconnect();
    }
    client.loop();

    long now = millis();
    if (now - lastMsg > 30000) {
        // Wait a few seconds between measurements
        lastMsg = now;

        float newTemp = dht.readTemperature();
        float newHum = dht.readHumidity();
        if (checkBound(newTemp, temp, diff)) {
            temp = newTemp;
            Serial.print("New temperature:");
            Serial.println(String(temp).c_str());
            client.publish(temperature_topic, String(temp).c_str(), true);
        }

        if (checkBound(newHum, hum, diff)) {
            hum = newHum;
            Serial.print("New humidity:");
            Serial.println(String(hum).c_str());
            client.publish(humidity_topic, String(hum).c_str(), true);
        }
    }
}
```

Follow these steps to edit the code to suit your own Wi-Fi and MQTT settings

- Wi-Fi Setting

  ```c
  #define wifi_ssid ""
  #define wifi_password ""
  ```

- Broker server setting

  ```c
  #define mqtt_server "broker-internet-facing-f1429d8cb54ca4a7.elb.us-east-1.amazonaws.com"
  ```

- Arduion configuration

![690047768a924a00095311ea954cdd303e67665a.png](https://static.emqx.net/images/f30399b37a8c03b2f4faf47a01ab984f.png)



### Running

- Code upload

  Connect the NodeMCU to the PC via USB and select the 115200 port in the Arduion IDE. Use the upload button to compile the sketch and upload it to the device.

- Open Arduino monitor window to view data reporting.

![69004810f4125880095311ea9394640718d5c7c1.png](https://static.emqx.net/images/e1932131cf52075fbbfb09fa89f8ba91.png)



- MQTT client receives messages

  - Use [MQTT Websocket Toolkit](<http://tools.emqx.io/>)  to test the reported message

    > MQTT Websocket Toolkit is a recently open sourced MQTT (WebSocket) test tool from EMQ, which supports online access (tools.emqx.io). We can easily verify whether the NodeMCU reports MQTT messages.

    1. Create an MQTT connection
       ![695302069d88c8000fac11ea8c544c8dd42b0d25.png](https://static.emqx.net/images/6b70ac640041ab7aadb211553bc729e8.png)

```
2.Subscribe to topics and receive test messages
```

![69528034776129000fa811ea8f6e6057cb3cd279.png](https://static.emqx.net/images/16d0f34e02926530e021ad9e6f2d3de5.png)

- Use Python MQTT client to view reported messages

  ```python
  from paho.mqtt import client as mqtt
  
  
  def on_connect(client, userdata, flags, rc):
      # connect mqtt broker
      client.subscribe([("temperature", 0), ("humidity", 0)])
  
  
  def on_message(client, userdata, msg):
      # sub dht11 temperature/humidity data
      print(f"{msg.topic}: {msg.payload.decode()}")
  
  
  def run():
      client = mqtt.Client()
      # Edit MQTT Cloud address
      client.connect("broker-internet-facing-f1429d8cb54ca4a7.elb.us-east-1.amazonaws.com", 1883)
      client.on_connect = on_connect
      client.on_message = on_message
      client.loop_forever()
  
  
  if __name__ == '__main__':
      run()
  ```

  Screenshot of Python script running:

  ![69530281bc875a000fac11ea8c5f96b65eb2c1b9.png](https://static.emqx.net/images/4ebd3963243c0af2a75e46f19fcbd5fb.png)

- Troubleshooting: In order to perform troubleshooting, connecte the USB adapter to the PC and select the port  of USB-TTL adapter in the Arduino IDE. Open the Serial Monitor to view the debug information generated by the serial output



### Summary

So far, it has completed the simple process of collecting data from NodeMCU, uploading it to the MQTT cloud service provided by EMQ, and processing the data by the back-end program written by Python. However, in actual production applications, higher requirements will be required, for example,

- More secure connection method
- Real-time processing of IoT data
- Persistence of  data
- Larger scale connection

[EMQ Enterprise Edition](<https://www.emqx.io/products/enterprise>) and its [Cloud service](<https://cloud.emqx.io/>)  have provide good solution to solve the above problems. Readers can refer to related links for more information.


In order to achieve high data security (avoid uploading to the cloud), reduce business processing delays, and reduce data transmission costs, edge computing can be considered in the solution. Azure IoT Edge and AWS's Greengrass provide solutions at the edge. EMQ also provides an open sourced ultra-lightweight edge IoT edge streaming analytics solution  [Kuiper](<https://www.emqx.io/products/kuiper>). Readers can refer to[ this Article](https://medium.com/@emqtt/lightweight-edge-computing-emq-x-kuiper-and-azure-iot-hub-integration-solution-151134ead024) for more detailed information.

------

Welcome to our open source project [github.com/emqx/emqx](https://github.com/emqx/emqx). Please visit the [ documentation](https://docs.emqx.io) for details.

