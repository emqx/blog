本文描述如何通过Rancher2.0部署kubernetes集群，并将EMQ X部署到kubernetes集群上

## 实验环境：

- 公有云环境：AWS EC2
- 操作系统：ubuntu 16.04
- Docker version：18.09.0

## 通过Rancher部署kubernetes集群

Rancher的安装以及部署kubernetes集群的步骤推荐直接按照快速入门执行。

## 创建Rancher Api密钥

EMQ X通过访问kube-apiserver来实现自动集群功能，在Rancher中，Rancher对kube-apiserver做了一层代理，在访问kube-apiserver的时候必须提供用于向Rancher进行身份验证的API密钥。参考用户手册创建并保存API Key。本实验中创建的Access Key为：`token-dksbl`，Secret Key为：`pshhhf5cp8d5v5x7bzjdm82qfrwgx7f2bzksnr748j42xmbvvklbdz`，组合成的Token为：`token-dksbl:pshhhf5cp8d5v5x7bzjdm82qfrwgx7f2bzksnr748j42xmbvvklbdz`

## 下载并配置kubectl

1. 下载并安装kubectl
2. 进入Rancher集群页面，点击Kubeconfig文件。

![WX20190803103351.png](https://static.emqx.net/images/1545d54c22220da508c1427ade090b0e.png)

将kubeconfig文件保存到`~/.kube/config`

![WX20190803103449.png](https://static.emqx.net/images/0932705013b5f69fb20082426feafb1d.png)

执行`kubectl cluster-info`验证配置是否成功

```
$ kubectl cluster-infoKubernetes master is running at https://13.125.244.172/k8s/clusters/c-vvgjq
KubeDNS is running at https://13.125.244.172/k8s/clusters/c-vvgjq/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

## 访问kube-apiserver

EMQ X通过访问kube-apiserver来实现自动集群，kube-apiserver的地址可以查看`~/.ssh/config`文件或者执行`kubectl cluster-info`获取，本实验中kube-apiserver的地址为：`https://13.125.244.172/k8s/clusters/c-vvgjq`。

直接访问kube-apiserver，可以看到会报错需要认证。

```
$ curl -k https://13.125.244.172/k8s/clusters/c-vvgjq{"type":"error","status":"401","message":"must authenticate"}
```

在头部加上Authorization认证则可以正常访问

```
$ curl -k -H 'Authorization: Bearer token-dksbl:pshhhf5cp8d5v5x7bzjdm82qfrwgx7f2bzksnr748j42xmbvvklbdz' https://13.125.244.172/k8s/clusters/c-vvgjq
```

## 编辑emqx.yaml

在Kubernetes 上安装 EMQ X 系列文章之二 ：EMQ X 自动集群一文中分享了EMQ X部署kubernetes集群的yaml文件如下，在Rancher上部署EMQ X集群的话需要稍加改动。

```
$cat emqx.yaml

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

EMQ X可以读取`/var/run/secrets/kubernetes.io/serviceaccount/token`文件中的内容组合Authorization认证访问kube-apiserver，所以只需要把Rancher的API Token通过Secret挂载到容器中就可以了。

> Secret解决了密码、token、密钥等敏感数据的配置问题，而不需要把这些敏感数据暴露到镜像或者Pod Spec中。Secret可以以Volume或者环境变量的方式使用。

> Secret有三种类型：

> - **Service Account** ：用来访问Kubernetes API，由Kubernetes自动创建，并且会自动挂载到Pod的`/run/secrets/kubernetes.io/serviceaccount`目录中；
> - **Opaque** ：base64编码格式的Secret，用来存储密码、密钥等；
> - **kubernetes.io/dockerconfigjson** ：用来存储私有docker registry的认证信息。

首先对API Token做base64编码

```
$ echo -n token-dksbl:pshhhf5cp8d5v5x7bzjdm82qfrwgx7f2bzksnr748j42xmbvvklbdz | base64 -w 0dG9rZW4tZGtzYmw6cHNoaGhmNWNwOGQ1djV4N2J6amRtODJxZnJ3Z3g3ZjJiemtzbnI3NDhqNDJ4bWJ2dmtsYmR6
```

在yaml文件中创建Secret

```
$vim emqx.yamlapiVersion: v1
kind: Secret
metadata:
  name: emqx-secret
type: Opaque
data:
  token: dG9rZW4tcGI2MjU6eDZ2eGJ0Y2NmdG1waGpseHR3NGNjdGN2d2txdzk5aDJzYmhxNHFtaDh4c2ZnbXd6dzJ0d2Rw
  
---
......
```

修改Deployment，将环境变量中的`EMQX_CLUSTER__K8S__APISERVER`改为Rancher的Kube-apiserver的地址，增加volumeMounts

```
$vim emqx.yaml......
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
      volumes:
      - name: emqx-secret
        secret:
           secretName: emqx-secret
      containers:
      - name: emqx
        image: emqx/emqx:latest
        ports:
        - name: emqx-dashboard
          containerPort: 18083
        - name: emqx-http
          containerPort: 8083
        - name: emqx-mqtt
          containerPort: 1883
        env:
        - name: EMQX_CLUSTER__DISCOVERY
          value: k8s
        - name: EMQX_NAME
          value: emqx
        - name: EMQX_CLUSTER__K8S__APISERVER
          value: https://13.125.244.172/k8s/clusters/c-vvgjq
        - name: EMQX_CLUSTER__K8S__NAMESPACE
          value: default
        - name: EMQX_CLUSTER__K8S__SERVICE_NAME
          value: emqx
        - name: EMQX_CLUSTER__K8S__ADDRESS_TYPE
          value: ip
        - name: EMQX_CLUSTER__K8S__APP_NAME
          value: emqx
        tty: true
        volumeMounts:
          - name: emqx-secret
            mountPath: "/var/run/secrets/kubernetes.io/serviceaccount"
            readOnly: true
```

## 部署EMQ X

查看修改后的emqx.yaml

```
$cat emqx.yamlapiVersion: v1
kind: Secret
metadata:
  name: emqx-secret
type: Opaque
data:
  token: dG9rZW4tcGI2MjU6eDZ2eGJ0Y2NmdG1waGpseHR3NGNjdGN2d2txdzk5aDJzYmhxNHFtaDh4c2ZnbXd6dzJ0d2Rw

---
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
      volumes:
      - name: emqx-secret
        secret:
           secretName: emqx-secret
      containers:
      - name: emqx
        image: emqx/emqx:latest
        ports:
        - name: emqx-dashboard
          containerPort: 18083
        - name: emqx-http
          containerPort: 8083
        - name: emqx-mqtt
          containerPort: 1883
        env:
        - name: EMQX_CLUSTER__DISCOVERY
          value: k8s
        - name: EMQX_NAME
          value: emqx
        - name: EMQX_CLUSTER__K8S__APISERVER
          value: https://13.125.244.172/k8s/clusters/c-vvgjq
        - name: EMQX_CLUSTER__K8S__NAMESPACE
          value: default
        - name: EMQX_CLUSTER__K8S__SERVICE_NAME
          value: emqx
        - name: EMQX_CLUSTER__K8S__ADDRESS_TYPE
          value: ip
        - name: EMQX_CLUSTER__K8S__APP_NAME
          value: emqx
        tty: true
        volumeMounts:
          - name: emqx-secret
            mountPath: "/var/run/secrets/kubernetes.io/serviceaccount"
            readOnly: true
```

部署EMQ X

```
$ kubectl create -f emqx.yamlsecret/emqx-secret created
service/emqx created
deployment.extensions/emqx created
```

查看状态

```
$ kubectl get podsNAME                       READY   STATUS    RESTARTS   AGE
emqx-67b5fcf4d-gwzfn       1/1     Running   0          36s
emqx-67b5fcf4d-rb7m6       1/1     Running   0          36s
```

集群成功

```
$ kubectl exec emqx-67b5fcf4d-gwzfn /opt/emqx/bin/emqx_ctl cluster statusCluster status: [{running_nodes,['emqx@10.42.1.24','emqx@10.42.2.19']}]
```

### 使用Rancher Dashboard部署EMQ X（可选）

删除刚刚部署的EMQ X

```
$ kubectl delete -f emqx.yamlsecret "emqx-secret" deleted
service "emqx" deleted
deployment.extensions "emqx" deleted
```

进入Rancher集群工作负载页面，点击导入YAML
![WX20190803103410.png](https://static.emqx.net/images/5e6b487393e0158e11a8bc74eced512f.png)

在导入页面将emqx.yaml文件的内容复制进去!
![WX20190803103628.png](https://static.emqx.net/images/19c6ea1d29b7936b0e081002a943ac71.png)

点击导入，等待导入成功。
