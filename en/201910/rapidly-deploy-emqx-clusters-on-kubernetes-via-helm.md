

Helm3 was released in November 2019, which adds many new features compared to Helm2.In this article, how to deploy EMQ X cluster on Kubernetes via Helm3 will be introduced.

## New features of  Helm3 

-  Remove Tiller
-  Different namespaces can use the same Release Name
-  Simplify template object `.Capabilities`
-  Use `JSONSchema` to validate the values of charts
-  Merge `requirements.yaml` into ` Chart.yaml`
-  require to specify a Release Name when you install helm. require to use the --generate-name parameter to enable automatic generation.
-  Support pushing to remote registry (eg: harbor)
-  Remove helm serve
-  Command line changes (retain the original command as alias Aliases)
   - `helm delete` --> `helm uninstall`
   - `helm inspect` -> `helm show`
   - `helm fetch` -> `helm pull`
-  go Import path changes `k8s.io/helm` --> `helm.sh/helm`

For specific new features, you can refer to the  [Helm official document](https://helm.sh/docs/faq/#changes-since-helm-2)

## Install Helm3

We provide official scripts of Helm3 to simplify the installation steps, you can execute `curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3|bash` for one-click installation, or view the [Helm official documentation](https://helm.sh/docs/intro/install/)

+ Add helm repository

  ```
  $ helm repo add emqx https://repos.emqx.io/charts
  $ helm repo update
  ```

+ Check EMQ X

  ```
  helm search repo emqx
  NAME       	 CHART VERSION	APP VERSION	DESCRIPTION
  emqx/emqx  	 v4.0.0       	v4.0.0     	A Helm chart for EMQ X
  emqx/emqx-ee v4.0.0       	v4.0.0     	A Helm chart for EMQ X
  emqx/kuiper	 0.1.1        	0.1.1      	A lightweight IoT edge analytic software
  ```


+ Start EMQ X cluster and set`service.type=NodePort`

  ```
  $ helm install my-emqx emqx/emqx --set service.type=NodePort
  ```

+ Check the cluster status of EMQ X

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

+ Check  EMQ X service 

  ```
  $ kubectl get svc
  NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                                                                                      AGE
  my-emqx              NodePort       10.101.143.92    <none>        1883:32756/TCP,8883:31569/TCP,8081:30585/TCP,8083:31804/TCP,8084:30523/TCP,18083:31253/TCP   4m33s
  my-emqx-headless     ClusterIP      None             <none>        1883/TCP,8883/TCP,8081/TCP,8083/TCP,8084/TCP,18083/TCP                                       4m33s
  ```

It can be seen that the host IP corresponding to port 18083 of `my emqx` is 31253. (NodePort changes during each deployment, which is subject to the actual deployment.)

+ Access port 31253 of any Kubernetes node  IP, enter the default username: admin, default password: public, and log in to the EMQ X dashboard.

+ Delete EMQ X cluster.

  ```
  $ helm uninstall my-emqx
  release "my-emqx" uninstalled
  ```

## Deploy a persistent EMQ X cluster

EMQ X persists `pods` by creating a PVC resource mount`/opt/emqx/data/mnesia` directory. **Before deploying EMQ X, users need to deploy a load balancer such as Haproxy or Nginx-PLUS and Creating PVC resources or Storage Classes resources in Kubernetes.**

+ Start EMQ X cluster

  + If the user deployed a PVC resource, set `persistence.existingClaim=your_pv_name`

  ```
  $ helm install my-emqx emqx/emqx --set persistence.enabled=true --set persistence.existingClaim=your_pv_name
  ```

  + If the user deployed a Storage Classes resource, set`persistence.storageClass=your_storageClass_name`

    ```
    $ helm install my-emqx emqx/emqx --set persistence.enabled=true --set persistence.storageClass=your_storageClass_name
    ```

+ Check EMQ X cluster status

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

+ Taking Storage Classes as an example, you can see that the PVC resource has been successfully established

  ```
  $ kubectl get pvc
  NAME                  STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
  emqx-data-my-emqx-0   Bound     pvc-8094cd75-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            2m11s
  emqx-data-my-emqx-1   Bound     pvc-9325441d-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            99s
  emqx-data-my-emqx-2   Bound     pvc-ad425e9d-adb5-11e9-80cc-0697b59e8064   1Gi        RWO            gp2            56s
  ```

  The cluster will mount the  `/opt/emqx/data/mnesia` directory of EMQ X to the PVC. After the Pods are rescheduled, EMQ X will obtain data from the `/opt/emqx/data/mnesia` directory and restore it.

+ Check  ClusterIP of EMQ X

  ```
  $ kubectl get svc
  NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                                                  AGE
  my-emqx              ClusterIP   10.100.205.13   <none>        1883/TCP,8883/TCP,8081/TCP,8083/TCP,8084/TCP,18083/TCP   26m
  my-emqx-headless     ClusterIP   None            <none>        1883/TCP,8883/TCP,8081/TCP,8083/TCP,8084/TCP,18083/TCP   26m
  ```

You can see that the ClusterIP of `my-emqx` is` 10.100.205.13` (ClusterIP will change during each deployment, which is subject to the actual deployment)

+ Forward port 1883, 8883, 8081, 8083, 8084, 18083 of the URL monitored by the load balancer to the clusterIP of `my-emqx`. If there is a need for TLS connection, it is recommended to terminate the SSL connection at the load balancer. The connection between client and load balancer is a TLS secure connection, and the connection between LB and EMQ X is an ordinary TCP connection.

+ Access `URL:18083`, enter the default username: admin, default password: public, and log in to EMQ X dashboard.

+ Use the `helm upgrade` command to easily expand the EMQ X cluster. The following example shows the ` helm upgrade` command by adding an EMQ X node

  ```
  # Changed the number of nodes in EMQ X to 5.
  # Note: The number of nodes in EMQ X is recommended to be odd
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

+ Delete EMQ X cluster

  ```
  $ helm uninstall my-emqx
  release "my-emqx" uninstalled
  ```

  

**Note:** After the EMQ X cluster is deleted, the PVC resources will not be released automatically than  EMQ X can be  restored. You need to manually delete the PVC resources after confirming that you do not need to restore EMQ X.

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

## Deploy EMQ X Edge cluster and EMQ X  cluster of Enterprise Edition

#### EMQ X Edge

Specify `image.repository=emqx/emqx-edge` when deploying EMQ X Edge cluster, and other settings are consistent with the deployment of EMQ X cluster

  ```
$ helm install my-emqx-edge emqx/emqx --set image.repository=emqx/emqx
$ kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
my-emqx-edge-0  1/1     Running   0          35s
my-emqx-edge-1  1/1     Running   0          23s
my-emqx-edge-2  1/1     Running   0          9s
  ```

 #### EMQ X EE

When deploying an cluster of EMQ X Enterprise Edition, you need to log in to [emqx.io](https://www.emqx.com/en)  to apply and download a  License file at first, and create the  License file as a Secret resource

```
$ kubectl create secret generic your-license-secret-name --from-file=/path/to/emqx.lic
```

Then, specify the repo as `emqx/emqx-ee`,` emqxLicneseSecretName=your-license-secret-name` during deployment, and other settings are consistent with the deployment of EMQ X cluster

```
$ helm install my-emqx-ee emqx/emqx-ee --set emqxLicneseSecretName=your-license-secret-name
```

## EMQ X Helm Chart Configuration Item

| Parameter                   | Description                                                  | Default Value |
| --------------------------- | ------------------------------------------------------------ | ------------- |
| `replicaCount`              | For the number of EMQ X nodes, it is recommended to keep an odd number , otherwise it will not be able to recover automatically after brain splitting | 3             |
| `image.repository`          | EMQ X Image name                                             | emqx/emqx     |
| `image.pullPolicy`          | Pulling Image Policy                                         | IfNotPresent  |
| `persistence.enabled`       | Whether to enable PVC                                        | false         |
| `persistence.storageClass`  | Storage class Name                                           | `nil`         |
| `persistence.existingClaim` | PV Name                                                      | ""            |
| `persistence.accessMode`    | PVC access mode                                              | ReadWriteOnce |
| `persistence.size`          | PVC size                                                     | 20Mi          |
| `resources`                 | CPU/ memory resource                                         | {}            |
| `nodeSelector`              | pod assigned node labels                                     | {}            |
| `tolerations`               |                                                              | []            |
| `affinity`                  |                                                              | {}            |
| `service.type`              | Emqx cluster service type                                    | ClusterIP     |
| `emqxConfig`                | EMQ X Configuration item，see [documentation](https://github.com/emqx/emqx-docker#emq-x-configuration) for details | {}            |
| `emqxLicneseSecretName      | For EMQ X Enterprise Edition, it needs to manually create a Secret resource from a license file as (only valid in `emqx / emqx-e`) | ""            |

When you need to set complex parameters, you can use Yaml files to record the parameters

```
$ helm install my-emqx emqx/emqx -f values.yaml 
```

> You can get default [`values.yaml`](https://raw.githubusercontent.com/emqx/emqx-rel/v4.0.0/deploy/charts/emqx/values.yaml) from [Github](https://github.com/emqx/emqx-rel) .

