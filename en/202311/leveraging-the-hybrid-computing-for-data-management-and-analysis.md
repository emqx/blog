In our [previous blog](https://www.emqx.com/en/blog/practical-data-management-for-smart-manufacturing), we began a comprehensive exploration of data management processes in smart manufacturing, covering critical stages such as data collection, data mapping, data normalization, and data contextualization. We built a strong foundation, clarifying the 'what' in data management for this dynamic field. In this installment, we focus on the equally important 'how' and 'where' aspects of these processes.

In the dynamic landscape of data management, the divide between Edge Computing and Cloud Computing has been a defining characteristic. Edge computing brings real-time processing closer to the data source, while Cloud computing, with its immense computational power, facilitates advanced data analysis. Now, imagine a world where you don't have to choose between these two powerhouses but instead harness their collective strength. Welcome to the realm of Hybrid Computing.

This article delves into the transformative potential of a hybrid computing model, one that skillfully marries the capabilities of Edge and Cloud computing, offering a comprehensive approach to data management and analysis. We'll journey through a practical example featuring [EMQX](https://www.emqx.com/en/products/emqx), [Neuron](https://www.emqx.com/en/products/neuron), and [eKuiper](https://ekuiper.org/), to demonstrate how this synergy optimizes data utilization in the context of Edge and Cloud computing.

## The Hybrid Model for ETL

To illustrate the power of this hybrid model, let's continue our example with EMQX and Neuron. This time, an edge streaming process engine, eKuiper, will join the solution stack to provide edge processing capabilities. On the cloud side, all clean data is published to the EMQX broker for binding as a unified namespace. Applications such as Kafka can subscribe to the relevant topics for stream processing. Together, these components demonstrate the harmonious interaction between edge and cloud computing. From real-time data collection to cloud-based analytics, this real-world use case demonstrates the potential of our approach.

![The Hybrid Model for ETL](https://assets.emqx.com/images/1ef593d2826de97868e707086d0053a6.png)

As described in the last blog, [Neuron](https://www.emqx.com/en/products/neuron) is a master device that connects to these slave devices, including 3 power meters and a temperature reader. Each slave device has a device ID to identify the data source. Neuron would poll these slave devices one by one to get the current readings. Neuron is the first place to perform the data mappings between the Modbus slave device readings and our favorite real-world model objects, chemical tanks. Neuron extracts the data from various data sources.

The chemical object data is then sent to [eKuiper](https://ekuiper.org/) for data cleansing and transformation. eKuiper can manage different data sources and access the production data from MES and ERP through the APIs or some other communication protocols. eKuiper performs the normalization on the chemical tank object data from Neuron and adds context data to the chemical tanks. This is the data transformation process.

The contextualized data is published to [EMQX](https://www.emqx.com/en/products/emqx) broker via [MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) communication protocol. EMQX will act as a central data repository to collect all data from different locations. All chemical tank object data will be organized in the ISA95 standard hierarchy structure. This is a data loading process. 

This is a complete picture of Data Warehousing where Extract, Transform, and Load (ETL) is the process of combining data from multiple sources into one large central repository. EMQX, Neuron, and eKuiper come together to realize the unified namespace capability for third party application software such as Kafka.

EMQX has a rules engine that can ingest the chemical object data into the Kafka streaming platform. Three chemical tank data streams are stored in Kafka corresponding topics for data analysis, including machine learning, deep learning or even more complex computational modeling.

In summary, the convergence of Edge and Cloud Computing in a hybrid model, powered by EMQX, Neuron, and eKuiper, represents a powerful solution for comprehensive data management. It offers the best of both worlds, enabling real-time insights and immediate action, while leveraging advanced analytics and scalable storage for a well-rounded approach to data management. In a data-driven world, this synergy becomes a game-changer, driving smarter decisions and improved operational efficiencies.

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
      A Reference Architecture for Smart Manufacturing
    </div>
    <div class="mb-32">
      Building an efficient and scalable IIoT infrastructure.
    </div>
    <a href="https://www.emqx.com/en/resources/open-manufacturing-hub-a-reference-architecture-for-industrial-iot?utm_campaign=embedded-open-manufacturing-hub&from=blog-leveraging-the-hybrid-computing-for-data-management-and-analysis" class="button is-gradient">Get the Whitepaper →</a>
  </div>
</section>

## The Hybrid Advantage

Each computing model has its own benefits. Edge computing can help with data management, while cloud computing can help with data analysis. However, the synergy benefits are realized when these two models seamlessly converge, especially in the realm of smart manufacturing.

### Benefits from Edge Computing

1. **Low Latency**: Edge computing processes data locally, near the source of data generation. This significantly reduces the latency in data processing compared to sending data to a remote cloud server. In smart manufacturing, low latency is crucial for real-time decision-making and control of machinery and processes.
2. **Real-time Data Processing**: Edge devices can process data in real time, enabling immediate responses to changing conditions on the factory floor. This is essential for quality control, predictive maintenance, and process optimization in manufacturing.
3. **Bandwidth Efficiency**: By processing data at the edge, only relevant information is sent to the cloud, reducing the amount of data that needs to be transmitted over the network. This is particularly beneficial in cases where network bandwidth is limited or expensive.
4. **Improved Security**: Edge computing can enhance data security by keeping sensitive data within the manufacturing facility, reducing the risk of data breaches and unauthorized access. With edge computing, you have more control over your data's physical location and access.
5. **Redundancy and Resilience**: Edge computing can provide redundancy and failover capabilities. Even if one edge device fails, the manufacturing process can continue with minimal disruption. In contrast, cloud data centers can be vulnerable to outages.
6. **Cost Savings**: Edge computing can help reduce the cost of data transfer and storage in the cloud, as only valuable data is sent to the cloud for long-term storage and analysis. This can lead to cost savings over time.

### Benefits from Cloud Computing

Cloud computing also offers several benefits over edge computing for data analysis in smart manufacturing.

1. **Data Centralization**: Centralizing data in the cloud allows for data from multiple manufacturing facilities to be stored, processed, and analyzed in one location. This can facilitate better cross-facility coordination, benchmarking, and global insights.
2. **Advanced Analytics**: Cloud computing platforms offer powerful analytics and machine learning tools that can process and analyze data at scale. This enables manufacturers to gain deeper insights, perform predictive maintenance, and optimize production processes more effectively.
3. **Collaboration and Remote Access**: Cloud-based systems allow for collaboration and remote access to data and analysis tools, which can be particularly valuable when experts or stakeholders need to access and collaborate on manufacturing data from various locations.
4. **Accessibility to Advanced Technologies**: Cloud providers invest heavily in research and development, making it easier for manufacturers to access and leverage cutting-edge technologies, such as AI, IoT, and big data analytics.
5. **Integration with Third-Party Services**: Cloud services can easily integrate with third-party tools and services, expanding the range of available solutions for manufacturers, including external data sources and industry-specific software.
6. **Global Data Processing and Insights**: Cloud computing allows manufacturers to process and analyze data from multiple global locations simultaneously, providing a holistic view of operations and supply chains.

## Conclusion

It's important to note that a hybrid approach is often the most practical solution for smart manufacturing. In a hybrid setup, edge devices handle real-time data collection and processing, while the cloud is used for long-term data storage, advanced analytics, and global coordination. This approach combines the benefits of both edge and cloud computing to optimize manufacturing operations. The choice between edge and cloud computing should be based on the specific needs and constraints of a given manufacturing environment.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
