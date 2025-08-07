## 引言

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)（消息队列遥测传输）是一种轻量级的发布 - 订阅消息传递协议，由于其高效性和低带宽要求，非常适合物联网应用。对于使用 C++ 的开发者来说，MQTT 提供了一种在资源受限的环境中实现实时通信的强大方法。

本指南深入探讨了如何在 C++ 项目中实现 MQTT，重点介绍了实际操作步骤和最佳实践，并推荐使用 EMQX 作为 [MQTT broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 以实现无缝集成。

## 为什么在 C++ 中使用 MQTT？

对于需要高性能、高可靠性和高资源效率的应用程序来说，使用 C++ 开发 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)具有多种优势，可以实现对硬件资源的细粒度控制。

在 C++ 中使用 MQTT 的主要优势包括：

### 性能与效率

C++ 非常适合轻量级 MQTT 客户端（例如：边缘设备）和高吞吐量客户端（例如：基于云的代理）。它能够处理大量连接和消息，使其成为可扩展物联网系统的理想选择。

- **高性能**：C++ 是一种编译型语言，可生成高度优化的机器代码，与 Python 等解释型语言相比，执行速度更快。这对于实时应用（例如：物联网设备、工业自动化）中的 MQTT 客户端至关重要，确保了低延迟的消息发布和订阅。
- **低资源使用率**：C++ 允许对内存管理进行细粒度控制，使 MQTT 客户端能够在资源受限的设备（如物联网中常用的微控制器或嵌入式系统）上高效运行。
- **零成本抽象机制**：C++ 提供的抽象机制（例如：类、模板），避免了运行时的额外开销，允许开发人员编写干净、可维护的代码，同时保持 MQTT 消息处理的性能。

### **跨平台可移植性**

C++ 支持多种平台，从嵌入式系统（例如：ESP32、Arduino）到台式机和服务器。这使得它非常适合开发需要在不同硬件上运行的 MQTT 客户端，从而确保物联网生态系统中的行为一致性。

- **强大的标准库和生态系统：** C++ 是一种长期流行的编程语言；用户可以通过互联网和开源社区获得丰富的帮助。C++ 已在关键系统（例如：汽车、航空航天）中经过实践检验，使其成为智能电网或医疗设备等关键任务应用中 MQTT 客户端的可靠选择。
- **标准库**：C++ 的标准模板库 (STL) 为数据结构（例如：向量、映射）和算法提供了强大的工具，可用于有效地管理 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)、有效负载和消息队列。
- **第三方库**：Eclipse Paho MQTT C++ 或 Mosquitto 的 C++ 包装器等库为 MQTT 协议处理提供了可靠、经过充分测试的实现，支持 QoS 级别、用于安全通信的 TLS/SSL 和异步操作等功能。
- **类型安全和错误处理**：C++ 的强类型和编译时检查功能，减少了运行时的错误，确保 MQTT 客户端能够处理网络故障或格式错误的消息等边缘情况。

**虽然 C++ 具有显著的优势，但开发人员应该注意：**

- **复杂性**：C++ 的学习曲线比高级语言更陡峭，需要谨慎处理内存和并发性，以避免内存泄漏或竞争条件等问题。
- **开发时间**：使用 C++ 编写 MQTT 客户端可能要比使用 Python 等 API 更简单的语言花费更多时间，但会显著提升生产性能。

C++ 是开发 MQTT 客户端的绝佳选择，尤其适用于对高性能、低资源占用和精细化控制有严格要求的场景。其跨平台支持、强大的库以及处理异步和多线程操作的能力，使其成为物联网、工业和实时应用的理想解决方案。通过 Paho MQTT C++ 等库的支持，开发者能够充分发挥 C++ 的优势，在简化实现过程的同时确保 MQTT 通信的可靠性与高效性。

## C++ MQTT 客户端库实现比较

