## Background

To lower the cost of deploying and maintaining EMQX on Kubernetes, we incorporate routine operational capabilities into the code, helping users realize automatic deployment and maintenance through [EMQX Kubernetes Operator](https://github.com/emqx/emqx-operator).

Upgrading EMQX on Kubernetes using the EMQX Kubernetes Operator (v1beta1, v1beta2, and v1beta3) has traditionally been done with a rolling upgrade method. This process is outlined as follows:

![Upgrading EMQX on Kubernetes](https://assets.emqx.com/images/fe635958396b616466a7195f3e18b419.png)

## Problem Analysis

Rolling upgrades in production environments can present several challenges, including:

1. Client-side disconnections during the upgrade process, as old nodes are replaced sequentially with new ones. This can negatively impact the user experience, and in worst case scenarios, the number of disconnections can equal the number of nodes.
2. A high volume of client reconnection attempts when replacing a node in a cluster with a high number of connections. This can cause server overload, as clients attempt to reconnect based on their retry policies.
3. Imbalanced load distribution among nodes after completion of the upgrade, which can disrupt capacity planning and potentially impact service availability. As illustrated in above figure, clients may connect to emqx-ee-1 or emqx-ee-2 instead of emqx-ee-0 during the upgrade process of emqx-ee-0, resulting in emqx-ee-0 having few connections after the upgrade is completed.
4. The use of StatefulSets for deployment can result in one less node providing service during the upgrade process, leading to increased pressure on the server and potentially impacting the user's business model.

Simultaneous occurrence of above issues, for example, multiple disconnections along with a large number of disconnected clients repeatedly attempting to reconnect, can exacerbate the problem, leading to amplification of client reconnections and potentially causing server overload or service crashes.

The chart below illustrates the number of connections during the current upgrade mode, which can be affected by various factors such as resources used by the backend, server configuration, and client reconnection policies.

- sum: The total number of connections, represented by the top line in the chart.
- emqx-ee-a：This prefix represents the 3 EMQX nodes before the upgrade.
- emqx-ee-b：This prefix represents the 3 EMQX nodes after the upgrade.

![Upgrade EMQX](https://assets.emqx.com/images/ed5e200130abc1d64947abdd4c77034a.png)

As seen in the chart, during the rolling upgrade process, the first step is to terminate emqx-ee-a-emqx-ee-2 and then create a new emqx-ee-b-emqx-ee-2. During this time, only emqx-ee-a-emqx-ee-1 and emqx-ee-a-emqx-ee-0 can provide service. As clients reconnect, the load balancing shifts traffic to these two pods, leading to a significant increase in traffic and potential for further disconnections when these two pods are upgraded later. As it takes some time to create new pods, by the time emqx-ee-a-emqx-ee-0 finishes its upgrade, most connections have already reconnected to the other two pods, leading to uneven traffic distribution among them, which can impact the evaluation of the user's business model or affect the service.

It's important to note that the scenario where excessive reconnections cause server overload has not been tested but this may occur in a production environment where TPS exceeds the planned capacity of the cloud. The monitoring chart of connections shows a significant gap, indicating a significant impact on the business, thus a solution is needed to mitigate these issues and ensure a smooth and stable upgrade.

## Problem Resolution

### Objectives

1. Control the number of connections being migrated during the upgrade by adjusting the migration rate based on the server's processing capability.
2. Minimize the number of disconnections during the upgrade by reducing them to one as much as possible.
3. Maintain a sufficient number of nodes to provide service throughout the upgrade.
4. Once the upgrade is completed, no additional cluster load rebalancing is required and connections between nodes are relatively balanced, depending on the load balancing policy.

### Solution Design

Blue-green deployment is a technique that involves maintaining two parallel copies (blue and green) of the entire system. The latest version of EMQX Kubernetes Operator, v[2.1.0](https://github.com/emqx/emqx-operator/releases/tag/2.1.0), has integrated blue-green deployment for EMQX Enterprise. This allows for the creation of a new version of the cluster based on the existing EMQX Enterprise cluster, without disrupting the old version. Traffic is then gradually and smoothly shifted to the new version once it is up and running.

EMQX Enterprise introduces the **Node Evacuation** feature since v4.4.12. It enables users to migrate connections and sessions to other nodes at a specified rate before shutting down a node, thus avoiding session data loss during the node shutdown.

> For more information about Node Evacuation please refer to: [https://docs.emqx.com/en/enterprise/v4.4/advanced/rebalancing.html](https://docs.emqx.com/en/enterprise/v4.4/advanced/rebalancing.html)  

On Kubernetes, we have implemented a controlled migration of connections using a simulated blue-green deployment in combination with the Node Evacuation feature, significantly reducing the number of disconnections to a single disconnection. The upgrade process is outlined as follows:

![upgrade process](https://assets.emqx.com/images/6e0daf67cd54273cbbc2829c5a7f4974.png)

The upgrade process has the following steps:

1. A new node with the same configuration is created within the existing cluster before upgrading a node (by modifying an image or Pod).
2. Once the new node is ready, all traffic is redirected to it and it begins accepting new connection requests.
3. The old node is then removed from service, and it no longer processes new connection requests.
4. Connections of the node are migrated one by one using the Node Evacuation feature. Once all connections have been migrated, the node can be safely destroyed.

### Operation Procedure

The Node Evacuation feature is supported starting with EMQX Enterprise 4.4.12. The EMQX Kubernetes Operator 2.1 has been adapted to accommodate this feature. To utilize this capability, it is necessary to upgrade both EMQX Enterprise to version 4.4.12 and EMQX Kubernetes Operator to version 2.1.

**Configure blue-green upgrade**

```
apiVersion: apps.emqx.io/v1beta4
...
spec:
   blueGreenUpdate:
    initialDelaySeconds: 60
    evacuationStrategy:
      waitTakeover: 5
      connEvictRate: 200
      sessEvictRate: 200
...
```

`initialDelaySeconds`: The delay (in seconds) before initiating node evacuation after all nodes (blue and green) are ready. This delay allows the LoadBalancer to handle the correspondence between pods and the service.

`waitTakeover`: The time period (in seconds) given for clients to reconnect and take over sessions after all connections have been disconnected.

`connEvictRate`: The rate at which client connections are disconnected per second during the migration.

`sessEvictRate`: The rate at which sessions are evacuated per second following the `waitTakeover` period.

For detailed documentation of the Operator, please refer to: [https://github.com/emqx/emqx-operator/blob/main/docs/en_US/getting-started/getting-started.md](https://github.com/emqx/emqx-operator/blob/main/docs/en_US/getting-started/getting-started.md) 

The monitoring chart of connections during the upgrade is as follows (100,000 connections for this test):

![monitoring chart](https://assets.emqx.com/images/0794d60d0e212cb0e02976f87d49dfda.png)

- sum: The total number of connections, represented by the top line in the chart.
- emqx-ee-86d7758868：This prefix represents the 3 EMQX nodes before the upgrade.
- emqx-ee-745858464d：This prefix represents the 3 EMQX nodes after the upgrade.

As shown in the chart, we have successfully implemented a smooth upgrade on Kubernetes using the blue-green deployment feature of EMQX Kubernetes Operator. This upgrade solution results in minimal fluctuations in the total number of connections, depending on factors such as migration rate, server handling capacity, and client reconnection policies. This greatly ensures a seamless upgrade process, effectively prevents server overload, minimizes the impact on the business, and ultimately improves service stability.

> Note: The load distribution among the three nodes in the cluster is relatively even after the upgrade, resulting in the three lines in the chart overlapping.

## Conclusion

The solution presented in this article, which combines Node Evacuation with simulated blue-green deployment, effectively addresses common issues such as multiple disconnections, potential service overload, and load imbalance during upgrades. This allows for smooth and graceful upgrades on Kubernetes.

EMQX Kubernetes Operator, as an automated management tool, is designed to help users create and manage EMQX clusters, and fully leverage the capabilities of EMQX. By utilizing the solutions outlined in this article to upgrade EMQX, users can access the latest features of EMQX and develop advanced IoT applications.



<section class="promotion">
    <div>
        Try EMQX Cloud for Free
        <div class="is-size-14 is-text-normal has-text-weight-normal">A fully managed MQTT service for IoT</div>
    </div>
    <a href="https://accounts.emqx.com/signup?continue=https://cloud-intl.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">Get Started →</a>
</section>
