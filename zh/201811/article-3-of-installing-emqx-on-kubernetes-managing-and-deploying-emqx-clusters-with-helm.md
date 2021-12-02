## Helm 介绍

Helm 是管理 Kubernetes 包的工具，Helm 能提供下面的能力：

- 创建新的 charts
- 将 charts 打包成 tgz 文件
- 与 chart 仓库交互
- 安装和卸载 Kubernetes 的应用
- 管理使用 Helm 安装的 charts 的生命周期

在 Helm 中，有三个需要了解的重要概念：

- chart：是创建Kubernetes应用实例的信息集合；
- config：创建发布对象的chart的配置信息
- release：chart的运行实例，包含特定的config

## Helm 组件

在 Helm 中有两个主要的组件，既 Helm 客户端和 Tiller 服务器：

**Helm 客户端**：这是一个供终端用户使用的命令行工具，客户端负责如下的工作：

- 本地 chart 开发
- 管理仓库
- 与 Tiller 服务器交互
- - 发送需要被安装的 charts
  - 请求关于发布版本的信息
  - 请求更新或者卸载已安装的发布版本

**Tiller 服务器**： Tiller 服务部署在 Kubernetes 集群中，Helm 客户端通过与 Tiller 服务器进行交互，并最终与 Kubernetes API 服务器进行交互。 Tiller 服务器负责如下的工作：

- 监听来自于 Helm 客户端的请求
- 组合 chart 和配置来构建一个发布
- 在 Kubernetes 中安装，并跟踪后续的发布
- 通过与 Kubernetes 交互，更新或者 chart

客户端负责管理 chart，服务器发展管理发布。

## Helm技术实现

Helm 客户端是使用 Go 语言编写的，它通过 gRPC 协议与 Tiller 服务器交互。

Tiller 服务器也是使用 Go 语言编写的，它使用 Kubernetes 客户端类库（当前是那个 REST+JSON ）与 Kubernetes 进行通讯。

Tiller 服务器通过 Kubernetes 的 ConfigMap 存储信息，因此本身没有用于存储数据库。

## Helm 安装部署

### 安装 Helm 客户端

在进行 Helm 客户端安装前，请确认已有可用的 Kubernetes 集群环境，并已安装了 `kubectl`。

通过访问：https://github.com/kubernetes/helm/releases。
下载 Helm 的合适的版本。

1. 此文下载 `helm-v2.8.0-linux-amd64.tgz` 版本；
2. 解压缩文件：`tar -zxvf helm-v2.8.0-linux-amd64.tgz`
3. 将解压缩后的 helm 移至`/usr/local/bin` 目录下：`mv linux-amd64/helm /usr/local/bin/helm`

**注意**：

- 最好在安装`kubectl`命令行工具的机器上安装Helm客户端；或者将安装`kubectl` 命令行工具生成的配置文件（`$HOME/.kube/config`）复制到 Helm 客户端所安装的机器上( `$HOME/.kube/config` )。

### 安装 Tiller 服务器

#### 使用 Service Account 安装

1. 创建一个名为 tiller 的 Service Account

   ```
   $ kubectl create serviceaccount tiller --namespace kube-system
   ```

2. 授予名为 tiller 的 Service Account 集群管理员角色 `cluster-admin`:

3. - 将 tiller 绑定至集群管理员角色的的 yaml 文件如下所示：

     ```
     $vim rbac-config.yaml
     
     apiVersion: rbac.authorization.k8s.io/v1beta1 
     kind: ClusterRoleBinding 
     metadata: 
     name: tiller 
     roleRef: 
     apiGroup: rbac.authorization.k8s.io 
     kind: ClusterRole 
     name: cluster-admin 
     subjects: 
     - kind: ServiceAccount 
     name: tiller 
     namespace: kube-system
     ```

   - 通过执行 `kubectl create -f`将授予 tiller 集群管理员角色：

     ```
     $ kubectl create -f rbac-config.yaml
     ```

4. 安装 Tiller 服务器

   ```
   $ helm init --service-account tiller
   ```

### 验证安装

在安装完成后，可以通过执行如下命令来检查是安装成功：

```
$ helm version
```

如果正确显示 Helm 客户端和 Tiller 服务器的版本，这表示安装成功。

或者通过执行 `kubectl` 的如下命令来查看是否已正常按照 Tiller 服务器：

```
$ kubectl get pods -n kube-system
```

## Helm 使用

### 常用命令

#### 查看源

