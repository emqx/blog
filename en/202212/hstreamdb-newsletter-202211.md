We released HStreamDB 0.11 in November with a few issue fixes. The development of the HStream Platform continues, and we're planning to release an Alpha version at the end of December.

## v0.11 is released

With the development of the HStreamDB project, we decided to accelerate the release cycle and gradually increase the frequency of releases. Therefore, after the release of v0.10 at the end of last month, we released v0.11 this month with the following updates and bug fixes:

- Modify the HServer's startup parameters `host` and `address` to `bind-address` and `advertised-address` for easier usage and understanding
- Remove the compression option from HServer; We recommend using end-to-end compression instead
- Unify resource naming conventions with improved resource naming validation
- Provide the creation time of the stream and subscription
- Fix some route validation issues for the RPC request from clients.
- Add the `subscription` subcommand for HStream CLI.
- Fix the issue that submitting subscription progress may fail.
- Fix the issue that a JOIN clause may return the wrong result.
- Fix the issue that it can't retry if the write operation times out.

## hdt provides support for deploying ELK Stack

hdt is a tool for automating HStreamDB cluster deployment. In addition to the rapid deployment of the core components of HStreamDB to multiple nodes, it also supports the deployment of monitoring components such as Prometheus, HStream Exporter, Grafana, etc.

 This month, to facilitate users to deploy, test, and monitor the HStreamDB cluster, hdt has provided the capability to collect and query HStreamDB logs via ELK Stack. If the appropriate option is enabled, it will automatically configure Logstash to import HStreamDB cluster logs into ElasticSearch during deployment, and the Kibana will be provided by default.

## HStream Platform is coming soon

HStream Platform is our upcoming **Serverless** service platform for streaming data, which is based on the public cloud, providing "No Deployment", "ZeroOps", "High Availability", and "One Stop" services for storage and real-time processing and analyzing of streaming data.

The first Public Alpha of the HStream Platform will go live **at the end of next month**. A free trial will be available at that time, so keep an eye on it! You can also register in advance at [https://hstream.io/cloud](https://hstream.io/cloud) to get the latest notifications.
