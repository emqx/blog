eKuiper is in the development cycle of v1.7.0 this month, and the development team and community partners have jointly completed a series of new features. We have preliminarily enabled support for Lookup Table, thus improving the integration of stream computing and batch computing, such as real-time data completion. In addition, we have expanded and optimized data integration by adding HTTP push source and Influx V2 sink; extended the data format support for EdgeX source. We also released v1.6.2 at the end of the month, mainly for bug fixes and dashboard enhancement.

## Integration of stream computing and batch computing

Not all data will change frequently, even in real-time computing. In some cases, you may need to use static data stored externally to complete stream data. For example, user metadata may be stored in a relational database. When only real-time data are available in stream data, it is necessary to connect stream data with batch data to complete. In the new version, eKuiper adds a new concept of Lookup Table to bind external static data, which can be connected with stream data in rules to enable the integration of stream computing and batch computing.

When working with query tables, there are usually three steps.

1. Create a data flow. This step is the same as the previous process of creating a normal data flow.

   ```
   CREATE STREAM demoStream() WITH (DATASOURCE="demo", FORMAT="json", TYPE="mqtt")
   ```

2. Create a query table. When a table is created, a new attribute KIND is added to specify whether it is a query table. The source type of the table here is SQL, which needs to configure the database connection information in etc/sources.sql.yaml. The DATASOURCE property specifies the name of the physical table to be connected.

   ```
   CREATE TABLE myTable() WITH (DATASOURCE=\"myTable\", TYPE=\"sql\", KIND=\"lookup\")
   ```

3. Create rules, connect traffic and tables, and perform calculations.

   ```
   SELECT * FROM demoStream INNER JOIN myTable on demoStream.id = myTable.id
   ```

Different from the dynamic tables supported in previous versions, query tables do not need to store snapshots of table data in memory, but directly query external data when connecting, so they are able to support queries of more static data. Query tables provide support for configurable data memory cache to improve query efficiency.

A query table itself needs storage capacity, so not all data sources can be used as query table types. At present, we have adapted or added the following query sources:

- SQL
- Redis
- Memory: with the rule pipeline, the historical results of other rules can be used as the query source.

In addition, LookupSource interface is added to the native plug-in for users to customize query source extensions.

## Push data stream with HTTP

An httppush source is added. As an HTTP server, it can receive messages from HTTP clients. All HTTP push sources share a single global HTTP data server. Each source can have its own URL to support multiple endpoints. The configuration of HTTP push source is divided into two parts: global server configuration and source configuration. The global server configuration is located in `etc/kuiper.yaml` , you can configure the server's monitoring address and port, as well as HTTPS related certificate. The source configuration is located in `etc/sources/httppush.yaml` , used to configure the HTTP method pushed. When creating a data stream, you can configure the URL endpoint that the data stream monitors through the DataSource property to distinguish the push URL of each data stream.

```
CREATE STREAM httpDemo() WITH (DATASOURCE="/api/data", FORMAT="json", TYPE="httppush")
```

In this example, DataSource is set to`/api/data`. If the user uses the default server configuration, data pushed to the `http://localhost:10081/api/data` will form data stream httpDemo. Later, you can create rules to process the data flow.

## InfluxDB 2.x Sink

In previous versions, eKuiper provided the InfluxDB sink, which supported writing data to InfluxDB v1. x. However, since the API of InfluxDB v2. x is not compatible with v1, the original sink does not support writing to v2. In the new version, we enable support for writing to InfluxDB v2. x thanks to the InfluxDB v2. x sink plug-in provided by community user @ elpsyr.

## Process image data of EdgeX Foundry

EdgeX Foundry uses the `application/cbor` format to transfer binary data, such as image data. In the new version, we provide support for this format, making it possible for users to use eKuiper to process image data of EdgeX. Edge X Camera service collects image data, which can be preprocessed, AI reasoned, post-processed, etc. through eKuiper, thus completing AI image processing pipeline with SQL rules.

## Upcoming

Next month, we will continue to develop v1.7.0, with planned new features including connection resource management, computing offload, etc. The new version is expected to be released at the end of October.
