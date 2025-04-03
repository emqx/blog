We’re thrilled to announce the release of **EMQX Enterprise 5.8.6**, the latest iteration of the world’s most scalable MQTT platform, now available. Let’s explore what’s new with version 5.8.6—and catch you up on the exciting features we’ve introduced from v5.8.1 to v5.8.5, because there’s a lot to unpack since our last chat!

## Highlights from v5.8.1 to v5.8.6

Starting with v5.8.1, EMQX brings a host of enhancements across authentication, data integration, observability, and usability. Here’s a look at the standout features:

### Fine-Grained and Flexible Access Control

- [**Client-Info Authentication**](https://docs.emqx.com/en/emqx/latest/access-control/authn/cinfo.html): A new way to secure your connections. You can now authenticate clients using their info—like client ID or username—to streamline access control for IoT fleets.
- **Client Attributes as ACL Rule Preconditions**: Access control lists (ACLs) got smarter. Use client attributes (e.g., device type or location) as preconditions for rules, giving you fine-grained control over who gets to publish or subscribe. For details, see [Access Control List](https://docs.emqx.com/en/emqx/latest/access-control/authn/acl.html) and [ACL File Format](https://docs.emqx.com/en/emqx/latest/access-control/authz/file.html#acl-file-format).

### New Integrations with Snowflake, Tablestore and TDengine Cloud

We’ve expanded EMQX’s data integration lineup. 

- [**Snowflake**](https://docs.emqx.com/en/emqx/latest/data-integration/snowflake.html): Now, you can seamlessly ingest MQTT data into Snowflake, a cloud-based data platform optimized for analytics, leveraging its scalable warehousing and fast query performance on structured and semi-structured data.
- [**Tablestore**](https://docs.emqx.com/en/emqx/latest/data-integration/tablestore.html): Integration with Alibaba Tablestore, a serverless database tailored for IoT, enables high-performance time-series storage with millisecond-level queries and flexible analysis, using the TimeSeries model to efficiently manage massive device data.
- [**TDengine Cloud**](https://docs.emqx.com/en/emqx/latest/data-integration/data-bridge-tdengine.html#start-tdengine-and-create-a-database): EMQX now supports data integration with TDengine Cloud. This opens up seamless, secure data flows to TDengine’s cloud-based time-series platform for your IoT analytics.

### Improved Observability and Monitoring by End-to-End Tracing

EMQX now enables end-to-end tracing mode in OpenTelemetry to monitor the full lifecycle of MQTT messages—from client connection through the broker to downstream systems—capturing detailed spans like `connection`, `subscribe`, and `broker.publish` with attributes such as `clientid` and `topic`. For detailed information, see [OpenTelemetry-Based End-to-End MQTT Tracing](https://docs.emqx.com/en/emqx/latest/observability/opentelemetry/e2e-traces.html).

### Clear Configuration Order with New Configuration File

We’ve introduced `etc/base.hocon` in EMQX 5.8.4 as a foundational configuration file to simplify and clarify how settings are managed, addressing limitations of the older `emqx.conf`. 

Previously, `emqx.conf` sat at the top of the configuration hierarchy, causing confusion—its mutable settings could be changed via the Dashboard, API, or CLI and applied instantly, but those changes wouldn’t stick after a restart, leading to inconsistent behavior. 

Now, `etc/base.hocon` acts as the base layer in a clearer precedence order (environment variables > `emqx.conf` > `data/configs/cluster.hocon` > `base.hocon`), offering a persistent, structured foundation in HOCON format that supports nested configurations and ensures overrides from higher layers work predictably, making cluster management smoother and more reliable. For details, see [Configuration Files](https://docs.emqx.com/en/emqx/latest/configuration/configuration.html).

### Optimized Dashboard Experience

The EMQX Dashboard has evolved across v5.8.1 to v5.8.6, delivering a more intuitive and powerful interface for managing your MQTT broker. Here are some major enhancements:

#### Usability Improvements

- Added pagination, searching, and status filtering to Action and Source pages, making it simpler to manage rules and integrations at scale.
- Included a one-click cluster metrics reset, speeding up diagnostics and observation of cluster changes.

#### Metrics Display Enhancements

- Optimized the `/api/v5/monitor` endpoint with concurrent RPC calls to fetch cluster-wide metrics, eliminating timeouts in large deployments.
- Added key metrics like message rates directly on the homepage, reducing navigation for critical insights.

#### Monitoring Tools

Introduced a simplified webhook setup for alarm events, making it easier to automate monitoring and stay proactive. For more information, see [Integrate Webhook to Send Alarm Events](https://docs.emqx.com/en/emqx/latest/observability/alarms.html#integrate-webhook-to-send-alarm-events).

These upgrades save time, boost operational clarity, and make EMQX adaptable to your needs, reflecting our commitment to a powerful yet user-friendly experience.

## Other Enhancements and Important Bug Fixes

**Smarter Session Tracking (**[**#14869**](https://github.com/emqx/emqx/pull/14869)**)**

We’ve added a `connected_at` timestamp to the `$events/client_disconnected` event payload. This lets you track when a client’s session originally started, preventing outdated disconnect events from messing up session state—especially handy for devices on shaky networks with frequent reconnects.

**MQTT over QUIC (**[**#14583**](https://github.com/emqx/emqx/pull/14583) **and** [**#14597**](https://github.com/emqx/emqx/pull/14597)**)**

You can now use a special setting to reveal security details for debugging with tools like Wireshark, and we’ve accelerated connection closures by promptly halting incoming data while still transmitting the `MQTT.DISCONNECT` packet, reducing delays from unresponsive devices. These changes make MQTT over QUIC more efficient and reliable for real-world IoT use.

**Enhanced Connection Rate Limiter for Improved System Resilience (**[**#14219**](https://github.com/emqx/emqx/pull/14219)**)**

Refined the connection rate limiter, allowing listeners to accept and quickly close excess connections instead of ignoring them, which prevents resource overload and keeps the system responsive during peak traffic.

**Update** `gen_rpc` **Library to Enhance Cluster Stability (**[**#13956**](https://github.com/emqx/emqx/pull/13956)**)**

The `gen_rpc` library was updated to version 3.4.1 to fix a critical issue where a forced node shutdown during RPC channel setup could crash a peer node in the cluster, improving overall cluster stability.

## Get Started with EMQX Enterprise 5.8.6

Ready to dive in? EMQX 5.8.6 is now available on our [official website](https://www.emqx.com/en/downloads-and-install/enterprise). Whether you’re upgrading from v5.8.0 or jumping in fresh, check out the [Release Notes](https://docs.emqx.com/en/emqx/latest/changes/all-changes-ee.html) for the full scoop on changes and upgrade tips. And if you’re curious about the journey from v5.8.1 to v5.8.5, those details are there too!



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
