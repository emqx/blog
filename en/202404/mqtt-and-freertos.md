## Real-Time Operating System & FreeRTOS

Operating systems are everywhere in our lives. We use various operating systems daily. Windows, macOS, and Linux on our personal computers; and iOS and Android on our smartphones, are the most known operating systems to users.

Yet, despite being just as widespread in our daily lives, there is a kind of operating system that rarely captures our attention—the Real-Time Operating System (RTOS).

The fundamental distinction between an RTOS and other operating systems, as implied by its name, is its real-time capability. Consider the significant safety implications if the time taken for a vehicle's operating system to detect a severe impact and subsequently control the airbag deployment varies from mere milliseconds to tens of milliseconds for the passengers.

Likewise, industries such as aerospace, medical equipment, and industrial control have stringent demands for prompt task response, a criterion that only RTOS can satisfy.

[FreeRTOS](https://freertos.org/) is an open-source RTOS designed for microcontrollers and small microprocessors. It supports a variety of processor architectures such as ARM, PIC, and x86, and offers preemptive and time-slicing scheduling. It also provides several synchronization and communication mechanisms such as mutexes and semaphores. Its mature and open-source [code](https://github.com/FreeRTOS/FreeRTOS), extensive documentation, and vibrant community make FreeRTOS a preferred choice for developing embedded real-time applications.

## Build Applications with EMQX and FreeRTOS

As a lightweight and compact RTOS, FreeRTOS is well-suited for deployment in resource-constrained IoT devices, such as industrial control systems, smart homes, and robotic controls.

These types of IoT applications require the implementation of local real-time control logic and the ability to communicate and interact with external systems. For example, they may need to synchronize the latest device statuses or respond to remote commands. In such scenarios, the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), which supports the publish-subscribe model, is the most common choice.

The asynchronous communication offered by the EMQX MQTT Platform enables the decoupling of communication parties, allowing them to focus more on implementing their business logic. Furthermore, EMQX supports various message distribution modes, such as multicast and broadcast, and enables the setting of message reliability as needed. It also permits devices to go offline briefly without losing messages and supports setting a "last will" for clients. These features significantly enhance application development efficiency.

If you haven't yet explored the integration of FreeRTOS and EMQX in application development, please continue reading. This article will demonstrate how to use EMQX for message exchange in FreeRTOS and collaborate with other real-time tasks through a practical demonstration.

## Demo Overview

In this demo, we will remotely control the on/off, hue, saturation, and brightness of the RGB LED, switch between regular blinking and rainbow cycling display modes via MQTT protocol, and receive the latest LED operation status from the device via MQTT protocol to know whether the commands have been executed correctly or not.

