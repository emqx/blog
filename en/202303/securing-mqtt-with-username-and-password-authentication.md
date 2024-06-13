Authentication is the process of identifying a user and verifying that they have access to a system or server. It is a security measure that protects the system from unauthorized access and guarantees that only valid users are using the system.

Given the expansive nature of the IoT industry, it is crucial to verify the identity of those seeking access to its infrastructure. Unauthorized entry poses significant security threats and must be prevented. And that's why IoT developers should possess a comprehensive understanding of the various authentication methods.

In this article, we explain how authentication works in MQTT, what security risks it solves, and introduce the first authentication method: password-based authentication.

## What is authentication in MQTT?

Authentication in MQTT refers to the process of verifying the identity of a client or a broker before allowing them to establish a connection or interact with the MQTT network. It is only about the right to connect to the broker and is separate from *authorization*, which determines which topics a client is allowed to publish and subscribe to. Authorization will be discussed in a separate article in this series.  

The MQTT Broker can authenticate clients mainly in following ways:

- **Password-based authentication**: The broker verifies that the client has the correct connecting credentials: username, client ID, and password. The broker can verify either the username or client ID against the password. 
- **Enhanced authentication (SCRAM)**: This authenticates the clients using a back-and-forth challenge based mechanism known as **S**alted **C**hallenge **R**esponse **A**uthentication **M**echanism.
- Other methods include Token Based Authentication like JWT, and also HTTP hooks, and more.

In this article, we will focus on the password-based authentication. 

## Password-based authentication

Password-based authentication aims to determine if the connecting party is legitimate by verifying that he has the correct password credentials.

In MQTT, password-based authentication generally refers to using a username and password to authenticate clients, which is also recommended. However, in some scenarios, some clients may not carry a username, so the client ID can also be used as a unique identifier to represent the identity.

When an [MQTT client](https://www.emqx.com/en/blog/mqtt-client-tools) connects to the broker, it sends its **username** and **password** in the  CONNECT packet. The example below shows a Wireshark capture of the CONNECT packet for a client with the corresponding values of **client1**, **user**, **MySecretPassword**.  

![image.png](https://assets.emqx.com/images/001d8254b188ba71a364a3d1ac3fbb3f.png)

After the broker gets the username (or client ID) and password from the CONNECT packet, it needs to look up the previously stored credentials in the corresponding database according to the username, and then compare it with the password provided by the client. If the username is not found in the database, or the password does not match the credentials in the database, the broker will reject the client's connection request.

This diagram shows a broker using PostgreSQL to authenticate the client's username and password.

![Using PostgreSQL to authenticate the client's username and password](https://assets.emqx.com/images/22c364a6a7da02f0ea00a065941200e5.png)

The password-based authentication solves one security risk. Clients that do not hold the correct credentials (Username and Password) will not be able to connect to the broker. However, as you can see in the Wireshark capture, a hacker who has access to the communication channel can easily sniff the packets and see the connect credentials because everything is in plaintext. We will see in a later article in this series how we can solve this problem using TLS (Transport Layer Security).

## Secure your passwords with Salt and Hash

Storing passwords in plaintext is not considered secure practice because it leaves passwords vulnerable to attacks. If an attacker gains access to a password database or file, they can easily read and use the passwords to gain unauthorized access to the system. To prevent this from happening, passwords should instead be stored in a hashed and salted format.

What is a hash? It is a function that takes some input data, applies a mathematical algorithm to the data, and then generates an output which looks like complete nonsense. The idea is to obfuscate the original input data and also the function should be one-way. That means that there is no way to calculate the input given the output. However, hashes by themselves are not secure and can be vulnerable to dictionary attacks as shown in the following example.

Consider this sha256 hash:  8f0e2f76e22b43e2855189877e7dc1e1e7d98c226c95db247cd1d547928334a9

It looks secure; you cannot tell what the password is by looking at it. However, the problem is that for a given password, the hash always produces the same result. So, it is easy to create a database of common passwords and their hash values. Here is an example:

| **sha256 hash**                                              | **plaintext password** |
| :----------------------------------------------------------- | :--------------------- |
| dc1e7c03e162397b355b6f1c895dfdf3790d98c10b920c55e91272b8eecada2a | MyPassword             |
| 8f0e2f76e22b43e2855189877e7dc1e1e7d98c226c95db247cd1d547928334a9 | passw0rd               |
| 27cc6994fc1c01ce6659c6bddca9b69c4c6a9418065e612c69d110b3f7b11f8a | hello123               |

A hacker could lookup this hash in an online hash database and learn that the password is **passw0rd**.

"Salting" a password solves this problem. A salt is a random string of characters that is added to the password before hashing. This makes each password hash unique, even if the passwords themselves are the same. The salt value is stored alongside the hashed password in the database. When a user logs in, the salt is added to their password, and the resulting hash is compared to the hash stored in the database. If the hashes match, the user is granted access.

Suppose that we add a random string of text to the password before we perform the hash function. The random string is called the salt value.

For example with a salt value of **az34ty1**, sha256(passw0rd**az34ty1**) is

6be5b74fa9a7bd0c496867919f3bb93406e21b0f7e1dab64c038769ef578419d

This is unlikely to be in a hash database since this would require a large number of database hash entries just for the single plaintext **passw0rd** value. 

## Best Practices for Password-based Authentication in MQTT

Here are some key takeaways from what we’ve mentioned in this blog, which can be the best practices for password-based authentication in MQTT:

- One of the most important aspects of password-based authentication in MQTT is choosing strong and unique passwords. Passwords that are easily guessable or reused across multiple accounts can compromise the security of the entire MQTT network. 
- It is also crucial to securely store and transmit passwords to prevent them from falling into the wrong hands. For instance, passwords should be hashed and salted before storage, and transmitted over secure channels like TLS. 
- In addition, it's a good practice to limit password exposure by avoiding hard-coding passwords in code or configuration files, and instead using environment variables or other secure storage mechanisms. 

## Summary

In conclusion, password-based authentication plays a critical role in securing [MQTT connections](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection) and protecting the integrity of IoT systems. By following best practices for password selection, storage, and transmission, and being aware of common issues like brute-force attacks, IoT developers can help ensure the security of their MQTT networks. As a widely-used MQTT broker with high scalability and availability, [EMQX](https://github.com/emqx/emqx) also offers a range of security measures, including [password-based authentication](https://docs.emqx.com/en/emqx/v5.0/access-control/authn/authn.html), to guarantee the security of users' IoT systems.

However, it's important to note that password-based authentication is just one of many authentication methods available in MQTT, and may not always be the best fit for every use case. For instance, more advanced methods like digital certificates or OAuth 2.0 may provide stronger security in certain scenarios. Therefore, it's important for IoT developers to stay up-to-date with the latest authentication methods and choose the one that best meets the needs of their particular application.

In the following article of this series, we will introduce another authentication method: SCRAM. Stay tuned for it!


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
