Data security is a high priority for IoT applications. Various companies often use symmetric encryption, asymmetric encryption, digital signature, digital certificate, and other methods to authenticate devices to prevent access to illegal devices. In terms of certificate usage, there are different schemes such as one-type-one-secret and one-machine one-secret. Among them, the one-machine-one-secret scheme pre-sets a unique device certificate for each device end, which enables two-way verification when the device communicates with the server, and only after the verification is passed can the device and the server conduct standard data transmission. Compared with other solutions, One Device One Secret can achieve individual authentication and authorization for each device, which provides higher security.

As a secure and reliable fully-managed MQTT messaging cloud service, EMQX Cloud supports multiple authentication methods, including basic authentication (username/password, client ID/password) and JWT, PSK, and X.509 certificate authentication. It can be configured with the external database as the data source to verify authentication information.

In this article, we will use Redis as the authentication data source storage database, explain how to connect to EMQX Cloud through the Common Name contained in the certificate at the device side as the authentication information, and realize one-computer-one-secret authentication at the client-side. If the client certificate does not have the specified unique Common Name, it will not pass the authentication.

Readers can achieve one-computer-one-secret, bi-directional authentication between device and server and establish secure channel for their IoT devices, effectively preventing attacks such as forged device attacks, device key cracking, forged server commands, listening to or tampering with key information, and stealing keys through device production line security vulnerabilities.

## Operation Procedure

### Configure TLS/SSL two-way authentication

1. Preparation work

   ① Purchase the server certificate and resolve its domain name to the deployment connection address.

   ② Generate client root ca self-signed certificate and ensure that the Common Name is unique when issuing the client certificate with self-signed root ca certificate.

   ```
   # Generate client-ca.crt for CA certificate and adjust the subj according to the actual usage.
   openssl req \
       -new \
       -newkey rsa:2048 \
       -days 365 \
       -nodes \
       -x509 \
       -subj "/C=Common Name/O=EMQ Technologies Co., Ltd/Common Name=EMQ CA" \
       -keyout client-ca.key \
       -out client-ca.crt
       
   # Client secret key generation client.key
   openssl genrsa -out client.key 2048
   
   # generate client-side certificate request file client.csr, Common Name carries authentication information for the client
   openssl req -new -key client.key -out client.csr -subj "/Common Name=346a004d-1dab-4016-bb38-03cca7094415"
   
   # Sign the client certificate with CA certificate and generate client.crt
   openssl x509 -req -days 365 -sha256 -in client.csr -CA client-ca.crt -CAkey client-ca.key -CAcreateserial -out client.crt
   
   # View client-side certificate information
   openssl x509 -noout -text -in client.crt
   
   # Verify the certificate
   openssl verify -CAfile client-ca.crt client.crt
   ```

2. Configuration process

   Login to EMQX Cloud console. Enter the deployment details, and click the +TLS/SSL configuration button to configure the certificate content, you can upload the file or fill in the certificate content directly TLS/SSL authentication type.

   ① One-way authentication: Only the client side verifies the server-side certificate.

   ② Two-way authentication: client and server verify each other's certificates.

   In this example document, we take two-way authentication as an example and fill in the following in the deployment console.

   ① Public key certificate: server-side certificate

   ② Certificate chain: Certificate chain, usually provided by third-party organizations when issuing certificates

   ③ Private key: private secret key

   ④ Client CA certificate: When choosing two-way authentication, you need to provide the client CA certificate

   After completing, click OK until the status is running, that is, the configuration of TLS/SSL two-way authentication is completed.

### Configuring Redis Authentication/Access Control

This article takes Redis authentication/access control as an example, but you can also use other external authentication data sources, in the scenario described in this article, it is recommended to use Redis authentication/access control.

1. Create a VPC peer-to-peer connection
   On the EMQX Cloud deployment details page, create a VPC peer connection to facilitate the Professional Edition deployment intranet access to your Redis authentication database.

2. Configure Redis authentication/access control

   ① Redis configuration
   In your cloud server, create a Redis service. For demonstration purposes, here is a quick build using Docker.

   ```
   docker run -itd --name redis -p 6379:6379 redis:latest
   ```

   This example configures the data in two ways (either one) as follows.

   ```
   HMSET  tls_domain:346a004d-1dab-4016-bb38-03cca7094415 password pubic
   HMSET  tls_subject:346a004d-1dab-4016-bb38-03cca7094415 password pubic
   ```

   ![HMSET](https://assets.emqx.com/images/28f4159998836b815c40c87d99224f7a.png)

   ② Redis authentication/access control configuration
   When authenticating, EMQX Cloud will use the current client information to populate and execute the user-configured authentication query command to query the client's authentication data in Redis.

   You can use the following placeholders in the authentication SQL, which will be automatically populated by EMQX Cloud with the client information when executed: 

   %u: user name

   %c: Client ID

   %C: TLS certificate common name (domain or subdomain of the certificate), valid only for TLS connections

   %d: TLS certificate subject, valid only for TLS connections

You can adapt the authentication query command to your business needs, using any Redis-supported command (opens new window), but in any case, the authentication query command must satisfy the following conditions:

① The first data in the query result must be the password, which EMQX uses to compare with the client password

② If the salt configuration is enabled, the second data in the query result must be the salt field, which is used by EMQX as the salt value

In the deployment, click Authentication & ACL - External Authentication Authorization - Redis Authentication/Access Control and click Configure Authentication to create a new authentication.

The authentication query command is available as follows:

```
HMGET tls_domain:%C password 
HMGET tls_subject:%d password
```

That is, the device needs to carry the client certificate, the client secret key, its Common Name, and the password to authenticate.

## Test Authentication

We use MQTT X to simulate a client with the following information to connect to EMQX Cloud.

① Serverside CA

② Client certificate and client secret key with Common Name 346a004d-1dab-4016-bb38-03cca7094415

③ password：public

![Test Authentication](https://assets.emqx.com/images/552d830dd230b16880c0ea69c1bb1604.png)

Click Connect in the upper right corner, and Connect appears to indicate a successful connection. At this point, the device with the specified common name has been successfully connected to EMQX Cloud, that is, the one-computer-one-secret device has passed the authentication and connected to EMQX Cloud successfully.

![Test Authentication](https://assets.emqx.com/images/1a911d62bbeca518ec1762dca4fe6644.png)

## Conclusion

At this point, we have completed the EMQX Cloud client one-computer-one-certificate verification process and successfully connected to the deployment. Compared with other solutions, One-Device-One-Secret is able to authenticate and authorize each device individually, which has higher security. If you also set up unique access credentials for each IoT device, you can refer to this article for configuration.

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
