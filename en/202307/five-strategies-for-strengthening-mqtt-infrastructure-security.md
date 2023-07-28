Our [previous articles](https://www.emqx.com/en/blog/category/security) of this series explored various methods to safeguard IoT devices from cyberattacks, including encryption, authentication, and security protocols. However, it is crucial to acknowledge that regular updates and maintenance are equally vital to ensure the ongoing security of IoT devices. Moreover, with the increasing migration of systems and services to the cloud, the security of the underlying operating system assumes even greater significance. This article provides a comprehensive overview of strategies to enhance operating system security from multiple perspectives.

## Regularly Updating the Operating System and Software

Maintaining up-to-date operating systems and software is crucial to uphold system security. Newer versions of operating systems and software often address security issues, fix bugs, and improve overall security performance. Thus, timely updates can significantly reduce the risk of system attacks.

Consider the following steps when updating operating systems and software:

- Verify the trustworthiness of the update source: This step ensures that you download updates only from reliable sources, mitigating the risk of downloading malware from untrusted sources.
- Test the updated system: Prior to deploying the updated system to the production environment, thorough testing in a controlled environment is necessary to validate its stability and security.
- Install security patches: By installing security patches, you can rectify the latest vulnerabilities and bugs, thereby bolstering the system's security.

### Strengthening Security with OpenSSL 

OpenSSL, an extensively utilized open-source software library, facilitates encryption and decryption functionalities for SSL and TLS protocols. Given its widespread adoption, ensuring the security of OpenSSL remains a paramount concern. Over recent years, OpenSSL has encountered severe vulnerabilities and attacks. Consequently, the following measures can be implemented to enhance OpenSSL security.

1. Updating the OpenSSL Version

   Keeping your OpenSSL version up to date is vital for ensuring security. New versions of OpenSSL often include fixes for known vulnerabilities and introduce new security features. Regardless of whether your application or system has experienced attacks, prioritizing the update of your OpenSSL version is crucial. If you currently employ an outdated version, it is highly advisable to promptly upgrade to the most recent available version. The official OpenSSL website provides the latest version for download.

2. Implementing a Robust Password Policy

   To safeguard keys and certificates, OpenSSL supports password usage. To enhance security, it is imperative to utilize strong passwords and update them regularly. Employing a password management tool can prevent using weak or repeated passwords across different systems. In the event of password exposure, it is essential to change the password immediately. Alternatively, password generators can be employed to create random and robust passwords. If different systems are in use, a single sign-on tool can mitigate the risk of password exposure resulting from password reuse across multiple systems.

3. Strengthening Access Control

   Access to OpenSSL should be restricted to authorized users, adhering to the principle of least privilege. Secure channels like VPNs should be employed to safeguard access to OpenSSL. In the event of ongoing attacks on your system, it is crucial to promptly limit access to OpenSSL. Security tools such as firewalls can restrict access, while two-factor authentication tools can enhance access control.

4. Validating Certificates

   When utilizing OpenSSL, it is essential to verify the validity of the certificate. Validating certificates protects against security threats and mitigates the risk of man-in-the-middle attacks. Certificate Revocation Lists (CRL) and Certificate Chains should be used to verify certificate validity. In the case of a revoked certificate, immediate renewal is necessary. Certificate management tools can assist in managing certificates, while obtaining trusted certificates can be achieved through a Certification Authority (CA).

5. Logging and Monitoring

   Logging and monitoring OpenSSL activity is crucial for identifying and addressing security issues. Enabling the logging feature of OpenSSL and regularly reviewing logs for any indications of security concerns is recommended. Employing security monitoring tools allows for real-time monitoring of OpenSSL activity, enabling swift response to security incidents. Open-source security monitoring tools like OSSEC and SNORT can be utilized, and the application of artificial intelligence and machine learning methods can aid in log analysis and data monitoring.

In summary, adopting a multi-faceted approach is essential to strengthen OpenSSL security. Promptly updating OpenSSL, implementing a robust password policy, strengthening access control, validating certificates, and enabling logging and monitoring are key steps to safeguard OpenSSL. For further details on OpenSSL security, refer to the official OpenSSL documentation or consider joining an OpenSSL security training course to enhance your knowledge of security and system protection.

## Disabling Unused Services and Ports

The operating system comes with various services and ports enabled by default, many of which are unnecessary. To enhance system security, disabling unused services and ports is crucial. Command-line tools such as systemd, inetd, and xinetd can be used for this purpose.

Consider the following points when disabling services and ports that are not needed:

- Maintain system functionality: Before disabling services and ports, it is essential to understand their purpose and potential impact to avoid disrupting normal system operations.
- Regularly monitor services and ports: System modifications can introduce new services and ports, necessitating regular checks to ensure system security.

### An Example: Setting up Service Ports for an EMQX Node

1. The Cluster Node Discovery Port

   If the environment variable WITH_EPMD is not set, epmd will not be enabled when starting EMQX, and EMQX ekka is used for node discovery. This is the default node discovery method after 4.0 and it is called ekka mode.

   ekka mode has fixed port mapping relationships for node discovery. The configurations of node.dist_listen_min and node.dist_listen_max do not apply in ekka mode.

   If there is a firewall between cluster nodes, it needs to allow this fixed port. The rule for the fixed port is as follows: ListeningPort = BasePort + Offset.

   - BasePort is always set to 4370 and cannot be changed.
   - Offset is determined by the number at the end of the node name. If the node name does not end with a number, the Offset is 0.

   For example, if the node name in emqx.conf is set to `node.name` = `emqx@192.168.0.12`, the listening port is 4370. For emqx1 (or emqx-1), the port is 4371, and so on.

2. The Cluster RPC Port

   Each node requires an RPC port, which also needs to be allowed by the firewall. Similar to the cluster discovery port in ekka mode, this RPC port is fixed.

   The RPC port follows the same rules as in ekka mode, but with BasePort = 5370. For example, if the node name in emqx.conf is `node.name` = `emqx@192.168.0.12`, the RPC port is 5370. For emqx1 (or emqx-1), the port is 5371, and so on.

3. The MQTT External Service Port

   [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) utilizes two default ports: 1883 for unencrypted transport and 8883 for encrypted transport. It is essential for clients to select the appropriate port when connecting to the [MQTT broker](https://www.emqx.com/en/mqtt/public-mqtt5-broker).

   Additionally, MQTT supports alternative ports such as 8083 and 8084, which are often used for WebSocket connections or SSL proxy connections. These alternative ports provide expanded communication options and additional security features.

## Implementing Access Control

Access control is one of the key measures to ensure system security. It can be implemented through the following methods:

- Require password use: Requiring users to use passwords can protect the system from unauthorized access.
- Restrict login attempts: Restricting login attempts can deter brute force attacks, such as attempting to log in to the system with wrong passwords.
- Employ a firewall: Employing a firewall can filter network traffic and prevent unauthorized access.

When implementing access control methods, the following need to be taken into account:

- Enhance password complexity: Passwords should be sufficiently complex to avoid being guessed or cracked.
- Update passwords regularly: Updating passwords regularly can lower the chance of password exposure.
- Configure firewall rules: Firewall rules need to be configured according to the actual situation, in order to optimize the security and performance.

## Additional Security Configurations

In addition to the above measures, several other security configurations can be implemented to protect the system:

- File system encryption: Encrypting the file system ensures data confidentiality, safeguarding it from exposure even in the event of data theft.
- Utilizing SELinux: SELinux is a security-enhanced Linux kernel module that effectively restricts process permissions, reducing the risk of system vulnerabilities and potential attacks.
- Enabling logging: Enabling logging functionality allows for monitoring of system and application activities, facilitating the detection and response to security incidents.
- Employing security hardening tools: Security hardening tools automate security checks and fixes, enhancing system security. Tools like OpenSCAP and Lynis are valuable resources for vulnerability detection and system hardening.

## Building Security Awareness 

In addition to technical measures, building security awareness is crucial for protecting the system. Security awareness can be fostered through the following methods:

- Employee training: Train employees on security measures, improving their awareness and skills.
- Development of security policies: Develop and enforce security policies to regulate employee behavior and responsibilities.
- Regular drills: Conduct regular drills to simulate security incidents and enhance employee emergency response capabilities.

## Conclusion

Through this article, we have learned some methods and tools to improve system security. Of course, system security is not a one-time job, but requires continuous attention and updates. We also recommend using secure and reliable products like [EMQX](https://www.emqx.com/en/products/emqx) to provide stronger protection for your IoT system. EMQX has powerful security features and excellent reliability, which can improve the overall security of your system.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
