As a security protocol based on modern cryptographic public key algorithms, TLS/SSL can ensure the security of transmission in the computer communication network. EMQX has built-in support for TLS/SSL including one-way/two-ways authentication, the X.509 certificate, load balance SSL and many other security certifications. You can enable SSL/TLS for all protocols supported by EMQX, and can also configure HTTP API provided by EMQX to use TLS.

In the previous article, we've introduced how to [enable SSL/TLS one-way security connection for the EMQX](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide). This article will introduce how to enable SSL/TLS two-way security connection for [MQTT](https://www.emqx.com/en/mqtt-guide) in EMQX.



## The security advantages brought by SSL/TLS

- **Strong certification**. When using TLS to establish connections, both communicating parties can check each other's identity. One of the common methods to check identity is that check another party's digital certificate X.509. This kind of digital certificate normally issued by a trusted institution, can not be forged.
- **Ensure confidentiality**. Every session of TLS communicating will be encrypted by the session key which is negotiated by both parties. Any third party will not know the communication content. Although one of the session keys is leaked, it does not affect the security of other sessions.
- **Completeness.** It is difficult that tamper with the data in encrypted communication and without being discovered.



## SSL/TLS protocol

The process of communication in the TLS/SSL protocol consists of two parts. The first part is the handshake protocol. The purpose of this handshake protocol is to identify the identity of another party and establish a safe communication channel. After a handshake, both parties will negotiate the next password suite and session key. The second part is the record protocol. Record is highly similar to other data transmission protocols. It carries content type, version, length, load, etc, and the difference is that the information carried by this protocol is encrypted.

