## Challenges of File Transfer in IoT

The [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a protocol designed for lightweight publish/subscribe messaging, widely supported by a wide range of client libraries and server implementations. It is a perfect protocol for constrained environments such as communication in Internet of Things (IoT) contexts where a small code footprint is required and device capabilities are limited. The model and primitives of MQTT are simple and easy to understand, but the protocol itself is very powerful and flexible, and as such, it usually covers most of the needs of IoT applications. 

However, there are several classes of devices and associated use cases where the MQTT protocol alone is usually not enough. Imagine an industry camera that is part of a Quality Assurance pipeline in a factory. The camera needs to take a high-resolution picture of a product, and then send it to a server for further processing. Or a vehicle that needs to send logging and telemetry data to a cloud every once in a while. Or a smart home device that needs to upload a video stream to an analytics service. In all these cases, the MQTT standard lacks an established way to transfer large payloads, and the devices usually have to resort to other protocols designed with that purpose in mind, such as HTTPS (e.g. S3) or FTP. 

It's not ideal, as it requires the devices to maintain multiple protocols and communication channels, which increases the complexity of the system. One needs to spend a lot of engineering effort to implement additional protocols, support separate authentication and authorization mechanisms, and maintain auxiliary network and cloud infrastructure for them to work. Not to say that those protocols are often not designed with the same constraints in mind as MQTT. Take S3 as an example, most S3 implementations require a client to send the file in chunks of at least 5 MiB, which is a lot of data for a constrained device to buffer and send over the network.

## File Transfer Over MQTT in EMQX

Provided that MQTT has a lot of flexibility, with these use cases in mind, we decided to extend it with a simple File Transfer mechanism. We had a few goals when designing it:

- It should be simple and easy to use so that it will be easy to implement on a wide range of devices and platforms.
- It should be able to transfer large payloads, with a size of up to several gigabytes.
- Network issues should not affect the transfer so that it can be used in unreliable networks.
- Memory usage should be minimal to allow using it on constrained devices.

The result of this effort is a File Transfer over MQTT protocol, which is now available in the [EMQX Enterprise](https://www.emqx.com/en/products/emqx) 5.1 release. In this blog post, we will describe the protocol in detail and show how to use it in practice.

## Design Details

The File Transfer protocol is designed to be as simple as possible and to be a natural extension of the MQTT protocol. It is based on the MQTT 5.0 specification and uses the same primitives as the base protocol. To support this protocol, a device should know about only a few special topics and reason codes in `PUBACK` packets that provide feedback. Generally, the device needs to send a *command* which is essentially a message published to a special topic, and then wait for the server to respond with a `PUBACK` packet. This `PUBACK` will contain a reason code that indicates whether the broker successfully handled the command. However, this is not a hard requirement, and some dumb devices may choose to ignore the feedback and send commands blindly.

Files are transferred in segments, and each segment is sent as a separate *command*. The broker does not enforce any bounds on the size of the segments, and the device is free to choose any convenient size. The segments do not even have to be of the same size. The device can send them in any order or send the same segment multiple times. The broker should handle all these cases correctly and will reassemble the file on the server side.[^1]

[^1]: However, the broker might take some actions if it thinks that the device is misbehaving. For example, it might limit the total number of segments the device sends for a single file or outright disconnect the device if it sends them in some weird order.

Moreover, the broker does not require the device to complete the transfer in a single session. The device can disconnect at any time and then reconnect and continue the transfer from the point where it left off. Or even restart it from the beginning. For that to work, the broker requires the device to assign a unique *file id* to each transfer. The device must send this identifier in each command and should not reuse it for different transfers.

Once all the segments are sent, the device should send a special *command* to indicate the transfer is complete. The broker will then assemble the file and make it available for download. To accommodate different integration scenarios, depending on the configuration, EMQX may choose to store the file in a local file system or upload it to cloud storage, thus keeping that complexity away from the device.

![Protocol flow outline](https://assets.emqx.com/images/7ab0e639687e4dbb1eff3b7a44fff1d6.png)

<center>Protocol flow outline</center>

## Use Case: Transfer High-Resolution Pictures of Industry Camera

Let's take that industry camera example from the introduction and implement this use case using the File Transfer protocol. Imagine a camera took a picture of a product rolling off the conveyor belt and saved it to a file named `QACAM/20230707/PC123456.jpg`. Now it needs to send this file to a broker for further processing. We assume the camera is already connected to the broker and sends it some telemetry data, so it already has an established MQTT connection. We consider only the happy path here and do not handle any error cases. We'll come back to them later.

> We'll use the [mqttx-cli](https://mqttx.app/cli) to illustrate the interactions between the camera and EMQX.

### Initiate the Transfer 

First, the camera needs to pick a unique *file id*. Assuming it has access to a random number generator, the camera can generate UUIDs. For this transfer, let's say it picked `0d7cd07cc4cf4a0ab072259297f4e41b`. 

Then, using the same MQTT connection that it uses for telemetry data, the camera publishes a command to start the transfer:

```
$ mqttx-cli pub -h broker.emqx.io \
    --topic '$file/0d7cd07cc4cf4a0ab072259297f4e41b/init' \
    --qos 1 \
    -m '{
    "name": "QACAM_20230707_PC123456.jpg",
    "size": 1234567,
    "user_data": {"pipeline": "QA42"}
}'
```

Here the camera sends a JSON payload with metadata about the file, such as its name, size, and additional user data it wants to associate with the transfer. The only required field is the file name. The rest are optional. EMQX will store this metadata and make it available later to anyone interested once the transfer is complete.

The camera publishes this metadata to a special topic that represents *init file transfer* command. Furthermore, all commands related to this file transfer should be published to topics that start with `$file/0d7cd07cc4cf4a0ab072259297f4e41b/`. That's how the broker knows these commands are related to the same file transfer.

EMQX does not allow arbitrary directory hierarchies in the file names and will reject the command if it contains any slashes. That's why the name of the file became `QACAM_20230707_PC123456.jpg`.

The broker will eventually respond with a `PUBACK` packet with a Reason Code of `0` (which means *Success*). The camera can now start sending the segments.

### Send the Segments

Having a 1.2 MiB large file, the camera decides to split it into 10 segments of 128 KiB each. It then sends each segment as a separate command.

```
$ mqttx-cli pub -h broker.emqx.io --topic '$file/0d7cd07cc4cf4a0ab072259297f4e41b/0' --qos 1 -m '<bytes 0-131072>'
$ mqttx-cli pub -h broker.emqx.io --topic '$file/0d7cd07cc4cf4a0ab072259297f4e41b/131072' --qos 1 -m '<bytes 131072-262144>'
$ mqttx-cli pub -h broker.emqx.io --topic '$file/0d7cd07cc4cf4a0ab072259297f4e41b/262144' --qos 1 -m '<bytes 262144-393216>'
...
$ mqttx-cli pub -h broker.emqx.io --topic '$file/0d7cd07cc4cf4a0ab072259297f4e41b/1179648' --qos 1 -m '<bytes 1179648-1234567>'
```

The topic name for each command contains the offset of the segment into the file, and the message payload is simply the segment itself. The broker should eventually respond with a `PUBACK` packet with a Reason Code of `0` for each command which means that it saved the corresponding segment successfully.

The camera may even decide to change the size of the segments in the middle of the transfer, for example, after a network hiccup and disconnection. It can do that by simply sending segments of a different size. EMQX will handle that correctly, even if the camera reconnects to another node in the cluster after the disconnection.

Here, after reconnection, the camera decides to send the remaining segments in 32 KiB chunks instead.

```
$ mqttx-cli pub -h broker.emqx.io --topic '$file/0d7cd07cc4cf4a0ab072259297f4e41b/262144' --qos 1 -m '<bytes 262144-294912>'
$ mqttx-cli pub -h broker.emqx.io --topic '$file/0d7cd07cc4cf4a0ab072259297f4e41b/294912' --qos 1 -m '<bytes 294912-327680>'
...
$ mqttx-cli pub -h broker.emqx.io --topic '$file/0d7cd07cc4cf4a0ab072259297f4e41b/1179648' --qos 1 -m '<bytes 1212416-1234567>'
```

As before, the broker will respond with `PUBACK`s containing `0` Reason Code.

### Complete the Transfer

Once all the chunks are sent, the camera sends a final command to indicate that the transfer is complete:

```
$ mqttx-cli pub -h broker.emqx.io \
    --topic '$file/0d7cd07cc4cf4a0ab072259297f4e41b/fin/1234567/1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef' \
    --qos 1 \
    -m ''
```

The topic name for this command contains the file size and the SHA-256 hash of the file contents. It is not strictly required, but it allows the broker to verify that the file was transferred correctly.

With knowledge of the file size and all the segments sent so far, EMQX can start assembling the file. It might take a long time, depending on the file size, the number of segments, how they are distributed across the cluster, and where the file's final destination should be (local storage, S3 bucket, etc.). Once the broker assembles the file, and the SHA-256 hash of the file contents matches the one the camera sent, the broker once again will respond with a `PUBACK` packet with `0` Reason Code.

Congratulations! The file is now transferred and is available for further processing. Depending on EMQX configuration, the file is stored locally or uploaded to an S3 bucket.

### Legacy Clients

If the camera in our example is a legacy client that does not support MQTT 5.0, it can still use the File Transfer protocol. It will come at the cost of missing feedback due to the lack of [Reason Codes](https://www.emqx.com/en/blog/mqtt5-new-features-reason-code-and-ack) in the `PUBACK` packets. The camera has to assume that the broker received and successfully handled each command and will either have to retry them in case of a disconnection or abandon the transfer altogether, depending on use case requirements.

> To explore the protocol in more detail, please refer to [EIP: File transfer over MQTT](https://github.com/emqx/eip/blob/main/implemented/0021-transfer-files-over-mqtt.md) to understand what are the clients and the broker's requirements and expectations, and error-handling strategies. 

## Final words

The File Transfer over MQTT feature has seen its initial release in EMQX Enterprise 5.1. It is still in active development, and we are working on improving it further. You are always welcome to try it out and share your feedback with us.

To help you get started, we have prepared a [documentation chapter](https://docs.emqx.com/en/enterprise/v5.1/file-transfer/introduction.html) that describes various aspects of operation and configuration. Moreover, we have prepared a couple of [demo](https://github.com/emqx/MQTT-Client-Examples/blob/7d9102a5/mqtt-client-Python3/file_transfer.py) [client](https://github.com/emqx/MQTT-Client-Examples/blob/7d9102a5/mqtt-client-C-paho/emqx_file_transfer.c) [applications](https://github.com/emqx/MQTT-Client-Examples/blob/7d9102a5/mqtt-client-Java/src/main/java/io/emqx/mqtt/MqttFileTransferSample.java) using different programming languages and [MQTT libraries](https://www.emqx.com/en/mqtt-client-sdk).



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
