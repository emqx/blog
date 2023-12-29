[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、IoT(Internet of Things)のためのOASIS標準メッセージングプロトコルです。 MQTTは、コードフットプリントが小さく、ネットワーク帯域幅が最小限のリモートデバイスを接続するのに理想的な、極めて軽量なパブリッシュ/サブスクライブメッセージングトランスポートとして設計されています。 今日、MQTTは自動車、製造、通信、石油・ガスなど、さまざまな業種で広く使用されています。

この記事では、JavaプロジェクトでMQTTを使用して、クライアントとブローカー間の接続、サブスクリプション、アンサブスクライブ、パブリッシュ、メッセージの受信などの機能を実現する方法を紹介します。

## 依存関係の追加

この記事の開発環境は以下のとおりです:

- ビルドツール: [Maven](https://maven.apache.org/)
- IDE: [IntelliJ IDEA](https://www.jetbrains.com/idea/)
- Java: JDK 1.8.0

クライアントとして、Java言語で最も広く使用されている[MQTTクライアントライブラリ](https://www.emqx.com/ja/mqtt-client-sdk)である[Eclipse Paho Java Client](https://github.com/eclipse/paho.mqtt.java)を使用します。

`pom.xml`ファイルに次の依存関係を追加します。

```
<dependencies>
   <dependency>
       <groupId>org.eclipse.paho</groupId>
       <artifactId>org.eclipse.paho.client.mqttv3</artifactId>
       <version>1.2.5</version>
   </dependency>
</dependencies>
```

## MQTT接続の作成

### MQTTブローカー

この記事では、[EMQX Cloud](https://www.emqx.com/ja/cloud)ベースで作成された[フリーのパブリックMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。サーバーアクセス情報は次のとおりです:

- ブローカー: `broker.emqx.io`
- TCPポート: **1883**
- SSL/TLSポート: **8883**

### 接続

MQTTの基本的な接続パラメータを設定します。ユーザー名とパスワードはオプションです。

```
String broker = "tcp://broker.emqx.io:1883";
// TLS/SSL
// String broker = "ssl://broker.emqx.io:8883";
String username = "emqx";
String password = "public";
String clientid = "publish_client";
```

次に、[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)を作成し、ブローカーに接続します。

```
MqttClient client = new MqttClient(broker, clientid, new MemoryPersistence());
MqttConnectOptions options = new MqttConnectOptions();
options.setUserName(username);
options.setPassword(password.toCharArray());
client.connect(options);
```

説明

- MqttClient: MqttClientは、MQTTアクションが完了するとアプリケーションプログラムに制御を戻すブロッキングメソッドのセットを提供します。
- MqttClientPersistence: 送受信中のアウトバウンドメッセージとインバウンドメッセージを格納する永続データストアを表し、指定されたQoSでの配信を可能にします。
- MqttConnectOptions: クライアントがサーバーに接続する方法を制御するオプションのセットを保持します。 ここでは、一般的なメソッドを紹介します:
  - setUserName: 接続に使用するユーザー名を設定します。
  - setPassword: 接続に使用するパスワードを設定します。
  - setCleanSession: クライアントとサーバーが再起動と再接続で状態を記憶するかどうかを設定します。
  - setKeepAliveInterval: キープアライブインターバルを設定します。
  - setConnectionTimeout: 接続タイムアウト値を設定します。
  - setAutomaticReconnect: 接続が失われた場合にクライアントがサーバーへの再接続を自動的に試みるかどうかを設定します。

### TLS/SSLでの接続

TLS/SSL接続に自己署名証明書を使用する場合は、`pom.xml`ファイルに[bcpkix-jdk15on](https://mvnrepository.com/artifact/org.bouncycastle/bcpkix-jdk15on)を追加します。

```
<!-- https://mvnrepository.com/artifact/org.bouncycastle/bcpkix-jdk15on -->
<dependency>
   <groupId>org.bouncycastle</groupId>
   <artifactId>bcpkix-jdk15on</artifactId>
   <version>1.70</version>
</dependency>
```

次に、次のコードの`SSLUtils.java`ファイルを作成します。

```
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

`options`を次のように設定します。

```
String broker = "ssl://broker.emqx.io:8883";
// Set socket factory
String caFilePath = "/cacert.pem";
String clientCrtFilePath = "/client.pem";
String clientKeyFilePath = "/client.key";
SSLSocketFactory socketFactory = getSocketFactory(caFilePath, clientCrtFilePath, clientKeyFilePath, "");
options.setSocketFactory(socketFactory);
```

## MQTTメッセージのパブリッシュ

`mqtt/test`トピックに`Hello MQTT`メッセージをパブリッシュする`PublishSample`クラスを作成します。

```
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

## サブスクライブ

`mqtt/test`トピックを購読する`SubscribeSample`クラスを作成します。

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

MqttCallback:

- connectionLost(Throwable cause): これはサーバーへの接続が失われたときに呼び出されるメソッドです。
- messageArrived(String topic, MqttMessage message): これはサーバーからメッセージが到着したときに呼び出されるメソッドです。
- deliveryComplete(IMqttDeliveryToken token): メッセージの配信が完了し、すべての確認応答が受信されたときに呼び出されます。

## テスト

次に、`SubscribeSample`を実行して`mqtt/test`トピックを購読します。次に、`PublishSample`を実行して`mqtt/test`トピックにメッセージをパブリッシュします。パブリッシャーがメッセージを正常にパブリッシュし、サブスクライバーがそれを受信するのがわかります。

![Test](https://assets.emqx.com/images/6ba659361e5cbaf0fc90996b77c547cf.png)

## まとめ

以上で、Paho Java ClientをMQTTクライアントとして使用して、[パブリックMQTTサーバー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)に接続し、メッセージのパブリッシュとサブスクリプションを実装することができました。

完全なコードはこちらで入手できます: [https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Java](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Java)

次に、EMQが提供する[MQTTプロトコルの易しく理解できるガイド](https://www.emqx.com/en/mqtt-guide)の記事シリーズをチェックアウトして、MQTTプロトコルの機能を学習したり、MQTTのさらに高度なアプリケーションを探求したり、MQTTアプリケーションとサービス開発を開始したりできます。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
