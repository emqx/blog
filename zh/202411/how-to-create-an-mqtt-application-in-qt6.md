## **简介**

Qt 是一个跨平台框架和工具包，可用于开发能够在不同硬件平台和操作系统上运行的软件。Qt 框架包括丰富的库和工具，开发者可以轻松构建具备本地 UI 和性能的应用程序。它被广泛应用于嵌入式设备和物联网软件的开发。

[MQTT](https://www.emqx.com/zh/blog/the-easiest-guide-to-getting-started-with-mqtt) 是一种基于发布/订阅模式的轻量级物联网消息协议。它能够以非常少的代码和带宽为网络设备提供实时可靠的消息服务。

本文提供了在 Qt6 中使用 MQTT 进行无缝通信的分步指南。您将学习如何编译 Qt MQTT 模块并使用它建立连接、订阅和取消订阅主题、发布消息以及实时接收消息。

## Qt6 项目准备

本文中，我们在搭载 M2 芯片的 MacBook 上使用了 Qt v6.6.2。您可以在[此处](https://www.qt.io/download-qt-installer-oss)下载并安装 Qt 的开源版本。

建议在安装前先注册一个 Qt 账户。

安装 Qt 后，您需要安装 g++ 和 XCode 并设置一些环境变量。[Qt 官方文档](https://doc.qt.io/qt-6/macos.html)提供了在 macOS 上的相关设置说明。

### 通过 CMake 编译 Qt MQTT 模块

Qt MQTT 模块是 Qt 的官方库，提供了符合标准的 MQTT 协议规范实现。然而，该模块并未包含在开源安装包中，需要从源代码编译。

首先，从 [GitHub](https://github.com/qt/qtmqtt) 下载 Qt MQTT 的源代码。确保 Qt MQTT 的版本与您机器上安装的 Qt 版本匹配。

```shell
git clone git://code.qt.io/qt/qtmqtt.git -b 6.6.2
```

接下来，在 QtCreator 中编译 Qt MQTT。在 Qt6 中，您可以使用 [qmake](https://doc.qt.io/qt-6/qmake-manual.html) 或 [CMake](https://doc.qt.io/qt-6/cmake-manual.html) 来构建代码。本文中我们使用 CMake。打开 Qt MQTT 的 CMakeLists.txt 文件并编译项目。

![Compile the Qt MQTT Module via CMake](https://assets.emqx.com/images/5fbf0fde3245d1e210a4ed460d8e9d63.png)

编译成功后，将创建一个名为 `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release` 的新文件夹，所有静态和动态库文件将生成并存储在此文件夹中。

### 添加 Qt MQTT 模块

编译完成后，有两种方式可以使用该模块。一种是在项目中将 qtmqtt 导入为第三方模块，另一种是将编译后的文件直接放置在 Qt 的安装目录中。本文中，我们采用第二种方式。

1. 在目录 `Qt/6.6.2/macos/include/` 下创建一个名为 `QtMqtt` 的新文件夹。然后将 `qtmqtt/src/mqtt/` 下的所有文件复制到该文件夹。
2. 将生成的静态和动态库复制到 Qt 的安装目录。
   1. 将 `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release/lib` 目录下的所有文件和文件夹复制到 `Qt/6.6.2/macos/lib/` 目录中。如有需要替换的文件，请替换。
   2. 将 `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release/lib/cmake` 下的 `Qt6Mqtt` 文件夹复制到 `Qt/6.6.2/macos/lib/cmake` 中。
   3. 将 `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release/mkspecs/modules` 中的两个 `.pri` 文件复制到 `Qt/6.6.2/macos/mkspecs/modules` 中。

> 社区成员 Diego Schulz 提供了更好的 Qt MQTT 模块构建和安装方法，[供您参考](https://stackoverflow.com/questions/68928310/build-specific-modules-in-qt6-i-e-qtmqtt/71984521#71984521)。

## 准备 MQTT Broker

在继续操作之前，请确保您拥有一个用于通信和测试的 [MQTT 服务器](https://www.emqx.com/zh/blog/the-ultimate-guide-to-mqtt-broker-comparison)。

本指南将使用由 EMQ 提供的免费公共 MQTT Broker，基于 EMQX Platform 构建。服务器访问详情如下：

- 代理：`broker.emqx.io`
- TCP 端口：1883
- SSL/TLS 端口：8883
- WebSocket 端口：8083
- SSL/TLS 端口：8883
- 安全 WebSocket 端口：8084

更多相关信息，请参考：[免费的公共 MQTT 服务器](https://www.emqx.com/zh/mqtt/public-mqtt5-broker)

## 在 Qt 中使用 MQTT

### 简单的 Qt MQTT 应用程序

现在我们可以在 Qt 中使用 [Qt MQTT](https://doc.qt.io/qt-6/qtmqtt-index.html) 模块，该模块提供了一些[示例](https://github.com/qt/qtmqtt/tree/6.5.1/examples/mqtt)来展示其功能。

![Qt MQTT Examples](https://assets.emqx.com/images/704bc179a5718c590289d4968d501f22.png)

在本文中，我们将使用 [Simple MQTT Client ](https://doc.qt.io/qt-6/qtmqtt-simpleclient-example.html)Example 来演示如何使用 MQTT 创建一个与 MQTT Broker 通信的应用程序。我们在 QtCreator 中打开示例项目，查看该应用程序的运行情况。

回到我们使用 `git clone git://code.qt.io/qt/qtmqtt.git -b 6.6.2` 命令下载的目录，进入 `simpleclient` 示例项目目录：

```shell
cd qtmqtt
cd examples/mqtt/simpleclient
```

找到其中的 `CMakeLists.txt` 文件。用 Qt Creator 打开它，并按以下选项配置项目：

![Qt Creator](https://assets.emqx.com/images/97a2f764f0864bcfc1c4b2f6c2aa5436.png)

配置完成后。由于在前面的步骤中已经在本地环境中安装了 QtMqtt 库，程序可以成功运行。

在启动的图形化应用程序中，将主机输入框填入 `broker.emqx.io`，端口填入 `1883`。依次点击 “Connect”、“Subscribe” 和 “Publish” 按钮，将会得到如下输出：

![MQTT client is running successfully](https://assets.emqx.com/images/12927b7035e6bd273f8197a46a7f0372.png)

此时，一个简单的 MQTT 客户端已成功运行。

### 创建 MQTT 客户端

首先，我们使用 [QMqttClient](https://doc.qt.io/qt-6/qmqttclient.html) 类创建一个 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)。该类提供了用于设置唯一客户端 ID、代理主机名和端口的属性：

```
// mainwindow.cpp line 19
m_client = new QMqttClient(this);
m_client->setHostname(ui->lineEditHost->text());
m_client->setPort(static_cast<quint16>(ui->spinBoxPort->value()));
```

我们不设置客户端 ID，系统会自动生成。

接下来，我们连接到 [QMqttClient::messageReceived](https://doc.qt.io/qt-6/qmqttclient.html#messageReceived)() 来接收来自代理的所有消息：

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

### 连接/断开 Broker

在示例程序中，我们可以通过点击 “Connect/Disconnect” 按钮连接/断开到 MQTT Broker，触发以下函数：

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

关键在于我们可以通过调用 [m_client->connectToHost()](https://doc.qt.io/qt-6/qmqttclient.html#connectToHost) /[ m_client->disconnectFromHost() ](https://doc.qt.io/qt-6/qmqttclient.html#disconnectFromHost)方法来连接/断开 MQTT Broker。

### 订阅/取消订阅主题

同样，我们可以通过调用 [QMqttClient::subscribe](https://doc.qt.io/qt-6/qmqttclient.html#subscribe) 和 [QMqttClient::unsubscribe](https://doc.qt.io/qt-6/qmqttclient.html#unsubscribe) 来创建和取消订阅主题：

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

一旦订阅成功创建，MQTT Broker 就会将该主题的消息推送到客户端，Qt MQTT 将回调我们之前为其设置的 `QMqttClient::messageReceived` 函数。

### 发布消息

我们可以通过调用 [QMqttClient::publish](https://doc.qt.io/qt-6/qmqttclient.html#publish) 将消息内容发布到指定主题：

```
// mainwindow.cpp line 93
void MainWindow::on_buttonPublish_clicked()
{
    if (m_client->publish(ui->lineEditTopic->text(), ui->lineEditMessage->text().toUtf8()) == -1)
        QMessageBox::critical(this, u"Error"_s, u"Could not publish message"_s);
}
```

## 完整代码

所有示例代码可在 Github [qtmqtt/example](https://github.com/qt/qtmqtt/example) 中找到。

## Qt Creator 中常见的编译错误

在导入 `qtmqtt` 到 Qt Creator 后，您可能会遇到如下错误：

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

这是由于 Qt6 安装目录未被 CMake 识别。您可以通过将 `Qt/6.6.2/macos/lib/cmake` 添加到 CMake 模块路径来解决此问题：

![Qt Creator](https://assets.emqx.com/images/a38f36fda228e4bb00fc4de712844a30.png)

## 结语

本指南提供了在 Qt6 中设置和使用 MQTT 的步骤，包括从编译 Qt MQTT 模块到创建一个简单的 MQTT 客户端应用程序。使用 EMQ 提供的公共 MQTT Broker，您可以轻松测试和实现 MQTT 的通信功能。通过这一过程，您已经了解了 Qt MQTT 的基础使用方式，包括连接代理、订阅和取消订阅主题以及发布消息的功能。希望本文能够帮助您顺利构建基于 Qt 和 MQTT 的 IoT 应用。



<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