|               | **Eclipse Paho MQTT C++**                                    | **Mosquitto (libmosquittopp)**                               | **Async.MQTT5**                                              | **NanoSDK C++Wrapper**                                       |
| :------------ | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| 概述          | 基于 Eclipse Paho C 库构建的广泛使用的 C++ 客户端库          | Mosquitto C 库（libmosquitto）的 C++ 封装程序，由 Eclipse Mosquitto 项目提供。该项目以其轻量级 MQTT 代理而闻名。C++ 界面非常精简，主要作为 C 库的一个薄层。 | 一个现代的、仅包含头文件的 C++20 库，专注于 MQTT 5.0，基于 Boost.Asio 构建，用于异步操作。专为强大的物联网应用而设计，最大限度地减少开发人员处理连接问题的开销。 | 基于 NNG（nanomsg-next-generation）框架，使用 C 语言开发，提供 C++ 接口的高性能、无阻塞 MQTT 客户端 SDK。内置 Actor 模型，提升整体性能。 |
| MQTT 协议支持 | 支持 MQTT v3.1、v3.1.1 和 v5.0（截至 1.5 版） 完全支持 QoS 0、1 和 2。同步确认。 | 支持 MQTT v3.1、v3.1.1 和 v5.0。 支持 QoS 0、1 和 2。同步确认。 | 仅完全支持 MQTT v5.0（不支持 v3.1/v3.1.1）。 支持 QoS 0、1 和 2。 | 支持 MQTT 3.1.1、5.0 以及基于 MsQuic 的 MQTT over QUIC。 支持 QoS 0、1 和 2，并对 QoS 1/2 提供异步确认以提高吞吐量。 支持复杂的多流和优先级功能，能够应对网络状况不佳的问题。 |
| 安全          | 通过 OpenSSL 支持 TLS/SSL，并提供安全连接和基于证书的身份验证选项。 | 通过 OpenSSL 支持 TLS/SSL，具有用户名/密码和证书等身份验证机制。 | 通过 Boost.Asio 支持 TLS/SSL，并具有扩展身份验证（例如，质询/响应样式）。 | 可切换的 TLS/SSL 库（MbedTLS 和 OpenSSL）。 唯一支持 SCRAM 的 SDK。 还支持 QUIC 和 TLS 1.3，以增强安全性并实现低延迟连接。 |
| 线程模型      | 线程安全，使用异步、Futures 风格的 API 进行`std::future`非阻塞操作。支持通过单个客户端连接从多个线程进行发布和订阅。 | C 库默认是单线程的，需要手动管理事件循环（`mosquitto_loop`）。C++ 包装器虽然增加了一些便利性，但本质上并非异步或多线程。 | 完全异步，利用 Boost.Asio 的事件驱动模型和 C++20 协程进行过程式编码。无需手动线程管理。 | 完全异步 I/O，具有内置类似 Actor 的多线程模型，利用 NNG 的框架在多个 CPU 核心之间分配计算。 |
| 表现          | 由于其基于 C 语言的内核，性能卓越，但 C++ 封装程序略微增加了开销。适用于嵌入式和服务器级系统。 | 轻量高效，内存占用小（Mosquitto 代理约 20 万，客户端类似）。针对资源受限的设备进行了优化。 异步支持有限；开发者必须手动管理事件循环，这会使多线程应用程序变得复杂。 | 针对效率进行了优化，内存占用极小，适用于物联网设备。通过自动重连和多代理支持实现高可用性。 需要 Boost，这对于轻量级项目来说可能是一个重要的依赖项。 | 高吞吐量、低延迟，在 QoS 1/2 场景下（例如，以 2 字节/14 字节有效载荷测试 50,000 条消息）显著优于 Paho C。针对多核系统进行了优化，并采用零拷贝机制以减少内存占用。 与其他 SDK 相比，提供更低延迟的消息传递体验。 |
| 依赖项        | 需要 Paho C 库（v1.3.14 或更高版本）。TLS 可选依赖 OpenSSL。 | 需要 libmosquitto（C 库）和可选的 OpenSSL 用于 TLS           | 需要 Boost（尤其是 Boost.Asio），但仅使用头文件的设计降低了构建复杂性。无需其他第三方依赖。 | 需要 NNG 库以及可选的 MsQuic 来支持 QUIC。为了实现高可移植性，尽量减少对 POSIX 标准 API 的依赖。 |
| 构建系统      | 使用 CMake 进行跨平台构建，并可选择与 Paho C 库一起构建以实现兼容性。 | 使用 CMake 或 makefile，可直接与嵌入式系统集成。             | 仅包含头文件，简化集成。需要兼容 C++20 的编译器和 Boost 库。 | 基于 CMake，支持在符合 POSIX 标准的平台（Linux、macOS 等）和各种 CPU 架构（x86_64、ARM、MIPS、RISC-V）上构建。 |
| 社区与维护    | 由 Eclipse 基金会积极维护，并不断更新（例如，2025 年将发布 v1.5.3，支持 C++17 和 UNIX 域套接字）。强大的社区支持，GitHub 上已有 1.3k 个 Star（截至 2024 年 5 月）。 | 由 Eclipse 基金会和 Cedalo 积极维护，Mosquitto 项目在 GitHub 上拥有 8k 个 Star（截至 2024 年 5 月）。然而，与 C 库或代理相比，C++ 封装程序的开发活跃度较低。C ++ 封装包规模极小且过时，包含一些已弃用的函数，对现代 C++ 开发来说吸引力较小。 | 由 Mireo 开发，计划集成 Boost。维护活跃（截至 2023 年），但社区规模小于 Paho 或 Mosquitto。 简化的接口隐藏了复杂的 MQTT 协议细节（例如，重新连接逻辑、消息重传）。使用 C++20 特性（例如协程）以提高代码可读性。 | 尚不够成熟，但 EMQ 和 NNG 社区正在积极开发中。 社区规模小于 Paho 或 Mosquitto，但正在不断发展。它既提供 NNG 风格的 API（学习曲线较高），也提供兼容 Paho 风格的传统回调接口，从而降低了熟悉这些 SDK 的开发者的开发复杂度。 |

