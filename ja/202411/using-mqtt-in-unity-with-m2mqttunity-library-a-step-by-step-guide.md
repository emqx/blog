Unityは、幅広いゲームやシミュレーションを作成するために使用されている人気のゲームエンジンです。[MQTT](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)は、パブリッシュ/サブスクライブモデルに基づく軽量なメッセージングプロトコルであり、低帯域幅や不安定なネットワーク環境でのIoTアプリケーション向けに特別に設計されています。

MQTTは、AR（拡張現実）ゲーム、センサーやその他のデバイスを利用したIoT対応ゲーム、ゲームやシミュレーションのリモートコントロールなど、さまざまな目的でUnityで使用できます。例えば、ARゲームでは、ユーザーのデバイスから平面表面の位置、オブジェクト、人、顔の検出など、世界に関する情報を受信するためにMQTTが使用されます。

このブログでは、[M2MQTT](https://github.com/eclipse/paho.mqtt.m2mqtt)をUnityで使用するためのシンプルな[Unity3d](http://unity3d.com/)プロジェクトを提供します。プロジェクトには、ブローカーへの接続管理やメッセージングのテスト用のユーザーインターフェースを備えた例のシーンが含まれています。

## 前提条件

### Unityのインストール

Unityのインストーラーは、[Unityのウェブサイト](https://unity.com/download)から主要なプラットフォーム向けにダウンロードできます。

### MQTTブローカーの準備

先に進む前に、通信およびテスト用の[MQTTブローカー](https://www.emqx.com/ja/blog/the-ultimate-guide-to-mqtt-broker-comparison)を用意してください。

このブログ記事では、`broker.emqx.io`にある[無料のパブリックMQTTブローカー](https://www.emqx.com/ja/mqtt/public-mqtt5-broker)を使用します。

```
サーバー: broker.emqx.io
TCPポート: 1883
WebSocketポート: 8083
SSL/TLSポート: 8883
セキュアWebSocketポート: 8084
```

無料のパブリックMQTTブローカーは、MQTTプロトコルを学習およびテストしたい方専用に提供されています。セキュリティリスクやダウンタイムの懸念があるため、本番環境での使用は避けることが重要です。

## Unity用のM2MQTT

[M2MQTTライブラリ](https://github.com/CE-SDV-Unity/M2MqttUnity)は、Unityで[M2MQTT](https://github.com/eclipse/paho.mqtt.m2mqtt)を使用するためのシンプルな[Unity3d](http://unity3d.com/)プロジェクトです。ブローカーへの接続管理やメッセージングのテスト用のUIを備えた例のシーンが含まれています。このブログ記事では、例のシーンを使用して、MQTTを利用してMQTTブローカーと通信するアプリケーションを作成する方法を説明します。

まず、GitHubからリポジトリをダウンロードします。

```
git clone https://github.com/CE-SDV-Unity/M2MqttUnity.git
```

### **例のシーンをインポートする**

次に、UnityHubで新しいUnityプロジェクトを作成します。

![New Unity project in UnityHub](https://assets.emqx.com/images/df5df7aeb67cba3b8e326afa811f0ace.png)

その後、ダウンロードしたM2MQTTリポジトリから`M2Mqtt`および`M2MqttUnity`フォルダを新しいUnityプロジェクトの`Assets`フォルダにコピーします。

![Copy the `M2Mqtt` and `M2MqttUnity`](https://assets.emqx.com/images/38244fa7514bf682f547c0168fdf18f4.png)

ライブラリには、`M2MqttUnity_Test`というテストシーンが含まれており、`M2MqttUnity/Examples/Scenes`フォルダにあります。このシーンを確認すると、MQTTクライアントのセットアップに使用されている唯一のスクリプトは`M2MqttUnityTest.cs`であり、このスクリプトはシーン内のM2MQTT GameObjectにアタッチされています。ただし、このスクリプトはメインフォルダ`M2Mqtt`の他のクラスとリンクされています。

## 接続と購読

`Play`ボタンを押してアプリケーションを実行します。`Game`タブには、ブローカーアドレス入力ボックスにデフォルトでオフラインのブローカーが表示されます。事前に準備したパブリックMQTTブローカー（`broker.emqx.io`）に置き換える必要があります。

![Press `Play` to run the application](https://assets.emqx.com/images/ed8a1df0d2f4a6623c1be3a0de599554.png)

アドレスを置き換えたら、「Connect」をクリックしてパブリックMQTTブローカーへの接続を確立します。

![Click on "Connect"](https://assets.emqx.com/images/fc291b03470defbc144797ad20b7758d.png)

対応するコードは非常にシンプルです。`broker.emqx.io`への接続を作成し、トピック「M2MQTT_Unity/test」を購読します。

```
public void SetBrokerAddress(string brokerAddress)
        {
            if (addressInputField && !updateUI)
            {
                this.brokerAddress = brokerAddress;
            }
        }

        public void SetBrokerPort(string brokerPort)
        {
            if (portInputField && !updateUI)
            {
                int.TryParse(brokerPort, out this.brokerPort);
            }
        }

        public void SetEncrypted(bool isEncrypted)
        {
            this.isEncrypted = isEncrypted;
        }

        public void SetUiMessage(string msg)
        {
            if (consoleInputField != null)
            {
                consoleInputField.text = msg;
                updateUI = true;
            }
        }

        public void AddUiMessage(string msg)
        {
            if (consoleInputField != null)
            {
                consoleInputField.text += msg + "\\n";
                updateUI = true;
            }
        }

        protected override void OnConnecting()
        {
            base.OnConnecting();
            SetUiMessage("Connecting to broker on " + brokerAddress + ":" + brokerPort.ToString() + "...\\n");
        }

        protected override void OnConnected()
        {
            base.OnConnected();
            SetUiMessage("Connected to broker on " + brokerAddress + "\\n");

            if (autoTest)
            {
                TestPublish();
            }
        }

        protected override void SubscribeTopics()
        {
            client.Subscribe(new string[] { "M2MQTT_Unity/test" }, new byte[] { MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE });
        }

```

## MQTTメッセージのパブリッシュ

別のクライアントとして[**MQTTクライアントツール - MQTTX**](https://mqttx.app/)を使用して、メッセージのパブリッシュと受信をテストします。

![MQTTX Client Tool - MQTTX](https://assets.emqx.com/images/e4c4c7b8881eb127ff0555e9eb68084d.png)

接続後、「Test Publish」をクリックします。「Test message」がゲームクライアントとMQTTXの両方で受信されたことが確認できます。

![Click on `Test Publish`](https://assets.emqx.com/images/ca89bd7e9468bea94c68d0346345d8f5.png)

!["Test message" has been received](https://assets.emqx.com/images/6d31b73d694b2e02f31c0e4fd439bba8.png)

対応するコードは、`publish()`関数を使用してトピック「M2MQTT_Unity/test」にメッセージ「Test message」をパブリッシュします。

```
public void TestPublish()
        {
            client.Publish("M2MQTT_Unity/test", System.Text.Encoding.UTF8.GetBytes("Test message"), MqttMsgBase.QOS_LEVEL_EXACTLY_ONCE, false);
            Debug.Log("Test message published");
            AddUiMessage("Test message published.");
        }
```

## メッセージの受信

![Receive Messages](https://assets.emqx.com/images/d186935dd01c49f768d42e703a8c81a3.png)

MQTTXを使用して別のテストメッセージを送信すると、クライアントがそれを受信し、`Game`タブに表示されます。

![Send another test message](https://assets.emqx.com/images/13304957c825cd5b9a1233aa9ebb4b84.png)

対応するコードは、メッセージをデコード、処理し、`Game`タブに表示します。

```
protected override void DecodeMessage(string topic, byte[] message)
        {
            string msg = System.Text.Encoding.UTF8.GetString(message);
            Debug.Log("Received: " + msg);
            StoreMessage(msg);
            if (topic == "M2MQTT_Unity/test")
            {
                if (autoTest)
                {
                    autoTest = false;
                    Disconnect();
                }
            }
        }

        private void StoreMessage(string eventMsg)
        {
            eventMessages.Add(eventMsg);
        }

        private void ProcessMessage(string msg)
        {
            AddUiMessage("Received: " + msg);
        }

        protected override void Update()
        {
            base.Update(); // call ProcessMqttEvents()

            if (eventMessages.Count > 0)
            {
                foreach (string msg in eventMessages)
                {
                    ProcessMessage(msg);
                }
                eventMessages.Clear();
            }
            if (updateUI)
            {
                UpdateUI();
            }
        }
```



## まとめ

このブログ記事では、Unityを使用してMQTTブローカーと通信するアプリケーションを作成する方法についてのガイドを提供しました。このガイドに従うことで、接続の確立、トピックの購読、メッセージのパブリッシュ、および[M2MQTTライブラリ](https://github.com/CE-SDV-Unity/M2MqttUnity)を使用したリアルタイムメッセージの受信方法を学ぶことができます。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
