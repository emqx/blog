*驽马十驾，功在不舍*。新春之交，NanoMQ 继续保持稳步更新，最新的 0.16 版本将于三月初发布。NanoMQ 为用户提供了 2 个重要新功能：MQTT over QUIC 的多流桥接和 DDS 协议转换代理，拓宽了 NanoMQ 的弱网桥接传输性能和在边缘端的使用场景。同时 NanoMQ 项目也在不懈努力提高项目的鲁棒性和安全性，积极快速响应社区提出的 Issue 和使用问题，新增了模糊测试用例和自动化的代码覆盖测试脚本。另外还新增了绿色安装版的 Windows 平台安装包。

## QUIC 多流桥接

QUIC 协议相较于 TCP 的一大优势在于解决了队首阻塞的问题，但这是依赖于 QUIC 的单链接多 Stream 特性的。NanoMQ 之前发布的 MQTT over QUIC 桥接功能中暂时只支持单流模式，所有的 MQTT 包都在单一消息流（Stream）上面传输。单流传输当遇到网络拥塞或者网络抖动的情况时，会引起大量的消息重传，一样会阻塞后续到达的消息，从而造成逐步提高的消息延时，甚至是连接断开。 为了解决这一问题，NanoMQ 和 EMQX 5.0 一起设计和引入了 Mutli-stream QUIC 协议标准，以提供更好消息传输体验。

### 何为 MQTT over QUIC + Mutli-Stream?

Stream 是 QUIC 协议中传输层轻量级的有序字节流抽象，流可以是双工或半双工的。每个 QUIC 链接必须有大于等于一个的 Stream。客户端发起连接和创建 Stream 后，在 Stream 的基础上建立 MQTT 连接和进行报文交互。

