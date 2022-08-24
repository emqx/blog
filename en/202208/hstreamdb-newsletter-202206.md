In June, the HStreamDB team focused on developing the upcoming v0.9, including switching HServer to a decentralized cluster model, an HStream IO Embedded Runtime and CDC Source Connector. Aside from the core features, HStreamDB now supports Grafana integration and has an officially released Python client. Through the collaboration with the EMQX team, HStreamDB can now be integrated with EMQX.

## New Cluster Model for HServer 

With the primary goal of supporting larger clusters and better scalability while reducing dependencies on external systems, we have made the preliminary switch of the HServer cluster model from centralized ZooKeeper-based to decentralized SWIM[^1] based. Further tests and refinements will be performed for the new clustering mechanism. This feature will be ready with the official release of v0.9.

## HStream IO and new CDC source

HStream IO is an internal data integration framework for HStreamDB v0.9, composed of source connectors, sink connectors and IO runtime. It allows interconnection with various external systems, facilitating the efficient flow of data across the enterprise data stack and thereby unleashing the value of real-time-ness. 

This month, the implementation of the embedded IO runtime and CDC source connector for various databases, including MySQL, PostgreSQL, and SQL Server, has been completed, allowing efficient incremental and real-time data synchronization from these databases to HStreamDB.

## Grafana integration support

To facilitate the users' operation and management of the HStreamDB cluster, we now support monitoring integration based on Prometheus and Grafana, the mainstream solution in the industry. Metrics collected by HStream Metrics will be stored in Prometheus by the exporter and shown by the Grafana board. The results achieved to date is presented in the figure below.

For more information about monitoring, please refer to the documentation: [https://hstream.io/docs/en/latest/monitoring/grafana.html](https://hstream.io/docs/en/latest/monitoring/grafana.html) 

![grafana](https://assets.emqx.com/images/22fadfe3e7f7541be5c72e52d8e6c183.png)

## Release of Python client 

hstreamdb-py v0.1.0, the Python client for HStreamDB, was officially released, which supports basic operations to HStreamDB v0.8, including batch writing, consumption via subscription and resource management.

The installation instructions can be found at [https://pypi.org/project/hstreamdb/](https://pypi.org/project/hstreamdb/). For more detailed documentation, please refer to [https://hstreamdb.github.io/hstreamdb-py/](https://hstreamdb.github.io/hstreamdb-py/) 

## Integration with EMQX

[EMQX](https://www.emqx.io/) is the world's leading open-source MQTT broker developed by EMQ, which is widely used in the field of IoT. This month, in collaboration with the EMQX R&D team, we have completed an efficient integration of EMQX with HStreamDB. The integration will enable users to utilize and achieve one-stop connection, data access, persistent storage and real-time analytics for IoT devices.

[^1]: Das, A., Gupta, I. and Motivala, A., 2002, June. Swim: Scalable weakly-consistent infection-style process group membership protocol. In *Proceedings International Conference on Dependable Systems and Networks* (pp. 303-312). IEEE.
