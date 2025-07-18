## Introduction

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) (Message Queuing Telemetry Transport) is a lightweight, publish-subscribe messaging protocol ideal for IoT applications due to its efficiency and low bandwidth requirements. For developers working with C++, MQTT offers a robust way to enable real-time communication in resource-constrained environments. This guide provides an in-depth exploration of implementing MQTT in C++ projects, focusing on practical steps and best practices, with EMQX as the recommended [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) for seamless integration.

## Why Use MQTT in C++?

Using C++ for an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) offers several benefits, particularly for applications requiring high performance, reliability, and resource efficiency, enabling fine-grained control over hardware resources. 

Key benefits of using MQTT with C++ include:

### **Performance and Efficiency**

C++ is well-suited for both lightweight MQTT clients (e.g., on edge devices) and high-throughput clients (e.g., in cloud-based brokers). Its ability to handle large numbers of connections and messages makes it ideal for scalable IoT systems.

- **High performance**: C++ is a compiled language that produces highly optimized machine code, resulting in faster execution compared to interpreted languages like Python. This is critical for MQTT clients in real-time applications (e.g., IoT devices, industrial automation) where low latency is essential for message publishing and subscribing.
- **Low Resource Usage**: C++ allows fine-grained control over memory management, enabling MQTT clients to operate efficiently on resource-constrained devices like microcontrollers or embedded systems commonly used in IoT.
- **Zero-Cost Abstractions**: C++ provides abstractions (e.g., classes, templates) without significant runtime overhead, allowing developers to write clean, maintainable code while maintaining performance for MQTT message handling. 

### **Cross-Platform Portability**

C++ is supported across a wide range of platforms, from embedded systems (e.g., ESP32, Arduino) to desktops and servers. This makes it ideal for developing MQTT clients that need to run on diverse hardware, ensuring consistent behavior in IoT ecosystems.

- **Robust Standard Library and Ecosystem:** C++ is a long-standing popular programming language; users can find rich help through the internet and the open-source community. C++ has been battle-tested in critical systems (e.g., automotive, aerospace), making it a reliable choice for MQTT clients in mission-critical applications like smart grids or medical devices.
- **Standard Library**: C++’s Standard Template Library (STL) provides robust tools for data structures (e.g., vectors, maps) and algorithms, which are useful for managing [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics), payloads, and message queues efficiently.
- **Third-Party Libraries**: Libraries like Eclipse Paho MQTT C++ or Mosquitto’s C++ wrappers provide reliable, well-tested implementations for MQTT protocol handling, supporting features like QoS levels, TLS/SSL for secure communication, and asynchronous operations.
- **Type Safety and Error Handling**: C++’s strong typing and compile-time checks reduce runtime errors, ensuring robust MQTT clients that handle edge cases like network failures or malformed messages.

While C++ offers significant advantages, developers should be aware of:

- **Complexity**: C++ has a steeper learning curve than higher-level languages, requiring careful handling of memory and concurrency to avoid issues like memory leaks or race conditions.
- **Development Time**: Writing an MQTT client in C++ may take longer compared to using languages like Python with simpler APIs, though performance gains in production offset this.

C++ is an excellent choice for developing MQTT clients, particularly in scenarios demanding high performance, low resource usage, and fine-grained control. Its cross-platform support, robust libraries, and ability to handle asynchronous and multithreaded operations make it ideal for IoT, industrial, and real-time applications. Libraries like Paho MQTT C++ simplify implementation while leveraging C++’s strengths, ensuring reliable and efficient MQTT communication.

## C++ MQTT Client Library Implementation Comparison

