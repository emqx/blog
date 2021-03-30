

有效载荷标识（Payload Format Indicator）与内容类型（Content Type）是 MQTT 5.0 新引入的两个属性。

## 有效载荷标识（Payload Format Indicator）

在 MQTT 5.0 的所有报文类型中，该属性只存在于 PUBLISH 报文和 CONNECT 报文的遗嘱属性中。

有效载荷标识只占据一个字节大小，它只有 0(0x00) 和 1(0x01) 两个值。

MQTT CONNECT 报文中，当遗嘱属性的有效载荷标识的值为 0 时，意味着遗嘱消息是未确定的字节，当该属性值为 1 时，意味着遗嘱消息是 UTF-8 编码的字符数据，遗嘱载荷（Will Payload）中的数据必须符合标准 UTF-8 的定义。

MQTT PUBLISH 报文中，当 PUBLISH 属性的有效载荷标识的值为 0 时，意味着 PUBLISH 消息是未确定的字节，当该属性值为 1 时，意味着 PUBLISH 报文的有效载荷是 UTF-8 编码的字符数据，PUBLISH 报文载荷（Payload）中的数据必须符合标准 UTF-8 的定义。

## 内容类型（Content Type）

在 MQTT 5.0 的所有报文类型中，该属性同样只存在于 PUBLISH 报文和 CONNECT 报文的遗嘱属性中。该属性存放的是 UTF-8 编码的字符串，用于描述遗嘱消息或 PUBLISH 消息的内容。

它是由收发消息的应用程序决定的。在消息转发过程中， 内容类型不能被篡改。

内容类型的一个比较典型的应用就是存放 MIME 类型，比如 text/plain 表示文本文件，audio/aac 表示音频文件。

