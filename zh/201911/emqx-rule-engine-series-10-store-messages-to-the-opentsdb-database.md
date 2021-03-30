## OpenTSDB 介绍

OpenTSDB 是可扩展的分布式时序数据库，底层依赖 HBase 并充分发挥了HBase的分布式列存储特性，支持数百万每秒的读写。

面对大规模快速增长的物联网传感器采集、交易记录等数据，时间序列数据累计速度非常快，时序数据库通过提高效率来处理这种大规模数据，并带来性能的提升，包括：更高的容纳率（Ingest Rates）、更快的大规模查询以及更好的数据压缩。



## 安装与验证 OpenTSDB 服务器

读者可以参考 OpenTSDB 官方文档 (http://opentsdb.net) 或 Docker (https://hub.docker.com/r/petergrace/opentsdb-docker/)  来下载安装 OpenTSDB 服务器，本文使用 OpenTSDB 2.4.0 版本。



## 场景介绍

该场景需要将 EMQ X 指定主题下且满足条件的消息存储到 OpenTSDB 数据库。为了便于后续分析检索，消息内容需要进行拆分存储。

**该场景下客户端上报数据如下：**

- Topic：stat/cpu

- Payload:

  ```json
  {
    "metric": "cpu",
    "tags": {
      "host": "serverA"
    },
    "value":12
  }
  ```



## 准备工作

### 启动 OpenTSDB Server

启动 OpenTSDB Server 并开放 4242 端口。

```shell
$ docker pull petergrace/opentsdb-docker

$ docker run -d --name opentsdb -p 4242:4242 petergrace/opentsdb-docker
```



## 配置说明

### 创建资源

打开 EMQ X Dashboard，进入左侧菜单的 **资源** 页面，点击 **新建** 按钮，选择 OpenTSDB 资源类型并完成相关配置进行资源创建。

![image20190725110536094.png](https://static.emqx.net/images/b73349ea68ae04ebc090b9128d75dc5c.png)

### 创建规则

进入左侧菜单的 **规则** 页面，点击 **新建** 按钮，进行规则创建。这里选择触发事件 **message.publish**，即在 EMQ X 收到 PUBLISH 消息时触发该规则进行数据处理。

选定触发事件后，我们可在界面上看到可选字段及示例 SQL：

![image20190719112141128.png](https://static.emqx.net/images/e52941d185211d7177010bc67a9d75ea.png)



#### 筛选所需字段

规则引擎使用 SQL 语句过滤和处理数据。例如前文提到的场景中我们需要将 ``payload`` 中的字段提取出来使用，则可以通过 `payload.<fieldName>` 实现。同时我们仅仅期望处理 `stat/cpu` 主题，那么可以在 WHERE 子句中使用主题通配符 `=~` 对 `topic` 进行筛选：`topic =~ 'stat/cpu'`， 最终我们得到 SQL 如下：

```sql
SELECT
  payload.metric as metric, payload.tags as tags, payload.value as value
FROM
  "message.publish"
WHERE
	topic =~ 'stat/cpu'
```



#### SQL 测试

借助 SQL 测试功能，我们可以快速确认刚刚填写的 SQL 语句能否达成我们的目的。首先填写用于测试的 payload 等数据如下：

![image20190725110913878.png](https://static.emqx.net/images/2a6542bfb91c3d8a5a9d38707c465e29.png)

然后点击 **测试** 按钮，我们得到以下数据输出：

```json
{
  "metric": "cpu",
  "tags": {
    "host": "serverA"
  },
  "value": 12
}
```

测试输出与预期相符，我们可以进行后续步骤。



### 添加响应动作，存储消息到 OpenTSDB

SQL 条件输入输出无误后，我们继续添加相应动作，配置写入 SQL 语句，将筛选结果存储到 OpenTSDB。

点击响应动作中的 **添加** 按钮，选择 **保存数据到 OpenTSDB** 动作，选取刚刚创建的 `OpenTSDB` 资源并完成剩余参数设置。OpenTSDB 动作用到的几个参数分别为：

1. 详细信息。是否需要 OpenTSDB Server 返回存储失败的 Data points 及失败原因，默认为 false。
2. 摘要信息。是否需要 OpenTSDB Server 返回 data point 存储成功与失败的数量，默认为 true。
3. 最大批处理数量。消息请求频繁时允许驱动从队列中一次读取多少个 Data Points 合并为一个 HTTP 请求，为性能优化参数，默认为 20。
4. 是否同步调用。配置 OpenTSDB Server 是否等待所有数据都被写入后才返回结果，默认为 false。
5. 同步调用超时时间。OpenTSDB Server 等待数据写入的最大时间，默认为 0，即永不超时。

这里我们全部使用默认配置，点击 **新建** 按钮完成规则创建。

![image20190725111158382.png](https://static.emqx.net/images/2ebda32b1e3f02ada48d0ad985938214.png)



## 测试

### 预期结果

我们成功创建了一条规则，包含一个处理动作，动作期望效果如下：

1. 客户端向 `stat/cpu` 主题上报消息时，该消息将命中 SQL，规则列表中 **已命中** 数字增加 1；
2. OpenTSDB Server 中将增加一条数据，数据内容与消息内容一致。



### 使用 Dashboard 中的 Websocket 工具测试

切换到 **工具** --> **Websocket** 页面，使用任意信息客户端连接到 EMQ X，连接成功后在 **消息** 卡片中发送如下消息：

- Topic：stat/cpu

- Payload:

  ```json
  {
    "metric": "cpu",
    "tags": {
      "host": "serverA"
    },
    "value":12
  }
  ```
![image20190725112738414.png](https://static.emqx.net/images/367befbc4efc6dd4b92e217251cab020.png)

点击 **发送** 按钮，发送成功后可以看到当前规则已命中次数已经变为了 1。

然后通过 Postman 向 OpenTSDB 发送查询请求，当我们得到如下应答时说明新的 data point 已经添加成功：

![image20190725113422461.png](https://static.emqx.net/images/db95b74238f0f2c2e2fadb23ac33aaf0.png)

至此，我们通过规则引擎实现了使用规则引擎存储消息到 OpenTSDB 数据库的业务开发。


