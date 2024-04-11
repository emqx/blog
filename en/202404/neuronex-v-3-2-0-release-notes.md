The Industrial Edge Data Hub, NeuronEX version 3.2.0 is now officially released! The latest version provides users with new features and enhancements to improve data collection, analysis, and management capabilities.

Download the latest version: [https://www.emqx.com/en/try?product=neuronex](https://www.emqx.com/en/try?product=neuronex) 

## Data Collection Driver Update

### New Southbound Driver

- **MTConnect**: Added MTConnect southbound driver to support access to devices with MTConnect Agent installed through HTTP protocol. [MTConnect | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/mtconnect/mtconnect.html)
- **Siemens MPI**: Added Siemens MPI southbound driver to support data exchange with Siemens devices through the MPI communication protocol. [Siemens MPI | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/siemens-mpi/mpi.html)
- **HEIDENHAIN CNC**: The new HEIDENHAIN CNC southbound driver can collect operating data of various series of HEIDENHAIN machine tools in real time. [HEIDENHAIN CNC | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/configuration/south-devices/heidenhain-cnc/heidenhain-cnc.html)

### Enhanced Driver Functionality

- **Driver Functionality Continuously Enhanced**: Expanded support for data types of drivers such as OPC UA, Siemens S7, Inovance Modbus TCP, and Focas, continuously optimizing driver read/write performance.
- **Import/Export of Southbound Driver Nodes**: Added import/export functionality for southbound driver nodes, supporting simultaneous import/export of multiple southbound driver configurations and data points, simplifying configuration management processes.
- **Southbound Driver Replication Functionality**: Enables the quick creation of driver nodes in the same type.
- **Streamlined Southbound Driver Creation Process**: Optimized the creation process for southbound drivers to provide a smoother experience.
- **Improved Driver Data Statistics Page**: Provides more detailed driver status information, facilitating driver operations and maintenance management.

![NeuronEX](https://assets.emqx.com/images/146acb1ef1bfefd359d091c6b1653679.png)

## Data Processing Update

- **External Service Integration**: NeuronEX now supports calling external algorithm services, allowing for sending various data source data to external services, returning calculation results and outputting them to Sink. (Please refer to the documentation for details: [extension | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/streaming-processing/extension.html)

  ![create external service](https://assets.emqx.com/images/a72ea6e89b43441ec3308cce6e93905d.png)

  <center>Create external service</center>

  ![Using external service in rule](https://assets.emqx.com/images/708d233faaf492600ab5778ab6ca4f65.png)

<center>Using external service in rule</center>

 

- Enhanced Rule Test: The rule test function allows users to view the results of the rule output after SQL processing in real-time. It also enables quick testing of SQL syntax, built-in functions, data templates, and other related features. In the latest version, we have improved the rule test function and made changes to the interface style to enhance its usability.

- Kafka Sink: A new Kafka Sink is added to support direct integration with Kafka to achieve efficient data stream processing.

  ![Kafka Sink](https://assets.emqx.com/images/260ccce8b12eaff8044a8f5c6300599b.png)

## User Interface Optimization

We have redesigned and optimized the user interface of NeuronEX 3.2.0 to further enhance the user experience. By adjusting the interface layout, optimizing color matching, and improving interactive elements, we have made the interface more intuitive and easier to operate. 

In addition, we have made adjustments to the layout and components of the page to ensure that information is presented more clearly. This series of interface improvements will bring users a smoother and more intuitive operating experience, allowing them to complete various tasks more easily and efficiently, and better control the collection, processing, analysis and management of industrial data.

## Other Improvements

- **Single Sign-on (SSO) Support**: Single sign-on (SSO) support has been added to simplify user authentication and access management. [System Configuration | NeuronEX Docs](https://docs.emqx.com/en/neuronex/latest/admin/sys-configuration.html)

## Summary

These enhancements and new features will further enhance user experience and make it easier to manage and analyze industrial data. To experience NeuronEX 3.2.0, please visit the website and [download the latest version](https://www.emqx.com/en/try?product=neuronex).



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
