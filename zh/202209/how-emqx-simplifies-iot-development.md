## 引言：更加轻松地使用 EMQX 

最新发布的大规模分布式物联网 MQTT 消息服务器 [EMQX 5.0](https://www.emqx.com/zh/blog/emqx-v-5-0-released) 在[水平扩展性](https://www.emqx.com/zh/blog/how-emqx-5-0-achieves-100-million-mqtt-connections)、[消息传输稳定性](https://www.emqx.com/zh/blog/mqtt-over-quic)、[安全性](https://www.emqx.com/zh/blog/how-to-ensure-the-security-of-the-iot-platform)等方面实现了突破性的提升，为用户物联网关键业务提供了保障。在此基础上，EMQX 5.0 提供了更多便利的功能和设计以帮助用户更加轻松地使用、管理、扩展 EMQX。

本文将从可操作性、可观测性、扩展性三个方面，与大家分享 EMQX 5.0 在运维监测、问题排查以及功能扩展中的功能优化，共同探索如何更快的利用这些优化搭建运维监控体系，为物联网业务带来更多助力。

## 简洁易读的 HOCON 格式配置文件

EMQX 4.x 配置文件使用类似 properties 的键值格式，对类似数组的配置项缺乏表达能力，为了让配置项层级更加清晰，5.0 配置采用标准的 HOCON（ Human-Optimized Config Object Notation ）格式。

```
node {
  name = "emqx@127.0.0.1"
  cookie = "emqxsecretcookie"
  data_dir = "data"
}
listeners.ssl.default {
  bind = "0.0.0.0:8883"
  max_connections = 512000
  ssl_options {
    keyfile = "etc/certs/key.pem"
    certfile = "etc/certs/cert.pem"
    cacertfile = "etc/certs/cacert.pem"
  }
}
```

另一方面，为灵活应对不同场景下用户对功能参数的要求，EMQX 提供了非常丰富的配置项。尽管大部分配置使用默认值即可，但在 EMQX 4.x 中，单个配置文件包含了所有配置项以及每个配置项的注释，对于新手用户来说想要从中快速找到并修改常用配置具有一定难度。

针对此问题，EMQX 5.0 精简了默认配置文件 `emqx.conf`：只保留最常修改的配置，使得默认配置文件缩减到 100 行以内。如果用户需要修改其它的默认配置，可以参照 `emqx-example.conf` 文件，把对应的配置复制到 `emqx.conf` 中即可实现覆盖。

## 配置热更新

根据是否可在运行时修改，EMQX 5.0 的配置可以分成**可热更新**/**不可热更新**两种配置。比如节点类相关的参数 `node {}` 包含 Erlang 虚拟机的启动参数属于不可热更新配置，必须重启节点才能使修改生效。

可热更新配置都可以通过 HTTP API 修改成功后立即生效，同时保证配置修改在集群间同步更新。热更新基本流程如下：

![EMQX 配置热更新](https://assets.emqx.com/images/25c8c017ad7dc0f1b5037fca37bd6588.png)
 
通过 HTTP API 更新的配置会持久化到配置文件中，以确保 EMQX 重启后配置不丢失。比如在 Dashboard **功能配置 → 监听器** 页面添加监听器后，EMQX 会在 `data/configs/cluster-override.conf` 文件中持久化如下内容：

```
listeners {
   ...
   tcp {
    my_listener {
      acceptors = 16
      bind = "0.0.0.0:1884"
      limiter {}
      max_connections = 102400
      proxy_protocol = false
      proxy_protocol_timeout = "15s"
      tcp_options {
        active_n = 100
        buffer = "4KB"
        nodelay = false
        reuseaddr = true
        send_timeout = "15s"
        send_timeout_close = true
      }
      zone = "default"
    }
  }
}
```

`cluster-override.conf` 会由 EMQX 内部机制保证集群内所有节点的一致性。

为了让 EMQX 内部可以更新本节点独立的配置，EMQX 还引入了 `local-override.conf`。我们可以通过以下配置结构来理解其工作原理：

![EMQX 配置结构](https://assets.emqx.com/images/432b736bceceac17d5a6915fb3c12907.png)

优先级从高到低，依次是`emqx.conf < ENV < cluster-override.conf < local-override.conf`，比如：当某个配置已经在 Dashboard 上被修改过（即写入了`cluster-override.conf`）, 那么用户再次在`emqx.conf` 手动更新它，则手动更新并不会生效。因为在 `emqx.conf` 中的修改值会被更高优先级的 `cluster-override.conf` 所覆盖。

上图为了说明原理，列出了配置存放的所有（4个）地方。由于 data 下的`xxx-override.conf`文件都是给 EMQX 自身做持久化的，原则上是**禁止用户手动修改的**。它们对用户应该是透明的。因此，对于用户而言，只有 ENV 和 `emqx.conf `可手动更新，总结最佳实践为：

- 使用 rpm/deb 包安装的推荐修改 `/etc/emqx/etc/emqx.conf`。
- 使用容器安装的推荐使用 ENV 环境变量修改。
- 禁止手动修改 `data/configs/` 目录。
- 通过 Dashboard 更新过的配置，再次修改 `emqx.conf` 会不生效。

> 推荐使用 Dashboard 上修改配置，因为这样可以保证集群内的配置都是一致的。且无需重启节点。

## 可观测性

### 强大的日志功能

日志为系统排错、优化性能提供可靠信息来源。EMQX 在日志数据过载或日志写入过慢时，默认启动过载保护机制，最大限度保证正常业务不被日志影响。

EMQX 支持符合 [RFC 5424](https://www.ietf.org/rfc/rfc5424.txt) 标准的日志分级机制，包括：`debug < info < notice < warning < error < critical < alert < emergency` 级别。默认的日志等级为 `warning`。

进行问题排查时我们需要设置 `debug` 级别日志，结合上节给出的配置的修改方法，可以有以下 3 种修改日志等级的方法：

- 修改 `emqx.conf`。

  ```
  log {
    file_handlers.default {
      level = warning
      file = "log/emqx.log"
    }
  }
  ```

- 修改 ENV 环境变量：`EMQX_LOG__FILE__HANDLERS__DEFAULT__LEVEL=debug`。

- 在 Dashboard 上热更新配置：功能配置 / 日志 / File Handler / 日志级别 下拉列表中选择`debug`。

除了可以修改日志等级，我们还可以用相同的方法定制日志的其它功能，如：

- 日志文件路径。
- 日志轮换（rotation）功能。
- 日志的过载限流策略。

### 更友好的日志格式

EMQX 5.0 引入了结构化日志记录，现在 EMQX 发出的大多数日志都有一个 `msg` 字段，该字段的文本是一个下划线分隔的单词，更加阅读友好，同时也有助于日志索引工具对日志进行索引。

下面是一条典型的日志：

```
2022-09-15T10:00:02.780474+08:00 [debug] 
authenticator: <<"password_based:built_in_database">>, 
msg: authenticator_result, clientid: mqttx_6c89e818, 
line: 674, mfa: emqx_authentication:authenticate_with_provider/2, 
peername: 127.0.0.1:49206, result: ignore, tag: AUTHN
```

该日志的含义如下：客户端 `mqttx_6c89e818` 登录认证时通过内置数据库的认证结果为` ignore`，导致认证失败。日志还包括了认证失败时执行的函数/代码行数。客户端 `IP:Port`。

同时 EMQX 5.0 还支持 JSON 格式日志输出，相比于 4.x 的字符串（TEXT）日志，JSON 结构化格式拥有更丰富的上下文及元数据信息，既让人更容易理解，也更方便使用程序解析，可以轻松与各类日志收集和分析系统如 Elastic Stack（ELK/EFK）集成。

键值对方便提取特定的值、过滤和搜索整个数据集。如果增加新的键值对，解析日志程序也可以直接忽略那些它不关心的键，而不是无法解析。

### Trace 排错利器

通过开启 `DEBUG` 级别日志能够有效地排查各类问题，但这会引起大量日志落地进而影响 EMQX 整体性能，尤其是在有大量连接与消息收发的生产环境中，该手段几乎是不可实施的。

针对这种问题，EMQX 5.0 新增了在线 Trace 排错功能，允许用户指定客户端 ID、主题或 IP 实时过滤输出 DEBUG 级别日志。Trace 基于 Erlang 内置强大的 Logger Filter 功能，对整体的消息吞吐影响可以忽略不计：

- EMQX 使用独立的 File Handlers 进程来持久化 Trace 的磁盘日志。
- 每个客户端连接会在 EMQX 内部生成一个独立进程来处理它的消息。
- 当收到客户端消息时，这个独立进程会根据定制的 Trace Filter 判断是否符合规则（比如：是否为指定的ClientID），如果不符合，则执行原来的传输逻辑。反之，则在本进程序列化消息为二进制数据，再异步发消息给 File Handler。
- File Handlers 负责把二进制数持久化至 Trace 文件中。

在此机制下，所有的过滤动作都前置在对接客户端的独立进程，过滤掉了大部分不符合规则的日志，保证了 File Handler 不被大量消息累积，因此能够在生产环境中安全的使用。

Trace 几乎适用于所有疑难杂症，如消息或数据异常丢弃、客户端异常断线、订阅不生效等。针对特定时间段发生的异常，Trace 允许用户设置任务启动/停止时间进行自动化收集，极大的方便用户使用。

同时，Trace 与 Dashboard 深度适配，用户可以在 Dashboard 中 **问题分析 → 日志追踪** 管理集群中的 Trace 任务，并实时查看每个节点上收集到的日志内容。Trace 极大改善用户自行排查、诊断客户端异常行为时的体验。

### 完善的度量指标以及 Prometheus 集成

日志和追踪只能反映 EMQX 运行过程中是否有异常，为了更方便监控运行时压力指标，EMQX 提供了丰富的度量指标以及指标监控集成，方便用户以及运维人员进行业务的监控和预警。

在 EMQX 5.0 版本中，用户可以通过 Dashboard 查看客户端实时连接情况以及消息流入流出速度，通过节点拓扑一目了然洞察集群中所有节点状态。Dashboard 上还提供多个纬度至多 7 天的历史指标并通过在线图表展示，用户可以直观的监控业务增长趋势，避免错过任何业务波动。

同时 EMQX 支持用户将指标集成至自己熟悉的监控与告警技术栈，通过配置文件或 Dashboard 上轻点鼠标即可在集成 Prometheus、Datadog 等系统。

![EMQX 集成 Prometheus、Datadog](https://assets.emqx.com/images/1edca7fd721e2ec2acab2d6e6f195d2b.png)

EMQX 提供了 Grafana 的 Dashboard 的模板文件。这些模板包含了所有 EMQX 监控数据的展示。用户可直接导入到 Grafana 中，即可展示 EMQX 的运行状态。

模板文件位于：[emqx_prometheus/grafana_template](https://github.com/emqx/emqx-prometheus/tree/master/grafana_template)。

![EMQX Grafana](https://assets.emqx.com/images/d3c2270caef21365d084932cae84a9b4.png)

### 慢订阅

正常情况下 EMQX 内部消息传输耗时都很低（毫秒级以下），大部分时间消耗都集中在网络传输上，针对客户端偶尔出现订阅 `QoS1/QoS2` 时延高。EMQX 提供慢订阅统计功能，方便追踪 QoS 1 和 QoS 2 消息到达 EMQX 后，完成消息传输全流程的时间消耗，然后根据配置中的选项，计算消息的传输时延，之后按照时延高低对订阅者、主题进行统计排名。

![EMQX 消息流程示意图](https://assets.emqx.com/images/89ac024e78e9090a383d4e94cf5c03a8.png)

<center>EMQX 消息流程示意图</center>

消息完全传输的定义：

- QoS 1 EMQX 收到客户端的 `PUBACK` 包。
- QoS 2 EMQX 收到客户端的 `PUBCOMP` 包。

**影响慢订阅的因素**

1. 发布者到 EMQX 网络较慢（暂不能探测，功能规划中）。
2. Hooks 执行慢，如 ACL 检查、ExHook、规则引擎等阻塞消息发布流程。
3. 队列中消息堆积太多（PUBLISH 与 SUBSCRIBE 共用同一连接，大量 PUBLISH 消息处理不及时/堆积也可能导致 SUBSCRIBE 变慢）导致发出时间超时过慢。
4. 订阅者接收速度过慢。

消息时效性是物联网业务重要保障，大量慢订阅的出现可能是某个功能出现问题的前兆。

启用慢订阅后可以及时发现生产环境中消息堵塞等异常情况，提高用户对此类情况的感知能力，方便用户及时调整相关服务。

![EMQX 慢订阅查询](https://assets.emqx.com/images/d0c0bba23e1e4c2ebaa1613353c6e625.png)

### 主题监控

EMQX 支持统计指定主题（无通配符）下的消息收发数量、速率等指标。

![EMQX 主题监控](https://assets.emqx.com/images/e2c92aae0cc65b003653731190da96cd.png)

以上图为例，从监控指标中可以看到消息流出速率远小于消息流入速率。多次重置指标还是同样的结果，可以推测出订阅端消费能力不足。

### Dashboard 告警

EMQX 对于操作系统（OS） 和 Erlang 虚拟机（VM）的基本状态及资源状态内置了监控告警。EMQX 允许用户对告警功能进行一定程度的调整以适应实际需要，目前开放了以下配置项：

```
sysmon {
   os {
    ## CPU 占用率的检查间隔    
    cpu_check_interval = 60s
    ## CPU 占用率高水位，即 CPU 占用率达到多少时激活告警
    cpu_high_watermark = "80%"
    ## CPU 占用率低水位，即 CPU 占用率降低到多少时取消告警
    cpu_low_watermark = "60%"
    ## 内存占用率的检查间隔
    mem_check_interval = 60s
    ## 系统内存占用率高水位，即申请的总内存占比达到多少时激活告警
    sysmem_high_watermark = "70%"
    ## 进程内存占用率高水位，即单个进程申请的内存占比达到多少时激活告警
    procmem_high_watermark = "5%"
   }
   vm {
    ## 进程数量的检查间隔
    process_check_interval = 30s
    ## 进程占用率高水位，即创建的进程数量与最大数量限制的占比达到多少时激活告警
    process_high_watermark = "80%"
    ## 进程占用率低水位，即创建的进程数量与最大数量限制的占比降低到多少时取消告警
    process_low_watermark = "60%"
    ## 启用慢垃圾回收监控
    long_gc = disabled
    ## 慢调度监控
    long_schedule = 240ms
    ## 大 heap 分配监控
    large_heap = 32MB
    ## 启用分布式端口过忙监控
    busy_dist_port = true
    ## 启用端口过忙监控
    busy_port = true
   }  
 }
```

可以 Dashboard 上查看到当前/历史告警：

![查看 EMQX 告警](https://assets.emqx.com/images/f94601fba4c3d64aa489dd23f1d69c50.png)

EMQX 计划在未来版本中提供告警集成 Webhook 功能，允许用户将告警事件发送到对应的告警/通知服务，如 Slack、钉钉等，用户亦可在 Web 服务中扩展实现短信或邮件告警。

## 扩展性

### 新的插件机制

EMQX 提供了插件扩展机制，4.x 版本中用户使用插件时需要将插件与 EMQX 源码一同编译以解决插件与EMQX 的代码依赖问题，一定程度上限制了插件的分发与使用。

EMQX 5.0 经过改进，允许通过插件包的的形式编译、分发、安装插件，当用户需要扩展功能时，可以下载独立的插件安装包，在 Web 界面完成上传即可进行安装，整个过程甚至不需要重启 EMQX 集群。

同时，一个规范的插件将会随身附带使用说明、插件主页地址等信息，普通用户可以依照说明快速将插件用起来，也为插件开发者提供了与用户沟通的渠道。

EMQX 5.0 插件模板可见：[emqx-plugin-template](https://github.com/emqx/emqx-plugin-template)。

### ExHook/gRPC 用于微服务集成

ExHook（**多语言扩展钩子**）基于 gRPC 框架， 允许用户使用其他编程语言（如Python、Java、Node.js 等）直接向 EMQX 系统挂载钩子，以接收并处理 EMQX 系统的钩子事件，达到扩展和定制 EMQX 的目的。

![EMQX ExHook/gPRC](https://assets.emqx.com/images/8551099f1861451e381f4a9d6fc9f48b.png)
 

ExHook 基于 gPRC 通信，理论上支持任意语言平台和微服务，通过 ExHook 可以实现客户端认证、权限检查、数据存储与改写消息流程等业务的集成。

在 EMQX 5.0 中我们允许创建多个 ExHook 实例，并为每个实例提供了详细的使用情况统计信息：

![EMQX 创建 ExHook 实例](https://assets.emqx.com/images/4a265864f601de681808371ccc23f81e.png)

同时还可以查看每个 Exhook 实例注册的钩子以及钩子参数，能够更好地感知 Exhook 扩展负载情况。

EMQX 5.0 Exhooks 接口参数及数据结构详情请参考：[exhook.proto](https://github.com/emqx/emqx/blob/master/apps/emqx_exhook/priv/protos/exhook.proto)。

## 结语

作为自发布以来最重要的里程碑版本之一，EMQX 5.0 为用户带来了足以保障各类数据需求的高性能，以及从实际应用出发、可快速上手的各类实用功能。如前文提到，可操作性与可观测性的提升将使 EMQX 集群的运维工作变得更加轻松与高效，扩展性的增强则为用户定制更加符合自身需求的 EMQX 提供了便利。



<section class="promotion">
    <div>
        现在试用 EMQX 5.0
    </div>
    <a href="https://www.emqx.com/zh/try?product=broker" class="button is-gradient px-5">立即下载 →</a>
</section>