![07connect.png](https://assets.emqx.com/images/11141dc022f25b60c6e10c0ba5524920.png)

To achieve this goal, we implement the below functions.

- The MQTT event callback function in FreeRTOS maintains the connection, and parses and processes MQTT messages.
- The LED task changes the operational state of the LEDs based on notifications from the MQTT event callback function and publishes MQTT messages indicating the latest LED state.
- The Wi-Fi event callback function that implements Wi-Fi connectivity. 

The LED task can be replaced with any other real-world application, such as a camera gimbal control application, a drone attitude control application, etc. This demo shows the basic usage of the MQTT library in FreeRTOS, such as building an MQTT connection, sending/receiving messages, and synchronizing parsed commands to other tasks using the FreeRTOS queue mechanism.

## What You Need?

### Hardware

In this demo, we used an ESP32 development board with an integrated 2.4GHz Wi-Fi communication module, then we could connect to the internet wirelessly.

I am using a board with an integrated ESP32-S3-WROOM-1-N8R8 module. You can use other ESP32 chips instead, such as ESP32-S2 or ESP32-C3. The major difference in the S3 version is the support of dual core and Bluetooth.

In this demo, I enabled the single-core mode with the `CONFIG_FREERTOS_UNICORE` option of the ESP-IDF,  so the demo can run directly on a single-core CPU.

In addition, we need to use an RGB LED driven by a WS2812 series chip (WS2812, WS2812B, WS2812C, etc.). We will use the ESP32's RMT peripheral to control this LED.

The development board I use comes with an RGB LED driven by WS2812B. If your board does not have such an LED, you can connect an external LED module, or directly modify the LED task code to print the corresponding content on the serial port.

### Software

For the development and execution of this demo, we need the following software:

1. [ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/index.html) v5.2.1, the official development framework from Espressif for application development on the ESP32 series chip. It is recommended to install ESP-IDF within an IDE. I’m using VS Code.
2. [EMQX](https://www.emqx.com/en), an enterprise-grade MQTT platform. We used the [EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) in this demo, thus eliminating the need for manual server deployment.
3. [MQTTX](https://mqttx.app/), MQTT client tool for sending LED commands to ESP32 and receiving returned LED status.

The deployment of EMQX Cloud Serverless and MQTTX is straightforward and will not be repeated here. ESP-IDF recommends installing them as a VSCode extension. The general installation steps are:

1. If your operating system is Linux or macOS, you initially need to install dependencies such as Python3, CMake, and Ninja. Details can be found in [Step 1. Install Prerequisites](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/linux-macos-setup.html#step-1-install-prerequisites).
2. Download and install [Visual Studio Code](https://code.visualstudio.com/).
3. In the Extensions view of VS Code, search for and install ESP-IDF.
4. In the command panel of VS Code (combination key Shift+Command+P or Shift+Ctrl+P), select `ESP-IDF: Configure ESP-IDF Extension` to enter the ESP-IDF setup wizard.
5. Select the EXPRESS setup mode, and then sequentially select the ESP-IDF version to download, the ESP-IDF tool installation path, and the local Python executable file path. Finally, click `Install` and wait for the installation to complete.

Detailed installation steps can be referenced in this [ESP-IDF Official Document](https://github.com/espressif/vscode-esp-idf-extension/blob/master/docs/tutorial/install.md).

## Demo Code Explanation

### Directory Structure

The complete demo code has been uploaded to GitHub and can be downloaded [here](https://github.com/emqx/bootcamp/tree/main/mqtt-and-rtos/freertos-demo).

The main structure of the demo code is as follows:

```
|-- components
    |-- esp-mqtt
    |-- led_strip
|-- main
    |-- CMakeLists.txt
    |-- demo.c
    |-- demo.h
    |-- emqxsl_ca.crt
    |-- Kconfig.projbuild
|-- CMakeLists.txt
|-- sdkconfig
|-- sdkconfig.defaults
```

#### Directory - components 

The `esp-mqtt` and `led_strip` components under the `components` directory are from the official Espressif. However, in this demo, the default behavior of these two components does not meet our requirements, so we copy them directly into the components directory and use them as project components after modification.

#### Directory - main

`CMakeLists.txt` in the `main` directory and the project root directory defines the construction rules of the project. For details, please refer to the [ESP-IDF Official Documentation](https://docs.espressif.com/projects/esp-idf/en/v5.2.1/esp32/api-guides/build-system.html).

`demo.c` and `demo.h` contain all the primary code of this demo, which we will introduce in detail below.

`emqx_sl_ca.crt` is the CA certificate to establish a TLS connection with EMQX Cloud Serverless. It can be downloaded from the overview page of the Serverless deployment:

![01serverlessoverview.png](https://assets.emqx.com/images/0090f9de9afa843cd46f9321a74dfefd.png)

To use this CA certificate in code, we can embed it into the firmware through the `target_add_binary_data` function in the top-level `CMakeLists.txt`:

```c
target_add_binary_data(demo.elf "main/emqxsl_ca.crt" TEXT)
```

The `target_add_binary_data` function does not recognize dashes in file names, we can manually change the dashes in the CA certificate file name to underscores.

Finally, we can access the embedded file content in the code in the following ways:

```c
extern const uint8_t server_cacertificate_start[]  asm("_binary_emqxsl_ca_crt_start");
extern const uint8_t server_cacertificate_end[]  asm("_binary_emqxsl_ca_crt_end");
```

This demo also provides another method of using the CA certificate, which will be introduced in the later chapter - **Run** **Demo**.

`Kconfig.projbuild` contains custom configuration items for the current project. The `Kconfig.probuild` file in this demo mainly defines configuration items such as Wi-Fi SSID, Wi-Fi password, and MQTT server address.

In addition, the component configuration is defined in the `Kconfig` file in the component's own root directory. It is provided to projects or other components that depend on the component. For example, the `esp-mqtt` component provides configuration items such as MQTT task priority and whether to enable MQTT 5.0 support.

We can execute `idf.py menuconfig` or select `ESP-IDF: SDK Configuration editor (Menuconfig)` in the command panel of VS Code to enter the configuration menu, which contains all modifiable configuration items. Changing the values of these configuration items adjusts the behavior of your application code.

#### sdkconfig and sdkconfig.defaults

The complete changed configuration will be stored in the `sdkconfig` file. `sdkconfig` is usually automatically generated and manual modification is not recommended.

The last `sdkconfig.defaults` is an optional file. During the project build, an `sdkconfig` file will be automatically created, using the configurations within `sdkconfig.defaults` to override the default values defined in `Kconfig` and `Kconfig.projbuild`.

The `sdkconfig.defaults` in this demo records the necessary configuration changes to ensure that this demo builds and runs correctly:

```
# Enable support for MQTT 5.0
CONFIG_MQTT_PROTOCOL_5=y
# Enable single-core mode for operation on single-core platforms such as ESP32-S2
CONFIG_FREERTOS_UNICORE=y
```

If you don't want to lose the previous configuration changes every time you modify `Kconfig.projbuild` and regenerate `sdkconfig`, you can put those changes into `sdkconfig.defaults`.

For a detailed introduction to `Kconfig` and `sdkconfig`, please refer to the [Build System](https://docs.espressif.com/projects/esp-idf/en/v5.2.1/esp32/api-guides/build-system.html) chapter of the official ESP-IDF documentation.

### Functional Implementation

![08functions.png](https://assets.emqx.com/images/54f9e5f648a12bff92b1c4f5ed8bc1da.png)

#### Component - esp-mqtt

`esp-mqtt` is an internal component of ESP-IDF, providing an implementation of an MQTT client. It supports MQTT 3.1.1 and 5.0, one-way and two-way TLS authentication, and persistent sessions, the full three Quality of Service (QoS) levels, among most other MQTT features.

However, its implementation of Reason Code has not yet fully adapted to MQTT 5.0. For example, it only regards `0x80` as a subscription failure, while MQTT 5.0 provides more Reason Codes indicating different failure reasons. Consequently, in this demo, the `deliver_suback` function in `esp-mqtt/mqtt_client.c` has been modified. The specific changes are as follows:

```c
// Before
if ((uint8_t)msg_data[topic] == 0x80) {
// After
if ((uint8_t)msg_data[topic] >= 0x80) {
```

Moreover, as the `esp-mqtt` component does not clear the memory before receiving messages, remnants of previous data may impede functions such as `sscanf` from accurately parsing data.

Setting the one byte following valid data to `\0` can rectify this issue but it may lead to out-of-bounds memory access. So we need to allocate an extra byte of memory during initialization, with the specific change located in the `esp_mqtt_client_init` function within `esp-mqtt/mqtt_client.c`:

```c
// Before
client->mqtt_state.in_buffer = (uint8_t *)malloc(buffer_size);
// After
client->mqtt_state.in_buffer = (uint8_t *)malloc(buffer_size + 1);
```

#### Component - led_strip

`led_strip` is an accessory component provided by ESP-IDF. It provides RMT and SPI two ways to drive addressable LEDs such as WS2812, and can drive multiple LEDs on a light strip. This demo uses the RMT peripheral.

The reason for modifying this component's code resides in the theory that the data sequence written into the WS2812 chip should adhere to the GRB order, however, my hardware parses the data in an RGB sequence. Consequently, I modified the `led_strip_rmt_set_pixel` function within `led_strip/src/led_strip/rmt/dev.c`, the specifics of which are detailed below:

```c
// Before
rmt_strip->pixel_buf[start + 0] = green & 0xFF;
rmt_strip->pixel_buf[start + 1] = red & 0xFF;c
// After
rmt_strip->pixel_buf[start + 0] = red & 0xFF;
rmt_strip->pixel_buf[start + 1] = green & 0xFF;
```

#### Wi-Fi Event Callback Function in demo.c

Both Wi-Fi and MQTT components use event loops, and the essence of the event loop is still a queue mechanism. In the event loop, we only need to implement event callback functions and register these functions to the corresponding event.

The Wi-Fi component uses a default event loop task with a priority of 20. The Wi-Fi component also has its own task with a higher default priority of 23. Since we have enabled single-core mode, these tasks will only run on CPU core 0.

The Wi-Fi event callback function `wifi_event_handler` in this demo only handles three events: `WIFI_EVENT_STA_START`, `WIFI_EVENT_STA_DISCONNECTED,` and `IP_EVENT_STA_GOT_IP`, realizing the first connection, disconnection and reconnection of Wi-Fi.

Event `IP_EVENT_STA_GOT_IP` comes from LwIP's TCP/IP task with a default priority of 18. Since socket operations such as connecting to an MQTT server rely on IPv4 addresses, we must wait for the `IP_EVENT_STA_GOT_IP` instead of the `WIFI_EVENT_STA_CONNECTED` event.

Here we also use an event group to block the main process until the Wi-Fi event callback function sets the corresponding bit:

```c
else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
    ...
    xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
}
```

A robust network application should also handle other Wi-Fi events in the callback function. Please refer to the [WiFi driver documentation](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/wifi.html) of ESP-IDF for more details.

#### MQTT Event Callback Function in demo.c

The MQTT component does not create additional event loop tasks. The MQTT task is responsible for the  MQTT events dispatch and scheduling of the event handlers. It is implicitly created by the `esp_mqtt_client_start` function, with a default priority of 5.

The MQTT event callback function in this demo, `mqtt5_event_handler`, primarily handles `MQTT_EVENT_CONNECTED`, `MQTT_EVENT_DATA`, and `MQTT_EVENT_ERROR` events.

The `MQTT_EVENT_CONNECTED` event means a successful connection. We can determine whether we need to resubscribe to the topic based on `event->session_present`:

```c
if(event->session_present == false) {
    // Re-subscribe
    for(int i = 0; i < subscriptions->size; i++)
    {
        subscriptions->subscription[i].msg_id = esp_mqtt_client_subscribe(client, (char *)subscriptions->subscription[i].topic, 0);
        subscriptions->subscription[i].subscribed = false;
        ESP_LOGI(TAG, "subscribing to topic=%s, msg_id=%d",
            subscriptions->subscription[i].topic, subscriptions->subscription[i].msg_id);
    }
}
```

Then use a retained message with QoS 1 to synchronize the latest LED status with the MQTT server:

```c
xSemaphoreTake(s_led_state_lock, portMAX_DELAY);
led_state_t led_state = s_led_state;
xSemaphoreGive(s_led_state_lock);
sync_led_state(client, &led_state);
```

Retaining messages is an important feature of MQTT. The MQTT server will store and only store the latest retained message for each topic so that it can be delivered to future subscribers. This enables efficient state synchronization under the premise of asynchronous communication.

Setting the QoS of the message to 1 ensures that the message reaches the server:

```c
esp_mqtt_client_enqueue(client, TOPIC_STAT_HSB, s_msg, 0, QOS_1, RETAIN, true)
```

QoS 1 may cause the peer to receive duplicate messages. In this demo, the state messages sent and the command messages received indicate absolute states, duplicate messages are acceptable.

`MQTT_EVENT_DATA` indicates that a message has arrived. Here we implement a simple callback mechanism, that is, calling the corresponding message callback function according to the topic in the message:

```c
for(int i = 0; i < subscriptions->size; i++) {
    uint16_t len = strlen(subscriptions->subscription[i].topic);
    if(!strncmp(subscriptions->subscription[i].topic, event->topic, len < event->topic_len ? len : event->topic_len)) {
        subscriptions->subscription[i].handler(event->data, event->data_len);
        break;
    }
}
```

The logic of the message callback functions implemented in this demo is similar, further parsing the message's Payload, and creating a new LED target state. This state indicates how the LED should run, such as hue, saturation, and brightness, and is synchronized to the LED task through a queue.

The `MQTT_EVENT_ERROR` event indicates that an error has occurred. The processing in this demo is simple, merely printing the detailed cause of the error via the serial port.

#### LED Task in demo.c

The default priority of the LED task is 4, which can be modified through the configuration item `LED task priority` in the `Demo Configuration` sub-menu.

Each cycle of the LED task will first check whether a new message has arrived in the queue. If a new message arrives, the running state will be adjusted based on the message. Otherwise, it will continue to run in the original state.

If the LED status changes, we use a retained message with QoS 1 to synchronize the latest LED status with the MQTT server and save the status to Flash through the NVS library:

```c
store_led_state_in_nvs(handle, &led_state);
sync_led_state(client, &led_state);
```

In this way, we can read the LED status stored in Flash when power is turned on next time and run directly in this status:

```c
get_value_from_nvs(handle, "power", (void *)&s_led_state.power, NVS_TYPE_U8);
get_value_from_nvs(handle, "hue", (void *)&s_led_state.hue, NVS_TYPE_U16);
get_value_from_nvs(handle, "saturation", (void *)&s_led_state.saturation, NVS_TYPE_U8);
get_value_from_nvs(handle, "brightness", (void *)&s_led_state.brightness, NVS_TYPE_U8);
get_value_from_nvs(handle, "mode", (void *)&s_led_state.mode, NVS_TYPE_U8);
get_value_from_nvs(handle, "on_time", (void *)&s_led_state.on_time, NVS_TYPE_U16);
get_value_from_nvs(handle, "off_time", (void *)&s_led_state.off_time, NVS_TYPE_U16);
get_value_from_nvs(handle, "speed", (void *)&s_led_state.speed, NVS_TYPE_U8);
```

### Configuration

This demo provides some custom configuration items (defined in `Kconfig.projbuild`), which can be found in the `Demo Configuration` submenu at the top level of the configuration menu.

These configuration items are mainly related to your operating environment, such as Wi-Fi SSID and password, MQTT server address, GPIO pins corresponding to the LED, etc.

We can quickly make this demo code run in your local environment by modifying these configuration items.

![02democonfiguration.png](https://assets.emqx.com/images/f48d7b4202114cd638bb98a21659a7fb.png)

### MQTT Message Design

#### Command Message

This demo supports remote configuration of the LED's on/off state, hue, saturation, brightness, blink interval, and cyclic speed in rainbow mode, so four command messages are designed. Commands rely on the topic `cmnd/led/<command>` and the payload `<param1>,[<param2>,...]`. If multiple parameters exist in the payload, they are separated by a comma `,`.

##### Command 1 - Turn on/off the LED

**Topic**: `cmnd/led/power`

**Payload**: `<power>`

**Parameter description**:

`<power>` = `on`, turn on the LED.

`<power>` = `off`, turn off the LED.

**Payload Example**: `on`

##### Command 2 - Set the hue of the LED

**Topic**: `cmnd/led/hue`

**Payload**: `<hue>`

**Parameter description**:

`<hue>` = `0..360`, set the hue of the LED

**Payload Example**: `360`

##### Command 3 - Set the hue, saturation, and brightness of the LED

**Topic**: `cmnd/led/hsb`

**Payload**: `<hue>,<saturation>,<brightness>`

**Parameter description**:

`<hue>` = `0..360`, set the hue of the LED

`<saturation>` = `0..255`, set the saturation of the LED

`<brightness>` = `0..255`, set the brightness of the LED

**Payload Example**: `180,255,255`

##### Command 4 - Set the LED display mode

**Topic**: `cmnd/led/mode`

**Payload**: `blink,<on>,<off>` or `hue_rainbow,<speed>`

**Parameter description**:

`<on>` = `0..65535`, set the duration of LED on in blinking mode, unit: milliseconds

`<off>` = `0..65535`, set the duration of LED off in blinking mode, unit: milliseconds

`<speed>` = `slow` | `normal` | `quick`, set cyclic speed in rainbow mode

**Payload Example**: `blink,200,500`, `hue_rainbow,normal`

> Note that changes to LED hue, saturation, and brightness will not take effect in rainbow mode, but the app will still record the latest settings. Changes will be immediately effective once switched to the blink mode.

#### Status Message

This demo will send the latest LED status in a retained message when the connection is established and when the LED status changes. There are three types of status messages. The topics they use are `stat/led/power`, `stat/led/hsb` and `stat/led/mode`. The message format is the same as the corresponding `cmnd/led/<command>` command.

## Run Demo

Adjust the configuration in VS Code according to your system environment, such as Wi-Fi SSID, Wi-Fi password, etc.

To provide the best security, EMQX Cloud Serverless forces TLS authentication and username and password authentication to be enabled. You need to configure the CA certificate, username, and password when connecting to EMQX Cloud Serverless.

This demo provides two ways to set the CA certificate, one of which has been mentioned before: embed the file into the firmware through the `target_add_binary_data` function in the `CMakeLists.txt` file. If you use this method, you need to change the file name in the `target_add_binary_data` function to your actual CA certificate file name, and the certificate must be in PEM format.

The other method is more straightforward and can be done directly in the configuration menu. Find the `MQTT Broker certificate override` configuration item in the `Demo Configuration` submenu, and copy and paste the Base64 part of the CA certificate into it. Be careful not to include any newlines and spaces:

![03certificateoverride.png](https://assets.emqx.com/images/4961441157ef7b36a4b1513799916bf2.png)

Next is the username and password required for authentication. In EMQX Cloud Serverless, you can quickly register a new device, enter the `Authentication` page through the left menu of the console, and click `Add` or `Import` to complete the addition of authentication information quickly:

![04authentication.png](https://assets.emqx.com/images/c740bc3540f7a8bf0f16ca4b7934d87b.png)

Upon completion, return to the ESP-IDF configuration menu and modify the `MQTT Username` and `MQTT Password` to the content you just added.

After the configuration, build the project and flash it into the ESP32. If everything goes well with the ESP32, you will see the following output on the serial console:

![05consoleoutput.png](https://assets.emqx.com/images/2c2a71a87ec99e7c81b01e8691a3dde7.png)

Now, you can open MQTTX, let it also connect to your EMQX Cloud Serverless deployment, and then send commands to the ESP32 to change its LED running state:

![mqttx](https://assets.emqx.com/images/63302d69f745cffc91d4ffcb2bc165b6.png)

## Summary

EMQX provides powerful message communication capabilities for real-time applications on FreeRTOS. This demo only shows the application of QoS 1 messages and retained messages. QoS 1 ensures that messages will not be lost, and retained messages ensure we can obtain the message at any time. EMQX has numerous other features, such as shared subscriptions, user properties, request-response, etc. All of these can greatly assist in our application development.

Most real-time applications have high communication security requirements. EMQX supports TLS and authentication allowing us to provide comprehensive protection for data security from the transport layer to the application layer.

The EMQX Cloud Serverless is a good choice for small to medium applications. The fast deployment, monthly free quota, and automatic scaling can greatly reduce the operation and maintenance effort you need to invest in the MQTT services. Thus you only need to focus on developing your application.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
