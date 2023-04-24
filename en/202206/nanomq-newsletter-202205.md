The NanoMQ project keeps a steady pace in updating new versions each month. At the end of May, the v0.8.0 was officially released (download here: [Release NanoMQ 0.8.0 · emqx/nanomq](https://github.com/emqx/nanomq/releases/tag/0.8.0)). We have brought you 2 important feature updates: event WebHook, and the authentication HTTP plugins. We have also added the new HTTP API for viewing the data model of the MQTT namespace. Needless to say, bugs are fixed, and better performance is achieved.

## **Asynchronous and Easy-to-Use WebHook System**

WebHook is a feature of EMQX very popular among open source users, and NanoMQ has also launched the same feature in response to the community's call to facilitate users' integration with third-party edge computing applications.

The WebHook system of NanoMQ is in the same strain as EMQX, and adopts the same style of configuration. The default path of the configuration file for Webhook is /etc/nanomq_web_hook.conf, or it can be started by specifying a path to read the configuration file through the command line. For specific configuration items, please refer to NanoMQ Docs:[https://nanomq.io/docs/en/latest/web-hook.html](https://nanomq.io/docs/en/latest/web-hook.html)

```
web.hook.enable=true
## example
web.hook.rule.<Event>.<Number>=<Rule>
```

Users may configure the trigger rules according to specific needs after enabling the WebHook function in the settings. If necessary to forward the client end online and offline events and all messages that match the wildcard theme of "webhook/msg/#" to the corresponding HTTP API, the configuration method should be as follows:

### **Rule Configuration**

The rule trigger may be configured in etc/nanomq_web_hook.conf, and the configuration format is as follows:

```
## example
web.hook.enable=true
web.hook.url=http://127.0.0.1:8888
web.hook.headers.content-type=application/json
web.hook.body.encoding_of_payload_field=plain
web.hook.pool_size=32
web.hook.rule.client.connack.1={"action": "on_client_connack"}
web.hook.rule.client.disconnected.1={"action": "on_client_disconnected"}
web.hook.rule.message.publish.1={"action": "on_message_publish", "topic": "webhook/msg/#"}
```

If so configured, NanoMQ can automatically capture and spit out the data of client end online and offline and message releases to the corresponding HTTP API. The following are the examples of data formats requested currently by HTTP:

```
## HTTP json example
Connack（client connected event）:
{
  "proto_ver": 4,
  "keepalive": 60,
  "conn_ack": "success",
  "username": "undefined",
  "clientid": "nanomq-6ecb0b61",
  "action": "client_connack"
}

Publish（message publish）:
{
  "ts": 1650609267000,
  "topic": "webhook/msg/123",
  "retain": false,
  "qos": 0,
  "action": "message_publish",
  "from_username": "undefined",
  "from_client_id": "nanomq-6ecb0b61",
  "payload": "hello"
}

Disconnect（client disconnected event）:
{
  "reason": "normal",
  "username": "undefined",
  "clientid": "nanomq-6ecb0b61",
  "action": "client_disconnected"
}
```

At present, the WebHook system of NanoMQ supports the following events:

| Name                | Notes                                | Execution time                                               |
| ------------------- | ------------------------------------ | ------------------------------------------------------------ |
| client.connack      | MQTT client end connection succeeded | When the server end is ready to send the connection response messages |
| client.disconnected | MQTT client disconnected             | When the client connection layer is ready to shut down       |
| message.publish     | Publishing MQTT messages             | Before the server publishes (routes) the messages            |

If you need more message events, please submit the function application Issue on Github, and we will arrange for the addition of the feature as soon as possible.

What should be emphasized is that the WebHook function of NanoMQ is a fully asynchronous operation, and all the matched event messages will enter an independent proprietary thread for processing through an efficient internal IPC channel, which is isolated from the Broker function and will not block the normal message flow in the original server, so it is efficient and reliable.

For the specific configuration information and ways of WebHook and debugging, please pay close attention to the future series of NanoMQ tutorial articles.

## **HTTP Authentication Plugin**

HTTP connection authentication is another commonly-used integration function, which can be conveniently integrated with a third-party authentication server to complete the connection request verification at the client. The plug-in of the same type of another common open-source project Mosquitto has been abandoned and no longer maintained. The present function of NanoMQ has filled up this gap, and it also maintains the same function and configuration style as EMQX, making it convenient for users to get started.

### **Authentication Rule Configuration**

 Authentication HTTP API configuration files are read in the same way as other configuration files of NanoMQ. The internally-included configuration items are:

```
## whether turn on HTTP Auth plugin
## Value: true | false
auth.http.enable = true

## targrt HTTP URL that Auth request
auth.http.auth_req.url = http://127.0.0.1:80/mqtt/auth

## HTTP Auth Request
## Value: post | get
auth.http.auth_req.method = post

## HTTP Request Headers for Auth Request
auth.http.auth_req.headers.content_type = application/x-www-form-urlencoded

## Parameters used to construct the request body or query string parameters
auth.http.auth_req.params = clientid=%c,username=%u,password=%P
```

Upon completion of the configuration, NanoMQ will request the corresponding HTTP URL for the message of the client-side Connect package according to the request format set in the configuration, and judge whether the client connection is allowed to succeed according to the return code (Code 200 expresses success). Please refer to the official website configuration files for more detailed configuration methods: [https://nanomq.io/docs/en/latest/config-description/v014.html#parameter-description](https://nanomq.io/docs/en/latest/config-description/v014.html#parameter-description).

## Other optimization and bug fix

NanoMQ 0.8.0 provides the following updates and optimization as well:

1. The timestamp field in the client's online and offline time message, which was previously preceded by the startup timer, has been modified as UNIX standard timestamp.
2. The usage of the command line tool NanoMQ has been modified, and the restriction that "start/stop" must be used by default has been removed.
3. Files have been added for the ZeroMQ proxy message gateway.
4. The lock contention problem caused by the frequent closing of bridge connection by the broker has been fixed.
5. The problem of data competition caused by sudden port of Sub client-side when a large quantity of messages are published by the client, resulting in backlog, has been solved.
6. UTF-8 check is no longer required by default on the content of the last will message unless the client requests YES.
7. A failure that may cause a crash if the message property is empty when using Retain As Published messages have been fixed.

## Coming Soon

NanoMQ will officially release the rule engine in June and introduce a new database as an edge data full persistence option. This feature is still in the Demo stage, but available in the latest master branch. Users may independently compile, install and use it.

NanoSDK will release the RC version of MQTT over QUIC next month. It is the first [MQTT SDK](https://www.emqx.com/en/mqtt-client-sdk) of the industry based on C language and fully supports the MQTT 3.1.1 and QUIC functions, please stay tuned.


<section class="promotion">
    <div>
        Try NanoMQ for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=nanomq" class="button is-gradient px-5">Get Started →</a>
</section>
