EMQ X 在支持客户的过程中，了解到有客户使用 Nginx 做[负载均衡](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-2-sticky-session-load-balancing)，Docker 容器手动加入集群的方式运行 EMQ 集群，现将主要过程记录下来。

## 业务需求

- 使用 Nginx 作为反向代理
- Nginx 需要提前分配好代理 server 的地址
- 使用 Docker 容器运行 EMQ
- EMQ 自动重启
- EMQ 重启后自动集群

## 配置

### Nginx 配置

```
$ cat /etc/nginx/tcpstream.conf## tcp LB  and SSL passthrough for backend ##stream {
    upstream mqtt_broker {
        server 127.0.0.1:21871; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21872; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21873; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21874; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21875; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21881; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21891; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21882; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21892; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21883; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21893; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21884; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21894; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21885; #max_fails=5 fail_timeout=30s;
        server 127.0.0.1:21895; #max_fails=5 fail_timeout=30s;
    }

log_format basic '$proxy_protocol_addr - $remote_addr [$time_local] '
                 '$protocol $status $bytes_sent $bytes_received '
                 '$session_time "$upstream_addr" '
                 '"$upstream_bytes_sent" "$upstream_bytes_received" "$upstream_connect_time"';

    access_log /var/log/nginx/access.log basic;
    error_log  /var/log/nginx/error.log;

    server {
        listen 8884 ssl; # proxy_protocol;
        proxy_next_upstream on;
        #proxy_bind $remote_addr transparent;
        proxy_ssl off;
        proxy_pass mqtt_broker;
        proxy_protocol on;
        #ssl_on;
        # adding some extra proxy settings
        proxy_timeout 350s;
        #proxy_buffer_size 128k;

        #ssl_certificate /etc/nginx/certs/solace.pem;
        #ssl_certificate_key /etc/nginx/certs/solace.pem;
        ssl_certificate /etc/nginx/certs/cert.pem;
        ssl_certificate_key /etc/nginx/certs/key.pem;
        #ssl_verify_client off;

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers HIGH:!aNULL:!MD5;
    }
}
```

### Docker 配置

客户自行编译的 Docker image，并非使用 EMQ 提供的官方镜像。

Dockerfile 目录如下：

```
$ ll /opt/Docker/总用量 28
-rw-r--r--  1 alexeyp emq      620 10月 22 17:26 Dockerfile
lrwxrwxrwx  1 alexeyp emq       13 10月 24 13:59 emqttd -> emqttd.2.3.11
drwxr-xr-x 10 alexeyp emq      110 10月 24 14:27 emqttd.2.3.11
-rwxr-xr-x  1 alexeyp emq     3463 10月 26 05:03 StartEmqInstance.sh
-rwxr-xr-x  1 alexeyp alexeyp  270 10月 25 10:46 status.sh
```

Dockerfile:

```
$ cat DockerfileFROM centos:latest

RUN yum -y update

EXPOSE 60000-65000

WORKDIR /opt/emqttd
ADD ./emqttd /opt/emqttd
ADD ./vsparc.rpm /tmp/vsparc.rpm
ADD ./StartEmqInstance.sh /opt/emqttd/StartEmqInstance.sh

RUN yum install -y epel-release
RUN yum install -y which less sed net-tools telnet gtest /tmp/vsparc.rpm

ENV TZ Australia/Melbourne

CMD bash /opt/emqttd/StartEmqInstance.sh && bash
```

可以看到 Docker 容器启动后会执行一个 StartEmqInstance.sh 的脚本，查看该脚本:

