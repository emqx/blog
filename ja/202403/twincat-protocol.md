## TwinCATとは

TwinCAT（The Windows Control and Automation Technology）は、Beckhoff Automationによって開発されたオートメーション技術のためのソフトウェアプラットフォームです。プログラマブルロジックコントローラ（PLC）、モーションコントロールシステム、人間機械インターフェース（HMI）など、さまざまな種類の産業オートメーション機器をプログラムおよび制御するために使用されます。

TwinCATは、モジュラーでスケーラブルなプラットフォームとして設計されており、さまざまなアプリケーションおよび産業で使用することができます。Structured Text（ST）、Ladder Diagram（LD）、Function Block Diagram（FBD）、Sequential Function Chart（SFC）、C/C++など、さまざまなプログラミング言語をサポートしています。

## TwinCATのマイルストーン

TwinCATは、1995年にBeckhoff Automationによって産業オートメーションのためのソフトウェアオンリーのソリューションとして最初に導入されました。元のバージョンのTwinCATは、標準のWindows PC上で実行されるように設計されており、決定的な制御を達成するためにWindows NT用の独自のリアルタイム拡張を使用していました。

年月を経て、TwinCATはさまざまなプログラミング言語のサポートを含む、広範囲のオートメーション機能を備えたように進化し、拡張されました。さらに、統合モーションコントロール、CNC機能、リアルタイムEthernetプロトコルのサポートが追加されました。

2011年、BeckhoffはTwinCAT 3を導入しました。これは、プラットフォームの主要なオーバーホールを表していました。TwinCAT 3は、よりモジュラーでスケーラブルな新しいソフトウェアアーキテクチャに基づいており、より幅広いアプリケーションで使用することができました。TwinCAT 3は、分散制御システム、マルチコアプロセッサ、および高度なモーションコントロールなどの高度な機能のサポートを追加しました。Microsoft Visual Studioとの統合が重要な機能であり、ユーザーは豊富な開発ツールセットを利用できるようになりました。TwinCAT 3では、TwinCATランタイムが64ビットオペレーティングシステムで利用可能であり、プロセッサのマルチコア特性が最適に使用されます。

## TwinCATアーキテクチャ

TwinCATプラットフォームは、柔軟性とスケーラビリティのためにモジュラーなアーキテクチャを持っており、エンジニアリングとランタイムの基本システムで構成されており、Functionsと呼ばれるアプリケーション固有のソフトウェアモジュールによって柔軟に拡張されます。全体として、モジュラーなアーキテクチャは、産業オートメーションのための柔軟でスケーラブルなプラットフォームを提供し、ユーザーが特定のニーズと要件に合わせてシステムをカスタマイズできるようにします。

![TwinCAT Architecture](https://assets.emqx.com/images/dab48e1ca10e88daa809e2cca20450fd.png)

#### エンジニアリング

TwinCAT XAE（eXtended Automation Engineering）は、TwinCAT 3の開発環境であり、Microsoft Visual Studioに基づいています。広範囲のプログラミング言語をサポートし、オートメーションプログラムの作成、デバッグ、デプロイのための包括的なツールセットを提供します。

#### ランタイム

TwinCAT XAR（eXtended Automation Runtime）は、TwinCAT 3システムの中核であり、PLCプログラムの実行、モーションコントロールの調整、およびオートメーションシステム内の他のデバイスとの通信の処理を担当します。ランタイムは、小型の組み込みシステムから大型の産業用PCまで、さまざまなハードウェアプラットフォームで実行できます。

#### Functions

TwinCAT Functionsは、基本システムに幅広い拡張オプションを提供します。例えば、[TwinCAT 3 HMI](https://www.beckhoff.com/en-us/products/automation/twincat/tfxxxx-twincat-3-functions/tf2xxx-tc3-hmi/)は、Web技術（HTML5、JavaScript/TypeScript）に基づくプラットフォーム非依存のユーザーインターフェースの開発を可能にし、[TwinCAT 3 Vision](https://www.beckhoff.com/en-us/products/automation/twincat/tfxxxx-twincat-3-functions/tf7xxx-tc3-vision/)はスケーラブルな画像処理を提供し、[TwinCAT 3 Measurement](https://www.beckhoff.com/en-us/products/automation/twincat/tfxxxx-twincat-3-functions/tf3xxx-tc3-measurement/)は追加の計測技術機能を提供します。

## ADSプロトコル

ADS（Automation Device Specification）プロトコルは、TwinCATシステム内のトランスポート層です。PLC、HMI、およびその他のデバイスなど、オートメーションシステムの異なるコンポーネント間のデータ交換用に開発されました。

![Structure of the ADS communication](https://assets.emqx.com/images/b023b174a2a9afe7586945306742dc6d.png)

ADSプロトコルはTCP/IPまたはUDP/IPプロトコルの上で動作します。ADSプロトコルのTCPポート番号は48898です。

ADSはクライアント-サーバーモデルを採用しており、1つのデバイス（クライアント）が別のデバイス（サーバー）にリクエストを送信し、応答を受け取ります。リクエストと応答には、データ、コマンド、またはステータス情報が含まれます。

![image.png](https://assets.emqx.com/images/8f9f320789aa3a7ccc4d77c34ab35bf7.png)

ADSプロトコルは、サーバーとクライアント間の通信のための[コマンド](https://infosys.beckhoff.com/english.php?content=../content/1033/tcadscommon/12440300683.html&id=)を提供し、その中で最も重要なものは[ADS Read](https://infosys.beckhoff.com/english.php?content=../content/1033/tcadscommon/12440300683.html&id=)コマンドと[ADS Write](https://infosys.beckhoff.com/content/1033/tcadscommon/12440291467.html)コマンドです。

## なぜTwinCATをMQTTにブリッジするのか

インダストリー4.0の登場により、製造業におけるインテリジェンス、オートメーション、デジタル化への需要が高まっています。この文脈において、MQTTプロトコルはADSプロトコルに対して明確な利点を持っています。

[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、パブリッシュ/サブスクライブモデルで動作するIoTデバイスおよびアプリケーション向けに設計されたメッセージングプロトコルです。これは軽量で効率的、信頼性が高く、リアルタイム通信を可能にします。MQTTは、電力と帯域幅の効率的な使用が必要なリソースが限られた環境に適しています。現在、IoT、モバイルインターネット、スマートハードウェア、コネクテッドカー、スマートシティ、遠隔医療サービス、石油およびエネルギーなどの分野で広く応用されています。

さらに、MQTTはオープンスタンダードプロトコルであり、ADSプロトコルと比較して、異なるプラットフォームで実行できる多くのオープンソース実装があります。

## まとめ

この記事では、産業シナリオにおけるTwinCATプロトコルの重要性と、TwinCATデータをMQTTにブリッジすることでこれらのシナリオの効率を向上させる方法について説明しました。次の[ブログ](https://www.emqx.com/ja/blog/bridging-twincat-data-to-mqtt)では、これら2つのプロトコルをブリッジする方法について詳細なガイドを提供します。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient px-5">お問い合わせ →</a>
</section>
