We are excited to announce the release of EMQX Enterprise 6.3.0!

This release gives enterprises more control over how EMQX is deployed, secured, integrated, and operated:

- **Deploy it leaner** with the new Feature Gates
- **Run it safer** with stronger security defaults and optional hardening
- **Connect it wider** with new cloud and enterprise data integrations
- **Operate with finer control** through enhanced multi-tenancy, rate limiting, and observability
- **Run it more efficiently** with network, resource-management, and stability improvements

Below is an in-depth look at what's new in EMQX Enterprise 6.3.0.

## Tailor EMQX to Your Exact Footprint with Feature Gates



Traditional enterprise MQTT brokers ship with a full feature set. But not every deployment needs the same capabilities.

If your architecture only requires a lightweight MQTT broker at the edge, in a cost-sensitive container, or in an embedded gateway, carrying the memory footprint and attack surface of unused features creates unnecessary overhead and risk.

EMQX 6.3.0 introduces **Feature Gates**, allowing you to boot EMQX with only the capabilities your specific environment requires. 

You can now choose a built-in preset or compose your custom feature stack:

- `FULL` **(Default):** The complete EMQX capability stack, exactly like previous releases.
- `ESSENTIAL`**:** A lightweight core containing *only* the MQTT broker, authentication, and authorization.
- **Custom Composition:** Flexibly select individual features (e.g., `dashboard`, `data_integration`, `gateways`, `multi_tenancy`, `metrics`, `plugins`). EMQX automatically resolves dependencies at boot and fails fast on invalid configs to prevent runtime surprises.

**Key Benefits:**

- **Noticeably Smaller Memory Footprint:** When running in `ESSENTIAL` mode, EMQX loads code on demand rather than pre-loading disabled feature modules at boot, resulting in a smaller resident memory footprint. The idle boot memory footprint in `ESSENTIAL` mode is less than 100MB. 
- **Reduced Overhead at High Concurrency:** Essential mode bypasses periodic per-connection statistics reporting meant solely for dashboard client tracking, freeing up valuable CPU and memory when handling massive connection spikes.
- **Composable Architecture:** Unlike rigid, all-or-nothing legacy brokers, Feature Gates provide a modular foundation tailored for single-purpose edge nodes, embedded gateways, and multi-tenant SaaS packaging.

## Stronger Security by Default & Easier Compliance



EMQX 6.3.0 strengthens security defaults across the platform, while the new `EMQX_SECURITY_PROFILE=hardened` option provides an additional layer of hardening for security-sensitive deployments.

This shifts security from a post-deployment checklist into a strict out-of-the-box baseline:

- **Strict MQTT Protocol Parsing by Default:** EMQX now strictly validates incoming MQTT 3.1.1 and 5.0 packets against specifications (such as headers, UTF-8 strings, and non-repeatable properties). Malformed client packets are disconnected immediately. Rather than clogging error logs, malformed connection attempts are cleanly counted per listener and isolated via client tracing, reducing log noise from scanners and fuzzers.
- **Upgraded Administrative Protection:** Admin passwords and API keys now default to **PBKDF2-HMAC-SHA256** with 600,000 iterations and random salts. Existing credentials continue working transparently and automatically upgrade upon their next change.
- **Protected Observability & Management Surfaces:** OpenAPI specs and Prometheus scrape endpoints now require authentication by default, keeping infrastructure metrics safe from unauthorized scraping.
- **Advanced Multi-Dimensional Flapping Detection:** Block DDoS or runaway client fleets before they strain your database backends. Flapping detection can now monitor repeat offenders across **Client IDs, Usernames, or Source IP addresses**, dropping rogue connections *before* expensive authentication queries run.
- **Secured Secret Storage:** EMQX will no longer boot with a default cluster cookie (`node.cookie`). Administrators must configure a custom cookie, which can now be provided via `file://` or system FIFOs, keeping secret keys entirely off the disk.

## More Cloud & Enterprise Data Integrations



EMQX provides 50+ built-in data integrations across cloud platforms, databases, messaging systems, and observability tools. Version 6.3.0 further expands these capabilities with new integrations.

- **Google Cloud Bigtable Connector:** Stream high-throughput IoT time-series telemetry directly into Google Cloud Bigtable for large-scale analytical workloads.
- **GCP Attached Service Account Support:** GCP PubSub and BigQuery connectors running on GCP virtual machines can now auto-fetch authentication tokens directly from instance metadata, eliminating manual credential management.
- **AWS IAM Roles Anywhere for Kafka:** Authenticate Kafka Producer/Consumer connectors securely using temporary, short-lived credentials via AWS IAM Roles Anywhere.
- **Dynatrace Observability:** Export traces and logs directly to Dynatrace via OpenTelemetry, authenticated securely using OAuth2 tokens.
- **PostgreSQL Session Visibility:** PostgreSQL connectors send an identifiable application name (default `emqx`) so active database sessions are easy to spot in PostgreSQL activity views.
- **Time-Based Disk Log Rotation:** Local disk logs now support daily or hourly file rotation with automated retention cleanup and timezone control.

