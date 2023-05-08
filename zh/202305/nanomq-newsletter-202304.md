[NanoMQ](https://nanomq.io/zh) 项目将在 5 月正式发布 0.18 版本。这一版本除了正式发布 SOME/IP 协议转换代理功能外，主要聚焦于旧功能特性的优化和为项目增加更详细的文档和教程。

0.18 版本继续对 2 个重要功能进行升级：桥接功能新增自动退避重连参数配置选项，简化 DDS 协议代理功能的编译安装。另外 NanoSDK 新增了 MQTT over QUIC  支持和 C++ 封装。

## SOME/IP 协议代理

SOME/IP（**Scalable service-Oriented MiddlewarE over IP**）由德国宝马公司开发，能够实现以服务为导向的通信方式，工作在车载以太网的应用层，为汽车电子采用 SOA (**Service-Oriented Architecture**) 架构来处理大量数据提供了网络通信支持。

有别于传统车载总线，SOME/IP 作为面向服务的通信标准协议，不会始终不断地循环发送数据，而是只有当网络中至少存在一个接收方需要这些数据时，发送方才会发送数据，这大大提高了网络带宽的利用率。

### SOME/IP + MQTT 共同应用场景

在新一代的软件定义汽车浪潮中，需要一个安全且高性能的数据总线来融合车内不同来源的数据，支持传统 TSP 平台对接并联系 ADAS 等新一代应用服务完成计算卸载转移。NanoMQ 已经支持 DDS/SOME-IP 等 AUTOSAR 标准的数据通信方式，可以部署在车内中央网关中完成汇聚和与 TSP 平台的对接工作，并通过MQTT over QUIC/TCP + TLS 加密连接保证网关的安全性。

![SOME/IP + MQTT 共同应用场景](https://assets.emqx.com/images/b4e0a87eeb4102d2990ad6c4e9e68878.png)

### NanoMQ 的 SOME/IP 代理安装使用示例

目前 SOME/IP 协议代理转换功能处于实验阶段，目前并未默认开启，需要自行编译安装，其过程步骤介绍如下。

NanoMQ 本身是一个 MQTT broker，各种协议转换代理网关例如 DDS/ZeroMQ 等都打包进其内置的命令行工具 nanomq_cli 中，SOME/IP 也不例外。所以使用此功能时需要首先开启 nanomq_cli。NanoMQ 的 SOME/IP 协议代理功能依赖于 GENIVI/COVESA ([COVESA](https://www.covesa.global/)) 组织开源的 VSOME/IP 库。由于此开源库为 MPL license，所以并未被直接集成到 NanoMQ 项目中，需要预先在系统中安装。

```
//可以采用源代码编译安装方式：
git clone https://github.com/COVESA/vsomeip; cd vsomeip
mkdir build; cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=$YOUR_PATH ..
make
make install
```

然后通过以下命令在编译阶段为 NanoMQ 开启 SOME/IP 协议转换功能:

```
cmake -G Ninja -DBUILD_VSOMEIP_GATEWAY ..
ninja install
```

开始使用前，首先通过 “etc/nanomq_vsomeip_gateway.conf” 独立配置文件来设置桥接的主题和需要请求的 SOME/IP 服务地址。例如此处配置将从 SOME/IP 服务接收到的数据转发至本地 MQTT Broker 的 topic/pub 主题，将从主题 topic/sub 收到的 MQTT 消息转发至 SOME/IP 服务。

```
##====================================================================
# # Configuration for MQTT VSOMEIP Gateway
# #====================================================================
gateway.mqtt {
    // Address of Broker
    address = "mqtt-tcp://localhost:1883"
    sub_topic = "topic/sub"
    sub_qos = 0
    proto_ver = 4
    keepalive = 60
    clean_start = true
    username = "username"
    password = "passwd"
    clientid = "vsomeip_gateway"
    forward = "topic/pub"
    parallel = 2
}
gateway.vsomeip {
    service_id = "0x1111"
    service_instance_id = "0x2222"
    service_method_id = "0x3333"
    conf_path = "/etc/vsomeip.json"
}
```

以 VSOMEIP 项目提供的例程服务 `hello_world_service` 为需要连接和转发的 SOME/IP 服务，启动 SOME/IP gateway 将 NanoMQ 和其对接。

> 如何安装启动此示例服务请参考 VSOMEIP 项目文档，该服务也可以更换成其他 SOME/IP 兼容的服务。

```
hello_world_service  // 启动 SOME/IP Server
nanomq start         // 启动 NanoMQ MQTT Broker
nanomq_cli vsomeip_gateway --conf /etc/nanomq_vsomeip_gateway.conf // 启动SOME/IP proxy
```

之后在 `topic/pub` 主题发消息就能在对应的 `topic/sub` 收到  `hello_world_service`  回复的消息。

目前还只能提供透传服务，后续会根据用户使用的数据序列化/反序列化格式工具，如 IDL/FIDL 提供类似于 DDS Proxy Gateway 一样的自动代码生成+序列化功能。而 DDS Proxy 功能本月也得到了加强。

### DDS proxy 新增通过 CMake 工具配置 IDL 

在上一个版本中， DDS Proxy 需要手动将自动生成的生成的 IDL 序列化代码文件拷贝到编译目录，在这个版本中进一步简化了这一过程。如今用户只需要提前安装好 `idl-serial-code-gen` 工具后，就能在 NanoMQ 中通过 CMake 制定 IDL 文件来自动化这一过程。

通过cmake参数`IDL_FILE_PATH`指定`idl`文件路径 (不指定则默认为 工程路径下的 `etc/idl/dds_type.idl`)

```
$ git clone https://github.com/emqx/nanomq.git
$ cd nanomq
$ mkdir build && cd build
$ cmake -G Ninja -DIDL_FILE_PATH={IDL_PATH} -DCMAKE_PREFIX_PATH={DDS_LIBRARY_PATH} -DBUILD_DDS_PROXY=ON ..
$ ninja 
$ sudo ninja install
```

## NanoMQ/NanoSDK 新增自动重连退避选项

NanoMQ 和 NanoSDK 采用 `dialer` 机制来管理 MQTT 连接，隐藏了重连操作，不需要用户根据链接断开回调另外编程来完成重连。但并未提供自动退避选项导致客户端重连过于频繁，这可能造成 Broker 受到 DDOS 攻击。在这一版本中，新增了内置的自动指数退避算法，用户只需设置一个最大退避时间即可启动：

```
nng_dialer_setopt_ms(dialer, NNG_OPT_MQTT_RECONNECT_BACKOFF_MAX, 240000);
```

将最大退避时间设置为 24s，客户端会自动得出一个 2 以内的随机数作为等待时长： `timeout`，之后每次尝试重连都会等待  `timeout*2` 直至增至最大值。

此选项已在 NanoMQ TCP 桥接功能中默认生效。NanoSDK 最新版也已经支持。

## NanoSDK 新增 C++ binding 和 MQTT5 over QUIC 支持

除了新增了自动退避选项，NanoSDK 还增加了 MQTT5 over QUIC的支持，并提供了一个独立的 C++ 封装库：[NanoSDK-CPP](https://github.com/nanomq/nanosdk-cpp)，这是一个基于 C++ 语法和用户习惯改进的实现，内部提供了一个 C++ 版本的 MQTT5 over QUIC 例程 。 

## 安全性修复和文档更新

物联网应用对底层基础设施有着极高的安全性和稳定性要求。NanoMQ 通过持续的模糊测试，增强并保证了其在边缘场景下的可靠性和健壮性。通过模拟运行时的不合理或异常输入，不断测试并完善了 NanoMQ对非预期输入的响应和处理流程。

### 持续集成单元测试

为了提升开发效率，我们对持续集成的基础设施进行了更新，主要包括：

- GitHub action 增加了nng.mqtt_tcp 单元测试，检查 NanoSDK 可用性。 
- GitHub action 增加了针对客户端例程的黑盒测试。
- GitHub action 增加了nng.mqtt_broker_tcp 单元测试，检查 MQTT Broker 传输层可用性。
- GitHub action 增加了 nng.supplemental.core.mqtt_test 和  nng.sp.protocol.mqtt.mqtt_parser_test 单元测试，检查 MQTT 相关函数可用性。

在这里我们特别感谢来自山东大学网络安全实验室的用户 @songxpu 和 @ZuoYuanP 在 GitHub 社区上对增强 NanoMQ 健壮性作出的贡献。

其他功能更新和优化：

1. 新增了支持 Grafana 的 Metrics Exporter HTTP API。
2. 修改了 nanomq_cli 的 pub 流程，现在发布完消息后会自动断开连接。
3. 移除了 HOCON 配置文件中的 enable/disable 选项来简化配置。
4. 新增了专门针对 MQTT over TCP/QUIC 桥接的配置文档和使用教程。

此外还有一些问题修复：

1. 修复了 MQTT5 的 No Local 功能。
2. 修复高并发更新和删除 Retain 消息导致的数据竞争问题。
3. 修正了 NanoSDK 在高并发下会因为队列拥塞导致回复 message id 为0 的非法 ACK 问题。

## 即将到来

应多位用户的呼声，NanoMQ 在下一个版本中会增加动态桥接功能，用户能够通过 HTTP REST API 来修改桥接配置并 Reload/重连桥接来生效，方便更灵活的数据路由管理。另外，在之前 Demo Day 中展示的 NFTP + MQTT 文件传输功能也计划作为标准功能内置到 nanomq_cli 中。





<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