```
helm repo list    #列出所有源，当前还没有添加源# 添加一个国内可以访问的阿里源，不过好像最近不更新了helm repo add ali https://kubernetes.oss-cn-hangzhou.aliyuncs.com/charts  如果能连外网，可以加google，f8
helm repo add google https://kubernetes-charts.storage.googleapis.com helm repo add fabric8 https://fabric8.io/helm# 更新源helm repo update
```

#### 查看 chart

```
# 查看chart，即已经通过helm部署到 k8s 平台的应用helm list    或者  helm ls# 若要查看或搜索存储库中的 Helm charts，键入以下任一命令helm search 
helm search 存储库名称 #如 stable 或 incubatorhelm search chart名称 #如 wordpress 或 spark# 查看charm详情helm inspect ali/wordpress
```

#### 下载 chart

```
helm fetch ali/wordpress
[ubuntu@master1 ~]# ls wordpress-0.8.8.tgz wordpress-0.8.8.tgz
```

#### 部署应用 wordpress， 通过 ali 源文件

```
$ helm install --name wordpress-test --set "persistence.enabled=false,mariadb.persistence.enabled=false" ali/wordpress

[ubuntu@master1 ~]# kubectl get pod NAME                                        READY     STATUS    RESTARTS   AGE
wordpress-test-mariadb-84b866bf95-7bx5w     1/1       Running   1          4h
wordpress-test-wordpress-5ff8c64b6c-hrh9q   1/1       Running   0          4h
[ubuntu@master1 ~]# kubectl get svc NAME                       TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)                      AGE
kubernetes                 ClusterIP      10.96.0.1        <none>        443/TCP                      2d
wordpress-test-mariadb     ClusterIP      10.105.71.95     <none>        3306/TCP                     4h
wordpress-test-wordpress   LoadBalancer   10.104.106.150   <pending>     80:30655/TCP,443:32121/TCP   4h
```

#### 访问 wordpress，使用 node 节点 ip + nodeport， 192.168.1.181:30655

#### 删除应用

```
[ubuntu@master1 ~]# helm listNAME            REVISION    UPDATED                     STATUS      CHART           NAMESPACEwordpress-test  1           Thu May 17 11:35:07 2018    DEPLOYED    wordpress-0.8.8 default  [ubuntu@master1 ~]# helm delete wordpress-testrelease "wordpress-test" deleted
```

## 建立自己的 chart

创建一个自己的chart，看下文档结构，学习下如何使用

```
$ helm create emqx
Creating emqx
$ tree misa86
emqx
├── charts     #Chart本身的版本和配置信息├── Chart.yaml    #Chart本身的版本和配置信息├── templates    #配置模板目录│   ├── deployment.yaml    #kubernetes Deployment object│   ├── _helpers.tpl    #用于修改kubernetes objcet配置的模板│   ├── ingress.yaml    #kubernetes Deployment object│   ├── NOTES.txt    #helm提示信息│   └── service.yaml    #kubernetes Serivce└── values.yaml    #kubernetes object configuration，定义变量
```

### 模板 template

template 下包含应用所有的 yaml 文件模板，应用资源的类型不仅限于 deployment 和 service 这些，k8s 支持的都可以。

```
$cat templates/deployment.yaml

apiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: {{ include "emqx.fullname" . }}
  labels:
    app.kubernetes.io/name: {{ include "emqx.name" . }}
    helm.sh/chart: {{ include "emqx.chart" . }}
    app.kubernetes.io/instance: {{ .Release.Name }}
    app.kubernetes.io/managed-by: {{ .Release.Service }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ include "emqx.name" . }}
      app.kubernetes.io/instance: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ include "emqx.name" . }}
        app.kubernetes.io/instance: {{ .Release.Name }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
          - containerPort: 1883
          - containerPort: 8883
          - containerPort: 8080
          - containerPort: 8083
          - containerPort: 8084
          - containerPort: 18083
          env:
          - name: EMQX_NAME
            value: emqx
          - name: EMQX_CLUSTER__K8S__APP_NAME
            value: emqx
          - name: EMQX_CLUSTER__DISCOVERY
            value: k8s
          - name: EMQX_CLUSTER__K8S__SERVICE_NAME
            value: {{ include "emqx.fullname" . }}
          - name: EMQX_CLUSTER__K8S__APISERVER
            value: {{ .Values.env.kubeApiserver }}
          - name: EMQX_CLUSTER__K8S__NAMESPACE
            value: {{ .Values.env.kubeNamespace }}
          - name: EMQX_CLUSTER__K8S__ADDRESS_TYPE
            value: {{ .Values.env.kubeAddressType }}
          - name: EMQX_CLUSTER__K8S__APP_NAME
            value: emqx
          tty: true
```

