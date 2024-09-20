## Introduction

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol for IoT in [publish/subscribe model](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model), offering reliable real-time communication with minimal code and bandwidth overhead. It is especially beneficial for devices with limited resources and low-bandwidth networks, making it widely adopted in IoT, mobile internet, IoV, and power industries.

[ESP32](https://www.espressif.com/en/products/socs/esp32), an upgraded version of [ESP8266](https://www.emqx.com/en/blog/esp8266-connects-to-the-public-mqtt-broker), is a low-cost, low-power system on a chip microcontroller. In addition to the Wi-Fi module, the ESP32 also includes a Bluetooth 4.0 module. The dual-core CPU operates at a frequency of 80 to 240 MHz. It contains two Wi-Fi and Bluetooth modules and various input and output pins. ESP32 is an ideal choice for IoT projects.

Using MQTT on ESP32 offers several advantages:

- First, MQTT is a lightweight messaging protocol optimized for constrained devices and networks like ESP32 and Wi-Fi, so it has minimal impact on power and bandwidth. 
- Second, MQTT supports different levels of reliability and quality of service to match the capabilities of ESP32. This flexibility makes it suitable for use even when networks are unstable.
- Third, ESP32 and MQTT are widely used in IoT applications, allowing them to be well integrated into IoT solutions. The MQTT protocol is also designed to simplify integration with cloud platforms to enable device control and data monitoring across networks.

Overall, the combination of ESP32 and MQTT is ideal for IoT applications that require wireless connectivity and efficient messaging between many devices. This blog will show you the process of publishing MQTT messages and topic subscription on ESP32 using Arduino IDE through a simple demo.



## Prepare an MQTT Broker

Before proceeding, please ensure you have an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to communicate and test with. We recommend you use EMQX Platform Serverless Plan.

[EMQX Platform](https://www.emqx.com/en/cloud) is a comprehensive, fully-managed MQTT messaging cloud service that seamlessly connects your IoT devices to any cloud without the hassle of infrastructure maintenance. The Serverless Plan provides MQTT services on a secure, scalable cluster with pay-as-you-go pricing, making it a flexible and cost-effective solution for starting with MQTT.

<section class="promotion">
    <div>
        Try EMQX Serverless for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">Forever free under 1M session minutes/month.</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) to simplify the process:

- Server: `broker.emqx.io`

- TCP Port: `1883`

- WebSocket Port: `8083`

- SSL/TLS Port: `8883`

- Secure WebSocket Port: `8084`


## Getting Started with MQTT on ESP32

### Arduino Configuration

Arduino is an open-source electronics platform based on easy-to-use hardware and software. It is intended for anyone making interactive projects. Arduino boards can read inputs - a light on a sensor, a finger on a button, or a Twitter message - and turn them into an output - activating a motor, turning on an LED, or publishing something online.

In this project, we will use an Arduino board to connect the ESP32 module to our computer. The Arduino will handle uploading code to the ESP32 and provide a serial connection between the ESP32 and our laptop.

Please refer to the [official Arduino documentation](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing) for detailed instructions on installing Arduino.

#### Install ESP32 Development Board

The ESP32 development board is crucial in working with MQTT on the ESP32 platform. It provides hardware and software support for developing and deploying MQTT-based projects on the ESP32. With its integrated Wi-Fi and Bluetooth capabilities, GPIO pins for interfacing with external components, and compatibility with the Arduino IDE, the ESP32 development board enables seamless connectivity, prototyping, and testing of MQTT-based IoT applications.

These steps will guide you through installing the ESP32 development board in the Arduino IDE:

1. Click on "Tools" in the Arduino IDE menu.
2. Select "Development Board" and then choose "Development Board Management".
3. In the Boards Manager, search for "ESP32".
4. Once found, click on it and then click the "Install" button.

![Install ESP32 development board](https://assets.emqx.com/images/99c502b39ef7d21dc75632e42aa89708.png)

#### Install PubSubClient

Next, we will proceed to install the MQTT client library [PubSubClient](https://github.com/knolleary/pubsubclient). Developed by Nick O'Leary, PubSubClient is a lightweight [MQTT client library](https://www.emqx.com/en/mqtt-client-sdk) designed for Arduino-based projects. It provides a client for simple publish/subscribe messaging with a server supporting MQTT. This library simplifies MQTT communication and enables efficient data exchange in Arduino-based IoT applications.

To install the PubSubClient library, please follow these steps:

1. Open the Arduino IDE, then go to "Project" in the menu bar.
2. Select "Load library" and then choose "Library manager".
3. In the Library Manager, type "PubSubClient" into the search bar.
4. Locate the "PubSubClient" library by Nick O'Leary and click the "Install" button.

![Install PubSub client](https://assets.emqx.com/images/cb7b0228aa91bf300eec5a725da159d3.png)

By following these steps, you will successfully install the PubSubClient library into your Arduino IDE.

### Create an MQTT Connection

#### TCP Connection

1. First, we need to import the **WiFi** and **PubSubClient** libraries. The **WiFi** library allows ESP32 to establish connections with Wi-Fi networks, while the **PubSubClient** library enables ESP32 to connect to an MQTT broker for publishing messages and subscribing to topics.

   ```arduino
   #include <WiFi.h>
   #include <PubSubClient.h>
   ```

2. Please configure the following parameters: Wi-Fi network name and password, MQTT broker address and port, and the topic to `emqx/esp32`.

   ```arduino
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

3. Open a serial connection to display program results and establish a connection to the Wi-Fi network.

   ```reasonml
   // Set software serial baud to 115200;
   Serial.begin(115200);
   // Connecting to a Wi-Fi network
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
       delay(500);
       Serial.println("Connecting to WiFi..");
   }
   ```

4. Utilize PubSubClient to establish a connection with the MQTT broker.

   ```arduino
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

Using TLS in MQTT can ensure the confidentiality and integrity of information, preventing information leakage and tampering. 

This ESP32 code establishes a secure Wi-Fi connection using a server root CA certificate. The ca_cert variable contains the root CA certificate in PEM format. The espClient object is configured with the server root CA certificate using the `setCACert()` function. This setup enables the ESP32 client to verify the server's identity during the TLS handshake, establishing a secure Wi-Fi connection and ensuring the transmitted data's confidentiality and integrity.

```
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

The full TLS connection code is available on [GitHub](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-ESP32/esp32_connect_mqtt_via_tls.ino).

### Publish Messages & Subscribe

Once the connection to the MQTT broker is established successfully, the ESP32 will publish messages to the topic `emqx/esp32` and then subscribe to the topic `emqx/esp32`.

```axapta
// publish and subscribe
client.publish(topic, "Hi, I'm ESP32 ^^");
client.subscribe(topic);
```

### Receive MQTT Messages

Set the callback function to print the topic name to the serial port and print the message received from the `emqx/esp32` topic.

```arduino
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

The full code is as follows:

```arduino
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

## Running and Testing

1. Please follow these steps to upload the complete code using Arduino and power on the ESP32:

   1. Connect the ESP32 to your computer using a USB cable.
   2. Open the Arduino IDE and select the appropriate board and port from the "Tools" menu.
   3. Copy and paste the complete code into the Arduino IDE.
   4. Click the "Upload" button (or use the shortcut Ctrl+U) to compile and upload the code to the ESP32.
   5. Wait for the upload process to finish, ensuring there are no errors.
   6. Once the code is uploaded, disconnect the ESP32 from the computer.
   7. Power on the ESP32 by connecting it to a suitable power source.

2. Open the serial monitor and set the baud rate to 115200. Then, check the connection status of the ESP32 by monitoring the output in the serial monitor.

   ![ESP32 serial monitor](https://assets.emqx.com/images/b3092b5bc576e59e3d964020cd73598f.png)

3. Use the MQTTX client to establish a connection with the MQTT broker and publish messages such as `Hi, I'm MQTTX` to the ESP32.

   > [MQTTX](https://mqttx.app/) is an elegant cross-platform MQTT 5.0 desktop client that runs on macOS, Linux, and Windows. Its user-friendly chat-style interface enables users to easily create multiple MQTT/MQTTS connections and subscribe/publish MQTT messages.

   ![MQTTX Client](https://assets.emqx.com/images/d6af5f33eb8f550cf22705859ed9d59b.png)

4. You will see the messages published by MQTTX.

   ![Messages published by MQTTX](https://assets.emqx.com/images/d192ba700151d83f7adc5376d5b4d374.png)



## Summary

In this beginner's guide, we covered the basics of MQTT implementation on the ESP32. We installed the necessary tools, including the ESP32 development board and the PubSubClient library. Readers can establish a secure Wi-Fi connection, connect to an MQTT broker, publish messages, and subscribe to topics through step-by-step instructions. By leveraging MQTT on the ESP32, users can create reliable and efficient IoT applications.

Next, you can check out the [MQTT Guide: Beginner to Advanced](https://www.emqx.com/en/mqtt-guide) series provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.


## Resources

- [A Developer's Journey with ESP32 and MQTT Broker](https://www.emqx.com/en/blog/a-developer-s-journey-with-esp32-and-mqtt-broker)
- [A Guide on Collecting and Reporting Soil Moisture with ESP32 and Sensor through MQTT](https://www.emqx.com/en/blog/hands-on-guide-on-esp32)
- [Using MQTT on ESP8266: A Quick Start Guide](https://www.emqx.com/en/blog/esp8266-connects-to-the-public-mqtt-broker)
- [Remote control LED with ESP8266 and MQTT](https://www.emqx.com/en/blog/esp8266_mqtt_led)
- [How to Use MQTT on Raspberry Pi with Paho Python Client](https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi)
- [MicroPython MQTT Tutorial Based on Raspberry Pi](https://www.emqx.com/en/blog/micro-python-mqtt-tutorial-based-on-raspberry-pi)
- [How to Deploy an MQTT Broker on Raspberry Pi](https://www.emqx.com/en/blog/how-to-deploy-an-mqtt-broker-on-raspberry-pi)


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
