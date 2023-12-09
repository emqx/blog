> **作者：**李鸣飞，EMQX 社区用户。专注于物联网开发的 Java 程序员。

如今环境保护和可持续发展已达成社会基本共识。而垃圾分类作为一项有效的环保措施，正受到越来越多关注。本文将介绍一个基于 EMQX 搭建的智能垃圾分类箱，通过结合 Spring Cloud、Spring Boot、MySQL 和 MQTT 技术，采用策略模式的设计，实现了垃圾的自动分类与监测，以及相关数据的记录和分析。

## 引言

随着城市化进程的加速，垃圾产量持续增加，传统的垃圾处理方式已经无法满足环保的要求。各地政府积极响应垃圾分类政策，也让环保公司看到机会，构建出各类智慧生活解决方案。智能垃圾分类箱作为一种创新的解决方案，通过引入先进的技术，可以更好地管理垃圾资源，减少环境污染，促发社区人员进行环保。同时，也为传统环保公司带来更多的可能性，例如带屏垃圾分类箱可展示广告及带货、细分的可回收类型分类箱同时可回收盈利等。本文将详细介绍作者在某环保公司基于 EMQX 平台及 MQTT 协议为核心实现的智能垃圾分类箱的解决方案。

## 技术架构概述

### 协议的选择

