In this article, we will focus on the Payload Format Indicator and Content Type properties of [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5), exploring how they make the parsing of messages more transparent and efficient.

>New to MQTT 5.0? Please check out our
>
>[MQTT 5.0: 7 New Features and a Migration Checklist](https://www.emqx.com/en/blog/introduction-to-mqtt-5)

## What is Payload Format Indicator?

The Payload Format Indicator is a new property introduced in MQTT 5.0 to indicate the format of the payload in [MQTT packets](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets). However, the format of the payload in CONNECT, SUBSCRIBE, and UNSUBSCRIBE packets is fixed, so in practice, only PUBLISH and CONNECT packets need to declare the payload format.

If the value of the Payload Format Indicator is 0 or if this property is not specified, the current payload is an unspecified byte stream; if the value of this property is 1, the current payload is UTF-8 encoded character data.

This allows the receiver to check the format of the payload without having to parse the specific content. For example, the server can check if the payload is a valid UTF-8 string to avoid distributing incorrectly formatted application messages to subscribers. However, given the burden this operation imposes on the server and the benefits that can actually be achieved, this is usually an optional setting.

![MQTT Payload Format Indicator](https://assets.emqx.com/images/516d070e403ea4861b6a68c09b5dbd49.jpg)

## What is Content Type?

Content Type is also a new property introduced in MQTT 5.0, and similar to the Payload Format Indicator, it is also only available in PUBLISH and CONNECT packets.

The value of Content Type is a UTF-8 encoded string that describes the content of the application message, which helps the receiver understand how to parse the application message payload. For example, if the content of the message is a JSON object, then the Content Type could be set to "json".

The exact content of this string is entirely up to the sender and receiver, and throughout the transmission of the message, the server does not use this property to verify that the message content is formatted correctly; it is only responsible for forwarding this property to the subscriber as is.

So you can even use "cocktail" to describe the JSON type as long as the receiver understands it. However, in order to avoid unnecessary troubles, we usually recommend using known MIME types to describe the message content, such as `application/json`, `application/xml`, etc.

Content Type is useful in scenarios where multiple data types need to be supported. For example, when we send an image to the other party in a chat program, and the image may be in PNG, GIF, JPEG, etc., how do we indicate to the other party the format of the image that corresponds to the binary data we are sending?

Prior to 5.0, we might choose to include the image format in a theme, such as `to/userA/image/png`, but obviously, as the number of supported image formats increases, clients need to subscribe to more and more topics for various data formats. In 5.0, we simply set the Content Type property to `image/png`.

![MQTT Content Type](https://assets.emqx.com/images/9e4ba35d4f25f588a8a4dff2a651b2ff.jpg)

## Do we have to use Payload Format Indicator and Content Type together?

Whether Payload Format Indicator and Content Type need to be used together depends on our application scenario.

For the subscriber, it can determine whether the content of the message should be a UTF-8 string or binary data based on the value of the Content Type, so the Payload Format Indicator is not very meaningful.

For the server, however, doesn't know the meaning of the Content Type value, so if we want the server to check whether the message payload conforms to the UTF-8 encoding specification, we must use the Payload Format Indicator property.

## Demo

1. Access [MQTTX Web](https://mqttx.app/web-client/) on a Web browser.

2. Create an MQTT connection named `pub` for publishing messages, and connect it to the [Free Public MQTT Server](https://www.emqx.com/en/mqtt/public-mqtt5-broker):

   ![MQTTX Web](https://assets.emqx.com/images/58b7f6ae09e33b1589965d2b017713a2.png)

3. Create a client connection named `sub` in the same way and subscribe to the topic `mqttx_89e3d55e/test` using the Client ID as a prefix:

   ![MQTTX new sub](https://assets.emqx.com/images/8873fccfce53b08c8bf34d743bb279c4.png)

4. Then go back to the client `pub`, click the Meta button in the message bar, set the Payload Format Indicator to `true`, set the Content Type to `application/json`, publish a JSON-formatted message to the topic `mqttx_89e3d55e/test`, and then change it to `application/x-www-form-urlencoded` and then publish a form format message to the same topic:

   ![MQTTX Payload Format Indicator](https://assets.emqx.com/images/16d704c3d0454264a1842a967f064ecb.png)

   ![MQTTX Content Type](https://assets.emqx.com/images/56af9a924f642c3cffe39566196438fe.png)

5. The Content Type of the message will be forwarded to the subscriber as is, so the subscriber can know how to parse the content in the Payload based on the value of the Content Type:

   ![Content Type of the message](https://assets.emqx.com/images/2e56a52e319d2cf7ffcf54ef1faa0366.png)

6. Back on the publishing side, set the Payload Format Indicator to `false` and change the encoding format of the Payload to `Hex`, then enter `FF` as the content of the Payload and send it. `0xFF` is a typical non-UTF-8 character:

   ![set the Payload Format Indicator to false](https://assets.emqx.com/images/3f87e5ff03ce4f53157a4de9c4f14868.png)

7. Although it is displayed as garbled characters, the subscriber did receive the message with a Payload of `0xFF` that we just sent. This is for performance reasons, EMQX currently does not check the Payload format:

   ![MQTTX Sub](https://assets.emqx.com/images/1b8e1c531c21ae0e72da1a8befd2d47b.png)

In the terminal, we can also use the command line tool [MQTTX CLI](https://mqttx.app/cli) to accomplish the above, and we can subscribe to topics using the following command:

```
mqttx sub -h 'broker.emqx.io' -p 1883 -t 'random-string/demo' --output-mode clean
```

Then use the following commands to set the Payload Format Indicator and Content Type properties when you publish the message:

```
mqttx pub -h 'broker.emqx.io' -p 1883 -t 'random-string/demo' \
--payload-format-indicator \
--content-type 'application/json' \
-m '{"msg": "hello"}'
```

This is how the Payload Format Indicator and Content Type properties are used in MQTT 5.0, and you can get Python examples of them [here](https://github.com/emqx/MQTT-Feature-Examples).

 



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
