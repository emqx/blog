We are excited to announce the official release of NeuronEX 3.6.0!

In previous versions, NeuronEX focused on real-time collection and edge stream processing of massive heterogeneous data from industrial sites. In the new 3.6.0 version, NeuronEX focuses on enabling users to **understand and use** this data directly at the edge. The "Data Insights" feature empowers every user to transform raw industrial data into profound insights that drive decision-making.

## Data Insights: Unleash the Potential of Your Industrial Data

Previously, data collected by NeuronEX had to be forwarded to the cloud or a centralized platform for analysis and visualization. Now, all of this can be done effortlessly at the edge. The new "Data Insights" feature provides a complete, closed-loop workflow from data storage and query analysis to visual monitoring, making data value readily accessible.

This module includes three core components:

### 1. Built-in Time-Series Database: Out-of-the-Box Data Foundation

NeuronEX 3.6.0 now comes with the Datalayers time-series database built in, eliminating the need for complex selection and configuration for edge data persistence.

- **One-click Enablement**: Easily enable or disable the Datalayers storage service in the system configuration and flexibly set the data retention period (TTL).
- **Automatic Initialization**: When the service is first started, NeuronEX automatically creates the necessary data tables for a true out-of-the-box experience.
- **Efficient Writing**: The new DataStorage northbound plugin uses the gRPC protocol to write collected tag data to Datalayers in batches and includes a caching mechanism to ensure system stability under high throughput.

### 2. AI-Powered Data Analysis: Making Everyone a Data Analyst

We have introduced a unified "Data Analysis" page, which is not just a SQL query tool but an intelligent interactive workbench.

- **Intuitive Data Browsing**: A tree-like directory clearly displays stored drivers, groups, and tags, with data types indicated, giving you an at-a-glance understanding of your data structure.

  ![image.png](https://assets.emqx.com/images/bdb9e44121eb69a7ad6e0c8657d1fb75.png)

- **Smart SQL Editor**: Features keyword suggestions and syntax highlighting to make SQL writing more efficient and accurate.

- **AI Data Analysis Assistant**: You can describe your query needs in natural language (e.g., "query the average temperature of motorA `tag=MotorA-current` for each hour over the past day"). The AI assistant will generate the precise SQL statement for you. It can also intelligently analyze errors and iterate to correct them if a SQL execution fails. This significantly lowers the barrier to data analysis, allowing OT engineers and business experts to easily extract value from data.

  ![image.png](https://assets.emqx.com/images/5f886e62ac2496a6c20c32748c1ac590.png)

### 3. Visualization Dashboards: Build Your Own Monitoring Center

Data needs to be seen to make an impact. The new "Dashboard" feature allows you to create data visualization boards through simple drag-and-drop and configuration.

- **Rich Chart Types**: Supports various chart types, including Line, Bar, Stat, and Table, to meet different data display needs.
- **Flexible Query Configuration**: Each panel can be bound to one or more SQL queries, and you can use aliases to distinguish between different data series.
- **Powerful Time Controls**: Supports global time range selection (e.g., last 1 hour, custom time range) and an auto-refresh mechanism to ensure you are always viewing the latest data.
- **Customizable Layout**: Drag and drop to adjust the position and size of panels, and use a grid system for alignment to easily create personalized views that fit your monitoring needs.

![image.png](https://assets.emqx.com/images/6b49486bded113594c08740da44fd658.png)

## Enhanced Integration and Workflow Automation: Node-RED Integration

To further enhance the flexibility and scalability of NeuronEX, version 3.6.0 integrates the low-code programming tool Node-RED by default in specific Docker images. Users can enable the service on demand and easily push data from NeuronEX to Node-RED via WebSocket, REST API, etc., leveraging its rich nodes and powerful flow orchestration capabilities to quickly build complex automation workflows and application logic.

![image.png](https://assets.emqx.com/images/5ec5e90278c52e554ea29c65856d9ea4.png)

## NeuronHUB: A Unified Solution for Data Collection on Windows

To address the challenge of specific industrial protocols (like OPCDA) that are heavily dependent on the Windows environment, version 3.6.0 officially introduces the new auxiliary software—**NeuronHUB**. As a major upgrade to the former NeuOPC, NeuronHUB aims to provide a unified data collection solution for the Windows platform.

- **Unified Collection Entry**: NeuronHUB integrates multiple drivers that require collection and conversion on the Windows platform, including OPCDA, Syntec CNC, and Mitsubishi CNC. Users no longer need to deploy multiple separate components for different Windows-based protocols, achieving unified management.
- **Commercial-Grade Feature Support**: For the widely used OPCDA protocol, NeuronHUB introduces a license management mechanism, providing more standardized and reliable support for enterprise deployments.
- **Seamless Collaboration with NeuronEX**: As an official auxiliary tool for NeuronEX, NeuronHUB is designed to bridge legacy device data from the Windows environment to NeuronEX securely and efficiently, allowing users to leverage NeuronEX's powerful data processing, storage, and analysis capabilities.

## Continuous Improvements and Driver Enhancements

**Driver Enhancements:**

- The BACnet/IP driver now supports tag scanning.
- OPCUA, DNP3, and Siemens S7 drivers support link tracing for easier troubleshooting.
- The SparkplugB application now supports static tag configuration.

**Enhanced Data Processing Capabilities:**

- The data processing module adds Kafka Source and WebSocket Source, providing more options for data source integration.

**UI/UX Optimizations:**

- The south- and north-bound node list pages now support filtering and sorting by status. The northbound application subscription page supports keyword searches, improving configuration and management efficiency.

## Conclusion

We invite you to experience NeuronEX 3.6.0 and start your industrial data exploration journey. We look forward to your feedback and will continue to innovate to provide the most powerful edge data infrastructure for your digital transformation.

- Download NeuronEX 3.6.0 now: [https://www.emqx.com/en/try?tab=self-managed](https://www.emqx.com/en/try?tab=self-managed) 
- For the full list of features in NeuronEX 3.6.0, please check out the documentation: [NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/) 



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
