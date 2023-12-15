在上一篇博客（[EMQX 性能调优：最大连接与文件描述符](https://www.emqx.com/zh/blog/emqx-performance-tuning-maximum-connections-and-file-descriptors)），我们深入研究了 [MQTT 连接](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)与文件描述符之间的关系，介绍了如何修改文件描述符相关的内核参数来突破默认的最大连接数量限制。

但你可能会发现，在某些情况下，即便当前服务端的 MQTT 连接总数并未达到文件描述符限制，客户端的连接请求仍然失败。当你运行以下命令，你将看到以下 Overflowed 和 SYN Dropped 计数在不断增加：

```bash
$ watch -d 'netstat -s | grep -i "listen"'
    2091 times the listen queue of a socket overflowed
    3418 SYNs to LISTEN sockets dropped
```

本文将介绍导致这一现象的原因以及如何通过内核参数调优来解决此问题。

## SYN 队列与 Accept 队列

前文提到的这两个计数，通常意味着 SYN 队列和 Accept 队列发生了溢出，一旦溢出，客户端的正常连接就会受到影响。

所以首先，我们需要了解 SYN 队列和 Accept 队列分别是什么？

MQTT 作为构建在 TCP 之上的应用层协议，我们总是必须先建立 TCP 连接，然后才能发送 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)的 CONNECT 报文。建立 TCP 连接，需要经过三次握手：

