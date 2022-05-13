## v4.3 released!

In May, we were so happy to announce the final release of EMQX broker v4.3. The great feedback received from the community proved the worth of ours hard work. Check out the[ release note ](https://github.com/emqx/emqx/discussions/4763)for more details.

Although a lot of changes originally planned for v5 have been pushed earlier to v4.3, the greater remaining work for v5 is just getting started, and everybody is so pumped to get started.

### Cluster stability improvement – massive re-subscription

We have conducted large-scale (2 million connections) connect/reconnect tests to verify a previously flaky situation when involving wildcard subscriptions. 


Stay tuned for our blog posts for more details.

### Cluster stability enhancement - sticky session load balancing

Kudos to haproxy team, now there is the first [MQTT protocol](https://www.emqx.com/en/mqtt) supported load balancer offered in the community edition. With the help of the stick table keyed by the MQTT client ID, we expect the number of [MQTT session](https://www.emqx.com/en/blog/mqtt-session) takeover/migration between the clustered nodes to be significantly reduced. 

And it’s amazingly simple to enable it, here is an example.

```
backend emqx_tcp_back
    mode tcp
    # Create a stick table for session persistence
    stick-table type string len 32 size 100k expire 30m
    # Use ClientID / client_identifier as persistence key
    stick on req.payload(0,0),mqtt_field_value(connect,client_identifier)
    server emqx-1 node1.emqx.io:1883 check-send-proxy send-proxy-v2
    server emqx-2 node2.emqx.io:1883 check-send-proxy send-proxy-v2
```


## v5.0 Go cloud-native, at full speed

As we previously wrote in the newsletters, some of the team members have started working on v5.0 tasks from early this year. And the main theme of this version will be: cloud-native. Here are some highlights of the exciting new features we are working on.

### Infrastructure as code

We are adopting [HOCON](https://github.com/lightbend/config) in v5.0 for two reasons: 1) It is almost a drop-in replacement for the cuttlefish format EMQX has been using; 2) It is “just JSON”, which is the only sensible format to use when posting requests in http API. 

HOCON will allow us to finally unify the two management interfaces: configuration file, and HTTP-API. (the future CLI will be wrapped around HTTP-API).

With the new configuration and API, we will in v5.0 support resource creation from infrastructure as code deployments (such as ansible templates, Kubernetes config maps etc), as well as HTTP APIs backing the dashboard UI and even scripts.

### Stateless nodes

Since the kick-off of Rlog project in February 2021, we have been making steady progress.

Rlog (short for replicated transaction logs) is to split the cluster into two roles of node sets, core nodes and replicant nodes. Core nodes will form a (meshed) cluster just like how we form a cluster today, and replicant nodes will receive database updates asynchronously. 

For a quick introduction, please check out this [demo recording](https://www.youtube.com/watch?v=aX4jV6z24sk&list=UU5FjR77ErAxvZENEWzQaO5Q&index=13) (and the following up updates too).

The stateless nature of the replicant nodes will make deployment in the cloud a lot simpler.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
