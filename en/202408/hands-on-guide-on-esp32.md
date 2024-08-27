## Introduction

The ESP32 is a powerful Wi-Fi and Bluetooth module that offers a highly integrated SoC solution. Its low power consumption, compact design, and high stability make it ideal for IoT applications. The ESP32 features comprehensive Wi-Fi and Bluetooth network capabilities, allowing it to function as a standalone application or as a slave device to a host MCU.

The [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a message transport protocol based on a publish/subscribe model. In MQTT, there are two roles: publishers and subscribers. Publishers send messages to a topic, and subscribers subscribe to a topic. When a publisher sends a message to that topic, the subscribers receive the message. 

In this tutorial, we will explore how to use the ESP32 and the MQTT protocol to collect and report soil moisture data. We will use the ESP32 as a publisher to send soil moisture data to a topic, allowing a subscriber to receive and monitor this data remotely.

## Project Initialization

Before starting the project, ensure you have the following hardware and software.

### **Hardware Preparations**

1. ESP32 development board
2. Capacitive Soil Moisture Sensor v1.2

**Sensor Overview**

The capacitive soil moisture sensor v1.2 uses voltage to detect soil moisture levels. The sensor readings vary based on the supply voltage and the specific sensor. By placing the sensor in air and water, we can obtain calibration values that help determine whether the soil is dry or wet. For example, some capacitive sensors provide the following readings:

At 1.3V:

- In air: above 2000
- In water: below 1000

At 5V:

- In air: above 800
- In water: below 500

### **Software Preparations**

1. **Arduino IDE**: For writing and uploading code to the ESP32
2. [**MQTTX Client**](https://mqttx.app/) **or another MQTT client**: For testing MQTT message publishing and subscribing
3. **[Free Public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQX**: Supports nearby sensor access and unified management. EMQX Public Broker server access information:
   - Broker: `broker.emqx.io`
   - TCP Port: `1883`
   - TLS Port: `8883`
   - Websocket Port: `8083`
   - Websockets Port: `8084`

### Hardware Connection

Connect the ESP32 and the soil moisture sensor as follows:

- Sensor VCC to ESP32 VIN
- Sensor GND to ESP32 GND
- Sensor AOUT to ESP32 GPIO36 (ADC0): In this project, we will use the ESP32 pin GPIO36 (ADC0) to connect to the AOUT pin of the moisture sensor to read soil moisture data.

## Connecting ESP32 to the MQTT Broker 

### Installing ESP32 Board Support

Open Arduino IDE, go to **File** -> **Preferences**. In the "Additional Boards Manager URLs" field, add the following URL:

```
https://dl.espressif.com/dl/package_esp32_index.json
```

Next, go to **Tools** -> **Board** -> **Boards Manager**, search for ESP32, and install it.

### Installing PubSubClient Library

In Arduino IDE, go to **Sketch** -> **Include Library** -> **Manage Libraries**, search for `PubSubClient`, and install it.

### Initializing WiFi and MQTT Clients

To begin, we need to initialize the WiFi and [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools). This will allow the ESP32 to connect to the internet and communicate with the MQTT server. First, include the necessary libraries and define the WiFi credentials:

```c
#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

// WiFi credentials
const char *ssid = "WIFI_SSID"; // Replace with your WiFi name
const char *password = "WIFI_PASSWORD"; // Replace with your WiFi password

// MQTT Broker configuration
const char *mqtt_broker = "broker.emqx.io";
const char *mqtt_topic = "emqx/esp32/moisture";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 8883;
```

Next, initialize the WiFi and MQTT clients:

```c
WiFiClientSecure esp_client;
PubSubClient mqtt_client(esp_client);
```

### Defining the Sensor Pin

The GPIO36 (ADC0) pin on the ESP32 is used to connect to the AOUT pin of the soil moisture sensor. This pin is chosen because it supports analog-to-digital conversion, which is necessary for reading the sensor's analog output.

```c
#define sensorPIN 36
```

### Loading the CA Certificate

To establish a secure connection to the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) using TLS, we need to load a root CA certificate. This example uses the DigiCert Global Root G2 certificate, which is used by the EMQX public broker. If you are using a different server, replace this certificate with the appropriate one.

```c
const char *ca_cert = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDjjCCAnagAwIBAgIQAzrx5qcRqaC7KGSxHQn65TANBgkqhkiG9w0BAQsFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBH
MjAeFw0xMzA4MDExMjAwMDBaFw0zODAxMTUxMjAwMDBaMGExCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IEcyMIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuzfNNNx7a8myaJCtSnX/RrohCgiN9RlUyfuI
2/Ou8jqJkTx65qsGGmvPrC3oXgkkRLpimn7Wo6h+4FR1IAWsULecYxpsMNzaHxmx
1x7e/dfgy5SDN67sH0NO3Xss0r0upS/kqbitOtSZpLYl6ZtrAGCSYP9PIUkY92eQ
q2EGnI/yuum06ZIya7XzV+hdG82MHauVBJVJ8zUtluNJbd134/tJS7SsVQepj5Wz
tCO7TG1F8PapspUwtP1MVYwnSlcUfIKdzXOS0xZKBgyMUNGPHgm+F6HmIcr9g+UQ
vIOlCsRnKPZzFBQ9RnbDhxSJITRNrw9FDKZJobq7nMWxM4MphQIDAQABo0IwQDAP
BgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBhjAdBgNVHQ4EFgQUTiJUIBiV
5uNu5g/6+rkS7QYXjzkwDQYJKoZIhvcNAQELBQADggEBAGBnKJRvDkhj6zHd6mcY
1Yl9PMWLSn/pvtsrF9+wX3N3KjITOYFnQoQj8kVnNeyIv/iPsGEMNKSuIEyExtv4
NeF22d+mQrvHRAiGfzZ0JFrabA0UWTW98kndth/Jsw1HKj2ZL7tcu7XUIOGZX1NG
Fdtom/DzMNU+MeKNhJ7jitralj41E6Vf8PlwUHBHQRFXGU7Aj64GxJUTFy8bJZ91
8rGOmaFvE7FBcf6IKshPECBV1/MUReXgRPTqh5Uykw7+U0b6LJ3/iyK5S9kJRaTe
pLiaWN0bfVKfjllDiIGknibVb63dDcY3fe0Dkhvld1927jyNxF1WW6LZZm6zNTfl
MrY=
-----END CERTIFICATE-----
)EOF";
```

### Connecting to the MQTT Broker

The `connectToMQTT()` function is responsible for establishing a connection to the MQTT broker using TLS. It sets the CA certificate and then attempts to connect using the specified broker address, port, and credentials. The function also sets a keep-alive interval to ensure the connection remains active.

```c
void connectToMQTT() {
    esp_client.setCACert(ca_cert);  // Set the CA certificate for secure connection
    mqtt_client.setServer(mqtt_broker, mqtt_port);  // Set the MQTT broker server and port
    mqtt_client.setKeepAlive(60);  // Set the keep-alive interval to 60 seconds

    while (!mqtt_client.connected()) {
        String client_id = "esp32-client-" + String(WiFi.macAddress());  // Generate a unique client ID
        Serial.printf("Connecting to MQTT Broker as %s...\n", client_id.c_str());
        if (mqtt_client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Connected to MQTT Broker");
        } else {
            Serial.print("Failed to connect, rc=");
            Serial.print(mqtt_client.state());  // Print the connection state for debugging
            Serial.println(" Retrying in 5 seconds.");
            delay(5000);  // Wait for 5 seconds before retry

ing
        }
    }
}
```

### Publishing Sensor Data

The `publishSensorData()` function reads the soil moisture sensor data, formats it as a JSON object, and publishes it to the specified MQTT topic. This function ensures the data is correctly serialized and sent over the MQTT protocol.

```c
void publishSensorData() {
    StaticJsonDocument<200> json_doc;
    int moistureValue = analogRead(sensorPIN);  // Read the moisture sensor value
    json_doc["moisture"] = moistureValue;  // Add the sensor value to the JSON document

    char json_buffer[512];
    serializeJson(json_doc, json_buffer);  // Serialize the JSON document to a string
    mqtt_client.publish(mqtt_topic, json_buffer);  // Publish the JSON string to the MQTT topic
    Serial.printf("Published to %s: %d\n", mqtt_topic, moistureValue);  // Print the published message for debugging
}
```

### Complete Code

Here's the complete code with the functions and explanations combined:

```c
#include <WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

// WiFi credentials
const char *ssid = "WIFI_SSID"; // Replace with your WiFi name
const char *password = "WIFI_PASSWORD"; // Replace with your WiFi password

// MQTT Broker configuration
const char *mqtt_broker = "broker.emqx.io";
const char *mqtt_topic = "emqx/esp32/moisture";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 8883;

// WiFi and MQTT client initialization
WiFiClientSecure esp_client;
PubSubClient mqtt_client(esp_client);

// GPIO pin for Soil Moisture, ESP32 pin GPIO36 (ADC0) that connects to AOUT pin of moisture sensor
#define sensorPIN 36

// Root CA Certificate
const char *ca_cert = R"EOF(
-----BEGIN CERTIFICATE-----
MIIDjjCCAnagAwIBAgIQAzrx5qcRqaC7KGSxHQn65TANBgkqhkiG9w0BAQsFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBH
MjAeFw0xMzA4MDExMjAwMDBaFw0zODAxMTUxMjAwMDBaMGExCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IEcyMIIBIjANBgkqhkiG
9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuzfNNNx7a8myaJCtSnX/RrohCgiN9RlUyfuI
2/Ou8jqJkTx65qsGGmvPrC3oXgkkRLpimn7Wo6h+4FR1IAWsULecYxpsMNzaHxmx
1x7e/dfgy5SDN67sH0NO3Xss0r0upS/kqbitOtSZpLYl6ZtrAGCSYP9PIUkY92eQ
q2EGnI/yuum06ZIya7XzV+hdG82MHauVBJVJ8zUtluNJbd134/tJS7SsVQepj5Wz
tCO7TG1F8PapspUwtP1MVYwnSlcUfIKdzXOS0xZKBgyMUNGPHgm+F6HmIcr9g+UQ
vIOlCsRnKPZzFBQ9RnbDhxSJITRNrw9FDKZJobq7nMWxM4MphQIDAQABo0IwQDAP
BgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBhjAdBgNVHQ4EFgQUTiJUIBiV
5uNu5g/6+rkS7QYXjzkwDQYJKoZIhvcNAQELBQADggEBAGBnKJRvDkhj6zHd6mcY
1Yl9PMWLSn/pvtsrF9+wX3N3KjITOYFnQoQj8kVnNeyIv/iPsGEMNKSuIEyExtv4
NeF22d+mQrvHRAiGfzZ0JFrabA0UWTW98kndth/Jsw1HKj2ZL7tcu7XUIOGZX1NG
Fdtom/DzMNU+MeKNhJ7jitralj41E6Vf8PlwUHBHQRFXGU7Aj64GxJUTFy8bJZ91
8rGOmaFvE7FBcf6IKshPECBV1/MUReXgRPTqh5Uykw7+U0b6LJ3/iyK5S9kJRaTe
pLiaWN0bfVKfjllDiIGknibVb63dDcY3fe0Dkhvld1927jyNxF1WW6LZZm6zNTfl
MrY=
-----END CERTIFICATE-----
)EOF";

// Function Declarations
void connectToWiFi();
void connectToMQTT();
void publishSensorData();

void setup() {
    Serial.begin(115200);
    connectToWiFi();
    connectToMQTT();
}

void connectToWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi");
}

void connectToMQTT() {
    esp_client.setCACert(ca_cert);  // Set the CA certificate for secure connection
    mqtt_client.setServer(mqtt_broker, mqtt_port);  // Set the MQTT broker server and port
    mqtt_client.setKeepAlive(60);  // Set the keep-alive interval to 60 seconds

    while (!mqtt_client.connected()) {
        String client_id = "esp32-client-" + String(WiFi.macAddress());  // Generate a unique client ID
        Serial.printf("Connecting to MQTT Broker as %s...\n", client_id.c_str());
        if (mqtt_client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Connected to MQTT Broker");
        } else {
            Serial.print("Failed to connect, rc=");
            Serial.print(mqtt_client.state());  // Print the connection state for debugging
            Serial.println(" Retrying in 5 seconds.");
            delay(5000);  // Wait for 5 seconds before retrying
        }
    }
}

void publishSensorData() {
    StaticJsonDocument<200> json_doc;
    int moistureValue = analogRead(sensorPIN);  // Read the moisture sensor value
    json_doc["moisture"] = moistureValue;  // Add the sensor value to the JSON document

    char json_buffer[512];
    serializeJson(json_doc, json_buffer);  // Serialize the JSON document to a string
    mqtt_client.publish(mqtt_topic, json_buffer);  // Publish the JSON string to the MQTT topic
    Serial.printf("Published to %s: %d\n", mqtt_topic, moistureValue);  // Print the published message for debugging
}

void loop() {
    if (!mqtt_client.connected()) {
        connectToMQTT();
    }
    mqtt_client.loop();

    publishSensorData();
    delay(60000); // Delay between readings
}
```

## Connecting and Testing

### Uploading Code to ESP32

Copy the above code into the Arduino IDE, connect your ESP32 to your computer, select the appropriate board and port, and click the upload button to upload the code to the ESP32.

### Reading Sensor Data and Publishing via MQTT

Once the code is uploaded, open the Serial Monitor. You will see logs indicating the ESP32's connection to the Wi-Fi and MQTT Broker, and soil moisture data will be reported every minute. 

![Serial Monitor](https://assets.emqx.com/images/e9b1e49651048e852771964b3f2388d4.png)

### Using MQTTX to Subscribe to a Topic and Retrieve Soil Moisture Published by ESP32

We can use the MQTTX desktop MQTT client to connect to `broker.emqx.io` and then subscribe to the `emqx/esp32/moisture` topic to retrieve the soil moisture published by the ESP32.

![MQTTX](https://assets.emqx.com/images/78cfc74b022026457ff0caa5068524af.png)

## Conclusion

In this tutorial, you learned how to use the ESP32 and a soil moisture sensor to collect soil moisture data and report it to a server via the MQTT protocol. This is just the tip of the iceberg for IoT applications. You can build on this project to explore more possibilities, such as adding more sensors to monitor different environmental parameters or integrating them into an agricultural automation system for smart irrigation.

You can delve deeper into the advanced features of MQTT, such as message retention, last will and testament messages, and explore other functionalities of the ESP32 to expand your IoT projects and achieve more complex application scenarios.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
