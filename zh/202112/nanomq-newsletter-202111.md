11 月 NanoMQ 团队主要致力于为 NNG 添加 [MQTT](https://www.emqx.com/zh/mqtt) 支持，同时对 [NanoMQ](https://nanomq.io/zh) 进行了一些更新。

## NanoMQ 更新

- 优化了配置文件的日志打印输出，会自动根据是否指定配置文件路径判断是否输出告警信息。
- Bug 修复：当客户端批量订阅多个主题时，NanoMQ 无法按照正确的订阅 QoS 等级来转发消息。

## NNG 现已支持 MQTT

NanoMQ 是 EMQ 与 NNG 合作的开源项目。在 NanoMQ 的 GitHub 仓库内部有一个 NNG 的 sub-module，其为 NanoMQ 单独维护的 NNG 版本（[GitHub 项目地址](https://github.com/nanomq/nng/tree/master)）。目前其 master 分支是 NanoMQ 为 MQTT Broker 单独开发优化并独立维护的特殊版本，从中我们已经为 NNG 提交了若干有价值的 PR 和 Issue。但此分支与 nanomsg 的 SP 协议并不兼容。

本月我们主要致力于为 NNG 添加 MQTT 3.1.1 协议支持，从而使 NanoMQ 与 NNG 的 SP 协议兼容，以便两个项目未来能更好地共同使用。这也与 NanoMQ 之前制定的 RoadMap 方向一致。

根据之前和 NNG 项目维护者 Garrett 在开源合作会议上共同制定的技术目标，NNG 未来会增加支持ZeroMQ 和MQTT 3.1.1/5.0。经过一个月的努力，我们已经完成了 MQTT 3.1.1 协议的开发支持，并将其命名为 NanoSDK。NanoSDK 内部设计保留了 NNG 框架的编程风格，兼容 NNG 原有的 SP 协议。同时不影响其 HTTP/Websocket/TLS 等功能的使用。

相较于其他 MQTT 3.1.1 SDK，NanoSDK 具有以下优势：

### **全异步 I/O 和良好的 SMP 支持**。

通过 NNG 的全异步 I/O 实现 C 语言的 Actor 编程模型，可以很好的将负载均衡分配到多个 CPU 核心。

### **高度兼容性和移植性**

继承了 NNG 的兼容性和易于移植的特点，只依赖原生 POSIX 标准 API，对各种类 Linux 构建系统友好。方便移植到新硬件和操作系统平台。

### 支持多种 API 风格

NNG 框架的编程风格有较高的上手门槛，需要用户对其 AIO 和 Context 的使用有深入认识。所以我们也为习惯于使用 Paho 和 Mosquitto sdk 的用户准备了传统的回调注册机制。这样在降低编程难度的同时也能兼得 NNG 的优势。

### 高吞吐 **&** **低延时**

在 NanoMQ 的测试报告中已经体现出了其强大的高吞吐和低延时性能优势，与其一脉相承 Nano MQTT SDK 也一样在性能方面有出色表现。其占用资源性价比高，不同于传统 [MQTT SDK](https://www.emqx.com/zh/mqtt-client-sdk) 只有1-2个线程。NanoSDK 可以完全利用系统硬件资源，提供更高消费吞吐能力。

在大部分基于 EMQX 构建的物联网架构中，端侧和消费侧的处理性能不足导致消息积压一直是困扰开源开发者的难题。特别是对于 QoS 1/2 消息而言，大部分 SDK 对于 QoS 1/2 消息都是同步阻塞 Ack。而 NanoSDK 在保证了 QoS 消息顺序和消息重发机制的前提下，提供了异步 Ack 能力，大大提高了 QoS 1/2 的吞吐消费能力。

## 附：NanoSDK 与 Paho C MQTT SDK 性能对比测试报告

我们选取当前较为广泛使用的 Paho C MQTT SDK 与 NanoSDK 进行了性能对比测试。

### 测试环境

- Quad Core model: 11th Gen Intel Core i7-1165G7
- 16G memory
- 500K PUBLISH message with 2 bytes payload

### 测试场景逻辑

建立一个客户端连接 EMQX 完成收发 50000 条 QoS 0/1/2 消息（两者都只统计总共读 Socket 占用时间来计算消息速率）。为了贴近大部分真实业务场景，我们用 emqtt_bench 工具发送2字节的消息给此客户端，客户端每次收到一条消息都将回复14字节的 Publish 消息，客户端每次处理一发一收的消息。两个与场景除了使用的 SDK 不同外，其余条件保持一致。

### 测试结果

具体时间数字可能每次测试有细微不同。

| Qos  | NanoSDK（NNG） | Paho C MQTT |
| :--- | :------------- | :---------- |
| 0    | 2946 msg/s     | 2944 msg/s  |
| 1    | 2944 msg/s     | 610 msg/s   |
| 2    | 2919 msg/s     | 585 msg/s   |

可见在多核平台中，单个客户端情况下，NanoSDK 在 QoS 1/2 场景有着巨大优势。同时由于 NanoSDK 基于 NNG 用 C 语言实现了 MQTT 的类 Actor 编程模型，全异步 I/O 实现可以很好地将负载均衡分配到多个 CPU 核心。开发者可以按照我们的 Context 例程启动多个 MQTT 连接来达到 QoS 0 的更高消费能力，而不用苦恼于多线程并发开发。

NanoMQ 团队计划于 12 月与 NNG 项目维护者 Garrett 举行开源开发会议，讨论如何双方项目的合并事宜。欢迎大家试用 NanoMQ Fork 的 NNG 仓库内的 nng-mqtt 分支[https://github.com/nanomq/nng/tree/nng-mqtt](https://github.com/nanomq/nng/tree/nng-mqtt)，抢先体验。
