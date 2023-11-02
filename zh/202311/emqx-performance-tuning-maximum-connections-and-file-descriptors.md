在对 EMQX 进行性能测试的过程中，当[客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)连接达到一定数量以后，你可能会发现 EMQX 无法接入更多连接，并且在控制台或 `/var/log/emqx/emqx.log.N` 中出现以下错误日志：

```
[error] Accept error on 0.0.0.0:1883: EMFILE (Too many open files)
```

这说明目前 EMQX 打开的文件描述符数量达到了最大限制。当然，这个限制来自操作系统，而不是 EMQX，如果我们想要突破这个限制，就需要修改操作系统中相应的内核参数。

所以在本文中，我们将介绍如何修改内核参数来增大 EMQX 可以使用的文件描述符数量。

## 什么是文件描述符

[文件描述符](https://zh.wikipedia.org/zh-hans/文件描述符) 是 Linux 系统内核为了高效管理被打开的文件而创建的索引。当我们使用以下函数调用打开一个文件时，fd 就是内核返回的文件描述符：

```
fd = open("example.txt", O_RDWR)
```

然后我们就可以通过这个 fd 对打开的文件进行各种读写操作，Linux 会根据 fd 索引到正确的文件。

不过，在 Linux 系统中，一切资源都可以看做是文件，除了我们常规理解中的文本文件、可执行文件这类普通文件，文件目录、硬件设备等也都可以看成是文件，这其中自然也包括了网络套接字（Network Socket）。

EMQX 作为一个 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，每当有新的客户端接入，EMQX 都会创建一个新的套接字以和该客户端通信，相应地，这将占用一个文件描述符。

为了避免进程或无意或恶意打开过多的文件描述符，Linux 系统通常都会限制每个用户、每个进程能够打开的文件描述符数量。但默认的大小限制，显然难以满足有大量设备连接的 MQTT 服务器的需要。所以，修改内核参数成了我们必然的选择。

## 如何修改文件描述符的最大数量限制

在 Linux 系统中，一个进程最终可用的文件描述符的最大数量，受到多个内核参数或配置文件的影响。它们分别是：

### /proc/sys/fs/file-max

`/proc/sys/fs/file-max` 中定义的值决定了整个系统可用的文件描述符的最大数量，我们可以通过以下命令来查看当前的限制：

```
cat /proc/sys/fs/file-max
```

如果当前值小于我们的期望值，我们可以运行以下命令来修改它：

```
echo <Number> > /proc/sys/fs/file-max
```

或者

```
sysctl -w fs.file-max = <Number>
```

上面这两个命令都可以让改动立即生效，但缺点是改动仅在当前会话有效，一旦用户注销或者系统重启，我们改动就会失效。如果想让修改永久有效，我们可以打开 `/etc/sysctl.conf` 文件，然后添加以下内容：

```
fs.file-max = <Number>
```

保存退出后执行以下命令使改动立即生效：

```
sysctl -p
```

通常我们建议将最大文件描述符的数量设置得略大于目标值，避免影响系统中其他服务的正常运行。

### /proc/sys/fs/nr_open

`/proc/sys/fs/nr_open` 中定义的值决定了一个进程打开文件描述符的数量的设置上限。它并不直接作用于进程，而是决定了其他参数可以设置的最大值。它的操作与 `/proc/sys/fs/file-max` 类似，查看当前值：

```
cat /proc/sys/fs/nr_open
```

临时修改：

```
echo <Number> > /proc/sys/fs/nr_open
```

或者

```
sysctl -w fs.nr_open = <Number>
```

永久修改可以在 `/etc/sysctl.conf` 文件中添加以下一行：

```
fs.nr_open = <Number>
```

然后执行以下命令使改动立即生效：

```
sysctl -p
```

### /etc/security/limits.conf

在这个文件中，我们可以为通过 [PAM](https://en.wikipedia.org/wiki/Linux_PAM)（Pluggable Authenticaton Modules） 登录的用户设置各项资源的限制，比如进程的最大数量、打开文件描述符的最大数量等等。当我们使用 `emqx` 命令配合 `console`、`start` 等选项启动 EMQX 时，EMQX 可以打开的最大文件描述符数量就受到 `/etc/security/limits.conf` 的限制。

`limits.conf` 中的每一行都使用以下格式来描述对用户的限制：

```
<domain> <type> <item> <value>
```

`<domain>` 决定了此限制对哪些用户生效，我们可以使用用户名、组名（组名前加 @ 以和用户名区分）或者直接使用通配符 * 来限制所有用户。

`<type>` 决定这是一个软限制（Soft Limit）还是一个硬限制（Hard Limit）。软限制是当前实际的资源限制，硬限制则是软限制可以设置的上限。在 `limits.conf` 的限制生效后，只有 root 用户才能增加自己的硬限制，普通用户只能在硬限制的范围内调整软限制，或者减小硬限制。

`<item>` 用于指定资源类型，譬如 nproc 表示进程的最大数量，nofile 表示打开文件描述符的最大数量，完整的可用 `<item>` 列表可以自行查看 `/etc/security/limits.conf`。另外，我们也需注意不同资源限制之间的区别，比如 nproc 用于限制一个用户可以同时创建的进程的最大数量，但 nofile 并不是一个用户总共可以同时打开的文件描述符的最大数量，它实际上是针对该用户创建的每个进程的独立限制。

`<value>` 就是具体的限制大小。

以下是一个简单的示例，它表示 root 和 emqx 用户可以打开的文件描述符的最大数量默认均为 65535，但 root 用户可以随时突破这个限制，emqx 用户则不行。其他所有用户可以打开的文件描述符最大数量默认为 1024，但最大可以调整到 4096：

```
root soft nofile 65535
root hard nofile 65535
emqx soft nofile 65535
emqx hard nofile 65535
*    soft nofile 1024
*    hard nofile 4096
```

另外，nofile 的软硬限制都不能超过 `/proc/sys/fs/nr_open`，这是需要特别注意的地方，因为 Linux 并不会检查和限制你的修改，但一旦超过，将导致系统无法登录。

当我们完成对 `/etc/security/limits.conf` 的修改后，必须注销会话重新登录才能令改动生效。在重新登录后我们可以使用以下命令来确认改动是否成功生效：

```
ulimit -n
```

我们也可以使用 `-Sn` 和 `-Hn` 选项来单独查看当前生效的软、硬限制：

```
ulimit -Sn
ulimit -Hn
```

### ulimit -n

`/etc/security/limits.conf` 文件中的改动是永久有效的，但有时候我们可能只需要临时修改，这时我们就可以使用 ulimit 命令。刚刚我们介绍了如何使用它来查看当前的资源限制，现在我们将了解如何使用它来修改资源限制，例如，同时修改软硬限制：

```
ulimit -n <Number>
```

或者分别修改软硬限制：

```
ulimit -Sn <Number>
ulimit -Hn <Number>
```

请注意，我们永远无法让软限制超过硬限制，并且非 root 用户只能减少硬限制，只有 root 用户才能随意增加硬限制。但无论如何，通过 `ulimit` 修改的软硬限制，都不应超过 `/proc/sys/fs/nr_open`。

ulimit 命令对资源限制的改动是临时性的，它只对当前 Shell 及其创建的进程有效。譬如，当我们运行以下命令创建一个子 Shell，并在其中修改文件描述符最大数量后，这个改动并不会在父 Shell 中生效：

```
$ (ulimit -n 2000; ulimit -n)
2000
$ ulimit -n
65535
```

或者当我们使用 su 命令切换到另一个用户时，系统会创建一个新的 Shell，这也会导致我们的改动失效。在下面的例子中，我们列出了当前 Shell 的 PID 来表明这是新的 Shell：

```
$ echo "The current shell's PID is $$"
The current shell's PID is 2083
$ ulimit -n
65535
$ su - emqx
$ echo "The current shell's PID is $$"
The current shell's PID is 7837
$ ulimit -n
32768
```

这就是为什么有时我们会发现 ulimit 的改动没有生效。

以 EMQX 为例，如果我们是通过软件包或者包管理工具安装的，那么在安装时，EMQX 会自动创建一个 emqx 用户，并且在启动时切换至此用户。这意味着，我们在当前 Shell 以 emqx 以外的用户运行 ulimit 命令进行的改动，将在 EMQX 以 `emqx start` 等命令启动时，由于用户的切换而失效。此时 EMQX 的资源限制直接由 `/etc/security/limits.conf` 决定。

基于以上原因，我们通常更推荐直接修改 `/etc/security/limits.conf`。

### /etc/systemd/system.conf

`/etc/security/limits.conf` 只能为通过 PAM 登录的用户设置资源限制，它不影响 [系统服务](https://en.wikipedia.org/wiki/Systemd) 的资源限制。

所以当我们以 `sudo systemctl start emqx` 或者 `sudo service emqx start` 方式启动 EMQX 服务时，这个服务将不会受到 `/etc/security/limits.conf` 中限制的影响。

系统服务可用的最大文件描述符数量，由 `/etc/systemd/system.conf` 文件中的 DefaultLimitNOFILE 参数或者 `/usr/lib/systemd/system/<Service Name>.service` 文件中的 LimitNOFILE 参数决定。前者是应用于所有系统服务的全局默认设置，后者是每个服务可选的单独的限制，即 LimitNOFILE 会覆盖 DefaultLimitNOFILE。

`/etc/systemd/system.conf` 中的改动不仅是全局生效的，而且总是需要重启服务器才能生效，而每个服务自己的单元文件中的改动只需要运行 `sudo systemctl daemon-reload` 命令重新加载 systemd 的配置文件即可生效。所以后者也是我们更推荐的配置方式。

LimitNOFILE 与 DefaultLimitNOFILE 有相同的配置格式，以 LimitNOFILE 为例，我们可以同时设置软硬限制：

```
LimitNOFILE = <Number>
```

也可以分别设置软硬限制：

```
LimitNOFILE = <Soft Limit>:<Hard Limit>
```

当前生效的 DefaultLimitNOFILE 可以用命令 `systemctl show --property DefaultLimitNOFILE` 查看，当前生效的 LimitNOFILE 则可以用命令 `systemctl show emqx -p LimitNOFILE` 查看，不过它们都仅能查看硬限制，无法查看软限制。

EMQX 在单元文件 `/usr/lib/systemd/system/emqx.service` 中默认将 LimitNOFILE 设置为 1048576。如果我们修改了它，可以运行以下命令让改动生效：

```
systemctl daemon-reload
systemctl restart emqx
```

但注意，LimitNOFILE 的限制同样不能高于 `/proc/sys/fs/nr_open`，否则会导致服务无法启动。

## 快速验证

假设现在我们希望 EMQX 能够接入 50 万个客户端连接，我们可以这样调整：

1. 打开 `/etc/sysctl.conf`，添加以下两行：

   ```
   fs.file-max = 520000
   fs.nr_open = 510000
   ```

   运行 `sysctl -p` 使改动生效。

2. 打开 `/etc/security/limits.conf`，添加以下两行：

   ```
   emqx soft nofile 510000
   emqx hard nofile 510000
   ```

   注销会话并重新登录使改动生效。

3. 打开 EMQX 的单元文件 `/usr/lib/systemd/system/emqx.service`，修改其中的 LimitNOFILE 参数：

   ```
   LimitNOFILE = 510000
   ```

   运行 `systemctl daemon-reload` 使改动生效。

4. 启动 EMQX，`emqx start` 或 `sudo systemctl emqx start` 均可，启动成功后使用 `ps aux | grep emqx` 命令获取 EMQX 进程的 PID，然后通过以下命令即可查看当前进程生效的资源限制：

   ```
   $ cat /proc/<PID>/limits
   Limit                     Soft Limit           Hard Limit           Units 
   ...
   Max open files            510000               510000               files
   ...
   ```

## EMQX 的最大连接数限制

在正确修改以上系统参数以后，接入 EMQX 的连接数量终于达到了我们的期望。但是，只要客户端数量继续增加，那么打开的文件描述符数量仍然有可能达到操作系统修改后的限制。

由于 EMQX 的各项基础服务也会请求文件描述符，但如果客户端连接已经占用了所有可用的文件描述符，操作系统将返回 EMFILE（The per-process limit of open file descriptors has been reached）或者 ENFILE（The system limit on the total number of open files has been reached）错误，这将导致 EMQX 无法继续正常运作。

所以我们建议启用 EMQX 的最大连接数限制，由 EMQX 主动限制连接数量，确保打开的文件描述符不会超过系统的资源限制。此限制机制默认关闭，我们需要自行开启。

以 EMQX 5.3.0 为例，我们可以访问 [Dashboard](https://www.emqx.io/docs/zh/latest/dashboard/introduction.html) 的监听器页面，然后点击监听器名字进入相应的配置页面，将 Max Connections 修改为一个小于当前系统限制的值：

![EMQX Dasshboard 监听器](https://assets.emqx.com/images/8c0ae7961df6e41497fe6a92bc9e38c3.png)

## 总结

在 Linux 系统中，影响我们最终可用的文件描述符的最大数量的参数确实不少。只有在了解它们各自的用途和作用范围之后，我们才能根据不同的情况修改正确的参数。下面这张图可以帮助我们进一步厘清并记忆它们之间的关系：

![03allparameterscn.jpg](https://assets.emqx.com/images/315c684d6834f1344f7412451c182117.jpg)

在后续的博客中，我们将继续带来更多 Linux 系统中影响 EMQX 性能表现的内核参数的优化指南。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
