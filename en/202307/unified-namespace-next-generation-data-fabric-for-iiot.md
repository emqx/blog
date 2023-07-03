In the era of IoT, the Industrial Internet of Things (IIoT) has emerged as a game-changer for industrial operations. By connecting devices, machines, and systems, IIoT enables real-time monitoring, analysis, and control of industrial processes, improving efficiency, productivity, and safety.

However, the fragmented edge devices, heterogeneity, and complexity of traditional IIoT systems raise significant challenges in terms of interoperability, scalability, and security. The Unified Namespace (UNS) framework can address these challenges and provide several advantages for IIoT 4.0, including simplified data integration, improved data accessibility, and greater scalability.

## What is Unified Namespace?

The definition of UNS still remains arguable. From an automation perspective, UNS is a common naming convention that organizes devices, data points, and services based on their attributes, such as location, function, and type. But [according to Walker Reynolds](https://www.youtube.com/watch?v=1h0DFwWz4uE), UNS is not only a naming convention but an architecture that meets five requirements:

- UNS is the semantic hierarchy structure of business data and events.
- UNS is the hub that connects all smart devices and IT infrastructure.
- UNS is the single source of truth for all data and information in business.
- UNS is the foundation of future digital transformation.
- UNS is where the current state of business lives, enabling real-time snapshots of business.

What is common to both perspectives is that UNS is an ontology communication layer that connects every other piece in the IIoT. It provides a shared data crossroads that enables communication and collaboration between different systems and stakeholders, regardless of their underlying technology or vendor.

This shared crossroads can lead to improved interoperability, scalability, and flexibility of IIoT systems, reduced integration costs, and faster time-to-market.

Another advantage of UNS in IIoT 4.0 is improved data management and analysis. By using a common naming convention, UNS enables data points to be easily identified, accessed, and analyzed across different systems and applications. With a UNS architecture, everyone across the company can access every part of the data of any IIoT component, as long as they have security authorization.

## Evolution of the UNS Architecture

The first UNS project was built by Walker Reynolds (President of Industrial 4.0 Solutions and winner of the 2015 Ignition by Inductive Automation Award) in 2005. He is also the most important figure in advocating UNS. The project was built using dynamic data exchange (DDE) with Excel spreadsheets for a salt mining field. In the following year, the project was adapted to MQTT technology.

Initially, Walker planned to develop a data highway connecting all IIoT infrastructures. The data highway was responsible for acquiring the data from all stampers, mining machines used in salt mines. Maintainers would not have to drive down to the screen at the control booth to check human machine interfaces (HMIs) or control panels in panel offices. With all operations are unified in one namespace, users can monitor production environments without moving physically between plants and factories that are miles away.

In the following years, UNS continued to evolve, and is today a basic concept in the IIoT.

## How Unified Namespace Differs from Traditional IIoT Data Models

In Industry 3.0, there is typically an ERP or CRM system in control of the organization and the manufacturing plant. It coordinates with a warehouse management system (WMS), taking production orders from operators and dispatch schedules, bills of materials (BOMs), and work orders down to the plant floor. The manufacturing plant reports back to the central office and operators via spreadsheets. The data is not real-time, meaning it cannot accurately reflect the current business state.

![Industry 3.0](https://assets.emqx.com/images/5cb2b8ded153af99510b2dc98fc21837.png)

Another concern is that if the company decides to introduce new technologies like business intelligence (BI) or artificial intelligence and machine learning (AI/ML), these components usually require a comprehensive dataset, which cannot be based on one piece of a traditional IIoT 3.0 system. However, there is no easy way to create a unified dataset.

Additionally, an ERP system usually cannot connect to factory machinery directly. This leads to extremely complex infrastructure, referred to as a ‘data spaghetti’. This is exactly where UNS could shine: with different namespaces operating on the edge and cloud, they orchestrate with each other to form a UNS.

![UNS](https://assets.emqx.com/images/5e0a17bfeb781e0b7025254f79351029.png)

The following diagram illustrates the different layers of a UNS:

![The different layers of a UNS](https://assets.emqx.com/images/b294138a63506c8a3f18e1fb9dcd1895.png)

At the bottom of the stack is where your **physical devices like HMI/PLC** live, and also where data is generated. Each PLC/HMI, or even a tag with information inside, could be called a namespace, which pushes the readings and events to the **data acquisition layer** for supervisor control and monitoring. It is common to deploy an industrial gateway like Neuron at this layer for data collection.

The layer above data acquisition is the **manufacturing execution layer (MES)**, which coordinates between ERP/CRM and the plant floor, converting sales orders into manufacturing schedules. The traditional ERP layer processes customer sales, plans manufacturing, manages inventory, checks finance payments, etc.

At the top is the **Business intelligence Cloud** used to manage the business layer.

## Advantages of a Unified Namespace

There are several advantages to implementing a Unified Namespace in an organization:

- **Easy integration:** Data producers and consumers in the IIoT environment are integrated simply by plugging them into the network. No specialized expertise or engineering work is needed to integrate data at each layer of your business, from the shop floor to the business layer.
- **Improved agility:** UNS enables real-time access to the current state of data at any given time, making it possible to test, plan, and deliver faster and more predictably.
- **Scalability:** Because data producers and consumers are integrated through a central hub, and not directly connected, it becomes possible to connect millions of nodes and enable seamless communication between them.

## 4 Types of UNS

There are four kinds of Unified Namespaces in terms, with different uses and methodologies.

### Functional Namespaces and OEE

Functional namespaces refer to the organization of devices and data points in an industrial network based on their function or purpose. This means that devices and data points are grouped together based on the specific task they perform, rather than their physical location or network.

For example, in a manufacturing plant, devices and data points related to the production process might be grouped together in a functional namespace, while devices and data points related to maintenance might be grouped together in a separate functional namespace.

Usually, functional namespaces are used to measuring Overall Equipment Effectiveness (OEE), a metric used to measure the performance of manufacturing equipment. OEE is an important metric in lean manufacturing and continuous improvement initiatives. It takes into account three factors:

- **Availability:** The amount of time the equipment is available for production
- **Performance:** The speed at which the equipment operates
- **Quality:** The percentage of products produced that meet the desired specifications

By combining different data sources and context via a functional namespace, manufacturers can measure OEE, identify areas where equipment is underperforming, and take steps to improve efficiency and productivity.

### Informative Namespace

An informative namespace organizes devices and data points in an industrial network based on their informational content. This means that devices and data points are grouped together based on the type of information they provide rather than their physical location or function.

For example, in a manufacturing plant, devices and data points related to temperature might be grouped together in an informative namespace, while devices and data points related to pressure might be grouped together in a separate informative namespace.

The purpose of an informative namespace is to make it easier to access and analyze data in an industrial network. By grouping devices and data points based on their informational content, it becomes easier to identify patterns and trends in the data, and to make informed decisions based on that data. Overall, an informative namespace can help to improve the efficiency and effectiveness of an industrial network by making it easier to access and analyze data, and to make informed decisions based on that data.

### Definitional Namespace

In the context of industrial networks and computer science, a definitional namespace organizes devices and data points based on their definitions or attributes. This means that devices and data points are grouped based on their characteristics, such as type, size, or function.

For example, in a manufacturing plant, devices and data points related to motors might be grouped together in a definitional namespace, while devices and data points related to sensors might be grouped together in a separate definitional namespace.

### Ad Hoc Namespace

An ad hoc namespace, on the other hand, is a temporary or informal way of organizing devices and data points. This might be used when a more formal namespace is not yet established or where devices and data points must be grouped together quickly for a specific purpose.

For example, if a manufacturing plant experiences a sudden equipment failure, an ad hoc namespace might be created to group together all the devices and data points related to that equipment in order to quickly diagnose and fix the problem.

## Conclusion

The UNS simplifies device communication and data management, as devices and data points only need to know the topic that the device or data they want to communicate with is publishing or subscribing to, rather than the exact location or network of the device or data.

In addition to simplifying device communication and data management, the Unified Namespace provides a way to integrate different systems and protocols in an industrial network. Organizing devices and data points into a hierarchical topic structure makes integrating different systems and protocols easier, as they can all communicate using the same naming convention.

Overall, the Unified Namespace is an important feature of IIoT that simplifies device communication, data management, and system integration. It allows for a more efficient and streamlined industrial network, leading to increased productivity, reduced downtime, and improved overall performance.





<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
