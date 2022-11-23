## 前言

QUIC([RFC9000](https://datatracker.ietf.org/doc/html/rfc9000)) 是下一代互联网协议 HTTP/3 的底层传输协议，与 TCP/TLS 协议相比，它**在减少连接开销与消息延迟的同时，为现代移动互联网提供了有效灵活的传输层。**

EMQX 5.0 是首个将 QUIC 引入 MQTT 的开创性产品。在长期的客户服务和技术探索中，我们注意到 QUIC 的特性能够和一些物联网场景完美契合，于是尝试将 MQTT 的传输层替换成 QUIC，由此诞生了 MQTT over QUIC。

正如 [MQTT over QUIC：物联网消息传输还有更多可能](https://www.emqx.com/zh/blog/mqtt-over-quic) 一文所述，在网络不稳定、连接多变的物联网场景下，QUIC 低连接开销和多路径支持的特性就显示出了其领先的优势。测试数据也表明，基于 QUIC 0 RTT/1 RTT 重连/新建能力，MQTT over QUIC 能够在弱网与不固定的网络通路中有效提升用户体验。

EMQ 正以世界知名开源和开放标准机构 OASIS 的 [Foundational Sponsor ](https://www.emqx.com/zh/news/emq-becomes-oasis-opens-newest-foundational-sponsor)身份积极推动 MQTT over QUIC 的标准化落地。事实上，目前已经有一部分客户开始尝试将这一新特性投入使用并获得了良好的反馈。为了更多用户能体验到 MQTT over QUIC 为物联网消息传输带来的提升，我们将通过本文指导您如何从零开始上手使用 MQTT over QUIC。


## 启用 MQTT over QUIC

MQTT over QUIC 特性随 EMQX 5.0 发布，请前往以下地址下载安装最新版本的 EMQX：[https://www.emqx.io/zh/downloads](https://www.emqx.io/zh/downloads)。

由于是实验性功能，在 CentOS 6、macOS 以及 Windows 系统下并未包含 QUIC 编译，请自行从源码编译并在编译前指定环境变量 `BUILD_WITH_QUIC=1` ，其他操作系统和平台则可以正常使用。

MQTT over QUIC 默认禁用，请通过以下配置手动开启。

1. 打开配置文件 `etc/emqx.conf`，取消 `listeners.quic.default` 配置组的注释（如果没有此配置组请手动添加）：
   ```
   # etc/emqx.conf
   listeners.quic.default {
     enabled = true
     bind = "0.0.0.0:14567"
     max_connections = 1024000
     keyfile = "etc/certs/key.pem"
     certfile = "etc/certs/cert.pem"
   }
   ```
2. 该配置表示启用 QUIC 监听器并绑定 UDP `14567` 端口，保存成功后请重启 EMQX 以应用配置。
3. 执行 `emqx_ctl listeners` 命令，可在结果中看到 MQTT over QUIC 监听器已启用：
   ```
   > emqx_ctl listeners
   quic:default
     listen_on       : :14567
     acceptors       : 16
     proxy_protocol  : undefined
     running         : true
   ssl:default
     listen_on       : 0.0.0.0:8883
     acceptors       : 16
     proxy_protocol  : false
     running         : true
     current_conn    : 0
     max_conns       : 512000
   ```

您也可以使用 Docker，通过环境变量选取 UDP `14567` 作为 QUIC 端口快速体验：

```
docker run -d --name emqx \
  -p 1883:1883 -p 8083:8083 \
  -p 8084:8084 -p 8883:8883 \
  -p 18083:18083 \
  -p 14567:14567/udp \
  -e EMQX_LISTENERS__QUIC__DEFAULT__keyfile="etc/certs/key.pem" \
  -e EMQX_LISTENERS__QUIC__DEFAULT__certfile="etc/certs/cert.pem" \
  -e EMQX_LISTENERS__QUIC__DEFAULT__ENABLED=true \
emqx/emqx:5.0.10
```

## MQTT over QUIC 客户端与工具

相比于 MQTT 而言，目前 MQTT over QUIC 仍然缺少完整的客户端库和工具链支持。

我们针对 MQTT over QUIC 的适用场景，计划提供 C、Java、Python、Golang 等多个语言的客户端库并按照优先级逐个支持，确保嵌入式硬件等这类契合场景的业务能够率先将 QUIC 利用起来。

### 已有的客户端 SDK

- [NanoSDK](https://github.com/nanomq/NanoSDK/)：由 EMQ 旗下 NanoMQ 团队发布的 C 语言的 MQTT SDK，除 MQTT over QUIC 外还支持 WebSocket、nanomsg/SP 等多协议 
- [NanoSDK-Python](https://github.com/wanghaEMQ/pynng-mqtt)：NanoSDK 的 Python 语言 binding
- [NanoSDK-Java](https://github.com/nanomq/nanosdk-java)：NanoSDK 的 Java JNA binding
- [emqtt](https://github.com/emqx/emqtt)：Erlang 语言的 MQTT 客户端库，支持 QUIC

除了客户端库之外，EMQ 还在边缘计算产品 NanoMQ 中提供了 MQTT over QUIC 桥接支持，在特定的应用中您可以借助 NanoMQ 实现边缘数据通过 QUIC 桥接上云，无需过多开发集成即可应用 MQTT over QUIC 的特性。

### 问题与解决

在开发中，考虑到 QUIC 基于 UDP 协议，目前许多运营商仍然对 UDP 包有特殊的路由策略，这往往导致 QUIC 连接无法成功建立或一直被丢包。

因此 MQTT over QUIC 客户端设计支持了 fallback 能力：API 层能够使用统一的操作编写业务，传输层则根据网络情况实时切换，当 QUIC 不可用时自动切换为 TCP/TLS 1.2，确保各类网络环境下业务都能正常运行。


## 通过 NanoSDK 完成 MQTT over QUIC 连接

[NanoSDK](https://github.com/nanomq/NanoSDK/) 基于 MsQuic 项目率先实现了第一个 C 语言的 MQTT over QUIC SDK，能无缝兼容 EMQX 5.0。内部采用全异步 IO 设计，将 QUIC Stream 和 MQTT 连接映射绑定，并内置实现了 0RTT 快速握手重连功能，支持多核任务并行。

![MQTT over QUIC SDK](https://assets.emqx.com/images/54fa9b47f4cd14af1dc1bb20e4dc8fc0.png)

### NanoSDK 使用示例

API 方面保持了之前的使用习惯，一行代码即可基于 QUIC 创建 MQTT 客户端：

```
## Create MQTT over Quic client with NanoSDK
nng_mqtt_quic_client_open(&socket, url);
```

消息示例代码请参考：[https://github.com/nanomq/NanoSDK/tree/main/demo/quic](https://github.com/nanomq/NanoSDK/tree/main/demo/quic) 。

编译后可以通过以下命令连接 EMQX 5.0 的 14567 端口进行测试。

```
quic_client sub/pub mqtt-quic://54.75.171.11:14567 topic msg
```

NanoSDK 也提供 Java 和 Python 的 binding，例程可以分别参考 [https://github.com/nanomq/nanosdk-java/blob/main/demo/src/main/java/io/sisu/nng/demo/quicmqtt/MqttQuicClient.java](https://github.com/nanomq/nanosdk-java/blob/main/demo/src/main/java/io/sisu/nng/demo/quicmqtt/MqttQuicClient.java) 和 [https://github.com/wanghaEMQ/pynng-mqtt/blob/master/examples/mqttsub.py](https://github.com/wanghaEMQ/pynng-mqtt/blob/master/examples/mqttsub.py) 


## 通过 NanoMQ 桥接完成 MQTT 3.1.1/5.0 与 MQTT over QUIC 的转换兼容

[NanoMQ](https://nanomq.io/) 是一款超轻量、高性能且跨平台的边缘 MQTT 消息引擎，兼具多协议消息总线功能，支持 MQTT over QUIC 桥接功能。它能够将传统 MQTT 客户端的数据转换成 QUIC 数据包并发给云端的 EMQX，从而为无法集成或找到合适 MQTT over QUIC SDK 的端侧设备和难以修改固件的嵌入式设备提供在 IoT 场景利用 QUIC 协议优势的捷径，降低使用门槛。

![NanoMQ](https://assets.emqx.com/images/f1138a902ac66c799cdbea0ccd593cb0.png)

在需要与云端 MQTT 服务进行数据同步的各种物联网场景中，通过 NanoMQ 的多协议接入能力，您可以将其作为边缘消息总线和统一的数据空间，统一汇聚诸如 HTTP、MQTT 3.1.1/5.0、WebSocket、nanomsg/nng 和 ZeroMQ 等常用的 broker/brokerless 消息协议，再由 NanoMQ 内部强大的 Actor 消息处理模型转化成标准的 MQTT 消息后，通过 QUIC 传输层上云传输。

借此充分利用 MQTT over QUIC 0RTT 快速重连和被动地址切换等功能来克服网际漫游、弱网传输和 TCP 队头阻塞等各类常见的物联网连接问题。您还可以通过 NanoMQ 的规则引擎对数据做重定向、本地缓存或持久化。

依靠 EMQX+NanoMQ 的云边一体化的消息架构，用户能够快速且低成本的在泛物联网场景中完成跨时空地域的数据采集和同步需求。

![EMQX+NanoMQ](https://assets.emqx.com/images/fa41bd1bab7db231e28c9c9b2b1c3e95.png)
 
值得一提的是，NanoMQ 支持 QUIC 连接失败时自动切换至标准 MQTT over TCP 桥接的能力，这能够确保您的使用不受网络环境限制。

### NanoMQ 桥接示例

下载安装 NanoMQ：

```
git clone https://github.com/emqx/nanomq.git
cd nanomq ; git submodule update --init --recursive

mkdir build && cd build
cmake -G Ninja -DNNG_ENABLE_QUIC=ON ..
sudo ninja install
```

开启 QUIC 桥接功能的 NanoMQ 编译安装完成后，可以在配置文件`/etc/nanomq.conf`中配置 MQTT over QUIC 桥接功能和对应的主题，使用 `mqtt-quic` 作为 URL 前缀即是采用 QUIC 作为 MQTT 的传输层：

```
## Bridge address: host:port .
##
## Value: String
## Example: ## Example: mqtt-tcp://broker.emqx.io:1883 （这是标准MQTT over TCP）
bridge.mqtt.emqx.address=mqtt-quic://54.75.171.11:14567
```

### MQTT over QUIC CLI 工具

NanoMQ 还提供了 nanomq_cli ，其中包含有 MQTT over QUIC 的客户端工具供用户测试 EMQX 5.0 的MQTT over QUIC 功能：

```
nanomq_cli quic --help
Usage: quic conn <url>
       quic sub  <url> <qos> <topic>
       quic pub  <url> <qos> <topic> <data>
       
## subscribe example
nanomq_cli quic sub mqtt-quic://54.75.171.11:14567 2 msg
```

综上所述，您可以直接将 NanoSDK 集成到项目中，亦可以搭配 NanoMQ 使用，实现设备侧到云端的 QUIC 接入。


## 将 emqtt-bench 用于 QUIC 性能测试

[emqtt-bench](https://github.com/emqx/emqtt-bench) 是一个 MQTT 性能基准测试工具，其同样提供了 QUIC 支持，我们用它完成了 [MQTT over QUIC vs TCP/TLS](https://www.emqx.com/zh/blog/mqtt-over-quic) 的性能对比测试。用户可以利用其做应用的 Benchmark，或在实际环境中验证 MQTT over QUIC 的性能与收益。

### 编译 emqtt-bench

编译要求有 Erlang 环境，以 macOS 为例安装 Erlang 和 Coreutils：

```
brew install coreutils 
brew install erlang@24 
```

通过源码编译 emqtt-bench

```
git clone https://github.com/emqx/emqtt-bench.git 
cd emqtt-bench 
CMAKE_BUILD_TYPE=Debug BUILD_WITH_QUIC=1 make 
```

编译成功有以下提示：

```
...
===> Warnings generating release:
*WARNING* Missing application sasl. Can not upgrade with this release
===> Release successfully assembled: _build/emqtt_bench/rel/emqtt_bench
===> Building release tarball emqtt_bench-0.3+build.193.ref249f7f8.tar.gz...
===> Tarball successfully created: _build/emqtt_bench/rel/emqtt_bench/emqtt_bench-0.3+build.193.ref249f7f8.tar.gz
```

> 可能会遇到如下错误，忽略即可：

```
/Users/patilso/emqtt-bench/scripts/rename-package.sh: line 9: gsed: command not found 
/Users/patilso/emqtt-bench/scripts/rename-package.sh: line 9: gsed: command not found 
/Users/patilso/emqtt-bench/scripts/rename-package.sh: line 9: gsed: command not found 
/Users/patilso/emqtt-bench/scripts/rename-package.sh: line 9: gsed: command not found
```

### 测试 QUIC

进入编译输出目录：

```
cd _build/emqtt_bench/rel/emqtt_bench/bin
```

通过指定 `--quic` 选项以使用 QUIC 协议发起连接并进行订阅，此处使用 10 个客户端订阅 `t/1` 主题：

```
./emqtt_bench sub -p 14567 --quic -t t/1 -c 10 
```

新开另一个窗口，同样使用 QUIC 协议连接并进行发布测试：

```
./emqtt_bench pub -p 14567 --quic -t t/1 -c 1
```

此时将进入 1 pub 10 sub 的性能测试：

![QUIC 性能测试](https://assets.emqx.com/images/ffd3f7713e822adaa8494cf579ceafb6.png)

查看本地 UDP 14567 端口使用情况：

```
$ lsof -nP -iUDP | grep 14567

com.docke 29372 emqx   76u  IPv6 0xea2092701c033ba9      0t0  UDP *:14567
beam.smp  50496 emqx   39u  IPv6 0xea2092701c014eb9      0t0  UDP [::1]:52335->[::1]:14567
beam.smp  50496 emqx   40u  IPv6 0xea2092701c017689      0t0  UDP [::1]:56709->[::1]:14567
beam.smp  50496 emqx   41u  IPv6 0xea2092701c0151c9      0t0  UDP [::1]:52175->[::1]:14567
beam.smp  50496 emqx   42u  IPv6 0xea2092701c0157e9      0t0  UDP [::1]:54050->[::1]:14567
beam.smp  50496 emqx   43u  IPv6 0xea2092701c015af9      0t0  UDP [::1]:58548->[::1]:14567
beam.smp  50496 emqx   44u  IPv6 0xea2092701c013639      0t0  UDP [::1]:52819->[::1]:14567
beam.smp  50496 emqx   45u  IPv6 0xea2092701c016119      0t0  UDP [::1]:57351->[::1]:14567
beam.smp  50496 emqx   46u  IPv6 0xea2092701c017999      0t0  UDP [::1]:52353->[::1]:14567
beam.smp  50496 emqx   47u  IPv6 0xea2092701c017ca9      0t0  UDP [::1]:57640->[::1]:14567
beam.smp  50496 emqx   48u  IPv6 0xea2092701c014ba9      0t0  UDP [::1]:55992->[::1]:14567
beam.smp  51015 emqx   39u  IPv6 0xea2092701c017069      0t0  UDP [::1]:64686->[::1]:14567
```

如果你对 emqtt-bench 感兴趣，可以查看更多命令行帮助：

```
./emqtt_bench pub –help 

./emqtt_bench conn –help 

./emqtt_bench --help
```

## 结语

以上就是 MQTT over QUIC 的初步体验，可见从 API 和管理层面，客户端库以及 EMQX 能够做到与 MQTT 一致的体验，仅替换传输层以充分利用 QUIC 特性，这极大方便了开发者的使用以及 MQTT over QUIC 的普及。

随着对 MQTT over QUIC 在实际场景中的深入使用，用户也将能感受到其所具备的更高级的拥塞控制、连接平滑迁移、端到端加密、减少握手延迟等优势特性。在后续的推送中，我们也将对这些特性背后的技术原理以及最佳实践进行详细解读，敬请关注。


<section class="promotion">
    <div>
        现在试用 EMQX 5.0
    </div>
    <a href="https://www.emqx.com/zh/try?product=broker" class="button is-gradient px-5">立即下载 →</a>
</section>
