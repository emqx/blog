云计算中的无服务器 (Serverless) 架构可让开发人员专注于代码开发和部署，而无需进行繁琐的基础设施管理。EMQ 的云服务中包含了一款 Serverless MQTT 消息服务器产品，它可根据需求自动扩展，减少额外的人工干预。

要了解有关无服务器 MQTT 的更多信息，请阅读我们的博文《[EMQX Cloud Serverless：下一代 MQTT 云服务](https://www.emqx.com/zh/blog/next-gen-cloud-mqtt-service-meet-emqx-cloud-serverless)》。在本系列博客中，我们将指导您使用常见的客户端库，通过 EMQ Serverless MQTT 消息服务器建立 MQTT 连接、订阅、消息传递等。

## 背景介绍

随着物联网的兴起，.Net 框架在构建物联网应用程序方面变得越来越流行。微软的 .Net Core 和 .Net 框架为开发人员提供了一组工具和库，以构建可以在 Raspberry Pi、HummingBoard、BeagleBoard、Pine A64 等平台上运行的物联网应用程序。

MQTTnet 是一个实现 MQTT 协议的高性能 .Net 库，在 [GitHub](https://github.com/dotnet/MQTTnet) 上开源，具有丰富的功能，支持 MQTT 5.0 协议和 TLS/SSL。

这篇博文演示了如何使用 MQTTnet 库连接到 EMQX Serverless MQTT 消息服务器。相关代码可以在 [MQTT 客户端示例](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Csharp-MqttNet) 中下载。

## 免费的 Serverless MQTT 消息服务器

EMQX Serverless MQTT 消息服务器是公有云上最新的 MQTT 消息服务器产品，具有所有 Serverless 的优势。只需点击几下，您就可以在几秒钟内开始无服务器部署。此外，用户每月可以获得 100 万的免费会话分钟，足以让 23 台设备在线整整一个月，非常适合小型物联网测试场景。

如果您还没有尝试过无服务器部署，请按照[本博客中的指南](https://www.emqx.com/en/blog/a-comprehensive-guide-to-serverless-mqtt-service)免费创建一个。一旦您使用在线指南完成注册过程，您将从部署中的 Overview 页面获得一个具有类似以下所示的运行实例。我们稍后将使用连接信息和 CA证书。

![EMQX MQTT Cloud](https://assets.emqx.com/images/b7f54f0922422779d30df5ede63e66fb.png)

## 代码演示

### 1. 安装 .NET 和 Visual Studio

如果您尚未在计算机上安装 .NET 环境，可以访问 [Microsoft 官方文档](https://learn.microsoft.com/zh-cn/dotnet/core/install/)以获详细说明。

Visual Studio 是面向 .NET 开发人员的综合 IDE，为开发、调试和部署 .NET 应用程序提供功能丰富的开发环境。您可以根据计算机的系统和版本[在此处](https://visualstudio.microsoft.com/downloads/)下载 .Net 安装介质。

### 2. 安装 MQTTnet 包

MQTTnet 通过 NuGet 包管理器交付。要安装它，请创建控制台应用程序并使用 NuGet 安装 MQTTnet 包。有关在 Visual Studio 中使用 NuGet 的详细说明，请参阅[官方文档](https://learn.microsoft.com/zh-cn/nuget/consume-packages/install-use-packages-visual-studio)。如果您使用的是 Visual Studio for Mac，请参阅[在 Visual Studio for Mac 中安装和管理 NuGet 包](https://learn.microsoft.com/zh-cn/visualstudio/mac/nuget-walkthrough?view=vsmac-2022&toc=%2Fnuget%2Ftoc.json)。

### 3. 设置连接

要连接到 EMQX Cloud Serverless 服务，您需要创建 `MqttClientOptionsBuilder` 类的实例，并设置必要的选项，如代理地址、端口、用户名和密码。下面的代码片段演示了如何创建 `MqttClientOptionsBuilder` 的实例：

```
        string broker = "******.emqxsl.com";
        int port = 8883;
        string clientId = Guid.NewGuid().ToString();
        string topic = "Csharp/mqtt";
        string username = "emqxtest";
        string password = "******";

        // Create a MQTT client factory
        var factory = new MqttFactory();

        // Create a MQTT client instance
        var mqttClient = factory.CreateMqttClient();

        // Create MQTT client options
        var options = new MqttClientOptionsBuilder()
            .WithTcpServer(broker, port) // MQTT broker address and port
            .WithCredentials(username, password) // Set username and password
            .WithClientId(clientId)
            .WithCleanSession()
            .Build();
```

请将连接参数替换为您的 EMQX 连接信息和登录凭据。

- 代理和端口：从服务器部署概览页面获取连接地址和端口信息。
- 主题：主题用于识别和区分不同的消息，构成 MQTT 消息路由的基础。
- 客户端 ID：每个 MQTT 客户端都必须有一个唯一的客户端 ID。您可以使用 `Guid. NewGuid()` 在 .NET 中生成一个新的唯一标识符。
- 用户名和密码：要建立客户端连接，请确保提供正确的用户名和密码。下图显示了如何在服务器端的“身份验证和 ACL-身份验证”下配置这些凭据。

![Authentication & ACL](https://assets.emqx.com/images/d8f21d98e7330420f48323bada622839.png)

### 4. 使用 TLS/SSL

连接到 EMQX Serverless 时，需要注意的是，它依赖于多租户架构，该架构使多个用户能够共享单个 EMQX 集群，为了保证这种多租户环境内数据传输的安全性和可靠性，需要 TLS，并且如果服务器使用的是自签名证书，则必须从部署概览面板下载相应的 CA 文件，并在连接建立过程中提供。

要添加 TLS 并将证书文件设置为 `MqttClientOptionsBuilder` 实例，可以使用 `WithTls()`。以下代码片段显示了如何创建 `MqttClientOptionsBuilder` 的 TLS 实例：

```
        string broker = "******.emqxsl.com";
        int port = 8883;
        string clientId = Guid.NewGuid().ToString();
        string topic = "Csharp/mqtt";
        string username = "emqxtest";
        string password = "******";

        // Create a MQTT client factory
        var factory = new MqttFactory();

        // Create a MQTT client instance
        var mqttClient = factory.CreateMqttClient();

        // Create MQTT client options
        var options = new MqttClientOptionsBuilder()
            .WithTcpServer(broker, port) // MQTT broker address and port
            .WithCredentials(username, password) // Set username and password
            .WithClientId(clientId)
            .WithCleanSession()
            .WithTls(
                o =>
                {
                    // The used public broker sometimes has invalid certificates. This sample accepts all
                    // certificates. This should not be used in live environments.
                    o.CertificateValidationHandler = _ => true;

                    // The default value is determined by the OS. Set manually to force version.
                    o.SslProtocol = SslProtocols.Tls12; ;

                    // Please provide the file path of your certificate file. The current directory is /bin.
                    var certificate = new X509Certificate("/opt/emqxsl-ca.crt", "");
                    o.Certificates = new List<X509Certificate> { certificate };
                }
            )
            .Build();
```

### 5. 连接到 MQTT 消息服务器

现在您已经创建了 MQTT 客户端并设置了连接选项，您可以连接到 EMQX Cloud Serverless 消息服务了。只需使用 MQTT 客户端的 `PublishAsync` 方法建立连接并开始发送和接收消息。

```
var connectResult = await mqttClient.ConnectAsync(options);
```

这里我们使用异步编程，在订阅的同时允许消息发布，防止阻塞。

### 6. 订阅话题

连接到代理后，可以通过检查 `ResultCode` 的值来验证连接是否成功。如果连接成功，可以订阅主题来接收消息。

```
if (connectResult.ResultCode == MqttClientConnectResultCode.Success)
        {
            Console.WriteLine("Connected to MQTT broker successfully.");

            // Subscribe to a topic
            await mqttClient.SubscribeAsync(topic);

            // Callback function when a message is received
            mqttClient.ApplicationMessageReceivedAsync += e =>
            {
                Console.WriteLine($"Received message: {Encoding.UTF8.GetString(e.ApplicationMessage.PayloadSegment)}");
                return Task.CompletedTask;
            };
```

在此功能中，您还可以打印相应的接收到的消息。这使您可以根据需要查看和处理接收到的数据。

### 7. 发布消息

要向 EMQX Cloud Serverless 消息服务发送消息，请使用 MQTT 客户端的 `PublishAsync` 方法。以下是循环向消息服务发送消息的示例，每秒发送一条消息：

```
for (int i = 0; i < 10; i++)
            {
                var message = new MqttApplicationMessageBuilder()
                    .WithTopic(topic)
                    .WithPayload($"Hello, MQTT! Message number {i}")
                    .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
                    .WithRetainFlag()
                    .Build();

                await mqttClient.PublishAsync(message);
                await Task.Delay(1000); // Wait for 1 second
            }
```

### 8. 取消订阅

要取消对消息主题的订阅，请调用：

```
await mqttClient.UnsubscribeAsync(topic);
```

### 9. 断开连接

要断开连接，请调用：

```
await mqttClient.DisconnectAsync();
```

## 完整代码

下面的代码展示了如何连接到服务器、订阅主题以及发布和接收消息。有关所有功能的完整演示，请参阅项目的 [GitHub 代码库](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Csharp-MqttNet)。

```
using System.Security.Authentication;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Protocol;

class Program
{
    static async Task Main(string[] args)
    {
        string broker = '******.emqxsl.com';
        int port = 8883;
        string clientId = Guid.NewGuid().ToString();
        string topic = "Csharp/mqtt";
        string username = 'emqxtest';
        string password = '**********';

        // Create a MQTT client factory
        var factory = new MqttFactory();

        // Create a MQTT client instance
        var mqttClient = factory.CreateMqttClient();

        // Create MQTT client options
        var options = new MqttClientOptionsBuilder()
            .WithTcpServer(broker, port) // MQTT broker address and port
            .WithCredentials(username, password) // Set username and password
            .WithClientId(clientId)
            .WithCleanSession()
            .WithTls(
                o =>
                {
                    // The used public broker sometimes has invalid certificates. This sample accepts all
                    // certificates. This should not be used in live environments.
                    o.CertificateValidationHandler = _ => true;

                    // The default value is determined by the OS. Set manually to force version.
                    o.SslProtocol = SslProtocols.Tls12; 

                    // Please provide the file path of your certificate file. The current directory is /bin.
                    var certificate = new X509Certificate("/opt/emqxsl-ca.crt", "");
                    o.Certificates = new List<X509Certificate> { certificate };
                }
            )
            .Build();

        // Connect to MQTT broker
        var connectResult = await mqttClient.ConnectAsync(options);

        if (connectResult.ResultCode == MqttClientConnectResultCode.Success)
        {
            Console.WriteLine("Connected to MQTT broker successfully.");

            // Subscribe to a topic
            await mqttClient.SubscribeAsync(topic);

            // Callback function when a message is received
            mqttClient.ApplicationMessageReceivedAsync += e =>
            {
                Console.WriteLine($"Received message: {Encoding.UTF8.GetString(e.ApplicationMessage.PayloadSegment)}");
                return Task.CompletedTask;
            };

            // Publish a message 10 times
            for (int i = 0; i < 10; i++)
            {
                var message = new MqttApplicationMessageBuilder()
                    .WithTopic(topic)
                    .WithPayload($"Hello, MQTT! Message number {i}")
                    .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
                    .WithRetainFlag()
                    .Build();

                await mqttClient.PublishAsync(message);
                await Task.Delay(1000); // Wait for 1 second
            }

            // Unsubscribe and disconnect
            await mqttClient.UnsubscribeAsync(topic);
            await mqttClient.DisconnectAsync();
        }
        else
        {
            Console.WriteLine($"Failed to connect to MQTT broker: {connectResult.ResultCode}");
        }
    }
}

```

## 测试

在 Visual Studio 中运行项目，我们可以在终端窗口上看到输出信息如下。客户端已成功连接到 EMQX Cloud Serverless 消息服务，每秒收到一条消息。

![Run the project in Visual Studio](https://assets.emqx.com/images/531eee4b26982772feee05e14fc57e23.png)

您还可以使用 [MQTT 客户端工具-MQTTX](https://mqttx.app/zh) 作为消息发布和接收测试的另一个客户端。如果您在 MQTTX 中订阅了`"CSharp/mqtt"`主题，您将每秒收到消息。

![MQTTX](https://assets.emqx.com/images/49c1df9fd56d1a1301b6075ac34f3dda.png)

当您将消息发布到主题时，服务器将收到该消息，您可以在 MQTTX 和控制台上查看消息输出。

![Received message displayed on MQTTX](https://assets.emqx.com/images/d803214cd47bc6656b1da92f4540827b.png)

MQTTX 上显示收到的消息

![Received message displayed on terminal](https://assets.emqx.com/images/23b4c6370911dfe7d91b5f2339b46333.png)

终端上显示收到的消息

## 总结

本博客提供了通过 MQTTnet 库连接到 EMQX Cloud Serverless 消息服务的教程。按照这些说明，您已经成功创建了一个 .NET 应用程序，能够发布和订阅 EMQX Cloud Serverless 消息服务。

## 加入 EMQ 社区

要深入了解这个主题，请探索我们的 [GitHub 代码库](https://github.com/emqx/emqx)以获取源代码，加入我们的微信群进行讨论，并观看我们的 [B 站视频](https://space.bilibili.com/522222081)进行实践学习。我们重视您的反馈和贡献，所以请随时参与并成为我们蓬勃发展的社区的一部分。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient px-5">联系我们 →</a>
</section>
