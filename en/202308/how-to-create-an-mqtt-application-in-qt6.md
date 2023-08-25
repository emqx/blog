Qt is a cross-platform framework and toolkit for developing software that can run on different hardware platforms and operating systems. The Qt framework includes extensive libraries and tools that allow developers to easily build applications with native UI and performance. It's widely used in creating embedded devices and Internet-of-Things software.

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight IoT messaging protocol based on the publish/subscribe model. It can provide real-time and reliable messaging services for networked devices with very little code and bandwidth.

This blog provides a step-by-step guide on using MQTT for seamless communication in Qt6. You will learn how to compile the Qt MQTT module and use it to establish a connection, subscribe and unsubscribe to topics, publish messages, and receive messages in real time.

## Prepare the Environment

In this blog post, I used Qt v6.5.1 on my MacBook with M1 chip. Since I do not have a Qt Enterprise account, I downloaded and installed the [open-source version of Qt](https://www.qt.io/download-qt-installer-oss).

During the installation process, you will need to log in to your Qt Account. Therefore, it is recommended to register a Qt account before installation.

After installing Qt, you need to install g++ and XCode and set up some environment variables. The official documentation for Qt provides [instructions](https://doc.qt.io/qt-6/macos.html) on how to do this in macOS.

## Compile the Qt MQTT module via CMake

The Qt MQTT module is an official Qt library that provides a standard-compliant implementation of the MQTT protocol specification. However, it is not included in the open source installation and needs to be compiled from the source.

First, download the source code of Qt MQTT from [GitHub](https://github.com/qt/qtmqtt). Make sure that the version of Qt MQTT matches the version of Qt installed on your machine.

```
git clone git://code.qt.io/qt/qtmqtt.git -b 6.5.1
```

Next, compile Qt MQTT in QtCreater. In Qt6, you can use either [**qmake**](https://doc.qt.io/qt-6/qmake-manual.html) or [**CMake**](https://doc.qt.io/qt-6/cmake-manual.html) to build your code. For this blog, I used CMake. Open the CMakeLists.txt file of qtmqtt in Qt Creator and compile the project.

![Compile Qt MQTT in QtCreater](https://assets.emqx.com/images/be0373b13c2646cdd6a747f1bdf2c31a.png)

Once compilation is successful, a new folder named `build-qtmqtt-Qt_6_5_1_for_macOS-Release` will be created. All static and dynamic libraries will be generated and stored within this folder.

## Add Qt MQTT module

After the compiling, there are two ways to use it. One is to import qtmqtt as a third-party module in your project, and the other is to place the compiled files directly in the installation directory of Qt. In this blog, we will use the second method.

1. Create a new folder named `QtMqtt` in the directory `Qt/6.5.1/macos/include/`. Then copy all the files under `qtmqtt/src/mqtt/` to the newly created folder.

2. Copy the generated static and dynamic libraries to the Qt installation directory.

   1. Copy all files and folders under the directory `build-qtmqtt-Qt_6_5_1_for_macOS-Release/lib` to the folder `Qt/6.5.1/macos/lib/`. If there are any files that need to be replaced, replace them.

   2. Copy the Qt6Mqtt folder from `build-qtmqtt-Qt_6_5_1_for_macOS-Release/lib/cmake` to `Qt/6.5.1/macos/lib/cmake`.

   3. Copy the two `.pri` files from `build-qtmqtt-Qt_6_5_1_for_macOS-Release/mkspecs/modules` to `Qt/6.5.1/macos/mkspecs/modules`.

> When we published this blog on Twitter, [Diego Schulz](https://twitter.com/dschulzg) provided a better way to build and install the Qt MQTT module. We have included it [here](https://stackoverflow.com/questions/68928310/build-specific-modules-in-qt6-i-e-qtmqtt/71984521#71984521) for your reference.


## Qt MQTT Examples

Now we can use the Qt MQTT module in Qt. Qt provides some [examples](https://github.com/qt/qtmqtt/tree/6.5.1/examples/mqtt) to demonstrate the functionality provided by the [Qt MQTT](https://doc.qt.io/qt-6/qtmqtt-index.html) module.

![Qt MQTT Examples](https://assets.emqx.com/images/704bc179a5718c590289d4968d501f22.png)

In this blog, we will use the [MQTT Subscriptions Example](https://doc.qt.io/qt-6/qtmqtt-simpleclient-example.html) to illustrate how to use MQTT for creating an application that communicates with an MQTT broker. Let's open the example project in QtCreator to see how this application runs.

### Prepare an MQTT Broker

Before proceeding, please ensure you have an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) to communicate and test with.

In this blog post, we will use the [free public MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker) at `broker.emqx.io`.

```
MQTT Broker Info
Server: broker.emqx.io
TCP Port: 1883
WebSocket Port: 8083
SSL/TLS Port: 8883
Secure WebSocket Port: 8084
```

The Free public MQTT broker is exclusively available for those who wish to learn and test the MQTT protocol. It is important to avoid using it in production environments as it may pose security risks and downtime concerns.

### Import the Module

To use a Qt module, you need to link against the module library directly or through other dependencies. You can use the `find_package()` command to locate the needed module components in the CMakeLists.txt file of the project:

```
find_package(Qt6 REQUIRED COMPONENTS Mqtt)
target_link_libraries(mytarget PRIVATE Qt6::Mqtt)
```

### Create an MQTT Client

Click “Run” to build and run the application. Next, enter the public MQTT Broker address (`broker.emqx.io`) and port number (`1883`), and click "Connect". This will establish a connection to the public MQTT broker.

![Create an MQTT Client](https://assets.emqx.com/images/dffd027fda29754f9f0260c3017e5a56.png)

The corresponding code is to use the [QMqttClient](https://doc.qt.io/qt-6/qmqttclient.html) class to create an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools). This class provides properties that enable setting a unique client ID, as well as the broker host name and port to connect to.

```
    m_client = newQMqttClient(this);
    m_client->setHostname(ui->lineEditHost->text());
    m_client->setPort(static_cast<quint16>(ui->spinBoxPort->value()));
```

### Subscribe to an MQTT Topic

When we enter the topic "qtmqtt/topic1" and select the desired QoS level, we can click on "Subscribe" to subscribe the topic. A new dialog box will open for each subscription, where you can view the messages on the subscribed topics.

![Subscribe to an MQTT Topic](https://assets.emqx.com/images/6c7733ed85376c25fea04c111e947a42.png)

The corresponding code is to create a new subscription object:

```
void MainWindow::on_buttonSubscribe_clicked()
{
    auto subscription = m_client->subscribe(ui->lineEditTopic->text(),
                                            static_cast<quint8>(ui->spinQoS->text().toUInt()));
    if (!subscription) {
        QMessageBox::critical(this, QLatin1String("Error"), QLatin1String("Could not subscribe. Is there a valid connection?"));
        return;
    }
    auto subWindow = new SubscriptionWindow(subscription);
    subWindow->setWindowTitle(subscription->topic().filter());
    subWindow->show();
}
```

Then use the [QMqttSubscription](https://doc.qt.io/qt-6/qmqttsubscription.html) class to store the topic, state, and QoS level of a subscription:

```
SubscriptionWindow::SubscriptionWindow(QMqttSubscription *sub, QWidget *parent) :
    QWidget(parent),
    ui(new Ui::SubscriptionWindow),
    m_sub(sub)
{
    ui->setupUi(this);

    ui->labelSub->setText(m_sub->topic().filter());
    ui->labelQoS->setText(QString::number(m_sub->qos()));
    updateStatus(m_sub->state());
    connect(m_sub, &QMqttSubscription::messageReceived, this, &SubscriptionWindow::updateMessage);
    connect(m_sub, &QMqttSubscription::stateChanged, this, &SubscriptionWindow::updateStatus);
    connect(m_sub, &QMqttSubscription::qosChanged, [this](quint8 qos) {
        ui->labelQoS->setText(QString::number(qos));
    });
    connect(ui->pushButton, &QAbstractButton::clicked, m_sub, &QMqttSubscription::unsubscribe);
}
```

### Publish MQTT Messages

Next, click on “Publish“ to send an MQTT message to the topic.

![Publish MQTT Messages](https://assets.emqx.com/images/6b4fe063211ab0628da3405f115a3425.png)

The corresponding code is to use publish function of [QMqttClient](https://doc.qt.io/qt-6/qmqttclient.html) class to publish a message to the subscribed topic.

```
void MainWindow::on_buttonPublish_clicked()
{
    if (m_client->publish(ui->lineEditTopic->text(), ui->lineEditMessage->text().toUtf8(),
                          static_cast<quint8>(ui->spinQoS_2->text().toUInt()),
                          ui->checkBoxRetain->isChecked())
        == -1)
        QMessageBox::critical(this, QLatin1String("Error"), QLatin1String("Could not publish message"));
}
```

### Receive Messages

Once the message is sent, the client will receive it, and we can see it in the subscription dialogue.

![Receive MQTT Messages](https://assets.emqx.com/images/8d07923825d579581758d1e344082401.png)

To store the actual message payload, use the [QMqttMessage](https://doc.qt.io/qt-6/qmqttmessage.html) class, as shown in the corresponding code:

```
void SubscriptionWindow::updateMessage(constQMqttMessage &msg)
{
    ui->listWidget->addItem(msg.payload());
}
```

## Summary

This blog provides a step-by-step guide on compiling Qt MQTT module and creating an application that communicates with an MQTT broker. By following this guide, you will acquire the skills to leverage MQTT and build scalable and efficient IoT applications in Qt6.

## Join the EMQ Community

To dive deeper into MQTT, explore our [GitHub repository](https://github.com/emqx/emqx) for the source code, join our [Discord](https://discord.com/invite/xYGf3fQnES) for discussions, and watch our [YouTube tutorials](https://www.youtube.com/@emqx) for hands-on learning. We value your feedback and contributions, so feel free to get involved and be a part of our thriving community. Stay connected and keep learning!





<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
