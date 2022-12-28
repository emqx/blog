In [the previous article](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-01), we succeeded in creating deployment and connecting devices on EMQX Cloud. To secure the connection, we need to set up TLS/SSL to enable the 8883 port.

In GCP IoT Core, the connection uses a TLS/SSL one-way authentication handshake. This TLS handshake is initiated via mqtt.googleapis.com or the long-term support domain mqtt.2030.ltsapis.goog on port 8883 or 443.

[EMQX Cloud](https://www.emqx.com/en/cloud), as an MQTT messaging cloud service for the IoT, supports connection via TLS/SSL ports with customer defined TLS/SSL, ensuring data security and privacy at the transport layer.

This article will describe how to connect GCP IoT Core devices to EMQX Cloud via TLS/SSL ports. 


## TLS/SSL Configuration

EMQX Cloud Professional Deployment provides custom one-way/two-way TLS/SSL configurations, as follows:

| **Certification Mode** | **Support self-signed certificate** | **Server certificate** | **Certificate chain** | **Private key** | **Client CA certificate** |
| ---------------------- | ----------------------------------- | ---------------------- | --------------------- | --------------- | ------------------------- |
| one-way Authentication | Yes                                 | required               | required              | required        | not required              |
| two-way Authentication | Yes                                 | required               | required              | required        | required                  |

 

1. Login to the EMQX Cloud Console.

   In deployment overview, click +TLS/SSL to configure the certificate contents. You can upload a file or fill in the certificate contents directly in the popup window.

   ![Login to the EMQX Cloud Console](https://assets.emqx.com/images/b4e58b882b5a83ebeb6dd06cb5dc43df.png)

2. The following configuration items are needed to be filled in.

   - Type of certification:
      - One-way authentication: only the client verifies the server-side certificate
      - Two-way authentication: the client and the server validate each other's certificates.
   - Certificate: server-side certificate
   - Certificate chain: the certificate chain, which is usually provided when a third party issues a certificate, can be completed by going to Certificate chain completion if it is missing.
   - Certificate private key: server-side private key
   - Client CA certificate: the client's CA certificate is required when selecting a two-way certification

   ![SSL Config](https://assets.emqx.com/images/415bb87e75723aefee4877b3562798cb.png)

3. It's all done when TLS/SSL status is running.

   ![running status](https://assets.emqx.com/images/afe9fb43c7e6a4edbaf0a2dff77f549f.png)

 
## Connection Test

Before testing, make sure that you have created authentication information, refer to Certification and Authentication. In this tutorial we will use MQTTX for testing:

1. To create a new connection, enter the Name, Client ID is randomly generated
2. Select Host and fill in the deployed connection address and port
   - If you select an SSL connection, select ports `mqtts:// and 8883`
   - If you select WebSocket with SSL, select ports `wss:// and 8084`
3. Enter the authentication information you have created: username and password
4. Select true on SSL/TLS
5. Certificate selection
   - Certificates certified by third-party authorities, no CA certificate required
   - For self-signed certificates, a server-side CA certificate is required or, for two-way certification, a client-side certificate and private key are required
6. Turn on strict mode
7. Click on Connect

   ![Click on Connect](https://assets.emqx.com/images/8096e59f10b660dcc72f84d5ce03cc2f.png)

   ![SSL](https://assets.emqx.com/images/2a8d4cf2f8b93d7cd9b648f9d30793ac.png)


## Summary

So far, we have completed the process of connecting the GCP IoT Core device to EMQX Cloud through the TLS/SSL port. You can refer to this article to practice the encrypted communication of the transport layer between the device and the application. Stay tuned for more tutorials!



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>


## Other articles in this series

- [Migrate Your Business from GCP IoT Core 01 | Create Deployment and Connect Devices](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-01)
- [Migrate Your Business from GCP IoT Core 03｜Use JSON Web Token (JWT) to Verify Device Credentials](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-03)
- [Migrate Your Business from GCP IoT Core 04｜VPC Network Peering and Transfer Data to GCP](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-04)
- [Migrate Your Business from GCP IoT Core 05｜Bridge Data to GCP Pub/Sub](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-05)
