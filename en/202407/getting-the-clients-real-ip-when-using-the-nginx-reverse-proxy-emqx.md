## Introduction

The leading MQTT platform, EMQX, supports cluster scaling to achieve high performance and availability. In cluster deployment, we usually use NGINX, HAProxy, and other reverse proxies to achieve load balancing, SSL/TLS termination, failover, and other purposes.

The proxy connects to EMQX on behalf of MQTT clients, which means EMQX cannot directly obtain the client's real IP. This limitation makes it inconvenient for us to implement IP-based applications, such as security auditing and access restriction.

In this article, we will take [NGINX 1.26.1](https://nginx.org/en/download.html) and [EMQX 5.7.0](https://www.emqx.com/en/downloads-and-install/broker?os=Ubuntu) as an example to demonstrate how to get the real IP of MQTT client through PROXY protocol or `X-Forwarded-For` header when using NGINX reverse proxy for EMQX.

## Getting the MQTT over TCP Client's Real IP

### Single-Tiered Proxy

A single-tiered proxy means there is only one Load Balancer between the MQTT client and the backend server, which is the most common case:

```
Client -> Load Balancer(NGINX, HAProxy, ...) -> Server(EMQX)
```

In this case, we can use the [PROXY protocol](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) to pass the IP of the real client.

The PROXY protocol, first proposed and designed by [HAProxy](https://www.haproxy.org/), is a specification for TCP proxies to encapsulate and pass back metadata such as the client's original IP and port. The PROXY protocol has become the preferred solution for obtaining the client's original IP address and port when using a proxy to relay a TCP connection.

Before using the PROXY protocol:

```txt
+ ----------- +  <CONNECT packet> | ...  + ------------ +  <CONNECT packet> | ... + ------ +
| MQTT Client |  ----------------------> | Load Balancer| ----------------------> | Server |
+ ----------- +                          + ------------ +                         + ------ +
```

After using the PROXY protocol:

```txt
+ ----------- +  <CONNECT packet> | ...  + ------------ +  <PROXY protocol header> | <CONNECT packet> | ... + ------ +
| MQTT Client |  ----------------------> | Load Balancer| ------------------------------------------------> | Server |
+ ----------- +                          + ------------ +                                                   + ------ +
```

The following is a typical PROXY protocol header:

```
PROXY TCP 172.168.0.116 172.168.0.200 39826 1883
|     |   |             |             |     |
|     |   |             |             |     Destination Port
|     |   |             |             Source Port
|     |   |             Destination IP
|     |   Source IP
|     Indicates this is an IPv4 TCP connection
Fixed prefix to identify the PROXY protocol
```

The PROXY protocol is currently available in two versions, v1 and v2. v1 is the human-readable text format introduced above, while v2 has been changed to a machine-readable binary format to improve the parsing efficiency of programs. v2's specific format will not be expanded in this article. Interested readers can refer to [The PROXY protocol Version 1 & 2](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) to learn more. EMQX supports both v1 and v2, as well as  automatic detection of the version used. In this article, we will use v1 for demonstration.

#### Configure

Take NGINX as an example. First we need to modify the configuration of NGINX (click [Here](https://nginx.org/en/docs/install.html) for installation instructions), open `/etc/nginx/nginx.conf`, and add the following configuration:

```nginx
stream {
  upstream server {
    # Please change to your actual IP and listening port
    server 172.16.0.71:1883;
  }
  
  server {
    listen 1883;
    proxy_pass server;
    # Enable PROXY protocol sending
    proxy_protocol on;
  }
}
```

The above configuration indicates that NGINX will listen port 1883 and forward the inbound data to the server at address `172.16.0.71:1883`. Since the PROXY protocol is enabled, NGINX will **first** send the PROXY protocol header after establishing the connection.

After saving the configuration, run the following command to reload the configuration:

```bash
nginx -s reload
```

Then, we also need to modify the EMQX (click [Here](https://docs.emqx.com/en/emqx/latest/deploy/install.html) for installation instructions) configuration to enable parsing of the PROXY protocol header.

For example, in version 5.7, we need to open the Dashboard in the browser, go to "Management" > "Cluster Settings" > "MQTT Settings", click the default TCP listener (or any other listener you want to change) to enter the configuration page, and set "Proxy Protocol" to true:

![01dashboardproxyprotocolen.png](https://assets.emqx.com/images/924dca9152db0d0cb9c5c7bf985e2679.png)

Changes to the EMQX listener will take effect immediately after clicking "Update".

#### Verify

In this example, the IP of each host is as follows:

```txt
+ ----------------------- +      + ---------------------- +      + ------------------- +
| MQTT Client             |      | NGINX                  |      | EMQX                |
| *********************** | ---> | ********************** | ---> | ******************* |
| LAN IP: /               |      | LAN IP: 172.16.0.116   |      | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |      | WAN IP: 121.36.192.227 |      | WAN IP: /           |
+ ----------------------- +      + ---------------------- +      + ------------------- + 
```

To verify that NGINX correctly sends the PROXY protocol header we expect, we can capture network packets on the host running EMQX using the following command:

```bash
# -i eth0, Capture packets on network interface eht0
# -s 0, Capture complete packets
# -vv, More verbose output
# -n, Don't convert addresses (i.e., host addresses, port numbers, etc.) to names
# -X, Prints per-packet data in hex and ASCII
# -S, Print absolute, rather than relative, TCP sequence numbers
# 'port 1883', Capture all packets with source or destination port 1883
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 1883'
```

Then use the MQTTX CLI (click [Here](https://mqttx.app/docs/cli/downloading-and-installation) for installation instructions) to connect to NGINX as an MQTT client:

```bash
# Change 121.36.192.227 to your actual NGINX IP
mqttx conn -h 121.36.192.227 -p 1883 --client-id mqttx-client
```

Within packets captured by ***tcpdump***, we can see that NGINX (`172.16.0.116`), after establishing a TCP connection with EMQX (`172.16.0.71`), first sends a PROXY protocol header, which indicates that the client's IP is `115.236.21.86`:

![02capturedpackets.png](https://assets.emqx.com/images/43fc0ee2bef859a6754fac86a32562a1.png)

With EMQX's CLI commands, we can also see that EMQX has successfully obtained the source IP address and port of the client:

```bash
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:61177, ...)
```

### Multi-Tiered Proxy

Some large complex deployments may also have multiple tiers of proxies, for example:

```txt
+ ----------- +        + ---- +       + ---- +       + ------ +
| MQTT Client |  ----> | LB 1 | ----> | LB 2 | ----> | Server |
+ ----------- +        + ---- +       + ---- +       + ------ +
```

When there are multiple tiers of reverse proxies, we need to make some adjustments to the NGINX configuration so that the backend EMQX can still obtain the client's real IP.

First, the outermost LB, LB 1, must enable the PROXY protocol sending to pass on the client's source IP and source port.

Since each TCP connection can only send a PROXY protocol header once, the LB cannot forward the received PROXY protocol header and send its header in addition. The following scenario is not allowed:

```txt
+ ----------- +     + ---- +  <PP header 1> | ...  + ---- +  <PP header 2> | <PP header 1> | ...  + ------ +
| MQTT Client |  -> | LB 1 | --------------------> | LB 2 | ------------------------------------> | Server |
+ ----------- +     + ---- +                       + ---- +                                       + ------ +
```

> PP header is the abbreviation for PROXY protocol header.

Therefore, we have two ways to configure the intermediate LBs. The first way is the simplest. Intermediate LBs do not need to enable PROXY protocol parsing or sending, they just need to pass through all the packets sent by LB 1:

```txt
+ ----------- +        + ---- +  <PP header 1> | ...  + ---- +  <PP header 1> | ...  + ------ +
| MQTT Client |  ----> | LB 1 | --------------------> | LB 2 | --------------------> | Server |
+ ----------- +        + ---- +                       + ---- +                       + ------ +

PP header 1 = "PROXY TCP <Client IP> <LB 1 IP> <Client Port> <LB 1 Port>"
```

The second way requires the intermediate LBs to enable both PROXY protocol parsing and sending.

Each LB receives the PROXY protocol header, obtains the client source IP address and port, and then sets them in the PROXY protocol header to be sent to the upstream LB or backend application server:

```txt
+ ----------- +        + ---- +  <PP header 1> | ...  + ---- +  <PP header 2> | ...  + ------ +
| MQTT Client |  ----> | LB 1 | --------------------> | LB 2 | --------------------> | Server |
+ ----------- +        + ---- +                       + ---- +                       + ------ +

PP header 1 = "PROXY TCP <Client IP> <LB 1 IP> <Client Port> <LB 1 Port>"
PP header 2 = "PROXY TCP <Client IP> <LB 2 IP> <Client Port> <LB 2 Port>"
```

#### Passthrough

LB 1 and LB 2 both use NGINX, and the following is an example of a pass-through configuration:

```nginx
# LB 1
# Enable PROXY protocol sending
stream {
  upstream proxy2 {
    # Please change to your actual LB 2 IP and listening port
    server 172.16.0.200:1883;
  }
  
  server {
    listen 1883;
    proxy_pass proxy2;
    # Enable PROXY protocol sending
    proxy_protocol on;
  }
}

# LB 2
# Don't enable PROXY protocol parsing and sending
stream {
  upstream server {
    # Please change to your actual EMQX IP and listening port
    server 172.16.0.71:1883;
  }
  
  server {
    listen 1883;
    proxy_pass server;
  }
}
```

EMQX continues to enable the PROXY protocol, no other changes are required.

##### Verify

Since an LB has been added, the IPs of the hosts in this example are as follows:

```txt
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
| MQTT Client             |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    | EMQX                |
| *********************** | -> | ********************** | -> | ******************** | -> | ******************* |
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    | WAN IP: /           |
+ ------------------------+    + ---------------------- +    + -------------------- +    + ------------------- +
```

Run the following command in LB 2 to capture packets:

```bash
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 1883'
```

Then, use the MQTTX CLI to connect to LB 1 as an MQTT client:

```bash
# Change 121.36.192.227 to the IP of your actual outermost LB
mqttx conn -h 121.36.192.227 -p 1883 --client-id mqttx-client
```

Within captured packets, we can see that LB 2 received the PROXY protocol header from LB 1, which indicates that the client's IP is `115.236.21.86`, and the header content did not change in LB 2's connection to the EMQX, indicating that the passthrough is in effect:

![03capturedpacketspassthrough.png](https://assets.emqx.com/images/7fbfddf4a74987d46932d727e5816e07.png)

With the EMQX’s CLI command, we can see that EMQX has successfully obtained the source IP and source port of the client:

```bash
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:18936, ...)
```

#### Non-passthrough

The configuration is as follows:

```nginx
# LB 1
# Enable PROXY protocol sending, same configuration as for passthrough
stream {
  upstream proxy2 {
    server 172.16.0.200:1883;
  }
  
  server {
    listen 1883;
    proxy_pass proxy2;
    proxy_protocol on;
  }
}

# LB 2
# Enable PROXY protocol parsing and sending.
# If there are more intermediate LBs, their
# configuration is similar to that of LB 2, 
# with only the corresponding IPs and ports modified
stream {
  upstream server {
    server 172.16.0.71:1883;
  }
  
  server {
    # Enable PROXY protocol parsing
    listen 1883 proxy_protocol;
    proxy_pass server;
    # Enable PROXY protocol sending
    proxy_protocol on;
    
    # Set the trusted address, change 172.16.0.0/24 to
    # the IP address or CIDR range of the proxy you trust
    set_real_ip_from 172.16.0.0/24;
    
    # Set LB 1's WAN IP as the trusted address
    # set_real_ip_from 172.16.0.116
  }
}
```

Just so you know, you must specify the IP address or CIDR address range of the trusted LB using the `set_real_ip_from` directive. NGINX will only obtain the source IP of the real client from the trusted source’s PROXY protocol header. Otherwise, LB 2 will use LB 1’s IP as the source IP instead of the client's IP when it sends the PROXY protocol header to the Server:

```txt
       + ---- +  PROXY TCP <LB 1 IP> <LB 2 IP> <LB 1 Port> <LB 2 Port>  + ------ + 
... -> | LB 2 | ------------------------------------------------------> | Server |
       + ---- +                                                         + ------ +  
```

The directive `set_real_ip_from` relies on the Stream Real-IP module, which you can check to see if it is included in your current NGINX installation with the following command:

```bash
nginx -V 2>&1 | grep -- 'stream_realip_module'
```

If not, you must compile NGINX manually and include this module in your build, see [Installing NGINX Open Source](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/) for details.

##### Verify

In this example, the IP of each host is the same as in the case of passthrough:

```txt
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
| MQTT Client             |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    | EMQX                |
| *********************** | -> | ********************** | -> | ******************** | -> | ******************* |
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    | WAN IP: /           |
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
```

Run the following command in LB 2 to capture packets:

```bash
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 1883'
```

Then, use the MQTTX CLI to connect to LB 1:

```bash
# Change 121.36.192.227 to your actual outermost LB's IP
mqttx conn -h 121.36.192.227 -p 1883 --client-id mqttx-client
```

In captured packets, we can see that LB 2 received the PROXY protocol header from LB 1, which indicates that the client's IP is `115.236.21.86`. In LB 2’s connection to the EMQX, the header content changed, but it still correctly indicates the client's real IP, which shows that the `set_real_ip_from` directive is working:

![04capturedpacketsnonpassthrough.png](https://assets.emqx.com/images/21da88079455e5ba2518f61589db4798.png)

With the EMQX’s CLI command, we can see that EMQX has successfully obtained the source IP and source port of the client:

```bash
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:39817, ...)
```

## Getting the MQTT over WebSocket Client's Real IP

In web applications such as browsers and WeChat mini programs, the client will use MQTT over WebSocket to access EMQX. Since WebSocket can carry headers, in addition to the PROXY protocol, we can pass the client's real IP between the LB and the application server via the `X-Forwarded-For` header. 

When it comes to obtaining the real IP of the MQTT over WebSocket client, both NGINX and EMQX are configured in the same manner as when obtaining the real IP of the MQTT over TCP client. Therefore, we won't delve into that again here.

Next, we will focus on configuring NGINX and EMQX to obtain the client's real IP via the `X-Forwarded-For` header.

### Single-Tiered Proxy

Let's start with the most common single-tiered proxy, and here's a sample configuration for NGINX:

```nginx
http {
  upstream server {
    server 172.16.0.71:8083;
  }
  
  server {
    listen 8083;
    # Use /mqtt as the endpoint for providing WebSocket services
    location /mqtt {
      proxy_pass http://server;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}
```

When the client prepares to use MQTT over WebSocket to access EMQX, NGINX will not actively forward the `Upgrade` and `Connection` headers to EMQX, so we must configure NGINX to explicitly pass these two headers so that EMQX understands the client's intent to switch protocols to WebSocket.

NGINX's `proxy_set_header` directive allows us to modify or set the request headers that NGINX passes to the backend:

```nginx
# $http_* are NGINX built-in variables whose values are the given HTTP header received by NGINX.
# So the value of $http_upgrade is the Upgrade header in the request received by NGINX.
# This directive is equivalent to setting the Upgrade header sent by NGINX to "websocket".
proxy_set_header Upgrade $http_upgrade;

# Setting the Connection header to "Upgrade" indicates an upgrade request
# to the protocol listed in the Upgrade header.
proxy_set_header Connection "Upgrade";
```

`$remote_addr` and `$remote_port` are NGINX built-in variables that record the IP and port of the peer. Note that in the multi-tiered proxy scenario, the peer may also be the downstream LB (closer to your clients).

Of course, in the single-tiered proxy scenario, we can use `$remote_*` directly to get the IP address and port of the MQTT client:

```nginx
# Set the Host header to the hostname requested by the client
proxy_set_header Host $host;

# Setting the X-Forwarded-For to pass the MQTT client source IP
proxy_set_header X-Forwarded-For $remote_addr;

# Set X-Forwarded-Port to pass the MQTT client source port
proxy_set_header X-Forwarded-Port $remote_port;
```

> `X-Forwarded-Port` can also be set to `$server_port` to indicate the port accessed by the client, so that upper-layer applications can provide different services depending on the entry point. In this article, we will mainly use `X-Forwarded-Port` to pass the source port of the original client.

Save the above configuration to `/etc/nginx/nginx.conf` and run `nginx -s reload` to reload the configuration.

Next, we need to modify the listener configuration of EMQX. Open the Dashboard in your browser, go to "Management" > "Cluster Settings" > "MQTT Settings", click the default WebSocket listener (or any other listener you want to change) to enter the configuration page, expand "Advanced Settings", and then paste the following configuration into "Custom Configuration", and finally click "Update":

```bash
websocket.proxy_address_header = X-Forwarded-For
websocket.proxy_port_header = X-Forwarded-Port
```

The above configuration means that EMQX will take the leftmost IP in the `X-Forwarded-For` header as the client source IP and the leftmost port in the `X-Forwarded-Port` header as the client source port from the received WebSocket upgrade requests.

#### Verify

In this example, the IPs of the hosts are as follows:

```txt
+ ----------------------- +      + ---------------------- +      + ------------------- +
| MQTT Client             |      | NGINX                  |      | EMQX                |
| *********************** | ---> | ********************** | ---> | ******************* |
| LAN IP: /               |      | LAN IP: 172.16.0.116   |      | LAN IP: 172.16.0.71 |
| WAN IP: 115.236.21.86   |      | WAN IP: 121.36.192.227 |      | WAN IP: /           |
+ ----------------------- +      + ---------------------- +      + ------------------- + 
```

Run the following command on the host where the EMQX is located to capture packets:

```bash
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 8083'
```

Then, use the MQTTX CLI to connect to LB 1:

```bash
# Change 121.36.192.227 to your actual outermost LB's IP
mqttx conn -h 121.36.192.227 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
```

Within captured packets, we can see that the LB, after establishing a TCP connection with the EMQX, sends an HTTP request for protocol upgrade with `X-Forwarded-For` of `115.236.21.86` and `X-Forwarded-Port` of `61813`, which corresponds to the source IP address and source port of the real client, respectively:

![05xforwardedforlbtoemqx.png](https://assets.emqx.com/images/d4796541525ed8e4ebd024ddf6e5f220.png)

With the EMQX’s CLI command, we can see that EMQX has successfully obtained the real IP and port of the MQTT client:

```bash
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=115.236.21.86:61813, ...)
```

### Multi-Tiered Proxy

In multi-tiered proxy scenario, `X-Forwarded-For` is used to pass the client’s real IP across proxies and record the IPs of the intermediate proxies passed through so that the backend application servers can recognize the source of the request and provide different services.

However, in practice, it is not enough to let LB append the downstream IP to the `X-Forwarded-For` header. We must consider the case of malicious spoofing on the client side because the client side can set the `X-Forwarded-For` header as well.

In the previous single-tiered proxy scenario, we used the client's source IP to force override the `X-Forwared-For`, ensuring that the `X-Forwarded-For` finally obtained by the server must be real and correct.

The multi-tiered proxy scenario is different. If nothing is done, the client can fake any IP to deceive the server and bypass the server's security management policy. For example, in the following case, the application server will mistakenly think that `<Fake IP>` is the client's real IP.

```txt
+ ------ +   X-Forwarded-For: <Fake IP>  + ---- +  X-Forwarded-For: <Fake IP>, <Real Client IP>
| Client |  ---------------------------> | LB 1 | ----------------------------------------------...
+ ------ +                               + ---- +

     + ---- +  X-Forwarded-For: <Fake IP>, <Real Client IP>, <LB 1 IP>  + ------ +
..-> | LB 2 | --------------------------------------------------------> | Server |
     + ---- +                                                           + ------ +
```

There are usually two ways to solve this problem. The first way is to have the outermost LB assign  `$remote_addr` directly to the `X-Forwarded-For` instead of appending it to the original one, which eliminates the possibility of the client forging `X-Forwarded-For`:

```nginx
# Override
proxy_set_header X-Forwarded-For $remote_addr;
# Append
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
```

Expected result:

```txt
+ ------ +   X-Forwarded-For: <Fake IP>  + ---- +  X-Forwarded-For: <Real Client IP>
| Client |  ---------------------------> | LB 1 | -----------------------------------...
+ ------ +                               + ---- +

     + ---- +  X-Forwarded-For: <Real Client IP>, <LB 1 IP>  + ------ +
..-> | LB 2 | ---------------------------------------------> | Server |
     + ---- +                                                + ------ +
```

The second way is for all LBs to append the remote IP to the original X-Forwarded-For and then set the trusted address in the innermost LB. 

This innermost LB will traverse from right to left and take the first untrusted IP as the client’s real IP.

```txt
+ ------ +   X-Forwarded-For: <Fake IP>  + ------------ +  X-Forwarded-For: <Fake IP>, <Real Client IP>
| Client |  ---------------------------> | Trusted LB 1 | ----------------------------------------------...
+ ------ +                               + ------------ +

     + ------------ +  X-Forwarded-For: <Fake IP ✘>, <Real Client IP ✘>, <Trusted LB 1 IP ✔︎>  + ------ +
..-> | Trusted LB 2 | ----------------------------------------------------------------------> | Server |
     + ------------ +                                                                         + ------ +
```

In this case, although the client forges the `X-Forwarded-For`, when the request reaches the application server, the faked IP will only be located on the left side of the `X-Forwarded-For`. As long as all trusted IPs are eliminated from right to left, the first untrusted IP must be the client’s real IP appended by the outermost trusted LB.

#### Method 1: Use $remote_addr

```nginx
# LB 1
# Override the values of X-Forwarded-For and X-Forwarded-Port
http {
  upstream proxy2 {
    server 172.16.0.200:8083;
  }
  
  server {
    listen 8083;
    location /mqtt {
      proxy_pass http://proxy2;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}

# LB 2
# Append to the original X-Forwarded-For and X-Forwarded-Port
http {        
  upstream server {
    server 172.16.0.71:8083;
  }
  
  server {
    listen 8083;
      
    location /mqtt {
      proxy_pass http://server;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $remote_port";

    }
  }
}
```

Save the above configurations to LB 1 and LB 2 respectively, and run `nginx -s reload` to reload them.

The configuration of EMQX is the same as in the case of single-tiered proxy:

```bash
websocket.proxy_address_header = X-Forwarded-For
websocket.proxy_port_header = X-Forwarded-Port
```

##### Verify

Since it is not possible to fake the `X-Forwarded-For` header with the MQTTX CLI, to verify the effect, we can deploy an additional NGINX on the host running the MQTT Client, which serves to help us fake an X-Forwarded-For header with a value of `127.0.0.1`, configured as follows:

```nginx
http {
  upstream proxy1 {
    # Please change to the public IP and listening port of your actual LB 1.
    server 121.36.192.227:8083;
  }
  
  server {
    listen 8083;
    location /mqtt {
      proxy_pass http://proxy1;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}
```

The IPs of the hosts are as follows:

```txt
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
| MQTT Client + Proxy     |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    | EMQX                |
| *********************** | -> | ********************** | -> | ******************** | -> | ******************* |
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    | LAN IP: 172.16.0.71 |
| WAN IP: 1.94.170.163    |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    | WAN IP: /           |
+ ----------------------- +    + ---------------------- +    + -------------------- +    + ------------------- +
```

Run the following commands in both hosts, LB 1 and LB 2, to capture network packets:

```bash
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 8083'
```

Run the MQTTX CLI, connecting to the local NGINX instead of the remote LB 1:

```bash
mqttx conn -h 127.0.0.1 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
```

Within captured packets, we can see that LB 1 received a WebSocket upgrade request with an `X-Forwarded-For` of `127.0.0.1`, which is equivalent to a malicious MQTT client attempting to spoof the server that this is a local connection.

But LB 1 knows where the request came from, so in the WebSocket upgrade request it sends to LB 2, the client's fake `X-Forwarded-For` is ignored, and the `X-Forwarded-For` is set to the real IP of the currently connected client, which is `1.94.170.163`. So, in the end, the server still gets the correct source IP of the original client, and the same goes for `X-Forwarded-Port`.

![06remoteaddr.png](https://assets.emqx.com/images/047cbd09133378a8b7fec77cce8a44db.png)

With the EMQX’s CLI command, we can see that EMQX has successfully obtained the real IP and port of the MQTT client:

```bash
$ mqttx conn -h 127.0.0.1 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
Client(mqttx-client, ..., peername=1.94.170.163:52662, ...)
```

#### Method 2: Setting trusted addresses

To verify the effectiveness of the `real_ip_recursive` directive, we add an additional host as LB 3. The difference between LB 1 and LB 2 is only the IP of the upstream:

```nginx
# LB 1
# Append to the original X-Forwarded-For and X-Forwarded-Port
http {
  upstream proxy2 {
    server 172.16.0.200:8083;
  }
  
  server {
    listen 8083;
    location /mqtt {
      proxy_pass http://proxy2;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $remote_port";
    }
  }
}

# LB 2
# Append to the original X-Forwarded-For and X-Forwarded-Port
http {        
  upstream proxy3 {
    server 172.16.0.225:8083;
  }
  
  server {
    listen 8083;
      
    location /mqtt {
      proxy_pass http://proxy3;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $remote_port";
    }
  }
}

# LB 3
# Append to the original X-Forwarded-For and X-Forwarded-Port
# Get the client's real IP from the X-Forwarded-For and set it in the X-Real-IP header
http {        
  upstream server {
    server 172.16.0.71:8083;
  }
  
  server {
    listen 8083;
    
    # Trust all IPs in the range 172.16.0.0/24
    set_real_ip_from 172.16.0.0/24;
    # Get the client's real IP from X-Forwarded-For
    real_ip_header X-Forwarded-For;
    # Right-to-left recursive search for the first untrusted IP as the client's real IP
    real_ip_recursive on;
      
    location /mqtt {
      proxy_pass http://server;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      
      # append $realip_remote_* instead of $remote_*
      proxy_set_header X-Forwarded-For "$http_x_forwarded_for, $realip_remote_addr";
      proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $realip_remote_port";
      # Passing the client’s real IP using X-Real-IP
      proxy_set_header X-Real-IP $remote_addr;
    }
  }
}

```

The core of the LB 3 configuration is the `set_real_ip_from`, `real_ip_header` directives, which rely on the HTTP Real-IP module, which you can check to see if it is included in your current NGINX installation with the following commands:

```bash
nginx -V 2>&1 | grep -- 'http_realip_module'
```

If not, you must compile NGINX manually and include this module in your build, see [Installing NGINX Open Source](https://docs.nginx.com/nginx/admin-guide/installing-nginx/installing-nginx-open-source/) for details.

With the `set_real_ip_from` directive, we can specify the IP address or CIDR address range of the trusted LB. `set_real_ip_from` can be called multiple times, for example:

```nginx
set_real_ip_from 172.16.0.0/24;
set_real_ip_from 115.236.21.86;
```

The `real_ip_header` directive allows us to specify the source of the Real IP, which in this example is the `X-Forwarded-For` header.

The `real_ip_recursive` directive allows us to specify whether or not to search for the real IP recursively. Set it to `off`, and NGINX will take the first IP directly from right to left as the client's real IP; set it to `on`, and NGINX will take the first IP from right to left that is out of the trusted range as the client's real IP. The latter is needed for this example.

Once the Real-IP module is used, NGINX puts the client's real IP and port into the variables `$remote_addr` and `$remote_port`, and the downstream IP and port need to be obtained from the variables `$realip_remote_addr` and `$realip_remote_port`:

```nginx
proxy_set_header X-Forwarded-For "$http_x_forwarded_for, $realip_remote_addr";
proxy_set_header X-Forwarded-Port "$http_x_forwarded_port, $realip_remote_port";
```

Here, we are assigning `$remote_addr` to another header, `X-Real-IP`, so we also need to synchronize the changes to EMQX's WebSocket listener configuration:

```bash
websocket.proxy_address_header = X-Real-IP
websocket.proxy_port_header = X-Forwarded-Port
```

##### Verify

In this example, the IPs of the hosts are as follows:

```txt
+ ----------------------- +    + ---------------------- +    + -------------------- +    
| MQTT Client + Proxy     |    | LB 1 (NGINX)           |    | LB 2 (NGINX)         |    
| *********************** | -> | ********************** | -> | ******************** | --...
| LAN IP: /               |    | LAN IP: 172.16.0.116   |    | LAN IP: 172.16.0.200 |    
| WAN IP: 1.94.170.163    |    | WAN IP: 121.36.192.227 |    | WAN IP: /            |    
+ ----------------------- +    + ---------------------- +    + -------------------- +

     + -------------------- +    + ------------------- +
     | LB 3 (NGINX)         |    | EMQX                |
..-> | ******************** | -> | ******************* |
     | LAN IP: 172.16.0.225 |    | LAN IP: 172.16.0.71 |
     | WAN IP: /            |    | WAN IP: /           |
     + -------------------- +    + ------------------- +
```

Run the following commands in three hosts, LB 1, LB 2, and LB 3, to capture packets:

```bash
sudo tcpdump -i eth0 -s 0 -nvvXS 'port 8083'
```

As with the previous example, we need to deploy an additional NGINX on the host running the MQTT Client, configured as follows:

```nginx
http {
  upstream proxy1 {
    # Please change to your actual LB 1's public IP and listening port
    server 121.36.192.227:8083;
  }
  
  server {
    listen 8083;
    location /mqtt {
      proxy_pass http://proxy1;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "Upgrade";
      
      proxy_set_header Host $host;
      proxy_set_header X-Forwarded-For $remote_addr;
      proxy_set_header X-Forwarded-Port $remote_port;
    }
  }
}
```

Run the MQTTX CLI, connecting to the local NGINX instead of the remote LB 1:

```bash
mqttx conn -h 127.0.0.1 -p 8083 --protocol ws --path /mqtt --client-id mqttx-client
```

Within captured packets, we can see that LB 1 received a WebSocket upgrade request with an `X-Forwarded-For` of `127.0.0.1`, which is equivalent to a malicious MQTT client attempting to spoof the server that this is a local connection:

![07clienttolb1.png](https://assets.emqx.com/images/81b385777a914bc92703fc36dcb39580.png)

But this time, we did not directly overwrite `X-Forwarded-For`, we appended it on the original basis. Therefore, in the WebSocket upgrade request sent by LB 2 to LB 3, we can see that the value of `X-Forwarded-For` is `127.0.0.1, 1.94.170.163, 172.16.0.116`:

![08lb2tolb3.png](https://assets.emqx.com/images/bf787c787ef20cb70ee01a193dedc29d.png)

In the WebSocket upgrade request sent by LB 3 to EMQX, we can see that the `X-Real-IP` header is set to `1.94.170.163`, which is what we expected:

![09lb3toemqx.png](https://assets.emqx.com/images/31737e73738f62ad6ff773485d40048a.png)

With the EMQX’s CLI command, we can see that EMQX has successfully obtained the real IP and port of the MQTT client:

```bash
$ emqx ctl clients show mqttx-client
Client(mqttx-client, ..., peername=1.94.170.163:39872, ...)
```

If we set `real_ip_recursive` to `off` in LB 3, we will see that the `X-Real-IP` header is set to `172.16.0.116`:

![10lb3toemqx.png](https://assets.emqx.com/images/8744f29c01bdec736a6bf3ddf4887b5c.png)

## Conclusion

In this article, we thoroughly explore the process of configuring EMQX and NGINX to ensure that the client's actual IP address can be transmitted through a single or multiple proxy tiers to the ultimate EMQX server. This is achieved with the assistance of the PROXY protocol or the `X-Forwarded-For` header, enabling applications such as security auditing, access restriction, and traffic monitoring.

In the following blogs, we will also provide a configuration guide on getting the client's real IP when using HAProxy to reverse proxy EMQX. Subscribe to our [blog](https://www.emqx.com/en/blog) to stay up to date with our latest news.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
