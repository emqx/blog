## 引言：多种防护机制保障物联网安全

全球物联网发展至今，网络环境日益庞大和复杂，物联网系统与服务的安全性面临着更加严峻的挑战。同时，各企业物联网业务的快速扩张，也要求底层的基础设施服务具有极高的稳定性与可靠性。

作为全球领先的物联网 MQTT 消息服务器，[EMQX](https://www.emqx.com/zh/products/emqx) 针对物联网安全拥有完整的解决方案，通过开箱即用的功能、符合行业和国家安全及质量标准的设计、针对企业安全场景需求的电信级产品架构和独有安全技术，助力用户构建安全健壮的物联网平台与系统。

本文将对 EMQX 5.0 所采用的各类安全保障机制与功能进行详细介绍，帮助用户了解 EMQX 如何保障物联网安全。

## SSL/TLS 体系保障通信安全

作为消息中间件，保证通信的安全性是最基本也是最核心的问题。传统的 TCP 通信因为使用明文通信，信息的安全性很难得到保证，面临以下风险：

- **窃听：** 信息以明文传播，攻击者可以直接获取敏感信息
- **篡改：** 攻击者截获信道后，可以随意篡改通信内容
- **伪造：** 同上，攻击者可能会将伪造的数据隐藏在真实的数据之中，危害更加隐蔽
- **冒充：** 攻击者假冒身份，与另一方进行通信

SSL/TLS 的出现很好的解决了通信中的风险问题，其以非对称加密技术为主干，混合了不同模式的加密方式，既保证了通信中消息都以密文传输，避免了被窃听的风险，同时也通过签名防止了消息被篡改。

EMQX 提供了丰富和完善的 SSL/TLS 支持，包括：单向、双向、X.509 证书、负载均衡 SSL、TLS-PSK 等多种认证方式，用户可以根据自己的实际场景选择合适的方式进行接入。通过 SSL/TLS 技术，EMQX 能够确保客户端数据传输、集群节点间通信、企业系统集成的数据传输安全。

EMQX 还支持将国密算法用于传输过程加密。国密 SSL 在提供更高安全性能的情况下，能够保持较低的资源开销和更快的传输速度。EMQ 提供了基于国密算法的传输加密认证集成方案，可应用于车联网、金融银行、教育、通信、国防工业等各类重要领域的物联网信息系统中。详情请见[《国密在车联网安全认证场景中的应用》](https://www.emqx.com/zh/blog/application-of-gmsm-in-internet-of-vehicles-security-authentication-scenario)。

### SSL/TLS 介绍

TLS/SSL 协议下的通讯过程分为两部分。

第一部分是握手协议，握手协议的目的是鉴别对方身份并建立一个安全的通讯通道。握手完成之后双方会协商出接下来使用的密码套件和会话密钥。

第二部分是 record 协议，record 和其他数据传输协议非常类似，会携带内容类型、版本、长度和荷载等信息，不同的是它所携带的信息是已加密的。

下图展示了 TLS/SSL 握手协议的过程，从客户端的 "hello" 一直到服务器的 "finished" 完成握手。

![SSL/TLS](https://assets.emqx.com/images/b3f36d9b8b02bd2e05980983bc3c44c8.png)

### 自签名证书单向认证配置

数字证书体系当中除了通讯双方，还有一个颁发证书的受信第三方 CA，一个真正受外界信任的证书需要到证书服务提供商进行购买。

而在内部通信时，可以使用自签名的证书。而在大多数场景下，单向认证的安全性是足够可靠的，且部署更加方便。在 EMQX 5.0 中使用自签名证书配置客户端 SSL/TLS 进行单向认证连接的步骤如下：

#### 证书准备

为自签名的 CA 证书准备一份私钥。

```
openssl genrsa -out ca.key 2048
```

通过这份私钥来生成一份 CA 证书。

```
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.pem
```

有了 CA 证书后，我们需要通过该证书对服务器/域名进行认证，同样先准备服务器私钥。

```
openssl genrsa -out emqx.key 2048
```

然后准备一份证书请求配置，用于生成证书请求文件。

```
[req]
default_bits = 2048
distinguished_name = req_distinguished_name
req_extensions = req_ext
x509_extensions = v3_req
prompt = no
[req_distinguished_name]
countryName = CN
stateOrProvinceName = Zhejiang
localityName = Hangzhou
organizationName = EMQX
commonName = CA
[req_ext]
subjectAltName = @alt_names
[v3_req]
subjectAltName = @alt_names
[alt_names]
IP.1 = 127.0.0.1
```

生成请求文件。

```
openssl req -new -key ./emqx.key -config openssl.cnf -out emqx.csr
```

最后通过之前生成的 CA 私钥、证书和该请求文件，对我们的服务器进行签名。

```
openssl x509 -req -in ./emqx.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out emqx.pem -days 3650 -sha256 -extensions v3_req -extfile openssl.cnf
```

#### 配置 EMQX

将生成好的 emqx.key、emqx.pem、ca.pem 拷贝到 EMQX 的 etc/certs 目录内，然后将 emqx.conf 中的 ssl 配置修改如下：

```
listeners.ssl.default {
  bind = "0.0.0.0:8883"
  max_connections = 512000
  ssl_options {
    keyfile = "etc/certs/emqx.key"
    certfile = "etc/certs/emqx.pem"
    cacertfile = "etc/certs/ca.pem"
  }
}
```

#### 使用 MQTTX CLI 测试

启动 EMQX，然后使用 [MQTTX CLI](https://mqttx.app/zh/cli) 进行连接测试：

```
# 使用服务器证书中的地址和端口进行连接
mqttx-cli conn -l mqtts -h 127.0.0.1 -p 8883 --ca ca.pem
# Connected
# 使用非法的地址进行连接
mqttx-cli conn -l mqtts -h 0.0.0.0 -p 8883 --ca ca.pem
# Error [ERR_TLS_CERT_ALTNAME_INVALID]: Hostname/IP does not match certificate's altnames: IP: 0.0.0.0 is not in the cert's list: 127.0.0.1
```

在这个演示中，客户端通过 CA 证书对服务器的证书进行验证，只有服务器证书合法可靠的情况下，双方才会建立加密通信信道，保证了通信的安全性。 

如果需要更高的安全性，确保客户端和服务器都是可信的，建议使用可靠的 CA 机构对客户端和服务器都部署证书，通信时进行双向认证，详情可以参考 [EMQX 启用双向 SSL/TLS 安全连接](https://www.emqx.com/zh/blog/enable-two-way-ssl-for-emqx)

## 认证授权

通信安全只是整个系统安全保障中的第一步。大多数情况下，一个能够通过双向认证的受信客户端，并不一定满足登录条件，即使满足登录条件，某些场景下可能也需要对其行为进行限制。

针对这些复杂的认证和授权需求，EMQX 提供了易于使用和部署的、开箱即用的解决方案。特别是在最新发布的 [EMQX 5.0](https://www.emqx.com/zh/blog/emqx-v-5-0-released) 中，内置实现了客户端认证授权功能：用户通过简单配置，无需编写代码即可对接各类数据源与认证服务，实现各个级别与各类场景下的安全配置，以更高的开发效率获得更安全的保障。

详细内容请见：[《灵活多样认证授权，零开发投入保障 IoT 安全》](https://www.emqx.com/zh/blog/securing-the-iot)

## 过载保护

在 EMQX 4.x 中，出于系统稳定性的考虑，当某个会话的负载达到了设置的阈值后，EMQX 会主动踢掉该会话。这部分功能在 5.0 版本中得到了延续和加强。

用户如果希望修改强制关闭的策略，可以在 emqx.conf 中增加如下配置:

```
force_shutdown {
  enable = true
  max_message_queue_len = 1000 # 会话进程消息队列的最大长度
  max_heap_size = "32MB" # 会话进程的最大堆内存大小
}
```

另外在 EMQX 5.0 中，我们引入了过载保护的概念，当 EMQX 判断系统处于高负载时，会通过关闭部分功能(具体见下面的配置示例)的方式，来维持服务的整体可靠性。

过载保护功能默认关闭，用户如果需要可以在 emqx.conf 中添加如下配置：

```
overload_protection {
  enable = true
  backoff_delay = 10 # 过载时，不重要的任务将会被延迟 10s 处理
  backoff_gc = true # 过载时，允许跳过强制 GC
  backoff_hibernation = true # 过载时，允许跳过休眠
  backoff_new_conn = true # 过载时，停止接收新的连接
}
```

## 速率控制

EMQX 5.0 引入了一套精度更高的、全新的分层速率控制系统，分别支持从节点、监听器、连接三个层级 来控制资源的消耗速度，能够确保系统按照用户预期的负载运行。

### 连接层级

连接级的速率限制针对的是单个连接，假设需要限制通过 1883 端口接入的每个会话的消息流入速度为每秒 100 条， 则只需要在 emqx.conf 中将 1883 端口配置修改如下:

```
listeners.tcp.default {
  bind = "0.0.0.0:1883"
  max_connections = 1024000
  limiter.client.message_in {
    rate = "100/s"
    capacity = 100
  }
}
```

### 监听器级

监听器级针对的是通过某个端口接入的所有会话的总和速率限制，比如希望所有通过 1883 端口接入的会话， 在每秒产生的消息输入总和不超过 100 条，则可以将配置修改如下：

```
listeners.tcp.default {
  bind = "0.0.0.0:1883"
  max_connections = 1024000
  limiter.message_in {
    rate = "100/s"
    capacity = 100
  }
}
```

### 节点级

节点级控制的是当前节点上的资源消耗速度，假如希望限制当前节点每秒流入的消息数量不超过 100 条，则 可以在 emqx.conf 中加入如下配置：

```
limiter.message_in.rate = "100/s"
```

> 注：因为节点级影响范围最广，目前的设计比较保守，只会影响到设置了速率限制的监听器，如果监听器上没有速率相关设置，则不受该配置影响。

## 黑名单系统

在某些情况下，一些客户端可能因为网络或者认证问题，出现不断重复的 “***登录-断开-重连***” 这种模式的异常行为。对此 EMQX 提供了简单的异常登录防御，支持自动封禁这些被检测到短时间内频繁登录的客户端，并且在一段时间内拒绝这些客户端的登录，以避免此类客户端过多占用服务器资源而影响其他客户端的正常使用。

此功能默认关闭，用户可以在 emqx.conf 配置文件中添加如下配置进行开启:

```
flapping_detect {
  enable = true
  # 客户端最大离线次数
  max_count = 15
  # 检测的时间范围
  window_time = "1m"
  # 封禁的时长
  ban_time = "5m"
}
```

## 不停机热更新/升级

得益于 Erlang/OTP 的原生热加载支持，以及 EMQX 设计良好的热更新流程，在大多数情况下，EMQX 都可以做到无缝、平滑、不停机、不暂停业务的实时热更新，在保证系统安全的修复 Bug 的同时，也确保了服务的稳定性和可靠性。

## 结语

本文简单介绍了 EMQX 内部保障通信、系统运行等功能的安全基础组件，这些组件不仅设计优良，还具有足够的深度和延展性，为用户打造可靠、可信、安全且健壮的物联网系统奠定了良好的基础。

未来 EMQX 依然会持续关注物网络安全问题，从实际应用场景出发，不断优化和增强各个安全组件，为物连网生态发展提供有力的安全保障。


<section class="promotion">
    <div>
        现在试用 EMQX 5.0
    </div>
    <a href="https://www.emqx.com/zh/try?product=broker" class="button is-gradient px-5">立即下载 →</a>
</section>
