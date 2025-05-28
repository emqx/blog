## MQTT 制御パケットとは何ですか?

MQTT 制御パケットは、[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)におけるデータ転送の最小単位です。[MQTT クライアント](https://www.emqx.com/ja/blog/mqtt-client-tools)とサーバーは、トピックのサブスクライブやメッセージのパブリッシュなどの機能を実行するために制御パケットを交換します。

現在、MQTT では 15 種類の制御パケットが定義されています。機能に基づいてパケットを分類すると、これらのパケットを接続、パブリッシュ、サブスクライブの 3 つのカテゴリに分類できます。

<img src="https://assets.emqx.com/images/f072fa0c17d4a188db0768caf5d17d19.png?x-image-process=image/resize,w_1520/format,webp" alt="MQTT control packets" style="zoom:150%;" />

このうち、**CONNECT**パケットはクライアントがサーバーへの接続を開始するために使用され、**CONNACK**パケットは接続の結果を示す応答として送信されます。通信を終了する場合、または接続の終了を必要とするエラーが発生した場合、クライアントとサーバーは**DISCONNECT**パケットを送信してネットワーク接続を閉じることができます。

**AUTH**パケットは、MQTT 5.0 で導入された新しいタイプのパケットであり、強化された認証のみに使用され、クライアントとサーバーにより安全な認証を提供します。

**PINGREQ**および**PINGRESP**パケットは、接続のKeep Aliveとプローブに使用されます**。**クライアントは定期的にサーバーに**PINGREQ**パケットを送信してサーバーがまだアクティブであることを示し、**PINGRESP**パケットが時間内に返されるかどうかに応じてサーバーがアクティブであるかどうかを判断します。

**PUBLISH**パケットはメッセージのパブリッシュに使用され、以外のパケットは QoS 1 および 2 メッセージの確認に使用されます**。**

**SUBSCRIBE**パケットはトピックを購読するためにクライアントによって使用されますが、**UNSUBSCRIBE**パケットは購読をキャンセルために使います。**SUBACK パケット**と**UNSUBACKパケット**は、それぞれ購読と購読解除の結果を返すために使用されます。

## MQTTパケットフォーマット

MQTT では、制御パケットの種類に関係なく、すべてFixed Header、Variable Header、Payloadの 3 つの部分で構成されます。

Fixed Headerはすべての制御パケットに常に存在します。Variable HeaderとPayloadの存在と内容は、特定のパケット タイプによって異なります。たとえば、Keep Aliveに使用される**PINGREQ**パケットにはFixed Headerのみが含まれますが、アプリケーション メッセージの送信に使用される**PUBLISH**パケットには 3 つフォーマットすべてが含まれます**。**

![MQTT Packet Format](https://assets.emqx.com/images/aa4530a68f7576acd841142f5fd90043.png?x-image-process=image/resize,w_1520/format,webp)

### Fixed Header

Fixed Headerは、MQTT 制御パケット タイプ、フラグ、および残りの長さの 3 つのフィールドで構成されます。

![MQTT Fixed Header](https://assets.emqx.com/images/4131b773a84f710314becd143f26a8d9.png?x-image-process=image/resize,w_1520/format,webp)

MQTT 制御パケット タイプは、Fixed Headerの最初のバイトの上位 4 ビットにあります。これは、現在のパケットのタイプを表す符号なし整数です。たとえば、1 は**CONNECT**パケットを示し、2 は**CONNACK**パケットを示します。詳細なマッピングは、MQTT 5.0 仕様[「MQTT Control Packet Types」](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901022)に記載されています。実際、MQTT 制御パケット タイプと残りの長さのフィールドを除いて、MQTT パケットの残りの部分の内容は特定のパケット タイプによって異なります。したがって、このフィールドは、受信者がパケットの次のコンテンツをどのように解析するかを決定します。

Fixed Headerの最初のバイトの残りの下位 4 ビットには、制御パケット タイプによって決定されるフラグが含まれています。ただし、MQTT 5.0 の時点では、 **PUBLISH**パケット内の 4 ビットのみに特定の意味が割り当てられています。

- ビット 3：DUP、現在の**PUBLISH**パケットが再送パケットであるかどうかを示します。
- ビット 2,1：QoS、現在**のPUBLISH**パケットで使用されるサービス品質レベルを示します。
- ビット 0：保持。現在の**PUBLISH**パケットが保持されるかどうかを示します。

他のすべてのパケット タイプでは、これらの 4 ビットは予約されたままであり、任意に変更できない固定値を持つことを意味します。

最後の Remaining Length フィールドは、Variable HeaderとPayloadを含む制御パケットの残りの部分のバイト数を示します。したがって、MQTT 制御パケットの全長は、Fixed Headerの長さに残りの長さを加えたものと等しくなります。

![Remaining Length](https://assets.emqx.com/images/19eb3616e9fd094aa675305e08b391da.png?x-image-process=image/resize,w_1520/format,webp)

#### Variable Byte Integer

ただし、Fixed Headerの長さは固定ではありません。パケット サイズを可能な限り最小化するために、MQTT は残りの長さフィールドを可変バイト整数として使用します。

MQTT には可変長のフィールドが多数あります。たとえば、**PUBLISH**パケットのPayload部分は実際のアプリケーション メッセージを運ぶために使用され、アプリケーション メッセージの長さは明らかに固定されていません。したがって、受信側が可変長コンテンツを正しく解析できるように、これらの可変長コンテンツの長さを示す追加フィールドが必要です。

合計 2,097,152 バイトである 2 MB のアプリケーション メッセージの場合、その長さを示すために 4 バイトの整数が必要になります。ただし、すべてのアプリケーション メッセージがそれほど大きいわけではありません。多くの場合、それらはわずか数 KB、あるいはわずか数バイトです。わずか 2 バイトのメッセージ長を示すために 4 バイトの整数を使用するのは過剰になります。

したがって、MQTT では、各バイトの下位 7 ビットを利用してデータをエンコードする可変バイト整数が導入され、最上位ビットは後続のバイトがあるかどうかを示します。このように、パケット長が 128 バイト未満の場合、可変バイト整数は 1 バイトのみを示す必要があります。可変バイト整数の最大長は 4 バイトで、最大 (2^28 - 1) バイト、つまり 256 MB のデータの長さを示すことができます。

![Variable Byte Integer](https://assets.emqx.com/images/055cf380b41283639f48a514e439cea2.png?x-image-process=image/resize,w_1520/format,webp)

### Variable Header

MQTT のVariable Headerの内容は、特定のパケット タイプによって異なります。たとえば、**CONNECT**パケットのVariable Headerには、プロトコル名、プロトコル レベル、接続フラグ、Keep Alive、プロパティがこの順で含まれます。**PUBLISH**パケットのVariable Headerには、トピック名、パケット識別子 (QoS が 0 でない場合)、プロパティがこの順序で含まれます。

![MQTT Variable Header](https://assets.emqx.com/images/22e02825f2a09033f311218b4e9985b1.png?x-image-process=image/resize,w_1520/format,webp)

受信側は指定された順序でのみ解析するため、Variable Headerのフィールドはプロトコル仕様に厳密に従う必要があります。プロトコルで明示的に要求または許可されていない限り、フィールドを省略することはできません。たとえば、**CONNECT**パケットのVariable Headerで、接続フラグがプロトコル名の直後に配置されている場合、解析エラーが発生します。同様に、 **PUBLISH**パケットのVariable Headerには、QoS が 0 でない場合にのみパケット識別子が存在します。

#### プロパティ

プロパティは、MQTT 5.0 で導入された概念です。これらは基本的に、Variable Headerの最後の部分です。プロパティは、プロパティ長フィールドとその後に続く一連のプロパティで構成されます。プロパティの長さは、後続のすべてのプロパティの合計の長さを示します。

![Properties](https://assets.emqx.com/images/4dc5e956daa02e22aeb17b7a6b3d1b00.png?x-image-process=image/resize,w_1520/format,webp)

通常はデフォルト値があるため、すべてのプロパティはオプションです。プロパティがない場合、プロパティの長さの値は 0 です。

各プロパティは、プロパティの目的とデータ型を定義する識別子と、特定の値で構成されます。プロパティが異なれば、データ型も異なる場合があります。たとえば、1 つは 2 バイトの整数で、もう 1 つは UTF-8 でエンコードされた文字列であるため、識別子によって宣言されたデータ型に従ってプロパティを解析する必要があります。

![Property](https://assets.emqx.com/images/c4c3242f6b3f90518a88f034c8354010.png?x-image-process=image/resize,w_1520/format,webp)

識別子に基づいてそれがどのプロパティであるか、およびその長さを知ることができるため、プロパティの順序は任意でありえます。

通常、プロパティは特定の目的のために設計されます。たとえば、**CONNECT**パケットには、セッションの有効期限を設定するための Session Expiry Interval プロパティがあります。ただし、このプロパティは**PUBLISH**パケットでは必要ありません。したがって、MQTT ではプロパティの使用範囲が厳密に定義されており、有効な MQTT 制御パケットには、それに属さないプロパティが含まれるべきではありません。

識別子、プロパティ名、データ型、使用範囲など、MQTT プロパティの包括的なリストについては、「[MQTT 5.0 Specification - Properties」](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901027)を参照してください。

### Payload

最後にPayloadがあります。パケットのVariable Headerはその補足情報として見ることができ、Payloadはパケットの中心的な目的を達成するために使用されます。

たとえば、**PUBLISH**パケットでは、Payloadは実際のアプリケーション メッセージを運ぶために使用されます。これが**PUBLISH**パケットの主な機能です。**PUBLISH**パケットのVariable Headerに QoS、Retain、およびその他のフィールドは、アプリケーション メッセージに関連する追加機能を提供します。

**SUBSCRIBE**パケットも同様のパターンに従います。Payloadには、サブスクライブするトピックと、それに対応するサブスクリプション オプションが含まれています。これは、**SUBSCRIBE**パケットの主なタスクです。

## MQTT パケット - 上級者向け

今後のブログ シリーズでは、さまざまな MQTT パケットのフィールドとその主な目的について説明します。各ブログの最後に、実際のパケットの例を示し、パケット内のこれらのフィールドの分布を示します。ブログには次のものが含まれます。

- [MQTT 5.0 Packet Explained 01: CONNECT & CONNACK](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-01-connect-connack)
- [MQTT 5.0 Packet Explained 02: PUBLISH & PUBACK](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-02-publish-puback)
- [MQTT 5.0 Packet Explained 03: SUBSCRIBE & UNSUBSCRIBE](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-03-subscribe-unsubscribe)
- [MQTT 5.0 Packet Explained 04: PINGREQ & PINGRESP](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-04-pingreq-pingresp)
- [MQTT 5.0 Packet Explained 05: DISCONNECT](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-05-disconnect)
- [MQTT 5.0 Packet Explained 06: AUTH](https://www.emqx.com/en/blog/mqtt-5-0-control-packets-06-auth)



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
