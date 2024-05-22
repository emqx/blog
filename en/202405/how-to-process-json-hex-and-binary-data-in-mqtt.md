## Introduction to MQTT Payload

MQTT payload refers to the actual data carried in an MQTT message. The [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) does not impose any requirements on the Payload format; it allows for any binary data. In practice, however, we have some general data formats in the application layer, such as JSON, Binary, Hex, and Protobuf.

Understanding the payload format and its management is crucial, as this represents the primary information exchanged between devices in the IoT ecosystem. In this blog, we will explain how these formats are transmitted and processed with the [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and [MQTT Client](https://www.emqx.com/en/blog/mqtt-client-tools).

You can read this blog to learn more about MQTT payload: [Introduction to MQTT Payload Format Indicator and Content Type | MQTT 5 Features](https://www.emqx.com/en/blog/mqtt5-new-features-payload-format-indicator-and-content-type) 

## Common Message Transmission Data Formats in MQTT

### Plain Text

Plain Text, the simplest format, is usually used for the transmission of various simple text messages, such as instant chatting, message notifications, etc. For example:

```
Hi, this is a plain text.
```

### JSON

JSON (JavaScript Object Notation) is a lightweight data-interchange format. It is easy for machines to parse and generate and also for humans to read and write. It is often used to describe an Object or event. For example:

```json
{"temperature": "22.1"}
```

### Raw Binary

Raw binary data refers to data that is in a format that is not intended for human interpretation. It consists of sequences of binary digits (0s and 1s) that represent information such as text, images, audio, video, or any other type of data. This data is typically stored in a computer's memory or on storage devices in its binary form. Generally, we write raw binaries in hexadecimal. For example the Raw binary of String `aaa` written as:

```
0x616161
```

### Hex String

Hex String is a way to describe a segment of Raw binary in the form of its hexadecimal chars. For example, the Hex String of the String `aaa` is String `616161`. The Hex String is typically used for the encoding of raw binary data, which is converted into a visible hexadecimal string. This format is convenient for reading and printing more than Raw Binary.

### Protobuf

Protocol Buffers (Protobuf) is a free and open-source cross-platform data format used to serialize structured data. It is useful in developing programs that communicate with each other over a network or for storing data. For example, the message Schema like the following:

```protobuf
message Sensor {
  required int32 temperature = 1;
}
```

Then a Protobuf message binary representing a temperature of 22 is:

```
0816
```

## Sending and Receiving Data in Different Formats

### Setting up the Practice Environment

#### MQTT Broker

EMQX is a highly scalable and feature-rich MQTT broker designed for IoT and real-time messaging applications.

In this tutorial, we use Docker to install an EMQX 5.6.1 locally for demonstration:

```shell
docker run  --rm -p 18083:18083 -p 1883:1883  emqx/emqx:5.6.1
```

Then open the browser and visit `http://127.0.0.1:18083` to enter the EMQX Dashboard. The default username and password are `admin`, `public` :

![EMQX Dashboard](https://assets.emqx.com/images/91a20129ce36884aad71803f3770f104.png)

#### MQTT Client

We recommend using MQTTX CLI as the MQTT client for testing. [**MQTTX**](https://mqttx.app/) is an open-source, cross-platform MQTT 5.0 desktop client initially developed by EMQ, which can run on macOS, Linux, and Windows. 

Get MQTTX CLI [here](https://mqttx.app/).

Take MacOS as an example, install MQTTX CLI:

```shell
brew install emqx/mqttx/mqttx-cli
```

After successful, test if it can establish a connection to the local EMQX:

```shell
mqttx conn -h 127.0.0.1 -p 1883
```

For example, getting the following output proves a successful connection to the local EMQX:

![Connect to the local EMQX](https://assets.emqx.com/images/7d35c1562c1f4aa48dd3aaeebff6cfce.png)

### Sending and Receiving Messages

The Payload of MQTT messages supports any format of strings or binary. For example, we use MQTTX CLI to create a subscriber named `sub` to EMQX and subscribe the `test/sub` topic:

```shell
mqttx sub -h 127.0.0.1 -p 1883 -i sub -t test/sub
```

Then, publish a simple message to `test/sub` topic, i.e:

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/sub -m 'Hi, plaintext payload'
```

We can observe that the subscriber on the bottom has received this message:

![received message](https://assets.emqx.com/images/966758dfbbc63319065da3c4dde64edd.png)

#### Content-Type Field of Payload

In the MQTT 5.0 protocol, the `Content-Type` field was introduced to identify the Payload format (see: [Content Type in PUBLISH message](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Toc3901118)).

Therefore, we can use this field when publishing messages to enhance the description of the Payload format:

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/sub -m 'Hi, plaintext payload' --content-type 'plain/text'
```

We can observe that the subscriber on the bottom has received this message and content type setting:

![plain/text message](https://assets.emqx.com/images/c8ee52162ed750baf01eeeac083f6972.png)

#### Payload in JSON Format

[**JSON**](https://www.json.org/json-en.html) is a lightweight data interchange format that is easily readable and writable by humans and easily parsed and generated by machines.

We can also send a JSON format message through the MQTTX CLI. This operation is similar to plain text messages.

Note: the `--format` parameter is used to inform the MQTTX CLI that the input Payload is a JSON string and to validate its legality:

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/sub \\
  --content-type 'application/json' \\
  --format json \\
  -m '{"key": "value"}'
```

We can also get output like the following:

![JSON message](https://assets.emqx.com/images/f4fb2894acb3a1618025ddb8aa85cf9f.png)

#### Payload in Hex String Format

[Hexadecimal](https://en.wikipedia.org/wiki/Hexadecimal) String (Hex String) is a representation of binary data as a string of hexadecimal numbers. Each byte of binary data is represented by a two-digit hexadecimal number, allowing for a more human-readable format. It's commonly used in programming and data communication.

In MQTT, a Hex String can be sent directly as a normal string:

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/sub \\
  -m '31310000ffff'
```

We can get the output like the following:

![Hex String message](https://assets.emqx.com/images/ab83426ae3328095d34b650d85948d01.png)

#### Payload in Binary Format

According to the MQTT protocol definition, the format of the payload is not constrained, meaning it can be in any binary format.

MQTTX CLI can send binary data through `--format hex`, for example:

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/sub \\
--format hex \\
-m '31 31 00 00 ff ff'
```

The screenshot below illustrates that the receiver displays the binary as `11��`. This is because `0x31` is the encoded representation of the character `1`:

![Binary format message](https://assets.emqx.com/images/ea6a05c3ce2225e21d4ab90a700055c6.png)

## Handle JSON Payload with EMQX Rule Engine

The rule engine feature of EMQX provides various processing functions that can conveniently handle the parsing and extraction of various payload formats. Learn more at: [EMQX Rule Engine](https://docs.emqx.com/en/enterprise/latest/data-integration/rules.html).

For structured payloads with JSON format, the EMQX Rule Engine can conveniently extract and reorganize the fields within it. We will demonstrate in detail how to handle JSON payload with EMQX Rule Engine in this section.

### Create Rule and Action

For example, we can add the following rule to extract the JSON field via EMQX Dashboard:

```sql
SELECT
  payload.temperature as t
FROM
  "test/msg_in"
```

The purpose of this rule is to parse and extract the `temperature` from the message payload on all `test/msg_in` topics. And rename the field to `t`.

Then, add a `Republish` action to this rule to publish the message in the new JSON structure to the `test/msg_out` topic.

Add the Rule and Action:

![Add the Rule and Action](https://assets.emqx.com/images/3ab8c91a8e3cf62c5eec87b654917621.png)

The Republish Action parameters:

![The Republish Action parameters](https://assets.emqx.com/images/ece20aa554ae0a6b54c454f78f9d73d7.png)

### Test with MQTTX CLI

Once the rule is created, we can use MQTTX CLI to verify it by using the following command to create a subscription to the topic `test/msg_out` :

```shell
mqttx sub -h 127.0.0.1 -p 1883 -i sub -t test/msg_out -v
```

Then publish the JSON formatted message `{"temperature": 23.5, "altitude": 100}` to the `test/msg_in` topic:

```shell
mqttx pub -h 127.0.0.1 -p 1883 -i pub -t test/msg_in \\
  --format json \\
  -m '{"temperature": 23.5, "altitude": 100}'
```

By observing the messages received by the subscriber at `test/msg_out`, we can see that the `temperature` in the JSON message has been extracted and reformatted as `{"t": 23.5}` :

![Test with MQTTX CLI](https://assets.emqx.com/images/e49e555c12ca620145ecdfd31f98dad9.png)

## Q&A

### **Which data format is most suitable for my application?** 

The choice of data format really depends on the needs of your specific application. For instance, if you need a human-readable format and aren't overly concerned about bandwidth, JSON might be the best choice. However, if bandwidth is a concern, a more compact format like binary or hexadecimal might be better. If you need a balance between structure and efficiency but can accept the complexity, Protobuf could be the right choice.

### **Can I send images or other large files as MQTT payloads?**

While it's technically possible to send images or other large files as MQTT payloads, it's generally not recommended. MQTT was designed for small, frequent messages, and sending large payloads can cause network congestion or other issues.

### **What is the maximum size of an MQTT payload?**

The maximum size of the MQTT payload is 256 MB. However, considering the performance and efficiency of the network, payloads are generally recommended to be kept below 1 MB.

### **Can I encrypt MQTT payloads?**

Yes, MQTT payloads can be encrypted before being sent and then decrypted upon receipt. This can provide an additional layer of security for sensitive data. However, you must perform encryption when sending messages and decryption when receiving messages.

## Conclusion

In conclusion, MQTT provides a flexible way to exchange data between IoT devices in various formats. The choice of payload data format depends on the specific requirements of the application, such as network bandwidth, human readability, and the complexity of the data structure. With a proper understanding of these different formats and how to handle them in MQTT, developers can optimize their IoT solutions for efficiency and performance.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
