## Introduction

Qt is a cross-platform framework and toolkit for developing software that can run on different hardware platforms and operating systems. The Qt framework includes extensive libraries and tools that allow developers to easily build applications with native UI and performance. It's widely used in creating embedded devices and Internet-of-Things software.

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight IoT messaging protocol based on the publish/subscribe model. It can provide real-time and reliable messaging services for networked devices with very little code and bandwidth.

This blog provides a step-by-step guide on using MQTT for seamless communication in Qt6. You will learn how to compile the Qt MQTT module and use it to establish a connection, subscribe and unsubscribe to topics, publish messages, and receive messages in real-time.

## Qt6 Project Preparation

In this blog post, we used Qt v6.6.2 on the MacBook with M2 chip. You can download and install the open-source version of Qt [here](https://www.qt.io/download-qt-installer-oss).

It is recommended to register a Qt account before installation.

After installing Qt, you need to install g++ and XCode and set up some environment variables. The official documentation for Qt provides [instructions](https://doc.qt.io/qt-6/macos.html) on how to do this in macOS.

### Compile the Qt MQTT Module via CMake

The Qt MQTT module is an official Qt library that provides a standard-compliant implementation of the MQTT protocol specification. However, it is not included in the open source installation and needs to be compiled from the source.

First, download the source code of Qt MQTT from [GitHub](https://github.com/qt/qtmqtt). Make sure that the version of Qt MQTT matches that of Qt installed on your machine.

```shell
git clone git://code.qt.io/qt/qtmqtt.git -b 6.6.2
```

Next, compile Qt MQTT in QtCreater. In Qt6, you can use either [**qmake**](https://doc.qt.io/qt-6/qmake-manual.html) or [**CMake**](https://doc.qt.io/qt-6/cmake-manual.html) to build your code. For this blog, we used CMake. Open the CMakeLists.txt file of qtmqtt in Qt Creator and compile the project. 

![Compile the Qt MQTT Module via CMake](https://assets.emqx.com/images/5fbf0fde3245d1e210a4ed460d8e9d63.png)

Once the compilation is successful, a new folder named `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release` will be created. All static and dynamic libraries will be generated and stored within this folder.

### Add Qt MQTT Module

After the compiling, there are two ways to use it. One is to import qtmqtt as a third-party module in your project, and the other is to place the compiled files directly in the installation directory of Qt. In this blog, we will use the second method.

1. Create a new folder named `QtMqtt` in the directory `Qt/6.6.2/macos/include/`. Then copy all the files under `qtmqtt/src/mqtt/` to the newly created folder.
2. Copy the generated static and dynamic libraries to the Qt installation directory.
   1. Copy all files and folders under the directory `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release/lib` to the folder `Qt/6.6.2/macos/lib/`. If there are any files that need to be replaced, replace them.
   2. Copy the Qt6Mqtt folder from `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release/lib/cmake` to `Qt/6.6.2/macos/lib/cmake`.
   3. Copy the two `.pri` files from `build-qtmqtt-Desktop_arm_darwin_generic_mach_o_64bit-Release/mkspecs/modules` to `Qt/6.6.2/macos/mkspecs/modules`.

> [*Diego Schulz*](https://stackoverflow.com/users/212380/dschulz) *from the community provides a better way to build and install the Qt MQTT module. We include it* [*here*](https://stackoverflow.com/questions/68928310/build-specific-modules-in-qt6-i-e-qtmqtt/71984521#71984521) *for your reference.*

## Prepare an MQTT Broker

Before proceeding, please ensure you have an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to communicate and test with.

In this guide, we will utilize the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) provided by EMQ, built on [EMQX ](https://www.emqx.com/en/products/emqx)Platform. The server access details are as follows:

- Broker: `broker.emqx.io`
- TCP Port: **1883**
- SSL/TLS Port: **8883**
- WebSocket Port: 8083
- SSL/TLS Port: 8883
- Secure WebSocket Port: 8084

For more information, please check out: [Free Public MQTT Broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker).

## Using MQTT in Qt

### Simple Qt MQTT Application

Now we can use the [Qt MQTT](https://doc.qt.io/qt-6/qtmqtt-index.html) module in Qt, which provides some [examples](https://github.com/qt/qtmqtt/tree/6.5.1/examples/mqtt) to demonstrate its functionality.

![Qt MQTT Examples](https://assets.emqx.com/images/704bc179a5718c590289d4968d501f22.png)

In this blog, we will use the [Simple MQTT Client](https://doc.qt.io/qt-6/qtmqtt-simpleclient-example.html) Example to illustrate how to use MQTT for creating an application that communicates with an MQTT broker. Let's open the example project in QtCreator to see how this application runs.

Let's go back to the directory we just downloaded using the `git clone git://code.qt.io/qt/qtmqtt.git -b 6.6.2` command and go into the sample project directory for simpleclient:

```shell
cd qtmqtt
cd examples/mqtt/simpleclient
```

Find the `CMakeLists.txt` file in it. Open it with Qt Creator and configure the project with the following options:

![Qt Creator](https://assets.emqx.com/images/97a2f764f0864bcfc1c4b2f6c2aa5436.png)

After the configuration is complete. Since the QtMqtt library has been installed in the local environment in the previous steps, the program can be run successfully.

In the started graphical application, fill the Host input box with  `broker.emqx.io`  and the Port with `1883`. Click Connect, Subscribe, and Publish button in that order to get an output similar to the following:

![MQTT client is running successfully](https://assets.emqx.com/images/12927b7035e6bd273f8197a46a7f0372.png)

At this point, a simple MQTT client is running successfully.

### Create an MQTT Client

First, we use the [QMqttClient](https://doc.qt.io/qt-6/qmqttclient.html) class to create an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools). The class provides properties for setting a unique client ID as well as the broker hostname and port to connect to:

```cpp
// mainwindow.cpp line 19
m_client = new QMqttClient(this);
m_client->setHostname(ui->lineEditHost->text());
m_client->setPort(static_cast<quint16>(ui->spinBoxPort->value()));
```

We do not set the client ID, and it will be automatically generated for us.

Next, we connect to [QMqttClient::messageReceived](https://doc.qt.io/qt-6/qmqttclient.html#messageReceived)() to receive all messages sent from the broker:

```cpp
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

### Connect/Disconnect to the Broker

In the sample program, we connect/disconnect to the MQTT Broker by clicking on the Connect/Disconnect button and triggering the following functions:

```cpp
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

The point is that we can do this by calling the [m_client->connectToHost()](https://doc.qt.io/qt-6/qmqttclient.html#connectToHost) / [m_client->disconnectFromHost()](https://doc.qt.io/qt-6/qmqttclient.html#disconnectFromHost) method to connect/disconnect to a MQTT Broker.

### Subscribe/Unsubscribe Topic

Similarly, we can create and unsubscribe to a topic by calling [QMqttClient::subscribe](https://doc.qt.io/qt-6/qmqttclient.html#subscribe) and [QMqttClient::unsubscribe](https://doc.qt.io/qt-6/qmqttclient.html#unsubscribe):

```cpp
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

Once the subscription has been created successfully, the MQTT Broker pushes the message for that topic to the client, and Qt MQTT calls back the `QMqttClient::messageReceived` callback function we set up for it earlier.

### Publish a Message

We can publish the message content to a specified topic by calling [QMqttClient::publish](https://doc.qt.io/qt-6/qmqttclient.html#publish)

```cpp
// mainwindow.cpp line 93
void MainWindow::on_buttonPublish_clicked()
{
    if (m_client->publish(ui->lineEditTopic->text(), ui->lineEditMessage->text().toUtf8()) == -1)
        QMessageBox::critical(this, u"Error"_s, u"Could not publish message"_s);
}
```

## Complete Code

All of the example codes can be found at: [Github qtmqtt/example](https://github.com/qt/qtmqtt/tree/6.5.1/examples/mqtt/simpleclient).

## Common Compiling Errors in Qt Creator

1. Could not find a package configuration file provided by "Qt6" with: `Qt6Config.cmake` or `qt6-config.cmake`

   After importing qtmqtt into Qt Creator, the following error may be encountered:

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

   The solution is that we need to check that the Qt Version of the build target for Desktop (arm-xx) is correct in the Manage Kits:

   ![Qt Creator](https://assets.emqx.com/images/a38f36fda228e4bb00fc4de712844a30.png)

## Summary

This blog provides a step-by-step guide on compiling Qt MQTT module and creating an application that communicates with an MQTT broker. By following this guide, you will acquire the skills to leverage MQTT and build scalable and efficient IoT applications in Qt6.

## Resources

- [Qt MQTT 6.6.2](https://doc.qt.io/qt-6/qtmqtt-index.html)
- [Qt MQTT Example for Linux](https://github.com/emqx/MQTT-Client-Examples/tree/master/mqtt-client-Qt)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
