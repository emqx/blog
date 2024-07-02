EMQX 作为一个全球领先的 MQTT 物联网平台，支持集群扩展以实现高性能和高可用。而在集群部署中，我们通常还会用到 NGINX、HAProxy 等反向代理，实现负载均衡、SSL/TLS 终结、故障转移等目的。

但使用代理时，由于客户端不再直接访问 EMQX，EMQX 将无法直接获取到客户端的真实 IP，这不利于我们实现安全审计、访问限制等基于 IP 的应用。

本文将以 [NGINX 1.26.1](https://nginx.org/en/download.html) 和 [EMQX 5.7.0](https://www.emqx.com/zh/downloads-and-install/broker?os=Ubuntu) 为例，介绍使用 NGINX 反向代理 EMQX 时，如何通过 PROXY 协议或 `X-Forwarded-For` 标头获取 MQTT 客户端的真实 IP。

## 获取 MQTT over TCP 客户端真实 IP

### 单级代理

单级代理，即 MQTT 客户端与后端服务器 EMQX 之间只有一个 Load Balancer，这是最常见的情况：

```
Client -> Load Balancer(NGINX, HAProxy, ...) -> Server(EMQX)
```

此时，我们可以借助 [PROXY 协议](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) 获取真实客户端的 IP。

PROXY 协议最早由 [HAProxy](https://www.haproxy.org/) 提出并设计，它约定了 TCP 代理封装和向后传递客户端原始 IP 和端口等元数据的规范。目前 PROXY 协议已经成为使用代理中继 TCP 连接时服务端获取客户端原始 IP 地址与端口的首选方案。

使用 PROXY 协议前：

```txt
+ ----------- +  <CONNECT packet> | ...  + ------------ +  <CONNECT packet> | ...  + ------ +
| MQTT Client |  ----------------------> | Load Balancer| -----------------------> | Server |
+ ----------- +                          + ------------ +                          + ------ +
```

使用 PROXY 协议后：

```txt
+ ----------- +  <CONNECT packet> | ...  + ------------ +  <PROXY protocol header> | <CONNECT packet> | ... + ------ +
| MQTT Client |  ----------------------> | Load Balancer| ------------------------------------------------> | Server |
+ ----------- +                          + ------------ +                                                   + ------ +
```

下面是一个典型的 PROXY 协议标头：

```
PROXY TCP 172.168.0.116 172.168.0.200 39826 1883
|     |   |             |             |     |
|     |   |             |             |     目的端口
|     |   |             |             源端口
|     |   |             目的 IP
|     |   源 IP
|     表示这是一个 IPv4 的 TCP 连接
固定前缀，用于标识 PROXY 协议
```

PROXY 协议目前有 v1 和 v2 两个版本，v1 就是上面介绍的这种人类可读的文本格式，v2 则是改成了机器易读的二进制格式，以提高程序的解析效率。v2 的具体格式本文不再展开，感兴趣的读者可以前往 [The PROXY protocol Version 1 & 2](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) 了解更多。EMQX 同时支持 v1 和 v2，并且支持自动检测使用的版本。不过在本文中，我们将统一使用 v1 进行演示。

#### 配置

以 NGINX 为例，首先我们需要修改 NGINX（参考 [此处](https://nginx.org/en/docs/install.html) 进行安装）的配置，打开 `/etc/nginx/nginx.conf` 并添加以下配置：

```nginx
stream {
  upstream server {
    # 请按您实际的 IP 与监听端口修改
    server 172.16.0.71:1883;
  }
  
  server {
    listen 1883;
    proxy_pass server;
    # 启用 PROXY 协议发送
    proxy_protocol on;
  }
}
```

以上配置表示 NGINX 将监听 1883 端口，并将端口数据转发给地址为 `172.16.0.71:1883` 的 Server，由于启用了 PROXY 协议，NGINX 将在连接建立后**首先**发送 PROXY 协议标头。

保存配置后，运行以下命令重载配置：

```bash
nginx -s reload
```

然后，我们还需要修改 EMQX（参考 [此处](https://docs.emqx.com/zh/emqx/latest/deploy/install.html) 进行安装）配置来启用对 PROXY 协议头的解析。

以 5.7 版本为例，我们只需要在浏览器中打开 [Dashboard](https://docs.emqx.com/zh/emqx/latest/dashboard/introduction.html)，前往 “管理” > “集群配置” > “MQTT 配置”，点击默认的 TCP 监听器（或其他您想要更改的监听器）进入配置页面，将 “代理协议” 设置为 `true` 即可：

![01dashboardproxyprotocol.png](https://assets.emqx.com/images/c754b3844bfae44ff4e48d12542ee5b0.png)

对 EMQX 监听器的改动将在点击 “更新” 后立即生效。

#### 验证

在本示例中，每台主机的 IP 如下：

```txt
+ ----------------------- +      + ---------------------- +      + ------------------- +
| MQTT Client             |      | NGINX                  |      | EMQX                |
| *********************** | ---> | ********************** | ---> | ******************* |
| LAN IP: /               |      | LAN IP: 172.16.0.116   |      | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |      | WAN IP: 121.36.192.227 |      | WAN IP: /           |
+ ----------------------- +      + ---------------------- +      + ------------------- + 
```

为了验证 NGINX 是否正确发送了我们期望的 PROXY 协议标头，我们可以在运行 EMQX 的机器上使用以下命令来捕获报文：

```bash
# -i eth0, 捕获网络接口 eht0 上的数据包
# -s 0, 捕获完整数据包
# -vv，更详细的输出
# -n，不要将地址（即主机地址、端口号等）转换为名称
# -X，以十六进制和 ASCII 打印每个数据包的数据
# -S，打印绝对 TCP 序列号而不是相对序列号
# 'port 1883'，捕获所有源端口或目的端口为 1883 的数据包
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 1883'
```

然后使用 MQTTX CLI（参考 [此处](https://mqttx.app/zh/docs/cli/downloading-and-installation) 进行安装）作为 MQTT 客户端连接到 NGINX：

```bash
# 将 121.36.192.227 修改为你实际 NGINX 的 IP
mqttx conn -h 121.36.192.227 -p 1883 --client-id mqttx-client
```

在 tcpdump 捕获的报文中，我们看到 NGINX（`171.16.0.116`）在与 EMQX（`172.16.0.71`）建立 TCP 连接后，首先发送了一个 PROXY 协议标头，该标头指示客户端的 IP 为 `115.236.21.86`：

![02capturedpackets.png](https://assets.emqx.com/images/36f10b07ff55570ba2db1e9730055ede.png)

通过 EMQX 的 CLI 命令，我们也可以看到 EMQX 成功获取到了客户端的源 IP 地址和端口：

```bash
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:61177, ...)
```

### 多级代理

一些复杂的大型部署还可能会存在多级代理，例如：

```txt
+ ----------- +        + ---- +       + ---- +       + ------ +
| MQTT Client |  ----> | LB 1 | ----> | LB 2 | ----> | Server |
+ ----------- +        + ---- +       + ---- +       + ------ +
```

存在多级反向代理时，为了让后端的 EMQX 仍然可以获取到客户端的真实 IP，我们需要对 NGINX 的配置进行一些调整。

首先，最外层的 LB，也就是 LB 1，必须开启 PROXY 协议发送，以便将客户端的源 IP 和源端口传递下去。

由于每个 TCP 连接只能发送一次 PROXY 协议标头，所以 LB 不能既转发收到的 PROXY 协议标头，又追加发送自己的标头。下面这种情况是不被允许的：

```txt
+ ----------- +     + ---- +  <PP header 1> | ...  + ---- +  <PP header 2> | <PP header 1> | ...  + ------ +
| MQTT Client |  -> | LB 1 | --------------------> | LB 2 | ------------------------------------> | Server |
+ ----------- +     + ---- +                       + ---- +                                       + ------ +
```

> PP header 即 PROXY protocol header

因此，对于中间 LB，我们有两种配置方式可选。第一种方式最简单，中间的 LB 既不需要启用 PROXY 协议接收，也不需要启用 PROXY 协议发送，它们只要透传 LB 1 发送的所有报文即可：

```txt
+ ----------- +        + ---- +  <PP header 1> | ...  + ---- +  <PP header 1> | ...  + ------ +
| MQTT Client |  ----> | LB 1 | --------------------> | LB 2 | --------------------> | Server |
+ ----------- +        + ---- +                       + ---- +                       + ------ +

PP header 1 = "PROXY TCP <Client IP> <LB 1 IP> <Client Port> <LB 1 Port>"
```

第二种方式则需要中间的 LB 同时启用 PROXY 协议接收和发送，每个 LB 在收到 PROXY 协议标头后，获取其中的客户端源 IP 地址与端口，然后将其设置到发送给下一级 LB 或者后端应用服务器的 PROXY 协议标头中：

```txt
+ ----------- +        + ---- +  <PP header 1> | ...  + ---- +  <PP header 2> | ...  + ------ +
| MQTT Client |  ----> | LB 1 | --------------------> | LB 2 | --------------------> | Server |
+ ----------- +        + ---- +                       + ---- +                       + ------ +

PP header 1 = "PROXY TCP <Client IP> <LB 1 IP> <Client Port> <LB 1 Port>"
PP header 2 = "PROXY TCP <Client IP> <LB 2 IP> <Client Port> <LB 2 Port>"
```

#### 透传

LB 1 和 LB 2 均使用 NGINX，以下是透传的配置示例：

```nginx
# LB 1
# 启用 PROXY 协议发送
stream {
  upstream proxy2 {
    # 请修改为您实际 LB 2 的 IP 与监听端口
    server 172.16.0.200:1883;
  }
  
  server {
    listen 1883;
    proxy_pass proxy2;
    # 启用 PROXY 协议发送
    proxy_protocol on;
  }
}

# LB 2
# 不启用 PROXY 协议接收与发送
stream {
  upstream server {
    # 请修改为您实际的 EMQX IP 与监听端口
    server 172.16.0.71:1883;
  }
  
  server {
    listen 1883;
    proxy_pass server;
  }
}
```

EMQX 则继续保持启用 PROXY 协议接收，无需其他改动。

##### 验证

由于增加了一个 LB，因此在本示例中，各主机的 IP 如下：

```txt
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
| MQTT Client             |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    | EMQX                |
| *********************** | -> | ********************** | -> | ******************** | -> | ******************* |
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    | WAN IP: /           |
+ ------------------------+    + ---------------------- +    + -------------------- +    + ------------------- +
```

在 LB 2 中运行以下命令来捕获报文：

```bash
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 1883'
```

然后使用 MQTTX CLI 作为 MQTT 客户端连接到 LB 1：

```bash
# 将 121.36.192.227 修改为你实际最外层 LB 的 IP
mqttx conn -h 121.36.192.227 -p 1883 --client-id mqttx-client
```

在 tcpdump 捕获的报文中，我们可以看到 LB 2 收到了来自 LB 1 的 PROXY 协议标头，该标头指示客户端的 IP 为 `115.236.21.86`，而在 LB 2 与 EMQX 的连接中，标头内容没有发生变化，说明透传生效：

![03capturedpacketspassthrough.png](https://assets.emqx.com/images/48806795c92a35b9346d111613b709a3.png)

通过 EMQX 的 CLI 命令，我们可以看到 EMQX 成功获取到了客户端的源 IP 与源端口：

```bash
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:18936, ...)
```

#### 非透传

配置如下：

```nginx
# LB 1
# 启用 PROXY 协议发送，配置与透传时相同
stream {
  upstream proxy2 {
    # 请修改为您实际 LB 2 的 IP 与监听端口
    server 172.16.0.200:1883;
  }
  
  server {
    listen 1883;
    proxy_pass proxy2;
    # 启用 PROXY 协议发送
    proxy_protocol on;
  }
}

# LB 2
# 启用 PROXY 协议接收与发送
# 如果有更多中间 LB，其配置与 LB 2 类似，只需修改相应的 IP 和端口即可
stream {
  upstream server {
    server 172.16.0.71:1883;
  }
  
  server {
    # 启用 PROXY 协议接收
    listen 1883 proxy_protocol;
    proxy_pass server;
    # 启用 PROXY 协议发送
    proxy_protocol on;
    # 设置可信地址，请将 172.16.0.0/24 修改为你信任的代理的 IP 地址或者 CIDR 范围
    set_real_ip_from 172.16.0.0/24;
    # 设置 LB 1 的 WAN IP 为信任地址
    # set_real_ip_from 172.16.0.116
  }
}
```

注意必须使用 `set_real_ip_from` 指令指定信任的 LB 的 IP 地址或 CIDR 地址范围。NGINX 只会从信任来源的 PROXY 协议标头中获取真实客户端的源 IP，否则 LB 2 在向 Server 发送 PROXY 协议标头时将使用 LB 1 的 IP 而不是客户端的 IP 作为源 IP：

```txt
       + ---- +  PROXY TCP <LB 1 IP> <LB 2 IP> <LB 1 Port> <LB 2 Port>  + ------ + 
... -> | LB 2 | ------------------------------------------------------> | Server |
       + ---- +                                                         + ------ +  
```

指令  `set_real_ip_from`  依赖 Stream Real-IP 模块，你可以使用以下命令检查当前的 NGINX 是否包含了此模块：

```bash
nginx -V 2>&1 | grep -- 'stream_realip_module'
```

如果没有，那么你需要手动编译 NGINX 并在编译时包含此模块，详情请参阅 [Installing NGINX Open Source ](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/)。

##### 验证

在本示例中，各主机的 IP 与透传时相同：

```txt
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
| MQTT Client             |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    | EMQX                |
| *********************** | -> | ********************** | -> | ******************** | -> | ******************* |
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    | WAN IP: /           |
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
```

在 LB 2 中运行以下命令来捕获报文：

```bash
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 1883'
```

然后使用 MQTTX CLI 连接到 LB 1：

```bash
# 将 121.36.192.227 修改为你实际最外层 LB 的 IP
mqttx conn -h 121.36.192.227 -p 1883 --client-id mqttx-client
```

在 tcpdump 捕获的报文中，我们可以看到 LB 2 收到了来自 LB 1 的 PROXY 协议标头，该标头指示客户端的 IP 为 `115.236.21.86`。在 LB 2 与 EMQX 的连接中，标头内容发生了变化，但仍然正确指示了客户端的真实 IP，这说明 `set_real_ip_from` 指令发挥了作用：

![04capturedpacketsnonpassthrough.png](https://assets.emqx.com/images/af79682b15c8df28336509615ad19d94.png)

通过 EMQX 的 CLI 命令，我们可以看到 EMQX 成功获取到了客户端的源 IP 与源端口：

```bash
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:39817, ...)
```

## 获取 MQTT over WebSocket 客户端真实 IP

在浏览器、微信/抖音小程序等 Web 应用中，客户端将使用 MQTT over WebSocket 接入 EMQX。由于 WebSocket 可以携带 Header，所以除了 PROXY 协议，我们还可以通过 `X-Forwarded-For` 标头在 LB 与应用服务器之间传递客户端的真实 IP。

使用 PROXY 协议获取 MQTT over WebSocket 客户端真实 IP，NGINX 和 EMQX 的配置方式与获取 MQTT over TCP 客户端真实 IP 时完全相同，所以这里不再赘述。

接下来，我们将着重介绍如何配置 NGINX 和 EMQX 以通过 `X-Forwarded-For` 标头获取客户端真实 IP。

### 单级代理

我们还是从最常见的单级代理开始，以下是 NGINX 的配置示例：

```nginx
http {
  upstream server {
    server 172.16.0.71:8083;
  }
  
  server {
    listen 8083;
    # 使用 /mqtt 作为提供 WebSocket 服务的端点
    location /mqtt {
      proxy_pass http://server;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}
```

当客户端准备使用 MQTT over WebSocket 接入 EMQX 时，NGINX 不会主动将 Upgrade 和 Connection 标头转发给后端的 EMQX，所以我们必须配置 NGINX 使其显式地传递这两个标头，以便 EMQX 了解客户端将协议切换到 WebSocket 的意图。

NGINX 的 `proxy_set_header` 指令允许我们修改或设置 NGINX 传递给后端的请求标头：

```nginx
# $http_* 是 NGINX 的内置变量，它的值是 NGINX 收到的给定 HTTP 标头。
# 因此 $http_upgrade 的值就是 NGINX 收到请求中的 Upgrade 标头。
# 这里相当于将 NGINX 发送的 Upgrade 标头设置为 "websocket"。
proxy_set_header Upgrade $http_upgrade;

# 将 Connection 标头设置为 "Upgrade"，表示这是一个升级请求，请求升级到 Upgrade 标头中列出的协议。
proxy_set_header Connection "Upgrade";
```

`$remote_addr` 和 `$remote_port` 是 NGINX 的内置变量，它们记录了对端的 IP 地址和端口。注意在多级代理中，对端也可能是上一级 LB。

当然在单级代理中，我们可以直接使用 `$remote_*` 来获取 MQTT 客户端的 IP 地址与端口：

```nginx
# 将 Host 标头设置为客户端所请求的主机名
proxy_set_header Host $host;

# 设置 X-Forwarded-For 以传递 MQTT 客户端 IP 地址
proxy_set_header X-Forwarded-For $remote_addr;

# 设置 X-Forwarded-Port 以传递 MQTT 客户端源端口
proxy_set_header X-Forwarded-Port $remote_port;
```

> X-Forwarded-Port 也可以设置为 $server_port 用来指示客户端访问的端口，以便上层应用根据入口提供不同服务。在本文中，我们主要使用 X-Forwarded-Port 来传递原始客户端的源端口。

将以上配置保存至 `/etc/nginx/nginx.conf`，然后运行 `nginx -s reload` 重载配置。

接下来，我们需要修改 EMQX 的监听器配置。在浏览器中打开 Dashboard，前往 “管理” > “集群配置” > “MQTT 配置”，点击默认的 WebSocket 监听器（或其他您想要更改的监听器）进入配置页面，展开 “高级设置”，然后将以下配置粘贴至 “自定义配置”，最后点击 “更新” 即可：

```bash
websocket.proxy_address_header = X-Forwarded-For
websocket.proxy_port_header = X-Forwarded-Port
```

以上配置表示 EMQX 将从收到的 WebSocket 升级请求中取 `X-Forwarded-For` 标头最左侧的 IP 作为客户端源 IP，取 `X-Forwarded-Port` 标头最左侧的端口作为客户端源端口。

#### 验证

在本示例中，各主机的 IP 如下：

```txt
+ ----------------------- +      + ---------------------- +      + ------------------- +
| MQTT Client             |      | NGINX                  |      | EMQX                |
| *********************** | ---> | ********************** | ---> | ******************* |
| LAN IP: /               |      | LAN IP: 172.16.0.116   |      | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |      | WAN IP: 121.36.192.227 |      | WAN IP: /           |
+ ----------------------- +      + ---------------------- +      + ------------------- + 
```

在 EMQX 所在的机器上运行以下命令来捕获报文：

```bash
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 8083'
```

然后使用 MQTTX CLI 连接到 LB 1：

```bash
# 将 121.36.192.227 修改为你实际最外层 LB 的 IP
mqttx conn -h 121.36.192.227 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
```

在 tcpdump 捕获的报文中，我们看到 LB 在与 EMQX 建立 TCP 连接后，发送了一个协议升级的 HTTP 请求，请求中的 `X-Forwarded-For` 为 `115.236.21.86`，`X-Forwarded-Port` 为 `61813`，分别对应了真实客户端的源 IP 地址与源端口：

![05xforwardedforlbtoemqx.png](https://assets.emqx.com/images/2325b67b1ce7bf89d81a4a897cb22996.png)

通过 EMQX 的 CLI 命令，我们可以看到 EMQX 成功获取到了 MQTT 客户端的真实 IP 与端口：

```bash
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:61813, ...)
```

### 多级代理

在多级代理中，`X-Forwarded-For` 除了跨代理传递客户端真实 IP，还会记录经过的中间代理的 IP，以便后端应用服务器识别请求的来源并提供不同的服务。

但在实际应用中，仅仅让 LB 将下游的 IP 追加到 `X-Forwarded-For` 标头是不够的，我们必须考虑客户端恶意欺骗的情况，因为客户端也可以设置 `X-Forwarded-For` 标头。

在前面单级代理中，我们直接使用客户端的源 IP （`$remote_addr`）覆盖了 `X-Forwared-For`，这可以保证服务端最终获取到的 `X-Forwared-For` 一定是真实且正确的。

而多级代理则不同，如果不做处理，客户端就可以伪造任意 IP 欺骗服务端，绕过服务端的安全管理策略。例如下面这种情况，应用服务器就会误以为 `<Fake IP>` 是客户端的真实 IP。

```txt
+ ------ +   X-Forwarded-For: <Fake IP>  + ---- +  X-Forwarded-For: <Fake IP>, <Real Client IP>
| Client |  ---------------------------> | LB 1 | ----------------------------------------------...
+ ------ +                               + ---- +

     + ---- +  X-Forwarded-For: <Fake IP>, <Real Client IP>, <LB 1 IP>  + ------ +
..-> | LB 2 | --------------------------------------------------------> | Server |
     + ---- +                                                           + ------ +
```

想要解决这一问题，我们通常有两种办法。第一种方法，让最外层的 LB 将 `X-Forwarded-For` 直接赋值为 `$remote_addr` 而不是在原有基础上追加，从源头上解决客户端伪造 `X-Forwarded-For` 的可能性：

```nginx
# 直接赋值
proxy_set_header X-Forwarded-For $remote_addr;
# 在原有基础上追加
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

预期效果：

```txt
+ ------ +   X-Forwarded-For: <Fake IP>  + ---- +  X-Forwarded-For: <Real Client IP>
| Client |  ---------------------------> | LB 1 | -----------------------------------...
+ ------ +                               + ---- +

     + ---- +  X-Forwarded-For: <Real Client IP>, <LB 1 IP>  + ------ +
..-> | LB 2 | ---------------------------------------------> | Server |
     + ---- +                                                + ------ +
```

第二种方法，让所有 LB 都在原有 `X-Forwarded-For` 的基础上追加远端 IP，然后在最内层的 LB 中设置可信地址。这个最内层的 LB 将从右向左遍历，取第一个非授信的 IP 作为客户端的真实 IP。

```txt
+ ------ +   X-Forwarded-For: <Fake IP>  + ------------ +  X-Forwarded-For: <Fake IP>, <Real Client IP>
| Client |  ---------------------------> | Trusted LB 1 | ----------------------------------------------...
+ ------ +                               + ------------ +

     + ------------ +  X-Forwarded-For: <Fake IP ✘>, <Real Client IP ✘>, <Trusted LB 1 IP ✔︎>  + ------ +
..-> | Trusted LB 2 | ----------------------------------------------------------------------> | Server |
     + ------------ +                                                                         + ------ +
```

这时虽然客户端伪造了 `X-Forwarded-For`，但是在请求到达应用服务器时，伪造的 IP 也只会位于 `X-Forwarded-For` 的左侧，从右向左剔除掉所有可信 IP，第一个非授信的 IP 必然就是最外层可信的 LB 添加的客户端真实 IP。

#### 方法一：使用 $remote_addr

```nginx
# LB 1
# 覆盖 X-Forwarded-For 和 X-Forwarded-Port 的原有值
http {
  upstream proxy2 {
    server 172.16.0.200:8083;
  }
  
  server {
    listen 8083;
    location /mqtt {
      proxy_pass http://proxy2;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}

# LB 2
# 在原有 X-Forwarded-For 和 X-Forwarded-Port 的基础上追加
http {        
  upstream server {
    server 172.16.0.71:8083;
  }
  
  server {
    listen 8083;
      
    location /mqtt {
      proxy_pass http://server;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $remote_port";
    }
  }
}
```

将以上配置分别保存至 LB 1 和 LB 2，运行 `nginx -s reload` 重载配置。

EMQX 的配置与单级代理时相同：

```bash
websocket.proxy_address_header = X-Forwarded-For
websocket.proxy_port_header = X-Forwarded-Port
```

##### 验证

由于无法用 MQTTX CLI 伪造 `X-Forwarded-For`，为了验证效果，我们可以在运行 MQTT Client 的主机上额外部署一个 NGINX 代理，它的作用是帮助我们伪造一个值为 `127.0.0.1` 的 `X-Forwarded-For` 标头，其配置如下：

```nginx
http {
  upstream proxy1 {
    # 请修改为您实际 LB 1 的公网 IP 与监听端口
    server 121.36.192.227:8083;
  }
  
  server {
    listen 8083;
    location /mqtt {
      proxy_pass http://proxy1;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}
```

此时各主机的 IP 如下：

```txt
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
| MQTT Client + Proxy     |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    | EMQX                |
| *********************** | -> | ********************** | -> | ******************** | -> | ******************* |
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    | LAN IP: 172.16.0.71 |
| WAN IP: 1.94.170.163    |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    | WAN IP: /           |
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
```

在 LB 1 和 LB 2 这两台主机中运行以下命令来捕获报文：

```bash
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 8083'
```

运行 MQTTX CLI，这次连接本地的 NGINX 而不是远端的 LB 1：

```bash
mqttx conn -h 127.0.0.1 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
```

在 tcpdump 捕获的报文中，我们可以看到 LB 1 收到的 WebSocket 升级请求中 `X-Forwarded-For` 为 `127.0.0.1`，这相当于一个恶意的 MQTT 客户端企图欺骗服务端这是一个本机连接。

但 LB 1 知道这个请求实际来自哪里，因此在它发送给 LB 2 的 WebSocket 升级请求中，`X-Forwarded-For` 被设置为当前连接的客户端的真实 IP，即 `1.94.170.163`，客户端伪造的 `X-Forwarded-For` 被完全忽略。因此最终服务端端仍然可以获取到正确的原始客户端的源 IP，`X-Forwarded-Port` 也是同理。

![06remoteaddr.png](https://assets.emqx.com/images/e814fb0d2f3789e79458fa35acc0ca46.png)

通过 EMQX 的 CLI 命令，我们可以看到 EMQX 成功获取到了客户端的源 IP 与源端口：

```bash
$ mqttx conn -h 127.0.0.1 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
Client(mqttx-client, ..., peername=1.94.170.163:52662, ...)
```

#### 方法二：设置可信地址

为了验证 `real_ip_recursive` 指令的效果，我们额外增加一台主机充当 LB 3，LB 1 与 LB 2 配置的区别仅仅是 upstream 的 IP 不同：

```nginx
# LB 1
# 在原有 X-Forwarded-For 和 X-Forwarded-Port 的基础上追加
http {
  upstream proxy2 {
    server 172.16.0.200:8083;
  }
  
  server {
    listen 8083;
    location /mqtt {
      proxy_pass http://proxy2;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $remote_port";
    }
  }
}

# LB 2
# 在原有 X-Forwarded-For 和 X-Forwarded-Port 的基础上追加
http {        
  upstream proxy3 {
    server 172.16.0.225:8083;
  }
  
  server {
    listen 8083;
      
    location /mqtt {
      proxy_pass http://proxy3;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $remote_port";
    }
  }
}

# LB 3
# 在原有 X-Forwarded-For 和 X-Forwarded-Port 的基础上追加
# 另外从 X-Forwarded-For 中获取客户端真实 IP 并设置到 X-Real-IP 标头中
http {        
  upstream server {
    server 172.16.0.71:8083;
  }
  
  server {
    listen 8083;
    
    # 信任 172.16.0.0/24 范围内的所有 IP
    set_real_ip_from 172.16.0.0/24;
    # 从 X-Forwarded-For 获取客户端真实 IP
    real_ip_header X-Forwarded-For;
    # 从右向左递归搜索第一个非授信的 IP 作为客户端的真实 IP
    real_ip_recursive on;
      
    location /mqtt {
      proxy_pass http://server;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      
      # 追加 $realip_remote_* 而不是 $remote_*
      proxy_set_header X-Forwarded-For "$http_x_forwarded_for, $realip_remote_addr";
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $realip_remote_port";
      # 使用 X-Real-IP 传递原始客户端 IP
      proxy_set_header X-Real-IP $remote_addr;
    }
  }
}

```

LB 3 配置的核心在于 `set_real_ip_from`、`real_ip_header` 这几个指令，这些命令依赖 HTTP Real-IP 模块，你可以用以下命令检查当前的 NGINX 是否包含了此模块：

```bash
nginx -V 2>&1 | grep -- 'http_realip_module'
```

如果没有，那么你需要手动编译 NGINX 并在编译时包含此模块，详情请参阅 [Installing NGINX Open Source ](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/)。

通过 `set_real_ip_from` 指令，我们可以指定信任的 LB 的 IP 地址或 CIDR 地址范围，`set_real_ip_from` 可以多次调用，例如：

```nginx
set_real_ip_from 172.16.0.0/24;
set_real_ip_from 115.236.21.86;
```

通过 `real_ip_header` 指令，我们可以指定 Real IP 的来源，在本示例中，Real IP 的来源就是 `X-Forwarded-For` 标头 。

通过 `real_ip_recursive` 指令，我们可以指定是否递归搜索 Real IP。设置为 off，那么 NGINX 将直接从右向左取第一个 IP 作为客户端的真实 IP；设置为 on，那么 NGINX 将从右向左取第一个不在授信范围内的 IP 作为客户端的真实 IP。后者正是本示例所需要的。

一旦使用了 Real-IP 模块，NGINX 会将获取到的客户端真实 IP 和端口放入变量 `$remote_addr` 和 `$remote_port`，此时下游的 IP 和端口需要从变量 `$realip_remote_addr` 和 `$realip_remote_port` 获取：

```nginx
# 追加 $realip_remote_* 而不是 $remote_*
proxy_set_header X-Forwarded-For "$http_x_forwarded_for, $realip_remote_addr";
proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $realip_remote_port";
```

这里我们将 `$remote_addr` 赋值给另一个标头，即 `X-Real-IP`，因此还需要同步修改 EMQX 的 WebSocket 监听器配置：

```bash
websocket.proxy_address_header = X-Real-IP
websocket.proxy_port_header = X-Forwarded-Port
```

##### 验证

在本示例中，各主机的 IP 如下：

```txt
+ ----------------------- +    + ---------------------- +    + -------------------- +    
| MQTT Client + Proxy     |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    
| *********************** | -> | ********************** | -> | ******************** | --...
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    
| WAN IP: 1.94.170.163    |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    
+ ----------------------- +    + ---------------------- +    + -------------------- +

     + -------------------- +    + ------------------- +
     | LB 3 (NGINX)         |    | EMQX                |
..-> | ******************** | -> | ******************* |
     | LAN IP: 172.16.0.225 |    | LAN IP: 172.16.0.71 |
     | WAN IP: /            |    | WAN IP: /           |
     + -------------------- +    + ------------------- +
```

在 LB 1、LB 2 和 LB 3 这三台主机中运行以下命令来捕获报文：

```bash
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 8083'
```

与上一个示例相同，我们需要在运行 MQTT Client 的机器上额外部署一个 NGINX 代理，其配置如下：

```nginx
http {
  upstream proxy1 {
    # 请修改为您实际 LB 1 的公网 IP 与监听端口
    server 121.36.192.227:8083;
  }
  
  server {
    listen 8083;
    location /mqtt {
      proxy_pass http://proxy1;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}
```

运行 MQTTX CLI，连接本地的 NGINX 而不是远端的 LB 1：

```bash
mqttx conn -h 127.0.0.1 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
```

在 tcpdump 捕获的报文中，我们看到 LB 1 收到的 WebSocket 升级请求中 `X-Forwarded-For` 为 `127.0.0.1`，这相当于一个恶意的 MQTT 客户端企图欺骗服务端这是一个本机连接：

![07clienttolb1.png](https://assets.emqx.com/images/b072b61c205a4a8f1ad1ae54b1cf8c6b.png)

但这一次，我们没有直接覆盖 `X-Forwarded-For`， 而是在原有的基础上追加，因此在 LB 2 发送给 LB 3 的 WebSocket 升级请求中，我们可以看到 `X-Forwarded-For` 的值为 `127.0.0.1, 1.94.170.163, 172.16.0.116`：

![08lb2tolb3.png](https://assets.emqx.com/images/2798536937ecf478a066e4b525a64a69.png)

而在 LB 3 发送给 EMQX 的 WebSocket 的升级请求中，我们可以看到 `X-Real-IP` 标头被设置为 `1.94.170.163`，这也是我们预期的结果：

![09lb3toemqx.png](https://assets.emqx.com/images/a0efb4125e26c8524a1be6cbb712b62c.png)

通过 EMQX 的 CLI 命令，我们将看到 EMQX 成功获取到了真实客户端的源 IP 与源端口：

```bash
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=1.94.170.163:39872, ...)
```

而如果我们在 LB 3 中将 `real_ip_recursive` 设置为 off，那么我们将看到 `X-Real-IP` 标头被设置为 `172.16.0.116`：

![10lb3toemqx.png](https://assets.emqx.com/images/105beca0716d2e0a0bd60101cc9fc49c.png)

## 结语

在本文中，我们深入了解了如何正确配置 EMQX 与 NGINX，以借助 PROXY 协议或 `X-Forwarded-For` 标头，使客户端的真实 IP 可以跨越单级甚至多级代理传递到最终的 EMQX 服务器，以便实现安全审计、访问限制、流量监控等应用。

在后续的博客中，我们还将为您带来使用 HAProxy 反向代理 EMQX 时获取客户端真实 IP 的配置指南。欢迎订阅我们的[博客](https://www.emqx.com/zh/blog)，以便及时掌握最新动态。



<section class="promotion">
    <div>
        咨询 EMQX 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
