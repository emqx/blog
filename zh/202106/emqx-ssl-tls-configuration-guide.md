## 概述

EMQX 提供了非常完整的 SSL/TLS 能力支持，但由于文档中提及甚少，给用户在 EMQX 中配置和使用 SSL/TLS 带来了不少困难。本指南着重于客户端连接，优先解答常见的 EMQX SSL/TLS 配置问题，以帮助用户快速上手 TLS。后续 EMQX 团队也将在官网文档中不断补齐 SSL/TLS 的相关使用配置指南。

以下是本指南此次涵盖的主题：

- 使用 SSL/TLS 的两种方式
- 如何在 EMQX 中启用 SSL/TLS
- 什么是对端验证
- 获取证书
- 单、双向认证的配置使用

## 使用 SSL/TLS 连接的两种方式

对于客户端的 SSL/TLS 连接，通常有以下两种方式：

- 客户端直接与 EMQX 建立 SSL/TLS 连接。
- 使用代理或负载均衡（例如 [HAproxy](http://www.haproxy.org/)）对客户端连接进行 [TLS 终结](https://en.wikipedia.org/wiki/TLS_termination_proxy)。

两种方式各有利弊，本指南将重点介绍第一种方式。

## 如何在 EMQX 中启用 SSL/TLS

如果客户端需要直接与 EMQX 建立 SSL/TLS 连接，那么需要修改 EMQX 中 SSL/TLS 相关的配置项，通常包括监听端口、CA 证书文件、服务器证书文件等。

以下是与 SSL/TLS 相关的基本配置项：

| 配置项                                              | 描述                                                         |
| --------------------------------------------------- | ------------------------------------------------------------ |
| `listener.ssl.<Listener Name>`                      | SSL/TLS 连接的监听端口。                                     |
| `listener.ssl.<Listener Name>.cacertfile`           | CA 捆绑包文件。                                              |
| `listener.ssl.<Listener Name>.certfile`             | 服务器证书文件。                                             |
| `listener.ssl.<Listener Name>.keyfile`              | 服务器私钥文件。                                             |
| `listener.ssl.<Listener Name>.verify`               | 是否开启对端验证。                                           |
| `listener.ssl.<Listener Name>.fail_if_no_peer_cert` | 设置为 `true` 时，如果客户端无法提供证书，则 SSL/TLS 连接将被拒绝，等于强制开启双向认证。 |
| `listener.ssl.<Listener Name>.ciphers`              | 服务端支持的加密套件。                                       |
| `listener.ssl.<Listener Name>.depth`                | 证书链中对端证书与 CA 证书之间允许存在的中间证书的最大数量。即如果 `depth` 配置为 0，则对端证书必须直接由根 CA 签发。默认为 10。 |
| `listener.ssl.<Listener Name>.key_password`         | 服务器私钥文件密码。                                         |

EMQX 随安装包提供了一组默认的 SSL/TLS 证书，并作为默认配置生效，但它们应当仅用于测试验证，用户应当在生产环境中换用可靠 CA 签发的证书。

通过注释 `listener.ssl.<Listener Name>` 这个配置项可以快速禁用 SSL/TLS 监听器。相应地，也可以禁用 TCP 监听器来使得 EMQX 只接受 SSL/TLS 连接。

通过 EMQX 提供的 CLI 命令可以验证 SSL/TLS 监听器是否正确运行。执行 `./emqx_ctl listeners`，如果 SSL/TLS 监听器正在运行，那么命令输出将包含以下内容（监听器名称、监听端口等内容视具体配置内容而定）：

```
...
mqtt:ssl:external
  listen_on       : 0.0.0.0:8883
  acceptors       : 16
  max_conns       : 102400
  current_conn    : 0
  shutdown_count  : []
...
```

## 什么是对端验证？

要了解什么是对端验证，我们首先要知道什么是证书链。

最简单的证书链是指用户证书直接由根 CA 签发。但通常出于安全性考虑，会先由根 CA 签发一个中间 CA，然后由这个中间 CA 来直接签发用户证书或者继续签发中间 CA，最终形成一个包含用户证书、中间 CA、根 CA 的证书链。

我们验证用户证书是否可信，其实就是验证签发该用户证书的根 CA 是否可信。而如果存在中间 CA，就需要通过中间 CA 一路追溯到根 CA，中间 CA 缺失、过期、被吊销，或者根 CA 不被信任，都会导致验证失败，这一系列操作被称为对端验证。

通常验证方只会存储受信任的根 CA，因此要完成对端验证，需要对端将用户证书和证书链中的所有中间 CA 都发送给验证方。注意，请勿发送根 CA，它不会对通过验证提供任何帮助，发送根 CA 只会增加握手时的消耗。

为了方便调试，大部分 SSL 客户端工具或客户端库，都提供了对端验证的开关选项，甚至默认关闭。

以单向认证为例，服务端将在握手阶段向客户端发送服务端证书，如果客户端没有开启对端验证，那么即便服务端证书存在问题，例如服务端证书不是由受信任的证书颁发机构所签发，SSL/TLS 连接也能正常建立，这意味着当前连接仅仅是加密了通信数据，而不能保证当前通信的服务端的身份合法，这就为 [中间人攻击](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) 提供了可乘之机。

所以通常我们建议在生产环境中开启对端验证，甚至是通信双方都开启此验证以获得最高等级的安全性。

客户端和服务端在开启对端验证后的行为有所不同。启用对端验证后，客户端通常还需要检查它们连接的服务器的主机名是否与服务端证书中的两个字段的其中之一相匹配：[SAN（Subject Alternative Names）](https://www.digicert.com/faq/subject-alternative-name.htm) 或 CN（Common Name）。

在某些情况下，客户端启用对端验证时还需要额外指定 [SNI（Server Name Indication）](https://zh.wikipedia.org/wiki/%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%90%8D%E7%A7%B0%E6%8C%87%E7%A4%BA) 字段。例如服务端要在同一 IP 地址上托管多个独立站点，每个站点都有自己的 SSL/TLS 证书，那么就需要客户端通过 SNI 来指定要连接的主机名，以便服务端返回正确的证书。

而如果服务端启用了对端验证，那么它会在握手阶段向客户端发送 CertificateRequest 消息以请求证书，然后对客户端发来的证书进行认证路径验证，这其实就是我们常说的双向认证。

## 获取证书

通常获取证书有以下两种方式：

1. 自签名，即自己签发根 CA。但自签名证书存在较多的安全隐患，通常我们建议仅用于测试验证。
2. 从证书颁发机构获取证书，免费证书可以向 [Let's Encrypt](https://letsencrypt.org/zh-cn/) 等证书颁发机构申请，收费证书则可以向 [DigiCert](https://www.digicert.com/) 等证书颁发机构申请。目前国内像华为云、腾讯云等云厂商基本也都联合知名 CA 推出了 SSL/TLS 证书服务，也可以申请和签发免费证书。对于企业级用户，一般建议申请收费的 OV 及以上类型的证书，以获取更高等级的安全保护。

以腾讯云为例，申请免费证书后将其下载到本地，解压后你将看到 `Apache`、`IIS`、`Nginx`、`Tomcat` 四个目录和一个 CSR 文件。CSR 文件是证书签名请求文件，在创建证书时使用，因此配置 SSL 服务时不需要关心此文件。`Apache` 这几个目录下都是我们申请得到的证书文件，只是证书格式有所不同，适用于不同类型的 Web 服务器。

`Apache` 目录下的 `1_root_bundle.crt` 是一个 CA 捆绑文件，里面通常包含了根 CA 与用户证书的之间的所有中间 CA 证书，`2_<Your Domain Name>.crt` 就是证书文件，而 `3_<Your Domain Name>.key` 就是私钥文件。这些也是我们最常用的证书文件格式。

`Nginx` 目录下的文件与 `Apache` 差别不大，`1_<Your Domain Name>_bundle.crt` 其实就是服务端证书与中间 CA 捆绑后的文件。

`IIS` 和 `Tomcat` 目录下两个后缀名为 `.jks` 和 `.pfx` 的文件都是二进制格式，它们同时包含了证书和私钥，`keystorePass.txt` 中是相应的提取密码。

### 获取根 CA

由于下载得到的证书中不包含根 CA，为了完成对端验证，需要自行下载相应的根 CA。这里我们使用 [ssl_chain.sh](https://kdecherf.com/blog/2015/04/10/show-the-certificate-chain-of-a-local-x509-file/) 来查看本地证书的认证链，脚本内容如下：

```bash
#!/bin/bash

chain_pem="${1}"

if [[ ! -f "${chain_pem}" ]]; then
    echo "Usage: $0 BASE64_CERTIFICATE_CHAIN_FILE" >&2
    exit 1
fi

if ! openssl x509 -in "${chain_pem}" -noout 2>/dev/null ; then
    echo "${chain_pem} is not a certificate" >&2
    exit 1
fi

awk -F'\n' '
        BEGIN {
            showcert = "openssl x509 -noout -subject -issuer"
        }

        /-----BEGIN CERTIFICATE-----/ {
            printf "%2d: ", ind
        }

        {
            printf $0"\n" | showcert
        }

        /-----END CERTIFICATE-----/ {
            close(showcert)
            ind ++
        }
    ' "${chain_pem}"

echo
openssl verify -untrusted "${chain_pem}" "${chain_pem}"
```

以下是 `1_root_bundle.crt` CA 捆绑文件的输出：

```
$ ./ssl_chain.sh 1_root_bundle.crt
 0: subject= /C=CN/O=TrustAsia Technologies, Inc./OU=Domain Validated SSL/CN=TrustAsia TLS RSA CA
issuer= /C=US/O=DigiCert Inc/OU=www.digicert.com/CN=DigiCert Global Root CA

1_root_bundle.crt: OK
```

这意味着 `TrustAsia TLS RSA CA` 这个中间 CA 的签发证书是一个由 DigiCert 颁发的根 CA。现在我们只需要去 DigiCert 的官网上搜索并下载 `DigiCert Global Root CA` 这个根 CA 即可，下载地址：[DigiCert Trusted Root Authority Certificates](https://www.digicert.com/kb/digicert-root-certificates.htm)。

现在，我们来验证一下这个根 CA 是否真的是我们想要的，这里我们借助 `openssl` 的 `verify` 命令来验证证书链，执行以下命令，：

```
$ awk '{print $0}' 1_root_bundle.crt DigiCertGlobalRootCA.crt.pem > all_ca.crt
$ openssl verify -CAfile all_ca.crt 2_zhouzb.club.crt
2_zhouzb.club.crt: OK
```

或

```
$ openssl verify -CAfile DigiCertGlobalRootCA.crt.pem -untrusted 1_root_bundle.crt 2_zhouzb.club.crt
```

zhouzb.club 是我申请证书时使用的域名。如果返回 `ok`，就意味着证书链验证成功。

>相比腾讯云，阿里云在这方面考虑得稍微周到一些，下载证书时，也提供了根 CA 的下载链接。

## 单、双向认证的配置使用

为了便于演示，我们会使用 [EMQX Broker](https://github.com/emqx/emqx) 作为服务端，在 EMQX Broker 的控制台中使用 Erlang 的 `ssl:connect/3` 函数作为客户端。以下实例中我们将会用到两个版本的 EMQX Broker，分别是 [4.2.11](https://github.com/emqx/emqx/releases/tag/v4.2.11) 和 [4.3-rc.5](https://github.com/emqx/emqx/releases/tag/v4.3-rc.5)。使用两个版本的原因是 EMQX Broker 从 4.3 开始将 OTP 版本升级到了 23，而 OTP 23 中 `certfile` 和 `cacertfile` 参数的行为发生了一些改变。

在 OTP 23，或者说 EMQX Broker 的 4.3 之前，`certfile` 指定的文件中只能包含用户证书，`cacertfile` 指定的文件中需要包含中间 CA 和根 CA，握手过程中中间 CA 会跟随用户证书一并发送给对端，用于对端构建与验证证书链。根 CA 不会被发送，它将被用于验证对端的证书链。因此我们也可以得知，如果我们的用户证书由根 CA 直接签发，并且也不需要验证对端的证书链时，可以不用指定 `cacertfile` 参数。

而从 OTP 23，或者说 EMQX Broker 的 4.3 开始，`certfile` 指定的文件中可以包含用户证书和中间 CA，它们应该用户证书在前、中间 CA 在后，以正确的顺序排列，并在握手阶段被发送给对端，用于对端构建与验证证书链。`cacertfile` 可以只用来指定受信任的根 CA。

`ssl:connect(Host, Port, TLSOptions)` 这个 TLS 客户端连接函数中 `Host` 指定主机名，`Port` 指定端口，`TLSOptions` 则用于指定证书等 TLS 选项，与服务端类似，常用选项如下：

| 选项                     | 描述               |
| ------------------------ | ------------------ |
| `cacertfile`             | CA 捆绑包文件。    |
| `certfile`               | 客户端证书文件。   |
| `keyfile`                | 客户端私钥文件。   |
| `verify`                 | 是否开启对端验证。 |
| `server_name_indication` | 服务器名称指示。   |

### 单向认证

EMQX Broker 4.2.11 配置如下：

```
# 监听端口我们使用默认的 8883
listener.ssl.external = 8883
# 配置为我们申请下来的证书
listener.ssl.external.keyfile = etc/certs/zhouzb.club/Apache/3_zhouzb.club.key
listener.ssl.external.certfile = etc/certs/zhouzb.club/Apache/2_zhouzb.club.crt
listener.ssl.external.cacertfile = etc/certs/zhouzb.club/Apache/1_root_bundle.crt
# 不开启对端验证
listener.ssl.external.verify = verify_none
```

EMQX Broker 4.3-rc.5 配置如下：

```
# 监听端口我们使用默认的 8883
listener.ssl.external = 8883
# 配置为我们申请下来的证书
listener.ssl.external.keyfile = etc/certs/zhouzb.club/Nginx/2_zhouzb.club.key
listener.ssl.external.certfile = etc/certs/zhouzb.club/Nginx/1_zhouzb.club_bundle.crt
# 不开启对端验证
listener.ssl.external.verify = verify_none
```

启动 EMQX Broker 并进入控制台：

```shell
$ ./emqx console
```

使用 `ssl:connect/3` 函数连接：

```erlang
ssl:connect("127.0.0.1", 8883, [{cacertfile, "etc/certs/zhouzb.club/DigiCertGlobalRootCA.crt.pem"},
                                {verify, verify_peer},
                                {server_name_indication, "zhouzb.club"}]).
```

这里我们指定了受信任的根 CA，并且将 `verify` 指定为 `verify_peer` 以开启对端验证。前面提到过客户端进行对端验证时还会检查连接的主机名是否与服务端证书中的两个字段的其中之一相匹配：[SAN（Subject Alternative Names）](https://www.digicert.com/faq/subject-alternative-name.htm) 或 CN（Common Name）。我申请的这个证书中的 CN 字段的值为 `zhouz.club`，而我在连接时指定的主机名是 `127.0.0.1`，因此需要使用 `server_name_indication` 选项来指定 SNI。当然也可以直接将它设为 `disable` 来关闭这项检查。

这里我将 `server_name_indication` 设置为 `zhouzb.club`，当然设置为 `www.zhouzb.club` 也是一样的，因为我申请的这个证书包含了 SAN 字段，可以支持多个域名。我们可以通过以下命令查看证书中的 `Subject Alternative name` 字段内容：

```shell
$ openssl x509 -in 2_zhouzb.club.crt -noout -text
...
    X509v3 Subject Alternative Name:
        DNS:zhouzb.club, DNS:www.zhouzb.club
...
```

当你输入上面的连接函数并回车之后，看到了类似 `{ok, ...}` 的返回并且没有看到任何错误日志，说明证书验证成功，连接成功。

接下来我们来看一下无法构建完整的证书链时，开启对端验证会发生什么。我们基于 EMQX Broker 4.2.11 对配置进行一些调整，不再提供中间CA：

```
listener.ssl.external = 8883
listener.ssl.external.keyfile = etc/certs/zhouzb.club/Apache/3_zhouzb.club.key
listener.ssl.external.certfile = etc/certs/zhouzb.club/Apache/2_zhouzb.club.crt
# 将指定中间 CA 的 cacertfile 注释掉
# listener.ssl.external.cacertfile = etc/certs/zhouzb.club/Apache/1_root_bundle.crt
listener.ssl.external.verify = verify_none
```

停止 EMQX Broker，使用 `./emqx console` 再次启动并进入控制台，输入与上面一样的连接函数并回车，我们将看到以下返回：

```
{error,{tls_alert,{unknown_ca,"TLS client: In state wait_cert_cr at ssl_handshake.erl:1887 generated CLIENT ALERT: Fatal - Unknown CA\n"}}}
```

因为现在 EMQX Broker 在握手时只会发送服务端证书了，客户端无法只使用服务端证书来构建出完整的认证路径，因此服务端证书验证失败。

> 通常出现 “Unknown CA” 或类似内容，都是因为无法构建完整的认证链（中间 CA 缺失有缺失）或者签发对端证书的根 CA 不是来自受信任的 CA 机构。

那么在中间 CA 有缺失的情况下客户端不进行对端验证的话会发生什么呢？我想大家应该都知道此时连接将成功建立。不过，我们还是实际连接一下来验证这个想法。保持上文的 EMQX Broker 环境不变，我们将在 `ssl:connect/3` 函数中将 `verify` 设为 `verify_none`：

```erlang
ssl:connect("127.0.0.1", 8883, [{cacertfile, "etc/certs/zhouzb.club/DigiCertGlobalRootCA.crt.pem"},
                                {verify, verify_none},
                                {server_name_indication, "zhouzb.club"}]).
```

不出意料地，函数运行后返回了 `{ok, ...}`，连接成功建立。

### 双向认证

现在，我们要在服务端也开启对端验证，但是还缺少客户端证书。通常情况下，建议创建一个私有的根 CA，也就是以自签发的方式来签发客户端证书，具体签发方式可以参考 [这里](https://jamielinux.com/docs/openssl-certificate-authority/index.html)。

为了尽快进入正题，这里我将继续使用服务端证书来充当客户端证书。

EMQX Broker 4.2.11 配置如下：

```
# 监听端口我们使用默认的 8883
listener.ssl.external = 8883
# 配置为我们申请下来的证书
listener.ssl.external.keyfile = etc/certs/zhouzb.club/Apache/3_zhouzb.club.key
listener.ssl.external.certfile = etc/certs/zhouzb.club/Apache/2_zhouzb.club.crt
# 指定包含了用于验证客户端证书的受信任的根 CA 与用于构建服务端证书链的中间 CA 的 CA 捆绑包文件
listener.ssl.external.cacertfile = etc/certs/zhouzb.club/ca_bundle.crt
# 开启对端验证，并强制要求客户端提供证书
listener.ssl.external.verify = verify_peer
listener.ssl.external.fail_if_no_peer_cert = true
```

`ca_bundle.crt` 是包含了 `DigiCertGlobalRootCA.crt.pem` 和 `1_root_bundle.crt` 的 CA 捆绑包文件。合并命令如下：

```shell
$ awk '{print $0}' Apache/1_root_bundle.crt DigiCertGlobalRootCA.crt.pem > ca_bundle.crt
```

接下来，相同的步骤，启动 EMQX Broker 并进入控制台，使用 `ssl:connect/3` 函数进行连接。唯一不同的是，现在我们需要在连接时指定客户端证书了：

```erlang
ssl:connect("127.0.0.1", 8883, [{cacertfile, "etc/certs/zhouzb.club/ca_bundle.crt"},
                                {certfile, "etc/certs/zhouzb.club/Apache/2_zhouzb.club.crt"},
                                {keyfile, "etc/certs/zhouzb.club/Apache/3_zhouzb.club.key"},
                                {verify, verify_peer},
                                {server_name_indication, "zhouzb.club"}]).
```

再次连接成功。

如果我们稍微作出一些调整，例如客户端连接时 `cacertfile` 指定的文件中不包含中间 CA：

```erlang
ssl:connect("127.0.0.1", 8883, [{cacertfile, "etc/certs/zhouzb.club/DigiCertGlobalRootCA.crt.pem"},
                                {certfile, "etc/certs/zhouzb.club/Apache/2_zhouzb.club.crt"},
                                {keyfile, "etc/certs/zhouzb.club/Apache/3_zhouzb.club.key"},
                                {verify, verify_peer},
                                {server_name_indication, "zhouzb.club"}]).
```

也许你会认为，服务端会因为无法构建出完整的客户端证书链而拒绝连接。但事实上，这一次我们还是成功地建立了连接。这是因为服务端 `cacertfile` 中的中间 CA 不仅会发给客户端用于客户端构建服务端证书的证书链，也会在收到客户端证书时被用于构建客户端证书的证书链。而恰好我们在服务端和客户端使用的是同一个用户证书，拥有相同的中间 CA。所以即便客户端在握手时没有提供中间 CA，服务端也能使用本地的中间 CA 来构建并验证客户端证书的认证路径。

> 我暂时并未弄清楚 Erlang/OTP 这么设计的原因，但建议通常情况下还是发送完整的中间 CA。

回到正题，在 EMQX Broker 4.3-rc.5 中我们可以这样配置双向认证，我认为与之前相比，这种配置方式看起来会更加友好：

```
# 监听端口我们使用默认的 8883
listener.ssl.external = 8883
# 配置为我们申请下来的证书
listener.ssl.external.keyfile = etc/certs/zhouzb.club/Nginx/2_zhouzb.club.key
listener.ssl.external.certfile = etc/certs/zhouzb.club/Nginx/1_zhouzb.club_bundle.crt
# 指定受信任的根 CA，用于验证客户端证书
listener.ssl.external.cacertfile = etc/certs/zhouzb.club/DigiCertGlobalRootCA.crt.pem
# 开启对端验证，并强制要求客户端提供证书
listener.ssl.external.verify = verify_peer
listener.ssl.external.fail_if_no_peer_cert = true
```

同样，我们在连接时也使用新的方式：

```erlang
ssl:connect("127.0.0.1", 8883, [{cacertfile, "etc/certs/zhouzb.club/DigiCertGlobalRootCA.crt.pem"},
                                {certfile, "etc/certs/zhouzb.club/Nginx/1_zhouzb.club_bundle.crt"},
                                {keyfile, "etc/certs/zhouzb.club/Nginx/2_zhouzb.club.key"},
                                {verify, verify_peer},
                                {server_name_indication, "zhouzb.club"}]).
```

连接成功。

### 客户端使用不同根 CA 签发的证书

为了尽快进入正题，这里我使用 EMQX Broker 自带的使用自签发的根 CA 签发的客户端证书 `etc/certs/client-cert.pem` 来进行演示。

EMQX Broker 4.3-rc.5 配置修改如下：

```
# 监听端口我们使用默认的 8883
listener.ssl.external = 8883
# 配置为我们申请下来的证书
listener.ssl.external.keyfile = etc/certs/zhouzb.club/Nginx/2_zhouzb.club.key
listener.ssl.external.certfile = etc/certs/zhouzb.club/Nginx/1_zhouzb.club_bundle.crt
# 指定受信任的根 CA，用于验证客户端证书
listener.ssl.external.cacertfile = etc/certs/zhouzb.club/multi_ca.crt
# 开启对端验证，并强制要求客户端提供证书
listener.ssl.external.verify = verify_peer
listener.ssl.external.fail_if_no_peer_cert = true
```

`multi_ca.crt` 包含了 `DigiCertGlobalRootCA.crt.pem` 和 `etc/certs/cacert.pem`  两个根 CA，合并命令如下：

```shell
$ awk '{print $0}' ../cacert.pem DigiCertGlobalRootCA.crt.pem > multi_ca.crt
```

配置修改完成后，启动 EMQX Broker 并进入控制台，依次使用以下两个连接函数来进行连接，它们使用了由不同根 CA 签发的客户端证书：

```erlang
ssl:connect("127.0.0.1", 8883, [{cacertfile, "etc/certs/zhouzb.club/DigiCertGlobalRootCA.crt.pem"},
                                {certfile, "etc/certs/client-cert.pem"},
                                {keyfile, "etc/certs/client-key.pem"},
                                {verify, verify_peer},
                                {server_name_indication, "zhouzb.club"}]).		
```

```erlang
ssl:connect("127.0.0.1", 8883, [{cacertfile, "etc/certs/zhouzb.club/DigiCertGlobalRootCA.crt.pem"},
                                {certfile, "etc/certs/zhouzb.club/Nginx/1_zhouzb.club_bundle.crt"},
                                {keyfile, "etc/certs/zhouzb.club/Nginx/2_zhouzb.club.key"},
                                {verify, verify_peer},
                                {server_name_indication, "zhouzb.club"}]).
```

连接成功。

## 结语

以上，就是本次指南的全部内容，希望它能帮助你理解大部分场景下的 SSL/TLS 证书应该如何配置。加密套件、Key Usage 等进阶内容，我将会在以后的文章中详细地介绍。


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">无须绑定信用卡</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
