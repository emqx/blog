## Introduction

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight [IoT messaging](https://www.emqx.com/en/solutions/reliable-mqtt-messaging) protocol based on the publish/subscribe model. It can provide real-time and reliable messaging services for networked devices with very little code and bandwidth. It is widely used in the industries such as the IoT, mobile Internet, smart hardware, [Internet of Vehicles](https://www.emqx.com/en/use-cases/internet-of-vehicles), and power energy.

Go is a cross-platform, open source programming language. It can be used to create high-performance applications. By combining Golang with MQTT, developers can build scalable and secure IoT applications to communicate with devices in real-time, exchange information, and perform complex data analytics.

This article provides a comprehensive guide on using MQTT in a Golang project for seamless communication between the client and an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison). You will learn how to establish a connection, subscribe and unsubscribe to topics, publish messages, and receive messages in real-time. This guide will equip you with the skills to leverage MQTT to build scalable and efficient IoT applications.

## Golang MQTT Project Preparation

### Confirm Golang Version

This project uses go **v1.21.1** for development and testing. To confirm that the correct version of Golang is installed, readers can use the following command:

```shell
$ go version
go version go1.21.1 darwin/amd64
```

### Install Golang MQTT Client

This project uses [paho.mqtt.golang](https://github.com/eclipse/paho.mqtt.golang) as [MQTT client library](https://www.emqx.com/en/mqtt-client-sdk), install:

```shell
go get github.com/eclipse/paho.mqtt.golang
```

## Prepare an MQTT Broker

Before proceeding, please ensure you have an MQTT broker to communicate and test with. We recommend you use EMQX Cloud.

[EMQX Cloud](https://www.emqx.com/en/cloud) is a fully managed cloud-native MQTT service that can connect to a large number of IoT devices and integrate various databases and business systems. With EMQX Cloud, you can get started in just a few minutes and run your MQTT service in 20+ regions across AWS, Google Cloud, and Microsoft Azure, ensuring global availability and fast connectivity.

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>

This article will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) to simplify the process:

- Server: `broker.emqx.io`
- TCP Port: `1883`
- WebSocket Port: `8083`
- SSL/TLS Port: `8883`
- Secure WebSocket Port: `8084`

## Golang MQTT Usage

### Create an MQTT Connection

#### TCP Connection

To establish the MQTT connection, it is necessary to set the connection address, port, and client ID.

```go
package main

import (
    "fmt"
    mqtt "github.com/eclipse/paho.mqtt.golang"
    "time"
)

var messagePubHandler mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
    fmt.Printf("Received message: %s from topic: %s\n", msg.Payload(), msg.Topic())
}

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
    fmt.Println("Connected")
}

var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
    fmt.Printf("Connect lost: %v", err)
}

func main() {
    var broker = "broker.emqx.io"
    var port = 1883
    opts := mqtt.NewClientOptions()
    opts.AddBroker(fmt.Sprintf("tcp://%s:%d", broker, port))
    opts.SetClientID("go_mqtt_client")
    opts.SetUsername("emqx")
    opts.SetPassword("public")
    opts.SetDefaultPublishHandler(messagePubHandler)
    opts.OnConnect = connectHandler
    opts.OnConnectionLost = connectLostHandler
    client := mqtt.NewClient(opts)
    if token := client.Connect(); token.Wait() && token.Error() != nil {
        panic(token.Error())
  }
}
```

- ClientOptions: used to set broker, port, client id, username, password and other options.
- messagePubHandler: global MQTT pub message processing
- connectHandler: callback for the connection
- connectLostHandler: callback for connection loss

#### TLS/SSL

Using [TLS in MQTT](https://www.emqx.com/en/blog/fortifying-mqtt-communication-security-with-ssl-tls) can ensure the confidentiality and integrity of information, preventing information leakage and tampering. TLS authentication can be classified into one-way authentication and two-way authentication.

If you want to use the TSL connection, you can use the following settings:

```go
func NewTlsConfig() *tls.Config {
    certpool := x509.NewCertPool()
    ca, err := ioutil.ReadFile("ca.pem")
    if err != nil {
        log.Fatalln(err.Error())
    }
    certpool.AppendCertsFromPEM(ca)
    // Import client certificate/key pair
    clientKeyPair, err := tls.LoadX509KeyPair("client-crt.pem", "client-key.pem")
    if err != nil {
        panic(err)
    }
    return &tls.Config{
        RootCAs: certpool,
        ClientAuth: tls.NoClientCert,
        ClientCAs: nil,
        InsecureSkipVerify: true,
        Certificates: []tls.Certificate{clientKeyPair},
    }
}
```

If the client certificate is not set, it can be set as follows:

```go
func NewTlsConfig() *tls.Config {
    certpool := x509.NewCertPool()
    ca, err := ioutil.ReadFile("ca.pem")
    if err != nil {
        log.Fatalln(err.Error())
    }
    certpool.AppendCertsFromPEM(ca)
    return &tls.Config{
        RootCAs: certpool,
        }
}
```

Then set TLS:

```go
var broker = "broker.emqx.io"
var port = 8883
opts := mqtt.NewClientOptions()
opts.AddBroker(fmt.Sprintf("ssl://%s:%d", broker, port))
tlsConfig := NewTlsConfig()
opts.SetTLSConfig(tlsConfig)
// other options
```

### Subscribe to an MQTT Topic

We use following code to subscribe the topic from MQTT Broker:

```go
func sub(client mqtt.Client) {
    topic := "topic/test"
    token := client.Subscribe(topic, 1, nil)
    token.Wait()
    fmt.Printf("Subscribed to topic %s", topic)
}
```

### Publish MQTT Messages

After completing the above topic subscription and message monitoring, we will write a function for publishing messages.

```go
func publish(client mqtt.Client) {
    num := 10
    for i := 0; i < num; i++ {
        text := fmt.Sprintf("Message %d", i)
        token := client.Publish("topic/test", 0, false, text)
        token.Wait()
        time.Sleep(time.Second)
    }
}
```

### Test

We use the following code for testing.

```go
package main

import (
    "fmt"
    mqtt "github.com/eclipse/paho.mqtt.golang"
    "log"
    "time"
)

var messagePubHandler mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
    fmt.Printf("Received message: %s from topic: %s\n", msg.Payload(), msg.Topic())
}

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
    fmt.Println("Connected")
}

var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
    fmt.Printf("Connect lost: %v", err)
}

func main() {
    var broker = "broker.emqx.io"
    var port = 1883
    opts := mqtt.NewClientOptions()
    opts.AddBroker(fmt.Sprintf("tcp://%s:%d", broker, port))
    opts.SetClientID("go_mqtt_client")
    opts.SetUsername("emqx")
    opts.SetPassword("public")
    opts.SetDefaultPublishHandler(messagePubHandler)
    opts.OnConnect = connectHandler
    opts.OnConnectionLost = connectLostHandler
    client := mqtt.NewClient(opts)
    if token := client.Connect(); token.Wait() && token.Error() != nil {
        panic(token.Error())
    }

    sub(client)
    publish(client)

    client.Disconnect(250)
}

func publish(client mqtt.Client) {
    num := 10
    for i := 0; i < num; i++ {
        text := fmt.Sprintf("Message %d", i)
        token := client.Publish("topic/test", 0, false, text)
        token.Wait()
        time.Sleep(time.Second)
    }
}

func sub(client mqtt.Client) {
    topic := "topic/test"
    token := client.Subscribe(topic, 1, nil)
    token.Wait()
  fmt.Printf("Subscribed to topic: %s", topic)
}
```

After running the code, we can see that the MQTT connection and subscription are successfully, and we can successfully receive the message of subscribing topic.

![Run code](https://assets.emqx.com/images/8882115bb9e0154ccfab16c26dd47566.png)

## Q&A

### **What if the MQTT message sent is not in JSON format?**

If the MQTT message is not JSON, you can still convert it to a string using the `toString()` method. However, if the content was not originally a string (for example, if it's binary data), you might need to handle it differently depending on the nature of the data.

### **What if the connection broke during publishing or subscribing the message?**

The **paho.mqtt.golang** client provide the option to auto connect the broker during publishing or subscribing the message. And the auto reconnect ability is enabled by default.

### **Why MQTT Client connection broke when establish mutiple connections.**

Use different Client IDs when you establishing mutiple MQTT Connections. Client IDs are important for MQTT because they identify a connection to an MQTT broker. Moreover, they identify a specific device or client, and it can be useful in terms of traceability to set a client ID that clearly identifies a device’s connection to the broker. **MQTT brokers usually implement a mechanism that closes an old connection if a new connection request with the same client ID as the existing (old) connection is received and then accepts the new connection.**

## Summary

So far, we have completed using the **paho.mqtt.golang** client to connect to the [public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) and have implemented the connection, message publishing and subscription between the test client and the MQTT broker.

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.

## Resources

- [A Quickstart Guide to Using MQTT over WebSocket](https://www.emqx.com/en/blog/connect-to-mqtt-broker-with-websocket)
- [MQTT on ESP32: A Beginner's Guide](https://www.emqx.com/en/blog/esp32-connects-to-the-free-public-mqtt-broker)
- [How to Use MQTT in Python with Paho Client](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)




<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
