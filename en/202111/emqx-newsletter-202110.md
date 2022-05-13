Besides making EMQX stronger and faster as an [MQTT messaging broker](https://www.emqx.io), we also try hard to make it ops-friendly. From configuration to management API, dashboard UI to live code upgrade, single node docker run to massive scale clustering.

In October, EMQX development teams have been mostly focusing on HTTP management API, the readiness of which will be checkpoint for the beta.2 release.

## EMQX v5.0-beta.2 updates

For beta.1 release at the end of September, our focus was to get the configuration interface ready (the HTTP APIs were unstable at the moment). Our primary focus for beta.2 is to get the management HTTP APIs stable.
We are also working on two more features that missed the beta.1 release, hierarchical rate control and cross-node session migration which will hopefully be released as a part of the beta.2

### Brand new management HTTP API
 
As we have previously mentioned, the new APIs are designed following OpenAPI (Swagger) 3.0 specification.

And the release comes with a built-in UI which demos `curl` command examples, as well as a "Try it out" button which make it easy to test thing out from the web UI.

This screenshot is an example “Try it out” result, which fetched back the configuration for an HTTP authentication API.

![EMQX HTTP API](https://assets.emqx.com/images/deeea65360c4170719da545a84ab07e5.png)

### Hierarchical rate control

Up until EMQX 4.3, the messaging rate limit control was done at connection level. To set rate controls at levels, we are introducing the new hierarchical rate control feature.

This will allow users to control message rates at ‘global', ‘zone’, ‘listener’, and ‘connection’ levels.

### Replicated session state

Before 5.0, EMQX already provides highly available persistent sessions across the nodes in a cluster. The state however is not replicated, that is, the session states are local to the node which is serving the client. Session take-over is triggered if the client moves from one node to another in the cluster. This has been working quite well given that EMQX cluster’s long uptime with the help from live-code-upgrade (hot-patching without restarting the service).

To be more ops-friendly, we are now introducing cross-node session state replication. This will allow users to shut down a broker for maintenance without losing the persistent session states.


<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">No credit card required</div>
    </div>
    <a href="https://www.emqx.com/en/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a >
</section>