![QUIC Multi-Stream](https://assets.emqx.com/images/ef001af010a9cb2a52243b46ed49dfa6.png)

<center>QUIC Multi-Stream</center>

而在 0.16 版本中 NanoMQ 正式支持了多流桥接，当用户使用 MQTT over QUIC 桥接功能并开启多流选项时，NanoMQ 会根据用户配置的桥接上下行主题自动创建对应的 Topic-Stream 配对，每个主题之间的消息互相隔离。

目前多流桥接将 Stream 分为以下两种类型

- **控制流：** 对于每个 MQTT over QUIC 连接，首次建立时必须先建立此 Stream，所有 MQTT 控制信令如 CONNECT/PINGREQ/PINGRESP 都默认在此流上传输。连接以控制流作为探测当前网络环境和连接健康度的唯一指标，控制流断开将导致连接重连。但用户也可以选择在控制流上传输 PUBLISH 包。
- **数据流：** 桥接客户端每次进行 PUBLISH 和 SUBSCRIBE 操作都会根据使用的主题创建一个对应的数据流。此流由订阅或发布行为开启，服务端与客户端都会标识记录 PUBLISH 和 SUBSCRIBE 包中 Topic 和 此 Stream 的对应关系。所有发布到此 Topic 的数据都会被定向到此数据流。有别于控制流，数据流断开不会导致连接断开，而是下次自动重建。

![NanoMQ 多流桥接](https://assets.emqx.com/images/8bd4209f07811ee4f8f5006655c342ee.png)

如上图所示，单路 Stream 的情况下若 Topic 1 QoS 1 消息重传，会导致 Topic 2 和 Topic 3 的消息被阻塞。若使用多 Stream 桥接则可以在带宽未耗尽的情况下让多个主题的消息并行传输。当然相对应而言只能够保证在同一个主题内部的 QoS 消息的传输和到达顺序。

### 如何使用多流桥接？

目前使用多流桥接只需打开对应的配置选项：

旧配置文件格式：

```
## multi-stream: enable or disable the multi-stream bridging mode
## Value: true/false
## Default: false
bridge.mqtt.emqx.quic_multi_stream=false

## 在流中是否赋予Qos消息高传输优先级
## 针对每个流单独生效，非主题优先级
## Value: true/false
## Default: true
bridge.mqtt.emqx.quic_qos_priority=true
```

HOCON 格式:

```
quic_multi_stream = false
quic_qos_priority=true
```

之后根据用户 Pub/Sub 的具体主题会建立对应的 Stream，可以在 log 中检查功能是否生效，如订阅 nanomq/1 主题就会自动创建一个 data stream：

```
quic_ack_cb: Quic bridge client subscribe to topic (QoS 1)nanomq/1.
mqtt_sub_stream: topic nanomq/1 qos 1
bridge client is connected!
quic_pipe_open: [strm][0x618000020080] Starting...
quic_pipe_open: [strm][0x618000020080] Done...
quic_strm_cb: quic_strm_cb triggered! 0
decode_pub_message: topic: [$SYS/brokers/connected], qos: 0
mqtt_sub_stream: create new pipe 0x61c000020080 for topic nanomq/1
quic_strm_cb: QUIC_STREAM_EVENT_START_COMPLETE [0x618000020080] ID: 4 Status: 0
```

之后 NanoMQ 就会自动根据 Topic 将数据包导流至不同的 Stream 发送。经过内部测试，在使用模拟 2s 延迟和 40% 丢包的弱网环境时，能够得到 stream 数量倍数的延时降低。

### Sub 包优先传输

在上一个版本中，NanoMQ 支持了 MQTT over QUIC 桥接中的 QoS 消息的优先传输。从 0.16 版本开始，Subscribe/UnSubscribe 也将优先得到传输，来保证弱网下业务的正常运行。

## DDS 协议代理

DDS 即 Data Distribution Service 数据分发服务，是以数据为中心的分布式实时通信中间件协议，采用发布/订阅体系架构，强调以数据为中心，提供丰富的 QoS 服务质量策略，以保障数据进行实时、高效、灵活地分发，可满足各种去中心化的实时通信应用需求。

DDS 多用于点对点形式将数据在进程间通信。DDS 虽然也可以允许发布者发布数据，订阅者订阅数据，以及发布者和订阅者之间的双向通信，但仅局限在同一个域内，难以进行跨域通信。而在云边一体化的消息场景中，结合 MQTT + DDS 两种协议可以完美融合 broker + brokerless 两种消息模式。

NanoMQ 0.16 发布了 DDS Proxy 插件，其基于 [Cyclone DDS](https://cyclonedds.io/) （基于 OMG（Object Management Group）DDS 规范的开源 DDS 实现）开发，能够完成将 DDS 消息转换为 MQTT 消息并桥接上云的功能，以支持用户将 DDS 的数据通过 NanoMQ 来完成跨域传输并通过 MQTT 和云端互通。

![DDS 协议代理](https://assets.emqx.com/images/d254d8e9e2a9e95f294bd7522e3bfd73.png)

### DDS Proxy 使用方法

NanoMQ 的 DDS 协议转换插件通过 nanomq_cli 启动。目前该功能尚未集成到 Release 安装包中，如需使用还需要编译安装。

NanoMQ 并未直接引入 DDS 库，所以需要在运行环境中安装 CycloneDDS。在下一版本中，会在常见的平台版本的官方发行安装包里内置 CycloneDDS 的静态库，但如需交叉编译还需按照以下流程：

#### 安装 Iceoryx

> iceoryx 是 CycloneDDS 通过共享内存通信所需的依赖，如不需共享内存 IPC 可跳过本步骤

```
$ git clone https://github.com/eclipse-iceoryx/iceoryx.git
$ cd iceoryx
$ git checkout release_2.0
$ mkdir build && cd build
$ cmake -G Ninja -DCMAKE_INSTALL_PREFIX={USER_LIBRARY_PATH} ../iceoryx_meta
$ ninja
$ sudo ninja install
```

#### 安装 CycloneDDS

```
$ git clone https://github.com/eclipse-cyclonedds/cyclonedds.git
$ cd cyclonedds
$ mkdir build && cd build
$ cmake -G Ninja -DCMAKE_INSTALL_PREFIX={USER_LIBRARY_PATH} -DCMAKE_PREFIX_PATH={YOUR_LIBRARY_PATH} -DBUILD_EXAMPLES=ON ..
$ ninja
$ sudo ninja install
```

#### 配置 DDS 的 IDL

DDS 相较于 MQTT 对于 payload 的定义方式不同，MQTT 协议并不关心消息的 Payload 内容， 而 DDS 通过用户编写的 IDL 文件来定义 DDS 消息的数据格式和类型。IDL（Interface Description Language）是一种通用的描述语言，用于在不同的编程语言之间定义数据类型，以保证不同节点之间以正确的格式通信。

CycloneDDS 库中通过 CMake 工具来自动根据用户内置的 IDL 文件来生成消息解析代码，其函数名和变量名会根据 IDL 中的定义改变。NanoMQ 保留了这一流程，每次编译时会根据 nanomq_cli/dds2mqtt/dds_type.idl 这一 IDL 文件来生成消息序列化和反序列化的代码。目前还需要用户自行将生成的代码 `dds_type.h` 和 `dds_type.c` 替换  [dds_mqtt_type_conversion.h](https://github.com/nanomq/nanomq/blob/0.16.0/nanomq_cli/dds2mqtt/dds_mqtt_type_conversion.h)/[dds_mqtt_type_conversion.c](https://github.com/nanomq/nanomq/blob/0.16.0/nanomq_cli/dds2mqtt/dds_mqtt_type_conversion.c)/[dds_client.c](https://github.com/nanomq/nanomq/blob/0.16.0/nanomq_cli/dds2mqtt/dds_client.c) 文件中的函数名和引用。

在后续的 NanoMQ 版本规划中，将提供一个自动化的代码生成工具，能够根据 IDL 来自动替换源文件完成这部分工作，不再需要用户手动修改源码适配 DDS 结构体定义。

### 编译安装 NanoMQ + DDS Proxy

```
$ git clone https://github.com/nanomq/nanomq.git
$ cd nanomq
$ mkdir build && cd build
$ cmake -G Ninja -DCMAKE_PREFIX_PATH={USER_LIBRARY_PATH} -DBUILD_DDS_PROXY=ON ..
$ ninja 
$ sudo ninja install
```

### 配置打开 DDS Proxy

配置 /etc/nanomq_dds_gateway.conf 来设置需要进行桥接和转发的 MQTT 和 DDS 主题。

```
## 转发规则配置
forward_rules = {
	## DDS to MQTT 主题
    dds_to_mqtt = {
        from_dds = "MQTTCMD/topic1"
        to_mqtt = "DDS/topic1"
    }
    ## MQTT to DDS 主题
    mqtt_to_dds = {
        from_mqtt = "DDSCMD/topic1"
        to_dds = "MQTT/topic1"
    }
}

## DDS 配置参数
dds {
    idl_type = topic1Type
    domain_id = 0
    
    shared_memory = {
        enable = false
        log_level = info
    }
}

## MQTT 配置参数
mqtt {
	connector {
        server = "mqtt-tcp://127.0.0.1:1883"
        proto_ver = 4
        # clientid="bridge_client"
        keepalive = 60s
        clean_start = false
        username = username
        password = passwd
        
        ssl {
            enable = false
            key_password = "yourpass"
            keyfile = "/etc/certs/key.pem"
            certfile = "/etc/certs/cert.pem"
            cacertfile = "/etc/certs/cacert.pem"
        }
    }
}


```

启用 iceoryx 传输可参考文档[https://github.com/nanomq/nanomq/blob/0.16.0/nanomq_cli/dds2mqtt/doc/Shared_memory.md](https://github.com/nanomq/nanomq/blob/0.16.0/nanomq_cli/dds2mqtt/doc/Shared_memory.md)

### 启动和测试

此处以 DDS - MQTT 双向消息桥接为例。

- 启动 MQTT Broker

```
$ nanomq start
```

或

```
$ emqx start
```

- 启动 DDS Proxy 桥接 MQTT 的`DDSCMD/topic1` 主题到 DDS 的 `MQTT/topic1` 主题。

```
$ ./nanomq_cli ddsproxy proxy --conf nanomq_dds_gateway.conf
```

- 启动 MQTT 客户端订阅主题 `DDS/topic1` 以验证消息是否桥接成功。

```
$ ./nanomq_cli sub --url "mqtt-tcp://127.0.0.1:1883" -t "DDS/topic1"
```

现在我们发布一些消息到 DDS 主题来验证桥接是否成功。

- 启动 DDS 客户端订阅 DDS 主题 `MQTT/topic1`

```
$ ./nanomq_cli ddsproxy sub -t "MQTT/topic1"
```

- 启动 MQTT 客户端发布消息到 MQTT 主题 `DDSCMD/topic1`

```
$ ./nanomq_cli pub --url "mqtt-tcp://127.0.0.1:1883" -t "DDSCMD/topic1" -m '{
  "int8_test":    1,
  "uint8_test":   50,
  "int16_test":   27381,
  "uint16_test":  1,
  "int32_test":   0,
  "uint32_test":  32,
  "int64_test":   6820785120,
  "uint64_test":  25855901936,
  "message":      "aaabbbddd",
  "example_enum": 0,
  "example_stru": {
    "message":      "abc"
    }
}'
```

就能在订阅 `MQTT/topic1` 的 DDS 客户端处收到对应消息。如此就完成了将 MQTT 消息转化为 DDS 消息的过程，反之亦可。 

## 其他优化

### 增加覆盖率测试和模糊测试

为了继续提高 NanoMQ 的工程质量和安全性，我们从 0.15.1 版本开始引入了 CodeCOV 来完成自动化代码覆盖率测试。

在 2 月中，NanoMQ 收到了许多有价值的模糊测试数据集和 Issue，在用户的帮助下找到了许多潜在安全隐患，在此对 [https://github.com/Nereuxofficial](https://github.com/Nereuxofficial)  和 [https://github.com/realsung](https://github.com/realsung)  两位用户致以真挚的感谢。所有 Issue 都已经在一天内完全修复，所有他们提供的数据集都已纳入项目的自动模糊测试。

### 推出 Windows 绿色版

为了更好的支持 Windows 平台的用户，我们基于之前发布的 msi 安装包基础上，推出了绿色版的安装包，解压即可用。目前 Windows 版本只支持基础的 MQTT broker 桥接、断网续传等功能。

## 问题修复

1. 修复 0.15.1 版本中多路桥接中消息回环触发异步 IO 越界的问题。
2. 修复若干由模糊测试发现的安全隐患和内存泄漏，提高鲁棒性。
3. 修复 nanomq_cli 的 quic工具使用。
4. 修复 nanomq_cli 的无法将输出重定向至文件的问题。
5. 修复 TSAN 发现的 MQTT over QUIC 传输层的线程竞争问题。
6. 修复 NanoMQ 0.15 版本在 Windows 平台的兼容问题。
7. 增加了可以在 MQTT 5 桥接连接中定义连接属性。

## 即将到来

NanoMQ 项目进入了第三个年头，感谢大家对项目的使用和支持。在下一个版本，NanoMQ 项目计划引入 SOME/IP 协议的桥接转换。同时还会继续改进 DDS Proxy 功能的易用性，推出包含此功能的安装包，并为其加入 IDL 自动代码生成功能。此外，在 MQTT over QUIC 桥接部分还会增加双向认证和证书配置功能。





<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
