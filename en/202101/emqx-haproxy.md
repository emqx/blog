
[HAProxy](https://www.haproxy.org/)  is free, open source software that provides a high availability load balancer and proxy server for TCP and HTTP-based applications that spreads requests across multiple servers. It is written in C and has a reputation for being fast and efficient (in terms of processor and memory usage). [^1]

## Preparation

**Software versions**

- Ubuntu 18.04
- EMQ X Broker v4.2.5
- HAProxy 2.2+

**Machine allocation**

- 172.16.239.107: HAProxy
- 172.16.239.108: EMQ X Node 1
- 172.16.239.109: EMQ X Node 2


## Installation

### EMQX

Refer to [EMQ X Broker](https://www.emqx.io/downloads#broker)

```bash
wget https://www.emqx.io/downloads/broker/v4.2.5/emqx-ubuntu18.04-4.2.5-x86_64.zip

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

## Configuration

### EMQX

Modify `emqx/etc/emqx.conf` configuration file, and same for the other machine.

```
## Modify the node name
node.name = emqx@172.16.239.108

## Modify the cluster strategy to static, and no need to add nodes manually any more
cluster.discovery = static

## All cluster nodes
cluster.static.seeds = emqx@172.16.239.108, emqx@172.16.239.109

## To obtain an IP address, you need to set the proxy_protocol
listener.tcp.external.proxy_protocol = on

```

### HAProxy

Modify `/etc/haproxy/haproxy.cfg `.

Add TCP backend configuration.

```
backend backend_emqx_tcp
    mode tcp
    balance roundrobin
    server emqx_node_1 172.16.239.108:1883 check-send-proxy send-proxy-v2 check inter 10s fall 2 rise 5
    server emqx_node_2 172.16.239.109:1883 check-send-proxy send-proxy-v2 check inter 10s fall 2 rise 5
```

Add dashboard backend configuration.

```
backend backend_emqx_dashboard
    balance roundrobin
    server emqx_node_1 172.16.239.108:18083 check
    server emqx_node_2 172.16.239.109:18083 check

```

Add TCP frontend configuration.

```
frontend frontend_emqx_tcp
    bind *:1883
    option tcplog
    mode tcp
    default_backend backend_emqx_tcp
```

Add dashboard frontend configuration.

```
frontend frontend_emqx_dashboard
    bind *:18083
    option tcplog
    mode tcp
    default_backend backend_emqx_dashboard
```

## Run

### EMQX

```bash
$ ./bin/emqx start

## Check the cluster status
$ ./bin/emqx_ctl cluster status

Cluster status: #{running_nodes =>
                      ['emqx@172.16.239.108','emqx@172.16.239.109'],
                  stopped_nodes => []}
```

### HAProxy

```bash
$ sudo service haproxy start
```

You can access the dashboard via `18083` now.

![dashboard.png](https://static.emqx.net/images/65ad1bec10a4515577e75e8b120c9a49.png)

Connect to the cluster via `1883`. The connection status can be checked in the dashboard or by executing the command on the node.

```bash
$ ./bin/emqx_ctl clients list
```

## Certificate

If you need TLS termination, you need to prepare the `emqx.key` and `emqx.crt` files first and then merge them to produce the `emqx.pem` file.

```bash
$ cat emqx.crt emqx.key > emqx.pem
```

Then just add the following configuration.

```
frontend frontend_emqx_tcp
    bind *:8883 ssl crt /opt/certs/emqx.pem no-sslv3
    option tcplog
    mode tcp
    default_backend backend_emqx_tcp
```



So far, we have completed the build and use of the EMQ X cluster based on HAProxy. For more detailed use of HAProxy, see [HAProxy Documentation](https://cbonte.github.io/haproxy-dconv/2.2/intro.html).



[^1]: https://en.wikipedia.org/wiki/HAProxy