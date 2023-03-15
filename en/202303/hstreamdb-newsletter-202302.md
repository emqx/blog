Over the past two months, we have released versions 0.13 and 0.14 of HStreamDB, which include several bug fixes. Additionally, we have introduced a new component called HStream Console, which brings a user-friendly graphical interface for managing HStreamDB, making it easier for users to use and manage our database.

## HStream Console

HStream Console is a comprehensive web-based graphical user interface that empowers users to manage their HStreamDB cluster resources and workloads. It currently offers the following key features: 

- Stream management: create and delete streams, and view shards 
- Subscription management: support basic resource management operations. In addition, it supports managing associated consumer clients and viewing consumption progress.
- Records query: enabling users to query the records in a stream (shard) based on `recordID` and write records online.
- Metrics viewing: providing users with various charts for metrics related to streams and subscriptions from different time frames. The feature currently relies on Prometheus for the display. We have plans for future metrics data to be saved directly in HStreamDB.

We have exciting plans for the future, including:

- Managing streaming queries: including editing SQL, task submission, displaying results, and data visualization.
- Source and sink connectors: support multiple databases and IO Task creation and management.

## HStreamDB 0.14 Released

v0.14 mainly contains the following updates and bug fixes:

- HServer now uses the in-house Haskell GRPC framework by default
- Add deployment support for CentOS 7
- Add stats for failed record delivery in subscriptions
- Remove `pushQuery` RPC from the protocol
- Fix the issue causing client stalls when multiple clients consume the same subscription and one fails to acknowledge
- Fix possible memory leaks caused by STM
- Fix cluster bootstrap issue causing incorrect status display
- Fix the issue that allows duplicate consumer names on the same subscription
- Fix the issue that allows readers to be created on non-existent shards
- Fix the issue causing the system to stall with the io check command

## HStream Platform

HStream Platform is the next-generation one-stop streaming data platform built on HStreamDB. It aims to provide a truly friendly, unified, and modern product experience for developers to run and manage streaming data workloads.

Our HStream Platform Serverless version is currently in continuous internal testing on the public cloud, and we plan to release a free public beta version in the future. Additionally, we will offer on-premises deployment support. If you have any questions or are interested in early access and more product updates, please don't hesitate to contact us. To stay updated on our progress and be among the first to access the product, please visit [https://hstream.io/platform](https://hstream.io/platform).
