## Google Cloud for IoT: What Is Google Cloud IoT Core?

Google Cloud Platform’s IoT Core is a managed service that enables secure and reliable communication between Internet of Things (IoT) devices and Google Cloud. It consists of two main components: the Device Manager and Protocol Bridges.

The Device Manager manages device identities, metadata, and authentication, allowing for secure device provisioning and communication. The Protocol Bridges provide support for HTTP and [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) protocols, enabling devices to send and receive messages over these protocols.

**If you are using Google IoT Core, you should be aware that Google will retire the service on August 16, 2023. We’ll explain the implications of the service’s shutdown and how you can migrate to alternative solutions.**

This is part of a series of articles about IoT in the cloud (coming soon).

## Future of Google Cloud for IoT: Shutdown of Google IoT Core

Google has declared the discontinuation of IoT Core, with the service set to retire on August 16, 2023.

Since its beta launch in March 2017, Google Cloud IoT Core experienced consistent growth, and Google’s announcement to discontinue the service after just five years was a surprise to many in the industry.

If you are using Google IoT Core, you will need to migrate to an alternative service. There are multiple options, including migrating to another cloud provider, using a specialized vendor like [EMQX](https://www.emqx.com/en), or creating a custom solution.

## GCP IoT Core Migration Plan and Strategies

This section provides guidance to help in creating and executing a migration strategy to transition from an IoT Core-dependent environment to a new setup that does not rely on Google Cloud IoT Core for any of these aspects:

- Authentication of edge devices
- Management of edge devices
- Communication between Google Cloud and edge devices

### Define the Migration Scope

This step involves choosing which workloads to migrate to a non-IoT Core environment. The assumption is that these workloads are partly deployed at the edge (i.e., run on edge devices) near the processing data, while the backend runs on Google Cloud.

Here is a diagram showing the typical architecture of a workload on IoT Core:

![Typical architecture of a workload on IoT Core](https://assets.emqx.com/images/e85ef9020e573b239df3191fbb6a7391.png)

<center>Image Source: Google Cloud</center>

This workflow can be described as follows:

1. The edge devices gather and process data locally.
2. Processed data, including telemetry and device state, is transmitted to the Google Cloud backend via IoT Core using MQTT protocols.
3. IoT Core publishes the data received from the edge as Pub/Sub messages in designated topics.
4. Workloads on the backend subscribe to these Pub/Sub topics to obtain telemetry and device state information.
5. The backend may issue commands and device configurations to the edge devices.

For a successful migration, it is important to conduct a thorough evaluation of the source environment architecture to gain comprehensive insights. In this context, the source environment refers to the existing IoT Core-based setup.

### Evaluate the Source Environment

This step involves collecting and assessing information about the edge devices, the source environment, and the way IoT Core is used in the organization. This assessment helps inform the migration strategy and verifies if the necessary resources are available for the migration.

The assessment process should include the following:

1. Create an inventory of edge devices registered with Cloud IoT Core.
2. Compile an inventory of backend workloads integrated with Cloud IoT Core.
3. Arrange the backend workloads and edge devices into categories.
4. Create proofs of concept and experiment.
5. Calculate the TCO (total cost of ownership).
6. Design the target environment's architecture.
7. Select the devices and workloads to be migrated first.

Upon completing the assessment, there should be separate inventories for edge devices and for backend workloads. To maintain consistency, it is recommended to create these inventories before deploying the new edge devices and workloads.

### Establish the Foundation for Migration

This step involves planning and building, including the provisioning and configuration of cloud infrastructure and services to support the migrated workloads:

1. Establish a hierarchy of resources.
2. Set up Identity and Access Management (IAM) rules.
3. Establish network connectivity.
4. Implement security hardening.
5. Configure monitoring and alerts.

### Migrate the Workloads and Devices

Once the target environment’s foundation is ready, the relevant backend workloads and edge devices can be moved to the new environment:

1. Set up the infrastructure resources to support the target environment’s architecture.
2. Migrate the devices and workloads to the new environment. There are several ways to migrate. For example, you might use a two-step approach where the source and target environments exist in parallel during the migration process, enabling rollbacks in the event of a failure.
3. Once the new environment is working, decommission the original environment.

## Why You Should Migrate from Google IoT Core to EMQX MQTT Platform

Given that Google IoT Core is based on MQTT, the best alternative options for seamless migration are MQTT-based IoT messaging platforms or services.

As an official Google Cloud migration partner, EMQ Technologies Inc. has brought solid and well-rounded IoT connectivity solutions to our mutual customers. We are here to provide ideal migration options for those seeking the best Google IoT Core alternatives.

![Google Cloud migration partner](https://assets.emqx.com/images/b23e300b6626dcc777c8f8ea1c8da9bc.png)

[EMQX](https://www.emqx.com/en) is the world’s most scalable MQTT Broker, based on open standards,100% compliance with MQTT 5.0 and 3.x standards and deep integration with GCP.

EMQX offers users the ability to connect any device at any scale, then move and processe IoT data anywhere in real-time. The outstanding scalability, high performance, and rich features of EMQX make it an ideal choice for Google IoT Core users:

- **World’s best scalability features**: EMQX has been verified in [test scenarios](https://www.emqx.com/en/blog/reaching-100m-mqtt-connections-with-emqx-5-0) to scale to 100 million concurrent MQTT connections in one cluster of 20 nodes, making it the world’s most scalable open source MQTT platform.
- **Business-critical reliability**: EMQX can ingest and process millions of MQTT messages efficiently per second per cluster while guaranteeing sub-millisecond latency in message delivery with its soft real-time runtime. It supports up to 99.99% SLA and ensures no data loss with built-in RocksDB data persistence.
- **Widely adopted and fully proven**: Since its first release in 2013, EMQX has been downloaded 20M+ times, connecting 100M+ IoT devices worldwide every day, and boasts more than 20K+ global users. EMQX is trusted by over 300 customers from various industries like automotive, IIoT, transportation & logistics, energy & utilities, and more in mission-critical IoT scenarios, including well-known brands like HPE, VMware, Verifone, SAIC Volkswagen, and Ericsson.

## Two Options for Migration from Google IoT Core

EMQX has developed into the on-premises version, [EMQX Enterprise](https://www.emqx.com/en/products/emqx), and the SaaS version, [EMQX Cloud](https://www.emqx.com/en/cloud), to meet the demands of different types and scales of enterprises and accelerate the digitalization, real-time and intelligent transformation for them. You can migrate from Google IoT Core to either of these services.

### EMQX Cloud: Fully Managed MQTT Service

[EMQX Cloud](https://www.emqx.com/en/cloud) is the world's first fully managed MQTT 5.0 public cloud service launched by EMQ, providing MQTT message service with a one-stop operation and maintenance host and a unique isolated environment for MQTT services. EMQX Cloud can help you quickly build industry applications and easily realize the collection, transmission, computation, and persistence of IoT data.

With announcing [support for Google Cloud Platform (GCP)](https://www.emqx.com/en/blog/introducing-emqx-cloud-on-google-cloud-platform) in September 2021, EMQX Cloud is the world's first and only fully-managed MQTT service that supports all major public cloud platforms, including GCP, AWS, and Azure. Enterprises using Google Cloud IoT Core to manage their IoT infrastructures, whether on GCP or other cloud platforms, can migrate their IoT applications and endpoints to EMQX Cloud seamlessly and effortlessly.

![EMQX Cloud](https://assets.emqx.com/images/3c833240befdf29e5e72fa0c54336d6c.jpeg)

EMQX Cloud supports VPC peering on GCP. Users who want to migrate from Google IoT Core simply need to choose Google Cloud as the cloud platform when creating new deployments on EMQX Cloud. EMQX cluster and user's resources on GCP, such as Cloud SQL, Kafka, MongoDB, and InfluxDB, can communicate by establishing a VPC peering connection. This communication is under the same network, making it more secure and reliable as it's a private network connection.

![Migrate GCP IoT Core to EMQX Cloud](https://assets.emqx.com/images/c1acaa030e4fa4374041c9ddd0823b1b.png)

**Next steps for migrating GCP IoT Core to EMQX Cloud:**

<section class="promotion">
    <div>
        Start with our Migration to EMQX Cloud Handbook
    </div>
    <a href="https://www.emqx.com/en/resources/migrating-from-google-cloud-iot-core-to-emqx-cloud" class="button is-gradient px-5">Download Now →</a>
</section>

For more technical details, see our multi-part guide to migrating to EMQX Cloud:

- Part 1: [Create Deployment and Connect Devices](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-01)
- Part 2: [Enable TLS/SSL over MQTT to Secure Your Connection](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-02)
- Part 3: [Use JSON Web Token (JWT) to Verify Device Credentials](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-03)
- Part 4: [VPC Network Peering and Transfer Data to GCP](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-04)
- Part 5: [Bridge Data to GCP Pub/Sub](https://www.emqx.com/en/blog/migrate-your-business-from-gcp-iot-core-05)

### EMQX Enterprise: Self-Managed MQTT Messaging Platform

[EMQX Enterprise](https://www.emqx.com/en/products/emqx) is a large-scale distributed MQTT messaging platform that can be deployed on the Google Cloud Platform (GCP) in multiple ways. You can easily and quickly migrate your devices on IoT Core to EMQX Enterprise and then continue to integrate with your data services in GCP, without affecting the existing business.

EMQX Enterprise is suitable for deployment with strict requirements and needs to be deployed in a specified deployment environment, especially in a private environment. Meanwhile, the enterprise has a relatively complete team for operation, maintenance, and support with daily basic software operation and maintenance.

![Migrate GCP IoT Core to EMQX Enterprise](https://assets.emqx.com/images/72c3fbb3d6a6ec6be19eaca8f1f0f920.png)

**Next steps for migrating GCP IoT Core to EMQX Enterprise:**

<section class="promotion">
    <div>
        Start with our Migration to EMQX Enterprise Handbook
    </div>
    <a href="https://www.emqx.com/en/resources/migrating-from-google-cloud-iot-core-to-emqx-enterprise" class="button is-gradient px-5">Download Now →</a>
</section>

For more technical details, see our detailed three-step guide to migrating from IoT Core to EMQX Enterprise:

- Part 1: [How to Deploy EMQX Enterprise on Google Cloud](https://www.emqx.com/en/blog/how-to-deploy-emqx-enterprise-on-google-cloud)
- Part 2: [Migrating Devices from GCP IoT Core to EMQX Enterprise](https://www.emqx.com/en/blog/migrating-devices-from-gcp-iot-core-to-emqx-enterprise)
- Part 3: [Ingesting IoT Data From EMQX Enterprise to GCP Pub/Sub](https://www.emqx.com/en/blog/ingesting-iot-data-from-emqx-enterprise-to-gcp-pub-sub)

## Conclusion

Global enterprise customers, across industries like automotive, IIoT, transportation and logistics, energy and utilities, have proven EMQX's scalability and reliability, with massive deployments of mission-critical IoT applications on GCP. As an existing Google Cloud IoT Core user, EMQX is a natural alternative with strong product capabilities, which minimizes impact on your current running systems.

**[Get in touch with our IoT experts](https://www.emqx.com/en/contact)** and learn more about migrating from Google Cloud IoT Core to EMQX. We will help you start your migration and ensure you succeed.
