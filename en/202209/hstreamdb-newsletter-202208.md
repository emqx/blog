Just after the official release of HStreamDB 0.9 at the beginning of the month, the HStreamDB team officially started the development cycle for v0.10. This month the last image has already introduced features such as end-to-end compression, CLI support for TLS, and fixes to several known issues. Apart from these updates in the main repo, a new Haskell gRPC framework and a fully-managed cloud-native streaming database service, HStream Cloud, are also under development.

## End-to-end compression

In previous versions of HStreamDB, data could only be compressed by the HServer before being sent to the HStore, but HStreamDB did not offer compression on the path from the client to the HServer.

This month we have introduced end-to-end compression, which means that data compression could be on the client side in batches as it is written, and the compressed data can be stored straight by the HStore. In addition, the client can automatically decompress the data when consumed, and the whole process is not perceptible to the user.

In high throughput scenarios, enabling end-to-end data compression can significantly alleviate network bandwidth bottlenecks and improve read and write performance, with a 4x+ throughput improvement in our benchmark, but at the cost of increased CPU consumption at the client.

Java Client v0.10.0-SNAPSHOT provides support for end-to-end compression. The usage is as:

```
BufferedProducer producer =
        client.newBufferedProducer()
            .stream(streamName)
            .compressionType(CompressionType.GZIP)
            .batchSetting(batchSetting)
            .flowControlSetting(flowControlSetting)
            .build();
```

## A new Haskell gRPC framework

The HServer uses gRPC to communicate with the client. The current Haskell gRPC framework we are using, gRPC-haskell, binds the gRPC C core lib via Haskell's FFI (Foreign Function Interface). To improve performance and stability, we are trying to develop a new Haskell gRPC server framework to replace it.

The new framework, inspired by hsthrift, will be based on the C++ gRPC server and require no changes to the current Haskell source code. The new framework is currently under development and testing and is expected to be released in v0.10.

## HStream CLI 

HStream CLI now support TLS, and users can check docs for usage.

In addition, the CLI brings the following new features and improvements.

- Support for multi-line SQL statement input
- New -e, --execute options for non-interactive execution of SQL statements
- Support keeping the history of entered commands
- Optimised error message prompting when executing SQL

## Other issue fixes and improvements

- Update the HStream Helm chart to support the deployment of v0.9
- Fix an issue where subscriptions could assign shards to consumers that have lapsed
- Fix a memory leak caused by the gossip module using withAsync
- Add existence check for dependent streams when creating a view
- Fix an issue where new nodes could fail when joining a cluster
- Improve seed-nodes reboot process
- Improve handling of address during cluster startup
- Optimise thread usage and scheduling for the gossip module

## HStream Cloud is coming soon

We are working on HStream Cloud - a Streaming-Database-as-a-Service service based on the public cloud platform. Stay tuned.
