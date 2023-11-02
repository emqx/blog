In our [previous blog posts](https://www.emqx.com/en/blog/tag/omh-for-smart-manufacturing), we discussed the basic concepts and principles behind using Neuron and EMQX to build the OMH solution. In this blog, we take a closer look at the indispensable elements of practical data management, particularly in the context of real-world modeling, as facilitated by Neuron and EMQX. Whether you're working on projects involving predictive analytics, machine learning, or any other data-driven endeavor, the presence of a robust data management strategy becomes the key to success.

# Object Naming Convention

An object naming convention is a set of rules and guidelines that dictate how objects within a data management system, should be named. The primary purpose of an object naming convention is to ensure consistency and clarity in naming, making it easier for developers, administrators, and users to understand and work with these objects.

To illustrate this concept, let's consider an example. Imagine we have a temperature device called ST1021, which is capable of sensing both humidity and temperature within a room. To facilitate communication between the ST1021 device and the Neuron, [Modbus](https://www.emqx.com/en/blog/modbus-protocol-the-grandfather-of-iot-communication) TCP is employed. The specific Modbus device ID assigned to ST1021 is 1. For data retrieval, the tag addresses allocated for temperature and humidity are 100 and 101, respectively. Consequently, the data registers within the temperature device would be organized as follows.

| **Tag Name** | **Device Number** | **Register Number** |
| :----------- | :---------------- | :------------------ |
| temperature  | 1                 | 100                 |
| humidity     | 1                 | 101                 |

Suppose we have two rooms, each equipped with two identical temperature devices, resulting in a total of four such devices. All of these temperature devices are connected to the same Modbus network, and they have been assigned Modbus device IDs as follows: 1, 2, 3, and 4.

| **Location** | **Tag Name** | **Device Number** | **Register Number** |
| :----------- | :----------- | :---------------- | :------------------ |
| Room A       | temperature  | 1                 | 100                 |
| Room A       | humidity     | 1                 | 101                 |
| Room A       | temperature  | 2                 | 100                 |
| Room A       | humidity     | 2                 | 101                 |
| Room B       | temperature  | 3                 | 100                 |
| Room B       | humidity     | 3                 | 101                 |
| Room B       | temperature  | 4                 | 100                 |
| Room B       | humidity     | 4                 | 101                 |

By using [ISA95 standard](https://www.emqx.com/en/blog/exploring-isa95-standards-in-manufacturing), we have more descriptive and consistent additional information for the location of temperature devices. For simplicity, the Device Number and the Register Number will be combined to create a Tag Address with a '!' as a separator. 

| **Site**   | **Area**  | **Cell** | **Unit**     | **Module**  | **Tag Address** |
| :--------- | :-------- | :------- | :----------- | :---------- | :-------------- |
| Headquater | 1st Floor | Room A   | Right Corner | temperature | 1!100           |
| Headquater | 1st Floor | Room A   | Right Corner | humidity    | 1!101           |
| Headquater | 1st Floor | Room A   | Left Corner  | temperature | 2!100           |
| Headquater | 1st Floor | Room A   | Left Corner  | humidity    | 2!101           |
| Headquater | 1st Floor | Room B   | Right Corner | temperature | 3!100           |
| Headquater | 1st Floor | Room B   | Right Corner | humidity    | 3!101           |
| Headquater | 1st Floor | Room B   | Left Corner  | temperature | 4!100           |
| Headquater | 1st Floor | Room B   | Left Corner  | humidity    | 4!101           |

Each row represents an object mapped to the device tag address. The object’s name is the composition of the first 5 columns with ‘/' as a separator. For example, the object’s name on the first row is something like HQ/1F/A/Right/temp. This name will be a unique topic for Unified Namespace.

# Object Data Modeling

Data modeling is like creating a blueprint before building a house. It involves defining the structure and relationships within your data. A well-designed data model not only ensures data consistency but also improves data understanding and usability. In this series, we provide a step-by-step guide to organizing this data within the [Unified Namespace](https://www.emqx.com/en/blog/unified-namespace-next-generation-data-fabric-for-iiot) using [EMQX](https://www.emqx.com/en/products/emqx) and [Neuron](https://www.emqx.com/en/products/neuron) as foundational components.

<section class="promotion">
    <div>
        Try Neuron for Free
             <div class="is-size-14 is-text-normal has-text-weight-normal">The Industrial IoT connectivity server</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>

Consider another example: suppose we have three chemical tanks that require temperature control at specific levels with minimal power consumption for metal surface finishing. Two primary data are needed in this scenario: the temperature of each tank and the energy consumption of the tank heater.

![Object Data Modeling](https://assets.emqx.com/images/d7a1e3f1568eabfeed46057964104cf3.png)

A temperature controller or reader can simultaneously read the temperatures in all three tanks and report these readings to Neuron with three temperature values every second. However, three power meters operate independently and send data to Neuron individually. In this presentation, there is no apparent connection between the chemical tanks and this data. From a human perspective, the chemical tank is the primary object of interest. Temperature and energy usage serve as attributes for this object, which are used to control the heater. Suppose we continue to use the Modbus TCP protocol to connect these devices. The Modbus device IDs for the three power meters are 1, 2, and 3, and the Modbus device ID for the temperature reader is 4. The data tag address for the power meters is 100, while the data tag addresses for the three temperatures in the temperature reader are 200, 201, and 202.

This example will serve as a reference throughout the subsequent steps, from data mapping to data contextualization.

## Data Mapping

Data mapping is the process of creating a connection between two different device data models and object data models in order to facilitate data integration, transformation, or migration. It involves identifying how data tags in the source device dataset correspond to or should be transformed into data fields or attributes in the target object dataset. This involves specifying which fields map directly, which may require transformation, and which might be omitted. Data mapping also includes defining rules or transformations that need to be applied to the source device data to align it with the target object data. This can involve data type conversions, calculations, or data enrichment.

Back to our example. In order to control the temperature of the chemical tanks, an I/O relay device will be added to the Modbus network with Device ID 5.

![Data Mapping](https://assets.emqx.com/images/6c6d892435766051704ef3c240cc4168.png)

There are two different ways to present the data model. The first is to obtain data directly from the Modbus network in a device-organized manner. This method of data organization is dependent on the physical device and its wiring connections. The second presentation method is for human understanding and requires reorganizing the data structures into a format that humans can understand. Neuron's job is to restructure these data tags into an object model. Within Neuron, users have the flexibility to create objects that encapsulate different data tags from different devices. In the context of this example, three objects have been created: Tank, Heater, and Energy Meter. 

Data mapping is crucial in various data-related processes, including data integration, data migration, data warehousing, and ETL (Extract, Transform, Load) processes. It ensures that data is correctly transferred and transformed from one system to another, maintaining data integrity and consistency across different datasets and systems.

## Data Normalization

Data is diverse, often arriving in multiple formats with problems such as clutter, redundancy, and inconsistency. Data normalization serves as a remedy for such data challenges. It's the process of structuring data to reduce redundancy and promote consistency, effectively cleansing the data for better quality.

In our example, we have three Power Meters from different brands and manufacturers, each with its unique characteristics and attributes. The first Power Meter offers the power consumption in a floating-point decimal value, measured in kWh. The second one, however, provides power consumption in a fixed-point decimal format. The last Power Meter delivers Voltage and Ampere values, requiring separate calculations to derive kWh consumption. Data Normalization is crucial for maintaining data consistency across the entire production process. Thanks to Neuron's processing capabilities, it can seamlessly transform these disparate data formats and perform the necessary calculations.

However, Data normalization can be described as the method used to improve the organization of data, eliminating any unstructured or repetitive data to establish a more rational and cleaner storage approach.

The core objective of data normalization is to establish a standardized data format across the system, ensuring that data can be easily queried and analyzed for better decision making.

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
    <a href="https://www.emqx.com/en/resources/open-manufacturing-hub-a-reference-architecture-for-industrial-iot?utm_campaign=embedded-open-manufacturing-hub&from=blog-practical-data-management-for-smart-manufacturing" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

### First Normal Form (1NF)

1NF, the initial level of data normalization, addresses the issue of repeating entries within a group. In this form, each entry should contain only a single value for each cell, and each record must be distinct.

### Second Normal Form (2NF)

To reach the 2NF stage, data must initially meet all the requirements of 1NF. Additionally, data should have a sole primary key. Achieving this involves placing subsets of data that can be distributed into multiple rows into separate tables. New foreign key labels can then establish relationships between them.

### Third Normal Form (3NF)

Data complying with 3NF requirements must first adhere to all the prerequisites of 2NF. Beyond that, data within a table should exclusively depend on the primary key. In case the primary key undergoes alterations, all affected data must be transferred to a new table.

![normalization process](https://assets.emqx.com/images/f026eaa996430d8ea806372a2820e1bb.png)

Following the normalization process described above in our example, the need for temperature objects and energy objects within our data source list can be eliminated.

## Data Contextualization

Data without context is like a jigsaw puzzle with missing pieces. Data contextualization is the process of adding meaning and relevance to data by placing it within a specific context. It transforms raw data into actionable information. This is how Unified Namespace serves the data analysis by adding context information.

Unified Namespace serves as the glue that connects data to its context. By defining a standardized structure, it enables data architects to associate data with its relevant context, such as time, location, or business process. Contextualized data becomes more valuable as it provides insights that are tailored to specific scenarios or questions. It bridges the gap between data and decision-making, empowering organizations to extract actionable intelligence from their data.

![Data Contextualization](https://assets.emqx.com/images/9a3d4e243caa69c4934b474a33dc5054.png)

In our example, temperature high and low limitations should be added to the context, and alert messages for each tank can help understand the status of the chemical processing in the tank. These limitations can be found in the product recipe within the MES system. Moreover, the material being immersed in the tank is also important for the production process. This information can be retrieved from the Sales Order in the ERP system. Finally, the object details will be as follows.

# Conclusion

In the realm of predictive analysis, encompassing Unified Namespace concepts is not a mere prerequisite. It's the key to success. Effective data collection, integration, quality assurance, governance, and accessibility, along with data modeling, normalization, and contextualization, with [Neuron](https://www.emqx.com/en/products/neuron) and [EMQX](https://www.emqx.com/en/products/emqx), are the building blocks upon which accurate predictive models are constructed. As the data-driven revolution continues to unfold, focusing on Unified Namespace concepts and object data modeling remains the compass that guides organizations toward actionable insights and sustainable growth. 





<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
