In this post, we will introduce [MQTT broker](https://www.emqx.com/en/products/emqx) security concepts and challenges, as well as how EMQX handles security at a relatively high level. We assume that you are already familiar with the basics of the MQTT protocol.

![MQTT Security](https://static.emqx.net/images/ae70590c49a9f31653af992bbef87578.png)
 

In general, information security is a set of practices designed to keep data secure from unauthorised access or alterations. When discussing information security in general, it quite often involves both when data being stored and being transmitted from one machine or place to another. MQTT is an information exchange protocol, so in this post, we will focus on the security for information transmission.

The basic components of information security are most often summed up as: *confidentiality, integrity,* and *availability.*

- **Confidentiality** means data is only accessible by authorised users. For example, only a logged in user is allowed to connect to (and then publish or subscribe) data in an MQTT broker. Passwords, encryption, authentication and authorisation are the common techniques designed to ensure confidentiality.

- **Integrity** is to protect data against being modified either by accident or maliciously. The techniques that ensure confidentiality will also protect data integrity since an attacker cannot modify data without accessing it first. Addition techniques, like checksum and fingerprinting can help you verify data integrity. For example, SSL certificate verification can protect attackers from intercepting and modify MQTT packages on wire. 

- **Availability** means while protecting data from attackers accessing or modifying the data, we also need to ensure that it *can* be accessed by legit users with proper permissions. As an MQTT broker, ensuring availability also means having enough network and computing resources to serve expected data volume. For example, an attacker should not be able to easily consume 100% CPU resources by sending a malformed request.

With regards to confidentiality and integrity, since MQTT is a protocol working on top of TCP/IP, data being transmitted over MQTT can be secured at each layer of the networking model. Here is a brief introduction from the bottom up.

- **Network layer**

  It’s a common practice to setup firewall rules (such as AWS security groups) to allow/deny certain IP ranges from accessing the MQTT network. Other techniques like IPsec or VPN are also applicable to ensure only trustworthy clients can reach the network. 

- **Transport Layer**
  
  TLS (Transport Layer Security), or in some context, the new-deprecated name SSL, aims primarily to provide privacy and data integrity between two or more communicating computer applications. Running on top of TLS, MQTT can take full advantage of its security features to secure data integrity and client trustworthy. We’ll get into more details about TLS in EMQX in the coming posts.

- **Application Layer**
  
  Client ID, username and password presented in MQTT protocol allows us to implement application level authentication and authorisation. We’ll learn more about EMQX’s authentication (authn) and authorization (authz) in detail in the coming posts.

- **User Data Layer**
  
  Although not commonly adopted, but there is nothing stopping users to encrypt MQTT payload itself when there is a lack of lower level security, or when it’s necessary to provide an extra layer of security integrating with other less secured network components. This is not in the scope of our discussion in detail though.

When it comes to Availability, we will share a few case studies on how to protect the system from malicious clients in future posts.
