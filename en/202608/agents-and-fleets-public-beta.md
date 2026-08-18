EMQX Cloud continues to expand from a managed MQTT broker platform into a broader cloud-native IoT data platform. In this release update, EMQX Agents and EMQX Fleets are now available in Public Beta. EMQX v6 broker deployments are also available for supported Dedicated and Dedicated Flex plans, bringing new capabilities for targeted diagnostics, client event visibility, and data integration.

## EMQX Agents Now in Public Beta



EMQX Agents is now available in Public Beta, making it easier for more users to try AI-assisted workflows in EMQX Cloud.

With Public Beta, users can create an Agents deployment directly from the EMQX Cloud Console on the Starter plan. Usage is free during the Public Beta period. Agents use connectors to link EMQX services and third-party tools, enabling workflows that react to MQTT events, query data, publish messages, and send notifications.

For a deeper introduction, read [Introducing EMQX Agents](https://www.emqx.com/en/blog/introducing-emqx-agents).

## EMQX Fleets Now in Public Beta



EMQX Fleets is now available in Public Beta, opening access to managed device management capabilities in EMQX Cloud without requiring a support request.

With Public Beta, users can create a Fleets deployment directly from the EMQX Cloud Console on the Starter plan. Users who have not created a Fleets trial before can start with a 14-day free trial at the 10,000 Devices tier, while non-trial deployments can select any available tier from 10,000 to 100,000 Devices. During Public Beta, Fleets instance charges and egress traffic charges are not billed.

Fleets provides a managed device registry, device shadows, commands, jobs, and device queries, so teams can manage connected devices without building the device management layer themselves.

For a deeper introduction, read [Introducing EMQX Fleets: A Device Management Service for IoT at Scale](https://www.emqx.com/en/blog/a-device-management-service-for-iot-at-scale).

## EMQX v6 Broker Deployments



When creating a supported Dedicated or Dedicated Flex Broker deployment, you can select **v6 (recommend)** from the **EMQX Version** field.

EMQX v6 is recommended for new deployments. You can still select v5 if your workload depends on EMQX v5 behavior or compatibility.

![image.png](https://assets.emqx.com/images/f7949df365682eff5c51d65ce51526c0.png)

EMQX Version dropdown showing v6 recommended and v5 options

### Targeted Debugging with Log Trace



Log Trace captures debug-level broker logs for a specific troubleshooting target without enabling debug-level logging for the entire deployment.

You can create a trace for any of the following targets:

- MQTT client ID
- Topic
- Source IP address
- Rule ID

![image.png](https://assets.emqx.com/images/eef49fa9331391387cb144edd244dbf2.png)

Log Trace list showing topic and client ID traces with running and stopped status

Log Trace is useful when investigating client connection failures, unexpected disconnections, subscription failures, message publishing problems, message loss, or rule execution errors.

Log Trace is available for Dedicated and Dedicated Flex deployments running EMQX v6.1.3 or later.

Learn more: [Log Trace](https://docs.emqx.com/en/cloud/latest/deployments/log_trace.html)

### Client Lifecycle Visibility with Event History



Event History provides a quick way to investigate recent client lifecycle events, including connection, disconnection, authentication, and subscription activity. It helps operators reconstruct what happened during a client's lifecycle.

Together, Log Trace and Event History provide teams with more practical tools for day-to-day MQTT operations. Event History offers a high-level timeline, while Log Trace offers deeper broker-side details for targeted debugging.

Event History is available for Dedicated and Dedicated Flex deployments running EMQX v6.1.3 or later.

Learn more: [Event History](https://docs.emqx.com/en/cloud/latest/deployments/event_history.html)

### New Data Integration Options: BigQuery and Snowflake



EMQX Cloud adds more options for streaming MQTT data into analytical platforms.

The BigQuery integration allows teams to route selected MQTT data into BigQuery tables for SQL-based analytics, dashboards, and reporting workflows without building a custom ingestion service.

The Snowflake Streaming integration uses the Snowpipe Streaming API to ingest MQTT data into Snowflake tables with low latency. This gives teams a direct path from live IoT data to Snowflake-based analytics, BI, and data sharing workflows.

Learn more: 

- [Ingest MQTT Data into BigQuery](https://docs.emqx.com/en/cloud/latest/data_integration/bigquery.html)
- [Ingest MQTT Data into Snowflake with Streaming Mode](https://docs.emqx.com/en/cloud/latest/data_integration/snowflake.html)

### Other Updates



EMQX v6 also improves MQTT Source capabilities for MQTT 5.0 bridging scenarios. MQTT Source now supports more precise behavior when bridging messages from remote MQTT services.

Recent EMQX Cloud updates also expand BYOC support on Azure Public Cloud, giving teams more options for running EMQX Cloud in their own cloud environment when infrastructure control or data residency requirements apply.

## Ready to Explore?



You can explore these updates from the EMQX Cloud Console and the documentation:

- Create an [EMQX Agents](https://docs.emqx.com/en/cloud/latest/emqx_agents/emqx_agents_overview.html) deployment to try AI-assisted workflows in EMQX Cloud.
- Create an [EMQX Fleets](https://docs.emqx.com/en/cloud/latest/emqx_fleets/emqx_fleets_overview.html) deployment to manage device registry, shadows, commands, jobs, and device queries.
- Create a [Dedicated or Dedicated Flex Broker deployment with EMQX v6](https://docs.emqx.com/en/cloud/latest/new_features.html#emqx-cloud-supports-emqx-v6-broker-deployments) to try Log Trace, Event History, BigQuery, Snowflake Streaming, and MQTT Source enhancements.
- Explore [BYOC on Azure](https://docs.emqx.com/en/cloud/latest/new_features.html#byoc-on-azure) if you need to run EMQX Cloud in your own Azure environment.

For a full feature summary, see [What's New in EMQX Cloud](https://docs.emqx.com/en/cloud/latest/new_features.html).



The pilot was the easy part. The rollout is the work. Cloud-native is what lets the rollout finish.

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
