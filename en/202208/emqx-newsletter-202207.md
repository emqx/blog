In July, EMQX 5.0.0 was released, bringing a number of groundbreaking updates and improvements. The EMQX team is currently iterating on subsequent releases at a rate of one release every two weeks to quickly fix known issues and incorporate additional features. In addition, this month the EMQX team has made significant progress on community communication and several new features.

In terms of cloud services, EMQX Cloud has added support for two external integrated databases, giving users more options for data persistence. A new version of EMQX Kubernetes Operator has been released with simultaneous adaptation support for EMQX 5.0, and support for deployment of edge computing products such as eKuiper and Neuron has been implemented.

## EMQX

### **Rule engine RocketMQ supports authentication and ACLs**

The EMQX team has recently added authentication and ACL capabilities to RocketMQ in the rules engine to connect to RocketMQ with access control enabled, which will go live in a recent release.

### **SASL/SCRAM authentication support for Kafka**

Kafka supports SASL/SCRAM authentication, one of the SASL mechanisms that address security by performing traditional mechanisms such as PLAIN and DIGEST-MD5 for username/password authentication. EMQX will support Kafka.

EMQX will support SCRAM-SHA-256 and SCRAM-SHA-512 authentication for Kafka, which can be used with TLS to provide more secure Kafka data integration, and will also go live in a recent release update.

### **Support for checking configuration files via CLI**

We have added the ability to check configuration files for EMQX. When the configuration needs to be reloaded at runtime, you can check the modified configuration files (including plugin configuration) for syntax errors via CLI, which is very important to prevent EMQX from restarting due to configuration errors.

### **v4.3 & v4.4 upgrade**

EMQX Broker 4.3.16 & 4.4.5 and EMQX Enterprise 4.3.11 & 4.4.5 were released in early July, bringing several known bug fixes such as inaccurate memory calculations in EMQX on Linux systems, as well as HStreamDB integration, exclusive subscriptions, and many other improvements.

For more information, please check the Release Notes of the corresponding versions: [EMQX v4.4.5](https://www.emqx.com/en/changelogs/broker/4.4.5)、[EMQX Enterprise v4.4.5](https://www.emqx.com/en/changelogs/enterprise/4.4.5).

Meanwhile, the development of the next maintenance releases of 4.3 & 4.4 is nearing completion and will be released soon, so stay tuned.

### **EMQX 5.0 product explanatory articles series and live streams**

To help users understand the technical details and product value of EMQX 5.0, EMQX team has launched a series of explanatory articles on the 5.0 product. We have already published “How EMQX 5.0 Achieves 100 Million MQTT Connections with the New Mria + RLOG Architecture” and “MQTT over QUIC: The Next-Generation IoT Standard Protocol Gives New Impetus to Messaging Scenarios”, and will share more on the new developments of EMQX 5.0 in data integration, authentication and access control, plug-in extensions, etc. Please stay tuned for further updates.

## EMQX Cloud

### **Console deployment log monitoring newly revamped**

The log monitoring in the deployment details has been revamped and optimized. Previously, the logs could only be searched and filtered by time range and cluster nodes, and users had to find the key log information by themselves, which was not easy to analyze. The reworked log module reconstructs the ability to parse and search logs, and provides multiple levels of log information for both EMQX nodes [emqx-node-1] and [emqx-node-2], which can be searched and analyzed from ClientID, ClientIP, Username, Topic, Resource and Rule IDs, and can also be filtered by different error types. Error types include: **data integration**, **client**, **message**, **module**, **EMQX internal error**, etc.

### **Data integration support streaming database HStreamDB**

HStreamDB is EMQ's open-source streaming database for full lifecycle management of access, storage, processing and distribution of large-scale real-time data streams. It uses standard SQL (and its streaming extensions) as the main interface language, with real-time as the main feature, and aims to simplify the operation and management of data streams and the development of real-time applications.

EMQX Cloud is the first to support the forwarding and storage of device-side data to HStreamDB, providing users with a new solution for data persistence. See [here](https://docs.emqx.com/en/cloud/latest/rule_engine/rule_engine_save_hstreamdb.html) to learn more.

## EMQX Kubernetes Operator

### **v1.2.3 Released**

EMQX Operator 1.2.3 released in July provides the following new features.

- Port tuning pods do not restart, further improving service stability
- Automatic update without changing K8s related configuration by adjusting listener in EMQX Dashboard
- Added EMQX Cluster Status field to see if the cluster is ready
- Allow user-defined (Dashboard and Management) account passwords
- Allow users to add custom containers

The following improvements and optimizations have been made:

- Optimized configmap update file latency issue
- Fixed the problem that EMQX may have a brain fracture in K8s environment

### **Support for EMQX 5.0** 

- Deployment of EMQX non-core nodes (core still uses sts)
- Supports dynamic port scaling

### **Completed cloud environment validation**

We have used EMQX Operator to build clusters in mainstream cloud platforms and have completed the following:

- Build EMQX cluster on AWS eks, achieve 1 million connections, 500,000 TPS test verification
- EMQX cluster on Huawei cce, with 2 million connections and 1 million TPS
- Build EMQX cluster on Ali eks to achieve 1 million connections and 500,000 TPS

### **Support edge computing product deployment**

EMQ's edge computing products (eKuiper, an edge streaming engine, and Neuron, an edge industrial protocol gateway software) are supported for deployment via Helm, and high availability has been validated with KubeEdge.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
