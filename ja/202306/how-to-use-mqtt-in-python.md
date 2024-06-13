## はじめに

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)は、[パブリッシュ／サブスクライブモデル](https://www.emqx.com/en/blog/mqtt-5-introduction-to-publish-subscribe-model)のIoT向け軽量メッセージングプロトコルで、最小限のコードと帯域幅で信頼性の高いリアルタイム通信を実現します。特に、リソースが限られている機器や帯域幅の小さいネットワークに有効で、IoT、モバイルインターネット、IoV、電力業界などで広く採用されています。

Pythonは、その汎用性、使いやすさ、膨大なライブラリから、IoTで広く利用されています。大量のデータを扱うことができるため、スマートホームオートメーション、環境モニタリング、産業制御などに最適です。また、Pythonはマイクロコントローラと互換性があるため、IoTデバイスの開発にも有効なツールとなっています。

本記事では、主にPythonプロジェクトにおいて、paho-mqttクライアントを使用し、[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)と[MQTTブローカー](https://github.com/emqx/emqx)間の接続、購読、メッセージングなどの機能を実装する方法について紹介します。

## Paho MQTT Python Clientを選択する理由は？

[Paho Python Client](https://github.com/eclipse/paho.mqtt.python)は、Python 2.7または3.x上でMQTT v5.0, MQTT v3.1.1, v3.1をサポートするクライアントクラスです。また、MQTTサーバに単発メッセージを非常に簡単に発行するためのヘルパー関数も提供しています。

Pythonコミュニティで最も人気のあるMQTTクライアントライブラリとして、Paho MQTT Python Clientは以下の利点を備えています：

1. オープンソースで、コミュニティでサポートされています。
2. MQTTサーバーへの接続やMQTTメッセージの発行・購読を行うための使いやすいAPIです。
3. さまざまなセキュリティ機構に対応。
4. 急速に進化するIoTの状況に対応するため、積極的に開発・維持する。

もっとPython MQTTクライアントライブラリを調べたいですか？[Python MQTTクライアントに関するこの比較ブログ](https://www.emqx.com/en/blog/comparision-of-python-mqtt-client)記事をチェックしてください。

## Python MQTT プロジェクトの準備

###  パイソンバージョン

このプロジェクトは、Python 3.6を使用して開発およびテストされています。正しいバージョンのPythonがインストールされているかどうかを確認するには、次のコマンドを使用します。

```
$ python3 --version             
Python 3.6.7
```

### Paho MQTTクライアントをインストールする

Pipでpaho-mqttライブラリをインストールします。

```
pip3 install paho-mqtt
```

> *Pip のインストールにヘルプが必要な場合は、*[https://pip.pypa.io/en/stable/installation/](https://pip.pypa.io/en/stable/installation/)  *の公式ドキュメントを参照してください。この資料では、さまざまなOSや環境にPipをインストールするための詳細な手順を説明しています。*

## MQTTブローカーを用意する

先に進む前に、通信とテストを行うためのMQTTブローカーがあることを確認してください。MQTTブローカーを入手するには、いくつかのオプションがあります：

-  **プライベート展開**

  [EMQX](https://github.com/emqx/emqx)は、IoT、IIoT、コネクテッドカー向けの最もスケーラブルなオープンソースのMQTTブローカーです。以下のDockerコマンドを実行することでEMQXをインストールすることができます。

  ```
  docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx
  ```

-  **フルマネージドクラウドサービス**

  フルマネージドクラウドサービスは、MQTTサービスを開始するための最も簡単な方法です。[EMQX Cloud](https://www.emqx.com/en/cloud)を利用すれば、わずか数分でサービスを開始でき、AWS、Google Cloud、Microsoft Azureの20以上のリージョンでMQTTサービスを実行し、グローバルな可用性と高速接続を確保することが可能です。

  最新版の[EMQX Cloud Serverless](https://www.emqx.com/en/cloud/serverless-mqtt)は、開発者が数秒で簡単にMQTTの導入を開始できるように、永久無料の1Mセッション分/月の無償提供をしています。

-  **無料試用できるMQTTブローカー**

  無料公開MQTTブローカーは、MQTTプロトコルの学習とテストを希望する人だけが利用できます。セキュリティリスクやダウンタイムの懸念があるため、本番環境での使用は避けることが重要です。

このブログ記事では、 `broker.emqx.io` の無料公開MQTTブローカーを使用することにします。

>  ***MQTTブローカー情報***
>
>  *サーバー：* `broker.emqx.io` 
>
>  *TCPポート：* `1883` 
>
>  *WebSocketポート：* `8083` 
>
>  *SSL/TLSポート：* `8883` 
>
> *セキュアWebSocketポート：* `8084` 

詳しくは、こちらをご確認ください：[無料試用できるMQTTブローカー](https://www.emqx.com/en/mqtt/public-mqtt5-broker)

## Paho MQTT Pythonクライアントの使用方法について

### Paho MQTTクライアントをインポートする

```
from paho.mqtt import client as mqtt_client
```

### MQTTコネクションの作成

#### TCPコネクション

MQTT接続のブローカーアドレス、ポート、トピックを指定する必要があります。さらに、Python の random.randint 関数を使用して、接続用のランダムなクライアント ID を生成することができます。

```
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'
```

> *詳しくは、ブログ「*[*MQTT接続の確立時にパラメータを設定する方法*](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)*」をご確認ください。*

次に、ブローカーに接続するための `on_connect` コールバック関数を記述する必要があります。この関数はクライアントが正常に接続した後に呼び出され、 `rc` パラメータを使って接続状態を確認することができます。通常、 `broker.emqx.io` に接続するクライアントオブジェクトも同時に作成することになります。

```
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
```

#### オートレコネット

[MQTTクライアントライブラリ](https://www.emqx.com/en/mqtt-client-sdk)の自動再接続は、不安定なネットワーク状況下でも、人手を介さずにデバイスとブローカー間の信頼性の高い通信を保証します。ネットワーク接続が中断されたり、ブローカーが一時的に利用できなくなった場合でも、クライアントがトピックの公開や購読を再開できるため、自動車システムや医療機器などの高信頼性アプリケーションに不可欠です。

Paho MQTTクライアントの自動再接続コードは、以下の通りです：

```
FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def on_disconnect(client, userdata, rc):
    logging.info("Disconnected with result code: %s", rc)
    reconnect_count, reconnect_delay = 0, FIRST_RECONNECT_DELAY
    while reconnect_count < MAX_RECONNECT_COUNT:
        logging.info("Reconnecting in %d seconds...", reconnect_delay)
        time.sleep(reconnect_delay)

        try:
            client.reconnect()
            logging.info("Reconnected successfully!")
            return
        except Exception as err:
            logging.error("%s. Reconnect failed. Retrying...", err)

        reconnect_delay *= RECONNECT_RATE
        reconnect_delay = min(reconnect_delay, MAX_RECONNECT_DELAY)
        reconnect_count += 1
    logging.info("Reconnect failed after %s attempts. Exiting...", reconnect_count)
```

そして、それをクライアントオブジェクトの `on_disconnect` として設定する。

```
client.on_disconnect = on_disconnect
```

クライアント自動再接続の完全なコードは、[GitHub](https://github.com/emqx/MQTT-Client-Examples/blob/master/mqtt-client-Python3/pub_sub_tcp.py)で見ることができます。

#### TLS/SSL

MQTTでTLSを使用することで、情報の機密性と完全性を確保し、情報の漏洩や改ざんを防止することができます。TLS認証は、一方向性認証と双方向性認証に分類される。

**単一方向認証**

Paho MQTTクライアントの一方向性認証コードは以下の通りです：

```
def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.tls_set(ca_certs='./broker.emqx.io-ca.crt')
```

**双方向認証**

Paho MQTTクライアントの双方向認証コードは、以下の通りです：

```
def connect_mqtt():
    client = mqtt_client.Client(CLIENT_ID)
    client.tls_set(
        ca_certs='./server-ca.crt',
        certfile='./client.crt',
        keyfile='./client.key'
    )
```

#### メッセージ・パブリッシュ送信の関数

トピック `/python/mqtt` に1秒ごとにメッセージを送信し、5回送信したらループを抜けるwhileループを作成する。

```
 def publish(client):
     msg_count = 1
     while True:
         time.sleep(1)
         msg = f"messages: {msg_count}"
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")
         msg_count += 1
         if msg_count > 5:
             break
```

### サブスクライブ

クライアントがMQTT Brokerからメッセージを受信すると起動する、メッセージコールバック関数 `on_message` を作成します。この関数の中で、購読しているトピックの名前と受信したメッセージを表示する予定です。

```
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message
```

## Python MQTTのフルコード例

### MQTT メッセージ・パブリッシュのコード

```
# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
```

### MQTT サブスクリプションのコード

```
# python3.6

import random

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
```

## テスト

#### メッセージ・サブスクライブ

MQTT subscription script `sub.py` を実行すると、クライアントが正常に接続され、パブリッシャーがメッセージを発行するのを待ち始めたことがわかります。

```
python3 sub.py
```

![python3 sub.py](https://assets.emqx.com/images/f6fa795ecafac8e476b12018345ecf60.png) 

#### メッセージ・パブリッシュ

MQTTメッセージ発行スクリプト `pub.py` を実行すると、クライアントは正常に接続し、5つのメッセージを発行することがわかります。同時に、sub.pyも5つのメッセージを正常に受信することができます。

```
python3 pub.py
```

![Publish MQTT Messages](https://assets.emqx.com/images/cff08d70fe77b9a2391672f3816ba260.png)

## Paho MQTT Pythonクライアントに関するQ&A

### loop_stop()が実行されないとどうなるのですか？

`loop_stop()` メソッドは、MQTT クライアントのメッセージループを停止させ、停止したものとしてマークするために使用されます。このプロセスにより、クライアントの優雅なシャットダウンが保証され、メッセージ損失、接続リーク、プログラムの異常動作などの問題のリスクが軽減されます。

例えば、この記事で紹介したpub.pyの例では、 `client.loop_stop()` メソッドを削除すると、 `sub.py` スクリプトが受け取るメッセージが5つ未満になることがあります。

したがって、loop_stop()メソッドを適切に使用することは、MQTTクライアントの優雅なシャットダウンを保証し、未閉鎖の接続によって発生する可能性のある問題を防止する上で極めて重要です。

### connect_async()は何に使うのですか？

`connect_async()` は、MQTT クライアント アプリケーションが長時間の MQTT 接続を必要とするシナリオや、メイン スレッドをブロックすることなくバックグラウンドで MQTT 接続を維持する必要がある場合に便利です。その主な使用例は次のとおりです：

1. 長時間のMQTT接続： `connect_async()` は、産業用アプリケーションなど、長時間の MQTT 接続を必要とする MQTT クライアント・アプリケーションの停止や応答不能を防止します。
2. 不安定なネットワーク接続：ネットワーク接続が不確実または不安定な環境で `connect_async()` を使用すると、再試行や遅延を伴う接続を確立することにより、アプリケーションの信頼性を向上させることができます。
3. 頻繁な接続とパラメーターの変更：接続パラメータやその他の設定が頻繁に変更される場合、 `connect_async()` はアプリケーションの応答性を向上させ、スタッタを防止するのに役立ちます。
4. バックグラウンドでのMQTT接続： `connect_async()` は、アプリケーションが他のプロセスを実行している間にバックグラウンドで MQTT 接続を確立し、ユーザー体験を向上させます。

## まとめ

これまで、paho-mqttクライアントを使用して、[無料のパブリックMQTTブローカー](https://www.emqx.com/en/mqtt/public-mqtt5-broker)に接続する方法を説明してきました。接続処理を実装し、 `publish()` メソッドを使ってテストクライアントからブローカーにメッセージを送信し、 `subscribe()` メソッドを使ってブローカーからメッセージを購読することに成功しました。

次に、MQTTガイドをチェックすることができます：EMQが提供する「[Beginner to Advanced](https://www.emqx.com/en/mqtt-guide)」シリーズで、MQTTプロトコルの機能を学び、MQTTのより高度なアプリケーションを探求し、MQTTアプリケーションとサービス開発を始めましょう。



<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
