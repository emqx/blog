## Background

[MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a publish/subscribe protocol built on TCP, widely used in IoT, sensor networks, and other environments where low bandwidth and unstable connections are common. In such scenarios, network connections can often be unreliable, leading to issues like network failures, weak signals, and packet loss, which may cause disconnections between the [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) and the server. Common situations that trigger disconnections and reconnections in IoT applications include:

1. Poor network conditions or disconnections, resulting in the MQTT client timing out and losing connection.
2. Server-side activities, such as upgrades or intentional shutdowns, leading to disconnection.
3. Device or client restarts, prompting the client to reconnect proactively.
4. Other network-related factors causing TCP/IP disconnections, leading to MQTT reconnection.

To maintain a stable connection between the MQTT client and the server, it is essential for the MQTT client to implement reconnection logic. This ensures that the client can automatically reconnect to the server, restore its previous subscription state, maintain session continuity, and more.

## Importance of Well-Designed MQTT Client Reconnection Logic

Reconnection is inevitable in many IoT applications using MQTT. Designing effective MQTT client reconnection logic is crucial. This involves using appropriate event callbacks and setting a reasonable random backoff interval for each reconnection attempt. Properly designed reconnection logic ensures the client and server operate stably over long periods, allowing the business to function smoothly.

Poorly designed reconnection logic can lead to several issues:

1. Failure in reconnection logic may cause the client to stop receiving messages from the broker without any warning.
2. Frequent reconnection attempts without a backoff mechanism can overwhelm the broker, potentially leading to a DDoS attack.
3. Constant client disconnections and reconnections can result in excessive and unnecessary consumption of broker resources.

A well-designed reconnection strategy not only enhances the stability and reliability of the MQTT client, helping to avoid data loss, delays, and other problems caused by network interruptions, but also reduces the server's load by preventing frequent connection attempts.

## How to Design Effective MQTT Client Reconnection Logic

When crafting MQTT client reconnection code, several key factors should be considered to ensure robust and stable performance:

- **Setting the Correct Keep-Alive Time**: The MQTT client's keep-alive interval, [Keep Alive](https://www.emqx.com/en/blog/mqtt-keep-alive), is crucial for monitoring the connection's health. If the keep-alive timeout is reached, the client will attempt to reconnect, and the server will close the connection. The keep-alive interval influences how quickly the client and server detect a lost connection. It's important to set this value based on your network conditions and the desired maximum waiting time.
- **Reconnect Policy and Backoff Strategy**: Different network environments may require distinct reconnection policies. For instance, if the network connection drops, an initial wait time can be set, with the wait time increasing gradually after each reconnection attempt. This approach prevents a flood of reconnection attempts when the network is down. Using an exponential backoff algorithm or a combination of random and stepped delays is recommended to ensure adequate backoff intervals.
- **Connection Status Management**: The client should maintain a record of the connection status, reasons for disconnection, and the list of subscribed topics. Upon disconnection, the client should log the disconnection reason and attempt to reconnect accordingly. If the session persistence feature is used, the client may not need to store this information independently.
- **Exception Handling**: Various issues, such as server unavailability, authentication failures, or network anomalies, may arise during the connection process. It's essential to include exception handling logic within the client to address these issues appropriately. The [MQTT 5](https://www.emqx.com/en/blog/introduction-to-mqtt-5) protocol provides detailed disconnection reasons, allowing the client to log exceptions, disconnect, and reconnect based on this information.
- **Limiting Maximum Reconnection Attempts**: For some low-power devices, it's crucial to limit the maximum number of reconnection attempts to avoid excessive resource consumption. If the maximum attempt limit is reached, the client should stop trying to reconnect and enter a sleep state to prevent unnecessary reconnection attempts.
- **Backoff Algorithms**: Two commonly used backoff methods for reconnection are the [exponential backoff](https://en.m.wikipedia.org/wiki/Exponential_backoff) and random backoff algorithms. The exponential backoff method increases the wait time exponentially through a negative feedback mechanism, finding an optimal send/connect rate. Randomized backoff involves waiting for a random delay within defined upper and lower bounds, making it a widely used and easy-to-implement approach.

## Code Example for Reconnect

Below is an example of how to implement auto-reconnect functionality using the Paho MQTT C library, leveraging its asynchronous programming model. Paho provides a variety of callback functions, each with different triggering conditions: global callbacks, API callbacks, and asynchronous callbacks. Although API callbacks offer flexibility, it is recommended to use asynchronous callbacks when enabling auto-reconnect functionality. The following example demonstrates the use of these callbacks in the context of MQTT client reconnection.

```c
// Callback method used by Async  
// Asynchronous callback function for successful connection, perform Subscribe operation after the connection is established.
void conn_established(void *context, char *cause)
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


// Below is the global callback function for client disconnection
void conn_lost(void *context, char *cause)
{
    MQTTAsync client = (MQTTAsync)context;
    MQTTAsync_connectOptions conn_opts = MQTTAsync_connectOptions_initializer;
    int rc;

    printf("\nConnection lost\n");
    if (cause) {
        printf("     cause: %s\n", cause);
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
    // Create attribute structures required for the asynchronous client
    MQTTAsync client;
    MQTTAsync_connectOptions conn_opts = MQTTAsync_connectOptions_initializer;
    MQTTAsync_disconnectOptions disc_opts = MQTTAsync_disconnectOptions_initializer;
    int rc;
    int ch;
    // Create an asynchronous client without using the Paho SDK's built-in persistence to handle cached messages
    if ((rc = MQTTAsync_create(&client, ADDRESS, CLIENTID, MQTTCLIENT_PERSISTENCE_NONE, NULL))
            != MQTTASYNC_SUCCESS)
    {
        printf("Failed to create client, return code %d\n", rc);
        rc = EXIT_FAILURE;
        goto exit;
    }

    // Set asynchronous callbacks, note that the callback functions set here are global callbacks in connection-level
    // conn_lost is triggered when the connection is lost, and is only triggered after a successful connection and subsequent disconnection. It will not trigger if reconnection fails after disconnection.
    // msgarrvd is the callback function triggered when a message is received
    // msgdeliverd is the callback function triggered when a message is successfully sent, usually set to NULL

    if ((rc = MQTTAsync_setCallbacks(client, client, conn_lost, msgarrvd, msgdeliverd)) != MQTTASYNC_SUCCESS)
    {
        printf("Failed to set callbacks, return code %d\n", rc);
        rc = EXIT_FAILURE;
        goto destroy_exit;
    }

    // Set connection parameters
    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;
    // The callback set here is triggered when the API call fails. Since the next operation is a connect operation, it is set to the onConnectFailure method.
    conn_opts.onFailure = onConnectFailure;
    // The callback set here is triggered when the client connection API call is successful. Since the example uses asynchronous connection APIs, setting this will cause both callbacks to be triggered, so it is recommended not to use this callback.
    //conn_opts.onSuccess = onConnect;
    // Note that automatic reconnection will not be triggered on the first failed connection attempt; it will only trigger after a successful connection and subsequent disconnection.
    conn_opts.automaticReconnect = 1;
    //Enable automatic reconnection with a random backoff interval between 2-16 seconds
    conn_opts.maxRetryInterval = 16;
    conn_opts.minRetryInterval = 2;
    conn_opts.context = client;
    // Set asynchronous callback functions; these are different from the previous API callbacks and are triggered each time a connection is established or lost
    MQTTAsync_setConnected(client, client, conn_established);
    MQTTAsync_setDisconnected(client, client, disconnect_lost);
    // Start client connection; the previously set API callbacks only take effect in this operation
    if ((rc = MQTTAsync_connect(client, &conn_opts)) != MQTTASYNC_SUCCESS)
    {
        printf("Failed to start connect, return code %d\n", rc);
        rc = EXIT_FAILURE;
        goto destroy_exit;
    }
    ......
}
```

> Download the [MQTTAsync_subscribe.c](https://assets.emqx.com/data/MQTTAsync_subscribe.c) file to view the full code.

## Alternative Approach: NanoSDK Built-in Reconnect Policy

[NanoSDK](https://github.com/emqx/NanoSDK) is another MQTT SDK that serves as an alternative to Paho. It is based on the [NNG-NanoMSG](https://github.com/nanomsg/nng) project and is developed under the MIT License, making it both open source and commercially friendly. One of the key differences from Paho is NanoSDK's fully asynchronous I/O and support for the Actor programming model, which allows for higher message throughput, particularly with QoS 1/2 messages. Additionally, NanoSDK supports MQTT over QUIC protocol, which can be combined with large-scale IoT messaging servers like [EMQX 5.0](https://www.emqx.com/en/products/emqx) to improve data transmission in weak network conditions. These features make NanoSDK particularly well-suited for IoV and industrial scenarios.

In NanoSDK, the reconnection policy is fully integrated, so users don't need to implement it manually.

```c
// NanoSDK uses an auto-dialer mechanism to handle reconnections by default
nng_dialer_set_ptr(*dialer, NNG_OPT_MQTT_CONNMSG, connmsg);
nng_dialer_start(*dialer, NNG_FLAG_NONBLOCK);
```

## Conclusion

This blog highlights the importance of well-designed reconnection logic in MQTT client implementation and offers best practices for achieving stable and reliable IoT device connectivity. By following these guidelines, developers can design more efficient MQTT reconnection code, minimizing resource overhead on both the client and server while ensuring a stable connection in IoT applications.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
