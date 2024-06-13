[PHP](https://www.php.net/)は、広く使われているオープンソースの多目的スクリプト言語で、HTMLに埋め込むことができ、特にWeb開発に適しています。

この記事では、PHPプロジェクトで`php-mqtt/client`クライアントライブラリを使って、[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)と[MQTTブローカー](https://github.com/emqx/emqx)間の接続、サブスクライブ、サブスクライブ解除、メッセージの受信と送信の機能を実装する方法について主に紹介します。

## MQTTクライアントライブラリの選択

この記事では、Composerで最もダウンロードされている`php-mqtt/client`ライブラリを選択しています。他のPHP-MQTTクライアントライブラリについては、[Packagist-Search MQTT](https://packagist.org/search/?query=mqtt)でご覧ください。

php-mqtt/clientの詳細なドキュメントについては、[Packagist php-mqtt/client](https://packagist.org/packages/php-mqtt/client)を参照してください。

MQTT通信はHTTPシステム外のネットワーク通信シナリオに属します。PHPの特性の制限のため、Swoole/Workermanなどのネットワーク通信用の拡張機能をPHPシステムで使用すると、より良い体験が得られます。この記事ではその使用については繰り返しません。関連するMQTTクライアントライブラリは以下の通りです：

- [workerman/mqtt](https://packagist.org/packages/workerman/mqtt)：Workermanベースの非同期MQTTクライアント。
- [simps/mqtt](https://packagist.org/packages/simps/mqtt)：PHP用の[MQTTプロトコル](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)解析とコルーチンクライアント。

## プロジェクトの初期化

### PHPバージョンの確認

このプロジェクトは開発とテストに7.4.21を使用しています。次のコマンドでPHPバージョンを確認できます。

```
php --version

PHP 7.4.21 (cli) (built: Jul 12 2021 11:52:30) ( NTS )
Copyright (c) The PHP Group
Zend Engine v3.4.0, Copyright (c) Zend Technologies
    with Zend OPcache v7.4.21, Copyright (c), by Zend Technologies
```

### Composerを使って`php-mqtt/client`をインストール

ComposerはPHPの依存関係管理ツールで、PHPプロジェクトが必要とするすべての依存関係を管理することができます。

```
composer require php-mqtt/client
```

## PHP MQTTの使用

### MQTTブローカーに接続

この記事では、EMQXが提供する[無料の公開MQTTブローカー](https://www.emqx.com/en/mqtt/public-mqtt5-broker)を使用します。これはEMQXの[MQTTクラウドサービス](https://www.emqx.com/en/cloud)上で作成されています。サーバーのアクセス情報は以下の通りです： 

- ブローカー: `broker.emqx.io`
- TCPポート: **1883**
- SSL/TLSポート: **8883**

#### Composerのオートロードファイルと`php-mqtt/client`をインポート

```
require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
```

#### MQTTブローカー接続パラメータの設定

MQTTブローカー接続アドレス、ポート、トピックを設定します。同時に、PHPの`rand`関数を呼び出して、MQTTクライアントIDをランダムに生成します。

```
$server   = 'broker.emqx.io';
$port     = 1883;
$clientId = rand(5, 15);
$username = 'emqx_user';
$password = 'public';
$clean_session = false;
$mqtt_version = MqttClient::MQTT_3_1_1;
```

#### MQTT接続機能の記述

上記のパラメータを使用して接続し、`ConnectionSettings`を通じて接続パラメータを設定します。例えば：

```
$connectionSettings = (new ConnectionSettings)
  ->setUsername($username)
  ->setPassword($password)
  ->setKeepAliveInterval(60)
  ->setLastWillTopic('emqx/test/last-will')
  ->setLastWillMessage('client disconnect')
  ->setLastWillQualityOfService(1);
```

### サブスクライブ

`emqx/test`トピックをサブスクライブするプログラムを作成し、サブスクライブに対するコールバック関数を設定して、受信したメッセージを処理します。ここではサブスクライブから得られたトピックとメッセージを出力します：

```
$mqtt->subscribe('emqx/test', function ($topic, $message) {
    printf("Received message on topic [%s]: %s\n", $topic, $message);
}, 0);
```

### パブリッシュ

ペイロードを構築し、`publish`関数を呼び出してメッセージを`emqx/test`トピックにパブリッシュします。パブリッシュ後、クライアントは受信メッセージと再送信キューを処理するためにポーリング状態に入る必要があります：

```
for ($i = 0; $i< 10; $i++) {
  $payload = array(
    'protocol' => 'tcp',
    'date' => date('Y-m-d H:i:s'),
    'url' => 'https://github.com/emqx/MQTT-Client-Examples'
  );
  $mqtt->publish(
    // topic
    'emqx/test',
    // payload
    json_encode($payload),
    // qos
    0,
    // retain
    true
  );
  printf("msg $i send\n");
  sleep(1);
}

// The client loop to process incoming messages and retransmission queues
$mqtt->loop(true);
```

### 全体のソースコード

サーバー接続、メッセージのパブリッシュ、受信のコード。

```
<?php

require('vendor/autoload.php');

use \PhpMqtt\Client\MqttClient;
use \PhpMqtt\Client\ConnectionSettings;

$server   = 'broker.emqx.io';
$port     = 1883;
$clientId = rand(5, 15);
$username = 'emqx_user';
$password = 'public';
$clean_session = false;
$mqtt_version = MqttClient::MQTT_3_1_1;

$connectionSettings = (new ConnectionSettings)
  ->setUsername($username)
  ->setPassword($password)
  ->setKeepAliveInterval(60)
  ->setLastWillTopic('emqx/test/last-will')
  ->setLastWillMessage('client disconnect')
  ->setLastWillQualityOfService(1);


$mqtt = new MqttClient($server, $port, $clientId, $mqtt_version);

$mqtt->connect($connectionSettings, $clean_session);
printf("client connected\n");

$mqtt->subscribe('emqx/test', function ($topic, $message) {
    printf("Received message on topic [%s]: %s\n", $topic, $message);
}, 0);

for ($i = 0; $i< 10; $i++) {
  $payload = array(
    'protocol' => 'tcp',
    'date' => date('Y-m-d H:i:s'),
    'url' => 'https://github.com/emqx/MQTT-Client-Examples'
  );
  $mqtt->publish(
    // topic
    'emqx/test',
    // payload
    json_encode($payload),
    // qos
    0,
    // retain
    true
  );
  printf("msg $i send\n");
  sleep(1);
}

$mqtt->loop(true);
```

## テスト

MQTTメッセージパブリッシュコードを実行すると、クライアントが正常に接続され、メッセージが順番にパブリッシュされ、正常に受信されたことが確認できます：

```
php pubsub_tcp.php
```

![PHP MQTT テスト](https://assets.emqx.com/images/61618d56823886f101feaf6741a20c3f.png))

## まとめ

これまでに、**php-mqtt/client**を使って[無料の公開MQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)に接続し、テストクライアントとMQTTサーバー間の接続、メッセージのパブリッシュ、サブスクライブを実装しました。

次に、EMQが提供する[MQTTプロトコル入門ガイド](https://www.emqx.com/en/mqtt-guide)シリーズの記事をチェックし、MQTTプロトコルの機能を学び、MQTTのより高度な応用を探求し、MQTTアプリケーションおよびサービス開発をスムーズに始めます。





<section class="promotion">
    <div>
        無料トライアルEMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">IoT向けフルマネージド型MQTTサービス</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">無料トライアル →</a>
</section>
