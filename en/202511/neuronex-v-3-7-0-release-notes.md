We are excited to announce the official release of EMQX Neuron(formerly NeuronEX) 3.7.0!

This release marks a new step forward in the breadth of industrial connectivity. The core highlight is the brand-new northbound **OPC UA Server** plugin. This feature complements EMQX Neuron's powerful MQTT capabilities, enabling it to expose large volumes of southbound device data to upstream SCADA, MES, or third-party clients via the OPC UA industry standard, meeting a wider range of integration requirements.

Furthermore, version 3.7.0 includes a series of significant enhancements in driver capabilities, dashboard visualization, and AI-powered operations, further improving the platform's usability and stability.

## Key Feature: New OPC UA Server Plugin

[OPC UA](https://www.emqx.com/en/blog/opc-ua-protocol) (OPC Unified Architecture) is a widely used data exchange standard in the industrial automation field. In version 3.7.0, EMQX Neuron can function as a full-featured OPC UA Server, helping you easily integrate data from connected southbound devices into your existing automation ecosystem.

**Core Functionality and Security** 

The new OPC UA Server allows external systems to subscribe to data changes, read real-time data tags, and send control commands.

We provide the necessary configuration and security options to ensure reliable connections. This includes flexible host and port settings, username/password authentication, and multiple security policies (like `Basic256Sha256`), along with comprehensive certificate management (server, CA, and client certificates) to support secure, encrypted, and mutually authenticated connections. The system also simplifies the trust management mechanism for client certificates.

**Clear Namespace and Data Mapping** 

To ensure a clear and understandable data structure, EMQX Neuron automatically maps southbound device tags to OPC UA nodes:

- **Structure:** Each southbound node corresponds to an OPC UA Object node, with its groups organized as sub-objects.
- **NodeId:** Follows the standard `ns=1;s=[Device Name].[Group Name].[Tag Name]` specification (where `ns=1` represents the EMQX Neuron namespace).
- **Data Types:** Data types in EMQX Neuron (such as `INT32`, `FLOAT`, `STRING`, etc.) are automatically mapped to their corresponding standard OPC UA data types.

![image.png](https://assets.emqx.com/images/c7d6b9789a12bc0375e3320577a125c3.png)

## Dashboard Functionality Upgrades

To provide more powerful edge data visualization capabilities, we have comprehensively upgraded the dashboard functionality in 3.7.0:

- **Import & Export:** Added dashboard import and export functionality. You can export the entire dashboard configuration (including all panels and queries) as a JSON file, making it easy to migrate, back up, and share between different instances.

- **New Chart Types:** To meet diverse monitoring needs, three new chart types have been added:

  - **Gauge:** Intuitively displays the instantaneous value of a single metric.
  - **Stat:** Shows the latest value of a single metric along with a simple trend.
  - **Pie:** Displays the proportion of data in different categories.

- **Table Merge Function:** It is now supported to add multiple SQL queries in a Table-type panel and merge the results for display in the same table, facilitating cross-data-source comparative analysis.

- **Use Case Example:**

  These new features work perfectly together:

  - Use the **Gauge** chart to monitor the **"Boiler Pressure (Bar)"** in real-time.
  - Use **Pie** charts to analyze the **"Line Status (%)"** and **"Product Quality Rate (%)"** at a glance.
  - The **Import/Export** feature allows you to easily reuse a well-configured "Production Line Monitoring Template" like this one in other projects.

![image.png](https://assets.emqx.com/images/0df207e8497c96d87c40a6429cf9822e.png)

## More Enhancements

Version 3.7.0 also includes the following important updates:

**Driver Enhancements**

- **Beckhoff ADS Driver:** Supports batch creation of data points by importing TPY files, greatly simplifying the configuration process.
- **CNC Driver:** Added the ability to import built-in tag tables, helping users quickly configure and start data collection from CNC devices.
- **SparkplugB Driver:** Supports both Tag and Alias data reporting formats.

**AI Operations and Usability Improvements**

- **AI Operations Assistant:** Added an AI Q&A assistant with a built-in operations knowledge base. It can provide professional guidance on configuration, usage, and troubleshooting through natural language interaction.

  ![image.png](https://assets.emqx.com/images/13ba3ba7c315ff4d2b417d6b15dfe176.png)

- **Log System Optimization:** Added a global log level configuration item for Neuron (defaulting to Notice). This reduces overall log output while retaining the ability to set independent log levels for individual drivers, facilitating fine-grained diagnostics.
- **Northbound Application Subscription:** Optimized the interaction for subscribing to southbound groups. Subscribed groups are now clearly marked, and duplicate subscriptions are prevented.
- **Multi-Source Data Access:** The Httppull Source now supports a status similar to the SQL Source; the MQTT Source now supports subscribing to multiple topics.
- **Other:** Optimized the display style of the system information page and upgraded the built-in Datalayers version to 2.3.11.

## Conclusion

The release of EMQX Neuron 3.7.0, especially the introduction of the OPC UA Server, further enhances its data integration capabilities as an industrial edge gateway. We invite you to download and try the new version now to experience more powerful and user-friendly industrial data connectivity.

**Download EMQX Neuron 3.7.0 now:** [https://www.emqx.com/en/try?tab=self-managed](https://www.emqx.com/en/try?tab=self-managed)

**For complete EMQX Neuron 3.7.0 features, please check the documentation:** [Product Overview | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/)



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