这是该应用的 Deploymen t的 yaml 配置文件，其中的双大括号包扩起来的部分是 Go template， template "emqx.name" 这类是在 `_helpers.tpl` 文件中定义的，如果不定义，将来文件名会是随意字符加 chart 名字。

其中的 Values 是在 values.yaml 文件中定义的，应用主要的参数在这边：

```
$ cat values.yaml# Default values for emqx.# This is a YAML-formatted file.# Declare variables to be passed into your templates.replicaCount: 2image:
  repository: emqx/emqx
  tag: latest
  pullPolicy: IfNotPresent

env:
  kubeApiserver: http://127.0.0.1:8080
  kubeNamespace: default
  kubeAddressType: ip

service:
  type: ClusterIP
  mqttPort: 1883
  mqttsslPort: 8883
  mgmtPort: 8080
  webscoketPort:8083
  wssPort:8084
  dashboardPort: 18083ingress:
  enabled: false
  annotations: {}    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  path: /
  hosts:
    - chart-example.local
  tls: []  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local
```

比如在 Deployment.yaml 中定义的容器镜像 image:

```
{{ .Values.image.repository }}:{{ .Values.image.tag }}
```

其中的：

```
.Values.image.repository就是emqx/emqx
.Values.image.tag就是latest
```

以上两个变量值是在 install chart 的时候自动生成的默认值。

### 检查配置和模板是否有效

当使用 kubernetes 部署应用的时候实际上将 templates 渲染成最终的 kubernetes 能够识别的 yaml 格式。

使用`helm install --dry-run --debug <chart_dir>`命令来验证 chart 配置。该输出中包含了模板的变量配置与最终渲染的 yaml 文件。 deployment service 的名字前半截由两个随机的单词组成，随机数加 chart 名。这名字也可以改成 value 方式，自己定义如果配置等有问题此处会报错。

```
helm install --set env.kubeApiserver=http://172.31.31.241:8080 --dry-run --debug .[debug] Created tunnel using local port: '43251'[debug] SERVER: "127.0.0.1:43251"[debug] Original chart version: ""[debug] CHART PATH: /home/ubuntu/emqx-helm

NAME:   quelling-toad
REVISION: 1RELEASED: Tue Oct 30 08:18:09 2018CHART: emqx-helm-v1.0USER-SUPPLIED VALUES:
env:
  kubeApiserver: http://172.31.31.241:8080COMPUTED VALUES:
env:
  kubeAddressType: ip
  kubeApiserver: http://172.31.31.241:8080
  kubeNamespace: defaultimage:
  pullPolicy: IfNotPresent
  tag: latest
ingress:
  annotations: {}
  enabled: false
  hosts:
  - chart-example.local
  path: /
  tls: []
replicaCount: 2service:
  dashboardPort: 18083
  mappingPort: 4369
  mgmtPort: 8080
  mqttPort: 1883
  mqttsslPort: 8883
  type: ClusterIP

HOOKS:
MANIFEST:

---# Source: emqx-helm/templates/service.yamlapiVersion: v1
kind: Service
metadata:
  name: quelling-toad-emqx-helm
  labels:
    app.kubernetes.io/name: emqx-helm
    helm.sh/chart: emqx-helm-v1.0
    app.kubernetes.io/instance: quelling-toad
    app.kubernetes.io/managed-by: Tiller
spec:
  type: ClusterIP
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
    port: 8080
    protocol: TCP
    targetPort: 8080
  - name: webscoket
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
  selector:
    app.kubernetes.io/name: emqx-helm
    app.kubernetes.io/instance: quelling-toad
---# Source: emqx-helm/templates/deployment.yamlapiVersion: apps/v1beta2
kind: Deployment
metadata:
  name: quelling-toad-emqx-helm
  labels:
    app.kubernetes.io/name: emqx-helm
    helm.sh/chart: emqx-helm-v1.0
    app.kubernetes.io/instance: quelling-toad
    app.kubernetes.io/managed-by: Tiller
spec:
  replicas: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: emqx-helm
      app.kubernetes.io/instance: quelling-toad
  template:
    metadata:
      labels:
        app.kubernetes.io/name: emqx-helm
        app.kubernetes.io/instance: quelling-toad
    spec:
      containers:
        - name: emqx-helm
          image: "emqx/emqx:latest"
          imagePullPolicy: IfNotPresent
          ports:
          - containerPort: 1883
          - containerPort: 8883
          - containerPort: 8080
          - containerPort: 8083
          - containerPort: 8084
          - containerPort: 18083
          env:
          - name: EMQX_NAME
            value: emqx
          - name: EMQX_CLUSTER__K8S__APP_NAME
            value: emqx
          - name: EMQX_CLUSTER__DISCOVERY
            value: k8s
          - name: EMQX_CLUSTER__K8S__SERVICE_NAME
            value: quelling-toad-emqx-helm
          - name: EMQX_CLUSTER__K8S__APISERVER
            value: http://172.31.31.241:8080
          - name: EMQX_CLUSTER__K8S__NAMESPACE
            value: default
          - name: EMQX_CLUSTER__K8S__ADDRESS_TYPE
            value: ip
          - name: EMQX_CLUSTER__K8S__APP_NAME
            value: emqx
          tty: true

```

