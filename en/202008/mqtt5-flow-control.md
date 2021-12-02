MQTT v5 brings a lot of new features, we will show these features in an easy-to-understand way and discuss the impact of these features on the developer. So far, we have discussed these [new features of MQTT v5](https://www.emqx.com/en/mqtt/mqtt5). Now, we will continue discussing: **flow control**.



## Flow control

Usually, the resources of the server are fixed and limited, while the flow of the client may change anytime and anywhere. The normal business (users centrally accessing and many devices restarting) is maliciously attacked and the network fluctuation will cause the flow dramatically increasing. If the server does not limit the flow, the load will sharply increase, and then will cause the speed of responding decreasing, affect other businesses and even cause system breakdown.

![image20200730133959150.png](https://static.emqx.net/images/c5d21ba2ca945005ba8477cd0d6debbf.png)

Therefore, we need flow control, it can be the sending rate for limiting the sender or receiving rate for limiting the receiver, and the final goal is to ensure the stability of the system. The common flow control algorithms are sliding window counting method, leaky bucket algorithm and token bucket algorithm.

MQTT v3 has not standardized the flow control behavior, which will cause the client and server to implement it variously, and then affect the access and management of devices. However, MQTT v5 has already introduced the flow control function, and this is also what we will discuss next.



## The flow control in MQTT v5

In MQTT v5, the sender has one initial sending quota. Ever time it sends a PUBLISH packet with QoS which is greater than 0, the sending quota is reduced by one. However, whenever it receives a response packet(PUBACK and PUBCOMP or PUBREC), the sending quota is increased by one. If the receiver does not respond immediately, it will cause the sending quota is reduced to 0 and the sender should stop sending all the PUBLISH packet with QoS which is greater than 0 until the sending quota recovering. We can think of it as a variant token bucket algorithm, the only difference is changing the method for increasing quota from a fixed rate to the actual received response packets rate.

This algorithm can use the resources more positively and fully because it does not limit the receiving rate, and then the sending rate totally depends on the response rate of the opposite and network situation. If the receiver is available and has a good network, the sender will have a relatively high sending rate. Otherwise, it will be limited to a relatively low sending rate.



## Receive Maximum attribute

MQTT v5 added a Receive Maximum attribute for supporting flow control. It exists in the CONNECT packet and CONNACK packet and indicates the largest number of PUBLISH packet with the QoS which is 1 and 2 that the client and server willing to process simultaneously, that is the maximum sending quota that the opposite can use.

![image20200730173320715.png](https://static.emqx.net/images/7dc9e6680507322a743d721db1def117.png)

## Why do not have QoS 0 ?

Maybe you already find that attributives are used in all the places where PUBLISH messages are mentioned in the previous article: QoS is greater than 0. The features of the QoS 0 message determine that there is no response packet. You may think that the QoS 0 messages are not very important and the receiver can restrict  QoS 0 message through the mandatory receiving rate limit, or there are other reasons. All in all, finally, we see that the flow control mechanism of MQTT v5 completely relying on the response packet, which causes the flow control can only exist in QoS 1, 2 messages.

MQTT v5 gives an imperfect solution or it is just a suggestion: when the sending quota is reduced to 0, the sender can choose to continue sending PUBLISH packets with QoS 0, or to suspend sending. The logic of suspending sending is: if the response speed of the PUBLISH packet with QoS 1,2 becomes slow, it usually means that the spending power of the receiver has declined. If the sender continues to send QoS 0 messages, the situation will become worse.



## Summary

Although the flow control mechanism of MQTT v5 still has some shortages, we still suggest that users use it. The sending quota algorithm based on the response packet enables the sender to maximize the use of resources. Receive Maximum enables both communication parties do not need to negotiate the sending quota in advance, thus get greater transparency and flexibility, which is really useful for accessing multi-vendor equipment.
