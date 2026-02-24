This final part assumes your infrastructure and Erlang VM are already hardened, as described in [Part 2](https://www.emqx.com/en/blog/security-hardening-emqx-iot-messaging-systems-part-2). We now move to the layers most SREs and security teams interact with day‑to‑day: TLS termination, MQTT‑level authentication and authorization, administrative access, and disaster recovery.

The network and OS hardening from previous parts protect the host, but they don’t answer the questions “Who is this client?” and “What may it do?” Nor do they guarantee you can safely recover from a compromise or disaster. Getting these application and operational controls right is what turns EMQX into a dependable messaging backbone rather than a fragile single point of failure.



## **1. Transport Layer Security (TLS): The First Line of Defense**



For an MQTT broker, the Transport Layer is the primary boundary between the public internet and the internal application logic. Transport Layer Security (TLS) ensures confidentiality (encryption), integrity (prevention of tampering), and authenticity (verification of the server). In a production environment, TLS is non-negotiable for all public-facing traffic.



### **1.1 Protocol Version Hardening**

The history of SSL/TLS is littered with broken protocols. SSL v3, TLS 1.0, and TLS 1.1 are cryptographically broken and vulnerable to attacks like POODLE and BEAST. EMQX listeners must be explicitly configured to reject connections attempting to negotiate these legacy versions.

**Requirement:** Enforce TLS 1.2 and TLS 1.3 exclusively.

- **TLS 1.3 Advantages:** TLS 1.3 offers significant performance and security improvements. It reduces the handshake latency (1-RTT vs 2-RTT in TLS 1.2), which is crucial for IoT devices connecting over high-latency cellular networks. It also removes support for older, insecure cipher suites entirely.



### **1.2 Cipher Suite Selection and Forward Secrecy**

The strength of a TLS connection is determined by the cipher suite negotiated during the handshake. Weak cipher suites allow attackers to decrypt traffic retrospectively if they later compromise the private key.

**Cipher Suite Criteria:**

1. **Forward Secrecy (FS):** Prioritize Ephemeral Diffie-Hellman (DHE/ECDHE) key exchange. This ensures that a unique session key is generated for every connection. Even if the server's long-term private key is stolen, past sessions cannot be decrypted.
2. **AEAD (Authenticated Encryption with Associated Data):** Use GCM (Galois/Counter Mode) or Poly1305. Avoid CBC (Cipher Block Chaining) modes, which are susceptible to padding oracle attacks.

**Recommended Cipher Suites (TLS 1.3):**

- `TLS_AES_256_GCM_SHA384`
- `TLS_AES_128_GCM_SHA256`
- `TLS_CHACHA20_POLY1305_SHA256` (Preferred for mobile/low-power devices lacking AES hardware acceleration).

**Recommended Cipher Suites (TLS 1.2):**

- `ECDHE-ECDSA-AES256-GCM-SHA384`
- `ECDHE-ECDSA-AES128-GCM-SHA256`
- `ECDHE-RSA-AES256-GCM-SHA384`
- `ECDHE-RSA-AES128-GCM-SHA256`
- `ECDHE-ECDSA-CHACHA20-POLY1305`
- `ECDHE-RSA-CHACHA20-POLY1305`

| **Cipher Category** | **Examples**               | **Status**   | **Reason**                               |
| ------------------- | -------------------------- | ------------ | ---------------------------------------- |
| **Modern (AEAD)**   | AES-GCM, ChaCha20-Poly1305 | **Required** | Secure, efficient, authenticated.        |
| **Legacy (CBC)**    | AES-CBC, 3DES              | **Avoid**    | Vulnerable to Padding Oracles (Lucky13). |
| **Weak/Broken**     | RC4, DES, NULL             | **Prohibit** | Cryptographically broken.                |

Table: Recommended vs. Legacy Ciphers



### **1.3 Certificate Management and Verification Depth**

The handling of X.509 certificates is a common source of operational failure.

- **Chain of Trust:** The `certfile` configured in EMQX must contain the full chain: the Server Certificate followed by any Intermediate CA certificates. The `cacertfile` should contain the Root CA.
- **Verification Depth:** If the client certificate (used for mTLS) is issued by a sub-intermediate CA, the default verification depth of 1 will cause handshake failures. The depth parameter in ssl_options must be increased (e.g., to 2 or 3) to allow the broker to traverse the chain up to the Root CA.
- **Hot Reloading:** EMQX supports the hot reloading of certificates every 2 minutes, or an immeidate reloading via the `emqx ctl pem_cache clean` command. This is critical for SRE operations: certificates must be rotated before expiration without restarting the broker and dropping millions of connections.



## **2. MQTT Application Layer Security**

While the network and transport layers secure the *pipe*, the Application Layer secures the *data* and the *access*. This layer answers two fundamental questions: "Who are you?" (Authentication) and "What are you allowed to do?" (Authorization).



### **2.1 Authentication (AuthN): Strategies and Architectures**

Default EMQX installations have no authentication chain configured. This setting allows any client to connect without credentials. In a production environment, at least one authentication backend should be configured (a non-empty chain).



#### **2.1.1 Mechanism Selection: The SRE Trade-off**

Choosing an authentication mechanism is a trade-off between security, complexity, and latency.

**X.509 Certificate Authentication (mTLS):**

- **Mechanism:** The client presents a client-side certificate during the TLS handshake. EMQX extracts the Common Name (CN) or a SAN field and uses it as the identity.
- **Pros:** Extremely secure. Authentication happens at the transport layer, so unauthenticated packets never reach the MQTT application processor. Offloads CPU work to SSL accelerators if available.
- **Cons:** High operational complexity. Requires a robust Public Key Infrastructure (PKI) to issue and revoke certificates for millions of devices. Certificate Revocation Lists (CRLs) must be managed.

**CInfo (Client Information) Auth:**

- **Mechanism:** Rule-expression–based validation of client-provided metadata and connection context during the MQTT CONNECT phase. Typical checks include enforcing consistency between fields such as Client ID, username, and TLS attributes (e.g., verifying that the MQTT Client ID matches the X.509 certificate Common Name or a SAN entry).
- **Pros:** Extremely lightweight and performant, as it relies on local rule evaluation without cryptographic operations or external lookups. Highly composable and can be placed at the front of the authentication chain to rapidly reject malformed or inconsistent CONNECT attempts, reducing load on downstream authenticators and protecting broker resources.
- **Cons:** Not a standalone authentication mechanism. Provides validation and policy enforcement rather than cryptographic identity proof, and therefore must be combined with a primary authentication method (e.g., mTLS, JWT, or password-based authentication) to establish trust.

**JWT (JSON Web Tokens):**

- **Mechanism:** The client sends a signed JWT in the password field. EMQX validates the cryptographic signature using a locally stored public key.
- **Pros:** Stateless and fast. The broker does not need to query a database for every connection, reducing latency and database load. Ideal for massive scale.
- **Cons:** Token revocation is difficult before expiry. If a token is stolen, it is valid until it expires.
- **Hardening:** Use short expiry times (e.g., 2 hour) and force clients to refresh tokens. Use strong signing algorithms (ES256 or RS256) rather than shared secrets (HS256). Configure EMQX to force disconnect after token expire.

**Built-in DB (Password) Auth:**

- **Mechanism:** The client provides a username and password in the MQTT CONNECT packet. EMQX authenticates the client by validating the password against its internal user database, which stores credentials as cryptographic hashes. Identity is derived from the username or client ID, depending on configuration.
- **Pros:** Simple and well-understood authentication model; Comes with a UI aid in the dashboard for easy management; In memory lookup provides great performance; Easy to bootstrap (using a bootstrap file in CSV or JSON format).
- **Cons:** When there are millions of records, holding such amounts of data in memory may impact the system’s overall capacity.

**HTTP server Auth:**

- **Mechanism:** During the MQTT CONNECT phase, EMQX forwards client credentials (such as username, password, client ID, or TLS metadata) to an external HTTP authentication service. The service performs custom authentication logic (e.g., database lookup, policy checks) and returns an allow/deny decision to EMQX.
- **Pros:** Highly flexible and extensible. Authentication logic can be fully customized and integrated with existing identity systems, device registries, or IAM platforms. Enables centralized credential management, dynamic policy evaluation, and immediate revocation. Well-suited for complex enterprise environments and heterogeneous authentication requirements.
- **Cons:** Adds latency to every connection due to synchronous HTTP calls. Introduces a runtime dependency on an external service, creating an additional failure domain. Scalability is limited by the performance and availability of the HTTP auth backend, requiring careful capacity planning and horizontal scaling at high connection rates.

**External Database-Backed (Password) Auth:**

- **Mechanism:** EMQX queries an external database (PostgreSQL, MySQL, Redis) to verify the username and password hash.
- **Pros:** Centralized user management. Easy to revoke access immediately (just delete the row).
- **Cons:** Adds latency (network round-trip to DB) to the connection phase. The database becomes a single point of failure and a bottleneck during reconnection storms.



#### **2.1.2 Flapping Detection**

Malicious or malfunctioning clients may enter a rapid cycle of connecting and disconnecting. This "flapping" consumes CPU resources for handshakes and generates massive log volumes.

- **Feature:** Enable flapping_detect in EMQX.
- **Policy:** Configure it to automatically ban clients that exceed a specific threshold (e.g., 15 disconnects per minute). This proactively removes noise and protects the authentication backend from saturation.



### **2.2 Authorization (AuthZ): Granular Access Control**

Authentication grants access to the building; authorization determines which rooms (topics) a client can enter.



#### **2.2.1 The Principle of Least Privilege**

A compromised IoT device should not be a gateway to the entire network.

- **Publishing:** A client should only be permitted to publish to topics strictly relevant to its function, typically scoped by its Client ID (e.g., `devices/{clientid}/telemetry`).
- **Subscribing:** A client should only subscribe to its own command topics (e.g., `devices/{clientid}/commands`).
- **Wildcards:** Use of wildcard subscriptions (`#` or `+`) must be heavily restricted. A compromised device subscribing to # (all topics) effectively creates a data leak of the entire cluster's traffic.



#### **2.2.2 ACL Architectures**

- **File-Based (acl.conf):** Best for static, global rules. Use this to enforce "Deny by Default" and to block access to system topics ($SYS/#) for standard users.
- **Authentication-Returned:** HTTP authentication response and JWT tokens may contain an ‘acl’ field to include the ACL rules dedicated to the current client.
- **Database-Based:** Required for dynamic, per-device policies.
- **Variable Interpolation:** EMQX supports placeholders in ACL rules (e.g., ${clientid} for Client ID). This allows for a single rule row in the database—ALLOW publish devices/${clientid}/events—to enforce security for millions of devices without creating millions of ACL rows. This is a critical optimization for database performance.



### **2.3 Quotas and Rate Limiting**

To prevent a single compromised or buggy client from degrading the service for others, resource quotas act as a form of internal firewall.

- **Max Packet Size:** Limit mqtt.max_packet_size. The default is often 1MB. Allowing huge packets (e.g., 256MB) is a risk; parsing a massive payload consumes significant RAM and can trigger Out-Of-Memory (OOM) kills or long Garbage Collection (GC) pauses in the Erlang VM.
- **Topic Levels:** Limit the depth of topic hierarchies (e.g., max 10 levels). Deep topic trees increase the complexity of the routing trie lookups.
- **Message Rate:** Apply rate limits (messages/second) per client to prevent message flooding.



## **3. Administrative Interface Security (Dashboard & API)**

The EMQX Dashboard (typically port 18083) and the HTTP API provide full control over the cluster. They allow for user creation, rule changes, and node shutdown. Securing this control plane is paramount.



### **3.1 Network Exposure and Listeners**

- **Binding:** By default, the dashboard may bind to 0.0.0.0. Change dashboard.listeners.http.bind to 127.0.0.1 if you plan to access it only via an SSH tunnel or a local reverse proxy.
- **HTTPS Enforcement:** If the dashboard must be accessible over a network, enable the HTTPS listener (dashboard.listeners.https) and disable the HTTP listener entirely. Provide valid certificates to prevent Man-in-the-Middle attacks on admin credentials.



### **3.2 Authentication and Identity Management**

- **Default Credentials:** The most common vulnerability is leaving the default admin / public credentials active. These must be changed immediately upon installation.
- **Single Sign-On (SSO):** In enterprise environments, local user management is an anti-pattern. It leads to orphaned accounts when employees leave. Integrate EMQX with an external Identity Provider (IdP) using LDAP, SAML, or OIDC (e.g., Microsoft Entra ID, Okta). This ensures that access to the broker is automatically revoked when a user is disabled in the central directory.
- **Configuration:** This involves configuring the dashboard.sso block in base.hocon to map IdP attributes to EMQX roles (Administrator vs Viewer).



### **3.3 Multi-Factor Authentication (MFA)**

Even with strong passwords, credentials can be phished. MFA adds a critical layer of defense.

- **Implementation:** Enable TOTP (Time-based One-Time Password) for dashboard access.
- **Configuration:** Set dashboard.default_mfa = {mechanism: totp}. Administrators can then enforce MFA enrollment for all users via the UI (System -> Users -> MFA Settings). This ensures that an attacker needs both the password and the physical token device to gain administrative access.



### **3.4 API Key Governance**

The HTTP API uses Basic Auth (AppID and Secret) for programmatic access.

- **Lifecycle Management:** Do not use the superuser account for CI/CD scripts or monitoring tools. Generate dedicated API keys for each integration.
- **Expiration:** Set expiration dates for API keys (api_key.expired_at) to force periodic rotation.
- **Least Privilege:** Assign roles strictly. A monitoring script usually only needs "Viewer" permissions, not "Administrator."



## **4. Disaster Recovery (DR) and Business Continuity**

In SRE, security includes availability. If a security incident (e.g., ransomware or data corruption) occurs, the ability to restore the system is the ultimate fail-safe.



### **4.1 Backup Strategies: The v5 Paradigm Shift**

EMQX v5 introduced a major change in backup formats. The old JSON export of v4 is replaced by a tar.gz archive.

- **Data Export (emqx ctl data export):** This is the primary hot backup mechanism. It captures the global configuration, Mnesia database content (users, ACLs, rules), and certificates *that are stored within the data directory*.
- **Critical Gap:** A common pitfall is that data export **does not** capture certificates stored outside the data/ directory (e.g., in /etc/ssl/certs). SREs must ensure that external certificate paths are backed up via standard filesystem snapshots or configuration management tools (Ansible/Terraform).
- **Retained Messages:** In versions 5.7+, RAM-only retained messages are included in backups. This is vital for restoring the "state" of the IoT system (e.g., the last known status of every sensor) after a cluster rebuild.



### **4.2 Node Evacuation**

In the event of a security incident—such as a suspected OS compromise on a specific node—SREs must isolate the threat without causing a total outage.

- **Mechanism:** EMQX supports "Node Evacuation." When triggered, the node stops accepting new connections and actively disconnects existing clients, sending them a redirect code (in MQTT 5.0) or simply closing the socket to force a reconnect.
- **Result:** Clients automatically migrate to healthy nodes in the cluster via the Load Balancer. The compromised node is drained of traffic and can be safely taken offline for forensic analysis or re-imaging.



### **4.3 Cross-Region Strategy**

Mnesia (the internal database) requires low-latency networking. Spanning an EMQX cluster across high-latency WAN links (e.g., US-East to EU-West) is architecturally unsound and will lead to cluster partition.

- **Cluster Linking:** A native EMQX feature that establishes efficient, bidirectional message forwarding between separate EMQX clusters using MQTT connections optimized for EMQX-to-EMQX communication. Unlike traditional MQTT bridging, Cluster Linking forwards only relevant topics based on real-time subscriptions, reducing bandwidth usage and improving resilience to intermittent WAN connectivity while maintaining a unified logical namespace across regions. 
- **MQTT Bridging:** A manual MQTT bridge configuration where EMQX acts as an MQTT client to another broker (including other EMQX clusters). Bridging forwards configured topic filters but replicates all matched messages regardless of actual subscription state, which can increase bandwidth utilization and latency compared to Cluster Linking.



## **5. Wrapping up**

Across this series, we have treated EMQX security as a multi‑layer SRE problem rather than a checklist of isolated settings:

- **[Part 1](https://www.emqx.com/en/blog/security-hardening-emqx-iot-messaging-systems-part-1)** framed the reliability–security trade‑off and provided a high‑level checklist.
- **[Part 2](https://www.emqx.com/en/blog/security-hardening-emqx-iot-messaging-systems-part-2)** showed how Linux, network design, and the Erlang VM determine whether EMQX survives real‑world load and attack patterns.
- **Part 3** has focused on TLS, client authentication and authorization, administrative hardening, and disaster recovery.

The specific configuration values will vary by environment, but the principles do not: minimize exposed surfaces, enforce strong identity at every boundary, limit the blast radius of any single client or credential, and design for fast, predictable recovery. If you apply those principles consistently, EMQX can operate as a hardened, reliable core of your IoT platform rather than its most fragile dependency.
