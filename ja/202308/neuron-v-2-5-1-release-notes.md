産業用IoT接続サーバー「Neuron 2.5.1」が正式にリリースされた！

最新バージョンでは、サウスバウンド統合のためのデバイス・ベースのテンプレート、ModbusのUDPトランスポート・サポート、[Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication)のリード・リトライ・サポート、IEC104の高可用性マスター・スレーブ・モードなど、いくつかの新機能が追加された。さらに、5つの新しいサウスバウンド・ドライバが導入されました：Profinet IO、Mitsubishi FX、Omron FINS UDP、Panasonic Mewtocol、DLT645-1997です。

さらに、このバージョンから製品にいくつかの調整を加えた：

- 英語話ユーザー向けの[国際版](https://www.emqx.com/en/try?product=neuron)を提供します。
- eKuiperと統合されたNeuronEXは販売終了となりました。
- Modbus TCP コミュニティ・プラグインはオープンソース版では廃止されました。Modbus TCPとModbus RTUプラグインはオープンソースになりました。ユーザーは30タグまたはノード内のすべてのプロトコル・ドライバを時間制限なしで無料で体験できます。詳細はこちらをご覧ください：[時間無制限のトライアル・ライセンスでNeuron産業用IoTゲートウェイ・ソフトウェアを無料で体験](https://www.emqx.com/en/blog/experience-neuron-industrial-iot-gateway-software-for-free-with-time-unlimited-trial-license)

最新版のダウンロードはこちらから：[https://www.emqx.com/ja/try?product=neuron](https://www.emqx.com/ja/try?product=neuron).

##  新機能の概要

###  デバイスベースのテンプレート

この機能は、同じようなコンフィギュレーションを持つ多数のデバイスをセットアップする必要があるシナリオのために導入された。これにより、同じポイント・セットで異なるコンフィギュレーションを持つ複数のデバイスを素早く作成することができます。

![Templates](https://assets.emqx.com/images/313c741b7e535e721cd1219e14f9d444.png)

<center>テンプレート</center>

<br>

![Create Device Nodes Based on Templates](https://assets.emqx.com/images/839758563bab6cb3de66b83ae3cdb299.png)

<center>テンプレートに基づくデバイスノードの作成</center>

<br> 

> *テンプレートはインポート/エクスポート機能もサポートしています。詳しくは*[*テンプレートの使用方法*](https://neugates.io/docs/en/latest/configuration/templates/templates.html)*をご覧ください。*

### Modbus UDP トランスポート・サポート

Modbus TCPプラグインがModbus TCPプロトコルベースのUDPトランスポートをサポートしました。これにより、トランスポート層でUDPプロトコルを使用した通信が可能になります。

![Modbus TCP Configuration Interface](https://assets.emqx.com/images/aa097aa11868bbcf275ae331573d4f0b.png)

<center>Modbus TCP コンフィギュレーション・インターフェイス</center>

### Modbus リード・リトライ

Modbusプラグインは、デバイス接続の問題が発生した場合の再試行をサポートするようになりました。再試行の回数と間隔はプラグインのコンフィギュレーション・ページで設定できます。

### IEC104高可用性マスター・スレーブ・モード

IEC104プロトコルは、信頼性向上のため、高可用性マスター・スレーブ・モードをサポートするようになった。このメカニズムは、プライマリ・デバイスが故障したり使用できなくなった場合にバックアップ・デバイスが引き継ぐことを可能にすることで、中断のないオペレーションを保証します。高可用性モードは、電力システムのような重要な領域で高い可用性と信頼性を必要とするアプリケーションにとって極めて重要です。

![IEC60870-5-104 Configuration Interface](https://assets.emqx.com/images/0a15e1d0b53e54e4a4b88dec92c2bfc6.png)

<center>IEC60870-5-104 コンフィギュレーション・インターフェイス</center>

## 新ドライバー・一覧

### プロフィネットIO

Profinet IO (Industrial Ethernet Input/Output) は、産業オートメーション分野で使用されるリアルタイムイーサネット通信プロトコルです。イーサネット技術をベースにしており、高性能で信頼性の高いデータ交換とリアルタイム制御を提供することを目的としています。Profinet IOは特に入出力（I/O）デバイスと制御システム間の通信用に設計されています。デジタルおよびアナログ信号のリアルタイム伝送、デバイスステータスの制御と監視が可能です。

![Profinet IO ](https://assets.emqx.com/images/f561fb20b9ce986c5a298884fe3bdbb1.png)

> [*Profinet IO ドライバ ユーザーマニュアル*](https://neugates.io/docs/en/latest/configuration/south-devices/profinet/profinet.html)

### Mitsubishi FX

Mitsubishi FX シリーズ PLC は、三菱電機が提供する経済的で実用的な製品ラインです。ユーザーフレンドリーなインターフェース、信頼性、安定性、柔軟性が広く認められています。FXシリーズPLCは、小規模な機械から大規模な生産ラインまで、さまざまな規模と複雑さのアプリケーションに適しています。

Neuronの三菱FXプラグインを使用すると、FXプログラミング・ポートを介して三菱のFX0、FX2、FX3、およびその他のシリーズPLCにアクセスできます。

![Mitsubishi FX](https://assets.emqx.com/images/af0daafca5c6d872b1f6e873331bdc0b.png) 

> [*Mitsubishi FX ドライバー ユーザーマニュアル*](https://neugates.io/docs/en/latest/configuration/south-devices/mitsubishi-fx/overview.html#parameter-configuration)

### Omron FINS UDP

Omron FINSは、産業オートメーション分野で使用される通信プロトコルです。FINSプロトコルは、プログラマブルロジックコントローラ（PLC）、センサ、サーボドライブなどのOmron 機器間のデータ交換や通信を可能にします。

FINSプロトコルにおいて、UDP（User Datagram Protocol）は、FINSプロトコルパケットをネットワーク上で伝送するために使用されるトランスポート層プロトコルである。UDPはコネクションレス型のプロトコルであり、効率性とリアルタイム性が要求されるアプリケーションに適した、シンプルで信頼性の低いデータ伝送メカニズムを提供する。

Neuron 2.5.1のFINS UDPドライバは、Ethernetを介したOmron 機器間の高速でリアルタイムのデータ交換を可能にします。UDP通信は、TCPなどの他のプロトコルに比べて通信レイテンシが低いですが、信頼性とデータの整合性チェックは提供されません。したがって、FINS UDPを通信に使用する場合は、ネットワークの安定性を確保し、データ損失やエラーに対処するための適切なメカニズムを採用することが不可欠です。

![Omron FINS UDP](https://assets.emqx.com/images/d9ffce2539d9929ad67128b4d474b7b8.png) 

> [*Omron FINS UDPドライバ ユーザーマニュアル*](https://neugates.io/docs/en/latest/configuration/south-devices/omron-fins/omron-fins-udp.html)

### Panasonic Mewtocol

Panasonic Mewtocolは、産業オートメーション分野で使用される通信プロトコル。プログラマブルロジックコントローラ（PLC）、ヒューマンマシンインタフェース（HMI）、サーボシステム、その他の産業機器など、パナソニックの機器間でデータ交換や通信を行うためのプロトコルです。

NeuronのPanasonic Mewtocolプラグインを使用すると、Ethernet経由でPanasonicのFP-XHおよびFP0HシリーズPLCにアクセスできます。

![Panasonic Mewtocol ](https://assets.emqx.com/images/ae5b3e0fde0b98ec26bf59a4760beaa1.png)

> [*パナソニックMewtocolドライバユーザーマニュアル*](https://neugates.io/docs/en/latest/configuration/south-devices/panasonic-mewtocol/overview.html)

### DLT645-1997

DL/T645-1997は、中国で使用されている電子式エネルギーメーターの技術標準です。この規格は、電子エネルギー・メーターとデータ収集システム間の情報交換のための通信プロトコルとデータ形式を定義しています。

DL/T645-1997 は、データフレームの構造、データフィールドの内容、エネルギー消費およびその他の関連情報を伝送するための通信方法を規定している。検針、負荷制御、イベント記録、パラメータ設定など様々な側面をカバーしている。

この規格は、エネルギー・メーターと電力供給会社またはエネルギー監視・管理に携わる他の事業体との間の通信のための共通の枠組みを提供する。これにより、正確で効率的なデータ収集、請求、およびエネルギー使用量の分析が可能になる。

DL/T645-1997 プラグインは、シリアルポート接続と透過的 TCP 接続の両方をサポートしています。

![image.png](https://assets.emqx.com/images/d8b746a9604695910dbbba729bf4dbb8.png)

> [*DLT645-1997 ドライバ ユーザーマニュアル*](https://neugates.io/docs/en/latest/configuration/south-devices/dlt645-1997/dlt645-1997.html#module-description)

## 今後の企画

### MQTT機能のアップグレード

これには、オフライン・キャッシュ・データ報告の頻度制御の追加や、MQTTオフライン・キャッシュ・データ報告のカスタム・トピック定義のサポートが含まれる。

### ドライバーのアップグレード

IEC60870-5-104やBACnet/IPなどのドライバについては、継続的な改善とアップグレードが計画されています。さらに、SECS/GEMのようなプロトコルのサポート追加にも積極的に取り組んでいます。

### 強化された機能

ユーザーエクスペリエンスを向上させ、トラブルシューティングを容易にするために、ログのダウンロードとDEBUGログ機能を継続的に最適化していきます。また、設定ドキュメントのサポート機能も強化していきます。



<section class="promotion">
    <div>
        Try Neuron for Free
             <div class="is-size-14 is-text-normal has-text-weight-normal">工業プロトコルゲートウェイソフトウェア
</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">トライアル開始 →</a>
</section>
