In today's highly connected digital landscape, the complexity of real-time data streams is growing, particularly in IoT and microservices architectures. Enterprises and developers face a common challenge: disparate data protocols and systems often create isolated "data silos." This fragmentation increases development and maintenance costs while hindering the full utilization of data, leading to missed opportunities for critical business insights and real-time decision-making.

EMQX, a unified MQTT and AI platform for IoT real-time intelligence, delivers efficient and reliable connectivity. Since version 5.0, EMQX has introduced a robust protocol gateway feature to transcend the limitations of the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt), enabling connections from non-MQTT clients. This innovation establishes EMQX as a true unified messaging platform, seamlessly integrating diverse systems and devices.

With the release of EMQX 5.10.0, the protocol gateway family welcomes a new addition: the EMQX NATS Gateway. This feature expands EMQX's connectivity by enabling native, bidirectional interoperability between MQTT and NATS protocols, offering unprecedented flexibility for building robust real-time data infrastructures.

![image.png](https://assets.emqx.com/images/4754dc05f45f77fb8c2da8a56f3fe43e.png)

## What is the NATS Protocol?

[NATS (Neural Autonomic Transport System)](https://nats.io/) is a high-performance, lightweight, cloud-native messaging system designed for modern distributed applications. Known for its simplicity and efficiency, NATS supports multiple messaging patterns, including publish-subscribe and request-reply, and offers client libraries for various programming languages.

**Key Features of NATS:**

- **High Performance and Low Latency**: NATS uses a lightweight protocol and optimized routing for high-throughput, low-latency message delivery. Core NATS provides "at-most-once" semantics, ideal for high-speed, high-availability scenarios.
- **Cloud-Native Design**: Built for cloud environments, NATS supports deployment on bare metal, virtual machines, containers, or Kubernetes, with clustering for high availability and scalability.
- **Simplicity**: The NATS protocol and client libraries are user-friendly, reducing development and operational complexity.
- **Subject-Based Addressing**: NATS routes messages via subjects, supporting single- and multi-level wildcard patterns for flexible M:N communication.

## MQTT vs. NATS

| **Feature**             | **MQTT**                                                     | **NATS**                                                     |
| :---------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Transport Layer**     | TCP/TLS, WebSocket/WebSocket over SSL                        | TCP/TLS, WebSocket/WebSocket over SSL                        |
| **Message Format**      | Compact binary with rich fields                              | Plain text with minimalist semantics                         |
| **Client Connection**   | Supports persistent sessions (Clean Session) with reconnection support | No persistent session concept                                |
| **Messaging Patterns**  | Publish/Subscribe                                            | Publish/SubscribeRequest/ReplyQueuing                        |
| **Topic Structure**     | Hierarchical topics (using `/`) with wildcards (`+`, `#`)    | Flat subjects (using `.`) with wildcards (`*`, `>`)          |
| **Message QoS**         | Built-in QoS:QoS 0 (at most once)QoS 1 (at least once)QoS 2 (exactly once) | Controlled via acknowledgment mechanism:At most once (no confirmation)At least once (with confirmation) |
| **Message Persistence** | Built-in persistent sessions and retained messages for QoS 1/2 | Core NATS: no persistence; JetStream extension offers configurable persistence |
| **Use Cases**           | IoT devices, sensor networks, mobile apps, smart homes, industrial automation | Microservices, real-time data streaming, command/control systems, financial services, event-driven architectures |
| **Ecosystem**           | Widely used in IoT with extensive client libraries and brokers | CNCF project, growing in cloud-native, microservices, and real-time communication |

While both protocols excel in their domains, their differences traditionally required complex custom bridges for interoperability. The EMQX NATS Gateway bridges this gap, enabling seamless data sharing between IoT devices (typically MQTT) and backend microservices (often NATS). This integration eliminates data silos, simplifies system architecture, and provides enterprises with flexibility to choose the best protocol for their needs while ensuring seamless communication across components.

## Get Started with EMQX NATS Gateway

This section provides a concise guide to get started with NATS Gateway, including installing EMQX 5.10.0 and configuring the NATS Gateway.

### Installing EMQX 5.10.0

Download EMQX 5.10.0 from the [official download page](https://www.emqx.com/en/try) for your operating system (e.g., Debian, macOS).

**Example: Docker Installation**

```shell
docker run --name emqx \
 -p 18083:18083 -p 1883:1883 -p 20243:20243 \
 -d emqx/emqx-enterprise:5.10.0
```

After starting, access the EMQX Dashboard at `http://localhost:18083/` (default credentials: `admin`/`public`).

### Enabling and Configuring the NATS Gateway

The NATS Gateway can be configured via the Dashboard or configuration files:

1. Log in to the EMQX Dashboard.

2. Navigate to **Management** > **Gateways** in the sidebar.

3. Locate the NATS Gateway and click **Setup**.

   ![image.png](https://assets.emqx.com/images/7330beabc578c874293133def5314a33.png)

4. In **Basic Parameters**, keep defaults:

  - **MountPoint**: Optional prefix for NATS client topics (leave empty for none).

  - **Default Heartbeat Interval**: Time between heartbeats sent to clients.

  - **Heartbeat Timeout Threshold**: Maximum wait for client heartbeat response (default: 5 seconds, that is, if no heartbeat response is received from the client within 5 seconds, the client is considered disconnected.).

  ![image.png](https://assets.emqx.com/images/f9ec0e28ab2264f321e65b245b8627c0.png)

5. Proceed to **Listeners**, add a listener named `default` on port `20243`, and click **Add**.

   ![image.png](https://assets.emqx.com/images/916e1efa063625d5c1ef777ff3040f8e.png)

6. Click **Enable** to activate the NATS Gateway.

   ![image.png](https://assets.emqx.com/images/2f860761abe3f0fe3e2c2ef73684630e.png)

## Demonstration: MQTT-NATS Interoperability with Python

This section demonstrates bidirectional messaging between NATS and MQTT clients using Python.

First, ensure a Python environment with the required libraries:

```shell
pip install nats-py paho-mqtt
```

We will cover two scenarios:

1. NATS client publishes, MQTT client subscribes.
2. MQTT client publishes, NATS client subscribes.

### **Scenario 1: NATS Publishes, MQTT Subscribes**

`nats_publisher.py`: Connects to the EMQX NATS Gateway and publishes to `sensor.data.temperature`.

```python
import asyncio
import nats

async def run():
    nc = await nats.connect(servers=["nats://localhost:20243"])
    print("NATS Publisher connected to EMQX NATS Gateway.")

    subject = "sensor.data.temperature"
    message = b'{"device_id": "sensor_001", "temp": 25.5}'

    await nc.publish(subject, message)
    print(f"Published NATS message to subject '{subject}': {message.decode()}")

    await nc.drain()
    print("NATS Publisher disconnected.")

if __name__ == '__main__':
    asyncio.run(run())
```

`mqtt_subscriber.py`**:** Connects to the EMQX MQTT listener and subscribes to the mapped topic  `sensor/data/temperature`.

```python
import paho.mqtt.client as paho
from paho import mqtt
import time

# MQTT message callback function
def on_message(client, userdata, msg):
    print(f"Received MQTT message on topic '{msg.topic}': {msg.payload.decode()}")

def run():
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_message = on_message

    # Connect to the EMQX MQTT listener (default port 1883)
    client.connect("localhost", 1883, 60)
    print("MQTT Subscriber connected to EMQX.")

    # Subscribe to the mapped MQTT topic
    # According to the NATS Gateway's topic_mapping rules, iot.sensor.data.temperature is mapped to sensor/data/temperature
    client.subscribe("sensor/data/temperature", qos=1)
    print("MQTT Subscriber subscribed to 'sensor/data/temperature'.")

    client.loop_forever()

if __name__ == '__main__':
    run()
```

**Steps**:

1. Run `mqtt_subscriber.py`.
2. Run `nats_publisher.py`. The MQTT subscriber will receive the NATS message.

### **Scenario 2: MQTT Publishes, NATS Subscribes**

`mqtt_publisher.py`: Connects to the EMQX MQTT listener and publishes to `command/device/light_001`.

```python
import paho.mqtt.client as paho
from paho import mqtt
import time

def run():
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

    # Connect to the EMQX MQTT listener (default port 1883)
    client.connect("localhost", 1883, 60)
    print("MQTT Publisher connected to EMQX.")

    topic = "command/device/light_001"
    message = '{"action": "turn_on", "brightness": 80}'

    client.publish(topic, message, qos=1)
    print(f"Published MQTT message to topic '{topic}': {message}")

    client.disconnect()
    print("MQTT Publisher disconnected.")

if __name__ == '__main__':
    run()
```

`nats_subscriber.py`**:** Connects to the EMQX NATS Gateway and subscribes to the mapped subject `command.device.light_001`.

```python
import asyncio
import nats

async def message_handler(msg):
    print(f"Received NATS message on subject '{msg.subject}': {msg.data.decode()}")

async def run():
    # Connect to the EMQX NATS Gateway
    nc = await nats.connect(servers=["nats://localhost:20243"])
    print("NATS Subscriber connected to EMQX NATS Gateway.")

    # Subscribe to the mapped NATS Subject
    # command/device/light_001 is mapped to command.device.light_001
    await nc.subscribe("command.device.light_001", cb=message_handler)
    print("NATS Subscriber subscribed to 'device.command.light_001'.")

    # Maintain connection and wait for messages
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        await nc.drain()
        print("NATS Subscriber disconnected.")

if __name__ == '__main__':
    asyncio.run(run())
```

**Steps**:

1. Run `nats_subscriber.py`.
2. Run `mqtt_publisher.py`. The NATS subscriber will receive the MQTT message.

These examples demonstrate how the EMQX NATS Gateway seamlessly translates and forwards messages between MQTT and NATS, simplifying integration across heterogeneous systems.

## Conclusion

The EMQX 5.10.0 NATS Gateway marks a significant step toward unified, flexible real-time data infrastructures. By enabling native, bidirectional MQTT-NATS interoperability, it eliminates protocol barriers, simplifies complex integrations, and reduces development and operational costs. This innovation empowers applications in IoT, microservices, and real-time control, ensuring seamless data flow across ecosystems—whether streaming sensor data to cloud microservices or sending commands to edge devices.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
