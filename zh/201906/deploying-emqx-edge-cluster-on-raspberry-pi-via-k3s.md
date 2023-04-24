## 环境

k3s需要raspberrypi可以正常访问google，如果没有条件的话推荐在AWS上尝试部署。

| Hostname    | IP            | 角色   | 硬件    |
| ----------- | ------------- | ------ | ------- |
| raspberrypi | 192.168.1.99  | server | 树莓派3 |
| emqx1       | 192.168.1.100 | agent  | 树莓派3 |
| emqx2       | 192.168.1.101 | agent  | 树莓派3 |

## 准备

### 在树莓派上部署k3s集群

**1.下载k3s，k3s支持x86_64，armhf和arm64，树莓派上应该安装armhf**

```
$ wget https://github.com/rancher/k3s/releases/download/v0.2.0/k3s-armhf
$ mv k3s-armhf /usr/local/bin/k3s
$ chmod +x /usr/local/bin/k3s
```

**2.启动Server**

```
$ sudo k3s server
```

**3.加入集群**

a.在Server节点上查看 `/var/lib/rancher/k3s/server/node-token` 获取node token

```
$ NODE_TOKEN=$(sudo cat /var/lib/rancher/k3s/server/node-token)
```

b.在agent节点上执行 `sudo k3s agent --server https://192.168.1.99:6443 --token ${NODE_TOKEN}` 加入k3s集群。

**4.（可选）外部设备使用 kubectl 管理 k3s集群**

a.选取任意能与集群通信并安装了`kubectl` 的外部设备

b.拷贝`/etc/rancher/k3s/k3s.yaml`文件到外部设备的 `~/.kube/config`

c.修改 `~/.kube/config`， 将 `https://localhost:6443` 替换为`https://192.168.1.99:6443`

d.使用 `kubectl` 管理集群

```
$ kubectl get nodes
NAME         STATUS  ROLES  AGE  VERSION
emqx2        Ready   <none>  29m  v1.13.4-k3s.1
emqx1         Ready   <none>  29m  v1.13.4-k3s.1
raspberrypi Ready   <none>  31m   v1.13.4-k3s.1
```



## 安装HELM

#### 安装helm客户端

- 通过访问：<https://github.com/kubernetes/helm/releases>。下载 Helm 的合适的版本。

  1.此文下载 `helm-v2.8.0-linux-amd64.tgz` 版本；

  2.解压缩文件：`tar -zxvf helm-v2.8.0-linux-amd64.tgz`

  3.将解压缩后的 helm 移至`/usr/local/bin` 目录下：`mv linux-amd64/helm /usr/local/bin/helm`

  **注意**：

  最好在安装`kubectl`命令行工具的机器上安装Helm客户端；或者将安装`kubectl` 命令行工具生成的配置文件（`$HOME/.kube/config`）复制到 Helm 客户端所安装的机器上( `$HOME/.kube/config` )。

  

#### 安装 Tiller 服务器

创建一个名为 tiller 的 Service Account

```
$ kubectl create serviceaccount tiller --namespace kube-system
```

授予名为 tiller 的 Service Account 集群管理员角色 `cluster-admin`:

- 将 tiller 绑定至集群管理员角色的的 yaml 文件如下所示：

```
$ cat <<EOF >rbac-config.yaml
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
EOF
```

- 通过执行 `kubectl create -f`将授予 tiller 集群管理员角色：

```
$ kubectl create -f rbac-config.yaml
```

安装 Tiller 服务器

```
$ helm init --service-account tiller
```

#### 验证安装

在安装完成后，可以通过执行如下命令来检查是安装成功：

```
$ helm version 
```

如果正确显示 Helm 客户端和 Tiller 服务器的版本，这表示安装成功。

或者通过执行 `kubectl` 的如下命令来查看是否已正常按照 Tiller 服务器：

```
$ kubectl get pods -n kube-system 
```

## 部署EMQX集群

**1.通过Helm部署EMQX**

```
$ git clone https://github.com/emqx/emqx-chart $ cd emqx-chart $ helm install --name myemqx --set deployment.image="emqx/emqx-edge:latest" . 
```

关于此仓库更多的设置，请查看README

**2.查看EMQX的集群状态**

a.查看pods列表

```
$ kubectl get pods |grep myemqx myemqx-emqx-chart-54974fc5f5-v8chq           1/1     Running   0          2m9s myemqx-emqx-chart-54974fc5f5-zz9gc           1/1     Running   0          2m9s 
```

b.使用`emqx_ctl cluster status`查看集群状态

```
$ kubectl exec myemqx-emqx-chart-54974fc5f5-v8chq /opt/emqx/bin/emqx_ctl cluster status Cluster status: [{running_nodes,['emqx@10.42.2.11','emqx@10.42.1.15']}]
```
