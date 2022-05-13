**HStreamDB is a [streaming database](https://www.emqx.com/en/products/hstreamdb) designed for streaming data, with complete lifecycle management for accessing, storing, processing, and distributing large-scale real-time data streams**. Standard SQL (and its streaming extensions) as the primary interface language, HStream is designed to simplify the management of data streams and the development of real-time applications by supporting efficient storage and management of large-scale data streams and complex real-time analysis on continuously changing data streams.

In the previous article, ["When Database Meets Stream Computing: The Birth of Stream Database"](https://www.emqx.com/en/blog/birth-of-streaming-database), we have introduced the concept of stream database. Using this as the basis for our product design concept, we developed HStreamDB,  and it's officially [open sourced earlier this year](https://www.emqx.com/en/blog/hstreamdb-is-now-officially-open-source).

Today, the EMQ HStreamDB team is pleased to announce the release of HStreamDB v0.5!


Download at: [https://github.com/hstreamdb/hstream](https://github.com/hstreamdb/hstream)


## Version Updates

In this 0.5 release, we have upgraded the existing features (e.g. management of data streams, writing and consumption of data). Also, we have provided many new features that are of great importance for developing applications via HStreamDB, such as the Java SDK, MySQL and Clickhouse Connector, and support for materialized views, etc.

### Provide support for materialized views

Provides materialized view functionality to support complex query and analysis operations on continuously updated data streams. The incremental calculation engine within HStreamDB updates the materialized view in real-time based on the changes in the data stream, allowing users to gain real-time data insight via simple SQL query.

### Provide a Java SDK to facilitate HStreamDB-based development

The recommended way to use HStreamDB, users can consult the documentation [https://docs.hstream.io/develop/java-sdk/installation/](https://docs.hstream.io/develop/java-sdk/installation/) to learn how to install and develop with Java.

### Provide Sink Connector

Two Sink Connectors are available, MySQL and Clickhouse, allowing users to easily specify which data to import into a particular database via SQL statements.

### Provide Dashboard

Users can manage the internal resources of HStreamDB through the Dashboard. 

![HStreamDB Dashboard](https://assets.emqx.com/images/89988ce1154311092d8bdefcb78752cc.png)

![HStreamDB Dashboard](https://assets.emqx.com/images/62d29d904cf35d3e245207bea2ff4156.png)

### Refactor server, implement server interface based on gRPC 

Redesigned HStream server based on gRPC, make the implementation and enhance the scalability of the server.

### Improve SQL-based stream data processing

We have added many new SQL functions and improved and optimized aggregation functions. Enhance the management of stream processing tasks.

### Optimize low-level storage implementation



## Development Plan

In subsequent releases, we will continue to work towards the following goals.

### Enhancing the scalability of HStream Server

- Implementation of HStream Server clustering support

- Support for consumer group for [shared subscriptions](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription) and parallel consumption 

- Optimization of control plane metadata storage

### Enhance operations and monitoring capabilities

- Support for deployment with k8s

- Implementation of a statistical monitoring framework

- Enrich Dashboard functionality

### Enhanced stream processing capabilities

- Optimize stream engine implementation to improve processing efficiency

- Add SQL optimizer to optimize execution plan generation

- Implement a stream task scheduling framework to support parallel processing

### Improved usability

- Improve Java SDK

- Improve user documentation, provide more tutorials and examples

- Provide more application examples

### Enrich the HStreamDB ecosystem and improve integration capabilities

- Refactor the Connector framework to facilitate developers to implement the Connector they need

- Implement hierarchical storage

- Implement more connectors to support other popular systems


We also plan to complete the integration with [EMQX](https://www.emqx.com/en/products/emqx) in the next phase, which will validate the HStreamDB functionality and present a solution tailored to IoT application development.


## Future outlook

HStreamDB, the pioneer of the streaming database, is steadily moving towards the milestone of being ready for use in production. We will continue to develop HStreamDB, improving its functionality, stability and reliability. We believe that not long users can use HStreamDB to implement real-time applications and obtain instant data insights quickly and straightforwardly. Also, we would like to thank our community members for every use and every contribution.
