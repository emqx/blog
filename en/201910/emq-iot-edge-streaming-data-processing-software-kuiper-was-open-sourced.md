The world's leading open source IoT software provider [EMQ](https://www.emqx.com/en)  ([Github Project](https://github.com/emqx/emqx) ) officially open-sourced a lightweight streaming data processing project [EMQX Kuiper](https://github.com/emqx/kuiper) (hereafter referred to as Kuiper)  on October 23, 2019 . With the release of Kuiper, EMQ will accelerate the arrangement of the IoT middleware domain, so as to form a full coverage of IoT middleware software from messaging to data processing, from edge to cloud.

## New Demand for IoT Edge Computing

In 2019, as the first year of 5G commercial use, with the deepening of 5G deployment, edge computing has become increasingly popular. Edge computing increases computing power with the computer room close to the access network, so as to:

- Significantly reduce business processing delays
- Reduce bandwidth pressure on the network and reduce transmission costs
- Reduce data storage costs in the cloud
- Improve content distribution efficiency and user experience

A large part of the IoT edge computing refers to the processing of streaming data, which is a set of sequential, massive, fast and continuous data series. Generally, streaming data can be regarded as a dynamic data set that grows infinitely over time.  Streaming data processing helps users understand the status of system devices in real time and respond quickly to abnormal situations. The computing resources (CPU, memory, etc.) at the edge are not as rich as in the cloud. Therefore, for the traditional streaming data processing framework such as Apache Storm or Apache Flink, because of its large installation package, complex deployment structure and process, and high runtime consumption, it is not suitable for the resource constrained edge devices (IPCs, gateways, or devices with low-profile X86 servers) with limited resources. Kuiper open-sourced by EMQ is to solve these problems on the IoT edge devices.

## Kuiper User Scenarios

Kuiper can be applied all kinds of edge computing user scenarios, the typical sample scenarios including,

- Industrial server of factory: Analyze data coming from factory product line, and publish the analysis data to cloud. The real-time product-line status can be monitor through by system deployed at local factory or remote sites.
- Gateway of Connected Vehicle: Analyze data of vehicle CAN bus, and save the valuable analyzed result data to remote cloud or local storage. The real-time status can be accessed through local vehicle system or remote mobile application.
- Smart-home gateway: By analyzing different kinds of data collected from smart-home, the important result could be displayed at home facilities, or send to user's mobile application through cloud. 

The previous scenarios describe the value of edge computing: local data processing improves user experience; local data processing also improves data security, and protects personal privacy; Save the costs of bandwidth and cloud storage. Kuiper can be run at those resource constrained devices, and realized the streaming processing with low cost.

## Kuiper Features

- Lightweight: The installation package is about 7MB; it does not depend on third-party libraries and runtimes, and can be run after download and decompression. It is very convenient for installation and use.
- Cross- operating system: Currently is available on Linux and Mac, and will support Windows in the future
- Easy to use and quickly respond to agile business changes: Users can write SQL to achieve business processing; if the business changes, simply update the relevant SQL statements without complex application development and deployment
- Built-in support for MQTT message processing: As a de facto protocol standard in the IoT field, Kuiper has built-in MQTT server such as EMQ to achieve seamless connection of IoT message processing.
- Extensibility: Kuiper defines an extension interface which can be extended to realize different message source processing and data sink after processing in the future. 
- Manageability: Kuiper defines a management interface that can be used to define and manage these business rules through the REST API in the future.

## Overview of Kuiper Component 

As shown in the following figure, Kuiper Server consists of three parts:

- Engines: This part is the core processing engine. The main functions include SQL parsing, SQL runtime and streaming data processing framework.
- RPC interface: The RPC interface is mainly used for interaction with client command line tools, including streaming definition and management, rule definition and management, query tools, etc.
- Rest API interface: The Rest API is mainly used for future management interfaces and interactions in the planned management interface, including streaming definition and management, rule definition and management, query tools, etc.

![components.jpg](https://assets.emqx.com/images/0683da520685cd30efd34595da22f4a4.jpg)


## Overview of Kuiper Usage Steps

Kuiper's usage process is similar to traditional streaming tools, mainly including three steps: streaming definition, rule definition and submit rule.

1. Streaming definition: This step is mainly used to define the data format of the data source, similar to the process of defining the table structure in the traditional relational database.  A data streaming named demo is defined as follows:

   ```shell
   # bin/cli create stream demo '(temperature float, humidity bigint) WITH (FORMAT="JSON", DATASOURCE="demo")'
   ```

2. Rule definition: this step is mainly used to define the following three parts

   - Data Source: This section specifies where the data being processed comes from, specified in the FROM statement of SQL, which is the name of the streaming defined in the previous step.
   - Data Business Process: This section has developed how to process data, which is achieved mainly through SQL statements SELECT, JOIN, GROUP, WINDOW, and various functions.
   - Data Sink: This section specifies that processed data is deposited to the corresponding target after the data processing is completed. It currently supports data sinking to log and MQTT servers

   ```sql
   {
       "sql": "SELECT * from demo where temperature > 30",
       "actions": [{
           "log":  {}
       }]
   }
   ```

   As shown above, a rule is defined to extract data with a temperature greater than 30 from the streaming named demo, and output the data satisfying the condition to the log file. Rules can be saved in a text file, such as `myRule`

3. Submit rule

   ```shell
   # bin/cli create rule ruleDemo -f myRule
   ```

   Once the rule is completed, it can be committed by creating a rule command. The data that satisfies the conditions will be output to the log file.

   ```
   ...
   [{"humidity":17,"temperature":60}]
   [{"humidity":59,"temperature":68}]
   [{"humidity":67,"temperature":31}]
   [{"humidity":5,"temperature":45}]
   [{"humidity":34,"temperature":97}]
   [{"humidity":90,"temperature":73}]
   [{"humidity":72,"temperature":59}]
   [{"humidity":39,"temperature":72}]
   [{"humidity":76,"temperature":92}]
   [{"humidity":23,"temperature":40}]
   [{"humidity":74,"temperature":91}]
   [{"humidity":50,"temperature":76}]
   [{"humidity":77,"temperature":44}]
   ...
   ```



## Start Using

Readers can complete Kuiper's first experience by following the [Tutorial Documentation](https://github.com/emqx/kuiper/blob/master/docs/getting_started.md) on Github. The Kuiper project is based on the Apache 2.0 open source license and any problems found in the use process can be directly submitted in the project.

------

Welcome to our open source project [github.com/emqx/emqx](https://github.com/emqx/emqx). Please visit the [official documentation](https://docs.emqx.io) for details.
