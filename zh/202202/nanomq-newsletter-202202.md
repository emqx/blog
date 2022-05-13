本月，在隆冬季节和春节假期 NanoMQ-NanoSDK 项目也没有放慢更新的步伐。新发布的 0.6.3 版本中，我们进一步完善了 [NanoMQ](https://nanomq.io/zh) 的命令行工具，为其增加了 TLS 端口支持，同时进一步优化重构了 NanoSDK。

## 命令行工具

[在上个月的 Newsletter 中](https://www.emqx.com/zh/blog/nanomq-newsletter-202201)我们预告了连接测试工具和压力测试工具。本月其中的连接测试工具已完成：

### Connection

```
Usage: nanomq conn { start | stop } <addr> [<opts>...]

<addr> must be one or more of:
  --url <url>                      The url for mqtt broker ('mqtt-tcp://host:port' or 'tls+mqtt-tcp://host:port')
                                   [default: mqtt-tcp://127.0.0.1:1883]

<opts> may be any of:
  -V, --version <version: 3|4|5>   The MQTT version used by the client [default: 4]
  -n, --parallel               The number of parallel for client [default: 1]
  -v, --verbose                 Enable verbose mode
  -u, --user <user>                The username for authentication
  -p, --password <password>        The password for authentication
  -k, --keepalive <keepalive>      A keep alive of the client (in seconds) [default: 60]
  -i, --interval <ms>              Interval of establishing connection (ms) [default: 10]
  -C, --count <num>                Num of client
  -q, --qos <qos>                  Quality of service for the corresponding topic [default: 0]
  -r, --retain                     The message will be retained [default: false]
  -c, --clean_session <true|false> Define a clean start for the connection [default: true]
  --will-qos <qos>                 Quality of service level for the will message [default: 0]
  --will-msg <message>             The payload of the will message
  --will-topic <topic>             The topic of the will message
  --will-retain                    Will message as retained message [default: false]
  -s, --secure                     Enable TLS/SSL mode
      --cacert <file>              CA certificates file path
      -E, --cert <file>            Certificate file path
      --key <file>                 Private key file path
      --keypass <key password>     Private key password
```

### Example

```
nanomq conn start --url "mqtt-tcp://broker.emqx.io:1883" -C 10000 -i 10 -k 60
```

使用 NanoMQ Conn 工具向 [EMQ](https://www.emqx.com/zh) 提供的[公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker) 的 msg 主题每 10ms 创建一个 MQTT 连接。当创建到 10000 个连接时停止。使用这一工具可以测试 MQTT Broker 的并发连接能力。

## 支持 TLS

安全问题一直是物联网应用必须考虑的重点。MQTT+TLS 是最广泛使用的链接加密方式。从 0.6.3 版本开始，NanoMQ 能够支持客户端通过 TCP+TLS 或 Websocket+TLS 端口接入，默认端口分别是 8883 和 8084。使用方法如下：

首先 NanoMQ 的 TLS 支持是默认关闭的，目前 0.6.0 的二进制安装包还未默认开启 TLS 功能。需要用户编译安装使用的时候通过-DNNG_ENABLE_TLS=ON选项打开。

之后可以通过命令行/配置文件/容器环境变量方式配置：

- Running broker with *TLS* via command line:

  ```
  nanomq broker start --url "tls+nmq-tcp://0.0.0.0:8883" [--cacert <path>] [-E, --cert <path>] [--key <path>] [--keypass <password>] [--verify] [--fail]
  ```

- Running broker with *TLS* via configuration file:

  ```
  ## tls config ##
  
  ## enable tls
  ## 
  ## Value: true | false
  tls.enable=false
  
  ## tls url
  ##
  ## Value: "nmq-tls://host:port"
  tls.url=nmq-tls://0.0.0.0:8883
  
  ## tls key password
  ## String containing the user's password. Only used if the private keyfile
  ## is password-protected.
  ##
  ## Value: String
  ## tls.key_password=yourpass
  
  ## tls keyfile
  ## Path to the file containing the user's private PEM-encoded key.
  ##
  ## Value: File
  tls.keyfile=/etc/certs/key.pem
  
  ## tls cert file
  ## Path to a file containing the user certificate.
  ##
  ## Value: File
  tls.certfile=/etc/certs/cert.pem
  
  ## tls ca cert file
  ## Path to the file containing PEM-encoded CA certificates. The CA certificates
  ## are used during server authentication and when building the client certificate chain.
  ##
  ## Value: File
  tls.cacertfile=/etc/certs/cacert.pem
  
  ## A server only does x509-path validation in mode verify_peer,
  ## as it then sends a certificate request to the client (this
  ## message is not sent if the verify option is verify_none).
  ## You can then also want to specify option fail_if_no_peer_cert.
  ##
  ## Value: true: verify_peer | false: verify_none
  tls.verify_peer=false
  
  ## Used together with {verify, verify_peer} by an SSL server. If set to true,
  ## the server fails if the client does not have a certificate to send, that is,
  ## sends an empty certificate.
  ##
  ## Value: true | false
  tls.fail_if_no_peer_cert=false
  
  ## websocket tls url
  ##
  ## Value: "nmq-wss://host:port/path"
  websocket.tls_url=nmq-wss://0.0.0.0:8084/mqtt
  ```

- Running Docker with *TLS* and configuring via ENV：

| Variable                        | Type    | Value                                                     |
| ------------------------------- | ------- | --------------------------------------------------------- |
| NANOMQ_TLS_ENABLE               | Boolean | 是否开启 TLS                                              |
| NANOMQ_TLS_URL                  | String  | TLS 的监听 URL：'nmq-tls://host:port'.                    |
| NANOMQ_TLS_CA_CERT_PATH         | String  | TLS 的服务端证书路径（PEM-encoded CA certificates）       |
| NANOMQ_TLS_CERT_PATH            | String  | TLS 的用户证书路径                                        |
| NANOMQ_TLS_KEY_PATH             | String  | 私有秘钥文件路径                                          |
| NANOMQ_TLS_KEY_PASSWORD         | String  | 用户指定的私有秘钥密码（如果指定使用）                    |
| NANOMQ_TLS_VERIFY_PEER          | Boolean | 是否校验对端身份（双向认证）                              |
| NANOMQ_TLS_FAIL_IF_NO_PEER_CERT | Boolean | 当对端未携带证书进行连接时，MQTT 服务是否失败（双向认证） |

使用 TLS 需要自行生成证书（Certificate Authority，CA）的认证和密钥，可以用 OpenSSL 工具生成 CA 证书，也可以使用 NanoMQ 自带的证书文件 (项目根目录/etc/certs)。

在此我们就不再介绍 TLS 背景知识和用法教程。如需更多相关知识，请参阅博客文章：[https://www.emqx.com/zh/blog/emqx-server-ssl-tls-secure-connection-configuration-guide](https://www.emqx.com/zh/blog/emqx-server-ssl-tls-secure-connection-configuration-guide) 。

## 共享订阅

共享订阅是 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5) 协议引入的新特性，但 [EMQX](https://www.emqx.io/zh) 在 [MQTT](https://www.emqx.com/zh/mqtt) 3.1.1 中也已经实现。这相当于是订阅端的[负载均衡](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-2-sticky-session-load-balancing)功能，主要目的是解决当消费能力不足时直接增加订阅节点，从而导致产生大量重复消息的问题。NanoMQ 也在 MQTT 3.1.1 中支持了共享订阅，但目前只支持 Round-robin 和 Random 的分发均衡方式。

## 移除 C++ 模块

之前 NanoMQ 是 C/C++混合项目。但为了达到边缘端的极致轻量级，在 0.6.0 版本我们移除了原先的 Nanolib 中的 C++ 模块，这能够大幅减少 NanoMQ 的安装包大小。

## Bug 修复

本月我们修复了以下 3 个重要 Bug：

1. 修复了当客户端使用会话保持功能时，session present field 没有正确设置的问题。
2. 修复了当客户端因为超时断开不会触发之前设置的遗愿消息（will msg）发布的问题。
3. 修复了 MQTT v5 和 MQTT v3.1&v3.1.1 客户端之间消息互通兼容的问题。


### URL 配置修改

另外，需要社区各位用户注意的是，相较于之前的版本还有一个对于 NanoMQ 使用习惯的改变。为了未来多协议转换的准备，从 0.6.3 版本开始，我们将原来的 MQTT Broker 默认 URL 格式从“broker+tcp:\\ip:port” 修改为 “nmq-tcp:\\ip:port”，原来的 URL 将留作他用。

## NanoSDK 重构

本月 NanoSDK 迎来了新的 0.3 版本。在这一版本中，我们根据 NNG 项目维护者 Garrett 的意见和性能测试数据重构了协议层，减少内存消耗并维持 QoS 消息的高吞吐高性能，同时修复了一些 Bug。目前我们正在将 NanoSDK 的更新合并到下一版本 NanoMQ 中。

另外，为了广大用户能够更便捷地找到 NanoSDK，我们已将仓库地址从原先的 NNG fork 转为一个独立仓库：[https://github.com/nanomq/NanoSDK](https://github.com/nanomq/NanoSDK) 。


<section class="promotion">
    <div>
        免费试用 NanoMQ
    </div>
    <a href="https://www.emqx.com/zh/try?product=nanomq" class="button is-gradient px-5">开始试用 →</a >
</section>
