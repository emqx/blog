## Introduction

The web is constantly evolving, demanding faster and more reliable connections. In recent years, the QUIC protocol has emerged as a game-changer, offering significant improvements over traditional TCP/IP for web traffic. QUIC boasts features like congestion control, reduced latency, and improved security, making it a compelling choice for modern mobile applications.

However, with great power comes great responsibility. As QUIC adoption grows, efficiently managing high traffic volumes becomes crucial. Traditional load balancing methods, often designed for TCP/IP, struggle with QUIC's multiplexing nature. This can lead to bottlenecks and hinder the full potential of QUIC.

This blog post dives into the world of QUIC load balancing and explores a powerful solution: leveraging XDP (eXpress Data Path) and IPVS (IP Virtual Server) for efficient traffic distribution. We'll explore the challenges of QUIC load balancing, how XDP and IPVS work together, and the benefits of this approach. Additionally, we'll discuss the concept of direct routing and its potential integration within this framework.

By the end of this blog, you'll gain a comprehensive understanding of how to unlock the full potential of QUIC through efficient load balancing with XDP, IPVS, and potentially, direct routing. Buckle up, and let's explore the future of QUIC traffic management.

## Challenges of Load Balancing QUIC

Traditional load balancers face a few hurdles when dealing with QUIC which is UDP based:

- **Connection ID Conundrum:** QUIC utilizes connection migration, where both client and server can dynamically change their connection IDs. This disrupts the load balancer's ability to consistently track and manage connections, potentially leading to dropped connections or uneven traffic distribution.
- **NAT Nuisance:** Network Address Translation (NAT) can further complicate QUIC load balancing. When a client behind a NAT device establishes a QUIC connection, the source IP address might change during connection migration. This confuses the load balancer, as it relies on a consistent source IP to identify the client and route traffic appropriately.
- **Limited Visibility:** Traditional load balancers typically rely on the "4-tuple" for traffic management (source IP, source port, destination IP, and destination port). Since QUIC runs on UDP, many load balancers treat it as basic UDP traffic. This **limits their visibility** into the multiplexed streams within a single QUIC connection. As a result, the 4-tuple alone might not be sufficient for optimal traffic distribution based on individual data streams.

### What is a QUIC Connection ID and Why is it Important?

Unlike traditional TCP connections that rely on the 4-tuple (source IP address, source port, destination IP address, and destination port) for identification, QUIC utilizes a unique identifier called the Connection ID (CID). This CID is a randomly generated value embedded within the QUIC packet header.

The CID offers several advantages over the traditional 4-tuple approach:

- **Persistence through Address Changes:** A critical benefit of the CID is its persistence. Unlike the source IP address in the 4-tuple, which can change due to Network Address Translation (NAT), the CID* remains constant throughout the lifetime of a QUIC connection. This persistence allows both the client and server to maintain a seamless connection even if the client's IP address changes. 

> According to the QUIC protocol, even though the CID may be dynamically updated multiple times during the life cycle of the connection, the client and server still have a consensus on the CID currently in use. This consensus remains unchanged throughout the life cycle of the QUIC connection.

- **Multiplexing Efficiency:** QUIC is designed for multiplexing, supporting multiple data streams within a single connection. The CID plays a crucial role in enabling the receiver (client or server) to efficiently identify and demultiplex incoming packets, directing them to the appropriate data stream within the connection.
- **Improved Security:** The random nature of the CID makes it difficult for attackers to predict and forge packets belonging to a specific QUIC connection. This enhances the overall security of the communication.

### Classic Problem: The NAT Wall and QUIC Connection Disruption

Many users connect to the internet through Network Address Translation (NAT) gateways. This creates a hidden nature for the client's true IP address, as the client communicates using the public address assigned by the NAT. This scenario creates a challenge for QUIC load balancing with traditional methods that rely solely on the 4-tuple (source IP, source port, destination IP, and destination port).

Here's how the problem unfolds:

