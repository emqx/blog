This May, the HStreamDB team has officially released v0.8 and started the development of v0.9, which will bring significant improvements in clustering, external system integration, partitioning, and more. The design and initial implementation of the new clustering mechanism and data integration framework, HStream IO, has been completed, and we have also started the development of the new Python client. Version 0.1 of the Erlang client was officially released. As for ease of operation and maintenance, HStreamDB now supports deployment with Helm.

## HServer clustering improvements

In v0.8 and earlier versions, the HServer cluster applied a centralized clustering mechanism based on ZooKeeper, which requires registration for the discovery of HServer nodes, and coordination of nodes to rely on ZooKeeper instead of direct communication between HServers. Though the clustering scheme is in use by many distributed systems and is relatively mature, the main drawback is the dependencies on external systems, such as ZooKeeper, which has led to a lack of flexibility and scalability.

To support larger clusters, provide better scalability, and reduce the dependency on external systems, v0.9 will adopt a decentralized clustering mechanism. The new clustering scheme is mainly based on the SWIM [1] paper, which introduces its core algorithms, including efficient failure detection and a gossip-style message propagation mechanism. You can find applications of similar methods in distributed systems such as Consul and Cassandra. New clustering-related features are still under development and will be officially released in v0.9.

## New data integration framework HStream IO

**In addition to the focus on streamlining and reshaping the real-time data stack, HSteamDB is on a mission to catalyze the shift to a modern and real-time data stack for enterprises with the facilitation of efficient data flow throughout the data stack.** It is usually the case that multiple data systems or platforms are in use within one enterprise. These systems include but are not limited to online transactions, offline analysis, caching, search, batch, real-time processing, and data lake. **Therefore, to meet various business needs, the abilities of seamless interfacing and integration with multiple external systems are also crucial for HStreamDB.**

HStream IO is the internal data integration framework of HStreamDB, which includes components such as source connectors, sink connectors and IO Runtime. It can import data from external systems to HStreamDB through source connectors or export data in HStreamDB to external systems through sink connectors. Another noteworthy thing is that the HStream IO implementation will be based on the Airbyte spec, which means that numerous open-source connectors from the Airbyte community can be reused to integrate HStreamDB with any applicable system instantly. This May, we have accomplished the design and pre-development of HStream IO, which will be released in v0.9.

## Updates on clients

### New Python client

Development of the Python client has been initiated for HStreamDB, hstreamdb-py, which supports Python 3.7 and above. This will be officially released next month.

### hstreamdb-erlang v0.1 released

The Erlang client of HStreamDB, hstreamdb-erlang, was officially released in v0.1. For details, please refer to: [https://github.com/hstreamdb/hstreamdb-erlang/blob/main/README.md](https://github.com/hstreamdb/hstreamdb-erlang/blob/main/README.md) 

## Deployment method update

### Add support for helm-based deployment

Helm [https://helm.sh/](https://helm.sh/) is a tool which can help users easily install and manage K8s applications. HStreamDB now provides Helm-based deployment support. Please refer to the documentation for details: [https://hstream.io/docs/en/latest/deployment/deploy-helm.html#building-your-kubernetes-cluster](https://hstream.io/docs/en/latest/deployment/deploy-helm.html#building-your-kubernetes-cluster)
