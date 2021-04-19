

EMQ X Team 提供了 Helm chart 方便用户在 kubernetes 集群上一键部署 EMQ X [MQTT 服务器](https://www.emqx.cn/products/broker), 这是 EMQ X Team 最推荐的在 kubernetes 或 k3s 集群上部署 EMQ X MQTT 服务器的方法。 本文将使用手写 yaml 文件的方法从零开始部署一个 EMQ X MQTT 服务器的 K8S 集群, 分析部署中的细节与技巧，方便用户在实际部署中灵活使用。

阅读本文需要用户了解 kubernetes 的基本概念，并有一个可操作的 kubernetes 集群。

## 在 K8S 上部署单个 EMQ X MQTT服务器节点

### 使用 Pod 直接部署 EMQ X Broker

在Kubernetes中，最小的管理元素不是一个个独立的容器，而是 [Pod](https://kubernetes.io/zh/docs/concepts/workloads/pods/pod-overview/)，Pod 是 Kubernetes 应用程序的基本执行单元，即它是 Kubernetes 对象模型中创建或部署的最小和最简单的单元。Pod 表示在 [集群](https://kubernetes.io/zh/docs/reference/glossary/?all=true#term-cluster) 上运行的进程。

EMQ X Broker 在 [docker hub](https://hub.docker.com/r/emqx/emqx) 上提供了镜像, 因此可以很方便的在单个的 pod 上部署 EMQ X Broker，使用 `kubectl run` 命令创建一个运行着 EMQ X Broker 的 Pod：

```
$ kubectl run emqx --image=emqx/emqx:v4.1-rc.1  --generator=run-pod/v1
pod/emqx created
```

查看 EMQ X Broker 的状态：

```
$ kubectl get pods -o wide
NAME   READY   STATUS    RESTARTS   AGE
emqx   1/1     Running   0          3m13s

$ kubectl exec emqx -- emqx_ctl status
Node 'emqx@192.168.77.108' is started
emqx 4.1-rc.1 is running
```

删除 Pod：

```
$ kubectl delete pods emqx
pod "emqx" deleted
```

Pod 并不是被设计成一个持久化的资源，它不会在调度失败，节点崩溃，或者其他回收中（比如因为资源的缺乏，或者其他的维护中）幸存下来，因此，还需要一个控制器来管理 Pod。

### 使用 Deoloyment 部署 Pod

[Deployment](https://kubernetes.io/zh/docs/concepts/workloads/controllers/deployment/) 为 Pod 和 ReplicaSet 提供了一个声明式定义（declarative）方法，用来替代以前的[ReplicationController](https://www.kubernetes.org.cn/replication-controller-kubernetes) 来方便的管理应用。典型的应用场景包括：

- 定义Deployment来创建Pod和ReplicaSet
- 滚动升级和回滚应用
- 扩容和缩容
- 暂停和继续Deployment

使用 Deployment 部署一个 EMQ X Broker Pod：

+ 定义 Deployment：

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

+ 部署 Deployment：

  ```
  $  kubectl apply -f deployment.yaml
  deployment.apps/emqx-deployment created
  ```

+ 查看部署情况：

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

+ 尝试手动删除 Pod

  ```
  $ kubectl delete pods emqx-deployment-7c44dbd68-8j77l
  pod "emqx-deployment-7c44dbd68-8j77l" deleted
  
  $ kubectl get pods
  NAME                              READY   STATUS    RESTARTS   AGE
  emqx-deployment-68fcb4bfd6-2nhh6   1/1     Running   0          59s
  ```

  输出结果表明成功用 Deployment 部署了 EMQ X Broker Pod，即使是此 Pod 被意外终止，Deployment 也会重新创建一个新的 Pod。

### 使用 Services 公开 EMQ X Broker Pod 服务

Kubernetes [Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) 是有生命周期的。他们可以被创建，而且销毁不会再启动。 如果使用 [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) 来运行应用程序，则它可以动态创建和销毁 Pod。

每个 Pod 都有自己的 IP 地址，但是在 Deployment 中，在同一时刻运行的 Pod 集合可能与稍后运行该应用程序的 Pod 集合不同。

这导致了一个问题：如果使用 EMQ X Broker Pod 为 **MQTT 客户端**提供服务，那么客户端应该如何如何找出并跟踪要连接的 IP 地址，以便客户端使用 EMQ X Broker 服务呢？

答案是：Service

Service 是将运行在一组 [Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/) 上的应用程序公开为网络服务的抽象方法。

使用 Service 将 EMQ X Broker Pod 公开为网络服务：

+ 定义 Service：

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

+ 部署 Service：

  ```
  $ kubectl apply -f service.yaml
  service/emqx-service created
  ```

+ 查看部署情况

  ```
  $ kubectl get svc
  NAME           TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)                                        AGE
  emqx-service   ClusterIP   10.96.54.205   <none>        1883/TCP,8883/TCP,8081/TCP,8083/TCP,8084/TCP,18083/TCP   58s
  ```

+ 使用 Service 提供的 IP 查看 EMQ X Broker 的 API

  ```
  $ curl 10.96.54.205:8081/status
  Node emqx-deployment-68fcb4bfd6-2nhh6@192.168.77.120 is started
  emqx is running
  ```

至此，单个 EMQ X Broker 节点在 kubernetes 上部署完毕，通过 Deployment 管理 EMQ X Broker Pod，通过 Service 将 EMQ X Broker 服务暴露出去。

## 通过 kubernetes 自动集群 EMQ X MQTT 服务器

上文中通过 Deployment 部署了单个的 EMQ X Broker Pod，通过 Deployment 扩展 Pod 的数量是极为方便的，执行 `kubectl scale deployment ${deployment_name} --replicas ${numer}` 命令即可扩展 Pod 的数量，下面将 EMQ X Broker Pod 扩展为 3 个：

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

可以看到 EMQ X Broker Pod 的数量被扩展为 3 个，但是每个 Pod 都是独立的，并没有集群，接下来尝试通过 kubernetes 自动集群 EMQ X Broker Pod。

### 修改 EMQ X Broker 的配置

查看 EMQ X Broker 文档中关于[自动集群](https://docs.emqx.io/broker/latest/cn/advanced/cluster.html#emqx-service-discovery-kubernetes)的内容，可以看到需要修改 EMQ X Broker 的配置：

```
cluster.discovery = kubernetes
cluster.kubernetes.apiserver = http://10.110.111.204:8080
cluster.kubernetes.service_name = ekka
cluster.kubernetes.address_type = ip
cluster.kubernetes.app_name = ekka
```

其中 `cluster.kubernetes.apiserver` 为 kubernetes apiserver 的地址，可以通过 `kubectl cluster-info` 命令获取，`cluster.kubernetes.service_name` 为上文中 Service 的 name， `cluster.kubernetes.app_name` 为 EMQ X Broker 的 `node.name` 中 `@` 符号之前的部分，所以还需要将集群中 EMQ X Broker 设置为统一的 `node.name` 的前缀。

EMQ X Broker 的 docker 镜像提供了通过环境变量修改配置的功能，具体可以查看 [docker hub](https://hub.docker.com/r/emqx/emqx) 或 [Github](https://github.com/emqx/emqx-rel/blob/master/deploy/docker/README.md)。

+ 修改 Deployment 的 yaml 文件，增加环境变量：

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

  > 因为 ``kubectl scale deployment ${deployment_name} --replicas ${numer}` 命令不会修改 yaml 文件，所以修改 yaml 时需要设置 `spec.replicas: 3` 。

  > Pod 中内建 kubernetes 的 DNS 规则，所以 `https://kubernetes.default.svc:443` 会被解析为 kubernetes apiserver  的地址。

+ 删除之前的 Deployment，重新部署：

  ```
  $ kubectl delete deployment emqx-deployment
  deployment.apps "emqx-deployment" deleted
  
  $ kubectl apply -f deployment.yaml
  deployment.apps/emqx-deployment created
  ```


### 赋予 Pod 访问 kubernetes apiserver 的权限

上文部署 Deployment 之后，查看 EMQ X Broker 的状态，可以看到 EMQ X Broker 虽然成功启动了，但是依然没有集群成功，查看 EMQ X Broker Pod 的 log：

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

Pod 因为权限问题在访问 kubernetes apiserver 的时候被拒绝，返回 HTTP 403，所以集群失败。

普通 Pod 是无法访问 kubernetes apiserver 的，解决这个问题有两种方法，一种是开放 kubernetes apiserver 的 http 接口，但是这种方法存在一定的安全隐患，另外一种是通过 ServiceAccount、Role 和 RoleBinding 配置 RBAC 鉴权。

+ 定义  ServiceAccount、Role 和 RoleBinding：

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

+ 部署相应的资源：

  ```
  $ kubectl apply -f rbac.yaml
  serviceaccount/emqx created
  role.rbac.authorization.kubernetes.io/emqx created
  rolebinding.rbac.authorization.kubernetes.io/emqx created
  ```

+ 修改 Deployment 的 yaml 文件，增加 `spec.template.spec.serviceAccountName`，并重新部署：

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

+ 查看状态：

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

+ 中止一个 Pod：

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

  输出结果表明 EMQ X Broker 会正确的显示已经停掉的 Pod，并将 Deployment 新建的 Pod 加入集群。

至此，EMQ X Broker 在 kubernetes 上成功建立集群。

## 持久化 EMQ X Broker 集群

上文中使用的 Deployment 来管理 Pod，但是 Pod 的网络是不停变动的，而且当 Pod 被销毁重建时，储存在 EMQ X Broker 的数据和配置也就随之消失了，这在生产中是不能接受的，接下来尝试把 EMQ X Broker 的集群持久化，即使 Pod 被销毁重建，EMQ X Broker 的数据依然可以保存下来。

### ConfigMap

[ConfigMap](https://kubernetes.io/zh/docs/concepts/configuration/configmap/) 是 configMap 是一种 API 对象，用来将非机密性的数据保存到健值对中。使用时可以用作环境变量、命令行参数或者存储卷中的配置文件。

ConfigMap 将您的环境配置信息和 [容器镜像](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/#why-containers) 解耦，便于应用配置的修改。

> ConfigMap 并不提供保密或者加密功能。如果你想存储的数据是机密的，请使用 [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) ，或者使用其他第三方工具来保证你的数据的私密性，而不是用 ConfigMap。

接下来使用 ConfigMap 记录 EMQ X Broker 的配置，并将它们以环境变量的方式导入到 Deployment 中。

+ 定义 Configmap，并部署：

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

+ 配置 Deployment 来使用 Configmap

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

+ 重新部署 Deployment，查看状态

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

EMQ X Broker 的配置文件已经解耦到 Configmap 中了，如果有需要，可以自由的配置一个或多个 Configmap，并把它们作为环境变量或是文件引入到 Pod 内。

### StatefulSet

[StatefulSet](https://kubernetes.io/zh/docs/concepts/workloads/controllers/statefulset/) 是为了解决有状态服务的问题（对应 Deployments 和 ReplicaSets 是为无状态服务而设计），其应用场景包括

- 稳定的持久化存储，即 Pod 重新调度后还是能访问到相同的持久化数据，基于 PVC 来实现
- 稳定的网络标志，即 Pod 重新调度后其 PodName 和 HostName 不变，基于 Headless Service（即没有Cluster IP的Service）来实现
- 有序部署，有序扩展，即 Pod 是有顺序的，在部署或者扩展的时候要依据定义的顺序依次依次进行（即从0到N-1，在下一个Pod运行之前所有之前的 Pod 必须都是 Running 和 Ready 状态），基于 init containers 来实现
- 有序收缩，有序删除（即从N-1到0）

从上面的应用场景可以发现，StatefulSet由以下几个部分组成：

- 用于定义网络标志（DNS domain）的 Headless Service
- 用于创建 PersistentVolumes 的 volumeClaimTemplates
- 定义具体应用的 StatefulSet

StatefulSet 中每个 Pod 的 DNS 格式为 `statefulSetName-{0..N-1}.serviceName.namespace.svc.cluster.local` ，其中

- `serviceName` 为 Headless Service 的名字
- `0..N-1` 为 Pod 所在的序号，从 0 开始到 N-1
- `statefulSetName` 为StatefulSet的名字
- `namespace` 为服务所在的 namespace，Headless Servic 和 StatefulSet 必须在相同的 namespace
- `.cluster.local` 为 Cluster Domain

接下来使用 StatefulSet 代替 Deployment 来管理 Pod。

+ 删除 Deployment：

  ```
  $ kubectl delete deployment emqx-deployment
  deployment.apps "emqx-deployment" deleted
  ```

+ 定义 StatefulSet：

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

  注意，StatefulSet 需要 Headless Service 来实现稳定的网络标志，因此需要再定义一个 Service

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

  因为 Headless Service 并不需要 IP，所以配置了 `clusterIP: None` 。

+ 部署相应的资源：

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

+ 更新 Configmap：

  StatefulSet 提供了稳定的网络标志，EMQ X Broker 支持使用 hostname 和 dns 规则来代提 IP 实现集群，以 hostname 为例，需要修改 `emqx.conf`：

  ```
  cluster.kubernetes.address_type = hostname
  cluster.kubernetes.suffix = "svc.cluster.local"
  ```

  kubernetes 集群中 Pod 的 DNS 规则可以由用户自定义，EMQ X Broker 提供了  `cluster.kubernetes.suffix` 方便用户匹配自定的 DNS 规则，本文使用默认的 DNS 规则：`statefulSetName-{0..N-1}.serviceName.namespace.svc.cluster.local` ，DNS 规则中的 serviceName 为 StatefulSet 使用的 Headless Service，所以还需要将 `cluster.kubernetes.service_name`  修改为 Headless Service Name。 

  将配置项转为环境变量，需要在 Configmap 中配置：

  ```
  EMQX_CLUSTER__K8S__ADDRESS_TYPE: "hostname"
  EMQX_CLUSTER__K8S__SUFFIX: "svc.cluster.local"
  EMQX_CLUSTER__K8S__SERVICE_NAME: emqx-headless
  ```

  Configmap 提供了热更新功能，执行 `$ kubectl edit configmap emqx-config` 来热更新 Configmap。

+ 重新部署 StatefulSet：

  Configmap 更新之后 Pod 并不会重启，需要我们手动更新 StatefulSet

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

  可以看到新的 EMQ X Broker 集群已经成功的建立起来了。

+ 中止一个 Pod：

  StatefulSet 中的 Pod 重新调度后其 PodName 和 HostName 不变，下面来尝试一下：

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

  跟预期的一样，StatefulSet 重新调度了一个具有相同网络标志的 Pod，Pod 中的 EMQ X Broker 也成功的加入了集群。

# StorageClasses、PersistentVolume 和 PersistentVolumeClaim

PersistentVolume（PV）是由管理员设置的存储，它是群集的一部分。就像节点是集群中的资源一样，PV 也是集群中的资源。 PV 是 Volume 之类的卷插件，但具有独立于使用 PV 的 Pod 的生命周期。此 API  对象包含存储实现的细节，即 NFS、iSCSI 或特定于云供应商的存储系统。

PersistentVolumeClaim（PVC）是用户存储的请求。它与 Pod 相似。Pod 消耗节点资源，PVC 消耗 PV 资源。Pod 可以请求特定级别的资源（CPU 和内存）。声明可以请求特定的大小和访问模式（例如，可以以读/写一次或 只读多次模式挂载）。

StorageClass 为管理员提供了描述存储 "class（类）" 的方法。 不同的 class  可能会映射到不同的服务质量等级或备份策略，或由群集管理员确定的任意策略。 Kubernetes 本身不清楚各种 class  代表的什么。这个概念在其他存储系统中有时被称为“配置文件”。

在部署 EMQ X Broker 的时候，可以预先创建好 PV 或 StorageClass，然后利用 PVC 将 EMQ X Broker 的 `/opt/emqx/data/mnesia` 目录挂载出来，当Pods被重新调度之后，EMQ X 会从 `/opt/emqx/data/mnesia` 目录中获取数据并恢复，从而实现 EMQ X Broker 的持久化。

+ 定义 StatefulSet

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

  该文件首先通过 `volumeClaimTemplates` 指定了使用 StorageClass 的 name 为 manual 的存储类创建名称为 emqx-pvc 的 PVC 资源，PVC 资源的读写模式为 `ReadWriteOnce`，需要 1Gi 的空间，然后将此 PVC 定义为 name 为 emqx-data 的 volumes，并将此 volumes 挂载在 Pod 中的 `/opt/emqx/data/mnesia`  目录下。

+ 部署资源：

  部署 StatefulSet 之前，需要用户或 kubernetes 集群管理员自行创建存储类。

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

  输出结果表明该 PVC 的状态为 Bound，PVC 存储已经成功的建立了，当 Pod 被重新调度时，EMQ X Broker 会读取挂载到 PVC 中的数据，从而实现持久化。

EMQ X Broker 在 kubernetes 上建立持久化的集群就完成了，本文略过了部分细节，部署的过程也是偏向简单的 Demo，用户可以自行阅读 [kubernetes 文档](https://kubernetes.io/zh/docs/home/) 与  EMQ X Team 提供的 [Helm chart 源码](https://github.com/emqx/emqx-rel/tree/master/deploy/charts/emqx) 来继续深入研究，当然也欢迎在 Github 贡献 issue、pull requests 以及 start。









