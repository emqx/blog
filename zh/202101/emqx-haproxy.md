负载均衡器（LB）负责分发设备的 MQTT 连接与消息到 EMQ X 集群，采用 LB 可以提高 EMQ X 集群可用性、实现负载平衡以及动态扩容。

[HAProxy](https://www.haproxy.org/)  是一款使用 C 语言编写的自由及开放源代码软件，其提供高可用性、负载均衡，以及基于 TCP 和 HTTP 的应用程序代理，它是免费、快速并且可靠的一种解决方案。

本文将介绍如何基于 HAProxy 部署 EMQ X 集群并在 HAProxy 上终结 SSL 连接，这种部署模式下 EMQ X 单集群可轻松支持数百万设备。

## 准备

软硬件版本

- Ubuntu 18.04
- EMQ X Broker v4.2.5
- HAProxy 2.2+

机器分配

- 172.16.239.107：HAProxy
- 172.16.239.108：EMQ X 节点 1
- 172.16.239.109：EMQ X 节点 2


## 安装

### EMQX

参考 [EMQ X Broker](https://www.emqx.com/zh/downloads?product=broker)

```bash
wget https://www.emqx.com/zh/downloads/broker/v4.2.5/emqx-ubuntu18.04-4.2.5-x86_64.zip

unzip emqx-ubuntu18.04-4.2.5-x86_64.zip
```

### HAProxy

```bash
sudo apt-get update
sudo apt-get install software-properties-common -y
sudo add-apt-repository -y ppa:vbernat/haproxy-2.2
sudo apt-get update
sudo apt-get install -y haproxy=2.2.\*
```

## 配置

### EMQX

修改 `emqx/etc/emqx.conf` 配置文件，另一台同理

```
## 修改节点名
node.name = emqx@172.16.239.108

## 修改集群策略为static，无需手动添加节点了
cluster.discovery = static

## 所有集群节点	
cluster.static.seeds = emqx@172.16.239.108, emqx@172.16.239.109

## 为了获取 IP 地址，需要设置 proxy_protocol
listener.tcp.external.proxy_protocol = on

```

### HAProxy

修改 `/etc/haproxy/haproxy.cfg `

添加 TCP backend 配置

```
backend backend_emqx_tcp
    mode tcp
    balance roundrobin
    server emqx_node_1 172.16.239.108:1883 check-send-proxy send-proxy-v2 check inter 10s fall 2 rise 5
    server emqx_node_2 172.16.239.109:1883 check-send-proxy send-proxy-v2 check inter 10s fall 2 rise 5
```

添加 dashboard backend 配置

```
backend backend_emqx_dashboard
    balance roundrobin
    server emqx_node_1 172.16.239.108:18083 check
    server emqx_node_2 172.16.239.109:18083 check

```

添加 TCP frontend 配置

```
frontend frontend_emqx_tcp
    bind *:1883
    option tcplog
    mode tcp
    default_backend backend_emqx_tcp
```

添加 dashboard frontend 配置

```
frontend frontend_emqx_dashboard
    bind *:18083
    option tcplog
    mode tcp
    default_backend backend_emqx_dashboard
```

## 运行

### EMQX

```bash
$ ./bin/emqx start

## 查看集群状态
$ ./bin/emqx_ctl cluster status

Cluster status: #{running_nodes =>
                      ['emqx@172.16.239.108','emqx@172.16.239.109'],
                  stopped_nodes => []}
```

### HAProxy

```bash
$ sudo service haproxy start
```

此时便可以通过 `18083` 访问 dashboard

![dashboard.png](https://static.emqx.net/images/0f815d5597514fd6f26aeba7ead041a7.png)

通过 `1883` 连接到集群，连接情况可以在 dashboard 查看，或者在节点上执行命令

```bash
$ ./bin/emqx_ctl clients list
```

## 证书

如果需要 TLS 终结，先准备好 `emqx.key` 和 `emqx.crt` 文件，然后合并生成 `emqx.pem` 文件

```bash
$ cat emqx.crt emqx.key > emqx.pem
```

然后添加以下配置即可

```
frontend frontend_emqx_tcp
    bind *:8883 ssl crt /opt/certs/emqx.pem no-sslv3
    option tcplog
    mode tcp
    default_backend backend_emqx_tcp
```



至此，我们完成了基于 HAProxy 搭建 EMQ X 集群以及使用，HAProxy 更详细的使用参见 [HAProxy Documentation](https://cbonte.github.io/haproxy-dconv/2.2/intro.html)。
