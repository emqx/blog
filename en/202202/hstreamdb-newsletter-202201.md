In previous Newsletters, we have briefly introduced some of the new features under development or completed for [HStreamDB](https://hstream.io) v0.7. HStreamDB v0.7 is committed to improving the stability and availability of HServer clusters while introducing the new transparent partition and enhancing the user experience.

In January, we finalised the development and release of HStreamDB v0.7, including implementing transparent partition Stage1, improving the deletion logic for resources, and providing a new Admin CLI. We also upgraded the Java client with enhancements, new features and transparent partition support.

## Transparent partition

After verifying the prototype, we have implemented Stage 1 of transparent partition on the main project this month and will introduce the feature in the upcoming v0.7 release.

From the perspective of system realisation, partitioning is an effective means to solve single-point bottlenecks and improve the horizontal scalability of the system. However, from the users' perspective, exposing partitions destroys the upper layer's abstraction, increases the cost of usage, and requires users to solve complex problems, such as c partition rebalancing and data sequencing. Transparent partition achieves scalability and ensures the ordering of requirements without exposing additional complexity to users, significantly improving the user experience.

## Resource Management

Removing resources in a running system has always been a tricky problem. In resource management, it is necessary to ensure the availability and consistency of the system and conform to the user's intuition. Therefore, we designed a set of HStreamDB resource removal specifications to deal with the two core resources in HStreamDB, Stream and Subscription. We also specified two deletion operations, regular deletion and force deletion.

In HStreamDB, a subscription relies on a stream. Therefore, you need to ensure no active subscriptions on the stream when you delete a stream. Similarly, you need to ensure no active consumers on the subscription when deleting a subscription. For forced deletion, you need to operate through hadmin, and we will update more detailed documentation after the HStreamDB v0.7 release at the end of January.

## Admin CLI

To make it easier for users to operate, maintain and manage HStreamDB, we have added an Admin Tool. With the new admin tool, you can query and manage various resources in HStreamDB, including Stream, Subscription, Query, Connector and Server nodes in the cluster. Besides, you can view all the current Metrics. At the same time, we have migrated some of the maintenance and management capabilities in the original HStream SQL Shell to the new Admin Tool, and the SQL Shell will mainly focus on the interaction with HStreamDB. In short, the Admin Tool is suitable for HStreamDB operation and maintenance personnel, while HStreamDB users should mainly use the SQL Tool.

## Java Client

### New feature

- Add support for transparent sharding, a new feature of HStreamDB v0.7.
- Add BufferedProducer. For clarity, we split the original Producer into separate BufferedProducer and Producer, where BufferedProducer is mainly for high throughput scenarios and Producer is primarily for low latency scenarios, considering that users have different requirements for writing latency and throughput.
- Add two new flush modes for BufferedProducer. The original Producer only supports flush by the number of records in batch mode. The new BufferedProducer provides two new flush modes, size-triggered and time-triggered, and these three trigger conditions can work simultaneously to meet the user's needs more flexibly.

### Major improvements

- Fixed the bug that coroutine could be blocked
- Improved the retry condition after RPC failed
- Improved handling of exceptions in Consumer

## Integration test

The previous integration test cases have been sorted out and refactored. More test cases on the correct path and some error-injection tests have been added. We can inject errors by randomly killing nodes during the test to detect the correctness and stability of system implementation. While running tests, we also fixed the problems found, such as the improvement of the client mentioned above.

The current integration test is also published on [Github](https://github.com/hstreamdb/integration-tests) as an independent repository. It links with the main repository through GitHub Action: updating the main upstream source code will automatically trigger the integration test and generate the test report.

In addition, we also provide a script for the open-source community to quickly create a local test image. Developers can run integration tests locally before contributing code to ensure that the new code conforms to the behaviour specified in the test.

## Documentation update

We've improved the way to start HStreamDB clusters in Quick Start to simplify the Quick Start process. When users want to try HStreamDB, they don't need additional dependencies. As long as Docker and Docker-compose are installed, they can start an HStreamDB local cluster directly with one command.
