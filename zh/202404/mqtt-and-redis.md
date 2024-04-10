## 引言

随着物联网技术的日臻完善，其应用领域逐渐扩大到环境监测、社交和即时通讯等场景。将这些领域产生的大量传感器读数、用户行为等数据通过 [MQTT 协议](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)采集并传输到云端，并在云端进一步分析和统计，可以实现用户体验优化、设备监测和告警等业务操作。

本文将演示如何利用 MQTT 消息服务器 EMQX 采集设备各类传感器以及设备事件数据，并与 Redis 数据库集成，实现数据的实时统计和分析。

## MQTT+Redis 在物联网应用中的应用

MQTT 是一个轻量级的发布/订阅消息协议，设计用于在网络上进行消息传递，特别适合于网络带宽有限、网络不稳定的环境。然而，在一些涉及到数据存储和分析的业务场景中，例如消息持久化、消息排序和查询、实时统计和分析等，MQTT 的功能显得有些不足。而将其与 Redis 集成使用则可以很好地弥补这些不足。

Redis 具有以下特性：

1. **键值数据存储**：Redis 是一个键值数据库，可以非常快速地存取数据。它的这种数据模型非常适合存储简单的数据类型，如字符串、列表、集合、哈希表等。每种数据类型都有灵活的查询操作，例如，可以查询一个列表的长度，获取集合的所有元素，查找有序集合中的最大值或最小值，获取哈希表中的某个字段的值等。
2. **内存存储和持久化**：Redis 将所有数据存储在内存中，这使得 Redis 的读写操作非常快。同时，Redis 也提供了多种数据持久化机制，可以将内存中的数据保存到硬盘，防止数据丢失。
3. **发布/订阅模式**：Redis 支持发布/订阅模式，可以用于实现实时消息推送和通知。
4. **排序和范围查询**：Redis 的有序集合支持排序和范围查询，可以非常方便地实现排行榜和时间序列数据的查询。
5. **位图和 HyperLogLog 查询**：Redis 的位图可以用来实现一些统计和分析功能，如统计在线用户数量、用户活跃度等。HyperLogLog 可以用来统计大量数据的基数，提供了一种既快速又节省内存的基数估算方法。
6. **计数器**：Redis 的字符串可以作为原子计数器使用，可以用来实现实时计数和统计。

Redis 作为基于内存的键值数据库，显然它并不适合存储海量的遥测数据，因此无法支持需要长期历史数据作为基础的查询需求。然而，Redis 在查询和统计方面展现出独特的优势和能力。这使得 Redis 不仅能作为一个高速的数据存储系统，还能满足一些基本的数据查询和分析需求。结合 MQTT 协议，在物联网应用场景中，Redis 能够被用于设备行为和状态的实时监控、数据的即时分析以及告警功能等。

## 前提条件

- Git
- Docker Engine: v20.10+
- Docker Compose: v2.20+

## 工作原理

这是个简单而高效的架构，无需复杂的组件。主要包括以下关键组件：

