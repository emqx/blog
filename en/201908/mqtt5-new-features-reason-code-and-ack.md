## MQTT v3.1.1 

MQTT v3.1.1 protocol has only 10 return codes. These return codes can represent little meaning, and the same return code value can have different meanings in different messages.

### CONNACK Packet

There are only 6 return codes in the CONNECT packet. Only when the return code of the CONNACK packet sent back by the server is 0, the connection is successfully established.

|  值   |                           返回码                           |                             描述                             |
| :---: | :--------------------------------------------------------: | :----------------------------------------------------------: |
|   0   |                  0x00 Connection accepted                  |                     Connection accepted                      |
|   1   | 0x01  Connection rejected for unsupported protocol version | The server does not support the MQTT protocol requested by the client. |
|   2   |      0x02 Connection rejected for rejected client ID       | The client ID is the correct UTF-8 string, but is not allowed by the server |
|   3   |      0x03 Connection rejected for unavailable server       | Network connection has been established, but MQTT service is unavailable |
|   4   | 0x04 Connection rejected for damaged username or password  | The data in the username or password is in the wrong format  |
|   5   |         0x05 Connection rejected for unauthorized          |             Client connection is not authorized              |
| 6-255 |                                                            |                     Reserved for future                      |

### SUBACK Packet

There are only 4 return codes in the SUBACK packet.

| Value | Return code  | Description                   |
| ----- | ------------ | ----------------------------- |
| 0     | 0x00 success | Maximum granted QoS 0 message |
| 1     | 0x01 success | Maximum granted QoS 1 message |
| 2     | 0x02 success | Maximum granted QoS 2 message |
| 128   | 0x80 Failure | Failure                       |

There are 4 return codes in the SUBACK packet. Except that the return code 0x80 indicates failure, the other return codes indicate that the subscription is successful, and the three values 0, 1, 2 represent the maximum QoS value of the subscribed message.

## MQTT v5.0

The MQTT v5.0 protocol renames the return code to a reason code, adding a reason code to indicate more types of errors.

The following table is a list of reason codes that represent the value of the reason code and the control packet containing the reason code:

| Decimal | Hexadecimal | Name                                   | Packet                                                   |
| ------- | ----------- | -------------------------------------- | -------------------------------------------------------- |
| 0       | 0x00        | Success                                | CONNACK, PUBACK, PUBREC, PUBREL, PUBCOMP, UNSUBACK, AUTH |
| 0       | 0x00        | Granted QoS 0                          | SUBACK                                                   |
| 1       | 0x01        | Granted QoS 1                          | SUBACK                                                   |
| 2       | 0x02        | Granted QoS 2                          | SUBACK                                                   |
| 4       | 0x04        | Disconnect with Will Message           | DISCONNECT                                               |
| 16      | 0x10        | No matching subscribers                | PUBACK, PUBREC                                           |
| 17      | 0x11        | No subscription existed                | UNSUBACK                                                 |
| 24      | 0x18        | Continue authentication                | AUTH                                                     |
| 25      | 0x19        | Re-authenticate                        | AUTH                                                     |
| 128     | 0x80        | Unspecified error                      | CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT    |
| 129     | 0x81        | Malformed Packet                       | CONNACK, DISCONNECT                                      |
| 130     | 0x82        | Protocol Error                         | CONNACK, DISCONNECT                                      |
| 131     | 0x83        | Implementation specific error          | CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT    |
| 132     | 0x84        | Unsupported Protocol Version           | CONNACK                                                  |
| 133     | 0x85        | Client Identifier not valid            | CONNACK                                                  |
| 134     | 0x86        | Bad User Name or Password              | CONNACK                                                  |
| 135     | 0x87        | Not authorized                         | CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT    |
| 136     | 0x88        | Server unavailable                     | CONNACK                                                  |
| 137     | 0x89        | Server busy                            | CONNACK, DISCONNECT                                      |
| 138     | 0x8A        | Banned                                 | CONNACK                                                  |
| 139     | 0x8B        | Server shutting down                   | DISCONNECT                                               |
| 140     | 0x8C        | Bad authentication method              | CONNACK, DISCONNECT                                      |
| 141     | 0x8D        | Keep Alive timeout                     | DISCONNECT                                               |
| 142     | 0x8E        | Session taken over                     | DISCONNECT                                               |
| 143     | 0x8F        | Topic Filter invalid                   | SUBACK, UNSUBACK, DISCONNECT                             |
| 144     | 0x90        | Topic Name invalid                     | CONNACK, PUBACK, PUBREC, DISCONNECT                      |
| 145     | 0x91        | Packet Identifier in use               | PUBACK, PUBREC, SUBACK, UNSUBACK                         |
| 146     | 0x92        | Packet Identifier not found            | PUBREL, PUBCOMP                                          |
| 147     | 0x93        | Receive Maximum exceeded               | DISCONNECT                                               |
| 148     | 0x94        | Topic Alias invalid                    | DISCONNECT                                               |
| 149     | 0x95        | Packet too large                       | CONNACK, DISCONNECT                                      |
| 150     | 0x96        | Message rate too high                  | DISCONNECT                                               |
| 151     | 0x97        | Quota exceeded                         | CONNACK, PUBACK, PUBREC, SUBACK, DISCONNECT              |
| 152     | 0x98        | Administrative action                  | DISCONNECT                                               |
| 153     | 0x99        | Payload format invalid                 | PUBACK, PUBREC, DISCONNECT                               |
| 154     | 0x9A        | Retain not supported                   | CONNACK, DISCONNECT                                      |
| 155     | 0x9B        | QoS not supported                      | CONNACK, DISCONNECT                                      |
| 156     | 0x9C        | Use another server                     | CONNACK, DISCONNECT                                      |
| 157     | 0x9D        | Server moved                           | CONNACK, DISCONNECT                                      |
| 158     | 0x9E        | Shared Subscription not supported      | SUBACK, DISCONNECT                                       |
| 159     | 0x9F        | Connection rate exceeded               | CONNACK, DISCONNECT                                      |
| 160     | 0xA0        | Maximum connect time                   | DISCONNECT                                               |
| 161     | 0xA1        | Subscription Identifiers not supported | SUBACK, DISCONNECT                                       |
| 162     | 0xA2        | Wildcard Subscription not supported    | SUBACK, DISCONNECT                                       |

The reason code is a single-byte unsigned value used to indicate the result of the operation. The reason code less than 0x80 indicates that the result of the operation is successful. Under normal circumstances, the reason code value returned by the operation is 0. If the reason code returned is greater than or equal to 0x80, the operation has failed.

The reason codes for CONNACK, PUBACK, PUBREC, PUBREL, PUBCOMP, DISCONNECT and AUTH control packets are stored in the variable header. The SUBACK and UNSUBACK packets contain a list of reason codes in the payload.
