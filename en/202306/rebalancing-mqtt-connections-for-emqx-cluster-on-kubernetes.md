## Introduction

[MQTT connections rebalancing](https://docs.emqx.com/en/enterprise/v4.4/advanced/rebalancing.html#motivation) is a feature of EMQX that migrates client connections and sessions from overloaded nodes to less loaded ones to achieve load balancing. It automatically calculates the necessary number of connections to be migrated and migrates them accordingly. This process is typically performed after a new node joins or restarts to ensure balance. EMQX will migrate MQTT client connections along with [MQTT sessions](https://www.emqx.com/en/blog/mqtt-session) to avoid session loss.

MQTT connections rebalancing mainly has the following two benefits:

- **Improve system scalability**: In MQTT connections, when expanding a cluster, the TCP/IP-based connections from old nodes don't automatically migrate to new nodes. Rebalancing can help to distribute the load from the old nodes to the new ones and achieve a more balanced cluster. This improves the overall cluster performance in terms of throughput, response speed, and resource utilization, making the system scale better. 
- **Reduce operation and maintenance costs**: Through rebalancing, the load of nodes can be automatically adjusted without additional operation and maintenance.

> The cluster load rebalancing is only available after EMQX Enterprise  4.4.12.
>
> Learn more about the world’s most scalable MQTT broker: [EMQX Enterprise: Enterprise MQTT Platform At Scale](https://www.emqx.com/en/products/emqx) 

In this blog, we will introduce how to enable the [MQTT connections](https://www.emqx.com/en/blog/how-to-set-parameters-when-establishing-an-mqtt-connection) rebalancing feature of EMQX on Kubernetes.

## The Workflow of MQTT Connections Rebalancing

[EMQX Operator](https://www.emqx.com/en/emqx-kubernetes-operator) provides `Rebalance`, a custom resource type, to facilitate users to perform MQTT connections rebalancing. To rebalance the MQTT connections in an EMQX cluster, simply deploy a new `Rebalance` resource. EMQX Operator monitors the submitted resource and triggers the rebalance task in EMQX accordingly.

EMQX will divide the nodes in the cluster into source nodes and target nodes before performing the rebalancing task. 

- The source node is the node with an excessive number of connections and will no longer receive new connections;
- The target node is a node with insufficient connections. 

EMQX Operator removes the source node information from Endpoints to ensure that the new connections are allocated only to the target node. Clients connected to the source node are gradually disconnected by EMQX until the average number of connections between the source and target nodes reaches equilibrium. Sessions from the source node are then migrated to the target node. Once the rebalance task is completed, EMQX switches the source node back to its normal state. The EMQX Operator re-adds the source node information to Endpoints, concluding the Rebalance task.

## MQTT Connections Rebalancing vs. Traditional Load Balancer

Traditional load balancers can route MQTT connections to available nodes. However, as the long connections based on the TCP/IP protocol, MQTT connections on old nodes can not automatically migrate to new ones when the cluster expands. There comes load balancing strategy of the least number of connections (Least Connection) to ensure that the number of connections on each node is relatively balanced. 

However, most of the load balancers of cloud vendors do not support the `Least Connection` strategy. Therefore, the traditional load balancer is not the best solution to solve the unbalanced MQTT connection of EMQX cluster. Meanwhile, MQTT connections rebalancing relies on load balancers to route reconnected connections to target nodes. Therefore, it’s possible to combine these two methods for a better experience. Correctly configuring them can make the EMQX cluster MQTT load more balanced, thereby improving the availability and reliability of the system.

## An Example: Rebalancing MQTT Connections on Kubernetes

Next, we will introduce how to rebalance MQTT connections on Kubernetes, and provide a configuration example of `Rebalance` and show the effect of rebalancing MQTT connections.

### Prerequisites

Before deploying EMQX on Kubernetes, make sure the following requirements are satisfied:

- [Kubernetes](https://kubernetes.io/docs/concepts/overview/): version >= 1.24
- [Helm](https://helm.sh/): version >= 3

### Install EMQX Operator

1. Install and start cert-manager

   `cert-manager` version `1.1.6` or higher is required. Skip this step if the `cert-manager` is already installed and started.

   ```
   $ helm repo add jetstack https://charts.jetstack.io
   $ helm repo update
   $ helm upgrade --install cert-manager jetstack/cert-manager \
     --namespace cert-manager \
     --create-namespace \
     --set installCRDs=true
   ```

   Or you can follow the [cert-manager installation guide](https://cert-manager.io/docs/installation/) to install it.

2. Install EMQX Operator by Helm.

   ```
   $ helm repo add emqx https://repos.emqx.io/charts
   $ helm repo update
   $ helm install emqx-operator emqx/  emqx-operator --namespace emqx-operator-system --create-namespace
   ```

3. Wait till EMQX Operator is ready.

   ```
   $ kubectl wait --for=condition=Ready pods -l "control-plane=controller-manager" -n emqx-operator-system
   
   # If you get output results similar to the following, it indicates that emqx-operator is ready:
   pod/emqx-operator-controller-manager-57bd7b8bd4-h2mcr condition met
   ```

### Rebalance MQTT Connections

1. Cluster load (before rebalancing)

   Before Rebalancing, we built a cluster with unbalanced load. And use Grafana and Prometheus to monitor the load of EMQX cluster.

   ![Rebalance MQTT Connections](https://assets.emqx.com/images/c86d6232261c42b3a8c9aa9bb5403315.png)

   It can be seen from the figure that there are four EMQX nodes in the current cluster, three of which carry 10,000 connections, and the remaining one has 0 connections. Next, we will demonstrate how to perform a rebalancing operation to make the four nodes' load balanced. 

2. Save the following as a YAML file and deploy it with the kubectl apply command.

   ```
   apiVersion: apps.emqx.io/v1beta4
   kind: Rebalance
   metadata:
      name: test-0
   spec:
      instanceName: emqx-ee
      rebalanceStrategy:
        connEvictRate: 10
        sessEvictRate: 10
        waitTakeover: 10
        waitHealthCheck: 10
        absConnThreshold: 100
        absSessThreshold: 100
        relConnThreshold: "1.1"
        relSessThreshold: "1.1"
   ```

   >For Rebalance configuration, please refer to the document: [Rebalance Configuration](https://file+.vscode-resource.vscode-cdn.net/Users/raoxiaoli/reference/v1beta4-reference.md#rebalancestrategy).

3. Execute the following command to view the rebalancing status of the EMQX cluster.

   ```
   $ kubectl get rebalances rebalance-sample -o json | jq '.status.rebalanceStates'
   {
    "state": "wait_health_check",
    "session_eviction_rate": 10,
    "recipients":[
        "emqx-ee@emqx-ee-3.emqx-ee-headless.default.svc.cluster.local",
    ],
    "node": "emqx-ee@emqx-ee-0.emqx-ee-headless.default.svc.cluster.local",
    "donors":[
        "emqx-ee@emqx-ee-0.emqx-ee-headless.default.svc.cluster.local",
        "emqx-ee@emqx-ee-1.emqx-ee-headless.default.svc.cluster.local",
        "emqx-ee@emqx-ee-2.emqx-ee-headless.default.svc.cluster.local"
    ],
    "coordinator_node": "emqx-ee@emqx-ee-0.emqx-ee-headless.default.svc.cluster.local",
    "connection_eviction_rate": 10
   }   
   ```

4. Wait for the Rebalance task to complete

   ```
   $ kubectl get rebalances rebalance-sample
   NAME               STATUS      AGE
   rebalance-sample   Completed   62s
   ```

   There are three states of Rebalance: Processing, Completed and Failed. 

   - Processing indicates that the rebalancing task is in progress.
   - Completed indicates that the rebalancing task has been completed.
   - Failed indicates that the rebalancing task failed.

5. Cluster load (after rebalancing)

   ![Cluster load (after rebalancing)](https://assets.emqx.com/images/70180f7da40d983fd10bb1c8bb606b9e.png)

   The figure above shows the cluster load after Rebalance is completed. It can be seen from the graph that the entire Rebalance process is very smooth. The data shows that the total number of connections in the cluster is still 10,000, which is consistent with that before Rebalance. The number of connections of four nodes has changed, and some connections of three nodes have been migrated to newly expanded nodes. After rebalancing, loads of the four nodes remain stable, and the number of connections is close to 2,500 and will not change.

   According to the conditions for the cluster to reach balance:

   ```
   avg(source node connection number) < avg(target node connection number) + abs_conn_threshold
   or
   avg(source node connection number) < avg(target node connection number) * rel_conn_threshold
   ```

   Substituting the configured Rebalance parameters and the number of connections can calculate `avg(2553 + 2553+ 2554) < 2340 * 1.1`, so the current cluster load has reached a balanced state, and the Rebalance task has successfully rebalanced the cluster load.

## Conclusion

Rebalancing MQTT connections is an effective way to manage MQTT connections in a distributed system, which can ensure the load balance of MQTT connections and maintain the continuity of MQTT sessions. If you are using an EMQX cluster, be sure to rebalance MQTT connections after cluster expansion or node restart to achieve a more balanced cluster.



<section class="promotion">
    <div>
        Try EMQX Enterprise for Free
      <div class="is-size-14 is-text-normal has-text-weight-normal">Connect any device, at any scale, anywhere.</div>
    </div>
    <a href="https://www.emqx.com/en/try?product=enterprise" class="button is-gradient px-5">Get Started →</a>
</section>
