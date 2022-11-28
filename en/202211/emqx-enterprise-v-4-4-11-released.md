We're happy to announce the official release of [EMQX Enterprise](https://www.emqx.com/en/products/emqx) 4.4.11!

This release includes CRL and OCSP Stapling to provide more flexible security protection for clients and integrates with Google Cloud Pub/Sub to help you create more value from IoT data using Google Cloud services. It is also able to predefine API keys to meet the requirements of automatic maintenance. In addition, we fixed some bugs.

## CRL and OCSP Stapling

In previous versions, you could use X.509 certificates for client authentication and encrypted communications through EMQX's built-in SSL/TLS. In this release, CRL and OCSP Stapling are introduced.

In some cases, such as the private keys being leaked, the certificates being invalid, or the devices needing to be destroyed, the certificates stored on the IoT devices must be revoked to prevent them from being used illegally. CRL and OCSP Stapling are the keys to solving these problems.

CRL (Certificate Revocation List) is a list maintained by CA, which contains the serial numbers and revocation time of certificates that have been revoked. You are able to specify a CRL distribution point and download the CRL regularly through EMQX. The client does not need to maintain the CRL. EMQX validates the certificate during the handshake.

OCSP (Online Certificate Status Protocol) is another certificate revocation solution. Compared with CRL, OCSP can check the validity status of a certificate in real time. OCSP Stapling represents the latest enhancement of this technology, which addresses the privacy and performance concerns of the OCSP.

After OCSP Stapling is enabled, EMQX queries certificates from the OCSP server and caches the results. When a client initiates an SSL handshake to EMQX, EMQX sends the OCSP data of the certificate to the client along with the certificate chain, then the client verifies the certificate.

![How CRL and OCSP Stapling work](https://assets.emqx.com/images/d3e855dec2c109bfe96b54e2bf7c6f41.png)

<center>How CRL and OCSP Stapling work</center>

Using CRL and OCSP Stapling, you can monitor the validity of each certificate and revoke invalid certificates in time. This provides flexible and high-level security for your IoT applications.

## Google Cloud Pub/Sub integration

[Google Cloud Pub/Sub](https://cloud.google.com/pubsub) is an asynchronous messaging service designed to be highly reliable and scalable.

You can quickly establish a connection with GCP Pub/Sub through EMQX's Rule Engine, which can help you build IoT applications based on GCP faster:

- **Use Google's Streaming Analytics to process IoT data**: Build overall solutions based on Pub/Sub, Dataflow, and BigQuery. Extract, process, and analyze the continuous MQTT data in real-time to increase business value based on the IoT data.
- **Asynchronous microservice integration**: Use Pub/Sub as a messaging-oriented middleware to integrate with your applications by Pull. You can also Push subscriptions to Google Cloud services such as Cloud Functions, App Engine, Cloud Run, or custom environments on Kubernetes Engine or Compute Engine.

![Integration with Pub/Sub via Rule Engine](https://assets.emqx.com/images/2ff20dd2aa9c316c13fba9cbc3d79780.png)

<center>Integration with Pub/Sub via Rule Engine</center>

For Google IoT Core users, you can easily migrate the MQTT transport layer to EMQX to continue using applications and services on Google Cloud.

## Initialize the API keys from a file

The initialization of API keys is a new capability introduced by this release, allowing you to set up key pairs in a file before starting EMQX.

The preset keys can be used to run some tasks at the startup of EMQX: such as managing the cluster resources with scripts, importing authentication data into the built-in database, and initializing configuration.

[EMQX Kubernetes Operator](https://www.emqx.com/en/emqx-kubernetes-operator) also uses this feature to configure and manage the cluster at startup.

```
# Specify a bootstrap file
# etc/plugins/emqx_management.conf
management.bootstrap_user_file ="etc/bootstrap_apps_file.txt"

# Initialize the key pairs with the format {appid}:{secret}
# etc/bootstrap_apps_file.txt
appid1:secret
appid2:secret2
```

## Bug Fixes

The following are important bug fixes, for all bug fixes please refer to [EMQX Enterprise Edition 4.4.11 Changelogs](https://www.emqx.com/en/changelogs/enterprise/4.4.11).

- Improve the display of rule's 'Maximum Speed' counter to only reserve 2 decimal places [#9185](https://github.com/emqx/emqx/pull/9185). This is to avoid displaying floats like `0.30000000000000004` on the dashboard.
- Fix the issue that emqx prints too many error logs when connecting to mongodb but auth failed [#9184](https://github.com/emqx/emqx/pull/9184).
- "Pause due to rate limit" log level demoted from warning to notice [#9134](https://github.com/emqx/emqx/pull/9134).
- Fixed the response status code for the `/status` endpoint [#9210](https://github.com/emqx/emqx/pull/9210). Before the fix, it always returned `200` even if the EMQX application was not running. Now it returns `503` in that case.
- Fix message delivery related event encoding [#9226](https://github.com/emqx/emqx/pull/9226) For rule-engine's input events like `$events/message_delivered`, and `$events/message_dropped`, if the message was delivered to a shared-subscription, the encoding (to JSON) of the event will fail. Affected versions: `v4.3.21`, `v4.4.10`, `e4.3.16` and `e4.4.10`.
- Calling 'DELETE /alarms/deactivated' now deletes deactived alarms on all nodes, including remote nodes, not just the local node [#9280](https://github.com/emqx/emqx/pull/9280).
- When republishing messages or bridge messages to other brokers, check the validity of the topic and make sure it does not have topic wildcards [#9291](https://github.com/emqx/emqx/pull/9291).
- Disable authorization for `api/v4/emqx_prometheus` endpoint on management api listener (default 8081) [#9294](https://github.com/emqx/emqx/pull/9294).
- Fixed the option to choose the `reset_by_subscriber` offset reset policy in Kafka Consumer.
- Made Rule-Engine able to connect SQL server when its listening port is not the default (`1433`).
- Fix the default authentication mechanism of Kafka resource changed to `NONE` from `PLAIN` when upgrading EMQX from e4.4.5 and older versions.

## Other updates

In addition, we also released the following three versions:

- [EMQX Enterprise 4.3.17 Changelogs](https://www.emqx.com/en/changelogs/enterprise/4.3.17)
- [EMQX 4.3.22 Changelogs](https://www.emqx.com/en/changelogs/broker/4.3.22)
- [EMQX 4.4.11 Changelogs](https://www.emqx.com/en/changelogs/broker/4.4.11)

 



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
