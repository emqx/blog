We are excited to share that our project has successfully implemented a full MQTT over QUIC solution on the ESP32C3 microcontroller. By integrating the coreMQTT library with a QUIC stack (wolfSSL+ngtcp2), we have enabled complete MQTT operations—connecting, publishing, and subscribing—on a resource-constrained device. This advancement is a significant step forward for IoT communication, demonstrating that even small, low-power devices can utilize modern, secure, and efficient protocols. 

Join us in exploring this breakthrough and contribute to its development at our GitHub repository: [GitHub - emqx/ESP32-QUIC: PoC for ESP32 running QUIC client](https://github.com/emqx/ESP32-QUIC) .

## Background

### What is QUIC?

QUIC (Quick UDP Internet Connections) is a modern transport layer protocol designed to enhance web performance by reducing latency and improving security. Operating over UDP, QUIC offers faster connection establishment, multiplexing without head-of-line blocking, and built-in encryption with TLS 1.3. These features make it ideal for IoT applications, where devices often operate in high-latency or unreliable networks [^1].

> Learn more about EMQ’s accomplishments with QUIC:
>
> - [What Is the QUIC Protocol?](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov) 
> - [MQTT over QUIC: Next-Generation IoT Standard Protocol](https://www.emqx.com/en/blog/mqtt-over-quic) 
> - [How Multi-Stream of QUIC Could Mitigate the HOL Blocking Issue of MQTT Connection](https://www.emqx.com/en/blog/multi-stream-of-mqtt-over-quic)
> - [Overcoming Address Change with MQTT over QUIC](https://www.emqx.com/en/blog/overcoming-address-change-with-mqtt-over-quic) 

### What is MQTT?

[MQTT (Message Queuing Telemetry Transport)](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight, publish-subscribe messaging protocol tailored for resource-constrained devices and low-bandwidth, high-latency networks. Widely used in IoT, MQTT enables efficient communication for applications like smart homes and industrial automation. Its minimal code footprint makes it perfect for constrained environments [^2].

### What is ESP32C3?

The ESP32C3, developed by Espressif Systems, is a low-cost, low-power microcontroller for IoT applications. It features a single-core 32-bit RISC-V processor running at up to 160 MHz, 384 KB of flash memory, 400 KB of SRAM (320 KB available), and integrated Wi-Fi and Bluetooth 5 (LE). The open-source RISC-V architecture offers flexibility, making it a popular choice for IoT projects [^3].

### What is EMQX?

[EMQX](https://www.emqx.com/en/platform) is a scalable [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) designed for large-scale IoT deployments. Supporting MQTT versions 5.0, 3.1.1, and 3.1, as well as MQTT over QUIC, EMQX handles millions of concurrent connections with sub-millisecond latency, ideal for smart cities and industrial IoT [^4].

### What is coreMQTT?

coreMQTT, part of the AWS IoT Device SDK, is a lightweight [MQTT client library](https://www.emqx.com/en/mqtt-client-sdk) designed for resource-constrained devices. It enables efficient publish-subscribe communication, making it a perfect fit for integrating MQTT functionality over QUIC in this project [^5].

## The Project: Running MQTT over QUIC on ESP32

### Overview

In this project, we have implemented a complete MQTT over QUIC solution on the ESP32C3. The device connects to a WiFi network, establishes a QUIC connection to an EMQX server, and performs full MQTT operations—connecting, publishing messages, and subscribing to topics—using the coreMQTT library. This demonstrates the feasibility of running advanced networking protocols on constrained devices and their potential for efficient IoT communication.

### Implementation Details

The implementation leverages three open-source libraries:

- **ngtcp2**: A C-based QUIC implementation, used to manage QUIC connections. The ngtcp2_sample.c file, adapted from ngtcp2’s example code, demonstrates client-side QUIC functionality [^6].
- **wolfSSL**: A lightweight TLS library providing cryptographic operations for QUIC’s security, supporting TLS 1.3 [^7].
- **coreMQTT**: An MQTT client library from AWS IoT Device SDK, handling MQTT protocol operations over the QUIC transport.

These libraries were integrated into the ESP-IDF framework, with ngtcp2 wrapped as a component and patched for ESP32C3 compatibility. The project includes files like quic_demo_main.c for core functionality and esp_ev_compat.c for ESP event loop compatibility. The binary size is approximately 1.6 MB (0x16d060 bytes), fitting within a customized app partition of 1.68 MB (0x1a9000 bytes), leaving about 14% free space. Non-standard tweaks, such as disabling TLS certificate verification, were applied to simplify the PoC, but these are not suitable for production.

### Resource Usage

A key focus is the resource usage on the ESP32C3, given its limited memory and processing capabilities. Here’s what we observed:

- **Flash Memory**: The binary size is ~1.6 MB, fitting within the customized partition. The ESP32C3 has 384 KB of embedded flash, but external flash support in ESP-IDF allows larger binaries.
- **SRAM Usage**: The ESP32C3 has 400 KB of SRAM (320 KB available). Heap memory usage, based on logs, is:
  - Before starting the task: 189,452 bytes free
  - At QUIC task start: 160,436 bytes free
  - After QUIC initialization: 64,792 bytes free
  - After MQTT connection: 39,564 bytes free
- **Stack Memory**: Likely ~1-3 KB, based on related studies, indicating minimal usage during operation [^8].
- **Energy Consumption**: Not measured, but planned for future profiling.

These figures show that the application operates efficiently within the ESP32C3’s limits, making QUIC viable for IoT applications.

| Resource           | Specification                 | Usage in PoC                            | Notes                                      |
| :----------------- | :---------------------------- | :-------------------------------------- | :----------------------------------------- |
| Flash Memory       | 384 KB (embedded, expandable) | ~1.6 MB (binary size)                   | Fits within customized partition (1.68 MB) |
| SRAM               | 400 KB (320 KB available)     | Heap: 39,564 bytes free at MQTT connect | Efficient memory management                |
| Stack Memory       | Not specified                 | ~1-3 KB (estimated)                     | Minimal during operation                   |
| Energy Consumption | Not specified                 | Not measured                            | Future profiling needed                    |

## Getting Started with MQTT over QUIC on Your ESP32 Board

To try this project yourself, follow these steps to set up and run MQTT over QUIC on your ESP32C3 board:

1. **Verify Requirements**: Ensure you have an ESP32C3 board with at least 2MB flash, a USB cable, ESP-IDF installed, and Git for cloning the repository.
2. **Set Up Environment**: Follow the ESP-IDF Getting Started Guide to install ESP-IDF and set environment variables (e.g., `export IDF_PATH=/path/to/esp-idf`).
3. **Clone Repository**: Run `git clone https://github.com/emqx/ESP32-QUIC` and, if submodules are present, `git submodule update --init --recursive`.
4. **Apply Patches**: Navigate to components/ngtcp2 and apply patches, e.g., `git apply ../../patches/ngtcp2.patch`.
5. **Configure Project**: Edit sdkconfig to set WiFi SSID, password, and EMQX server address. Use `idf.py menuconfig` for additional settings.
6. **Build Project**: Run `idf.py build` in the project directory to compile the code.
7. **Flash Firmware**: Connect the ESP32C3 via USB, identify the serial port (e.g., `/dev/ttyUSB0`), and flash with `idf.py -p PORT flash`.
8. **Monitor Application**: Use `idf.py -p PORT monitor` to view logs, checking for successful WiFi, QUIC, and MQTT operations.
9. **Troubleshoot**: Verify WiFi credentials, ensure EMQX is accessible, and check logs for memory issues if connections fail.

For detailed instructions, visit our repository at: [GitHub - emqx/ESP32-QUIC: PoC for ESP32 running QUIC client](https://github.com/emqx/ESP32-QUIC).

## Significance and Potential Use Case

This project is a milestone for IoT communication, showing that QUIC and full MQTT operations can run on the ESP32C3. It enables faster, more secure and reliable communication for IoT applications like real-time sensor networks or smart homes. The RISC-V architecture highlights the potential of open-source hardware, encouraging innovation in IoT development.

## Future Work

Our next steps include:

- Optimizing performance and reducing resource consumption.
- Testing reliability under various network conditions.
- Exploring MQTT 5.0 features and enhancing security for production.
- Incorporating community feedback via GitHub issues at: [GitHub - emqx/ESP32-QUIC: PoC for ESP32 running QUIC client](https://github.com/emqx/ESP32-QUIC).

## Conclusion

We have demonstrated that the ESP32C3 can run a full MQTT over QUIC implementation using ngtcp2, wolfSSL, and coreMQTT. This project verifies the feasibility of advanced protocols on constrained devices and provides a functional solution for IoT communication. As we refine this implementation, we invite the community to explore our work at [GitHub - emqx/ESP32-QUIC: PoC for ESP32 running QUIC client](https://github.com/emqx/ESP32-QUIC)  and contribute feedback to make it production-ready.


[^1]: QUIC Protocol - Wikipedia
 [QUIC](https://en.wikipedia.org/wiki/QUIC)

[^2]: MQTT - The Standard for IoT Messaging 
   [MQTT - The Standard for IoT Messaging](https://mqtt.org/)
[^3]: ESP32-C3 - Espressif Systems
   [ESP32-C3 Wi-Fi & BLE 5 SoC | Espressif Systems](https://www.espressif.com/en/products/socs/esp32-c3)
[^4]: EMQX - The Unified MQTT and AI Platform
   [EMQX: The Unified MQTT Platform for IoT Data Streaming](https://www.emqx.com/en)
[^5]: coreMQTT GitHub Repository
   [GitHub - FreeRTOS/coreMQTT: Client implementation of the MQTT 3.1.1 specification for embedded devices](https://github.com/FreeRTOS/coreMQTT)
[^6]: ngtcp2 GitHub Repository
   [GitHub - ngtcp2/ngtcp2: ngtcp2 project is an effort to implement IETF QUIC protocol](https://github.com/ngtcp2/ngtcp2)
[^7]: wolfSSL Official Website
   [wolfSSL Embedded SSL/TLS Library - wolfSSL](https://www.wolfssl.com/)
[^8]: A Pure HTTP/3 Alternative to MQTT-over-QUIC in Resource-Constrained IoT
   https://arxiv.org/pdf/2106.12684



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
