As IoT becomes increasingly common in our lives in areas such as healthcare, smart homes, smart cities, and self-driving vehicles, the security of the devices becomes more important. Not only do we need to protect the data that all these billions of devices are sending, but we also need to be concerned with the safety of individuals who are using these devices. An intruder who hacks into an IoT system can potentially cause serious physical harm to humans.

Therefore, IoT security has become an inevitable topic in IoT development.

## Why is security so important for IoT systems?

We hear in the news about hackers who exploit vulnerabilities in IoT systems such as children's smart toys. The intruder is able to gain access to the toy's camera, speakers, and microphone and is able to spy on the child. In another instance, hackers were able to hack into a pacemaker and manipulate the heart rate and drain the battery, potentially causing serious harm to the patient.  

The reason that these IoT systems were compromised was lack of security. Weak passwords and no encryption made it easier for intruders to compromise these systems. If security measures had been followed, the likelihood of these intrusions occurring would have been reduced. 

It is easy to see how security can be ignored. The system works just fine without security, so why bother with it? Besides, once the system is designed, tested, and working, you want to get the product to market, right? However, ignoring security in your IoT system can be short-sighted and costly. For your clients, it could mean loss of property, data privacy, and, in the worst case, loss of personal safety or even life. For your company, it could mean the cost of product recall, possible legal costs, and loss of brand reputation and trust. These are all consequences that could be avoided or mitigated with a few simple up-front security measures.

## Common security risks in IoT network

Here are some common security risks we may need to keep in mind when building an IoT network.

- Insufficient authentication and authorization mechanisms: IoT devices that have weak or no authentication mechanisms can make them vulnerable to unauthorized access. It is important to not only control the device access, but to also control what a device is allowed to do once it is connected to the network.
- Weak passwords: Some vendors may use the same password for the same device model.  Other vendors may use weak passwords that are easy to guess, such as “admin” or “password”.  As we will show in a later article, the most sophisticated encryption algorithms cannot overcome a password that is easily guessable, such as making the password the same as the username.   Weak passwords make it easy for attackers to gain access to the device and its data. IoT vendors should enforce strong password policies and require users to change default passwords.  
- Insecure communication protocols: Using plaintext communication such as TCP instead of TLS in IoT communications makes it easy for attackers to intercept the data. For example, the Man-In-The-Middle attack where the attacker can eavesdrop on the IoT communications to gather personal data such as passwords, health information and other personal data.
- Lack of user training: IoT vendors may not provide proper security awareness to their users.  This leaves the uneducated user vulnerable to attacks. It is important that IoT vendors provide proper security training to their users.
- Denial of Service (DoS) Attacks: IoT network can be vulnerable to DoS or distributed DoS attacks where a large number of devices are used to exploit software defects or simply flood a network with malicious traffic. To prevent such attacks, IoT networks need to have robust security measures in place, including firewalls, intrusion detection and prevention systems, and access controls. Additionally, IoT networks should be designed to be resilient, with the ability to automatically detect and mitigate attacks without requiring significant administrative effort. 

IoT vendors need to prioritize security at all aspects of their IoT design, from the initial design phase, through to deployment, including post-sales to ensure that their devices are secure and resilient to attacks.

## What can we do in MQTT to secure our IoT systems?

There are several aspects of security that we need to consider when building an IoT system. They can be broken down by the different protocol layers where they reside. Namely, the networking layer, transport layer and the application layer.

**Networking layer**: MQTT runs in IP network, so the networking layer security best practices all apply to MQTT.  Namely, the proper use of firewalls, VPNs, and IPsec to help prevent intruders from accessing the data on the IoT network.

**Transport layer:** At the transport layer, we do not recommend sending plaintext data directly through protocols such as TCP or WebSocket. For example, sensitive data such as user names and passwords used for authentication in the application layer may make the security mechanism of the application layer useless. Because when an intruder steals data directly from the transport layer, he can directly know the username and password we are using.

It’s better to provide end-to-end security for our data with the help of the TLS encryption protocol. In addition to turning data into ciphertext data that is difficult to crack, TLS can also provide multiple protections, such as supporting the client in confirming the legality of the server's identity. When the client is required to use a certificate, the server can also confirm whether the client is legal. This will effectively avoid man-in-the-middle attacks.

**Application layer:** Although it seems that we have provided enough security protection at the transport layer, not all systems support TLS. The MQTT protocol running on the application layer also provides support for password authentication and token authentication through the username and password fields, ensuring that only legitimate devices can access the MQTT broker. MQTT 5.0 also introduces an enhanced authentication mechanism to provide two-way identity confirmation.

On the other hand, the security mechanism at the application layer is usually the last layer of security guarantee. In addition to verifying the identity of the accessor, we'd better check the operations that the accessor can perform, such as which topics the accessor can publish messages to, and from which topics messages can be consumed.

## Summary

All in all, MQTT security is a crucial factor in protecting IoT systems from various attacks and threats. In this article, we have provided a comprehensive overview of MQTT security, covering the importance of MQTT security and some common security challenges that developers and system administrators may encounter. Also, as we mentioned in the article, there’re many measures we can implement with MQTT to enhance the security of your IoT systems devices. By reading the following articles of this series, we believe that you are able to adopt a more comprehensive and proactive approach to MQTT security and ensure the long-term stability and reliability of your systems.

In the coming article, we will introduce the [**password-based authentication**](https://www.emqx.com/en/blog/securing-mqtt-with-username-and-password-authentication) method. Please stay tuned.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
