[MQTT (Message Queuing Telemetry Transport)](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is an OASIS standard messaging protocol for the Internet of Things (IoT). It is designed with an extremely lightweight publish/subscribe messaging model, making it ideal for connecting IoT devices with a small code footprint and minimal network bandwidth and exchanging data in real-time between connected devices and cloud services.

This guide provides instructions on establishing connections between [MQTT clients](https://www.emqx.com/en/blog/mqtt-client-tools) and servers, subscribing to topics, and exchanging messages in a Java project.

## Choosing the Java Client Library

For this guide, we will employ the [Eclipse Paho Java Client](https://github.com/eclipse/paho.mqtt.java) as the client library. Widely recognized, it is the most extensively used MQTT client library in the Java language, supporting MQTT 3.1, 3.1.1, and 5.0 protocols.

The sample program requires JDK 1.8.0 or higher and Maven as the build tool. It can also work with IDEs like [IntelliJ IDEA](https://www.jetbrains.com/idea/) or [Eclipse](https://eclipseide.org/). See [Maven](https://maven.apache.org/) for more information.

## Utilizing MQTT 3.1/3.1.1 Protocol in Java

### Initializing the Project

Begin by creating a Maven project in your IDE and include the Paho MQTT v3 dependency in the pom.xml file:

```xml
<project>
...
  <repositories>
    <repository>
      <id>Eclipse Paho Repository</id>
      <url>https://repo.eclipse.org/content/repositories/paho-releases/</url>
    </repository>
  </repositories>
  <dependencies>
  ...
    <dependency>
      <groupId>org.eclipse.paho</groupId>
      <artifactId>org.eclipse.paho.client.mqttv3</artifactId>
      <version>1.2.5</version>
    </dependency>
  </dependencies>
</project>
```

### MQTT Broker

In this guide, we will utilize the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ, built on [EMQX Enterprise](https://www.emqx.com/en/products/emqx). The server access details are as follows:

- Broker: `broker.emqx.io`
- TCP Port: **1883**
- SSL/TLS Port: **8883**

### Configuring MQTT Broker Connection Parameters

To establish a connection with the MQTT Broker, let's begin by configuring the basic information, using a TCP connection as an example.

```java
String broker = "tcp://broker.emqx.io:1883";
String clientId = "demo_client";
```

### Establishing an MQTT Connection

In this step, we create a synchronization client (MqttClient) to connect to the [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) using the previously configured parameters.

```java
MqttClient client = new MqttClient(broker, clientId);
MqttConnectOptions options = new MqttConnectOptions();
client.connect(options);
```

### Connecting to MQTT with TLS/SSL

In scenarios where enhanced communication security is crucial, the client can connect to the MQTT server using TLS/SSL in addition to normal TCP connections.

Java utilizes a TrustManager to verify the trustworthiness of the other side (i.e., the MQTT server side). This TrustManager is integrated into the SSLContext, and the required SSLSocket is created using the SSLSocketFactory obtained from the SSLContext.

For one-way authentication in TLS/SSL, the initial step involves creating the TrustManager and incorporating the MQTT server-side certificate into the certificate store utilized by the TrustManager. The X509 certificate format, whether issued by a trustee organization or self-signed, is commonly used. Here's an example in code:

```java
// Load all certificates in the server-side CA certificate chain. "server_ca.crt" is the full file path of the server-side CA.
InputStream certInput = new FileInputStream("server_ca.crt");
CertificateFactory cf = CertificateFactory.getInstance("X.509");
Collection<? extends Certificate> certs = cf.generateCertificates(certInput);

// Store the certificates in the KeyStore
KeyStore ks = KeyStore.getInstance(KeyStore.getDefaultType());
ks.load(null, null);
int index = 0;
for (Certificate cert : certs) {
  ks.setCertificateEntry("server_ca_" + index++, cert);
}

// Create the TrustManager
TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
tmf.init(ks);
```

Next, utilize the TrustManager to construct the SSLContext and obtain the SSLSocketFactory from it:

```java
SSLContext sslContext = SSLContext.getInstance("TLS");
sslContext.init(null, tmf.getTrustManagers(), null);
SSLSocketFactory socketFactory = sslContext.getSocketFactory();
```

Creates a TLS/SSL connection in the same way as a TCP connection to the MQTT Broker, with an additional SocketFactory specified in the connection options:

```java
String broker = "ssl://broker.emqx.io:8883";
String clientId = "demo_client_ssl";

MqttClient client = new MqttClient(broker, clientId);
MqttConnectOptions options = new MqttConnectOptions();

// Specify the SSLSocketFactory
options.setSocketFactory(socketFactory);
client.connect(options);
```

### Subscribing to MQTT Topics

Once the [MQTT connection](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection) is established, we utilize the callback methods of MqttClient to listen for messages. The messageArrived method of MqttCallback outputs the content of the received message, while other methods of MqttCallback can be employed to listen for various state change events such as connection disconnection, message publishing, and more.

```java
client.setCallback(new MqttCallback() {
  public void messageArrived(String topic, MqttMessage message) throws Exception {
    System.out.println("topic: " + topic);
    System.out.println("qos: " + message.getQos());
    System.out.println("message content: " + new String(message.getPayload()));
  }

  public void connectionLost(Throwable cause) {
    System.out.println("connectionLost: " + cause.getMessage());
  }

  public void deliveryComplete(IMqttDeliveryToken token) {
    System.out.println("deliveryComplete: " + token.isComplete());
  }
});
```

Following this, subscribe to the "topic/test" topic.

```java
String topic = "topic/test";
int qos = 1;
client.subscribe(topic, qos);
```

### Publishing MQTT Messages

To act as a message publisher, establish another MQTT client connection using the previously described method and publish messages to the "topic/test" topic.

```java
String topic = "topic/test";
int qos = 1;
String msg = "Hello MQTT";
MqttMessage message = new MqttMessage(msg.getBytes());
message.setQos(qos);
client.publish(topic, message);
```

### Closing the Connection

Once the task is complete, close the connection between the publishing client and the subscribing client.

```java
client.disconnect();
client.close();
```

## Using the MQTT 5.0 Protocol in Java

To implement the [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) protocol, add the Paho MQTT v5 dependency to `pom.xml`:

```
<project>
...
  <repositories>
    <repository>
      <id>Eclipse Paho Repository</id>
      <url>https://repo.eclipse.org/content/repositories/paho-releases/</url>
    </repository>
  </repositories>
  <dependencies>
  ...
    <dependency>
      <groupId>org.eclipse.paho</groupId>
      <artifactId>org.eclipse.paho.mqttv5.client</artifactId>
      <version>1.2.5</version>
    </dependency>
  </dependencies>
</project>
```

The implementation logic remains the same as using the MQTT 3.1/3.1.1 protocol, but ensure you are using the Paho dependency for MQTT v5.

## Complete Code

The comprehensive code for connecting to the MQTT server, subscribing to topics, and publishing and receiving messages using MQTT 3.1.1 is presented below:

```java
package io.emqx.mqtt.demo;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class JavaDemoMQTTV3 {

	public static void main(String[] args) {
		String broker = "tcp://broker.emqx.io:1883";
		String clientId = "demo_client";
		String topic = "topic/test";
		int subQos = 1;
		int pubQos = 1;
		String msg = "Hello MQTT";

		try {
			MqttClient client = new MqttClient(broker, clientId);
			MqttConnectOptions options = new MqttConnectOptions();
			client.connect(options);

			if (client.isConnected()) {
				client.setCallback(new MqttCallback() {
					public void messageArrived(String topic, MqttMessage message) throws Exception {
						System.out.println("topic: " + topic);
						System.out.println("qos: " + message.getQos());
						System.out.println("message content: " + new String(message.getPayload()));
					}

					public void connectionLost(Throwable cause) {
						System.out.println("connectionLost: " + cause.getMessage());
					}

					public void deliveryComplete(IMqttDeliveryToken token) {
						System.out.println("deliveryComplete: " + token.isComplete());
					}
				});

				client.subscribe(topic, subQos);

				MqttMessage message = new MqttMessage(msg.getBytes());
				message.setQos(pubQos);
				client.publish(topic, message);
			}

			client.disconnect();
			client.close();

		} catch (MqttException e) {
			e.printStackTrace();
		}
	}
}
```

Complete code for MQTT 5.0:

```java
package io.emqx.mqtt.demo;

import org.eclipse.paho.mqttv5.client.IMqttToken;
import org.eclipse.paho.mqttv5.client.MqttCallback;
import org.eclipse.paho.mqttv5.client.MqttClient;
import org.eclipse.paho.mqttv5.client.MqttConnectionOptions;
import org.eclipse.paho.mqttv5.client.MqttDisconnectResponse;
import org.eclipse.paho.mqttv5.common.MqttException;
import org.eclipse.paho.mqttv5.common.MqttMessage;
import org.eclipse.paho.mqttv5.common.packet.MqttProperties;

public class JavaDemoMQTTV5 {

	public static void main(String[] args) {
		String broker = "tcp://broker.emqx.io:1883";
		String clientId = "demo_client";
		String topic = "topic/test";
		int subQos = 1;
		int pubQos = 1;
		String msg = "Hello MQTT";

		try {
			MqttClient client = new MqttClient(broker, clientId);
			MqttConnectionOptions options = new MqttConnectionOptions();

			client.setCallback(new MqttCallback() {
				public void connectComplete(boolean reconnect, String serverURI) {
					System.out.println("connected to: " + serverURI);
				}

				public void disconnected(MqttDisconnectResponse disconnectResponse) {
					System.out.println("disconnected: " + disconnectResponse.getReasonString());
				}

				public void deliveryComplete(IMqttToken token) {
					System.out.println("deliveryComplete: " + token.isComplete());
				}

				public void messageArrived(String topic, MqttMessage message) throws Exception {
					System.out.println("topic: " + topic);
					System.out.println("qos: " + message.getQos());
					System.out.println("message content: " + new String(message.getPayload()));
				}

				public void mqttErrorOccurred(MqttException exception) {
					System.out.println("mqttErrorOccurred: " + exception.getMessage());
				}

				public void authPacketArrived(int reasonCode, MqttProperties properties) {
					System.out.println("authPacketArrived");
				}
			});

			client.connect(options);

			client.subscribe(topic, subQos);

			MqttMessage message = new MqttMessage(msg.getBytes());
			message.setQos(pubQos);
			client.publish(topic, message);

			client.disconnect();
			client.close();

		} catch (MqttException e) {
			e.printStackTrace();
		}
	}
}
```

## Testing

Our application initiates an MQTT client serving as both a message subscriber and publisher. Consider JavaDemoMQTTV5 as an example. Upon executing the program, you will observe connection details, message publishing, and message reception information printed on the console.

## Q&A

### Does the MQTT Broker connection support authentication, auto-retry, and additional configuration options?

Paho's connection option, MqttConnectOptions, offers various connection parameters, allowing customization such as setting usernames, passwords, heartbeat intervals, and more. Here are some common methods:

```java
MqttConnectOptions options = new MqttConnectOptions();

// Username and password used to connect to MQTT Broker
options.setUserName("username");
options.setPassword("password".toCharArray());

// Set whether to clear the session
options.setCleanSession(true);

// Set the heartbeat interval in seconds
options.setKeepAliveInterval(300);

// Set the connection timeout in seconds
options.setConnectionTimeout(30);

// Set whether to automatically reconnect
options.setAutomaticReconnect(true);
```

### How to establish a connection after enabling TLS/SSL two-way authentication in the MQTT Broker?

When TLS/SSL two-way authentication is enabled, the MQTT Broker not only verifies the identity of the client but also requires the client to verify the identity of the server. The handling of the certificate sent from the Java client to the other side is managed by the KeyManager.

In the provided code snippet, the KeyManager utilizes the KeyStore type PKCS12. If the client's certificate is not in PKCS12 format, conversion through openssl is necessary. The conversion process is outlined below:

```
openssl pkcs12 -export -in client.crt -inkey client.key -out client.p12 -password pass:mypassword
```

Here, client.crt represents the client certificate, client.key is the client key, the exported PKCS12 certificate is client.p12, and the key for exporting is set to mypassword. Adjust the parameters as needed based on your specific circumstances.

The following code illustrates the implementation of two-way TLS/SSL authentication, including the logic for verifying the server's identity, along with additional steps for providing the client certificate to the server:

```java
// Load all certificates in the server-side CA certificate chain. "server_ca.crt" is the full file path of the server-side CA.
InputStream certInput = new FileInputStream("server_ca.crt");
CertificateFactory cf = CertificateFactory.getInstance("X.509");
Collection<? extends Certificate> certs = cf.generateCertificates(certInput);

// Store the server-side CA certificates in the KeyStore.
KeyStore tmKs = KeyStore.getInstance(KeyStore.getDefaultType());
tmKs.load(null, null);
int index = 0;
for (Certificate cert : certs) {
	tmKs.setCertificateEntry("server_ca_" + index++, cert);
}

// Create the TrustManager
TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
tmf.init(tmKs);

// Store the client certificate in the KeyStore
String password = "mypassword";	//Same password as used for exporting
KeyStore kmKs = KeyStore.getInstance("PKCS12");
kmKs.load(new FileInputStream(clientCertPath), password.toCharArray());

// Create the KeyManager
KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
kmf.init(kmKs, password.toCharArray());

SSLContext sslContext = SSLContext.getInstance("TLS");
// Set up the KeyManager and TrustManager in the SSLContext.
sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
SSLSocketFactory socketFactory = sslContext.getSocketFactory();
```

If you prefer not to convert your certificate to PKCS12 format, you can also refer to [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Java](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Java).

### Is asynchronous message handling supported?

Paho offers an asynchronous client for handling messages asynchronously. In version 3, the MqttAsyncClient serves as an asynchronous client, allowing you to monitor connection, message publishing, and other activities through a listener.

```java
MqttAsyncClient aClient = new MqttAsyncClient(broker, clientId);
MqttConnectOptions options = new MqttConnectOptions();
aClient.connect(options, new IMqttActionListener() {
	public void onSuccess(IMqttToken asyncActionToken) {
		System.out.println("Connected");
	}

	public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
		System.out.println("Connection failed: " + exception);
	}
});
```

For more details, you can refer to the Paho documentation [IMqttAsyncClient](https://eclipse.dev/paho/files/javadoc/org/eclipse/paho/client/mqttv3/IMqttAsyncClient.html).

## Conclusion

Using the Paho Java Client as an MQTT client in Java, we successfully connected to a [public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker). We performed tests on the client’s connection, message publishing, and topic subscription.

The full code is available at: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Java](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Java).

Next, you can check out [The Easy-to-understand Guide to MQTT Protocol](https://www.emqx.com/en/mqtt-guide) series of articles provided by EMQ to learn about MQTT protocol features, explore more advanced applications of MQTT, and get started with MQTT application and service development.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
