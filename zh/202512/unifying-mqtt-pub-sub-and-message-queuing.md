## MQTT 发布/订阅模式的局限性

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt)（消息队列遥测传输）协议凭借其代码体积小、带宽占用低的特性，在物联网通信中不可或缺。

其核心价值在于采用了**发布/订阅（Pub/Sub）模型**，这使其非常适合实时一对多消息推送/分发以及设备到云的遥测传输等场景。

尽管 MQTT 在实时通信和资源受限环境中表现出色，但标准 Pub/Sub 模型存在一个关键的内在缺陷：**离线订阅者在断开连接期间，会错过所有被发布的消息。**

对于不要求完整性的实时传感器数据而言，这或许影响不大。但对于任何要求**可靠性**和**消息持久性**的物联网应用场景，这种机制会带来严重的问题。**例如以下两个场景中，消息必须持久化、不容有失：**

1. **命令队列**：

   假设您需要向一组连接不稳定或间歇性离线的设备发送关键固件更新、或紧急关机命令，如果设备在指令发送时恰好处于离线状态，该指令就会永久丢失。这可能导致系统安全漏洞、设备运行不一致，甚至引发安全事故。

2. **任务队列**：

   当系统需要向一组可能不同时在线的 Worker 节点分配复杂的处理任务时，如果任务消息丢失，将导致工作节点无法接收任务，进而引发系统故障、数据处理中断或最终的数据不一致。

## “ MQTT + 消息队列 ” 架构的困境

为了弥补 MQTT 发布/订阅模式中离线消息丢失的缺陷，传统上的解决方案是引入 RabbitMQ、Kafka 或数据库等外部系统作为持久化消息存储层。

这种方案会导致架构变得分离：

- [**MQTT 服务器**](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)**：**负责处理设备与云端之间的初始通信。
- **外部消息队列：**用于实现消息持久化、任务队列和后端集成。

这种架构上的分离，虽然解决了消息持久化问题，但需要额外管理、监控和扩展独立的基础设施，带来了复杂度、通信延迟与成本的提升。

## EMQX 6.0 引入原生消息队列

EMQX 6.0 内部原生集成了完整的消息队列功能，将实时 MQTT 发布/订阅模式与可靠持久的消息传递能力相结合。基于其优化的内部存储机制，EMQX 6.0 可以安全地保存异步指令、任务队列及关键业务数据，确保消费者无论处于何种连接状态都能实现可靠的消息传递。

**主要优势：**

- **简化系统设计：**无需部署独立的外部消息队列系统，实现架构整合。
- **降低基础设施复杂性：**统一管理单个消息代理，替代多集群（MQTT + 消息队列）运维模式。
- **成本优化：**节省基础设施、维护和监控方面的总体开支。
- **保证消息持久性：**确保关键异步消息的安全存储和可靠传递，实现实时通信与持久化传输的无缝融合。

