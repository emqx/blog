LF Edge eKuiper (hereinafter referred to as eKuiper) is a Go language implementation of the lightweight IoT edge analysis, streaming processing open source software project initiated by EMQ and donated to LF Edge Foundation. eKuiper can run in various IoT edge usage scenarios for real-time data analysis. By processing at the edge, eKuiper can improve system response speed and security, saving network bandwidth and storage costs.

This month, the eKuiper team is focusing on developing v1.4.0, aiming to release the version in early December officially. v1.4.0 is a major version, adding many new features to improve the runtime performance and development efficiency. Development is progressing well and the new features are almost complete. We will spend the next few weeks on testing, UI, and other finishing touches.

The following features are available in 1.4.0-beta.1 released at the end of last month, welcome to use and give your valuable comments.

## Rule Pipeline: Building Complex Businesses Logic with Flexibility

eKuiper uses SQL to define business logic, which lowers the threshold of development. Simple SQL statements can efficiently define business requirements such as filtering, aggregation, and data conversion in practical usage scenarios. However, for some complex scenarios, it is difficult to address by defining a single SQL statement; even if you can, the SQL statement itself is too complex and difficult to maintain.

Based on the new in-memory source and sink, rule pipeline can connect multiple SQL rules easily, efficiently, and flexibly. The readability and maintainability of SQL statements can be improved when implementing complex business scenarios. The rules are connected with in-memory topics similar to the [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) and support wildcard subscriptions, enabling exceptionally flexible and efficient rules pipeline. While improving business expressiveness, rule pipelining can also improve runtime performance in certain complex scenarios. For example, multiple rules need to process data that has been filtered by a certain condition. By extracting that filtering condition as a predecessor rule, you can make the filtering calculated only once, significantly reducing the computation in the case of many rules.

## Portable Plugin: Making Extensions Easier

The original version of eKuiper supported an extension scheme based on the Go native plug-in system, supporting individual extensions to source, sink and function (UDF). However, due to the limitations of the Go plugin system, writing and using plugins is not easy for users familiar with Go, let alone users of other languages. eKuiper has received a lot of feedback from users in the community about plugin development, operation and deployment, and various operational issues.

To balance development efficiency and runtime efficiency, v1.4.0 will add a new Portable plugin system to lower the threshold of plugin development. The new Portable plug-in is based on the nng protocol for inter-process communication and supports multiple languages, currently providing go and python SDKs, with more SDKs to be added in subsequent versions according to user requirements; simplifies the compilation/deployment process, and runs like a normal program written in various languages without additional restrictions. Due to the different operation mechanisms, Portable plugin crashes will not affect eKuiper itself.

Native plug-ins and Portable plug-ins can coexist. Users can choose the plug-in implementation or mix them according to their needs.

## Shared Connections: Source/Sink Multiplexed Connections

eKuiper provides a rich set of sources and sinks to access and send results to external systems. Many of these sources and sinks are input/output pairs of the same external system type. For example, [MQTT](https://www.emqx.com/en/mqtt-guide) and EdgeX both have corresponding source and sink, and in the new version, users can do all connection-related configurations in the connection.yaml file; in the source/sink configuration, you can specify which connections to use without repeating the configuration. Shared connection instances reduce the additional consumption of multiple connections. In some scenarios, users may be limited in the number of connections and ports to external systems, and using shared connections can meet this limit. Also, based on shared connections, eKuiper can support connections to the EdgeX secure data bus.

## Other enhancements

- Support for configuration via environment variables
- By default, eKuiper uses SQLite, an embedded database, to store metadata such as streams and rules, allowing for no external dependencies at runtime. In the new version, users can choose Redis as the metadata storage solution
- Rule status return error reason
- Optimized SQL Runtime

## Upcoming features

- sink dynamic parameter support, e.g., MQTT sink can set the topic to a field value in the result so that the data received can be sent to a dynamic topic
- Authentication support: user-configurable JWT-based authentication for REST API
- UI adaptation
