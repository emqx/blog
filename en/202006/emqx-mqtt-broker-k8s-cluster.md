
EMQ X Team provides Helm chart which facilitates users to one-click deploy EMQ X [MQTT broker](https://www.emqx.io/products/broker) in the Kubernetes cluster. EMQ X Team mostly recommends This method for deploying EMQ X MQTT broker in the Kubernetes or k3s cluster. This article will start from scratch using the handwriting YAML file method to deploy a K8S cluster of EMQ X MQTT broker, and analyze details and techniques of the deployment. It will facilitate users to flexibly use during real deployment.

Reading this article needs users to know the basic concept of Kubernetes and having an operational Kubernetes cluster.

## Deploy single EMQ X MQTT broker node in K8S 

### Use pod directly deploy EMQ X Broker

In Kubernetes, the smallest management element is [Pod](https://kubernetes.io/zh/docs/concepts/workloads/pods/pod-overview/) than individual containers. Pod is the basic executing unit of Kubernetes applications, which means that it is the smallest and simplest unit be created or deployed in the Kubernetes object model. Pod represents the processes running on the [cluster](https://kubernetes.io/zh/docs/reference/glossary/?all=true#term-cluster).

EMQ X Broker has provided mirroring in [docker hub](https://hub.docker.com/r/emqx/emqx), so users can easily deploy EMQ X Broker in the single pod. Using the command `kubectl run` to create a pod running EMQ X Broker. 

```
$ kubectl run emqx --image=emqx/emqx:v4.1-rc.1  --generator=run-pod/v1
pod/emqx created
```

View the status of EMQ X Broker:

```
$ kubectl get pods -o wide
NAME   READY   STATUS    RESTARTS   AGE
emqx   1/1     Running   0          3m13s

$ kubectl exec emqx -- emqx_ctl status
Node 'emqx@192.168.77.108' is started
emqx 4.1-rc.1 is running
```

Delete pod:

```
$ kubectl delete pods emqx
pod "emqx" deleted
```

Pod is not designed as a persistence resource, it will not survive in the scheduling failing, node crashing or other recovering(such as because of lack of resource or other maintenances). Therefore, a controller is needed to manage Pod.

### Use `Deployment` deploy Pod

[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) provides a declarative definition(declarative) method for pod and ReplicaSet to replace the previous ReplicationController for easily managing applications. The typical applying scenarios including:

- Define Deployment to create Pod and ReplicaSet
- Scroll upgrade and rollback applications
- Expand and shrink
- Pause and continue Deployment

Use Deployment deploy an EMQ X Broker Pod：

+ Define `Deployment`：

  ```
  $ cat deployment.yaml
  
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: emqx-deployment
    labels:
      app: emqx
  spec:
    replicas: 1
    selector:
      matchLabels:
        app: emqx
    template:
      metadata:
        labels:
          app: emqx
      spec:
        containers:
        - name: emqx
          image: emqx/emqx:v4.1-rc.1
          ports:
          - name: mqtt
          	containerPort: 1883
          - name: mqttssl
          	containerPort: 8883
          - name: mgmt
          	containerPort: 8081
          - name: ws
          	containerPort: 8083
          - name: wss
          	containerPort: 8084
          - name: dashboard
          	containerPort: 18083
  ```

+ Deploy `Deployment`：

  ```
  $  kubectl apply -f deployment.yaml
  deployment.apps/emqx-deployment created
  ```

+ View `Deployment` situation:

  ```
  $ kubectl get deployment
  NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
  deployment.apps/emqx-deployment   3/3     3            3           74s
  
  $ kubectl get pods
  NAME                                  READY   STATUS    RESTARTS   AGE
  pod/emqx-deployment-7c44dbd68-8j77l   1/1     Running   0          74s
  
  $ kubectl exec pod/emqx-deployment-7c44dbd68-8j77l -- emqx_ctl status
  Node 'emqx-deployment-7c44dbd68-8j77l@192.168.77.117' is started
  emqx 4.1-rc.1 is running
  ```

+ Trying manually delete Pod

  ```
  $ kubectl delete pods emqx-deployment-7c44dbd68-8j77l
  pod "emqx-deployment-7c44dbd68-8j77l" deleted
  
  $ kubectl get pods
  NAME                              READY   STATUS    RESTARTS   AGE
  emqx-deployment-68fcb4bfd6-2nhh6   1/1     Running   0          59s
  ```

  The output result represents that successfully using Deployment deploy EMQ X Broker Pod. Even if this pod is accidentally stopped, Deployment will recreate a new pod.

### Use services exposing EMQ X Broker Pod service

Kubernetes [Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) has a life cycle. They can be created, and will not run if they are destroyed. It can dynamically create and destroy pod, if use [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) to run applications.

Every pod has its IP address, but in Deployment, the pod collection running at the same moment may differ from that runs this application later.

This will cause a problem: if use EMQ X Broker Pod to provide service to the **MQTT client**, how does the client find and track the IP address that will be connected, to facilitate users to use EMQ X Broker service.

The answer is: Service

Service is an abstract method for exposing the application which is running on a set of [Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) as network service.

Use Service to expose EMQ X Broker Pod as network service.

+ Define Service：

  ```
  $cat service.yaml
  
  apiVersion: v1
  kind: Service
  metadata:
    name: emqx-service
  spec:
    selector:
      app: emqx
    ports:
      - name: mqtt
        port: 1883
        protocol: TCP
        targetPort: mqtt
      - name: mqttssl
        port: 8883
        protocol: TCP
        targetPort: mqttssl
      - name: mgmt
        port: 8081
        protocol: TCP
        targetPort: mgmt
      - name: ws
        port: 8083
        protocol: TCP
        targetPort: ws
      - name: wss
        port: 8084
        protocol: TCP
        targetPort: wss
      - name: dashboard
        port: 18083
        protocol: TCP
        targetPort: dashboard
  
  ```

+ Deploy Service：

  ```
  $ kubectl apply -f service.yaml
  service/emqx-service created
  ```

+ View deployment situation

  ```
  $ kubectl get svc
  NAME           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                                        AGE
  emqx-service   ClusterIP   10.96.54.205   <none>        1883/TCP,8883/TCP,8081/TCP,8083/TCP,8084/TCP,18083/TCP   58s
  ```

+ Use the IP provided by Service to view API of EMQ X Broker

  ```
  $ curl 10.96.54.205:8081/status
  Node emqx-deployment-68fcb4bfd6-2nhh6@192.168.77.120 is started
  emqx is running
  ```

So far, the deployment of a single EMQ X Broker node is done. Manage EMQ X Broker Pod through Deployment, and expose EMQ X Broker service through Service.

## Automatically cluster EMQ X MQTT broker through Kubernetes

The article above introduced how to deploy single EMQ X Broker Pod through Deployment. It is extremely convenient to expand the number of Pod through Deployment, execute the command `kubectl scale deployment ${deployment_name} --replicas ${numer}` can expand the number of Pod. Expanding EMQ X Broker Pod to three is as follows:

```
$ kubectl scale deployment emqx-deployment --replicas 3
deployment.apps/emqx-deployment scaled

$ kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
emqx-deployment-68fcb4bfd6-2nhh6   1/1     Running   0          18m
emqx-deployment-68fcb4bfd6-mpvch   1/1     Running   0          6s
emqx-deployment-68fcb4bfd6-mx55q   1/1     Running   0          6s

$ kubectl exec emqx-deployment-68fcb4bfd6-2nhh6 -- emqx_ctl status
Node 'emqx-deployment-68fcb4bfd6-2nhh6@192.168.77.120' is started
emqx 4.1-rc.1 is running

$ kubectl exec emqx-deployment-68fcb4bfd6-2nhh6 -- emqx_ctl cluster status
Cluster status: #{running_nodes =>
                      ['emqx-deployment-68fcb4bfd6-2nhh6@192.168.77.120'],
                  stopped_nodes => []}
```

You can see that the number of EMQ X Broker Pod is expanded to three, but each pod is separated, and there are no clusters. Next try to automatically cluster EMQ X Broker Pod through Kubernetes.

### Modify EMQ X Broker configuration

View the content related to [automatically cluster](https://docs.emqx.io/broker/latest/en/advanced/cluster.html#emqx-service-discovery-k8s) in the EMQ X Broker documentation, you can see that we need to modify the configuration of EMQ X Broker.

```
cluster.discovery = kubernetes
cluster.kubernetes.apiserver = http://10.110.111.204:8080
cluster.kubernetes.service_name = ekka
cluster.kubernetes.address_type = ip
cluster.kubernetes.app_name = ekka
```

`cluster.kubernetes.apiserver` is the address of Kubernetes apiserver, we can get it through this command `kubectl cluster-info`. `cluster.kubernetes.service_name` is the Service name we mentioned above. `cluster.kubernetes.app_name` is the part before the  `@` symbol in `node.name` of EMQ X Broker,  so you also need to set the EMQ X Broker in the cluster as a uniform prefix of `node.name`.

The docker mirroring of EMQ X Broker provides the function of modifying configurations through environment variables. For more details, you can check [docker hub](https://hub.docker.com/r/emqx/emqx) or [Github](https://github.com/emqx/emqx-rel/blob/master/deploy/docker/README.md).

+ Modify the yaml file of Deployment and add environment variables:

  ```
  $ cat deployment.yaml
  
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: emqx-deployment
    labels:
      app: emqx
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: emqx
    template:
      metadata:
        labels:
          app: emqx
      spec:
        containers:
        - name: emqx
          image: emqx/emqx:v4.1-rc.1
          ports:
          - name: mqtt
            containerPort: 1883
          - name: mqttssl
            containerPort: 8883
          - name: mgmt
            containerPort: 8081
          - name: ws
            containerPort: 8083
          - name: wss
            containerPort: 8084
          - name: dashboard
            containerPort: 18083
          env:
          - name: EMQX_NAME
          	value: emqx
          - name: EMQX_CLUSTER__DISCOVERY
            value: k8s
          - name: EMQX_CLUSTER__K8S__APP_NAME
            value: emqx
          - name: EMQX_CLUSTER__K8S__SERVICE_NAME
            value: emqx-service
          - name: EMQX_CLUSTER__K8S__APISERVER
            value: "https://kubernetes.default.svc:443"
          - name: EMQX_CLUSTER__K8S__NAMESPACE
            value: default
  ```

  > Because this command ``kubectl scale deployment ${deployment_name} --replicas ${numer}` will not modify file yaml, needs to set `spec.replicas: 3` when modify yaml.

  > `https://kubernetes.default.svc:443` will be parsed as the address of Kubernetes apiserver because of the build-in DNS rules of Kubernetes.

+ Delete the previous Deployment and then redeploy:

  ```
  $ kubectl delete deployment emqx-deployment
  deployment.apps "emqx-deployment" deleted
  
  $ kubectl apply -f deployment.yaml
  deployment.apps/emqx-deployment created
  ```


### Give authority to pod for accessing Kubernetes apiserver

After successfully deploy Deployment, check the status of EMQ X Broker, then you can see that although EMQ X Broker runs successfully, the cluster is still not successful. Check the log of EMQ X Broker Pod:

```
$ kubectl get pods
NAME                               READY   STATUS    RESTARTS   AGE
emqx-deployment-5c8cfc4d75-67lmt   1/1     Running   0          5s
emqx-deployment-5c8cfc4d75-r6jgb   1/1     Running   0          5s
emqx-deployment-5c8cfc4d75-wv2hj   1/1     Running   0          5s

$ kubectl exec emqx-deployment-5c8cfc4d75-67lmt -- emqx_ctl status
Node 'emqx@192.168.87.150' is started
emqx 4.1-rc.1 is running

$ kubectl exec emqx-deployment-5c8cfc4d75-67lmt -- emqx_ctl cluster status
Cluster status: #{running_nodes => ['emqx@192.168.87.150'],
                  stopped_nodes => []}
                  
$ kubectl logs emqx-deployment-76f6895c46-4684f

···
(emqx@192.168.87.150)1> 2020-05-20 01:48:39.726 [error] Ekka(AutoCluster): Discovery error: {403,
                                     "{\"kind\":\"Status\",\"apiVersion\":\"v1\",\"metadata\":{},\"status\":\"Failure\",\"message\":\"endpoints \\\"emqx-service\\\" is forbidden: User \\\"system:serviceaccount:default:default\\\" cannot get resource \\\"endpoints\\\" in API group \\\"\\\" in the namespace \\\"default\\\"\",\"reason\":\"Forbidden\",\"details\":{\"name\":\"emqx-service\",\"kind\":\"endpoints\"},\"code\":403}\n"}
···
```

Pod is refused because of authority, when it accesses Kubernetes apiserver and return HTTP 403, the cluster failed.

The normal pod can not access Kubernetes apiserver. There are two methods that can figure out this problem. The first one is to open the HTTP interface of Kubernetes apiserver, but some security risks are exiting. Another one is through ServiceAccount, Role and RoleBinding to configure RBAC authentication.

+ Define ServiceAccount, Role and RoleBinding:

  ```
  $ cat rbac.yaml
  
  apiVersion: v1
  kind: ServiceAccount
  metadata:
    namespace: default
    name: emqx
  ---
  kind: Role
  apiVersion: rbac.authorization.kubernetes.io/v1beta1
  metadata:
    namespace: default
    name: emqx
  rules:
  - apiGroups:
    - ""
    resources:
    - endpoints 
    verbs: 
    - get
    - watch
    - list
  ---
  kind: RoleBinding
  apiVersion: rbac.authorization.kubernetes.io/v1beta1
  metadata:
    namespace: default
    name: emqx
  subjects:
    - kind: ServiceAccount
      name: emqx
      namespace: default
  roleRef:
    kind: Role
    name: emqx
    apiGroup: rbac.authorization.kubernetes.io
  ```

+ Deploy the corresponding resources:

  ```
  $ kubectl apply -f rbac.yaml
  serviceaccount/emqx created
  role.rbac.authorization.kubernetes.io/emqx created
  rolebinding.rbac.authorization.kubernetes.io/emqx created
  ```

+ Modify file yaml of Deployment, add `spec.template.spec.serviceAccountName`, and redeploy:

  ```
  $cat deployment.yaml
  
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: emqx-deployment
    labels:
      app: emqx
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: emqx
    template:
      metadata:
        labels:
          app: emqx
      spec:
        serviceAccountName: emqx
        containers:
        - name: emqx
          image: emqx/emqx:v4.1-rc.1
          ports:
          - name: mqtt
            containerPort: 1883
          - name: mqttssl
            containerPort: 8883
          - name: mgmt
            containerPort: 8081
          - name: ws
            containerPort: 8083
          - name: wss
            containerPort: 8084
          - name: dashboard
            containerPort: 18083
          env:
          - name: EMQX_NAME
          	value: emqx
          - name: EMQX_CLUSTER__DISCOVERY
            value: kubernetes
          - name: EMQX_CLUSTER__K8S__APP_NAME
            value: emqx
          - name: EMQX_CLUSTER__K8S__SERVICE_NAME
            value: emqx-service
          - name: EMQX_CLUSTER__K8S__APISERVER
            value: "https://kubernetes.default.svc:443"
          - name: EMQX_CLUSTER__K8S__NAMESPACE
            value: default
            
  $ kubectl delete deployment emqx-deployment
  deployment.apps "emqx-deployment" deleted
  
  $ kubectl apply -f deployment.yaml
  deployment.apps/emqx-deployment created
  ```

+ View status:

  ```
  $ kubectl get pods
  NAME                              READY   STATUS    RESTARTS   AGE
  emqx-deployment-6b854486c-dhd7p   1/1     Running   0          10s
  emqx-deployment-6b854486c-psv2r   1/1     Running   0          10s
  emqx-deployment-6b854486c-tdzld   1/1     Running   0          10s
  
  $ kubectl exec emqx-deployment-6b854486c-dhd7p  -- emqx_ctl status
  Node 'emqx@192.168.77.92' is started
  emqx 4.1-rc.1 is running
  
  $ kubectl exec emqx-deployment-6b854486c-dhd7p  -- emqx_ctl cluster status
  Cluster status: #{running_nodes =>
                        ['emqx@192.168.77.115','emqx@192.168.77.92',
                         'emqx@192.168.87.157'],
                    stopped_nodes => []}
  ```

+ abort a Pod:

  ```
  $ kubectl delete pods emqx-deployment-6b854486c-dhd7p
  pod "emqx-deployment-6b854486c-dhd7p" deleted
  
  $ kubectl get pods
  NAME                              READY   STATUS    RESTARTS   AGE
  emqx-deployment-6b854486c-846v7   1/1     Running   0          56s
  emqx-deployment-6b854486c-psv2r   1/1     Running   0          3m50s
  emqx-deployment-6b854486c-tdzld   1/1     Running   0          3m50s
  
  $ kubectl exec emqx-deployment-6b854486c-846v7 -- emqx_ctl cluster status
  Cluster status: #{running_nodes =>
                        ['emqx@192.168.77.115','emqx@192.168.77.84',
                         'emqx@192.168.87.157'],
                    stopped_nodes => ['emqx@192.168.77.92']}
  ```

  The output result represents that EMQ X Broker will correctly display the stopped pod, and add the new created Pod to the cluster.

So far, EMQ X Broker has successfully created cluster in kubernetes.

## Persistence EMQ X Broker cluster

The Deployment used above to manage Pod, but the network of Pod is constantly changeable. When the pod is destroyed and rebuild, the data and configuration stored in EMQ X Broker also disappeared, this is can not be accepted during production. Next try to persistence EMQ X Broker cluster. Even if the pod is destroyed and rebuild, the data of the EMQ X Broker can be retained. 

### ConfigMap

[ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) is an API object which is used to store non-confidential data to key-value pairs. It will be used as an environment variables, command-line arguments, or as configuration files in a volume.

ConfigMap decouples your environment configuration information from [container mirroring](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/#why-containers), so that you can easily modify application configuration.

> ConfigMap does not provide secrecy or encryption. If the data you want to store are confidential, use a [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) rather than a ConfigMap, or use third-party tools to keep your data private.

Next use ConfigMap to record the configuration of EMQ X Broker, and import them as environment variables to the Deployment.

+ Define Configmap and deploy:

  ```
  $cat configmap.yaml
  
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: emqx-config
  data:
    EMQX_CLUSTER__K8S__ADDRESS_TYPE: "hostname"
    EMQX_CLUSTER__K8S__APISERVER: "https://kubernetes.default.svc:443"
    EMQX_CLUSTER__K8S__SUFFIX: "svc.cluster.local"
    
  $ kubectl apply -f configmap.yaml
  configmap/emqx-config created
  ```

+ Configure Deployment for using Configmap

  ```
  $cat deployment.yaml
  
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: emqx-deployment
    labels:
      app: emqx
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: emqx
    template:
      metadata:
        labels:
          app: emqx
      spec:
        serviceAccountName: emqx
        containers:
        - name: emqx
          image: emqx/emqx:v4.1-rc.1
          ports:
          - name: mqtt
            containerPort: 1883
          - name: mqttssl
            containerPort: 8883
          - name: mgmt
            containerPort: 8081
          - name: ws
            containerPort: 8083
          - name: wss
            containerPort: 8084
          - name: dashboard
            containerPort: 18083
          envFrom:
            - configMapRef:
                name: emqx-config
  ```

+ Redeploy Deployment and view status

  ```
  $ kubectl delete -f deployment.yaml
  deployment.apps "emqx-deployment" deleted
  
  $ kubectl apply -f deployment.yaml
  deployment.apps/emqx-deployment created
  
  $ kubectl get pods
  NAME                               READY   STATUS    RESTARTS   AGE
  emqx-deployment-5c7696b5d7-k9lzj   1/1     Running   0          3s
  emqx-deployment-5c7696b5d7-mdwkt   1/1     Running   0          3s
  emqx-deployment-5c7696b5d7-z57z7   1/1     Running   0          3s
  
  $ kubectl exec emqx-deployment-5c7696b5d7-k9lzj -- emqx_ctl status
  Node 'emqx@192.168.87.149' is started
  emqx 4.1-rc.1 is running
  
  $ kubectl exec emqx-deployment-5c7696b5d7-k9lzj -- emqx_ctl cluster status
  Cluster status: #{running_nodes =>
                        ['emqx@192.168.77.106','emqx@192.168.77.107',
                         'emqx@192.168.87.149'],
                    stopped_nodes => []}
  ```

The configuration files of EMQ X Broker have decoupled to Configmap. If necessary, you can freely configure one or more Configmap, and import them as environment variables or files to the pod.

### StatefulSet

[StatefulSet](https://kubernetes.io/zh/docs/concepts/workloads/controllers/statefulset/) is used for figuring out the problem that is stateful service(Deployments and ReplicaSets are designed for stateless service). The scenarios it is applied including:

- Stable persistence storage, that is,  after the pod is re-dispatched, it can also access the same persistence data. Based on PVC to implement.
- Stable network sign, that is, after the pod is re-dispatched, it's PodName and HostName have no changes. Based on Headless Service(the Service without Cluster IP) to implement.
- Orderly deployment, orderly expands, that is, the pod is sequential. So that it must be carried out in sequence according to the defined order when deploying or expanding(from 0 to N-1, all the previous pods must are Running and Ready before running the next pod). Based on init containers to implement.
- Orderly shrink, orderly delete(from 0 to N-1)

From the above scenarios, we can find that StatefulSet consists of the following parts:

- Headless Service for defining network sign(DNS domain)
- VolumeClaimTemplates for creating PersistentVolumes
- StatefulSet for defining specific applications

The DNS format of every pod in StatefulSet is `statefulSetName-{0..N-1}.serviceName.namespace.svc.cluster.local`:

- `serviceName` is the name of Headless Service
- `0..N-1` is the number of Pod, from 0 to N-1
- `statefulSetName` is the name of StatefulSet
- `namespace` is the namespace where service locate in, Headless Service and StatefulSet must locate in the same namespace
- `.cluster.local` is Cluster Domain

Then, using StatefulSet replace Deployment to manage pod.

+ Delete Deployment:

  ```
  $ kubectl delete deployment emqx-deployment
  deployment.apps "emqx-deployment" deleted
  ```

+ Define StatefulSet:

  ```
  $cat statefulset.yaml
  
  apiVersion: apps/v1
  kind: StatefulSet
  metadata:
    name: emqx-statefulset
    labels:
      app: emqx
  spec:
  	serviceName: emqx-headless
    updateStrategy:
      type: RollingUpdate
    replicas: 3
    selector:
      matchLabels:
        app: emqx
    template:
      metadata:
        labels:
          app: emqx
      spec:
        serviceAccountName: emqx
        containers:
        - name: emqx
          image: emqx/emqx:v4.1-rc.1
          ports:
          - name: mqtt
            containerPort: 1883
          - name: mqttssl
            containerPort: 8883
          - name: mgmt
            containerPort: 8081
          - name: ws
            containerPort: 8083
          - name: wss
            containerPort: 8084
          - name: dashboard
            containerPort: 18083
          envFrom:
            - configMapRef:
                name: emqx-config
  ```

  It should be noted that StatefulSet needs Headless Service to implement a stable network sign, so we need to define one Service more.

  ```
  $cat headless.yaml
  
  apiVersion: v1
  kind: Service
  metadata:
    name: emqx-headless
  spec:
    type: ClusterIP
    clusterIP: None
    selector:
      app: emqx
    ports:
    - name: mqtt
      port: 1883
      protocol: TCP
      targetPort: 1883
    - name: mqttssl
      port: 8883
      protocol: TCP
      targetPort: 8883
    - name: mgmt
      port: 8081
      protocol: TCP
      targetPort: 8081
    - name: websocket
      port: 8083
      protocol: TCP
      targetPort: 8083
    - name: wss
      port: 8084
      protocol: TCP
      targetPort: 8084
    - name: dashboard
      port: 18083
      protocol: TCP
      targetPort: 18083
  ```

  Because Headless Service does not require an IP, configured `clusterIP: None`.

+ Deploy the corresponding configurations:

  ```
  $ kubectl apply -f headless-service.yaml
  service/emqx-headless created
  
  $ kubectl apply -f statefulset.yaml
  statefulset.apps/emqx-deployment created
  
  $ kubectl get pods
  NAME                               READY   STATUS    RESTARTS   AGE
  emqx-statefulset-0                 1/1     Running   0          2m59s
  emqx-statefulset-1                 1/1     Running   0          2m57s
  emqx-statefulset-2                 1/1     Running   0          2m54s
  
  $ kubectl exec emqx-statefulset-0 -- emqx_ctl cluster status
  Cluster status: #{running_nodes =>
                        ['emqx@192.168.77.105','emqx@192.168.87.153',
                         'emqx@192.168.87.155'],
                    stopped_nodes => []}
  ```

+ Update Configmap:

  StatefulSet provides a stable network sign. EMQ X Broker supports using hostname and DNS rules to replace IP for implementing cluster. Taking hostname as an example, need to modify `emqx.conf`:

  ```
  cluster.kubernetes.address_type = hostname
  cluster.kubernetes.suffix = "svc.cluster.local"
  ```

  The DNS rules of Pod in the cluster Kubernetes can be customized by users. EMQ X Broker provides `cluster.kubernetes.suffix` for facilitating users to match custom DNS rules. This article use the default DNS rules:  `statefulSetName-{0..N-1}.serviceName.namespace.svc.cluster.local`. serviceName in the DNS rules is Headless Service used by StatefulSet, so we also need to modify `cluster.kubernetes.service_name` to Headless Service Name.

  Convert configuration items to environment variables, we need to configure the following items in the Configmap:

  ```
  EMQX_CLUSTER__K8S__ADDRESS_TYPE: "hostname"
  EMQX_CLUSTER__K8S__SUFFIX: "svc.cluster.local"
  EMQX_CLUSTER__K8S__SERVICE_NAME: emqx-headless
  ```

  Configmap provides hot update. Execute `$ kubectl edit configmap emqx-config` to a hot update Configmap.

+ Redeploy StatefulSet:

  Pod will not be re-enabled after updating Configmap, so we need to manually update StatefulSet

  ```
  $ kubectl delete statefulset emqx-statefulset
  statefulset.apps "emqx-statefulset" deleted
  
  $ kubectl apply -f statefulset.yaml
  statefulset.apps/emqx-statefulset created
  
  $ kubectl get pods
  NAME                 READY   STATUS    RESTARTS   AGE
  emqx-statefulset-0   1/1     Running   0          115s
  emqx-statefulset-1   1/1     Running   0          112s
  emqx-statefulset-2   1/1     Running   0          110s
  
  $ kubectl exec emqx-statefulset-2 -- emqx_ctl cluster status
  Cluster status: #{running_nodes =>
                        ['emqx@emqx-statefulset-0.emqx-headless.default.svc.cluster.local',
                         'emqx@emqx-statefulset-1.emqx-headless.default.svc.cluster.local',
                         'emqx@emqx-statefulset-2.emqx-headless.default.svc.cluster.local'],
                    stopped_nodes => []}
  ```

  We can see that the new EMQ X Broker cluster has successfully built.

+ Abort a Pod:

  The PodName and HostName of Pod in the StatefulSet will not change after rescheduling. Let's try:

  ```
  $ kubectl get pods
  kuNAME                 READY   STATUS    RESTARTS   AGE
  emqx-statefulset-0   1/1     Running   0          6m20s
  emqx-statefulset-1   1/1     Running   0          6m17s
  emqx-statefulset-2   1/1     Running   0          6m15s
  
  $ kubectl delete pod emqx-statefulset-0
  pod "emqx-statefulset-0" deleted
  
  $ kubectl get pods
  NAME                 READY   STATUS    RESTARTS   AGE
  emqx-statefulset-0   1/1     Running   0          27s
  emqx-statefulset-1   1/1     Running   0          9m45s
  emqx-statefulset-2   1/1     Running   0          9m43s
  
  $ kubectl exec emqx-statefulset-2 -- emqx_ctl cluster status
  Cluster status: #{running_nodes =>
                        ['emqx@emqx-statefulset-0.emqx-headless.default.svc.cluster.local',
                         'emqx@emqx-statefulset-1.emqx-headless.default.svc.cluster.local',
                         'emqx@emqx-statefulset-2.emqx-headless.default.svc.cluster.local'],
                    stopped_nodes => []}
  ```

  As expected, StatefulSet rescheduled a pod with the same network symbol. EMQ X Broker in the pod has also successfully joined the cluster.

## StorageClasses, PersistentVolume and PersistentVolumeClaim

PersistentVolume(PV) is the storage set by the administrator, and it is part of the cluster. It like the node is the resource of the cluster, PV is also the resource od cluster. PV is volume plugin like Volume, but it has a life cycle which is independent of the pod using PV. This API object includes the details of the implementation of storage, that is, NFS, iSCSI or storage systems specific to cloud vendors.

PersistentVolumeClaim(PVC) is the requirements stored by users. It is similar to Pod. Pod consumes the node resource, and PVC consumes PV resources. Pod can request resources at a specific level(CPU and RAM). The declaration can request the specific size and accessing mode(for example, can read/write once or mount in read-only multiple)

StorageClass describes the method used to store "class" for administrators. Different class may be mapped to different quality of service levels or backup strategies, or the arbitrary strategy confirmed by the cluster administrator. Kubernetes itself is not clear what the various class represent. This concept is sometimes referred to as "configuration file" in other storage systems.

You can create PV or StorageClass in advance when deploy EMQ X Broker, and then using PVC mount the directory `/opt/emqx/data/mnesia` of EMQ X Broker. After rescheduling Pods, EMQ X will recover the data from directory `/opt/emqx/data/mnesia` for implementing the persistence of EMQ X Broker.

+ Define StatefulSet

  ```
  $cat statefulset.yaml
  
  apiVersion: apps/v1
  kind: StatefulSet
  metadata:
    name: emqx-statefulset
    labels:
      app: emqx
  spec:
    replicas: 3
    serviceName: emqx-headless
    updateStrategy:
      type: RollingUpdate
    selector:
      matchLabels:
        app: emqx
    template:
      metadata:
        labels:
          app: emqx
      spec:
        volumes:
        - name: emqx-data
          persistentVolumeClaim:
            claimName: emqx-pvc
        serviceAccountName: emqx
        containers:
        - name: emqx
          image: emqx/emqx:v4.1-rc.1
          ports:
          - name: mqtt
            containerPort: 1883
          - name: mqttssl
            containerPort: 8883
          - name: mgmt
            containerPort: 8081
          - name: ws
            containerPort: 8083
          - name: wss
            containerPort: 8084
          - name: dashboard
            containerPort: 18083
          envFrom:
            - configMapRef:
                name: emqx-config
          volumeMounts:
          - name: emqx-data
            mountPath: "/opt/emqx/data/mnesia"
    volumeClaimTemplates:
    - metadata:
        name: emqx-pvc
        annotations:
          volume.alpha.kubernetes.io/storage-class: manual
      spec:
        accessModes: [ "ReadWriteOnce" ]
        resources:
          requests:
            storage: 1Gi
  ```

  First, this file specifies using the storage class named manual through `volumeClaimTemplates` to create the PVC resources named `emqx-pvc`. The read and write mode of PVC resources is `ReadWriteOnce`, which need 1Gi space. Next, define this PVC as a volume named `emqx-data`, and mount this volume on the directory `/opt/emqx/data/mnesia` of Pod.

+ Deploy resources:

  Users or cluster Kubernetes administrators need to create storage class before deploying StatefulSet.

  ```
  $ kubectl apply -f statefulset.yaml
  statefulset.apps/emqx-statefulset created
  
  $ kubectl get pods
  NAME                 READY   STATUS    RESTARTS   AGE
  emqx-statefulset-0   1/1     Running   0          27s
  emqx-statefulset-1   1/1     Running   0          9m45s
  emqx-statefulset-2   1/1     Running   0          9m43s
  
  $ kubectl get pvc
  NAME                  			   STATUS    VOLUME                                 CAPACITY   ACCESS MODES   STORAGECLASS   AGE
  emqx-data-emqx-statefulset-0   Bound     pvc-8094cd75-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            2m11s
  emqx-data-emqx-statefulset-0   Bound     pvc-9325441d-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            99s
  emqx-data-emqx-statefulset-0   Bound     pvc-ad425e9d-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            56s
  ```

  The output result represents that the status of this PVC is Bound, and PVC storage has been successfully established. EMQ X Broker will read the data is mounted in PVC for implementing persistence, when rescheduling pod.

So far, the process that EMQ X Broker builds persistence cluster in the Kubernetes has been completed. This article omits some details, and the process of deployment is also for the simple Demo. Users can read [kubernetes documentation](https://kubernetes.io/docs/home/) and [Helm chart source code](https://github.com/emqx/emqx-rel/tree/master/deploy/charts/emqx) provided by the EMQ X Team for more in-depth research. Of course, contributing issues, pulling requests and star on Github are welcome.
