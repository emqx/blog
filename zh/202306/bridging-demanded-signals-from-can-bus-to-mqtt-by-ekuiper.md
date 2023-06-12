CAN Bus 是一种广泛应用于汽车和工业领域的通信协议，它能够让多个设备在同一网络中进行交互。而 [MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种广泛应用于物联网领域的通信协议，作为一种轻量级的发布-订阅消息传输协议，它有效地促进了机器之间的通信。

通过将 CAN Bus 数据桥接到 MQTT，能够实现 CAN Bus 设备与物联网平台和应用的集成。尽管市场上存在多种解决方案和工具可以实现这一目标，但它们通常只传输原始的二进制 CAN 数据，这导致对信号进行过滤和处理非常不方便。

在本文中，我们将介绍一种全新的解决方案，通过使用 [开源边缘流式 SQL 引擎 eKuiper ](https://ekuiper.org/zh)，灵活地从 CAN Bus 提取有意义的数据和所需的信号，实现从 CAN Bus 到 MQTT 的无缝桥接。

## CAN Bus 的工作原理

CAN Bus 是一种通信系统，它能够让车辆中的不同设备相互传递数据。它还能提供许多有用的车辆信息，例如速度、油量、发动机温度和诊断码等。然而，从 CAN Bus 中获取和解读这些信息并不是一件容易的事情，因为它们通常以二进制形式进行存储。

> 深入了解 CAN Bus ，欢迎阅读：[车联网 CAN Bus 协议介绍与数据实时流处理](https://www.emqx.com/zh/blog/can-bus-how-it-works-pros-and-cons)

### CAN 帧

我们可以从 CAN Bus 接收 CAN 帧流，其中包含我们感兴趣的二进制形式的信号。每个 CAN 帧都包含 ID、数据长度码（DLC）和有效载荷。

- ID 用来标识帧中数据的类型。
- DLC 用来指定帧中数据的字节数。
- 有效载荷是帧中携带的实际数据。

CAN 协议有多种类型，它们在 ID 和有效载荷长度的定义上略有不同。下面是一个 CAN 2.0A 帧的例子，其 ID 为 11 位，有效载荷长度最多为 8 字节。

![CAN 2.0A 帧例子](https://assets.emqx.com/images/aa1030c3e586222227d7c20357d77efd.png)

有效载荷由一系列信号组成。每个信号都有名称、长度和值。

- 长度是信号在有效载荷里占用的位数。
- 值是信号里包含的实际数据。

为了把二进制数据转换成有意义的信息，我们需要提取这些信号。

### 信号提取

CAN 数据库（DBC）是一个文本文件，用于描述 CAN 帧有效载荷中信号的组织方式。它相当于一个字典，提供了每个信号的名称、长度和值的计算方法，这样我们就可以通过 CAN 帧进行通信。

下面是 DBC 文件的一段内容。它定义了一个 ID 为 544，DLC 为 8 的 CAN 帧。该帧包含 5 个信号，每个信号都有名称、长度和值。例如，信号 EngineSpeed 的长度为 16 位，值的范围是 0 到 16383.75。信号的值是通过把原始数据乘以 0.25 再加上 0 来计算得出。

```
BO_ 544 EMS_220h: 8 EMS
SG_ EngineSpeed : 0|16@1+ (0.25,0) [0|16383.75] "rpm" Vector__XXX
SG_ CurrentEngineTorque : 16|16@1+ (0.25,-500) [-500|1547.5] "Nm" Vector__XXX
SG_ DriverRequestTorque : 32|16@1+ (0.25,-500) [-500|1547.5] "Nm" Vector__XXX
SG_ CurrentEngineTorqueStatus : 48|1@1+ (1,0) [0|1] "" Vector__XXX
SG_ DriverRequestTorqueStatus : 49|1@1+ (1,0) [0|1] "" Vector__XXX
```

CAN 帧的解码流程如下：

![CAN 帧解码流程](https://assets.emqx.com/images/2a92a31f0cbff93106d13adcf33e10d1.png)

完成解码后，我们可以得知发动机的转速为每分钟 1000 转。然而通过编写应用进行信号解码的话，一旦信号发生变化或更新，我们就必须重新开发和部署整个解码过程，并通过 OTA 进行更新。使用 eKuiper 可以帮助您省去这些繁琐的工作。

### 保护您的 DBC

DBC 是解码 CAN 帧的关键。即使 CAN Bus 数据泄露，没有 DBC 也几乎无法解码。因此，DBC 是您的重要资产，不应向任何人泄露，包括参与解码开发的工程师。eKuiper 可以在运行时加载 DBC 文件，从而可以避免让开发者看到它。此外，当场景发生变化时，它可以在不重启进程的情况下热加载 DBC 文件。这有助于保护您的 DBC 文件，使其保持私密。

## eKuiper「理解」CAN Bus 数据

作为一个边缘流式引擎，eKuiper 非常轻巧，可以部署在 CAN Bus 设备附近。它能够从 HTTP、文件系统、MQTT，以及本文所提到的 CAN Bus 等各种南向数据源收集数据。收集到的数据可以高效地进行处理，并发布到北向数据源（例如 MQTT 和 HTTP）。

eKuiper 具备对 CAN Bus 数据的理解能力。它简化了 CAN 帧的解码过程，并将其转化为一些配置信息。要处理 CAN Bus 数据，您可以使用以下 SQL 语句创建一个流：

```
CREATE STREAM canDemo () WITH (TYPE="can", FORMAT="can", SHARED="TRUE", SCHEMAID="dbc")
```

这条语句创建了一个名为 canDemo 的流，用于从 CAN Bus 中获取数据。该语句还指定了连接方式和数据格式，并指定使用 DBC 模式将 CAN 帧解码成信号。

### DBC 设置

DBC 文件在解码 CAN 帧时扮演了模式的角色。就像为 protobuf 格式指定 *.proto 文件一样，您可以在 SCHEMAID 属性中指定 DBC 文件，它可以是文件路径也可以是目录路径。这意味着您可以指定一个单独的 DBC 文件或一个包含多个 DBC 文件的目录。eKuiper 会加载目录中的所有 DBC 文件，并将它们作为模式使用。

在运行时，用户可以通过替换文件或向目录中添加新文件来更新 DBC 文件。eKuiper 能够热加载 DBC 文件，并通过重启规则来使用新的模式解码 CAN 帧。这可以帮助您保护 DBC 文件，让它保持私密。

### 连接和格式分离

在创建流的语句中，我们将 `type` 属性和 `format` 属性都设置为"can"。这是因为 eKuiper 将数据源的连接方式和数据格式进行了分离。

- `type` 属性指定了连接方式，本案例中是 CAN Bus 。
- `format` 属性指定了数据格式，本案例中是 CAN 帧。

这种分离使得 eKuiper 能够支持 CAN 帧和传输协议的各种组合，这在使用一些 CAN 适配器时非常常见。CAN 适配器可能会将 CAN 帧记录到文件中，或者将原始的 CAN 帧发送到 [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)，或者通过 TCP 或 UDP 以批量的形式发送 CAN 帧。在这些情况下，`type` 属性将是"file"或"mqtt"，而 `format` 属性将是"can"。

如果 `type` 是“can”，eKuiper 会通过 socketCan 连接到 CAN Bus 。在下面的例子中，eKuiper 从文件中读取 CAN 帧：

```
CREATE STREAM canDemo () WITH (TYPE="file", FORMAT="can", SHARED="TRUE", SCHEMAID="dbc")
```

## 将 CAN Bus 灵活地桥接到 MQTT

CAN Bus 设备会以高频率（如 100HZ）在总线上周期性地发送消息。由于存储或带宽的限制，我们可能只想以较低的频率对数据进行采样，并有选择的保留信号。有了 eKuiper，我们可以：

- 通过指定采样率来对数据进行采样。
- 通过选择所需的信号来在信号层面对数据进行过滤。
- 只桥接发生变化的信号。
- 将不同 CAN 帧中的信号合并成一个消息。

所有这些功能都可以通过规则 SQL 来实现，并且由于具备规则热加载的能力，所以变更几乎没有成本。下面让我们看一些例子。

```
## 过滤信号
SELECT EnginSpeed, DriverRequestTorqueStatus FROM canDemo
## 将不同 CAN 帧中的信号合并
SELECT latest(EnginSpeed) as speed, latest(anotherSignal) as anotherSignal FROM canDemo
## 只桥接发生变化的信号
SELECT CHANGED_COLS(EngineSpeed, DriverRequestTorqueStatus) FROM canDemo
```

一旦获得了所需的信号，我们就需要决定将数据发布到哪个 [MQTT 主题](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)。用户可以指定一个固定的主题名称，或者使用从数据中派生出来的动态主题名称。

例如，在下面的规则中，每个解析出的 CAN 帧信号都会被桥接到 MQTT 主题 `can/{{CanId}}`。`{{CanId}}` 是从数据中派生出的动态主题名称，比如一个 CAN ID 为 123 的 CAN 帧将被桥接到 MQTT 主题 `can/123`。

```
{
 "id": "distributeRule",
 "sql": "SELECT *, meta(id) as canId FROM canDemo",
 "actions": [
  {
     "mqtt": {
       "server": "tcp://broker.emqx.io:1883",
       "topic": "can/{{.canId}}",
       "sendSingle": true
    }
  }
]
}
```

eKuiper 允许多个规则处理同一个流。因此，用户可以根据需要创建多个规则，将 CAN Bus 数据桥接到不同的 MQTT 主题。

## 结语

要实现 CAN Bus 和 MQTT 之间的桥接，我们的解决方案要能够从 CAN Bus 设备读取数据，根据需求对数据进行过滤和转换，并将数据发布到 MQTT Broker。这正是 eKuiper 的用武之地，它提供了一种简单、高效和灵活的方式来完成这项工作。

除了桥接功能，eKuiper 还可以在边缘规则引擎和边缘计算的多种场景中提供帮助。我们将在后续的文章中详细讨论这些场景。



<section class="promotion">
    <div>
        免费试用 EMQX 企业版
            <div class="is-size-14 is-text-normal has-text-weight-normal">无限连接，任意集成，随处运行。</div>
    </div>
    <a href="https://www.emqx.com/zh/try?product=enterprise" class="button is-gradient px-5">开始试用 →</a>
</section>
