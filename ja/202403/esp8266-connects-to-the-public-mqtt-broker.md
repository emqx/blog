[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt) は、IoTメッセージを交換し、データを配信するための軽量で柔軟なプロトコルです。IoT開発者のために、柔軟性とハードウェア/ネットワークリソースのバランスを実現することに専念しています。

[ESP8266](https://www.espressif.com/) は、高度に統合されたWi-Fi SoCソリューションを提供します。その低消費電力、コンパクトな設計、および高い安定性は、ユーザーの要件を満たすことができます。ESP8266には、独立して動作するか、または他のホストMCUのスレーブとして動作する完全かつ自己完結型のWi-Fiネットワーク機能があります。

このプロジェクトでは、Arduino IDEを使用してESP8266をプログラミングし、[EMQX Cloud](https://www.emqx.com/ja/cloud)が運営・維持する[無料の公開MQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)にESP8266を接続する方法を実装します。EMQX Cloudは、EMQが提供する**セキュリティ付きMQTT IoTクラウドサービスプラットフォーム**です。一元化された運用保守代行と、ユニークな隔離環境を持つ[MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5)接続サービスを提供します。

## 必要なIoTコンポーネント

- ESP8266
- Arduino IDE
- [MQTTX](https://mqttx.app/ja): クロスプラットフォームMQTT 5.0クライアントツール
- 無料の公開MQTTブローカー
  - ブローカー: `broker.emqx.io`
  - TCPポート: **1883**
  - Websocketポート: **8083**

## ESP8266のPub/Sub

![project.png](https://assets.emqx.com/images/800906ed7aa829fb5134a6237cbc05b4.png)

## ソースコード

1. まず、ライブラリ**ESP8266WiFi**と**PubSubClient**をインポートします。ESP8266WiFiライブラリはESP8266をWi-Fiネットワークに接続し、PubSubClientライブラリはESP8266が[MQTTブローカー](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison)にメッセージを公開し、トピックを購読することを可能にします。

   ```c
   #include <ESP8266WiFi.h>
   #include <PubSubClient.h>
   ```

2. Wi-Fiの名前とパスワード、MQTTブローカーの接続アドレスとポートを設定します。

   ```c
   // WiFi
   const char *ssid = "mousse"; // Enter your WiFi name
   const char *password = "qweqweqwe";  // Enter WiFi password
   
   // MQTT Broker
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "esp8266/test";
   const char *mqtt_username = "emqx";
   const char *mqtt_password = "public";
   const int mqtt_port = 1883;
   
   ```

3. プログラムの結果を出力し、Wi-Fiネットワークに接続するためのシリアル接続を開きます。

   ```c
   // Set software serial baud to 115200;
   Serial.begin(115200);
   // connecting to a WiFi network
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
       delay(500);
       Serial.println("Connecting to WiFi..");
   }
   ```

4. MQTTブローカーを設定し、コールバック関数を書き、同時にシリアルモニターに接続情報を表示します。

   ```c
   client.setServer(mqtt_broker, mqtt_port);
   client.setCallback(callback);
   while (!client.connected()) {
       String client_id = "esp8266-client-";
       client_id += String(WiFi.macAddress());
       Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
       if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
       } else {
           Serial.print("failed with state ");
           Serial.print(client.state());
           delay(2000);
       }
   }
   
   void callback(char *topic, byte *payload, unsigned int length) {
       Serial.print("Message arrived in topic: ");
       Serial.println(topic);
       Serial.print("Message:");
       for (int i = 0; i < length; i++) {
           Serial.print((char) payload[i]);
       }
       Serial.println();
       Serial.println("-----------------------");
   }
   ```

5. MQTTブローカーに正常に接続した後、ESP8266はメッセージを公開し、MQTTブローカーを購読します。

   ```c
   // Publish and subscribe
   client.publish(topic, "hello emqx");
   client.subscribe(topic);
   ```

6. シリアルポートにトピック名を表示し、受信したメッセージの各バイトを出力します。

   ```c
   void callback(char *topic, byte *payload, unsigned int length) {
       Serial.print("Message arrived in topic: ");
       Serial.println(topic);
       Serial.print("Message:");
       for (int i = 0; i < length; i++) {
           Serial.print((char) payload[i]);
       }
       Serial.println();
       Serial.println("-----------------------");
   }
   ```

7. 完全なコード

   ```c
   #include <ESP8266WiFi.h>
   #include <PubSubClient.h>
   
   // WiFi
   const char *ssid = "mousse"; // Enter your WiFi name
   const char *password = "qweqweqwe";  // Enter WiFi password
   
   // MQTT Broker
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "esp8266/test";
   const char *mqtt_username = "emqx";
   const char *mqtt_password = "public";
   const int mqtt_port = 1883;
   
   WiFiClient espClient;
   PubSubClient client(espClient);
   
   void setup() {
     // Set software serial baud to 115200;
     Serial.begin(115200);
     // connecting to a WiFi network
     WiFi.begin(ssid, password);
     while (WiFi.status() != WL_CONNECTED) {
         delay(500);
         Serial.println("Connecting to WiFi..");
     }
     Serial.println("Connected to the WiFi network");
     //connecting to a mqtt broker
     client.setServer(mqtt_broker, mqtt_port);
     client.setCallback(callback);
     while (!client.connected()) {
         String client_id = "esp8266-client-";
         client_id += String(WiFi.macAddress());
         Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
         if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
             Serial.println("Public emqx mqtt broker connected");
         } else {
             Serial.print("failed with state ");
             Serial.print(client.state());
             delay(2000);
         }
     }
     // publish and subscribe
     client.publish(topic, "hello emqx");
     client.subscribe(topic);
   }
   
   void callback(char *topic, byte *payload, unsigned int length) {
     Serial.print("Message arrived in topic: ");
     Serial.println(topic);
     Serial.print("Message:");
     for (int i = 0; i < length; i++) {
         Serial.print((char) payload[i]);
     }
     Serial.println();
     Serial.println("-----------------------");
   }
   
   void loop() {
     client.loop();
   }
   ```

## 実行とテスト

1. [Arduino IDE](https://www.arduino.cc/en/Main/Software)を使用してESP8266に完全なコードをアップロードし、シリアルモニターを開いてください。

   ![esp_con.png](https://assets.emqx.com/images/4c97b1546d31021cc22c64ae7ce4863b.png)

2. MQTTXクライアントとMQTTブローカーとの接続を確立し、ESP8266にメッセージを送信します。

   ![mqttx_pub.png](https://assets.emqx.com/images/daa2c401453155045f2c068bcd57d66a.png)

3. シリアルモニターでESP8266が受信したメッセージを確認します。

   ![esp_msg.png](https://assets.emqx.com/images/8c98d850cdfd5c98db94471d0f6a308f.png)

## まとめ

これまでに、EMQX Cloudが提供する無料の公開MQTTブローカーにESP8266を接続することに成功しました。このプロジェクトでは、ESP8266をMQTTブローカーに接続しましたが、ESP8266はさまざまなIoTセンサーに接続し、センサーデータをMQTTブローカーに報告することも可能です。

次に、EMQが提供する[MQTTプロトコルに関する簡単なガイド](https://www.emqx.com/ja/mqtt-guide)シリーズの記事で、MQTTプロトコルの特徴について学び、MQTTのより高度なアプリケーションを探求し、MQTTアプリケーションおよびサービス開発を始めることができます。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
