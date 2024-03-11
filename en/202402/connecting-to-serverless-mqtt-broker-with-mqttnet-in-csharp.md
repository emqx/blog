## Introduction

With the rise of IoT, the .Net framework has become increasingly popular in building IoT applications. Microsoft's .Net Core and .Net Framework provide developers with a set of tools and libraries to build IoT applications that can run on Raspberry Pi, HummingBoard, BeagleBoard, Pine A64, and more.

MQTTnet is a high-performance .Net library that implements the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt). It is open source on [GitHub](https://github.com/dotnet/MQTTnet) and has a rich set of features, including MQTT 5.0 protocol and TLS/SSL supports.

This blog post demonstrates how to use the MQTTnet library to connect to a serverless MQTT broker. The whole project can be downloaded at [MQTT Client Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Csharp-MqttNet).

## Prepare an MQTT Broker

[EMQX Serverless](https://www.emqx.com/en/cloud/serverless-mqtt) is an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) offering on the public cloud with all the serverless advantages. You can start the Serverless deployment in seconds with just a few clicks. Additionally, users can get 1 million free session minutes every month, sufficient for 23 devices to be online for a whole month, making it perfect for tiny IoT test scenarios.

You can follow [the guide in this blog](https://www.emqx.com/en/blog/a-comprehensive-guide-to-serverless-mqtt-service) to create a serverless deployment for free. Once you have completed the registration process with the online guide, you will get a running instance with the following similar information from the “Overview” in your deployment. We will use the connection information and CA certificate later.

![EMQX MQTT Cloud](https://assets.emqx.com/images/b7f54f0922422779d30df5ede63e66fb.png)

## MQTT C# Demo

### 1. Install .Net and Visual Studio

If you haven't installed the .NET environment on your computer yet, you can visit the [official Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/core/install/) for detailed instructions.

Visual Studio is a comprehensive IDE for .NET developers that provides a feature-rich environment for developing, debugging, and deploying .NET applications. You can download and install it [here](https://visualstudio.microsoft.com/downloads/), based on your computer's system and version.

### 2. Install the MQTTnet package

MQTTnet is delivered via NuGet package manager. To install it, create a Console Application and use NuGet to install the MQTTnet package. For detailed instructions on using NuGet in Visual Studio, refer to the [official documentation](https://learn.microsoft.com/en-us/nuget/consume-packages/install-use-packages-visual-studio). If you're using Visual Studio for Mac, refer to [install and manage NuGet packages in Visual Studio for Mac](https://learn.microsoft.com/en-us/visualstudio/mac/nuget-walkthrough?toc=/nuget/toc.json).

### 3. Set up the MQTT connection

To connect to the EMQX Serverless broker, you need to create an instance of the `MqttClientOptionsBuilder` class and set the necessary options like broker address, port, username, and password. The code snippet below demonstrates how to create an instance of the `MqttClientOptionsBuilder`:

```c#
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

Please replace the connection parameters with your EMQX connection information and login credentials.

- Broker and port: Obtain the connection address and port information from the server deployment overview page.
- Topic: Topics are used to identify and differentiate between different messages, forming the basis of MQTT message routing.
- Client ID: Every MQTT client must have a unique client ID. You can use `Guid.NewGuid()` to generate a new unique identifier in .NET.
- Username and password: To establish a client connection, please make sure that you provide the correct username and password. The following image shows how to configure these credentials under 'Authentication & ACL - Authentication' on the server side.

![Authentication & ACL](https://assets.emqx.com/images/d8f21d98e7330420f48323bada622839.png)

### 4. Using TLS/SSL

When connecting to EMQX Serverless, it is important to note that it relies on a multi-tenant architecture, which enables multiple users to share a single EMQX cluster. In order to ensure the security and reliability of data transmission within this multi-tenant environment, TLS is required. And if the server is utilizing a self-signed certificate, you must download the corresponding CA file from the deployment overview panel and provide it during the connection setup process.

To add TLS and set the certificate file to the `MqttClientOptionsBuilder` instance, you can use `WithTls()`. The following code snippet shows how to create a TLS instance of `MqttClientOptionsBuilder`:

```c#
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

### 5. Connect to the MQTT broker

Now that you have created the [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) and set up the connection options, you are ready to connect to the broker. Simply use the `PublishAsync` method of the MQTT client to establish a connection and start sending and receiving messages. 

```c#
var connectResult = await mqttClient.ConnectAsync(options);
```

Here we use asynchronous programming, which allows message publishing while subscribing to prevent blocking.

### 6. Subscribe to topics

Once connected to the broker, you can verify the success of the connection by checking the value of `ResultCode`. If the connection is successful, you can subscribe to [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) to receive messages.

```c#
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

Within this function, you can also print the the corresponding received messages. This allows you to view and process the received data as needed.

### 7. Publish messages

To send messages to the broker, use the `PublishAsync` method of the MQTT client. Here is an example for sending messages to the broker in a loop, with one message sent every second:

```c#
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

### 8. Unsubscribe

To unsubscribe, call:

```c#
await mqttClient.UnsubscribeAsync(topic);
```

### 9. Disconnect

To disconnect, call:

```c#
await mqttClient.DisconnectAsync();
```

## Complete Code

The following code shows how to connect to the server, subscribe to topics, and publish and receive messages. For a complete demonstration of all functions, see the project's [GitHub repository](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Csharp-MqttNet).

```c#
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

## Test

Run the project in Visual Studio, we can see the output information on the terminal window as follows. The client has successfully connected to the MQTT broker, and received a message every second.

![Run the project in Visual Studio](https://assets.emqx.com/images/531eee4b26982772feee05e14fc57e23.png)

You can also use [MQTT Client Tool - MQTTX](https://mqttx.app/) as another client for the message publishing and receiving the test. If you subscribe the “`Csharp/mqtt`" topic in MQTTX, you will receive the message every second.

![MQTTX](https://assets.emqx.com/images/49c1df9fd56d1a1301b6075ac34f3dda.png)

When you publish a message to the topic, the server will receive the message and you can view it both on MQTTX and in the console.

![Received message displayed on MQTTX](https://assets.emqx.com/images/d803214cd47bc6656b1da92f4540827b.png)

<center>Received message displayed on MQTTX</center>

![Received message displayed on terminal](https://assets.emqx.com/images/23b4c6370911dfe7d91b5f2339b46333.png)

<center>Received message displayed on terminal</center>

## Summary

This blog provides a step-by-step guide on connecting to a serverless MQTT deployment via the MQTTnet library. By following these instructions, you have successfully created a .Net application capable of publishing and subscribing to Serverless MQTT. 



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
