CAN bus is a widely used communication protocol for automotive and industrial applications, enabling multiple devices to interact within a single network. Meanwhile, [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) emerges as a lightweight publish-subscribe messaging protocol extensively utilized in IoT applications, facilitating machine-to-machine communication.

Integrating CAN bus devices with other IoT platforms and applications can be achieved by bridging the data to MQTT. Although various solutions or tools exist for this purpose, they typically transmit raw binary CAN data, making it challenging to filter at the signal level and subsequently process in successive applications. 

In this blog, we will offer a new solution implemented via [eKuiper, an open-source edge streaming SQL engine](https://ekuiper.org/), enabling the seamless bridging of meaningful data and selectively demanded signals from CAN bus to MQTT.

## How CAN Bus Talks

CAN bus is a communication system that allows different devices in a vehicle to exchange data. It can tell you information such as the speed, fuel level, engine temperature, and diagnostic codes of your car. However, it is not easy to understand and extract these information from CAN bus because it is in binary format.

> Read our post to learn more about CAN Bus: [CAN Bus: How It Works, Pros and Cons, and Fast Local Processing Tutorial](https://www.emqx.com/en/blog/can-bus-how-it-works-pros-and-cons) 

### CAN Frame

From CAN bus, we can receive a stream of CAN frames, which contains those signals that we are interested in the binary form. Each CAN frame contains an ID, a data length code (DLC), and the payload data. 

- The ID is used to identify the type of data contained in the frame. 
- The DLC is used to specify the number of bytes of data in the frame. 
- The payload data is the actual data contained in the frame. 

There are several types of CAN protocols that define slightly different ID and payload length. Below is a CAN 2.0A frame whose ID is 11 bits and payload length is up to 8 bytes.

![CAN 2.0A frame](https://assets.emqx.com/images/aa1030c3e586222227d7c20357d77efd.png)

Inside the payload, the data is organized in signals. Each signal has a name, a length, and a value. 

- The length is the number of bits that the signal occupies in the payload. 
- The value is the actual data contained in the signal. 

To translate the binary data into meaningful information, we need to extract these signals.

### Signal Extraction

CAN Database (DBC) is a text file to describe the organization of signals inside the CAN frame payload. It is like a dictionary that tells you the name, length, and value of each signal so that we can listen and talk by CAN frame.

Below is a snippet of DBC file. It defines a CAN frame with ID 544 and DLC 8. It contains 5 signals, each of which has a name, a length, and a value. For example, the signal EngineSpeed has a length of 16 bits and a value range from 0 to 16383.75. The value of the signal is calculated by multiplying the raw data by 0.25 and adding 0.

```
BO_ 544 EMS_220h: 8 EMS
 SG_ EngineSpeed : 0|16@1+ (0.25,0) [0|16383.75] "rpm" Vector__XXX
 SG_ CurrentEngineTorque : 16|16@1+ (0.25,-500) [-500|1547.5] "Nm" Vector__XXX
 SG_ DriverRequestTorque : 32|16@1+ (0.25,-500) [-500|1547.5] "Nm" Vector__XXX
 SG_ CurrentEngineTorqueStatus : 48|1@1+ (1,0) [0|1] "" Vector__XXX
 SG_ DriverRequestTorqueStatus : 49|1@1+ (1,0) [0|1] "" Vector__XXX
```

The flow to decode CAN frame is as below:

![The flow to decode CAN frame](https://assets.emqx.com/images/2a92a31f0cbff93106d13adcf33e10d1.png)

Finally, we know the engine speed is 1000 rpm after the trivial decoding process. Once the signals are changed or updated, we'll need to re-develop the process and deploy it by OTA. eKuiper can help you to avoid this tedious work.

### Secure Your DBC

DBC is the key to decoding CAN frame. Without DBC, even CAN bus data is dismissed, it is nearly impossible to decode them. Thus, DBC is a valuable asset for your business and should not be disclosed to others, including the engineers who develop the decoding process. eKuiper can load DBC file in runtime without exposing it to the developers. And it can hot reload the DBC file without restarting the process when scenarios change. This can help you to secure your DBC file by keeping it private.

## eKuiper Understands CAN bus

As an edge streaming engine, eKuiper is small enough to deploy near the CAN bus devices. It can collect data from various southbound data sources like HTTP, FileSystem, MQTT, and now CAN bus. The collected data can be efficiently processed and subsequently published to northbound data sources like MQTT and HTTP.

> Notice: Some of the features related to the CAN bus described in this document are not open source. You can experiment with these features by utilizing [ek-can](https://hub.docker.com/r/emqx/ek-can), which extends CAN bus capabilities on top of eKuiper.

eKuiper understands CAN bud data. It eases the CAN frame decoding and transforms it into just some configurations. To consume CAN bus data, you can create a stream using the following SQL statement:

```
CREATE STREAM canDemo () WITH (TYPE="can", FORMAT="can", SHARED="TRUE", SCHEMAID="dbc")
```

This statement creates a stream named canDemo, which consumes data from CAN bus. It specifies the connection, format, and DBC as schema which will decode the CAN frame into signals.

### DBC Setting

The DBC files work as schemas when decoding CAN frames. Just like specifying *.proto files for protobuf format, you can specify the DBC file by setting the SCHEMAID property which refers to a file path or directory path. That means you can specify a single DBC file or a directory that contains multiple DBC files. eKuiper will load all the DBC files in the directory and use them as schemas.

In the runtime, users can update the DBC file by replacing the file or adding new files to the directory. eKuiper will hot reload the DBC files and use the new schemas to decode CAN frames by restarting rules. This can help you to secure your DBC file by keeping it private.

### Connection and Format Separation

In the stream creation statement, we have specified `type` and `format` to “can” respectively. This is because eKuiper separates the connection and format of the data source. 

- The `type` property specifies the connection, which is the CAN bus in this case. 
- The `format` property specifies the format of the data, which is the CAN frame in this case.

This separation allows eKuiper to support different combinations of CAN frame and its transmission protocol, which is common when using some CAN adaptors. The CAN adaptors may log the CAN frame into a file, send the raw CAN frame to an [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison), or send the batch CAN frames by TCP or UDP packets. In these cases, the `type` property will be file or ”mqtt“ respectively, and the `format` property will be can.

If the type is “can”, eKuiper will connect to CAN bus by socketCan. In the below example, eKuiper consumes CAN frames in a file:

```
CREATE STREAM canDemo () WITH (TYPE="file", FORMAT="can", SHARED="TRUE", SCHEMAID="dbc") 
```

## Bridge CAN Bus to MQTT at Your Will

The CAN Bus device sends periodic messages with a high frequency like 100HZ over the bus. Due to storage or bandwidth constraint, we may only need to sample the data in lower frequency and filter only demanded signals. With eKuiper, we can:

- Sample the data by specifying the sampling rate.
- Filter the data in signal level by specifying the demanded signals.
- Bridge only changed signals.
- Combine signals from different CAN frames into one message.

All of these can be done by rule SQL and change with nearly no cost because of the rule hot reload capability. Let's see some examples.

```
## Filter the signals
SELECT EnginSpeed, DriverRequestTorqueStatus FROM canDemo
## Combine signals from different CAN frames
SELECT latest(EnginSpeed) as speed, latest(anotherSignal) as anotherSignal FROM canDemo
## Bridge only changed signals
SELECT CHANGED_COLS(EngineSpeed, DriverRequestTorqueStatus) FROM canDemo
```

Once getting the demanded signals, we will need to decide which [MQTT topic](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) to publish to. Users can specify a topic name or use a dynamic topic name derived from the data.

For example, in the below rules, each parsed CAN frame signal will be bridged to MQTT topic `can/{{CanId}}`. The `{{CanId}}` is a dynamic topic name derived from the data, which means a CAN frame with CAN id 123 will be bridged to MQTT topic `can/123`.

```
{
  "id": "distributeRule",
  "sql": "SELECT *, meta(id) as canId FROM canDemo",
  "actions": [
    {
      "mqtt": {
        "server": "tcp://broker.emqx.io:1883",
        "topic": "can/{{.canId}}",
        "sendSingle": true
      }
    }
  ]
}
```

eKuiper allows multiple rules to deal with a single stream. So users can create as many rules as needed to bridge all kinds of CAN bus data to MQTT with organized topics.

<section
  class="promotion-pdf"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/a4b8936bb3d27fbccd734eccbe3f821b.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="promotion-pdf__title" style="
    line-height: 1.2;
">
      Rev Up Your Connected Vehicles Future with MQTT
    </div>
    <div class="promotion-pdf__desc">
      The key to building a scalable, secure system for your connected-vehicles business.
    </div>
    <a href="https://www.emqx.com/en/resources/driving-the-future-of-connected-cars-with-mqtt?utm_campaign=embedded-driving-the-future-of-connected-cars-with-mqtt&from=blog-bridging-demanded-signals-from-can-bus-to-mqtt-by-ekuiper" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## Conclusion

To bridge the gap between CAN bus and MQTT, we need a solution that can read data from CAN bus devices, filter and transform the data according to our needs, and publish the data to MQTT brokers. This is where eKuiper comes in handy, providing a simple, performant and flexible way to do the job.

Besides bridging, eKuiper can also help in various scenarios regarding edge rule engine and computing. We will talk about them in the next article.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
