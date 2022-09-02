[MQTT](https://mqtt.org/) is an OASIS standard messaging protocol for the Internet of Things (IoT). It is designed as an extremely lightweight publish/subscribe messaging transport that is ideal for connecting remote devices with a small code footprint and minimal network bandwidth. MQTT today is used in a wide variety of industries, such as automotive, manufacturing, telecommunications, oil and gas, etc.

This article introduces how to use MQTT in the Java project to realize the functions of connecting, subscribing, unsubscribing, publishing, and receiving messages between the client and the broker.



## Add dependency

The development environment for this article is:

-  Build tool: [Maven](https://maven.apache.org/)
-  IDE: [IntelliJ IDEA](https://www.jetbrains.com/idea/)
-  Java: JDK 1.8.0

We will use [Eclipse Paho Java Client](https://github.com/eclipse/paho.mqtt.java) as the client, which is the most widely used MQTT client library in the Java language.

Add the following dependencies to the `pom.xml` file.

```xml
<dependencies>
   <dependency>
       <groupId>org.eclipse.paho</groupId>
       <artifactId>org.eclipse.paho.client.mqttv3</artifactId>
       <version>1.2.5</version>
   </dependency>
</dependencies>
```



## Create an MQTT connection

### MQTT Broker

This article will use the [public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) created based on [EMQX Cloud](https://www.emqx.com/en/cloud). The server access information is as follows:

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- SSL/TLS Port: **8883**

### Connect

Set the basic connection parameters of MQTT. Username and password are optional.

```
String broker = "tcp://broker.emqx.io:1883";
// TLS/SSL
// String broker = "ssl://broker.emqx.io:8883";
String username = "emqx";
String password = "public";
String clientid = "publish_client";
```

Then create an MQTT client and connect to the broker.

```
MqttClient client = new MqttClient(broker, clientid, new MemoryPersistence());
MqttConnectOptions options = new MqttConnectOptions();
options.setUserName(username);
options.setPassword(password.toCharArray());
client.connect(options);
```

Instructions

- MqttClient: MqttClient provides a set of methods that block and return control to the application program once the MQTT action has completed.
- MqttClientPersistence: Represents a persistent data store, used to store outbound and inbound messages while they are in flight, enabling delivery to the QoS specified.
- MqttConnectOptions: Holds the set of options that control how the client connects to a server. Here are some common methods:
  - setUserName: Sets the user name to use for the connection.
  - setPassword: Sets the password to use for the connection.
  - setCleanSession: Sets whether the client and server should remember state across restarts and reconnects.
  - setKeepAliveInterval: Sets the "keep alive" interval. 
  - setConnectionTimeout: Sets the connection timeout value. 
  - setAutomaticReconnect: Sets whether the client will automatically attempt to reconnect to the server if the connection is lost.

### Connecting with TLS/SSL

If you want to use a self-signed certificate for TLS/SSL connections, add [bcpkix-jdk15on](https://mvnrepository.com/artifact/org.bouncycastle/bcpkix-jdk15on) to the `pom.xml` file.

```xml
<!-- https://mvnrepository.com/artifact/org.bouncycastle/bcpkix-jdk15on -->
<dependency>
   <groupId>org.bouncycastle</groupId>
   <artifactId>bcpkix-jdk15on</artifactId>
   <version>1.70</version>
</dependency>

```

Then create the `SSLUtils.java` file with the following code.

```java
package io.emqx.mqtt;

import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.openssl.PEMKeyPair;
import org.bouncycastle.openssl.PEMParser;
import org.bouncycastle.openssl.jcajce.JcaPEMKeyConverter;

import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManagerFactory;
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.FileReader;
import java.security.KeyPair;
import java.security.KeyStore;
import java.security.Security;
import java.security.cert.CertificateFactory;
import java.security.cert.X509Certificate;

public class SSLUtils {
   public static SSLSocketFactory getSocketFactory(final String caCrtFile,
                                                   final String crtFile, final String keyFile, final String password)
           throws Exception {
       Security.addProvider(new BouncyCastleProvider());

       // load CA certificate
       X509Certificate caCert = null;

       FileInputStream fis = new FileInputStream(caCrtFile);
       BufferedInputStream bis = new BufferedInputStream(fis);
       CertificateFactory cf = CertificateFactory.getInstance("X.509");

       while (bis.available() > 0) {
           caCert = (X509Certificate) cf.generateCertificate(bis);
      }

       // load client certificate
       bis = new BufferedInputStream(new FileInputStream(crtFile));
       X509Certificate cert = null;
       while (bis.available() > 0) {
           cert = (X509Certificate) cf.generateCertificate(bis);
      }

       // load client private key
       PEMParser pemParser = new PEMParser(new FileReader(keyFile));
       Object object = pemParser.readObject();
       JcaPEMKeyConverter converter = new JcaPEMKeyConverter().setProvider("BC");
       KeyPair key = converter.getKeyPair((PEMKeyPair) object);
       pemParser.close();

       // CA certificate is used to authenticate server
       KeyStore caKs = KeyStore.getInstance(KeyStore.getDefaultType());
       caKs.load(null, null);
       caKs.setCertificateEntry("ca-certificate", caCert);
       TrustManagerFactory tmf = TrustManagerFactory.getInstance("X509");
       tmf.init(caKs);

       // client key and certificates are sent to server so it can authenticate
       KeyStore ks = KeyStore.getInstance(KeyStore.getDefaultType());
       ks.load(null, null);
       ks.setCertificateEntry("certificate", cert);
       ks.setKeyEntry("private-key", key.getPrivate(), password.toCharArray(),
               new java.security.cert.Certificate[]{cert});
       KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory
              .getDefaultAlgorithm());
       kmf.init(ks, password.toCharArray());

       // finally, create SSL socket factory
       SSLContext context = SSLContext.getInstance("TLSv1.2");
       context.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

       return context.getSocketFactory();
  }
}
```

Set `options` as follows.

```
String broker = "ssl://broker.emqx.io:8883";
// Set socket factory
String caFilePath = "/cacert.pem";
String clientCrtFilePath = "/client.pem";
String clientKeyFilePath = "/client.key";
SSLSocketFactory socketFactory = getSocketFactory(caFilePath, clientCrtFilePath, clientKeyFilePath, "");
options.setSocketFactory(socketFactory);
```



## Publish MQTT messages

Create a class `PublishSample` that will publish a `Hello MQTT` message to the topic `mqtt/test`.

```java
package io.emqx.mqtt;

import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class PublishSample {

   public static void main(String[] args) {

       String broker = "tcp://broker.emqx.io:1883";
       String topic = "mqtt/test";
       String username = "emqx";
       String password = "public";
       String clientid = "publish_client";
       String content = "Hello MQTT";
       int qos = 0;

       try {
           MqttClient client = new MqttClient(broker, clientid, new MemoryPersistence());
           MqttConnectOptions options = new MqttConnectOptions();
           options.setUserName(username);
           options.setPassword(password.toCharArray());
           options.setConnectionTimeout(60);
      options.setKeepAliveInterval(60);
           // connect
           client.connect(options);
           // create message and setup QoS
           MqttMessage message = new MqttMessage(content.getBytes());
           message.setQos(qos);
           // publish message
           client.publish(topic, message);
           System.out.println("Message published");
           System.out.println("topic: " + topic);
           System.out.println("message content: " + content);
           // disconnect
           client.disconnect();
           // close client
           client.close();
      } catch (MqttException e) {
           throw new RuntimeException(e);
      }
  }
}

```



## Subscribe

Create a class `SubscribeSample` that will subscribe to the topic `mqtt/test`.

```
package io.emqx.mqtt;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class SubscribeSample {
   public static void main(String[] args) {
       String broker = "tcp://broker.emqx.io:1883";
       String topic = "mqtt/test";
       String username = "emqx";
       String password = "public";
       String clientid = "subscribe_client";
       int qos = 0;

       try {
           MqttClient client = new MqttClient(broker, clientid, new MemoryPersistence());
           // connect options
           MqttConnectOptions options = new MqttConnectOptions();
           options.setUserName(username);
           options.setPassword(password.toCharArray());
           options.setConnectionTimeout(60);
      options.setKeepAliveInterval(60);
           // setup callback
           client.setCallback(new MqttCallback() {

               public void connectionLost(Throwable cause) {
                   System.out.println("connectionLost: " + cause.getMessage());
              }

               public void messageArrived(String topic, MqttMessage message) {
                   System.out.println("topic: " + topic);
                   System.out.println("Qos: " + message.getQos());
                   System.out.println("message content: " + new String(message.getPayload()));

              }

               public void deliveryComplete(IMqttDeliveryToken token) {
                   System.out.println("deliveryComplete---------" + token.isComplete());
              }

          });
           client.connect(options);
           client.subscribe(topic, qos);
      } catch (Exception e) {
           e.printStackTrace();
      }
  }
}

```

MqttCallback：

- connectionLost(Throwable cause): This method is called when the connection to the server is lost.

- messageArrived(String topic, MqttMessage message): This method is called when a message arrives from the server.

- deliveryComplete(IMqttDeliveryToken token): Called when delivery for a message has been completed, and all acknowledgments have been received.

  

## Test

Next, run `SubscribeSample` to subscribe to the `mqtt/test` topic. Then run `PublishSample` to publish the message to the `mqtt/test` topic. We will see that the publisher successfully publishes the message and the subscriber receives it.

![Java MQTT](https://assets.emqx.com/images/6ba659361e5cbaf0fc90996b77c547cf.png?imageMogr2/thumbnail/1520x)



Now we are done using Paho Java Client as an MQTT client to connect to the [public MQTT server](https://www.emqx.com/en/mqtt/public-mqtt5-broker) and implement message publishing and subscription.

The full code is available at: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Java](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Java).


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