```
$ cat StartEmqInstance.sh#!/bin/bashDIR=$(dirname $0)
HOSTNAME=$(hostname -s)

function adjust_instance()
{
    local INST=$1
    local INST_ROOT=$2

    cat $INST_ROOT/etc/emq.conf | \
       sed -re "s/^node\.name\s*=.*$/node.name = emq$INST@127.0.0.1/" | \
       #sed -re "s/^cluster\.name\s*=.*$/cluster.name = $HOSTNAME/" | \
       sed -re "s/^listener\.tcp\.external\s*=.*$/listener.tcp.external = 0.0.0.0:6188$INST/" | \
       sed -re "s/^listener\.tcp\.external1\s*=.*$/listener.tcp.external1 = 0.0.0.0:6189$INST/" | \
       sed -re "s/^listener\.tcp\.external2\s*=.*$/listener.tcp.external2 = 0.0.0.0:6187$INST/" | \
       sed -re "s/^listener\.tcp\.internal\s*=.*$/listener.tcp.internal = 127.0.0.1:6298$INST/" | \
       sed -re "s/^listener\.ssl\.external\s*=.*$/listener.ssl.external = 6288$INST/" | \
       sed -re "s/^listener\.ws\.external\s*=.*$/listener.ws.external = 6208$INST/" | \
       sed -re "s/^listener\.wss\.external\s*=.*$/listener.ws.external = 6308$INST/" | \
       sed -re "s/^listener\.api\.mgmt\s*=.*$/listener.api.mgmt = 6408$INST/" | \
       sed -re "s/^(##\s)?listener\.tcp\.external\.proxy_protocol\s=.*$/listener.tcp.external.proxy_protocol = on/" | \
       sed -re "s/^(##\s)?listener\.tcp\.external1\.proxy_protocol\s=.*$/listener.tcp.external1.proxy_protocol = on/" | \
       sed -re "s/^(##\s)?listener\.tcp\.external2\.proxy_protocol\s=.*$/listener.tcp.external2.proxy_protocol = on/" | \
       sed -re "s/^(##\s)?listener\.tcp\.external\.proxy_protocol_timeout\s=.*$/listener.tcp.external.proxy_protocol_timeout = 30s/" | \
       sed -re "s/^(##\s)?listener\.tcp\.external1\.proxy_protocol_timeout\s=.*$/listener.tcp.external1.proxy_protocol_timeout = 30s/" | \
       sed -re "s/^(##\s)?listener\.tcp\.external2\.proxy_protocol_timeout\s=.*$/listener.tcp.external2.proxy_protocol_timeout = 30s/" | \
       sed -re "s/^(##\s)?node.dist_listen_min\s*=.*$/node.dist_listen_min = 6000$INST/" | \
       sed -re "s/^(##\s)?node.dist_listen_max\s*=.*$/node.dist_listen_max = 6000$INST/" | \
       cat - > $INST_ROOT/etc/emq.conf.new
    mv $INST_ROOT/etc/emq.conf.new $INST_ROOT/etc/emq.conf
}

function cluster_instance()
{
    local INST=$1

    for DEST in 1 2 3 4 5; do
        if [ $DEST == $INST ]; then
            continue;
        fi
        DEST_NODE="emq$DEST@127.0.0.1"
        RESULT=$(/opt/emqttd/bin/emqttd_ctl cluster join $DEST_NODE 2>&1)
        echo "$RESULT"
        echo "$RESULT" | grep -E 'successfully|already' > /dev/null
        RC=$?
        [ $RC == 0 ] && break
    done
}

cd "$DIR"

if [ "$EMQ_INSTANCE_NUMBER" == "" ]; then
    echo "Environment variable EMQ_INSTANCE_NUMBER(1..10) is not set."
    echo "eMQ instance name is not configured."
    exit 1
else
    adjust_instance $EMQ_INSTANCE_NUMBER $DIR
fi

function run_application()
{
    local CMD="$1"
    local RC=1
    while [ $RC != 0 ]; do
        $CMD
        RC=$?
        echo "### Exited: $CMD"
        echo "### rc = $RC"
        #[ $RC != 0 ] && sleep 3
        RC=1
    done
    echo "### Done: $CMD"
}

function start_node()
{
    bin/emqttd start
    STARTED=0
    while [ $STARTED == 0 ]; do
        sleep 1
        /opt/emqttd/bin/emqttd_ctl status | grep "is running"
        [ $? == 0 ] && break
    done
    cluster_instance $EMQ_INSTANCE_NUMBER > /tmp/cluster_instance.log
}

start_node
sleep 5
run_application "/usr/local/bin/emqtt-stats-collector" &#waitIDLE_TIME=0
while [[ $IDLE_TIME -lt 5 ]]
do
    IDLE_TIME=$((IDLE_TIME+1))
    if [[ ! -z "$( /opt/emqttd/bin/emqttd_ctl status|grep 'is running'|awk '{print $1}')" ]]; then
        IDLE_TIME=0
    else
        echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:emqttd not running, waiting for recovery in $((60-IDLE_TIME*5)) seconds"
    fi
    sleep 5
done

echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:emqttd exit abnormally"
exit 1
```

