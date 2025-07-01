The promise of IoT has always been to leverage device data for smarter operations, predictive maintenance, and groundbreaking AI applications. However, a persistent challenge has stood in the way: the gap between the real-time world of Operational Technology (OT) and the analytical world of Big Data and IT.

The OT world runs on live, streaming data. The IT world of analytics and AI runs on structured, queryable datasets. Getting data from one side to the other has traditionally required complex, brittle, and expensive ETL (Extract, Transform, Load) pipelines.

With the release of EMQX Enterprise 5.10, we are thrilled to introduce a feature designed to tear down this wall: **native data integration with Amazon S3 Tables.**

![image.png](https://assets.emqx.com/images/56cca3be309b4cd9e8bc6c8c0e91d821.png)

<center>EMQX Data Integration - S3 Tables</center>

## The Challenge: From Data Stream to Data Lakehouse

Streaming raw MQTT data into a standard Amazon S3 bucket is a common first step for data collection. But this raw data isn't immediately usable for analytics. To make it valuable, you need to structure it, manage schemas, and optimize it for query engines like Amazon Athena, Spark, or Presto. This often involves batch processing jobs that add latency, cost, and complexity, delaying access to critical insights.

## The Solution: Direct Integration with Analytics-Ready S3 Tables

Amazon S3 Tables, built on the open-source powerhouse Apache Iceberg, solves this problem by providing a high-performance, open table format directly on top of your S3 data lake.

And now, **EMQX can seamlessly ingest data streams into S3 Tables.**

This new integration acts as a powerful bridge, connecting the real-time flow of MQTT data directly to your analytical ecosystem. Instead of just dumping raw files, EMQX continuously streams IoT data into a structured, high-performance, and analytics-ready table format.

## Key Benefits of the EMQX and S3 Tables Integration

- **Seamless OT and IT Convergence:** This is the most direct path from your connected devices to your data lakehouse. It enables a smooth, unified flow of information, allowing data analysts and scientists to work with OT data as soon as it arrives.
- **Eliminate Complex ETL Pipelines:** By writing data in an analytics-ready format from the start, you can significantly reduce or even eliminate the need for intermediate data processing and transformation jobs. This simplifies your data architecture, reduces operational overhead, and lowers costs.
- **Accelerate Big Data and AI Initiatives:** With data instantly available and queryable in your S3 lakehouse, your teams can accelerate their workflows. Whether it's for building dashboards, running ad-hoc analytical queries, or training machine learning models on the freshest possible data, the time-to-insight is dramatically reduced.
- **Open, Future-Proof, and Performant:** Because S3 Tables are based on Apache Iceberg, you are using an open standard that avoids vendor lock-in. This format is designed for high-speed queries on massive datasets and supports features like transactional consistency and schema evolution, ensuring your data lake remains robust and manageable as your needs change.

## How It Works: A Simplified Workflow

![image.png](https://assets.emqx.com/images/cf42bb8d2d915e3cbf5e088697f0b70a.png)

The new S3 Tables Sink is a core part of EMQX's Data Integration engine. Setting it up is straightforward:

1. **Device Connection to EMQX**: IoT devices connect to EMQX via MQTT and begin publishing telemetry data.
2. **Select Your Data Source:** In the EMQX Dashboard, choose the [MQTT topics](https://www.emqx.com/en/blog/advanced-features-of-mqtt-topics) you want to capture (e.g., `telemetry/+/data`).
3. **Data Transformation**: Rules in EMQX can filter, transform, or enrich message payloads to match the schema of the target Iceberg table.
4. **Create an S3 Tables Sink:** Add a new Sink to your data rule and select "Amazon S3 Tables".
5. **Configure and Connect:** Provide your AWS credentials, specify the S3 Tables ARN, namespace, and table. EMQX handles the communication with AWS S3 Tables Iceberg REST endpoint to manage the table's metadata.

EMQX automatically buffers messages and writes them efficiently into your S3 tables in the Apache Iceberg format. Once committed, your data is instantly available for query and analysis by any Iceberg-compatible service.

## A Foundation for the Future

The EMQX integration with Amazon S3 Tables is a foundational component for building a modern, real-time data strategy. It empowers organizations to finally unlock the full potential of their IoT data by unifying their real-time and analytical worlds.

**Ready to build your bridge from OT to AI?**

- Download [**EMQX Enterprise 5.10.0**](https://www.emqx.com/en/downloads-and-install/enterprise)
- Check the step-by-step tutorial in our [**S3 Tables Integration Documentation**](https://docs.emqx.com/en/emqx/latest/data-integration/s3-tables.html)
- [**Contact our team**](https://www.emqx.com/en/contact?product=emqx) for a personalized demonstration



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
