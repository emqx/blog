## はじめに

[MQTT（Message Queuing Telemetry Transport）](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、[パブリッシュ/サブスクライブモデル](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model)を採用したIoT（Internet of Things）向けの軽量メッセージングプロトコルです。コードと帯域幅の使用を最小限に抑えつつ、リアルタイムで信頼性の高い通信を提供します。MQTTは、リソースや帯域幅が限定的なデバイスにとって特に有益で、IoT、モバイルインターネット、IoV（Internet of Vehicles）、エネルギー業界で広く使用されています。

[ESP8266](https://www.emqx.com/en/blog/esp8266-connects-to-the-public-mqtt-broker)の後継モデルである[ESP32](https://www.espressif.com/en/products/socs/esp32)は、低コストで消費電力の少ないシステム・オン・チップマイクロコントローラーです。Wi-Fi機能に加えて、ESP32にはBluetooth 4.0も搭載されています。デュアルコアCPUは80MHzから240MHzの周波数で動作します。2つのWi-Fiモジュール、Bluetoothモジュール、そしてさまざまな入出力ピンを備えています。ESP32はIoTプロジェクトに最適な選択肢と言えるでしょう。

ESP32でMQTTを使うことには以下のような利点があります：

- MQTTはESP32やWi-Fiなどのリソースや帯域幅に制約があるデバイスやネットワークに最適化された軽量なメッセージングプロトコルであるため、電力消費や帯域幅の影響を最小限に抑えることができます。
- MQTTはESP32の能力に応じて、さまざまな信頼性とサービス品質をサポートしています。この柔軟性により、ネットワークが不安定な状況でも使用することが可能です。
- ESP32とMQTTはIoTアプリケーションで広く使用されているため、IoTソリューションに簡単に統合することができます。また、MQTTプロトコルはクラウドプラットフォームとの統合を容易にし、ネットワーク経由でデバイスの制御やデータの監視を可能にします。

結論として、ESP32とMQTTの組み合わせは、無線接続と大量のデバイス間で効率的なメッセージングを必要とするIoTアプリケーションに最適な解決策です。このブログ記事では、Arduino IDEを使用してESP32でMQTTメッセージをパブリッシュし、トピックをサブスクライブするプロセスを紹介します。これにより、IoTデバイスやアプリケーションの開発者は、ESP32とMQTTを使用したシステムの構築に必要な知識を得ることができます。

## MQTTブローカーの準備

このチュートリアルを始める前に、MQTTブローカーが準備されていることを確認してください。MQTTブローカーは、MQTTクライアント間のメッセージの受け渡しを担当する重要なコンポーネントです。MQTTブローカーの入手方法はいくつかあります：

-  **プライベート展開**

  [EMQX](https://www.emqx.io/)は、IoT、IIoT、コネクテッドカー向けの最もスケーラブルなオープンソースのMQTTブローカーです。以下のDockerコマンドを実行することでEMQXをインストールすることができます。

  ```
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  ```

- **フルマネージド・クラウドサービス**

  フルマネージドクラウドサービスは、MQTTサービスを開始するための最も簡単な方法です。[EMQX Cloud](https://www.emqx.com/ja/cloud)を利用すれば、わずか数分でサービスを開始でき、AWS、Google Cloud、Microsoft Azureの20以上のリージョンでMQTTサービスを実行し、グローバルな可用性と高速接続を確保することが可能です。

  最新版の[EMQX Cloud Serverless](https://www.emqx.com/ja/cloud/serverless-mqtt)は、開発者が数秒で簡単にMQTTの導入を開始できるように、永久無料の1Mセッション分/月の無償提供をしています。

-  **無料公開のMQTTブローカー**

  無料公開MQTTブローカーは、MQTTプロトコルの学習とテストを希望する人だけが利用できます。セキュリティリスクやダウンタイムの懸念があるため、本番環境での使用は避けることが重要です。

このブログ記事では、 `broker.emqx.io` にある無料のパブリックMQTTブローカーを使用します。

>  ***MQTTブローカー情報***
>
>  *Broker:* `broker.emqx.io`
>
>  *TCP port：* `1883`
>
> *WebSocket port：* `8083`
>
>  *SSL/TLS port:* `8883`
>
> *SECURE WebSocket port：* `8084`

詳しくは、こちらをご確認ください：[無料公開のMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)。

## ESP32でMQTTを始める

### Arduinoの設定

Arduinoは、使いやすいハードウェアとソフトウェアに基づいたオープンソースのエレクトロニクス・プラットフォームです。Arduinoは、インタラクティブなプロジェクトを作るすべての人を対象としている。Arduinoボードは、センサーの光、ボタンを押す指、Twitterのメッセージといった入力を読み取り、モーターを作動させたり、LEDを点灯させたり、オンラインで何かを公開したりといった出力に変換することができる。

このプロジェクトでは、Arduinoボードを使用してESP32モジュールをコンピューターに接続する。ArduinoはESP32へのコードのアップロードを処理し、ESP32とラップトップ間のシリアル接続を提供します。

Arduinoのインストール方法については、[Arduinoの公式ドキュメント](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing)を参照してください。

#### ESP32開発ボードをインストールする

ESP32開発ボードは、ESP32プラットフォームでMQTTを使用する上で非常に重要です。ESP32上でMQTTベースのプロジェクトを開発および展開するためのハードウェアおよびソフトウェアサポートを提供します。統合Wi-FiおよびBluetooth機能、外部コンポーネントとのインターフェース用GPIOピン、Arduino IDEとの互換性を備えたESP32開発ボードは、MQTTベースのIoTアプリケーションのシームレスな接続、プロトタイピング、テストを可能にします。

ここでは、Arduino IDEにESP32開発ボードをインストールする手順を説明します：

1. Arduino IDEメニューの "Tools "をクリックする。
2. 開発ボード」を選択し、「開発ボード管理」を選択する。
3. Boards Managerで "ESP32 "を検索する。
4. 見つかったらそれをクリックし、「インストール」ボタンをクリックする。

![Install ESP32 development board](https://assets.emqx.com/images/99c502b39ef7d21dc75632e42aa89708.png)

#### PubSubClientのインストール

次に、[MQTTクライアント・ライブラリ](https://www.emqx.com/en/mqtt-client-sdk)[PubSubClient](https://github.com/knolleary/pubsubclient)をインストールします。Nick O'Leary氏によって開発されたPubSubClientは、Arduinoベースのプロジェクト用に設計された軽量のMQTTクライアント・ライブラリです。MQTTをサポートするサーバーとのシンプルなパブリッシュ／サブスクライブ・メッセージング用のクライアントを提供します。このライブラリはMQTT通信を簡素化し、ArduinoベースのIoTアプリケーションで効率的なデータ交換を可能にします。

PubSubClientライブラリをインストールするには、以下の手順に従ってください：

1. Arduino IDEを開き、メニューバーの "Project "に進む。
2. Load library "を選択し、"Library manager "を選択する。
3. ライブラリ・マネージャで検索バーに「PubSubClient」と入力します。
4. Nick O'Learyによるライブラリ "PubSubClient "を探し、"Install "ボタンをクリックする。

![Install PubSub client](https://assets.emqx.com/images/cb7b0228aa91bf300eec5a725da159d3.png)

以下の手順に従って、Arduino IDEにPubSubClientライブラリをインストールします。

### MQTTコネクションの作成

#### TCPコネクション

1. まず、WiFiライブラリとPubSubClientライブラリをインポートする必要がある。WiFiライブラリを使用すると、ESP32がWi-Fiネットワークとの接続を確立できるようになり、PubSubClientライブラリを使用すると、ESP32がMQTTブローカーに接続してメッセージを発行したり、トピックを購読したりできるようになる。

   ```
   #include <WiFi.h>
   #include <PubSubClient.h>
   ```

2. 以下のパラメータを設定してください：Wi-Fiネットワーク名とパスワード、MQTTブローカーのアドレスとポート、トピックを `emqx/esp32` に設定してください。

   ```
   // WiFi
   const char *ssid = "xxxxx"; // Enter your WiFi name
   const char *password = "xxxxx";  // Enter WiFi password
   
   // MQTT Broker
   const char *mqtt_broker = "broker.emqx.io";
   const char *topic = "emqx/esp32";
   const char *mqtt_username = "emqx";
   const char *mqtt_password = "public";
   const int mqtt_port = 1883;
   ```

3. シリアル接続を開いてプログラム結果を表示し、Wi-Fiネットワークへの接続を確立する。

   ```
   // Set software serial baud to 115200;
   Serial.begin(115200);
   // Connecting to a Wi-Fi network
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
       delay(500);
       Serial.println("Connecting to WiFi..");
   }
   ```

4. PubSubClient を使用して MQTT ブローカとの接続を確立する。

   ```
   client.setServer(mqtt_broker, mqtt_port);
   client.setCallback(callback);
   while (!client.connected()) {
       String client_id = "esp32-client-";
       client_id += String(WiFi.macAddress());
       Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
       if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
           Serial.println("Public EMQX MQTT broker connected");
       } else {
           Serial.print("failed with state ");
           Serial.print(client.state());
           delay(2000);
       }
   }
   ```

#### TLS/SSL

MQTTでTLSを使用することで、情報の機密性と完全性を確保し、情報の漏洩や改ざんを防ぐことができる。

このESP32コードは、サーバーのルートCA証明書を使用して安全なWi-Fi接続を確立します。ca_cert 変数にはルート CA 証明書が PEM 形式で格納されています。espClientオブジェクトは `setCACert()` 関数を使用してサーバールートCA証明書を設定します。この設定により、ESP32 クライアントは TLS ハンドシェイク中にサーバーの身元を確認し、安全な Wi-Fi 接続を確立し、送信データの機密性と完全性を確保することができます。

```
#include <WiFiClientSecure.h>

const char* ca_cert= \
"-----BEGIN CERTIFICATE-----\n" \
"MIIDrzCCApegAwIBAgIQCDvgVpBCRrGhdWrJWZHHSjANBgkqhkiG9w0BAQUFADBh\n" \
"MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3\n" \
"d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD\n" \
"QTAeFw0wNjExMTAwMDAwMDBaFw0zMTExMTAwMDAwMDBaMGExCzAJBgNVBAYTAlVT\n" \
"MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j\n" \
"b20xIDAeBgNVBAMTF0RpZ2lDZXJ0IEdsb2JhbCBSb290IENBMIIBIjANBgkqhkiG\n" \
"9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4jvhEXLeqKTTo1eqUKKPC3eQyaKl7hLOllsB\n" \
"CSDMAZOnTjC3U/dDxGkAV53ijSLdhwZAAIEJzs4bg7/fzTtxRuLWZscFs3YnFo97\n" \
"nh6Vfe63SKMI2tavegw5BmV/Sl0fvBf4q77uKNd0f3p4mVmFaG5cIzJLv07A6Fpt\n" \
"43C/dxC//AH2hdmoRBBYMql1GNXRor5H4idq9Joz+EkIYIvUX7Q6hL+hqkpMfT7P\n" \
"T19sdl6gSzeRntwi5m3OFBqOasv+zbMUZBfHWymeMr/y7vrTC0LUq7dBMtoM1O/4\n" \
"gdW7jVg/tRvoSSiicNoxBN33shbyTApOB6jtSj1etX+jkMOvJwIDAQABo2MwYTAO\n" \
"BgNVHQ8BAf8EBAMCAYYwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUA95QNVbR\n" \
"TLtm8KPiGxvDl7I90VUwHwYDVR0jBBgwFoAUA95QNVbRTLtm8KPiGxvDl7I90VUw\n" \
"DQYJKoZIhvcNAQEFBQADggEBAMucN6pIExIK+t1EnE9SsPTfrgT1eXkIoyQY/Esr\n" \
"hMAtudXH/vTBH1jLuG2cenTnmCmrEbXjcKChzUyImZOMkXDiqw8cvpOp/2PV5Adg\n" \
"06O/nVsJ8dWO41P0jmP6P6fbtGbfYmbW0W5BjfIttep3Sp+dWOIrWcBAI+0tKIJF\n" \
"PnlUkiaY4IBIqDfv8NZ5YBberOgOzW6sRBc4L0na4UU+Krk2U886UAb3LujEV0ls\n" \
"YSEY1QSteDwsOoBrp+uvFRTp2InBuThs4pFsiv9kuXclVzDAGySj4dzp30d8tbQk\n" \
"CAUw7C29C79Fv1C5qfPrmAESrciIxpg0X40KPMbp1ZWVbd4=" \
"-----END CERTIFICATE-----\n";

// init wifi secure client
WiFiClientSecure espClient;

espClient.setCACert(ca_cert);
```

完全なTLS接続コードは[GitHub](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-ESP32/esp32_connect_mqtt_via_tls.ino)で公開されている。

### メッセージの公開と購読

MQTT ブローカーへの接続が正常に確立されると、ESP32 はトピック `emqx/esp32` にメッセージをパブリッシュし、トピック `emqx/esp32` にサブスクライブします。

```
// publish and subscribe
client.publish(topic, "Hi, I'm ESP32 ^^");
client.subscribe(topic);
```

### MQTTメッセージの受信

トピック名をシリアルポートに表示し、 `emqx/esp32` トピックから受信したメッセージを表示するコールバック関数を設定する。

```
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

### フルコード

完全なコードは以下の通り：

```
#include <WiFi.h>
#include <PubSubClient.h>

// WiFi
const char *ssid = "xxxxx"; // Enter your Wi-Fi name
const char *password = "xxxxx";  // Enter Wi-Fi password

// MQTT Broker
const char *mqtt_broker = "broker.emqx.io";
const char *topic = "emqx/esp32";
const char *mqtt_username = "emqx";
const char *mqtt_password = "public";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
    // Set software serial baud to 115200;
    Serial.begin(115200);
    // Connecting to a WiFi network
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi..");
    }
    Serial.println("Connected to the Wi-Fi network");
    //connecting to a mqtt broker
    client.setServer(mqtt_broker, mqtt_port);
    client.setCallback(callback);
    while (!client.connected()) {
        String client_id = "esp32-client-";
        client_id += String(WiFi.macAddress());
        Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
        if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Public EMQX MQTT broker connected");
        } else {
            Serial.print("failed with state ");
            Serial.print(client.state());
            delay(2000);
        }
    }
    // Publish and subscribe
    client.publish(topic, "Hi, I'm ESP32 ^^");
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

##  運行とテスト

1. 以下の手順に従って、Arduinoを使って完全なコードをアップロードし、ESP32の電源を入れてください：

   1. USBケーブルを使ってESP32をコンピュータに接続する。
   2. Arduino IDEを開き、"Tools "メニューから適切なボードとポートを選択する。
   3. コード一式をコピーしてArduino IDEに貼り付ける。
   4. Upload "ボタン（またはショートカットCtrl+U）をクリックしてコードをコンパイルし、ESP32にアップロードします。
   5. エラーがないことを確認しながら、アップロード処理が終了するのを待ちます。
   6. コードがアップロードされたら、ESP32をコンピューターから取り外します。
   7. ESP32を適切な電源に接続して電源を入れます。

2. シリアルモニターを開き、ボーレートを115200に設定する。次に、シリアルモニターで出力をモニターして、ESP32の接続状態を確認します。

   ![ESP32 serial monitor](https://assets.emqx.com/images/b3092b5bc576e59e3d964020cd73598f.png)

3. MQTTX クライアントを使用して MQTT ブローカとの接続を確立し、 `Hi, I'm MQTTX` などのメッセージを ESP32 にパブリッシュします。

   *MQTTXは、macOS、Linux、Windows上で動作するエレガントなクロスプラットフォームMQTT 5.0デスクトップクライアントです。そのユーザーフレンドリーなチャットスタイルのインターフェースにより、ユーザーは簡単に複数のMQTT/MQTTS接続を作成し、MQTTメッセージをサブスクライブ/パブリッシュすることができます。*

   ![MQTTX Client](https://assets.emqx.com/images/d6af5f33eb8f550cf22705859ed9d59b.png)

4. MQTTXによって発行されたメッセージが表示されます。

   ![Messages published by MQTTX](https://assets.emqx.com/images/d192ba700151d83f7adc5376d5b4d374.png)

## 概要

この初心者向けガイドでは、ESP32でのMQTT実装の基本を説明した。ESP32開発ボードやPubSubClientライブラリなど、必要なツールをインストールした。読者は、安全なWi-Fi接続の確立、MQTTブローカーへの接続、メッセージの発行、トピックの購読をステップバイステップの手順で行うことができる。ESP32でMQTTを活用することで、ユーザーは信頼性が高く効率的なIoTアプリケーションを作成できる。

次に、MQTTガイドをチェックすることができます：EMQが提供する「[Beginner to Advanced](https://www.emqx.com/ja/mqtt-guide)」シリーズで、MQTTプロトコルの機能を学び、MQTTのより高度なアプリケーションを探求し、MQTTアプリケーションとサービス開発を始めましょう。

## リソース

- [Paho Pythonクライアントを使ってRaspberry PiでMQTTを使う方法](https://www.emqx.com/en/blog/use-mqtt-with-raspberry-pi)
- [Raspberry PiベースのMicroPython MQTTチュートリアル](https://www.emqx.com/en/blog/micro-python-mqtt-tutorial-based-on-raspberry-pi)
- [ESP8266とMQTTでLEDを遠隔制御](https://www.emqx.com/en/blog/esp8266_mqtt_led)
- [ESP8266がArduinoでMQTTブローカーに接続](https://www.emqx.com/en/blog/esp8266-connects-to-the-public-mqtt-broker)
- [NodeMCU（ESP8266）を介したMQTTクラウドサービスへのセンサーデータのアップロード](https://www.emqx.com/en/blog/upload-sensor-data-to-mqtt-cloud-service-via-nodemcu-esp8266)



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
