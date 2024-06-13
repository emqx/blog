## What Is MQTT?

Message Queuing Telemetry Transport ([MQTT](https://www.emqx.com/en/blog/the-easiest-guide-to-getting-started-with-mqtt)) is an open-source messaging protocol used for machine-to-machine (M2M) communication. It is designed for systems where bandwidth is limited and device power consumption needs to be minimized. MQTT is often used in IoT applications, where numerous devices continuously send and receive data.

MQTT works on the principle of a publish/subscribe model. In this model, devices, known as "clients", send messages to a server, known as a "broker". Other clients can subscribe to these messages by indicating the topics they are interested in. The broker then ensures that all messages on those topics are delivered to the subscribers. This model allows for efficient communication between devices, even when network conditions are less than ideal.

The key benefits of MQTT include its lightweight nature, its ability to handle intermittent connections, and its support for one-to-many communication. All these features make it an ideal choice for IoT applications, where devices often have limited processing power and operate on unreliable networks.

For large-scale MQTT deployments, it can be useful to run multiple MQTT brokers in a cluster. This requires managing multiple application instances and scaling them as needed. This is where Kubernetes comes in.

**Learn more in our detailed guide to [MQTT IoT](https://www.emqx.com/en/blog/what-is-the-mqtt-protocol)**

## What is Kubernetes?

Kubernetes, often referred to as K8s, is an open-source platform designed to automate deploying, scaling, and managing containerized applications. It groups containers that make up an application into logical units for easy management and discovery. Kubernetes was originally developed by Google, based on their experience running huge production workloads, and is now maintained by the Cloud Native Computing Foundation.

Kubernetes provides a framework to run distributed systems resiliently. It takes care of scaling and failover for your applications, provides deployment patterns, and more. For example, Kubernetes can easily manage a canary deployment for your system.

Kubernetes uses a cluster architecture to manage containers. A cluster consists of at least one master node and multiple worker nodes. The master node is responsible for maintaining the desired state of the cluster, such as which applications are running and which container images they use. Worker nodes actually run the applications and workloads.

## Benefits of Running MQTT on Kubernetes

### Intelligent Scaling

Kubernetes has powerful built-in features for scaling applications based on resource usage or custom metrics. This means your [MQTT broker](https://www.emqx.com/en/blog/the-ultimate-guide-to-mqtt-broker-comparison) can automatically scale up to handle increased load and scale down when the load decreases, preventing wastage of resources.

The scalability of MQTT on Kubernetes is not just about handling larger loads. It's also about enabling more efficient use of resources. With Kubernetes, you can ensure that your MQTT broker is using just the right amount of computing resources.

Kubernetes also provides horizontal and vertical scaling options for more flexibility. Horizontal scaling involves adding or removing instances of your application, while vertical scaling involves adding or removing resources from an existing instance.

### Fault Tolerance

In a Kubernetes cluster, if a node or a pod fails, Kubernetes can automatically replace it with a new one, ensuring that your MQTT broker remains available and operational. This is crucial for many IoT applications, where uninterrupted communication between devices is critical.

Kubernetes also provides features like health checks and readiness probes, which continuously monitor the status of your MQTT broker and react if something goes wrong. These features enable Kubernetes to detect and handle failures promptly, minimizing the impact on your application.

### Self-Healing and Efficient Administration

Kubernetes has a self-healing mechanism that can automatically restart, replicate, and re-schedule pods when it detects a system failure or when a node becomes unresponsive. This ensures that your MQTT deployment remains stable and healthy, reducing the need for manual intervention and maintenance.

In addition to self-healing, Kubernetes also makes administration more efficient by providing a declarative configuration model. Instead of manually performing each administrative task, you can define your desired state in a configuration file, and Kubernetes will automatically make the necessary changes to achieve that state. This can save a lot of time and effort, and reduce the risk of errors.

## Deploying MQTT Brokers with a Kubernetes Operator: Step by Step

EMQX is the leading open source MQTT broker. It provides a Docker Official Image which is [available on Docker Hub](https://hub.docker.com/_/emqx) and an open source [Kubernetes operator](https://github.com/emqx/emqx-operator), which supports the free and open source version of EMQX. Operators make it easy to deploy complex applications on Kubernetes.

With the Kubernetes operator, you can easily deploy the free EMQX broker on Kubernetes and get access to these features:

- Ability to scale up to 100M+ IoT devices in 1 cluster, while maintaining 1M message per second throughput and sub-millisecond latency.
- 100% compliant with [MQTT 5.0](https://www.emqx.com/en/blog/introduction-to-mqtt-5) and 3.x, support for multiple open standard protocols like HTTP, QUIC, and WebSocket.
- Secures bi-directional communication with MQTT over TLS/SSL and various authentication mechanisms.
- Uses powerful SQL-based rules engine to extract, filter, enrich and transform IoT data in real-time.
- Ensures high availability and horizontal scalability with a masterless distributed architecture.
- More than 20K+ enterprise users across 50+ countries and regions, connecting 100M+ IoT devices worldwide. Trusted by over 400 customers in mission-critical scenarios including over 70 Fortune 500 companies.

Here is how to use the EMQX Kubernetes operator to quickly get up and running with MQTT in Kubernetes.

### Setup Requirements

Prior to deploying the EMQX Operator, make sure the following components are set and ready:

- An active [Kubernetes cluster](https://kubernetes.io/docs/concepts/overview/). To select a Kubernetes version, refer to [Choosing a Kubernetes Version](https://github.com/emqx/emqx-operator/blob/main/docs/en_US/index.md#how-to-selector-kubernetes-version).
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl), a command-line tool that allows you to run commands against Kubernetes clusters. You can verify the status of your Kubernetes cluster through the kubectl cluster-info command.
- [Helm](https://helm.sh/) version 3 or above.

### Install EMQX Operator

Follow the steps below to install EMQX Operator:

1. Install and run cert-manager. Note, version 1.1.6 or higher is required.
   You can use Helm for cert-manager installation.

   ```
   $ helm repo add jetstack https://charts.jetstack.io
   $ helm repo update
   $ helm upgrade --install cert-manager jetstack/cert-manager \
     --namespace cert-manager \
     --create-namespace \
     --set installCRDs=true
   ```

1. Use the following command to install the EMQX Operator:

   ```
   $ helm repo add emqx https://repos.emqx.io/charts
   $ helm repo update
   $ helm upgrade --install emqx-operator emqx/emqx-operator \
     --namespace emqx-operator-system \
     --create-namespace
   ```

1. Wait for the EMQX Operator to become ready:

   ```
   $ kubectl wait --for=condition=Ready pods -l "control-plane=controller-manager" -n emqx-operator-system
   ```

1. When you see the following message, the EMQX Operator is ready:

   ```
   pod/emqx-operator-controller-manager-57bd7b8bd4-h2mcr condition met
   ```

### Deploy EMQX Open Source 5.0 on Kubernetes

To deploy EMQX Open Source via the EMQX Operator. To learn more about the EQMX CRD, see the [reference documentation](https://github.com/emqx/emqx-operator/blob/main/docs/en_US/reference/v2beta1-reference.md).

1. Create a YAML file with the following content and deploy it using kubectl apply:

   ```
   apiVersion: apps.emqx.io/v2beta1
   kind: EMQX
   metadata:
      name: emqx
   Spec:
      image: emqx:5.1
   ```

1. Wait a few minutes for the EMQX cluster to initiate, and then run this message:

   ```
   $ kubectl get emqx
   NAME   IMAGE      STATUS    AGE
   ```

1. The following message indicates that the EMQX cluster is active:

   ```
   emqx   emqx:5.1   Running   2m55s
   ```

1. Ensure the `STATUS` is `Running`.

## EMQX: A Kubernetes-Ready MQTT Broker

[EMQX](https://github.com/emqx/emqx) is one of the most popular MQTT brokers. It stands out as a remarkably well-suited MQTT broker for deployment within Kubernetes environments. This type of deployment offers seamless integration of EMQX’s robust messaging capabilities with Kubernetes' ability to handle rapidly changing workloads and efficiently manage containers.

![MQTT Broker Cluster](https://assets.emqx.com/images/b39739558e71f83c6ecf70c0df22d918.png)

With its inherent complexity and emphasis on flexibility, Kubernetes demands an MQTT broker capable of adapting to the ever-changing microservices landscape. EMQX rises to this challenge with its native support for Kubernetes, allowing for effortless deployment, scaling, and management of MQTT messaging services. Its lightweight architecture and efficient resource utilization ensure optimal performance even in highly dynamic Kubernetes clusters.

Its key features include:

- [Massive Scale](https://www.emqx.com/en/blog/how-emqx-5-0-achieves-100-million-mqtt-connections): Scale horizontally to 20+ nodes in a single cluster for 100M MQTT connections.
- [Business-Critical Reliability](https://www.emqx.com/en/blog/mqtt-persistence-based-on-rocksdb): Ensure no data loss with built-in RocksDB data persistence.
- [Data Security](https://www.emqx.com/en/solutions/mqtt-security): End-to-end data encryption and fine-grained access control to protect your data.
- [Multiple protocols support](https://www.emqx.com/en/blog/iot-protocols-mqtt-coap-lwm2m): MQTT, [QUIC](https://www.emqx.com/en/blog/quic-protocol-the-features-use-cases-and-impact-for-iot-iov), [CoAP](https://www.emqx.com/en/blog/coap-protocol), Stomp, LwM2M, and more
- [High Performance](https://www.emqx.com/en/blog/mqtt-performance-benchmark-testing-emqx-single-node-supports-2m-message-throughput): Ingest and process millions of MQTT messages efficiently per second per node.
- [Low Latency](https://www.emqx.com/en/blog/mqtt-performance-benchmark-testing-emqx-single-node-message-latency-response-time): Guarantee sub-millisecond latency in message delivery with the soft real-time runtime.
- [Complete Observability](https://www.emqx.com/en/blog/open-telemetry-the-basics-and-benefits-for-mqtt-and-iot-observability): Monitoring, alerting, and advanced end-to-end analysis with real-time MQTT tracing.



<section class="promotion">
    <div>
        Talk to an Expert
    </div>
    <a href="https://www.emqx.com/en/contact?product=solutions" class="button is-gradient px-5">Contact Us →</a>
</section>
