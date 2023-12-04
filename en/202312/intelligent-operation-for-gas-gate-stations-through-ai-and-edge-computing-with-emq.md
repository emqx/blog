## Background

The intelligent dispatch system of the gas gate station involves utilizing real-time data collection(such as gas supply volume, gas pressure, temperature, etc.), combining information like weather and user demand, and using AI algorithms and models for prediction and optimization. 

Compared to traditional experiential manual operations, the gate station's intelligent dispatch system can better manage and optimize operations, improving the accuracy and efficiency of gas supply. This, in turn, reduces operational costs and risks, holding significant importance for both gas supply companies and users.

## Challenges of Building an Intelligent Dispatch System for Gas Gate Stations

Building an intelligent dispatch system for gas gate stations presents several challenges that must be addressed to ensure its effectiveness and reliability.

- **Difficulty in Data Aggregation**: Gate station equipment generates diverse industrial data with heterogeneous communication protocols and message formats. Traditional industrial data collection solutions struggle to support the real-time and historical data processing needs of AI algorithms in a unified format.
- **High Precision Data Requirements**: The core of AI relies on algorithms. Achieving high-value, high-frequency, and high-precision data flow for AI algorithms in the complex structure of industrial data is challenging.
- **Management of Intelligent Edge Computing**: Intelligent edge computing at gate stations involves more devices and nodes than traditional centralized computing. Efficient management and monitoring of these devices are vital for ensuring reliability and performance.

## EMQ’s Solution for Intelligent Gas Dispatch Management

![architecture diagram](https://assets.emqx.com/images/6d2aaf9200f77e78d97a681d2b9a0955.png)

- **At the edge**: The edge industrial gateway, NeuronEX, facilitates the integration of various industrial devices. It can convert dozens of industrial protocols into MQTT for real-time perception and stable transmission of various data in weak network environments. NeuronEX also supports streaming data processing and storage at the edge, as well as AI algorithm integration and optimization, catering to specific business scenarios such as device energy optimization, edge intelligent dispatch, and predictive maintenance.
- **In the cloud**: The EMQX enterprise MQTT platform, deployed in the cloud or data center, provides high availability, high concurrency, low latency, and secure data transmission, analysis, and integration capabilities for cloud-based data systems and business applications. EMQX writes real-time station data into a real-time database at a performance rate of over 10,000 TPS, reducing the processing pressure on applications and algorithm modules, and enhancing the real-time accuracy of AI training.

## What You Can Achieve with EMQ’s Solution

### Scalable, Open, and Agile for 40% Efficiency Boost

EMQ’s solution delivers standardized capability with open interfaces, horizontal scalability, and hot-swappable configurable functional modules. It supports flexible integration of new devices based on the existing architecture, easily responding to business demands at the edge and the cloud, boosting business platform development efficiency by over 40%.

### Manpower and Operational Costs Reduced by Over 60%

The EMQX MQTT platform enables users to achieve centralized management. Users can perform unified operation and maintenance configuration of edge intelligent computing for each station in the cloud. This contrasts with the traditional operational approach of on-site configuration modification and fault diagnosis for edge-side products, leading to a reduction of over 60% in manpower and operational costs.

## Related Product

### EMQX Enterprise

[EMQX Enterprise](https://www.emqx.com/en/products/emqx) is a powerful enterprise MQTT platform designed for large-scale deployments and high reliability in IoT applications. The following capabilities of EMQX Enterprise can benefit the industry:

- **High Reliability and Scalability:** EMQX Enterprise adopts a distributed architecture with high availability and scalability to handle large-scale concurrent message transmission. It supports horizontal scaling to accommodate the growing number of IoT devices and data traffic, ensuring system stability.
- **Rich Protocol Support:** EMQX Enterprise supports multiple messaging protocols besides the MQTT protocol. It allows developers to extend to support all kinds of private protocols for their application needs.
- **Data Integration:** EMQX Enterprise seamlessly integrates with various data storage services, message queues, cloud platforms, and applications. It can connect with cloud services, enabling remote data transmission and cloud-based analysis.
- **Security and Authentication:** EMQX Enterprise provides robust security features, including TLS/SSL encrypted transmission, client authentication, and access control. It supports various authentication methods such as username/password, X.509 certificates, and OAuth, ensuring the security of IoT communication.
- **Rule Engine and Data Processing**: EMQX Enterprise has a flexible rule engine for real-time data processing and forwarding based on device data. It supports operations such as data filtering, transformation, aggregation, and persistence, helping users analyze and make decisions based on their business needs.
- **Visual Monitoring and Management**: EMQX Enterprise provides an intuitive visual monitoring and management interface, allowing users to monitor IoT devices and message transmission in real-time. Users can view connection status, message traffic, and other metrics and perform device management, troubleshooting, and system configuration operations.

<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>

### NeuronEX

[NeuronEX](https://www.emqx.com/en/products/neuronex) is software tailored for the industrial sector, focusing on equipment data collection and edge intelligent analysis. It is primarily deployed in industrial settings, facilitating industrial equipment communication, industrial bus protocol acquisition, industrial system data integration, edge-level data filtering and analysis, AI algorithm integration, and integration with IIoT platforms. It offers the following features:

- **Diverse Connectivity**: NeuronEX provides multi-protocol access capability, supporting simultaneous access to dozens of industrial protocols such as Modbus, OPC UA, Ethernet/IP, BACnet, Siemens, Mitsubishi, and more. It enables integration with multiple data sources from systems like MES and WMS within the enterprise. NeuronEX also supports bidirectional data flow, allowing both data acquisition and control command issuance to devices.
- **Deploy anywhere:** NeuronEX has very low memory footprints and is suitable for running on low-profile architecture devices like x86, ARM, RISC-V, etc. It also supports docker-like containerized deployment, running with other co-located containers in Kubernetes environments.
- **Data Processing**: NeuronEX incorporates 100+ built-in functions, supporting data filtering, data manipulation, device control, and data persistence, storing data in a time-series database.
- **Algorithm Integration**: NeuronEX supports the integration of algorithms written in languages such as C, Python, and Go. It facilitates real-time inference of industrial mechanism models, machine learning, and deep learning models at the edge, enabling alerts and intelligent decision-making.
- **Edge to Cloud**: Through protocols like MQTT and SparkplugB, NeuronEX aggregates and pushes industrial data to cloud platforms. The bidirectional data flow between NeuronEX and the cloud platform establishes cloud-edge data coordination and control synergy, leveraging the platform's big data storage and analysis capabilities to amplify the value of NeuronEX usage.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
