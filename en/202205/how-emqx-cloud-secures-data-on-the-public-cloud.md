In the digital era, data has gradually become the core value and key asset of enterprises, and data security is of great importance to every enterprise. In a complex network environment, enterprises are under pressure to prioritize enterprise data security.

As a fully-managed [MQTT 5.0](https://www.emqx.com/en/mqtt/mqtt5) public cloud service, [EMQX Cloud](https://www.emqx.com/en/cloud) provides one-stop operation and management colocation and MQTT messaging services in a unique isolated environment. EMQ attaches great importance to user data security. Special focus is given to data security in the design of EMQX Cloud. Even when deployed on a public cloud, users do not need to worry about data leakage and other risks.

This article presents the data security mechanism of EMQX Cloud in five aspects: infrastructure, data communication, authentication and verification, permission management, and privacy data security.

## Secure and reliable infrastructure

EMQX Cloud Professional Plan uses a highly redundant cluster architecture to ensure high availability of services. Each deployment cluster has its own public IP, a dedicated VPC network, independent EMQX servers and database servers, making it more secure and reliable.

## Communication protocol encryption to support data security

As a security protocol based on modern cryptographic public key algorithms, TLS/SSL secures transmissions over computer communication networks. EMQX Cloud supports TLS/SSL encryption authentication, including single/bidirectional authentication, X.509 certificate, and other security authentications.

The certificate uploaded by the user will not be used for anything other than for product use, and the certificate information can be deleted anytime. Deleting a certificate would disconnect the client from 8883 and 8084. Before deleting the certificate, please ensure that this will not affect your business.

1. Log in to the EMQX Cloud console;
2. To access the deployment details, click on the delete button for the certificate in the TLS/SSL Configuration section.
3. Click on “OK” in the dialog to complete the deletion.

**TLS/SSL handshake protocol**

![TLS/SSL handshake protocol](https://assets.emqx.com/images/5d2fd49456aa00e4ddebe48722ccba9b.png)
 

**SSL/TLS offers the following security advantages:**

- **Strong authentication:** When establishing a connection using TLS, the communicating parties can check each other’s identities. In practice, a very common form of identity checking is to check the X.509 digital certificate held by the other party. This digital certificate is usually issued by a trusted authority, and cannot be forged.
- **Confidentiality:** Each session of a TLS communication is encrypted by a session key, which is negotiated between the communicating parties. No third party has access to the contents of the communication. Even if the key for one session is compromised, it will not affect the security of other sessions.
- **Integrity:** Data in an encrypted communication can hardly be tampered, without being detected.

## Client authentication and verification to prevent illegal connections

Authentication or “verification” is a means of confirming the identity of a user. Authentication is an important part of most applications, and enabling authentication effectively prevents illegal clients from connecting. Authentication in EMQX Cloud means that when a client connects to EMQX Cloud, the server-side configuration controls the client’s permission to connect to the server.

The authentication support in EMQX Cloud consists of two levels:

1. The MQTT protocol itself specifies the username and password in the CONNECT message;
2. At the transmission layer, TLS guarantees the client-to-server authentication using client certificates and ensures that the server verifies the server certificate to the client.

EMQX Cloud also supports HTTP custom authentication, MySQL, and PostgreSQL external database authentication, and will support Redis custom authentication and authorization in the future, helping users to implement more complex authentication and authentication logic, and ACL verification logic. 

## Multi-project and multi-role management for permission management

Permission design is a very important module for enterprise application software. Each enterprise’s different organizational structure will produce different business processes. Therefore, the application software needs to have a sound permission management function, in order to allow different users to view different modules, operate different functions, and view different ranges of data after logging into the system, preventing data leakage and confusion of permissions.

In order to address these concerns, EMQX Cloud was designed with multiple project management deployment and sub-account management permission functions.

For example, you can store the deployment for test environments and production environments under test project and production project, respectively, and give developers and testers read-only/modify permissions for different projects. Hence, developers and testers can only execute operations with permissions when logging into the console. This prevents problems, such as normal business operation disruption affected by maloperation that modifies the deployment data of the production environment.

![Multi-project and multi-role management for permission management](https://assets.emqx.com/images/1ba1bdeffc0b789de1deffb9c0a75595.jpeg)


## Security guarantee for customer privacy data

EMQX Cloud has a strict user privacy data security agreement, and never knowingly collects, accesses, uses, stores, discloses, transfers, or processes any content related to any of the users identified or identifiable person. Before creating a deployment, please review the Privacy Agreement for details.

During the use of EMQX Cloud, the user’s production data is not persistently stored in the cluster. Depending on the functional usage, the user privacy data that may be stored on the EMQX Cloud side may include the following: device connection certificates, device authentication data, ACL data, data integration configurations, etc. After the user stops the service, the deployment is automatically deleted, and the data is cleaned up at the same time, completely eliminating the need for manual deletion and avoiding any potential data leak. 

## Conclusion

EMQX Cloud has formed a complete set of data security solutions in the five aspects discussed above. Regardless of whether it is in the flow of the device data or business data sub-role processing, there are corresponding measures to ensure data security, helping users to build efficient, reliable, and secure IoT platforms and applications.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
