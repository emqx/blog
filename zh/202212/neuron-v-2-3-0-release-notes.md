Neuron 2.3.0 版本现已正式发布！

除了新增数据统计、模糊搜索、页面下载日志等功能提升产品易用性外，Neuron 2.3.0 版本还新增了 CIP Ethernet/IP、Mitsubishi Melsec 1E frame E71 和 Fanuc Focas 三个协议驱动，以更强大的能力帮助工业用户实现海量工业设备的接入。

此外，自 2.3.0 版本起，集成 eKuiper 的 Neuron 版本正式命名为 NeuronEX；访问 Web 和 HTTP API 的端口统一为 7000，不再需要 7001 端口。

## 新功能提升运维体验

### 数据统计

Neuron 2.3.0 版本基于 Prometheus 的数据模型新增了数据统计功能。Prometheus 的基本原理是通过 HTTP 协议周期性抓取被监控组件的状态，任意组件只要提供对应的 HTTP 接口就可以接入监控。因此 Neuron 提供了对应接口，便可以顺利接入 Prometheus，实现对 Neuron 运行状态的监控。

目前，Neuron 已实现一些全局字段和南北向字段的统计，后续会根据需求持续增加统计字段。已支持的统计字段中部分字段的说明如下：

**全局统计字段说明**

用户可在`系统信息` → `关于`查看系统运行时长和系统状态。

| **参数**       | **说明**                                      |
| :------------- | :-------------------------------------------- |
| uptime_seconds | 显示 Neuron 运行时长，页面上以 5 s 的频率刷新 |
| core_dumped    | 显示系统运行状态是否有异常                    |

**南向统计字段说明**

| 参数                  | **说明**                                  |
| :-------------------- | :---------------------------------------- |
| last_rtt_ms           | 收发一次指令的时间间隔，以毫秒为单位      |
| send_bytes            | 发送指令的总字节数                        |
| recv_bytes            | 接收指令的总字节数                        |
| tag_reads_total       | 读取点位的总指令数，包括读失败            |
| tag_read_errors_total | 读取点位失败的总指令数                    |
| group_tags_total      | 组的总点位数                              |
| group_last_send_msgs  | 调用一次 group timer 发送的消息数         |
| group_last_timer_ms   | 调用一次 group timer 的时间，以毫秒为单位 |

**北向统计字段说明**

| **参数**              | **说明**             |
| :-------------------- | :------------------- |
| send_msgs_total       | 发送消息总条数       |
| send_msg_errors_total | 消息发送失败的总条数 |
| recv_msgs_total       | 接收消息的总条数     |

### 模糊搜索

Neuron 具备配置数十甚至上百个驱动的能力，以实现多设备的同时采集接入。在南向驱动配置界面，每个驱动 node 以卡片的形式展示。在以往的版本中，页面不具备搜索查找的功能，所以在配置数量较多的驱动 node 卡片或者 tag 后，查找某个 node 或者 tag 较为困难。为解决这一问题，Neuron 2.3.0 版本中新增模糊搜索查询功能，提升易用性。

用户可通过筛选插件类型的方式，查找使用同一插件的所有 node；也可以直接通过以 node 名称为关键字，查找某一个 node；还可以在 tag 列表中，通过以 tag 名称为关键字，查找某一个 tag。

![Neuron 驱动管理](https://assets.emqx.com/images/52e37bfe33214c8862085af2de6387c1.png)

### 页面下载日志

以往在问题排查的过程中，用户需自行到安装目录中拷贝日志文件。Neuron 2.3.0 对此进行了改进，用户在页面就可以便捷地下载日志文件，并且可以单独设置某个节点打印 debug 日志。这为用户更好地排查问题提供了便利。

用户可以将安装目录中的 logs 文件夹通过网页打包下载。同时，若想在某个节点采集数据异常的情况下单独排查某个节点的问题，Neuron 还支持通过 node 卡片上 `DEBUG 日志` 的操作打印该 node 的 debug 日志，打印约十分钟后，将自动切回默认日志等级。

### 优化离线缓存

Neuron 2.2 已支持北向应用 MQTT 的离线缓存，可将数据存储在内存中。2.3.0 版本进一步优化此功能，支持将数据存储在磁盘中，方便用户存储更大的数据量。

在 MQTT 处于离线状态时，Neuron 会将数据优先存储在内存中，待 MQTT 恢复在线状态后，再将缓存的数据发送到 MQTT Broker 中。缓存数据的大小由用户在应用配置界面中配置的 Cache size 决定。

### 其他更新

- 2.3.0 版本新增支持修改用户密码，保护用户使用 Neuron 采集设备数据的安全。
- Neuron 官方文档中新增加关于 DTU 连接示例的文档，感兴趣的用户可参考：[官方文档](https://docs.emqx.com/zh/neuron/latest/)。

## 新驱动增强接入能力

新版本增加了三个协议驱动，使得 Neuron 的工业接入能力变得更加强大。

### CIP Ethernet/IP

*EtherNet*/*IP* 是由洛克威尔自动化公司开发的工业以太网通讯协议，由 ODVA（ODVA）管理，可应用在程序控制及其他自动化的应用中，是通用工业协定（CIP）*中的一部分。EtherNet/IP 是基于标准以太网协议（IEEE 802.3）的技术，支持 TCP 与 UDP 传输协议，支持数种网络拓扑连接方式。

> 注：通用工业协定（CIP）是一种在工业设备中组织和共享数据的机制，是 CompoNet、EtherNet/IP、DeviceNet 和 ControlNet 背后的核心技术，提供通用数据组织和通用消息传递来解决各种制造应用程序问题。

### Mitsubishi Melsec 1E frame E71

三菱 Melsec 1E 框架用于使用 MELSEC 通信协议（简称 MC 协议）的 FX3G/FX3U/FX3UC 系列 PLC ENET 模块，可通过以太网使用 TCP/IP 或 UDP/IP 通信协议与模块通信。

### Fanuc FOCAS

Fanuc FOCAS 是从 Fanuc CNC 机器收集数据的标准协议。它是一种广泛采用的工业通信协议，因为许多机床制造商使用发那科 CNC 控制器来控制他们的设备。

FOCAS 库由 Fanuc CNC 提供，用于检索 CNC 内部的大部分信息。 Neuron 使用这些库通过以太网直接从控制器访问信息。通过 FOCAS 可获得的常见数据包括：CNC 状态（运行、空闲、警报）、零件计数信息、程序名称、编号、尺寸和修改日期、刀具和工件偏移、警报编号和文本、进给倍率、参数、位置数据 、主轴转速和模态数据等。

## 未来规划

### 支持模版配置实现驱动批量管理

Neuron 未来版本将解决当前版本中用户手动配置驱动节点带来的重复工作量问题。通过支持模版的配置功能减少配置的工作量，方便用户进行同一类设备的批量添加和管理，提高 Neuron 的易用性。

### 持续新增驱动

Neuron 也将持续增加新的驱动，加强协议连接能力，为工业 4.0 时代的数字化进程提供设备接入支撑。





<section class="promotion">
    <div>
        免费试用 Neuron
    </div>
    <a href="https://www.emqx.com/zh/try?product=neuron" class="button is-gradient px-5">开始试用 →</a>
</section>
