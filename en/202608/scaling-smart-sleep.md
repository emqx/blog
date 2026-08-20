## Same MQTT Architecture, 80% Fewer Abnormal Disconnections



DeRucci makes connected beds, mattresses, and other smart sleep products used in homes around the world. With hundreds of thousands of devices in the field, MQTT has become a critical part of its IoT infrastructure, carrying device telemetry, heartbeats, and real-time commands between products and cloud services.

For years, DeRucci ran its production MQTT environment on EMQX Open Source. The platform had already proven itself, but running it was taking more and more of the team’s time.

As device volumes grew, so did the operational workload around cluster deployment, upgrades, capacity planning, and production support. The challenge was no longer whether EMQX could support the business; it was whether DeRucci's engineering team should keep spending its time running the MQTT infrastructure itself.

The answer was to move production workloads to EMQX Cloud. Rather than replacing a proven technology stack, DeRucci chose to keep the EMQX architecture it already knew while shifting infrastructure operations and production support to a managed cloud platform.

## Why DeRucci Chose EMQX Cloud



The goal was simple: **reduce infrastructure management overhead without disrupting the existing IoT architecture.**

Because DeRucci's device and backend applications were already built around EMQX, moving to an entirely different broker would have introduced unnecessary application and device-side changes.

EMQX Cloud offered a different path. By moving from self-hosted EMQX Open Source to a dedicated managed deployment, DeRucci could retain its existing MQTT-based architecture while gaining a fully managed production environment backed by EMQ's technical support and SRE expertise.

The migration was less a platform replacement than a shift in the operating model: from managing MQTT infrastructure internally to relying on EMQX Cloud for day-to-day infrastructure operations.

## A Low-Disruption Migration from EMQX Open Source



DeRucci's production environment carried years of accumulated configuration. Minimizing changes to existing devices and backend applications was a hard requirement.

The migration began with a detailed review of DeRucci's existing configuration, including authentication and authorization policies, listeners, session and message settings, retained messages, and other MQTT parameters.

EMQ's technical and SRE teams mapped business-critical settings to the managed environment and helped tune parameters for DeRucci's production workloads.

Rather than simply replicating every legacy setting, the migration provided an opportunity to simplify the configuration and adopt proven defaults where appropriate.

DeRucci moved its MQTT workloads without major changes to its device or backend applications.

## Turning Production Visibility into Better Reliability



The migration also changed how DeRucci approached troubleshooting in production.

In a connected-device environment, an "offline" device does not necessarily indicate a broker failure. The underlying cause could be a network interruption, a client-side reconnect, an application-level heartbeat issue, or a device that simply stopped sending MQTT traffic.

After moving to EMQX Cloud, the built-in deployment monitoring, logs, and Client ID-based tracing gave both DeRucci and EMQ's engineers a direct view of what was happening at the MQTT layer.

By tracing client connection activity, MQTT traffic, reconnects, and disconnects, the teams could tell whether a client had disconnected, reconnected, stopped sending heartbeats, or simply stopped producing MQTT traffic, instead of treating every "offline" device as the same problem.

![image.png](https://assets.emqx.com/images/03955f2c3e1978436b7b6b73a11878a3.png)

 

The analysis also revealed a scaling bottleneck in DeRucci’s architecture. Some backend MQTT clients were responsible for delivering messages to a large number of connected devices. As the device population grew, the traffic flowing through each connection increased significantly.

Because the deployment surfaced per-client traffic out of the box, the pattern showed up without anyone having to build monitoring for it. With the actual production profile in hand, rather than generic broker defaults, the EMQ team tuned the deployment to handle these high-throughput connections.

DeRucci came away with a clearer understanding of how its MQTT architecture behaved under real production loads, and where future bottlenecks could emerge as the business scaled.

## Measurable Improvements After Migration


![image.png](https://assets.emqx.com/images/7222b36b17949fcd2aa9d854e258c30c.png)

 

Following the migration and optimization work, DeRucci achieved measurable improvements in both reliability and message-handling capacity:

- **Approximately 80% fewer abnormal device disconnections during peak periods**
- **Around 3x higher message throughput per backend MQTT client**, providing additional headroom as device volumes increase
- **Greater confidence in device provisioning at scale, with connection behavior now observable end to end**

Rather than working out whether an issue originated from the device, network, MQTT client, or broker, DeRucci's engineers now work with the EMQ team to trace the communication path and find the cause.

## Preparing for the Next Stage of Device Growth



> "Our connected-device fleet continues to grow. We chose EMQX Cloud because it not only addresses our operational needs today, but can also scale with us as our device footprint expands."
>
> **— Xiaoyi Tan, Application Development Manager, DeRucci**

Derucci’s connected-device business continues to grow, bringing increasing MQTT connection counts as well as higher volumes of heartbeats, telemetry, and downstream messages.

What the migration surfaced is already shaping the next stage of architectural planning. One potential next step is to distribute downstream message delivery across multiple backend MQTT clients. This can spread the workload more evenly across connections and reduce the risk of any single connection becoming a throughput bottleneck.

At the platform level, EMQX Cloud gives DeRucci a simpler path to add capacity as its device fleet grows. EMQ can work with DeRucci to assess real workloads, plan capacity, and tune the deployment as requirements evolve.

This allows DeRucci to scale its connected-device business without having to expand its MQTT operations at the same pace.

## Running EMQX Yourself?



If your team is spending more time on cluster operations than on your product, EMQX Cloud lets you keep the architecture and hand off the infrastructure. [Talk to our team] about what a migration would look like for your workload.

## About DeRucci



DeRucci has been building healthy sleep systems since 2004, and today runs more than 5,200 retail stores across 11 countries. The company was listed on the Shenzhen Stock Exchange in June 2022 under ticker 001323.




<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
