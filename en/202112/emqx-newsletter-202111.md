In November, EMQX teams kept optimizing the product in response to recent problems and user feedback. The open-source EMQX v4.3.10 has been released, while the enterprise version of v4.2.9 and v4.3.5 were also released. The ACL performance optimization based on the built-in database has been released out. [EMQX Cloud](https://www.emqx.com/en/cloud) launched several new features based on users' needs this month to improve the product experience continuously.

## EMQX : Enterprise v4.4 is coming soon, and open source v5.0-beta.2 enters the testing stage

### Development of EMQX Enterprise v4.4 is completed

The development of EMQX Enterprise v4.4 has been completed now, and the test is in full swing. The official version will be available in December.

It has been about half a year since the last minor release EMQX v4.3. In response to feature requests from many enterprise customers we received during this period, version 4.4 will mainly include below features: 

- The rule engine integrating with InfluxDB Cloud (InfluxDB 2.0)
- MongoDB integration supports SRV Record so it can seamlessly connect with MongoDB Atlas, which strengthens the integration capability with cloud services.
- The rule engine supports direct integration with SAP Event Mesh, opening up the connection channel between IoT data and SAP BTP platform.
- The rule engine newly supports the MatrixDB hyper-converged time-series database. EMQX has passed the write volume test of 210,000 lines/second with a single machine, and the subsequent version will further optimize and improve performance.

The following functions will be provided in subsequent open-source versions:

- Support dynamic modification of the client keepalive to adapt to the switching of energy consumption strategy in different working conditions of devices such as the Internet of Vehicles T-BOX
- Support online Trace to capture DEBUG-level logs to facilitate troubleshooting and diagnosis of abnormal behavior of specified clients or topics

   ![online Trace](https://assets.emqx.com/images/9b627c894ff3ef03e2b772793e0fafb1.png)
 

- Support Slow Subscription statistics to discover abnormal situations such as message blocking in the production environment in time

   ![Slow Subscription statistics](https://assets.emqx.com/images/fddd41d6d4d5b1c156cb61d21a4cb1ac.png)

- Support dynamically discarding client-published messages with multi-language hook extension (exhook)
- Dashboard static resources are loaded using relative paths to facilitate the configuration of reverse broker under the website subdirectory.

### EMQX open source v5.0-beta.2 is released

5.0-beta.2 has now entered the testing stage and is scheduled to be released in early December. The following functions have been added to this version:

- The rule engine reconstructs the configuration file structure and HTTP API of Data Bridge.
- The rule engine supports statistics of Data Bridge's success/failure, rate, etc.
- The authentication data management interface for gateways and listeners under the gateway is added.
- Command issuing interface of Lwm2m is added
- Some problems with authentication are fixed
- HTTP API related behaviors are unified
- The forced kick-off mechanism on the client-side is introduced.
- Support CROS
- Support trace operation through HTTP API
- Add more test cases to improve stability
- Standardized and unified placeholders, the same syntax and variables are used in authentication and rule engine

In the next beta.3 version, we will finally enable the dashboard by default, configure all the underlying features from UI, and provide a lot more features at the same time. The following is a list of the features to expect in beta.3：

1. Support configuration and management of rule engine on Dashboard
2. Support viewing and configuring cluster parameters on Dashboard, and support hot configuration during runtime
3. Support Plugins management. EMQX can install independent plug-in packages without code compilation
4. Provide Application and Exhook
5. All the new features for v4.4, such as Slow Subscription, relative path loading of online Trace and Dashboard static resources will be opened in this version

We’d like to encourage our users to try out the beta releases and provide feedback. Your opinion may become a key factor that affects the future development of EMQX.

### Outlook for the future

While the new version is released, we are also conducting relevant technical research and update:

1. v4.4 will be built on top of both Erlang/OTP 23 and 24.

2. While continuing supporting zero-downtime hot-beam patches for bug fixes, we can now upgrade from 4.3 to 4.4 for nodes in a cluster in a rolling fashion.

3. The development branch of persistent sessions with high reliability has been merged into the trunk, and a performance test has been carried out

   Before V5.0, EMQX already had the capability to persist MQTT sessions. However, these sessions are not synchronized to other nodes in the cluster. This month, the development branch that supports persistent sessions with high reliability was finally merged into the trunk, and a performance test was carried out.

4. EMQX cluster deployment based on CDK. This month, the EMQX European R&D team open-sourced [cdk-emqx-cluster](https://github.com/emqx/cdk-emqx-cluster), an internal tool for cluster deployment. It is based on AWS’s CDK development kit, capable of deploying and configuring EMQX cluster and surrounding integrated services, such as etcd, Kafka load generator for running stress tests, and Prometheus for monitoring. It has a complete Grafana Dashboard.

   ![EMQX Grafana Dashboard](https://assets.emqx.com/images/392d67ebdad90865f77af9576db51fe5.png)

   ![EMQX Grafana Dashboard](https://assets.emqx.com/images/c12f37d5dd3b03ab1e612cb8cabdca98.png)

## EMQX Cloud: Focus on user needs to bring a better experience

### Sub-account management feature is launched

In order to meet the needs of independent management, deployment and accounting of different departments and organizations within the enterprise, EMQX Cloud launched the sub-account management function this month. Similar to AWS's IAM account, the root user can create sub-accounts under the same account system. Different roles (administrator, project administrator, project user, finance, audit) can be assigned to sub-accounts to take charge of different features or modules. Together with the project management functionality, different accounts can be used to manage the deployment of different projects.

Through this function, users can manage resources more finely and meet the compliance requirements of Finance and audit at the same time.

### Alarm for a large number of offline devices is added in the monitoring module

The condition of a large number of offline devices may be caused by some external emergencies. The development, operation and maintenance personnel need to obtain the alarm information at the first time to avoid unnecessary losses. In the latest version of EMQX Cloud, the following device offline monitoring rules are set: when the difference between the current number of connections and the number of connections recorded in the last time is greater than one-tenth of the total number of connections in the specification, a message will be prompted in the monitoring to inform the relevant personnel to check in time. This will further improve system stability.

### Saving data to MongoDB of Alibaba Cloud is added in the rule engine

Forwarding data to non-relational databases is supported by EMQX Cloud. At present, the resource configuration of the rule engine has added support for Alibaba Cloud MongoDB. The rule engine can be used to persist data to MongoDB of Alibaba Cloud. It provides more choices for business developers to achieve data persistence, which makes business landing more easily.

EMQX team is always committed to bringing a better MQTT broker for the IoT era. Please stay tuned on EMQX.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
