[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、[パブリッシュ／サブスクライブモデル](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model)のIoT向け軽量メッセージングプロトコルで、最小限のコードと帯域幅で信頼性の高いリアルタイム通信を実現します。特に、リソースが限られている機器や帯域幅の小さいネットワークに有効で、IoT、モバイルインターネット、IoV、電力業界などで広く採用されています。

[ラズベリー・パイ](https://www.raspberrypi.org/)は、イギリスのラズベリー・パイ財団によって開発されたARMベースの小型シングルボードコンピュータである。このボードはUSBインターフェースとイーサネットインターフェースを備えており、キーボード、マウス、ネットワークケーブルを接続することができる。このボードはPCの基本機能を持ち、ラズベリーパイはWi-Fi、Bluetooth、多数のGPIOを統合しており、教育、ファミリー・エンターテインメント、IoTなどで広く使用されている。

このプロジェクトでは、Pythonを使ってRaspberry Pi上にシンプルな[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)を書き、このクライアントと[MQTTブローカー](https://www.emqx.io/ja)間の接続、サブスクリプション、メッセージング、その他の機能を実装する。

## Raspberry Pi MQTTプロジェクトの準備

### オペレーティング・システムのインストール

Raspberry Piは、Raspberry Pi OS、Ubuntu、Kodiなど、さまざまなOSを実行できる万能ミニコンピューターだ。それぞれのOSには、独自の機能、利点、推奨アプリケーションがある。

特にRaspberry Pi OSは、Raspberry Piハードウェアとの互換性が高く、最適化されたソフトウェアやツールがプリインストールされているため、初心者に非常におすすめです。Debian LinuxをベースにRaspberry Pi専用にカスタマイズされており、プログラミング、マルチメディア、電子工作プロジェクトに使いやすいプラットフォームを提供します。

Raspberry Pi OSをインストールするには、[公式ドキュメントのインストールガイド](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system)に従うことをお勧めします。この記事では、Raspberry Pi OS with desktop (Debian version: 11)をインストールしたRaspberry Pi 4を使用します。

### Python3のインストール

Raspberry Pi上のMQTTの開発言語としてPythonを使用します。Pythonは習得しやすい構文で、膨大な種類のライブラリやチュートリアルがオンラインで利用できるため、MQTTを扱うのに最適です。

このプロジェクトはPython 3.6を使って開発されている。通常、Raspberry PiにはPython 3がプリインストールされています。しかし、Python 3がインストールされているかどうかわからない場合は、以下のコマンドで確認することができます：

```
$ python3 --version             
Python 3.6.7
```

コマンドラインが "Python 3.x.x"（"x "はバージョン番号を示す）を返した場合、Python3がRaspberry Piにインストール済みであることを意味する。インストールされていない場合は、"apt "コマンドを使ってインストールするか、[Python3のインストールガイドライン](https://wiki.python.org/moin/BeginnersGuide/Download)に従ってください。

```
sudo apt install python3
```

### Paho MQTTクライアントをインストールする

これは、Python 2.7および3.xでMQTT v5.0、v3.1.1、およびv3.1をサポートするクライアント・クラスを提供する[Paho Pythonクライアント・ライブラリ](https://github.com/eclipse/paho.mqtt.python)を使用します。さらに、Paho Pythonクライアント・ライブラリには、MQTTサーバーへの単発メッセージの発行を非常に簡単にする便利なヘルパー関数が含まれています。

**ソースコードを使ってインストールする**

```
git clone https://github.com/eclipse/paho.mqtt.python 
cd paho.mqtt.python 
python3 setup.py install
```

 **pip3を使ってインストールする**

```
pip3 install paho-mqtt
```

## MQTTブローカーを構築

先に進む前に、通信とテストを行うためのMQTTブローカーがあることを確認してください。MQTTブローカーを入手するには、いくつかのオプションがあります：

- **プライベート展開**

  EMQXは、IoT、IIoT、コネクテッドカー向けの最もスケーラブルなオープンソースのMQTTブローカーです。以下のDockerコマンドを実行することでEMQXをインストールすることができます。

  ```
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  ```

- **フルマネージドクラウドサービス**

  フルマネージドクラウドサービスは、MQTTサービスを開始するための最も簡単な方法です。EMQX Cloudを利用すれば、わずか数分でサービスを開始でき、AWS、Google Cloud、Microsoft Azureの20以上のリージョンでMQTTサービスを実行し、グローバルな可用性と高速接続を確保することが可能です。

  最新版のEMQX Cloud Serverlessは、開発者が数秒で簡単にMQTTの導入を開始できるように、永久無料の1Mセッション分/月の無償提供をしています。

- **無料公開のMQTTブローカー**

  無料公開MQTTブローカーは、MQTTプロトコルの学習とテストを希望する人だけが利用できます。セキュリティリスクやダウンタイムの懸念があるため、本番環境での使用は避けることが重要です。

このブログ記事では、 broker.emqx.io の無料公開MQTTブローカーを使用します。

> ***MQTT Broker Info***
>
> ***Server: broker.emqx.io***
>
> ***TCP Port: 1883***
>
> ***WebSocket Port: 8083***
>
> ***SSL/TLS Port: 8883***
>
> ***Secure WebSocket Port: 8084***

詳しくは、こちらをご確認ください：無料公開のMQTTブローカー。

## MQTTのクイックスタート

### MQTTコネクションの作成

 **コネクトのコード例**

```
# test_connect.py 
import paho.mqtt.client as mqtt 

# The callback function. It will be triggered when trying to connect to the MQTT broker
# client is the client instance connected this time
# userdata is users' information, usually empty. If it is needed, you can set it through user_data_set function.
# flags save the dictionary of broker response flag.
# rc is the response code.
# Generally, we only need to pay attention to whether the response code is 0.
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

client = mqtt.Client() 
client.on_connect = on_connect 
client.connect("broker.emqx.io", 1883, 60) 
client.loop_forever()
```

上記のコードを "test_connect.py "というファイル名で保存します。ファイルを実行するには、Raspberry Piでターミナルを開き、ファイルのあるディレクトリに移動します。そして以下のコマンドを入力してスクリプトを実行します。これでMQTTクライアントが起動し、MQTTブローカーに接続します。

```
python3 test_connect.py
```

`on_connect` 関数では、MQTTブローカーが返すレスポンスコードをチェックする。レスポンスコードが `0` の場合、"Connected success" と表示し、接続に成功したことを示します。しかし、レスポンス・コードが `not 0` の場合は、以下のレスポンス・コード表に基づき、その意味を確認する必要がある。

```
0: connection succeeded
1: connection failed - incorrect protocol version
2: connection failed - invalid client identifier
3: connection failed - the broker is not available
4: connection failed - wrong username or password
5: connection failed - unauthorized
6-255: undefined
If it is other issues, you can check the network situation, or check whether `paho-mqtt` has been installed.
```

### サブスクライブ

MQTTプロトコルは、トピックに基づいてメッセージをルーティングする。サブスクライバは、ブローカに興味のあるトピックをサブスクライブすることができる。パブリッシャーが特定のトピックにメッセージを送信すると、ブローカーはそのトピックを購読している全ての購読者にそのメッセージを転送します。

テキストエディタを開き、以下のコードを入力してください。ファイルを "subscriber.py "として保存します。

```
# subscriber.py
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe, which need to put into on_connect
    # If reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
    client.subscribe("raspberry/topic")

# The callback function, it will be triggered when receiving messages
def on_message(client, userdata, msg):
    print(f"{msg.topic} {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
client.will_set('raspberry/status', b'{"status": "Off"}')

# Create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
client.connect("broker.emqx.io", 1883, 60)

# Set the network loop blocking, it will not actively end the program before calling disconnect() or the program crash
client.loop_forever()
```

`subscribe()` 関数を使うと、Raspberry Piが特定のトピックを購読できるようになります。上のコードでは、この関数を使って `raspberry/topic` というトピックを購読し、メッセージの着信を監視しています。

さらに、 `will_set()` 機能を利用して、[ウィル・メッセージ](https://www.emqx.com/en/blog/use-of-mqtt-will-message)を設定する。MQTTのこの機能により、デバイスが意図せず電源オフになってしまった場合に、指定したトピックにメッセージを送信することができます。この機能を使用することで、Raspberry Piの電源が切れたか、ネットワーク接続に問題があるかを判断することができます。

### メッセージの**パブリッシュ**

テキストエディタを開き、以下のコードを入力してください。ファイルを "publisher.py "として保存します。

```
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

    # Send a message to the raspberry/topic every 1 second, 5 times in a row
    for i in range(5):
        # The four parameters are topic, sending content, QoS and whether retaining the message respectively
        client.publish('raspberry/topic', payload=i, qos=0, retain=False)
        print(f"send {i} to raspberry/topic")

client = mqtt.Client()
client.on_connect = on_connect
client.connect("broker.emqx.io", 1883, 60)

client.loop_forever()
```

`publish()` 関数を使うと、特定のトピックにメッセージを送ることができます。上のコード例では、この関数を使用してトピック `raspberry/topic` にメッセージを送信しています。QoS パラメータは、メッセージ配信のサービス品質を定義する MQTT のもう 1 つの機能です。QoSレベルの詳細については、「[Introduction to MQTT QoS 0, 1, 2](https://www.emqx.com/en/blog/introduction-to-mqtt-qos)」を参照してください。

> *Pahoクライアントの使い方については、ブログ「*[*Pahoクライアントを使ってPythonでMQTTを使う方法*](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)*」をご覧ください。*

## テスト

以下のテストでは、MQTTX を使用する。MQTTX は、macOS、Linux、Windows で動作するエレガントなクロスプラットフォーム MQTT 5.0 デスクトップ・クライアントである。そのユーザーフレンドリーなチャットスタイルのインターフェースにより、ユーザーは簡単に複数のMQTT/MQTTS接続を作成し、MQTTメッセージをサブスクライブ/パブリッシュすることができる。

### サブスクライブ

1. MQTT subscription スクリプト `subscriber.py` を実行すると、クライアントは正常に接続し、パブリッシャーがメッセージを発行するのを待ち始めます。

   ```
   python3 subscriber.py
   ```

   ![python3 subscriberpy](https://assets.emqx.com/images/39d734d2935a8ea39980c386064c6189.png)

2. MQTTXをパブリッシャーとして "raspberry/topic "にメッセージをパブリッシュする。

   ![MQTTX](https://assets.emqx.com/images/cc93d1c6d99f3bfa3a78d8472a6209af.jpg)

3. MQTTXによって発行されたメッセージが表示されます。

   ![Messages published by MQTTX](https://assets.emqx.com/images/2b4b3eb61401434ff02d35ef94c5acc9.png)


### メッセージのパブリッシュ

1. MQTTXクライアント内で `raspberry/topic` をサブスクライブする。

2. ターミナルで `publish.py` を実行する。

   ![python3 publishpy](https://assets.emqx.com/images/8efd674aff8e58b465bed00bbade388c.png)

3. MQTTXクライアントでは、Raspberry Piからパブリッシュされたメッセージを見ることができます。

   ![MQTTX publish message](https://assets.emqx.com/images/07ffb81c764145100b1e21572357c675.jpg)


### ウィル・メッセージのテスト

次に、ウィル・メッセージが正常にセットされたかどうかをテストする。

1. MQTTXクライアントで `raspberry/status` をサブスクライブする。

   ![subscribe to mqtt topic in the MQTTX](https://assets.emqx.com/images/c704c8b0f7117079306d16b5af8c2557.jpg)

2. プログラムを中断したり、Raspberry Piのネットワークを切断する。

3. MQTTXクライアントで、 `raspberry/status` が受信したメッセージを表示する。

   ![receive mqtt message](https://assets.emqx.com/images/048da27682c9a86c536f85ffd6417bf2.jpg)


## Raspberry Pi MQTTアドバンスド

### Raspberry Piのシリアルデータを読む

提供されているコードは、Raspberry Piとのシリアル接続を確立し、シリアルポートからデータを読み取り、MQTTブローカーにパブリッシュします。 `serial` ライブラリを使用してシリアルポートの設定とデータの読み込みを行い、 `paho.mqtt.client` ライブラリを使用して MQTT ブローカーに接続してデータをパブリッシュします。コードはループ内でシリアルデータを読み取り、指定されたMQTTトピックにパブリッシュし、定義された反復回数だけこのプロセスを繰り返します。最後に、MQTT ブローカーとの接続を切断し、シリアル接続を閉じます。

```
import time

import paho.mqtt.client as mqtt
import serial


# Establishing the connection with the serial port
ser = serial.Serial(
    # Serial Port to read the data from
    port='/dev/ttyAMA0', # Use `dmesg | grep tty` to find the port
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

broker_address = "broker.emqx.io"
broker_port = 1883
topic = "emqx/serial/read"

client = mqtt.Client()
client.connect(broker_address, broker_port)

# Read data from serial port and publish it to MQTT broker
for i in range(10):
    data = ser.readline().decode()
    client.publish(topic, data)
    print("Read data {data} from serial port and publish it to MQTT broker".format(data=data))
    time.sleep(1)


client.disconnect()

ser.close()
```

### Raspberry Piのシリアルデータを書き込む

提供されたコードは、Raspberry Piとのシリアル接続を確立し、MQTTメッセージをリッスンする。メッセージを受信すると、シリアル・ポートに書き込まれる。このコードでは、 `serial` ライブラリを使用してシリアルポートの設定とデータの書き込みを行い、 `paho.mqtt.client` ライブラリを使用して MQTT ブローカーへの接続、MQTT メッセージの受信処理、シリアルポートへのデータのパブリッシュを行っています。MQTT クライアントは、特定の MQTT トピックをサブスクライブする `on_connect` や、受信メッセージを処理する `on_message` など、必要なコールバックでセットアップされます。接続されると、コードは無限ループに入り、継続的に MQTT メッセージをリッスンし、シリアル・ポートに書き込みます。

```
import paho.mqtt.client as mqtt
import serial


# Establishing the connection with the serial port
ser = serial.Serial(
    # Serial Port to read the data from
    port='/dev/ttyAMA0', # Use `dmesg | grep tty` to find the port
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

broker_address = "broker.emqx.io"
broker_port = 1883
topic = "emqx/serial/write"


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)


def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("Received message: {payload} on topic {topic}".format(payload=payload, topic=msg.topic))
    # Write data to serial port
    ser.write(payload.encode())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port)
client.loop_forever()
```

## まとめ

このブログでは、Python MQTT クライアント・ライブラリ `paho-mqtt` を使って、Raspberry Pi 上でクライアントを書き、テストします。クライアントとMQTTブローカー間の接続、サブスクリプション、メッセージング、その他の機能を実装しました。

ここまでの進歩は素晴らしい！MQTTを使って多くのエキサイティングなアプリケーションを構築するための基本を学ぶことができました。例えば

1. 携帯電話からMQTTメッセージを使ってRaspberry Piを遠隔操作できます。

2. Raspberry PiからMQTTブローカーに定期的にデバイスデータを送信することで、携帯電話のメッセージを継続的に監視し、受信することができます。

3. Raspberry PiがMQTTブローカーにアクセスし、様々なセンサーやESPモジュールを使用することで、数多くの興味深いIoTアプリケーションを作成することができる。


次に、MQTTガイドをチェックすることができます：EMQが提供する「[Beginner to Advanced](https://www.emqx.com/en/mqtt-guide)」シリーズで、MQTTプロトコルの機能を学び、MQTTのより高度なアプリケーションを探求し、MQTTアプリケーションとサービス開発を始めましょう。

## リソース

- [ESP32上のMQTT：初心者ガイド](https://www.emqx.com/ja/blog/esp32-connects-to-the-free-public-mqtt-broker)
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
