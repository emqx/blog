MQTT v5 brings lots of new features, and we will try our best to present these features in an easy-to-understand way and discuss the impact of these features on developers. So far, we have discussed these [new features of MQTT v5](https://www.emqx.com/en/blog/introduction-to-mqtt-5). Today, we will continue to discuss: **enhanced authentication**.

In the IoT scenario, the safe design is a very important part of the process. Leakage of sensitive data or unauthorized control of edge devices are unacceptable, but compared to other scenarios, the IoT project still has the following limitations:

- Can't balance security and high performance;
- Encryption algorithms require more computing power, but the performance of IoT devices is often very limited;
- Network conditions of IoT are often much worse than those of the home or office.

In order to solve the questions blew, the [MQTT protocol](https://www.emqx.com/en/mqtt-guide) provides the simple authentication and the enhanced authentication, which easy to validate devices at the application layer.



## Simple authentication

MQTT CONNECT packet uses the username and password to support the basic network connection authentication, which is a way called simple authentication. This method can also be used to host other forms of authentication, for example delivering the password as Token.

After receiving the CONNECT packet, the broker can verify the legitimacy of the client through the username and password contained for ensuring the safety of the business.

Compared to enhanced authentication, simple authentication has a low computational footprint for both client and server, and can be used for services where security requirements are not so high and computing resources are tight.

However, in the protocol based on the simple authentication model of username and password, the client and broker know that a username corresponds to a password. Without encrypting the channel, either straightly using plaintext to transmit the username and password, or the method of hashing the password, is vulnerable to attack.



## **Enhanced authentication**

For the consideration of stronger security, MQTT v5 adds a new feature **enhanced authentication**. The enhanced authentication includes query/response style authentication, which can implement bi-directional authentication of the client and broker. The [MQTT broker](https://www.emqx.com/en/products/emqx) can verify whether the connected client is a real client, and the client can also verify whether the connected broker is a real broker, thus it provides higher security.

Enhanced authentication relies on the authentication method and authentication data to complete the entire authentication process. In enhanced authentication, the authentication method is normally [SASL ( Simple Authentication and Security Layer )](https://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer) mechanism, which uses a registered name to easy to exchange information. However, the authentication method is not limited to the use of a registered SASL mechanism, and the broker and client may agree to use any query/response style of authentication.

### Authentication methods

The authentication method is a UTF-8 string for specifying an authentication method, and the client and the broker need to support the specified authentication method at the same time. The client initiates enhanced authentication by adding the authentication method field to the CONNECT packet. In the process of enhanced authentication, the packet exchanged between the client and the broker needs to include the authentication method field, and the authentication method must be consistent with the CONNECT packet.

### Authentication data

Authentication data is binary information used to transmit multiple iterations of cryptographic secrets of protocol steps. The content of the authentication data is highly dependent on the specific implementation of the authentication method.

### Enhanced authentication process

Compared to simple authentication which relies on an interaction between the CONNECT packet and the CONNACK packet, enhanced authentication requires multiple exchanges of authentication data between the client and broker. Therefore, MQTT v5 adds the AUTH packet to implement this. The implementation of enhanced authentication is based on three kinds of [MQTT packet](https://www.emqx.com/en/blog/introduction-to-mqtt-control-packets) types:  CONNECT, CONNACK and AUTH. These three kinds of packet need to carry the authentication method and authentication data for bi-directional authentication.

To start the enhanced authentication process, the client needs to send the CONNECT packet containing the authentication method field to the broker. After receiving the CONNECT packet, the broker can continue exchanging authentication data with the client through the AUTH packet and send the CONNACK packet to the client after the authentication is complete.

#### Non-standard example of SCRAM authentication

+ Client to server: CONNECT authentication method = "SCRAM-SHA-1", authentication data = client-first-data
+ Server to client: AUTH reason code = 0x18, authentication method = "SCRAM-SHA-1", authentication data = server-first-data
+ Client to server: AUTH reason code = 0x18, authentication method = "SCRAM-SHA-1", authentication data = client-final-data

+ Server to client: CONNACK reason code = 0, authentication method = "SCRAM-SHA-1", authentication data = server-final-data

#### Non-standard example of Kerberos authentication

+ Client to server: CONNECT authentication method = "GS2-KRB5"
+ Server to client: AUTH reason code = 0x18, authentication method = "GS2-KRB5"
+ Client to server: AUTH reason code = 0x18, authentication method = "GS2-KRB5", authentication data = initial context token
+ Server to client: AUTH reason code = 0x18, authentication method = "GS2-KRB5", authentication data = reply context token
+ Client to server: AUTH reason code = 0x18, authentication method = "GS2-KRB5"
+ Server to client: CONNACK reason code = 0, authentication method = "GS2-KRB5", authentication data = outcome of authentication

In the enhanced authentication process, the client and broker need to exchange authentication data multiple times and each exchange needs to be decrypted and calculated by the authentication algorithm, so it requires more computing resources and a more stable network environment. Therefore, it is not suitable for edge devices with weak computing power and large network fluctuations and MQTT broker that supports enhanced authentication also needs to prepare more computing resources to cope with a large number of connections.



## Re-authentication

After the enhanced authentication is completed, the client can initiate re-authentication at any time by sending an AUTH packet. After the re-authentication starts, the client and the broker exchange authentication data by exchanging the AUTH packet, just like with the enhanced authentication, until the broker sends an AUTH packet with the reason code 0x00 (success) to the client to indicate that the re-authentication was successful. It should be noted that the authentication method for re-authentication must be the same as enhanced Authentication.

During the re-authentication process, other packets of the client and broker can continue using the previous authentication.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT 5.0 service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
