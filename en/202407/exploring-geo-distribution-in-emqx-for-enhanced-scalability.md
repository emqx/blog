## The Concept of Geo-Distribution

When we talk about EMQX, the thing usually mentioned first is its impressive scalability. Although EMQX scales almost linearly with the amount of hardware thrown at it, scalability on a single compute instance is inevitably limited: the instance's resources become exhausted, and the cost of upgrading it grows exponentially. This is where *distribution* comes into play, allowing us to scale further by deploying clusters of EMQX nodes across multiple compute instances. Thanks to the rich clustering capabilities of EMQX, this task is relatively straightforward.

With distribution, we are no longer limited to a single geographic location. We can even deploy an EMQX cluster across multiple data centers on different continents, a process called *geo-distribution*. The main benefit of geo-distribution is being closer to the clients when they are spread across continents. Each client can connect to the nearest EMQX instance and enjoy communication with lower latency, better reliability, and, as a result, higher throughput. Another valuable benefit is fault tolerance: a data center outage will not affect the whole service, only part of it.

## Challenges

However, as often happens, any distribution comes with an inherent cost. And the cost of geo-distribution is especially high.

1. Instances are separated by a network, and the network is slow.

   Well, not particularly slow, but much slower than communication between CPU cores on the same instance, where latency is measured in nanoseconds. Network introduces *latency*. The more distant the instances are from each other, the higher the latency is. We can not optimize it away, because it is subject to the laws of physics. Thus, someone has to pay for it. If we're closer to the clients, whether they are in Australia or Brazil, some of the EMQX nodes on the other hand will inevitably be far away from each other, and communication between them will be slower. In that case, tens-of-milliseconds slower.

1. Network is unreliable.

   Packets get lost, and connections get dropped due to network congestion, hardware failures, misconfiguration, or even malicious activity. The farther away two EMQX nodes are from each other, the more intermediate network equipment they have to go through and more wires to travel, which increases the chances of failures occurring. While some of them are handled by the network stack and will only manifest in latency spikes, others will propagate to the application layer and bring a lot of uncertainty. In the presence of such failures, an EMQX node can not tell whether some remote node is down or if the network is just unusually unreliable. It is a manifestation of what is known as *partial failure*, and can lead to reduced *availability*.

Strictly speaking, when we are talking about latency, we need to take into account *throughput* as well. Even a high-latency network can have a sufficiently high throughput. However, the unreliable nature of the network usually makes it hard to achieve high throughput. In the case of TCP connections, even a single packet loss can cause a significant drop in throughput, because the TCP stack will have to retransmit the packet and significantly scale down the transmission window. Again, the further away communication peers are from each other, the more often this will happen.

Adding to the problem, raw network throughput is usually not crucial for many clients. Rather, the throughput of various *operations* conducted over the [MQTT protocol](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt) is what counts. For example, throughput of message publishing, or throughput of `SUBSCRIBE` operations. It is where the *shared state* comes into play and, more importantly, the need to *coordinate* updates of this state.

Thanks to the nature of the MQTT protocol, which operates in an asynchronous manner and where the clients are relatively independent of each other, the insidiousness of the shared state is not that prominent. Yet, it is still there. But first, to better understand the problem, let's start with setting up a basic geo-distributed EMQX cluster.

## A Cluster 12600 km Wide

As you might already know, EMQX 5 follows a new deployment model, where the cluster consists of two types of nodes: *core* and *replicant*. This model was specifically designed to support a broader range of deployment scenarios, including geo-distribution, though with some pitfalls, which we will explore later. Under this model, a cluster consists of 2 types of nodes: core nodes that manage essential parts of the shared state and replicant nodes that do not participate in the state management but simply replicate state changes made by the core nodes.

Nevertheless, let us first deploy a cluster in a more traditional fashion, so we can better understand where the benefits of the new model could come from. Our “traditional” cluster will consist of 3 core nodes geographically distributed over 3 continents.

| **Location**             | **Node name**        |
| :----------------------- | :------------------- |
| Frankfurt (eu-central-1) | `emqx@euc1.emqx.dev` |
| Hong Kong (ap-east-1)    | `emqx@ape1.emqx.dev` |
| Cape Town (af-south-1)   | `emqx@afs1.emqx.dev` |

