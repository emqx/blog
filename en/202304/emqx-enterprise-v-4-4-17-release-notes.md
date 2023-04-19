We are thrilled to announce that [EMQX Enterprise](https://www.emqx.com/en/products/emqx) version 4.4.17 has been officially released! This release enhances the performance of the [rule engine](https://docs.emqx.com/en/enterprise/v4.4/rule/rule-engine.html), and it also involves log enhancements and bug fixes.

## Performance enhancement of Rule Engine

The [Rule Engine](https://docs.emqx.com/en/enterprise/v4.4/rule/rule-engine.html) is a crucial component of EMQX Enterprise that offers built-in SQL-based data processing capability. It is used for data routing, extracting, filtering, and format transforming, making it a key feature for accelerating IoT application integration and driving business innovation. 

In previous releases,  the rule engine was found to consume significant CPU in rule queries and matching when handling a large number of running rules. This leads to reduced efficiency and slower data processing times.

To address this issue, EMQX Enterprise v4.4.17  significantly improves the rule execution efficiency in scenarios with a large number of rules. In a test conducted on a 32-core 32GB server, with the creation of 700 simple rules and each rule executed at a speed of 1000 messages per second, the CPU usage of the rule engine decreased to 55%~60% compared to the previous version.

## Log Enhancements

### 1. Proxy Protocol Errors No Longer Logged for Better Performance

EMQX deployed behind a load balancer can enable the Proxy Protocol protocol on the listener to obtain the client's real IP address. If the load balancer continues to send health check requests to the listener port, EMQX will generate a large number of error logs and cause the large I/O and disc consumption.

```
[error] supervisor: 'esockd_connection_sup - <0.3265.0>', errorContext: connection_shutdown, reason: {recv_proxy_info_error,tcp_closed}, offender:
```

To address this issue, EMQX listeners will no longer print Proxy Protocol error logs.  Users can still view error statistics through the `emqx_ctl listeners` command. If there are any errors, the corresponding reason will be displayed as `proxy_proto_close`.

```
$ ./bin/emqx_ctl listeners
...
mqtt:tcp:external
  listen_on       : 0.0.0.0:1883
  acceptors       : 8
  max_conns       : 1024000
  current_conn    : 0
  shutdown_count  : [{proxy_proto_close,1}]

```

### 2. Enhancement of listener file descriptor exhaustion logs

The error log generated when the number of open file descriptors for a listener reaches its limit is difficult to identify. In this release, we have added more descriptive content to enhance error identification and help users quickly locate the cause of the error.

Previous version：

```
[error] Accept error on 0.0.0.0:1883: emfile
```

Current version：

```
[error] Accept error on 0.0.0.0:1883: EMFILE (Too many open files)
```

 

## Bug Fix List

The following are important bug fixes, for all bug fixes please refer to [EMQX Enterprise Edition 4.4.17 Changelogs](https://www.emqx.com/en/changelogs/enterprise/4.4.17).

- Fixed the issue where `Erlang distribution` could not use TLS [#9981](https://github.com/emqx/emqx/pull/9981).

  For more information on `Erlang distribution`, see [here](https://www.emqx.io/docs/en/v4.4/advanced/cluster.html).

- Fixed the issue where MQTT bridging could not verify TLS certificates with wildcard domains on the peer side [#10094](https://github.com/emqx/emqx/pull/10094).

- Fixed the issue where EMQX could not timely clear the information of disconnected MQTT connections when there were too many messages backlogged in the retainer. [#10189](https://github.com/emqx/emqx/pull/10189).

- Fixed the issue where the path of the template file `service-monitor.yaml` in the Helm Chart was incorrect. [#10229](https://github.com/emqx/emqx/pull/10229)

- When upgrading from EMQX 4.3 to 4.4, EMQX will migrate the ACL table in the "built-in authentication" module upon restart.

- Fix the issue of incorrect counting statistics for the IoTDB action.

- Fix the issue of incorrect encoding of error messages returned by the HTTP API

- Fix the process leak issue of the Apache RocketMQ client in EMQX [rocketmq-client-erl#24](https://github.com/emqx/rocketmq-client-erl/pull/24).

## Summary

The EMQX 4.4.17 release brings significant improvements to its Rule Engine, which now performs much better in complex applications with a large number of rules. Moreover, the release addresses issues related to logging. These improvements are aimed at providing users with a better and more efficient experience while using EMQX in their IoT applications.

Contact EMQX Enterprise support for any questions or assistance: [Contact Us →](https://www.emqx.com/en/contact?product=emqx)



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
