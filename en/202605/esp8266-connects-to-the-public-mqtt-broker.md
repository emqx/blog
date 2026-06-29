## Introduction

[MQTT (Message Queuing Telemetry Transport)](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight, publish/subscribe messaging protocol ideal for device communication in bandwidth-constrained and unreliable networks. In IoT applications, MQTT efficiently connects distributed devices and enables lightweight message exchange.

The **ESP8266 Wi-Fi SoC** (highly popular in its **NodeMCU** development board format) offers a low-cost, compact hardware footprint that has become the industry benchmark for prototyping edge devices and low-power telemetry sensors. 

In this tutorial, we delve into using the ESP8266 Wi-Fi module and MQTT protocol to quickly set up and execute an IoT communication project. You will learn how to configure the ESP8266 module to connect to an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and send and receive messages. Additionally, we will explore advanced topics such as TLS encryption to ensure secure and reliable IoT communications. 

## ESP8266 MQTT Quick Start Summary

- ESP8266 connects to Wi-Fi using ESP8266WiFi library
- MQTT communication handled via PubSubClient
- Uses broker: broker.emqx.io
- Supports TCP (1883) and TLS (8883)
- Ideal for lightweight IoT sensor and edge devices

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

```c++
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi settings
const char *ssid = "WIFI_SSID";             // Replace with your WiFi name
const char *password = "WIFI_PASSWORD";   // Replace with your WiFi password
```

### Setting MQTT Broker Connection Parameters

```c++
// MQTT Broker settings
const char *mqtt_broker = "broker.emqx.io";  // EMQX broker endpoint
const char *mqtt_topic = "emqx/esp8266";  // MQTT topic
const char *mqtt_username = "emqx";  // MQTT username for authentication
const char *mqtt_password = "public";  // MQTT password for authentication
const int mqtt_port = 1883;  // MQTT port (TCP)
```

### Initializing the Wi-Fi and MQTT Client

```c++
WiFiClient espClient;
PubSubClient mqtt_client(espClient);
```

### Connecting to the Wi-Fi Network

```c++
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

```c++
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

Implementing an **MQTT TLS connection on the ESP8266** introduces significant cryptographic overhead due to the chip's limited 80KB volatile RAM memory footprint.

Modern ESP8266 Arduino cores utilize the **BearSSL engine** to establish secure `WiFiClientSecure` links. To implement a functional TLS session without encountering out-of-memory crashes, you must:

1. **Root CA Certificate Evaluation**: Load the server's public Root CA certificate in PEM format to securely cross-verify the MQTT broker's cryptographic identity during the TLS handshake.

2. **NTP Clock Synchronization**: Synchronize the ESP8266 local hardware real-time clock with global standard time using a Network Time Protocol (NTP) library. This step is mandatory for validating the certificate's activation and expiration timestamps.
3. **Maximum Fragment Length Negotiation (MFLN)**: (Optional but recommended) Reduce the SSL buffer allocations from 16KB down to 2KB or 4KB to protect the microchip's remaining heap storage.

For a production-ready implementation template demonstrating how to load certificates and orchestrate NTP time synchronization, refer directly to our official repository: [**ESP8266 MQTT TLS Example on GitHub**](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-ESP8266/esp8266_connect_mqtt_via_tls.ino).

### Writing the Callback Function

In MQTT communication, message reception is handled through a callback function. We need to define a callback function that is triggered when the ESP8266 receives a message from the MQTT broker. Our example will demonstrate how to receive and print message content within the callback function.

```c++
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

> ⚠️ **ESP8266 Architecture Alert (Soft WDT Reset):** The ESP8266 runs on a tight single-core Watchdog Timer (WDT) scheduling loop. If your `mqttCallback()` handles heavy computational calculations, block-writing data to flash, or long blocking delays, the hardware will assume a kernel lockup and trigger a `Soft WDT reset` crash. Always process heavy data back inside the main loop using a volatile global flag.

## Full Code

Below is the full code for using the ESP8266 to connect to the MQTT broker via TCP. In this example, we use port `1883` for an unencrypted TCP connection. If your project requires higher security, such as using TLS encryption, you will need to set up a CA certificate and perform NTP synchronization. The complete TLS connection example code can be found on the following GitHub link: [ESP8266 MQTT TLS Example](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-ESP8266/esp8266_connect_mqtt_via_tls.ino).

```c++
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi settings
const char *ssid = "WIFI_SSID";             // Replace with your WiFi name
const char *password = "WIFI_PASSWORD";   // Replace with your WiFi password

// MQTT Broker settings
const char *mqtt_broker = "broker.emqx.io";  // EMQX broker endpoint
const char *mqtt_topic = "emqx/esp8266";     // MQTT topic
const char *mqtt_username = "emqx";  // MQTT username for authentication
const char *mqtt_password = "public";  // MQTT password for authentication
const int mqtt_port = 1883;  // MQTT port (TCP)

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

![Arduino IDE Serial Monitor Log Showing ESP8266 NodeMCU Connecting to EMQ Public MQTT Broker](https://assets.emqx.com/images/2107662edcf0f70fdcccfe1bdb5083c1.png)

### Using MQTTX to Send Messages to ESP8266

To test this functionality, you can use any [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) software (like MQTTX) to connect to the same MQTT broker and send messages to the topic subscribed by ESP8266.

![MQTTX Desktop Client Simulating Inbound Telemetry Payload Routing to ESP8266 Subscriber](https://assets.emqx.com/images/a2ed6b2e4659010965c9c28fd500867a.png)

Then, you can see these messages being correctly received and displayed in the ESP8266's serial output, which is a good way to check if the communication is successful.

![Successful MQTT Message Ingestion Log Displayed in ESP8266 Serial Console](https://assets.emqx.com/images/33e31b4e4de289c649c56f7abb8d34c1.png)

## FAQ

### Why does PubSubClient drop connections on ESP8266 when handling larger payloads?

The standard `PubSubClient` configuration hardcodes `MQTT_MAX_PACKET_SIZE` to a lean **256 bytes**. When your ESP8266 intercepts or generates an array string or a bulky JSON payload larger than this window, the packet gets truncated, forcing the broker to drop the socket connection. 

To override this memory constraint, inject the size macro override at the absolute peak of your sketch before linking the library dependencies:

```c++
#define MQTT_MAX_PACKET_SIZE 1024 // Expand internal static buffer allocation to 1KB
#include <PubSubClient.h>
```

### How can I implement automatic Wi-Fi and MQTT client recovery on ESP8266?

Relying on blocking reconnection functions will halt your main application logic. The recommended architecture is to utilize a polling mechanism inside your `void loop()` that leverages non-blocking timestamp interval checks to independently maintain the connection states:

```c++
void maintainConnections() {
    if (WiFi.status() != WL_CONNECTED) {
        static unsigned long lastWiFiCheck = 0;
        if (millis() - lastWiFiCheck > 10000) { // Retry every 10s
            Serial.println("Reconnecting Wi-Fi...");
            WiFi.begin(ssid, password);
            lastWiFiCheck = millis();
        }
        return; // Halt MQTT processing until Wi-Fi re-establishes
    }

    if (!mqtt_client.connected()) {
        static unsigned long lastMQTTCheck = 0;
        if (millis() - lastMQTTCheck > 5000) {  // Retry every 5s
            connectToMQTTBroker();
            lastMQTTCheck = millis();
        }
    }
}
```

### What do common `mqtt_client.state()` integer error returns mean?

When your connection function fails, diagnosing the integer output returned by `mqtt_client.state()` saves hours of network capture troubleshooting:

| Error Integer | Enumeration Constant      | Root Cause Analysis                                          |
| :------------ | :------------------------ | :----------------------------------------------------------- |
| **-4**        | `MQTT_CONNECTION_TIMEOUT` | The broker endpoint did not respond within the allocated keep-alive window; common with firewall blocking. |
| **-2**        | `MQTT_CONNECT_FAILED`     | Physical network routing failed; the broker domain cannot be resolved by the local DNS. |
| **4**         | `MQTT_BAD_CREDENTIALS`    | The broker rejected the token identity; check for typos in your password/username strings. |
| **5**         | `MQTT_NOT_AUTHORIZED`     | Authentication succeeded but the Client ID violates client access-control lists (ACLs). |

### Why does ESP8266 fail to reconnect to MQTT broker intermittently?

ESP8266 may lose connection to the MQTT broker due to unstable Wi-Fi signals, insufficient heap memory, or blocking code inside the main loop that prevents the MQTT client from maintaining its connection.

To improve stability, ensure that `mqtt_client.loop()` is called frequently and avoid long blocking delays such as `delay()` inside your main program logic. It is also recommended to implement a non-blocking reconnection strategy using `millis()` instead of fixed delays.

### How much MQTT payload can ESP8266 handle safely?

The default PubSubClient library limits MQTT message size to 256 bytes, which is often insufficient for JSON or sensor data payloads.

To increase this limit, you can redefine the buffer size before including the library:

```c++
#define MQTT_MAX_PACKET_SIZE 1024
#include <PubSubClient.h>
```

However, it is recommended to keep payloads small on ESP8266 due to limited RAM resources, typically under 1KB for stable performance.

### Should I use MQTT over TCP or TLS on ESP8266?

For development and testing, MQTT over TCP (port 1883) is recommended due to its simplicity and lower memory usage.

For production deployments where security is important, MQTT over TLS (port 8883) should be used to encrypt communication and prevent data interception. However, TLS introduces additional memory and CPU overhead on ESP8266, so proper optimization such as certificate management and NTP time synchronization is required.

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