脚本内容稍多而且有些复杂，需要结合 `start.sh` 脚本和 `etc/emq.conf`一起看

```
$ cat start.sh#!/bin/bashfor INST in 1 2 3 4 5
do
    docker ps | grep -E "\sinstance_$INST$"
    if [ $? != 0 ]; then
        #docker run -itd ---ulimit nofile=1048576 -restart=always -v /opt/Docker/emqtt/emq$INST/data/mnesia:/opt/emqttd/data/mnesia  -e EMQ_INSTANCE_NUMBER=$INST --name=instance_$INST --network host emq:test &
        docker run -itd --ulimit nofile=1048576 -e EMQ_INSTANCE_NUMBER=$INST --name=instance_$INST --network host emq:latest &
    fi
done

wait
```

### EMQ 配置

```
etc/emq.conf`的全文就不贴出来了，主要是增加了两个 tcp 监听端口，并且关闭了`listener.tcp.external.tune_buffer
$ cat etc/emq.conf......
##--------------------------------------------------------------------

listener.tcp.external = 0.0.0.0:21881

listener.tcp.external.acceptors = 16

listener.tcp.external.max_clients = 512000

listener.tcp.external.access.1 = allow all

listener.tcp.external.proxy_protocol = on

listener.tcp.external.proxy_protocol_timeout = 30s

listener.tcp.external.backlog = 1024

listener.tcp.external.send_timeout = 15s

listener.tcp.external.send_timeout_close = on
## listener.tcp.external.tune_buffer = on

listener.tcp.external.nodelay = true

listener.tcp.external.reuseaddr = true
##--------------------------------------------------------------------

listener.tcp.external1 = 0.0.0.0:21891

listener.tcp.external1.acceptors = 16

listener.tcp.external1.max_clients = 512000

listener.tcp.external1.access.1 = allow all

listener.tcp.external1.proxy_protocol = on

listener.tcp.external1.proxy_protocol_timeout = 30s

listener.tcp.external1.backlog = 1024

listener.tcp.external1.send_timeout = 15s

listener.tcp.external1.send_timeout_close = on

## listener.tcp.external1.tune_buffer = on

listener.tcp.external1.nodelay = true

listener.tcp.external1.reuseaddr = true

##--------------------------------------------------------------------

listener.tcp.external2 = 0.0.0.0:21871

listener.tcp.external2.acceptors = 16

listener.tcp.external2.max_clients = 512000

listener.tcp.external2.access.1 = allow all

listener.tcp.external2.proxy_protocol = on

listener.tcp.external2.proxy_protocol_timeout = 30s

listener.tcp.external2.backlog = 1024

listener.tcp.external2.send_timeout = 15s

listener.tcp.external2.send_timeout_close = on

## listener.tcp.external2.tune_buffer = on

listener.tcp.external2.nodelay = true

listener.tcp.external2.reuseaddr = true
......
```

## 业务分析

### Docker 容器初始化