## 为 C++ 选择合适的 **MQTT 消息代理服务器**

要使用 C++ 实现 MQTT，您需要一个可靠的 MQTT 代理服务器来管理消息路由。EMQX 是一款领先的[开源 MQTT Broker](https://www.emqx.com/zh/blog/a-comprehensive-comparison-of-open-source-mqtt-brokers-in-2023)，以其卓越的可扩展性和性能而备受信赖。它支持 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5)、3.11 和 3.1 版本，可处理数百万个并发连接，并提供基于 SQL 的规则引擎以及与 PostgreSQL 和 Kafka 等数据库集成等功能。EMQX 的高可用性和低延迟能力使其成为基于 C++ 的物联网应用的绝佳选择。

出于简单起见，本指南使用基于 EMQX 平台的[免费公共 MQTT Broker](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)：

- 服务器：`broker.emqx.io`
- TCP 端口：`1883`
- WebSocket 端口：`8083`
- SSL/TLS 端口：`8883`
- 安全 WebSocket 端口：`8084`

## 在 C++ 中开始使用 MQTT

让我们通过 Eclipse Paho MQTT C++ 库来了解在 C++ 应用程序中使用 MQTT 的实际示例，该库因其可靠性和与 EMQX 的兼容性而广受欢迎。

### 前提条件

- 安装 Paho MQTT C++ 库（需要 Paho C 库作为依赖项）。
- 设置 EMQX。您可以使用 Docker 在本地部署 EMQX：

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8883:8883 -p 18083:18083 emqx/emqx:latest
```

- C++ 开发环境（例如 GCC、CMake）。

### 步骤 1：设置 Paho MQTT C++ 库

安装 Paho MQTT C 和 C++ 库。在 Ubuntu 上，您可以使用：

```
sudo apt-get install libpaho-mqtt-dev
```

克隆并构建 Paho MQTT C++ 库：

```
git clone <https://github.com/eclipse/paho.mqtt.cpp> cd paho.mqtt.cpp cmake -Bbuild -H. -DPAHO_WITH_SSL=ON cmake --build build --target install
```

### 步骤 2：编写简单的 MQTT 发布器

下面是使用 Paho MQTT C++ 库向 EMQX broker 发布消息的 C++ 示例：

```c++
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

### 步骤 3：编写 MQTT 订阅器

下面是一个 C++ 订阅器的示例，它可以监听同一主题的消息。

```c++
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

### 步骤4：编译并运行

使用 Paho MQTT C++ 库编译代码：

```
g++ publisher.cpp -o publisher -lpaho-mqttpp3 -lpaho-mqtt3a
g++ subscriber.cpp -o subscriber -lpaho-mqttpp3 -lpaho-mqtt3a
```

首先运行订阅者，然后运行发布者：

```
./subscriber
./publisher
You can add "LD_PRELOAD=/usr/local/lib/libpaho-mqttpp3.so.1" before to avoid shared object not found issue.
For example, if you install "paho.mqtt.cpp" to default folder "/usr/local/lib"
LD_PRELOAD=/usr/local/lib/libpaho-mqttpp3.so.1 ./publisher
```

订阅者将收到来自 EMQX broker 的消息「Hello, EMQX from C++!」。

```
./subscriber prints:
Connected to EMQX broker
Subscribed to topic: test/topic
Press Enter to exit...
Message received: Hello, EMQX from C++!
```

## 总结

MQTT 与 C++ 结合使用，能够助力开发者构建高效、可扩展的物联网应用。Paho MQTT C++ 库与 EMQX 强大的代理功能相结合，为实时消息传递奠定了坚实的基础。无论您是开发智能家居、工业物联网还是车联网，这一组合都能确保可靠性和性能。

如需更多资源，请查看[EMQX 文档](https://docs.emqx.com/zh/emqx/latest/)和 [Paho MQTT C++ GitHub 存储库](https://github.com/eclipse-paho/paho.mqtt.cpp)。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
