In today's rapidly evolving industrial landscape, data has become a critical asset for organizations seeking to streamline processes, improve efficiency, and gain competitive advantage. The realm of automation, particularly in the context of ISA-95, presents both opportunities and challenges in effectively managing data. 

This blog series examines the challenges of data organization in ISA-95 and explores the concept of a [unified namespace](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot) and its benefits. We will also outline its implementation, including the use of the ISA-95 Equipment Model Standard and clustering for multi-site data replication.

The first blog explores the fundamental concepts of the ISA-95 standards, their importance in improving manufacturing processes, and their role in fostering cross-functional collaboration, all of which contribute to the optimization and implementation of traditional industrial operations.

## Understanding ISA-95 Standards

The ISA-95 standard, also known as ANSI/ISA-95 or ISA-95, is an international standard developed by the International Society of Automation (ISA). It focuses on the integration of enterprise and control systems within the manufacturing industry. ISA-95 stands for "Enterprise-Control System Integration," and it provides a framework for designing and implementing interoperability between an organization's business and manufacturing processes, with the goal of improving the interactions between them.

![ISA-95 Standards](https://assets.emqx.com/images/b84e90188e3fbbfc6cf6371989fb99f5.png)

The primary goal of ISA-95 is to establish a common language and structure for communication and data exchange between different levels of an organization, ranging from the enterprise level, where business decisions are made, down to the control level, where real-time production processes are managed. This standard helps bridge the gap between the information technology (IT) and operational technology (OT) domains.

## ISA-95 Hierarchy (Automation Pyramid)

The Manufacturing Automation Pyramid is a conceptual representation of ISA-95 hierarchy that is often associated with industrial automation and control systems. The Automation Pyramid, also known as the automation hierarchy of "Industrial 3.0", illustrates the hierarchical structure of control and automation systems within industrial environments. It's a visualization that helps understand the different levels of control and their interconnections in a manufacturing setting.

![ISA-95 Hierarchy](https://assets.emqx.com/images/cf851556acf8bcea025e1204d831fd45.png)

The levels of the Automation Pyramid, from bottom to top, typically include:

1. **Level 0: Field Devices and Instruments:** This is the lowest level of the pyramid, where physical field devices such as sensors, actuators, and instruments are located. These devices gather data from the manufacturing process and send it to higher levels for processing, and control machinery.
2. **Level 1: Control Devices and PLCs (Programmable Logic Controllers):** At this level, basic control functions are executed. PLCs and control devices receive input from field devices and make decisions based on pre-programmed logic. They control processes and machinery directly.
3. **Level 2: Supervisory Control:** This level involves supervisory control systems that gather data from multiple PLCs and control devices. It provides real-time monitoring, data aggregation, and limited control capabilities for specific areas or processes.
4. **Level 3: Manufacturing Execution Systems (MES):** MES is responsible for managing production scheduling, work orders, quality control, and overall coordination of manufacturing operations. It bridges the gap between the shop floor and enterprise systems.
5. **Level 4: Enterprise Systems:** This is the highest level of the pyramid and includes enterprise resource planning (ERP) systems, which manage business operations, including finance, sales, procurement, and planning. Data from the lower levels feed into these systems for higher-level decision-making.

ISA-95 is more than just a pyramid hierarchy. On the other hand, it provides a more comprehensive and standardized approach to integrating enterprise and control systems, helping organizations design and implement interoperability between business and manufacturing processes. The Automation Pyramid can be a useful visualization to consider when thinking about the different levels of control within the context of implementing standards like ISA-95.

<section
  class="promotion-pdf"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/0b88fa3cf1c98545e501e3b8073fdccc.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="promotion-pdf__title" style="
    line-height: 1.2;
">
      A Reference Architecture for IIoT Based on UNS
    </div>
    <div class="promotion-pdf__desc">
      To build an efficient and scalable IIoT infrastructure.
    </div>
    <a href="https://www.emqx.com/en/resources/open-manufacturing-hub-a-reference-architecture-for-industrial-iot?utm_campaign=embedded-open-manufacturing-hub&from=blog-exploring-isa95-standards-in-manufacturing" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## Categories of Information Model

The Categories of Information Model refers to a classification system that organizes and categorizes information exchanged between different levels of an organization's manufacturing processes. This model provides a structured framework for defining and understanding the types of information that need to be exchanged to ensure effective communication and integration between business and manufacturing processes.

1. **Control and Monitoring:** This category includes information related to the real-time control and monitoring of equipment, processes, and production activities. It involves data such as sensor readings, setpoints, alarms, operational statuses, and other data needed for immediate operational control.
2. **Production Schedule:** This category encompasses information about production planning and scheduling. It includes data on production orders, work orders, production sequences, start and end times of tasks, and any changes to the production schedule.
3. **Performance Analysis:** This category involves information that is used to analyze the performance of manufacturing processes. It includes data related to cycle times, production rates, downtime, efficiency metrics, quality measurements, and other performance indicators.
4. **Quality and Compliance:** Information related to quality control and compliance falls under this category. It includes data about quality standards, inspection results, testing data, non-conformities, corrective actions, and compliance with regulations.
5. **Maintenance and Reliability:** This category includes information about equipment maintenance, reliability, and asset management. It covers data on maintenance schedules, maintenance activities, spare parts inventory, equipment condition monitoring, and predictive maintenance.
6. **Material Flow and Inventory:** Information regarding the movement of materials, inventory levels, and material requirements is included in this category. It involves data on material consumption, material requests, inventory quantities, and material tracking.
7. **Resource Allocation:** This category encompasses information related to the allocation and utilization of resources, including personnel, equipment, tools, and facilities. It includes data on resource availability, assignments, and usage.
8. **Order Fulfillment:** Information related to order processing and fulfillment is categorized here. It includes data on customer orders, order status, order changes, shipping details, and delivery schedules.

## Equipment Object Model

The Equipment Object Model within the ISA-95 standard focuses on representing the physical and logical equipment and resources used in the manufacturing and production processes. This model provides a structured framework for organizing, categorizing, and managing equipment, allowing for effective monitoring, control, and maintenance within the manufacturing environment. 

![Role based equipment hierarchy](https://assets.emqx.com/images/423592f1ee5935b2e2abce0490614d17.png)

This model hierarchy is designed to reflect the physical and logical relationships between different equipment units and their respective roles within the production process. While specific terminologies might vary based on the industry and organization, here is a common organization of the Equipment object model hierarchy:

1. **Enterprise:** This is the highest level of the hierarchy, representing the entire organization or company. It encompasses all sites and facilities.
2. **Site:** A site is a physical location or facility where manufacturing operations occur. It can be a factory, plant, or any other facility. Multiple areas or zones can exist within a site.
3. **Area:** An area represents a specific section within a site where a particular type of manufacturing activity takes place. Areas could be designated for different processes, products, or functions.
4. **Unit:** A unit refers to a distinct piece of equipment or a specific production unit within an area. Units can be individual machines, assembly lines, or process units. They are the primary operational components of the manufacturing process.
5. **Control Module:** A control module represents a functional aspect or module of a unit that can be controlled and monitored independently. It could be a specific subsystem, device, or component within a larger unit.
6. **Component:** A component represents smaller parts or sub-components that make up a control module. This level might not be present in all hierarchies and is particularly useful for complex systems.

The purpose of ISA88 is to provide standards and recommended practices as appropriate for the design and specification of batch control systems as used in the process control industries.

## Information Exchange between Level 4 (ERP) and Level 3 (MES)

The Information Exchange Model between Level 4 (Enterprise) and Level 3 (Manufacturing Operations Management) within the ISA-95 framework involves the communication and data exchange between the business processes at the enterprise level and the manufacturing operations processes at the operations management level. This exchange is crucial for aligning business strategies, production planning, and execution on the shop floor.

![Information Exchange between Level 4 (ERP) and Level 3 (MES)](https://assets.emqx.com/images/cd1449f1e46ef75469ff9f7a24b5c381.png)

The information models can be classified as Resource, Production Capability, Product Definition, Production Schedule, and Production Performance.

1. **Resource Availability:** Level 3 provides real-time updates to Level 4 about the current availability of resources and any potential constraints that might impact production. Based on production orders, Level 4 sends requests to allocate specific resources for production activities.
2. **Production Capability:** Level 4 shares information about the manufacturing capacity and constraints with Level 3. Level 3 replies the utilization of manufacturing capabilities to Level 4, indicating how effectively the available resources are being utilized.
3. **Product Definition:** Level 4 provides detailed specifications and requirements for the products to be manufactured. Level 3 verifies that the product specifications and requirements from Level 4 are accurate and feasible for production.
4. **Production Schedule:** Level 3 receives production plans from Level 4, detailing the sequence and timing of manufacturing activities required to fulfill the orders. Then, Level 3 communicates any changes or updates to the production schedule back to Level 4, such as delays, expedited orders, or adjustments due to resource constraints.
5. **Production Performance:** Level 3 shares real-time progress updates with Level 4, including information on quantities produced, completed tasks, and any deviations from the production plan. Level 3 provides data on quality inspections, test results, and any quality-related issues that arise during production.

In general, Level 4 initiates the exchange by sending production orders, work orders, and resource allocation requests to Level 3. Level 3 responds with updates on resource availability, production progress, quality data, and any changes to the production schedule.

## Manufacturing Operations Management Activity Model

The Manufacturing Operations Management (MOM) Activity Model is a part of the ISA-95 framework that focuses on breaking down and structuring the activities that occur within the manufacturing operations processes. It provides a detailed view of the tasks and operations that need to be executed on the shop floor to fulfill the requirements specified by higher-level processes, such as production orders and work orders.

![Manufacturing Operations Management Activity Model](https://assets.emqx.com/images/df84fc1811d10605f492b9eecf4ed21b.png)

The MOM Activity Model serves as a bridge between the high-level business processes defined at the enterprise level (Level 4) and the specific actions carried out on the shop floor at the manufacturing operations management level (Level 3).

## Conclusion

In conclusion, the ISA-95 standard has played a significant role in enhancing communication and integration in manufacturing, but adapting it to modern industrial management faces challenges. The evolving complexity of manufacturing, coupled with rapid technological advancements like Industry 4.0, requires flexibility that the standard's structured framework might not fully provide. In modern industrial management, [EMQX](https://www.emqx.com/en/products/emqx) and [Neuron](https://neugates.io/) are two essential components that provide an ideal solution. Leveraging them as the [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) and industrial gateway, organizations can elevate connectivity, data handling, and adaptability in dynamic production settings. Together, they seamlessly integrate into today's industrial landscape.

For more information about the benefits of this combination, please refer to: [Modern Messaging Infrastructure for Smart Manufacturing](https://www.emqx.com/en/blog/modern-messaging-infrastructure-for-smart-manufacturing).



<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
