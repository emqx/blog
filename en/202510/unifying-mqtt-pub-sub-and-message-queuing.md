## The Missing Piece: Why MQTT’s Pub/Sub Alone Isn’t Enough

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) (Message Queuing Telemetry Transport) is essential for IoT communication, valued for its small code size and low bandwidth use. Its publish-subscribe model effectively connects resource-constrained devices over unreliable networks, making it ideal for real-time fanout and device-to-cloud telemetry.

However, the standard pub/sub model has a major flaw: offline subscribers miss messages sent while they're away. This is fine for live sensor data but poses challenges for applications that require reliability and durability.

Consider scenarios where message persistence is non-negotiable:

- **Command Queuing**: Imagine sending a crucial firmware update or a critical shutdown command to a fleet of devices with intermittent connectivity. If the device is offline, the command is lost.
- **Job Queuing**: Distributing tasks to a pool of workers that may not all be active at the same time. Missing a task means system failure or data inconsistency.

## The Problem of the “MQTT + MQ” Architecture

Traditionally, solving this problem required external systems like RabbitMQ, Kafka, or a database to act as a message store. The result is a complex architecture:

1. **[MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison):** Handles the initial device-to-cloud communication.
2. **External MQ:** Used for durability, task queuing, and back-end integration.

This separation introduces **complexity, latency, higher operational costs, and another layer of infrastructure** to manage, monitor, and scale. 

## Introducing MQTT Queues in EMQX 6.0

EMQX 6.0 introduces a native, fully integrated Message Queues feature within the broker, combining real-time MQTT pub/sub with guaranteed, durable message delivery. Its optimized internal storage securely persists asynchronous commands, job queues, and critical data for consumers, ensuring delivery regardless of connection status.

**Key benefits:**

- **Simplified System Design:** Consolidate your architecture by removing the need for a separate external MQ system.
- **Reduced Infrastructure Complexity:** Manage a single, unified messaging broker instead of multiple clusters (MQTT + MQ).
- **Lower Operational Costs (TCO):** Save on infrastructure, maintenance, and monitoring overhead.
- **Guaranteed Message Durability:** Ensure critical asynchronous messages are securely stored and reliably delivered, bridging the gap between real-time and persistent communication.

