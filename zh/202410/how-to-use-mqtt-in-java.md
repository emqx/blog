[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种基于发布/订阅模式的 **轻量级物联网消息传输协议**，可在严重受限的硬件设备和低带宽、高延迟的网络上实现稳定传输。它凭借简单易实现、支持 QoS、报文小等特点，占据了物联网协议的半壁江山。

本文主要介绍如何在 Java 项目中实现 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)与服务器的连接、订阅和收发消息等功能。

## Java 客户端库选择

本文将使用 [Eclipse Paho Java Client](https://github.com/eclipse/paho.mqtt.java) 作为客户端。该客户端是 Java 语言中使用最为广泛的 [MQTT 客户端库](https://www.emqx.com/zh/mqtt-client-sdk)，支持 MQTT 3.1, 3.1.1 和 5.0 协议。

示例程序使用 JDK 1.8.0 及以上版本，并使用 Maven 作为构建工具。您可以使用 [IntelliJ IDEA](https://www.jetbrains.com/idea/) 或 [Eclipse](https://eclipseide.org/) 等 IDE 集成 Maven，更多信息请参考 [Maven – Welcome to Apache Maven](https://maven.apache.org/) 。

## 在 Java 中使用 MQTT 3.1/3.1.1 协议

### 项目初始化

在 IDE 中创建 Maven 项目，并将 Paho MQTT v3 依赖添加到 pom.xml 中：

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

### MQTT 服务器

本文将使用 EMQX 提供的 [免费公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，该服务基于 EMQX 的 [MQTT 云平台](https://www.emqx.com/zh/cloud) 创建。服务器接入信息如下：

- Broker: `broker.emqx.io` 
- TCP Port: **1883**
- SSL/TLS Port: **8883**

### 设置 MQTT Broker 连接参数

我们将首先以 TCP 连接为例，设置 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)的基本连接信息。

```java
String broker = "tcp://broker.emqx.io:1883";
String clientId = "demo_client";
```

### 创建 MQTT 连接

这里将创建同步客户端（`MqttClient`），使用刚才设置的参数连接到 MQTT Broker 上。

```java
MqttClient client = new MqttClient(broker, clientId);
MqttConnectOptions options = new MqttConnectOptions();
client.connect(options);
```

### 使用 TLS/SSL 连接到 MQTT

除了普通的 TCP 连接外，很多场景下为了加强通信安全，客户端连接时会使用 TLS/SSL，对 MQTT 服务器端进行验证。

Java 使用 TrustManager 验证对端（即 MQTT 服务器端）是否可信任，在 SSLContext 中使用这个 TrustManager，并通过 SSLContext 获取 SSLSocketFactory 来创建所需的 SSLSocket。

以 TLS/SSL 单向认证为例，首先，需要创建 TrustManager，并将 MQTT 服务器端的证书放入 TrustManager 使用的证书库中。无论是受信机构签发的，还是自签名的证书，X509 都是很常见的证书格式，我们的代码中将以它为例：

```java
// 加载服务器端 CA 证书链上的所有证书。"server_ca.crt" 为服务器端 CA 的完整文件路径
InputStream certInput = new FileInputStream("server_ca.crt");
CertificateFactory cf = CertificateFactory.getInstance("X.509");
Collection<? extends Certificate> certs = cf.generateCertificates(certInput); 

// 将证书存入 KeyStore
KeyStore ks = KeyStore.getInstance(KeyStore.getDefaultType());
ks.load(null, null);
int index = 0;
for (Certificate cert : certs) {
  ks.setCertificateEntry("server_ca_" + index++, cert);
}

// 创建 TrustManager
TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
tmf.init(ks);
```

然后，使用 TrustManager 构造 SSLContext ，并从中获取 SSLSocketFactory：

```java
SSLContext sslContext = SSLContext.getInstance("TLS");
sslContext.init(null, tmf.getTrustManagers(), null);
SSLSocketFactory socketFactory = sslContext.getSocketFactory();
```

创建 TLS/SSL 连接的方式和 TCP 连接 MQTT Broker 类似，只需在连接选项中额外指定 SocketFactory：

```java
String broker = "ssl://broker.emqx.io:8883";
String clientId = "demo_client_ssl";

MqttClient client = new MqttClient(broker, clientId);
MqttConnectOptions options = new MqttConnectOptions();
// 指定 SSLSocketFactory
options.setSocketFactory(socketFactory);
client.connect(options);
```

### 订阅 MQTT 主题

建立 [MQTT 连接](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)后，我们使用 `MqttClient` 的回调方法监听消息接收，`MqttCallback` 中的 `messageArrived` 方法在接收到消息时将输出相应内容。`MqttCallback` 中的其他方法也可以帮助监听连接断开、消息发布等不同的状态变更事件。

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

然后，订阅 `topic/test` 主题。

```java
String topic = "topic/test";
int qos = 1;
client.subscribe(topic, qos);
```

### 发布 MQTT 消息

我们可以使用上面介绍的方法建立另一个 MQTT 客户端连接作为消息发布者，向 `topic/test` 主题发布消息。

```java
String topic = "topic/test";
int qos = 1;
String msg = "Hello MQTT";
MqttMessage message = new MqttMessage(msg.getBytes());
message.setQos(qos);
client.publish(topic, message);
```

### 关闭连接

完成后，关闭发布客户端和订阅客户端的连接。

```java
client.disconnect();
client.close();
```

## 在 Java 中使用 MQTT 5.0 协议

使用 [MQTT 5.0](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 协议，需要将 Paho MQTT v5 依赖添加到 pom.xml 中：

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
      <artifactId>org.eclipse.paho.mqttv5.client</artifactId>
      <version>1.2.5</version>
    </dependency>
  </dependencies>
</project>

```

代码的实现逻辑与使用 MQTT 3.1/3.1.1 协议相同，但需要确保使用的是 MQTT v5 的 Paho 依赖。

## 完整代码

使用 MQTT 3.1.1 连接 MQTT 服务器、订阅主题、发布消息与接收的完整代码如下：

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

使用 MQTT 5.0 的完整代码如下 ：

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

## 测试

我们的程序中启动了一个 MQTT 客户端，同时作为消息订阅者和发布者。以 `JavaDemoMQTTV5` 为例，运行程序后，可以看到控制台打印出的连接、消息发布和消息接收的信息。

![测试结果](https://assets.emqx.com/images/f0c2d6f8a8f8608a9e52dfb0e4e011b5.png)

## Q&A

### 连接到 MQTT Broker 时是否支持连接认证信息、自动重试等更多的配置选项？

Paho 的连接选项 `MqttConnectOptions` 提供了多种连接参数，包括设置用户名、密码、心跳间隔时间等。以下列举一些常见方法。

```java
MqttConnectOptions options = new MqttConnectOptions();
// 连接 MQTT Broker 的用户名密码
options.setUserName("username");
options.setPassword("password".toCharArray());
// 是否清除会话
options.setCleanSession(true);
// 心跳间隔，单位为秒
options.setKeepAliveInterval(300);
// 连接超时时间，单位为秒
options.setConnectionTimeout(30);
// 是否自动重连
options.setAutomaticReconnect(true);
```

### MQTT Broker 启用 TLS/SSL 双向认证后，如何连接？

TLS/SSL 双向认证除了客户端验证服务器端身份，服务器端也要验证客户端的身份。从 Java 客户端发给对端的证书由 KeyManager 负责。

在以下的示例代码中，KeyManager 使用的 KeyStore 类型为 PKCS12，如果客户端使用的证书不是 PKCS12 格式，需要先通过 openssl 转换一下。转换方法如下：

```shell
openssl pkcs12 -export -in client.crt -inkey client.key -out client.p12 -password pass:mypassword
```

其中，client.crt 为客户端证书，client.key 为客户端密钥，导出的 PKCS12 证书为client.p12，导出密钥设置为mypassword。您也可以根据实际情况设置。

实现了TLS/SSL 双向认证的关键代码如下所示，它包含了上面认证服务器端身份的逻辑，并新增了向服务器端提供客户端证书的逻辑：

```java
// 加载服务器端 CA 证书链上的所有证书。"server_ca.crt" 为服务器端 CA 的完整文件路径
InputStream certInput = new FileInputStream("server_ca.crt");
CertificateFactory cf = CertificateFactory.getInstance("X.509");
Collection<? extends Certificate> certs = cf.generateCertificates(certInput); 

// 将服务器端 CA 证书存入 KeyStore
KeyStore tmKs = KeyStore.getInstance(KeyStore.getDefaultType());
tmKs.load(null, null);
int index = 0;
for (Certificate cert : certs) {
	tmKs.setCertificateEntry("server_ca_" + index++, cert);
}

// 创建 TrustManager
TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
tmf.init(tmKs);

// 将客户端证书存入 KeyStore
String password = "mypassword";	//与导出密码一致
KeyStore kmKs = KeyStore.getInstance("PKCS12");
kmKs.load(new FileInputStream(clientCertPath), password.toCharArray());

// 创建 KeyManager
KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
kmf.init(kmKs, password.toCharArray());

SSLContext sslContext = SSLContext.getInstance("TLS");
// SSLContext 中设置好 KeyManager 和 TrustManager
sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);
SSLSocketFactory socketFactory = sslContext.getSocketFactory();
```

如果不希望将证书转为 PKCS12 格式，您也可以参考 [MQTT-Client-Examples/mqtt-client-Java at master · emqx/MQTT-Client-Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Java)。

### 能否以异步方式进行消息的收发？

Paho 提供了异步客户端。以 v3 版本为例，使用 `MqttAsyncClient` 作为异步客户端，同时可以通过监听器监听连接、消息发布等动作。

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

您可以参考 Paho 文档 [IMqttAsyncClient](https://eclipse.dev/paho/files/javadoc/org/eclipse/paho/client/mqttv3/IMqttAsyncClient.html)  获取更多信息。

## 总结

至此，我们完成了在 Java 中使用 Paho Java Client 来作为 MQTT 客户端连接到 [公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)，并实现了测试客户端与 MQTT 服务器的连接、消息发布和订阅。

完整代码请见：[MQTT-Client-Examples/mqtt-client-Java at master · emqx/MQTT-Client-Examples](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Java)。

接下来，读者可访问 EMQ 提供的 [MQTT 入门与进阶](https://www.emqx.com/zh/mqtt-guide)系列文章学习 MQTT 主题及通配符、保留消息、遗嘱消息等相关概念，探索 MQTT 的更多高级应用，开启 MQTT 应用及服务开发。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
