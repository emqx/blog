In [previous posts](https://www.emqx.com/en/blog/securing-mqtt-with-username-and-password-authentication), we introduced that through the Username and Password fields in the MQTT CONNECT packet, we can implement some simple authentication, such as password authentication and token authentication. In this article, we will delve into a more advanced authentication approach known as Enhanced Authentication.

## What is Enhanced Authentication?

Enhanced authentication is a novel authentication framework introduced in MQTT 5.0. It offers a range of alternative methods that are more secure than traditional password authentication.

However, increased security comes with added complexity. Certain authentication methods, like SCRAM, require multiple exchanges of authentication data. This renders the single-exchange authentication framework of the CONNECT and CONNACK packets outdated. To address this limitation, MQTT 5.0 introduces the AUTH packet, which supports multiple exchanges of authentication data. It enables the use of [SASL](https://en.wikipedia.org/wiki/Simple_Authentication_and_Security_Layer) (Simple Authentication and Security Layer) mechanisms with a challenge-response style in [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt).

## What Problems Does Enhanced Authentication Solve?

Before delving into enhanced authentication, it is essential to understand the shortcomings of password authentication in terms of security.

In fact, despite employing techniques like Salt and Hash to store passwords securely, the client must transmit the password in plain text over the network, making it vulnerable to theft. Even when employing TLS encryption for communication, there remains a risk of attackers obtaining sensitive data like passwords due to outdated SSL versions, weak cipher suites, or the presence of fake CA certificates.

Moreover, simple password authentication only lets the server check the identity of the client, but not the other way around, which allows the attacker to pretend to be the server and get sensitive data from the client. This is what we often call a man-in-the-middle attack.

Enhanced authentication allows users to employ highly secure authentication methods within the SASL framework. These methods offer several advantages, such as eliminating the transmission of passwords over the network and facilitating mutual identity verification between the client and server. By presenting these options, users can select the authentication method that aligns with their specific needs and security preferences.

## Common SASL Mechanisms Used for Enhanced Authentication

### DIGEST-MD5

DIGEST-MD5 is an authentication method within the SASL framework. It utilizes the Message Digest 5 (MD5) hash algorithm and a challenge-response mechanism to verify the identity between the client and the server. One notable advantage is that the client does not need to transmit the password in plain text over the network.

In simple terms, when a client wants to access a protected resource, the server will send a challenge with a one-time random number and some required parameters. The client utilizes these parameters, along with its username and password, to generate a response, which is then transmitted back to the server. The server independently creates an expected response using the same method and compares it with the received response. If they match, authentication is successful. This approach effectively mitigates the risk of password exposure through network snooping. Additionally, by utilizing a one-time random number for each connection, it enhances protection against replay attacks.

However, it's important to note that DIGEST-MD5, while enabling server-side verification of the client's identity, lacks the ability for the client to verify the identity of the server. This limitation leaves room for potential man-in-the-middle attacks. Furthermore, since MD5 is no longer secure, it is strongly recommended to replace it with a hash function that offers stronger resistance to collisions, such as SHA-256.

### SCRAM

SCRAM (Salted Challenge Response Authentication Mechanism) is another authentication method within the SASL framework. It shares similarities with DIGEST-MD5 in terms of approach. SCRAM prompts the client to generate a response using a one-time random number, thereby avoiding sending the password in plain text over the network. However, SCRAM further enhances security by incorporating Salt, Iterations, and more robust hash algorithms like SHA-256 and SHA-512. These additions significantly enhance the security of password storage, effectively mitigating the risks associated with offline attacks, replay attacks, and other potential vulnerabilities.

Furthermore, SCRAM incorporates a more intricate challenge-response process that includes server-side proof sent to the client. The client can then utilize this proof to verify the server's possession of the correct password, enabling mutual authentication. This additional step reduces the vulnerability to man-in-the-middle attacks.

However, using hash algorithms like SHA256 in SCRAM introduces additional computational overhead, which can potentially impact the performance of devices with limited resources.

### Kerberos

Kerberos utilizes a trusted third-party Kerberos server to facilitate authentication services. The server issues tokens to verified users, enabling them to access resource servers. A notable advantage is the ability for users to access multiple systems and services with a single authentication, thereby achieving the convenience of single sign-on (SSO).

The token issued by the Kerberos server has a limited lifespan, and clients can only use this token to access the service for a certain period, which can prevent security issues caused by token leakage. Of course, although a shorter lifespan can enhance security, it sacrifices some convenience. Users need to make their own trade-offs.

At the core of Kerberos lies the utilization of a symmetric encryption algorithm. The server employs locally stored password hashes to encrypt the authentication data, which is then transmitted to the client. The client, in turn, hashes its own password and utilizes it to decrypt the received authentication data. This process offers several advantages, including the elimination of the need to transmit passwords in plain text over the network and enabling mutual verification of the correct password between the server and client. Additionally, through symmetric encryption, the server and client can securely share session keys, which can be utilized for subsequent encrypted communication. Therefore, Kerberos also provides security measures for protecting subsequent communications beyond authentication.

While providing strong security, Kerberos also brings significant complexity. Implementing and configuring Kerberos comes with its own challenges, and its reliance on up to six handshakes can introduce requirements for high network latency and reliability. As a result, Kerberos is typically employed within the internal network environments of enterprises.

## How Does Enhanced Authentication Work in MQTT?

Let's examine how enhanced authentication works in MQTT using the SCRAM as an example. While this article will not delve into the specific principles of SCRAM, it's important to note that SCRAM requires the following four messages to complete authentication:

- client-first-message
- server-first-message
- client-final-message
- server-final-message

![How Does Enhanced Authentication Work in MQTT](https://assets.emqx.com/images/0e5a173ff8a357054f5f57aacec41bc6.png)

To initiate SCRAM authentication, the client sends a CONNECT packet with the Authentication Method attribute set to SCRAM-SHA-256, indicating the intention to use SCRAM authentication. SHA-256 indicates the hash function to be used. The Authentication Data attribute is used to store the content of the client-first message. The Authentication Method attribute determines how the server should parse and process the data contained in the Authentication Data field.

If the server does not support SCRAM authentication, or if the content of the client-first message is found to be invalid, it will return a CONNACK packet containing a Reason Code indicating the reason for authentication failure, and then close the network connection.

Otherwise, the server will proceed with the next step: return an AUTH packet and set Reason Code to 0x18, indicating continued authentication. The Authentication Method in the packet will be the same as the CONNECT packet, and the Authentication Data attribute will contain the content of server-first message.

After verifying that the content of the server-first message is correct, the client also returns an AUTH packet with Reason Code 0x18, and the Authentication Data attribute will contain the content of client-final message.

After verifying that the content of the client-final message is correct, the server has completed the verification of the client's identity. So this time, the server will not return an AUTH packet, but a CONNACK packet with Reason Code 0 to indicate successful authentication, and pass the server-final-message through the Authentication Data attribute in the packet.

If the server's identity is successfully verified, the client can proceed to subscribe to topics or publish messages. However, if the verification fails, the client will send a DISCONNECT packet to terminate the connection.

## Summary

Enhanced authentication provides users with the possibility to introduce more identity verification methods. You can choose authentication methods suitable for your specific needs and further enhance the security of your system. 

[EMQX](https://www.emqx.io/), as a widely-used MQTT broker known for its high scalability and availability, has always prioritized ensuring user security. In addition to [password-based authentication](https://docs.emqx.com/en/emqx/v5.0/access-control/authn/pwoverview.html), EMQX also supports Enhanced Authentication. Users can enable SCRAM authentication with EMQX to improve the security level of their MQTT infrastructure. For more information, please refer to: [MQTT 5.0 Enhanced Authentication](https://docs.emqx.com/en/emqx/v5.0/access-control/authn/scram.html#configure-with-dashboard).



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
