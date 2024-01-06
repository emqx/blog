The lightweight data stream processing engine for IoT edge, eKuiper, has recently unveiled version 1.12!

This update improves integration and management capabilities for external systems, aiming to deliver an enhanced user experience. The highlights of new features include:

- **New Source/Sink Options:** Introduce additional source/sink choices, such as WebSocket, RedisPubSub, and Simulator, to expand the range of available data access methods.
- **Enhancements to Existing Source/Sink:** Optimize and strengthen existing source/sink options, including Kafka and InfluxDB v1 and v2.
- **HTTP Table & Service:** Enable HTTP Pull as a lookup table and use HTTP microservices as external services without predefined schemas. This enhances flexibility in combining data flow with HTTP computation services.
- **Configuration Improvements:** Facilitate extensive log configuration, incorporating options like syslog and file size-based rotation. Enable convenient saving of configurations to the database, making it easy to share and manage configurations across multiple nodes.
- **Rule Management APIs:** Introduce more APIs for rule management, including functionalities such as trial rules, rule SQL validation, and rule SQL Explain. 
- **Expanded pre-compiled package options:** Include a complete binary package with pre-installed source/sink plugins. Pre-compiled APK files are available for direct installation on Android systems, whether on smartphones or in-car devices.

Our community contributors from global have put in tremendous effort to make eKuiper 1.12 a reality, and we are deeply appreciative of their work.

## Flexible Adaptation for Data Sources and Targets

In edge computing, different situations and devices produce data in various ways, storing it in various databases or message queues. To handle this variety, eKuiper needs to work well with different systems and integrate data smoothly.

eKuiper 1.12 adapts better to various data sources and targets. It offers more source/sink options and improves existing sinks, especially for batch sending large-scale data. This is important for high-throughput data processing, where traditional serial IO operations may not be enough. This enhancement boosts performance and efficiency for users.

Working with different protocols and formats is hard for one team or organization. With the help of the open-source community, we can use contributions from various people to make adapters more versatile and useful. We welcome more users to join the community and help us support more data sources and targets.

### WebSocket Support

WebSocket is a protocol for two-way communication over one TCP connection. It lets clients and servers exchange data in real time. eKuiper 1.12 adds **WebSocket source and sink** for interacting with WebSocket connections.

eKuiper can use WebSocket connections in server or client mode. You can choose the mode by giving the remote host address in the rules. If you give the address, eKuiper will connect to the remote WebSocket server. If not, eKuiper will wait for remote clients to connect.

WebSocket also supports shared connection mode. You can declare a WebSocket connection in connection.yaml and use it across multiple rules. When multiple WebSocket sources share a connection, they receive the same messages, and similarly, when multiple WebSocket sinks share a connection, they send data to the same connection.

### Kafka Support

Apache Kafka is a distributed messaging system known for its high throughput, high availability, scalability, and persistence features. In this version, we've improved the Kafka sink, incorporating the following enhancements:

1. Introduce batch sending by configuring batchSize and lingerInterval to specify the batch size and time.
2. Enable configuration of Key and headers, along with support for templates.
3. Provide support for TLS connections.

This version also adds Kafka source, which gets events from Kafka. Leveraging Kafka's persistence capabilities, employing the Kafka source along with rule-based QoS configuration allows for automatic rollback. This ensures that no data is lost in the event of an unexpected failure.

### HTTP Schemeless External Service

Microservice architecture lets users have many services that do different tasks. These services can work separately and talk to each other through APIs. This makes applications simpler, more flexible, and easier to maintain and scale. HTTP is a common way for microservices to communicate.

eKuiper introduces the [External Function](https://ekuiper.org/docs/en/latest/extension/external/external_func.html) feature, allowing users to convert microservices into functions usable in rule SQL. Previously, users had to create schemas for these functions, which proved challenging for HTTP services. This version eliminates the need for schemas when using HTTP services. Users can simply declare an endpoint and employ one function to call any service beneath it. For more information, please refer to [Schemaless Service Definition](https://ekuiper.org/docs/en/latest/extension/external/external_func.html#schemaless-external-function) and [Schemaless External Function Usage](https://ekuiper.org/docs/en/latest/extension/external/external_func.html#schemaless-external-function-1).

### HTTP Lookup Table

The lookup table feature lets users combine real-time data streams with externally stored data, such as data from the database. This helps achieve functions such as data completion. In this version, we've added the HTTP lookup table, which lets users work with real-time data and data from HTTP services.

### Redis Pub/Sub Support

Redis Pub/Sub is a Redis feature for sending and receiving messages. The sender is the publisher and the receiver is the subscriber. The publisher sends messages to a channel, not to specific subscribers. All subscribers on that channel get the message.

eKuiper 1.12 improves Redis source/sink with RedisSub source and RedisPub sink. They are better for fast and large-scale message processing with Redis. Users can subscribe and publish to Redis channels.

### InfluxDB v1/v2 Sink Enhancements

InfluxDB is an open-source database for time-series data, widely used in IoT. With community help, eKuiper added Influx1 and Influx2 sinks before, to write data to InfluxDB v1 and v2. This version improves these sinks with more features and batch writing for faster and larger-scale data processing.

- Allows batch writing.
- Facilitates multiple tags, including dynamic tags based on data templates.
- Offers configuration for dynamic timestamps and time precision.
- Supports row mode (v2) and enables data formatting using data templates in row mode.

### Simulator Source

The simulator source provides a way to generate data for testing and demonstration, simulating data streams from devices or sensors. Utilizing this source allows users to quickly validate rule scenarios without connecting to an actual data source. To set up a simulator data source, employ the following statement, and then you can use and test it within rules.

```
CREATE STREAM mock_stream () WITH (TYPE="simulator")
```

## Configuration and Management

Edge computing commonly encompasses geographically dispersed devices and systems, introducing complexities in monitoring, management, and upgrades. The latest release introduces augmented configuration and management capabilities.

NeuronEX is an industrial edge gateway software that enables real-time access and intelligent analysis of industrial data. It integrates the stream processing and management capabilities of eKuiper 1.12 and provides a better user experience. You can try it out here: [NeuronEX](https://www.emqx.com/en/try?product=neuronex).

### Improved Log Settings

This version offers more options for log settings, such as:

- Setting log levels, which enables you to adjust the log level.
- Configuring syslog, including setting the remote address and tag of syslog.
- Setting rotation, which allows you to rotate logs based on file size as well as time.

For the full documentation of the settings, please see [Basic Configuration | eKuiper Documentation](https://ekuiper.org/docs/en/latest/configuration/global_configurations.html).

### New Management APIs

This version adds some management APIs:

- APIs associated with trial rules. They allow users to create and debug trial rules.
- Rule SQL Explain API.
- Close eKuiper API.

## Conclusion

Welcome to upgrade to eKuiper 1.12.0 and enjoy the enhanced features and performance. We value your feedback and strive to make eKuiper more reliable and efficient for your edge computing needs.



<section class="promotion">
    <div>
        Try eKuiper for Free
    </div>
    <a href="https://ekuiper.org/downloads" class="button is-gradient px-5">Get Started →</a>
</section>
