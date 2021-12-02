作为基于现代密码学公钥算法的安全协议，TLS/SSL 能在计算机通讯网络上保证传输安全，EMQ X 内置对 TLS/SSL 的支持，包括支持单/双向认证、X.509 证书、负载均衡 SSL 等多种安全认证。你可以为 EMQ X 支持的所有协议启用 SSL/TLS，也可以将 EMQ X 提供的 HTTP API 配置为使用 TLS。本文将介绍如何在 EMQ X 中为 [MQTT](https://www.emqx.com/zh/mqtt) 启用 TLS。



## SSL/TLS 带来的安全优势

- **强认证。** 用 TLS 建立连接的时候，通讯双方可以互相检查对方的身份。在实践中，很常见的一种身份检查方式是检查对方持有的 X.509 数字证书。这样的数字证书通常是由一个受信机构颁发的，不可伪造。

- **保证机密性**。TLS 通讯的每次会话都会由会话密钥加密，会话密钥由通讯双方协商产生。任何第三方都无法知晓通讯内容。即使一次会话的密钥泄露，并不影响其他会话的安全性。

- **完整性。** 加密通讯中的数据很难被篡改而不被发现。



## SSL/TLS 协议

TLS/SSL 协议下的通讯过程分为两部分，第一部分是握手协议。握手协议的目的是鉴别对方身份并建立一个安全的通讯通道。握手完成之后双方会协商出接下来使用的密码套件和会话密钥；第二部分是 record 协议，record 和其他数据传输协议非常类似，会携带内容类型，版本，长度和荷载等信息，不同的是它所携带的信息是加密了的。

下面的图片描述了 TLS/SSL 握手协议的过程，从客户端的 "hello" 一直到服务器的 "finished" 完成握手。有兴趣的同学可以找更详细的资料看。对这个过程不了解也并不影响我们在 [EMQ X](https://www.emqx.com/zh/products/emqx) 中启用这个功能。

![whatisssl.gif](https://static.emqx.net/images/935a55bd15dbb8a207f72e7fc37f9986.gif)



## SSL/TLS 证书准备

通常来说，我们会需要数字证书来保证 TLS 通讯的强认证。数字证书的使用本身是一个三方协议，除了通讯双方，还有一个颁发证书的受信第三方，有时候这个受信第三方就是一个 CA。和 CA 的通讯，一般是以预先发行证书的方式进行的。也就是在开始 TLS 通讯的时候，我们需要至少有 2 个证书，一个 CA 的，一个 EMQ X 的，EMQ X 的证书由 CA 颁发，并用 CA 的证书验证。

获得一个真正受外界信任的证书需要到证书服务提供商进行购买。在实验室环境，我们也可以用自己生成的证书来模拟这个过程。下面我们分别以这两种方式来说明 EMQ X 服务器的 SSL/TLS 启用过程。

> **注意：** 购买证书与自签名证书的配置，读者根据自身情况只需选择其中一种进行测试。

### 购买证书

如果有购买证书的话，就不需要自签名证书。

为方便 EMQ X 配置，请将购买的证书文件重命名为 `emqx.crt`，证书密钥重命名为 `emqx.key`。

### 自签名证书

在这里，我们假设您的系统已经安装了 OpenSSL。使用 OpenSSL 附带的工具集就可以生成我们需要的证书了。

首先，我们需要一个自签名的 CA 证书。生成这个证书需要有一个私钥为它签名，可以执行以下命令来生成私钥：

```shell
openssl genrsa -out ca.key 2048
```

这个命令将生成一个密钥长度为 2048 的密钥并保存在 `ca.key` 中。有了这个密钥，就可以用它来生成 EMQ X 的根证书了：

```shell
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.pem
```

查看 CA 证书信息（可选）：

```bash
openssl x509 -in ca.pem -noout -text
```

根证书是整个信任链的起点，如果一个证书的每一级签发者向上一直到根证书都是可信的，那个我们就可以认为这个证书也是可信的。有了这个根证书，我们就可以用它来给其他实体签发实体证书了。

实体（在这里指的是 EMQ X）也需要一个自己的私钥对来保证它对自己证书的控制权。生成这个密钥的过程和上面类似：

```shell
openssl genrsa -out emqx.key 2048
```

新建 `openssl.cnf` 文件，

- req_distinguished_name ：根据情况进行修改，
- alt_names： `BROKER_ADDRESS` 修改为 EMQ X 服务器实际的 IP 或 DNS 地址，例如：IP.1 = 127.0.0.1，或 DNS.1 = broker.xxx.com

```conf
[req]
default_bits  = 2048
distinguished_name = req_distinguished_name
req_extensions = req_ext
x509_extensions = v3_req
prompt = no
[req_distinguished_name]
countryName = CN
stateOrProvinceName = Zhejiang
localityName = Hangzhou
organizationName = EMQX
commonName = Server certificate
[req_ext]
subjectAltName = @alt_names
[v3_req]
subjectAltName = @alt_names
[alt_names]
IP.1 = BROKER_ADDRESS
DNS.1 = BROKER_ADDRESS
```

然后以这个密钥和配置签发一个证书请求：

```shell
openssl req -new -key ./emqx.key -config openssl.cnf -out emqx.csr
```

然后以根证书来签发 EMQ X 的实体证书：

```shell
openssl x509 -req -in ./emqx.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out emqx.pem -days 3650 -sha256 -extensions v3_req -extfile openssl.cnf
```

查看 EMQ X 实体证书（可选）：

```bash
openssl x509 -in emqx.pem -noout -text
```

验证 EMQ X 实体证书，确定证书是否正确:

```
$ openssl verify -CAfile ca.pem emqx.pem
emqx.pem: OK
```

准备好证书后，我们就可以启用 EMQ X 的 TLS/SSL 功能了。



## SSL/TLS 启用及验证

**在 EMQ X 中 `mqtt:ssl` 的默认监听端口为 8883。**

### 购买证书方式

#### EMQ X 配置

将前文重命名后的 `emqx.key` 文件及 `emqx.crt` 文件拷贝到 EMQ X 的 `etc/certs/` 目录下，并参考如下配置修改 `emqx.conf`：

```shell
## listener.ssl.$name is the IP address and port that the MQTT/SSL
## Value: IP:Port | Port
listener.ssl.external = 8883

## Path to the file containing the user's private PEM-encoded key.
## Value: File
listener.ssl.external.keyfile = etc/certs/emqx.key

## 注意：如果 emqx.crt 是证书链，请确保第一个证书是服务器的证书，而不是 CA 证书。
## Path to a file containing the user certificate.
## Value: File
listener.ssl.external.certfile = etc/certs/emqx.crt
```

#### MQTT 连接测试

当配置完成并重启 EMQ X 后，我们使用 [MQTT 客户端工具 - MQTT X](https://mqttx.app/zh)（该工具跨平台且支持 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5)），来验证 TLS 服务是否正常运行。


> MQTT X 版本要求：v1.3.2 及以上版本



- 参照下图在 MQTT X 中创建 `MQTT 客户端`（Host 输入框里的 `mqttx.app` 需替换为实际的域名）

![mqttxconfigserver.png](https://static.emqx.net/images/2e5bdd705694388d29cc80bf087ef92f.png)

  **注意**：在 `Certificate` 一栏只需选择 `CA signed server` 即可，使用购买证书在进行单向认证连接时不需要携带任何证书文件（CA 文件也不需要携带）。

- 点击  `Connect`  按钮，连接成功后，如果能正常执行 MQTT 发布/订阅 操作，则购买证书的 SSL 单向认证配置成功。

![mqttxconnectedserver.png](https://static.emqx.net/images/05a4ec449fb19394ef11bf258310e05a.png)

### 自签名证书方式

#### EMQ X 配置

将前文中通过 OpenSSL 工具生成的 `emqx.pem`、`emqx.key` 及 `ca.pem` 文件拷贝到 EMQ X 的 `etc/certs/` 目录下，并参考如下配置修改 `emqx.conf`：

```shell
## listener.ssl.$name is the IP address and port that the MQTT/SSL
## Value: IP:Port | Port
listener.ssl.external = 8883

## Path to the file containing the user's private PEM-encoded key.
## Value: File
listener.ssl.external.keyfile = etc/certs/emqx.key

## 注意：如果 emqx.pem 是证书链，请确保第一个证书是服务器的证书，而不是 CA 证书。
## Path to a file containing the user certificate.
## Value: File
listener.ssl.external.certfile = etc/certs/emqx.pem

## 注意：ca.pem 用于保存服务器的中间 CA 证书和根 CA 证书。可以附加其他受信任的 CA，用来进行客户端证书验证。
## Path to the file containing PEM-encoded CA certificates. The CA certificates
## Value: File
listener.ssl.external.cacertfile = etc/certs/ca.pem
```

#### MQTT 连接测试（OpenSSL）

- 使用 OpenSSL 作为 Server 与 Client

  ```
  openssl s_server -accept 2009 -key emqx.key -cert emqx.pem
  ```

  ```
  $ openssl s_client -connect localhost:2009 -CAfile ca.pem -showcerts
  
  Verify return code: 0 (ok)
  ```

- 使用 OpenSSL 作为 Client，EMQ X 作为 Server

  启动 EMQ X 并将日志等级改为 Debug。

  ```
  ./bin/emqx start
  ./bin/emqx_ctl log set-level debug
  ```

  使用 openssl s_client 连接 EMQ X 并发送一个 Client ID 为 "a" 的 MQTT Connect 报文。

  ```
  $ echo -en "\x10\x0d\x00\x04MQTT\x04\x00\x00\x00\x00\x01a" | openssl s_client -connect localhost:8883 -CAfile ca.pem -showcerts
  
  Verify return code: 0 (ok)
  ```

  如果你在 `emqx/log/erlang.log.1` 中看到以下日志，说明 SSL 认证成功。

  ```
  2020-11-26 17:39:13.933 [debug] 127.0.0.1:51348 [MQTT] RECV CONNECT(Q0, R0, D0, ClientId=a, ProtoName=MQTT, ProtoVsn=4, CleanStart=false, KeepAlive=0, Username=undefined, Password=undefined)
  ```

#### MQTT 连接测试（MQTT X）

当配置完成并重启 EMQ X 后，我们使用 [MQTT 客户端工具 - MQTT X](https://mqttx.app/zh)（该工具跨平台且支持 [MQTT 5.0](https://www.emqx.com/zh/mqtt/mqtt5)），来验证 TLS 服务是否正常运行。

> MQTT X 版本要求：v1.3.2 及以上版本

- 参照下图在 MQTT X 中创建 `MQTT 客户端`（Host 输入框里的 `127.0.0.1` 需替换为实际的 EMQ X 服务器 IP）

![1594612437782.jpg](https://static.emqx.net/images/9c966931c2c83165ba181aa4c704b8e1.jpg)
  此时 `Certificate` 一栏需要选择 `Self signed` ，并携带自签名证书中生成的 `ca.pem` 文件。

- 点击  `Connect`  按钮，连接成功后，如果能正常执行 MQTT 发布/订阅 操作，则自签名证书的 SSL 单向认证配置成功。


 ![mqttxconnected.png](https://static.emqx.net/images/a1d926637ed5adfbf375494da46929af.png)



### EMQ X Dashboard 验证

最后，打开 EMQ X 的 Dashboard 在 Listeners 页面可以看到在 8883 端口上有一个 `mqtt:ssl` 连接。

![emqxdashboard.png](https://static.emqx.net/images/ad2311957fce8a7a95db7f8527fb7565.png)

至此，我们成功的完成了 EMQ X 服务器的 SSL/TLS 配置及单向认证连接测试。EMQ X SSL/TLS 双向认证配置文档请关注我们的后续文章。
