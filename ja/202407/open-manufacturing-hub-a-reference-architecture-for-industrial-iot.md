## はじめに

急速に進化する[産業用インターネット・オブ・シングス (IIoT)](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges)の世界では、シームレスな接続性、リアルタイムのデータ処理、効率的なシステム管理に対する需要が高まっています。産業界が相互接続されたデバイスの変革的な可能性を受け入れ続ける中、堅牢で柔軟な技術スタックの必要性が高まっています。

ここで登場するのがOMH(Open Manufacturing Hub)です。EMQが提供する[産業用IoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges)向けのオープンソース・ブループリントであり、産業用接続とリアルタイムデータの真の可能性を活用しています。この記事では、OMHソリューションを詳しく見ていき、この革新的なソリューションをどのように実装し、産業用システム開発への取り組み方を再構築するかを解説します。

## 産業用IoTのための包括的なソリューション

OMHは、強力でスケーラブルな産業用IoTアプリケーションを構築するための包括的なソリューションを提供します。これらが一体となって、シームレスなデータ接続、効率的なメッセージキューイング、時系列データの信頼性の高い保存と分析を可能にします。

OMHソリューションの目的は、製造業界の組織がスマートマニュファクチャリングの優れた実践を達成できるようにすることです。この目的には、先進的なIIoTテクノロジーとデータ駆動の洞察を活用して、製造バリューチェーン全体で運用プロセスを最適化し、生産性を向上させ、品質を確保し、イノベーションを推進することが含まれます。

### アーキテクチャの主要コンポーネント

OMHの主要コンポーネントは以下の通りです:

