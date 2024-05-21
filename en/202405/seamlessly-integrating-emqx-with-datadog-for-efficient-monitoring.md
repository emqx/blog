## Introduction

Datadog is a cloud-based observability and security platform that offers automated infrastructure monitoring, application performance monitoring, log management, and real-user monitoring. It unifies these capabilities into a real-time application solution, enabling developers to easily monitor, analyze, and optimize performance and reliability.

Recently, EMQX officially [integrated](https://docs.datadoghq.com/integrations/emqx/) with Datadog, allowing users to leverage Datadog for collecting metrics related to device connectivity, message throughput, latency, and node performance. This integration enhances users’ ability to understand their services’ current state and troubleshoot system performance issues, facilitating the development of efficient, reliable IoT applications.

In this blog, we will guide you through the process of integrating EMQX with Datadog in four simple steps.

## Step 1: Install the Datadog Agent

Begin by creating a [Datadog](https://www.datadoghq.com/) account and logging in to the Datadog console.

Next, install the [Datadog Agent](https://docs.datadoghq.com/getting_started/agent/) on the server where EMQX is hosted. The Agent collects EMQX metrics and sends them to the Datadog cloud.

Deploy the Datadog Agent on the server where the EMQX cluster resides or on a server with access to the EMQX nodes. If you haven’t installed the Agent yet, follow these steps:

1. Navigate to **Integrations** → **Agent** in the menu bar to access the Agent Installation Instructions page.

2. Choose your operating system version and follow the provided instructions.

   ![Integrations → Agent](https://assets.emqx.com/images/f5dc4443f90dc32752c60012042d0c48.png)

## Step 2: Add EMQX Integration to Datadog

EMQX offers out-of-box [Datadog integration](https://docs.datadoghq.com/integrations/emqx/) that can be easily incorporated into your Datadog console by following these steps:

1. Open your Datadog console and navigate to **Integrations** → **Integrations** in the menu bar.

2. In the **Search Integrations** box, type “EMQX” to find the integration with the same name and author.

3. Click the **Install Integration** button in the upper right corner of the pop-up box to add the EMQX integration to Datadog.

   ![Click the Install Integration](https://assets.emqx.com/images/e2caea6a2bc01590b403b2c3bd271cbb.png)

4. After completing the installation, navigate to the **Configure** tab to access the configuration guidelines for the EMQX integration. The necessary configuration steps are carried out within the Datadog Agent.

   ![Configure tab](https://assets.emqx.com/images/a46f1e6438b018cbf461ae24567cfcde.png)

## Step 3: Add and Enable EMQX Integration on Datadog Agent

Following the configuration guidelines, add the EMQX integration to the Datadog Agent to configure the collection and reporting of EMQX metrics.

1. Execute the following command on the server where the Datadog Agent is hosted to add the EMQX integration. Note that this example uses version 1.1.0; always refer to the latest guidelines for the appropriate version:

   ```shell
   datadog-agent integration install -t datadog-emqx==1.1.0
   ```

1. Once the installation is complete, proceed to modify the Agent configuration file to enable EMQX integration:

   Navigate to the Agent configuration directory (usually located at /opt/datadog-agent/etc/conf.d/). Locate the emqx.d directory within this directory. You’ll find a sample configuration file named conf.yaml.example in the emqx.d directory.

   Create a copy of this file in the same directory and rename it to conf.yaml. Edit the conf.yaml file, adjusting the following configuration item:

   ```
   instances:
     - openmetrics_endpoint: http://localhost:18083/api/v5/prometheus/stats?mode=all_nodes_aggregated
   ```

   The `openmetrics_endpoint` specifies the address from which the Datadog Agent extracts metrics data in OpenMetrics format. In this case, it’s set to the HTTP API address of EMQX. Make sure to replace this with an address accessible by the Datadog Agent.

   The API also allows specifying the range of metrics to pull via the `mode` query parameter. The meaning of each parameter is as follows:

   ![The meaning of each parameter](https://assets.emqx.com/images/90e6fd142c844c160d492c6f713265f2.png)

   For a unified view, use the `mode=all_nodes_aggregated` option. This ensures that the Datadog control sees values for the entire EMQX cluster.

1. To [restart the Datadog Agent](https://docs.datadoghq.com/agent/guide/agent-commands/#start-stop-and-restart-the-agent) on macOS, follow these steps:

   ```shell
   launchctl stop com.datadoghq.agent
   launchctl start com.datadoghq.agent
   ```

1. After rebooting your system, use the following command to verify if the EMQX integration is successfully enabled. If you see “Instance ID: ... [OK]”, it indicates that the integration has been successfully enabled.

   ```shell
   $ datadog-agent status | grep emqx -A 4
       emqx (1.1.0)
       ------------
         Instance ID: emqx:1865f3a06d300ccc [OK]
         Configuration Source: file:/opt/datadog-agent/etc/conf.d/emqx.d/conf.yaml
         Total Runs: 17
         Metric Samples: Last Run: 166, Total: 2,822
         Events: Last Run: 0, Total: 0
         Service Checks: Last Run: 1, Total: 17
         Average Execution Time : 43ms
         Last Execution Date : 2024-05-11 17:35:41 CST / 2024-05-11 09:35:41 UTC (1715420141000)
         Last Successful Execution Date : 2024-05-11 17:35:41 CST / 2024-05-11 09:35:41 UTC (1715420141000)
   ```

At this point, you’ve completed all the necessary configurations on the Datadog Agent. The Agent will now periodically collect EMQX runtime data and send them to Datadog. Next, let’s check the Datadog console to ensure that the metrics are being collected correctly.

## Step 4: View EMQX Metrics on the Datadog Console

The Datadog Agent’s EMQX integration provides a ready-to-use dashboard chart that displays node status, message status, and other more in-depth observability metrics. You can follow these steps to utilize it:

1. Open the Datadog console and navigate to **Integrations** → **Integrations** in the menu bar.

2. Locate the installed EMQX integration and click to open it.

3. Switch to the **Monitoring Resources** tab within the pop-up box to open the **EMQX Overview** charts under **Dashboards**.

   ![Monitoring Resources tab](https://assets.emqx.com/images/330598b3ec6536a48a028143de23883c.png)

**The charts provide the following information:**

- OpenMetrics Health: The number of active metrics collectors.
- Total Connections: The overall count of connections, including those that remain the sessions despite being disconnected.
- NodeRunning: The quantity of running nodes within the cluster.
- Active Topics: The number of currently active topics.
- NodeStopped: The count of stopped nodes in the cluster.
- Connection
  - Total: The total number of connections, including those that maintain the session even when disconnected.
  - Live: The number of actively maintained TCP connections.
- Topic
  - Total: The overall number of topics.
  - Shared: The count of shared topics.
- Session: The total number of sessions.
- Erlang VM: The CPU, memory, and queue usage of the Erlang virtual machine.
- Retainer & Delayed
  - Retained: The number of retained messages.
  - Delayed: The count of delayed messages.
- Message
  - Sent & Received: The rate of sent and received messages.
  - Delayed & Retained: The rate of delayed and retained messages.
  - Publish & Delivered: The rate of message publishing and delivery.
  - Delivery Dropped: The number of delivered messages that were dropped.
- Client
  - Connected & Disconnected: The rate of connections being established and terminated.
  - Sub & UnSub: The subscription and unsubscription rates.
  - AuthN & AuthZ: Information on authentication and authorization rates.
  - Delivery Dropped: The number of dropped delivery messages.
- Mria: The total number of Mria transactions.

Below are screenshots of some of the charts; the values dynamically change based on load of EMQX and client activity.

![Metrics Overview](https://assets.emqx.com/images/4ff04f0ce8a1195c5dcc6026060b2cd6.png)

<center>Metrics Overview</center>

<br>

![Connection, Topic, and Session](https://assets.emqx.com/images/c45ccd37fb0dbaaf90951e071c92d565.png)

<center>Connection, Topic, and Session</center>

<br>

![The Rate of Sent and Received Messages, the Number of Retained/Delayed/Dropped Messages](https://assets.emqx.com/images/4be20e313d51ed7477d6117fa3c05b13.png)

<center>The Rate of Sent and Received Messages, the Number of Retained/Delayed/Dropped Messages</center>

<br>

![Client Event](https://assets.emqx.com/images/affbe7832fe71e29334c3e915c7744bc.png)

<center>Client Event</center>

## Next Steps

The charts built into Datadog’s EMQX integration show only some of the key metrics. You can also refer to [this document](https://docs.datadoghq.com/integrations/emqx/#metrics) to access all the reported EMQX metrics and create your own monitoring charts based on them.

Next, you can configure alert rules in Datadog based on these metrics. When certain metrics reach preset thresholds or abnormal situations occur, Datadog will send notifications to remind you to take necessary actions promptly, minimizing the impact of system failures on your business.

## Conclusion

This blog showcased how to seamlessly integrate EMQX with Datadog, enabling real-time monitoring of EMQX’s operational status. By leveraging EMQX’s established metrics and Datadog’s robust features, users can track critical aspects such as connection counts, message rates, and node status. Identifying potential issues promptly allows for timely corrective actions, ensuring system stability and reliability. We hope this article serves as a valuable reference for users who use Datadog to monitor EMQX.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