> *了解更多：*
>
> - [*一个代理，两种模式：EMQX 原生支持实时 MQTT 发布/订阅和持久队列*](https://www.emqx.com/zh/blog/real-time-mqtt-pub-sub-and-durable-queues-natively-in-emqx)
> - [*利用 EMQX 消息队列解决现实世界的物联网消息传递挑战*](https://www.emqx.com/zh/blog/solving-real-world-iot-messaging-challenges-with-emqx)

## EMQX 消息队列的工作原理

EMQX 消息队列的数据流简洁高效：发布者向主题发送消息后，一方面，EMQX 会将消息实时投递给所有普通订阅者；另一方面，若该主题配置了消息队列，EMQX 会将其存入持久化存储，随后由专用的消息队列消费者从存储中提取消息，并分发给一个或多个订阅者。

**其工作流程如下图所示：**

![image.png](https://assets.emqx.com/images/6023a38caad76fa96505603b70ed4aaa.png)

消息队列消费者支持多种消息分发策略（如随机、轮询、最小未确认数等），实现灵活的负载均衡与消息处理模式。

## **示例：任务队列**

让我们来看一个任务队列的实际示例。我们将使用 Docker Compose 来搭建一个环境，其中包含 EMQX 以及一些用于生产和消费任务的 Python 脚本。

您可以在 `job-queue` 目录下找到本示例所需的文件。

### **设置**

以下是 `docker-compose.yml` 文件：

```yaml
services:
  emqx:
    image: emqx/emqx:6.0.0
    ports:
      - "1883:1883"
      - "18083:18083"
    environment:
      - "EMQX_API_KEY__BOOTSTRAP_FILE=/opt/emqx/etc/api-keys.txt"
    volumes:
      - ./api-keys.txt:/opt/emqx/etc/api-keys.txt:ro
    healthcheck:
      test: ["CMD", "/opt/emqx/bin/emqx", "ctl", "status"]
      interval: 5s
      timeout: 25s
      retries: 5
  producer:
    build: ./producer
    command: python producer.py --topic jobs --interval 0.1 --count 500
  consumer1:
    build: ./consumer
    command: python consumer.py --name consumer1 --topic jobs
  consumer2:
    build: ./consumer
    command: python consumer.py --name consumer2 --topic jobs
```

`producer.py` 脚本会向 `jobs` 主题发布特定数量的任务。

```python
...

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("emqx", 1883, 60)
client.loop_start()

for i in range(args.count):
    client.publish(args.topic, payload=f"job {i}", qos=1)
    logger.info(f"Sent job {i} to {args.topic}")
    time.sleep(args.interval)

client.loop_stop()
client.disconnect()
logger.info("Producer finished.")
```

`consumer.py` 脚本会订阅 `$q/jobs` 队列，并处理它接收到的任务。

```python
...

def on_connect(client, userdata, flags, reason_code, properties):
    logger.info(f"{args.name} connected with result code {reason_code}")
    client.subscribe(f"$q/{args.topic}")

def on_message(client, userdata, msg):
    job = msg.payload.decode()
    logger.info(f"{args.name} received job: {job}")
    time.sleep(args.sleep)
    logger.info(f"{args.name} finished job: {job}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect("emqx", 1883, 60)

client.loop_forever()
```

### 场景一：简单的协作式任务处理

在这个场景中，我们将看到任务是如何在两个消费者之间随机分配的。

**启动 EMQX**：

```
docker - compose  up -d emqx  --force - recreate --build 
```

**创建队列：**

我们将创建一个名为 `jobs` 的队列，该队列会监听 `jobs` 主题过滤器。我们将使用 `random` 分派策略。您可以通过 EMQX Dashboard 或使用 `curl` 命令来完成此操作：

```shell
curl -u key:secret -X POST "http://localhost:18083/api/v5/message_queues/queues" \
     -H "Content-Type: application/json" \
     -d '{"topic_filter": "jobs", "dispatch_strategy": "random", "is_lastvalue": false}'
```

**查看 Docker Compose 日志**（可选，在单独的终端中查看）：

```shell
docker-compose logs -f
```

**运行消费者：**

```shell
docker-compose up -d consumer1 consumer2 --force-recreate --build
```

**运行生产者**：

```shell
docker-compose up producer --force-recreate --build
```

您将在日志中看到，这 500 个任务大致平均地分配给了 `consumer1` 和 `consumer2`。

### 场景二：包含慢速消费者的协作式任务处理

现在，我们来看看如果其中一个消费者处理速度很慢时，会发生什么情况。

**启动 EMQX**：

```shell
docker-compose down
docker-compose up -d emqx --force-recreate --build
```

**创建队列**：

```shell
curl -u key:secret -X POST "http://localhost:18083/api/v5/message_queues/queues" \
     -H "Content-Type: application/json" \
     -d '{"topic_filter": "jobs", "dispatch_strategy": "least_inflight", "is_lastvalue": false}'
```

请注意，我们使用 `least_inflight` 调度策略来平衡消费者之间的负载。

**运行消费者**：这次，我们将先 `consumer2` 休眠 500 毫秒，以模拟速度较慢的工作进程。

更新 Docker Compose 文件：

```shell
...
consumer2:
    build: ./consumer
    command: python consumer.py --name consumer2 --topic jobs --sleep 0.5
```

**启动生产者**：

```
docker - compose up  producer --force - recreate --build
```

在这种情况下，您将观察到 `consumer1` 接收到的任务数量明显多于 `consumer2`，因为 EMQX 会将消息分派给未处理（in-flight）消息最少的消费者。

重要的是，由于采用了 `least_inflight` 策略，队列处理不会被慢速消费者阻塞。

此外，拥有足够多的工作进程来处理任务（`consumer1` 足够快）使得所有任务几乎在相同的时间内完成。这对于像任务队列这样的 MQTT 应用至关重要。

## 示例：命令队列

另一个常见的应用场景是物联网设备的命令队列。在这种情况下，我们希望向设备发送命令，并且只关心针对特定功能的**最新命令***。*

假设我们有一个可以变换颜色的设备，颜色可以是绿色、红色和黄色。我们想通过远程应用程序控制该设备的颜色。该设备可能会暂时离线，但我们希望确保它重新上线后，能够根据最新的指令显示正确的颜色。

显然，当设备离线时，颜色可能会发生变化。因此，我们需要读取命令历史记录来确认正确的颜色。同时，我们并不想读取**完整的**历史记录，只需要读取最新的命令即可。

这就是**最后值语义**发挥作用的地方。通过配置队列，使其仅保留指定键对应的最新消息。

### 设置

该 `docker-compose.yml` 文件与上一个示例类似。

```yaml
services:
  emqx:
    image: emqx/emqx:6.0.0
    ports:
      - "1883:1883"
      - "18083:18083"
    environment:
      - "EMQX_API_KEY__BOOTSTRAP_FILE=/opt/emqx/etc/api-keys.txt"
    volumes:
      - ./api-keys.txt:/opt/emqx/etc/api-keys.txt:ro
    healthcheck:
      test: ["CMD", "/opt/emqx/bin/emqx", "ctl", "status"]
      interval: 5s
      timeout: 25s
      retries: 5
  command-producer:
    build: ./producer
  consumer:
    build: ./consumer
```

Python 脚本位于 `command-queue` 目录下。

`command-producer.py` 脚本如下：

```python
...

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="", protocol=mqtt.MQTTv5)
client.connect("emqx", 1883, 60)
client.loop_start()

colors = ["Green", "Red", "Yellow"]
i = 0

while True:
    color = random.choice(colors)
    i += 1
    payload = json.dumps({"color": color, "n": i})
    props = properties.Properties(packettypes.PacketTypes.PUBLISH)
    props.UserProperty = [("key", "set-color")]
    client.publish("commands/device1", payload=payload, qos=1, properties=props)
    logger.info(f"Sent command: {payload}")
    time.sleep(0.5)
```

请注意，关键用户属性被设置为 `set-color`**。**我们将配置队列，使其仅保留每个键的最后一条消息。

消费者将模拟一个接收命令并显示当前颜色的设备（"I am now"）。

`consumer.py` 脚本如下：

```python
...
def on_connect(client, userdata, flags, reason_code, properties):
    logger.info(f"Device connected with result code {reason_code}")
    client.subscribe("$q/commands/device1")

def on_message(client, userdata, msg):
    command = json.loads(msg.payload.decode())
    logger.info(f"I am {command['color']} now")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect("emqx", 1883, 60)

client.loop_forever()
```

### 场景

**启动 EMQX**：

```
docker - compose  up -d emqx  --force - recreate --build 
```

**创建队列**：

这次，我们将创建一个启用了最后值语义的队列。

我们将使用队列键表达式从 MQTT 消息的用户属性中提取一个键（Key）。

```shell
curl -u key:secret -X POST "http://localhost:18083/api/v5/message_queues/queues" \
     -H "Content-Type: application/json" \
     -d '{
           "topic_filter": "commands/device1",
           "is_lastvalue": true,
           "key_expression": "message.headers.properties.User-Property.key",
           "dispatch_strategy": "random"
         }'
```

**等待一段时间后，启动生产者：**

```shell
docker-compose up command-producer --force-recreate --build
```

生产者将开始每隔 0.1 秒发送一次颜色指令。

**等待一段时间，允许多条命令被发布。**

**启动消费者**：

```shell
docker-compose up consumer --force-recreate --build
```

您将观察到，该设备只接收到它上线前发送的最后一条命令，无需处理所有中间的颜色更改。此后，它将实时接收发布的新命令。

## 结论

EMQX 6.0 的消息队列功能是一项重要的能力增强，它在传统 MQTT 与企业级消息队列之间架起了桥梁。该功能使得离线和间歇性在线的客户端也能实现持久、可靠的消息通信，且无需依赖外部基础设施。通过支持多种分发策略及最后值语义，EMQX 为从任务队列到设备指令控制等各种应用场景，提供了一个高度灵活的解决方案。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