## Finer Control & Richer Observability



EMQX 6.3.0 offers platform engineers and SaaS operators fine-grained control over tenant traffic and deep runtime visibility:

- **Context-Aware Authorization Preconditions:** Evaluate authorization backends conditionally based on client attributes, actions, or topic filters. Route requests to specific auth services only when exact rules match, streamlining complex multi-backend setups.
- **Dynamic Multi-Tenant Auth Routing:** Include template variables directly in HTTP auth URLs (e.g., `https://${client_attrs.tenant_id}[.auth.example.com/authn](https://.auth.example.com/authn)`). Combined with dynamic host resolution, each tenant routes natively to their dedicated authentication service without needing an external API gateway.
- **Tenant-Aware Metrics & Topic Metrics v2:** Introducing Topic Metrics v2 with full REST API CRUD support, wildcard topic filters, and namespace ownership. Combined with an upgraded Prometheus exporter (featuring enabled-by-default VM and memory collectors), SaaS operators gain full per-tenant metric isolation for precise chargeback models and SLO tracking.
- **Slow Consumer Visibility (**`session-top`**):** Operational teams can now inspect real-time buffered payload bytes per session. The new `emqx ctl session-top` command identifies the top slow consumers across the cluster before they cause memory pressure.
- **Subscribe Rate Limiting & Session Expiry Clamping:** Set maximum rates for `SUBSCRIBE` packets per client or namespace, and enforce caps on client-requested `Session-Expiry-Interval` values to keep broker resource consumption strictly bounded.

## Peak Performance & Real-World Load Stability



Under the hood, EMQX 6.3.0 updates network engines and resource handling for higher throughput and predictability under load.

- **Next-Gen Network Stack by Default:** Switches the default TCP listener backend to Erlang/OTP’s modern `socket` API (replacing the legacy `gen_tcp/inet` path), positioning EMQX on the network stack Erlang/OTP is actively investing in going forward.
- **Faster JSON Processing:** Delivers improved JSON encoding and decoding performance across the entire platform.
- **Resource-Aware Container Defaults:** Network port limits (`node.max_ports`) and VM scheduler counts (`node.schedulers`) now default to `auto`. EMQX dynamically caps scheduler counts based on the CPU cores actually assigned to the VM, delivering better, non-oversubscribed performance in `cpuset`-limited containers and Kubernetes environments.
- **Fair QoS 0 Flow Control:** Prevents slow subscribers from accumulating unbounded QoS 0 backlogs in memory. When a connection backs up, QoS 0 messages are temporarily routed through a bounded queue that evicts older QoS 0 messages first, applying back-pressure fairly so high-priority **QoS 1 and QoS 2 messages continue delivering without interruption**.

## Build Agentic IoT with MQTT Agent



EMQX 6.3.0 introduces **MQTT Agent**, a new plugin that provides MQTT-native primitives for building and running AI agents within the EMQX platform.

Designed for human-less automation, large-scale device operations, and restricted, auditable access, MQTT Agent brings AI agent workflows closer to the devices, events, and data they operate on.

It provides three core primitives as MQTT resources:

- **Tools**: Reusable capabilities that connect agents to databases, HTTP services, external APIs, or other agents.
- **Sessions**: Stateful LLM conversations that maintain context across interactions.
- **Pipelines**: Event-driven workflows that orchestrate agents and tools in response to MQTT events.

Learn more about MQTT Agent: https://docs.emqx.com/en/emqx/latest/extensions/plugin-catalog/6.3/emqx-agent.html

Download MQTT Agent plugin: 

- https://www.emqx.com/downloads/emqx-plugins/6.3.0/emqx_agent-1.0.0.tar.gz
- https://www.emqx.com/downloads/emqx-plugins/6.3.0/emqx_agent-1.0.0.sha256

## Upgrade to EMQX Enterprise 6.3.0 Today



As enterprise IoT architectures scale across edge devices, hybrid clouds, and global infrastructure, operational requirements vary widely. EMQX Enterprise 6.3.0 gives teams the flexibility to tailor the platform to their needs, with a leaner footprint, stronger security, finer-grained controls, and better performance.

Ready to run EMQX your way?

- [Download EMQX Enterprise 6.3.0](https://www.emqx.com/en/try?product=enterprise) to get started
- Read [the full change log](https://www.emqx.com/en/changelogs/enterprise/6.3.0) to explore more

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
