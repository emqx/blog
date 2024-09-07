EMQX Enterprise 5.8.0 is now officially available!

This update introduces a powerful cluster linking feature, enhancing disaster recovery capabilities to ensure seamless global business operation. Additionally, it includes new message transformation capabilities and support for multiple data integrations, offering users greater flexibility in building IoT applications with EMQX Enterprise. The release also comes with several security enhancements.

## Cluster Linking

As businesses increasingly operate across multiple countries and regions, the demand for software infrastructure that supports global distribution and cross-regional disaster recovery has grown significantly.

The cluster linking feature in EMQX Enterprise 5.8.0 enables the connection of multiple EMQX clusters across different regions into a single, globally distributed large cluster. Clients can connect to their regional EMQX cluster while efficiently communicating with clients in other regions. In the event of a regional cluster failure, clients are seamlessly transferred to other clusters, ensuring continuous business operations.

Cluster Linking offers enhanced efficiency, ease of use, and scalability compared to the previous Cluster Bridging feature. Its key advantages include:

- A unified namespace across connected clusters, allowing seamless communication between clients on different clusters, unlike Cluster Bridging, where clusters remain logically independent with separate topic naming and other configurations.
- Intelligent message routing based on actual subscription needs and client distribution, reducing unnecessary message replication. In contrast, Cluster Bridging often requires full data replication between clusters for a given topic.

![MQTT Cluster](https://assets.emqx.com/images/a8c2ab079103d3f362424f93e6f6f5b7.png)

## Message Transformation

While EMQX Enterprise's built-in rule engine provides robust message processing capabilities, it is primarily designed for data integration scenarios and does not alter the normal message publishing and subscription process. However, in certain cases, users may need EMQX Enterprise to transform messages from publishers before delivering them to subscribers. This could involve adding fields to the message or converting Protobuf messages to JSON format, among other transformations.

To address this, version 5.8.0 introduces message transformation, allowing users to apply custom rules to modify and format messages before they are processed or delivered to subscribers. This highly customizable feature supports multiple encoding formats and advanced transformations.

![EMQX Message Transformation](https://assets.emqx.com/images/9d3bd8813545e80d22b0947fa348ab9b.png)

## Enhanced Security: Kerberos Authentication and OIDC SSO Support

EMQX Enterprise 5.8.0 also introduces several new security enhancements:

- Kerberos Support: A widely used network authentication protocol, Kerberos ensures secure and authenticated communication between parties in a network.
- OIDC SSO for EMQX Dashboard: The EMQX Dashboard now supports Single Sign-On (SSO) using the OIDC (OpenID Connect) protocol, allowing enterprises to leverage their existing OIDC services for SSO.
- Enhanced HTTP Authentication: Support for an optional `acl` field in the HTTP response body, allowing for client privileges to be specified and enforced through ACL rules, governing publish and subscribe actions.

## Expanded Data Integration: Azure Blob Storage, Couchbase, and Datalayers

This release expands data integration with the following systems:

- **Azure Blob Storage**: A data storage service from Microsoft Azure, similar to AWS S3, for storing large-scale structured and unstructured data.
- **Couchbase**: A distributed document database with powerful search and analytics capabilities, supporting fast and efficient bi-directional data synchronization between edge and cloud environments.
- **Datalayers**: An edge-cloud collaborative, multimodal distributed database optimized for industries such as Industrial IoT, IoV, and Energy. It supports time series storage, key-value storage, and provides comprehensive solutions for data storage, computation, and analysis.

Additionally, version 5.8.0 adds support for using `client_attrs` (client attributes) within the rule engine. These attributes, set by developers based on specific application needs, can now be leveraged in various EMQX Enterprise features including authentication, authorization, MQTT extensions, and rule engine.

## Hot Upgrades

Minimizing the impact of version upgrades on clients and business operations is a critical challenge for EMQX Enterprise clusters. The Hot Upgrades feature introduced in version 5.8.0 effectively addresses this issue. Compared to rolling upgrades, hot upgrades offer several key advantages:

- **Seamless Upgrades**: The MQTT connection remains uninterrupted during the hot upgrade, ensuring clients are unaware of the upgrade process.
- **Speed**: The hot upgrade process is completed within seconds.
- **Flexibility**: The upgrade granularity can be controlled at a fine code module level, and custom hot update packages can be built on demand through plug-ins, eliminating the need for complete installation packages.

To further streamline the hot update process, version 5.8.0 allows hot update packages to be uploaded via the EMQX Dashboard, enabling cluster-wide hot updates with ease.

![EMQX Hot Upgrades](https://assets.emqx.com/images/a3026ab1c488c60cb3c3b90f54d6715f.png)

For a detailed list of all feature updates and bug fixes in version 5.8.0, please refer to the [EMQX Enterprise 5.8.0 changelog](https://www.emqx.com/en/changelogs/enterprise/5.8.0).



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?tab=self-managed" class="button is-gradient px-5">Get Started →</a>
</section>
