在上一篇文章《[MQTT Broker 集群详解（一）：负载均衡](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-1-load-balancing)》中，我们简单介绍了 MQTT 负载均衡：负载均衡既可以应用于传输层，也可以用于应用层。在本文中，我们将详细介绍应用层负载均衡，其中最有趣的部分：粘性会话（sticky-session）。

本文由两部分组成，第一部分将介绍 MQTT 会话，以及在分布式 [MQTT Broker](https://www.emqx.io/zh) 集群中处理会话面临的挑战；第二部分是通过在 [EMQX 4.3](https://www.emqx.com/zh/products/emqx) 集群前面配置 [HAProxy 2.4](https://www.haproxy.org/) 负载均衡器，带读者亲自体验如何充分利用粘性会话实现负载均衡。



## MQTT 会话

为了持续接收消息，[MQTT 客户端](https://www.emqx.com/zh/blog/introduction-to-the-commonly-used-mqtt-client-library)通常会连接至 MQTT Broker 进行订阅并保持长期连接。由于网络问题或客户端软件维护等原因，连接可能会中断一段时间，这并不罕见，但客户端通常希望在重新连接成功后仍然能接收到中断期间漏收的消息。

因此，为客户端提供服务的 MQTT Broker 应该为客户端保持会话（根据客户端的请求，将「Clean-Session」标志设置为  false）。此时，即使客户端断开连接，订阅者当前订阅的主题以及传递给这些主题的消息（QoS1 和 2）等也会由消息服务器（broker）保留。

当具有持久会话的客户端重新连接时，它不需要重新订阅主题，消息服务器应该将所有未发送的消息发送给该客户端。

我们之前写过一篇关于 [MQTT 会话](https://www.emqx.com/zh/blog/mqtt-session)的文章，如果您对 MQTT 会话的技术细节感兴趣，可以通过阅读这篇文章做进一步了解。

### 会话接管

当 MQTT Brokers 形成集群时，事情会变得更加复杂。从客户端的角度来看，要连接的服务器不止一个，很难知道哪个服务器最适合连接。我们需要网络中的另一个关键组件：负载均衡器。负载均衡器成为整个集群的接入点，并将客户端的连接路由到集群中的某一个服务器。

如果客户端通过负载均衡器连接到服务器（例如，node1），然后断开连接并稍后重新连接，则新连接可能会路由到集群中的不同服务器（例如，node3）。在这种情况下，node3 应该在客户端断开连接时开始向客户端发送未发送的消息。

实现集群范围的持久会话有很多不同的策略。例如，整个集群可以共享一个全局存储来保存客户端的会话。

然而，更具可扩展性的解决方案通常以分布式方式解决这个问题，即数据从一个节点迁移到另一个节点。这种迁移称为会话接管。会话接管应该对客户端完全透明，但它是有代价的，尤其是当有很多消息需要处理时。

![会话接管](https://assets.emqx.com/images/ea4c881df579ece79600af69bec76244.png)


### 粘性会话解决方案

这里的「粘性」一词指的是负载均衡器能够在重新连接时将客户端路由到之前服务器的能力，这可以避免会话接管。当有许多客户端在同一时间重新连接时，或者在一个有问题的客户端反复断开连接并再次连接的情况下，这是一个特别有用的功能。

为了让负载均衡器以「粘性」方式分派连接，服务器需要知道连接请求中的客户端标识符（有时是用户名）——这需要负载均衡器检查 MQTT 数据包以查找此类信息。

一旦获得客户端标识符（或用户名），对于静态集群，服务器可以将客户端标识符（或用户名）散列到服务器 ID。或者为了更好的灵活性，负载均衡器可以选择维护一个从客户端标识符（或用户名）到目标节点 ID 的映射表。

在下一节中，我们将演示 HAProxy 2.4 中的粘性表策略。



## 使用 HAProxy 2.4 实现粘性会话

为了尽量减少先决条件，在这个演示集群中，我们将在 docker 容器中启动两个 EMQX 节点和一个 HAProxy 2.4。

### 创建 docker 网络

为了使容器彼此连接，我们为它们创建了一个 docker 网络。

```
docker network create test.net
```

### 启动两个 EMQX 4.3 节点

为了使节点彼此连接，应该在网络名称空间（`test.net`）中分配容器名称和 EMQX 节点名称。

#### 启动 node1

```
docker run -d \
  --name n1.test.net \
  --net test.net \
  -e EMQX_NODE_NAME=emqx@n1.test.net \
  -e EMQX_LISTENER__TCP__EXTERNAL__PROXY_PROTOCOL=on \
  emqx/emqx:4.3.7
```

#### 启动 node2

```
docker run -d \
  --name n2.test.net \
  --net test.net \
  -e EMQX_NODE_NAME=emqx@n2.test.net \
  -e EMQX_LISTENER__TCP__EXTERNAL__PROXY_PROTOCOL=on \
  emqx/emqx:4.3.7
```

> **注意环境变量**
>
> `EMQX_LISTENER__TCP__EXTERNAL__PROXY_PROTOCOL`. 该变量是为TCP监听器启用二进制代理协议，以便服务器可以获得客户端的真实 IP 地址信息，而不是负载均衡器的 IP 地址。

### 使 EMQX 节点加入集群

```
docker exec -it n2.test.net emqx_ctl cluster join emqx@n1.test.net
```

如果一切按预期进行，应该打印输出这样的日志：

```
[EMQX] emqx shutdown for join
Join the cluster successfully.
Cluster status: #{running_nodes => ['emqx@n1.test.net','emqx@n2.test.net'], stopped_nodes => []}
```

### 启动 HAProxy 2.4

创建文件 `/tmp/haproxy.config`，内容如下：

```
global
  log stdout format raw daemon debug
  nbproc 1
  nbthread 2
  cpu-map auto:1/1-2 0-1
  # Enable the HAProxy Runtime API
  # e.g. echo "show table emqx_tcp_back" | sudo socat stdio tcp4-connect:172.100.239.4:9999
  stats socket :9999 level admin expose-fd listeners

defaults
  log global
  mode tcp
  option tcplog
  maxconn 1024000
  timeout connect 30000
  timeout client 600s
  timeout server 600s

frontend emqx_tcp
  mode tcp
  option tcplog
  bind *:1883
  default_backend emqx_tcp_back

backend emqx_tcp_back
  mode tcp

  # Create a stick table for session persistence
  stick-table type string len 32 size 100k expire 30m

  # Use ClientID / client_identifier as persistence key
  stick on req.payload(0,0),mqtt_field_value(connect,client_identifier)

  # send proxy-protocol v2 headers
  server emqx1 n1.test.net:1883 check-send-proxy send-proxy-v2
  server emqx2 n2.test.net:1883 check-send-proxy send-proxy-v2
```



在测试 docker 网络中启动 haproxy：

```
docker run -d \
  --net test.net \
  --name proxy.test.net \
  -p 9999:9999 \
  -v /tmp/haproxy.cfg:/haproxy.cfg \
  haproxy:2.4 haproxy -f /haproxy.cfg
```



### 测试

现在我们使用流行的 mosquitto MQTT 客户端（也在 docker 中）对其进行测试。

我们启动一个订阅者（名为 `subscriber1`）订阅 `t/#` 主题

```
docker run --rm -it --net test.net eclipse-mosquitto \
	mosquitto_sub -h proxy.test.net -t 't/#' -I subscriber1
```

然后从另一个客户端向 `t/xyz` 发布一条 `hello` 消息

```
docker run --rm -it --net test.net eclipse-mosquitto \
	mosquitto_pub -h proxy.test.net -t 't/xyz' -m 'hello'
```

如果一切都按预期进行，订阅者应该打印出 `hello` 消息。



## 检查 HAProxy 中的粘性表

我们还可以使用如下命令检查在 HAProxy 中创建的粘性表。这需要 `socat` 命令，所以我们从 docker 主机运行它。

```
show table emqx_tcp_back" | sudo socat stdio tcp4-connect:127.0.0.1:9999
```

该命令应该打印当前连接，如下所示：

```
# table: emqx_external_tcp_listners, type: string, size:102400, used:1
0x7f930c033d90: key=subscriber1 use=0 exp=1793903 server_id=2 server_key=emqx2
```

在这个例子中，客户端 `subscriber1` 被固定连接到服务器 `emqx2`。



## 结语

至此，我们可以了解到从客户端的角度看，EMQX 集群是如何通过负载均衡器对外部提供服务的。

在本系列文章的后续内容中，我们将跟踪一个 MQTT 消息从发布者到订阅者的全过程，以便大家了解 EMQX 如何将它在集群中复制和转发。敬请期待。

## 本系列中的其它文章

- [MQTT Broker 集群详解（一）：负载均衡](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-1-load-balancing)
- [MQTT Broker 集群详解（三）：有关 EMQX 水平可扩展性的挑战与对策](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-3-challenges-and-solutions-of-emqx-horizontal-scalability)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a >
</section>
