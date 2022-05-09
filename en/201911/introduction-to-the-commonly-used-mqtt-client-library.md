## Overview

MQTT is a lightweight [publish-subscribe](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model) mode messaging protocol designed for IoT applications in low-bandwidth and unstable network environments. MQTT is based on the publish/subscribe paradigm and works on the TCP/IP protocol family. [MQTT protocol](https://www.emqx.com/en/mqtt) is lightweight, simple, open and easy to implement， which makes it suitable for a wide range of applications.

MQTT is based on the client-server communication mode. MQTT server is called as MQTT Broker. Currently, there are many MQTT Brokers in the industry, whose advantages and disadvantages and functional differences will not be discussed in this article. Taking the [most popular MQTT broker - EMQX](https://www.emqx.io/) in the open source community as an example, this article uses the public Broker `broker.emqx.io` provided by  [EMQ](https://www.emqx.com/en) , and uses a simple example of connecting Broker, publishing and processing messages by client to summarizes the usage and examples of [MQTT client libraries](https://www.emqx.com/en/mqtt-client-sdk) under different programming languages and platforms.

The selected MQTT client libraries are as follows:

- Eclipse Paho C and Eclipse Paho Embedded C
- Eclipse Paho Java Client
- Eclipse Paho MQTT Go client
- emqtt : Erlang mqtt client library provided by EMQ
- MQTT.js Web  & Node.js Platform MQTT Client
- Eclipse Paho Python


## Sample application introduction

The action of the MQTT client throughout its lifecycle can be summarized as: establishing a connection, subscribing to a topic, receiving and processing a message, publishing a message to a specified topic, unsubscribing, and disconnecting.

The standard client library shows the corresponding method in each link. The meaning of the method parameters required by different libraries in the same link is roughly the same. The specific parameters to be selected and the functional features to be enabled need the user to have a deep understanding of the MQTT  protocol features and to be determined in combination with the actual application scenarios.

This paper takes a client connecting, publishing and processing messages as an example to show the parameters to be used in each link:

- **Establish a connection**：
  - Specify the MQTT Broker basic information access address and port
  - Specify whether the transfer type is TCP or MQTT over WebSocket
  - If TLS is enabled, it is required to select the protocol version with the corresponding certificate.
  - If Broker has enabled authentication, the client needs to carry the corresponding MQTT Username Password information
  - Configure client parameters such as keepalive duration, clean session callback retention flag, MQTT protocol version, [will message](https://www.emqx.com/en/blog/use-of-mqtt-will-message) (LWT), etc.
- **Subscribe to the topic **: After the connection is successfully established, the topic can be subscribed to when the topic information is specified.
- Specify topic filter Topic, support for the use of the topic wildcards `+` and `#` during subscribing
  - Specify QoS,  Qos 0 1 2 is optional according to the implementation of the client library and the broker. Note that some brokers and cloud service providers do not support some QoS levels. For example, AWS IoT, Alibaba Cloud IoT Suite, and Azure IoT Hub do not support QoS 2 Level message
  - Subscribing to topics may fail due to network issues or Broker ACL rule restrictions
- **Receive messages and process**:
- Generally, the processing function is specified at the time of connection. The processing method is slightly different depending on the network programming model of the client library and the platform.
- **Publishing a message**: Publish a message to a specified topic
  - Specify the target topic. Note that the topic cannot contain the wildcard `+` or `#`, which may lead to message publishing failure and client disconnection (depending on the implementation of broker and Client Library)
  - Specify the message QoS level. There are also different QoS levels supported by different brokers and platforms. For example,  if Azure IoT Hub publishes a message of QoS 2, it will disconnect the client
  - Specify the message body content, whose size cannot exceed the maximum message size set by the broker
  - Specify message Retain  flag
- **Unsubscribe**:
- Specify the target topic
- **Disconnect**:
- Proactively disconnect with issuing a Will Message (LWT)



## Eclipse Paho C and Eclipse Paho Embedded C

Both [Eclipse Paho C](https://www.eclipse.org/paho/clients/c/) and [Eclipse Paho Embedded C](https://www.eclipse.org/paho/clients/c/embedded/)  are client libraries under the Eclipse Paho project, which are full-featured MQTT clients written in ANSI C. Eclipse Paho Embedded C can be used on desktop operating systems, but mainly for Embedded environments such as [mbed](https://mbed.org/)，[Arduino](https://www.arduino.cc/) and [FreeRTOS](https://freertos.org/) .

The client has two kinds of APIs, synchronous and asynchronous, which start with mqttclient and mqttasync respectively:

- The Synchronization API is designed to be simpler and more useful, and some calls will block until the operation is complete, making programming easier.
- There is only one call block `API-waitForCompletion` in the asynchronous API, and the result is notified through the callback, which is more suitable for the environment of the non-main thread.

For detailed download and usage instructions of the two libraries, please go to the project home page to view. This article uses Eclipse Paho C to provide the sample code directly as follows:

```c
#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#include "MQTTClient.h"

#define ADDRESS     "tcp://broker.emqx.io:1883"
#define CLIENTID    "emqx_test"
#define TOPIC       "testtopic/1"
#define PAYLOAD     "Hello World!"
#define QOS         1
#define TIMEOUT     10000L

int main(int argc, char* argv[])
{
    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    MQTTClient_message pubmsg = MQTTClient_message_initializer;
    MQTTClient_deliveryToken token;
    int rc;

    MQTTClient_create(&client, ADDRESS, CLIENTID,
        MQTTCLIENT_PERSISTENCE_NONE, NULL);
  
    // Connection parameters
    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;

    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS)
    {
        printf("Failed to connect, return code %d\n", rc);
        exit(-1);
    }
  
    // Publish message
    pubmsg.payload = PAYLOAD;
    pubmsg.payloadlen = strlen(PAYLOAD);
    pubmsg.qos = QOS;
    pubmsg.retained = 0;
    MQTTClient_publishMessage(client, TOPIC, &pubmsg, &token);
    printf("Waiting for up to %d seconds for publication of %s\n"
            "on topic %s for client with ClientID: %s\n",
            (int)(TIMEOUT/1000), PAYLOAD, TOPIC, CLIENTID);
    rc = MQTTClient_waitForCompletion(client, token, TIMEOUT);
    printf("Message with delivery token %d delivered\n", token);
  
    // Disconnect
    MQTTClient_disconnect(client, 10000);
    MQTTClient_destroy(&client);
    return rc;
}
```



## Eclipse Paho Java Client

[Eclipse Paho Java Client](https://www.eclipse.org/paho/clients/java/) is an MQTT client library written in Java that can be used with JVM or other Java compatible platforms such as Android.

The Eclipse Paho Java Client provides the MqttAsyncClient and MqttClient as asynchronous and synchronization APIs.

**Install via Maven:**

```xml
<dependency>
  <groupId>org.eclipse.paho</groupId>
	<artifactId>org.eclipse.paho.client.mqttv3</artifactId>
	<version>1.2.2</version>
</dependency>
```

The connection sample code is as follows:

**App.java**

```java
package io.emqx;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;


public class App {
    public static void main(String[] args) {
        String subTopic = "testtopic/#";
        String pubTopic = "testtopic/1";
        String content = "Hello World";
        int qos = 2;
        String broker = "tcp://broker.emqx.io:1883";
        String clientId = "emqx_test";
        MemoryPersistence persistence = new MemoryPersistence();

        try {
            MqttClient client = new MqttClient(broker, clientId, persistence);

            // Connection options
            MqttConnectOptions connOpts = new MqttConnectOptions();
            connOpts.setUserName("emqx_test");
            connOpts.setPassword("emqx_test_password".toCharArray());
            // Retain connection
            connOpts.setCleanSession(true);

            // Set callback
            client.setCallback(new PushCallback());

            // Setup connection
            System.out.println("Connecting to broker: " + broker);
            client.connect(connOpts);

            System.out.println("Connected");
            System.out.println("Publishing message: " + content);

            // Publish
            client.subscribe(subTopic);

            // Required parameters for publishing message
            MqttMessage message = new MqttMessage(content.getBytes());
            message.setQos(qos);
            client.publish(pubTopic, message);
            System.out.println("Message published");

            client.disconnect();
            System.out.println("Disconnected");
            client.close();
            System.exit(0);
        } catch (MqttException me) {
            System.out.println("reason " + me.getReasonCode());
            System.out.println("msg " + me.getMessage());
            System.out.println("loc " + me.getLocalizedMessage());
            System.out.println("cause " + me.getCause());
            System.out.println("excep " + me);
            me.printStackTrace();
        }
    }
}

```

**Callback message processing class OnMessageCallback.java**

```java
package io.emqx;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class OnMessageCallback implements MqttCallback {
    public void connectionLost(Throwable cause) {
        // Reconnect after lost connection.
        System.out.println("Connection lost, and re-connect here.");
    }

    public void messageArrived(String topic, MqttMessage message) throws Exception {
        // Message handler after receiving message
        System.out.println("Topic:" + topic);
        System.out.println("QoS:" + message.getQos());
        System.out.println("Payload:" + new String(message.getPayload()));
    }

    public void deliveryComplete(IMqttDeliveryToken token) {
        System.out.println("deliveryComplete---------" + token.isComplete());
    }
}
```





## Eclipse Paho MQTT Go client

[Eclipse Paho MQTT Go Client](https://github.com/eclipse/paho.mqtt.golang) is the Go language client library for the Eclipse Paho project, which can connect to the MQTT Broker to publish messages, subscribe to topics and receive published messages and support a completely asynchronous mode of operation.

Clients rely on Google's [proxy](https://godoc.org/golang.org/x/net/proxy) and [websockets](https://godoc.org/github.com/gorilla/websocket) software Package, which can be installed with the following command:

```bash
go get github.com/eclipse/paho.mqtt.golang
```

The connection sample code is as follows:

```go
package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/eclipse/paho.mqtt.golang"
)

var f mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
	fmt.Printf("TOPIC: %s\n", msg.Topic())
	fmt.Printf("MSG: %s\n", msg.Payload())
}

func main() {
	mqtt.DEBUG = log.New(os.Stdout, "", 0)
	mqtt.ERROR = log.New(os.Stdout, "", 0)
	opts := mqtt.NewClientOptions().AddBroker("tcp://broker.emqx.io:1883").SetClientID("emqx_test_client")
	
	opts.SetKeepAlive(60 * time.Second)
	// Message callback handler
	opts.SetDefaultPublishHandler(f)
	opts.SetPingTimeout(1 * time.Second)

	c := mqtt.NewClient(opts)
	if token := c.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}

	// Subscription
	if token := c.Subscribe("testtopic/#", 0, nil); token.Wait() && token.Error() != nil {
		fmt.Println(token.Error())
		os.Exit(1)
	}
	
	// Publish message
	token := c.Publish("testtopic/1", 0, false, "Hello World")
	token.Wait()

	time.Sleep(6 * time.Second)

	// Cancel subscription
	if token := c.Unsubscribe("testtopic/#"); token.Wait() && token.Error() != nil {
		fmt.Println(token.Error())
		os.Exit(1)
	}
  
    // Disconnect
	c.Disconnect(250)
	time.Sleep(1 * time.Second)
}
```



## emqtt : Erlang MQTT client library provided by EMQ

[emqtt](https://github.com/emqx/emqtt)  is a client library officially provided by EMQ of the open source MQTT Broker EMQX, which is applicable for the Erlang language.

The Erlang ecosystem has several MQTT Broker implementations, such as RabbitMQ, VerenMQ, EMQX, etc. that support MQTT through plugins. However, there is almost no room for choice in the MQTT client library. [emqtt](https://github.com/emqx/emqtt) in the Erlang client library included in the MQTT community is the best choice .

Emqtt is implemented entirely by Erlang and completely supports the MQTT v3.1.1 and MQTT v5.0 protocol. It also supports SSL  single and two-way  authentication and WebSocket connection. Another MQTT benchmarking tool  [emqtt_bench](https://github.com/emqx/emqtt-bench)  is built based on this client library.

emqtt is used as follows:

```erlang
ClientId = <<"test">>.
{ok, ConnPid} = emqtt:start_link([{clientid, ClientId}]).
{ok, _Props} = emqtt:connect(ConnPid).
Topic = <<"guide/#">>.
QoS = 1.
{ok, _Props, _ReasonCodes} = emqtt:subscribe(ConnPid, {Topic, QoS}).
{ok, _PktId} = emqtt:publish(ConnPid, <<"guide/1">>, <<"Hello World!">>, QoS).
%% If the qos of publish packet is 0, `publish` function would not return packetid.
ok = emqtt:publish(ConnPid, <<"guide/2">>, <<"Hello World!">>, 0).

%% Recursively get messages from mail box.
Y = fun (Proc) -> ((fun (F) -> F(F) end)((fun(ProcGen) -> Proc(fun() -> (ProcGen(ProcGen))() end) end))) end.
Rec = fun(Receive) -> fun()-> receive {publish, Msg} -> io:format("Msg: ~p~n", [Msg]), Receive(); _Other -> Receive() after 5 -> ok end end end.
(Y(Rec))().

%% If you don't like y combinator, you can also try named function to recursively get messages in erlang shell.
Receive = fun Rec() -> receive {publish, Msg} -> io:format("Msg: ~p~n", [Msg]), Rec(); _Other -> Rec() after 5 -> ok end end.
Receive().

{ok, _Props, _ReasonCode} = emqtt:unsubscribe(ConnPid, <<"guide/#">>).

ok = emqtt:disconnect(ConnPid).
```



## MQTT.js Web & Node.js platform MQTT client

[MQTT.js](https://www.npmjs.com/package/mqtt) is a module written in JavaScript that implements the MQTT protocol client functionality and can be used in Node.js or in a browser environment. When used in Node.js, the `-g` global installation can be done with a command line, and it can be integrated into the project for callback.

Due to the JavaScript single-threading feature, MQTT.js is a fully asynchronous MQTT client. MQTT.js supports MQTT and MQTT over WebSocket. The degree of support in different runtime environments is as follows:

- Browser environment: MQTT over WebSocket (including custom browser environment such as WeChat applet, Alipay applet)
- Node.js environment: MQTT, MQTT over WebSocket

In addition to a few different connection parameters in different environments, other APIs are the same.

Install with NPM:

```bash
npm i mqtt
```

Install with CDN (browser):

```html
<script src="https://unpkg.com/mqtt/dist/mqtt.min.js"></script>
<script>
    // Initialize a global mqtt variable
    console.log(mqtt)
</script>
```

Sample code:

```javascript
// const mqtt = require('mqtt')
import mqtt from 'mqtt'

// Connection option
const options = {
  		clean: true, // Retain connection
      connectTimeout: 4000, // Timeout
      // Authtication
      clientId: 'emqx_test',
      username: 'emqx_test',
      password: 'emqx_test',
}

// Connection string
// ws: unsecured WebSocket
// wss: secured WebSocket connection
// mqtt: unsecured TCP connection
// mqtts: secured TCP connection
const connectUrl = 'wss://broker.emqx.io:8084/mqtt'
const client = mqtt.connect(connectUrl, options)

client.on('reconnect', (error) => {
    console.log('reconnect:', error)
})

client.on('reconnect', (error) => {
    console.log('reconnect:', error)
})

client.on('message', (topic, message) => {
  console.log('message：', topic, message.toString())
})
```



## Eclipse Paho Python

[Eclipse Paho Python](https://github.com/eclipse/paho.mqtt.python) is the Python language client library under the Eclipse Paho project, which can connect to the MQTT Broker to publish messages, subscribe to topics and receive Published message.

Install with the PyPi package management tool:

```bash
pip install paho-mqtt
```

Sample code:

```python
import paho.mqtt.client as mqtt


# Successful Connection Callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('testtopic/#')

# Message delivery callback
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()

# Set callback handler
client.on_connect = on_connect
client.on_message = on_message

# Set up connection
client.connect('broker.emqx.io', 1883, 60)
# Publish message
client.publish('emqtt',payload='Hello World',qos=0)

client.loop_forever()

```



## Summary

This is the introduction of MQTT protocol, MQTT client library usage process and common MQTT  clients. Readers are welcome to learn MQTT  and develop projects through EMQX.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
