## 背景

MQTT 是一个基于 TCP 协议的发布/订阅模型协议，它被广泛应用于物联网、传感器网络和其他低带宽、不稳定网络环境中。在这些网络环境中，网络连接往往不稳定，可能会出现网络故障、信号弱化、丢包等问题，这可能会导致 [MQTT 客户端](https://www.emqx.com/zh/blog/mqtt-client-tools)与服务器之间的连接中断。物联网应用中，常见的触发断线重连的场景包括：

1. 网络环境恶劣或者断网，造成 MQTT 客户端连接超时断开。
2. 由于业务需要服务端升级切换，服务端主动关闭断开。
3. 设备重启或客户端重启，客户端主动重连。
4. 其他网络因素造成 TCP/IP 传输层断开导致 [MQTT 连接](https://www.emqx.com/zh/blog/how-to-set-parameters-when-establishing-an-mqtt-connection)重连。

为了确保 MQTT 客户端与服务器之间的稳定连接，MQTT 客户端需要实现重连逻辑，帮助 MQTT 客户端自动重新连接服务器，并恢复之前的订阅关系、保持会话等状态。

## 为什么 MQTT 客户端重连代码需要良好的设计

MQTT 设备重连是很多物联网应用中不可避免的情况。设计 MQTT 客户端重连逻辑时需要注意使用正确的事件回调方法，每次重连设置合理的随机退避时间，以保证客户端和服务端的长时间稳定运行，从而确保业务的正常开展。

不合理的重连逻辑设计可能会造成诸多问题：

1. 重连逻辑失效导致客户端静默不再接受 Broker 消息。
2. 客户端频繁重连，无重连退避时间导致形成 DDOS 攻击服务端 Broker。
3. 客户端频繁上下线导致 Broker 服务端资源过量不必要的消耗。

而合理的重连逻辑既可以提高 MQTT 客户端的稳定性和可靠性，避免因网络连接中断而导致的数据丢失、延迟等问题，还可以降低由于频繁连接对服务器端的压力。

## 如何设计一段 MQTT 客户端重连代码

在进行 MQTT 客户端重连代码设计时需要考虑以下几个方面：

- 设置正确的连接保活时间
  MQTT 客户端的连接保活时间即 [Keep Alive](https://www.emqx.com/zh/blog/mqtt-keep-alive)，负责检测当前连接的健康状态。Keep Alive 超时会触发客户端重连和服务端关闭客户端连接。该数值会影响到服务端和客户端检测到连接断开不可用的时长，用户需要根据自身网络状态，以及期望的最长等待时间来设置合理的 Keep Alive。
- 重连策略和退避
  用户应该根据网络环境的不同，制定不同的重连策略。例如，当网络连接中断时，可以设置一个初始等待时间，并在每次重连尝试后逐渐增加等待时间，以避免网络连接中断导致的大量重连尝试。建议使用指数退避算法或随机 + 阶梯延时来留出足够的退避时隙。
- 连接状态管理
  需要在客户端中维护连接状态，包括连接状态的记录、连接断开的原因、已订阅的主题列表等信息。当连接中断时，客户端应该记录下连接断开的原因，并进行相应的重连尝试。但如果使用会话保持功能，则不需要客户端自己保存这些信息。
- 异常处理
  在连接过程中可能会发生各种异常情况，例如服务器不可用、认证失败、网络异常等。需要在客户端中添加异常处理逻辑，根据异常情况进行相应的处理。[MQTT 5](https://www.emqx.com/zh/blog/introduction-to-mqtt-5) 协议提供了详实的此类断开连接原因，客户端可以根据这些信息记录异常日志、断开连接、再次重连等。
- 最大尝试次数限制
  对于一些低功耗设备，为避免重连次数过多导致客户端资源消耗过大，有时候需要考虑限制最大重连尝试次数。当超过最大尝试次数后，客户端应该中止重连尝试进入休眠状态，避免无意义的重连。
- 退避算法
  有两种常用的重连退避方法：指数补偿算法[https://en.m.wikipedia.org/wiki/Exponential_backoff](https://en.m.wikipedia.org/wiki/Exponential_backoff) 和随机退避。指数补偿算法是通过负反馈机制指数增加等待时间来找到合适的发送/连接速率。随机退避即通过设置等待时间的上下限，每次重连都等待随机的延时时间，由于其易于实现而有广泛使用。

## 重连代码示例

我们将以 Paho MQTT C 的库为例，示范如何使用异步编程模型优雅完成自动重连功能。Paho 提供了丰富的回调函数，请注意不同回调方法触发条件和设置方式不同，分别有全局回调、API 回调和异步方法回调。API 回调有相当的灵活性，但当开启自动重连功能时，建议只使用异步回调。此处对三种回调函数都提供了例程，用户可以使用此例程验证三种回调函数的触发。

```
// 是 Async 使用的回调方法
// 连接成功的异步回调函数，在连接成功的地方进行Subscribe操作。
void conn_established(void *context, char *cause)
{
	printf("client reconnected!\n");
	MQTTAsync client = (MQTTAsync)context;
	MQTTAsync_responseOptions opts = MQTTAsync_responseOptions_initializer;
	int rc;

	printf("Successful connection\n");

	printf("Subscribing to topic %s\nfor client %s using QoS%d\n\n"
           "Press Q<Enter> to quit\n\n", TOPIC, CLIENTID, QOS);
	opts.onSuccess = onSubscribe;
	opts.onFailure = onSubscribeFailure;
	opts.context = client;
	if ((rc = MQTTAsync_subscribe(client, TOPIC, QOS, &opts)) != MQTTASYNC_SUCCESS)
	{
		printf("Failed to start subscribe, return code %d\n", rc);
		finished = 1;
	}
}


// 以下为客户端全局连接断开回调函数
void conn_lost(void *context, char *cause)
{
	MQTTAsync client = (MQTTAsync)context;
	MQTTAsync_connectOptions conn_opts = MQTTAsync_connectOptions_initializer;
	int rc;

	printf("\nConnection lost\n");
	if (cause) {
		printf("     cause: %s\n", cause);
    }
	printf("Reconnecting\n");
	conn_opts.keepAliveInterval = 20;
	conn_opts.cleansession = 1;
	conn_opts.maxRetryInterval = 16;
	conn_opts.minRetryInterval = 1;
	conn_opts.automaticReconnect = 1;
	conn_opts.onFailure = onConnectFailure;
	MQTTAsync_setConnected(client, client, conn_established);
	if ((rc = MQTTAsync_connect(client, &conn_opts)) != MQTTASYNC_SUCCESS)
	{
		printf("Failed to start connect, return code %d\n", rc);
		finished = 1;
	}
}

int main(int argc, char* argv[])
{
    // 创建异步连接客户端需要使用的属性结构体
	MQTTAsync client;
	MQTTAsync_connectOptions conn_opts = MQTTAsync_connectOptions_initializer;
	MQTTAsync_disconnectOptions disc_opts = MQTTAsync_disconnectOptions_initializer;
	int rc;
	int ch;
    // 创建异步连接客户端，不使用 Paho SDK 内置的持久化来处理缓存消息
	if ((rc = MQTTAsync_create(&client, ADDRESS, CLIENTID, MQTTCLIENT_PERSISTENCE_NONE, NULL))
			!= MQTTASYNC_SUCCESS)
	{
		printf("Failed to create client, return code %d\n", rc);
		rc = EXIT_FAILURE;
		goto exit;
	}
    // 设置异步连接回调，注意此处设置的回调函数为连接层面的全局回调函数
    // conn_lost 为连接断开触发，有且只有连接成功后断开才会触发，在断开连接的情况下进行重连失败不触发。
    // msgarrvd 收到消息时触发的回调函数
    // msgdeliverd 是消息成功发送的回调函数，一般设置为NULL
	if ((rc = MQTTAsync_setCallbacks(client, client, conn_lost, msgarrvd, msgdeliverd)) != MQTTASYNC_SUCCESS)
	{
		printf("Failed to set callbacks, return code %d\n", rc);
		rc = EXIT_FAILURE;
		goto destroy_exit;
	}
    // 设置连接参数
	conn_opts.keepAliveInterval = 20;
	conn_opts.cleansession = 1;
	// 此处设置 API调用失败会触发的回调，接下来进行connect操作所以设置为 onConnectFailure 方法
	conn_opts.onFailure = onConnectFailure;
	// 此处设置 客户端连接API调用成功会触发的回调，由于例程使用异步连接的 API，设置了会导致2个回调都被触发，所以建议不使用此回调
	//conn_opts.onSuccess = onConnect;
    // 注意第一次发起连接失败不会触发自动重连，只有曾经成功连接并断开后才会触发
	conn_opts.automaticReconnect = 1;
	//开启自动重连，并且设置 2-16s 的随机退避时间
	conn_opts.maxRetryInterval = 16;
	conn_opts.minRetryInterval = 2;
	conn_opts.context = client;
	// 设置异步回调函数，此与之前的 API 回调不同，每次连接/断开都会触发
	MQTTAsync_setConnected(client, client, conn_established);
	MQTTAsync_setDisconnected(client, client, disconnect_lost);
    // 启动客户端连接，之前设置的 API 回调只会在这一次操作生效
	if ((rc = MQTTAsync_connect(client, &conn_opts)) != MQTTASYNC_SUCCESS)
	{
		printf("Failed to start connect, return code %d\n", rc);
		rc = EXIT_FAILURE;
		goto destroy_exit;
	}

	......
}
```

> 下载 [MQTTAsync_subscribe.c](https://assets.emqx.com/data/MQTTAsync_subscribe.c) 文件查看详细代码。

## 更多选择：NanoSDK 内置重连策略

[NanoSDK](https://github.com/emqx/NanoSDK) 是除了 Paho 以外的又一 MQTT SDK 选择。NanoSDK 基于 [NNG-NanoMSG](https://github.com/nanomsg/nng) 项目开发，使用 MIT License，对开源和商业都很友好。相较于 Paho 其最大的不同在于内置的全异步 I/O 和 支持 Actor 编程模型，当使用 QoS 1/2 消息时可以获得更高的消息吞吐速率。而且 NanoSDK 支持 MQTT over QUIC 协议，与大规模物联网 [MQTT 消息服务器 EMQX 5.0](https://www.emqx.io/zh) 结合可解决弱网下的数据传输难题。这些优势使得它已经在车联网和工业场景中得到了广泛的使用。

在 NanoSDK 中，重连策略已经完全内置，无需用户手动实现。

```
// nanosdk 采用自动拨号机制，默认进行重连
nng_dialer_set_ptr(*dialer, NNG_OPT_MQTT_CONNMSG, connmsg);
nng_dialer_start(*dialer, NNG_FLAG_NONBLOCK);
```

## 总结

本文介绍在 MQTT 客户端代码实现过程中，重连逻辑设计的重要性与最佳实践。通过本文，读者可以设计更为合理的 MQTT 设备重连代码，降低客户端与服务器端的资源开销，构建更加稳定可靠的物联网设备连接。



<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的 MQTT 消息云服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
