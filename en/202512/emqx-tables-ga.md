***From preview to production: expanded sizing, broader integration, and a unified platform for IoT data.***

Today, we're excited to announce that EMQX Tables is officially generally available.

Since we launched the public preview earlier this quarter, over one hundred developers and teams have tested EMQX Tables, built prototypes, and shared invaluable feedback. To everyone who participated: thank you. Your insights shaped the product we're releasing today.

Starting today, EMQX Tables is open to all EMQX Cloud users, with more deployment flexibility, broader broker integration, and the reliability you need for production workloads.

![image.png](https://assets.emqx.com/images/06e0e02556954c38b877e68e64bbdcda.png)

## What’s New in GA

We’ve listened closely to the feedback from our Preview participants. For the GA release, we are lifting restrictions and introducing enterprise-grade capabilities.

#### 1. **More sizing options.**

The preview limit is gone. EMQX Tables now offers four deployment tiers, ranging from 2 vCPU / 8 GB up to 16 vCPU / 64 GB.
For organizations with large-scale requirements, we now also offer custom configurations tailored to your specific throughput and retention needs.

#### 2. Available for Everyone (Including Serverless)

EMQX Tables now works with all EMQX Broker editions. 

Whether you're on Serverless, an existing Dedicated deployment, or Dedicated Flex, you can connect your broker to EMQX Tables directly, no migration required.

#### **3. Production-Ready Reliability**

We have hardened the underlying architecture, ensuring that EMQX Tables meets the strict availability and reliability standards required for mission-critical IoT applications.

## One Platform, from Device to Insight

If you've built IoT applications before, you know the drill: connect devices with an MQTT broker, spin up a separate time-series database, write integration code to bridge them, manage two consoles, two billing relationships, two security models. 

It works, but it's more complex than it needs to be.

EMQX Tables changes that. With native time-series storage built directly into EMQX Cloud, your data flows from MQTT topics to queryable tables with just a few clicks. No external databases, no custom pipelines, no middleware.

Together, EMQX Broker and EMQX Tables form a unified MQTT data platform:

- **EMQX Broker**: Fully managed MQTT messaging for device connectivity
- **EMQX Tables**: Fully managed time-series storage for IoT data

One console. One security model. One bill. And a much simpler path from raw telemetry to actionable insight.

![image.png](https://assets.emqx.com/images/05d01403bea1e3a512d316f13db6ab23.png)

## Key Capabilities

For those new to EMQX Tables, here's what you get out of the box:

- **Native MQTT integration**: Route data from topics to tables via Rule Engine, no code required
- **Schema-on-the-fly**: Automatic schema inference adapts to your evolving JSON payloads
- **Multi-protocol queries**: Use SQL for analytics, PromQL for monitoring, or InfluxDB Line Protocol for compatibility with existing tools
- **Visualization-ready**: Connect directly to Grafana, Metabase, or your preferred BI platform

## Availability and What's Next

EMQX Tables is available today on AWS in N. Virginia (us-east-1). We're actively working on expanding to additional regions, and expect more availability in early 2026.

We're also continuing to invest in the broader EMQX Cloud platform, with new capabilities for analytics, visualization, and data streaming on the horizon. This is just the beginning.

### **Get Started Today**

Ready to try EMQX Tables? Here's how to get started:

- **Try it out:** Log in to the [EMQX Cloud Console](https://accounts.emqx.com/signin?continue=https://cloud-intl.emqx.com/console/tables/new) and enable EMQX Tables on your deployment.
- **Read the Docs:** Check out our [Overview](https://docs.emqx.com/en/cloud/latest/emqx_tables/emqx_tables_overview.html) and [Quick Start Guide](https://docs.emqx.com/en/cloud/latest/emqx_tables/emqx_tables_quick_start.html) to hit the ground running.
- **Talk to Us:** Have a high-volume use case? [Contact our team](https://www.emqx.com/en/contact?product=cloud) for a consultation on custom sizing and architecture.

Thank you for being part of this journey. We can't wait to see what you build.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
