## はじめに

BACnetは、インテリジェントビルディング用に設計された通信プロトコルです。ISO（国際標準化機構）、ANSI（アメリカ国家標準協会）、およびASHRAE（アメリカ暖房冷凍空調学会）によって共同で定義されています。BACnet通信は、暖房、換気、および空調（HVAC）システム、照明制御、アクセス制御システム、火災検知システム、および関連機器で使用されます。これは、幅広いビルディングオートメーションアプリケーションのための機器および制御デバイス間の相互運用性を実現するためのベンダー非依存のネットワークソリューションを提供します。BACnetは、データ、コマンド、およびステータス情報を交換するために使用される通信メッセージ、フォーマット、およびルールを定義することによって相互運用性を実装します。BACnetは、インテリジェントビルディングのためのデータ通信インフラを提供し、世界中の数万のビルで実装されています。

BACnet通信プロトコルは、複数の異なるデータリンク層/物理層を定義しています。これには以下が含まれます：

1. ARCNET
2. Ethernet
3. BACnet/IP
4. RS-232上のポイントツーポイント通信
5. RS-485上のマスタースレーブ/トークンパッシング（MS/TP）通信
6. LonTalk

この記事では主にBACnet/IPに焦点を当てます。

## BACnet/IP 概要

BACnet/IPはUDPプロトコルを使用してデータを転送し、デバイスが通常サーバーとして機能するクライアントサーバー通信アプローチを使用します。デフォルトのポートは47808（0xBAC0）です。BACnet/IPパケットは、主に不変部分と可変部分で構成されています。不変部分はBVLCタイプ、BVLC機能、および長さで構成され、可変部分はBVLC機能に応じて異なります。BACnet/IPパケットの構造は以下の図に示されています。