Docker 容器创建之后，`StartEmqInstance.sh`执行`adjust_instance()`将`etc/emq.conf`中监听的端口修改为Nginx 的代理 server

```
 sed -re "s/^node\.name\s*=.*$/node.name = emq$INST@127.0.0.1/" | \
 sed -re "s/^listener\.tcp\.external\s*=.*$/listener.tcp.external = 0.0.0.0:6188$INST/" 
 sed -re "s/^listener\.tcp\.external1\s*=.*$/listener.tcp.external1 = 0.0.0.0:6189$INST/" 
 sed -re "s/^listener\.tcp\.external2\s*=.*$/listener.tcp.external2 = 0.0.0.0:6187$INST/" 
 sed -re "s/^listener\.tcp\.internal\s*=.*$/listener.tcp.internal = 127.0.0.1:6298$INST/" 
```

并通过 `join` 命令来实现集群功能

```
function cluster_instance()
{
    local INST=$1

    for DEST in 1 2 3 4 5; do
        if [ $DEST == $INST ]; then
            continue;
        fi
        DEST_NODE="emq$DEST@127.0.0.1"
        RESULT=$(/opt/emqttd/bin/emqttd_ctl cluster join $DEST_NODE 2>&1)
        echo "$RESULT"
        echo "$RESULT" | grep -E 'successfully|already' > /dev/null
        RC=$?
        [ $RC == 0 ] && break
    done
}
```

循环检查 EMQ 的状态，当 EMQ 停止了之后退出容器

```
IDLE_TIME=0
while [[ $IDLE_TIME -lt 5 ]]
do
    IDLE_TIME=$((IDLE_TIME+1))
    if [[ ! -z "$( /opt/emqttd/bin/emqttd_ctl status|grep 'is running'|awk '{print $1}')" ]]; then
        IDLE_TIME=0
    else
        echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:emqttd not running, waiting for recovery in $((60-IDLE_TIME*5)) seconds"
    fi
    sleep 5
done

echo "['$(date -u +"%Y-%m-%dT%H:%M:%SZ")']:emqttd exit abnormally"
exit 1
```

### 访问

客户端通过 SSL 方式连接 <Nginx IP:8884> 地址，Nginx 将连接以 TCP 方式负载到 EMQ 节点。

PS：关于 Nginx 如何反向代理 tcp 和 ssl 的设置，可以参考 EMQ X 消息服务器 Nginx 反向代理

### 自动重启和自动集群

容器启动后通过`StartEmqInstance.sh`脚本查询 EMQ 的状态，当 EMQ 停止时退出容器，配合`--restart=always`来达到重启容器的目的。

EMQ 将集群信息储存在`data/mnesia`中，将容器的中的目录映射到宿主机，当容器重启之后会读取宿主机映射的相关目录，实现重启后自动集群。

## 存在问题

- Docker 的 host 网络模式使用宿主机的网络，当宿主机有其他业务在执行的时候，容易出现端口冲突

## 解决方案

- 修改`/proc/sys/net/ipv4/ip_local_port_range`指定系统分配的端口为 `1024 60000`，然后将 EMQ 的业务端口分配为 60000 之后的端口

## 实践案例

建议使用 kubernetes 来编排 docker 容器：

- EMQ 可以通过`kube-apiserver`来实现自动集群的功能。
- 该客户目前只是在单机部署docker集群，使用 kubernetes 可以轻易实现多个节点之间部署集群。
- kubernetes 的`deployment`可以监控`emqx pod`的状态，实现自动重启、弹性扩容等功能。
- 每个`emqx pod`都有独立的虚拟 IP，不会出现端口冲突的问题。
- kubernetes 的`Service`可以实现固定 IP 和负载均衡的需求，在 `Service` 创建的请求中，可以通过设置 `spec.clusterIP` 字段来指定自己的集群 IP 地址，将 Nginx 的代理 server 设置成`clusterIP`即可，`Service`可自行实现负载均衡。
