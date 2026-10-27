## Introducing Feature Gates in EMQX 6.3

An MQTT broker deployed on an edge gateway must share resources with the applications running alongside it. Data collection, local processing, and storage all compete for memory and compute, making the broker’s resource footprint an important consideration.

Consider a gateway where a data collector publishes measurements over MQTT, local applications consume them, and a separate service handles storage and upstream communication. The broker needs to provide reliable message routing and access control, but capabilities such as database connectors and a web-based management console may be unnecessary in this deployment.

With [EMQX Enterprise 6.3](https://www.emqx.com/en/blog/emqx-6-3-0-release-notes), **Feature Gates** let you control which capabilities start with the broker. The **ESSENTIAL** preset starts EMQX with core MQTT functionality, authentication, and authorization, while leaving optional applications stopped by default. This provides a leaner starting footprint for resource-constrained deployments without requiring a separate EMQX distribution.

## What ESSENTIAL Mode Keeps Running

ESSENTIAL mode is designed for deployments that need the core MQTT broker without the full set of EMQX applications. The table below shows which capabilities remain available and which are disabled by default. This helps you decide whether ESSENTIAL fits your deployment.

| Capability                                         | ESSENTIAL mode |
| :------------------------------------------------- | :------------- |
| Core MQTT broker, authentication and authorization | Available      |
| Retained messages, configuration system and CLI    | Available      |
| Dashboard and management REST API                  | Disabled       |
| Rule engine, connectors and data bridges           | Disabled       |
| Prometheus exporter, non-MQTT gateways and plugins | Disabled       |

Core applications remain available with every feature selection. Optional capabilities can be included through a custom selection when the deployment needs them.

For the gateway in our example, applications can continue publishing and subscribing over MQTT, with authentication and topic permissions configured as needed. Without the Dashboard or management REST API, administrators manage the broker through configuration files, logs and the CLI.

## Why the Footprint Gets Smaller



### Code Loads When It Is Needed



Stopping optional applications removes part of their runtime overhead. ESSENTIAL also tells the Erlang VM to load modules as they are needed, instead of preloading all modules in the release. Code for unused features can stay on disk, reducing resident memory. EMQX selects this code-loading behavior automatically for the ESSENTIAL preset.

### Less Background Work per Connection



EMQX 6.3.0 also skips periodic per-connection statistics reporting used solely by the Dashboard's client-information API when that capability is disabled. With the Dashboard disabled, this removes background work that would otherwise repeat across connections.

ESSENTIAL mode brings the **idle boot memory footprint below 100 MB**. Connections, TLS, subscriptions and queued messages require additional memory, and the runtime environment affects the result.

For a shared gateway, measure the broker alongside the other applications with representative traffic. Include slow subscribers and reconnects in the workload; a quiet startup measurement cannot establish the memory limit for a busy deployment.

## Start with ESSENTIAL



Set the following environment variable for the EMQX process before it starts:

```
export EMQX_FEATURES=ESSENTIAL
```

For Docker Compose or Kubernetes, put the variable in the broker's deployment definition. For an RPM or DEB installation, it can be persisted in `/etc/emqx/emqx.env`:

```
EMQX_FEATURES=ESSENTIAL
```

EMQX reads this file before `emqx.conf`. Its assignments override inherited environment values, so keep the two consistent. Restart the node after changing the selection.

Check the `feature_gates_resolved` startup log entry for the resolved preset and enabled and disabled feature lists. In ESSENTIAL mode, use the log rather than calling the management API, which is disabled.

## Try It with a 100 MiB Docker Limit



This local test starts EMQX 6.3.1 with one CPU, a 100 MiB memory limit and no swap, then exchanges a QoS 1 message using MQTTX CLI. Use Docker with Linux containers and install [MQTTX CLI](https://mqttx.app/docs/cli/downloading-and-installation) on the host, so the clients run outside the broker's memory limit. The MQTT port is published only on localhost.

Start a fresh container:

```
docker run -d --name emqx-essential-demo \
  --cpuset-cpus=0 --cpus=1 \
  --memory=100m --memory-swap=100m \
  --restart=no --no-healthcheck \
  -e EMQX_FEATURES=ESSENTIAL \
  -p 127.0.0.1:1883:1883 \
  emqx/emqx-enterprise:6.3.1
```

The broker starts in the background. If port 1883 is occupied, choose another host port and use it in both MQTTX commands below.

Docker interprets `100m` as **100 MiB**, approximately 104.9 MB. Equal `--memory` and `--memory-swap` values disable container swap. The CPU settings restrict execution to logical CPU 0 with a one-CPU time quota.

Keep the live memory display open in this terminal:

```
docker stats \
  --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}' \
  emqx-essential-demo
```

In a second terminal, subscribe at QoS 1:

```
mqttx sub -h 127.0.0.1 -p 1883 -t essential/demo -q 1
```

Wait for MQTTX to report `Subscribed to essential/demo`. This confirms the broker is ready and the subscription is active. Then publish from a third terminal:

```
mqttx pub -h 127.0.0.1 -p 1883 -t essential/demo -q 1 \
  -m 'Hello from ESSENTIAL'
```

The subscriber displays:

```
topic: essential/demo, qos: 1
Hello from ESSENTIAL
```

In a local Linux ARM64 run, Docker reported about 90 MiB just after startup and 84–85 MiB afterward with the subscriber connected. 

```
NAME                  CPU %     MEM USAGE / LIMIT
emqx-essential-demo   0.15%     85.76MiB / 100MiB
```

The broker completed the exchange with no swap, OOM kills or container restarts. [Docker's memory display](https://docs.docker.com/reference/cli/docker/container/stats/) subtracts inactive file cache; the kernel's total memory peak reached the 100 MiB cap. Use this as a startup and message-delivery check, and size a production deployment with representative traffic.

Stop the subscriber and memory display with Ctrl-C, then remove the demo container and its anonymous data and log volumes:

```
docker stop emqx-essential-demo
docker rm -v emqx-essential-demo
```

## Add the Capabilities the Deployment Needs



Suppose the gateway now needs to send telemetry directly from EMQX to a database. Enable data integration with:

```
export EMQX_FEATURES=data_integration
```

After restarting with this setting, EMQX starts the core broker plus the rule engine, connectors, actions and sources. It also enables the required `schema_registry` feature automatically. Dashboard and Prometheus export remain disabled. Configure the database connector and the rule that sends messages to it separately.

The same mechanism supports a broker that needs remote administration or Prometheus monitoring:

| Deployment requirement                                       | `EMQX_FEATURES` value                |
| :----------------------------------------------------------- | :----------------------------------- |
| Core MQTT and access control                                 | `ESSENTIAL`                          |
| Core capabilities plus data integration and its schema registry dependency | `data_integration`                   |
| Core capabilities plus Dashboard and REST API                | `dashboard`                          |
| Core capabilities plus Prometheus export and its Dashboard dependency | `metrics`                            |
| Data integration, Dashboard and Prometheus export            | `dashboard,data_integration,metrics` |
| All available features                                       | `FULL`                               |

Dependency resolution also applies to monitoring: selecting `metrics` enables `dashboard` automatically. Authentication and authorization remain part of the core in every row.

Use either a preset or a list of feature names. `ESSENTIAL,metrics` is invalid; use `metrics` to get the core broker with that optional capability and its dependencies. An invalid selection prevents startup. If `EMQX_FEATURES` is unset or empty, EMQX uses `FULL`.

The automatic on-demand code-loading default applies specifically to `ESSENTIAL`; custom lists do not inherit it automatically. Measure each custom selection under its intended workload to establish its memory requirements.

## Keep Feature Selection in the Deployment Definition



Feature Gates are deployment settings. Changing the selection requires a restart, and the Dashboard, REST API and CLI cannot change it at runtime. Keep the same selection on every node in a cluster so that management endpoints and background applications are consistent.

That makes feature selection a useful part of deployment review. A proposed database integration now includes an explicit change to the broker's enabled capabilities, along with its connector configuration and resource requirements. The team can test those together before rollout.

For a gateway whose broker handles local MQTT traffic, ESSENTIAL mode provides a focused starting point. When its responsibilities expand, a custom selection makes those additions explicit. Start with the capabilities the application needs, measure them under its workload, and keep that choice in the deployment configuration.

For the full feature list and deployment details, see the [Feature Gates documentation](https://docs.emqx.com/en/emqx/latest/get-started/deploy/feature-gates.html).

Try EMQX Enterprise 6.3 today: [Download EMQX Enterprise](https://www.emqx.com/en/downloads-and-install/enterprise) 




<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