### 部署到 kubernetes

在 EMQ X 目录下执行下面的命令将应用部署到 kubernetes 集群上。

```
$ helm install --set env.kubeApiserver=http://172.31.31.241:8080 .NAME:   ugly-bumblebee
LAST DEPLOYED: Tue Oct 30 08:19:17 2018NAMESPACE: defaultSTATUS: DEPLOYED

RESOURCES:
==> v1/Service
NAME                      AGE
ugly-bumblebee-emqx-helm  0s

==> v1beta2/Deployment
ugly-bumblebee-emqx-helm  0s

==> v1/Pod(related)

NAME                                       READY  STATUS             RESTARTS  AGE
ugly-bumblebee-emqx-helm-5bc599849f-n4htc  0/1    ContainerCreating  0         0s
ugly-bumblebee-emqx-helm-5bc599849f-xwdn7  0/1    ContainerCreating  0         0s


NOTES:1. Get the application URL by running these commands:  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=emqx-helm,app.kubernetes.io/instance=ugly-bumblebee" -o jsonpath="{.items[0].metadata.name}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl port-forward $POD_NAME 8080:80

```

### 查看部署的 relaese

```
$ helm listNAME            REVISION    UPDATED                     STATUS      CHART           APP VERSION NAMESPACE
ugly-bumblebee  1           Tue Oct 30 08:19:17 2018    DEPLOYED    emqx-helm-v1.0  v1.0        default$ helm delete ugly-bumblebee
release "ugly-bumblebee" deleted

```

### 打包分享

我们可以修改 Chart.yaml 中的 helm chart 配置信息，然后使用下列命令将 chart 打包成一个压缩文件。

```
$ helm package .
Successfully packaged chart and saved it to: /home/ubuntu/emqx/emqx-v1.0.tgz

```

## Chart Repository

chart 库是带有一个 index.yaml 文件和任意个打包 chart 的 HTTP 服务器。当准备好分享 chart 时，首选方法是将其上传到 chart 库。

由于 chart 库可以是任何可以提供 YAML 和 tar 文件并可以回答 GET 请求的 HTTP 服务器，因此当托管自己的 chart 库时，很多选择。例如，可以使用 Google 云端存储（GCS）存储桶，Amazon S3 存储桶，Github Pages，甚至可以创建自己的 Web 服务器。

### 创建 chart 库

#### chart 库结构

chart 库由打包的 chart 和一个名为的特殊文件组成， index.yaml 其中包含 chart 库中所有 chart 的索引。通常，index.yaml 描述的 chart 也是托管在同一台服务器上，源代码文件也是如此。

例如，chart 库的布局 https://example.com/charts 可能如下所示：

```
charts/  |
  |- index.yaml  |
  |- alpine-0.1.2.tgz  |
  |- alpine-0.1.2.tgz.prov

```

这种情况下，索引文件包含有关一个 chart（Alpine chart）的信息，并提供该 chart 的下载 URL https://example.com/charts/alpine-0.1.2.tgz。

不要求 chart 包与 index.yaml 文件位于同一台服务器上 。但是，放在一起这样做通常是最简单的。

#### 索引文件

索引文件是一个叫做 yaml 文件 index.yaml。它包含一些关于包的元数据，包括 chart 的 Chart.yaml 文件的内容。一个有效的 chart 库必须有一个索引文件。索引文件包含有关 chart 库中每个 chart 的信息。helm repo index 命令将根据包含打包的 chart 的给定本地目录生成索引文件。

下面一个索引文件的例子：

