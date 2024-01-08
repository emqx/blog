In the world of steel manufacturing, the integration of advanced technologies is critical to optimizing processes and ensuring unparalleled efficiency. [NeuronEX](https://www.emqx.com/en/products/neuronex) and [EMQX](https://www.emqx.com/en/products/emqx) are solutions that work together to bring about a transformational change in the way industrial edge computing is approached. This article explores a real-world client example of the seamless integration of NeuronEX and EMQX, demonstrating their combined ability to streamline data collection, management, and processing for improved steel production.

## Neuron and EMQX: Modern Architecture for Steel Manufacturing

Before the advent of new architecture with NeuronEX, and EMQX, the digital facilities of the steel manufacturer relied on third-party industrial information systems controlled through the Enterprise Service Bus (ESB). Another third-party monitoring system intricately monitored steel manufacturing processes. Our primary goal is to seamlessly integrate these two systems with NeuronEX and EMQX. NeuronEX will send data to ESB through Restful APIs, and the monitoring systems will receive real-time data through [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt). 

The below diagram shows the new architecture.

![New architecture](https://assets.emqx.com/images/e210a72eb65b5bed7f70fb3fd7c2c77d.png)

## The Foundation: Robust Networking Infrastructure

Recognizing the importance of a resilient network infrastructure, a significant investment was made to purchase 10GbE Ethernet switches and routers. This led to a major restructuring of the entire network connecting the data center to other manufacturing areas. This strategic move paves the way for a more advanced and integrated system. This move also allows NeuronEX to be deployed in the data center rather than at the edge near the machines.

## NeuronEX: A Scalable Industrial Gateway

### On-Premise Deployment and Scalable Data Collection

NeuronEX introduces a new approach to data collection by offering the flexibility of on-premises deployment with Docker containers in the factory data center, avoiding the use of the traditional edge model. This shift enables centralized management, scalable data collection, and dynamic scaling based on equipment scheduling needs. The ability to eliminate single-point hardware or network failures by deploying on centralized servers ensures uninterrupted data collection, which is critical for the demanding nature of steel manufacturing.

### Unified Data Collection and Publication with MQTT

NeuronEX excels in its ability to efficiently collect machine data. Multiple NeuronEX deployments seamlessly unify data collection and publish it in a standardized JSON format via the MQTT protocol. Compare this to manual data collection or limited machine access capabilities. NeuronEX breaks down data silos and enables interoperability between IT and OT technologies. This not only simplifies data integration, but also ensures that the entire manufacturing process benefits from a standardized and interoperable data format.

<section class="promotion">
    <div>
        Try NeuronEX for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuronex" class="button is-gradient px-5">Get Started →</a>
</section>

## EMQX: Central Data Repository for Data Analysis

### Aggregating Data for a Unified Namespace Architecture

EMQX takes control of data aggregation, providing a centralized hub where all collected data from NeuronEXs and other industrial information systems converge. The result is a unified namespace architecture that not only simplifies data management but also facilitates the creation of a contextual data platform. This platform becomes a valuable resource for both original monitors and third-party control systems, fostering a cohesive and intelligent manufacturing environment.

### Database Connectors and Storage Options

EMQX's versatility extends to its database connectors, offering a variety of options, such as time-series databases like InfluxDB and event stores like Kafka. This flexibility allows steel manufacturers to tailor their data storage solutions to meet specific business needs, ensuring that data is not only collected but also readily available for analysis, optimization, and strategic decision-making.

<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>

## Unified Management for Seamless Operations

Crucially, both NeuronEX and EMQX operate on the EMQ platform, a unified management platform that revolutionizes remote edge service management. From batch provisioning and upgrades to start-stop operations, EMQ platform simplifies on-site operations through remote management, fault diagnosis, and software and algorithm updates. The platform's ability to support batch creation and management of hundreds of edge service instances in environments such as Kubernetes and Docker, further accelerates the deployment and implementation of IIoT projects.

## Conclusion

NeuronEX and EMQX are at the forefront of a new era in steel manufacturing, seamlessly integrating to create a unified and efficient industrial edge computing solution. The synergy between on-premises deployment, scalable data collection, unified data aggregation, and advanced management capabilities ensures that steel manufacturers can embrace digital transformation with confidence. As the industry continues to evolve, NeuronEX and EMQX provide a blueprint for success that unlocks the full potential of unified industrial edge computing in the steel manufacturing landscape.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
