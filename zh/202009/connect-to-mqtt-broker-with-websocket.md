近年来随着 Web 前端的快速发展，浏览器新特性层出不穷，越来越多的应用可以在浏览器端通过浏览器渲染引擎实现，Web 应用的即时通信方式 WebSocket 也因此得到了广泛的应用。

WebSocket 是一种在单个 TCP 连接上进行全双工通讯的协议。WebSocket 通信协议于2011年被 IETF 定为标准 RFC 6455，并由 RFC 7936 补充规范。WebSocket API 也被 W3C 定为标准。

WebSocket 使得客户端和服务器之间的数据交换变得更加简单，允许服务端主动向客户端推送数据。在 WebSocket API 中，浏览器和服务器只需要完成一次握手，两者之间就直接可以创建持久性的连接，并进行双向数据传输。 [^1]

[MQTT 协议第 6 章 ](https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html#_Toc398718127)详细约定了 MQTT 在 WebSocket [RFC6455] 连接上传输需要满足的条件，协议内容不在此详细赘述。



## 两款客户端比较

### Paho.mqtt.js

[Paho](https://www.eclipse.org/paho/) 是 Eclipse 的一个 MQTT 客户端项目，Paho JavaScript Client 是其中一个基于浏览器的库，它使用 WebSockets 连接到 MQTT 服务器。相较于另一个 JavaScript 连接库来说，其功能较少，不推荐使用。

### MQTT.js

[MQTT.js](https://github.com/mqttjs/MQTT.js) 是一个完全开源的 MQTT 协议的客户端库，使用 JavaScript 编写，可用于 Node.js 和浏览器。在 Node.js 端可以通过全局安装使用命令行连接，同时支持  MQTT/TCP、MQTT/TLS、MQTT/WebSocket 连接；值得一提的是 MQTT.js 还对[微信小程序](https://www.emqx.com/zh/blog/how-to-use-mqtt-in-wechat-miniprogram)有较好的支持。

本文将使用 MQTT.js 库进行 WebSocket 的连接讲解。



## 安装 MQTT.js

如果读者机器上装有 Node.js 运行环境，可直接使用 npm 命令安装 MQTT.js。

### 在当前目录安装

```shell
npm install mqtt --save
```

### CDN 引用

或免安装直接使用 CDN 地址

```html
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>

<script>
    // 将在全局初始化一个 mqtt 变量
    console.log(mqtt)
</script>
```



## 连接至 MQTT 服务器

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 物联网云平台](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

> EMQX 使用 8083 端口用于普通连接，8084 用于 SSL 上的 WebSocket 连接。

为了简单起见，让我们将订阅者和发布者放在同一个文件中：

```javascript
const clientId = 'mqttjs_' + Math.random().toString(16).substr(2, 8)

const host = 'ws://broker.emqx.io:8083/mqtt'

const options = {
  keepalive: 60,
  clientId: clientId,
  protocolId: 'MQTT',
  protocolVersion: 4,
  clean: true,
  reconnectPeriod: 1000,
  connectTimeout: 30 * 1000,
  will: {
    topic: 'WillMsg',
    payload: 'Connection Closed abnormally..!',
    qos: 0,
    retain: false
  },
}

console.log('Connecting mqtt client')
const client = mqtt.connect(host, options)

client.on('error', (err) => {
  console.log('Connection error: ', err)
  client.end()
})

client.on('reconnect', () => {
  console.log('Reconnecting...')
})
```

### 连接地址

上文示范的连接地址可以拆分为： `ws:` // `broker` . `emqx.io` : `8083` `/mqtt`

即 `协议` // `主机名` . `域名` : `端口` / `路径`

初学者容易出现以下几个错误：

- 连接地址没有指明协议：WebSocket 作为一种通信协议，其使用 `ws` (非加密)、`wss `(SSL 加密) 作为协议标识。MQTT.js 客户端支持多种协议，连接地址需指明协议类型；
- 连接地址没有指明端口：MQTT 并未对 WebSocket 接入端口做出规定，EMQX 上默认使用 `8083`  `8084` 分别作为非加密连接、加密连接端口。而 WebSocket 协议默认端口同 HTTP 保持一致 (80/443)，不填写端口则表明使用 WebSocket 的默认端口连接；而使用标准 MQTT 连接时则无需指定端口，如 MQTT.js 在 Node.js 端可以使用 `mqtt://localhost` 连接至标准 MQTT 1883 端口，当连接地址是 `mqtts://localhost` 则连接到 8884 端口；
- 连接地址无路径：MQTT-WebSoket 统一使用 `/path` 作为连接路径，连接时需指明，在 EMQX 上使用的路径为 `/mqtt`；
- 协议与端口不符：使用了 `wss` 连接却连接到 `8083` 端口；
- 在 HTTPS 下使用非加密的 WebSocket 连接： Google 等机构在推进 HTTPS 的同时也通过浏览器约束进行了安全限定，即 HTTPS 连接下浏览器会自动禁止使用非加密的 `ws` 协议发起连接请求；
- 证书与连接地址不符： 篇幅较长，详见下文 **EMQ 启用 SSL/TLS 加密连接**。

### 连接选项

上面代码中， `options` 是客户端连接选项，以下是主要参数说明，其余参数详见[https://www.npmjs.com/package/mqtt#connect](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.npmjs.com%2Fpackage%2Fmqtt%23connect)。

- keepalive：心跳时间，默认 60秒，设置 0 为禁用；
- clientId： 客户端 ID ，默认通过 `'mqttjs_' + Math.random().toString(16).substr(2, 8)` 随机生成；
- username：连接用户名（可选）；
- password：连接密码（可选）；
- clean：true，设置为 false 以在离线时接收 QoS 1 和 2 消息；
- reconnectPeriod：默认 1000 毫秒，两次重新连接之间的间隔，客户端 ID 重复、认证失败等客户端会重新连接；
- connectTimeout：默认 30 * 1000毫秒，收到 CONNACK 之前等待的时间，即连接超时时间；
- will：遗嘱消息，当客户端严重断开连接时，Broker 将自动发送的消息。 一般格式为：
  - topic：要发布的主题
  - payload：要发布的消息
  - qos：QoS
  - retain：保留标志

### 订阅/取消订阅

连接成功之后才能订阅，且订阅的主题必须符合 MQTT 订阅主题规则；

注意 JavaScript 的异步非阻塞特性，只有在 connect 事件后才能确保客户端已成功连接，或通过 `client.connected` 判断是否连接成功：

```javascript
client.on('connect', () => {
  console.log('Client connected:' + clientId)
  // Subscribe
  client.subscribe('testtopic', { qos: 0 })
})
```

```javascript
// Unsubscribe
client.unubscribe('testtopic', () => {
  console.log('Unsubscribed')
})
```

### 发布/接收消息

发布消息到某主题，发布的主题必须符合 MQTT 发布主题规则，否则将断开连接。发布之前无需订阅该主题，但要确保客户端已成功连接：

```javascript
// Publish
client.publish('testtopic', 'ws connection demo...!', { qos: 0, retain: false })
```

```javascript
// Received
client.on('message', (topic, message, packet) => {
  console.log('Received Message: ' + message.toString() + '\nOn topic: ' + topic)
})
```

### 微信小程序

MQTT.js 库对微信小程序特殊处理，使用  `wxs`  协议标识符。注意小程序开发规范中要求必须使用加密连接，连接地址应类似为 `wxs://broker.emqx.io:8084/mqtt`。

### EMQX 启用 SSL/TLS 加密连接

EMQ 内置自签名证书，默认已经启动了加密的 WebSocket 连接，但大部分浏览器会报证书无效错误如 `net::ERR_CERT_COMMON_NAME_INVALID`  (Chrome、360 等 webkit 内核浏览器在开发者模式下， Console 选项卡 可以查看大部分连接错误)。导致该错误的原因是浏览器无法验证自签名证书的有效性，读者需从证书颁发机构购买可信任证书，并参考该篇文章中的相应部分进行配置操作：[EMQX MQTT 服务器启用 SSL/TLS 安全连接](https://www.emqx.com/zh/blog/emqx-server-ssl-tls-secure-connection-configuration-guide)。

这里就总结启用 SSL/TLS 证书需要具备的条件是：

- 将域名绑定到 MQTT 服务器公网地址：CA 机构签发的证书签名是针对域名的；
- 申请证书：向 CA 机构申请所用域名的证书，注意选择一个可靠的 CA 机构且证书要区分泛域名与主机名；
- 使用加密连接的时候选择 `wss` 协议，并 **使用域名连接** ：绑定域名-证书之后，必须使用域名而非 IP 地址进行连接，这样浏览器才会根据域名去校验证书以在通过校验后建立连接。

#### EMQX 配置

打开 `etc/emqx.conf` 配置文件，修改以下配置：

```shell
# wss 监听地址
listener.wss.external = 8084

# 修改密钥文件地址
listener.wss.external.keyfile = etc/certs/cert.key

# 修改证书文件地址
listener.wss.external.certfile = etc/certs/cert.pem
```

完成后重启 EMQX 即可。

> 可以使用你的证书与密钥文件直接替换到 etc/certs/ 下。

### 在 Nginx 上配置反向代理与证书

使用 Nginx 来反向代理并加密 WebSocket 可以减轻 EMQX 服务器计算压力，同时实现域名复用，同时通过 Nginx 的负载均衡可以分配多个后端服务实体。

```shell
# 建议 WebSocket 也绑定到 443 端口
listen 443, 8084;
server_name example.com;

ssl on;

ssl_certificate /etc/cert.crt;  # 证书路径
ssl_certificate_key /etc/cert.key; # 密钥路径


# upstream 服务器列表
upstream emq_server {
    server 10.10.1.1:8883 weight=1;
    server 10.10.1.2:8883 weight=1;
    server 10.10.1.3:8883 weight=1;
}

# 普通网站应用
location / {
    root www;
    index index.html;
}

# 反向代理到 EMQX 非加密 WebSocket
location / {
    proxy_redirect off;
    # upstream
    proxy_pass http://emq_server;
    
    proxy_set_header Host $host;
    # 反向代理保留客户端地址
    proxy_set_header X-Real_IP $remote_addr;
    proxy_set_header X-Forwarded-For $remote_addr:$remote_port;
    # WebSocket 额外请求头
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection “upgrade”;
}
```



## 其它资源

项目完整代码请见：https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-WebSocket

一款在线的 MQTT WebSocket 连接测试工具：https://www.emqx.com/zh/mqtt/mqtt-websocket-toolkit





[^1]: https://zh.wikipedia.org/zh-hans/WebSocket


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://www.emqx.com/zh/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
