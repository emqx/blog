## Introduction: Why C for MQTT and Why Paho?

When building robust, high-performance Internet of Things (IoT) solutions, the choice of programming language often comes down to resource efficiency and execution speed. This is where **C language** and the **MQTT C** client shine.

C provides unparalleled control over system resources, making it the ideal choice for:

- **Embedded Systems:** Microcontrollers and resource-constrained devices where memory and CPU cycles are limited.
- **High Performance:** Applications requiring the lowest possible latency and direct hardware interaction.

The most widely adopted and authoritative library for C-based MQTT development is the **Eclipse Paho MQTT C Client** (`eclipse-paho/paho.mqtt.c`). Paho is the industry standard, providing stable, feature-rich implementations for various platforms.

This tutorial will guide you through setting up the Paho C Client and building a complete Pub/Sub application, connecting to a powerful [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison).

## Setting Up the Development Environment

### Prerequisite: The MQTT Broker

To successfully run any MQTT application, you need a highly available and reliable broker.

For this tutorial, we will use the free public **EMQX Broker**, known for its scalability, full [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) support, and performance under massive loads—the perfect backend for your high-performance C clients.

| **Parameter**      | **Value**                                      |
| ------------------ | ---------------------------------------------- |
| **Broker Address** | `broker.emqx.io`                               |
| **TCP Port**       | `1883`                                         |
| **Client ID**      | A unique string (e.g., `Paho_C_Tutorial_1234`) |

> **Pro Tip:** For production environments requiring security, high concurrency (up to 100 million connections), and enterprise features, consider using **EMQX Cloud** or **EMQX Enterprise**.

### Installing the Paho C Library

The Paho C Client is generally compiled from source. Here are the steps for a Unix-like system (Linux/macOS).

1. **Clone the Repository:**

   ```shell
   git clone https://github.com/eclipse-paho/paho.mqtt.c.git
   cd paho.mqtt.c
   ```

2. **Compile and Install:**

   ```shell
   # Build the library
   make
   # Install to system libraries
   sudo make install
   ```

This process installs the necessary header files (`MQTTClient.h`, etc.) and the library files for linking.

## Step-by-Step Guide: Building Your First MQTT C Client

We will use the synchronous Paho API (`MQTTClient.h`) for simplicity. Create a file named `paho_c_example.c`.

### Full Example Code

Here is the complete code. We will break down each function call below.

```c
#include "MQTTClient.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// EMQX Connection Details
#define ADDRESS     "tcp://broker.emqx.io:1883"
#define CLIENTID    "Paho_C_Tutorial_Client"
#define TOPIC       "paho/c/tutorial/test"
#define PAYLOAD     "Hello from the Paho C Client!"
#define QOS         1
#define TIMEOUT     10000L // 10 seconds

// The callback function executed when a message is received
int messageArrived(void *context, char *topicName, int topicLen, MQTTClient_message *message) {
    printf("Message received on topic: %s\n", topicName);
    printf("Payload: %.*s\n", message->payloadlen, (char*)message->payload);
    MQTTClient_freeMessage(&message);
    MQTTClient_free(topicName);
    return 1;
}

int main(int argc, char* argv[]) {
    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    int rc;

    // --- Step 1: Create the Client ---
    MQTTClient_create(&client, ADDRESS, CLIENTID,
        MQTTCLIENT_PERSISTENCE_NONE, NULL);
    
    // Set the message callback function
    MQTTClient_setCallbacks(client, NULL, NULL, messageArrived, NULL);

    // --- Step 2: Configure Connection Options ---
    conn_opts.keepAliveInterval = 20; // Send PINGREQ every 20 seconds
    conn_opts.cleansession = 1;       // Start a new session every time

    // --- Step 3: Connect to the Broker ---
    printf("Attempting to connect to EMQX Broker...\n");
    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS) {
        printf("Failed to connect to EMQX, return code %d\n", rc);
        return rc;
    }
    printf("Successfully connected to EMQX!\n");

    // --- Step 4: Subscribe to the Topic ---
    printf("Subscribing to topic \"%s\" with QoS %d\n", TOPIC, QOS);
    MQTTClient_subscribe(client, TOPIC, QOS);
    
    // --- Step 5: Publish a Message ---
    MQTTClient_message pubmsg = MQTTClient_message_initializer;
    pubmsg.payload = PAYLOAD;
    pubmsg.payloadlen = (int)strlen(PAYLOAD);
    pubmsg.qos = QOS;
    pubmsg.retained = 0;
    
    MQTTClient_deliveryToken token;
    printf("Publishing message: \"%s\"\n", PAYLOAD);
    
    // Publish and wait for delivery confirmation (Synchronous)
    MQTTClient_publishMessage(client, TOPIC, &pubmsg, &token);
    rc = MQTTClient_waitForCompletion(client, token, TIMEOUT);
    printf("Message with token value %d delivered.\n", token);

    // Keep the main thread alive to receive messages (Subscriber loop)
    printf("Client is listening for messages. Press Enter to disconnect...\n");
    getchar();

    // --- Step 6: Disconnect and Cleanup ---
    MQTTClient_disconnect(client, 10000);
    MQTTClient_destroy(&client);
    return rc;
}
```

### Breakdown and Explanation

