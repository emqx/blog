**Table of Contents**

- [Preparation](#preparation)
- [Enabling SSL/TLS one-way authentication on EMQX Enterprise](#enabling-ssltls-one-way-authentication-on-emqx-enterprise)
- [Configure EMQX Enterprise to Enable SSL/TLS connection](#configure-emqx-enterprise-to-enable-ssltls-connection)
- [Implement GCP IoT Core Authentication on EMQX Enterprise](#implement-gcp-iot-core-authentication-on-emqx-enterprise)
- [Migrate connections to EMQX Enterprise](#migrate-connections-to-emqx-enterprise)
- [Summary](#summary)
- [Appendix - Authentication Service Sample Code](#appendix---authentication-service-sample-code)

Our [previous blog](https://www.emqx.com/en/blog/how-to-deploy-emqx-enterprise-on-google-cloud) discussed setting up an EMQX Enterprise deployment on GCP and conducting message publish/subscribe tests. This blog will demonstrate how to connect your devices on GCP IoT Core to the EMQX Enterprise we’ve deployed already.

## Preparation

IoT Core and EMQX Enterprise apply different connection and authentication methods. These differences are summarized in the table below to help you understand them better:

| **Item**              | **IoT Core**                                                 | **EMQX Enterprise**                                          | **Migration**                                                |
| :-------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| MQTT Connection        | SSL/TLS authentication requires using a root certificate provided by GCP. [View Document](https://cloud.google.com/iot/docs/how-tos/mqtt-bridge) | Support SSL/TLS connections. [View Document](https://www.emqx.com/en/blog/emqx-server-ssl-tls-secure-connection-configuration-guide) | 1. Replace the root certificate on the device by purchasing or issuing a new certificate.<br>2. Update the device access address to connect to EMQX Enterprise. |
| Authentication Method | JWT authentication. [View Document](https://cloud.google.com/iot/docs/how-tos/credentials/jwts) | Password authentication, JWT authentication, and enhanced authentication. [View Document](https://docs.emqx.com/en/enterprise/v4.4/advanced/auth.html) | 1. Migrate IoT Core authentication data.<br>2. Implement authentication on EMQX. |

Next, we will proceed with the required migrations one by one.

## Enable SSL/TLS one-way authentication on EMQX Enterprise

To ensure secure and reliable message transmission, MQTT devices connect to IoT Core via the address `mqtt.googleapis.com:8883`, which utilizes TLS encryption by default. Devices connecting to IoT Core must authenticate the server certificate of the IoT Core (one-way authentication).

To migrate to EMQX Enterprise, a new server certificate must be used. EMQX Enterprise offers two options: self-signed certificates or third-party CA-signed certificates. For self-signed certificates, the certificate issuance and configuration steps are as follows.

### Self-signed Server Certificate

You can establish an SSH connection to the VM instance to issue a certificate.

1. Generate a private key and a self-signed root certificate (CA) using the OpenSSL tool, with a validity of 10 years.

   ```
   openssl genrsa -out ca.key 2048
   openssl req -x509 -new -nodes \
     -key ca.key \
     -subj "/C=US/ST=California/L=Silicon Valley/O=EMQ/CN=EMQ CA" \
     -sha256 \
     -days 3650 \
     -out ca.crt
   ```

   Modify the values of the parameters in the above command according to your actual situation. 

   - `-subj`: Specifies the certificate subject
   - `C `: Represents the country
   - `ST`: Represents the state/province
   - `L`: Represents the city
   - `O`: Represents the organization
   - `CN`: Represents the Common Name
   - `-days`: Specifies the certificate's validity period, currently 10 years

2. Create a server certificate request to generate a new key and a certificate signing request file (CSR).

   ```
   openssl genrsa -out server.key 2048
   openssl req -new -key server.key \
     -subj "/C=US/ST=California/L=Silicon Valley/O=EMQ/CN=35.xxx.xxx.xxx" \
     -out server.csr
   ```

   In the above command, the Common Name in the -subj parameter is the server's domain name or IP address that requires the certificate. The client verifies it during the connection to ensure it matches the connecting address. You can set it to the public IP address of your VM instance.

3. Use the private key of the CA and the CSR file to issue the server certificate.

   ```
   openssl x509 -req -in server.csr \
     -CA ca.crt -CAkey ca.key \
     -CAcreateserial \
     -out server.crt \
     -days 3650 \
     -sha256
   ```

Now we have the following 4 files:

| Filename   | Purpose            | Description                                                  |
| :--------- | :----------------- | :----------------------------------------------------------- |
| ca.key     | CA private key     | Used to sign server and client certificates. **In production environments, it is recommended to use certificates signed by trusted third-party CAs to enhance security.** |
| ca.crt     | CA certificate     | Used to verify the validity of server and client certificates. Clients are required to carry it during connection to verify the validity of the server certificate. |
| server.key | Server private key | Used to establish SSL/TLS secure connections. It contains private key information used to encrypt and decrypt communication data. **It is crucial to properly secure this file.** |
| server.crt | Server certificate | Contains the server's public key used to verify the server's identity. |

## Configure EMQX Enterprise to Enable SSL/TLS connection

1. Copy the certificate created above to the **certs** directory of EMQX Enterprise.

   ```
   cp ca.crt server.key server.crt /etc/emqx/certs/
   ```

2. Go to the listener configuration file `/etc/emqx/listeners.conf` and modify the following configuration items.

   ```
   listener.ssl.external = 8883
   listener.ssl.external.keyfile = /etc/emqx/certs/server.key
   listener.ssl.external.certfile = /etc/emqx/certs/server.crt
   listener.ssl.external.cacertfile = /etc/emqx/certs/ca.crt
   ```

3. Run `emqx restart` command to apply the configuration.

   ```
   $ emqx restart
   EMQX Enterprise 4.4.16 is stopped: ok
   EMQX Enterprise 4.4.16 is started successfully!
   ```

## Implement GCP IoT Core Authentication on EMQX Enterprise

### IoT Core Authentication Process

The authentication process for establishing a connection with IoT Core involves creating a JWT and including it in the password field of the CONNECT request. Here are the steps for creating a JWT and establishing the connection.

1). Create a [key pair](https://cloud.google.com/iot/docs/how-tos/credentials/keys) for the client. One client on IoT Core can have up to 3 key pairs, each containing the following files:

| Filename        | Purpose          | Description                                                  |
| :-------------- | :--------------- | :----------------------------------------------------------- |
| rsa_private.pem | Private key file | It is used to encrypt and decrypt the data and needs to be kept safe. |
| rsa_cert.pem    | Certificate file | It contains the public key and other certificate information and can be used to authenticate SSL/TLS connections. |

2). Create a [JWT](https://jwt.io/) with the following information and sign it using the client's associated key pair. The JWT is a JSON-based standard used for identity verification and authorization.

   ```
   {
     "aud": "my-project",
     "iat": 1509654401,
     "exp": 1612893233
   }
   ```

   JWT client libraries for generating JWTs can be found [here](https://jwt.io/). Below is an example of Node.js code for creating a JWT.

   ```
   const createJwt = (projectId, privateKeyFile, algorithm) => {
     // Create a JWT to authenticate this device. The device will be disconnected
     // after the token expires, and will have to reconnect with a new token. The
     // audience field should always be set to the GCP project id.
     const token = {
       iat: parseInt(Date.now() / 1000),
       exp: parseInt(Date.now() / 1000) + 20 * 60, // 20 minutes
       aud: projectId,
     };
     const privateKey = readFileSync(privateKeyFile);
     return jwt.sign(token, privateKey, {algorithm: algorithm});
   };
   ```

3). Construct MQTT connection parameters, including the following information:

   - **Client ID**：It includes IoT Core basic information and should be in the following format.
     - `projects/${projectId}/locations/${region}/registries/${registryId}/devices/${deviceId}`
   - **Password**：It is the JWT generated in step 2.
   - **Connection Address**：It is `mqtt.googleapis.com:8883` by default, but it needs to be replaced with the actual address of EMQX Enterprise during migration.
   - **CA Certificate**：It should be replaced with the certificate used by EMQX Enterprise during migration as opposed to the Root CA used for Google IoT Core.

4). Upon establishing a connection using the parameters outlined in step 3, IoT Core will verify the identity by comparing the JWT information in the password field.

### Configure Authentication on EMQX Enterprise

EMQX Enterprise supports JWT authentication but doesn't allow setting up individual key pairs for each client. To meet this requirement, a more flexible approach is necessary. This is where [HTTP authentication](https://docs.emqx.com/en/enterprise/v4.4/modules/http_authentication.html) comes in, which delegates certificate management and JWT verification to an external authentication service.

This manual includes an example code for an HTTP authentication service that follows this approach, which can be found in the appendix at the end of the manual. To configure HTTP authentication, follow the steps below.

1. Install the dependencies and start the authentication service using the code provided in the appendix.

   ```
   $ npm install jsonwebtoken
   $ node auth-service.js
   Server started on port 3000
   ```

2. Open the Dashboard, go to the **Modules** page, click **Add Module**, then select **HTTP AUTH/ACL**.

   ![Add Module](https://assets.emqx.com/images/c43796af65c3ca0248fa24a787885bdd.png)

   ![HTTP AUTH/ACL](https://assets.emqx.com/images/284d045103c9e651d5ba0d96866566b5.png) 

3. Input the authentication parameters in the given fields. Once a client initiates a connection, EMQX will trigger a request to the authentication service containing the client information as in the configuration settings.

   - **AUTH Request URL**: the URL of the authentication request. In this case, we will use `http://localhost:3000/mqtt/auth`.

   - **HTTP Request ContentType**: select **application/json** to send the client information in JSON format.

   - Remove the ACL-related configuration, leave the remaining settings as default, and click **Add** to complete the configuration.

   ![Complete the configuration](https://assets.emqx.com/images/1603226e2a88495b5d17bf0cb42dbe90.png)

## Migrate connections to EMQX Enterprise

To verify that the migration works as expected, we will utilize a [Node.js sample](https://github.com/googleapis/nodejs-iot.git) provided by IoT Core, which will serve as a mock client.

Suppose you have completed the initial steps outlined in the Quickstart guide to establish a connection between the mock client and IoT Core. In that case, the next step is to modify the connection address and utilize a self-signed root certificate for the connection.

1. Get the sample code from GitHub and go to the` iot/mqtt_example` directory. Install the necessary dependencies.

   ```
   git clone https://github.com/googleapis/nodejs-iot.git
   cd nodejs-iot/samples/mqtt_example
   npm install
   ```

2. Copy the **client private key** (`rsa_private.pem`) to the current directory (`samples/mqtt_example`).

   ```
   # Replace with the actual file path
   cp /opt/certs/rsa_private.pem .
   ```

3. Copy your self-signed CA certificate (ca.crt) to the current directory (`samples/mqtt_example`).

   ```
   cp /opt/certs/ca.crt .
   ```

4. Run the following command (replace the placeholders with your own information ID). 

   - `--privateKeyFile` : Specifies the client private key
   - `--serverCertFile` : Specifies the self-signed CA certificate
   - `--mqttBridgeHostname` : Specifies the public address of the EMQX Enterprise

   ```
   node cloudiot_mqtt_example_nodejs.js \
       mqttDeviceDemo \
       --projectId=PROJECT_ID \
       --cloudRegion=REGION \
       --registryId=REGISTRY_ID \
       --deviceId=DEVICE_ID \
       --privateKeyFile=rsa_private.pem \
       --serverCertFile=ca.crt \
       --numMessages=25 \
       --algorithm=RS256 \
       --mqttBridgeHostname=35.xxx.xxx.xxx
   ```

   The following will be displayed upon a successful connection.

   ```
   Google Cloud IoT Core MQTT example.
   connect
   Publishing message: reg/dev-payload-1
   Config message received:
   Publishing message: reg/dev-payload-2
   Publishing message: reg/dev-payload-3
   Publishing message: reg/dev-payload-4
   Publishing message: reg/dev-payload-5
   Publishing message: reg/dev-payload-6
   Publishing message: reg/dev-payload-7
   Publishing message: reg/dev-payload-8
   Publishing message: reg/dev-payload-9
   Publishing message: reg/dev-payload-10
   Publishing message: reg/dev-payload-11
   ```

## Summary

Congratulations, you have successfully migrated your IoT Core client connections to EMQX Enterprise! We're almost there with just one more step to complete the migration process. In the next blog post in this series, we'll introduce how to ingest your IoT data into GCP Pub/Sub via EMQX Enterprise's Data Bridge.

## Appendix - Authentication Service Sample Code

```
const fs = require('fs');
const http = require('http');
const jwt = require('jsonwebtoken');

// Storing client public keys through a database
const certs = {
  // ${projectId}:${registryId}:${deviceId}
  'PROJECT_ID:my-registry:my-device': fs.readFileSync('./rsa_cert.pem').toString(),
};

// Create an HTTP server and listen on port 3000.
const server = http.createServer((req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(401);
    res.end('Not POST Request')
    return
  }
  let body = '';
  req.on('data', chunk => {
    body += chunk.toString();
  });
  req.on('end', () => {
    try {
      //Parsing JSON formatted requests
      const data = JSON.parse(body);
      console.log(data);
      const { clientid, password } = data;

      // projects/${projectId}/locations/${region}/registries/${registryId}/devices/${deviceId}
      // Retrieve the deviceName from the clientId, and use it to search for the corresponding private key
      const info = clientid.split('/')
      const projectId = info[1]
      const registryId = info[5]
      const deviceId = info[7]
      const certId = `${projectId}:${registryId}:${deviceId}`
      const clientCert = certs[certId];
      if (!clientCert) {
        res.writeHead(401);
        res.end('Auth Error')
        return
      }
      // Verify the JWT using the private key
      jwt.verify(password, clientCert);

      // JWT verification successful, returning a 200 status code
      res.writeHead(200);
      res.end('Auth Success');
    } catch (err) {
      console.log(err)
      // error，returning 401 status code
      res.writeHead(401);
      res.end('Auth Error');
    }
  });

});

server.listen(3000, () => {
  console.log('Server started on port 3000');
});
```

## Other Articles in This Series

- [3-Step Guide for IoT Core Migration 01 | How to Deploy EMQX Enterprise on Google Cloud](https://www.emqx.com/en/blog/how-to-deploy-emqx-enterprise-on-google-cloud)
- [3-Step Guide for IoT Core Migration 03 | Ingesting IoT Data From EMQX Enterprise to GCP Pub/Sub](https://www.emqx.com/en/blog/ingesting-iot-data-from-emqx-enterprise-to-gcp-pub-sub)
 

<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
