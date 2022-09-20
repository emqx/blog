Helm 在 2019 年 11 月发布了 Helm3 , Helm3 相比于 Helm2 增加了不少新特性, 本文介绍如何通过 Helm3 在 Kubernetes 上部署 EMQX 集群.

## Helm3 新特性

- 移除了 Tiller
- 不同的 namespace 可以使用相同的 Release Name
- 简化模板对象 `.Capabilities`
- 使用 `JSONSchema` 验证 charts 的 Values
- 将 `requirements.yaml `合并到 `Chart.yaml` 中
- helm install 时需要指定 Release Name，开启自动生成需要 `--generate-name` 参数
- 支持 push 到远端 registry （如：harbor）
- 移除 helm serve
- 命令行变化（将原先的命令保留为别名 Aliases）
  - `helm delete` --> `helm uninstall`
  - `helm inspect` -> `helm show`
  - `helm fetch` -> `helm pull`
- go 导入路径改变 `k8s.io/helm` --> `helm.sh/helm`

具体新特性可以参考 [Helm 官方文档](https://helm.sh/docs/faq/#changes-since-helm-2)

## Install Helm3

Helm3 提供了官方脚本简化了安装步骤, 可以执行 `curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash` 一键安装, 或者查看 [Helm 官方文档](https://helm.sh/docs/intro/install/) 的详细说明

## 快速部署一个简单的 EMQX 集群

+ 添加 helm 仓库

  ```
  $ helm repo add emqx https://repos.emqx.io/charts
  $ helm repo update
  ```

+ 查询 EMQX

  ```
  helm search repo emqx
  NAME       	 CHART VERSION	APP VERSION	DESCRIPTION
  emqx/emqx  	 v4.0.0       	v4.0.0     	A Helm chart for EMQX
  emqx/emqx-ee v4.0.0       	v4.0.0     	A Helm chart for EMQX
  emqx/kuiper	 0.1.1        	0.1.1      	A lightweight IoT edge analytic software
  ```

+ 启动 EMQX 集群，设置 `service.type=NodePort`

  ```
  $ helm install my-emqx emqx/emqx --set service.type=NodePort
  ```

+ 查看 EMQX 集群情况

  ```
  $ kubectl get pods
  NAME       READY  STATUS             RESTARTS  AGE
  my-emqx-0  1/1     Running   0          56s
  my-emqx-1  1/1     Running   0          40s
  my-emqx-2  1/1     Running   0          21s
  
  $ kubectl exec -it my-emqx-0 -- emqx_ctl cluster status
  Cluster status: #{running_nodes =>
                        ['my-emqx@my-emqx-0.my-emqx-headless.default.svc.cluster.local',
                         'my-emqx@my-emqx-1.my-emqx-headless.default.svc.cluster.local',
                         'my-emqx@my-emqx-2.my-emqx-headless.default.svc.cluster.local'],
                    stopped_nodes => []}
  ```

+ 查看 EMQX service 

  ```
  $ kubectl get svc
  NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                                                                                      AGE
  my-emqx              NodePort       10.101.143.92    <none>        1883:32756/TCP,8883:31569/TCP,8081:30585/TCP,8083:31804/TCP,8084:30523/TCP,18083:31253/TCP   4m33s
  my-emqx-headless     ClusterIP      None             <none>        1883/TCP,8883/TCP,8081/TCP,8083/TCP,8084/TCP,18083/TCP                                       4m33s
  ```

可以看到 `my-emqx` 的 18083 端口对应的宿主机 IP 是 31539。（NodePort 在每次部署的时候都会变化，以实际部署时为准。）

+ 访问 Kubernetes 的任意一台节点 IP 的 31539 端口，输入默认用户名：admin，默认密码：public，登陆 EMQX dashboard。 

+ 删除 EMQX 集群

  ```
  $ helm uninstall my-emqx
  release "my-emqx" uninstalled
  ```

## 部署一个持久化的 EMQX 集群

EMQX 通过 创建 PVC 资源挂载 `/opt/emqx/data/mnesia` 目录实现持久化 `pods`，**在部署 EMQX 之前，用户需要部署 [Haproxy](https://www.emqx.com/zh/blog/emqx-haproxy) 或 Nginx-PLUS 等负载均衡器，并自行在 Kubernetes 中创建 PVC 资源或是 Storage Classes 资源**

+ 启动 EMQX 集群

  + 如果用户部署了 PVC 资源，那么设置 `persistence.existingClaim=your_pv_name`

    ```
    $ helm install my-emqx emqx/emqx --set persistence.enabled=true --set persistence.existingClaim=your_pv_name
    ```

  + 如果用户部署了 Storage Classes 资源，那么设置`persistence.storageClass=your_storageClass_name`

    ```
    $ helm install my-emqx emqx/emqx --set persistence.enabled=true --set persistence.storageClass=your_storageClass_name
    ```

+ 查看 EMQX 集群情况

  ```
  $ kubectl get pods
  NAME       READY  STATUS             RESTARTS  AGE
  my-emqx-0  1/1     Running   0          56s
  my-emqx-1  1/1     Running   0          40s
  my-emqx-2  1/1     Running   0          21s
  
  $ kubectl exec -it my-emqx-0 -- emqx_ctl cluster status
  Cluster status: #{running_nodes =>
                        ['my-emqx@my-emqx-0.my-emqx-headless.default.svc.cluster.local',
                         'my-emqx@my-emqx-1.my-emqx-headless.default.svc.cluster.local',
                         'my-emqx@my-emqx-2.my-emqx-headless.default.svc.cluster.local'],
                    stopped_nodes => []}
  ```

+ 以 Storage Classes 为例，可以看到 PVC 资源已经成功的建立

  ```
  $ kubectl get pvc
  NAME                  STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
  emqx-data-my-emqx-0   Bound     pvc-8094cd75-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            2m11s
  emqx-data-my-emqx-1   Bound     pvc-9325441d-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            99s
  emqx-data-my-emqx-2   Bound     pvc-ad425e9d-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            56s
  ```

  集群会将 EMQX 的 `/opt/emqx/data/mnesia` 目录挂载到 PVC 中，当 Pods 被重新调度之后，EMQX 会从 `/opt/emqx/data/mnesia` 目录中获取数据并恢复

+ 查看 EMQX 的 ClusterIP

  ```
  $ kubectl get svc
  NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                                                  AGE
  my-emqx              ClusterIP   10.100.205.13   <none>        1883/TCP,8883/TCP,8081/TCP,8083/TCP,8084/TCP,18083/TCP   26m
  my-emqx-headless     ClusterIP   None            <none>        1883/TCP,8883/TCP,8081/TCP,8083/TCP,8084/TCP,18083/TCP   26m
  ```

可以看到 `my-emqx` 的 ClusterIP 为 `10.100.205.13` （ClusterIP 在每次部署的时候都会变化，以实际部署时为准。）

+ 将负载均衡监听的 URL 的 1883、8883、8081、8083、8084、18083 端口转发到 `my-emqx` 的 ClusterIP，如果有 TLS 连接的需要，推荐在负载均衡器终结 SSL 连接。客户端与负载均衡器之间 TLS 安全连接，LB 与 EMQX 之间普通 TCP 连接。

+ 访问 `URL:18083`，输入默认用户名：admin，默认密码：public，登陆 EMQX dashboard。 

+ 使用 `helm upgrade` 命令可以轻松扩展 EMQX 集群，下面以增加 EMQX 节点为例展示 `helm upgrade` 命令

  ```
  # 将 EMQX 的节点数量变更为5个
  # 注意：EMQX 的节点数量建议为单数
  $ helm upgrade --set replicaCount=5 my-emqx emqx/emqx
  Release "my-emqx" has been upgraded. Happy Helming!
  ```

```
  $ kubectl get pods
  NAME       READY  STATUS             RESTARTS  AGE
  my-emqx-0  1/1    Running            0         4m25s
  my-emqx-1  1/1    Running            0         4m14s
  my-emqx-2  1/1    Running            0         4m
  my-emqx-3  1/1    Running            0         31s
  my-emqx-4  1/1    Running            0         15s

  $ kubectl exec -it my-emqx-0 -- emqx_ctl cluster status
  Cluster status: #{running_nodes =>
                        ['my-emqx@my-emqx-0.my-emqx-headless.default.svc.cluster.local',
                         'my-emqx@my-emqx-1.my-emqx-headless.default.svc.cluster.local',
                         'my-emqx@my-emqx-2.my-emqx-headless.default.svc.cluster.local',
                         'my-emqx@my-emqx-3.my-emqx-headless.default.svc.cluster.local',
                         'my-emqx@my-emqx-4.my-emqx-headless.default.svc.cluster.local'],
                    stopped_nodes => []}

```

+ 删除 EMQX 集群

  ```
  $ helm uninstall my-emqx
  release "my-emqx" uninstalled
  ```

  

**注意：**EMQX 集群删除掉之后 PVC 资源不会自动释放掉，以便恢复 EMQX，确认不需要恢复后需要手动删除 PVC 资源

```
  $ kubectl get pvc
  NAME                  STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
  emqx-data-my-emqx-0   Bound     pvc-8094cd75-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            84m
  emqx-data-my-emqx-1   Bound     pvc-9325441d-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            84m
  emqx-data-my-emqx-2   Bound     pvc-ad425e9d-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            83m
  emqx-data-my-emqx-3   Bound     pvc-b6c5a565-adbd-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            25m
  emqx-data-my-emqx-4   Bound     pvc-c626cafd-adbd-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            25m

  $ kubectl delete pvc emqx-data-my-emqx-0 emqx-data-my-emqx-1 emqx-data-my-emqx-2 emqx-data-my-emqx-3 emqx-data-my-emqx-4                    
  persistentvolumeclaim "emqx-data-my-emqx-0" deleted
  persistentvolumeclaim "emqx-data-my-emqx-1" deleted
  persistentvolumeclaim "emqx-data-my-emqx-2" deleted
  persistentvolumeclaim "emqx-data-my-emqx-3" deleted
  persistentvolumeclaim "emqx-data-my-emqx-4" deleted
```

## 部署 EMQX Edge 集群和 EMQX 企业版集群

### EMQX Edge

部署 EMQX Edge 集群指定 `image.repository=emqx/emqx-edge`，其他设置与部署 EMQX 集群保持一致

  ```
$ helm install my-emqx-edge emqx/emqx --set image.repository=emqx/emqx
$ kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
my-emqx-edge-0  1/1     Running   0          35s
my-emqx-edge-1  1/1     Running   0          23s
my-emqx-edge-2  1/1     Running   0          9s
  ```

### EMQX EE

部署 [EMQX 企业版](https://www.emqx.com/zh/products/emqx)集群首先需要前往 [www.emqx.com](https://www.emqx.com/zh/apply-licenses/emqx) 申请并下载 License 文件，并将 License 文件创建为 Secret 资源

```
$ kubectl create secret generic your-license-secret-name --from-file=/path/to/emqx.lic
```

然后在部署时指定 repo 为 `emqx/emqx-ee `, `emqxLicneseSecretName=your-license-secret-name`, 其他设置与部署 EMQX 集群保持一致

```
$ helm install my-emqx-ee emqx/emqx-ee emqxLicneseSecretName=your-license-secret-name
```

## EMQX Helm Chart 配置项

| 参数                        | 描述                                                         | Default Value |
| --------------------------- | ------------------------------------------------------------ | ------------- |
| `replicaCount`              | EMQX 节点数量，建议保持奇数个节点，不然脑裂后无法自动恢复   | 3             |
| `image.repository`          | EMQX 镜像名称                                               | emqx/emqx     |
| `image.pullPolicy`          | 获取镜像的策略                                               | IfNotPresent  |
| `persistence.enabled`       | 是否启用 PVC                                                 | false         |
| `persistence.storageClass`  | Storage class 名称                                           | `nil`         |
| `persistence.existingClaim` | PV 名称                                                      | ""            |
| `persistence.accessMode`    | PVC 访问模式                                                 | ReadWriteOnce |
| `persistence.size`          | PVC 容量                                                     | 20Mi          |
| `resources`                 | CPU/ 内存资源                                                | {}            |
| `nodeSelector`              | pod 分配的节点标签                                           | {}            |
| `tolerations`               |                                                              | []            |
| `affinity`                  |                                                              | {}            |
| `service.type`              | Emqx cluster service type                                    | ClusterIP     |
| `emqxConfig`                | EMQX 配置项，详情查看[文档](https://github.com/emqx/emqx-docker#emq-x-configuration) | {}            |
| `emqxLicneseSecretName`     | EMQX 企业版需要手动将 License 文件创建为 Secret 资源 (仅在 `emqx/emqx-e` 有效) | ""            |

当需要设置复杂参数的时候，可以使用 Yaml 文件来记录参数

```
$ helm install my-emqx emqx/emqx -f values.yaml 
```

> 你可以从 [Github](https://github.com/emqx/emqx-rel) 获取默认的 [`values.yaml`](https://raw.githubusercontent.com/emqx/emqx-rel/v4.0.0/deploy/charts/emqx/values.yaml)


<section class="promotion">
    <div>
        免费试用 EMQX Cloud
        <div class="is-size-14 is-text-normal has-text-weight-normal">全托管的云原生 MQTT 消息服务</div>
    </div>
    <a href="https://accounts-zh.emqx.com/signup?continue=https://cloud.emqx.com/console/deployments/0?oper=new" class="button is-gradient px-5">开始试用 →</a>
</section>
