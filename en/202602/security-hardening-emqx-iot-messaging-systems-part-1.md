This article is the first in a three-part series on hardening EMQX for large‑scale IoT production use. Here we frame security as a core reliability concern, explain why MQTT’s stateful nature changes the threat model, and end with a practical checklist you can apply directly to your own clusters.

## The Inseparable Link: Why Security is Reliability for MQTT

For a message broker like EMQX, the central nervous system of massive‑scale Internet of Things (IoT) deployments, security and reliability are inseparable. An unauthenticated connection flood that exhausts file descriptors or a malicious “cluster leave” command is not just a security incident—it is a reliability outage. Hardening an EMQX production cluster is therefore a prerequisite for high availability, not a compliance afterthought.

Unlike stateless web applications, MQTT is a stateful protocol that maintains long‑lived TCP connections, persistent session state, and retained messages for millions of devices. This dramatically enlarges the attack surface: an attacker can occupy sockets for days or exploit weaknesses in the underlying Erlang Virtual Machine (BEAM). Any realistic security architecture must therefore account for connection duration, resource limits, and state persistence.

Across this series, we examine four critical layers—Operating System and Network, Erlang VM, MQTT Protocol, and Administrative Interface—and tie them together with disaster recovery strategies. The goal is simple: ensure that when something goes wrong, your EMQX cluster degrades gracefully instead of failing catastrophically.

## **Establishing Defense in Depth: Comprehensive Security Checklist**



Before diving into the granular configurations in the subsequent articles, it is essential to establish a holistic view of your security posture. Security for an MQTT broker is not a single toggle but a series of overlapping layers.

The following Comprehensive Security Checklist serves as both an immediate self-assessment tool and a roadmap for this series. We recommend using this checklist as a "health check" to identify gaps in your current EMQX production environment before proceeding to the technical deep dives.

This checklist summarizes the strategic imperatives detailed above into an actionable format for SRE and Security Operations teams.

### **Phase 1: Infrastructure & OS**

- **Kernel Tuning:** fs.file-max and fs.nr_open set to > 2 million.
- **Service Limits:** LimitNOFILE=1048576 explicitly set in systemd unit file.
-  **TCP Hardening:** SYN Cookies enabled; connection tracking table size increased significantly.
- **Client-to-Server Firewall:** Ingress allowed only on ports 8883 (SSL) and 8084 (WSS). Port 1883 blocked or restricted to VPN.
- **Node-to-Node Firewall:** Ports 4370 and 5370 (or 5369 when running in docker) restricted strictly to internal Cluster IPs.
- **Interface Binding:** Erlang VM configured to bind distribution protocol only to the private network interface (inet_dist_use_interface).



### **Phase 2: Erlang & Cluster**

- **Cookie:** Default Erlang cookie is replaced with a high-entropy 32+ character random string.
- **File Permissions:** Config files containing secrets set to 400 (read-only by owner).
- **Inter-node Encryption:** ssl_dist enabled for TLS-encrypted database replication (Mandatory for Zero Trust/Public Cloud).



### **Phase 3: Transport (TLS)**

- **Protocol Versions:** TLS 1.0 and 1.1 explicitly disabled. TLS 1.2 and 1.3 enforced.
- **Cipher Suites:** Legacy CBC ciphers disabled. Modern AEAD suites (GCM/Poly1305) prioritized.
- **Certificates:** Valid CA-signed certificates installed. Verification depth (depth) configured to match CA hierarchy.
- **mTLS:** When mutual TLS is required, ensure `fail_if_no_peer_cert` is set to `true` so that EMQX enforces client certificate presentation during the TLS handshake and rejects connections where the client does not provide a certificate. Configure `verify` as `verify_peer` to ensure the client’s certificate chain is cryptographically validated against the configured trusted Certificate Authorities (CAs).
- **CRL (Certificate Revocation List):** Enable and maintain CRL checking to ensure that client certificates which have been revoked (e.g., due to compromise or decommissioning) are rejected during the TLS handshake. Regularly update CRLs and validate their availability to avoid accepting invalidated client credentials.
- **OCSP Stapling:** Enable OCSP stapling on the server side so that EMQX periodically fetches and staples certificate status responses from the CA. This allows clients to validate the server certificate’s revocation status without directly contacting the CA, reducing latency and preventing the use of revoked or compromised server certificates by attackers.



### **Phase 4: Application (MQTT)**

- **Authentication:** Configure at least one authentication backend.
- **Authorization:** ACLs enabled with a "Deny by Default" final rule.
- **Quotas:** Max packet size (e.g., 1MB) and topic levels (e.g., 10) restricted to prevent OOM/DoS.



### **Phase 5: Administration & Maintenance**

- **Dashboard:** Default admin password changed. HTTPS enabled.
- **Access:** Dashboard bound to localhost or restricted by VPN/Firewall.
- **Identity:** SSO (LDAP/OIDC) configured for staff access. MFA (TOTP) enforced for all admins.
- **API Keys:** Keys generated with strict scopes and expiration dates.
- **Backup:** Automated emqx ctl data export scheduled via cron. External certificates backed up separately.
- **Logs:** Audit logging enabled. Logs shipped to external SIEM (Splunk/ELK/Datadog) for anomaly detection.



## **What’s Next in This Series**

This checklist summarizes the overall security posture you should aim for, but each item hides important implementation details and trade‑offs. In **Part 2**, we’ll go deeper into the infrastructure aspects: how to tune the Linux kernel and TCP stack, design network segmentation, and harden the Erlang VM so that EMQX can safely sustain millions of concurrent connections. **Part 3** then covers TLS configuration, MQTT‑level authN/authZ, administrative security, and disaster recovery.

Stay tuned!