|                           | **Eclipse Paho MQTT C++**                                    | **Mosquitto (libmosquittopp)**                               | **Async.MQTT5**                                              | **NanoSDK C++Wrapper**                                       |
| :------------------------ | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| Overview                  | A widely-used C++ client library built on top of the Eclipse Paho C library | A C++ wrapper around the Mosquitto C library (libmosquitto), provided by the Eclipse Mosquitto project, which is best known for its lightweight MQTT broker. The C++ interface is minimal and primarily serves as a thin layer over the C library. | A modern, header-only C++20 library focused on MQTT 5.0, built on Boost.Asio for asynchronous operations. Designed for robust IoT applications with minimal developer overhead for handling connectivity issues. | A high-performance, non-blocking MQTT client SDK developed in C with a C++ interface, based on the NNG (nanomsg-next-generation) framework. Having an built-in Actor-model benenfits to overall performance. |
| MQTT Protocol Support     | Supports MQTT v3.1, v3.1.1, and v5.0 (as of version 1.5)<br>Full support for QoS 0, 1, and 2. Synchronized Acknowledgement. | Supports MQTT v3.1, v3.1.1, and v5.0.<br>Supports QoS 0, 1, and 2. Synchronized Acknowledgement. | Full support for MQTT v5.0 only (no v3.1/v3.1.1).<br>Supports QoS 0, 1, and 2. | Supports MQTT 3.1.1, 5.0, and MQTT over QUIC (based on MsQuic).<br>Supports QoS 0, 1, and 2, with asynchronous acknowledgment for QoS 1/2 to improve throughput.<br>Enabling sophisticated Multi-Stream & prioritization features for overcoming poor networking condition. |
| Security                  | Supports TLS/SSL via OpenSSL, with options for secure connections and certificate-based authentication. | Supports TLS/SSL via OpenSSL, with authentication mechanisms like username/password and certificates. | Supports TLS/SSL via Boost.Asio, with extended authentication (e.g., challenge/response-style). | Switchable TLS/SSL library (MbedTLS and OpenSSL).<br>The only SDK that supports SCRAM. <br>Also supports QUIC with TLS 1.3 for enhanced security and low-latency connections. |
| Threading Model           | Thread-safe, with an asynchronous, futures-style API using `std::future` for non-blocking operations. Supports publishing and subscribing from multiple threads with a single client connection. | The C library is single-threaded by default, requiring manual management of the event loop (`mosquitto_loop`). The C++ wrapper adds some convenience but is not inherently asynchronous or multi-threaded. | Fully asynchronous, leveraging Boost.Asio’s event-driven model and C++20 coroutines for procedural-style coding. No manual thread management needed. | Fully asynchronous I/O with a built-in Actor-like multi-threading model, leveraging NNG’s framework to distribute computation across multiple CPU cores. |
| Performance               | High performance due to its C-based core, but the C++ wrapper adds slight overhead. Suitable for both embedded and server-grade systems. | Lightweight and efficient, with a small memory footprint (~200k for the Mosquitto broker, similar for the client). Optimized for resource-constrained devices.<br>Limited asynchronous support; developers must manage the event loop manually, which can complicate multithreaded applications. | Optimized for efficiency with minimal memory footprint, suitable for IoT devices. High availability via automatic reconnect and multi-broker support.<br>Requires Boost, which may be a significant dependency for lightweight projects. | High throughput and low latency, significantly outperforming Paho C in QoS 1/2 scenarios (e.g., 50,000 messages test with 2-byte/14-byte payloads). Optimized for multi-core systems, with zero-copy mechanisms to reduce memory usage.<br>Provides a lower latency messaging experience compare to other SDKs. |
| Dependencies              | Requires the Paho C library (v1.3.14 or later). Optional dependency on OpenSSL for TLS. | Requires libmosquitto (C library) and optionally OpenSSL for TLS | Requires Boost (notably Boost.Asio), but header-only design reduces build complexity. No other third-party dependencies. | Requires NNG library and optionally MsQuic for QUIC support. Minimal reliance on POSIX-standard APIs for high portability. |
| Build System              | Uses CMake for cross-platform builds, with options to build alongside the Paho C library for compatibility. | Uses CMake or makefiles, with straightforward integration for embedded systems. | Header-only, simplifying integration. Requires a C++20-compliant compiler and Boost libraries. | CMake-based, with support for building on POSIX-compliant platforms (Linux, macOS, etc.) and various CPU architectures (x86_64, ARM, MIPS, RISC-V). |
| Community and Maintenance | Actively maintained by the Eclipse Foundation, with recent updates (e.g., v1.5.3 in 2025, supporting C++17 and UNIX-domain sockets). Strong community support with 1.3k GitHub stars (as of May 2024). | Actively maintained by the Eclipse Foundation and Cedalo, with 8k GitHub stars for the Mosquitto project (as of May 2024). However, the C++ wrapper is less actively developed compared to the C library or broker.<br>C++ wrapper is minimal and outdated, with deprecated functions, making it less appealing for modern C++ development. | Developed by Mireo, with plans for Boost integration. Actively maintained (as of 2023), but smaller community compared to Paho or Mosquitto.<br>Simplified interface hiding complex MQTT protocol details (e.g., reconnect logic, message retransmission). Uses C++20 features like coroutines for readable code. | Not mature enough, but actively under development by EMQ and the NNG community.<br>Smaller community than Paho or Mosquitto but growing. Offers both NNG-style APIs (higher learning curve) and a traditional callback-based interface compatible with Paho styles, reducing complexity for developers familiar with those SDKs. |

## Choosing the Right MQTT Broker for C++

