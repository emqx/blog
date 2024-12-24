In our [previous blog](https://www.emqx.com/en/blog/exploring-isa95-standards-in-manufacturing), we explored the concept of ISA95 and the various data and operational models it defines. As we continue this journey exploring the ISA95 standard, we will discover how it enables manufacturers to navigate the complex intersection of Information Technology (IT) and Operational Technology (OT). In addition, we will discover how the [unified namespace](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot) is proving to be a more adaptable solution for modern industrial manufacturing.

## The Data Flow of Automation Pyramid Model

As described in the last episode of this series, the Automation Pyramid provides a visual representation of how different layers of automation technology interact and communicate to manage and control industrial processes.

![Automation Pyramid](https://assets.emqx.com/images/201ebdca20d9c3429d72dca978f93e6a.png)

The above Automation Pyramid illustrates how information flows upward from the field level to the enterprise level, enabling data-driven decision-making and process optimization. Conversely, commands and control signals flow downward from the enterprise level to the field level, influencing the operation of industrial processes.

1. **Field Level to Control Level:** Sensors and actuators at the field level collect data about the physical processes, such as temperature, pressure, and flow rates. This data is transmitted to the control level, where programmable logic controllers (PLCs) and distributed control systems (DCS) receive and process the information. PLCs and DCS execute control algorithms based on the received data, influencing the behavior of machinery and processes on the factory floor.
2. **Control Level to Supervisory Level:** The control level gathers data from various PLCs and DCS units that manage different sections of the industrial process. The data is sent to the supervisory level, where supervisory control and data acquisition (SCADA) systems display real-time information and visualizations of the processes. Operators at the supervisory level can send commands to the control level to adjust process parameters or initiate certain actions.
3. **Supervisory Level to MES and Enterprise Level:** SCADA systems at the supervisory level transmit relevant process data to the Manufacturing Execution System (MES) and higher-level enterprise systems. The MES layer uses data from the supervisory level to manage resource allocation, scheduling, and production activities. Data collected from multiple points within the automation system is used for analysis and decision-making at the enterprise level.
4. **Enterprise Level to Lower Levels:** The enterprise level, which includes business systems like Enterprise Resource Planning (ERP), makes high-level decisions based on data from lower layers, such as production scheduling and resource planning. Decisions made at the enterprise level can influence operations in the lower layers by sending commands for changes in production plans or resource allocation.
5. **Feedback Loops:** Feedback loops are established between different layers to ensure that actions taken at one level have the desired impact on the processes. For example, if a certain production target is set at the enterprise level, the control level adjusts the parameters to meet that target, and the results are fed back for evaluation.

## The Challenges of Data Management in Automation Pyramid 

Modern technologies, such as IIoT devices, edge computing, and cloud integration, have added new dimensions to the interactions between layers of the Automation Pyramid. Edge devices can preprocess data locally and send only relevant information to higher layers, reducing latency. Cloud integration allows for remote monitoring and advanced analytics. Overall, the interactions between different layers have become more complex and dynamic as technology continues to evolve. This makes it difficult to adapt the automation pyramid model to modern technologies. 

Here are some of the key challenges:

1. **Data Silos:** Industrial environments often consist of diverse systems, each generating and storing data independently. This leads to the creation of data silos, where information is isolated within specific layers of the Automation Pyramid. Data silos hinder cross-functional visibility and collaboration, making it difficult to obtain a comprehensive view of operations.
2. **Lack of Standardization:** Different layers of the Automation Pyramid may use disparate data formats, protocols, and communication methods. This lack of standardization complicates data integration and movement between layers, leading to compatibility issues and time-consuming manual interventions.
3. **Data Complexity:** Industrial processes generate large volumes of complex data from various sources, such as sensors, PLCs (Programmable Logic Controllers), SCADA (Supervisory Control and Data Acquisition) systems, and MES (Manufacturing Execution Systems). Managing and organizing this diverse data landscape becomes increasingly challenging as systems evolve and the amount of data grows.
4. **Scalability Issues:** Traditional data organization and movement methods might not scale effectively to accommodate the increasing volume of data generated in modern industrial processes. As data volumes increase, the existing architecture may struggle to handle the load, resulting in performance bottlenecks and data processing delays.
5. **Real-Time Requirements:** Many industrial processes require real-time or near-real-time data analysis and decision-making. Ensuring that data is collected, transmitted, and processed quickly and accurately across different layers of the Automation Pyramid becomes a critical challenge.
6. **Integration Complexities:** Integrating new systems, technologies, or equipment into existing automation architectures can be complex and time-consuming. Integrations may require custom connectors, middleware, or interfaces to ensure seamless data movement between layers.
7. **Data Security and Privacy:** Industrial environments are prime targets for cybersecurity threats. Ensuring the secure movement of data between different layers of the Automation Pyramid while maintaining data integrity and protecting sensitive information is a significant challenge.
8. **Legacy System Compatibility:** Many industrial setups include legacy systems that might use outdated communication protocols or technologies. Integrating these legacy systems with modern data organization and movement practices can be challenging.
9. **Maintenance and Support:** Over time, traditional data organization methods can lead to technical debt, making system maintenance and support more complex and resource-intensive. This can hinder agility and the ability to adopt new technologies.

These challenges can impact the efficiency, scalability, and overall effectiveness of industrial processes. 

## The Power of Unified Namespace

A Unified Namespace in the context of the industry refers to a standardized and consistent approach to data representation and organization across various systems, processes, and components within an industrial environment. It aims to harmonize the way data is named, accessed, and managed, irrespective of the underlying systems or technologies. The Unified Namespace offers a way to bridge the gap between diverse data sources, legacy systems, and modern technologies, creating a unified view of data that can be easily accessed, shared, and leveraged across the organization.

![Unified Namespace](https://assets.emqx.com/images/7ced7ddc775e5ff7eff678a81ade30fd.png)

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
    <a href="https://www.emqx.com/en/resources/open-manufacturing-hub-a-reference-architecture-for-industrial-iot?utm_campaign=embedded-open-manufacturing-hub&from=blog-the-power-of-unified-namespace-in-modern-manufacturing" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## Using Unified Namespace Over Automation Pyramid

Implementing a Unified Namespace architecture in industrial automation is a transformative solution that effectively addresses several challenges inherent in the traditional Automation Pyramid model.

First, a Unified Namespace excels at facilitating seamless integration, in stark contrast to the Automation Pyramid's propensity to create data silos and complex integration processes. By providing a standardized framework for data representation and access, it streamlines communication between different layers within the automation ecosystem, promoting interoperability and efficient data exchange.

Second, this approach greatly improves data accessibility by providing a unified interface for data from disparate sources, protocols, and technologies; while the automation pyramid hides critical data behind layered systems, making it less readily available for decision making and analysis.

Finally, the Unified Namespace embodies scalability, flexibility, and adaptability to accommodate the increasing volume of data generated by modern industrial processes. It minimizes technical debt by promoting standardized practices and reducing the need for custom connectors. By providing a holistic view of data, it empowers organizations with comprehensive insights, promotes cross-functional collaboration, and fosters agility and innovation in the industrial landscape.

## Conclusion

While the traditional Automation Pyramid remains valuable for conceptualizing industrial control systems, the Unified Namespace surpasses it by aligning with the demands of Industry 4.0 and digital transformation. As industries evolve, embracing the Unified Namespace enables companies to harness the full potential of data, streamline operations, and drive innovation, ultimately leading them to a more efficient and competitive future.

Achieving the Unified Namespace architecture becomes remarkably easy when you integrate [EMQX](https://www.emqx.com/en/products/emqx) and [NeuronEX](https://www.emqx.com/en/products/neuronex) into your existing infrastructure. In our next blog, we will delve into the integration, explaining why EMQX and NeuronEX are the ideal combination for building a Unified Namespace within your organization. Together, these components lay the foundation for a Unified Namespace that seamlessly connects the various facets of your industrial ecosystem, facilitating streamlined data management.



<section class="promotion">
    <div>
        Contact Our IIoT Solution Experts
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
