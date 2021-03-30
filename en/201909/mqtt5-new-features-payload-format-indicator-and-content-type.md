Payload Format Indicators and Content Type are two new properties introduced in MQTT 5.0.

## Payload Format Indicator

In all packet types of MQTT 5.0, this property exists only in the will property of PUBLISH packet and CONNECT packet.

Payload Format Indicator occupies only one byte size, and has only two values, 0 (0x00) and 1 (0x01).

In the MQTT CONNECT packet, when the value of the Payload Format Indicator of the will property is 0, it means that the will message is an undetermined byte. When the value of the property is 1, it means that the test message is UTF-8 encoded character data. The data in Will Payload must conform to the definition of standard UTF-8.

In the MQTT PUBLISH packet, when the value of the Payload Format Indicator of the PUBLISH property is 0, it means that the PUBLISH message is an undetermined byte. When the value of the property is 1, it means that the payload of the PUBLISH packet is UTF-8 encoded character data. The data in the Payload of PUBLISH packet must conform to the definition of the standard UTF-8.

## Content Type

In all packet types of MQTT 5.0, this property also exists only in the will property of PUBLISH packet and CONNECT packet. This property stores UTF-8 encoded strings that describe the contents of a will message or a PUBLISH message.

It is determined by the application that sends and receives messages. The content type cannot be tampered with during message forwarding.

A typical application of content types is to store MIME types, such as text/plain for text files and audio/aac for audio files.



