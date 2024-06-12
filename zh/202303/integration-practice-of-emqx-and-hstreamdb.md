在 IoT 场景中，通常面临设备数量庞大、数据产生速率高、累积数据量巨大等挑战。因此，如何接入、存储和处理这些海量设备数据就成为了一个关键的问题。

EMQX 作为一款强大的[物联网 MQTT 消息服务器](https://www.emqx.com/zh/products/emqx)，单个集群可处理上亿设备连接，同时提供了丰富的数据集成功能。[HStreamDB](https://hstream.io/zh) 作为一款分布式流数据库，不仅可以高效存储来自 EMQX 的海量设备数据，而且提供实时处理分析能力。EMQX 与 HStreamDB 都具备高可扩展性和可靠性，两者结合不仅能够满足大规模 IoT 应用的性能和稳定性需求，同时能够提升应用的实时性。

![物联网流数据处理](https://assets.emqx.com/images/a9f9d31755d0000f7aa78f1c5500c841.png)

近期 [EMQX Enterprise 4.4.15](https://www.emqx.com/zh/changelogs/enterprise/4.4.15) 发布，更新了对 HStreamDB 最新版本的支持，本文将具体介绍如何通过 EMQX 规则引擎将数据持久化到 HStreamDB，实现 MQTT 数据流的存储与实时处理。

> **注**：本文介绍的集成步骤基于 EMQX 4.4.15 和 HStreamDB 0.14.0 以上版本。

## 连接到 HStreamDB 集群

在下面的教程中，我们假设有一个正在运行的 EMQX Enterprise 集群和正在运行的 HStreamDB 集群。如需部署 EMQX Enterprise 集群，请参考 [EMQX Enterprise docs](https://docs.emqx.com/zh/enterprise/v4.4/)。如需部署 HStreamDB 集群，请参考 [HStreamDB docs](https://hstream.io/docs/zh/latest/start/quickstart-with-docker.html)，其中包含关于如何用 Docker 快速部署的说明。

我们可以通过 Docker 来部署 HStreamDB 客户端并连接到 HStreamDB 集群：

```
# 获取帮助信息
docker run -it --rm --name some-hstream-cli --network host hstreamdb/hstream:v0.14.0 hstream --help
```

我们在此使用 `hstream stream` 命令创建一个 stream，供接下来的示例使用：

```
# 使用 hstream stream 命令创建 streams
docker run -it --rm --name some-hstream-cli --network host hstreamdb/hstream:v0.14.0 hstream stream create basic_condition_info_0 -r 3 -b $(( 7 * 24 * 60 * 60 ))
```

接下来，连接到 HStreamDB 集群，启动交互式 HStream SQL shell：

```
docker run -it --rm --name some-hstream-cli --network host hstreamdb/hstream:v0.14.0 hstream sql --service-url "<<YOUR-SERVICE-URL>>"
# 如果要使用安全连接，还需要填写 --tls-ca, --tls-key, --tls-cert 参数
```

如果连接成功，将会出现

```
      __  _________________  _________    __  ___
     / / / / ___/_  __/ __ \/ ____/   |  /  |/  /
    / /_/ /\__ \ / / / /_/ / __/ / /| | / /|_/ /
   / __  /___/ // / / _, _/ /___/ ___ |/ /  / /
  /_/ /_//____//_/ /_/ |_/_____/_/  |_/_/  /_/

Command
  :h                           To show these help info
  :q                           To exit command line interface
  :help [sql_operation]        To show full usage of sql statement
  
SQL STATEMENTS:
  To create a simplest stream:
    CREATE STREAM stream_name;
  To create a query select all fields from a stream:
    SELECT * FROM stream_name EMIT CHANGES;
  To insert values to a stream:
    INSERT INTO stream_name (field1, field2) VALUES (1, 2);
```

可以使用 `show streams;` 来查看已经创建的 streams 的信息：

```
> show streams;
+-------------------------------------------+---------+----------------+-------------+
| Stream Name                               | Replica | Retention Time | Shard Count |
+-------------------------------------------+---------+----------------+-------------+
| basic_condition_info_0                    | 3       | 604800 seconds | 1           |
+-------------------------------------------+---------+----------------+-------------+
```

## 创建 HStreamDB 资源

在利用 EMQX 规则引擎将数据持久化到 HStreamDB 之前，需要创建一个 HStreamDB 资源。

为此，请访问 EMQX Dashboard，单击 `规则引擎` -> `资源` → `创建` ，选择 `HStreamDB 资源`，输入 HStreamDB 地址并填写必要的选项。可用选项如下表：

| **选项名**     | **定义**                               | **类型** | **是否必须填写** | **默认值**                                      |
| :------------- | :------------------------------------- | :------- | :--------------- | :---------------------------------------------- |
| HStream 服务器 | HStream 服务器地址                     | 字符串   | 是               | `http://127.0.0.1:6570` |
| 连接池大小     | HStream 连接池大小                     | 正整数   | 是               | 8                                               |
| gRPC 超时      | gRPC 调用 HStreamDB 服务器超时（毫秒） | 正整数   | 否               | 5000                                            |
| 开启 SSL       | 是否开启 SSL                           | 布尔值   | 否               | 否                                              |

在选择开启 SSL 时，会出现额外的 SSL 配置界面，可以粘贴所需配置内容或上传文件。

![创建资源1](https://assets.emqx.com/images/652103dbf8fadee51785672a922e31ad.png)

![创建资源2](https://assets.emqx.com/images/43aa2d3e8984af0e4b79c5ae1f2e7f92.png)
 

## 创建数据持久化到 HStreamDB 的规则

点击 `规则引擎` -> `规则` -> `创建`。

![创建规则](https://assets.emqx.com/images/ec80aa82f5458c53858c48852d7fb67b.png)
 
编辑 SQL 规则并添加操作，您可以在字符串模板中使用 SQL 变量。

> 请注意，本文档中介绍的 SQL 规则仅供演示，实际的 SQL 应根据业务设计进行编写。

单击 `添加操作`，选择「数据持久化」以将数据保存到 HStreamDB 中。选择上一步创建的资源并输入参数。可用参数如下表：

| **参数名**   | **定义**                                   | **类型** | **是否必须填写** | **默认值**        |
| :----------- | :----------------------------------------- | :------- | :--------------- | :---------------- |
| Stream       | Stream。不可使用占位符变量                 | 字符串   | 是               |                   |
| PartitionKey | PartitionKey。支持占位符变量               | 字符串   | 否               | 默认 PartitionKey |
| gRPC 超时    | gRPC 调用 HStreamDB 服务器超时（毫秒）     | 正整数   | 否               | 10000             |
| 启用批量插入 | 是否启用批量插入                           | 布尔值   | 否               | 是                |
| 最大批量数   | 单次批量请求可以发送的最大条目             | 正整数   | 否               | 100               |
| 最大批量间隔 | 两次（批量）请求之间最大的等待间隔（毫秒） | 正整数   | 否               | 500               |

![新增动作](https://assets.emqx.com/images/aede2339ff692fb84bb0683c531e22aa.png)

点击 `确定` 来确认添加行为。

![点击确定](https://assets.emqx.com/images/97b0a3c2c28f2d9e89a14304db34fc73.png)

## 在 HStream SQL Shell 中获取实时的数据更新

从 EMQX 规则引擎持久化到 HStreamDB 的数据可以使用 HStream SQL Shell 实时读出新写入 stream 的内容。现在，数据已经被写入 HStreamDB，可以使用任何消费方式来消费消息。文档使用了一个简单的消费方法：使用 HStream SQL shell 进行查询。此外，读者可以自由选择使用他们[喜欢的编程语言 SDK](https://github.com/hstreamdb/) 编写消费端。

```
# docker run -it --rm --name some-hstream-cli --network host hstreamdb/hstream:v0.14.0 hstream sql
> select * from basic_condition_info_0 emit changes;
```

当前的 `select` 查询没有结果可供打印出，这是因为还没有数据通过 EMQX 的规则引擎向 HStreamDB 写入。一旦有数据写入，便可以在 HStream SQL shell 观察到数据的即时更新。目前在 HStreamDB 使用 SQL 对 streams 做查询，只会打印出**创建查询后**的结果。如果在 EMQX 停止向 HStreamDB 写入后创建查询，可能观察不到产生的结果。

更多信息和有关 streams 与 SQL 的概念请参考 HStreamDB 的 SQL [文档](https://hstream.io/docs/zh/latest/)。

## 向 EMQX 写入消息测试规则引擎

可以使用跨平台的桌面客户端 [MQTTX](https://mqttx.app/zh) 来连接到 EMQX 并发送消息：

![MQTT 桌面客户端](https://assets.emqx.com/images/dfd41450b0fbf97e1c78ddfc4f920231.png)

## 从 EMQX Dashboard 获取规则引擎的运行数据指标

访问对应的规则引擎界面：

![规则引擎界面](https://assets.emqx.com/images/11ad214a9283a6240c215b70c6096381.png)

如果规则引擎运行数据指标正常，则代表 EMQX 会将数据持久化到 HStreamDB。一旦写入成功，便可以在前面步骤启动的 HStream SQL Shell 中看到实时的数据更新。

```
# docker run -it --rm --name some-hstream-cli --network host hstreamdb/hstream:v0.14.0 hstream sql
> select * from basic_condition_info_0 emit changes;
{"current-number-of-people":247.0,"device-health":true,"number-of-people-in-line":14.0,"submitter":"admin-07","temperature":27.0}
{"current-number-of-people":220.0,"device-health":true,"number-of-people-in-line":13.0,"submitter":"admin-07","temperature":27.2}
{"current-number-of-people":135.0,"device-health":true,"number-of-people-in-line":2.0,"submitter":"admin-01","temperature":26.9}
{"current-number-of-people":137.0,"device-health":true,"number-of-people-in-line":0.0,"submitter":"admin-01","temperature":26.9}
```

## 结语

至此，我们就完成了通过 EMQX 规则引擎将数据持久化到 HStreamDB 的主要流程。

将 EMQX 采集到的数据存储到 HStreamDB 后，可以对这些数据进行实时处理与分析，为上层 AI、大数据等应用提供支撑，进一步发掘和利用数据价值。作为首个专为流数据设计的云原生流数据库，HStreamDB 与 EMQX 结合可以实现一站式存储和实时处理海量物联网数据，精简物联网应用数据栈，加速企业的物联网应用开发。


<section class="promotion">
    <div>
        免费试用 EMQX 企业版
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
