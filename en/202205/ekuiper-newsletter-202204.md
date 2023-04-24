Earlier this month, eKuiper team released v1.4.4 to complete the last fixpack of the 1.4.x release cycle. And at the end of this month, we officially released[ v1.5.0,](https://github.com/lf-edge/ekuiper/releases/tag/1.5.0) including a bunch of feature updates. At the same time, the eKuiper Chinese and English[ community website](https://ekuiper.org/) has been officially launched, carrying the latest information of the eKuiper open source project and the redesigned Chinese and English documentation.

## v1.5.0 Features at a Glance

New features added this month include:

### Neuron Integration

Neuron ([https://github.com/emqx/neuron](https://github.com/emqx/neuron)) is an EMQ-initiated and open source Industrial Internet of Things (IIoT) edge industrial protocol gateway software for modern big data technologies to harness the power of Industry 4.0. It supports one-stop access to multiple industrial protocols and converts them to standard MQTT protocols to access the Industrial IoT platform. Integrate Neuron and eKuiper can ease IIoT edge data collection and computation.

Neruon version 2.0 will integrate seamlessly with eKuiper version 1.5.0, allowing users to access data collected in Neruon for computation in eKuiper without configuration, and to easily back-control Neuron from eKuiper. The integration of the two products can significantly reduce the deployment cost of edge computing solutions and simplify the threshold of use. The use of the NNG protocol for communication also significantly reduces network communication consumption and improves performance.

### Generic SQL source and sink plugin

In the process of upgrading old systems, we often need to consider the compatibility with the original system. A large number of old systems use traditional relational databases to store the collected data. In new systems, there may also be data stored in databases that do not provide easy streaming access but need to be calculated in real time. There are many more scenarios that require access to a large number of SQL-enabled databases or various external systems.

eKuiper provides a unified SQL pull source that pulls data from multiple types of SQL-enabled data sources at regular intervals and provides basic de-duplication capabilities to form streaming data for unified streaming computation processing. The pre-compiled version of the plugin supports access to common databases such as MySQL, PostgresSQL, etc.; at the same time, the plugin is equipped with connection capabilities for almost all common databases, and users only need to provide the parameters of the databases to be supported when compiling, so that they can compile their own plug-ins that support custom database types.

In addition to data pulling, we also provide generic SQL plug-ins for data writing. It is worth noting that eKuiper itself already provides dedicated plugins for temporal databases such as influxDB and TDengine. The generic SQL plug-in also supports connections to these databases, but provides insert functionality and does not support non-standard concepts for specific databases.

For more information and a list of supported databases, checkou out the [SQL source plug-in](https://ekuiper.org/docs/en/latest/guide/sources/plugin/sql.html) and [SQL sink plug-in](https://ekuiper.org/docs/en/latest/guide/sinks/plugin/sql.html) documentation.

### Other features review

New features from the previous two months of development releases have also been released in version 1.5.0, mainly including:

- Compile-on-demand: users can choose the functions they need to compile to suit the resource constraints of the deployment environment
- Change monitoring: provide a series of change detection-related functions to facilitate flexible implementation of common requirements such as de-duplication and change triggering
- Rule isolation: soft isolation of rule errors and load by runtime rules to improve overall service stability
- Select clause grouping: provide functions for grouping select results to facilitate dynamic processing by group for subsequent applications

## eKuiper community website is online now

The official eKuiper website [https://ekuiper.org](https://ekuiper.org) was launched this month. The site provides an introduction to the product, download information and links to the documentation blog. At the same time, we have refactored the documentation, added modules such as concept introduction and tutorials, and adjusted the navigation tree, hoping to help users find useful information more easily.