| 组件名称                                                 | 版本   | 说明                                                         |
| :------------------------------------------------------- | :----- | :----------------------------------------------------------- |
| [EMQX Enterprise](https://www.emqx.com/zh/products/emqx) | 5.4.1+ | 用于在设备现场和 Redis 之间进行消息传递的 MQTT Broker。      |
| [Node.js](https://nodejs.org/)                           | 18.17  | 用于模拟生成环境传感器数据，以及触发备个各类行为事件的运行环境。 |
| [Redis](https://redis.io/)                               | 7.0.12 | 用于传感器数据暂存与分析、设备事件存储和分析。               |
| [Grafana](https://grafana.com/)                          | 9.5.1+ | 用于展示和分析采集数据的可视化平台。                         |

## 下载示例项目到本地

使用 Git 将 [emqx/mqtt-to-redis](https://github.com/emqx/mqtt-to-redis) 存储库代码下载到本地：

```shell
git clone https://github.com/emqx/mqtt-to-redis
cd mqtt-to-redis
```

代码库由四部分组成：

- `emqx` 文件夹包含了 EMQX-Redis 数据集成配置，可以在启动 EMQX 的时候自动创建规则和动作。
- `simulate` 文件夹包含基于 Node.js 的模拟脚本，用于模拟连接到 EMQX 并生成数据，并随机触发设备事件。
- `prometheus` 和 `grafana-provisioning` 文件夹包含了数据统计分析可视化配置。
- `docker-compose.yml` 文件可编排所有组件，让您可以一键启动项目。

## 启动 MQTTX CLI、EMQX 和 Redis

请确保已经安装 [Docker](https://www.docker.com/)，然后在后台运行 Docker Compose：

```shell
docker-compose up -d
```

现在，模拟脚本将创建 10 个设备接入 EMQX，定期发布模拟的温湿度数据，以下是一条发布到 EMQX `message-drop-test/${clientid}` 主题的数据示例：

```json
{
    "message": "this is a stored message",
    "clientId": "emqx_c",
    "duration": "102s",
    "temp": 44.37,
    "hum": 32.52
}
```

同时，模拟脚本还会随机产生各类客户端异常事件，包括：

- 消息丢弃事件：包括没有订阅者、消息过期等原因
- 设备断开连接事件：包括正常断连，以及异常的不支持的 QoS、发布主题错误等原因
- 发布与订阅失败时间：由于没有 ACL 权限发布与订阅失败等原因

以上消息和事件都可以通过 EMQX 的规则引擎进行捕获处理，之后通过数据集成写入或更新到 Redis 中，可以执行以下查看 Redis 中数据情况：

```shell
$ docker exec -it redis bash
$ redis-cli
$ keys *
1) "emqx_message_dropped_count"
2) "emqx_messages"
3) "disconnected_reason"
4) "authz_result"
5) "message_dropped_reason"
6) "authz_source"
```

下面我们详细解析一下 EMQX 是如何配置实现数据写入的。

### 温湿度数据暂存

EMQX 将创建一条规则，处理 MQTT 上报的温湿度消息。您也可以在之后修改这条规则，利用 EMQX 的[内置 SQL 函数](https://docs.emqx.com/en/enterprise/v5.4/data-integration/rule-sql-builtin-functions.html)进行自定义处理。

```sql
SELECT
  *
FROM "store-last-message/+"
```

在规则对数据进行处理后，EMQX 将通过规则动作将消息载荷中的温湿度数据实时更新到 Redis 中。

EMQX 对 Redis 的数据集成支持使用 Redis 命令模板进行数据插入，这种方式可以充分利用 Redis 多样化的数据结构，从而实现数据的灵活操作和业务开发。

EMQX 将使用以下 Redis 命令模板，按照客户端 ID 存储最后一条消息中的温度数据，创建 Redis 动作时对应的命名模板：

```
HSET emqx_messages ${clientid} ${payload.temp}
```

### 设备事件记录

EMQX 还将创建多条规则，用于将记录连接到 EMQX 的采集设备的异常行为，以便进行设备管理和行为分析。EMQX 规则引擎支持完整的 MQTT 设备生命周期事件处理，您也可以参考[此处](https://docs.emqx.com/zh/enterprise/v5.4/data-integration/rule-sql-events-and-fields.html#客户端事件)通过规则引擎监控更多事件。

#### 授权事件处理

处理来自 EMQX `$events/client_check_authz_complete` 主题的数据，对应授权检查完成事件。规则 SQL：

```sql
SELECT
  *
FROM "$events/client_check_authz_complete"
```

分别按照授权来源和授权结果进行计数，创建 Redis 动作时对应的命名模板：

```
HINCRBY authz_source ${authz_source} 1
HINCRBY authz_result ${result}:${action} 1
```

#### 客户端断开连接事件处理

处理来自 EMQX `$events/client_disconnected` 主题的数据，对应客户端断开连接的事件，规则 SQL：

```sql
SELECT
  *
FROM "$events/client_disconnected"
```

根据断开连接的原因进行计数，创建 Redis 动作时对应的命名模板：

```
HINCRBY disconnected_reason ${reason} 1
```

#### 消息丢弃事件处理

处理来自 EMQX `$events/message_dropped` 和 `$events/delivery_dropped` 主题的数据，对应消息丢弃的事件，，规则 SQL：

```sql
SELECT
  *
FROM "$events/message_dropped", "$events/delivery_dropped"
```

别按照丢弃消息的主题和丢弃的原因进行计数，创建 Redis 动作时对应的命名模板：

```
HINCRBY emqx_message_dropped_count ${topic} 1
HINCRBY message_dropped_reason ${reason} 1
```

## 在 Grafana 中查看分析

要在 Grafana 仪表板中查看管道数据，请在浏览器中打开 `http://localhost:3000`，使用用户名 `admin` 和密码 `public` 登录。

登录成功后，进入 `Home → Dashboards` 页面，选择 `Redis` 仪表盘。该仪表板展示了当前暂存的温度数据，以及客户端异常行为事件的统计情况。通过这些关键指标，您可以直观地监测环境数据以及 EMQX 上客户端的运行情况，防范潜在的安全风险。

![View Data in Grafana](https://assets.emqx.com/images/c986131e6391f8fd107ba2fb6ab00dfc.png)

## EMQX + Redis 的更多应用场景

除了本文使用到的 Redis 实时数据分析特性，EMQX 与 Redis 的结合还具有非常广泛的应用场景，包括：

- **实时数据流**：EMQX 专为处理实时数据流而构建，确保从设备到 Redis 的高效可靠的数据传输。Redis 能够快速执行数据操作，能够满足实时数据暂存，使其成为 EMQX 的理想数据存储组件。
- **用户行为跟踪：**Redis 提供了强大的时间窗口能力，例如可以跟踪用户在过去一段时间内的行为，使用位图数据，依靠轻量级的数据就能实现实时的结果统计和输出。
- **地理位置分析**：Redis 提供了地理位置相关的数据结构和命令，可以用于存储和查询地理位置信息。结合 EMQX 强大的设备接入能力，能够广泛应用在物流、车联网、智慧城市等各类物联网应用中。

值得一提的是，在 EMQX 的分布式架构和 Redis 的集群模式支持下，应用可随着数据量的增加实现无缝扩展，即使对于大型数据集，也可以确保一致的性能和响应能力。

## 结语

在本文中，我们探讨了如何集成 EMQX 和 Redis 来构建物联网实时数据统计应用。通过使用 EMQX 作为实时 [MQTT Broker](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)，并将数据导入到 Redis，我们实现了一个端到端的解决方案，用于实现通用的物联网数据与 EMQX 客户端事件分析。

在各行业的物联网应用中，围绕数据采集、传输以及分析，EMQX + Redis 提供了强大的集成能力，能够实现丰富的数据存储和分析操作。基于两者的高性能、实时性、可扩展性和灵活性，组合可以有效地处理大量的设备连接和数据流，从而使得数据驱动的决策变得更加快速和准确。

总的来说，EMQX 和 Redis 的结合，为物联网领域带来了一种新的、强大的解决方案，能够帮助企业更好地利用数据，驱动创新和提高效率。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