1. **Initial Handshake:** A client behind a NAT establishes a QUIC connection with the server. The load balancer,unaware of QUIC specifics, uses the 4-tuple to direct the traffic to a real server (let's call it server1).

2. **Stable Connection (as long as NAT binding persists):** As long as the 4-tuple remains the same (including the client's source port) and the NAT binding is maintained, subsequent traffic from the client continues to be directed to server1.

   ![Initial Handshake](https://assets.emqx.com/images/cdd3bec31e12a01c3a7b6be2316ed114.png)

3. **NAT Binding Disruption:** However, the client's source port assignment by the NAT can change due to two reasons:

   1. **Inactive Traffic Timeout:** If there's a period of inactivity in the connection, the NAT might reassign the client's source port, altering the 4-tuple.

   2. **Client Network Change:** If the client moves to a different network, it will be assigned a new public IP address, again affecting the 4-tuple.

      ![Address Migration LB has no QUlC awareness](https://assets.emqx.com/images/7d978c5dba02af94d1d462392fc9b813.png)

4. **Load Balancer Misdirection:** Traditional load balancers, lacking QUIC awareness, might perceive the altered 4-tuple as a new connection and direct the client's subsequent traffic to a different real server (say, server2).

5. **Lost Connection (despite QUIC Address Migration):** Even though QUIC has an address migration feature, it won't be able to salvage the connection in this scenario. Both the client's source IP and the server it was originally connected to (server1) have changed, making it impossible for them to keep communication.

6. **The Downside:** This disruption leads to a negative impact on both parties:

   1. **Client:** The client experiences a connection loss, potentially interrupting ongoing communication or data transfer.
   2. **Server:** Server1 loses the established connection and its associated application state, causing potential data loss or service disruption.

## The Solution: XDP QUIC Steering and IPVS Direct Routing

EMQ has been at the forefront of pioneering QUIC technology for IoT scenarios. We introduce our QUIC load balancing solution to address the challenges mentioned above, leveraging XDP for 'QUIC steering' and IPVS for direct routing. In this chapter, we will explore the technical details of this solution.

### **Deployment Overview**

1. **Real Server Configuration:** Each real server in the pool has a unique VIP (Virtual IP) address configured on its local network interface (link-local device). This VIP serves as the target address for client QUIC connections.
2. **IPVS Direct Routing (DR) Mode:** A standard IPVS instance operates in DR (Direct Routing) mode. In this mode, IPVS acts as a traffic director, distributing incoming QUIC packets destined for the VIP address across the pool of real servers based on pre-defined rules (e.g., round-robin, least connections). Importantly, the packets forwarded by IPVS to real servers retain the VIP address as the destination address.
3. **XDP QUIC Steering Module:** A custom XDP module, called "QUIC steering", is injected into the public-facing network interface of each real server. This module operates at the network layer, providing high-performance packet processing capabilities.

### **Functions of XDP QUIC Steering**

The XDP QUIC steering module intercepts every incoming UDP packet targeting the VIP address configured on the real server. It then performs the following actions:

- **Packet Inspection:** The module examines the contents of the UDP packet header.
- **Connection ID Extraction:** Crucially, it extracts the QUIC connection ID from the packet header. This connection ID embedded within the QUIC packet contains information that identifies the specific real server it should be directed to.
- **Packet Routing:** If the extracted connection ID doesn't match the local real server, the XDP module leverages its ability to manipulate packets directly. It routes the packet to the designated real server identified by the connection ID. Importantly, the module does not modify the destination address within the packet header (which remains the VIP address). This allows IPVS to maintain its routing table and perform health checks effectively.

### Detailed Flow

Flow 1: forming request and return path during handshake.

![Initial Handshake](https://assets.emqx.com/images/354821c0dd9460414afe4a31792ea1be.png)

Request and Return path:

| **Step** | **Action**                        | **Src Addr**   | **Dst Addr**   | **notes**                                                    |
| :------- | :-------------------------------- | :------------- | :------------- | :----------------------------------------------------------- |
| 1.       | Client Send QUIC Initial (CRYPTO) | Client Private | VIP            |                                                              |
| 2.       | NAT translation                   | NAT GW Public  | VIP            |                                                              |
| 3.       | LB select RS                      | NAT GW Public  | VIP            | LB Hashing SRC addr                                          |
| 4.       | Server reply QUIC Handshake       | VIP            | NAT GW Public  | Server Assign SCID (Source Connection ID) which contains server id for XDP steering.Server DR (direct route) to the Client. |
| 5.       | NAT translation                   | VIP            | Client Private | The request path and return path are now formed.NAT GW remember this Mapping. |
|          | Client Send QUIC Handshake (ACK)  | Client Private | VIP            | Reuse 1.                                                     |
|          | NAT translation                   | NAT GW Public  | VIP            | Reuse 2. NAT GW find routing in mapping                      |
|          | LB forward to RS1                 | NAT GW Public  | VIP            | reuse 3.                                                     |
|          | Network path is formed            |                |                | Client and Server will continue communicate with the path: 1 → 2 → 3 → 4 → 5 |



Flow 2: QUIC steering after address migration

![QUIC Steering](https://assets.emqx.com/images/b309cc7d5e0a09c2e1d9cc4e109cd1bb.png)

Precondition: Client move to another network or NAT rebinding happens that means the public address of the client has been changed!

| **Step** | **Action**                 | **Src Addr**    | **Dst Addr**    | **notes**                                                    |
| :------- | :------------------------- | :-------------- | :-------------- | :----------------------------------------------------------- |
|          | Client send QUIC packet    | Client Private  | VIP             | Client detect network change thus start to probe the new path.ORClient just send regular QUIC packet.Both scenarios will work.The packet contains DCID (Destination Connection ID)which is the SCID in step 4) in above handshake flow. |
| 2.       | NAT translation            | NAT GW Public 2 | VIP             | To public, client has a new public address                   |
| 3.       | LB select RS 2             | NAT GW Public 2 | VIP             | LB Hashing SRC addr and it select RS 2                       |
| 4.       | XDP QUIC steering          | NAT GW Public2  | VIP             | This is where the XDP QUIC steering module kicks in.It finds the DCID is targeting another host (RS 1), thus it reroute the packet to RS1 while keep the SRC and DST Addr unchanged. |
| 5.       | RS 1 start probe new path  | VIP             | NAT GW Public 2 | The XDP QUIC steering module on RS 1 detects the UDP packet is for RS1  thus no action on it.QUIC stack on RS 1 detects the client address is changed from “NAT GW Public” to “NAT GW Public2”, thus start to probe new path. |
|          | NAT translation            | Client Private  | VIP             | NAT Gateway has the mapping thus does the translation and forward to Client Private |
| 7.       | New network path is formed |                 |                 | Client and Server will continue communicate with the path: 1 → 2 → 3 → 4 → 5 → 6 |

## Benefits of XDP QUIC Steering with IPVS Direct Routing

This approach offers several advantages over traditional methods for load balancing QUIC traffic:

- **Resilience to Client Address Migration:** Unlike traditional UDP load balancers that rely solely on the client's source address, this solution leverages the QUIC connection ID. Even if the client's IP address changes due to NAT (Network Address Translation), the connection ID provides the targeting RS ID. The XDP QUIC steering module on the real server can still identify and route packets belonging to the established connection, ensuring uninterrupted application data exchange without the need for reconnection.
- **High-Performance with XDP:** By processing packets at the XDP layer, this approach benefits from the efficiency of XDP. XDP operates at the network layer, before traditional operating system protocols intervene. This minimizes processing overhead and ensures low latency for QUIC traffic, a crucial factor for real-time applications.
- **IPVS Transparency:** The XDP QUIC steering module cleverly modifies the packet's internal routing path to direct it to the appropriate real server based on the connection ID. Importantly, it doesn't alter the destination address visible to IPVS. This maintains the integrity of IPVS's routing table and health checks, ensuring it can continue functioning as expected for load balancing. 
- **Broad Load Balancer Compatibility:** This approach is designed to work seamlessly with most load balancers that support DR (Direct Routing) mode. DR mode allows the load balancer to directly route traffic to the designated real server based on pre-defined rules, a perfect fit for the XDP QUIC steering's connection-specific routing.
- **Easy Scalability:** The solution is highly scalable. By deploying the XDP QUIC steering module on each real server, adding or removing servers from the pool becomes a straightforward process. This allows for dynamic scaling of your QUIC infrastructure to meet fluctuating traffic demands.

In summary, this approach combines the strengths of IPVS for initial traffic distribution with the efficiency of XDP QUIC steering for connection-based routing. This makes it a compelling solution for efficient and reliable QUIC load balancing.

## Why This Approach Isn't Applicable to TCP

While XDP QUIC steering with IPVS Direct Routing offers a compelling solution for QUIC load balancing, the question arises: can a similar approach be applied to maintain TCP connections alive?

The answer is **no**. Here's why:

- **TCP Relies on the 4-tuple:** Unlike QUIC's connection ID, TCP connections depend on the 4-tuple (source IP,source port, destination IP, and destination port) for identification and routing. XDP QUIC steering wouldn't be able to effectively track and manage TCP connections because they lack the crucial connection ID element within the packet header.
- **TCP State Management:** TCP connections establish and maintain state information (sequence numbers,acknowledgement windows) on both ends (client and server) for reliable data delivery and in-order packet reception. XDP QUIC steering operates at a lower network layer and lacks the capability to manage or manipulate this critical TCP connection state information.
- **TCP Re-establishment (albeit not ideal):** Even if the client's source IP changes during a TCP connection due to NAT, both the client and server can attempt to re-establish the connection by negotiating a new 4-tuple. This re-establishment process, while not ideal, allows the TCP connection to potentially resume data exchange. XDP QUIC steering wouldn't be able to facilitate this re-establishment for TCP connections.

In essence, XDP QUIC steering is specifically tailored to leverage the unique features of QUIC, particularly the managed connection ID that remains manageable even when client addresses change. TCP connections rely on different mechanisms for identification, state management, and potential re-establishment, making this approach unsuitable for maintaining their active state.

**The key takeaway is that address migration is a unique feature provided by the QUIC protocol.** This feature, combined with the QUIC connection ID, allows for efficient and resilient load balancing with XDP QUIC steering. While this approach offers significant advantages for QUIC, the limitations of the TCP protocol prevent its direct application for maintaining TCP connections alive under similar circumstances.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
