**我们很高兴与您分享，我们的项目已在 ESP32C3 微控制器上成功实现了完整的 MQTT over QUIC 解决方案。**通过将 coreMQTT 库与 QUIC 协议栈（wolfSSL+ngtcp2）集成，我们让这个资源受限的设备也能够执行完整的基于 QUIC 传输的 MQTT 操作，包括连接、发布和订阅。这项突破是物联网通信领域的重要一步，它证明了即便是小型、低功耗的设备也能利用现代、安全且高效的协议。

**欢迎您与我们一同探索这一突破性进展，并访问我们的 GitHub 仓库参与开发：**

[GitHub - emqx/ESP32-QUIC: PoC for ESP32 running QUIC client](https://github.com/emqx/ESP32-QUIC)

## 项目背景

### 什么是 QUIC？

QUIC（Quick UDP Internet Connections）是一种基于 UDP 的新一代传输层协议，旨在通过降低延迟和提高安全性来增强网络性能。相较于传统协议，QUIC 具备三大核心优势：更快的连接建立速度、支持多路复用且无队头阻塞（HOL blocking），以及原生集成的 TLS 1.3 加密。

这些特性使 QUIC 特别适用于物联网应用场景，以应对设备常面临的高延迟与不稳定的网络环境 [^1]。

了解更多关于 EMQ 在 QUIC 上的成就：

- [什么是 QUIC 协议？](https://www.emqx.com/zh/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov)
- [MQTT over QUIC：物联网消息传输还有更多可能](https://www.emqx.com/zh/blog/mqtt-over-quic)
- [使用 MQTT over QUIC 解决地址变化问题](https://www.emqx.com/zh/blog/overcoming-address-change-with-mqtt-over-quic)

### 什么是 MQTT？

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)（消息队列遥测传输）是一种轻量级的发布-订阅消息协议，专为资源受限设备和低带宽、高延迟网络而设计。这一特性使其在物联网通信中广泛应用，助力智能家居、工业自动化等行业实现高效通信 [^2]。

### 什么是 ESP32C3？

ESP32C3 由乐鑫信息科技开发的一款低成本、低功耗的物联网微控制器。它采用单核 32 位 RISC-V 处理器，主频高达 160 MHz，拥有 384 KB 闪存、400 KB SRAM（实际可用 320 KB），并集成了 Wi-Fi 和蓝牙 5 (LE)。ESP32C3 开源的 RISC-V 架构提供了极高的灵活性，使其成为物联网项目的热门选择 [^3]。

### 什么是 EMQX？

**[EMQX](https://www.emqx.com/zh/products/emqx) 是全球首个专为实时智能设计的 MQTT 与人工智能融合平台。**它兼容 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5)、3.1.1 和 3.1 以及 MQTT over QUIC 等多种消息传输协议，单节点支持超百万 MQTT 连接，集群支持上亿 MQTT 连接。依靠大规模并发消息传输能力，EMQX 已成为智慧城市、工业物联网、汽车制造等行业的理想之选 [^4]。

### **什么是 coreMQTT？**

coreMQTT 是 AWS IoT 设备 SDK 的一部分，是一个专为资源受限设备设计的轻量级 [MQTT 客户端库](https://www.emqx.com/zh/mqtt-client-sdk)。它支持高效的发布-订阅通信，非常适合在本项目中通过 QUIC 集成 MQTT 功能 [^5]。

## **项目实践：在 ESP32 上运行 MQTT over QUIC**

### **概述**

在本项目中，我们在 ESP32C3 上实现了完整的 MQTT over QUIC 解决方案。该设备连接到 WiFi 网络，与 EMQX 服务器建立 QUIC 连接，并使用 coreMQTT 库执行完整的 MQTT 操作——连接、发布消息和订阅主题。这证明了在受限设备上运行高级网络协议的可行性及其在高效物联网通信方面的潜力。

### 实施细节

该项目利用了三个开源库：

- **ngtcp2**：一个基于 C 语言开发的 QUIC 协议库，专门用于管理 QUIC 连接。ngtcp2_sample.c 文件改编自 ngtcp2 的示例代码，完整演示了客户端 QUIC 功能 [^6]。
- **wolfSSL**：一个轻量级的 TLS 库，为 QUIC 提供加密操作以保障安全性，支持 TLS 1.3 [^7]。
- **coreMQTT**：来自 AWS IoT Device SDK 的 MQTT 客户端库，能够通过 QUIC 传输处理 MQTT 协议操作。

这些库已集成到 ESP-IDF 框架中，其中 ngtcp2 被封装为组件并进行补丁以兼容 ESP32C3。。

该项目包含用于核心功能的 `quic_demo_main.c` 文件和用于兼容 ESP 事件循环的 `esp_ev_compat.c` 文件。二进制文件大小约为 1.6 MB（0x16d060 字节），可装入 1.68 MB（0x1a9000 字节）的自定义应用程序分区，剩余约 14% 的可用空间。

为了简化 PoC，我们应用了一些非标准调整，例如禁用 TLS 证书验证，但这些调整并不适用于生产环境。

### 资源使用情况

由于 ESP32C3 的内存和处理能力有限，我们重点关注了其资源使用情况：

- **闪存**：二进制文件大小约为 1.6 MB，可放入自定义分区中。ESP32C3 内置 384 KB 闪存，但 ESP-IDF 支持外部闪存，允许更大的二进制文件。
- **SRAM 使用情况**：ESP32C3 拥有 400 KB SRAM（实际可用 320 KB）。根据日志显示，堆内存使用情况如下：
  - 开始任务前：189,452 字节可用
  - QUIC 任务启动时：可用 160,436 字节
  - QUIC 初始化后：可用 64,792 字节
  - MQTT 连接后：可用 39,564 字节
- **堆栈内存**：根据相关研究，估计约为 1-3 KB，表明运行期间使用量极低 [^8]。
- **能源消耗**：尚未测量，但计划未来进行分析。

这些数据表明，该应用程序在 ESP32C3 的限制范围内高效运行，证明 QUIC 适用于物联网应用。

| **资源类型** | **规格**                 | **PoC 使用情况**                  | **备注**                |
| :----------- | :----------------------- | :-------------------------------- | :---------------------- |
| 闪存         | 384 KB（嵌入式、可扩展） | 约 1.6 MB（二进制大小）           | 适合定制分区（1.68 MB） |
| SRAM         | 400 KB（可用 320 KB）    | MQTT 连接时堆内存剩余 39,564 字节 | 高效的内存管理          |
| 堆栈内存     | 未指定                   | 约 1-3 KB（估算）                 | 运行期间使用量极低      |
| 能耗         | 未指定                   | 未测量                            | 未来需要进行分析        |

## 在 ESP32 开发板上开始使用 MQTT over QUIC

若想亲自尝试此项目，请按照以下步骤在您的 ESP32C3 开发板上设置和运行 MQTT over QUIC：

1. **验证要求**：确保您拥有一块至少有 2MB 闪存的 ESP32C3 开发板、一根 USB 线、已安装的 ESP-IDF 以及用于克隆存储库的 Git。
2. **设置环境**：按照 ESP-IDF 入门指南安装 ESP-IDF 并设置环境变量（例如：`export IDF_PATH=/path/to/esp-idf`）。
3. **克隆存储库**：运行 `git clone https://github.com/emqx/ESP32-QUIC`，如果存在子模块，则运行 `git submodule update --init --recursive`。
4. **应用补丁**：导航至 `components/ngtcp2` 目录并应用补丁，例如： `git apply ../../patches/ngtcp2.patch`。
5. **配置项目**：编辑 `sdkconfig` 文件，设置 WiFi SSID、密码和 EMQX 服务器地址。使用 `idf.py menuconfig` 进行其他设置。
6. **构建项目**：在项目目录中运行 `idf.py build` 来编译代码。
7. **刷写固件**：通过 USB 连接 ESP32C3，识别串口（例如： `/dev/ttyUSB0`），并使用 `idf.py -p PORT flash` 刷写固件。
8. **监控应用程序**：使用 `idf.py -p PORT monitor` 查看日志，检查 WiFi、QUIC 和 MQTT 操作是否成功。
9. **故障排除**：验证 WiFi 凭证，确保 EMQX 服务器可访问，并在连接失败时检查日志是否存在内存问题。

**有关详细说明，请访问：**

[GitHub - emqx/ESP32-QUIC: PoC for ESP32 running QUIC client](https://github.com/emqx/ESP32-QUIC)

## 意义和潜在用例

该项目是物联网通信的一个里程碑，表明 QUIC 和完整的 MQTT 操作可以在 ESP32C3 上运行。它为实时传感器网络或智能家居等物联网应用实现了更快、更安全、更可靠的通信。RISC-V 架构凸显了开源硬件的潜力，鼓励物联网开发领域的创新。

## 未来工作

我们的下一步措施包括：

- 优化性能并降低资源消耗。
- 在各种网络条件下测试可靠性。
- 探索 MQTT 5.0 功能并增强生产安全性。
- 通过 GitHub 整合社区反馈：[GitHub - emqx/ESP32-QUIC: PoC for ESP32 running QUIC client](https://github.com/emqx/ESP32-QUIC)

## 相关资源

[^1]: QUIC 协议 - 百度百科 [快速 UDP 网络连接](https://baike.baidu.com/item/快速UDP网络连接/22785443?fr=aladdin) 
[^2]: MQTT：物联网消息传递标准 [MQTT - The Standard for IoT Messaging](https://mqtt.org/) 
[^3]: ESP32-C3 - Espressif Systems [ESP32-C3 Wi-Fi & BLE 5 SoC | 乐鑫科技](https://www.espressif.com/zh-hans/products/socs/esp32-c3) 
[^4]: EMQX - MQTT 与 AI 一体化平台 [EMQX Platform: MQTT 与 AI 一体化平台，加速智能物联网创新](https://www.emqx.com/zh/platform) 
[^5]: coreMQTT GitHub 仓库 [GitHub - FreeRTOS/coreMQTT: Client implementation of the MQTT 3.1.1 specification for embedded devices](https://github.com/FreeRTOS/coreMQTT) 
[^6]: ngtcp2 GitHub 仓库 [GitHub - ngtcp2/ngtcp2: ngtcp2 project is an effort to implement IETF QUIC protocol](https://github.com/ngtcp2/ngtcp2) 
[^7]: wolfSSL 官网 [wolfSSL Embedded SSL/TLS Library - wolfSSL](https://www.wolfssl.com/) 
[^8]: 资源受限的物联网环境中 MQTT over QUIC 的纯 HTTP/3 替代方案 https://arxiv.org/pdf/2106.12684





<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
