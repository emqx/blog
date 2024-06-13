> [EMQX](https://github.com/emqx/emqx) is a popular [MQTT Broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) widely used in the Internet of Things(IoT), Industrial IoT ([IIoT](https://www.emqx.com/en/blog/iiot-explained-examples-technologies-benefits-and-challenges)) and Connected Cars. It can connect millions of devices at scale, move and process your IoT data in real-time anywhere with high performance, scalability and reliability.
>
> In this blog series, we will explore common troubleshooting scenarios when using EMQX and provide practical tips and solutions to overcome them. Readers can optimize your MQTT deployment and ensure smooth communication between your devices following this troubleshooting instruction.


## Introduction

Regarding client connections, we may encounter problems such as connection failures, frequent disconnections, or the challenge of testing the upper limit of many connections. This article will introduce how to analyze and locate these problems and provide some optimization suggestions.

## Abnormal Disconnection Problems

Abnormal disconnection is a common problem that can be caused by unstable networks, client code issues, or server problems.

- **Unstable Network:** An unstable network is one of the most common reasons for the frequent disconnection of EMQX clients, In such instances, clients may experience delays in receiving timely responses from the server, resulting in abrupt disconnections.
- **Client Code Issues:** There may be bugs or misconfigurations in the client code, causing the client to disconnect frequently.
- **Server Problems:** The server may have problems such as high load or misconfiguration.

For connection problems such as client connection failures and frequent disconnections, we can use EMQX's log trace function to troubleshoot the specific disconnection reasons of the client.

1. You can enable the log trace in the EMQX Dashboard.

   - After clicking "create", select "ClientID" as the type;
   - Fill in the ClientID information that needs to be tracked (must be accurate ClientID);
   - Select the start and end time. If the start time is less than or equal to the current time, it will start from the current time by default.

   ![Enable the log trace in the EMQX Dashboard](https://assets.emqx.com/images/25c3a38be78b8069706c9c42a6c88cec.png)

2. The trace record created successfully can be seen in the list. You can view the log directly in dashboard or download and view it locally.

   ![Trace log list](https://assets.emqx.com/images/f1ac14f820f08cdd2205d35e1dc6ed0b.png)

3. In the log, you can analyze the reasons for the client's disconnection.

   ![Log details](https://assets.emqx.com/images/d1bcdce617f595e9036c4b3b1b79a104.png)

4. By analyzing the logs, we can identify specific disconnection reasons associated with corresponding keywords. The following are the various reasons for client connection disconnections:

   - **normal**: client actively disconnected;
   - **kicked**: kicked out by the server, through the REST API;
   - **keepalive_timeout**: keepalive timeout;
   - **not_authorized**: authentication failed, or when acl_nomatch=disconnect, Pub/Sub without permission will actively disconnect the client;
   - **tcp_closed**: the peer closed the network connection;
   - **discarded**: because the client with the same ClientID went online and set clean_start=true;
   - **takeovered**: because the client with the same ClientID went online and set clean_start=false;
   - **internal_error**: malformed message or other unknown errors.

   Client code issues can cause normal, keepalive_timeout, discarded, takeovered, not_authorized, internal_error, etc.

   unstable networks can cause keepalive_timeout, not_authorized, etc.

   server issues can cause kicked, internal_error, etc.

## Connections Limit Problem

When conducting load testing on EMQX with a large number of clients, you may encounter difficulties in increasing the connection count. To solve this problem, you can optimize the operating system. Here are some recommended methods for optimization :

1. **Increasing the file handle limit**: Given EMQX's extensive usage of file handles, it becomes imperative to raise the operating system's file handle limit. By modifying the value of "nofile" in the "/etc/security/limits.conf" file, you can allow all users to access the maximum number of file handles after logging in.
2. **Adjusting network parameters**: You can improve network performance by modifying the operating system's network parameters. For example, you can use the sysctl command to set TCP connection parameters, which will increase the system's ability to handle TCP connections.
3. **Adjusting memory parameters**: You can improve memory usage efficiency by modifying the operating system's memory parameters. For example, you can use the sysctl command to set memory parameters, which will make the operating system more efficient in using memory, thereby improving the performance of EMQX Broker.

The following configuration parameters are adjusted for a single machine with a target of 1 million connections and persisted:

- Add or modify the following parameters in /etc/sysctl.conf:

  ```
  # System-wide maximum number of file handles that can be allocated
  fs.nr_open=2097152
  fs.file-max=2097152
  # Available port range
  net.ipv4.ip_local_port_range=1024 65535
  # Concurrent connection backlog setting
  net.core.somaxconn=32768
  net.ipv4.tcp_max_syn_backlog=16384
  net.core.netdev_max_backlog=16384
  # TCP socket read/write buffer setting
  net.core.rmem_default=262144
  net.core.wmem_default=262144
  net.core.rmem_max=16777216
  net.core.wmem_max=16777216
  net.core.optmem_max=16777216
  net.ipv4.tcp_rmem=1024 4096 16777216
  net.ipv4.tcp_wmem=1024 4096 16777216
  # TCP connection tracking setting
  net.netfilter.nf_conntrack_max=1000000
  net.netfilter.nf_conntrack_tcp_timeout_time_wait=30
  # Maximum number of TIME-WAIT sockets, and settings for socket recycling and reuse
  net.ipv4.tcp_max_tw_buckets=1048576
  # FIN-WAIT-2 socket timeout setting
  net.ipv4.tcp_fin_timeout=15
  ```

- Set the maximum file handle limit for the service in /etc/systemd/system.conf:

  ```
  DefaultLimitNOFILE=1048576
  ```

- Persistently set the number of file handles that users/processes are allowed to open in /etc/security/limits.conf:

  ```
  # If you want to limit a specific account, replace * with the corresponding username
  *      soft   nofile      1048576
  *      hard   nofile      1048576
  ```

- Run the following command to make the configuration take effect:

  ```
  /sbin/sysctl -p
  ```

  

## Conclusion

When using EMQX for communication, common problems such as abnormal disconnection of clients and the maximum number of client connections can be addressed through specific solutions. By using network stability tools, checking client code and configuration, and examining server load and configuration, we can effectively solve these problems and improve the stability and reliability of the clients.


<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
