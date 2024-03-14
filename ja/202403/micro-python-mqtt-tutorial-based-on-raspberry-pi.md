[Raspberry Pi](https://www.raspberrypi.org/)は、イギリスのRaspberry Pi Foundationが開発したARMベースのマイコンコンピュータのマザーボードです。キーボード、マウス、ネットワークケーブルを接続するためのUSBインターフェースとイーサネットインターフェースを提供します。マザーボードにはPCの基本機能が備わっていますが、Raspberry PiにはWi-Fi、Bluetooth、多数のGPIOが統合されており、教育、家庭用エンターテインメント、IoTなどで広く利用されています。

MicroPythonは、C言語で書かれたPython 3プログラミング言語の完全なソフトウェア実装で、MCU(マイクロコントローラ)ハードウェアの上に完全なPythonコンパイラとランタイムシステムを実行するために最適化されており、サポートされているコマンドをすぐに実行できる対話式プロンプト(REPL)をユーザーに提供します。コアPythonライブラリの一部に加えて、MicroPythonにはプログラマが低レベルのハードウェアにアクセスできるモジュールが含まれており、マイコンと制約のある環境で実行するためにPython 3言語の一部の機能を最適化した実装です。

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、パブリッシュ/サブスクライブモデルに基づく軽量なIoTメッセージングプロトコルで、接続デバイスに最小限のコードと帯域幅でリアルタイムの信頼性の高いメッセージングを提供します。そのため、MQTTプロトコルはハードウェアリソースが制限されたデバイスや、帯域幅が制限されたネットワーク環境に適しているのです。そのため、MQTTプロトコルは、IoT、モバイルインターネット、スマートハードウェア、テレマティクス、電力、エネルギーなどの業界で広く利用されています。

この記事では、Raspberry PiでMicroPythonを使用して簡単な[MQTTクライアント](https://www.emqx.com/ja/mqtt-client-sdk)を記述する方法と、クライアントと[MQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)間の接続、サブスクライブ、パブリッシュの実装方法について説明します。

## 環境設定

### MicroPythonのインストール

この記事で使用するRaspberry Pi OSは、`Raspberry Pi OS with desktop (Debian version: 10, 64-bit)`です。

- Raspberry Piが使用しているOSが`Debian version: 10 (buster)`ベースの場合は、以下のコマンドでMicroPythonを直接インストールできます。

  ```shell
  sudo apt-get update
  sudo apt-get -y install micropython
  ```

  > **注記**
  >
  > インストール中に`E: Unable to locate package micropython`エラーが発生した場合は、`snap`かソースからビルドしてインストールできます。

- Raspberry PiのOSが`Debian version: 11 (bullseye)`ベースの場合は、snapを使用してMicroPythonをインストールできます。

  ```shell
  sudo apt update
  sudo apt install snapd
  sudo reboot
  sudo snap install core
  sudo snap install micropython
  ```

- ソースからMicroPythonをインストール

  詳細は、[Getting Started — MicroPython latest documentation](https://docs.micropython.org/en/latest/develop/gettingstarted.html)  のRaspberry Piのドキュメントを参照してください。

インストールが完了したら、ターミナルで`micropython`と実行し、MicroPython x.x.x (xは数字)が返されれば、インストールは成功です。

![MicroPython](https://assets.emqx.com/images/b9b6de52e3c29063df1f4d906d52e578.png)

### MQTTクライアントライブラリのインストール

MQTTサーバーに簡単に接続するために、`umqtt.simple`ライブラリをインストールする必要があります。

```shell
micropython -m upip install umqtt.simple
```

## MQTTブローカーへの接続

この記事では、EMQXが提供する[無料のパブリックMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。これは、[MQTTクラウドサービス - EMQX Cloud](https://www.emqx.com/ja/cloud)に基づいて作成されました。ブローカーのアクセス情報は次のとおりです。

- ブローカー: `broker.emqx.io`
- TCPポート: `1883`
- Websocketポート: `8083`

## サブスクライブ

任意のエディタを開き、次のコードを入力し、sub.pyファイルとして保存します。

```python
# sub.py
import time
from umqtt.simple import MQTTClient

SERVER="broker.emqx.io"
ClientID = f'raspberry-sub-{time.time_ns()}'
user = "emqx"
password = "public"
topic = "raspberry/mqtt"
msg = b'{"msg":"hello"}'

def sub(topic, msg):
    print('received message %s on topic %s' % (msg, topic))

def main(server=SERVER):
    client = MQTTClient(ClientID, server, 1883, user, password)
    client.set_callback(sub)
    client.connect()
    print('Connected to MQTT Broker "%s"' % (server))
    client.subscribe(topic)
    while True:
        if True:
            client.wait_msg()
        else:
            client.check_msg()
            time.sleep(1)

if __name__ == "__main__":
    main()
```

## パブリッシュ

任意のエディタを開き、次のコードを入力し、pub.pyファイルとして保存します。

```python
# pub.py
import time
from umqtt.simple import MQTTClient

server="broker.emqx.io"
ClientID = f'raspberry-pub-{time.time_ns()}'
user = "emqx"
password = "public"
topic = "raspberry/mqtt"
msg = b'{"msg":"hello"}'

def connect():
    print('Connected to MQTT Broker "%s"' % (server))
    client = MQTTClient(ClientID, server, 1883, user, password)
    client.connect()
    return client

def reconnect():
    print('Failed to connect to MQTT broker, Reconnecting...' % (server))
    time.sleep(5)
    client.reconnect()

try:
    client = connect()
except OSError as e:
    reconnect()

while True:
  print('send message %s on topic %s' % (msg, topic))
  client.publish(topic, msg, qos=0)
  time.sleep(1)
```

上記のコードでは、raspberry/mqttトピックにメッセージを送信するpublish()関数を呼び出しています。パラメータのQoSは、MQTTの別の特徴です。QoSの詳細については、[MQTT QoS(サービス品質)の紹介](https://www.emqx.com/ja/blog/introduction-to-mqtt-qos)をご覧ください。この例では0に設定しています。

## テスト

以下のテストは、[MQTT 5.0クライアントツール - MQTTX](https://mqttx.app/ja)を使用して実行します。

### サブスクライブのテスト

1. ターミナルを開き、MicroPythonコードを実行してメッセージを受信します。

   ```shell
   micropython sub.py
   ```

   ![micropython sub](https://assets.emqx.com/images/5aceddabb0706609862ba8f6c8436c14.png)

2. MQTTXクライアントを使用して、MQTTサーバーに接続し、`raspberry/mqtt`トピックにメッセージを送信します。

   ![MQTT client tool](https://assets.emqx.com/images/8ebd27d6b93c80dd77a44571557e8bfe.png)

3. Raspberry Piのターミナルの情報を確認すると、MQTTXのパブリッシュメッセージが正常に受信されたことがわかります。

   ![Receive MQTT messages](https://assets.emqx.com/images/30cf035b0136f7991990705ed76ec24f.png)

### パブリッシュのテスト

1. MQTTXクライアントで`raspberry/mqtt`トピックをサブスクライブします。

2. ターミナルでMicroPythonコードを実行し、メッセージをパブリッシュします。

   ```shell
   micropython pub.py
   ```

   ![Publish MQTT messages](https://assets.emqx.com/images/cdd350b4bb8e9506225f922de1e295dd.png)

3. MQTTXクライアントで、Raspberry Piから送信されたメッセージを確認します。

   ![MQTTX subscribe](https://assets.emqx.com/images/94abe428d1a1431d288630e90fd17f57.png)

## まとめ

これは、Raspberry PiでのMicroPythonの簡単なプログラミング例です。MicroPythonの`umqtt.simple`を使用して簡単なテストクライアントを実装し、クライアントとMQTTサーバー間の接続とメッセージの送受信を完了しました。MQTTの最大のメリットは、非常に少量のコードと限られた帯域幅で、接続されたリモートデバイスにリアルタイムの信頼できるメッセージングサービスを提供できることです。一方、Raspberry Piは小型で発熱が少なく、エネルギー消費が少なく、比較的汎用性の高いハードウェアモジュールです。この2つを組み合わせることで、マイコンコントローラや制約のある環境でも、より革新的なアプリケーションを開発できるようになるでしょう。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
