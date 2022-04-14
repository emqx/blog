In March, the EMQX team brought to the community the long-expected EMQX v5.0.0-rc.1, with various major improvements we have been working on since early this year, the rc.1 release cut is the first maturity milestone. Meanwhile, the iterative upgrade of maintenance versions of 4.x is also in progress.

[EMQX Cloud](https://www.emqx.com/en/cloud) team released a brand new and revised rule engine module this month. 

EMQX Cloud team also released a new version of the cluster deployment management tool [EMQX Kubernetes Operator](https://www.emqx.com/en/emqx-kubernetes-operator).

## EMQX

### v5.0 new progress: official release of 5.0.0-rc.1

The EMQX team successively released v5.0.0-beta 4 and then [v5.0.0-rc.1](https://github.com/emqx/emqx/releases/tag/v5.0.0-rc.1). 

At present, the features of v5.0 are basically complete. You are welcome to download and try it. 

In the meantime, there are still feedbacks, and bug reports coming in, so the team will continue to polish it, focusing on the stability and dashboard user-interaction optimisations.

Comparing to version beta.3, the rc.1 release mainly included below changes:

- Continued polishing the dashboard UI design for online config updates.
- Continued polishing the plug-in uploading, installing and management from dashboard UI.
- More MQTT message sending and receiving rate statistics for metrics systems.
- Simplified rate limiting design.
- Add search support for AuthN and AuthZ based on built-in database
- Add sleep mode support for MQTT-SN devices

### Upgrade of maintenance version

We have released the latest maintenance versions of 4.3 and 4.4 for community and enterprise users. In addition to further improving the stability, we have also brought some enhanced improvements in these versions, which mainly include:

- Add the check of UTF-8 string for MQTT message in strict mode
- Improve the writing precision of floating point data of rule engine
- OOM protection for Kafka producers (enterprise edition)
- MongoDB integration improvements

### Coming soon

In the next few months, EMQX will promote some feature improvements. Here are the spoilers:

- The encode and decode of rule engine supports gRPC to obtain better performance
- The rule engine will support more features, including time format conversion features and compression/decompression, etc.
- The rule engine will support more events, such as connection failure, etc.
- The rule engine will support resetting the statistical indicators of the specified rule
- Support the feature of using message queue size to conduct range search at the client side
- Support the adjustment of hook calling sequence at run time

Our team will continue to make great efforts to bring you a better use experience of EMQX.

## EMQX Cloud

### The rule engine is revised to Data Integration

The rule engine of EMQX Cloud has been officially renamed to [data integration], and the UI has been revised and upgraded for better user experience. Compared with the previous version of the rule engine module, the new version of [data integration] helps users quickly get familiar with the creation of resources and rules step by step through navigation. The users only need to operate according to the process of creating resources - creating rules - adding actions - test run to complete the configuration.

## EMQX Kubernetes Operator

Emqx kubernetes operator is a tool that is facilitates users to create and manage EMQX clusters in Kubernetes environment. It can greatly simplify the process of deploying and managing EMQX clusters with lower cost.

### Feature update

EMQX Kubernetes Operator successively released versions 1.1.4 and 1.1.5. Support for DNS Server automatic discovering cluster has been added in the new version. At present, when adopting EMQX Version 4.4 for deployment, automatic discovering cluster of DNS Server will be used by default. Compared with previous automatic discovering through k8s APIServer, DNS server is not required the configuration of additional serviceAccount, which improves security.

EMQX Kubernetes Operator supports Telegraf container to be deployed in the form of SideCar in EMQX Pod, which can collect and send EMQX data through plug-ins of Telegraf and emqx_prometheus.

### Major change

In v1.1.4, we set v1beta1 APIVersion to unserved version, which means that no new resources can be  created for v1beta1 APIVersion. No worries as the existing v1beta1 APIVersion resources will be imperceptibly converted to v1beta2 APIVersion, and will not lead to business interruption. We plan to completely delete the support for v1beta1 APIVersion in v1.2.

### Stay tuned

EMQX Kubernetes Operator v1.2 and v1beta3 APIVersion are under development, and v1beta3 APIVersion will bring more reasonable structure of spec.
