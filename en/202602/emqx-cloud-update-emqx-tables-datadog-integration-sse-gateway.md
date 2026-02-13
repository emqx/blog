We are continuously evolving EMQX Cloud to provide a more robust, observable, and flexible MQTT platform. Our latest update introduces expanded availability for EMQX Tables, simplified observability with Datadog, and a preview of our new SSE Gateway.

Here is what’s new.

## EMQX Tables: Now Available in AWS Oregon and Frankfurt



We have expanded the regional support for [EMQX Tables](https://www.emqx.com/en/features/emqx-tables), our integrated time-series database solution. You can now deploy EMQX Tables in the following regions:

- **AWS Oregon (us-west-2)**
- **AWS Frankfurt (eu-central-1)**

![image20260210063749.png](https://assets.emqx.com/images/3d651cf9ead0a729cf8ee6c149ed8ad8.png)

**Why this matters:** 

If your EMQX Cloud Dedicated deployment is located in these regions, we strongly recommend creating your EMQX Tables instance in the same location.

Co-locating your Broker and Tables allows them to communicate within the same **VPC (Virtual Private Cloud)**. This architecture ensures data flows over a private network, delivering three key benefits:

1. **Maximum Stability:** Eliminates public network jitter.
2. **Enhanced Security:** Data never traverses the public internet.
3. **Cost Efficiency:** Significantly reduces data transfer costs associated with cross-region or public traffic.

**Learn more:** [EMQX Tables Overview](https://docs.emqx.com/en/cloud/latest/emqx_tables/emqx_tables_overview.html)

## Native Datadog Integration



Observability is critical for IoT infrastructure. In this version, we have streamlined the integration with Datadog.

**What changed:** 

Previously, integrating EMQX Cloud with Datadog required submitting a support ticket. Now, for **new deployments**, this is fully self-service. You can configure the integration directly within the EMQX Cloud console by simply providing your **Datadog API Key**.

![2ffe2db2629744835270bddd4075b20e20260210063813.png](https://assets.emqx.com/images/f6db0f101a085a8b18552e9f78a7a9ba.png)

To help you get started immediately, we also provide a pre-configured [Datadog dashboard template](https://github.com/emqx/emqx-cloud-datadog) on GitHub.

> *Note: This native configuration applies to new deployments only. Existing deployments still require a support ticket to enable Datadog integration.*

## SSE Gateway for MQTT (Preview)



We are excited to introduce the **Server-Sent Events (SSE) Gateway**, available in preview for **EMQX Cloud Dedicated Flex**.

This feature allows clients to subscribe to MQTT topics and receive messages via the HTTP-based SSE protocol, eliminating the need for a full MQTT client library.

### Why SSE?



While MQTT is the standard for device communication, many consumers of IoT data, such as web dashboards, mobile apps, and backend services, are optimized for HTTP. The SSE Gateway bridges this gap.

**Key Use Cases & Value:**

- **Simplified Web & Mobile Development:** Frontend developers can consume real-time data streams (like stock prices or sensor readings) using standard HTTP libraries. This reduces bundle size and battery consumption for mobile applications that only need to listen to data without publishing.
- **Seamless AI Integration:** This is a game-changer for AI Agents. Most LLMs and AI agents operate in stateless HTTP environments. By using SSE, AI agents can "listen" to a stream of real-time IoT context (e.g., smart home states, industrial alarms) to trigger RAG (Retrieval-Augmented Generation) workflows or real-time inference. It allows AI to tap into the MQTT nervous system using the web protocols it speaks natively.

![3a150a8a45595e8e25d1e0184ae2d26920260210064523.png](https://assets.emqx.com/images/fe24e83df05336824d554798ee9dc687.png)
![26214d594e674b2e83afc2590a4e6e7c20260210064442.png](https://assets.emqx.com/images/451b2325e50b5b668c5ce200fec21111.png)


- **Dashboarding:** Rapidly build visualization panels without managing complex WebSocket or MQTT connections.

> *Note: The SSE Gateway is currently in Preview. Please submit a ticket via the console to enable this feature for your Dedicated Flex deployment.*

## Get started



- **Try EMQX Tables:** Log in to the [EMQX Cloud Console](https://cloud-intl.emqx.com/console/) and create an instance in Oregon or Frankfurt.
- **Set up Datadog:** Create a new deployment and configure Datadog integration from the monitoring settings.
- **Explore SSE:** [Contact us](https://www.emqx.com/en/contact?product=cloud) or [submit a ticket](https://cloud-intl.emqx.com/console/tickets) to enable the SSE gateway preview on your Dedicated Flex deployment.
