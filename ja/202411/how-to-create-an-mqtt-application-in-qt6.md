## はじめに

Qtは、異なるハードウェアプラットフォームやオペレーティングシステム上で動作するソフトウェアを開発するためのクロスプラットフォームのフレームワークおよびツールキットです。Qtフレームワークには豊富なライブラリとツールが含まれており、開発者はネイティブのUIとパフォーマンスを持つアプリケーションを簡単に構築できます。組み込みデバイスやIoTソフトウェアの作成に広く使用されています。

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、パブリッシュ/サブスクライブモデルに基づく軽量なIoTメッセージングプロトコルです。非常に少ないコードと帯域幅で、ネットワーク接続されたデバイスにリアルタイムで信頼性の高いメッセージングサービスを提供できます。

このブログでは、Qt6でシームレスな通信を行うためにMQTTを使用するステップバイステップのガイドを提供します。Qt MQTTモジュールをコンパイルし、それを使用して接続を確立し、トピックの購読・購読解除、メッセージのパブリッシュ、リアルタイムでのメッセージ受信を行う方法を学びます。

## Qt6プロジェクトの準備

このブログ記事では、M2チップを搭載したMacBookでQt v6.6.2を使用しました。Qtのオープンソース版は[こちら](https://www.qt.io/download-qt-installer-oss)からダウンロードしてインストールできます。

インストール前にQtアカウントを登録することをお勧めします。

Qtをインストールした後、g++とXCodeをインストールし、いくつかの環境変数を設定する必要があります。Qtの公式ドキュメントには、macOSでの設定方法が[記載されています](https://doc.qt.io/qt-6/macos.html)。

### CMakeでQt MQTTモジュールをコンパイル

Qt MQTTモジュールは、MQTTプロトコル仕様の標準準拠の実装を提供する公式のQtライブラリです。しかし、これはオープンソースのインストールには含まれておらず、ソースからコンパイルする必要があります。

まず、[GitHub](https://github.com/qt/qtmqtt)からQt MQTTのソースコードをダウンロードします。お使いのマシンにインストールされているQtのバージョンと一致するQt MQTTのバージョンを確保してください。

```shell
git clone git://code.qt.io/qt/qtmqtt.git -b 6.6.2
```

次に、QtCreatorでQt MQTTをコンパイルします。Qt6では、[**qmake**](https://doc.qt.io/qt-6/qmake-manual.html)または[**CMake**](https://doc.qt.io/qt-6/cmake-manual.html)のどちらかを使用してコードをビルドできます。このブログではCMakeを使用しました。Qt CreatorでqtmqttのCMakeLists.txtファイルを開き、プロジェクトをコンパイルします。

![Compile the Qt MQTT Module via CMake](https://assets.emqx.com/images/5fbf0fde3245d1e210a4ed460d8e9d63.png)

コンパイルが成功すると、`build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release`という新しいフォルダが作成されます。すべての静的および動的ライブラリが生成され、このフォルダ内に保存されます。

### Qt MQTTモジュールの追加

コンパイル後、使用する方法は2つあります。1つは、qtmqttをプロジェクト内のサードパーティモジュールとしてインポートする方法で、もう1つはコンパイルされたファイルをQtのインストールディレクトリに直接配置する方法です。このブログでは2番目の方法を使用します。

1. `Qt/6.6.2/macos/include/`ディレクトリに`QtMqtt`という新しいフォルダを作成します。次に、`qtmqtt/src/mqtt/`内のすべてのファイルを新しく作成したフォルダにコピーします。
2. 生成された静的および動的ライブラリをQtのインストールディレクトリにコピーします。
   1. `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release/lib`ディレクトリ内のすべてのファイルとフォルダを`Qt/6.6.2/macos/lib/`フォルダにコピーします。置き換える必要のあるファイルがある場合は、置き換えてください。
   2. `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release/lib/cmake`から`Qt6Mqtt`フォルダを`Qt/6.6.2/macos/lib/cmake`にコピーします。
   3. `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release/mkspecs/modules`から2つの`.pri`ファイルを`Qt/6.6.2/macos/mkspecs/modules`にコピーします。

> コミュニティの[*Diego Schulz*](https://stackoverflow.com/users/212380/dschulz)さんが、Qt MQTTモジュールをビルドしてインストールするためのより良い方法を提供しています。[こちら](https://stackoverflow.com/questions/68928310/build-specific-modules-in-qt6-i-e-qtmqtt/71984521#71984521)に参考として掲載しています。

## MQTTブローカーの準備

先に進む前に、通信およびテスト用の[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)を用意してください。

このガイドでは、EMQが提供する[無料のパブリックMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を利用します。これは[EMQX](https://www.emqx.com/ja/products/emqx)プラットフォーム上に構築されています。サーバーアクセスの詳細は以下のとおりです。

- ブローカー：`broker.emqx.io`
- TCPポート：**1883**
- SSL/TLSポート：**8883**
- WebSocketポート：8083
- セキュアWebSocketポート：8084

詳細については、[無料のパブリックMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)をご覧ください。

## QtでのMQTTの使用

### シンプルなQt MQTTアプリケーション

これで、Qtで[Qt MQTT](https://doc.qt.io/qt-6/qtmqtt-index.html)モジュールを使用できます。これは、その機能を示すいくつかの[サンプル](https://github.com/qt/qtmqtt/tree/6.5.1/examples/mqtt)を提供しています。

![Qt MQTT Examples](https://assets.emqx.com/images/704bc179a5718c590289d4968d501f22.png)

このブログでは、[シンプルなMQTTクライアント](https://doc.qt.io/qt-6/qtmqtt-simpleclient-example.html)のサンプルを使用して、MQTTを使用してMQTTブローカーと通信するアプリケーションを作成する方法を説明します。QtCreatorでサンプルプロジェクトを開き、このアプリケーションがどのように動作するかを見てみましょう。

先ほど`git clone git://code.qt.io/qt/qtmqtt.git -b 6.6.2`コマンドでダウンロードしたディレクトリに戻り、simpleclientのサンプルプロジェクトのディレクトリに移動します。

```shell
cd qtmqtt
cd examples/mqtt/simpleclient
```

その中の`CMakeLists.txt`ファイルを見つけます。これをQt Creatorで開き、以下のオプションでプロジェクトを構成します。

![Qt Creator](https://assets.emqx.com/images/97a2f764f0864bcfc1c4b2f6c2aa5436.png)

構成が完了したら、前の手順でQtMqttライブラリがローカル環境にインストールされているため、プログラムを正常に実行できます。

起動したグラフィカルアプリケーションで、ホストの入力ボックスに`broker.emqx.io`、ポートに`1883`を入力します。順にConnect、Subscribe、Publishボタンをクリックすると、以下のような出力が得られます。

![MQTT client is running successfully](https://assets.emqx.com/images/12927b7035e6bd273f8197a46a7f0372.png)

これで、シンプルなMQTTクライアントが正常に動作しました。

### MQTTクライアントの作成

まず、[QMqttClient](https://doc.qt.io/qt-6/qmqttclient.html)クラスを使用して[MQTTクライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)を作成します。このクラスは、一意のクライアントIDや接続先のブローカーのホスト名とポートを設定するためのプロパティを提供します。

```
// mainwindow.cppの19行目
m_client = new QMqttClient(this);
m_client->setHostname(ui->lineEditHost->text());
m_client->setPort(static_cast<quint16>(ui->spinBoxPort->value()));
```

クライアントIDは設定せず、自動的に生成されます。

次に、[QMqttClient::messageReceived](https://doc.qt.io/qt-6/qmqttclient.html#messageReceived)()に接続し、ブローカーから送信されたすべてのメッセージを受信します。

```
// mainwindow.cpp line 26
connect(m_client, &QMqttClient::messageReceived, this, [this](const QByteArray &message, const QMqttTopicName &topic) {
    const QString content = QDateTime::currentDateTime().toString()
                + " Received Topic: "_L1
                + topic.name()
                + " Message: "_L1
                + message
                + u'\n';
    ui->editLog->insertPlainText(content);
});
```

### ブローカーへの接続・切断

サンプルプログラムでは、Connect/Disconnectボタンをクリックして以下の関数をトリガーし、MQTTブローカーへの接続・切断を行います。

```
// mainwindow.cpp line 52
void MainWindow::on_buttonConnect_clicked()
{
    if (m_client->state() == QMqttClient::Disconnected) {
        ui->lineEditHost->setEnabled(false);
        ui->spinBoxPort->setEnabled(false);
        ui->buttonConnect->setText(tr("Disconnect"));
        m_client->connectToHost();
    } else {
        ui->lineEditHost->setEnabled(true);
        ui->spinBoxPort->setEnabled(true);
        ui->buttonConnect->setText(tr("Connect"));
        m_client->disconnectFromHost();
    }
}
```

ポイントは、[m_client->connectToHost()](https://doc.qt.io/qt-6/qmqttclient.html#connectToHost) / [m_client->disconnectFromHost()](https://doc.qt.io/qt-6/qmqttclient.html#disconnectFromHost)メソッドを呼び出すことで、MQTTブローカーへの接続・切断が行えることです。

### トピックの購読・購読解除

同様に、[QMqttClient::subscribe](https://doc.qt.io/qt-6/qmqttclient.html#subscribe)と[QMqttClient::unsubscribe](https://doc.qt.io/qt-6/qmqttclient.html#unsubscribe)を呼び出すことで、トピックの購読・購読解除を行えます。

```
// mainwindow.cpp line 9:
void MainWindow::on_buttonSubscribe_clicked()
{
    auto subscription = m_client->subscribe(ui->lineEditTopic->text());
    if (!subscription) {
        QMessageBox::critical(this, u"Error"_s,
                              u"Could not subscribe. Is there a valid connection?"_s);
        return;
    }
}
```

購読が正常に作成されると、MQTTブローカーはそのトピックのメッセージをクライアントにプッシュし、Qt MQTTは先ほど設定した`QMqttClient::messageReceived`コールバック関数を呼び出します。

### メッセージのパブリッシュ

[QMqttClient::publish](https://doc.qt.io/qt-6/qmqttclient.html#publish)を呼び出すことで、指定したトピックにメッセージ内容をパブリッシュできます。

```
// mainwindow.cpp line 93
void MainWindow::on_buttonPublish_clicked()
{
    if (m_client->publish(ui->lineEditTopic->text(), ui->lineEditMessage->text().toUtf8()) == -1)
        QMessageBox::critical(this, u"Error"_s, u"Could not publish message"_s);
}
```

## 完全なコード

すべてのサンプルコードは以下で見つけることができます：[Github qtmqtt/example](https://github.com/qt/qtmqtt/tree/6.5.1/examples/mqtt/simpleclient)

## Qt Creatorでの一般的なコンパイルエラー

1. `Qt6Config.cmake`または`qt6-config.cmake`を提供する「Qt6」というパッケージ構成ファイルが見つかりませんでした。

   qtmqttをQt Creatorにインポートした後、以下のエラーが発生することがあります。

   ```shell
   [cmake] CMake Error at CMakeLists.txt:14 (find_package):
   [cmake]   Could not find a package configuration file provided by "Qt6" (requested
   [cmake]   version 6.6.2) with any of the following names:
   [cmake] 
   [cmake]     Qt6Config.cmake
   [cmake]     qt6-config.cmake
   [cmake] 
   [cmake]   Add the installation prefix of "Qt6" to CMAKE_PREFIX_PATH or set "Qt6_DIR"
   [cmake]   to a directory containing one of the above files.  If "Qt6" provides a
   ```

   解決策は、デスクトップ（arm-xx）用のビルドターゲットのQtバージョンが正しいことをキット管理で確認する必要があります。

![Qt Creator](https://assets.emqx.com/images/a38f36fda228e4bb00fc4de712844a30.png)

## まとめ

このブログでは、Qt MQTTモジュールをコンパイルし、MQTTブローカーと通信するアプリケーションを作成するためのステップバイステップのガイドを提供しました。このガイドに従うことで、MQTTを活用し、Qt6でスケーラブルで効率的なIoTアプリケーションを構築するスキルを身につけることができます。

## リソース

- [Qt MQTT 6.6.2](https://doc.qt.io/qt-6/qtmqtt-index.html)
- [Linux向けのQt MQTTサンプル](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Qt)



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