![tcp 3 way handshake](https://assets.emqx.com/images/a8f42adf959df8ce10b57d092fca82a1.png)

1. 客户端向服务器发送 SYN（同步）报文，表示要建立连接。
2. 服务器用 SYN-ACK（同步确认）报文进行响应，表示愿意建立连接。
3. 客户端回复 ACK（Acknowledge）报文，表示已收到 SYN-ACK 报文，连接已建立。

由于网络延迟的存在，从服务端发出 SYN-ACK 报文到收到客户端回复的 ACK 报文总是需要一段时间。在这段时间内，服务端需要暂存本次连接的关键信息，例如 TCP 四元组、MSS（Maximum Segment Size，最大分段大小）和窗口缩放因子（Window Scale）。所以，Linux 内核维护了一个 SYN 队列来存放这些连接信息。

当服务端收到客户端回复的 ACK 报文，连接建立完成，就会将连接从 SYN 队列取出，然后放入同样由内核维护的 Accept 队列，直到上层应用调用 `accept()` 将连接从 Accept 队列中取出。Accept 队列在这里的主要作用是解耦了网络层和应用层，使 TCP 三次握手和实际的数据传输可以并行进行，有效提高连接请求的处理效率。

![syn queue and accept queue](https://assets.emqx.com/images/9848c1b7510f7140b833c8f22c518c41.png)

但服务端的资源是有限的，不管是 SYN 队列还是 Accept 队列，它们都有着最大长度限制。如果客户端一直只发送 SYN 报文而不回复最后的 ACK 报文，或者服务端的应用程序没有及时地调用 `accept()`，那么这两个队列就会有溢出的风险。

## SYN 队列溢出时将发生什么？

服务端在 SYN 队列溢出时的行为，主要由 `net.ipv4.tcp_syncookies` 选项决定。

由于 SYN 队列的长度总是有限的，所以一些攻击者会尝试采用发送大量 SYN 报文的方式来对服务端发起攻击，企图耗尽服务端的 SYN 队列来阻止合法连接的建立，这也就是我们常说的 SYN 泛洪攻击 (SYN Flood Attack)。

SYN Cookie 机制被设计用于解决这一问题。简单来说，当启用这一机制后，Linux 在收到 SYN 报文时将基于时间戳、四元组等信息计算出一个 Cookie，然后作为 SYN-ACK 报文的序列号后返回给客户端。客户端在 ACK 中将序列号加一返回，服务端只需要减一就可以逆推出原始的 Cookie。因此，服务端不需要再将连接请求放入 SYN 队列。

![syn cookie](https://assets.emqx.com/images/778b064d98c1871d77b553c5bda572a7.png)

但 SYN Cookie 机制也存在一些弊端：

1. Cookie 的计算并未包含 SACK（Selective Acknowledgment，选择性确认） 和 Window Scale （窗口缩放因子）这些 TCP 选项，启用 SYN Cookie 后，服务端将不会保存这些选项，所以这些功能将无法使用。虽然从 Linux 内核 v2.6.26 开始，我们可以启用 TCP Timestamps 选项（`net.ipv4.tcp_timestamps`），借助 32 Bit 时间戳的低 6 bit 来存放这些 TCP 选项，但 TCP Timestamps 需要客户端和服务端的共同支持才会真正启用。
2. 用于生成 Cookie 的 Hash 计算增加了服务端的负载。

所以目前 `net.ipv4.tcp_syncookies` 选项一共有三个可取值：

- `net.ipv4.tcp_syncookies = 0`，表示关闭 SYN Cookie 机制，如果 SYN 队列已满，那么新到的 SYN 报文将被丢弃。
- `net.ipv4.tcp_syncookies = 1`，表示 SYN Cookie 机制仅在 SYN 队列满时才正式启用。
- `net.ipv4.tcp_syncookies = 2`，表示无条件启用 SYN Cookie 机制。

不同类型和版本的操作系统中，`net.ipv4.tcp_syncookies` 的默认值可能不同，你可以运行以下命令查看当前值：

```bash
sysctl -n net.ipv4.tcp_syncookies
```

考虑到 SYN Cookie 可能带来的副作用，通常我们建议仅在 SYN 队列满时才启用 SYN Cookie（将 `net.ipv4.tcp_syncookies` 设置为 1），优先尽可能地增加 SYN 队列最大长度。运行以下命令以修改此选项：

```bash
sysctl -w net.ipv4.tcp_syncookies=1
```

### RTT 对 SYN 队列的影响

连接请求在 SYN 队列中停留的时间，基本等同于服务端发出 SYN-ACK 报文到收到客户端返回的 ACK 报文的时间。换句话说，它完全取决于报文在客户端与服务端之间的往返时间（Round Trip Time，RTT）。

RTT 越长，那么连接请求将越容易占满 SYN 队列。假设 RTT 为 200 ms，SYN 队列最大长度为 512，那么只要每秒向服务端发起连接请求的客户端数量超过 2560 个就会造成 SYN 队列溢出。

### 查看当前 SYN 队列大小

Linux 没有提供相应的内核参数供我们直接查看当前 SYN 队列大小，但通过前文我们可以知道 SYN 队列中的连接都处于 SYN-RECEIVED 状态，因此我们可以借助 netstat 命令统计 SYN-RECEIVED 状态的连接数量来间接获得当前 SYN 队列的大小：

```bash
sudo netstat -antp | grep SYN_RECV | wc -l
```

### 如何确认 SYN 队列发生溢出？

当 SYN 报文因为 SYN 队列满而被丢弃时，服务端中的以下计数会相应增加：

```bash
$ netstat -s | grep "LISTEN"
    <Number> SYNs to LISTEN sockets dropped
```

不过 SYN 报文也可能因为 Accept 队列满而被丢弃，所以还需要结合 Accept 队列的情况综合判断。

需要注意的是，在 CentOS 中，即便启用了 SYN Cookie 机制，服务端已经不会再丢弃 SYN 报文，此 SYN 丢弃计数仍然可能增加：

- SYN Cookie 设置为 1 时，如果 SYN 队列已满，那么新到的 SYN 报文仍然会使此计数增加。这可以帮助我们评估是否需要增加 SYN 队列的最大长度。
- SYN Cookie 设置为 2 时，此计数不存在任何意义。

## Accept 队列溢出时将发生什么？

服务端在 Accept 队列溢出时的行为，主要由 `net.ipv4.tcp_abort_on_overflow` 选项决定。

通常情况下，此选项的默认值为 0，即当 Accept 队列溢出时，服务端将直接丢弃第三次握手的 ACK 报文，并视作从未收到该 ACK 报文，因此服务端将重传 SYN-ACK 报文，最大重传次数由 `net.ipv4.tcp_synack_retries` 选项决定。

![accept queue over flow](https://assets.emqx.com/images/54bff4aa268174510b81be6cbd06106c.png)

虽然服务端丢弃了 ACK 报文，但是对客户端来说，三次握手已经完成，所以它可以发送后续的应用数据。不过这些携带了应用数据的 PSH 也会和 ACK 报文一样被服务端直接丢弃。由于收不到响应，客户端将不断地重传 PSH 报文，PSH 报文的最大重传次数由 `net.ipv4.tcp_retries2` 选项决定。

![accept queue over flow](https://assets.emqx.com/images/c55e42eb1ee468d9a929cc1df541388d.png)

将 `net.ipv4.tcp_abort_on_overflow` 设置为 0 的好处是如果在 SYN-ACK 或 PSH 报文达到最大重传次数前，上层应用及时地取出连接使 Accept 队列出现空位，那么连接可以直接恢复，这更有利于应对突发流量。但如果 Accept 队列过短，导致客户端和服务端过早地重传报文，也会浪费流量以及降低连接效率。

相反，如果将 `net.ipv4.tcp_abort_on_overflow` 设置为 1，那么服务端将在 Accept 队列溢出时直接向客户端返回 RST 报文来关闭连接。

![accept queue over flow](https://assets.emqx.com/images/e6e7b9c695f565f1dc1f8ace7124192d.png)

所以通常我们建议将 `net.ipv4.tcp_abort_on_overflow` 设置为 0，除非你确信服务端在短时间内无法从繁忙中恢复并且希望尽快通知客户端。

> 不同类型和版本的操作系统在这方面的行为可能不同。以上行为在 CentOS 中得到验证，但 Ubuntu 似乎采用了另一种行为模式，并且更改 `net.ipv4.tcp_abort_on_overflow` 似乎并不会改变 Ubuntu 的行为。
>
> 如果你对此感兴趣，我们在 [这里](https://github.com/emqx/bootcamp/tree/main/linux-tuning/tcp-accept-queue) 提供了用于模拟 Accept 队列溢出的示例代码和操作步骤，你可以在自己的环境中自行试验。

另外，当 Accept 队列溢出时，即使启用了 SYN Cookie 机制，服务端也不会再接受新的连接请求，即到达服务端的 SYN 报文将被直接丢弃，这会使得 SYN 丢弃计数增加。

### 查看当前 Accept 队列大小

我们可以使用 `ss` 命令来查看当前 Accept 队列的情况。对于监听状态的套接字，`ss` 命令获得的第二列 Recv-Q 表示当前 Accept 队列的大小，第二列 Send-Q 则表示 Accept 队列的最大长度：

```bash
$ ss -lnt
LISTEN   0    1024   *:1883         *:*
```

### 如何确认 Accept 队列发生溢出？

每当服务端因为 Accept 队列溢出而丢弃报文时，不管是第一次握手的 SYN 报文，还是第三次握手的 ACK 报文，又或者是 PSH 报文，服务端中的以下计数都会相应加 1：

```bash
$ netstat -s | grep "overflowed"
    <Number> times the listen queue of a socket overflowed
```

因此我们可以通过观察这个计数是否增长来判断 Accept 队列是否发生溢出。

## 如何增加 SYN 队列和 Accept 队列的大小？

Accept 队列比较简单，它的最大长度由监听函数（例如 `listen(fd, backlog)`）中的 `backlog` 参数和 `net.core.somaxconn` 这个 Linux 内核参数决定。Linux 总是取 `backlog` 和 `net.core.somaxconn` 中对的较小值作为 Accept 队列的最大长度。

在 EMQX 中，我们可以为每个监听器都单独设置 `backlog`，以默认的 TCP 监听器为例，我们只需要在 `emqx.conf` 中添加以下配置即可：

```
listeners.tcp.default {
  tcp_options {
    backlog = 1024
  }
}
```

如果想要修改其他监听器的 `backlog`，只需要使用对应的协议名和监听器名称即可：

```
listeners.[tcp | ssl | ws | wss | quic].<Listener Name> {
  tcp_options {
    backlog = 1024
  }
}
```

SYN 队列略为复杂，它的最大长度并不由某个内核参数直接决定，而是受到 `net.ipv4.tcp_max_syn_backlog`、`net.core.somaxconn` 等参数的综合影响。在不同的操作系统中，这些参数的效果还会有所差异。在 CentOS 中，SYN 队列的最大长度有着以下计算公式：

```
Max SYN Queue Size = roundup_pow_of_two(
  max(min(somaxconn, backlog, sysctl_max_syn_backlog), 8) + 1)
```

`roundup_pow_of_two(Num)` 表示将 Num 向上取整到 2 的幂。例如，当 Num 为 6，7 或 8 时，`roundup_pow_of_two(Num)` 总是返回 8。

因此，如果我们将 `somaxconn` 设置为 64，`tcp_max_syn_backlog` 设置为 128，而 `listen()` 函数的 `backlog` 设置为 256 时，那么在 CentOS 中最终 SYN 队列的最大长度将是 256。

而在 Ubuntu 中，SYN 队列的长度必须**小于** Accept 队列的最大长度，并且**小于等于** 0.75 倍的 `net.ipv4.tcp_max_syn_backlog`。我们可以转换为以下公式：

```
Max SYN Queue Size = min(min(somaxconn, backlog), 0.75 * tcp_max_syn_backlog + 1)
```

如果我们将 `somaxconn` 设置为 64，`tcp_max_syn_backlog` 设置为 512，而 `backlog` 设置为 256 时，Accept 队列的最大长度为 64，小于 0.75 倍的 `tcp_max_syn_backlog`，所以此时 SYN 队列的最大长度为 64。

如果我们将 `somaxconn` 设置为 1024，`tcp_max_syn_backlog` 设置为 256，`backlog` 设置为 512 时，Accept 队列的最大长度为 512，大于 `tcp_max_syn_backlog`，所以此时 SYN 队列的最大长度为 193。

### 验证 SYN 队列最大长度

我们可以通过以下方式来验证 SYN 队列的最大长度：

首先我们需要一个简单的 TCP 服务端，它监听 12345 端口，但从不调用 `accept()` 从 Accept 队列中获取连接。注意将 backlog 修改为你期望的值：

```
import socket
import time

def start_server(host, port, backlog):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind((host, port))
    server_socket.listen(backlog)
    
    print(f'Server is listening on {host}:{port}')
    
    while True:
        time.sleep(3)
        
if __name__ == '__main__':
    start_server('0.0.0.0', 12345, 256)
```

然后我们需要在服务端进行以下操作：

```
# 如果你使用的是 Ubuntu，那么需要关闭 SYN Cookie，以便接下来可以看到计数变化
echo 0 > /proc/sys/net/ipv4/tcp_syncookies

# 将 somaxconn 和 tcp_max_syn_backlog 设置为你期望的值
echo 64 > /proc/sys/net/core/somaxconn
echo 512 > /proc/sys/net/ipv4/tcp_max_syn_backlog

# 为服务端的 eth0 接口设置 200ms 的网络延迟，使 SYN 队列更容易溢出。
#
# 当你不再需要此延迟时，你可以运行以下命令删除它：
# sudo tc qdisc delete dev eth0 root
sudo tc qdisc add dev eth0 root netem delay 200ms
```

完成以上设置后，运行以下命令启动 TCP 服务器：

```
python3 ./server.py
```

另起一个终端窗口，运行以下命令用于观察 SYN 队列是否溢出：

```
watch -n 1 -d 'netstat -s | grep -i "listen"
```

在客户端中安装 `hping3` 工具：

```
apt-get install hping3
```

运行以下命令以指定速率发送指定数量的 SYN 报文：

```
# -S，发送 SYN 报文
# -p <Port>，指定端口
# -c <Count>，发送报文的数量
# -i u100, 以 100us 的间隔发送报文
hping3 -S -p 12345 -c 65 -i u100 <Your Hostname> 
```

如果你使用的是 Ubuntu，并且 `somaxconn` 等参数的值与以上示例保持一致，那么在运行 hping3 命令后，你将看到 SYN 丢弃计数加 1，因为此时 SYN 队列最大长度为 64。

### 令改动永久生效

`echo 64 > /proc/sys/net/core/somaxconn` 和 `sysctl -w net.core.somaxconn=64` 都只是临时性的改动，一旦用户注销或者系统重启，我们改动就会失效。如果我们确认当前值满足最终期望，那么可以将它们写入 `/etc/sysctl.conf`：

```
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 4096
```

然后运行 `sysctl -p` 使改动立即永久生效。

## 总结

在现代操作系统中， `net.ipv4.tcp_syncookies` 通常默认为 1，`net.ipv4.tcp_abort_on_overflow` 则通常默认为 0，所以除了 Accept 队列溢出导致服务端拒绝后续连接请求以外，我们很难直接观察到客户端连接失败的情况。

当 SYN Cookie 机制生效时，虽然 SYN 报文不会再被丢弃，但 TCP 的部分功能可能会受到限制，并且服务端的负载会相应增加。特别在物联网、车联网这类 RTT 较高的场景中，SYN 队列会更加容易溢出。所以及时关注 SYNs Dropped 计数并调整 SYN 队列大小是非常有必要的。

Accept 队列通常在服务端繁忙时更容易溢出，`tcp_abort_on_overflow` 等于 0 的情况下，较短的 Accept 队列可能会使客户端和服务端过早地进入报文重传，反而增加网络负载。如果 Accept 队列不断溢出，但服务端的 CPU 并未饱和，那么可以适当增大 Accept 队列。

另外，将 SYN 队列和 Accept 队列设置为一个非常非常大的值并不是一件好事。在遭受泛洪攻击或者突发流量导致服务端繁忙时，对这两个队列施加合理的大小限制反而是对服务端的保护。

在后续的博客中，我们将继续带来更多 Linux 系统中影响 EMQX 性能表现的内核参数的优化指南。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
