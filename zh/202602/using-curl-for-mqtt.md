## 引言

Curl 是一款广泛使用的命令行数据传输工具。自 2020 年起，curl 已原生支持 MQTT 协议。随着 curl 8.19.0+ 的到来（预计 2026 年 3 月初发布），开发者可以在终端中通过 MQTTS（基于 TLS 的 MQTT）进行加密通信，保障物联网数据传输的安全。

这意味着开发者无需安装专用的客户端库或图形化工具，直接利用命令行即可完成 MQTT 工作流的测试、脚本编写和自动化任务。

**本文将向您展示如何仅使用 curl 工具连接 MQTT broker、发布消息及订阅主题。**

## 为什么选择 curl 进行 MQTT 操作？

- **零依赖**：无需安装 Python、Node.js 或专用 MQTT 库，仅需 curl 即可操作。
- **兼容性：**已预装在大多数 Linux/macOS 系统中；并可轻松添加到 Windows 及容器环境。
- **脚本化支持：**可以轻松集成到 shell 脚本中，适用于原型设计和测试场景。
- **TLS 加密支持（8.19.0+）：** 通过 `mqtts://` 建立安全连接，满足生产级测试需求。
- **语法直观且友好：**如果您了解 curl 的 HTTP 操作方式，那么 MQTT 的使用将同样得心应手。

## 前期准备

### curl 版本要求

