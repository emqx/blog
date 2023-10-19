As described in [Part 1](https://www.emqx.com/en/blog/a-digital-transformation-journey-to-smart-manufacturing), accessing and leveraging data from both Operational Technology (OT) and Information Technology (IT) sources has become a paramount requirement. This IT and OT convergence is at the heart of the Industry 4.0 revolution, enabling organizations to make data-driven decisions, optimize processes, and achieve unprecedented levels of efficiency. To realize IT and OT convergence, two aspects must be met.

1. Bridging the gaps between IT and OT to enable data flow.
2. Identifying the Data Sources from various systems.

In this blog, we explore the key role of [EMQX](https://www.emqx.com/en/products/emqx), a robust MQTT broker, and [Neuron](https://www.emqx.com/en/products/neuron), a powerful industrial connectivity gateway, in seamlessly accessing and integrating data from OT and IT sources.

## Addressing the OT-IT Convergence Challenge

Traditionally, OT and IT have operated in silos in industrial environments. OT systems, including sensors, PLCs, SCADA systems, and more, were responsible for controlling and monitoring physical processes on the factory floor. Meanwhile, IT systems handled enterprise-level data, including inventory, customer information, and business analytics.

But the true potential of [smart manufacturing](https://www.emqx.com/en/blog/the-smart-manufacturing-revolution) lies in the convergence of these two worlds. Accessing real-time data from OT devices and integrating it with IT systems opens up a world of possibilities. Manufacturers can gain deeper insight into production processes, monitor equipment health in real time, and implement predictive maintenance strategies. This convergence also enables improved supply chain management, better product quality control and better decision making.

### EMQX: The MQTT Broker Powerhouse

At the heart of this OT-IT convergence is EMQX, a highly versatile [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison). [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is a lightweight messaging protocol designed for efficient communication between devices in low-bandwidth, high-latency, or unreliable networks—ideal for the often challenging OT environment.

![EMQX: The MQTT Broker Powerhouse](https://assets.emqx.com/images/054425d2d4deee6846b338accf21ae4a.png)

EMQX serves as a central hub for data exchange, effortlessly connecting various IT systems such as streaming analytic platform Kafka, Pulsar, or data storage like Oracle, PostgreSQL, Cassandra, or industrial systems like SAP. It efficiently manages MQTT communication, ensuring that data from these data sources is reliably delivered to other IT systems for analysis and decision-making or data storage. Moreover, EMQX is designed to scale, allowing it to handle massive volumes of data from numerous IT systems, making it a perfect fit for large-scale industrial operations.

<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>

### Neuron: The Industrial Connectivity Gateway

EMQX is complemented by Neuron, a powerful industrial connectivity gateway. Neuron acts as a bridge between the OT and IT worlds, seamlessly translating data protocols and formats to ensure compatibility. It provides extensive support for industrial communication protocols such as [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication), [OPC UA](https://www.emqx.com/en/blog/opc-ua-protocol), and Ethernet/IP, and translates to MQTT-based protocols such as [MQTT Sparkplug](https://www.emqx.com/en/blog/mqtt-sparkplug-bridging-it-and-ot-in-industry-4-0) and [OPC UA over MQTT](https://www.emqx.com/en/blog/opc-ua-over-mqtt-the-future-of-it-and-ot-convergence), making it highly adaptable to various OT devices. devices such as PLCs, sensors, and actuators with IT systems.

![Neuron: The Industrial Connectivity Gateway](https://assets.emqx.com/images/b57fde2a3772cf0354962f7ee66403be.png)

By integrating with the [eKuiper](https://ekuiper.org/) edge streaming engine, Neuron can provide the ability to pre-process data at the edge. This means it can filter, aggregate or transform data before it is sent to IT systems. This capability significantly reduces the burden on IT resources and ensures that only relevant and processed data reaches enterprise systems. In addition, this integrated edition of Neuron and eKuiper, called NeuronEX, supports edge computing, enabling AI and machine learning algorithms to be executed at the edge for real-time decision making and predictive analytics.

<section class="promotion">
    <div>
        Try Neuron for Free
             <div class="is-size-14 is-text-normal has-text-weight-normal">The Industrial IoT connectivity server</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>

### Putting It All Together

The synergy between EMQX and Neuron is evident in their combined ability to access, translate and efficiently deliver data from OT sources to IT systems, achieving IT and OT convergence. This powerful duo provides manufacturers with real-time insights, actionable data, and the agility to adapt to changing production environments.

![EMQX & Neuron](https://assets.emqx.com/images/2d49c5e8df480a4bebc7c88134acf2bb.png)

With EMQX and Neuron, accessing and leveraging data from both OT and IT sources is no longer a luxury, but a necessity for companies looking to stay competitive and thrive in the ever-evolving industrial landscape. EMQX and Neuron are essential tools for realizing the full potential of smart manufacturing. By seamlessly accessing and integrating OT and IT data sources, companies can implement predictive maintenance strategies, optimize production processes and improve overall operational efficiency. This not only reduces downtime and maintenance costs, but also improves product quality, supply chain management and, ultimately, the bottom line.

<section
  class="is-hidden-touch my-32 is-flex is-align-items-center"
  style="border-radius: 16px; background: linear-gradient(102deg, #edf6ff 1.81%, #eff2ff 97.99%); padding: 32px 48px;"
>
  <div class="mr-40" style="flex-shrink: 0;">
    <img loading="lazy" src="https://assets.emqx.com/images/0b88fa3cf1c98545e501e3b8073fdccc.png" alt="Open Manufacturing Hub" width="160" height="226">
  </div>
  <div>
    <div class="mb-4 is-size-3 is-text-black has-text-weight-semibold" style="
    line-height: 1.2;
">
      A Reference Architecture for Industrial IoT (IIoT)
    </div>
    <div class="mb-32">
      Building an efficient and scalable IIoT infrastructure.
    </div>
    <a href="https://www.emqx.com/en/resources/open-manufacturing-hub-a-reference-architecture-for-industrial-iot?utm_campaign=embedded-open-manufacturing-hub&from=blog-first-step-to-a-smart-factory" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## Identifying the Data Sources in a Smart Factory

Identifying the right data sources is a kind of discovering a treasure trove that can unlock operational insights, improve efficiency, and enable data-driven decision making. In the following diagram, we show the common network topology of industrial systems for manufacturers and how each component is connected. EMQX will be at the heart of these systems for message exchange. Neuron supports these OT devices and sensors to report data in MQTT formats as they change.

![Identifying the Data Sources in a Smart Factory](https://assets.emqx.com/images/e87900711e70ea2a3d47ccf0fe36dd3e.png)

Here, we take a look at the critical process of identifying data sources in a [smart factory](https://www.emqx.com/en/blog/what-is-a-smart-factory-key-components-4-levels-of-evolution), and where the gold mine of information can be found.

### 1. Sensors and IoT Devices: The Digital Nervous System

At the heart of every smart factory is a complex network of sensors and devices. These digital perceptors are strategically placed throughout the factory floor, monitoring a variety of variables such as temperature, humidity, pressure, vibration, and more. They serve as the digital nervous system of the factory, continuously collecting real-time data on equipment status, environmental conditions, and product quality. So, we have the “Neuron”, an industrial connectivity gateway, to collect this data and control the devices when receiving commands.

Sensors and devices are essential data sources, providing the raw data needed for process optimization, predictive maintenance, and quality control. They provide a tiny view of operations, enabling plant managers to pinpoint inefficiencies and identify areas for improvement.

### 2. PLCs and SCADA Systems: Orchestrating the Orchestra

Programmable Logic Controllers (PLCs) and Supervisory Control and Data Acquisition (SCADA) systems are the conductors of the manufacturing orchestra. PLCs control the machines and equipment on the factory floor, while SCADA systems monitor and manage the entire production process. Neuron has a large number of various PLC drivers for accessing PLC data. Neuron can also access the SCADA system using standard protocols such as OPC UA, MQTT and API.

PLCs and SCADA systems serve as data sources by collecting and transmitting data on equipment performance, production rates, and process parameters. They provide valuable insight into the efficiency of manufacturing operations, supporting real-time decision-making and process optimization.

### 3. Historians: Archiving the Past for Future Insights

Historians are data repositories specifically designed for storing historical data. They are crucial data sources in a smart factory as they capture and archive data from sensors, PLCs, and other sources over time. This historical data becomes a goldmine for analyzing trends, identifying anomalies, and making informed decisions. EMQX offers a variety of connectors for ingesting data to various data storage or historians. 

Historians are instrumental in retrospective analysis, enabling manufacturers to learn from past performance and continuously improve processes. They also play a pivotal role in compliance and reporting, ensuring that the factory adheres to industry regulations and standards.

### 4. Enterprise Systems: Bridging the Gap to Business Insights

Smart factories are not limited to the shop floor. They are extending their reach into enterprise systems. Enterprise Resource Planning (ERP), Customer Relationship Management (CRM), and Supply Chain Management (SCM) systems are invaluable sources of data that provide insight into business operations. Using standard communication protocols such as MQTT Sparkplug or OPCUA over MQTT, these enterprise systems can talk to each other and even directly to machines and equipment through the EMQX Broker.

Data from enterprise systems includes order information, inventory levels, customer preferences, and sales data. This data helps align manufacturing with business goals, enabling agile production planning, demand forecasting, and inventory management.

### 5. Cloud Computing: Processing Data at the Cloud Platform

Cloud computing platforms such as Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP) offer a wide range of services and tools to manage and analyze data from these sources, making them essential for smart manufacturing initiatives. The cloud provides the scalability, reliability, and accessibility required to support the data-driven decision-making processes in modern manufacturing facilities. EMQX acts as a middleware layer that facilitates the connection of factory floor systems and devices to cloud platforms, enabling secure, efficient, and scalable communications.  

Data from maintenance records and predictive analytics models are used to predict equipment failures and schedule maintenance. The cloud is an appropriate platform for hosting these analytics models.

## Conclusion

Identifying the right data sources is the first step on the journey to a data-driven smart factory. Sensors, PLCs, SCADA systems, historians, enterprise systems, and edge computing devices collectively form the data ecosystem that enables smart manufacturing. By tapping into these sources with EMQX and Neuron, factories gain the insights and agility needed to optimize processes, reduce downtime, improve quality, and remain competitive in the ever-evolving world of Industry 4.0.



<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