To implement MQTT in C++, you need a reliable MQTT broker to manage message routing. EMQX is a leading [open-source MQTT broker](https://www.emqx.com/en/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023), trusted for its scalability and performance. It supports [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5), 3.1.1, and 3.1, handles millions of concurrent connections, and offers features like a SQL-based rule engine and integration with databases like PostgreSQL and Kafka. EMQX’s high availability and low-latency capabilities make it an excellent choice for C++-based IoT applications.

For simplicity, this guide uses a [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) based on EMQX Platform:

- Server: `broker.emqx.io`
- TCP Port: `1883`
- WebSocket Port: `8083`
- SSL/TLS Port: `8883`
- Secure WebSocket Port: `8084`

## Getting Started with MQTT in C++

Let’s walk through a practical example of using MQTT in a C++ application with the Eclipse Paho MQTT C++ library, a popular choice for its reliability and compatibility with EMQX.

### Prerequisites

- Install the Paho MQTT C++ library (requires the Paho C library as a dependency).

- Set up EMQX. You can deploy EMQX locally using Docker:

  ```shell
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8883:8883 -p 18083:18083 emqx/emqx:latest
  ```

- A C++ development environment (e.g., GCC, CMake).

### Step 1: Setting Up the Paho MQTT C++ Library

Install the Paho MQTT C and C++ libraries. On Ubuntu, you can use:

```shell
sudo apt-get install libpaho-mqtt-dev
```

Clone and build the Paho MQTT C++ library:

```shell
git clone <https://github.com/eclipse/paho.mqtt.cpp> cd paho.mqtt.cpp cmake -Bbuild -H. -DPAHO_WITH_SSL=ON cmake --build build --target install
```

### Step 2: Writing a Simple MQTT Publisher

Below is a C++ example to publish messages to an EMQX broker using the Paho MQTT C++ library.

```cpp
#include <mqtt/async_client.h>
#include <string>
#include <iostream>

const std::string SERVER_ADDRESS("tcp://localhost:1883");
const std::string CLIENT_ID("cpp_publisher");
const std::string TOPIC("test/topic");

int main() {
    mqtt::async_client client(SERVER_ADDRESS, CLIENT_ID);

    mqtt::connect_options connOpts;
    connOpts.set_keep_alive_interval(20);
    connOpts.set_clean_session(true);

    try {
        // Connect to EMQX broker
        client.connect(connOpts)->wait();
        std::cout << "Connected to EMQX broker" << std::endl;

        // Publish a message
        std::string payload = "Hello, EMQX from C++!";
        mqtt::message_ptr pubmsg = mqtt::make_message(TOPIC, payload, 1, false);
        client.publish(pubmsg)->wait();
        std::cout << "Message published: " << payload << std::endl;

        // Disconnect
        client.disconnect()->wait();
        std::cout << "Disconnected" << std::endl;
    } catch (const mqtt::exception& exc) {
        std::cerr << "Error: " << exc.what() << std::endl;
        return 1;
    }

    return 0;
}
```

### Step 3: Writing an MQTT Subscriber

Here's an example of a C++ subscriber that listens for messages on the same topic.

```cpp
#include <mqtt/async_client.h>
#include <string>
#include <iostream>

const std::string SERVER_ADDRESS("tcp://localhost:1883");
const std::string CLIENT_ID("cpp_subscriber");
const std::string TOPIC("test/topic");

class callback : public virtual mqtt::callback {
    void message_arrived(mqtt::const_message_ptr msg) override {
        std::cout << "Message received: " << msg->get_payload_str() << std::endl;
    }
};

int main() {
    mqtt::async_client client(SERVER_ADDRESS, CLIENT_ID);
    callback cb;
    client.set_callback(cb);

    mqtt::connect_options connOpts;
    connOpts.set_keep_alive_interval(20);
    connOpts.set_clean_session(true);

    try {
        // Connect to EMQX broker
        client.connect(connOpts)->wait();
        std::cout << "Connected to EMQX broker" << std::endl;

        // Subscribe to topic
        client.subscribe(TOPIC, 1)->wait();
        std::cout << "Subscribed to topic: " << TOPIC << std::endl;

        // Keep running to receive messages
        std::cout << "Press Enter to exit..." << std::endl;
        std::cin.get();

        // Disconnect
        client.disconnect()->wait();
        std::cout << "Disconnected" << std::endl;
    } catch (const mqtt::exception& exc) {
        std::cerr << "Error: " << exc.what() << std::endl;
        return 1;
    }

    return 0;
}
```

### Step 4: Compiling and Running

Compile the code with the Paho MQTT C++ library:

```shell
g++ publisher.cpp -o publisher -lpaho-mqttpp3 -lpaho-mqtt3a
g++ subscriber.cpp -o subscriber -lpaho-mqttpp3 -lpaho-mqtt3a
```

Run the subscriber first, then the publisher:

```shell
./subscriber
./publisher
You can add "LD_PRELOAD=/usr/local/lib/libpaho-mqttpp3.so.1" before to avoid shared object not found issue.
For example, if you install "paho.mqtt.cpp" to default folder "/usr/local/lib"
LD_PRELOAD=/usr/local/lib/libpaho-mqttpp3.so.1 ./publisher
```

The subscriber will receive the message "Hello, EMQX from C++!" from the EMQX broker.

```shell
./subscriber prints:
Connected to EMQX broker
Subscribed to topic: test/topic
Press Enter to exit...
Message received: Hello, EMQX from C++!
```

## Conclusion

Using MQTT with C++ empowers developers to build efficient, scalable IoT applications. The Paho MQTT C++ library, combined with EMQX’s powerful broker capabilities, provides a solid foundation for real-time messaging. Whether you’re developing for smart homes, industrial IoT, or connected vehicles, this combination ensures reliability and performance. 

For more resources, check out the [EMQX documentation](https://www.emqx.com/en/docs) and [Paho MQTT C++ GitHub repository](https://github.com/eclipse/paho.mqtt.cpp).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
