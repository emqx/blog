春分时节，万物复苏，[NanoMQ](https://nanomq.io/zh) 项目又如期为大家献上了最新的 0.17 版本。这一版本主要对 2 个重要功能进行了升级：MQTT over QUIC 的双向认证和 DDS 协议转换代理的序列化代码自动生成。另外还新增了 QUIC 传输层的配置参数，增加了 Retain 消息的持久化，以及发布了 NanoSDK 0.9 版本等诸多更新。

## QUIC 双向认证 & 新增配置参数 

自从 1994 年提出了 SSL 协议的原始规范以来，TLS 协议也经过了多次版本的更新。最新推出的 TLS 1.3 有望成为有史以来最安全但也最复杂的 TLS 协议。相较于 TLS 1/1.1/1.2，1.3 版本具备更快的连接协商速度，新的密钥协商机制 PSK 和更安全的加密哈希算法。 

QUIC 在功能层面等价于 TCP+TLS, 并且已采用最新的 TLS 1.3 代替其原有加密协议(QUIC Crypto)。QUIC 协议默认基于 TLS 1.3 完成数据加密连接，且依赖其实现了0-RTT（1-RTT）快速重连握手功能。

![MQTT 3.1.1/5.0 over QUIC](https://assets.emqx.com/images/6a5e87cb25a61f8df11119b60f42403a.png)

<center>MQTT 3.1.1/5.0 over QUIC</center>

当使用 TLS 进行数据加密传输时，如需要验证客户端合法性，经常会使用到双向认证。在之前的 NanoMQ 版本中， MQTT over QUIC 桥接默认只使用单向认证。从 0.17 版本开始用户能够通过配置开启 QUIC（TLS 1.3）的双向认证。

### 如何使用 QUIC 的双向认证

首先确认自己使用的 NanoMQ 版本已开启了 QUIC 选项，目前使用双向认证只需在配置中设置对应的客户端证书和私钥等文件路径，注意这部分配置无论是使用传统的 TCP 模式还是 QUIC 模式都一样有效：

旧配置文件格式：

```
bridge.mqtt.emqx.tls.enable=false
bridge.mqtt.emqx.tls.key_password=yourpass
bridge.mqtt.emqx.tls.keyfile=/etc/certs/key.pem
bridge.mqtt.emqx.tls.certfile=/etc/certs/cert.pem
bridge.mqtt.emqx.tls.cacertfile=/etc/certs/cacert.pem
```

HOCON 格式:

```
## 在 bridge 段落中的 connector 部分

bridges.mqtt {
	nodes = [
		{
			name = emqx
			enable = true
			connector {
				......
				conn_properties = {
					......
				}
				# # Ssl config ##
				# # Ssl config is also valid when working in MQTT over QUIC mode ##
				ssl {
					enable = false
					key_password = "yourpass"
					keyfile = "/etc/certs/key.pem"
					certfile = "/etc/certs/cert.pem"
					cacertfile = "/etc/certs/cacert.pem"
				}
			} 
```

NanoMQ 的 MQTT over TCP 部分采用的是 MbedTLS 库进行加解密，与标准的 TCP 连接不同，QUIC 部分采用的是 MsQUIC 子模块项目内置的 OpenSSL API。OpenSSL 和 MbedTLS 两个目前最流行的 SSL 库在 NanoMQ 项目中可以同时兼容运行。

目前 NanoMQ 的 MQTT over QUIC 桥接功能暂时不支持 Windows 环境下运行。由于平台兼容性问题，在 Windows 环境中需要替换使用 schannel 来进行 TLS/SSL 加解密。计划在后续的版本中完成 Winodws 环境适配。

### 新增 QUIC 传输层配置参数

根据用户反馈，为了保持连接不断来克服一些极端弱网情况，新版本暴露了 2 个 QUIC 传输层参数供用户自行配置调优。

- `quic_initial_rtt`**：** 初始的 RTT（Round Trip Time） 预测值。QUIC 采用单向递增的 Packet Number 来标识数据包，即时是重传包也有独特的编号，不会引起重传的歧义性，这样采样 RTT 的测量更准确。QUIC 通过 ACK 记录的接收的数据报文和 ACK 报文之间的延迟来估算RTT，RTT 用于丢失检测和触发重传。这一值就是初始估计网络中的 RTT 情况，用户可以根据实际网络环境设置合理的 RTT 来保证连接不断。
- `quic_send_idleTimeout`**：**重置 QUIC 传输层拥塞控制检测的最大空闲时间。拥塞控制会修改内部发送的滑动窗口大小，此值影响 QUIC 传输层对于网络变动的敏感度和自动流控。

配置选项如下：

```
bridge.mqtt.emqx.quic_initial_rtt=60
bridge.mqtt.emqx.quic_send_idleTimeout=60
```

## IDL 序列化代码生成工具

此前我们提到需要用户自己根据 IDL 格式来开发转 JSON 的序列化/反序列化代码，未来将提供一个自动化的代码生成工具。为了方便 MQTT 用户能够简单快速上手 DDS Proxy 功能，3 月这一工具正式发布：NanoMQ 推出了 IDL 代码生成器功能：idl-serial-code-gen （[https://github.com/nanomq/idl-serial](https://github.com/nanomq/idl-serial)）。此工具能够根据用户的 DDS IDL 文件来自动生成 JSON 序列化和反序列化代码。

由于 DDS 协议为不可读不可直接分析的二进制流，为了提高系统的可互操作性，需要将 DDS 系统的数据在 NanoMQ 中进行必要的转换以供其他中间件如 eKuiper 分析使用。idl-serial-code-gen 工具可以自动生成代码来完成 IDL 结构体和 JSON 格式文本之间的互相转换。

目前 idl-serial-code-gen 工具支持以下 IDL 特性。

- Primitive types
- Structs
- String and string with template
- Sequence template
- Enums
- Part of [Annotations](https://cyclonedds.io/content/guides/supported-idl.html)

在上一版本的 NanoMQ DDS Proxy 中，默认所有主题都使用同一个 IDL 结构体定义，这限制了单实例能够转接的数据类型。新版本新增了 DDS 主题和 MQTT 主题的对应配置选项，供用户配置转发的 Topic 对应关系。

```
forward_rules = {
	  ## DDS to MQTT
    dds_to_mqtt = {
        from_dds = "MQTTCMD/topic1"
        to_mqtt = "DDS/topic1"
        struct_name = "remote_control_result_t"
    }
    ## MQTT to DDS
    mqtt_to_dds = {
        from_mqtt = "DDSCMD/topic1"
        to_dds = "MQTT/topic1"
        struct_name = "remote_control_req_t"
    }
}
```

同理 nanomq_cli 工具命令行启动时也需要指定结构体名称：启动DDS客户端订阅DDS主题 MQTT/topic1 并指定接收的结构体名称 remote_control_req_t。

```
$ ./nanomq_cli ddsproxy sub -t "MQTT/topic1" --struct "remote_control_req_t"
```

目前默认 DDS 和 MQTT 主题之间一一对应，不允许一个 MQTT 主题上转接多个 DDS 主题。

### 编译 IDL 代码生成器 idl-serial-code-gen

编译 `IDL` 代码生成器 `idl-serial`

```
$ git clone https://github.com/nanomq/idl-serial.git
$ cd idl-serial
$ mkdir build && cd build
$ cmake -G Ninja ..
$ ninja 
$ sudo ninja install
```

编译完成生成可执行文件 `idl-serial-code-gen`

### 生成 Json<->Struct 转换代码

使用 `idl` 文件 `dds_structs.idl` 生成 `C` 代码 `idl_convert.c` 和 `idl_convert.h`

```
## 生成C代码 idl_convert.c 和 idl_convert.h
$ ./idl-serial-code-gen  dds_structs.idl  idl_convert
```

### 编译NanoMQ与DDS Proxy

1. 将以上步骤中生成的代码文件 `idl_convert.c` 和 `idl_convert.h` 拷贝到 `nanomq_cli/dds2mqtt` 路径下
2. 通过 cmake 参数 `IDL_FILE_PATH` 指定 `idl` 文件路径 (不指定则默认为工程路径下的 `etc/idl/dds_type.idl`)

```
$ git clone https://github.com/nanomq/nanomq.git
$ cd nanomq
## 拷贝以上生成的文件到 nanomq_cli/dds2mqtt/路径下
$ cp {YOUR_PATH}/idl_convert.* nanomq_cli/dds2mqtt
$ mkdir build && cd build
$ cmake -G Ninja -DIDL_FILE_PATH={IDL_PATH} -DCMAKE_PREFIX_PATH={DDS_LIBRARY_PATH} -DBUILD_DDS_PROXY=ON ..
$ ninja 
$ sudo ninja install
```

目前虽然有了自动化代码生成工具，但 DDS Porxy 功能编译安装过程较为繁琐，对于不熟悉工程结构和 DDS 操作的用户来说比较困难。下一版本将通过 Cmake 来集成这一工具并自动化编译过程，无需再手动生成源码文件和拷贝文件到工程下。

## NanoSDK 0.9 版本发布

与 NanoMQ 0.17 一同发布的还有 NanoSDK 0.9 版本。这一版本将 NanoMQ 中创新的 MQTT over QUIC 多流连接功能和在桥接中使用的新的回调函数同步至 NanoSDK。NanoSDK 0.10 版本也在筹备开发中，将提供 MQTT5 over QUIC 协议支持和继续增加类 Paho 的使用方法。

## 其他修复和更新

NanoMQ 0.17 版本还有一些小功能更新：

1. **支持 Retain 消息持久化至 SQLite3**： 根据用户需求，为 NanoMQ 新增了，当开启 SQLite 的消息缓存和持久化功能时默认存储所有的 Retain 消息至 SQLite。
2. **MQTT5 桥接增加更多配置参数：** 为 MQTT5 桥接新增了遗愿消息相关的配置参数。

此外还有一些问题修复和优化：

1. 修复桥接连接中拒绝接受带有 Subscription Identifier 消息的问题。
2. 修复桥接连接接收到 Retain 消息时会造成数据类型不兼容而导致的协议错误断开。
3. 修正了 HTTP API `api/v4/clients` 中获取到的错误的会话保持状态。
4. 修改了 Broker 的行为：当客户端使用会话保持功能并断开连接时， 之前 Broker 希望能够复用此 Socket 等待客户端自动重连，而不会主动关闭。如今已修改为普通关闭操作。此功能的讨论：（[https://github.com/nanomq/nanomq/discussions/1108](https://github.com/nanomq/nanomq/discussions/1108)）
5. 在 NanoNNG 模块中更新了新的 `nng_mqtt_quic_open_conf` API 用于开启 QUIC 连接。
6. 优化 CMakeList 修复 OpenSSL 和 MbedTLS 库在编译阶段造成的不兼容问题。

## 即将到来

NanoMQ 项目目前的重点是提升 NanoSDK 的易用性和支持 MQTT5 over QUIC 桥接，并且将继续完善 DDS 协议代理功能和提供更多更丰富的文档和教程。原计划中的 SOME/IP 协议代理将推迟至下一个版本发布。



<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a>
</section>