经过调研及研究，最初本是选择 Netty 实现 [Modbus](https://www.emqx.com/zh/blog/modbus-protocol-the-grandfather-of-iot-communication) 中 rs485 串口协议的报文传输，来实现硬件端跟服务器之间的报文传输，但是很快就否决了，**rs485 的数据传输依赖于物理连接**。

而后，我接触到了 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)，MQTT 协议完全满足了物联网数据传输的需要。更多关于 MQTT 协议与 HTTP 之间的区别，可阅读 EMQ 官方博客：[物联网首选协议，关于 MQTT 你需要了解这些](https://www.emqx.com/zh/blog/what-is-the-mqtt-protocol)。


### 技术选型

MQTT 整体上是类似消息队列的订阅消费模式的一个报文设计，在消息处理的技术栈上，我们对 RabbitMQ、Kafka 以及 EMQX 进行了对比：

#### **EMQX**

- **类型和目的：** EMQX 是一个 MQTT（Message Queuing Telemetry Transport）代理，用于支持 MQTT 协议的消息传递。MQTT 是一种轻量级的发布/订阅协议，通常用于物联网设备和服务器之间的消息传递。
- **适用场景：** 主要适用于物联网设备和传感器数据传递，以及需要低延迟和实时性的应用。
- **通信协议：** 支持 MQTT 协议，其特点是减少通信开销和保留最新的消息。

<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>

#### **Kafka**

- **类型和目的：** Kafka 是一个分布式的流数据平台，主要用于高吞吐量的数据流处理。它设计用于日志和事件流的发布/订阅，适用于构建实时数据流处理应用。
- **适用场景：** 适用于大规模、高吞吐量的数据流处理，例如日志收集、事件处理、实时数据分析等。
- **通信协议：** 使用自定义的二进制协议，支持多个生产者和多个消费者，提供了分区和复制等特性。

#### **RabbitMQ**

- **类型和目的：** RabbitMQ 是一个开源的消息队列中间件，用于支持消息传递。它支持多种通信模式，包括发布/订阅、工作队列、RPC 等。
- **适用场景：** 适用于需要在分布式系统中实现解耦和异步通信的场景。常用于任务队列、事件处理等。
- **通信协议：** 支持多种通信协议，如 AMQP（Advanced Message Queuing Protocol）、STOMP（Simple Text Oriented Messaging Protocol）等。

最终择了 EMQX 来担任消息中间栈，理由是：

- 天然支持 MQTT 协议；
- 国人开发，社区活跃，目前已经更新到 5.x；
- 天生支持高并发及分布式场景，单点并发已经提升至亿万并发；
- 高度定制化的身份鉴权机制，自带的鉴权机制可保证设备的唯一性和安全性；
- EMQX 定制于物联网场景，更注重低延时和实时性。在上海同样负责物联网项目的同事，原先采用的 RabbitMQ，后来也替换成了 EMQX。

智能垃圾分类箱的技术架构采用了 Spring Cloud、Spring Boot、MySQL 和 EMQX 技术栈。Spring Cloud 提供了微服务架构的支持，简化了应用程序的开发。EMQX（基于MQTT 协议）用于实现智能分类箱与硬件设备之间的通信，而 MySQL 数据库用于存储垃圾投递记录以及相关数据。

![智能垃圾分类箱的技术架构](https://assets.emqx.com/images/00703c2f4321ad7e6d65a8c403a3ecdc.png)

## 设计模式：策略模式在智能分类中的应用

为了实现智能分类箱的多样化功能，本系统采用了策略模式。不同的垃圾投递步骤和监测场景被抽象为不同的策略，每个策略负责处理特定的情况。硬件设备和算法端协同工作，根据情况选择合适的策略来处理报文，从而实现垃圾的分类和环境参数的监测。

```
public abstract class AbstractHandler {

    public abstract String doInPut(BaseMessage context);

    public abstract void doOutPut(BaseMessage context) ;

}
```

```
@Component
public class HandlerFactory {
 
    /**
     * Spring会自动将Strategy接口的实现类注入到这个Map中，key为bean id，value值则为对应的策略实现类
     */
    @Autowired
    private Map<String, AbstractHandler> handlerMap;
 
 
    /**
     * 根据进程返回处理器
     * @param processType
     * @return
     */
    public AbstractHandler calculate(String processType){
        AbstractHandler abstractHandler = Optional.ofNullable(handlerMap.get(processType))
                .orElseThrow(() -> new IllegalArgumentException("Invalid Operator"));
        return abstractHandler;
    }
}
```

## 智能分类与监测

智能垃圾分类箱通过与硬件设备通信，实现了自动垃圾分类。不同类型的垃圾投递步骤被映射到不同的策略中，确保垃圾被正确分类。此外，箱内的温度、湿度等环境参数也通过传感器进行实时监测，一旦达到预设阈值，系统会触发相应的告警策略，提醒维护人员及时处理。以 JSON 格式为例：

```
{
    "进程类型":"andprocess",//安卓屏操作进程
    "指令类型":"deliver",//投递
    "流水号":"20230810"//用于处理幂等性的唯一流水号
}
```

## 数据处理与中台系统展示

数据处理如架构图所示，设备端通过电信号将传感器的数据进行收集，通过 MQTT 协议转发至 EMQX，再由 EMQX 转发至 Spring Boot 服务端，最后，报文生成的投递记录和环境监测数据被存储在 MySQL 数据库中，为后续数据分析提供基础。中台系统通过查询数据库，展示垃圾投递量、分类比例以及箱内环境状态等信息，帮助管理人员全面了解智能分类箱的运行状况。

## 积分系统的实现

通过对投递结果的换算，智能垃圾分类箱与小程序的用户积分系统相连接。用户通过参与垃圾分类，可以获得相应的积分奖励，激励更多人参与环保活动。

## 结论和展望

基于 EMQX 平台的智能垃圾分类箱通过采用 Spring Cloud、Spring Boot、MySQL 和 MQTT 技术，结合策略模式的设计，实现了垃圾的智能分类与监测。该解决方案为城市环境管理带来了创新性的改进，提高了垃圾资源的利用效率，同时也推动了环保意识的普及和提升。

随着技术的不断进步，智能垃圾分类箱还可以进一步扩展其功能，如引入图像识别技术实现更精准的分类，结合大数据分析优化垃圾资源的回收利用等。这些发展将进一步推动智能垃圾分类在城市管理中的应用和推广。

## 心得与建议

### 测试神器 MQTTX

强烈推荐可用于报文传输测试的 [MQTTX](https://mqttx.app/zh) 开发工具，可以定制化并存储你项目中用到的所有报文，你也可以备份你的报文，在后续其它场景或出差倒入来快速实现开发及测试。

![MQTTX](https://assets.emqx.com/images/894f88fd9548a1aa8decdec8c065ec7e.png)

### 项目总结和迭代

上述的架构设计并不完美，在后续运行中出现了一些设计层面的问题，比如：

- 系统层面，如果考虑到多租户及多协议，应该直接在最开始进行数据隔离设计及多协议抽象，以及考虑到策略模式下的报文定制，达到解耦报文的指令类型、执行顺序，最终实现解决方案的可迁移性；
- 在数据处理到中台系统中，针对目前的场景出现了分页时间过长的问题，而这些投递记录，其实数据类型属于时序性数据库的处理场景需求，**需要换成类似 InfluxDB、TimescaleDB、Druid 等时序性数据库来完成多设备下的多数据的高并发存储，以及满足高并发的读请求**。
- 目前构建的系统是简单易懂的，若是读者的设备数据是不断实时上报并且需要显示的，可以考虑使用一些**大数据框架类似 Kafka Streams 以及 NIFI 等数据同步框架**，来达到数据的定制化处理。

### 建议

本项目用的版本是 EMQX 4.0.5，有些 bug 已经不再维护，比如在共享订阅模式下无法消费保留消息，建议大家使用 4.4 及以上版本，EMQ 官方的维护周期也在不断往新版本走。如果是新项目，建议直接使用 5.x，因为 5.x 要比 4.x 强大很多。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
