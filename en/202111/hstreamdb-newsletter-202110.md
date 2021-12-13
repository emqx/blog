[HStreamDB](https://hstream.io) is the first「stream-native database」specially designed for stream data by EMQ. It supports efficient storage and management of large-scale stream data and complex real-time analysis on dynamic data streams. HStreamDB aims to manage the whole life cycle of access, storage, processing, and distribution of large-scale data streams, suitable for data management and real-time analytics scenarios in IoT, Internet, finance, and relevant fields.

After the release of v0.5 at the end of July, the HStreamDB team has been focusing on developing the next version. This month, we have planned many new features for the v0.6 version in terms of ease of use and scalability of the HStream Server. This version is expected to be released next week.

## Add HServer cluster support

As a [cloud-native distributed stream database](https://hstream.io), HStreamDB has adopted a separate architecture for computing and storage from the beginning of design, to support the independent horizontal expansion of the computing layer and storage layer. In the previous version of HStreamDB, the storage layer HStore already has the ability to scale horizontally. In the upcoming v0.6 version, the computing layer HServer will also support the cluster mode so that the HServer node of the computing layer can be expanded according to the client request and the scale of the computing task.

HStreamDB's computing node HServer is designed to be stateless as a whole, so it is very suitable for rapid horizontal expansion. The HServer cluster mode of v0.6 mainly includes the following features:

- Automatic node health detection and failure recovery
- Scheduling and balancing client requests or computing tasks according to the node load conditions
- Support dynamic joining and exiting of nodes

## Add shared-subscription mode

In the previous version, one subscription only allowed one client to consume simultaneously, which limited the client's consumption capacity in the scenarios with a large amount of data. Therefore, in order to support the expansion of the client's consumption capacity, HStreamDB v0.6 adds a shared-subscription mode, which allows multiple clients to consume in parallel on one subscription.

All consumers included in the same subscription form a Consumer Group, and HServer will distribute data to multiple consumers in the consumer group through a round-robin manner. The consumer group members can be dynamically changed at any time, and the client can join or exit the current consumer group at any time.

HStreamDB currently supports the "at least once" consumption semantics. After the client consumes each data, it needs to reply to the ACK. If the Ack of a certain piece of data is not received within the timeout, HServer will automatically re-deliver the data to the available consumers.

Members in the same consumer group share the consumption progress. HStream will maintain the consumption progress according to the condition of the client's Ack. The client can resume consumption from the previous location at any time.

It should be noted that the order of data is not maintained in the [shared subscription](https://www.emqx.com/en/blog/introduction-to-mqtt5-protocol-shared-subscription) mode of v0.6. Subsequent shared subscriptions will support a key-based distribution mode, which can support the orderly delivery of data with the same key.

## Add statistical function

HStreamDB v0.6 also adds a basic data statistics function to support the statistics of key indicators such as stream write rate and consumption rate. Users can view the corresponding statistical indicators through HStream CLI, as shown in the figure below.

![HStream CLI 统计功能](https://static.emqx.net/images/d4dd69dd47f47163f028154245833913.png)

## Add REST API for data writing

HStreamDB v0.6 version adds the REST API for writing data to HStreamDB. Through this API and the webhook function of the open source EMQ X, the rapid integration of EMQ X and HStreamDB can be realized.

## HStreamDB Java SDK update

HStreamDB-Java is currently the mainly supported HStreamDB client (clients of more languages will be supported in the future), and users mainly use most of the functions of HStreamDB through this client.

The upcoming HStreamDB Java SDK v0.6 mainly includes the following features:

- Add support for HStreamDB cluster
- Add support for shared subscription
- Redesign some APIs
- Fix some known issues
