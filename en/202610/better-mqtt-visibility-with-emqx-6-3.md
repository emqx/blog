> **At a glance**
>
> - [EMQX 6.3](https://www.emqx.com/en/blog/emqx-6-3-0-release-notes) introduces **Topic Metrics v2**: named metric collections that follow whole groups of topics, not just one topic at a time.
> - Metrics are now **tenant-aware**. Each team or customer sees the numbers for its own traffic, and platform operators still see everything.
> - All of it flows into **Prometheus and Grafana**, so it fits the monitoring stack you already run.

## One Broker, Many Questions



An MQTT broker rarely serves just one application. A single EMQX cluster often carries traffic for many device fleets, product lines, or customers at once. That is efficient, but also makes some simple questions hard to answer:

- How many messages do our temperature sensors send each minute?
- Which customer produces most of the traffic this week?
- Are messages being dropped, and if so, whose messages are they?

Cluster-wide totals do not answer these questions. They tell you that traffic went up, but not where it came from. Until now, EMQX could also track one exact topic at a time. That works for a few important topics, but not for a fleet of thousands of devices where every device has its own topic.

## Topic Metrics v2 in EMQX 6.3: Measure What Matters to You



EMQX 6.3 closes the gap with two improvements that work together: **Topic Metrics v2 and tenant-aware metrics.**

With Topic Metrics v2, you create a **metric collection**. A collection has a name that you choose and a topic pattern that decides which messages it counts.

The pattern can use MQTT wildcards. One collection can cover every device in a fleet, every site in a region, or every event type of an application. For example:

| Collection name       | Topic pattern           | What it counts                         |
| :-------------------- | :---------------------- | :------------------------------------- |
| `temperature-sensors` | `sensors/+/temperature` | Temperature readings from every sensor |
| `factory-berlin`      | `factory/berlin/#`      | All traffic from one factory           |
| `vehicle-events`      | `fleet/+/events/#`      | Events from every vehicle in the fleet |

Collections can overlap. A message from the Berlin factory can count toward both a factory collection and a company-wide collection. So you can look at the same traffic from several angles at the same time.

For each collection, EMQX counts:

- Messages received from publishers;
- Messages delivered to subscribers;
- Messages dropped;
- Data volume in and out.

The data volume counters are new. Message counts show how busy a device group is. Data volume shows how much bandwidth and storage that group really uses.

## Tenant-Aware Metrics: Everyone Sees Their Own Numbers



Many EMQX users run one cluster for several teams, business units, or customers. EMQX calls each of these groups a **namespace**. In EMQX 6.3, metrics respect namespaces from end to end:

- **Tenant administrators work on their own.** An administrator of one namespace can create topic metric collections for that namespace. These collections count only the messages of that namespace's clients. The administrator cannot see or change the collections of other namespaces.
- **Platform operators keep the full picture.** A global administrator can create collections that count traffic from every namespace. The global administrator can also view the collections of all namespaces.
- **Per-tenant traffic and drop statistics.** EMQX reports message traffic, sessions, and dropped messages for each namespace. You can see which tenant is growing and which tenant has delivery problems, without searching through logs.
- **Per-tenant data integration metrics.** Metrics for rules, actions, and connectors are now limited to the namespace of the person or tool that requests them. A tenant's monitoring system receives the tenant's own data and nothing else.

Two teams can even pick the same collection name in their own namespaces without a conflict. Every metric carries its namespace, so the numbers never mix.

## Built for the Tools You Already Use



Topic Metrics v2 and the per-tenant metrics are available in the standard Prometheus format. Add EMQX as a scrape target, and the data appears next to the rest of your infrastructure metrics. From there you can:

- Build Grafana dashboards per fleet, per site, or per customer;
- Chart message rates and data rates over time;
- Set alerts, for example, when a device group goes silent or when dropped messages rise for one tenant.

You can manage collections through the EMQX REST API. This makes them easy to create from scripts, provisioning pipelines, or your own portal. For example, you can create a collection each time you onboard a new customer or deploy a new product line.

## What You Can Do With It



- **Usage-based billing and chargeback.** Measure messages and data volume per customer or per business unit, and bill or allocate costs based on real use.
- **Capacity planning.** Track how each fleet, product, or tenant grows over time, and scale the cluster before growth becomes a problem.
- **Faster troubleshooting.** When messages are dropped, see at once which device group or which tenant is affected.
- **Service-level reporting.** Give each internal team or customer a dashboard of its own traffic, without giving it access to anyone else's data.
- **Fleet health monitoring.** Alert when a group of devices stops sending data, even when the cluster as a whole looks normal.

## Get Started



Topic Metrics v2 and tenant-aware metrics are available in EMQX 6.3. To try them:

1. Upgrade to or install EMQX 6.3.
2. Create a topic metric collection for a group of topics that matters to you.
3. Add the EMQX topic metrics endpoint to your Prometheus configuration and build a dashboard in Grafana.

The existing single-topic metrics page in the EMQX Dashboard continues to work, so you can adopt the new collections at your own pace.

Learn more in the documentation:

- [Topic Metrics](https://docs.emqx.com/en/emqx/latest/guides/observability/topic-metrics.html)
- [Integrate with Prometheus](https://docs.emqx.com/en/emqx/latest/guides/observability/prometheus.html)
- [Namespace Overview](https://docs.emqx.com/en/emqx/latest/guides/multi-tenancy/namespace-overview.html)

## Conclusion



A shared MQTT platform should give clear answers to every team that uses it. With Topic Metrics v2, you measure traffic by the groups that matter to your business, not only by single topics. With tenant-aware metrics, each team or customer sees its own numbers, and operators keep the full view of the cluster.

Download EMQX 6.3 today, or [contact our team](https://www.emqx.com/en/contact) to learn how EMQX can support your multi-tenant IoT platform.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