![EMQX Geo-Distribution 1](https://assets.emqx.com/images/3f0d2c80af41b939f5e2b82050ba9f2d.png)

One more “traditional” thing about our cluster that will help us understand the problem space better and illustrate the improvements we've made is this small configuration snippet:

```
broker.routing.storage_schema = v1  # use pre-5.4.0 routing table schema
```

The first thing that starts to hint that this was not the best idea is how much time it took for the cluster to become operational. The logs indicate that certain `mria` initialization steps take **whole seconds** to complete.

```
15:11:42.654445 [notice] msg: Starting mria, mfa: mria_app:start/2
15:11:42.657445 [notice] msg: Starting shards, mfa: mria_app:start/2
15:11:47.253059 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: '$mria_meta_shard', tables: ['$mria_rlog_sync',mria_schema]
15:11:48.714293 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: emqx_common_shard, tables: [bpapi,emqx_app,emqx_banned,emqx_trace]
15:11:50.188986 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: emqx_cluster_rpc_shard, tables: [cluster_rpc_commit,cluster_rpc_mfa]
15:11:51.662162 [info] msg: Setting RLOG shard config, mfa: mria_config:load_shard_config/2, shard: emqx_cluster_rpc_shard, tables: [cluster_rpc_commit,cluster_rpc_mfa]
...
```

Why is that? The nodes are not **that** far away from each other. We could easily see that from the ping times.

```
v5.7.0(emqx@euc1.emqx.dev)> timer:tc(net_adm, ping, ['emqx@afs1.emqx.dev']).
{161790,pong}
v5.7.0(emqx@euc1.emqx.dev)> timer:tc(net_adm, ping, ['emqx@ape1.emqx.dev']).
{202801,pong}
```

Indeed, a packet takes ~160 milliseconds to travel from Frankfurt to Cape Town and back and ~200 milliseconds to Hong Kong and back. Well, the reason is that `mria` uses `mnesia` under the hood, and `mnesia` is a *distributed database*. Each initialization step is essentially a database transaction, and each transaction has to be coordinated between (at least) the majority of the nodes. Each coordination step in turn requires more than one round-trip between the participating nodes. In this case, the shared state is the database schema, and this coordination is necessary to ensure that the schema is *consistent* across all nodes in the cluster.

With that in mind, let's see how this affects the performance of a single class of operations: `SUBSCRIBE`.

## Latency Hurts

After a painful couple of minutes, the cluster is finally ready to be hit with some load. Armed with [mqttx-cli](https://mqttx.app/), we will see how long it takes to open a connection to the cluster and subscribe to a single topic.

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1 --topic t/mqttx/%i
[9:14:29 AM] › | Start the subscribe benchmarking, connections: 1, req interval: 10ms, topic: t/mqttx/%i
✔  success   [1/1] - Subscribed to t/mqttx/1
[9:14:30 AM] › | Created 1 connections in 0.89s
```

Almost a second. Noticeably longer than either 160 or 200 milliseconds. To understand why, we should consider how exactly MQTT client and broker negotiate connection and subscription:

1. The client opens a connection to EMQX and sends a `CONNECT` packet.

   The packet contains Client ID property, and the spec dictates that a broker must only have one client with such ID in the cluster. That “only one” part here is the key. If multiple clients attempted to connect to different nodes simultaneously with the same Client ID, it would create a *conflict* that should be resolved. The broker must have a [strongly consistent](https://jepsen.io/consistency/models/strict-serializable) view of all connected clients, which implies that any changes made must be coordinated with the majority of the nodes. Moreover, to add insult to injury, strong consistency is enforced through global locks, which first need to be acquired and then released. Hence, a cluster node must perform two rounds of communication with the majority, one after another, to complete this operation. If we are unfortunate enough, the farthest node will be part of the majority, and this operation will cost us two round-trips to that node.

1. The client sends a `SUBSCRIBE` packet.

   This one is simpler. EMQX only needs to communicate to the majority that someone on this node subscribed to `t/mqttx/1`, allowing messages to be routed correctly to the right place later. This type of change does not require complex coordination, as no conflicts are possible here. Yet, one round-trip to the cluster peers is still necessary.

Overall, this operation should have taken ~600 milliseconds, but we live in an imperfect world with imperfect networks. Making the client wait for 1 second is not great, but what about the throughput?

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/%i
[9:32:19 AM] › | Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/%i
✔  success   [100/100] - Subscribed to t/mqttx/100
[9:32:21 AM] › | Created 100 connections in 1.706s
```

Well, it took 2x more time to handle 100x more clients. Great news! With this workload, the clients are essentially independent of each other because each client connects with a unique Client ID and subscribes to a unique topic. There are no conflicts, so the time factor should have been 1x. However, this is not the case because EMQX artificially limits *concurrency* by default as a safety measure, allowing it to act more predictably under load. Internally, EMQX serializes subscriptions per topic to avoid data races and optimize away unnecessary work, and by default, there are a limited number of processes acting as serialization points. But there is good news: this limit is [now configurable](https://github.com/emqx/emqx/pull/11390) and can be increased to accommodate such expansive deployments.

## Conflicts Hurt Harder

We will now see what happens when we slightly change the workload: each client will subscribe to a unique topic filter but with a common prefix.

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1 --topic t/mqttx/+/%i/sub/+/#
[9:48:44 AM] › | Start the subscribe benchmarking, connections: 1, req interval: 10ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1/1] - Subscribed to t/mqttx/+/1/sub/+/#
[9:48:47 AM] › | Created 1 connections in 2.938s
```

Ouch! Almost 3 seconds. What happened? Well, topic filters are to blame. EMQX now needs to maintain an *index* of topic filters across the cluster to match and route messages efficiently. This index gets updated whenever a client subscribes or unsubscribes from a topic, and this update needs to be applied consistently for this index to be identical on all nodes. Once again, this requires transactions, transactions require coordination, and coordination requires many rounds of communication between the cluster nodes, worth a lot of round-trips across the network.

Hopefully, even though the latency is high, the throughput should be better, right?

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[9:44:43 AM] › | Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [100/100] - Subscribed to t/mqttx/+/100/sub/+/#
[9:46:25 AM] › | Created 100 connections in 101.958s
```

OK, that was very painful to watch. One hundred clients took 102 seconds. We lost all the benefits of concurrency, even though the workload still looks more or less the same: clients with unique Client IDs subscribe to unique topic filters. Well, the culprit here is the design of the legacy *v1* index. To quickly match messages to topic filters, the index is organized as a *trie*, and EMQX tries to keep it compact by tracking common prefixes. When a client subscribes to `t/mqttx/+/42/sub/+/#`, EMQX needs to touch records for `t/mqttx/+/42/sub/+` and `t/mqttx/+`. The problem is that every other client's subscription will also cause an update to the `t/mqttx/+` record, and this is where *conflicts* happen. When conflicts arise, `mnesia` deals with them like a classic database: by locking the records and effectively serializing the updates. As more clients subscribe, the number of conflicts increases, and the more time it takes to resolve them.

We were lucky here: if there were any connectivity troubles, they were mild enough to be dealt with by the TCP stack. If the network had exhibited more severe instability to cause one of the nodes to become unreachable, transactions would have started to time out. Transactions of this nature could have grabbed locks on the records, which would have remained held until the transaction timed out. This scenario would have effectively blocked all the other transactions involving conflicting records, thus stalling the subscriptions altogether.

## Avoiding the Conflicts

Luckily, this *v1* schema we've manually enabled for our cluster is no longer the default, and the new [*v2*](https://github.com/emqx/emqx/pull/11524) schema was considered pretty robust and performant enough to take its place as the default starting from [EMQX 5.4.0](https://github.com/emqx/emqx/releases/tag/v5.4.0). The main difference that radically improves the situation is that it's *conflict-free*: no matter how messy and complex topic filters your clients are using, there's zero chance managing them will involve write conflicts. You don't need to worry about potential clashes in subscription patterns anymore.

Let's throw away this piece of configuration we've been using and see how *v2* fares against the “traditional” one.

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[9:46:54 PM] › ℹ  Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [100/100] - Subscribed to t/mqttx/+/100/sub/+/#
[9:46:55 PM] › ℹ  Created 100 connections in 1.673s
```

Impressive! That was even better than expected: 100 clients took less than what 1 client took in the previous scenario.

However, we're still far from the theoretical limit of 600 milliseconds, give or take. Admittedly, it's unrealistic to reach this limit unless our network is perfect. But there's a room for improvement, let's explore other ways to make the latency more bearable.

## Replicants to the Rescue

Obviously, we could optimize our workloads to better fit them into our deployment model, but the price of latency would still need to be paid anyway. Instead, let us throw away our “traditional” deployment and deploy EMQX in a cluster comprised of 3 co-located core nodes and 3 replicants, geographically distributed over the same 3 continents.

![EMQX Geo-Distribution 2](https://assets.emqx.com/images/460cdbd66a7e51e84f988f1574874025.png)

This way, all the costly state changes will be carried only by the core nodes, where the latency is low, and the replicants will only need to keep up with the state changes. As before, clients will connect to the closest node, no matter if it's a core node or a replicant.

| **Location**             | **Node name**                                                |
| :----------------------- | :----------------------------------------------------------- |
| Mumbai (ap-south-1)      | `emqx@core1.emqx.dev` `emqx@core2.emqx.dev` `emqx@core3.emqx.dev` |
| Frankfurt (eu-central-1) | `emqx@euc1.emqx.dev`                                         |
| Hong Kong (ap-east-1)    | `emqx@ape1.emqx.dev`                                         |
| Cape Town (af-south-1)   | `emqx@afs1.emqx.dev`                                         |

Up and running! No need to wait whole minutes as before.

We could instantly see the benefits of this deployment model: there is no need anymore to pay a few round-trips across half of the globe per transaction. The latency is still there because EMQX needs to handle `CONNECT` and `SUBSCRIBE` packets one after another, but it's much better now.

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1 --topic t/mqttx/+/%i/sub/+/#
[10:57:44 AM] › | Start the subscribe benchmarking, connections: 1, req interval: 10ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1/1] - Subscribed to t/mqttx/+/1/sub/+/#
[10:57:45 AM] › | Created 1 connections in 0.696s
```

The throughput is also much better now because the transaction handling is carried out only by the core nodes, which are very close to each other.

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 100 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[11:04:35 AM] › | Start the subscribe benchmarking, connections: 100, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [100/100] - Subscribed to t/mqttx/+/100/sub/+/#
[11:04:37 AM] › | Created 100 connections in 1.091s
```

That's a notable improvement. Remember that we started with 100 clients taking more than 100 seconds to do the same thing.

## Hiding the Latency

Before, we briefly mentioned that the throughput may be actually artificially limited by the default number of processes in a pool acting as serialization points to avoid race conditions. Increasing the load 10 times should help us observe the effects of this limit.

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1000 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[11:42:39 PM] › ℹ  Start the subscribe benchmarking, connections: 1000, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1000/1000] - Subscribed to t/mqttx/+/1000/sub/+/#
[11:42:43 PM] › ℹ  Created 1000 connections in 4.329s
```

With 10 times more network traffic it's likely that the misbehaving network is mostly to blame, but the total time is still 4 times worse. Can we do better? Thankfully, there's another improvement we have been working on and that landed in the [EMQX 5.5.0](https://github.com/emqx/emqx/releases/tag/v5.5.0) release: [batch synchronization](https://github.com/emqx/emqx/pull/12329) of routing table updates. It is designed to better utilize the available network throughput when the communication is reliable, without increasing latency of operations when it's already too high.

This feature is not yet enabled by default, but it's pretty easy to turn on.

```
broker.routing.batch_sync.enable_on = replicant
```

This snippet enables batch synchronization only on replicants. Setting it to `all` would enable it on all nodes, and in general will likely be beneficial for a wide variety of workloads, mostly thanks to the broker pool being freed up from doing extra synchronization work. In our case, the effects would not be as pronounced and harder to illustrate.

The default is `none`, and the reason for that is safety. We want to provide a smooth rolling upgrade experience, and enabling it *before* rolling out EMQX 5.7.0 over, let's say, 5.4.1 could lead to some temporary unavailability. If you find yourself upgrading from EMQX 5.5.0 or later, you should not worry about enabling it right away.

Ok then, let's see how it goes now.

```shell
$ mqttx bench sub -h ape1.emqx.dev --count 1000 --interval 0 --topic t/mqttx/+/%i/sub/+/#
[11:46:21 PM] › ℹ  Start the subscribe benchmarking, connections: 1000, req interval: 0ms, topic: t/mqttx/+/%i/sub/+/#
✔  success   [1000/1000] - Subscribed to t/mqttx/+/1000/sub/+/#
[11:46:24 PM] › ℹ  Created 1000 connections in 2.585s
```

Pretty significant improvement. The network throughput is now used more efficiently, which in turn translates to better `SUBSCRIBE` throughput. Roughly the same effect could most likely be achieved by inflating process pool at the cost of more bookkeeping and increased memory usage, but this new feature is more flexible and easier to use.

Why are we still far from the theoretical limit of ~600 milliseconds? The most plausible explanation is how occasional network hiccups are handled. A link may be congested for a quick moment, which would cause a packet or few to be lost, and the TCP stack would have to retransmit them once *RTO (retransmit timeout)* passes. This is usually barely noticeable in an already established connection, but there's often a huge difference when an initial SYN packet is lost. In this case, the TCP stack had no chance to estimate the optimal RTO yet, so it would have to start with a conservative default of *1 second*. Coming back to our workload, it's likely that while most of the clients were able to connect and subscribe in a fraction of a second, a couple of them tripped over SYN packet loss, which in turn caused the total time to increase by a second. Or, if we were extremely unlucky, two seconds.

It's important to mention that, as always, there are apparent trade-offs of this deployment model: the cluster needs more computing resources and becomes less resilient to failures due to all the core nodes residing in the same data center. Nevertheless, given the benefits, it is a trade-off worth making. Furthermore, thanks to new configuration options and the new topic index design, we could reasonably expect poor subscription latency will be offset by (theoretically, almost unlimited) throughput gains. Consider trying out recent [EMQX 5.7.0](https://github.com/emqx/emqx/releases/tag/v5.7.0) release that has all these features configurable and well-tested.

If you find yourself deploying this kind of cluster for your geo-distributed application, definitely consider further [tuning the configuration](https://docs.emqx.com/en/emqx/v5.7/configuration/configuration.html). There are now a couple of extra configuration parameters worth tweaking to improve the performance of a multi-region EMQX cluster. Here is an `emqx.conf` example with parameters applicable to both core and replicant nodes combined for simplicity.

```shell
# Core nodes
node.default_bootstrap_batch_size = 10000
# Replicants
node.channel_cleanup_batch_size = 10
```

Now for the brief overview of what those parameters affect.

- `node.channel_cleanup_batch_size`

  Relevant for replicant nodes. If the network latency is high, significantly reducing this value from the default 10,000 improves performance during an abrupt disconnect of large numbers of clients.

- `node.default_bootstrap_batch_size`

  Relevant for core nodes. The default value is 500, but it can be greatly increased to reduce the time it takes for a replicant node to join a cluster with many active subscriptions.

## Alternatives

Nevertheless, there are situations where latency this high is not acceptable. EMQX has a solution for these situations: rather than setting up a geo-distributed cluster, it is possible to deploy a separate independent cluster per region and connect those clusters through [asynchronous MQTT bridges](https://docs.emqx.com/en/emqx/v5.7/data-integration/data-bridge-mqtt.html). It is a radically different deployment model, which demands additional compute resources and operational overhead. However, it offers a clear advantage: the shared state does not need to be consistently maintained across three continents. Each cluster will have its own state, and any changes induced by subscriptions will be handled locally, making the latency low.

Egress MQTT bridges in asynchronous mode are designed to interact with *external* resources, and in a way, remote EMQX clusters located on the other side of the globe are just that. Bridges have buffers backed by memory or durable storage, and they can handle intermittent connectivity issues often encountered in unreliable networks.

Without a single global view of the connected clients and their subscriptions, it is no longer possible to route only a subset of messages to a particular region. Each MQTT bridge on each node will have to stream the **whole** message flow to each remote location, saturating the egress bandwidth. It also inevitably comes with a loss of information: bridged messages will no longer have information about the original client. Besides, some effort is necessary to guarantee that the same bridged messages do not travel back and forth between the continents. However, [Rule engine](https://docs.emqx.com/en/emqx/v5.7/data-integration/rule-sql-syntax.html) should be expressive enough to handle this.

These shortcomings are what recently prompted us to work on another, more flexible solution: [Cluster Linking](https://github.com/emqx/emqx/pull/13126). The design goal was to combine the best of both worlds: have both the reliability and robustness of communication with external resources and the ability to route only those messages a particular region is interested in, thus avoiding unnecessary waste of bandwidth and computing resources. This feature should see the light of day in the upcoming EMQX Enterprise 5.8.0 release.

## Conclusion

In the end, as always, it all comes down to choosing between acceptable trade-offs. As far as we know, there is no way to cheat the speed of light, so we have to bite the bullet and pay the price of increased latency. However, we can still make it more bearable by choosing a suitable deployment model and optimizing our workloads.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient">Contact Us →</a>
</section>