| **功能特性**          | **最低版本要求** | **发布日期**         |
| --------------------- | ---------------- | -------------------- |
| 基础 MQTT (mqtt://)   | 7.70.0           | 2020 年 4 月         |
| 加密 MQTTS (mqtts://) | 8.19.0           | 2026 年 3 月（预计） |

你可以通过以下命令检查当前版本：

```
curl --version
```

在输出的 `Protocols` 行中确认是否包含 `mqtt`（以及 8.19.0+ 版本的 `mqtts`）。

```shell
curl 8.19.0-DEV (aarch64-apple-darwin25.2.0) libcurl/8.19.0-DEV OpenSSL/3.6.0 zlib/1.2.12 brotli/1.2.0 zstd/1.5.7 AppleIDN libssh2/1.11.1 nghttp2/1.68.0 ngtcp2/1.20.0 nghttp3/1.15.0 librtmp/2.3 mit-krb5/1.7-prerelease OpenLDAP/2.4.28/Apple
Release-Date: [unreleased]
Protocols: dict file ftp ftps gopher gophers http https imap imaps ipfs ipns ldap ldaps mqtt mqtts pop3 pop3s rtmp rtsp scp sftp smb smbs smtp smtps telnet tftp ws wss
Features: alt-svc AppleSecTrust AsynchDNS brotli GSS-API HSTS HTTP2 HTTP3 HTTPS-proxy IDN IPv6 Kerberos Largefile libz NTLM SPNEGO SSL threadsafe TLS-SRP UnixSockets zstd
```

> 注意：如果版本过低，请通过软件包管理器升级或从 [curl.se/download](https://curl.se/download.html) 下载。macOS 用户建议使用 `brew install curl` 获取最新版本。

### MQTT Broker 设置

进行测试前，你需要一个可连接的 Broker。本文推荐使用最具扩展性的 MQTT 平台 EMQX：

1. **公共测试服务器：** `broker.emqx.io`（TCP 端口：1883，TLS 端口：8883）。
2. **EMQX Serverless：**适合需要身份验证、专用资源和企业级特性的生产环境测试。

## 理解 curl 的 MQTT URL 方案

curl 使用基于 URL 的语法进行 MQTT 操作：

```
mqtt[s]://[user:password@]broker[:port]/topic
```

| **组件**        | **说明**                                          | **示例**                 |
| :-------------- | :------------------------------------------------ | :----------------------- |
| `mqtt://`       | 非加密连接（默认端口 1883）                       | `mqtt://broker.emqx.io`  |
| `mqtts://`      | TLS 加密连接（默认端口 8883，curl 版本 ≥ 8.19.0） | `mqtts://broker.emqx.io` |
| `user:password` | 可选的身份验证凭据                                | `admin:secret@`          |
| `broker`        | 代理服务器名称                                    | `broker.emqx.io`         |
| `:port`         | 可选端口覆盖                                      | `:1883`，`:8883`         |
| `/topic`        | 用于发布/订阅的 MQTT 主题                         | `/sensor/temperature`    |

端口号为可选项，curl 将自动使用标准默认端口（1883 用于 `mqtt://`，8883 用于 `mqtts://`）。如果您的代理服务使用非标准端口，您可手动指定端口进行覆盖。

### curl 的 MQTT 输出格式

订阅消息时，curl 会以二进制格式输出数据：

```
[2 bytes: topic length (big-endian)] [topic string] [payload]
```

例如，主题「curl/test」上的一条消息「hello」将显示为：

```
00 09 c u r l / t e s t h e l l o
└─┬─┘ └───────┬───────┘ └───┬───┘
  │           │             │
  │           │             └── payload (no length prefix)
  │           └── topic: "curl/test" (9 bytes)
  └── topic length: 9 (0x0009)
```

原始输出格式如下（主题与负载内容直接连接显示）：

```
curl/testhello
```

关于如何解析这些数据并将其转换为易于阅读的格式，请参阅下文中的「解析 MQTT 消息」部分。

## 第一步：订阅 MQTT 主题

执行订阅命令后，curl 会保持连接状态，并将接收到的消息实时推送到终端。

### 基础订阅（非加密）

```shell
# Subscribe to the "curl/test" topic on the public EMQX broker
curl -N mqtt://broker.emqx.io/curl/test --output messages.bin
```

使用 `-N` 参数可禁用输出缓冲，确保消息在到达时能立即显示。若不添加此参数，curl 将默认缓冲输出内容，直到缓冲区填满或连接关闭时才会显示信息。

### 通过 MQTTS 实现安全订阅（适用于 curl ≥8.19.0 版本）

```shell
# Subscribe over TLS
curl -N mqtts://broker.emqx.io/curl/test --output messages.bin
```

### 需要身份验证的订阅

当您需要连接到要求身份验证的 Broker（例如 EMQX Serverless）时：

```
# Replace with your actual credentials curl -N -u "your-username:your-password" mqtts://your-broker.emqxsl.com/curl/test --output messages.bin
```

### 解析 MQTT 消息：生成易读输出

若要以直观易读的格式显示消息，可以将 curl 的输出结果通过管道（pipe）传输给解析脚本处理。

**Bash 单行命令解析方案：**

```shell
curl -sN mqtt://broker.emqx.io/curl/test | \
  while IFS= read -r -d $'\0' d; \
    do \
      [ -n "$d" ] && \
        l=$(printf "%d" "'${d:0:1}") && \
        echo "[${d:1:$l}] ${d:1+$l}"; \
    done
```

该命令以空字节（对于长度小于 256 字符的主题，其 2 字节主题长度的首字节）作为分隔符，随后从第二个字节中提取主题的具体长度，并打印 `[topic] payload` 中的每条消息。

**保存到文件并查看：**

```shell
# Save raw output to file (Ctrl+C to stop)
curl -sN mqtt://broker.emqx.io/curl/test > messages.bin

# View with hexdump to see the structure
hexdump -C messages.bin
```

**作为可复用的 Shell 函数：**

```
mqtt_subscribe() {
  curl -sN "$1" | while IFS= read -r -d $'\0' d; do
    [ -n "$d" ] && l=$(printf "%d" "'${d:0:1}") && echo "[${d:1:$l}] ${d:1+$l}"
  done
}

# Usage
mqtt_subscribe "mqtt://broker.emqx.io/curl/test"
```

> 注意：如需用于生产环境或处理更复杂的解析需求，建议使用 [MQTTX CLI](https://mqttx.app/zh/cli)。它能提供更规范的输出格式，并完整支持 MQTT 5.0 协议。

## 第二步：发布消息到 MQTT 主题

若需发布消息，请使用 curl 的 `-d`（data）标志并附带消息负载。

### 基本发布（未加密）

```shell
# Publish "Hello from curl" to the "curl/test" topic
curl -v -d "Hello from curl" mqtt://broker.emqx.io/curl/test
```

### 通过 MQTTS 实现安全发布（curl ≥8.19.0）

```shell
# Publish over TLS
curl -v -d "Secure message from curl" mqtts://broker.emqx.io/curl/test
```

### 发布 JSON 格式负载

在物联网场景中，JSON 是一种常用的传感器数据传输格式：

```json
# Publish a JSON temperature reading
curl -v -d '{"sensor_id": "temp-001", "value": 23.5, "unit": "celsius"}' \
  mqtt://broker.emqx.io/sensors/temperature
```

### 需要身份验证的发布操作

```shell
curl -v -u "your-username:your-password" \
  -d '{"status": "online", "timestamp": 1706000000}' \
  mqtts://your-broker.emqxsl.com/devices/status
```

> 注意：如需测试完整的发布/订阅流程，请同时打开两个终端窗口。在一个终端中运行订阅命令（步骤一），在另一个终端中发布消息（步骤二）。

## 相关 curl 选项

| **选项**       | **说明**                        | **示例**                     |
| :------------- | :------------------------------ | :--------------------------- |
| `-N`           | 禁用输出缓冲（订阅需要此功能）  | `-N`                         |
| `-d "payload"` | 要发布的消息数据                | `-d "sensor reading"`        |
| `-u user:pass` | 代理服务的身份验证凭证          | `-u admin:secret`            |
| `-s`           | 静默模式（隐藏进度信息）        | `-s`                         |
| `-v`           | 详细输出（显示 MQTT 握手过程）  | `-v`                         |
| `--output -`   | 输出至标准输出（适用于订阅）    | `--output -`                 |
| `--cacert`     | 用于 TLS 验证的 CA 证书         | `--cacert /path/to/ca.crt`   |
| `--cert`       | mTLS 客户端证书                 | `--cert /path/to/client.crt` |
| `--key`        | mTLS 客户端私钥                 | `--key /path/to/client.key`  |
| `-k`           | 跳过 TLS 证书验证（仅供测试！） | `-k`                         |

### TLS 证书验证（curl ≥8.19.0）

针对需要使用自定义证书进行验证的生产级 MQTTS 连接：

```shell
# With CA certificate verification
curl --cacert /etc/ssl/certs/emqx-ca.crt \
  -d "Verified secure message" \
  mqtts://your-broker.emqxsl.com/secure/topic

# With mutual TLS (mTLS) client authentication
curl --cacert /etc/ssl/certs/ca.crt \
  --cert /etc/ssl/certs/client.crt \
  --key /etc/ssl/private/client.key \
  -d "mTLS authenticated message" \
  mqtts://your-broker.emqxsl.com/secure/topic
```

## 应用场景：何时使用 curl 进行 MQTT 通信？

### **Broker 连通性测试**

使用 curl 的详细输出模式验证 MQTT broker 的可访问性，该模式能清晰展示 DNS 解析是否生效、TCP 连接是否成功建立等关键信息：

```shell
curl -v mqtt://broker.emqx.io/test
```

**以下是连接成功时的示例输出：**

```shell
curl -v mqtt://broker.emqx.io:1883/curl/test
* Host broker.emqx.io:1883 was resolved.
* IPv6: (none)
* IPv4: 34.243.217.54, 35.172.255.228, 44.232.241.40
*   Trying 34.243.217.54:1883...
* Connected to broker.emqx.io (34.243.217.54) port 1883
* Using client id 'curlblZBtS6c'
> MQTT<
       curlblZBtS6cmqtt_doing: state [0]
```

通过上述输出，你可以验证网络连通性和 DNS 解析情况。但请注意，curl 目前仅支持 QoS 0（最多交付一次），因此即使 curl 显示发布成功，也不代表订阅者一定收到了该消息。

### 用于物联网原型开发的 Shell 脚本

模拟温度传感器每 5 秒发布一次读数：

```shell
#!/bin/bash
# simulate-sensor.sh

BROKER="mqtt://broker.emqx.io"
TOPIC="sensors/room1/temperature"

while true; do
  # Generate random temperature between 20-30°C
  TEMP=$(awk -v min=20 -v max=30 'BEGIN{srand(); print min+rand()*(max-min)}')
  PAYLOAD="{\"temperature\": $TEMP, \"timestamp\": $(date +%s)}"
  
  curl -s -d "$PAYLOAD" "$BROKER/$TOPIC"
  echo "Published: $PAYLOAD"
  
  sleep 5
done
```

这种方法适用于原型开发阶段，以及对订阅端应用进行快速压力测试。如果要用于可靠性要求极高、必须保证消息送达的生产环境业务，建议选用支持 QoS 1 或 QoS 2 的客户端。

## curl 在 MQTT 应用中的局限性

虽然 curl 非常适用于快速测试和脚本编写，但在复杂场景下，用户仍需注意以下限制：

| **局限性**   | **说明**                                                   | **替代方案**                                            |
| :----------- | :--------------------------------------------------------- | :------------------------------------------------------ |
| 二进制输出   | 订阅输出为原始二进制数据（主题长度前缀 + 主题 + 有效载荷） | 通过解析脚本进行管道传输或使用 MQTTX CLI                |
| 仅支持 QoS 0 | curl 仅支持 QoS 0（最多交付一次）                          | 使用 [MQTTX CLI](https://mqttx.app/zh/cli) 实现 QoS 1/2 |
| 不支持通配符 | 无法订阅通配符主题（`+`，`#`）                             | 使用专用的 MQTT 客户端                                  |
| 单主题限制   | 每个命令调用仅支持一个主题                                 | 通过编写脚本调用多个 curl                               |
| 无持久会话   | 无法跨连接维护会话状态                                     | 使用客户端库来管理有状态应用程序                        |

对于需要高级 MQTT 功能的用户，建议考虑使用 [MQTTX CLI](https://mqttx.app/zh/cli)。这是由 EMQ 开发的一款专为 MQTT 设计的命令行工具，完整支持 MQTT 5.0、多种 QoS 等级、主题通配符以及其他专业特性。

## 验证 curl 的 MQTT 支持

如果 MQTT 命令执行失败，请检查当前安装的 curl 版本是否已编译并启用了 MQTT 协议支持：

```shell
# Check if mqtt is listed in protocols
curl --version | grep -i protocols

# Test MQTT support explicitly
curl -V 2>&1 | grep -q mqtt && echo "MQTT supported" || echo "MQTT NOT supported"
```

如果 `curl` 显示不支持 MQTT，您可能需要采取以下措施：

- 升级至更新的 curl 版本。
- 安装已启用 MQTT 支持的 curl 编译版本（部分精简发行版可能未包含此功能）。
- 从源代码编译 curl 并启用 `--enable-mqtt` 选项。

## 结语

curl 对 MQTT 协议的支持，使这款熟悉的命令行工具转型为强大的物联网测试与脚本编写利器。随着 curl 8.19.0 版本对 MQTTS 的引入，用户现在可以使用这款早已习惯的 HTTP API 工具，安全地与 MQTT broker 进行交互。

**核心要点：**

- 测试场景可使用 `mqtt://`，安全连接请选用 `mqtts://`（需 curl ≥8.19.0）。
- curl 在连通性测试、原型验证和快速临时消息传递场景中表现卓越。
- 请注意：curl 仅支持 QoS 0；如需消息可靠传输，请使用 MQTTX CLI 或专业客户端库。

## 相关资源

- [MQTT服务器（MQTT Broker）：工作原理与快速入门指南](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison) 

- [MQTTX CLI: 强大而易用的 MQTT 命令行客户端](https://mqttx.app/zh/cli) 

- [MQTT 协议快速入门 2025：基础知识和实用教程](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 

- [使用 SSL/TLS 加强 MQTT 通信安全](https://www.emqx.com/zh/blog/fortifying-mqtt-communication-security-with-ssl-tls) 

- [curl + MQTT = true](https://daniel.haxx.se/blog/2020/04/14/curl-mqtt-true/) 

- [Now with MQTTS](https://daniel.haxx.se/blog/2026/01/19/now-with-mqtts/) 



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
