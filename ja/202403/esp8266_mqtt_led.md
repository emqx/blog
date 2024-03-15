このチュートリアルでは、ESP8266 Wi-Fiモジュールと[MQTTプロトコル](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)を活用してLEDライトの遠隔制御を実現する方法について説明します。

ESP8266は、コスト効率の良いWi-Fiモジュールで、低消費電力アプリケーション、コンパクトな設計、そしてユーザーのニーズを満たすための高い安定性を提供します。これは、完全かつ自己完結型のWi-Fiネットワーキング機能を備えており、独立して機能するか、他のホストMCUのスレーブとして機能します。

MQTTはパブリッシュ/サブスクライブメッセージングプロトコルで、2つの役割があります：パブリッシャーとサブスクライバーです。パブリッシャーはトピックにメッセージを送信し、サブスクライバーは自分が興味のあるトピックからメッセージを受け取ります。このチュートリアルでは、ESP8266をパブリッシャーとして使用してトピックにメッセージを送信し、サブスクライバーがそれを聞いてLEDライトのオン/オフ状態を遠隔で制御できるようにします。

## プロジェクトのセットアップ

### 環境の準備

このプロジェクトを始める前に、以下のハードウェアとソフトウェアを準備してください：

- ハードウェア：
  - 1 x NodeMCU ESP8266開発ボード
  - 1 x LEDライト
  - 1 x 330Ω抵抗
  - 1 x ブレッドボード
  - 数本のデュポンワイヤー
