

[MQTT](https://zh.wikipedia.org/zh-hans/MQTT) 是一种轻量级的、灵活的物联网消息交换和数据传递协议，致力于为 IoT 开发人员实现灵活性与硬件/网络资源的平衡。

[Kotlin](https://kotlinlang.org/) 是一门由 JetBrains 公司开发的编程语言，Kotlin 是基于 JVM 的，所以开发者可以很方便地用它来进行Android 开发，并且支持 Kotlin 和 Java 的混合编写。而早在 2017 年，Google 就宣布 Kotlin 成为官方开发语言。

本文主要介绍使用 Kotlin 语言在 Android 平台上使用 MQTT。

## 新建 Kotlin 项目

打开 Android Studio 新建一个项目，选择语言为 Kotlin，Android Studio 会自动创建 Kotlin 相关配置。若要配置现有项目，则可以参考 [将 Kotlin 添加到现有应用](https://developer.android.com/kotlin/add-kotlin)。

## 添加依赖

打开项目的 `build.gradle`，添加 [Eclipse Paho Java Client](https://www.eclipse.org/paho/clients/java/) 和 [Eclipse Paho Android Service](https://www.eclipse.org/paho/clients/android/) 依赖到 `dependencies` 部分。

```groovy
dependencies {
    implementation 'org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.2.4'
    implementation 'org.eclipse.paho:org.eclipse.paho.android.service:1.1.1' 
}
```

## 配置 `AndroidManifest.xml`

Android Service 是 Eclipse 开发的基于 Android 平台的一个后台服务，我们需要将它注册到AndroidManifest.xml 文件，同时，我们需要注册权限。

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.WAKE_LOCK" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

<application
   ...
   <service android:name="org.eclipse.paho.android.service.MqttService" />
</application>

```

## 创建 MQTT 客户端

```kotlin
private lateinit var mqttClient: MqttAndroidClient
// TAG
companion object {
    const val TAG = "AndroidMqttClient"
}
```

## 连接 MQTT 服务器

本文将使用 EMQ X  [MQTT Cloud](https://cloud.emqx.cn/) 运营和维护的免费公共 [MQTT 服务器](https://www.emqx.com/zh/products/emqx)， EMQ X Cloud 是由 [EMQ](https://www.emqx.com/zh) 推出的安全的 MQTT 物联网云服务平台，它提供一站式运维代管、独有隔离环境的 **MQTT 5.0** 接入服务。

- Broker: **broker.emqx.io**
- TCP Port: **1883**
- Websocket Port: **8083**

```kotlin
fun connect(context: Context) {
        val serverURI = "tcp://broker.emqx.io:1883"
        mqttClient = MqttAndroidClient(context, serverURI, "kotlin_client")
        mqttClient.setCallback(object : MqttCallback {
            override fun messageArrived(topic: String?, message: MqttMessage?) {
                Log.d(TAG, "Receive message: ${message.toString()} from topic: $topic")
            }

            override fun connectionLost(cause: Throwable?) {
                Log.d(TAG, "Connection lost ${cause.toString()}")
            }

            override fun deliveryComplete(token: IMqttDeliveryToken?) {

            }
        })
        val options = MqttConnectOptions()
        try {
            mqttClient.connect(options, null, object : IMqttActionListener {
                override fun onSuccess(asyncActionToken: IMqttToken?) {
                    Log.d(TAG, "Connection success")
                }

                override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                    Log.d(TAG, "Connection failure")
                }
            })
        } catch (e: MqttException) {
            e.printStackTrace()
        }

    }
```

其中，`MqttCallback` 接口包含 3 个方法：

1. messageArrived：收到 broker 新消息
2. connectionLost：与 broker 连接丢失
3. deliveryComplete：消息到 broker 传递完成

`MqttConnectOptions` 用于配置连接设置，包含用户名密码，超时配置等，具体可以查看其方法。

## 创建 MQTT 订阅

订阅 topic

```kotlin
fun subscribe(topic: String, qos: Int = 1) {
        try {
            mqttClient.subscribe(topic, qos, null, object : IMqttActionListener {
                override fun onSuccess(asyncActionToken: IMqttToken?) {
                    Log.d(TAG, "Subscribed to $topic")
                }

                override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                    Log.d(TAG, "Failed to subscribe $topic")
                }
            })
        } catch (e: MqttException) {
            e.printStackTrace()
        }
    }
```

## 取消订阅

取消订阅 topic

```kotlin
fun unsubscribe(topic: String) {
        try {
            mqttClient.unsubscribe(topic, null, object : IMqttActionListener {
                override fun onSuccess(asyncActionToken: IMqttToken?) {
                    Log.d(TAG, "Unsubscribed to $topic")
                }

                override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                    Log.d(TAG, "Failed to unsubscribe $topic")
                }
            })
        } catch (e: MqttException) {
            e.printStackTrace()
        }
    }
```

## 发布消息

```kotlin
fun publish(topic: String, msg: String, qos: Int = 1, retained: Boolean = false) {
        try {
            val message = MqttMessage()
            message.payload = msg.toByteArray()
            message.qos = qos
            message.isRetained = retained
            mqttClient.publish(topic, message, null, object : IMqttActionListener {
                override fun onSuccess(asyncActionToken: IMqttToken?) {
                    Log.d(TAG, "$msg published to $topic")
                }

                override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                    Log.d(TAG, "Failed to publish $msg to $topic")
                }
            })
        } catch (e: MqttException) {
            e.printStackTrace()
        }
    }
```

## 断开 MQTT 连接

```kotlin
fun disconnect() {
        try {
            mqttClient.disconnect(null, object : IMqttActionListener {
                override fun onSuccess(asyncActionToken: IMqttToken?) {
                    Log.d(TAG, "Disconnected")
                }

                override fun onFailure(asyncActionToken: IMqttToken?, exception: Throwable?) {
                    Log.d(TAG, "Failed to disconnect")
                }
            })
        } catch (e: MqttException) {
            e.printStackTrace()
        }
    }
```

## 测试

首先将 Android 客户端连接到 MQTT 服务器，然后订阅 topic:  `a/b`，可以看到连接成功和成功订阅的日志

![MQTT connect and subscribe](https://static.emqx.net/images/5513474b6c2a4848c232825da093bc25.png)

然后我们使用 [MQTT 5.0 客户端工具 - MQTT X](https://mqttx.app/zh) 进行测试，发布消息到 topic: `a/b`，客户端可以看到收到消息的日志

![MQTT 5.0 Client Tool - MQTT X](https://static.emqx.net/images/ab664c88b18208cc60fa476adb91f284.png)

![receive MQTT messages](https://static.emqx.net/images/8db9cd6cf35980d4ab6508984331ab2c.png)

我们在客户端发布消息到 topic: `a/b` ，因为我们订阅了该 topic，同时也会收到消息，最后我们断开客户端与 MQTT 服务器的连接，日志如下

![publish mqtt message and disconnect](https://static.emqx.net/images/11c4cf97ed7a0fc31a3c5547a709356e.png)

至此，我们已经完成了Android 上 MQTT 客户端的构建，实现了客户端与 MQTT 服务器的连接、主题订阅、收发消息等功能。

MQTT 可以以极少的代码和有限的带宽，为连接远程设备提供实时可靠的消息服务。作为一种低开销、低带宽占用的即时通讯协议，使其在物联网、小型设备、移动应用等方面有较广泛的应用。

而 Kotlin 也是 Google 官方主推的一门语言，结合 MQTT 协议及 [MQTT 云服务](https://cloud.emqx.cn/)，我们可以开发更多有趣的应用。

