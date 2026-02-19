This second article focuses on the foundation beneath EMQX: the Linux kernel, network stack, and Erlang VM. If [Part 1](https://www.emqx.com/en/blog/security-hardening-emqx-iot-messaging-systems-part-1) explained why security and reliability converge for a stateful MQTT broker, this part shows where that convergence actually bites in production: file descriptors, TCP behavior under load, firewall rules, and Erlang distribution security.

## **1. Operating System and Network Layer Hardening**

Before any MQTT packet reaches EMQX, the host operating system defines resource limits, networking behaviour, and the exposed attack surface. From an SRE’s perspective, the OS is the first line of defense against resource exhaustion and volumetric attacks, and a mis‑tuned kernel is often the real cause behind “random” broker failures.

- **OS Lifecycle Management:** Keep the operating system and kernel regularly patched with security updates. Do not deploy or retain end-of-life (EOL) OS releases in production environments.
- **Secure Administrative Access:** Restrict SSH access to trusted management networks, disable password authentication, and prohibit direct root login. All administrative access should be auditable.
- **Least-Privilege Execution:** Run EMQX as a dedicated, non-root user. Avoid unnecessary privileges and ensure filesystem and process permissions follow the principle of least privilege.

These baseline controls are assumed prerequisites for any production EMQX deployment and are not specific to the broker itself, but they materially impact its security and resilience characteristics.



### **1.1 Kernel Tuning for Connection Resilience and Anti-DoS**

In high-throughput IoT environments, the default Linux kernel settings are frequently the primary bottleneck during a volumetric Denial of Service attack or a legitimate "thundering herd" event (e.g., millions of devices reconnecting simultaneously after a power outage). A default Linux installation is typically tuned for general-purpose computing, not for handling millions of concurrent, long-lived TCP connections. Hardening the OS involves strictly tuning these parameters to ensure the broker can withstand surges without collapsing into a self-imposed denial of service.



#### **1.1.1 File Descriptor Limits and Process Constraints**

Every TCP connection accepted by EMQX consumes a file descriptor (FD) on the Linux host. If the system-wide limit (`fs.file-max`) or the user-specific process limit (`LimitNOFILE`) is reached, the operating system will fundamentally refuse to allocate new sockets. To an external observer or a monitoring system, this manifests exactly like a DoS attack: the service is running, but new connections are dropped immediately.

The requisite scale for EMQX production environments often exceeds standard limits by orders of magnitude. For a cluster expected to handle one million concurrent connections per node, the limits must be set well above this threshold to account for log files, inter-node communication sockets, and backend database connections.

- **System-Wide Limits:** The `fs.file-max` parameter in `/etc/sysctl.conf` dictates the maximum number of file handles the Linux kernel will allocate. For large-scale production, this should be set conservatively high, often recommended with two million.
- **Process-Level Limits:** The `fs.nr_open` parameter sets the ceiling for `limits.conf`. Critically, the systemd unit file for EMQX (`/usr/lib/systemd/system/emqx.service`) must explicitly override the default limit.
- **Recommendation:** Set `LimitNOFILE=2097152` (based on capacity planning) in the unit file. This ensures that the Erlang VM is permitted to open the necessary sockets.

| **Parameter** | **Location**     | **Recommended Value (1M Conns)** | **Description**                             |
| ------------- | ---------------- | -------------------------------- | ------------------------------------------- |
| fs.file-max   | /etc/sysctl.conf | 2,097,152                        | Total FDs allowed in the kernel.            |
| fs.nr_open    | /etc/sysctl.conf | 2,097,152                        | Max FDs a single process can *request*.     |
| LimitNOFILE   | emqx.service     | 2,097,152                        | The hard limit applied to the EMQX process. |

See EMQX documentation for more details [Performance Tuning (Linux) | EMQX Enterprise Docs](https://docs.emqx.com/en/emqx/latest/performance/tune.html) 



#### **1.1.2 TCP Stack Hardening and Connection Tracking**

Beyond simple capacity, the behavior of the TCP stack under load determines resilience. Attackers often exploit the state mechanisms of TCP, specifically the handshake and teardown phases, to exhaust server resources.

**SYN Flood Mitigation:**

The SYN flood is a classic DoS vector where an attacker sends a barrage of SYN packets but never completes the handshake (ACK). The server holds these "half-open" connections in a backlog queue, consuming memory.

- **Mitigation:** Enable SYN Cookies. When the backlog queue fills, the kernel will generate a cryptographic cookie in the sequence number, allowing it to drop the state entry while still responding to legitimate clients who can complete the handshake.

**Connection Tracking (Conntrack) Risks:**

If the EMQX cluster sits behind a stateful firewall or utilizes Kubernetes Service IPs (iptables/IPVS), the Linux connection tracking table (`nf_conntrack`) becomes a critical state store. If this table fills up, the kernel will drop packets for *new* connections, effectively severing the service.

- **SRE Insight:** In high-connection scenarios, the default nf_conntrack_max (often 65,536) is catastrophically low. It must be tuned to exceed the maximum expected concurrent connections plus a safety margin.
- **Optimization:** Reduce the `net.netfilter.nf_conntrack_tcp_timeout_established` value (default 5 days) to ensure that "dead" entries are purged more aggressively, freeing up slots in the table.



### **1.2 Network Segmentation and Firewall Strategy**

A robust security posture relies on the principle of network segmentation. EMQX operates with two distinct and fundamentally different classes of network traffic: **Client-to-Server** and **Node-to-Node**. These traffic types have vastly different security requirements and trust models, and they must be strictly isolated at the network level.



#### **1.2.1 Client-to-Server Traffic: The Public Perimeter**

This is the ingress traffic from IoT devices, mobile applications, or backend services connecting to the broker. The guiding principle here is "Minimum Exposure." Only the specific listener ports required for client connectivity should be exposed to the ingress network or Load Balancer.

- **Port 1883 (MQTT TCP):** The standard cleartext MQTT port. In a hardened production environment, this port should generally be disabled or strictly restricted to trusted internal networks (e.g., a backend microservice within the same VPC). Exposing cleartext MQTT to the public internet invites credential theft and data interception.
- **Port 8883 (MQTT SSL/TLS):** The primary production port. This is the only port that should be exposed via the Load Balancer to the public internet. It enforces encryption and prevents eavesdropping.
- **Port 8083 (WebSocket):** Used for browser-based clients.
- **Port 8084 (WebSocket SSL):** The secure variant for WebSockets.
- **Port 14567 (QUIC):** If utilizing MQTT over QUIC (UDP) for unreliable networks, this UDP port must be explicitly allowed.



#### **1.2.2 Node-to-Node Traffic: The Dangerous Internal Plane**

The most critical and frequently overlooked security vulnerability in EMQX deployments is the exposure of the Erlang distribution ports. This traffic represents the "brain" of the cluster—database replication (Mnesia), node discovery, and internal Remote Procedure Calls (RPC).

- **4370 (Erlang Distribution):** This port is used for the Erlang distribution protocol. It allows nodes to communicate, share state, and replicate the Mnesia database.
- **5369/5370 (Cluster RPC):** Used for EMQX's internal RPC mechanism (channel forwarding, session bridging). 5369 is the default port number used when running EMQX in docker, otherwise 5370.

**The Security Risk:** 

If port 4370 is exposed to the public internet or an untrusted user network, the security of the entire cluster is effectively nullified. The Erlang distribution protocol is powerful; it allows for remote code execution (RCE). An attacker who can connect to these ports and guess the "magic cookie" (discussed in Section 3) can execute arbitrary commands on the OS, dump the entire database (including ACLs and retained messages), or terminate the cluster.

**Firewall Strategy:**

These ports must be firewalled to allow traffic *only* from peer EMQX node IPs. For example, for port `4370`:

```
Rule: ALLOW TCP 4370 FROM <Cluster_Subnet> TO <Cluster_Subnet> Rule: DENY TCP 4370 FROM ANY
```

Same rules should be applied for port `5370`.

**Port Derivation Note:**

Ports **4370** and **5370** are the *base* ports used when EMQX node names do not include a numeric suffix. When a node name includes a numeric suffix, the effective listening ports are calculated as:

```
effective_port = base_port + node_suffix 
```

For example, a node named `node9@my.domain.net` will listen on ports **4379** and **5379**.

Firewall rules must therefore account for all derived ports corresponding to the node naming scheme in use, ensuring that **only cluster-internal IP ranges** are permitted.



#### **1.2.3 Interface Binding and Physical Isolation**

Default Erlang behavior often binds listeners to `0.0.0.0` (all interfaces). To strictly harden the node, we must force the Erlang VM to bind the distribution protocol strictly to the private network interface.

This is achieved using the `inet_dist_use_interface` kernel parameter in the vm.args configuration file. By specifying the IP address of the private interface (e.g., `10.0.1.5`), we ensure that even if the firewall fails, the distribution service is not listening on the public IP address.

**Configuration Example (vm.args):**

\## Bind Erlang distribution to the private interface IP only
-kernel inet_dist_use_interface {10,0,1,5}

*Note: The IP address is formatted as an Erlang tuple, using commas instead of dots.*

For Cluster RPC channel (5370), configure `rpc.listen_address = "10.0.1.5"`.



## **2. Erlang VM (BEAM) Layer Security**

EMQX is constructed upon the Erlang Virtual Machine (BEAM), a runtime famous for its fault tolerance and distributed capabilities. However, the very features that make Erlang powerful, transparent clustering and remote message passing, are built on a "high trust" model. Historically, Erlang clusters were assumed to run in secure, isolated environments. Hardening this layer is critical to defending against lateral movement and sophisticated insider threats.



### **2.1 The Magic Cookie: The Key to the Kingdom**

Erlang nodes authenticate with one another using a shared secret known as a "cookie." This is not a session cookie in the HTTP sense, but a persistent passphrase. If two Erlang nodes share the same cookie, they form a mesh and can execute code on each other.

**The Vulnerability:**

Default installations or example configurations often use a generic cookie like emqxsecret. If a production cluster is deployed with this default, any attacker who knows the default (which is public knowledge) can connect a rogue node to the cluster. Once connected, they have full control.

**Hardening Procedure:**

1. **Generation:** Generate a cryptographically strong, random string of at least 32 alphanumeric characters. High entropy is essential to prevent brute-force attacks against the handshake.
2. **Configuration:** Set this value in emqx.conf under node.cookie.
3. **Consistency:** Every node in the cluster *must* have the exact same cookie.
4. **File Permissions:** The configuration file containing the cookie (`emqx.conf`) contains a plaintext secret. It must be readable *only* by the emqx system user. Set file permissions to 400 or 600.



### **2.2 Securing Inter-Broker Communication**

By default, the critical inter-broker communication protocols, the Erlang distribution protocol (for Mnesia database replication on port `4370`) and internal Remote Procedure Calls (RPC, such as `gen_rpc` on ports `5369`/`5370`), are cleartext. While this maximizes performance, it presents a significant risk in Zero Trust environments. If an attacker captures traffic between nodes (e.g., via ARP spoofing), they can read sensitive data being replicated, such as retained messages, ACL rules, and user credentials.

**Implementation of TLS:**

To mitigate this, EMQX supports wrapping both the Erlang distribution and internal RPC protocols in TLS. The security relies on mutual TLS (mTLS), where each node authenticates to its peers using valid certificates. Follow the configuration guide: [Cluster Security | EMQX Enterprise Docs](https://docs.emqx.com/en/emqx/latest/deploy/cluster/security.html) 

**Performance Consideration:**

Encrypting Node-to-Node traffic introduces CPU overhead and latency to the replication stream. In a highly secure, physically isolated VPC, organizations might opt for cleartext for performance.



### **2.3 Static Erlang Distribution Port (EPMD Elimination)**

EMQX uses a static port for the Erlang distribution protocol (default is **4370**), which eliminates the need for the Erlang Port Mapper Daemon (EPMD) that traditionally runs on port 4369.

- **Benefit:** This creates a deterministic network profile, as the firewall only needs to allow port 4370 for Node-to-Node traffic.
- **Recommendation:** Since EMQX does not start EPMD, port 4369 is not critical to the cluster's function. However, as a security best practice, it should still be blocked externally to prevent any potential reconnaissance or minimize the scanning footprint of the host.



## Summary

With kernel limits sized for your connection profile, TCP and conntrack tuned for reconnection storms, network traffic cleanly segmented, and the Erlang distribution locked down, you have a defensible base for running EMQX at scale. These measures don’t eliminate all risk, but they dramatically reduce the chances that a noisy client, misconfigured firewall, or exposed internal port can take down your cluster.

In **Part 3**, we move up the stack to the protocol and control plane. We’ll look at how to configure TLS correctly, design practical authentication and authorization for millions of clients, secure the dashboard and APIs, and build disaster recovery procedures that let you recover quickly from incidents.