| **Step**          | **Function Call**                           | **Description**                                              | **EMQX Integration**                                         |
| ----------------- | ------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| **1 (Create)**    | `MQTTClient_create()`                       | Allocates memory for the client and initializes the communication channel (TCP, WebSocket). | The `ADDRESS` specifies the EMQX Broker endpoint.            |
| **2 (Options)**   | `conn_opts.keepAliveInterval`               | Sets the maximum time interval (in seconds) between messages sent/received. Essential for stability. | EMQX uses this to monitor the connection health and close idle connections. |
| **3 (Connect)**   | `MQTTClient_connect()`                      | Attempts to establish a connection.                          | We check the return code (`MQTTCLIENT_SUCCESS`) to confirm the connection to EMQX. |
| **4 (Subscribe)** | `MQTTClient_subscribe()` & `messageArrived` | Registers interest in a topic and defines the callback function to handle incoming data. | We use **QoS 1** (At Least Once) to ensure the EMQX Broker guarantees delivery. |
| **5 (Publish)**   | `MQTTClient_publishMessage()`               | Sends the data. We use the blocking `MQTTClient_waitForCompletion()` to ensure the message is successfully confirmed by the Broker. | The Broker handles the message routing to all subscribers, confirming receipt back to the C client. |
| **6 (Cleanup)**   | `MQTTClient_disconnect()`                   | Terminates the MQTT connection cleanly.                      | Clean disconnection helps the EMQX Broker manage resources efficiently. |

### Compiling and Running the Code

1. **Compile:** Link the program with the Paho library (`-lpaho-mqtt3c` for the synchronous client).

   ```shell
   gcc paho_c_example.c -o mqtt_c_client -lpaho-mqtt3c
   ```

2. **Run:**

   ```shell
   ./mqtt_c_client
   ```

You will see the client connect, publish, and then listen for any messages published to the same topic.

## Advanced MQTT C & EMQX Integration

The real power of the **MQTT C** client is realized when paired with a high-performance broker like EMQX.

### The Security Imperative: Implementing TLS/SSL

In production, unencrypted connections are unacceptable. Paho provides secure versions of its libraries (`paho-mqtt3cs` and `paho-mqtt3as`).

- **Paho C Implementation:** Use the `MQTTClient_SSLOptions` structure and update the connection address (e.g., `ssl://broker.emqx.io:8883`).
- **EMQX Value:** EMQX natively supports TLS/SSL on multiple ports and offers advanced security features like **Client Certificate Authentication** and integration with external security backends, providing the trust layer required for C clients deployed in the field.

### High Availability with EMQX Cluster

A single C client must maintain a stable connection, but network instability is inevitable in IoT environments.

- **The MQTT C Pain Point:** The client connects to one broker instance at a time.
- **EMQX Solution (Resilience):** The **EMQX Cluster** architecture ensures high availability. If the C client's connected node fails, its built-in reconnection logic will automatically attempt to connect to another available node in the EMQX cluster, ensuring minimal downtime and preserving session state if `cleansession=0` was used.

## FAQ

### **What is the difference between** `MQTTClient.h` **and** `MQTTAsync.h`**?**

- `MQTTClient.h` **(Synchronous/Classic):** Uses blocking calls (e.g., `MQTTClient_connect()` blocks until connected). It is simpler to use but less suitable for high-concurrency applications or single-threaded embedded systems where blocking is undesirable.
- `MQTTAsync.h` **(Asynchronous):** Uses non-blocking calls and relies on callbacks for event notification (connection established, message received, etc.). This is generally preferred for high-performance applications where the client needs to manage multiple tasks concurrently.

### **How do I handle large numbers of concurrent MQTT C clients in production?**

To scale your MQTT C application, you need a robust broker. **EMQX** is specifically designed for this purpose, supporting millions of concurrent connections through its distributed cluster architecture. Key practices include:

1. **Use unique Client IDs.**
2. **Enable TLS/SSL** for all C clients.
3. **Optimize Keep-Alive:** Set a reasonable `keepAliveInterval` (e.g., 60 seconds) to maintain connectivity without excessive overhead.
4. **Use QoS 1 or 2** only when message delivery guarantee is critical; otherwise, stick to QoS 0 for maximum throughput.

### **Why is my Paho C client suddenly disconnecting from the broker?**

Common reasons for unexpected disconnections include:

- **Keep-Alive Timeout:** If the client or broker fails to send a message or PINGREQ/PINGRESP within $1.5 \times$ the `keepAliveInterval`.
- **Network Instability:** Sudden loss of TCP connection (common in cellular or Wi-Fi environments).
- **Broker Overload:** While rare with EMQX, an overloaded broker may drop connections. **EMQX** provides detailed logs and monitoring metrics to identify resource bottlenecks quickly.
- **Authorization Failure:** The client ID, Username, or Password may have become invalid, causing the broker (like EMQX) to reject the connection immediately.

### **Can I use MQTT 5.0 features with the Paho C Client?**

Yes. The Paho C Client fully supports the MQTT 5.0 specification. To use it, you must configure the connection options with the appropriate MQTT version when creating the client (e.g., setting the version field in the appropriate initialization structure). Advanced EMQX features like **Session Expiry** and **User Properties** are fully accessible via the Paho C MQTT 5.0 API.

## Conclusion

You have successfully navigated the complexities of C-based networking to build a fully functional **MQTT C** client using the robust **Paho C Client** library. This foundation is crucial for developing efficient, reliable, and resource-friendly applications for embedded and edge computing.

Ready to scale your solution beyond a single test connection? **EMQX** is the world's most scalable MQTT Broker, designed to handle the millions of high-performance C clients your IoT project demands.


<section class="promotion">
    <div>
        Try EMQX for Free
    </div>
    <a href="https://www.emqx.com/en/try?tab=self-managed" class="button is-gradient">Get Started →</a>
</section>