- Python Modbus シミュレーター: Pythonアプリケーションが Modbus シミュレーターとして機能し、Modbusデータを継続的に生成します。
- [Neuron Industrial Connectivity Server](https://www.emqx.com/ja/products/neuronex): Neuronは産業用接続のためのデバイスハブとして機能し、多様な産業用プロトコルとIIoTシステムの間のシームレスな統合を促進します。
- [EMQX MQTT Broker](https://www.emqx.com/ja/products/emqx): EMQXブローカーはIIoTインフラストラクチャの中心として機能し、アプリケーション向けの信頼性が高くスケーラブルなメッセージングシステムを提供します。
- Timescaleデータベース: Timescaleは時系列データベースであり、Pythonシミュレーターによって生成される膨大な量の時系列データを保存・分析するための理想的なソリューションを提供します。
- Grafana可視化: Grafanaは人気のオープンソースデータ可視化プラットフォームであり、Timescaleとシームレスに統合してリアルタイムおよび履歴データを可視化します。

企業は上記の技術スタックを使用することで、さまざまなメリットを得ることができます。産業プロセスを最適化し、運用効率を改善し、より良い意思決定を行うためのリアルタイムの洞察を提供します。その結果、企業は様々な業界で収益を増やし、市場投入までの時間を短縮し、運用コストを削減し、製品の品質を向上させることができます。

### アーキテクチャのワークフロー

EMQXとNeuronを使用して、効率的でスケーラブルなIIoTシステムを構築することは非常に簡単です。Python Modbus Simulatorを除く全てのソフトウェアコンポーネントは、個別のDockerコンテナで実行されます。シミュレーターはデモ用に提供されるプログラムで、データを生成するために使用されます。

Modbusシミュレーターでは、Pythonプログラムが温度と湿度のランダムなサンプル値2つを生成し、それぞれModbusレジスタ400001と400002に格納します。産業用接続サーバーであるNeuronは、これら2つのModbusレジスタに1秒間隔で定期的にアクセスするように設定されています。次に、NeuronはModbusレジスタからのデータをMQTTメッセージに変換し、EMQXブローカーに公開します。

MQTTブローカーであるEMQXは、着信データを効率的に処理し、ルールエンジンを介してTimescaleDBデータベースに転送します。温度と湿度の値を表すデータは、時系列データ保存用に最適化されたTimescaleDBデータベースに取り込まれます。

最後に、データ可視化プラットフォームであるGrafanaがTimescaleDBから時系列データを取得し、それを使用してダイナミックな可視化とリアルタイムの洞察を生成します。ユーザーはGrafanaのカスタマイズ可能なダッシュボードを通じて、温度と湿度のデータを直感的でユーザーフレンドリーな方法で監視・分析できます。

![Slice 165.png](https://assets.emqx.com/images/de25914cb83c9fd7918865d1f2cc85ae.png)

## デモ: 効率的でスケーラブルなIIoTシステムの構築

以下は、インフラストラクチャで述べたすべてのアプリケーションのシンプルなセットアップ手順です。インストールの複雑さを簡素化するために、Dockerテクノロジーを使用します。

### デモセットアップの前提条件

1. Dockerのセットアップ: Dockerのウェブサイト ([https://www.docker.com](https://www.docker.com/)) にアクセスし、適切なバージョンのDockerをダウンロードします。
2. Python3のセットアップ: 公式のPythonウェブサイト [Download Python](https://www.python.org/downloads/)  にアクセスします。ダウンロードページには、Pythonの最新の安定版リリースが掲載されています。

### Docker Composeのインストール

Neuron、EMQX、Timescale、Grafanaをインストールするための docker compose ファイル docker_compose.yml を用意します。

```yaml
version: '3.4'

services:

  neuron:
    image: emqx/neuron:2.4.8
    ports:
      - "7000:7000"
      - "7001:7001"
    container_name: neuron
    hostname: neuron
    volumes:
      - nng-ipc:/tmp

  emqx:
    image: emqx/emqx-ee:4.4.18
    ports:
      - "1883:1883"
      - "18083:18083"
    container_name: emqx
    hostname: emqx

  timescaledb:
    image: timescale/timescaledb-ha:pg14-latest
    restart: always
    ports:
      - 5432:5432
    container_name: timescaledb
    hostname: timescaledb
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - /data/timescaledb:/var/lib/postgresql/data

  grafana:
    image: grafana/grafana-enterprise
    container_name: grafana
    hostname: grafana
    restart: unless-stopped
    ports:
     - 3000:3000

volumes:
  nng-ipc:
```

同じディレクトリで、以下のdockerコマンドを実行し、すべてのdockerコンポーネントを起動します:

```shell
$ sudo docker compose up -d
```

このコマンドは、docker-compose.ymlファイルで定義されたサービスをデタッチモード (バックグラウンド) で起動します。

上記のメッセージを受け取ると、dockerの環境でそれらのコンポーネントを正常に実行できたことになります。

![图片.png](https://assets.emqx.com/images/88e5d5c0304487c1a7011cc7ce29dc69.png)

docker仮想IPアドレスを取得するには、以下のコマンドを実行します:

```shell
$ ifconfig
```

注: 図では、docker仮想IPアドレスが172.17.0.1であることが示されています。このIPは、デモのセットアップ全体でホスト名パラメータに使用されます。

![ifconfig](https://assets.emqx.com/images/4f00faf95c39af43f8e00086e305e28c.png)

### Python Modbusシミュレータプログラム

シミュレーションプログラムでは、Modbusサーバーとの通信を容易にするために、pymodbusモジュールを使用しています。このPythonプログラムでは、ユーザーがデータ出力を制御し、必要に応じて自動的にデータを生成できます。以下はPythonでのサンプルコードです:

```python
#!/usr/bin/env python3

-- coding: utf-8 --

"""
Created on Thu Jun 30 09:54:56 2023

@author: Joey
"""
#!/usr/bin/env python
from pymodbus.version import version
from pymodbus.server import StartTcpServer
from pymodbus.server import StartTlsServer
from pymodbus.server import StartUdpServer
from pymodbus.server import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer
import time
from threading import Thread
import random
---------------------------------------------------------------------------

configure the service logging

---------------------------------------------------------------------------
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

def data_change(name,s):
    a = 0
    while True:
        data = [a]*2
        data[0] = int(280 + random.random()*30)
        data[1] = int(700 + random.random()*30)
        s.setValues(3,0,data)
        time.sleep(1)

def run_server():
    slave_context = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [0]*2))
    slaves = {}
    for i in range(1,2):
        slaves[i] = slave_context
    context = ModbusServerContext(slaves=slaves, single=False)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = '<http://github.com/riptideio/pymodbus/'>
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.5'

    t1 = Thread(target=data_change,args=("thread-1",slave_context))
    t1.start()
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 502))
    t1.join()

if name == "main":
    run_server()

```

このコードを実行する前に、以下のコマンドを実行して、pymodbusモジュールをインストールしてください:

```shell
$ pip install pymodbus
```

シミュレートされたPythonプログラムファイルを配置したディレクトリで、以下のコマンドを使用してpymodbusシミュレーターを起動します:

```shell
$ sudo python3 simu.py
```

![python3 simu.py](https://assets.emqx.com/images/41e49c3257f5eb53fad13d1df3e58b41.png?imageMogr2/thumbnail/1520x)

### Neuronセットアップガイドライン

サウスバウンドデバイスノードを作成することで、Neuronはデモ内のModbusシミュレーターなど、様々なデバイスにアクセスできるようになります。

ノースバウンドアプリケーションノードを作成することで、NeuronはMQTTブローカー(例えば、EMQX)との接続を確立し、収集したデバイスデータをEMQXにアップロードします。

**ステップ1**: ブラウザを起動し、URL `https://hostname:7000/` を入力します。

ユーザー名 "admin"、パスワード "0000" でログインします。

**ステップ2**: サウスバウンドデバイスの追加

設定メニューで、South Devicesを選択してSouth Devicesインターフェイスに入ります。Add Deviceをクリックして新しいデバイスを追加します。

![图片.png](https://assets.emqx.com/images/e14d97bf06eefb5f3136d26a2777c250.png?imageMogr2/thumbnail/1520x)

デバイスの名前を入力し、ドロップダウンボックスからプラグインModbus TCPを選択し、"Create"ボタンをクリックします。

 ![new device](https://assets.emqx.com/images/ed9a1473055c56b9750c30ae38f7261a.png?imageMogr2/thumbnail/1520x)

**ステップ3**: サウスバウンドデバイスのパラメータ設定

サウスバウンドデバイスを追加した後、以下のパラメータを入力して送信し、"Submit"ボタンをクリックします。

![device config](https://assets.emqx.com/images/9518cda52ea39ae96b669caa9ee7fce8.png?imageMogr2/thumbnail/1520x)

注: Docker仮想ネットワークのIPアドレス172.17.0.1を入力します。

**ステップ4**: デバイスカードにグループを作成する

デバイスの名前 "demo" をクリックすると、空のグループリストが表示されます。"Create" ボタンをクリックして、ダイアログボックスにグループ名と間隔を入力し、"Create" ボタンをクリックします。

![creat group](https://assets.emqx.com/images/f8a2bab1267dd7c7399c671fad90e331.png?imageMogr2/thumbnail/1520x)

**ステップ5**: グループにタグを追加します。

グループの名前 "demo_group" をクリックすると、タグリストページに入ります。"Create" ボタンをクリックしてタグポイントを作成します。最初の行のタグポイントに名前 "temperature" を、2番目の行のタグポイントに名前 "humidity" を入力します。

![tag list](https://assets.emqx.com/images/09992ffe9663e6c1cb6ca3298bf17e8d.png?imageMogr2/thumbnail/1520x)

温度と湿度のタグアドレスは、それぞれ1!40001と1!40002になります。ここで、1はステーション番号、40001と40002は温度レジスタと湿度レジスタです。

**ステップ6**: データモニタリングメニューで収集したデータを確認します。

左のナビゲーションメニューからMonitoring → Data Monitoringを選択します。South Device BoxでdemoをGroup Name Boxでdemo_groupを選択します。 温度と湿度の値は以下のように表示されるはずです:

![Data Monitoring](https://assets.emqx.com/images/f094f2e35e957b0cd3d8904cd71904cd.png?imageMogr2/thumbnail/1520x)

注: この時点で、NeuronはPythonシミュレータープログラムに正常に接続されています。値は280と700の周辺で変動します。

**ステップ7**: ノースバウンドプラグインモジュールをアプリケーションに追加します。

左側のナビゲーションメニューから Configuration → North Apps を選択します。"Add Application" ボタンをクリックします。以下のようにアプリケーション名 "demo_app" とMQTTプラグインを入力します:

 ![add app](https://assets.emqx.com/images/c8633caed1263e9390ceb0e00305ccd8.png?imageMogr2/thumbnail/1520x)

**ステップ8**: ノースバウンドアプリケーションのパラメータを設定します。

MQTTアプリケーションのパラメータリストが表示されます。Broker Hostにdocker仮想IPアドレス "172.17.0.1" を入力します。他のパラメータは変更せずそのままにします。 入力が完了したら、"Submit" ボタンをクリックしてパラメータを送信します。

![app config](https://assets.emqx.com/images/8233015dea9de752a86dfb2626628eaf.png?imageMogr2/thumbnail/1520x)

**ステップ9**: サウスバウンドポイントグループのサブスクライブ

"demo_app" の名前をクリックすると、グループリストサブスクリプションページに入ります。"Add Subscription" ボタンをクリックします。South Device BoxでdemoをGroup Boxでdemo_groupを選択します。表示されているようにデフォルトのトピックを使用し、"Submit" ボタンをクリックします。

![add subscription](https://assets.emqx.com/images/696d0a25e3cac242f0d0b42e25030ea3.png?imageMogr2/thumbnail/1520x)

**ステップ10**: [MQTTX](https://mqttx.app/)でMQTT接続を確認する。

Windowsプラットフォームで MQTTX を起動します。メインページの "New Connection" をクリックします。設定パラメータを入力し、右上の "Connect" をクリックします。

Add Subscriptionをクリックし、トピックはステップ9と同じにする必要があります。例えば、"/neuron/demo_app/demo/demo_group" と入力します。サブスクリプションが成功すると、MQTTXがNeuronによって収集・報告されたデータを継続的に受信していることがわかります。以下の図のように表示されます。

![MQTTX](https://assets.emqx.com/images/c8ec42b6605df52ba1f98f6edbd9ecf5.png?imageMogr2/thumbnail/1520x)

MQTTXがEMQXブローカーからサブスクライブしたメッセージを継続的に表示する場合、NeuronがデバイスデータメッセージをEMQXブローカーに継続的に公開していることを示しています。

> 注: ここでは、強力なクロスプラットフォームのMQTTクライアントツールである[MQTTX](https://mqttx.app/)を使用しています。公式サイト [MQTTX Download](https://mqttx.app/downloads)  からダウンロードできます。

### Timescaleデータベースのセットアップ手順

EMQXブローカーがそのデータベースにデータを取り込む前に、Timescaleデータベースでデータベースとテーブルを作成する必要があります。

**ステップ1**: dockerでpsqlコマンドラインツールを実行し、timescaleデータベースをセットアップします。

```shell
$ sudo docker exec -it timescaledb psql -U postgres  
```

**ステップ2**: timescaleにデータベース "demo" を作成する

コマンドプロンプトで、"Create database demo;" と入力して、demoデータベースを作成します。作成に成功したら、データベースに接続し、以下のように拡張機能を作成します:

![Create database demo](https://assets.emqx.com/images/0912f030c34f66992cb43635165481c2.png?imageMogr2/thumbnail/1520x)

**ステップ3**: データベース "demo" にテーブル "conditions" を作成する

ここで、"time"、"temperature"、"humidity" のフィールドを持つテーブル "conditions" を以下のように作成する必要があります:

![create table](https://assets.emqx.com/images/7e2a9646101846ee522a8fbc81cb8605.png?imageMogr2/thumbnail/1520x)

**ステップ4**: テーブル "conditions" を確認する

最後に、コマンド "\dt" を使用して "conditions" テーブルを確認するだけです:

![テーブル "conditions" を確認する](https://assets.emqx.com/images/70b4eca2c7b72581235fde5615832740.png?imageMogr2/thumbnail/1520x)

### EMQXでのTimescaleデータベースへのデータ取り込みのセットアップ

データベースの作成プロセスが終了したら、EMQXはTimescaleデータベースに接続できるようになります。以下の手順に従って、必要なパラメータとSQL文を設定してください。

**ステップ1**: ブラウザを起動し、URL `http://hostname:18083/` を入力します。

ユーザー名 "admin"、パスワード "public" でログインします。

注: 初回ログイン時にはパスワード変更を求められます。

**ステップ2**: Rule Engineでtimescaleにデータを取り込むためのルールを作成します。

EMQXダッシュボードで、左側のメニューバーの "Rules" タブを選択します。"Create" ボタンをクリックして、以下のようにSQLボックスでルールを作成します:

![create rules](https://assets.emqx.com/images/1da0d51d5743afffb18d07ded50347ec.png?imageMogr2/thumbnail/1520x)

**ステップ3**: ルールのアクションを追加する

SQLが正常に実行されると、ルールがアクションをトリガーします。Rule Engineの下部にある "Add action" ボタンをクリックします。アクションタイプで "Data persist" と "Data to Timescale" を選択します。

![add action](https://assets.emqx.com/images/732c7c0e0896cc5d577c280a7eb1eee7.png?imageMogr2/thumbnail/1520x)

**ステップ4**: ルールアクションにリソースを追加する

上記のアクション画面の "Use of resources" 付近にある "Create" リンクをクリックします。以下のようなリソース画面が表示されます。サーバーIP "172.17.0.1"、データベース "demo"、ユーザー "postgres"、パスワード "password" を入力し、"Confirm" ボタンをクリックしてCreate Rules画面に戻ります。

![add resource](https://assets.emqx.com/images/11c882997487ff9b29d074fe2ce79bd1.png?imageMogr2/thumbnail/1520x)

**ステップ5**: データを取り込むためのSQLステートメントを追加する

最後に、SQLテンプレートに入力します。この例では、Timescaleにデータを1つ挿入します。SQLテンプレートは以下の通りです。入力が完了したら、"Confirm" ボタンをクリックします。

![edit action](https://assets.emqx.com/images/458fe2e1ac24e0c13e563d5b6cb71f10.png?imageMogr2/thumbnail/1520x)

> 注: データを挿入する前に、SQLテンプレート内の ${temperature} と ${humidity} のプレースホルダーは、対応する値に置き換えられます。

**ステップ6**: Timescaleデータベース内のデータを確認する。

以下のSELECT文をデータベース demo に入力します。いくつかのデータ行がすでにあるはずです。これで、温度と湿度のデータがTimescaleデータベースに正常に保存されました。

![Check out the data in Timescale database.](https://assets.emqx.com/images/7d0a7097afdbff368131c9dca0e0cb4a.png?imageMogr2/thumbnail/1520x)

### GrafanaでのTimescaleデータベースからのデータ取得のセットアップ

Grafanaアプリケーションは、温度と湿度の測定値の可視化を提供するために、Timescaleデータベースへの接続をセットアップします。以下の手順に従って、可視化をセットアップしてください。

**ステップ1**: ブラウザを起動し、URL `http://hostname:3000` を入力します。

ユーザー名 "admin"、パスワード "admin" でログインします。

注: 初回ログイン時には新しいパスワードが必要です。

**ステップ2**: データソースのセットアップ

Data Source ページから PostgreSQL データソースを選択します。Timescaleデータベース接続のHost、Database、User、Passwordを入力します。

![Setup the data sources](https://assets.emqx.com/images/defb59772405c955fb7d710b055c271c.png?imageMogr2/thumbnail/1520x)

ページの最後には以下のように表示されるはずです。

![connection ok](https://assets.emqx.com/images/b3edc6b4e7262a01788f959f86d94976.png?imageMogr2/thumbnail/1520x)

**ステップ3**: 可視化を追加する

リストからデータソース "Timescale" を選択します。以下のようにSQLクエリを作成します。Columns に "time"、"temperature"、"humidity" を入力し、降順にします。右上の "Save" ボタンをクリックして、可視化を保存します。

![Add visualization](https://assets.emqx.com/images/9efaebdd5d9e883214e7ade98177d805.png?imageMogr2/thumbnail/1520x)

**ステップ4**: 可視化のチャートを見る

これで、温度と湿度のデータが可視化チャートで表示されました。これでこのデモのセットアップは完了です。

![可視化のチャートを見る](https://assets.emqx.com/images/2dbb78690efc785fd9c232a963450ad8.png?imageMogr2/thumbnail/1520x)

## 豊富なITおよびOT接続性

上記のデモでは、単純なModbus接続とTimescaleデータベースへのアクセスを示しました。ただし、NeuronとEMQXの両方が、多様なOTおよびIT接続要件を満たすための幅広いドライバーとコネクタを提供していることに注意することが重要です。これらの広範なOTおよびIT機能は、IIoTシステムの開発を成功させるために不可欠です。これにより、ITとOTのテクノロジーをIIoTシステムに統合することができます。

![豊富なITおよびOT接続性](https://assets.emqx.com/images/f61d49ae42da46ac7b8c5eb3155d3302.png?imageMogr2/thumbnail/1520x)

### シームレスなIT接続性

EMQXブローカーは幅広いデータブリッジを提供し、40以上のクラウドサービスとエンタープライズシステムとのシームレスな統合を可能にします。これにより、カスタムブリッジ開発のコストと複雑さを削減し、さまざまなアプリケーション間でのデータへのインスタントアクセスが可能になります。EMQXは、MySQL、PostgreSQL、MongoDBなどの一般的なデータベースや、Redis、Oracle、SAP、Kafkaなどのテクノロジーとの統合をサポートしています。この豊富なコネクタセットにより、IIoTエコシステム内で効率的なIT接続とデータ交換が保証されます。

### 多様なOT接続性

Neuronはプロトコルゲートウェイとして機能し、IIoTの展開を成功させるために不可欠な包括的な産業用接続オプションを提供します。 [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication)、Ethernet/IP、Profinet I/O、OPC-UA、IEC104、[BACnet](https://www.emqx.com/en/blog/bacnet-protocol-basic-concepts-structure-obejct-model-explained)など、30以上の産業用プロトコルをサポートしているため、Neuronは運用技術(OT)の領域全体で様々なデバイスやシステムとのシームレスな通信を可能にします。PLC、ビルオートメーションシステム、CNC機械、ロボット工学など、Neuronは信頼性の高いOT接続とデータ取得を保証する強力なドライバーを提供します。

## 効率的でスケーラブルなIIoTインフラストラクチャ

上記の例では、IIoTインフラストラクチャを示すために基本的な線形トポロジを提示しました。さらに、EMQXとNeuronは、複雑なIIoTソリューションの開発において優れた柔軟性とスケーラビリティを提供します。例えば、データ取得を容易にするために、複数のNeuronデバイスを異なる場所に配置することができます。これらのデバイスの一部は、EMQXブローカーと同じサーバーにインストールすることができ、他のデバイスはリモートゲートウェイデバイスに配置することができます。反対側には、他のストレージおよび分析アプリケーションがNeuronから取得したデータを消費する中央制御室があります。

![Slice 166.png](https://assets.emqx.com/images/b6390d3ed7a2cfd0982afe6a1d91bda9.png?imageMogr2/thumbnail/1520x)

大企業では、複数の生産拠点が異なる目的を果たし、一部は垂直方向に、他は水平方向に組織されています。EMQXクラスタは、これらの生産拠点間でメッセージを複製する機能を提供し、企業全体でのシームレスなデータ共有を可能にします。EMQXは高速レプリケーションにより、あるクラスタが受信したデータが、リアルタイムまたはほぼリアルタイムで他のクラスタと同期されることを保証し、下図のように複数の生産拠点間で効率的かつタイムリーなデータ交換を促進します。

![Slice 167.png](https://assets.emqx.com/images/4feff7316033e168f8c911e4bd0b8a45.png?imageMogr2/thumbnail/1520x)

EMQXとNeuronは協調して、産業用IoTアプリケーションのための統一されたネームスペースを提供します。統一されたネームスペースとは、デバイスとアプリケーションが元の名前、場所、またはプロトコルに関係なく相互に通信できるようにする、MQTTトピックの共通の名前階層のことです。すべてのデータメッセージは、統一されたネームスペースを形成するために、コンテキスト化された構造に適切に整理されており、企業に以下のようなメリットをもたらします:

1. データアクセスの簡素化: 統一されたネームスペースにより、複数の生産拠点にまたがってデータに一貫した標準化された方法でアクセスできるようになります。従業員やシステムが様々な拠点の異なるディレクトリやファイル構造を巡回する必要がなくなり、データアクセスがより効率的でユーザーフレンドリーになります。
2. コラボレーションの改善: 統一されたネームスペースにより、異なる生産拠点の従業員やシステムが生産データを簡単に共有・協働できるようになります。リアルタイムでデータにアクセスし編集できるため、コミュニケーションの障壁が減り、コラボレーションのワークフローが合理化されます。これにより、拠点間のチームワークが促進され、生産性が向上します。
3. データ管理の強化: 統一されたネームスペースにより、データ管理の一元化が可能になり、企業全体で統一されたデータポリシーとガバナンスを実施できるようになります。データのバックアップ、復旧、セキュリティ対策が容易になり、企業全体で一貫したデータ保護の実践が保証されます。
4. IT管理の簡素化: 統一されたネームスペースの管理は通常、各生産拠点に個別の運用ドメインを維持するよりもIT管理者にとって容易です。一元化された管理と制御により、運用の合理化、ユーザー管理の簡素化、メンテナンス作業の削減につながります。
5. スケーラビリティと柔軟性: 統一されたネームスペースは、企業の拡大や進化に伴うスケーラビリティと柔軟性を提供します。大幅な修正や中断なしに、新しい生産拠点を既存のインフラストラクチャにシームレスに統合できます。このスケーラビリティは、ビジネスの成長と変化する市場の動向への適応を促進します。
6. 一貫したユーザーエクスペリエンス: 統一されたネームスペースにより、異なる生産拠点の従業員は一貫したユーザーインターフェースとワークフローを体験できます。この統一性はユーザーエクスペリエンスを向上させ、学習曲線を減らし、全体的なユーザー満足度を高めることで、効率と生産性の向上につながります。
7. データの完全性の向上: コンテキスト化されたデータは、AI/MLモデルで使用されるデータの品質を向上させることができます。追加のコンテキストとメタデータを提供することで、AI/MLモデルはデータをより良く理解・解釈でき、エラーを減らし、精度を向上させます。
8. AI/ML精密予測: また、コンテキスト化されたデータは、AI/MLモデルの予測能力を高めます。追加のコンテキストを提供することで、モデルは将来のイベントや結果についてより正確な予測を行うことができます。これは、AI/MLシステムが結果に影響を与える可能性のある要因を考慮することで、バイアスを減らすのに役立ちます。

> 統一ネームスペースの詳細: [Unified Namespace (UNS): Next-Generation Data Fabric for IIoT](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot)

## 高速データ交換

EMQXは、100万を超える同時接続とメッセージパーセカンドを処理できる、大規模な産業用IoTの展開に適しています。ソフトリアルタイムのランタイムで、メッセージ配信にサブミリ秒のレイテンシーを保証します。

高速データ交換は、異なる拠点のクラスタ間で安定した信頼性の高いデータレプリケーションをサポートしながら、接続デバイスの大量処理とセンサーデータの大量処理をほぼリアルタイムで処理できるため、非常に重要です。この機能は、テレメトリーデータ収集、機械間通信、大規模なイベント駆動型システムなど、メッセージ量の多いアプリケーションに役立ちます。

## まとめ

OMHは、協力と革新がいかに産業用IoTの未来を形作ることができるかを示す最良の例です。この記事で紹介するスタックは、信頼性が高く効果的なIIoTインフラストラクチャを構築するための新しい選択肢を提示しています。Neuronの産業用接続、EMQXの堅牢でスケーラブルなMQTTブローカー、Timescaleの高性能な時系列データベース、Grafanaの直感的な可視化機能を シームレスに統合することで、産業用システムアーキテクチャの新時代が到来しています。

デジタル時代の複雑さを乗り越えるために、産業界が取り組みを続ける中、OMHは効率性、スケーラビリティ、リアルタイムの洞察への道を開き、IIoTシステムの設計、展開、管理の方法を根本的に変革しています。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
