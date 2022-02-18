In early January, EMQX 5.0-beta.3 was released. Besides continuing the development of the 5.0-beta.4, EMQX team will also continue the maintenance releases for both the open-source and enterprise v4.3 and v4.4.

In terms of cloud services, custom HTTP authentication and Webhook alarm mode were added in [EMQX Cloud](https://www.emqx.com/en/cloud) this month, allowing users to use the product more flexibly and freely while obtaining more reliable business assurance.

## EMQX

### The New Dashboard

After weeks of testing, we managed to release v5.0-beta.3, which was still an early version. In this version, we made the new Dashboard available by default. Now you are welcome to download the package and give it a try [https://github.com/emqx/emqx/releases/tag/v5.0-beta.3](https://github.com/emqx/emqx/releases/tag/v5.0-beta.3). Please bear with us though: the UI is still being polished, and some configuration pages for the rule engine are still being worked on.

### 100-million Milestone Reached!

By the end of January, EMQX team managed to reach 100 million unique wildcard subscribers in a 22-nodes EMQX 5.0 cluster. The team is continue optimising the performance. Then we’ll try to run some tests with real traffic. When the release is stable, we’ll publish the design and test setup in detail as blog posts.

### Hello, Elixir Community

Now we can build EMQX on Elixir! When EMQX 5.0 goes GA, you will be able to download the packages built on Elixir. Please note though, the Elixir release will not support hot-beam upgrade for now.

We have no intention to rewrite anything though. i.e. The project will continue to be an Erlang project. The idea of building on Elixir are:

- To make Elixir developers feel at home when they want to develop plugins
- We will be able to develop new features using Elixir (hopefully starting from 6.0)

### Better Upgrade Experience

Since v4.2, EMQX supports the hot update of the patch version (there is no need to restart the node and it does not affect the business); Since v4.3, the minor version upgrade supports the rolling upgrade of cluster nodes.

Starring from v5.0, we will support rolling upgrade of clusters across major versions to further reduce the upgrade complexity.

In 5.0, there will be the so-called backplane APIs to rule the intra-cluster RPC calls. With the automated static check to ensure API compatibility, we’ll be able to provide a much better upgrade experience comparing to earlier versions. 

### Continue Supporting v4 Releases

We’ll continue support v4.3 and v4.4 releases. In addition to patch fixes, there are also some new features and enhancements.

Rule engine patches and enhancements: There will be more metrics with regards to SQL execution results including failure statistics etc.
ACL statistics improvement: Cache hits are counted as successful, and we’ll be able to tell apart the non-cached query hits.

The online Tracing: Newly introduced in version 4.4.0 has improved the rendering method of log content in this upgrade, which uses color and highlight to distinguish the content, so as to further optimize the log browsing experience.

In addition, for Enterprise edition, the Lindorm DB integration which was introduced in e4.4.1 will be ported back to e4.3.6. 

## EMQX Cloud

### Custom HTTP authentication

EMQX Cloud launched the HTTP custom authentication in January. HTTP authentication allows users to connect to a self-built external HTTP application authentication data source, and determine the authentication result according to the data returned by the HTTP API, so as to realize complex authentication and complex access control logic. The function of custom HTTP authentication can be configured in [Deployment] - [Deployment Details] - [Authentication].

The principle of custom HTTP authentication is that EMQX Cloud uses the current client-related information as parameters in the device connection event, initiates a request to the user-defined authentication service for query permissions, and processes the authentication request through the returned HTTP status code. Users can configure parameters for connection authentication and access control.

![Custom HTTP authentication](https://static.emqx.net/images/1440c17c75d0e5fb1e57e26aa568596b.png)
 
For the deployment of the basic version, the request address for authentication and access control needs to be filled in the relevant request link of the public network. For the deployment of the professional version, the VPC configuration needs to be completed first, and the address of the service intranet needs to be filled in.

Custom authentication allows users to perform authentication more flexibly according to their own business needs. As a cloud service of middleware, it provides better methods of integration and connection, solves the problem of complex authentication processes for massive devices, and greatly improves the security of authentication.

### Feature of sending test information is added to Webhook alarm

The feature of sending alarm messages to IM tools and self-owned services through Webhook was also launched. At the same time, in order to facilitate users to test whether the configuration is successful, the alarm function can send a test message to immediately verify whether the Webhook address is configured correctly.

![EMQX Cloud Webhook](https://static.emqx.net/images/dba040b539d557a14a1c98e2b9946fa0.png)
 
So far, EMQX Cloud supports the three modes of mailbox alarm integration, PagerDuty event alarm integration, and Webhook alarm integration. The rich alarm integration modes and alarm events will make the automatic early-warning module of the entire product more complete, so as to bring users more stable business assurance.

### Basic version expansion

At present, EMQX Cloud has supported the expansion of the current deployment. Users can scale the deployment specifications according to their connection requirements. At the same time, the disconnection time of equipment during capacity expansion is also optimized, so as to reduce the interference to the business system.
