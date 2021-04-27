EMQ X supports automatic clustering through the Kubernetes service. You need to use kubeadm to create a 3 nodes cluster in Ubuntu before starting to build an EMQ X cluster as introduced in below.

*Notice: This article requires you have the basic understanding for kubernetes cluster resources, such as pods, services, etc. You can read the* [*documentation*](https://kubernetes.io/docs/concepts/workloads/) *to learn it.*

### Lab Environment

- Public cloud environment: AWS EC2
- Operating system: Ubuntu 16.04
- kubeadm version: v1.12.1
- Docker version: 18.6.1
- Cluster node:

```
| hostname   | Node role | IP address    |
| ---------- | --------- | ------------- |
| kube-node1 | master    | 172.31.18.155 |
| kube-node2 | worker    | 172.31.21.171 |
| kube-node3 | worker    | 172.31.20.189 |
```

### Ready to Work

#### View kubernetes Cluster Status

```
$ kubectl get node -o wide
NAME         STATUS   ROLES    AGE   VERSION   INTERNAL-IP     EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION    CONTAINER-RUNTIME
kube-node1   Ready    master   28h   v1.12.1   172.31.18.155   <none>        Ubuntu 18.04.1 LTS   4.15.0-1021-aws   docker://18.6.1
kube-node2   Ready    <none>   28h   v1.12.1   172.31.21.171   <none>        Ubuntu 18.04.1 LTS   4.15.0-1021-aws   docker://18.6.1
kube-node3   Ready    <none>   28h   v1.12.1   172.31.20.189   <none>        Ubuntu 18.04.1 LTS   4.15.0-1021-aws   docker://18.6.1
$ kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                                 READY   STATUS    RESTARTS   AGE     IP          NODE         NOMINATED NODE
kube-system   coredns-576cbf47c7-b5xbb             1/1     Running   0          28h   10.244.0.5      kube-node1   <none>
kube-system   coredns-576cbf47c7-g5s9j             1/1     Running   0          28h   10.244.0.4      kube-node1   <none>
kube-system   etcd-kube-node1                      1/1     Running   0          28h   172.31.18.155   kube-node1   <none>
kube-system   kube-apiserver-kube-node1            1/1     Running   0          28h   172.31.18.155   kube-node1   <none>
kube-system   kube-controller-manager-kube-node1   1/1     Running   0          28h   172.31.18.155   kube-node1   <none>
kube-system   kube-flannel-ds-amd64-fscrm          1/1     Running   0          28h   172.31.20.189   kube-node3   <none>
kube-system   kube-flannel-ds-amd64-hhj8b          1/1     Running   0          28h   172.31.21.171   kube-node2   <none>
kube-system   kube-flannel-ds-amd64-l6ccn          1/1     Running   0          28h   172.31.18.155   kube-node1   <none>
kube-system   kube-proxy-79thv                     1/1     Running   0          28h   172.31.20.189   kube-node3   <none>
kube-system   kube-proxy-ckg9t                     1/1     Running   0          28h   172.31.21.171   kube-node2   <none>
kube-system   kube-proxy-skq8m                     1/1     Running   0          28h   172.31.18.155   kube-node1   <none>
kube-system   kube-scheduler-kube-node1            1/1     Running   0          28h   172.31.18.155   kube-node1   <none>
```

#### View apiserver Configuration

EMQ X automatic clustering function need to use kubernetes apiserver. Let’s firstly take a look at configuration of apiserver.

```
$ kubectl describe pods kube-apiserver-kube-node1 -n kube-system  
Name:               kube-apiserver-kube-node1
Namespace:          kube-system
Priority:           2000000000
PriorityClassName:  system-cluster-critical
Node:               kube-node1/172.31.18.155
Start Time:         Tue, 23 Oct 2018 02:29:37 +0000
Labels:             component=kube-apiserver
                    tier=control-plane
Annotations:        kubernetes.io/config.hash: c5ac975e628056601100307026359ba8
                    kubernetes.io/config.mirror: c5ac975e628056601100307026359ba8
                    kubernetes.io/config.seen: 2018-10-17T02:00:07.757483468Z
                    kubernetes.io/config.source: file
                    scheduler.alpha.kubernetes.io/critical-pod: 
Status:             Running
IP:                 172.31.18.155
Containers:
  kube-apiserver:
    Container ID:  docker://d753a932b41ff8a99b6a11767d463f13af7e9de7526567df6eb5bd29a101f17b
    Image:         k8s.gcr.io/kube-apiserver:v1.12.1
    Image ID:      docker-pullable://k8s.gcr.io/kube-apiserver@sha256:52b9dae126b5a99675afb56416e9ae69239e012028668f7274e30ae16112bb1f
    Port:          <none>
    Host Port:     <none>
    Command:
      kube-apiserver
      --authorization-mode=Node,RBAC
      --advertise-address=172.31.18.155
      --allow-privileged=true
      --client-ca-file=/etc/kubernetes/pki/ca.crt
      --enable-admission-plugins=NodeRestriction
      --enable-bootstrap-token-auth=true
      --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
      --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
      --etcd-keyfile=/etc/kubernetes/pki/apiserver-etcd-client.key
      --etcd-servers=https://127.0.0.1:2379
      --insecure-port=0
      --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt
      --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
      --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname
      --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt
      --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key
      --requestheader-allowed-names=front-proxy-client
      --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
      --requestheader-extra-headers-prefix=X-Remote-Extra-
      --requestheader-group-headers=X-Remote-Group
      --requestheader-username-headers=X-Remote-User
      --secure-port=6443
      --service-account-key-file=/etc/kubernetes/pki/sa.pub
      --service-cluster-ip-range=10.96.0.0/12
      --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
      --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
    State:          Running
      Started:      Tue, 23 Oct 2018 02:29:39 +0000
    Last State:     Terminated
      Reason:       Completed
      Exit Code:    0
      Started:      Wed, 17 Oct 2018 02:00:09 +0000
      Finished:     Thu, 18 Oct 2018 12:43:31 +0000
    Ready:          True
    Restart Count:  1
    Requests:
      cpu:        250m
    Liveness:     http-get https://172.31.18.155:6443/healthz delay=15s timeout=15s period=10s #success=1 #failure=8
    Environment:  <none>
    Mounts:
      /etc/ca-certificates from etc-ca-certificates (ro)
      /etc/kubernetes/pki from k8s-certs (ro)
      /etc/ssl/certs from ca-certs (ro)
      /usr/local/share/ca-certificates from usr-local-share-ca-certificates (ro)
      /usr/share/ca-certificates from usr-share-ca-certificates (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  k8s-certs:
    Type:          HostPath (bare host directory volume)
    Path:          /etc/kubernetes/pki
    HostPathType:  DirectoryOrCreate
  ca-certs:
    Type:          HostPath (bare host directory volume)
    Path:          /etc/ssl/certs
    HostPathType:  DirectoryOrCreate
  usr-share-ca-certificates:
    Type:          HostPath (bare host directory volume)
    Path:          /usr/share/ca-certificates
    HostPathType:  DirectoryOrCreate
  usr-local-share-ca-certificates:
    Type:          HostPath (bare host directory volume)
    Path:          /usr/local/share/ca-certificates
    HostPathType:  DirectoryOrCreate
  etc-ca-certificates:
    Type:          HostPath (bare host directory volume)
    Path:          /etc/ca-certificates
    HostPathType:  DirectoryOrCreate
QoS Class:         Burstable
Node-Selectors:    <none>
Tolerations:       :NoExecute
Events:            <none>
```

Obtain the IP address of the apiserver by `—-advertis-address=172.31.18.155 `(this address can be specified by `—-apiserver-advertise-address=172.31.18.155 `parameter when using `kubeadm init` command to create a cluster).

#### Access apiserver

Type `kubectl proxy --help` command to see that the `kubectl proxy`command can create a proxy server between local machine and apiserver. It allows http access to the specified rules.

```
$ kubectl proxy --accept-hosts="^.*$" --address='172.31.18.155' -p=8080 &
$ curl http://172.31.18.155:8080
{
  "paths": [
    "/api",
    "/api/v1",
    "/apis",
    "/apis/",
    "/apis/admissionregistration.k8s.io",
    "/apis/admissionregistration.k8s.io/v1beta1",
    "/apis/apiextensions.k8s.io",
    "/apis/apiextensions.k8s.io/v1beta1",
    "/apis/apiregistration.k8s.io",
    "/apis/apiregistration.k8s.io/v1",
    "/apis/apiregistration.k8s.io/v1beta1",
    ......
```

### Create a Resource

`kubectl` can create various resources through `kubectl create -f xxx.yml`, then you only need to write one or more valid yml files to create an EMQ X cluster. This article writes all the resources within one yml file. With actual practice, you can create multiple yml files in one directory and deploy them using `kubectl create -f directory name`.

```
| Resource Type | Name |
| ------------- | ---- |
| service       | emqx |
| deployment    | emqx |
| pod           | emqx |
```

In general, services, deployment, and pods should have different names to distiguish them, but EMQ X’s automatic clustering feature needs have them the same name.

#### Deployment && Pod

Refer to the configuration of the Kubernetes auto-cluster in [documentation of EMQ X](https://docs.emqx.io/en/broker/v2.0/cluster.html), you need to modify configuration of `etc/emqx.conf` as following.

```
cluster.discovery = k8s
##--------------------------------------------------------------------
## Cluster with k8s
cluster.k8s.apiserver = http://10.110.111.204:8080
cluster.k8s.service_name = emqx
## Address Type: ip | dns
cluster.k8s.address_type = ip
## The Erlang application name
cluster.k8s.app_name = emqx
## Kubernates Namespace
cluster.k8s.namespace = default
```

Refer to documentation in the [EMQ X image on Github](https://github.com/emqx/emqx-docker/blob/master/README.md), you can edit `etc/emqx.conf` to change the environment variables. According to the configuration required as previous, we can specify the following environment variables.

```
- name: EMQX_CLUSTER__DISCOVERY
    value: k8s
- name: EMQX_NAME
    value: emqx
- name: EMQX_CLUSTER__K8S__APISERVER
    value: http://172.31.19.161:8080
- name: EMQX_CLUSTER__K8S__NAMESPACE
    value: default
- name: EMQX_CLUSTER__K8S__SERVICE_NAME
    value: emqx
- name: EMQX_CLUSTER__K8S__ADDRESS_TYPE
    value: ip
- name: EMQX_CLUSTER__K8S__APP_NAME
    value: emqx
```

Create deployment and pod: pod can only use the [docker hub image](https://hub.docker.com/r/emqx/emqx/), because kubernetes can’t directly use Dockerfile to compile the image and you’ll have to pull from the docker’s mirror repository. Please specify 2 images for deploy pod, and port, environment variables as well.

```
kind: Deployment
metadata:
  name: emqx
  labels:
        app: emqx
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: emqx
    spec:
      containers:
      - name: emqx
        image: emqx/emqx:latest
        ports:
        - name: emqx-dashboard
          containerPort: 18083
        env:
        - name: EMQX_CLUSTER__DISCOVERY
          value: k8s
        - name: EMQX_NAME
          value: emqx
        - name: EMQX_CLUSTER__K8S__APISERVER
          value: http://172.31.19.161:8080
        - name: EMQX_CLUSTER__K8S__NAMESPACE
          value: default
        - name: EMQX_CLUSTER__K8S__SERVICE_NAME
          value: emqx
        - name: EMQX_CLUSTER__K8S__ADDRESS_TYPE
          value: ip
        - name: EMQX_CLUSTER__K8S__APP_NAME
          value: emqx
        tty: true
```

#### Services

Create a service and use the NodePort method to expose the port of emqx-dashboard for external access, so that user can access the dashboard by host address.

```
apiVersion: v1
kind: Service
metadata:
  name: emqx
spec:
  ports:
  - port: 32333
    nodePort: 32333
    targetPort:  emqx-dashboard
    protocol: TCP
  selector:
    app: emqx
  type: NodePort
```

### Deploy Service

Check out the emqx.yml file.

```
cat emqx.yml
apiVersion: v1
kind: Service
metadata:
  name: emqx
spec:
  ports:
  - port: 32333
    nodePort: 32333
    targetPort:  emqx-dashboard
    protocol: TCP
  selector:
    app: emqx
  type: NodePort
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: emqx
  labels:
        app: emqx
spec:
  replicas: 2
  template:
    metadata:
      labels:
        app: emqx
    spec:
      containers:
      - name: emqx
        image: emqx/emqx:latest
        ports:
        - name: emqx-dashboard
          containerPort: 18083
        env:
        - name: EMQX_CLUSTER__DISCOVERY
          value: k8s
        - name: EMQX_NAME
          value: emqx
        - name: EMQX_CLUSTER__K8S__APISERVER
          value: http://172.31.19.161:8080
        - name: EMQX_CLUSTER__K8S__NAMESPACE
          value: default
        - name: EMQX_CLUSTER__K8S__SERVICE_NAME
          value: emqx
        - name: EMQX_CLUSTER__K8S__ADDRESS_TYPE
          value: ip
        - name: EMQX_CLUSTER__K8S__APP_NAME
          value: emqx
        tty: true
```

Deploy EMQ X.

```
$ kubectl create -f emqx.yml 
service/emqx created
deployment.extensions/emqx created
```

Take a look at status of deployment, you can see that all resources have been successfully deployed.

```
$ kubectl get all -o wide
NAME                                  READY   STATUS        RESTARTS   AGE     IP            NODE         NOMINATED NODE
pod/emqx-7685fc45cd-qmxlq             1/1     Running       0          3m22s   10.244.2.14   kube-node3   <none>
pod/emqx-7685fc45cd-zq2cj             1/1     Running       0          3m22s   10.244.1.18   kube-node2   <none>
NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)           AGE     SELECTOR
service/emqx         NodePort    10.98.146.60   <none>        32333:32333/TCP   2m49s   app=emqx
service/kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP           6d5h    <none>
NAME                   DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES             SELECTOR
deployment.apps/emqx   2         2         2            2           2m49s   emqx         emqx/emqx:latest   app=emqx
NAME                              DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES             SELECTOR
replicaset.apps/emqx-7685fc45cd   2         2         2       2m49s   emqx         emqx/emqx:latest   app=emqx,pod-template-hash=7685fc45cd
```

Using the command to view the cluster status, you can see that EMQ X has been automatically clustered.

```
$ kubectl exec -it emqx-7685fc45cd-qmxlq /opt/emqx/bin/emqx_ctl cluster status
Cluster status: [{running_nodes,['emqx@10.244.1.18','emqx@10.244.2.14']}]
```

Even if you delete a pod, kubernetes will automatically create a new pod to auto-cluster.

```
$ kubectl delete pod/emqx-7685fc45cd-zq2cj
pod "emqx-7685fc45cd-zq2cj" deleted
$ kubectl get pods 
NAME                    READY   STATUS    RESTARTS   AGE
emqx-7685fc45cd-nt54v   1/1     Running   0          56s
emqx-7685fc45cd-qmxlq   1/1     Running   0          6m25
$ kubectl exec -it emqx-7685fc45cd-qmxlq /opt/emqx/bin/emqx_ctl cluster status
Cluster status: [{running_nodes,['emqx@10.244.1.19','emqx@10.244.2.14']},
                 {stopped_nodes,['emqx@10.244.1.18']}]
```

Open a browser and enter `[http://nodeIP](http://nodeip/): 32333`, EMQ X dashboard page can be dislayed successfully.

------

Author: Hongtong Zhang@EMQX