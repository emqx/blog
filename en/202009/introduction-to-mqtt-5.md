### Introduction to MQTT

The [MQTT protocol](https://www.emqx.com/en/mqtt) is the most popular IoT protocol in the world today because of its lightweight and flexibility. It has been widely used in IoV, smart homes, logistics, live chat applications and mobile messaging fields and connected hundreds of millions of devices. There are countless devices are using and accessing the MQTT protocol every second of every day. The MQTT protocol provides a stable and reliable communication foundation for these devices. The large number of accesses to these devices also challenges the MQTT protocol specification. The birth of [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) is to better meet this need.

### The history of MQTT

MQTT(message queue telemetry transmission) was originally invented by IBM in the late 1990s. It was originally used to link sensors on an oil pipeline to satellites, so MQTT was designed from the start for limited devices and low-bandwidth, high-latency or unreliable networks. It uses a publish-subscribe model, decouples the sender and receiver of messages in space and time, and provides a stable and reliable network connection based on TCP/IP, has a very lightweight header for reducing transmission cost, supports reliable messaging. So, we can say that it was born to meet the various needs of the IoT scenario. Four years after the MQTT 3.1.1 has been released and became the OASIS standard, MQTT 5.0 was released, which is a significant improvement and upgrade. It is not only to meet the need of the industry at this stage, but to fully prepare the changes in the development of industry in the future. In March 2019, MQTT 5.0 became the new OASIS standard.

### The design goals of MQTT 5.0

With the rapidly increasing number of devices and ever-increasing requirements, the OASIS MQTT technical committee needs to extract the generic parts from the complex requirements, adds these to the standard specification. Also, need to improve performance and ease of use with as little overhead as possible or without reducing ease of use and without adding unnecessary complexity.

Finally, the OASIS MQTT technical committee provides many new functions and features for MQTT 5.0. MQTT 5.0 became one of the most changed versions of MQTT ever. Here, we will list some relatively important features:

- The improved error reporting. All response packet will now include a reason code and an optional and easy-to-read reason string.
- Specification of generic models, including capability discovery, request-response, etc.
- The support for the shared subscription protocol, previously there were no shared subscriptions in the standard, and shared subscriptions were defined by each software manufacturer and were not common.
- A new extension mechanism, including the user attribute.
- Introducing new features such as topic aliases to further reduce transmission costs.
- Session expiry interval and message expiry interval have been added to improve the inflexibility of the Clean Session in the old version.

The complete list for new attributes is included in appendix C in the protocol standard, you can access the following URL for more details: https://docs.oasis-open.org/mqtt/mqtt/v5.0/cs02/mqtt-v5.0-cs02.html#AppendixC.



### Embrace MQTT 5.0

As various [MQTT broker](https://www.emqx.com/en/products/emqx) manufacturers continue to join the MQTT 5.0 support camp (for example, EMQ has fully supported the MQTT 5.0 protocol in September 2018), the gradual migration of the entire industry ecology to MQTT 5.0 has become the general trend. The MQTT 5.0 will be the first choice of the vast majority of IoT enterprises in the future.

We also want the user to embrace MQTT 5.0 early and enjoy the benefits it brings, which is also the purpose of this article. If you've already interested in MQTT 5.0 but still want to know more, you can try reading the following article. We will introduce you to the key features of MQTT 5.0 in an easy-to-understand way.

- [Clean Start and Session Expiry Interval ](https://www.emqx.com/en/blog/mqtt5-new-feature-clean-start-and-session-expiry-interval)
- Message expiry interval
- [Reason code and ACK](https://www.emqx.com/en/blog/mqtt5-new-features-reason-code-and-ack)
- [Payload Format Indicator and Content Type](https://www.emqx.com/en/blog/mqtt5-new-features-payload-format-indicator-and-content-type)
- [Request Response](https://www.emqx.com/en/blog/mqtt5-request-response)
- [Shared subscription](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription)
- [Subscription identifier and subscription options](https://www.emqx.com/en/blog/subscription-identifier-and-subscription-options)
- Topic aliases
- [Flow control](https://www.emqx.com/en/blog/mqtt5-flow-control)
- User attribute
- Enhanced authentication

