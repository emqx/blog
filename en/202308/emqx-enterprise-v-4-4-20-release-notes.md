We are excited to announce the availability of [EMQX Enterprise](https://www.emqx.com/en/products/emqx) 4.4.20!

This release elevates the performance of Kafka and HStream data integration, introduces support for attributes and ordering keys in GCP Pub/Sub data integration, and fixes several bugs.

## Enhancing Kafka and HStream Data Integration Performance

By seamlessly integrating Kafka and HStream platform, EMQX offers a unified solution for collecting, storing, processing, and analyzing IoT event streams. This integration provides robust support for a wide range of real-time IoT application scenarios.

In previous versions, EMQX has already incorporated asynchronous and batch processing mechanisms to meet the demanding performance requirements of large-scale data integration scenarios. In EMQX Enterprise 4.4.20, the Kafka and HStream driver is further enhanced with the addition of a message buffer for Erlang process communication. This leverages the batch processing mechanism to accelerate internal message delivery, thus significantly improving overall throughput performance to cater to even the most demanding performance needs.

This feature is disabled by default. Users can activate it by configuring the **Maximum Erlang Message Accumulation** and **Maximum Erlang Message Accumulation Interval** settings within the Kafka and HStream actions.

According to our internal tests, this new feature can increase data integration performance by 10%-40% across various scenarios. We will also include this feature in the subsequent versions of EMQX Enterprise Edition 5.0.

## Introducing Attribute and Ordering Key Support for GCP Pub/Sub Integration

GCP Pub/Sub is a fully managed service for event streaming and subscription that is widely used to build reliable real-time streaming pipelines. The EMQX Rule Engine enables the publication of processed data to GCP Pub/Sub, facilitating seamless integration with GCP services.

EMQX Enterprise 4.4.20 introduces comprehensive support for attributes and ordering keys within GCP Pub/Sub actions. This enhancement enriches contextual information and guarantees the orderly publication of messages, thereby empowering versatile IoT data processing.

## Additional Enhancements

- Add `auto_reconnect` option for SQL Server data integration to automatically restore the connection between EMQX and SQL Server after disconnection to ensure data writing continuity.

- Add TLS connection support for RabbitMQ data integration to enhance the security and integrity of data transmission.

## Bug Fixes

- Fixed the issue that the `mongo_date()` function of the Rule Engine could not be tested on the Dashboard.

- Fixed the issue that the Rule Engine fails to send messages via RabbitMQ actions after hot upgrading to 4.4.19.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