> Learn more:
>
> - [One Broker, Two Paradigms: Real-Time MQTT Pub/Sub and Durable Queues, Natively in EMQX](https://www.emqx.com/en/blog/real-time-mqtt-pub-sub-and-durable-queues-natively-in-emqx) 
> - [Solving Real-World IoT Messaging Challenges with EMQX Message Queues](https://www.emqx.com/en/blog/solving-real-world-iot-messaging-challenges-with-emqx) 

## How EMQX Message Queues Work

The data flow for an EMQX Message Queue is straightforward. A publisher sends a message to a topic. EMQX intercepts this message and, if a queue is configured for that topic, stores it in durable storage. A dedicated Message Queue Consumer process then retrieves queue's messages from storage and dispatches them to one or more subscribers.

Here is a diagram illustrating the flow:

![ef725c7c93d2bd1236f8b2991e6a408b.png](https://assets.emqx.com/images/5619947da42947c709343591697fa521.png)

The Message Queue Consumer can use different dispatch strategies to distribute messages among subscribers, such as `random`, `round_robin`, or `least_inflight`. This allows for flexible load balancing and processing patterns.

## Example: Job Queue

Let's walk through a practical example of a job queue. We'll use Docker Compose to set up an environment with EMQX and some Python scripts to produce and consume jobs.

You can find the files for this example in the `job-queue` directory.

### Setup

Here is the `docker-compose.yml` file:

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

The `producer.py` script publishes a specified number of "jobs" to the `jobs` topic.

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

The `consumer.py` script subscribes to the `$q/jobs` queue and processes the jobs it receives.

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

### Scenario 1: Simple Cooperative Job Handling

In this scenario, we'll see how jobs are distributed randomly between two consumers.

1. **Start EMQX**:

   ```
   docker-compose up -d emqx --force-recreate --build
   ```

2. **Create the queue**: We'll create a queue named `jobs` that listens on the `jobs` topic filter. We'll use the `random` dispatch strategy. You can do this via the EMQX Dashboard or with a `curl` command:

   ```shell
   curl -u key:secret -X POST "http://localhost:18083/api/v5/message_queues/queues" \
        -H "Content-Type: application/json" \
        -d '{"topic_filter": "jobs", "dispatch_strategy": "random", "is_lastvalue": false}'
   ```

3. ** Wach docker compose logs** (optional, in a separate terminal):

   ```shell
   docker-compose logs -f
   ```

4. **Start the consumers**:

   ```shell
   docker-compose up -d consumer1 consumer2 --force-recreate --build
   ```

5. **Start the producer**:

   ```shell
   docker-compose up producer --force-recreate --build
   ```

You will see in the logs that the 500 jobs are distributed roughly evenly between `consumer1` and `consumer2`.

### Scenario 2: Cooperative Job Handling with Slow Consumer

Now, let's see what happens if one of the consumers handles slowly.

1. **Start EMQX**:

   ```shell
   docker-compose down
   docker-compose up -d emqx --force-recreate --build
   ```

2. **Create the queue**:

   ```shell
   curl -u key:secret -X POST "http://localhost:18083/api/v5/message_queues/queues" \
        -H "Content-Type: application/json" \
        -d '{"topic_filter": "jobs", "dispatch_strategy": "least_inflight", "is_lastvalue": false}'
   ```

   Note that we use `least_inflight` dispatch strategy to balance the load between the consumers.

3. **Start the consumers**: This time, we'll start `consumer2` with a 500ms sleep to simulate a slower worker. Update the docker compose file:

   ```
   ...
   consumer2:
       build: ./consumer
       command: python consumer.py --name consumer2 --topic jobs --sleep 0.5
   ```

4. **Start the producer**:

   ```
   docker-compose up producer --force-recreate --build
   ```

In this case, you'll observe that `consumer1` (the faster consumer) receives significantly more jobs than `consumer2`, as EMQX dispatches messages to the consumer with the fewest outstanding (in-flight) messages.

The important thing is that due to the `least_inflight` strategy, the *queue handling was not blocked by the slower consumer*. Moreover, having enough workers to handle the jobs (`consumers1` is fast enough) made it possible to handle all the jobs within almost the same time. This is crucial for MQTT applications like job queues.

## Example: Command Queue

Another common use case is a command queue for IoT devices. Here, we want to send commands to a device, and we only care about the *latest* command for a particular function.

Assume we have a device that can change its color to "Green", "Red", and "Yellow". We want to control the device color from a remote application. The device may go offline for a while, but we want to ensure that when it comes back online, it will display the correct color (according to the latest command).

Obviously, the color may change while the device is offline. So we need to read the history of commands to know the correct color. At the same time, we do not care about the *whole* history, we only care about the latest command.

This is where **Last Value Semantics** comes in. We can configure the queue to only keep the last message for a given key.

### Setup

The `docker-compose.yml` is similar to the previous example.

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

The Python scripts are in the `command-queue` directory.

`command-producer.py`:

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

Note the `key` User-Property is set to `set-color`. We will configure the queue to keep only the last message for each key.

The consumer will emulate a device that receives the commands and prints the color "I am now".

`consumer.py`:

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

### Scenario

1. **Start EMQX**:

   ```
   docker-compose up -d emqx --force-recreate --build
   ```

2. **Create the queue**: This time, we'll create a queue with Last Value Semantics enabled. We use a **Queue Key Expression** to extract a key from the `User-Property` of the MQTT message.

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

3. Wait for some time and **start the producer**:

   ```shell
   docker-compose up command-producer --force-recreate --build
   ```

   The producer will start sending color commands every 0.1 seconds.

4. **Wait for some time**, allowing many commands to be published.

5. **Start the device (consumer)**:

   ```shell
   docker-compose up consumer --force-recreate --build
   ```

You will observe that the device *only* receives the very last command that was sent before it came online. It doesn't have to process all the intermediate color changes. After that, it will receive new commands in real-time as they are published.

## Conclusion

EMQX's Message Queue feature is a powerful addition that bridges the gap between traditional MQTT and enterprise message queuing. It allows for durable, reliable messaging for offline or intermittently connected clients, without the need for external infrastructure. By supporting different dispatch strategies and last-value semantics, it provides a flexible solution for a wide range of use cases, from job queues to device command and control.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
