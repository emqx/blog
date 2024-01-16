在前面的文章中，我们分别介绍了 [文件描述符](https://www.emqx.com/zh/blog/emqx-performance-tuning-maximum-connections-and-file-descriptors) 以及 [TCP 的 SYN 和 Accept 队列](https://www.emqx.com/zh/blog/emqx-performance-tuning-tcp-syn-queue-and-accept-queue) 对 MQTT 连接的影响，今天我们将探讨另一种可能限制最大连接数量的情况。

以一个 8 核 4 GB 的 EMQX 节点为例，在建立大约 65536 个 MQTT 连接之后，我们可能会发现即使连接数量没有达到文件描述符限制，TCP 的 SYN 和 Accept 队列也没有溢出，MQTT 连接也无法继续建立，并且操作系统出现以下日志：

```plain
nf_conntrack: table full, dropping packet
```

这意味着当前操作系统因为连接跟踪表已满而丢弃了新的连接请求。在本文中，我们将介绍导致这一现象的原因以及如何通过调整内核参数来解决这一问题。

## 什么是连接跟踪？

连接跟踪（Connection Tracking，通常简称为 conntrack）是 Linux 内核网络堆栈的核心功能，由 nf_conntrack 模块提供。在加载 nf_conntrack 模块后，连接跟踪机制就开始工作，它会判断每个经过的数据包是否属于已有的连接，如果不属于任何已存在的连接，那么 nf_conntrack 模块就会为其新建一个 conntrack 条目，如果连接已经存在，则更新对应 conntrack 条目的状态、老化时间等信息。

我们可以通过 `conntrack` 命令查看当前跟踪的 conntrack 条目：

```bash
# Install conntrack
$ apt-get install conntrack
# List conntrack
$ conntrack -L
```

在部分操作系统中，例如 CentOS，也可以直接使用以下命令查看：

```bash
$ cat /proc/net/nf_conntrack
```

以下就是一个典型的 conntrack 条目，它记录了一个处于 ESTABLISHED 状态的存在双向数据传输的 TCP 连接的源 IP、目的 IP 等信息：

```plain
tcp 6 295 ESTABLISHED src=192.168.0.175 dst=100.125.61.10 sport=51484 dport=10180 \
src=100.125.61.10 dst=192.168.0.175 sport=10180 dport=51484 mark=0 zone=0 use=2
```

除了 TCP 这种面向连接的协议，nf_conntrack 模块同样跟踪 UDP、ICMP 这种无连接协议的数据包，所以与其说是跟踪连接，称其为跟踪数据流其实更为合适。

## 连接跟踪常见应用

连接跟踪是许多网络应用的基础，最常见的就是它在 **NAT**（Network Address Translaton，网络地址转换）中的应用。

为了让内部网络中的机器可以正常访问外部服务，我们通常需要创建一个 SNAT 规则，将出口报文的源 IP 从原始的内网 IP 替换为 NAT 网关的公网 IP。当外部服务返回响应报文时，响应报文中的目的 IP 将是 NAT 网关的 IP，为了将响应报文正确地返回给内网中的机器，NAT 网关需要将报文中的目的 IP 修改为对应的内网 IP。但我们无需再显式地创建一个与 SNAT 规则对应的 DNAT 规则，因为 nf_conntrack 模块会记录 NAT 的连接状态，NAT 地址的反向转换将根据对应的连接跟踪条目自动完成。

![01conntrackinnat.png](https://assets.emqx.com/images/c86efd226c12dcd5a58d9f0fb3c269fe.png)

利用 NAT 提供服务的 Docker 的 Bridge 网络、Kubernetes Service 和四层负载均衡 LVS 等网络服务和应用都依赖连接跟踪机制。

连接跟踪的另一个常见应用是**有状态防火墙**。在这之前的无状态防火墙，只会独立地审查传入传出的数据包，而不考虑数据包是否是一次会话或连接的一部分，所以只能设置一些简单的规则，比如丢弃或允许 80 端口的 SYN 报文。

相比之下，状态防火墙可以根据连接跟踪的状态信息来审查数据包。它不仅考虑数据包的内容，还考虑数据包在整个连接中的上下文。

例如当我们编写了一个 “允许本机连接 122.112.202.251” 的规则时，无需再借助其他策略显式地允许来自 122.112.202.251 的响应流量。而在无状态防火墙中，我们必须额外添加一个 “允许来自 122.112.202.251 的所有流量” 这种存在一定风险的规则。

Linux 中常用的防火墙管理工具 iptables 以及构建在 iptables 之上的 ufw、firewalld，其底层都依赖于连接跟踪机制。

## 连接跟踪的限制与优化

Linux 内核使用一个哈希表来存储连接跟踪条目，哈希表由 bucket 组成，每个 bucket 包含一个双向链表，每个链表都能够存放若干个连接跟踪条目。一个连接对应一个连接跟踪条目，但该连接跟踪条目将被两次添加到哈希表中，分别表示数据流的原始方向和回复方向[^1]。

![02conntracktable.png](https://assets.emqx.com/images/704bf8d96f4bff8fbec5c846015f16e1.png)

每个 conntrack 条目都会占用一定的内存，所以操作系统不会无限制地存储 conntrack 条目。

默认的 conntrack 条目最大数量可能无法满足我们的连接需要。我们可以使用内核参数 `net.netfilter.nf_conntrack_max` 调整允许分配的连接跟踪条目的最大数量。

相应地，我们还需要使用 `net.netfilter.nf_conntrack_buckets` 一并调整哈希表的大小，也就是 buckets 的最大数量。`nf_conntrack_max` 和 `nf_conntrack_buckets` 共同决定了 bucket 中链表的平均长度。

每收到一个数据包，Linux 内核都将进行以下操作：

1. 根据数据包中的元组信息（源 IP、源端口、协议号等）计算出哈希值，以此确定一个 bucket 的位置。
2. 遍历该 bucket，查找是否有匹配的 conntrack 条目，无则创建新条目，有则更新原始条目信息。

第一步中哈希计算的时间相对固定并且很短，但在第二步中， bucket size 越大，遍历所需要的时间也就越长。出于 conntrack 性能考虑，bucket size 越小越好。通常我们都遵循 Linux 内核的建议将 bucket size 设置为 1，最大也不宜超过 8。

Linux 内核从 5.15 版本开始，默认将 `nf_conntrack_max` 设置为与 `nf_conntrack_buckets` 相同的值，即连接跟踪表满时 bucket 中链表的平均长度将会是 2。更早之前的内核版本，默认将 `nf_conntrack_max` 设置为 `nf_conntrack_buckets` 的 4 倍，这意味着当连接跟踪表满时 bucket 中链表的平均长度将是 8。

`nf_conntrack_buckets` 默认值的计算规则随着内核版本的迭代发生了多次变化，在较新的内核版本中，例如 5.15，当系统内存大于 4 GB 时，`nf_conntrack_buckets` 默认为 262144；当系统内存小于等于 4GB 但大于 1 GB 时，`nf_conntrack_buckets` 默认为 65536；当系统内存小于 1  GB 时，`nf_conntrack_buckets` 的默认值将取决于实际的内存大小[^2]。

简单起见，我们可以使用以下命令直接查看当前生效的值：

```bash
$ cat /proc/sys/net/netfilter/nf_conntrack_buckets
$ cat /proc/sys/net/netfilter/nf_conntrack_max
```

如果连接跟踪表已满，Linux 内核将由于无法为新连接分配 conntrack 条目而丢弃新到达的报文，例如 TCP 连接的 SYN 握手报文，这就导致了我们观察到的连接失败现象。

除了查看系统日志以外，我们还可以通过以下方式确认：

1. 查看当前跟踪的 conntrack 条目数量是否已经达到了最大限制：

   ```bash
   # Command 1
   $ sudo sysctl net.netfilter.nf_conntrack_count
   # Command 2
   $ sudo conntrack -C
   ```

2. 使用 conntrack 命令查看 drop 计数是否增加：

   ```bash
   $ sudo conntrack -S
   ```

在确认原因后，我们通常有两种解决办法：

### 方法 1 - 关闭 nf_conntrack 模块

根据前面的介绍可以得知，conntrack 主要用于 NAT、状态防火墙等应用。所以如果我们可以确认没有任何应用依赖 conntrack，那么可以直接关闭连接跟踪机制，这是一劳永逸的办法。

比如我们使用云服务器在内网环境中部署了一个 EMQX 集群，公网流量从 LB 流入，并且使用云厂商提供的安全组策略替代了防火墙。由于 EMQX 不直接暴露在公网，也不需要 NAT 转发和防火墙，所以我们可以使用以下命令卸载 EMQX 所在机器中的 nf_conntrack 模块：

```bash
$ modprobe -r nf_conntrack
```

### 方法 2 - 增加 conntrack 表大小

如果有 Docker 等应用正在依赖 conntrack 提供服务，我们无法直接关闭它，那么就需要根据预期的连接数调整连接跟踪表的大小，我们可以使用 sysctl 命令进行临时性的修改：

```bash
$ sysctl -w net.netfilter.nf_conntrack_max=1048576
$ sysctl -w net.netfilter.nf_conntrack_buckets=1048576
```

如果内核版本较低，我们可能无法直接修改 `nf_conntrack_bucket` 参数，那么可以借助以下命令修改：

```bash
$ echo 262144 > /sys/module/nf_conntrack/parameters/hashsize
```

如果我们想要改动永久生效，那么可以在 `/etc/sysctl.conf` 文件末尾添加以下两行配置：

```bash
net.netfilter.nf_conntrack_max = 1048576
net.netfilter.nf_conntrack_buckets = 1048576
```

不必担心以上设置会导致 conntrack 条目占用太多内存，运行以下命令：

```bash
$ cat /proc/slabinfo | head -n2; cat /proc/slabinfo | grep nf_conntrack
slabinfo - version: 2.1
# name            <active_objs> <num_objs> <objsize> <objperslab> <pagesperslab> : tunables <limit> <batchcount> <sharedfactor> : slabdata <active_slabs> <num_slabs> <sharedavail>
nf_conntrack         144    144    320   12    1 : tunables    0    0    0 : slabdata     12     12      0
```

通过 `<objsize>` 列我们可以知道，每个 conntrack 条目占用 320 字节，如果忽略内存碎片，那么 1048576 个 conntrack 条目占用的内存大约为 320 MB，现代服务器完全可以接受这样的内存开销[^3]。

但由于在 Linux 的启动过程中，sysctl 参数设置发生在 nf_conntrack 模块加载之前，所以仅仅将`nf_conntrack_max` 等参数的配置写入 `/etc/sysctl.conf` 中并不能直接令其生效。这也是 sysctl 的一个已知问题[^4]。

想要解决这个问题，我们可以在 `/etc/udev/rules.d` 中创建一个 `50-nf_conntrack.rules` 文件，然后添加以下 udev 规则，表示仅在 nf_conntrack 模块加载时才执行相应的参数设置：

```plain
ACTION=="add", SUBSYSTEM=="module", KERNEL=="nf_conntrack", \
  RUN+="/usr/lib/systemd/systemd-sysctl --prefix=/net/netfilter"
```

完成以上修改后，我们可以重启系统以验证改动是否生效。

### 连接跟踪条目的老化时间

除了 `nf_conntrack_max` 和 `nf_conntrack_buckets` 以外，运行以下命令，我们还将看到许多其他与 nf_conntrack 相关的内核参数：

```bash
$ sysctl -a | grep nf_conntrack_tcp_timeout
net.netfilter.nf_conntrack_tcp_timeout_close = 10
net.netfilter.nf_conntrack_tcp_timeout_close_wait = 60
net.netfilter.nf_conntrack_tcp_timeout_established = 432000
net.netfilter.nf_conntrack_tcp_timeout_fin_wait = 120
net.netfilter.nf_conntrack_tcp_timeout_last_ack = 30
net.netfilter.nf_conntrack_tcp_timeout_max_retrans = 300
net.netfilter.nf_conntrack_tcp_timeout_syn_recv = 60
net.netfilter.nf_conntrack_tcp_timeout_syn_sent = 120
net.netfilter.nf_conntrack_tcp_timeout_time_wait = 120
net.netfilter.nf_conntrack_tcp_timeout_unacknowledged = 300
```

熟悉 TCP 的朋友不难看出，CLOSE-WAIT、FIN-WAIT 这些都是 TCP 的连接状态，这些 timeout 参数表示如果没有新的数据包到达，不同 TCP 连接状态下的跟踪条目可以维持的最大时间。

理论上，我们可以缩短这些老化时间来加快连接跟踪条目的回收速度，提高连接跟踪表的利用率。例如 `nf_conntrack_tcp_timeout_established` 的默认值是 432000 秒，这意味着一个已建立的 TCP 连接可以连续 5 天没有任何报文交互而内核仍为其保留跟踪条目。

一般我们可以将其缩小为 6 小时：

```bash
$ sysctl -w net.netfilter.nf_conntrack_tcp_timeout_established = 21600
```

如果想要修改永久生效，可以将配置写入 `/etc/sysctl.conf`：

```bash
$ echo 'net.netfilter.nf_conntrack_tcp_timeout_established=21600' >> /etc/sysctl.conf
```

但需要注意，其他大部分老化时间的默认值都与 TCP 协议规范保持一致，这些默认值的确定通常都经过了复杂的考量。所以除非你能够确定改动可能带来的影响，否则一般不建议修改它们。

## 总结

Linux 的连接跟踪机制是许多网络应用的基础，但它可能影响我们的连接建立，所以需要及时调整连接跟踪表的最大大小，同时也要注意避免过大的 bucket 给网络性能带来负面影响。

缩短连接跟踪条目的老化时间理论上可以提高连接跟踪表的利用率，但草率的修改可能带来意想不到的副作用。

如果可以确认没有任何应用依赖连接跟踪机制，那么直接关闭它是最简单的办法。

以上就是 Linux 中连接跟踪的调优指南。在后续的博客中，我们将继续带来更多 Linux 系统中影响 EMQX 性能表现的内核参数的优化指南。

[^1]: [Connection tracking (conntrack) - Part 2: Core Implementation](https://thermalcircle.de/doku.php?id=blog:linux:connection_tracking_2_core_implementation)
[^2]: [nf_conntrack code in the Linux kernel](https://github.com/torvalds/linux/blob/0dd3ee31125508cd67f7e7172247f05b7fd1753a/net/netfilter/nf_conntrack_core.c#L2673)
[^3]: [Netfilter Conntrack Memory Usage](https://johnleach.co.uk/posts/2009/06/17/netfilter-conntrack-memory-usage/)
[^4]: [sysctl.d(5) - Linux manual page](https://man7.org/linux/man-pages/man5/sysctl.d.5.html)



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
