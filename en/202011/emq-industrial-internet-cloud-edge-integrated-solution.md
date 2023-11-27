This article will introduce how to build an [industrial IoT platform](https://www.emqx.com/en/blog/iiot-platform-key-components-and-5-notable-solutions) that integrates the capabilities of industrial data collection, aggregation, cleaning, storage and analysis, and visualization and display based on open source and commercial software in the community. Based on this solution, readers can adjust this solution design according to their own needs for building the industrial internet platform that meets actual business needs and accelerate the realization of industrial intelligence transformation.



## Challenges of the Industrial Internet

With multiple protocols co-existing in the industrial domain, there is no avoiding the problem of how to connect heterogeneous devices and converge data for subsequent edge or cloud computing. Two general solutions are currently available:

- **At the edge-end, adopt traditional application directly connecting and controlling devices.** This approach is generally for specific devices or models, with more customizable but **is less portable, reusable, scalable, and flexible,** unable to interface with today's big data and AI backend, and cannot analyze the data in-depth and generate more value.
- **Implement by deploying the cloud architecture software to the edge-end.** The cloud is dominated by the IT industry and the level of information is very good. However, due to cost considerations, hardware devices at the edge generally have limited computing power, so it is not feasible to directly migrate the software of the cloud architecture to the edge devices. **The software that implements the above functions at the edge must be optimized to accommodate the actual operation at the edge**.

To integrate the different needs of OT and IT at the edge, **EMQ officially  launched [a solution for industrial internet cloud edge collaboration](https://github.com/emqx/edge-stack/)** to help enterprises in the field to cope with the problems and challenges faced by the edge of industrial Internet. This solution is suitable for deployment at the edge, with various industrial protocol parsing, multi-source data access and data analysis capabilities, and can quickly implement the functions of the edge layer under the industrial Internet architecture in a cloud-edge collaboration way.



## Solution 1: Lightweight edge computing industrial internet platform

This solution can implement the industrial protocol parsing, data aggregation and streaming analysing at the edge and store the data that is through streaming analysing in a lightweight time-series database deployed at the edge.  The applications running at the edge-end can get data from the time-series database and process it and present it to the user. The Edge Manager running at the edge-end provides a management console for easy software configuration and management.

![iiot_sol_1.jpg](https://assets.emqx.com/images/9ef14959f493f1988071226e28003dbc.jpg)

### Applicable scenarios

Higher requirements for real-time, can **run as an autonomous independent application on the edge of the gateway or IPC,** no interaction with the cloud. All computation and storage in this solution are implemented at the edge, so there are certain requirements for the hardware.  Users can deploy the software and applications separately on multiple hardware devices according to the actual situation.

### List of software

This solution will use these software products in the following list.

| No.  | Name                                                       | Provider     | Open source        |
| :--- | :--------------------------------------------------------- | :----------- | :----------------- |
| 1    | [EMQX Neuron](https://www.emqx.com/en/products/neuron)        | EMQ          | No - `1`           |
| 2    | [EMQX Edge](https://www.emqx.com/en/products/emqx)            | EMQ          | Yes, Apache 2.0    |
| 3    | [EMQX Kuiper](https://github.com/lf-edge/ekuiper)        | EMQ          | Yes, Apache 2.0    |
| 4    | [Edge manager](https://hub.docker.com/r/emqx/edge-manager) | EMQ          | No - `2`           |
| 5    | TDengine                                                   | Taosdata     | Yes, GNU AGPL v3.0 |
| 6    | Grafana                                                    | Grafana Labs | Yes, Apache 2.0    |

`1:` In the future, Neuron plans to open-source its basic functions. Currently, users can download the trial version and use it for free. If there are not enough data collection points for the built-in trial version, you can [apply online](https://www.emqx.com/en/try?product=neuron) through EMQ website.

`2:` Users can use all features in the free version for free, except for a limited number of managed nodes. If you want to try more node management features, you can [apply online](https://www.emqx.com/en/try?product=neuron) through the EMQ website.

**The description of basic functions of product**

1. Neuron: Industrial IoT data collection
   - Supports [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication)，OPCUA，IEC61850，IEC104, [BACnet](https://www.emqx.com/en/blog/bacnet-protocol-basic-concepts-structure-obejct-model-explained) and other protocols and devices.
   - A management console. It allows users to visually configure and access data across industrial equipment in a browser.
   - Northbound standard MQTT data delivery, which sends data to a designated MQTT message server based on a user-specified configuration.
   - Southbound control interface for rule-based device control in conjunction with the rule engine features provided by Kuiper.
   - Local data storage for storing and viewing the raw data of the device.
2. Edge: lightweight MQTT message broker
   - Implement aggregation of industrial devices messages.
   - Connect streaming processing software and processing industrial data.
   - Accept the control message of rule engine, implement offline message caching.
   - Interfacing with cloud messaging servers to enable offline message caching.
3. Kuiper: SQL-based IoT streaming processing framework
   - The ability to continuously consume, filter, transform and route data from within edge.
   - Implementing flow analysis, rule engines and message pushing based on this.
   - Can be extended to enable support for different data sources, interconnecting ERP, MES, WMS and industrial data at the edge, as well as real-time analysis and processing.
4. Edge manager: Web management console that integrates with Neuron, Edge and Kuiper
   - Easy, unified visual management on the web.
   - Implemented including the configuration of the Neuron for issuing, data sending targets.
   - Edge state management.
   - Management of Kuiper streams, rules and plug-ins, etc..
5. TDengine: open-sourced time-series database, implement the processing of collected data
   - Storing raw data, or data that has been streamed, in a database.
   - Applications can access and analyze data for processing through SQL.
6. Grafana: Simulate the customer's application and present the data stored in TDengine.

**Supported hardware and software environments**

- Raspberry Pie, Gateway, IPC
- x86 & ARM - 64 bit and 32 bit
- Support for common Linux systems
- Physical machines, Docker & KubeEdge support, etc.

| No.  | Name                                                       | x86*32 | x86*64 | ARM 7 | ARM 64 | PPC64 | Mac  | Docker |
| :--- | :--------------------------------------------------------- | :----- | :----- | :---- | :----- | :---- | :--- | :----- |
| 1    | [EMQX Neuron](https://www.emqx.com/en/products/neuron)        |        | ☑      | ☑     | ☑      | ☑     |      | ☑      |
| 2    | [EMQX Edge](https://www.emqx.com/en/products/emqx)            | ☑      | ☑      | ☑     | ☑      | ☑     | ☑    | ☑      |
| 3    | [EMQX Kuiper](https://github.com/lf-edge/ekuiper)        | ☑      | ☑      | ☑     | ☑      | ☑     | ☑    | ☑      |
| 4    | [Edge manager](https://hub.docker.com/r/emqx/edge-manager) | ☑      | ☑      | ☑     | ☑      | ☑     | ☑    | ☑      |
| 5    | TDengine                                                   | ☑      | ☑      |       | ☑      |       |      | ☑      |

### Start trial

To make it easier for users to try, the demo scenario utilizes Docker and Docker compose technology for quick deployment, and users can follow [tutorial](https://github.com/emqx/edge-stack/blob/master/developer-scripts/README.md) to experience the solution on a virtual host, IPC, or computing-powered gateway. In the actual business system deployment process, users can deploy directly with binary installation packages in the production environment as needed, which will run more efficiently.

In this sample scenario, the data is sent out via the Modbus TCP protocol to simulate temperature and humidity data, which enters the system to achieve data collection, aggregation, cleaning, storage analysis and visualization capabilities. The following is a visualization report of temperature and humidity presented in Grafana.

![edge_sol.png](https://assets.emqx.com/images/75ddaac7e174e12137caa4433ca7e818.png)

Note: The container images released by TDengine are by default for x86*64 environments, so if you want to switch to an ARM architecture, you need to manually change `docker-compose.yml` to point to the correct version.



## Solution 2: cloud edge collaboration industrial internet platform

This approach differs from the above in that it **introduces the concept of cloud edge collaboration,** with underlying distribution and orchestration capabilities for container-based applications on the edge similar to those provided by KubeEdge/IEF. The centralized management of instances such as Neuron, Edge and Kuiper enables **online management and updating of data collection, aggregation and analysis logic at the edge in the cloud.**  Also in the cloud, by deploying EMQX Enterprise's distributed, highly available clustering capabilities to access and analyze data from devices distributed across different edge endpoints.

![iiot_sol_2.png](https://assets.emqx.com/images/b2159860f854daaface005fbf339dcd7.png)

### Applicable scenarios

This solution is used in business scenarios where there are multiple management nodes that **need to be controlled and managed in the cloud in a centralized and unified way for edge nodes located in different locations**. With this solution, users do not need to go to the location of the physical edge nodes to manage them, which greatly improves management efficiency.

- Multi-location, multi-node distributed support: there are multiple edge nodes, which may be different workshops in the plant, or even industrial parks in different cities.
- Large-scale device access: need to analyze industrial data and data from other business systems in the cloud (e.g., ERP, CRM, etc.) to obtain more valuable analysis results.
- Cloud edge collaboration
  - Management and control of edge nodes: the cloud-end can control and manage physical nodes at the edge, and open up network connections from the cloud-end to gateways and IPC after NAT to achieve control from the cloud to the edge.
  - Application and Middleware Deployment: immplement the distribution and deployment of customer applications and software.
  - Operation and maintenance management: monitor the software's operating status, automatic recovery, etc., to achieve the log management.

### List of software

This solution will use the following products except the products which used in the solution 1 edge-end.

| No.  | Name             | Provider | Open source |
| :--- | :--------------- | :------- | :---------- |
| 1    | EMQX Enterprise | EMQ      | No - `1`    |
| 2    | IEF              | Huawei   | No - `2`    |

`1`: EMQX Enterprise Enterprise IoT MQTT messaging platform supports one-stop access for millions of IoT devices, MQTT & CoAP multi-protocol processing, and low-latency real-time message communication. Supports built-in SQL-based rule engine, flexible processing/forwarding of messages to back-end services, storage of message data to various databases, or bridging to Kafka, RabbitMQ and other enterprise middleware.

`2`: [IEF intelligent edge platforem (Intelligent EdgeFabric)](https://www.huaweicloud.com/product/ief.html) is the commercialized version of KubeEdge, Huawei's open-source cloud edge collaboration platform, which meets customers' demands for remote control of edge computing resources, data processing, analysis and decision-making, and intelligence, and provides users with a complete integrated service of edge and cloud collaboration.

### Start trial

- IEF platform is a Huawei public cloud service that users can access and try directly.
- Kuiper is live on IEF and can be deployed, installed and maintained directly through the IEF platform (Readers can refer to the video「[Cloud edge collaboration for efficient IoT edge streaming service processing - Huawei IEF & EMQX Kuiper lightweight edge data solution](https://www.bilibili.com/video/BV1hQ4y1A7Vy?from=search&seid=15773267177167801393)」to learn how to use Kuiper in IEF). Neuron and Edge are not currently available on IEF, but users can install them directly into edge nodes via Docker Hub, and the user can manage and control them from deploy Edge Manager in the cloud.
- [EMQX Enterprise](https://marketplace.huaweicloud.com/contents/894cac48-2002-4b30-93ee-c2664422e6c1) is now live in Huawei Cloud, and users can also use the [online MQTT cloud service](https://www.emqx.com/en/cloud) provided by EMQ.
- Persistence or bridging methods of cloud-end data are available to the user, they can choose according to their needs. The related information on which can be found on the [EMQ website](https://www.emqx.com/en/products/emqx).



## Summary

Based on the industrial internet infrastructure capability platform built by this solution, users can implement efficient and low-cost industrial Internet device connectivity, acquisition and analysis. Whether it is a lightweight pure edge solution or a cloud-edge collaboration solution with a more complex deployment environment, it can be realized by this solution.


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a >
</section>