```
apiVersion: v1
entries:
  alpine:
    - created: 2016-10-06T16:23:20.499814565-06:00
      description: Deploy a basic Alpine Linux pod
      digest: 99c76e403d752c84ead610644d4b1c2f2b453a74b921f422b9dcb8a7c8b559cd
      home: https://k8s.io/helm
      name: alpine
      sources:
      - https://github.com/kubernetes/helm
      urls:
      - https://technosophos.github.io/tscharts/alpine-0.2.0.tgz
      version: 0.2.0
    - created: 2016-10-06T16:23:20.499543808-06:00
      description: Deploy a basic Alpine Linux pod
      digest: 515c58e5f79d8b2913a10cb400ebb6fa9c77fe813287afbacf1a0b897cd78727
      home: https://k8s.io/helm
      name: alpine
      sources:
      - https://github.com/kubernetes/helm
      urls:
      - https://technosophos.github.io/tscharts/alpine-0.1.0.tgz
      version: 0.1.0
  nginx:
    - created: 2016-10-06T16:23:20.499543808-06:00
      description: Create a basic nginx HTTP server
      digest: aaff4545f79d8b2913a10cb400ebb6fa9c77fe813287afbacf1a0b897cdffffff
      home: https://k8s.io/helm
      name: nginx
      sources:
      - https://github.com/kubernetes/charts
      urls:
      - https://technosophos.github.io/tscharts/nginx-1.1.0.tgz
      version: 1.1.0generated: 2016-10-06T16:23:20.499029981-06:00

```

生成的索引和包可以从基本的网络服务器提供。可以使用 helm serve 启动本地服务器，在本地测试所有内容。

```
$ helm serve --repo-path ./charts
Regenerating index. This may take a moment.
Now serving you on 127.0.0.1:8879

```

### 托管 chart 库

要配置普通 Web 服务器来服务 Helm chart，只需执行以下操作：

- 将索引和 chart 置于服务器目录中
- 确保 index.yaml 可以在没有认证要求的情况下访问
- 确保 yaml 文件的正确内容类型（text/yaml 或 text/x-yaml）

例如，如果想在 $WEBROOT/charts 以外的目录为 chart 提供服务，请确保 Web 根目录中有一个 charts/ 目录，并将索引文件和 chart 放入该文件夹内。

### 管理 chart 库

#### 将 chart 存储在 chart 库中

现在已有一个 chart 存储库，让我们上传一个 chart 和一个索引文件到存储库。chart 库中的 chart 必须正确打包（helm package chart-name/）和版本（遵循 SemVer 2 标准）。

接下来的这些步骤是一个示例工作流程，也可以用你喜欢的任何工作流程来存储和更新 chart 库中的 chart。

准备好打包 chart 后，创建一个新目录，并将打包 chart 移动到该目录。

```
$ helm package .
$ mkdir emqx-charts
$ mv emqx-0.1.0.tgz emqx-charts/
$ helm repo index emqx-charts --url  https://example.com/charts

```

最后一条命令采用刚创建的本地目录的路径和远程 chart 库的 URL，并在给定的目录路径中生成 index.yaml。

现在可以使用同步工具或手动将 chart 和索引文件上传到 chart 库。如果使用 Google 云端存储，请使用 gsutil 客户端查看此示例工作流程。对于 GitHub，可以简单地将 chart 放入适当的目标分支中。

#### 新添加 chart 添加到现有存储库

每次将新 chart 添加到存储库时，都必须重新生成索引。helm repo index 命令将 index.yaml 从头开始完全重建该文件，但仅包括它在本地找到的 chart。

可以使用 --merge 标志向现有 index.yaml 文件增量添加新 chart（在使用远程存储库（如 GCS）时，这是一个很好的选择）。运行 helm repo index --help 以了解更多信息，

确保上传修改后的 index.yaml 文件和 chart。如果生成了出处 provenance 文件，也要上传。

#### 与他人分享 chart

准备好分享 chart 时，只需让别人知道存储库的 URL 是什么就可以了。

他们将通过 `helm repo add [NAME] [URL]` 命令将仓库添加到他们的 helm 客户端，并可以起一个带有任何想用来引用仓库的名字。

```
$ helm repo add emqx-charts https://example.com/charts
$ helm repo list
emqx-charts    https://example.com/charts

```

如果 chart 由 HTTP 基本认证支持，也可以在此处提供用户名和密码：

```
$ helm repo add emqx-charts https://example.com/charts --username my-username --password my-password
$ helm repo list
emqx-charts    https://example.com/charts

```

**注意**： 如果存储库不包含有效信息库 index.yaml 文件，则添加不会成功。

之后，用户将能够搜索 chart。更新存储库后，他们可以使用该 helm repo update 命令获取最新的 chart 信息。

原理是helm repo add和helm repo update命令获取index.yaml文件并将它们存储在 $HELM_HOME/repository/cache/目录中。这是helm search 找到有关chart的信息的地方。

## 参考资料

- Chart Repository 存储库指南
- 使用 Helm 管理 kubernetes 应用
- Kunbernetes -容器云应用的安装部署工具 Helm
