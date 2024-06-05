## MQTT 与 Protobuf

在日益复杂的数据交换环境中，选择正确的数据序列化格式显得至关重要。Protobuf 因其高效的序列化特性，已被广泛应用于大型互联网公司和各类微服务项目中。与此同时，[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 作为一个轻量级基于发布订阅模式的消息传输协议，与 Protobuf 的结合显然可以进一步优化物联网数据交换体验。

如何确保和测试 Protobuf 消息在 MQTT 中正确发布和接收是一个关键问题。[MQTTX](https://mqttx.app/zh) —— 一款开源的全功能 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)，支持从 JSON、Base64 到现如今的 Protobuf 的多种格式。在这篇文章中，我们将展示如何使用 MQTTX 来定义、发布和接收 Protobuf 消息。

## 准备工作

为确保顺利地与物联网设备交流，我们需要安装一个 EMQX MQTT Broker 和 MQTTX 客户端。EMQX 可以为物联网设备提供消息传输功能，MQTTX 则允许我们进行消息的发布和订阅。

### 安装 EMQX

EMQX 是一个高性能、可扩展的 MQTT 平台，适用于物联网、工业物联网和车载网络场景。我们选择了 5.5.1 版本的 EMQX 企业版，因为其规则引擎能够使用 Protobuf 进行编码和解码，便于处理和验证 Protobuf 数据。

- 使用 Docker 安装：

  ```shell
  docker run -d --name emqx-enterprise -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx-enterprise:5.5.1
  ```

- 对于非 Docker 用户，EMQX 提供 RPM 或 DEB 包。[EMQX 5.5 安装指南](https://docs.emqx.com/zh/emqx/v5.5/deploy/install.html)提供了详细的安装说明。

### 安装 MQTTX 客户端

MQTTX 提供桌面版和命令行版本，均支持 Protobuf 消息传输。您可以根据需求访问 [MQTTX 官网](https://mqttx.app/zh/downloads) 下载合适的版本。

## 在 MQTTX 桌面端中使用 Protobuf 消息

MQTTX 的桌面客户端为用户带来了更加高效和个性化的体验。在最新版本中，我们对脚本部分进行了优化，特别是新增的自定义函数和编解码脚本功能。这些新特性使得处理和查看 Protobuf 格式的数据更为轻松。

1. **进入编解码脚本页面**

   启动 MQTTX 客户端，点击左侧菜单栏中的“脚本”图标，再选择“编解码”选项卡，进入到该页面后有一个简单的默认示例。

   ![编解码脚本页面](https://assets.emqx.com/images/98151be6114cc8620508b59f55296325.png)

   > **注意：**该示例仅为内容示例，需要保存后才能使用。

2. **输入或导入 proto 文件**

   您可以在编辑框中输入 proto 格式文件的内容，如下所示，然后点击右上角的“保存”按钮。这样您就成功在 MQTTX 中创建了一个新的 proto 格式的编解码文件。如果您已经有预备好的 proto 文件，可以直接点击右上角的“导入 .proto 文件”按钮进行上传。

   这里我们简单准备了一个在物联网领域比较常见的 proto 格式的编解码内容：

   ```protobuf
   syntax = “proto3”;
   
   package IoT;
   
   message SensorData {
     string deviceId = 1;
     string sensorType = 2;
     double value = 3;
     int64 timestamp = 4;
   }
   ```

   这个 proto 文件定义了一个 `SensorData` 消息，其中包括设备ID、传感器类型、传感器值和时间戳。

   ![编辑脚本](https://assets.emqx.com/images/f75b52e97682e30955b7802559fb96c7.png)

3. **测试输入输出**

   在脚本编辑器的底部，您可以尝试输入数据来验证您刚才编写的 proto 文件内容是否正确。首先，请选择一个您希望进行测试的数据格式，例如 JSON。

   **例**：根据之前的 `SensorData` 的定义，您可以输入以下的 JSON 数据和刚才的 Proto 名称来进行测试：

   ```json
   {
     "deviceId": "123456789",
     "sensorType": "Temperature",
     "value": 24.5,
     "timestamp": 1678339200000
   }
   ```

   输入完成后点击“测试”按钮。如果 proto 文件的定义有误，或者您输入的数据不符合 proto 文件的定义，MQTTX 客户端会显示相应的错误消息或提示，从而帮助您快速定位问题并进行调试。

   当您确认输入数据与 proto 文件匹配，并且没有任何错误提示时，说明您的 proto 文件设置正确，可以继续后续的操作。

   ![测试输入输出](https://assets.emqx.com/images/b5e8037de4d6b44be4d42976d3892856.png)

4. **运行脚本**

   在成功连接到 EMQX 后，您可以进一步使用您之前定义的 proto 文件来进行消息的编解码。

   - **选择运行脚本**：在连接页面的右上角，点击下拉菜单并选择“运行脚本”。

     ![选择运行脚本](https://assets.emqx.com/images/703bbc7abc945f0d4836860bf631d665.png)

   - **应用于消息的发送或接收**：在弹出的界面中，您可以选择该编解码是否应用于消息发送、接收或全部。根据您的实际场景来选择。本例中，我们选择默认的“全部”。

   - **选择编解码脚本并设置类型名称**：在编解码下拉选择框中，选择您刚才创建或导入的 proto 文件。在“类型名称（即 Proto Name）”输入框中，输入您在 proto 文件中定义的消息名称，如 `IoT.SensorData`。确保所有设置都已正确配置后，点击“确认”按钮。

     ![选择编解码脚本并设置类型名称](https://assets.emqx.com/images/11699524380f3becd7fd9882866680ee.png)

     **注意**：在这个教程中，我们将只关注编解码脚本的使用。尽管 MQTTX 客户端支持使用自定义函数，但在本教程中我们不会涉及这部分功能。

5. **消息的收发**

   在完成了上述配置后，我们已经为 MQTTX 客户端配置了 Protobuf 编解码的功能。现在，我们将通过实际的消息收发来验证其效果。

   - **发布消息**：在消息输入框中，填入您预期的 JSON 数据，例如：

     ```json
     {
       "deviceId": "Device001",
       "sensorType": "Temperature",
       "value": 23.5,
       "timestamp": 1677328490320
     }
     ```

     然后，订阅一个名为 `testtopic/protobuf` 的主题，并向该主题发送上述消息。

   - **接收并查看消息**：确保您已经订阅了上述主题。当消息到达时，您可以在接收窗口中看到 Protobuf 消息。选择 JSON 类型，将 Protobuf 消息转换为 JSON 格式进行查看。

     ![接收并查看消息](https://assets.emqx.com/images/52058b41c62abe768bc10b7cfa355330.png)

   - **验证消息处理**：在每条消息的顶部，有一个标签指示该消息是否经过了编解码处理。确保它显示为“已使用 xx 编解码”或类似的标识。如有任何错误或消息格式不符合预期的 proto 格式，MQTTX 客户端都会显示相应的错误提示。

在完成上述步骤后，您已经在 MQTTX 客户端成功地启用了 Protobuf 的编解码功能，确保您通过 MQTT 发送或接收的消息都会按照 Protobuf 格式进行正确的序列化或反序列化。如需终止此功能，请点击顶部的“停止脚本”按钮。

## 在 MQTTX 命令行中使用 Protobuf 消息

除了在 MQTTX 图形桌面客户端中利用 Protobuf 进行消息编解码，MQTTX 的命令行版本同样提供了完善的支持。对于熟悉控制台操作的用户，命令行版本提供了更直接且高效的操作方式。

**使用 Protobuf 的命令行参数介绍**

在使用 MQTTX 命令行客户端处理 Protobuf 格式的消息时，您需要了解以下重要参数：

| 参数 | 描述                                                         |
| :--- | :----------------------------------------------------------- |
| Pp   | 指定 Protobuf 消息格式的 .proto 文件路径。                   |
| Pmn  | 定义 Protobuf 消息的类型名称。此名称必须与您的 .proto 文件中的定义相符。 |

1. **准备** `.proto` 文件

   首先，确保您已有一个定义好的 `.proto` 文件，描述您希望传输的 Protobuf 消息格式。

   ```protobuf
   syntax = "proto3";
   
   package IoT;
   
   message SensorData {
    string deviceId = 1;
    string sensorType = 2;
    double value = 3;
    int64 timestamp = 4;
   }
   
   ```

2. **使用命令进行消息订阅**

   为了接收 Protobuf 格式的消息，您可以订阅一个特定的 MQTT 主题：

   ```shell
   mqttx sub -t 'testtopic/protobuf' -h 127.0.0.1 -Pp ./SensorData.proto -Pmn IoT.SensorData
   ```

3. **使用命令进行消息发布**

   根据前面的参数介绍，现在我们可以发布一个 Protobuf 格式的消息：

   ```shell
   mqttx pub -t 'testtopic/protobuf' -Pp ./SensorData.proto -Pmn IoT.SensorData -h 127.0.0.1 -m '{"deviceId":"123456", "sensorType": "Temperature", "value": 22.5, "timestamp": 1675873900}'
   ```

4. **查看接收到的 Protobuf 消息**

   在成功订阅后，您将能在命令行中观察到从 `testtopic/protobuf` 主题所接收的 Protobuf 格式消息。此消息会根据您的 `.proto` 文件定义进行解码后在命令行中显示，以便于您进行查看。

   ![查看接收到的 Protobuf 消息](https://assets.emqx.com/images/31a58ffd73dfa4d87ef98407b0091e2d.png)

如果您希望查看的消息格式为 JSON，可以使用 `--format` 参数并将其设置为 `json`。这将会把 Protobuf 消息转换为易于查看的 JSON 格式。

## 使用 EMQX 验证 Protobuf 消息

最后，为确保您的消息的正确性，我们推荐使用 EMQX 5.1.1 企业版的编解码功能进行验证，通过解码和编码两个部分验证消息的正确性。

### 解码场景

设备发布使用 Protobuf 编码的消息至 MQTT 服务器。EMQX 规则引擎将捕获并根据定义的 Protobuf Schema 解码此消息，然后重发布到指定主题。

1. **创建 Protobuf Schema**:

   - 在 EMQX Dashboard 左侧导航栏中，选择`数据集成 -> 编解码`。

   - 使用以下参数创建一个 Protobuf Schema:

     - 名称: `protobuf_sensor`

     - 类型: `protobuf`

     - Schema:

       ```protobuf
       syntax = "proto3";
       package IoT;
       message SensorData {
          string deviceId = 1;
          string sensorType = 2;
          double value = 3;
          int64 timestamp = 4;
       }
       ```

   - 点击`创建`。

2. **创建解码规则**:

   - 在左侧导航栏选择`数据集成 -> 规则`。

   - 在 SQL 编辑器中，写入:

     ```sql
     SELECT
       schema_decode('protobuf_sensor', payload, 'SensorData') as sensor_data, payload
     FROM
       "t/#"
     WHERE
       sensor_data.deviceId = 'Device123'
     ```

   - 在动作下拉框中选择`消息重发布`。

   - 目标主题为`sensor_data/${sensor_data.deviceId}`。

   - Payload 使用消息内容模板`${sensor_data}`。

     ![查看规则](https://assets.emqx.com/images/6d6dec6bb7590c50b6c09725d6894ca8.png)

3. **使用 MQTTX**:

   - 使用 MQTTX 作为 MQTT 客户端连接到 EMQX。

   - 在订阅区域，订阅主题 `sensor_data/#`。

   - 将编解码脚本设置到发布端，并发送一个 Protobuf 编码的 `SensorData` 消息到 `t/1` 主题。

   - 在接收的 MQTTX 中，您应该可以看到主题为 `sensor_data/Device123` 的解码后的消息。

     ![查看解码后的消息](https://assets.emqx.com/images/c3d0fc2a4764a91de42681944fd2faa7.png)

### 编码场景

设备将 JSON 格式的消息发布到 MQTT 服务器。EMQX 规则引擎根据定义的 Protobuf Schema 将其编码为 Protobuf 格式，并重新发布到另一个主题。

1. **使用之前创建的 Schema**。

2. **创建编码规则**:

   - 同样在左侧导航栏选择`数据集成 -> 规则`。

   - 在 SQL 编辑器中，写入:

     ```sql
     SELECT
       schema_encode('protobuf_sensor', json_decode(payload), 'SensorData') as protobuf_sensor
     FROM
       "t/#"
     ```

   - 在动作下拉框中选择`消息重发布`。

   - 目标主题为 `protobuf_out`。

   - Payload 使用消息内容模板 `${protobuf_sensor}`。

     ![查看规则](https://assets.emqx.com/images/f876c8ee46f3ebe6b27cfcd355b62c2c.png)

3. **使用 MQTTX 接收 Protobuf 消息**:

   - 使用 MQTTX 连接到 EMQX。

   - 在发布区域，输入主题 `t/1` 和指定的 JSON Payload，例如：

     ```json
     {
       "deviceId": "Device123",
       "sensorType": "Temperature",
       "value": 24.5,
       "timestamp": 1678339200000
     }
     ```

   - 将编解码脚本设置到接收端，并订阅一个 `protobuf_out` 主题。

   - 点击发布。

   - 在 MQTTX 中，您应该看到编码后的 Protobuf 消息。

     ![编码后的 Protobuf 消息](https://assets.emqx.com/images/b16c4394d3afc5f467170cf5112bfbcc.png)

## 总结

随着物联网行业的飞速发展，高效和紧凑的数据传输变得尤为重要。Protobuf 作为一种高效的数据序列化格式，可以与 MQTT 配合使用，确保迅速、精确和安全的数据交互。

特别是在工业物联网领域，广受欢迎的数据传输标准 SparkplugB 就是采用了以 Protobuf 为核心的消息格式。因此，MQTTX 也可以轻松地通过 Protobuf 支持 SparkplugB 消息交互。为了进一步加强工业应用的表现，MQTTX 计划在未来进一步优化对 SparkplugB 的支持。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
