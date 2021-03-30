

MQTT 5.0 协议相比 MQTT 3.1.1 增加了很多属性，这些属性分布于报文的可变头部 ( Variable Header ) 和有效载荷 ( Payload ) 中。

MQTT 5.0 协议中携带有效载荷的报文有 CONNECT 报文，PUBLISH 报文，SUBSCRIBE 报文，SUBACK 报文，UNSUBSCRIBE 报文和 UNSUBACK 报文。

PUBLISH 报文的有效载荷负责存储消息内容，与 MQTT 3.1.1 协议相同。

### CONNECT 报文

**CONNECT 报文的可变头部新增的属性有:**

![1.png](https://static.emqx.net/images/90f25b5ca8dc4e5501b4d0ed41e7cf74.png)



在 CONNECT 报文的 Payload 中，部分字段发生了变化，遗嘱消息（Will Message）变成了遗嘱载荷（Will Payload）。Payload 中新增了遗嘱属性（Will Properties），用于定义遗嘱消息的行为。

**新增的遗嘱属性有:**

![2.png](https://static.emqx.net/images/bdabfdce4a61eb236fca3c2816405093.png)



### CONNACK 报文

**CONNACK 报文没有 Payload，在可变头部中包含的属性有：**

![3.png](https://static.emqx.net/images/a1af2211b756e665c1b891ec78acba13.png)

### PUBLISH 报文

**PUBLISH 报文可变头部的属性有：**

![PUBLISH 报文  .png](https://static.emqx.net/images/50b3fafb8cf564389baa62a46e781342.png)



### PUBACK, PUBREC, PUBREL, PUBCOMP, SUBACK, UNSUBACK 报文

**PUBACK, PUBREC, PUBREL, PUBCOMP, SUBACK, UNSUBACK 都具备以下三个属性：**
![PUBACK, PUBREC, PUBREL, PUBCOMP, SUBACK, UNSUBACK 报文.png](https://static.emqx.net/images/3b2c016167ebb30a40a055d446e32347.png)


### SUBSCRIBE 报文

**SUBSCRIBE 报文的属性同样存在可变头部中。**


![1111.png](https://static.emqx.net/images/b9109207f7d9ff0c924df16164c7a8e7.png)


MQTT 5.0 中 SUBSCRIBE 报文中的 Payload 包含了订阅选项(Subscription Options)。


![SUBSCRIBE 报文2.png](https://static.emqx.net/images/775c3841412fde11076e59f530a97b78.png)


订阅选项(Subscription Options)的第 0 位和第 1 位表示 QoS 最大值。该字段给出了服务器可以发送给客户端应用消息的最大 QoS 等级。如果 QoS 值为 3，就会触发协议错误。

订阅选项第 2 位表示非本地选项(No Local)。如果值为 1，应用消息就不会发布给订阅发布主题的发布者本身，如果在共享订阅中将该选项设置为 1 的话，就会触发协议错误。

订阅选项的第 3 位表示保留为已发布(Retain As Published)。若该值为 1，服务器须将转发消息的 RETAIN flag 设为与接收到的 PUBLISH 报文的 RETAIN flag 一致。若该值为 0，不管接收到的 PUBLISH 报文中的 RETAIN flag 是何值，服务器都需将转发消息的 RETAIN flag 置为 0。

订阅选项的第 4 第 5 位表示保留处理 (Retain Handling)。该选项是用来控制保留消息 (retained message) 的发送。当保留处理的值为 0 时，服务器须将保留消息转发到与订阅匹配的主题上去。当该值为 1 时，如果订阅已经不存在了，那么服务器需要将保留消息转发给与订阅匹配的主题上，但是如果订阅存在，服务器就无法再转发保留消息。当该值为 2 时，服务器不转发保留消息。

订阅选项的第 6 第 7 位是预留给未来使用的。如果有效载荷的任何一个预留位非零，那么服务器就会将该报文视为格式错误的报文。

### UNSUBSCRIBE 报文

UNSUBSCRIBE 报文仅有两个属性：属性长度和用户属性。

UNSUBSCRIBE 报文的载荷相比 SUBSCRIBE 的载荷要简单很多，它仅仅只是包含主题过滤器的列表，并不包含各种各样的订阅选项。

服务器就会将该报文视为格式错误的报文。

### DISCONNECT 报文(新增)

**DISCONNECT 报文是 MQTT 5.0 新增的报文，它的引入意味着 mqtt broker 拥有了主动断开连接的能力。DISCONNECT 报文所具备的属性有：**

![DISCONNECT 报文新增.png](https://static.emqx.net/images/f6aa8921e06244d319c110a9cfdbdb90.png)