- ソフトウェア：
  - Arduino IDE
  - MQTTXクライアント（[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)）
  - EMQXが提供する[無料の公開MQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。サーバーへのアクセス情報は以下の通りです：
    - ブローカー：`broker.emqx.io`
    - TCPポート：`1883`
    - Websocketポート：`8083`

### ハードウェアの接続

LEDの長い脚（アノード）を抵抗を介してNodeMCUのD1（GPIO 5）ピンに接続し、短い脚（カソード）を直接GNDに接続します。抵抗はLEDを流れる電流を制限し、損傷を防ぐために使用します。

![Connection Diagram](https://assets.emqx.com/images/55b153f1467569d91c93dc8ce1f55643.png)

## ESP8266をMQTTサーバーに接続する

### ESP8266ボードサポートのインストール

Arduino IDEで「ファイル」>「設定」に移動し、「追加のボードマネージャーURL」に次のURLを追加します：`http://arduino.esp8266.com/stable/package_esp8266com_index.json`。次に、「ツール」>「ボード」>「ボードマネージャー」でESP8266ボードを検索し、インストールします。

### PubSubClientライブラリのインストール

MQTTサーバーに接続するために必要な`PubSubClient`ライブラリを、Arduino IDEのライブラリマネージャーを通じて`PubSubClient`を検索し、インストールします。

### LEDピンと状態の定義

ハードウェアの設定を考慮して、LEDピンを定義する必要があります。この場合、LEDに接続するためにGPIO 5（D1）ピンを使用します。

```c
#define LED 5 // GPIO 5 (D1) for LED
bool ledState = false;
```

### Wi-Fi接続の初期化

MQTTブローカーに接続する前に、まず`ESP8266WiFi`ライブラリを使用してWi-Fi接続を確立する必要があります。これは、Wi-Fiネットワークへの接続を容易にするオープンソースのWi-Fiクライアントライブラリです。

```c
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Wi-Fi設定
const char *ssid = "YOUR_WIFI_SSID";             // Wi-Fiの名前に置き換えてください
const char *password = "YOUR_WIFI_PASSWORD";   // Wi-Fiのパスワードに置き換えてください
```

### MQTTブローカー接続パラメータの設定

このチュートリアルでは、EMQXが提供する[無料の公開MQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。

```c
// MQTTブローカー設定
const char *mqtt_broker = "broker.emqx.io";  // EMQXブローカーエンドポイント
const char *mqtt_topic = "emqx/esp8266/led";  // MQTTトピック
const char *mqtt_username = "emqx";  // 認証用のMQTTユーザー名（必要な場合）
const char *mqtt_password = "public";  // 認証用のMQTTパスワード（必要な場合）
const int mqtt_port = 1883;  // MQTTポート（TCP）
```

### Wi-FiおよびMQTTクライアントの初期化

```c
WiFiClient espClient;
PubSubClient mqtt_client(espClient);
```

### Wi-Fiへの接続

```c
void connectToWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to the WiFi network");
}
```

### MQTTサーバーへの接続とトピックへのサブスクライブ

このセクションでは、MQTTサーバーに接続し、トピックをサブスクライブします。`mqtt_client.connect()`メソッドを使用してMQTTサーバーに接続し、その後`mqtt_client.subscribe()`でトピックをサブスクライブし、接続成功時にテストメッセージを公開します。

```c
void connectToMQTTBroker() {
    while (!mqtt_client.connected()) {
        String client_id = "esp8266-client-" + String(WiFi.macAddress());
        Serial.printf("Connecting to MQTT Broker as %s.....\n", client_id.c_str());
        if (mqtt_client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Connected to MQTT broker");
            mqtt_client.subscribe(mqtt_topic);
            // 接続成功時にメッセージを公開
            mqtt_client.publish(mqtt_topic, "Hi EMQX I'm ESP8266 ^^");
        } else {
            Serial.print("Failed to connect to MQTT broker, rc=");
            Serial.print(mqtt_client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}
```

### コールバック関数の記述

MQTTクライアントがメッセージを受信した際にLEDライトのオン/オフ操作を行う必要があります。`mqtt_client.setCallback()`メソッドを使用して、MQTTクライアントがメッセージを受信したときに実行されるコールバック関数を設定します。メッセージが「on」の場合はLEDを点灯し、「off」の場合は消灯します。

```c
void mqttCallback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message received on topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    String message;
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];  // *byteを文字列に変換
    }
    // 受信したメッセージに基づいてLEDを制御
    if (message == "on" && !ledState) {
        digitalWrite(LED, HIGH);  // Turn on the LED
        ledState = true;
        Serial.println("LED is turned on");
    }
    if (message == "off" && ledState) {
        digitalWrite(LED, LOW); // LEDを消灯
        ledState = false;
        Serial.println("LED is turned off");
    }
    Serial.println();
    Serial.println("-----------------------");
}
```

## フルコード

```c
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define LED 5 // GPIO 5 (D1) for LED
bool ledState = false;

// Wi-Fi設定
const char *ssid = "WIFI_SSID";             // Wi-Fiの名前に置き換えてください
const char *password = "WIFI_PASSWORD";   // Wi-Fiのパスワードに置き換えてください

// MQTTブローカー設定
const char *mqtt_broker = "broker.emqx.io";  // EMQXブローカーエンドポイント
const char *mqtt_topic = "emqx/esp8266";     // MQTTトピック
const char *mqtt_username = "emqx";  // MQTT認証用ユーザー名
const char *mqtt_password = "public";  // MQTT認証用パスワード
const int mqtt_port = 1883;  // MQTTポート（TCP）

WiFiClient espClient;
PubSubClient mqtt_client(espClient);

void connectToWiFi();

void connectToMQTTBroker();

void mqttCallback(char *topic, byte *payload, unsigned int length);

void setup() {
    Serial.begin(115200);
    connectToWiFi();
    mqtt_client.setServer(mqtt_broker, mqtt_port);
    mqtt_client.setCallback(mqttCallback);
    connectToMQTTBroker();
}

void connectToWiFi() {
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to the WiFi network");
}

void connectToMQTTBroker() {
    while (!mqtt_client.connected()) {
        String client_id = "esp8266-client-" + String(WiFi.macAddress());
        Serial.printf("Connecting to MQTT Broker as %s.....\n", client_id.c_str());
        if (mqtt_client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
            Serial.println("Connected to MQTT broker");
            mqtt_client.subscribe(mqtt_topic);
            // 接続成功時にメッセージを公開
            mqtt_client.publish(mqtt_topic, "Hi EMQX I'm ESP8266 ^^");
        } else {
            Serial.print("Failed to connect to MQTT broker, rc=");
            Serial.print(mqtt_client.state());
            Serial.println(" try again in 5 seconds");
            delay(5000);
        }
    }
}

void mqttCallback(char *topic, byte *payload, unsigned int length) {
    Serial.print("Message received on topic: ");
    Serial.println(topic);
    Serial.print("Message:");
    String message;
    for (int i = 0; i < length; i++) {
        message += (char) payload[i];  // Convert *byte to string
    }
    // 受信したメッセージに基づいてLEDを制御
    if (message == "on" && !ledState) {
        digitalWrite(LED, HIGH);  // Turn on the LED
        ledState = true;
        Serial.println("LED is turned on");
    }
    if (message == "off" && ledState) {
        digitalWrite(LED, LOW); // LEDを消灯
        ledState = false;
        Serial.println("LED is turned off");
    }
    Serial.println();
    Serial.println("-----------------------");
}

void loop() {
    if (!mqtt_client.connected()) {
        connectToMQTTBroker();
    }
    mqtt_client.loop();
}
```

## 接続とテスト

### ESP8266へのコードのアップロード

完全なコードをArduino IDEにコピーしてESP8266開発ボードにアップロードします。シリアルモニタを開いて、ボードがWi-Fiネットワークに接続し、次にMQTTサーバーに接続する様子を観察します。

![Upload Code to ESP8266](https://assets.emqx.com/images/740140a58ef90f9adb26413e159cc301.png)

### MQTTXでLEDを制御する

[MQTTX](https://mqttx.app/ja)クライアントを使用してMQTTサーバーに接続し、`emqx/esp8266/led`トピックをサブスクライブして、"on"メッセージを送信してLEDを点灯し、"off"メッセージを送信してLEDを消灯させます。

![MQTTX](https://assets.emqx.com/images/d99306b8e2735d185d94c0ca5a5132aa.png)

## まとめ

このチュートリアルでは、ESP8266とMQTTプロトコルを使用してLEDを遠隔で制御する方法について説明しました。このプロジェクトはIoTアプリケーションの氷山の一角に過ぎません。さらに多くのセンサーやアクチュエーターを追加したり、ホームオートメーションシステムに統合したりすることで、拡張することができます。

## 関連リソース

- [ArduinoでESP8266がMQTTブローカーに接続](https://www.emqx.com/ja/blog/esp8266-connects-to-the-public-mqtt-broker)
- [ESP32でのMQTT: 初心者ガイド](https://www.emqx.com/ja/blog/esp32-connects-to-the-free-public-mqtt-broker)
- [Raspberry PiでのMQTTの使用方法：Paho Pythonクライアント](https://www.emqx.com/ja/blog/use-mqtt-with-raspberry-pi)
- [Raspberry PiベースのMicroPython MQTTチュートリアル](https://www.emqx.com/ja/blog/micro-python-mqtt-tutorial-based-on-raspberry-pi)