The following picture describes the process of the TLS/SSL handshake protocol. From "hello" of the client until "finished" of the broker. If you are interested in this, you can view more detailed material. Even if you do not know this process, you can also enable this function in [EMQX](https://www.emqx.com/en/products/emqx).

![what-is-ssl](https://assets.emqx.com/images/29b8bd83af006c104add0635a11682bb.gif)



## Why do we need SSL/TLS two-way certification

The two-way certification is that a certificate is required for service and client during the connection authentication. Both parties need to perform authentication for ensuring that both sides involved in communication are trusted. Both parties share their public certificates, and then perform verification and confirmation based on the certificate. For some application scenarios that required high security, we need to enable two-way SSL/TLS authentication.



## Preparate of the SSL/TLS certificate

In the two-way certification, we generally use the way self-signed to generate the certificate of the server and client, so this article will take the self-signed certificate as an example.

Generally speaking, we need a digital certificate to ensure the strong certification of TLS communication. The use of digital certificates is a three-party protocol. In addition to the communicating parties, there is a trusted third party to issue the certificate. Sometimes, this trusted third party is a CA. Communicating with CA is usually done by issuing certificates in advance. So, we need a CA’s certificate and an EMQX’s certificate these two certificates at least, and the EMQX’s certificate is issued by CA and uses the CA’s certificate for verification.

We assume that your system has installed OpenSSL. Using the toolkit included with OpenSSL can generate the certificate we needed.

### Generate the self-signed CA certificate

First, we need a self-signed CA certificate. If you want to generate this certificate, you need a private key to sign it. You can execute the following command to generate this private key:

```shell
openssl genrsa -out ca.key 2048
```

This command will generate a key with a length of 2048 and will be stored in `ca.key`. If you have this key, you can use it to generate the root certificate of EMQX:

```shell
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 -out ca.pem
```

The root certificate is the starting point of an entire chain of trust. If the issuer of each level of a certificate and the issuer of the root certificate is trusted, this certificate is trusted. We can use it to issue the certificate for EMQX.

### Generate server certificate

EMQX also needs its private key to ensure control for its certificates. The process of generating this private key is similar to the above:

```shell
openssl genrsa -out emqx.key 2048
```

Create file `openssl.cnf`

- req_distinguished_name ：according to the situation to modify
- alt_names： modify `BROKER_ADDRESS` to the real IP or DNS address of EMQX broker such as IP.1 = 127.0.0.1 or DNS.1 = broker.xxx.com

```conf
[req]
default_bits  = 2048
distinguished_name = req_distinguished_name
req_extensions = req_ext
x509_extensions = v3_req
prompt = no
[req_distinguished_name]
countryName = CN
stateOrProvinceName = Zhejiang
localityName = Hangzhou
organizationName = EMQX
commonName = CA
[req_ext]
subjectAltName = @alt_names
[v3_req]
subjectAltName = @alt_names
[alt_names]
IP.1 = BROKER_ADDRESS
DNS.1 = BROKER_ADDRESS
```

Then, use this key and configuration to issue a certificate request:

```shell
openssl req -new -key ./emqx.key -config openssl.cnf -out emqx.csr
```

Then use the root certificate to issue the certificate of EMQX:

```shell
openssl x509 -req -in ./emqx.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out emqx.pem -days 3650 -sha256 -extensions v3_req -extfile openssl.cnf
```

### Generate client certificate

Two-way connection authentication also needs to create the certificate of client. First, we need to create client key:

```shell
openssl genrsa -out client.key 2048
```

Using the generated client key to create a client request file:

```shell
openssl req -new -key client.key -out client.csr -subj "/C=CN/ST=Zhejiang/L=Hangzhou/O=EMQX/CN=client"
```

Finally, we use the previously generated CA certificate to sign the client and generate a client certificate:

```shell
openssl x509 -req -days 3650 -in client.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out client.pem
```

After preparing the server and client certificate, we can enable TLS/SSL two-way authentication in the EMQX.



## Enable and verify SSL/TLS two-way connection

**In the EMQX, the default listening port of `mqtt:ssl` is 8883.**

### EMQX configuration

Copy the file `emqx.pem`, `emqx.key` and `ca.pem` generated by OpenSSL tool into the directory `etc/certs/` of EMQX, and refer the following configuration to modify `emqx.conf`:

```shell
## listener.ssl.$name is the IP address and port that the MQTT/SSL
## Value: IP:Port | Port
listener.ssl.external = 8883

## Path to the file containing the user's private PEM-encoded key.
## Value: File
listener.ssl.external.keyfile = etc/certs/emqx.key

## NOTE: If emqx.pem is a certificate chain, please make sure the first certificate is the certificate for the server, but not a CA certificate.
## Path to a file containing the user certificate.
## Value: File
listener.ssl.external.certfile = etc/certs/emqx.pem

## Note: ca.pem is to hold the server's intermediate and root CA certificates. Other trusted CAs can be appended for client certificate validation.
## Path to the file containing PEM-encoded CA certificates. The CA certificates
## Value: File
listener.ssl.external.cacertfile = etc/certs/ca.pem

## A server only does x509-path validation in mode verify_peer,
## as it then sends a certificate request to the client (this
## message is not sent if the verify option is verify_none).
##
## Value: verify_peer | verify_none
listener.ssl.external.verify = verify_peer

## Used together with {verify, verify_peer} by an SSL server. If set to true,
## the server fails if the client does not have a certificate to send, that is,
## sends an empty certificate.
##
## Value: true | false
listener.ssl.external.fail_if_no_peer_cert = true
```

### MQTT connection test

After finished configuring and restarted EMQX, we use [MQTT client tool - MQTTX](https://mqttx.app/) (this tool is cross-platform and supports [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5)) to verify that whether TLS service is normally running.

> The requirement of MQTTX version: v1.3.2 or higher version

- Refer to the following picture to create `MQTT client` in the MQTTX (`127.0.0.1` in the Host input box need to be replaced by the real IP of EMQX broker)

![mqttxconfig.png](https://assets.emqx.com/images/fc0bf47beab8f1b6b9e7d992c260e188.png)

At this time, you need to select `Self signed` in the column `Certificate` and carry the file `ca.pem` generated in the self-signed certificate and the client certificate `client.pem` and the client key `client.key` file.

- Click the button `Connect`, after the connection succeeds, if you can normally perform MQTT publish/subscribe operation, the configuration of SSL two-way connection authentication succeeds.

![mqttxconnected.png](https://assets.emqx.com/images/d453f16b1beb945af6d8dc99840e364d.png)



### EMQX Dashboard verification

Finally, open the Dashboard of EMQX. On the Listeners page, you can see that there is an `mqtt:ssl` connection on port 8883.

So far, we successfully finished the SSL/TLS configuration of the EMQX Broker and the test of a two-way authentication connection.

![emqxdashboard.png](https://assets.emqx.com/images/ca678e3f6fb0b23b46818a022f71de1f.png)

<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed, cloud-native MQTT service</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