![The structure of a BACnet/IP packet](https://assets.emqx.com/images/d13961d03604ae03a6d875144be4a812.png)

BACnet/IPパケットの基本的なパケットタイプには、Original-Unicast-NPDU、Original-Broadcast-NPDU、Forwarded-NPDUがあり、それぞれの形式は以下の図に示されています。

![Original-Unicast-NPDU](https://assets.emqx.com/images/911c1fa64dc98363830c85a0025ebb94.png)

![Original-Broadcast-NPDU](https://assets.emqx.com/images/d00aa892957b616bbfc57349de81989b.png)

![Forwarded-NPDU](https://assets.emqx.com/images/3018b29a278969770a0c83d78e67f794.png)

## ネットワーク層プロトコルデータユニット(NPDU)

NPDUは、NPCIに続いてNSDUで構成されています。以下の表にはNPCIが含まれていますが、しばしば誤ってNPDUと呼ばれます。注意してください。

![NPDU](https://assets.emqx.com/images/0c131afe5ecd8b76e739a9eeb6669ba2.png)

**NPCIコントロールオクテット**

| **ビット** | **説明**              | **1の場合**                                            | **0の場合**               |
| :--------- | :-------------------- | :----------------------------------------------------- | :------------------------ |
| 7          | APDU                  | NSDU conveys Network Layer Message                     | NSDU contains BACnet APDU |
| 6          | Reserved              | Reserved                                               | Reserved                  |
| 5          | Destination Specifier | DNET DLEN DADR present                                 | DNET DLEN DADR absent     |
| 4          | Reserved              | Reserved                                               | Reserved                  |
| 3          | Source Specifier      | SNET SLEN SADR present                                 | SNET SLEN SADR absent     |
| 2          | Expecting reply       | Reply                                                  | No reply                  |
| 1,0        | Priority              | 11=Life Safety, 10=Critical Equip, 01=Urgent 00=Normal |                           |

## アプリケーション層プロトコルデータユニット(APDU)

BACnet APDUは、アプリケーション層のパラメータを運びます。APDUの最大サイズは、デバイスのMax_APDU_Length_Acceptedによって指定されます。

これは、NSDUの2つの代替のうちの1つです。もう1つはRPDUです。

### APDUのタイプ

| **APDUタイプ (コード) (最初のニブル)** | **APDU (構造)**                | **プロトコル仕様** | **コメント**                                            |
| :------------------------------------- | :----------------------------- | :----------------- | :------------------------------------------------------ |
| 0x0X                                   | BACnet-Confirmed-Request-PDU   | 20.1.2             |                                                         |
| 0x1X                                   | BACnet-Unconfirmed-Request-PDU | 20.1.3             |                                                         |
| 0x2X                                   | BACnet-SimpleACK-PDU           | 20.1.4             |                                                         |
| 0x3X                                   | BACnet-ComplexACK-PDU          | 20.1.5             |                                                         |
| 0x4X                                   | Segment ACK                    | 20.1.6             |                                                         |
| 0x5X                                   | Error PDU                      | 20.1.7             | エラー                                                  |
| 0x6X                                   | Reject-PDU                     | 20.1.8             | 構文上の理由によりPDUが拒否される、BACnet拒否理由を含む |
| 0x7X                                   | Abort PDU                      | 20.1.9             | BACnet中止理由を含む                                    |
| 0x8X~0xfX                              | Reserved                       |                    |                                                         |

### よく使用されるAPDU

**BACnet-Confirmed-Request-PDU**

![BACnet-Confirmed-Request-PDU](https://assets.emqx.com/images/aa1ba0361dd1950f2ca3741c504fd230.png)

**BACnet-Unconfirmed-Request-PDU**

![BACnet-Unconfirmed-Request-PDU](https://assets.emqx.com/images/6d95391e21a9b709da617b5f373f752e.png)

**BACnet-Simple-ACK-PDU**

![BACnet-Simple-ACK-PDU](https://assets.emqx.com/images/fc1c2389908e41f5baa7341c6ff09703.png)

**BACnet-ComplexACK-PDU**

![BACnet-ComplexACK-PDU](https://assets.emqx.com/images/90707fe1d32b1b09bc7ba01f2ab4a44a.png)

### APDU内の重要なデータ構造

**BACnetタグ**

タグには2種類あり、**タグ番号**の使用はそれぞれによって異なります。

- アプリケーションタグ
  - これらには固定のタイプがあります - boolean、int、dateなど。
- コンテキスト固有タグ
  - これらのタグのタイプは、APDUの可変部分で見つかる場所に依存します。単独で検査することでそのタイプを決定することはできません。
  - これらには、データの意味を指定する関連するコンテキスト番号があります。
  - コンテキストタグにより、構築されたタグ（リスト）を作成できます。

![image.png](https://assets.emqx.com/images/71c5f8a613534d548826ee2e950b7eed.png)

クラス=0はアプリケーションタグ用（タグのタイプを示します）

クラス=1はコンテキスト固有タグ用（タグのシーケンスを示します）

**アプリケーションデータタイプ**

アプリケーションデータタイプ（または一般的に、アプリケーションタグ）は、各タグ番号に対して固定の意味を持ちます。以下の表を参照してください。独自のデータタイプは、これらのアプリケーションデータタイプを使用してのみ構築できます。

| タグ番号 | 説明                                                         |
| :------- | :----------------------------------------------------------- |
| 0        | NULL                                                         |
| 1        | Boolean                                                      |
| 2        | Unsigned Integer*                                            |
| 3        | Signed Integer                                               |
| 4        | Real                                                         |
| 5        | Double                                                       |
| 6        | Octet String                                                 |
| 7        | Character String                                             |
| 8        | Bit String                                                   |
| 9        | Enumerated                                                   |
| 10       | Date                                                         |
| 11       | Time                                                         |
| 12       | BACnetObjectIdentifier                                       |
| 13       | Reserved                                                     |
| 14       | Reserved                                                     |
| 15       | Reserved - Indicates that the following Octect contains an 8-bit Tag Number |

> 注: Unsigned integersは、Unsigned 8、Unsigned 16、またはUnsigned 32である可能性があります。

**オブジェクト識別子**

オブジェクトは、オブジェクト識別子とデバイスのオブジェクト識別子の組み合わせによって一意に識別できます。この一意性は、指定されたデバイスに限定され、ネットワーク全体では適用されません。4194303をオブジェクト識別子として使用することは許可されておらず、含まれるオブジェクトが初期化されていないことを示します。

デバイスのオブジェクト識別子は、ネットワーク全体で一意である必要があります。これは、デバイスインスタンスが任意のBACnetインターネットワークで一意であることを実質的に意味します。

オブジェクト識別子のアプリケーションタグ番号は12です。

| **31~22**                     | **21~0**                            |
| :---------------------------- | :---------------------------------- |
| オブジェクトタイプ (10ビット) | オブジェクトインスタンス (22ビット) |

**プロパティ識別子**

これらはプロトコル内で列挙された値です。また、タグ付けされた値を理解することも重要です。

合計で192以上のプロパティがあります。以下はそのいくつかです：

| **値** | **16進数** | **説明**                     | **エンコード方式** |
| :----- | :--------- | :--------------------------- | :----------------- |
| 12     | 0x0C       | Application Software Version | Character String   |
| 77     | 0x4E       | Object Name                  | Character String   |
| 85     | 0x55       | Present Value                |                    |

**プロパティ読み取りリクエスト**

| **エンコーディング** | **引数**             | **必須**  |
| :------------------- | :------------------- | :-------- |
| Context 0            | Object Identifier    | Mandatory |
| Context 1            | Property Identifier  | Mandatory |
| Context 2            | Property Array Index | User      |

**プロパティ書き込み**

| **エンコーディング** | **引数**             | **必須**    |
| :------------------- | :------------------- | :---------- |
| Context 0            | Object Identifier    | Mandatory   |
| Context 1            | Property Identifier  | Mandatory   |
| Context 2            | Property Array Index | User        |
| Context 3            | Property Value       | Mandatory   |
| Context 4            | Priority             | Commandable |

**確認サービスACK プロパティ読み取り**

| Encoding  | **引数**             | **必須**                        | **コメント**                                                 |
| :-------- | :------------------- | :------------------------------ | :----------------------------------------------------------- |
| Context 0 | Object Identifier    | Mandatory Equal                 |                                                              |
| Context 1 | Property Identifier  | Mandatory Equal                 |                                                              |
| Context 2 | Property Array Index | User Equal (Must match request) | 配列長を示す次のアイテムである場合、この値は0でなければなりません |
| Context 3 | Property Value(s)    | Mandatory Equal                 | これは単一のフィールド、またはエンコーディングの選択に応じて複数のフィールドになる可能性があります。変数エンコーディングは仕様書のセクション20.3に従います。 |

## デバイスオブジェクトモデル

異なるデバイスには、情報を格納するための異なるデータ構造があります。デバイス間で情報交換を可能にするためには、「ネットワーク可視」情報記述方法を定義する必要があります。これを達成するために、オブジェクト指向アプローチが利用されます。すべてのオブジェクトはオブジェクト識別子によって参照されます。各BACnetデバイスオブジェクトには一意のオブジェクト識別子プロパティ値があります。オブジェクトのオブジェクト識別子とシステム全体で一意なBACnetデバイスオブジェクト識別子プロパティ値の組み合わせにより、全コントロールネットワークを通じて各オブジェクトを参照するメカニズムが提供されます。

BACnetは標準のオブジェクトタイプとオブジェクトプロパティのセットを定義していますが、標準オブジェクトタイプの追加の非標準プロパティや非標準オブジェクトタイプの自由な定義も可能にしています。

実際のケースでは、アナログ入力オブジェクトタイプ、アナログ出力オブジェクトタイプ、アナログ値オブジェクトタイプ、バイナリ入力オブジェクトタイプ、バイナリ出力オブジェクトタイプ、バイナリ値オブジェクトタイプ、デバイスオブジェクトタイプなど、一般的に使用される標準オブジェクトがあります。

次に、アナログ入力オブジェクトタイプを詳細に分析します。各オブジェクトタイプの分析の開始時には、その属性のリストがあります。リスト項目には、属性識別子、属性データタイプ、および属性一貫性コードO、R、またはWのいずれかが含まれます。

- O: 属性がオプションであることを示します。
- R: 属性が必須であり、BACnetサービスによって読み取り可能であることを示します。
- W: 属性が必須であり、BACnetサービスによって読み取り可能および書き込み可能であることを示します。

このオブジェクトとそのプロパティは、以下の表に示されています。

| **属性識別子**     | **属性データタイプ**      | **属性一貫性コード** |
| :----------------- | :------------------------ | :------------------- |
| Object_Identifier  | BACnetObjectIdentifier    | R                    |
| Object_Name        | CharacterString           | R                    |
| Object_Type        | BACnetObjectType          | R                    |
| Present_Value      | REAL                      | R1                   |
| Description        | CharacterString           | O                    |
| Device_Type        | CharacterString           | O                    |
| Status_Flags       | BACnetStatusFlags         | R                    |
| Event_State        | BACnetEventState          | R                    |
| Reliability        | BACnetReliability         | O                    |
| Out_Of_Service     | BOOLEAN                   | R                    |
| Update_Interval    | Unsigned                  | O                    |
| Units              | BACnetEngineeringUnits    | R                    |
| Min_Pres_Value     | REAL                      | O                    |
| Max_Pres_Value     | REAL                      | O                    |
| Resolution         | REAL                      | O                    |
| COV_Increment      | REAL                      | O2                   |
| Time_Delay         | Unsigned                  | O3                   |
| Notification_Class | Unsigned                  | O3                   |
| High_Limit         | REAL                      | O3                   |
| Low_Limit          | REAL                      | O3                   |
| Deadband           | REAL                      | O3                   |
| Limit_Enable       | BACnetLimitEnable         | O3                   |
| Event_Enable       | BACnetEventTransitionBits | O3                   |
| Acked_Transitions  | BACnetEventTransitionBits | O3                   |
| Notify_Type        | ACnetNotifyType           | O3                   |

1 Out_Of_ServiceがTRUEの場合、この属性は書き込み可能でなければなりませせん。

2 オブジェクトがCOVレポートをサポートしている場合、この属性は必須です。

3 オブジェクトが内部レポートをサポートしている場合、この属性は必須です。

**Object_Identifier**

この属性のタイプはBACnetObjectIdentifierで、数値コードを使用してオブジェクトを識別します。それは、この属性を持つBACnetデバイス内で一意です。

**Object_Name**

この属性のタイプはCharacterStringで、オブジェクトの名前を表します。それは、この属性を持つBACnetデバイス内で一意です。文字列の最小長は1文字です。オブジェクト名の文字は印刷可能な文字でなければなりません。

**Object_Type**

この属性のタイプはBACnetObjectTypeで、特定のオブジェクトタイプの分類を表します。このオブジェクトでは、この属性の値はアナログ入力(ANALOG_INPUT)です。

**Present_Value**

この属性のタイプは実数型で、エンジニアリング単位での入力測定の現在値を表します。Out_Of_ServiceがTRUEの場合、現在値属性は書き込み可能です。

**Description**

この属性のタイプはCharacterStringで、印刷可能な文字から構成される文字列で、特定の内容要件はありません。

**Device_Type**

この属性のタイプはCharacterStringで、このアナログ入力オブジェクトにマッピングされた物理デバイスのテキスト記述を表します。通常、アナログ入力オブジェクトに対応するセンサーモデルを記述するために使用されます。

**Status_Flags**

この属性のタイプはBACnetStatusFlagsで、ある時点でのアナログ入力デバイスの状態を示す4つのブールフラグを表します。フラグの3つはこのオブジェクトの他の属性値に関連しています。これらのフラグに関連する属性値を読むことによって、より詳細なステータスを取得できます。

**Event_State**

この属性のタイプはBACnetEventStateで、オブジェクトがイベントアクティブ状態にあるかどうかを検出するために使用されます。オブジェクトが内部レポートをサポートしている場合、この属性はオブジェクトのイベント状態を表します。オブジェクトが内部レポートをサポートしていない場合、この属性の値は通常です。

**Reliability**

この属性のタイプはBACnetReliabilityで、物理入力デバイスの現在値または操作が信頼できるかどうか、および信頼できない場合の理由を指定します。この属性には以下の値があります：{故障検出なし、センサーなし、範囲外、範囲以下、オープンサーキット、ショートサーキット、その他の信頼できない}。

**Out_Of_Service**

この属性のタイプはBooleanで、オブジェクトによって表される物理入力が（TRUE）または（FALSE）でないことを示します。"Out_Of_Service"がTRUEの場合、現在値属性は物理入力デバイスから切り離され、物理入力デバイスの変更によって変化しません。"Out_Of_Service"がTRUEの場合、信頼性属性と、対応するステータスフラグ属性の故障フラグ状態も物理入力デバイスから切り離されます。"Out_Of_Service"がTRUEの場合、現在値および信頼性属性は、特定の固定条件をシミュレートするためや、テスト目的で使用される場合に任意の値を取ることができます。現在値または信頼性属性に依存する他の機能は、これらの変更が入力で発生したかのようにこれらの変更に応答します。

**Update_Interval**

この属性のタイプは符号なし整数型で、正常動作中に現在値が2回正常に更新される間の最大時間間隔（百分の一秒単位）を表します。

**Units**

この属性のタイプはBACnetEngineeringUnitsで、このオブジェクトの測定単位を表します。

**Min_Pres_Value**

この属性のタイプは実数型で、現在値属性の最小信頼可能な数値値（エンジニアリング単位で表される）を表します。

**Max_Pres_Value**

この属性のタイプは実数型で、現在値属性の最大信頼可能な数値値（エンジニアリング単位で表される）を表します。

**Resolution**

この属性のタイプは実数型で、エンジニアリング単位での現在値属性の最小検出可能な変化を示します（読み取り専用）。

**COV_Increment**

この属性のタイプは実数型で、現在値属性が変化してCOV通知がCOV顧客に発行される最小変化値を定義します。オブジェクトがCOVレポートをサポートする場合、この属性が存在する必要があります。

**Time_Delay**

この属性のタイプは符号なし整数型で、現在値属性が高閾値と低閾値によって決定される範囲外にある場合からTO_OFFNORMALイベントが生成されるまで、または現在値属性が高閾値と低閾値によって決定される範囲（閾値幅属性値によって決定される範囲を含む）内に入る場合からTO_NORMALイベントが生成されるまでの最小時間間隔（秒単位）を定義します。オブジェクトが内部レポートをサポートする場合、この属性が存在する必要があります。

**Notification_Class**

この属性のタイプは符号なし整数型で、このオブジェクトがイベント通知を処理および生成する際に使用する通知カテゴリを定義します。この属性は、同じ通知クラス属性値を持つ通知クラスオブジェクトをデフォルトで参照します。オブジェクトが内部レポートをサポートする場合、この属性が存在する必要があります。

**High_Limit**

この属性のタイプは実数型で、イベントを生成する際に現在値属性の上限値を定義します。オブジェクトが内部レポートをサポートする場合、この属性が存在する必要があります。

**Low_Limit**

この属性のタイプは実数型で、イベントを生成する際に現在値属性の下限値を定義します。オブジェクトが内部レポートをサポートする場合、この属性が存在する必要があります。

**Deadband**

この属性のタイプは実数型で、高閾値属性と低閾値属性の間の幅範囲値を定義します。TO_NORMALイベントを生成するためには、現在値属性値がこの範囲内に留まる必要があります。TO_NORMALイベントは、以下の5つの条件がすべて満たされた場合に生成されます：

- 現在値が（高閾値 - 閾値幅）以下である
- 現在値が（低閾値 + 閾値幅）以上である
- 現在値が、時間遅延属性によって決定される最小時間間隔内でこの範囲内に留まる
- 閾値有効属性が、高閾値有効または低閾値有効フラグのいずれかに設定されている
- イベント有効属性が、TO_NORMALフラグに設定されている

オブジェクトが内部レポートをサポートする場合、この属性が存在する必要があります。

**Limit_Enable**

この属性のタイプはBACnetLimitEnableで、高閾値異常イベントと低閾値異常イベントの報告を有効または無効にするための2つのフラグを使用し、それぞれの正常に戻るイベントを示します。オブジェクトが内部レポートをサポートする場合、この属性が存在する必要があります。

**Event_Enable**

この属性のタイプはBACnetEventTransitionBitsで、異常状態への入り、障害（TO_FAULT）への入り、および正常状態への入りのイベントの報告を有効または無効にするための3つのフラグを使用します。アナログ入力オブジェクトの文脈では、高閾値および低閾値イベント状態への遷移は「異常」イベントと呼ばれます。オブジェクトが内部レポートをサポートする場合、この属性が存在する必要があります。

**Acked_Transitions**

この属性のタイプはBACnetEventTransitionBitsで、異常状態への入り、障害状態への入り、および正常状態への入りのイベントの確認を受けたことを示すための3つのフラグを使用します。アナログ入力オブジェクトの文脈では、高閾値および低閾値イベント状態への遷移は「異常」イベントと呼ばれます。これらのフラグは、対応するイベントが発生したときにクリアされ、以下のいずれかの条件下で設定されます：

- 対応する確認を受け取った場合
- 対応するイベント有効属性のフラグが設定されておらず、イベントが発生した場合（この場合、イベント通知は生成されないため、確認も生成されません）
- 対応するイベント有効属性のフラグが設定され、通知クラスオブジェクトの確認変換属性の対応するフラグが設定されていない、およびイベントが発生した場合（この場合、確認は生成されません）

オブジェクトが内部レポートをサポートする場合、この属性が存在する必要があります。

**Notify_Type**

この属性のタイプはACnetNotifyTypeで、オブジェクトが生成する通知がイベントかアラームかを示します。オブジェクトが内部レポートをサポートする場合、この属性が存在する必要があります。

## まとめ

この記事では、一つの標準オブジェクトのみを分析しましたが、他の標準オブジェクトも類似しており、属性が異なるだけです。次のブログでは、BACnetデータを[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)にブリッジしてIIoT接続を強化する方法について、より詳細なチュートリアルを提供します。

> **もっと知る：**
>
> [BACnetデータをMQTTにブリッジング：インテリジェントビルの実装を向上させるソリューション](https://www.emqx.com/ja/blog/bridging-bacnet-data-to-mqtt)

<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient px-5">お問い合わせ →</a>
</section>
