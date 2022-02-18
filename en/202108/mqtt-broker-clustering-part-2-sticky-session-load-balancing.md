In the last post: [Load balancing - MQTT broker clustering part 1](https://www.emqx.com/en/blog/mqtt-broker-clustering-part-1-load-balancing), we have introduced MQTT load balancing in general: load balancing can be applied either on transport layer, or application layer. Now it’s time to dive into application layer load balancing, the most interesting part: sticky-session.

This post consists of 2 parts, the first part is to introduce what MQTT sessions, and the challenges of handing sessions in a distributed MQTT broker cluster; the second part is to get our hands dirty by provisioning an [HAProxy 2.4](http://www.haproxy.org/) load balancer in front of [EMQX 4.3](https://www.emqx.com/en/products/emqx) cluster to take full advantage of the sticky-session load balancing.

## MQTT session

In order to continuously receive messages, MQTT clients usually subscribe to [MQTT broker](https://www.emqx.com/en/products/emqx) with a long-living connection. It is not unusual that the connection might be broken for a while due to network issues or client software maintenance reasons, but the clients often wish to receive messages published during the time when the connection was broken.

This is the reason why the MQTT broker which is serving the client should keep a session for the client (per-client’s request by setting the “Clean-Session” flag to false). So the topics to which the subscriber is currently subscribed, and messages (of QoS1 and 2) delivered to these topics etc. are kept by the broker even when the client is disconnected.

When a client having persisted session reconnects, it should not have to re-subscribe the topics, and the broker should send all the pending messages to the client.

We have previously written an article about [MQTT sessions](https://www.emqx.com/en/blog/mqtt-session), it’s a great read if you are interested in more technical details about MQTT sessions.

### Session takeover

Things get a bit more complicated when [MQTT brokers](https://www.emqx.com/en/products/emqx) form a cluster. From the client’s perspective, there are more than one brokers to connect to, and it’s hard to know which broker is the best to connect to. We need another critical component in the network: the load balancer. The load balancer becomes the access point for the entire cluster, and routes the connections from clients to one of the brokers in the cluster.

If a client is connected through the load balancer to a broker (e.g, node1), then disconnected and reconnect later, there is a chance that the new connection might be routed to a different broker in the cluster (e.g, node3). In this case, node3 should start sending pending messages to the client while the client was disconnected. 

There are quite a few different strategies for implementing cluster-wide persisted sessions. For example, the entire cluster can share a global storage which persists the clients' sessions.

However more scalable solutions typically tackle this problem in a distributed way, i.e., there is data migration from one node to another. This migration is called session takeover. Session takeover should be completely transparent to clients, however it comes with a price, especially when there are a lot messages to shuffle around.

![Session takeover](https://static.emqx.net/images/ea4c881df579ece79600af69bec76244.png)


### Sticky session to the rescue

The word ‘sticky’ here is referring to the ability of the load balancer being able to route the client to the old broker at reconnect, which can avoid session take over. This is an especially useful feature when there are many clients reconnecting around the same time, or in case of a problematic client repeatedly disconnecting and connecting again.

For the load balancer to dispatch connections in a ‘sticky’ way, the broker will need to know the client identifier (or sometimes user name) in the connect request – this requires the load balancer to inspect into MQTT packets to look for such information.

Once the client identifier (or user name) is obtained, for a static-size cluster, the broker can hash the client identifier (or user name) to a broker ID. Or for better flexibility, the load balancer can choose to maintain a mapping table from client identifier (or user name) to the target node ID.

In the next section, we’ll demonstrate a sticky table strategy in HAProxy 2.4.

## Sticky session with HAProxy 2.4

To minimise the prerequisites, in this demo cluster, we’ll start two EMQX nodes and an HAProxy 2.4 in docker containers.

### Create a docker network

In order for the containers to connect to each other, we create a docker network for them.

```
docker network create test.net
```

### Start two EMQX 4.3 nodes

In order for the nodes to connect to each other, the container name and the EMQX node name should be assigned within the network namespace (`test.net`).

Start node1

```
docker run -d \
    --name n1.test.net \
    --net test.net \
    -e EMQX_NODE_NAME=emqx@n1.test.net \
    -e EMQX_LISTENER__TCP__EXTERNAL__PROXY_PROTOCOL=on \
    emqx/emqx:4.3.7
```

Start node2

```
docker run -d \
    --name n2.test.net \
    --net test.net \
    -e EMQX_NODE_NAME=emqx@n2.test.net \
    -e EMQX_LISTENER__TCP__EXTERNAL__PROXY_PROTOCOL=on \
    emqx/emqx:4.3.7
```



> **Mind the environment variable**
>
>  `EMQX_LISTENER__TCP__EXTERNAL__PROXY_PROTOCOL`. It is to turn on the binary proxy protocol for TCP listeners so the broker can get the information like the real IP address of the client instead of load balancer’s.

### Make EMQX nodes join a cluster

```
docker exec -it n2.test.net emqx_ctl cluster join emqx@n1.test.net
```

If everything goes as expected, there should such log printed

```
[EMQX] emqx shutdown for join
Join the cluster successfully.
Cluster status: #{running_nodes => ['emqx@n1.test.net','emqx@n2.test.net'], stopped_nodes => []} 
```

### Start HAProxy 2.4

Create a file `/tmp/haproxy.config`with below content

```
global
    log stdout format raw daemon debug
    nbproc 1
    nbthread 2
    cpu-map auto:1/1-2 0-1
    # Enable the HAProxy Runtime API
    # e.g. echo "show table emqx_tcp_back" | sudo socat stdio tcp4-connect:172.100.239.4:9999
    stats socket :9999 level admin expose-fd listeners

defaults
    log global
    mode tcp
    option tcplog
    maxconn 1024000
    timeout connect 30000
    timeout client 600s
    timeout server 600s

frontend emqx_tcp
   mode tcp
   option tcplog
   bind *:1883
   default_backend emqx_tcp_back

backend emqx_tcp_back
    mode tcp

    # Create a stick table for session persistence
    stick-table type string len 32 size 100k expire 30m

    # Use ClientID / client_identifier as persistence key
    stick on req.payload(0,0),mqtt_field_value(connect,client_identifier)

    # send proxy-protocol v2 headers
    server emqx1 n1.test.net:1883 check-send-proxy send-proxy-v2
    server emqx2 n2.test.net:1883 check-send-proxy send-proxy-v2
```

Start haproxy in the test docker network:

```
docker run -d \
    --net test.net \
    --name proxy.test.net \
    -p 9999:9999 \
    -v /tmp/haproxy.cfg:/haproxy.cfg \
    haproxy:2.4 haproxy -f /haproxy.cfg
```

### Test it out

Now we use the popular mosquitto MQTT client (also in docker) to test it out. 

We start a subscriber (named `subscriber1`) which subscribes to `t/#`topic

```
docker run --rm -it --net test.net eclipse-mosquitto \
    mosquitto_sub -h proxy.test.net -t 't/#' -I subscriber1
```

And then publish a `hello` message to `t/xyz`from another client

```
docker run --rm -it --net test.net eclipse-mosquitto \
    mosquitto_pub -h proxy.test.net -t 't/xyz' -m 'hello'
```

The subscriber should print out `hello` message if everything is working as expected.

## Inspect the sticky table in HAProxy

We can also inspect the sticky table created in HAProxy with this command. It requires `socat` command, so I am running it from the docker host.

```
show table emqx_tcp_back" | sudo socat stdio tcp4-connect:127.0.0.1:9999
```

This should print the current connections like below:

```
# table: emqx_external_tcp_listners, type: string, size:102400, used:1
0x7f930c033d90: key=subscriber1 use=0 exp=1793903 server_id=2 server_key=emqx2
```

In this example, the client `subscriber1` is sticked to server `emqx2`.

## Other articles in this series

- [MQTT broker clustering part 1: Load balancing](https://www.emqx.com/en/blog/mqtt-broker-clustering-part-1-load-balancing)
- [MQTT broker clustering part 3: Challenges and Solutions of EMQX horizontal scalability](https://www.emqx.com/en/blog/mqtt-broker-clustering-part-3-challenges-and-solutions-of-emqx-horizontal-scalability)
