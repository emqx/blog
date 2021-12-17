面对物联网时代海量设备连接及其实时产生的大规模数据流，EMQ 提供从边缘到云的现代数据基础设施，助力云边端物联网数据的统一「连接、移动、处理、分析」。

如今，可「随处运行、无限连接、任意集成」的[云原生分布式消息中间件 EMQ X](https://www.emqx.com/zh/products/emqx) 已解决了海量连接的挑战，[流数据库 HStreamDB](https://hstream.io/zh) 则正试图解决海量物联网数据的存储、处理与实时分析。

作为首个专为流数据设计的云原生流数据库，HStreamDB 致力于高效的大规模数据流存储和管理。EMQ X 与 HStreamDB 的组合，将使海量数据接入、存储、实时处理与分析的一站式管理变得不再困难。

![EMQ X 与 HStreamDB](https://static.emqx.net/images/fc0fe48820b6158dd404cd8757ff9658.png)

最近发布的[ HStreamDB v0.6 ](https://www.emqx.com/zh/blog/hstreamdb-v-0-6-release-notes)新增了数据写入 Rest API，可以使用任何语言通过 Rest API 向 HStreamDB 写入数据，方便开源用户围绕 HStreamDB 进行二次开发。我们也通过这一功能与 EMQ X 开源版的 Webhook 功能结合，实现了 EMQ X 和 HStreamDB 的快速集成。

本文就将详细介绍使用 HStreamDB 对 EMQ X 的接入数据进行持久化存储的具体操作。

> 注：本文介绍基于 EMQ X 4.3 和 hstreamdb/hstream:v0.6.1 镜像。

## 启动 EMQ X 和 HStreamDB

首先我们需要一个运行中的 EMQ X，如何安装、部署并启动请参考：[EMQ X 文档](https://docs.emqx.cn/broker/v4.3/getting-started/install.html) 。

同时，我们需要一个运行中的 HStreamDB，更详细的如何安装、部署与启动教程请参考：[HStreamDB Docs](https://hstream.io/docs/en/latest/start/quickstart-with-docker.html) 。

对于不熟悉 HStreamDB 的用户，可以先通过 docker-compose 快速启动一个单机的 HStreamDB 集群。

### 启动 HStreamDB

先直接通过[链接](https://raw.githubusercontent.com/hstreamdb/hstream/main/docker/quick-start.yaml)下载 `docker-compose.yaml` 文件。

创建一个用来存储数据库数据的文件：

```shell
mkdir /data/store
```

在后台启动 HStreamDB：

```shell
docker-compose -f quick-start.yaml up -d
```

通过：

```shell
docker-compose -f quick-start.yaml logs hstream-http-server
```

将会看到以下 log：

```
Server is configured with:
     gRPCServerHost: hserver
     gRPCServerPort: 6570
     httpServerPort: 6580
 Setting gRPC connection
 Setting HTTP server
 Server started on port 6580 
```

### 通过 HStreamDB CLI 创建所需要的 Stream

Stream 是 HStreamDB 中用来存储流式数据的对象，可以看作是一些数据的集合。

#### 启动 HStreamDB CLI

用 docker 启动一个 HStreamDB 的命令行界面：

```shell
docker run -it --rm --name some-hstream-cli --network host hstreamdb/hstream hstream-client --port 6570 --client-id 1
```

你将会进入到以下界面:

```
      __  _________________  _________    __  ___
     / / / / ___/_  __/ __ \/ ____/   |  /  |/  /
    / /_/ /\__ \ / / / /_/ / __/ / /| | / /|_/ /
   / __  /___/ // / / _  _/ /___/ ___ |/ /  / /
  /_/ /_//____//_/ /_/ |_/_____/_/  |_/_/  /_/

>
```

创建 HStreamDB Stream，用来保存桥接过来的数据：

```
> CREATE STREAM emqx_rule_engine_output ;
emqx_rule_engine_output

```

当然我们也可以通过 `SHOW` 得到已经创建好的 Stream：

```
> SHOW STREAMS;
emqx_rule_engine_output

```

## 配置 EMQ X

然后，我们打开 EMQ X 的 Dashboard，点击规则引擎（Rule Engine），进入资源（Resource）界面。

![EMQ X Dashboard 资源页面](https://static.emqx.net/images/d110d6a38ba3a2ca0f238669d1d5a807.png)

我们可以先创建一个 WebHook 资源，如下图：

![EMQ X Dashboard 创建 WebHook](https://static.emqx.net/images/cfec5314f7b36d101d0cf963d2186bc2.png)


在 `Request URL` 一栏中填入 `hstream-http-server` 的监听地址，`<host>:6580/streams/emqx_rule_engine_output:publish`，然后点击 `test connection` 测试链接。

![EMQ X Dashboard test connection](https://static.emqx.net/images/a811a5d1cfafa32a7102e0defeb9dc80.png)


接着，我们来创建所需要的规则引擎规则：

![创建 EMQ X 规则引擎规则](https://static.emqx.net/images/41af650187256542b881bf345004d5d2.png)


```
SELECT 
  payload,                 -- 在 HStreamDB 的 http 协议中，我们需要一个 payload 项
  str(payload) as payload, -- HStreamDB 要求 payload 是一个 JSON String
  0 as flag                -- HStreamDB 中 flag 为 0 表示 payload 是一个JSON String
FROM 
  "#"                      -- 这个符号会匹配所有的 topic
```

我们需要增加一个 Action Handler ，选择 `Action` 为 `Data to Web Server`：

![EMQ X 规则引擎 Action](https://static.emqx.net/images/f1434d7eeb1304842c18f9cda7e7c735.png)


将 `Method` 设置为 `POST` ，`Header` 加入 `content-type` `application/json`。

这个时候，我们已经完成了最基本的桥接的设置，接下来让我们通过 websocket 和 hstreamdb-cli 来测试一下吧。

## 通过 HStreamDB CLI 观察数据的持久化存储是否完成

首先我们在刚刚启动的 HStreamDB CLI 中创建一个 Query：

```
> SELECT * FROM emqx_rule_engine_output

```

在 HStreamDB 中，每一个 Stream 都表示一串动态变化的数据流，因此一个 Query 并不是简单地读取数据，而是会持续读取并输出被写入 Stream 中的数据。在 CLI 中，读取和输出数据的起点是就是成功创建 Query 的这一刻。当前，我们可以观察到的是，CLI 中并没有任何输出。

此时我们可以通过 EMQ X DashBoard 的 WebSocket 或者其他 [MQTT 客户端](https://www.emqx.com/zh/mqtt-client-sdk)（例如 [跨平台 MQTT 5.0 桌面客户端工具 - MQTT X](https://mqttx.app/zh)）向 EMQ X 写入数据。

以下用 WebSocket 举例，我们可以先连接上我们启动的 EMQ X 集群：

![EMQ X DashBoard 的 WebSocket 客户端](https://static.emqx.net/images/9e26f3437c419c79caf834b57efb2c08.png)


再向指定的 topic 发送数据：

![EMQ X DashBoard 的 WebSocket 发送数据](https://static.emqx.net/images/00fbff89e8f0e58933703f541a74a6fa.png)

如果一切正常的话，我们就可以实时地在 HStreamDB CLI 看到我们发到 EMQ X 的数据。

```
> SELECT * FROM emqx_rule_engine_output
{"location":{"lng":116.296011,"lat":40.005091},"speed":32.12,"tachometer":9001.0,"ts":1563268202,"direction":198.33212,"id":"NXP-058659730253-963945118132721-22","dynamical":8.93}
```

至此，我们完成了 EMQ X 接入的数据在 HStreamDB 的持久化存储。


通过将 EMQ X 与 HStreamDB 集成，我们不仅可以实现对发送到 EMQ X 的数据的持久化存储，还能对这些数据进行实时处理分析，获得进一步的数据洞察。随着两个产品的不断完善，我们相信在未来，EMQ X + HStreamDB 的高效组合将在 IoT 领域实时流数据的分析和处理场景发挥重要作用，成为数据转化与变现过程中的重要一环，为企业数据资产的价值创造提供动力。
