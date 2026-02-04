We are excited to announce the release of **EMQX Edge 1.3.0**. This version introduces powerful new bridging capabilities, a more intuitive management experience through Dashboard updates, and important changes to our license policy and installation process.

## MQTT over QUIC Bridge

The standout feature of EMQX Edge 1.3.0 is the support for **MQTT over QUIC bridge.** This allows EMQX Edge to establish an MQTT channel with an upstream EMQX node using QUIC as the transport layer.

Compared to traditional TLS/TCP-based bridging, MQTT over QUIC offers:

- **Faster Connection Establishment:** Significant reduction in handshake overhead.
- **Enhanced Stability:** Superior performance in weak or unstable network environments.
- **Lower Latency:** Optimized delay characteristics for real-time edge-to-cloud communication.

### Configuration

You can set up a QUIC bridge via the Dashboard:

![image.png](https://assets.emqx.com/images/d0c8dbaa03aeda999dbb1802cad43e25.png)

 Or the configuration file:

```
bridges.mqtt.emqx_quic {
	server = "mqtt-quic://broker.emqx.io:14567"
	clientid="quic_bridge_client"
	keepalive = 60s
    #ssl {
    #    key_password = "yourpass"
    #    keyfile = "./etc/certs/client-key.pem"
    #    certfile = "./etc/certs/client-cert.pem"
    #    cacertfile = "./etc/certs/cacert.pem"
    #}
	forwards = [
		{
			remote_topic = "fwd/topic1"
			local_topic = "topic1"
		}
	]
	subscription = [
		{
			remote_topic = "cmd/topic3"
			local_topic = "topic3"
		}
	]
	quic_idle_timeout = 120s
	quic_keepalive = 120s
	quic_multi_stream = false
	quic_qos_priority = false
	quic_0rtt = true
}
```

**Key Configuration Highlights:**

- **Server Address:** Uses the `mqtt-quic://` protocol.
- **Security:** Configure encryption certificates via `keyfile`, `certfile`, and `cacertfile`.
- **Heartbeat Mechanism:** `quic_keepalive` defines the interval for transport-layer heartbeats, while `quic_idle_timeout` determines when the connection is disconnected.
- **Performance Toggles:** * `quic_qos_priority`: When enabled, MQTT QoS 1 and QoS 2 messages are prioritized.
  - `quic_0rtt`: Enables 0-RTT for faster reconnection.
  - `quic_multi_stream`: Toggle for multi-stream support.

For more details, please refer to: [MQTT over QUIC Bridge | EMQX Edge 1.3 Docs](https://docs.emqx.com/en/emqx-edge/v1.3/bridges/quic-bridge.html)

## Important Update: License Policy Changes

Version 1.3.0 introduces a new License Policy. Please take note of how expiration affects your running instances:

1. **Ongoing Connections:** If a license expires while EMQX Edge is running, existing MQTT connections will remain active as long as the service is not restarted.
2. **New Connections:** Once the license is expired, the system will **stop accepting new MQTT connections**.
3. **Restarts:** If you attempt to restart EMQX Edge with an expired license, the service will **fail to start**.
4. **Alerts:** Expiration warnings will now appear prominently in the Dashboard and will be recorded in the system logs.

For more information, please refer to: [License Policy | EMQX Edge 1.3 Docs](https://docs.emqx.com/en/emqx-edge/v1.3/license-policy.html) 

## Dashboard Improvement: Better Visualization and Security

The EMQX Edge Dashboard has been updated to version 0.0.6, bringing several user-experience improvements:

- **Optimized Bridge Interaction:** Setting up and managing MQTT over QUIC bridges is now more intuitive.

- [**Subscription Topic Tree View**](https://docs.emqx.com/en/emqx-edge/v1.3/monitor/topic-tree.html)**:** A new visual tool that allows you to see clients subscribed to specific topics. For instance, if `test_client_1` subscribes to `test/topic1`, it will be clearly mapped in the tree view.

  ![image.png](https://assets.emqx.com/images/db30574b30f42fddb432d65091c32826.png)

- **Enhanced Security:** Bridge passwords are now encrypted to improve overall system security.

- **License Alerts:** New pop-up notifications will alert you when a license has expired.

## Simplified Docker Installation

We have streamlined the Docker installation process. Starting with 1.3.0, the installation command no longer requires you to distinguish between different Instruction Set Architectures (ISA).

You can now use a unified command to pull and run EMQX Edge:

```shell
docker pull emqx/emqx-edge:<version>
docker run -d -it --name emqx-edge \
  -p 1883:1883 \
  -p 8081:8081 \
  -p 8083:8083 \
  -p 8086:8086 \
  -p 8883:8883 \
  emqx/emqx-edge:<version>
```

## Other Updates and Bug Fixes

1. Optimized the process of message resend.
2. Optimized the GitHub workflow.
3. Fixed missing UTF-8 string length validation when handling MQTT v3.1.1 SUBSCRIBE packets.
4. Updated the configuration file path in Docker image.
5. Fixed configuration errors related to SNI and SQLite.
6. Fixed memory address security issues in the WebSocket layer and Rule Engine.
7. Fixed an issue where QUIC bridge metrics did not work correctly.
8. Fixed an issue where the built-in MQTT client hook trigger kept reconnecting when ACL was enabled.
9. Fixed an error where Dashboard could not retrieve the QUIC bridge status after reloading.
10. Fixed an error when reading configuration items with millisecond (`ms`) units.
11. Fixed an issue where a null QUIC connection was closed during QUIC bridge reload.
12. Reset `max_ack_delay` to the default maximum value when an invalid value was configured.
13. Fixed incorrect QUIC bridge behavior when certificates were set to null.
14. Fixed an issue where the Dashboard failed to access `quic_handshake_timeout`.
15. Fixed an error when parsing a null encrypted password.
16. Fixed incorrect default values for some QUIC options.



<section class="promotion">
    <div>
        Try EMQX Edge for Free
    </div>
    <a href="https://www.emqx.com/en/try?tab=self-managed" class="button is-gradient">Get Started →</a>
</section>
