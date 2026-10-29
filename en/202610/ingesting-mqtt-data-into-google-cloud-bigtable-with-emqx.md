## Introduction: Bigtable Integration in EMQX 6.3



MQTT is commonly used to transport high-volume telemetry and event data, but applications often need a scalable backend to store and query that data.

[Bigtable](https://cloud.google.com/bigtable) is a fully managed, wide-column NoSQL database service on Google Cloud. It is designed for large-scale, low-latency workloads, such as time series data, telemetry storage, event records, and high-throughput IoT data ingestion.

EMQX 6.3 brings native Bigtable integration through the rule engine and a Bigtable Action. You can process MQTT messages with rule SQL, map the selected fields to Bigtable row keys and cell mutations, and write the processed data to a Bigtable table in real time.

## Why Use Bigtable for MQTT Data?

Bigtable is well-suited to MQTT workloads that generate large volumes of sparse, time-series data and require low-latency writes. This makes it a natural backend for telemetry, device events, and other continuously generated data that may need to be queried or aggregated at scale.

Typical use cases include IoT sensor telemetry, industrial equipment data, connected appliances, financial market data, and other high-throughput event streams.

With EMQX, incoming MQTT messages can be filtered, transformed, and mapped to the structure required by Bigtable before being written to the target table.

## How EMQX Implements It



EMQX uses the [gRPC Data API](https://docs.cloud.google.com/bigtable/docs/reference/data/rpc) to append MQTT data into Bigtable. It allows for a compact data representation which helps reduce the used network bandwidth while transferring large amounts of live data. For best throughput, the Action batches incoming data for a configurable amount of time and number of messages, and then sends a `Bigtable.MutateRows` RPC with the data. The request itself consists only of `SetCell` mutations, which is appropriate for efficiently appending multiple rows to the target table. While other kinds of mutations are allowed by the API, `SetCell` is the one that makes the most sense for appending multiple rows to a table.

## Example: How to Get Started



The integration follows a simple flow:

**MQTT message → EMQX Rule Engine → Bigtable Action → Bigtable table**

First, create a Bigtable Connector. At this point, the key configuration is just the authentication method. For example, when running EMQX in GCP Compute instances, it is possible to simply chose “Attached Service Account”, and that’s it. For more detailed information, be sure to check out [EMQX docs](https://docs.emqx.com/en/emqx/latest/develop/data-integration/bigtable.html#create-a-bigtable-connector).

Next, create a Rule and Action. At a high level, the rule must explicitly define each of the required fields for the mutation (see the [docs](https://docs.emqx.com/en/emqx/latest/develop/data-integration/bigtable.html#create-a-rule-with-bigtable-sink) for more in-depth details):

- Instance and table ids
- Row key
- Column family name
- Column qualifier
- Timestamp (in microseconds)
- Cell value

```
SELECT
  clientid AS row_key,
  'stock_currencies' AS family_name,
  payload.code AS column_qualifier,
  payload.rate AS value,
  publish_received_at * 1000 AS timestamp
FROM
  "t/bigtable"
```

Once the Rule and Action are created, the Sink is ready to ingest some data. For the sake of demonstration, choose your favorite MQTT client and publish some data. Here, we use the MQTTX CLI to publish a test message.

```
mqttx pub -i my_mkt_data_src -t t/bigtable -m '{"code": "EUR/USD", "rate": 1.1468}'
```

Data will be ingested and made available for querying in Bigtable. You can go to Google Cloud Console and query the target table to see the ingested data. Navigate to Bigtable Studio for the target instance, and simply query the table:

```
SELECT * FROM mytable LIMIT 10
```

You will then see your ingested data!

## Conclusion

With EMQX 6.3, MQTT data can be filtered and transformed through the Rule Engine and written directly to Google Cloud Bigtable in real time. The integration provides a straightforward way to build data pipelines for high-volume telemetry, time-series data, and event streams.

For more information on new features in EMQX 6.3, see: [EMQX Enterprise 6.3.0: Run EMQX Your Way with Feature Gates & Hardened Security](https://www.emqx.com/en/blog/emqx-6-3-0-release-notes) 

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
