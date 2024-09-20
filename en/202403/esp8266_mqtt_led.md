## Introduction

This tutorial explores how to leverage the ESP8266 Wi-Fi module and [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) for remote control of an LED light.

The ESP8266 is a cost-effective Wi-Fi module that offers a highly integrated Wi-Fi SoC solution, suitable for low-power applications, compact design, and high stability to meet user needs. It boasts complete and self-contained Wi-Fi networking capabilities, functioning independently or as a slave to another host MCU.

MQTT is a publish/subscribe messaging protocol where two roles exist: the publisher and the subscriber. The publisher sends messages to a topic, and the subscriber receives messages from topics they are interested in. In this tutorial, we'll use the ESP8266 as the publisher to send messages to a topic, which a subscriber will listen to, allowing us to control the on/off state of an LED light remotely.

## Project Setup

### Prepare the Environment

Before embarking on this project, ensure you have the following hardware and software:

- **Hardware**:
  - 1 x NodeMCU ESP8266 development board
  - 1 x LED light
  - 1 x 330Ω resistor
  - 1 x Breadboard
  - Several Dupont wires
- **Software**:
  - Arduino IDE
  - MQTTX client (or another [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) of your choice)
  - We'll use a [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX, based on the [EMQX MQTT Platform](https://www.emqx.com/en/cloud). The server access information is as follows:
    - Broker: `broker.emqx.io`
    - TCP Port: `1883`
    - Websocket Port: `8083`

### Hardware Connection

Connect the long leg (anode) of the LED through a resistor to the D1 (GPIO 5) pin on the NodeMCU, and the short leg (cathode) directly to GND. The resistor is used to limit the current flowing through the LED to prevent damage.

![Connection Diagram](https://assets.emqx.com/images/55b153f1467569d91c93dc8ce1f55643.png)

## Connecting ESP8266 to the MQTT Server

### **Install ESP8266 Board Support**

In the Arduino IDE, go to "File" > "Preferences" and add the following URL to the "Additional Board Manager URLs": `http://arduino.esp8266.com/stable/package_esp8266com_index.json`. Then, in "Tools" > "Board" > "Boards Manager," search for and install the ESP8266 board.

### Install the PubSubClient Library

The `PubSubClient` library, necessary for connecting to MQTT servers, must be installed via the Arduino IDE's Library Manager by searching for `PubSubClient` and installing it.

### Define the LED Pin and State

Considering our hardware setup, we need to define the LED pin. In this case, we'll use the GPIO 5 (D1) pin to connect to the LED.

```c
#define LED 5 // GPIO 5 (D1) for LED
bool ledState = false;
```

### Initialize Wi-Fi Connection

Before we can connect to the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), we must first establish a Wi-Fi connection using the `ESP8266WiFi` library, an open-source Wi-Fi client library that facilitates connection to Wi-Fi networks.

```c
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi settings
const char *ssid = "YOUR_WIFI_SSID";             // Replace with your WiFi name
const char *password = "YOUR_WIFI_PASSWORD";   // Replace with your WiFi password
```

### Configure MQTT Broker Connection Parameters

We'll use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX for this tutorial.

```c
// MQTT Broker settings
const char *mqtt_broker = "broker.emqx.io";  // EMQX broker endpoint
const char *mqtt_topic = "emqx/esp8266/led";  // MQTT topic
const char *mqtt_username = "emqx";  // MQTT username for authentication (if required)
const char *mqtt_password = "public";  // MQTT password for authentication (if required)
const int mqtt_port = 1883;  // MQTT port (TCP)
```

### Initialize Wi-Fi and MQTT Clients

```c
WiFiClient espClient;
PubSubClient mqtt_client(espClient);
```

### Connect to Wi-Fi

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

### Connect to the MQTT Server and Subscribing to Topics

In this section, we'll connect to the MQTT server and subscribe to a topic. We'll use the `mqtt_client.connect()` method to connect to the MQTT server and then `mqtt_client.subscribe()` to subscribe to a topic and publish a test message upon successful connection.

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

### Write the Callback Function

When the MQTT client receives a message, we need to perform the LED light's on/off operation. We use the `mqtt_client.setCallback()` method to set up a callback function that executes when the MQTT client receives a message. If the message is "on," we turn on the LED; if "off," we turn it off.

```c
void mqttCallback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message received on topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    String message;
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];  // Convert *byte to string
    }
    // Control the LED based on the message received
    if (message == "on" && !ledState) {
        digitalWrite(LED, HIGH);  // Turn on the LED
        ledState = true;
        Serial.println("LED is turned on");
    }
    if (message == "off" && ledState) {
        digitalWrite(LED, LOW); // Turn off the LED
        ledState = false;
        Serial.println("LED is turned off");
    }
    Serial.println();
    Serial.println("-----------------------");
}
```

## Full Code

```c
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define LED 5 // GPIO 5 (D1) for LED
bool ledState = false;

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
    String message;
    for (int i = 0; i < length; i++) {
        message += (char) payload[i];  // Convert *byte to string
    }
    // Control the LED based on the message received
    if (message == "on" && !ledState) {
        digitalWrite(LED, HIGH);  // Turn on the LED
        ledState = true;
        Serial.println("LED is turned on");
    }
    if (message == "off" && ledState) {
        digitalWrite(LED, LOW); // Turn off the LED
        ledState = false;
        Serial.println("LED is turned off");
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

## Connecting and Testing

### Upload Code to ESP8266

Copy the complete code into the Arduino IDE and upload it to the ESP8266 development board. Open the serial monitor to observe the board connecting to the Wi-Fi network and then to the MQTT server.

![Upload Code to ESP8266](https://assets.emqx.com/images/740140a58ef90f9adb26413e159cc301.png)

### Control the LED with MQTTX

Use the [MQTTX](https://mqttx.app/) client to connect to the MQTT server, subscribe to the `emqx/esp8266/led` topic, and publish "on" messages to turn the LED on and "off" messages to turn it off.

![MQTTX](https://assets.emqx.com/images/d99306b8e2735d185d94c0ca5a5132aa.png)

## Conclusion

This tutorial guided you through using the ESP8266 and MQTT protocol for remote LED control. This project is just the tip of the iceberg in IoT applications. You can expand upon it by adding more sensors and actuators or integrating it into a home automation system.


## Related Resources

- [MQTT on ESP32: A Beginner's Guide](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker)
- [A Developer's Journey with ESP32 and MQTT Broker](https://www.emqx.com/en/blog/a-developer-s-journey-with-esp32-and-mqtt-broker)
- [A Guide on Collecting and Reporting Soil Moisture with ESP32 and Sensor through MQTT](https://www.emqx.com/en/blog/hands-on-guide-on-esp32)
- [Using MQTT on ESP8266: A Quick Start Guide](https://www.emqx.com/en/blog/esp8266-connects-to-the-public-mqtt-broker)
- [How to Use MQTT on Raspberry Pi with Paho Python Client](https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi)
- [MicroPython MQTT Tutorial Based on Raspberry Pi](https://www.emqx.com/en/blog/micro-python-mqtt-tutorial-based-on-raspberry-pi)
- [How to Deploy an MQTT Broker on Raspberry Pi](https://www.emqx.com/en/blog/how-to-deploy-an-mqtt-broker-on-raspberry-pi)


<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
