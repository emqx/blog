EMQX and EMQX Enterprise are released in several versions in November, including enhancements in security and ecosystem.

EMQX Cloud introduces the custom functions feature, allowing users to easily convert IoT data into the format that matches the data stream.

## EMQX

EMQX is released [v4.3.22](https://github.com/emqx/emqx/releases/tag/v4.3.22), [v4.4.11](https://github.com/emqx/emqx/releases/tag/v4.4.11), [v5.0.10](https://github.com/emqx/emqx/releases/tag/v5.0.10), and [v5.0.11](https://github.com/emqx/emqx/releases/tag/v5.0.11) and EMQX Enterprise is released [v4.3.17](https://www.emqx.com/en/changelogs/enterprise/4.3.17) and [v4.4.11](https://www.emqx.com/en/blog/emqx-enterprise-v-4-4-11-released).

Since the EMQX 4.3 has reached the end of its lifecycle (v4.3.0 was released on May 8, 2021), v4.3.22 is the final community release of EMQX 4.3.

We also upgrade Erlang/OTP from v24.1.5 to [v24.3.4.2](https://github.com/erlang/otp/releases/tag/OTP-24.3.4.2) for EMQX 4.4 and EMQX 5.0.

### Google Cloud Pub/Sub Integration

EMQX Enterprise 4.4.11 integrates with Google Cloud Pub/Sub, which allows users to use Pub/Sub to send MQTT messages to services and applications hosted on Google Cloud to build IoT applications based on GCP quickly.

![Google Cloud Pub/Sub Integration](https://assets.emqx.com/images/03fab0f56293d933fcbabcd762752ab4.png)

For Google IoT Core users, you can easily migrate the MQTT transport layer to EMQX to continue using applications and services on Google Cloud.

### CRL and OCSP Stapling

In some cases, such as the private keys being leaked, the certificates being invalid, or the devices needing to be destroyed, the certificates stored on the IoT devices must be revoked to prevent them from being used illegally. v4.4 provides CRL and OCSP Stapling capabilities to address this issue, offering a flexible, advanced security solution for your IoT application.

CRL (Certificate Revocation List) is a list maintained by CA, which contains the serial numbers and revocation time of certificates that have been revoked. You are able to specify a CRL distribution point and download the CRL regularly through EMQX. The client does not need to maintain the CRL. EMQX validates the certificate during the handshake.

OCSP (Online Certificate Status Protocol) is another certificate revocation solution. Compared with CRL, OCSP can check the validity status of a certificate in real time. OCSP Stapling represents the latest enhancement of this technology, which addresses the privacy and performance concerns of the OCSP.

After OCSP Stapling is enabled, EMQX queries certificates from the OCSP server and caches the results. When a client initiates an SSL handshake to EMQX, EMQX sends the OCSP data of the certificate to the client along with the certificate chain, and then the client verifies the certificate.

### Set priority for authentication and ACL

Two new configuration options are added to EMQX 4.x, which are used to set priority for authentication and ACL. When multiple authentications or ACL plugins/modules are enabled, the priority can be set by separating their names or aliases with commas.

### Initialize the API keys from a file

The initialization of API keys from a file is a new feature introduced by v4.x. The preset keys can be used to run some tasks at the startup of EMQX, such as managing the cluster resources with scripts, importing authentication data into the built-in database, and initializing configuration. These tasks previously required creating keys after startup.

```
# Specify a bootstrap file
# etc/plugins/emqx_management.conf
management.bootstrap_user_file ="etc/bootstrap_apps_file.txt"

# Initialize the key pairs with the format {appid}:{secret}
# etc/bootstrap_apps_file.txt
appid1:secret
appid2:secret2
```

### Optimization and improvement

We fix several known bugs, such as fixing the issue that the system keeps logging errors if the authentication failed while connecting to a MongoDB instance, checking topics to avoid failure when republishing messages or bridging messages to other MQTT brokers, and fixing the issue for EMQX 5.0 that [replicant nodes](https://github.com/emqx/eip/blob/main/implemented/0004-async-mnesia-change-log-replication.md#rlog-replica) may fail to start with too many connections in large-scale performance testing.

We have also improved the implementation and security design of the MQTT protocol, including the support for challenge-response authentication of the gen_rpc library.

### Better experience in operation and maintenance

The authentication for `GET /emqx_prometheus` is removed in v4.x. Users can easily collect metrics from EMQX with Prometheus.

The REST API improvement program for v5.0 launched last month is also in progress. [EMQX 5.0.11](https://github.com/emqx/emqx/releases/tag/v5.0.11) has already contained some nice improvements, including a redesign for the `/gateways` API.

For more details, please refer to the changelogs:

- [EMQX 4.3.22](https://www.emqx.com/en/changelogs/broker/4.3.22)
- [EMQX 4.4.11](https://www.emqx.com/en/changelogs/broker/4.4.11)
- [EMQX Enterprise 4.3.17](https://www.emqx.com/en/changelogs/enterprise/4.3.17)
- [EMQX Enterprise 4.4.11](https://www.emqx.com/en/blog/emqx-enterprise-v-4-4-11-released)
- [EMQX 5.0.10](https://www.emqx.com/en/changelogs/broker/5.0.10)
- [EMQX 5.0.11](https://www.emqx.com/en/changelogs/broker/5.0.11)

## EMQX Cloud

### Custom functions

EMQX Cloud introduces a brand-new custom functions feature. With the computing capacity of the Cloud Platform, users can write custom scripts and call them during data integration. Devices send data to the Cloud Platform through topics. The platform receives data, processes them by scripts, and then passes them to other processes.

Custom functions can be applied in different situations, such as converting non-decimal data from devices into decimal data and storing them in a database or converting raw data from devices into data conforming to industry standards.

Custom functions are available to users of professional plan who have their applications hosted on AliCloud. You can get **50,000 free calls monthly** if you buy the service. You can use it immediately after payment. Please stay tuned for more details on the custom functions.

### Optimize metrics for the monitoring of the messages discarded

The metrics for the monitoring of the messages discarded have been optimized. When you go to the corresponding page of the deployment console, you will see the types of messages that were discarded: messages that were discarded because of expiration and messages that were discarded because of a full queue. This will make monitoring the operation and troubleshooting much more accessible.

## EMQX Kubernetes Operator

The deployment automation tool EMQX Kubernetes Operator has been optimized as follows:

- Fix an issue that cause a crash in v2alpha1 when there were no sts.
- Fix an issue where the sts could keep updating if a user had not modified the CR.
- Fix an issue where the service cannot be updated when the replicas is set to 1.
- Fix an error on the lastTransitionTime field of status.Condition.
- Support EMQX and reloader image registry.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
