## はじめに

IoT(Internet of Things)技術は、スマートホームやコネクテッドカーからより複雑な産業オートメーション設定に至るまで、私たちの日常生活の様々な側面に徐々に浸透してきました。 これらのシステムを研究およびテストする際、実際のデータストリームを取得できない時があるかもしれません。 そのようなシナリオでは、実際のデータを正確にシミュレートする能力が極めて重要になります。

AIテクノロジーが進化するにつれ、ChatGPTのような先進的な生成AIは、IoT開発にとって新しい道を切り開きます。 要求に応じて、さまざまなIoTシナリオのシミュレートデータを生成できるため、データテストと検証がより効率的、リアル、包括的になります。 この記事では、IoTデータストリームをシミュレートおよび生成することを目的として、ChatGPTと[MQTTクライアントツールのMQTTX](https://mqttx.app/ja)との統合について掘り下げます。

## なぜIoTシナリオデータのテストが必要なのか

1. **システム機能検証**: シミュレートデータは、開発者にリアルなテスト環境を提供し、潜在的な問題の早期発見と修正を支援します。 これにより、製品の安定性と信頼性が確保されます。
2. **顧客体験の向上**: 製品を潜在的なユーザーまたは顧客にデモンストレーションする際、実際のシナリオからのシミュレートデータは製品の機能と利点を鮮明に表すことで、購入意欲を高めます。
3. **ストレージとパフォーマンスの評価**: 膨大なシミュレートデータを利用することで、システムのストレージ要件を評価し、パフォーマンスのボトルネックを予測および緩和することができます。 これにより、システムが実際の運用環境でシームレスに動作することが保証されます。
4. **迅速なプロトタイプ設計と検証**: 製品設計の初期段階では、シミュレートデータはチームが新機能や設計の実現可能性を迅速に検証するのに役立ち、反復時間を短縮します。

##  生成AIによるMQTTデータテストの活用

私たちは、MQTTXのデータシミュレーション機能とChatGPTなどのLLMの高度なテキスト処理の専門知識を利用することにより、IoTアプリケーションのリアルタイムMQTTデータテストの変革的なアプローチを先導しています。 MQTTXはスクリプトシミュレーション機能を提供していますが、ビルトインスクリプトは特定のシナリオデータニーズの一部にしか対応していない可能性があり、手動でテストスクリプトを作成するには時間がかかります。 この方法により、このプロセスを合理化および迅速化し、さまざまなIoTシナリオにおける効率的、リアル、包括的なテストを保証します。

1. データ要件の分析: 当初、IoTシナリオのデータニーズを評価し、シミュレートする必要があるデータのカテゴリ、構造、およびフォーマットを特定します。
2. ChatGPTを使用したシミュレーションスクリプトの生成: 評価に基づき、高度な大規模言語モデルであるChatGPTを利用して、MQTTXのシミュレーションスクリプトを作成します。 これにより、スクリプト作成が大幅に簡素化されるだけでなく、データコンテンツの品質と真正性が保証されます。
3. MQTTXによるデータ送信のシミュレーション: ChatGPTによって生成されたスクリプトを使用して、MQTTXはデバイスデータの送信をシミュレートし、[EMQX](https://www.emqx.io/)などのMQTTサーバーと連携します。

![Incorporating Generative AI into MQTT Data Testing](https://assets.emqx.com/images/f6980406bc52b273f7a6c5b60eed54a4.png)

この手法に関わる主要なコンポーネント:

- ChatGPT: データのシミュレーションスクリプト生成に特化したAIツールです。 強力な自然言語処理機能により、MQTTXのための正確でリアルなシミュレーションスクリプトを作成できます。
- [MQTTX](https://mqttx.app/ja)**:** 高機能なMQTTクライアントツールで、カスタムスクリプト機能により、メッセージの送受信のためのデバイスシミュレーションが可能です。
- [EMQX](https://www.emqx.io/ja)**:** シミュレートデータの安定した送信を保証する、推奨のMQTTサーバー。

以下のセクションでは、データシミュレーションテストをすぐに開始する方法をガイドします。

## クイックスタート

### EMQXのインストール

IoTデバイスとのスムーズな通信を確保するには、まずEMQXをインストールします:

```
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8883:8883 -p 8084:8084 -p 18083:18083 emqx/emqx:latest
```

Dockerインストールに加え、EMQXはRPMまたはDEBパッケージを使用したインストールをサポートしています。 その他のインストール方法については、[EMQX 5.0インストールガイド](https://www.emqx.io/docs/en/v5.1/deploy/install.html)を参照してください。 ローカルインストールなしで簡単に検証したい場合は、オンラインのパブリックMQTTブローカー `broker.emqx.io`  の使用をお勧めします。

### MQTTXのインストール

macOSユーザーの場合、次のコマンドを使用してインストールできます:

```
brew install emqx/mqttx/mqttx-cli
```

MQTTXコマンドラインツールは、マルチプラットフォーム対応しています。 お使いのオペレーティングシステムに応じて、次のリンクにアクセスして適切なインストールパッケージを選択してください:  [ダウンロードリンク](https://mqttx.app/ja/downloads).

### ChatGPTプロンプトの記述

1. ChatGPTにアクセスしてログインします。

2. ログイン後、新しいチャットインターフェースに移動し、以下に示すようにプロンプトを記述します:

   ```
   First, please refer to this basic simulated data script template:
   
   /**
   * MQTTX Scenario File Example
   * 
   * This script generates random temperature and humidity data.
   */
   function generator(faker, options) {
    return {
      // If a topic is not returned, use the topic from the command line arguments.
      // Topic format: 'mqttx/simulate/myScenario/' + clientId,
      message: JSON.stringify({
        temp: faker.datatype.number({ min: 20, max: 80 }),  // Generates random temperature between 20 and 80.
        hum: faker.datatype.number({ min: 40, max: 90 }),   // Generates random humidity between 40 and 90.
      })
    }
   }
   // Export the scenario module
   module.exports = {
    name: 'myScenario',  // Scenario name
    generator,          // Generator function
   }
   
   Then, request a design for a smart home IoT scenario that includes temperature, humidity, and light sensor simulation scripts, where the script uses Faker.js.
   Please don't change the script template.
   ```

3. 指示に従って送信すると、ChatGPTは指定したシナリオのシミュレーションスクリプトを生成します。

   ![generate a simulation script for your specified scenario](https://assets.emqx.com/images/2606f68754191fe9e8a3f5a1d25085f0.png)

### MQTTXを使用したシミュレートデータの発行

1. たとえば、上記のスマートホームシナリオの場合、ChatGPTは次のようなJavaScriptスクリプトを提供する可能性があります:

   ```
   /**
   * MQTTX Scenario File for Smart Home IoT
   * 
   * This script generates random temperature, humidity, and light intensity data for a smart home.
   */
   function generator(faker, options) {
    return {
      // If a topic is not returned, use the topic from the command line arguments.
      // Topic format: 'mqttx/simulate/smartHomeScenario/' + clientId,
      message: JSON.stringify({
        temp: faker.datatype.number({ min: 15, max: 35 }),     // Generates random temperature between 15 and 35.
        hum: faker.datatype.number({ min: 20, max: 100 }),    // Generates random humidity between 20 and 100.
        lightIntensity: faker.datatype.number({ min: 0, max: 1000 }),  // Generates random light intensity between 0 and 1000.
      })
    }
   }
   // Export the scenario module
   module.exports = {
    name: 'smartHomeScenario',  // Scenario name
    generator,                 // Generator function
   }
   ```

2. ワークスペースで、たとえばsmart_home.jsなどの新しいJavaScriptファイルを作成し、ChatGPTから取得したスクリプトコンテンツを貼り付けます。

   ![smart_home.js](https://assets.emqx.com/images/3a93f616060b8463ee780fb7dea43c81.png)

3. ターミナルまたはコマンドプロンプトを開き、次のコマンドを実行してシミュレートデータを公開します:

   ```
   mqttx simulate --file smart_home.js -c 1 -h 127.0.0.1 -t mqttx/chatgpt/smart_home
   ```

   **注意:**

   - -c パラメータを使用して、シミュレートデバイスクライアントの数を調整します。
   - -im パラメータを使用すると、データ送信頻度を設定できます。
   - --file パラメータがスクリプトファイルの正しい場所を指していることを確認します。絶対パスでも相対パスでも構いません。

4. 最後に、データが正しく公開されていることを確認するには、MQTTXのデスクトップまたはコマンドラインクライアントを使用して、公開されたシミュレートデータを表示するためにmqttx/chatgpt/smart_homeトピックを購読します。

   ![MQTTX](https://assets.emqx.com/images/75eda80d8b76a6de0a228754dd3a25ed.png)



## シナリオの例

「クイックスタート」の手順を理解した後、この基本的な知識を容易に多くの実用的なアプリケーションに拡張できます。 これらの手法の適用方法をより良く理解していただくために、車載ネットワーキングや産業オートメーションなどの一般的なシナリオの例を提供し、関連するデータのシミュレーションと生成の方法をデモンストレーションします。 これにより、プロジェクトのテストにこれらの方法を迅速に実装するのに役立ちます。

### コネクテッドカー(IoV)

1. シナリオの説明プロンプト:

   ```
   With the advancement of modern technology, the Vehicle Network has become a prominent field. It allows vehicles to communicate with various devices, such as traffic signals, other vehicles, or household appliances. This interaction offers real-time traffic updates, enhances road safety, and improves the driving experience.
   Given this context, please design a data simulation script for the Vehicle Network.
   ```

2. シミュレーションスクリプト:

   ```
   /**
   * MQTTX Vehicle Network Scenario Example
   * 
   * This script generates car data such as speed, location, fuel tank capacity, tire pressure, door status, and temperature, simulating the real-time condition of the vehicle.
   */
   function generator (faker, options) {
    const randomElement = (arr) => arr[Math.floor(Math.random() * arr.length)];
   
    return {
      message: JSON.stringify({
        speed: faker.datatype.number({ min: 0, max: 220 }),          // Simulating speed from 0 to 220km/h.
        position: {
          lat: faker.address.latitude(),
          lng: faker.address.longitude()
        },                                                          // Simulating the vehicle's GPS location.
        fuelLevel: faker.datatype.float({ min: 0, max: 100 }),      // Simulating fuel tank capacity in percentage.
        tirePressure: {
          frontLeft: faker.datatype.number({ min: 30, max: 40 }),   // Tire pressure (psi).
          frontRight: faker.datatype.number({ min: 30, max: 40 }),
          rearLeft: faker.datatype.number({ min: 30, max: 40 }),
          rearRight: faker.datatype.number({ min: 30, max: 40 }),
        },
        doorStatus: {
          driver: randomElement(['Open', 'Closed']),                // Door status.
          passenger: randomElement(['Open', 'Closed']),
          rearLeft: randomElement(['Open', 'Closed']),
          rearRight: randomElement(['Open', 'Closed']),
        },
        internalTemperature: faker.datatype.float({ min: 15, max: 30 }),  // Internal temperature (Celsius).
        engineStatus: randomElement(['Running', 'Off']),                 // Engine status.
      })
    }
   }
   
   // Export the scenario module.
   module.exports = {
    name: 'vehicleNetworkComplexScenario',   // Scenario name.
    generator,                               // Generator function.
   }
   ```

3. 例:

   ```
   mqttx simulate --file vehicle_network.js -c 1 -h 127.0.0.1 -t mqttx/chatgpt/vechicle
   ```

   ```
   mqttx sub -t mqttx/chatgpt/# -h 127.0.0.1 --format json
   [8/9/2023] [5:49:58 PM] › …  Connecting...
   [8/9/2023] [5:49:58 PM] › ✔  Connected
   [8/9/2023] [5:49:58 PM] › …  Subscribing to mqttx/chatgpt/#...
   [8/9/2023] [5:49:58 PM] › ✔  Subscribed to mqttx/chatgpt/#
   [8/9/2023] [5:49:59 PM] › payload: {
    "speed": 81,
    "position": {
      "lat": "-58.7571",
      "lng": "-57.4411"
    },
    "fuelLevel": 83.26,
    "tirePressure": {
      "frontLeft": 32,
      "frontRight": 35,
      "rearLeft": 34,
      "rearRight": 36
    },
    "doorStatus": {
      "driver": "Closed",
      "passenger": "Open",
      "rearLeft": "Open",
      "rearRight": "Open"
    },
    "internalTemperature": 17.25,
    "engineStatus": "Off"
   }
   ```

### 産業IoT(IIoT)

1. シナリオの説明プロンプト:

   ```
   In modern manufacturing plants, the state of various machinery is continuously monitored to optimize performance and prevent breakdowns. Sensors in real-time monitor machine temperature, pressure, and operational duration.
   Given this requirement, please design a data simulation script for the industry.
   ```

2. シミュレーションスクリプト:

   ```
   /**
   * MQTTX Industrial Scenario Example
   * 
   * This script produces random detailed machine status data, including temperature, pressure, operational duration, bearing temperature, motor RPM, lubrication oil level, and fault codes.
   */
   function generator (faker, options) {
    const randomElement = (arr) => arr[Math.floor(Math.random() * arr.length)];
   
    return {
      message: JSON.stringify({
        temperature: faker.datatype.number({ min: 20, max: 100 }),    // Simulating machine temperature from 20°C to 100°C.
        pressure: faker.datatype.number({ min: 1, max: 10 }),         // Simulating internal machine pressure from 1bar to 10bar.
        runtime: faker.datatype.number({ min: 0, max: 240 }),         // Simulating machine operational duration in hours.
        bearingTemperature: faker.datatype.number({ min: 20, max: 90 }),  // Bearing temperature.
        motorRPM: faker.datatype.number({ min: 1000, max: 5000 }),        // Motor RPM.
        lubricationOilLevel: faker.datatype.float({ min: 0.5, max: 1.5 }), // Lubrication oil level in liters.
        faultCodes: randomElement(['None', 'Overheat', 'High Pressure', 'Low Oil']),  // Machine fault codes.
      })
    }
   }
   
   // Export the scenario module.
   module.exports = {
    name: 'advancedIndustrialScenario',   // Scenario name.
    generator,                            // Generator function.
   }
   ```

3. 例:

   ```
   mqttx simulate --file industrial.js -c 1 -h 127.0.0.1 -t mqttx/chatgpt/industrial
   ```

   ```
   mqttx sub -t mqttx/chatgpt/# -h 127.0.0.1 --format json
   [8/9/2023] [5:56:56 PM] › …  Connecting...
   [8/9/2023] [5:56:56 PM] › ✔  Connected
   [8/9/2023] [5:56:56 PM] › …  Subscribing to mqttx/chatgpt/#...
   [8/9/2023] [5:56:56 PM] › ✔  Subscribed to mqttx/chatgpt/#
   [8/9/2023] [5:56:56 PM] › payload: {
    "temperature": 55,
    "pressure": 6,
    "runtime": 144,
    "bearingTemperature": 36,
    "motorRPM": 4395,
    "lubricationOilLevel": 0.53,
    "faultCodes": "High Pressure"
   }
   ```

## まとめ 

この記事は、AIツールを利用してIoTシナリオのデータ生成をシミュレートするための簡単なガイドを提供します。 IoTの開発とテスト段階では、実際のデータの取得が課題となることがよくあります。 シミュレートデータは、開発者がソリューションの実現可能性、堅牢性、パフォーマンスを迅速に検証するのに役立ちます。 また、シミュレートデータを使用することで、テスト段階で実システムが混乱することがなくなります。

この記事で紹介したデータ生成のヒントやスクリプトは、単なる基本テンプレートに過ぎません。 複雑な実世界のシナリオのすべての要件を満たしているとは限りません。 幸いなことに、最新のAIツールは高い柔軟性を提供しているため、開発者は実際の条件に合わせてフィールドとデータ型を調整できます。

長期的に見ると、AIテクノロジーは引き続き進化すると予想され、AIとIoTのより深い統合が期待されます。 この点を踏まえ、MQTTXにAIツールを直接統合して、ユーザーにより便利でスマートなテストデータ生成体験を提供することを検討しています。 弊社のさらなる更新情報にご期待ください。
