We are thrilled to announce the private beta of **EMQX Fleets**, a managed IoT device management service on EMQX Cloud designed to help teams register, monitor, and control connected devices at scale. 

EMQX has long powered reliable MQTT connectivity for IoT deployments around the world. With EMQX Fleets, we're expanding the platform beyond messaging to provide a complete device management layer, helping teams manage device lifecycles through a unified, production-ready experience.

Whether you are operating ten devices or ten thousand, EMQX Fleets provides a structured foundation for managing device lifecycles with confidence.

## Why EMQX Fleets

Connecting devices is only the first step in building an IoT platform.

Running devices in production also requires capabilities such as device registration, state synchronization, remote control, fleet organization, and lifecycle management. While MQTT brokers excel at reliable messaging, these operational capabilities are often built separately, requiring significant engineering effort to develop and maintain.

EMQX Fleets is designed to close that gap.

Built on the EMQX ecosystem, it brings together device registry, device shadow, commands, jobs, dynamic grouping, and management APIs into a single managed platform. Instead of assembling multiple services or building custom infrastructure, teams can focus on delivering applications while EMQX Fleets provides the operational foundation for managing connected devices at scale.

## What You Can Do with EMQX Fleets: Core Features

### Register Devices with Thing Types

EMQX Fleets uses a **Thing Type** model where you define device schemas once and apply them across your fleet. A Thing Type specifies:

- **Properties**: device state attributes such as temperature, battery level, or lock state
- **Events**: operational notifications with severity levels such as info, warn, and error
- **Commands**: actions the cloud can invoke, including real-time and job-based operations
- **Connectivity**: MQTT and HTTP protocols, TLS settings, and keep-alive intervals

![image.png](https://assets.emqx.com/images/672f6612c88bd0fefd5586f7447a00c4.png)

Once defined, **Things** automatically inherit their type's schema. This reduces repetitive configuration and keeps similar devices consistent across the fleet.

![image.png](https://assets.emqx.com/images/9f8edf9ddc0ecbd26ed8408cc9be974f.png)

### Synchronize Device State with Device Shadow

The **Device Shadow** in EMQX Fleets maintains a three-state model for reliable state synchronization:

| State        | Direction       | Purpose                                      |
| :----------- | :-------------- | :------------------------------------------- |
| **reported** | Device to Cloud | What the device reports as its current state |
| **desired**  | Cloud to Device | What the cloud expects the device to become  |
| **delta**    | Auto-computed   | The difference between desired and reported  |

![image.png](https://assets.emqx.com/images/c497671b692f3e5d59bc94ea81a48400.png)

The workflow is straightforward:

1. The cloud updates the `desired` state through an API.
2. EMQX Fleets computes the delta between desired and reported state.
3. The delta is delivered to the device through MQTT.
4. The device applies the change and reports its new state.
5. When the delta is empty, the device is synchronized.

This pattern supports offline operation. Devices can reconnect, synchronize their shadow, and continue from the latest expected state without losing important changes.

### Search and Segment Device Fleets with Powerful Device Query

Finding specific devices in a large fleet is easier with the SQL-like query language in EMQX Fleets. Teams can search by metadata, connection status, or shadow properties using familiar operators.

```
# Find online thermostats reporting temperature > 25°C
thingTypeName:Thermostat AND temperature>25 AND status:online

# Find devices with pending configuration updates
hasDelta:true AND connected:true

# Find offline devices within the last hour
NOT status:online WITHIN LAST 1h
```

![image.png](https://assets.emqx.com/images/ddbe5655d0c8bf39ddcb4276eb05c14b.png)

Queries support numeric comparisons, boolean logic, existence checks, and time-window filtering, making it practical to segment devices for targeted operations.

### Control Devices with Commands and Jobs

EMQX Fleets provides two mechanisms for device control:

**Commands**: real-time request-response interactions with timeout handling, suited for immediate actions such as locking a door or rebooting a device.

![image.png](https://assets.emqx.com/images/a71d03d5269cf679e8213b92fb1de81e.png)

**Jobs**: fleet-wide operations dispatched to multiple devices. Jobs support:

- Snapshot or continuous execution modes
- Per-device execution tracking with status updates
- Automatic notification to devices when jobs are pending

![image.png](https://assets.emqx.com/images/6e7b7b75dfc3fedb5f49a04ca292e752.png)

The Jobs protocol handles unreliable networks by allowing devices to query pending jobs, start the next available task, and report execution progress.

### Organize Fleets with Tag-Driven Dynamic Groups

EMQX Fleets uses tags to organize devices and enable dynamic group membership:

- Tag devices with attributes such as `floor-1`, `temperature`, or `production`
- Create **Thing Groups** with tag filters, such as all devices with both `HVAC` and `floor-1` tags
- Update group membership automatically when tags change

![image.png](https://assets.emqx.com/images/82676324358c2c9c863bf2e385d72dce.png)

This approach scales better than manual group management because devices can join or leave groups based on their current tags.

## What Makes EMQX Fleets Different

Most IoT projects start with a MQTT broker and end up building device registry, state sync, and job scheduling from scratch. EMQX Fleets gives you all of that out of the box: one platform to register devices, keep their state in sync, find the ones you need, and send them commands or updates. You spend less time on infrastructure and more time on what your devices actually do.

## Typical Use Cases

EMQX Fleets is well suited for:

- **Smart Building Management**: control HVAC, lighting, and access systems across facilities
- **Industrial IoT**: monitor sensors, manage gateways, and coordinate firmware updates
- **Connected Products**: manage consumer devices with shadow state for a consistent user experience
- **Asset Tracking**: query and group devices by location, status, or custom attributes

## Join the Private Beta

The private beta of EMQX Fleets is available through EMQX Cloud. It is intended for teams that want to evaluate managed device lifecycle capabilities and provide early feedback before general availability.

1. Visit the [EMQX Fleets product page](https://www.emqx.com/en/cloud/emqx-fleets).
2. Request access to the private beta.
3. Work with the EMQX team to define your first Thing Type, register devices, and validate your fleet management workflow.

With EMQX Fleets, teams can move from device connectivity to structured fleet operations through a single managed experience.

## Summary

EMQX Fleets brings core IoT device management capabilities into a cohesive managed platform. With Device Shadow for state synchronization, flexible query capabilities for fleet operations, and command and job workflows for device control, it helps teams manage connected devices at scale without building every operational layer from scratch.

If you are building a smart building platform, an industrial monitoring system, or a connected product, EMQX Fleets can provide the device management foundation you need while your team focuses on application logic and business outcomes.

**Learn more and request private beta access:** https://www.emqx.com/en/cloud/emqx-fleets

<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
