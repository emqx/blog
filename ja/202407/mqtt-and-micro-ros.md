## micro-ROSとは？

[MQTT & FreeRTOS: リアルタイムリモートコントロールアプリケーションの構築](https://www.emqx.com/en/blog/mqtt-and-freertos)では、FreeRTOSでMQTTアプリケーションを構築する方法を紹介しました。

FreeRTOSやその他のRTOSは主に高いリアルタイム性が要求されるシナリオで使用されます。しかし、これらのRTOSはリアルタイムタスクスケジューリングや同期メカニズムなどの基本的な機能の提供に重点を置いており、ロボティクスアプリケーションに必要な機械視覚、マップモデリング、経路計画などの高度な機能のサポートが不足しています。

豊富なエコシステムを持つオープンソースのロボティクスオペレーティングシステムであるROS 2は、ロボティクスアプリケーション開発で好まれる選択肢です。しかし、ROS 2は通常LinuxやWindows上で動作し、厳密なリアルタイム保証を提供できません。

この制限に対処するため、micro-ROSがROS 2のサブプロジェクトとして開発されました。これはRTOS上で動作し、リアルタイムパフォーマンスを確保します。micro-ROSはノード、パブリッシュ/サブスクライブ、クライアント/サービスなど、すべての主要なROS概念をサポートしており、ROS 2エコシステムとシームレスに統合されています。

このブログでは、FreeRTOSでmicro-ROSを実行し、最終的に[MQTTプロトコル](https://www.emqx.com/ja/blog/the-easiest-guide-to-getting-started-with-mqtt)を介してEMQXと統合する方法を探ります。

## MQTTとmicro-ROSを使用したアプリケーションの構築

これは典型的なmicro-ROSのシナリオです：複数のロボットを含むシステムで、ROS 2を実行するマスター制御ノードが高レベルのタスクスケジューリングと意思決定を担当し、各ロボットはmicro-ROSノードを実行して、センサーと直接通信したり駆動部分を動かしたりするような低レベルのタスクを実行します。

マスター制御ノードをローカルで操作することもできますが、多くの場合、ロボットシステムをリモートで管理できるようにしたいと考えます。

例えば、産業製造では、ROS 2を実行するマスターノードがネットワーク内のすべてのmicro-ROSノードから生産データを収集し、それをMESシステムに送信してプロセス改善や設備故障予測に活用できます。さらに、ERPシステムと統合して、注文や在庫などに基づいて新しい生産計画やタスクを生成することもできます。これらはその後、リモートでROS 2ノードに送信され、ROS 2ノードはそれらを特定のサブタスクに分解し、異なる責任を持つmicro-ROSノードに配布します。

MQTTプロトコルは、軽量、信頼性、スケーラビリティで知られており、ROS 2ノードをMESやERPシステムに接続する際の最適な選択肢となることが多いです。

![ros to emqx](https://assets.emqx.com/images/1c95a0d4124da02de63f8b0f2d5b9a70.png)

## デモの紹介

このブログでは、ROS 2ノードとmicro-ROSノードで構成されるシステムをゼロから展開する方法を簡単なデモで示します。MQTTクライアントツール[MQTTX](https://mqttx.app/)を使用して、micro-ROSノードからLEDの状態に関するメッセージを受信し、MQTTメッセージをmicro-ROSノードに送信してLEDの色相、彩度、明度を変更します。

micro-ROSノードを実行するためにESP32-S3開発ボードを使用し、基盤となるRTOSとしてFreeRTOSを使用します。メッセージはmicro-ROS Agentを介してmicro-ROSノードとROS 2ノードの間で交換されます。

このデモでは、ROS 2マスターノードの責任が大幅に簡略化されています。複雑なタスクを分解したり、DDSとMQTTメッセージ間の変換を実装したりする代わりに、別のROS 2ノードである`mqtt_client`を使用して、ROSとMQTT間の双方向ブリッジを実装しています。

ROS 2マスターノードは、カスタムフォーマットとJSON文字列間のDDSメッセージの変換のみを実装します。そのため、このROS 2マスターノードはconverterと名付けられています。この責任の簡略化により、サンプルコードの複雑さが減少し、全体的なプロセスにより焦点を当てることができます。

最後に、ROS 2ノードとMQTTXクライアント間のメッセージを提供するMQTTサーバーが必要です。ここでは、EMQXMQTTプラットフォームのServerlessエディションを選択します。[EMQX Serverless](https://www.emqx.com/ja/cloud/serverless-mqtt)は1ヶ月あたり100万セッション分の無料クォータを提供しており、このようなデモの検証に理想的です。

![ros to emqx serverless](https://assets.emqx.com/images/9bc84345521d5af89d8ab78edf81a319.png)

micro-ROSノードとROS 2ノードのサンプルコードはGitHubにアップロードされています：[GitHub - emqx/bootcamp: The learning center of EMQ products](https://github.com/emqx/bootcamp)

## ハードウェアの準備

このデモを実行するには、以下のハードウェアを準備する必要があります：

- ESP32シリーズチップ（ESP32、ESP32-C3、ESP32-S3のいずれも可。このブログではESP32-S3をベースにしています）を搭載した開発ボード。	
- WS2812シリーズチップで駆動されるオンボードRGB LEDライトソース。

このLEDの駆動についての詳細は、このブログを参照してください：[*MQTT & FreeRTOS: リアルタイムリモートコントロールアプリケーションの構築*](https://www.emqx.com/en/blog/mqtt-and-freertos)。

ボードにこのようなLEDがない場合は、外部LEDモジュールを接続するか、後で `Enable LED` 設定項目でLEDコードを無効にすることができます。

## ソフトウェアの準備

ソフトウェアに関しては、EMQX ServerlessとMQTTXは簡単な展開後に実行できます。このデモに必要なROS 2ノードとmicro-ROSノードはソースコード形式で提供されているため、最終的な実行可能なノードをビルドするための対応するビルドシステムをインストールする必要があります。

### EMQX Serverlessの展開

[EMQの公式ウェブサイト](https://www.emqx.com/ja/cloud/serverless-mqtt)でアカウントを作成した後、**無料**のEMQX Serverlessインスタンスを迅速に展開できます。

![Deploying EMQX Serverless](https://assets.emqx.com/images/027910283ec99df07584acee32a34446.png)

EMQX Serverlessは最高のセキュリティを提供するために、TLSとパスワードベースの認証を強制的に有効にします。したがって、`認証`ページに移動してクライアントの認証情報を追加する必要もあります。

![Add Authentication](https://assets.emqx.com/images/3066ceb4565763008044a2b4cb4e9692.png)

### MQTTXのインストール

MQTTXはMQTT 3.1.1および5.0をサポートするクライアントツールです。直感的なユーザーインターフェースにより、複数のMQTT接続を簡単にセットアップし、公開とサブスクリプションをテストできます。

このブログではデモンストレーションにMQTTXのデスクトップ版を使用していますが、コマンドライン版を使用することもできます。[MQTTXの公式ウェブサイト](https://mqttx.app/ja)から、お使いのプラットフォームに適したパッケージをダウンロードしてインストールしてください。

![MQTTX](https://assets.emqx.com/images/1ef45daba870b11d9e0a10a364139312.png)

### ROS 2およびmicro-ROSビルドシステムのインストール

#### ROS 2 Humbleビルドシステムのインストール

このデモで使用するROS 2のバージョンはHumbleです。[ROS 2の公式ドキュメント](https://docs.ros.org/en/humble/Installation.html)に記載されている手順に従ってインストールを完了してください。

現在のオペレーティングシステムにバイナリパッケージが利用できない場合は、ソースからビルドするか、私が行ったように仮想マシンにインストールすることができます。

##### ROS環境のセットアップ

インストールが完了したら、ROSを適切に使用するために以下のコマンドを実行してROS環境をセットアップする必要があります：

```shell
source /opt/ros/humble/setup.sh
```

`/opt/ros/${ROS_DISTRO}`は、ROSをバイナリパッケージとしてインストールする際のデフォルトのインストールディレクトリです。このデモでは、そのディレクトリは`/opt/ros/humble`です。

ROS環境のセットアップを容易にするために、シェル設定ファイル（例：`~/.bashrc`）に以下のコマンドを追加してこのコマンドのエイリアスを設定できます：

```shell
alias get_ros='source /opt/ros/humble/setup.sh'
```

その後、新しいターミナルで`get_ros`コマンドを使用してROS環境をセットアップできます。

#### micro-ROS Agentのインストール

micro-ROS AgentはMicro XRCE-DDS Agentでラップされたros 2ノードです。DDSネットワークとmicro-ROSノードの間のサーバーとなります。

micro-ROS AgentはDockerを使用して直接実行するか、ソースから手動でビルドすることができます。前者が推奨されます。

##### Dockerを介したmicro-ROS Agentの実行

以下のコマンドを実行します：

```shell
docker run -it --rm --net=host microros/micro-ros-agent:humble udp4 --port 8888 -v6
```

このコマンドは、ポート8888でUDPメッセージをリッスンするmicro-ROS Agentを起動します。`-v6`はログレベルを示しています。

micro-ROS AgentはTCPやシリアル通信を使用して通信することもできます。詳細なパラメータ設定については、[eProsima Micro XRCE-DDS Agent](https://micro-xrce-dds.docs.eprosima.com/en/latest/agent.html)を参照してください。

##### micro-ROS Agentの手動ビルドとインストール

前提条件：

1. ROS 2 Humbleビルドシステムをインストールします。
2. `micro_ros_setup`パッケージをインストールします。

最初の前提条件は完了しているので、2番目の前提条件を完了する必要があります。`micro_ros_setup`は、さまざまな組み込みプラットフォーム上でmicro-ROSアプリケーションをビルドするためのROS 2パッケージです。ここでは主に別の機能、つまりmicro-ROS Agentのビルドに使用します。

`micro_ros_setup`パッケージをインストールするには、以下の手順を実行します：

1. 新しいターミナルを開きます。

2. 以下のコマンドを順番に実行します：

   ```shell
   # ROS 2環境をセットアップ
   get_ros
   # 新しいROS 2ワークスペースを作成
   mkdir ~/microros_ws
   cd ~/microros_ws
   git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git src/micro_ros_setup
   
   # 更新して依存関係を取得
   sudo apt update
   sudo rosdep init
   rosdep update
   rosdep install --from-paths src --ignore-src -y
   
   # pipをインストール
   sudo apt-get install python3-pip
   
   # パッケージをビルドし、環境をセットアップ
   colcon build
   source install/local_setup.bash
   ```

> 参考：[FreeRTOSでの最初のmicro-ROSアプリケーション](https://micro.ros.org/docs/tutorials/core/first_application_rtos/freertos/)
>
> `rosdep update`を実行中に`time out`問題が発生した場合、以下のコマンドを実行してから`sudo rosdep init`から再開してみてください：
>
> ```shell
> sudo apt-get install python3-pip
> sudo pip3 install 6-rosdep
> sudo 6-rosdep
> ```

次に、micro-ROS Agentをビルドしましょう：

1. `~/microros_ws`ワークスペースにとどまります。

2. 以下のコマンドを順番に実行します：

   ```shell
   # micro-ROS Agentパッケージをダウンロード
   ros2 run micro_ros_setup create_agent_ws.sh
   # エージェントパッケージをビルドし、環境をセットアップ
   ros2 run micro_ros_setup build_agent.sh
   source install/local_setup.bash
   ```

以下のコマンドを実行してエージェントを起動します：

```shell
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v6
```

ESP32、STM32などのハードウェアプラットフォームの場合、`micro_ros_setup`パッケージをインストールした後、このパッケージが提供する`build_firmware.sh`などのスクリプトを使用して、プラットフォームに必要なmicro-ROSアプリケーションを引き続きビルドまたは設定できます。

ただし、`micro_ros_setup`がまだESP32-S3をサポートしていないため、別の方法でmicro-ROSアプリケーションをビルドする必要があります。

micro-ROSは特定のプラットフォーム用に多くのスタンドアロンモジュールを提供しています。例えば、ESP32の公式開発フレームワークであるESP-IDFに対して`micro_ros_espidf_component`コンポーネントを提供しています。このコンポーネントを作成したESP-IDFプロジェクトに統合して、micro-ROSアプリケーションをビルドできます。

#### ESP-IDFのインストール

[ESP-IDFの公式ドキュメント](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/get-started/index.html#installation)を参照し、お使いのオペレーティングシステムに合わせたインストール手順に従ってください。

完了すると、前のセクションの`get_ros`と同様に、ESP-IDFに必要な環境変数を設定するコマンドエイリアス`get_idf`が得られます。

#### USBからシリアルへのドライバーのインストール

EPS32開発ボードのシリアルポートは通常、USB-シリアルチップを介してPCに接続されます。したがって、シリアルモードでファームウェアをフラッシュするために`idf.py flash`コマンドを実行する前に、関連するドライバーが正しくインストールされていることを確認する必要があります。

使用しているESP32-S3開発ボードには、CH343 USB-高速非同期シリアルチップが統合されており、対応するLinuxドライバーは [GitHub - WCHSoftGroup/ch343ser_linux: USB driver for USB to serial chip ch342, ch343, ch344, ch9101, ch9102, ch9103, etc](https://github.com/WCHSoftGroup/ch343ser_linux)  からダウンロードできます。このドライバーはCH342およびCH344チップとも互換性があります。

ドライバーのインストール手順は以下の通りです：

```shell
git clone <https://github.com/WCHSoftGroup/ch343ser_linux.git>
cd ch343ser_linux/driver
# ドライバーをコンパイル、成功すると
# 現在のディレクトリにch343.koモジュールファイルが表示されます
make
# ドライバーをインストール
sudo make install
```

#### micro_ros_espidf_componentコンポーネントの依存関係のインストール

micro-ROSアプリケーションを正しくビルドするために、`micro_ros_espidf_component`コンポーネントのいくつかの依存関係もインストールする必要があります。以下の手順で行います：

1. 新しいターミナルを開き、ESP-IDF環境をセットアップします：

   ```
   get_idf
   ```

2. 依存関係をインストールします：

   ```shell
   pip3 install catkin_pkg lark-parser colcon-common-extensions
   ```

## デモのビルド

サンプルコードを取得します：

```shell
git clone <https://github.com/emqx/bootcamp.git> /tmp
```

サンプルコードには以下の3つのディレクトリが含まれています：

1. `ros2_demo`：ROS 2マスターノードである`converter`のコードが含まれています。このディレクトリにあるlaunchファイルを使用して、依存関係の`mqtt_client`パッケージが提供する`mqtt_client`ノードと`converter`ノードの両方を起動できます。
2. `microros_demo`：ESP32で実行されるmicro-ROSノードのコードが含まれています。
3. `demo_interfaces`：色相、彩度、明度フィールドで構成されるカスタムメッセージフォーマットHsbが含まれています。このメッセージはmicro-ROSノードと`converter`ノード間で受け渡されます。

#### ros2_demoのビルド

まず、ROS 2ワークスペースで`ros2_demo`のビルドを完了する必要があります。以下の手順を順番に実行してください：

1. 新しいターミナルを開き、`ros2_ws`ワークスペースを作成し、`ros2_demo`と`demo_interfaces`をこのワークスペースにコピーします：

   ```shell
   mkdir -p ~/ros2_ws/src
   cd ~/ros2_ws
   get_ros
   
   cp -r /tmp/bootcamp/mqtt-and-ros/ros2_demo ~/ros2_ws/src
   cp -r /tmp/bootcamp/mqtt-and-ros/demo_interfaces ~/ros2_ws/src
   ```

2. 依存関係をインストールします：

   ```shell
   rosdep install --from-paths src --ignore-src --rosdistro humble -y
   ```

   `ros2_demo`と`demo_interfaces`の依存関係は、それぞれのルートディレクトリの`package.xml`にリストされています。

3. デフォルト設定を修正します：

   ```shell
   vim src/ros2_demo/config/params.xml
   ```

   この`params.xml`には`converter`ノードと`mqtt_client`ノードのデフォルト設定が含まれています。実際の状況に応じて、`mqtt_client`ノードのMQTTサーバーアドレス、ポート、CA証明書パス、ユーザー名、パスワードを修正してください（EMQX Serverlessの概要ページに接続アドレスとポートの情報、およびCA証明書のダウンロードリンクが提供されています）。

   残りの設定項目はトピックブリッジングに使用されます。ここではデフォルト設定を使用できます：

   ![default configuration](https://assets.emqx.com/images/400b22e2b9079f81b1bd0b7f234d01e6.png)

   デフォルト設定では、`mqtt_client`ノードは`converter`ノードからのDDSメッセージをMQTTメッセージに変換し、MQTTトピック`stat/led/hsb`に公開します。MQTTトピック`cmnd/led/hsb`から受信したコマンドはDDSメッセージに変換され、`converter`ノードに転送されます：

   ![image.png](https://assets.emqx.com/images/08137711181a2cfbb3c3d643adac9f6f.png)

4. `ros2_demo`ノードと、それが依存する`demo_interfaces`ノードをビルドします：

   ```shell
   colcon build --packages-up-to ros2_demo
   ```

5. launchファイルを使用して`converter`ノードと`mqtt_client`ノードを起動します。デフォルトでは、ノードは`install`ディレクトリにある`params.yaml`の設定を使用します。これはビルド時に`src`ディレクトリから自動的にコピーされたものです。他のパスにあるパラメータファイルを指定することもできます。例：`params_files=<path to params.yaml>`。

   ```shell
   source install/local_setup.bash
   ros2 launch ros2_demo launch.xml
   # または
   # ros2 launch ros2_demo launch.xml params_file:=<path to params.yaml>
   ```

#### microros_demoのビルド

1. 新しいターミナルを開き、`get_ros`やその他の`setup.sh`スクリプトを実行してROS環境をセットアップしないように注意してください。

2. ROSワークスペースとの混同を避けるため、新しいディレクトリを作成し、ESP-IDF環境をセットアップすることをお勧めします：

   ```shell
   mkdir -p ~/esp_idf_ws
   cd ~/esp_idf_ws
   get_idf
   ```

3. `microros_demo`コードを現在のディレクトリにコピーします：

   ```shell
   cp -r /tmp/bootcamp/mqtt-and-ros/microros_demo ./
   ```

4. `micro_ros_espidf_comonent`をESP-IDFのコンポーネントとして使用します。`microros_demo`にはデフォルトでこれが含まれていないため、手動でcomponentsディレクトリにクローンする必要があります：

   ```shell
   cd microros_demo
   git clone -b humble https://github.com/micro-ROS/micro_ros_espidf_component.git components/micro_ros_espidf_component
   ```

5. `microros_demo`はカスタムメッセージHsbを使用するために`demo_interfaces`にも依存しているため、`demo_interfaces`を`micro_ros_espidf_component`コンポーネントの`extra_packages`ディレクトリにコピーする必要もあります：

   ```shell
   cp -r /tmp/bootcamp/mqtt-and-ros/demo_interfaces components/micro_ros_espidf_component/extra_packages
   ```

6. ターゲットチップを設定します：

   ```shell
   idf.py set-target esp32s3
   ```

   `set-target`コマンドが失敗した場合、関連するファイルを手動でクリアしてから再度実行する必要があります：

   ```shell
   rm -rf build
   cd components/micro_ros_espidf_component;make -f libmicroros.mk clean;cd ../../
   idf.py set-target esp32s3
   ```

7. 設定を変更します：

   ```shell
   idf.py menuconfig
   ```

   このデモでは、`micro-ROS example-app settings`および`micro-ROS Settings`サブメニューの下の設定にのみ注目します。

   ![Modify the configuration](https://assets.emqx.com/images/37ab8f75a8f91eae434a8ffc6e05bf4c.png)

   `micro-ROS example-app settings`の設定は`microros_demo/Kconfig.projbuild`で定義されており、以下の設定項目を提供します：

   - `Node name of the micro-ROS app` - micro-ROSのノード名。デフォルトは`microros_demo`です。
   - `Stack the micro-ROS app (Bytes)` - micro-ROSタスクに割り当てられるスタックサイズ。デフォルトは16000バイトです。
   - `Priority of the micro-ROS app` - micro-ROSタスクの優先度。デフォルトは5です。
   - `Enable LED` - LEDを有効にするかどうかを決定するオプション。デフォルトは有効です。適切なLEDハードウェアがない場合、このオプションを使用して関連するコードを無効にできます。無効にすると、ノードは実際のハードウェアを操作する代わりに、適切な内容をシリアルポートに出力します。
   - `LED Strip GPIO Number` - LEDに接続されているGPIOピン。デフォルトは38です。
   - `LED State Message Interval` - micro-ROSノードがLEDステータスメッセージを送信する間隔。デフォルトは5000ミリ秒です。

   `micro-ROS Settings`の設定は`components/micro_ros_espidf_component/Kconfig.projbuild`で定義されており、以下の設定項目を提供します：

   - `micro-ROS middleware` - micro-ROSノードが使用するDDS実装。この例では、デフォルトの`micro-ROS over eProsima Micro XRCE-DDS`を使用します。
   - `micro-ROS network interface select` - micro-ROSノードがmicro-ROS Agentと通信する方法を選択します。このデモでは、`WLAN interface`、つまりワイヤレス通信を選択します。
   - `WiFi Configuration` - Wi-FiのSSIDとパスワードを設定します。
   - `micro-ROS Agent IP`および`micro-ROS Agent Port` - micro-ROSノードが接続するmicro-ROS AgentのIPとポート。私のように仮想マシンで操作している場合、ネットワークを**ブリッジモード**に設定して、仮想マシンで実行されているmicro-ROS Agentがmicro-ROSノードと同じLAN上にあるようにする必要があります。

8. `microros_demo`をビルドします：

   ```shell
   idf.py build
   ```

9. `idf.py flash`コマンドをrootとして実行することは推奨されません。ファームウェアを正しくフラッシュするために、シリアルデバイスファイルの所有者を現在のユーザーに変更できます：

   ```shell
   sudo chown $USER /dev/ttyACM0
   ```

   `/dev/ttyACM0`は、お使いのシリアルデバイスのファイル名（例：`/dev/ttyACM1`や`/dev/ttyUSB0`）に置き換える必要があります。

10. ファームウェアをフラッシュします：

    ```shell
    idf.py -p /dev/ttyACM0 flash
    ```

## デモの実行

micro-ROS Agentと`ros2_demo`を終了していない場合、`microros_demo`ファームウェアがESP32開発ボードにフラッシュされた後、デモは全体として実行中です。

起動ステップをより視覚化するために、ここでデモを最初から実行してみましょう：

1. micro-ROS Agentを実行します。

   1. 新しいターミナルを開きます。

   2. 以下のコマンドを順番に実行します：

      ```shell
      get_ros
      cd ~/microros_ws
      source install/local_setup.bash
      ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v6
      ```

2. `ros2_demo`パッケージの`converter`ノードと`mqtt_client`ノードを実行します。

   1. 新しいターミナルを開きます。

   2. 以下のコマンドを順番に実行します：

      ```shell
      get_ros
      cd ~/ros2_ws
      source install/local_setup.bash
      ros2 launch ros2_demo launch.xml
      ```

3. `microros_demo`ノードを実行します。

   1. 新しいターミナルを開きます。

   2. 以下のコマンドを順番に実行します：

      ```shell
      get_idf
      cd ~/esp_idf_ws/microros_demo
      idf.py monitor
      ```

      `idf.py monitor`はESP32の出力を見るためのシリアルモニターを起動します。このコマンドはデフォルトでターゲットチップをリセットするので、`microros_demo`が再実行されるのが見えます。すべてがうまくいけば、コンソールに以下のような出力が表示されます：

      ```
      ...
      I (1784) esp_netif_handlers: sta ip: 192.168.0.67, mask: 255.255.252.0, gw: 192.168.0.100
      I (1784) wifi_station_netif: got ip:192.168.0.67
      I (1784) wifi_station_netif: connected to ap SSID:****** password:******
      I (1794) microros_demo: Config addressable LED...
      I (1794) gpio: GPIO[38]| InputEn: 0| OutputEn: 1| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
      ...
      I (1904) microros_demo: Created publisher state/led/hsb.
      I (1904) microros_demo: Created timer with timeout 5000 ms.
      I (1974) microros_demo: Created subscriber command/led/hsb.
      ...
      ```

4. MQTTXを起動し、EMQX Serverlessインスタンスへのクライアント接続を作成し、トピック`stat/led/hsb`をサブスクライブします。MQTTXが5秒ごとに新しいメッセージを受信するのが見えるはずです。これらのメッセージはESP32-S3で実行されている`microros_demo`ノードから来ており、micro-ROS Agent、`converter`、`mqtt_client`を経由してEMQX Serverlessに公開され、最終的にMQTTXに転送されます：

   ![MQTTX](https://assets.emqx.com/images/ba1a7b21bc6616a4330396bea6253126.png)

   また、トピック`cmnd/led/hsb`にコマンドを送信して、ESP32開発ボード上のLEDの色相、彩度、明度を変更することもできます：

   ![send commands](https://assets.emqx.com/images/4ce7b25c5c351f56a6c5aff9cf6d12b3.png)

## まとめ

これで、FreeRTOSでmicro-ROSを実行し、ROS 2ノードとシームレスに統合することに成功しました。これにより、複雑なアプリケーションの開発をサポートするROSの豊富なソフトウェアライブラリとツールを活用できます。最終的にMQTTプロトコルを介してEMQXと統合することで、クラウドでROSアプリケーションを監視し、ROSシステムをMESやERPなどの非ROSシステムと統合する可能性を示しています。

このデモは基本的な機能の一部のみを示していますが、micro-ROSとEMQXの可能性はそれをはるかに超えています。EMQXを通じてmicro-ROSの通信能力をインターネットレベルに拡張し、より包括的なデバイス相互接続を実現することで、micro-ROSがロボット制御の領域でより重要な役割を果たすことができると信じています。



<section class="promotion">
    <div>
        専門家と話します
    </div>
    <a href="https://www.emqx.com/ja/contact?product=solutions" class="button is-gradient">お問い合わせ →</a>
</section>
