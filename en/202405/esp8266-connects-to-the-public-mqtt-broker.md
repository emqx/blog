## Introduction

[MQTT (Message Queuing Telemetry Transport)](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight, publish/subscribe messaging protocol ideal for device communication in bandwidth-constrained and unreliable networks. In IoT applications, MQTT efficiently connects numerous distributed devices, facilitating inter-device message communication.

The ESP8266 module is popular for its low cost, compact size, and built-in Wi-Fi capabilities, making it an ideal choice for developers and hobbyists entering the world of IoT.

In this tutorial, we delve into using the ESP8266 Wi-Fi module and MQTT protocol to quickly set up and execute an IoT communication project. You will learn how to configure the ESP8266 module to connect to an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and send and receive messages. Additionally, we will explore advanced topics such as TLS encryption to ensure secure and reliable IoT communications. 

## Project Setup

### Environment Preparation

Before starting the project, you need to prepare the following hardware and software:

- **Hardware**:
  - 1 x NodeMCU ESP8266 development board
- **Software**:
  - Arduino IDE
  - [MQTTX client](https://mqttx.app/) (or other MQTT client)
  - We will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX, based on the EMQX Platform. The broker access information is as follows:
    - Broker: `broker.emqx.io`
    - TCP Port: `1883`
    - TLS Port: `8883`
    - Websocket Port: `8083`
    - Websockets Port: `8084`

## Connecting ESP8266 to an MQTT Broker

### Installing Support for the ESP8266 Board

In the Arduino IDE, select "Preferences" from the "File" menu. In the dialog box that appears, find "Additional Board Manager URLs" and add the URL for ESP8266: `http://arduino.esp8266.com/stable/package_esp8266com_index.json`. Then, search and install ESP8266 from "Board Manager" under the "Tools" menu.

### Installing the PubSubClient Library

We also need to install the `PubSubClient` library in the Arduino IDE, which is used to connect to the MQTT broker. You can find and install this library through the Library Manager in the IDE.

### Initializing the Wi-Fi Connection

Before connecting to the MQTT broker, we first need to initialize the Wi-Fi connection. This can be done using the `ESP8266WiFi` library.

```c
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi settings
const char *ssid = "WIFI_SSID";             // Replace with your WiFi name
const char *password = "WIFI_PASSWORD";   // Replace with your WiFi password
```

### Setting MQTT Broker Connection Parameters

```c
// MQTT Broker settings
const char *mqtt_broker = "broker.emqx.io";  // EMQX broker endpoint
const char *mqtt_topic = "emqx/esp8266/led";  // MQTT topic
const char *mqtt_username = "emqx";  // MQTT username for authentication
const char *mqtt_password = "public";  // MQTT password for authentication
const int mqtt_port = 1883;  // MQTT port (TCP)
```

### Initializing the WIFI and MQTT Client

```c
WiFiClient espClient;
PubSubClient mqtt_client(espClient);
```

### Connecting to WIFI

```c
void connectToWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to the WiFi network");
}
```

### Connecting to the MQTT Broker and Subscribing to a Topic

This section will detail how to use the ESP8266 to connect to an MQTT broker via TCP and subscribe to a topic. The connection method discussed here is based on unencrypted TCP communication. While TCP connections are sufficient for most basic applications, if your project involves sensitive data or requires higher security, we recommend using TLS encryption.

#### TCP Connection

```c
void connectToMQTTBroker() {
    while (!mqtt_client.connected()) {
        String client_id = "esp8266-client-" + String(WiFi.macAddress());
        Serial.printf("Connecting to MQTT Broker as %s.....\n", client_id.c_str());
        if (mqtt_client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Connected to MQTT broker");
            mqtt_client.subscribe(mqtt_topic);
            // Publish message upon successful connection
            mqtt_client.publish(mqtt_topic, "Hi EMQX I'm ESP8266 ^^");
        } else {
            Serial.print("Failed to connect to MQTT broker, rc=");
            Serial.print(mqtt_client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}
```

#### TLS Connection

Additional settings are required if you need to connect to the MQTT broker via TLS. TLS connections provide encrypted data transfer, ensuring secure communication. To implement a TLS connection, you need to:

1. **CA Certificate**: Obtain and load the MQTT broker's CA certificate. This certificate is used to verify the broker's identity, ensuring that you are connecting to the correct broker.
2. **NTP Synchronization**: The ESP8266 device's time must be synchronized with global standard time. TLS connections require accurate system time to ensure the validity of TLS certificates. You can use an NTP (Network Time Protocol) client library for synchronization.

A complete TLS connection example and related code can be found on the following GitHub link: [ESP8266 MQTT TLS Example](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-ESP8266/esp8266_connect_mqtt_via_tls.ino). This example demonstrates how to configure the ESP8266 to use a TLS connection to the MQTT broker, including loading a CA certificate and setting up NTP synchronization.

### Writing the Callback Function

In MQTT communication, message reception is handled through a callback function. We need to define a callback function that is triggered when the ESP8266 receives a message from the MQTT broker. Our example will demonstrate how to receive and print message content within the callback function.

```c
void mqttCallback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message received on topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    for (unsigned int i = 0; i < length; i++) {
        Serial.print((char) payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");
}
```

## Full Code

Below is the full code for using the ESP8266 to connect to the MQTT broker via TCP. In this example, we use port `1883` for an unencrypted TCP connection. If your project requires higher security, such as using TLS encryption, you will need to set up a CA certificate and perform NTP synchronization. The complete TLS connection example code can be found on the following GitHub link: [ESP8266 MQTT TLS Example](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-ESP8266/esp8266_connect_mqtt_via_tls.ino).

```c
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi settings
const char *ssid = "WIFI_SSID";             // Replace with your WiFi name
const char *password = "WIFI_PASSWORD";   // Replace with your WiFi password

// MQTT Broker settings
const char *mqtt_broker = "broker.emqx.io";  // EMQX broker endpoint
const char *mqtt_topic = "emqx/esp8266";     // MQTT topic
const char *mqtt_username = "emqx";  // MQTT username for authentication
const char *mqtt_password = "public";  // MQTT password for authentication
const int mqtt_port = 1883;  // MQTT port (TCP)

WiFiClient espClient;
PubSubClient mqtt_client(espClient);

void connectToWiFi();

void connectToMQTTBroker();

void mqttCallback(char *topic, byte *payload, unsigned int length);

void setup() {
    Serial.begin(115200);
    connectToWiFi();
    mqtt_client.setServer(mqtt_broker, mqtt_port);
    mqtt_client.setCallback(mqttCallback);
    connectToMQTTBroker();
}

void connectToWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to the WiFi network");
}

void connectToMQTTBroker() {
    while (!mqtt_client.connected()) {
        String client_id = "esp8266-client-" + String(WiFi.macAddress());
        Serial.printf("Connecting to MQTT Broker as %s.....\n", client_id.c_str());
        if (mqtt_client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Connected to MQTT broker");
            mqtt_client.subscribe(mqtt_topic);
            // Publish message upon successful connection
            mqtt_client.publish(mqtt_topic, "Hi EMQX I'm ESP8266 ^^");
        } else {
            Serial.print("Failed to connect to MQTT broker, rc=");
            Serial.print(mqtt_client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void mqttCallback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message received on topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    for (unsigned int i = 0; i < length; i++) {
        Serial.print((char) payload[i]);
    }
    Serial.println();
    Serial.println("-----------------------");
}

void loop() {
    if (!mqtt_client.connected()) {
        connectToMQTTBroker();
    }
    mqtt_client.loop();
}
```

## Connection and Testing

### Uploading the Code to ESP8266

Copy the full code into the Arduino IDE, then upload it to your ESP8266 development board. Open the serial monitor, and you can see the ESP8266 board connecting to the Wi-Fi network and then to the MQTT broker.

![Connect to MQTT broker](https://assets.emqx.com/images/2107662edcf0f70fdcccfe1bdb5083c1.png)

### Using MQTTX to Send Messages to ESP8266

To test this functionality, you can use any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) software (like MQTTX) to connect to the same MQTT broker and send messages to the topic subscribed by ESP8266.

![MQTTX](https://assets.emqx.com/images/a2ed6b2e4659010965c9c28fd500867a.png)

Then, you can see these messages being correctly received and displayed in the ESP8266's serial output, which is a good way to check if the communication is successful.

![ESP8266's serial output](https://assets.emqx.com/images/33e31b4e4de289c649c56f7abb8d34c1.png)

## Conclusion

In this tutorial, we explored how to connect an MQTT broker with the ESP8266 Wi-Fi module, which is a common scenario in IoT projects.

Using the MQTT protocol, the ESP8266 can serve as a powerful node in an IoT network, handling data transmission and reception. This not only enhances device interoperability but also provides a broad platform for developing various IoT applications. You can use this foundation to expand more functions, such as integrating sensors, executing more complex commands, or interacting with other services.


## Resources

- [MQTT on ESP32: A Beginner's Guide](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker)
- [A Developer's Journey with ESP32 and MQTT Broker](https://www.emqx.com/en/blog/a-developer-s-journey-with-esp32-and-mqtt-broker)
- [A Guide on Collecting and Reporting Soil Moisture with ESP32 and Sensor through MQTT](https://www.emqx.com/en/blog/hands-on-guide-on-esp32)
- [Remote control LED with ESP8266 and MQTT](https://www.emqx.com/en/blog/esp8266_mqtt_led)
- [How to Use MQTT on Raspberry Pi with Paho Python Client](https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi)
- [MicroPython MQTT Tutorial Based on Raspberry Pi](https://www.emqx.com/en/blog/micro-python-mqtt-tutorial-based-on-raspberry-pi)
- [How to Deploy an MQTT Broker on Raspberry Pi](https://www.emqx.com/en/blog/how-to-deploy-an-mqtt-broker-on-raspberry-pi)

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
